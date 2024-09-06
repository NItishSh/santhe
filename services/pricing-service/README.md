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
