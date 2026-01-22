from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .database import get_db, engine, Base
from .models import Review
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic models
class ReviewBase(BaseModel):
    rating: int
    content: str
    reviewer_id: int
    reviewed_id: int

class ReviewResponse(ReviewBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class Rating(BaseModel):
    rating: int
    rated_user_id: int

class ModerationRequest(BaseModel):
    review_id: str
    reason: str

@app.post("/api/reviews", response_model=ReviewResponse)
def create_review(review: ReviewBase, db: Session = Depends(get_db)):
    new_review = Review(**review.model_dump(), id=str(uuid.uuid4()))
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@app.get("/api/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.patch("/api/reviews/{review_id}", response_model=ReviewResponse)
def update_review(review_id: str, rating: int, content: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.rating = rating
    review.content = content
    db.commit()
    db.refresh(review)
    return review

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

@app.get("/api/ratings/{user_id}")
def get_average_rating(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Review.rating).filter(Review.reviewed_id == user_id).all()
    if not ratings:
        return {"average_rating": None}
    average = sum(r[0] for r in ratings) / len(ratings)
    return {"average_rating": average}

@app.post("/api/ratings")
def rate_user(rating: Rating, db: Session = Depends(get_db)):
    new_review = Review(
        rating=rating.rating,
        content="",
        reviewer_id=rating.rated_user_id, # Simplified logic from original code, though typically reviewer != reviewed
        reviewed_id=rating.rated_user_id, 
        id=str(uuid.uuid4())
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"review_id": new_review.id}

@app.post("/api/moderate")
def flag_for_moderation(request: ModerationRequest, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == request.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if not review.content.startswith("[MODERATED]"):
        review.content = "[MODERATED] " + review.content
        db.commit()
    return {"message": "Review flagged for moderation"}

@app.get("/api/moderated-reviews", response_model=List[ReviewResponse])
def get_moderated_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.content.like("[MODERATED]%")).all()
