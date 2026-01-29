#!/bin/bash
set -e

echo "🧨  Resetting Migration State..."

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

for SERVICE_NAME in "${SERVICES[@]}"; do
    DB_NAME=$(echo "$SERVICE_NAME" | tr '-' '_')_db
    echo "--------------------------------------------------"
    echo "🧹  Cleaning $DB_NAME..."
    
    # Drop alembic_version table
    kubectl run -i --rm --restart=Never "clean-db-$SERVICE_NAME-$(date +%s)" \
        --image=postgres:16 \
        --namespace=database \
        --env="PGPASSWORD=postgres" \
        -- psql -h postgres-postgresql -U postgres -d $DB_NAME -c "DROP TABLE IF EXISTS alembic_version;" || echo "⚠️  Failed to drop alembic_version for $DB_NAME"
done

echo "✅ Migration state reset. Now run ./scripts/run-migrations.sh"
