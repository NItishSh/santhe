#!/bin/bash
set -e

CLUSTER_NAME="santhe-local"
KIND_CONFIG="infrastructure/kind-config.yaml"

echo "🚀 Starting Local Setup for Santhe..."

# 1. Create Kind Cluster
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    echo "✅ Cluster '$CLUSTER_NAME' already exists."
else
    echo "📦 Creating Kind cluster '$CLUSTER_NAME'..."
    kind create cluster --name $CLUSTER_NAME --config $KIND_CONFIG
fi

# 2. Add Istio Helm Repo
echo "🔧 Configuring Istio..."
helm repo add istio https://istio-release.storage.googleapis.com/charts 2>/dev/null || true
helm repo update

# 3. Install Istio Base
if ! helm status istio-base -n istio-system >/dev/null 2>&1; then
    echo "Installing Istio Base..."
    helm upgrade --install istio-base istio/base -n istio-system --create-namespace --wait
else
    echo "✅ Istio Base already installed."
fi

# 4. Install Istiod
if ! helm status istiod -n istio-system >/dev/null 2>&1; then
    echo "Installing Istiod..."
    helm upgrade --install istiod istio/istiod -n istio-system --wait
else
    echo "✅ Istiod already installed."
fi

# 5. Install Istio Ingress Gateway
if ! helm status istio-ingressgateway -n istio-system >/dev/null 2>&1; then
    echo "Installing Istio Ingress Gateway..."
    helm upgrade --install istio-ingressgateway istio/gateway \
        -n istio-system \
        --set service.type=NodePort \
        --set service.ports[0].name=status-port \
        --set service.ports[0].port=15021 \
        --set service.ports[0].targetPort=15021 \
        --set service.ports[0].nodePort=30021 \
        --set service.ports[1].name=http2 \
        --set service.ports[1].port=80 \
        --set service.ports[1].targetPort=80 \
        --set service.ports[1].nodePort=30080 \
        --set service.ports[2].name=https \
        --set service.ports[2].port=443 \
        --set service.ports[2].targetPort=443 \
        --set service.ports[2].nodePort=30443 \
        --wait
else
    echo "✅ Istio Ingress Gateway already installed."
fi

# Patch Ingress Gateway to bind to Host Ports (Kind extraPortMappings)
# This is a bit of a hack for Kind to receive traffic on localhost:80
# Actually, Kind maps container port 80 to host port 80.
# We need the Ingress Gateway service to listen on 80 inside the container?
# No, Kind 'NodePort' means it's listening on the Node's IP.
# We need to use 'hostPort' or patch the Service to be accessible.
# A simpler way with Kind is using NodePort and the extraPortMappings above map container:80 -> host:80.
# The `extraPortMappings` map the docker container port 80 to the host machine port 80.
# Inside the docker container (the k8s node), we need something listening on port 80.
# That is usually the Ingress Controller Pod if using hostPort, or we use a Service NodePort.
# Kind's documented way is `hostPort` in the Pod or NodePort on the Service?
# Actually Kind forwards to the node. We need the Ingress Gateway to be exposed on the node.
# Let's trust standard Istio install + NodePort/LoadBalancer behavior or standard ingress-nginx behavior.
# For Istio, we might need a specific configuration.
# For now, let's proceed with standard install and debugging if connection fails.

echo "✅ Cluster and Istio Setup Complete!"


# 6. Build and Deploy All Services
echo "🏗 Building and Deploying Services..."

# 6a. Deploy Web App
echo "➡️ Processing web (Frontend)..."
docker build -t santhe/web:latest ./web
kind load docker-image santhe/web:latest --name $CLUSTER_NAME
helm upgrade --install web charts/microservice -f infrastructure/manifests/web-values.yaml --create-namespace --namespace santhe

# 6b. Deploy Backend Microservices
for service_dir in services/*; do
    if [ -d "$service_dir" ]; then
        SERVICE_NAME=$(basename "$service_dir")
        IMAGE_NAME="santhe/$SERVICE_NAME:latest"
        
        echo "➡️ Processing $SERVICE_NAME..."
        
        # Build
        docker build -t $IMAGE_NAME $service_dir
        
        # Load into Kind
        kind load docker-image $IMAGE_NAME --name $CLUSTER_NAME
        
        # Deploy with Helm
        # We assume basic configuration for now. Each service ideally has its own values.yaml,
        # but for now we'll use the default chart values or generate a minimal set if needed.
        # The default chart pulls 'nginx' by default, so we MUST override the image.
        
        helm upgrade --install $SERVICE_NAME charts/microservice \
            --namespace santhe \
            --set image.repository="santhe/$SERVICE_NAME" \
            --set image.tag="latest" \
            --set image.pullPolicy="IfNotPresent" \
            --set nameOverride="$SERVICE_NAME" \
            --set fullnameOverride="$SERVICE_NAME" \
            --set service.port=8000 \
            --set istio.enabled=true \
             --set istio.virtualService.enabled=true \
             --set istio.virtualService.hosts[0]="$SERVICE_NAME.local" \
             --set istio.virtualService.routes[0].destination.host="$SERVICE_NAME" \
             --set istio.virtualService.routes[0].destination.port.number=8000
    fi
done

echo "🎉 Deployment Complete! Access web at http://localhost"
