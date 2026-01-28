#!/bin/bash
# Hot reload a single service - fastest option for iterating on one service
# Usage: ./scripts/hot-reload.sh <service-name>
# 
# Does NOT rebuild the image - copies src/ files directly into running pod
# Best for: Python code changes (NOT requirements.txt changes)
set -e

SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: ./scripts/hot-reload.sh <service-name>"
    echo ""
    echo "Hot reloads Python source code without rebuilding Docker image."
    echo "Use for rapid iteration on code changes."
    echo ""
    echo "⚠️  Does NOT work for:"
    echo "   - requirements.txt changes (use quick-deploy.sh)"
    echo "   - Dockerfile changes (use quick-deploy.sh)"
    echo ""
    exit 1
fi

if [ ! -d "services/$SERVICE_NAME" ]; then
    echo "❌ Service '$SERVICE_NAME' not found"
    exit 1
fi

# Get pod name
POD=$(kubectl get pods -n santhe -l app=$SERVICE_NAME -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$POD" ]; then
    echo "❌ No running pod found for $SERVICE_NAME"
    echo "   Run ./scripts/quick-deploy.sh $SERVICE_NAME first"
    exit 1
fi

echo "🔥 Hot reloading $SERVICE_NAME..."
echo "   Pod: $POD"

# Copy source files to pod
echo "📂 Copying src/ to pod..."
kubectl cp services/$SERVICE_NAME/src/. santhe/$POD:/app/src/ -c $SERVICE_NAME 2>/dev/null || \
kubectl cp services/$SERVICE_NAME/src/. santhe/$POD:/app/src/

# Restart the uvicorn process (by killing it - K8s will restart)
echo "♻️  Restarting uvicorn..."
kubectl exec -n santhe $POD -- pkill -f uvicorn 2>/dev/null || true

# Wait for pod to be ready
echo "⏳ Waiting for pod to restart..."
sleep 2
kubectl wait --for=condition=ready pod/$POD -n santhe --timeout=30s 2>/dev/null || true

echo "✅ Hot reload complete for $SERVICE_NAME"
echo "   Test at: kubectl port-forward svc/$SERVICE_NAME 8001:8000 -n santhe"
