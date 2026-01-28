from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the Pricing Service"}
