# Pricing Service for Santhe Platform

## Overview

The Pricing Service is responsible for managing pricing details for the agricultural products listed on the Santhe platform. It allows middlemen to place bids or quotes for products, enabling dynamic pricing mechanisms.

## Features

- Pricing Updates
- Price History Tracking
- Bid Management

## API Endpoints

### Pricing Management

- POST `/api/prices`: Create a new price record
- GET `/api/prices/{priceId}`: Retrieve a specific price record
- PATCH `/api/prices/{priceId}`: Update an existing price record
- DELETE `/api/prices/{priceId}`: Remove a price record

### Bid Management

- POST `/api/bids`: Place a bid for a product
- GET `/api/bids/{bidId}`: Retrieve a specific bid
- PATCH `/api/bids/{bidId}`: Update an existing bid
- DELETE `/api/bids/{bidId}`: Cancel a bid

### Price History

- GET `/api/prices/history/{productId}`: Get price history for a product

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

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

### Key points about this README:

1. Provides an overview of the Pricing Service's purpose within the Santhe platform.
2. Lists the main features of the service.
3. Outlines the API endpoints for various pricing-related operations.
4. Specifies the dependencies required for the service.
5. Includes setup instructions for local development.
6. Mentions testing procedures.
7. Points to the location of API documentation.
8. Encourages contributions and specifies the license.

This README serves as a good starting point for documenting the Pricing Service. You may need to adjust some details based on your specific implementation choices (e.g., exact API endpoints, additional features, etc.). Remember to keep updating this file as you develop and refine the service.

Citations:
[1] https://www.squash.io/connecting-fastapi-with-postgresql-a-practical-approach/
[2] https://medium.com/@navinsharma9376319931/mastering-fastapi-crud-operations-with-async-sqlalchemy-and-postgresql-3189a28d06a2
[3] https://medium.com/@kacperwlodarczyk/fast-api-repository-pattern-and-service-layer-dad43354f07a
[4] https://medium.com/@stanker801/creating-a-crud-api-with-fastapi-sqlalchemy-postgresql-postman-pydantic-1ba6b9de9f23
[5] https://mattermost.com/blog/building-a-crud-fastapi-app-with-sqlalchemy/
[6] https://patrick-muehlbauer.com/articles/fastapi-with-sqlalchemy/
[7] https://facundojmaero.github.io/blog/2021/08/fastapi-db-tests/
[8] https://dev.to/tobias-piotr/patterns-and-practices-for-using-sqlalchemy-20-with-fastapi-49n8
[9] https://github.com/fastapi/full-stack-fastapi-template
[10] https://fastapi.tiangolo.com/tutorial/sql-databases/