#!/bin/bash
set -e

SERVICE_NAME=$1
CLUSTER_NAME="santhe-local"

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./scripts/deploy-service.sh <service-name>"
    exit 1
fi

SERVICE_DIR="services/$SERVICE_NAME"

if [ ! -d "$SERVICE_DIR" ]; then
    echo "❌ Service directory '$SERVICE_DIR' not found."
    exit 1
fi

echo "🚀 Deploying $SERVICE_NAME..."

# Build
echo "🏗 Building Docker image..."
docker build -t santhe/$SERVICE_NAME:latest $SERVICE_DIR

# Load
echo "📦 Loading image into Kind..."
kind load docker-image santhe/$SERVICE_NAME:latest --name $CLUSTER_NAME

# Deploy
echo "☸️ Deploying to Kubernetes..."
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

echo "✅ $SERVICE_NAME deployed successfully!"
