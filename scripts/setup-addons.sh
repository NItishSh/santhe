#!/bin/bash
set -e

# Source common functions
source "$(dirname "$0")/common.sh"

echo "🚀 Setting up Istio Addons and MetalLB..."

# 1. Install Istio Observability Stack
echo "📊 Installing Istio Observability Stack (Prometheus, Grafana, Jaeger, Kiali)..."
kubectl apply -f infrastructure/manifests/istio-addons/
check_status "Istio Addons Application"

# 1.b Install Loki (Log Aggregation)
echo "🪵  Installing Loki Stack (Loki + Promtail)..."
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install loki grafana/loki-stack \
  --namespace istio-system \
  --set grafana.enabled=false \
  --set prometheus.enabled=false \
  --set loki.isDefault=false \
  --set promtail.enabled=true
check_status "Loki Stack Installation"

# 2. Install MetalLB
echo "⚖️  Installing MetalLB LoadBalancer..."
kubectl apply -f infrastructure/manifests/metallb/metallb-native.yaml
check_status "MetalLB Installation"

# 3. Wait for MetalLB to be ready
echo "⏳ Waiting for MetalLB components to be ready..."
kubectl wait --namespace metallb-system \
  --for=condition=ready pod \
  --selector=app=metallb \
  --timeout=90s
check_status "MetalLB Readiness"

# 4. Configure MetalLB Address Pool
echo "📝 Configuring MetalLB Address Pool..."

# Get Kind Network CIDR and Calculate IP Range using Python
echo "ℹ️  Detecting Kind Network IPv4 Subnet..."
METALLB_IP_RANGE=$(docker network inspect kind | python3 -c "
import sys, json, ipaddress

try:
    data = json.load(sys.stdin)
    # Find IPv4 subnet (exclude IPv6 which contains ':')
    configs = data[0]['IPAM']['Config']
    subnet = next(c['Subnet'] for c in configs if ':' not in c['Subnet'])
    print(f'Subnet: {subnet}', file=sys.stderr)

    net = ipaddress.IPv4Network(subnet)
    # Use IPs at the very end of the range
    # e.g., for 172.18.0.0/16, end is 172.18.255.254
    # We take range end-50 to end-10
    total = net.num_addresses
    start_ip = net.network_address + total - 50
    end_ip = net.network_address + total - 10
    print(f'{start_ip}-{end_ip}')
except Exception as e:
    print(f'Error calculating range: {e}', file=sys.stderr)
    sys.exit(1)
")
check_status "IP Range Calculation"
echo "ℹ️  Calculated MetalLB IP Range: $METALLB_IP_RANGE"

# Generate Config
cat <<EOF > infrastructure/manifests/metallb-config.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - $METALLB_IP_RANGE
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
EOF

# Apply Config
kubectl apply -f infrastructure/manifests/metallb-config.yaml
check_status "MetalLB Configuration"

# 5. Patch Istio Ingress Gateway to use LoadBalancer
echo "🔌 Patching Istio Ingress Gateway to use LoadBalancer..."
kubectl patch svc istio-ingressgateway -n istio-system -p '{"spec": {"type": "LoadBalancer"}}'
check_status "Istio Ingress Gateway Patch"

echo "✅ Addons and LoadBalancer Setup Complete!"
echo "ℹ️  Istio Ingress IP: $(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
