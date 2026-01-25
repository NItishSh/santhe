#!/bin/bash
set -e

SERVICE_NAME=$1
VERSION=${2:-latest}
CLUSTER_NAME="santhe-local"

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./scripts/deploy-service.sh <service-name> [version]"
    exit 1
fi

SERVICE_DIR="services/$SERVICE_NAME"

if [ ! -d "$SERVICE_DIR" ]; then
    echo "❌ Service directory '$SERVICE_DIR' not found."
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
# DB Host: postgres.santhe.svc.cluster.local (Standard K8s DNS)
DB_NAME="${SERVICE_NAME//-/_}_db"
DATABASE_URL="postgresql://postgres:postgres@postgres-postgresql.santhe.svc.cluster.local:5432/$DB_NAME"

echo "   - Configured DB: $DATABASE_URL"

helm upgrade --install $SERVICE_NAME charts/microservice \
    --namespace santhe \
    --set image.repository="santhe/$SERVICE_NAME" \
    --set image.tag="$VERSION" \
    --set image.pullPolicy="IfNotPresent" \
    --set nameOverride="$SERVICE_NAME" \
    --set fullnameOverride="$SERVICE_NAME" \
    --set service.port=8000 \
    --set istio.enabled=true \
        --set istio.virtualService.enabled=true \
        --set istio.virtualService.hosts[0]="$SERVICE_NAME.local" \
        --set istio.virtualService.routes[0].destination.host="$SERVICE_NAME" \
        --set istio.virtualService.routes[0].destination.port.number=8000 \
    --set env[0].name=DATABASE_URL \
    --set env[0].value="$DATABASE_URL" \
    --set env[1].name=SECRET_KEY \
    --set env[1].value="supersecret" \
    --set migrations.enabled=true

echo "✅ $SERVICE_NAME deployed successfully!"
