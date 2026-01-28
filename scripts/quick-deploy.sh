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

# Import common utilities
source scripts/common.sh

# Check if Kind cluster exists
if ! kind get clusters 2>/dev/null | grep -q "^$CLUSTER_NAME$"; then
    print_error "Kind cluster '$CLUSTER_NAME' not found. Run ./scripts/setup-local.sh first."
    exit 1
fi

# Determine which services to deploy
if [ "$1" == "--changed" ]; then
    SERVICES=$(get_changed_services)
    
    if [ -z "$SERVICES" ]; then
        print_warning "No changed services detected. Use --all or specify services."
        exit 0
    fi
    echo "🔍 Detected changed services: $SERVICES"
elif [ "$1" == "--all" ]; then
    # All services + web
    SERVICES="web $(ls -d services/*/ 2>/dev/null | xargs -n1 basename)"
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

# Deploy a single service (for parallel execution)
deploy_service_quick() {
    local service=$1
    echo "[$service] Starting..."
    
    local dir="services/$service"
    if [ "$service" == "web" ]; then
        dir="web"
    fi

    if [ ! -d "$dir" ]; then
        echo "[$service] ❌ Not found, skipping"
        return 1
    fi
    
    # Use deploy-service.sh for actual deployment
    if ! ./scripts/deploy-service.sh "$service" latest > /dev/null 2>&1; then
        echo "[$service] ❌ Deploy failed"
        return 1
    fi
    echo "[$service] ✅ Deployed"
}

# Run deployments
export -f deploy_service_quick
export CLUSTER_NAME

SERVICE_COUNT=$(echo $SERVICES | wc -w)
if [ "$SERVICE_COUNT" -eq 1 ]; then
    # Single service - show full output
    ./scripts/deploy-service.sh $SERVICES latest
else
    # Multiple services - run in parallel (up to 4 at a time)
    echo "$SERVICES" | tr ' ' '\n' | xargs -P4 -I{} bash -c 'deploy_service_quick "{}"'
fi

echo ""
print_status "Quick deploy complete!"
echo "🎉 Done! Services deployed: $SERVICES"
