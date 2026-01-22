from sqlalchemy import Column, Integer, String, Float
from .database import Base
import uuid

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rating = Column(Float, nullable=False)
    content = Column(String, nullable=False)
    reviewer_id = Column(Integer, nullable=False)
    reviewed_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Review(id={self.id}, rating={self.rating}, content={self.content}, reviewer_id={self.reviewer_id}, reviewed_id={self.reviewed_id})"
