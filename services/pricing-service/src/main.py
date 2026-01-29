import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import router
from .health import router as health_router
from .logging_config import setup_logging, get_logger
from .metrics import setup_metrics
from .rate_limit import get_limiter, setup_rate_limiting

# Setup structured logging
logger = setup_logging("pricing-service")

# Setup rate limiter
limiter = get_limiter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting pricing-service")
    # Tables are now managed by Alembic migrations via Helm Job
    # Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down pricing-service")

app = FastAPI(
    title="Pricing Service",
    description="Product pricing and discount management",
    version="1.0.0",
    lifespan=lifespan
)

# Setup Prometheus metrics (exposes /metrics endpoint)
setup_metrics(app, "pricing-service")

# Setup rate limiting
setup_rate_limiting(app, limiter)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """Log all HTTP requests with request ID for tracing."""
    request_id = str(uuid.uuid4())[:8]
    log = get_logger("pricing-service.request")
    
    log.info(f"[{request_id}] {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    log.info(f"[{request_id}] Response: {response.status_code}")
    return response


# Include routers
app.include_router(health_router)
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Pricing Service API", "version": "1.0.0"}
