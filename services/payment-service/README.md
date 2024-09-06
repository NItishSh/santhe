# Payment Service for Santhe Platform

## Overview

The Payment Service is responsible for facilitating secure financial transactions between farmers and middlemen on the Santhe platform. It processes payments, maintains payment histories, and handles refunds and disputes.

## Features

- Payment Processing
- Payment History Tracking
- Refund Handling
- Dispute Resolution

## API Endpoints

### Payment Processing

- POST `/api/payments`: Process a payment transaction
- GET `/api/payments/{paymentId}`: Retrieve a specific payment details
- PATCH `/api/payments/{paymentId}`: Update a payment status

### Payment History

- GET `/api/payments/history/{userId}`: Get payment history for a user

### Refunds

- POST `/api/refunds`: Initiate a refund for a payment
- GET `/api/refunds/{refundId}`: Check status of a refund request

### Disputes

- POST `/api/disputes`: Open a dispute for a payment
- GET `/api/disputes/{disputeId}`: Get details of a dispute

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Payment Gateway: Stripe (or similar)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export STRIPE_SECRET_KEY=your_stripe_secret_key_here
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

## Security Considerations

- Implement HTTPS for all API communications
- Use strong encryption for storing sensitive payment information
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
