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

# Per-service resource configuration (based on load testing results)
case "$SERVICE_NAME" in
    user-service)
        # High CPU for bcrypt password hashing
        CPU_REQ="200m"; CPU_LIM="500m"; MEM_REQ="128Mi"; MEM_LIM="256Mi"
        ;;
    product-catalog-service)
        # Medium - handles catalog queries
        CPU_REQ="100m"; CPU_LIM="300m"; MEM_REQ="128Mi"; MEM_LIM="256Mi"
        ;;
    cart-management-service|order-management-service|payment-service)
        # Medium - transactional services
        CPU_REQ="100m"; CPU_LIM="300m"; MEM_REQ="96Mi"; MEM_LIM="192Mi"
        ;;
    notification-service)
        # Medium - may have external API calls
        CPU_REQ="100m"; CPU_LIM="300m"; MEM_REQ="96Mi"; MEM_LIM="192Mi"
        ;;
    *)
        # Light services (analytics, compliance, feedback, logistics, pricing, review)
        CPU_REQ="50m"; CPU_LIM="100m"; MEM_REQ="64Mi"; MEM_LIM="128Mi"
        ;;
esac

echo "   - Resources: CPU ${CPU_REQ}/${CPU_LIM}, Memory ${MEM_REQ}/${MEM_LIM}"

helm upgrade --install $SERVICE_NAME charts/microservice \
    --namespace santhe \
    --set image.repository="santhe/$SERVICE_NAME" \
    --set image.tag="$VERSION" \
    --set image.pullPolicy="IfNotPresent" \
    --set nameOverride="$SERVICE_NAME" \
    --set fullnameOverride="$SERVICE_NAME" \
    --set service.port=8000 \
    --set resources.requests.cpu="$CPU_REQ" \
    --set resources.requests.memory="$MEM_REQ" \
    --set resources.limits.cpu="$CPU_LIM" \
    --set resources.limits.memory="$MEM_LIM" \
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

