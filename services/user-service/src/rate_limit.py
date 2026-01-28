"""Rate limiting configuration for FastAPI services."""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import os


def get_limiter():
    """Create a rate limiter instance."""
    return Limiter(
        key_func=get_remote_address,
        default_limits=["100/minute"],  # Default: 100 requests per minute per IP
        storage_uri=os.getenv("REDIS_URL", "memory://"),
        strategy="fixed-window",
    )


def setup_rate_limiting(app, limiter: Limiter):
    """Configure rate limiting for the FastAPI app."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    
    return limiter


# Decorators for custom rate limits on specific endpoints
# Usage: @limiter.limit("10/minute")
# Apply to routes that need stricter limits (e.g., login, registration)
