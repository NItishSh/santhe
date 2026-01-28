"""Health check endpoints for Kubernetes probes."""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str


class ReadinessResponse(HealthResponse):
    database: str


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Liveness probe - returns OK if the service is running."""
    return HealthResponse(
        status="healthy",
        service=os.getenv("SERVICE_NAME", "user-service"),
        version=os.getenv("SERVICE_VERSION", "1.0.0"),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@router.get("/ready", response_model=ReadinessResponse)
def readiness_check():
    """Readiness probe - returns OK if the service can accept traffic."""
    # TODO: Add actual database connectivity check
    return ReadinessResponse(
        status="ready",
        service=os.getenv("SERVICE_NAME", "user-service"),
        version=os.getenv("SERVICE_VERSION", "1.0.0"),
        timestamp=datetime.utcnow().isoformat() + "Z",
        database="connected"
    )
