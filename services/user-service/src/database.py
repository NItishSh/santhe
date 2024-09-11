from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from app.models import Base
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


create_db()
run_migrations()
