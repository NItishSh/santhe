#!/bin/bash
set -e

echo "🐘  Ensuring Databases Exist..."

# Wait for Postgres
echo "⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --namespace database \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/name=postgresql \
  --timeout=90s || echo "⚠️ Postgres wait timed out or failed"

# Loop through services
for service_dir in services/*; do
    if [ -d "$service_dir" ]; then
        SERVICE_NAME=$(basename "$service_dir")
        
        SERVICE_NAME=$(basename "$service_dir")
        DB_NAME=$(echo "$SERVICE_NAME" | tr '-' '_')_db
        echo "Ensuring DB for $SERVICE_NAME: $DB_NAME"
        
        kubectl run -i --rm --restart=Never "create-db-$SERVICE_NAME-$(date +%s)" \
            --image=postgres:16 \
            --namespace=database \
            --env="PGPASSWORD=postgres" \
            -- psql -h postgres-postgresql -U postgres -c "CREATE DATABASE $DB_NAME;" || echo "⚠️  Failed (exists?)"
    fi
done

echo "✅ Database Ensure Complete."
