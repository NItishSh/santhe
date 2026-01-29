#!/bin/bash
set -e

echo "🔄 Running Database Migrations..."

# List of services that need migrations
SERVICES=(
    "user-service"
    "cart-management-service"
    "product-catalog-service"
    "order-management-service"
    "payment-service"
    "pricing-service"
    "notification-service"
    "logistics-management-service"
    "feedback-and-support-service"
    "compliance-and-audit-service"
    "analytics-and-reporting-service"
    "review-and-rating-service"
)

for SERVICE in "${SERVICES[@]}"; do
    echo "--------------------------------------------------"
    echo "🛠  Migrating $SERVICE..."
    
    # Get the pod name
    POD=$(kubectl get pod -n santhe -l app=$SERVICE -o jsonpath="{.items[0].metadata.name}")
    
    if [ -z "$POD" ]; then
        echo "⚠️  No pod found for $SERVICE. Skipping."
        continue
    fi
    
    echo "📍 Pod: $POD"
    
    # Run alembic upgrade head
    kubectl exec -n santhe "$POD" -- alembic upgrade head || echo "❌ Migration failed for $SERVICE"
done

echo "✅ All migrations attempted."
