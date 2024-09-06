# Feedback and Support Service for Santhe Platform

## Overview

The Feedback and Support Service is responsible for managing customer inquiries, resolving issues, and gathering valuable feedback to improve the Santhe platform experience. It provides a centralized hub for users to seek assistance and share their experiences.

## Features

- Customer Support Ticket Management
- Feedback Collection and Analysis
- Knowledge Base Integration
- Multi-channel Support (Email, Chat, Social Media)

## API Endpoints

### Support Tickets

- POST `/api/support/tickets`: Create a new support ticket
- GET `/api/support/tickets`: Retrieve all support tickets
- GET `/api/support/tickets/{ticketId}`: Retrieve a specific support ticket details
- PATCH `/api/support/tickets/{ticketId}`: Update an existing support ticket
- DELETE `/api/support/tickets/{ticketId}`: Close a support ticket

### Feedback Submission

- POST `/api/feedback`: Submit feedback
- GET `/api/feedback/stats`: Get aggregated feedback statistics

### Knowledge Base

- GET `/api/knowledge-base/topics`: List available topics in the knowledge base
- GET `/api/knowledge-base/articles/{topicId}`: Retrieve articles for a specific topic

### Multi-channel Support

- POST `/api/support/chat`: Initiate a chat session
- POST `/api/support/email`: Send an email support request
- POST `/api/support/social-media`: Post a support query on social media platforms

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Chatbot: Rasa (for automated support)
- Email Service: SendGrid (for sending support emails)
- Social Media API: Twitter API (as an example, can be extended to other platforms)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export RASA_MODEL_PATH=/path/to/rasa/model 
export SENDGRID_API_KEY=your_sendgrid_api_key_here 
export TWITTER_API_KEY=your_twitter_api_key_here 
export TWITTER_API_SECRET=your_twitter_api_secret_here
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

- Implement rate limiting to prevent abuse of support endpoints
- Use strong encryption for storing sensitive customer data
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
