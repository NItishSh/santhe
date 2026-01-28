"""Prometheus metrics configuration for FastAPI services."""
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
import time


# Custom metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_REQUESTS = Gauge(
    "http_requests_active",
    "Number of active HTTP requests"
)

DB_QUERY_COUNT = Counter(
    "db_queries_total",
    "Total database queries",
    ["operation"]
)


def setup_metrics(app, service_name: str):
    """Initialize Prometheus metrics for the FastAPI app."""
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/health", "/ready", "/metrics"],
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )
    
    # Add default metrics
    instrumentator.add(
        instrumentator.metrics.default()
    ) if hasattr(instrumentator, 'metrics') else None
    
    # Instrument the app and expose /metrics endpoint
    instrumentator.instrument(app).expose(app, endpoint="/metrics")
    
    return instrumentator
