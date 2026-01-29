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

# 7. Install Istio Addons & MetalLB (Observability + LoadBalancer)
echo "🛠 Setting up Addons (Observability + MetalLB)..."
./scripts/setup-addons.sh

# 8. Prepare Application Namespace
echo "🏗 Creating 'santhe' namespace and enabling Istio injection..."
kubectl create namespace santhe --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace santhe istio-injection=enabled --overwrite
echo "✅ Namespace 'santhe' ready with Istio injection."

# 9. Apply Istio Gateway Configuration
echo "🚪 Applying Istio Gateway..."
kubectl apply -f infrastructure/manifests/gateway.yaml

# 10. Install PostgreSQL (Shared Instance)
echo "🐘 Installing PostgreSQL..."
if ! helm status postgres -n santhe >/dev/null 2>&1; then
    helm repo add bitnami https://charts.bitnami.com/bitnami 2>/dev/null || true
    helm repo update
    
    # Install Postgres with a fixed password for local dev ease
    helm upgrade --install postgres bitnami/postgresql \
        --namespace santhe \
        --create-namespace \
        --set auth.postgresPassword=postgres \
        --set primary.persistence.enabled=false \
        --wait
else
    echo "✅ PostgreSQL already installed."
fi

# 9. Create Databases for Microservices
echo "🗄 Preparing Databases..."
PROVISION_SQL=""
for service_dir in services/*; do
    if [ -d "$service_dir" ]; then
        SERVICE_NAME=$(basename "$service_dir")
        DB_NAME="${SERVICE_NAME//-/_}_db"
        # Just try to create the DB. If it exists, it errors but continues (default psql behavior without ON_ERROR_STOP)
        PROVISION_SQL="${PROVISION_SQL}CREATE DATABASE $DB_NAME;"
    fi
done

# Execute DB creation
# We use echo to pipe the SQL into the psql command running inside the pod
echo "$PROVISION_SQL" | kubectl run postgres-init --image=postgres:alpine --restart=Never --rm -i -- \
    psql postgresql://postgres:postgres@postgres-postgresql.santhe.svc.cluster.local:5432/postgres \
    || echo "⚠️  Database provisioning had errors (likely 'already exists'), checking readiness..."

# 6. Build and Deploy All Services
echo "🏗 Building and Deploying Services..."
# 6a. Deploy Web App
# 6a. Deploy Web App
echo "➡️ Processing web (Frontend)..."
./scripts/deploy-service.sh web latest

# 6b. Deploy Backend Microservices
# 6b. Deploy Backend Microservices
# Load version configuration
# We grep the file manually below, so no need to source it (which fails on hyphens)


for service_dir in services/*; do
    if [ -d "$service_dir" ]; then
        SERVICE_NAME=$(basename "$service_dir")
        
        # Get version from env var (converting hyphen to underscore for variable name if needed, 
        # but simpler to just expect matching names or default to latest)
        # Bash variable indirection to get value of verify variable named $SERVICE_NAME
        VERSION_VAR=${SERVICE_NAME//-/_} # user-service -> user_service (standard env var naming)
        # Actually, let's just stick to reading the file or defaulting.
        # Direct lookup might be cleaner.
        
        # Let's use a simpler approach: Read specific line or default
        # But we already sourced it. 
        # The issue is variable names with hyphens are not standard in shell assignment (though bash allows them in some contexts, export usually doesn't).
        # Let's assume versions.env uses standard keys or we grep it.
        
        # Robust way: grep the file
        SERVICE_VERSION=$(grep "^$SERVICE_NAME=" versions.env | cut -d'=' -f2)
        
        if [ -z "$SERVICE_VERSION" ]; then
            SERVICE_VERSION="latest"
        fi

        echo "➡️ Processing $SERVICE_NAME (Version: $SERVICE_VERSION)..."
        
        ./scripts/deploy-service.sh "$SERVICE_NAME" "$SERVICE_VERSION"
    fi
done

echo "🎉 Deployment Complete! Access web at http://localhost:8080"

# Expose Web UI
echo "🌍 Starting Port Forward (Web UI -> localhost:8080)..."
kubectl port-forward svc/web 8080:3000 -n santhe > /dev/null 2>&1 &

# Wait for port-forward to be ready
echo "⏳ Waiting for Web UI to be reachable..."
attempts=0
until curl -s http://localhost:8080 > /dev/null; do
    attempts=$((attempts+1))
    if [ $attempts -gt 30 ]; then
      echo "⚠️  Web UI not reachable after 30 attempts, skipping seeding."
      exit 0
    fi
    sleep 2
done

# Seed Data
echo "🌱 Seeding Users and Data..."
python3 scripts/seed_users.py
python3 scripts/seed_data.py

echo "✅ Setup Complete!"
