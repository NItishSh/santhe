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

SERVICE_DIR="services/$SERVICE_NAME"
VALUES_FILE="$SERVICE_DIR/values.yaml"

if [ ! -d "$SERVICE_DIR" ]; then
    echo "❌ Service directory '$SERVICE_DIR' not found."
    exit 1
fi

if [ ! -f "$VALUES_FILE" ]; then
    echo "❌ Values file '$VALUES_FILE' not found."
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

# DB Connection String
DB_NAME="${SERVICE_NAME//-/_}_db"
DATABASE_URL="postgresql://postgres:postgres@postgres-postgresql.santhe.svc.cluster.local:5432/$DB_NAME"

echo "   - Using values from: $VALUES_FILE"
echo "   - Configured DB: $DATABASE_URL"

# Deploy using per-service values.yaml
helm upgrade --install $SERVICE_NAME charts/microservice \
    --namespace santhe \
    -f "$VALUES_FILE" \
    --set image.tag="$VERSION" \
    --set env[0].name=DATABASE_URL \
    --set env[0].value="$DATABASE_URL" \
    --set env[1].name=SECRET_KEY \
    --set env[1].value="supersecret"

echo "✅ $SERVICE_NAME deployed successfully!"
