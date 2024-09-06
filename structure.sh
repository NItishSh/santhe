#!/bin/bash

# Array of microservices
services=(
    "user-service" 
    "product-catalog-service"
    "pricing-service"
    "order-management-service"
    "payment-service"
    "review-and-rating-service"
    "notification-service"
    "logistics-management-service"
    "analytics-and-reporting-service"
    "compliance-and-audit-service"
    "feedback-and-support-service"
)

# Create the services directory
mkdir -p services

# Loop through each service and create the directory structure
for service in "${services[@]}"
do
    echo "Creating structure for $service..."

    # Create directories
    mkdir -p services/$service/src
    mkdir -p services/$service/tests
    mkdir -p services/$service/config

    # Create placeholder files if they don't exist
    [ ! -f services/$service/src/__init__.py ] && touch services/$service/src/__init__.py
    [ ! -f services/$service/src/main.py ] && touch services/$service/src/main.py
    [ ! -f services/$service/tests/test_${service//-/}.py ] && touch services/$service/tests/test_${service//-/}.py
    [ ! -f services/$service/config/settings.py ] && touch services/$service/config/settings.py
    [ ! -f services/$service/Dockerfile ] && touch services/$service/Dockerfile
    [ ! -f services/$service/requirements.txt ] && touch services/$service/requirements.txt
    [ ! -f services/$service/README.md ] && touch services/$service/README.md
    [ ! -f services/$service/Makefile ] && touch services/$service/Makefile

    echo "$service structure created."
done

echo "All microservices structure created successfully!"
