from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db, engine, Base
from .schemas import (
    ReviewCreate, ReviewUpdate, ReviewResponse,
    Rating, ModerationRequest
)
from .services import ReviewService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return ReviewService.create_review(db, review)

@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    return ReviewService.get_all_reviews(db)

@app.get("/api/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = ReviewService.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.patch("/api/reviews/{review_id}", response_model=ReviewResponse)
def update_review(review_id: str, rating: int = None, content: str = None, db: Session = Depends(get_db)):
    # Note: Using query params in original code for update?
    # Original: def update_review(review_id: str, rating: int, content: str, ...)
    # This implies query parameters if not Pydantic model.
    # To keep API contract same, we accept them as params and create update object.
    
    review_update = ReviewUpdate(rating=rating, content=content)
    review = ReviewService.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return ReviewService.update_review(db, review, review_update)

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str, db: Session = Depends(get_db)):
    review = ReviewService.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    ReviewService.delete_review(db, review)
    return {"message": "Review deleted"}

@app.get("/api/ratings/{user_id}")
def get_average_rating(user_id: int, db: Session = Depends(get_db)):
    average = ReviewService.get_average_rating(db, user_id)
    return {"average_rating": average}

@app.post("/api/ratings")
def rate_user(rating: Rating, db: Session = Depends(get_db)):
    # Returns {"review_id": ...}
    new_review = ReviewService.rate_user(db, rating)
    return {"review_id": new_review.id}

@app.post("/api/moderate")
def flag_for_moderation(request: ModerationRequest, db: Session = Depends(get_db)):
    review = ReviewService.flag_for_moderation(db, request)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review flagged for moderation"}

@app.get("/api/moderated-reviews", response_model=List[ReviewResponse])
def get_moderated_reviews(db: Session = Depends(get_db)):
    return ReviewService.get_moderated_reviews(db)
