# src/main.py

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from config.settings import settings
import uuid

# Database setup
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class ReviewBase(BaseModel):
    rating: int
    content: str
    reviewer_id: int
    reviewed_id: int

class Review(ReviewBase):
    id: uuid.UUID

class Rating(BaseModel):
    rating: int
    rated_user_id: int

class ModerationRequest(BaseModel):
    review_id: uuid.UUID
    reason: str

app = FastAPI()

@app.post("/api/reviews")
async def create_review(review: ReviewBase, db: Session = Depends(get_db)):
    new_review = Review(**review.dict(), id=uuid.uuid4())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"review_id": new_review.id}

@app.get("/api/reviews")
async def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return [{"id": r.id, "rating": r.rating, "content": r.content, "reviewer_id": r.reviewer_id, "reviewed_id": r.reviewed_id} for r in reviews]

@app.get("/api/reviews/{review_id}")
async def get_review(review_id: uuid.UUID, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return {"error": "Review not found"}
    return {"id": review.id, "rating": review.rating, "content": review.content, "reviewer_id": review.reviewer_id, "reviewed_id": review.reviewed_id}

@app.patch("/api/reviews/{review_id}")
async def update_review(review_id: uuid.UUID, rating: int, content: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return {"error": "Review not found"}
    review.rating = rating
    review.content = content
    db.commit()
    return {"id": review.id, "rating": review.rating, "content": review.content}

@app.delete("/api/reviews/{review_id}")
async def delete_review(review_id: uuid.UUID, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return {"error": "Review not found"}
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

@app.get("/api/ratings/{user_id}")
async def get_average_rating(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Review.rating).filter(Review.reviewed_id == user_id).all()
    if not ratings:
        return {"average_rating": None}
    average = sum(rating[0] for rating in ratings) / len(ratings)
    return {"average_rating": average}

@app.post("/api/ratings")
async def rate_user(rating: Rating, db: Session = Depends(get_db)):
    new_review = Review(**rating.dict(), content="", reviewer_id=rating.rated_user_id, reviewed_id=rating.rated_user_id, id=uuid.uuid4())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"review_id": new_review.id}

@app.post("/api/moderate")
async def flag_for_moderation(request: ModerationRequest, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == request.review_id).first()
    if not review:
        return {"error": "Review not found"}
    review.content = "[MODERATED] " + review.content
    db.commit()
    return {"message": "Review flagged for moderation"}

@app.get("/api/moderated-reviews")
async def get_moderated_reviews(db: Session = Depends(get_db)):
    moderated_reviews = db.query(Review).filter(Review.content.startswith("[MODERATED]")).all()
    return [{"id": r.id, "rating": r.rating, "content": r.content, "reviewer_id": r.reviewer_id, "reviewed_id": r.reviewed_id} for r in moderated_reviews]
