# Order Management Service for Santhe Platform

## Overview

The Order Management Service is responsible for handling the flow of orders between farmers and middlemen on the Santhe platform. It manages order creation, updates, cancellations, and tracks order statuses.

## Features

- Order Creation, Updating, and Cancellation
- Order Status Tracking
- Notifications for Order Updates

## API Endpoints

### Order Management

- POST `/api/orders`: Create a new order
- GET `/api/orders`: Retrieve all orders
- GET `/api/orders/{orderId}`: Retrieve a specific order details
- PATCH `/api/orders/{orderId}`: Update an existing order
- DELETE `/api/orders/{orderId}`: Cancel an order

### Order Status

- GET `/api/orders/status`: Get current status of all orders
- GET `/api/orders/{orderId}/status`: Get current status of a specific order

### Notifications

- POST `/api/notifications`: Send notifications for order updates

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Message Queue: RabbitMQ (for asynchronous task processing)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export RABBITMQ_URL=amqp://user:password@host:port/vhost
```

3. Run migrations:
```
alembic upgrade head
```

4. Start the service:
```
uvicorn main:app --reload
```

## Testing

To run tests:
```
pytest
```


## API Documentation

API documentation is available at `/docs` after starting the service.

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
