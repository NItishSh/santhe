#!/bin/bash
# Deploy a single service to the local Kind cluster
# Usage: ./scripts/deploy-service.sh <service-name> [version]
set -e

SERVICE_NAME=$1
VERSION=${2:-latest}
CLUSTER_NAME="santhe-local"

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./scripts/deploy-service.sh <service-name> [version]"
    exit 1
fi

# Handle Web App Special Case
if [ "$SERVICE_NAME" == "web" ]; then
    SERVICE_DIR="web"
    VALUES_FILE="web/values.yaml"
else
    SERVICE_DIR="services/$SERVICE_NAME"
    VALUES_FILE="$SERVICE_DIR/values.yaml"
fi

if [ ! -d "$SERVICE_DIR" ]; then
    echo "❌ Directory '$SERVICE_DIR' not found."
    exit 1
fi

echo "🚀 Deploying $SERVICE_NAME:$VERSION..."

# Build
echo "🏗 Building Docker image..."
docker build -t santhe/$SERVICE_NAME:$VERSION $SERVICE_DIR

# Load
echo "📦 Loading image into Kind..."
kind load docker-image santhe/$SERVICE_NAME:$VERSION --name $CLUSTER_NAME

# Deploy
echo "☸️ Deploying to Kubernetes..."

# Handle DB Connection String if not using values.yaml, 
# but now we expect values.yaml to exist and contain it.
# We'll just pass -f VALUES_FILE.

if [ -f "$VALUES_FILE" ]; then
    echo "   - Using values from: $VALUES_FILE"
    HELM_ARGS="-f $VALUES_FILE"
else
    echo "❌ Values file required but not found."
    exit 1
fi

# Deploy
helm upgrade --install $SERVICE_NAME charts/microservice \
    --namespace santhe \
    --set image.tag="$VERSION" \
    $HELM_ARGS

echo "✅ $SERVICE_NAME deployed successfully!"
