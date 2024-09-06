# Analytics and Reporting Service for Santhe Platform

## Overview

The Analytics and Reporting Service is responsible for collecting, analyzing, and presenting data insights across various aspects of the Santhe platform. It generates reports on sales trends, user behavior, and operational performance to support decision-making.

## Features

- Data Collection from Various Services
- Advanced Analytics
- Customizable Reports
- Real-time Dashboards

## API Endpoints

### Data Collection

- POST `/api/analytics/data`: Submit raw data points for analysis
- GET `/api/analytics/status`: Check status of data collection jobs

### Analytics Jobs

- POST `/api/analytics/jobs`: Schedule an analytics job
- GET `/api/analytics/jobs/{jobId}`: Retrieve details of a scheduled job

### Report Generation

- POST `/api/reports/generate`: Generate a custom report
- GET `/api/reports/{reportId}`: Download generated report

### Dashboard Management

- GET `/api/dashboards`: List available dashboards
- POST `/api/dashboards`: Create a new dashboard
- PATCH `/api/dashboards/{dashboardId}`: Update an existing dashboard

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Analytics Engine: Apache Superset (for interactive dashboards)
- Visualization Library: Matplotlib (for generating reports)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export SUPERTABLE_URL=https://your-supertable-url.com 
export MATPLOTLIB_BACKEND=Agg
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

- Implement rate limiting to prevent abuse of data submission endpoints
- Use strong encryption for storing sensitive data
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
