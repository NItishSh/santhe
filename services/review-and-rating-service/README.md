# Review and Rating Service for Santhe Platform

## Overview

The Review and Rating Service is responsible for managing reviews and ratings between middlemen and farmers on the Santhe platform. It facilitates the submission of reviews, implements a rating system, and moderates reviews to promote trust and accountability among users.

## Features

- Review Submission
- Rating System
- Review Moderation

## API Endpoints

### Review Management

- POST `/api/reviews`: Submit a new review
- GET `/api/reviews`: Retrieve all reviews
- GET `/api/reviews/{reviewId}`: Retrieve a specific review details
- PATCH `/api/reviews/{reviewId}`: Update an existing review
- DELETE `/api/reviews/{reviewId}`: Remove a review

### Rating System

- GET `/api/ratings/{userId}`: Get average rating for a user
- POST `/api/ratings`: Rate a user

### Review Moderation

- POST `/api/moderate`: Flag a review for moderation
- GET `/api/moderated-reviews`: View pending reviews for moderation

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname
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

- Implement rate limiting to prevent abuse of review submission endpoints
- Use strong encryption for storing sensitive user data
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
