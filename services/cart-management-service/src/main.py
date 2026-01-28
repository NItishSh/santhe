from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (Create tables)
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
