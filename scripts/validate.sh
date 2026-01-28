#!/bin/bash
# Validate services without full rebuild - runs tests locally then quick deploys
# Usage: ./scripts/validate.sh [service1] [service2] ...
#        ./scripts/validate.sh --changed   # Validate only git-changed services
set -e

# Import common utilities
source scripts/common.sh

# Determine which services to validate
if [ "$1" == "--changed" ]; then
    SERVICES=$(get_changed_services)
    
    if [ -z "$SERVICES" ]; then
        print_warning "No changed services detected."
        exit 0
    fi
    echo "🔍 Validating changed services: $SERVICES"
else
    SERVICES="$@"
fi

if [ -z "$SERVICES" ]; then
    echo "Usage: ./scripts/validate.sh [service1] [service2] ..."
    echo "       ./scripts/validate.sh --changed   # Validate git-changed services"
    exit 1
fi

FAILED=()
PASSED=()

for service in $SERVICES; do
    SERVICE_DIR="services/$service"
    
    if [ ! -d "$SERVICE_DIR" ]; then
        print_warning "Service '$service' not found, skipping"
        continue
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 Validating: $service"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Step 1: Lint with ruff (fast)
    echo "📝 Linting..."
    if docker run --rm -v "$(pwd)/$SERVICE_DIR:/app" -w /app python:3.11-slim-bookworm \
        pip install -q ruff && ruff check . 2>/dev/null; then
        echo "   Lint: ✓"
    else
        print_warning "Lint issues (non-blocking)"
    fi
    
    # Step 2: Build image (includes running tests via Dockerfile)
    echo "🏗️  Building (includes tests)..."
    if docker build -t santhe/$service:test $SERVICE_DIR > /tmp/build_$service.log 2>&1; then
        echo "   Build: ✓"
        echo "   Tests: ✓ (passed in Dockerfile)"
        PASSED+=("$service")
    else
        print_error "Build failed for $service"
        echo "   See: /tmp/build_$service.log"
        FAILED+=("$service")
        continue
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 VALIDATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ${#PASSED[@]} -gt 0 ]; then
    print_status "Passed: ${PASSED[*]}"
fi

if [ ${#FAILED[@]} -gt 0 ]; then
    print_error "Failed: ${FAILED[*]}"
    echo ""
    echo "Fix the failures and re-run, or deploy passing services with:"
    echo "  ./scripts/quick-deploy.sh ${PASSED[*]}"
    exit 1
fi

echo ""
echo "🚀 All validations passed! Deploy with:"
echo "  ./scripts/quick-deploy.sh ${PASSED[*]}"
