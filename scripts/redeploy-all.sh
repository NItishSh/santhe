#!/bin/bash
set -e

echo "🚀 Redeploying ALL Services..."

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
    echo "🔄 Redeploying $SERVICE..."
    ./scripts/deploy-service.sh "$SERVICE"
done

echo "✅ All services redeployed."
