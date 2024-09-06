# Product Catalog Service for Santhe Platform

## Overview

The Product Catalog Service is responsible for managing agricultural products listed by farmers on the Santhe platform. It handles product creation, updates, categorization, and provides search and filtering capabilities.

## Features

- Product Creation, Updating, and Deletion
- Product Categorization
- Search Functionality
- Filtering Options

## API Endpoints

### Product Management

- POST `/api/products`: Create a new product listing
- GET `/api/products/{productId}`: Retrieve a specific product details
- PATCH `/api/products/{productId}`: Update a product listing
- DELETE `/api/products/{productId}`: Remove a product listing

### Categorization

- GET `/api/categories`: List available categories
- POST `/api/categories`: Create a new category
- PATCH `/api/categories/{categoryId}`: Update a category
- DELETE `/api/categories/{categoryId}`: Delete a category

### Search and Filtering

- GET `/api/products/search`: Search products by name, description, or category
- GET `/api/products/filter`: Filter products by price range, category, etc.

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
