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


