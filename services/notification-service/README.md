# Notification Service for Santhe Platform

## Overview

The Notification Service is responsible for sending real-time notifications to users (farmers and middlemen) about orders, payments, and platform updates on the Santhe platform.

## Features

- SMS Notifications
- Email Notifications
- In-app Notifications
- Notification Preferences Management

## API Endpoints

### Notification Management

- POST `/api/notifications`: Send a notification
- GET `/api/notifications/{notificationId}`: Retrieve a specific notification details
- PATCH `/api/notifications/{notificationId}`: Update a notification status

### User Preferences

- GET `/api/preferences/{userId}`: Get user's notification preferences
- PATCH `/api/preferences/{userId}`: Update user's notification preferences

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Message Queue: RabbitMQ (for asynchronous task processing)
- Notification Services: Twilio (SMS), SendGrid (Email)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export RABBITMQ_URL=amqp://user:password@host:port/vhost 
export TWILIO_ACCOUNT_SID=your_twilio_account_sid_here 
export TWILIO_AUTH_TOKEN=your_twilio_auth_token_here 
export SENDGRID_API_KEY=your_sendgrid_api_key_here
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

- Implement rate limiting to prevent abuse of notification endpoints
- Use strong encryption for storing sensitive user data
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
