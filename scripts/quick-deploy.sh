#!/bin/bash
# Quick deploy - Only redeploy specified services (or changed ones)
# Usage: ./scripts/quick-deploy.sh [service1] [service2] ...
#        ./scripts/quick-deploy.sh --changed   # Deploy only git-changed services
#        ./scripts/quick-deploy.sh --all       # Parallel deploy all (faster than setup-local.sh)
set -e

CLUSTER_NAME="santhe-local"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if Kind cluster exists
if ! kind get clusters 2>/dev/null | grep -q "^$CLUSTER_NAME$"; then
    print_error "Kind cluster '$CLUSTER_NAME' not found. Run ./scripts/setup-local.sh first."
    exit 1
fi

# Determine which services to deploy
if [ "$1" == "--changed" ]; then
    # Get services with changes (staged or unstaged)
    SERVICES=$(git diff --name-only HEAD 2>/dev/null | grep "^services/" | cut -d'/' -f2 | sort -u)
    SERVICES="$SERVICES $(git diff --cached --name-only 2>/dev/null | grep "^services/" | cut -d'/' -f2 | sort -u)"
    SERVICES=$(echo "$SERVICES" | tr ' ' '\n' | sort -u | tr '\n' ' ')
    
    if [ -z "$SERVICES" ]; then
        print_warning "No changed services detected. Use --all or specify services."
        exit 0
    fi
    echo "🔍 Detected changed services: $SERVICES"
elif [ "$1" == "--all" ]; then
    SERVICES=$(ls -d services/*/ 2>/dev/null | xargs -n1 basename)
else
    SERVICES="$@"
fi

if [ -z "$SERVICES" ]; then
    echo "Usage: ./scripts/quick-deploy.sh [service1] [service2] ..."
    echo "       ./scripts/quick-deploy.sh --changed   # Deploy git-changed services"
    echo "       ./scripts/quick-deploy.sh --all       # Deploy all services"
    echo ""
    echo "Available services:"
    ls -d services/*/ 2>/dev/null | xargs -n1 basename | sed 's/^/  - /'
    exit 1
fi

echo "🚀 Quick Deploy: $SERVICES"
echo ""

# Deploy services in parallel (up to 4 at a time)
deploy_service() {
    local service=$1
    echo "[$service] Starting..."
    
    if [ ! -d "services/$service" ]; then
        echo "[$service] ❌ Not found, skipping"
        return 1
    fi
    
    # Build
    if ! docker build -q -t santhe/$service:latest services/$service > /dev/null 2>&1; then
        echo "[$service] ❌ Build failed"
        return 1
    fi
    echo "[$service] Built ✓"
    
    # Load into Kind
    if ! kind load docker-image santhe/$service:latest --name $CLUSTER_NAME > /dev/null 2>&1; then
        echo "[$service] ❌ Load failed"
        return 1
    fi
    echo "[$service] Loaded ✓"
    
    # Helm upgrade (quick, no wait)
    if ! ./scripts/deploy-service.sh "$service" latest > /dev/null 2>&1; then
        echo "[$service] ❌ Deploy failed"
        return 1
    fi
    echo "[$service] ✅ Deployed"
}

# Run deployments (parallel if multiple)
export -f deploy_service
export CLUSTER_NAME

SERVICE_COUNT=$(echo $SERVICES | wc -w)
if [ "$SERVICE_COUNT" -eq 1 ]; then
    # Single service - show full output
    ./scripts/deploy-service.sh $SERVICES latest
else
    # Multiple services - run in parallel
    echo "$SERVICES" | tr ' ' '\n' | xargs -P4 -I{} bash -c 'deploy_service "{}"'
fi

echo ""
print_status "Quick deploy complete!"

# Restart pods to pick up new images
echo "♻️  Restarting deployments..."
for service in $SERVICES; do
    kubectl rollout restart deployment/$service -n santhe 2>/dev/null || true
done

echo "🎉 Done! Services deployed: $SERVICES"
