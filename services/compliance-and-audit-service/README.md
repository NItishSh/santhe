# Compliance and Audit Service for Santhe Platform

## Overview

The Compliance and Audit Service is responsible for ensuring regulatory adherence and maintaining transparency throughout the Santhe platform. It manages compliance checks, audit logs, and reporting for various business activities.

## Features

- Regulatory Compliance Checks
- Audit Log Management
- Compliance Reporting
- Automated Risk Assessment

## API Endpoints

### Compliance Checks

- POST `/api/compliance/checks`: Perform a compliance check
- GET `/api/compliance/results/{checkId}`: Retrieve compliance check results

### Audit Logs

- POST `/api/logs`: Create a new audit log entry
- GET `/api/logs`: Retrieve all audit logs
- GET `/api/logs/{logId}`: Retrieve a specific audit log details

### Compliance Reports

- POST `/api/reports/generate`: Generate a compliance report
- GET `/api/reports/{reportId}`: Download generated report

### Risk Assessment

- POST `/api/risk-assessment`: Conduct automated risk assessment
- GET `/api/risk-assessment/results/{assessmentId}`: Retrieve risk assessment results

## Dependencies

- Database: PostgreSQL
- ORM: SQLAlchemy
- API Framework: FastAPI
- Compliance Tools: OWASP ZAP (for vulnerability scanning)
- Reporting Engine: JasperReports (for generating compliance reports)

## Setup and Running

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set environment variables:
```
export DATABASE_URL=postgresql://user:password@host:port/dbname 
export OWASP_ZAP_URL=https://your-owasp-zap-url.com 
export JASPERREPORTS_SERVER=your_jasperreports_server_url_here
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

- Implement strict access controls for compliance-related endpoints
- Use strong encryption for storing sensitive audit logs
- Regularly update dependencies and security patches

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
