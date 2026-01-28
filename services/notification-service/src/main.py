import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import router
from .health import router as health_router
from .logging_config import setup_logging, get_logger

logger = setup_logging("notification-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting notification-service")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down notification-service")

app = FastAPI(
    title="Notification Service",
    description="Email, SMS, and push notifications",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    log = get_logger("notification-service.request")
    log.info(f"[{request_id}] {request.method} {request.url.path}")
    response = await call_next(request)
    log.info(f"[{request_id}] Response: {response.status_code}")
    return response

app.include_router(health_router)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Notification Service API", "version": "1.0.0"}
