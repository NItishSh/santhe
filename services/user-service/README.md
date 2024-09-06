# User Service for Santhe Platform

## Overview

The User Service is responsible for handling user-related operations in the Santhe platform. It manages user registration, authentication, and profile management for farmers, middlemen, and admin users.

## Features

- User Registration
- Authentication (Login/Logout)
- Role-Based Access Control
- Profile Management
- Password Management and Recovery

## API Endpoints

### User Registration

- POST `/api/users/register`: Register a new user
- POST `/api/users/admin-register`: Register a new admin user

### Authentication

- POST `/api/auth/login`: Login a user
- POST `/api/auth/logout`: Logout a user

### Profile Management

- GET `/api/users/me`: Get current user profile
- PATCH `/api/users/me`: Update current user profile
- GET `/api/users/{userId}`: Get a specific user's profile

### Role Management

- GET `/api/roles`: List available roles
- PATCH `/api/users/{userId}/role`: Assign a role to a user

### Password Management

- POST `/api/password/forgot`: Initiate password reset
- POST `/api/password/reset`: Reset password

## Dependencies

- Database: PostgreSQL
- Authentication: JWT
- Validation: Pydantic

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export SECRET_KEY=your_secret_key_here
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


