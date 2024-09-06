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
```

### Key points about this README:

1. It provides an overview of the User Service's purpose within the Santhe platform.
2. Lists the main features of the service.
3. Outlines the API endpoints for various user-related operations.
4. Specifies the dependencies required for the service.
5. Includes setup instructions for local development.
6. Mentions testing procedures.
7. Points to the location of API documentation.
8. Encourages contributions and specifies the license.

This README serves as a good starting point for documenting the User Service. You may need to adjust some details based on your specific implementation choices (e.g., framework, database ORM, etc.). Remember to keep updating this file as you develop and refine the service.

Citations:
[1] https://dzone.com/articles/a-readme-for-your-microservice-github-repository
[2] https://github.com/wjoz/microservices-example-user-service
[3] https://medium.com/@kc_clintone/the-ultimate-guide-to-writing-a-great-readme-md-for-your-project-3d49c2023357
[4] https://dev.to/mfts/how-to-write-a-perfect-readme-for-your-github-project-59f2
[5] https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
[6] https://dev.to/yuridevat/how-to-create-a-good-readmemd-file-4pa2
[7] https://github.com/overture-stack/microservice-template-java/blob/master/README.template.md
[8] https://github.com/piomin/sample-spring-microservices/blob/master/readme.md
[9] https://dev.to/kwing25/how-to-write-a-good-readme-for-your-project-1l10
[10] https://markdown.land/readme-md