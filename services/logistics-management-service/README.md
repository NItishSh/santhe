# Logistics Management Service for Santhe Platform

## Overview

The Logistics Management Service is responsible for coordinating and managing the physical movement of goods between farmers and middlemen on the Santhe platform. It handles order tracking, shipping, and delivery management.

## Features

- Order Tracking
- Shipping Management
- Delivery Confirmation
- Real-time Location Updates

## API Endpoints

### Order Tracking

- GET `/api/orders/{orderId}/tracking`: Get tracking information for an order
- POST `/api/orders/{orderId}/track`: Update order tracking status

### Shipping Management

- POST `/api/shipping`: Create a new shipping label
- GET `/api/shipping/{shippingId}`: Retrieve shipping details
- PATCH `/api/shipping/{shippingId}`: Update shipping status

### Delivery Management

- POST `/api/deliveries`: Mark a shipment as delivered
- GET `/api/deliveries/{deliveryId}`: Get delivery details

### Real-time Location Updates

- POST `/api/location-updates`: Receive real-time location updates for shipments

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Mapping Service: OpenStreetMap API (for geocoding)
- Real-time Tracking: Google Maps API (for route optimization)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export OPENSTREETMAP_API_KEY=your_openstreetmap_api_key_here 
export GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
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

- Implement rate limiting to prevent abuse of tracking endpoints
- Use strong encryption for storing sensitive shipping data
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
