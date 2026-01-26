import uuid
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from .models import Review
from .schemas import ReviewCreate, ReviewUpdate, Rating, ModerationRequest

class ReviewService:
    @staticmethod
    def create_review(db: Session, review: ReviewCreate) -> Review:
        # Original logic: id=str(uuid.uuid4())
        new_review = Review(
            **review.model_dump(), 
            id=str(uuid.uuid4())
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    @staticmethod
    def get_all_reviews(db: Session) -> List[Review]:
        return db.query(Review).all()

    @staticmethod
    def get_review(db: Session, review_id: str) -> Optional[Review]:
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def update_review(db: Session, review: Review, update: ReviewUpdate) -> Review:
        if update.rating is not None:
            review.rating = update.rating
        if update.content is not None:
            review.content = update.content
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete_review(db: Session, review: Review) -> None:
        db.delete(review)
        db.commit()

    @staticmethod
    def get_average_rating(db: Session, user_id: int) -> float | None:
        ratings = db.query(Review.rating).filter(Review.reviewed_id == user_id).all()
        if not ratings:
            return None
        # ratings is list of tuples [(val,), (val,)]
        average = sum(r[0] for r in ratings) / len(ratings)
        return average

    @staticmethod
    def rate_user(db: Session, rating: Rating) -> Review:
        # Simplified logic from main.py: create a review with empty content
        new_review = Review(
            rating=rating.rating,
            content="",
            reviewer_id=rating.rated_user_id, # Simplified logic as per main.py
            reviewed_id=rating.rated_user_id,
            id=str(uuid.uuid4())
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    @staticmethod
    def flag_for_moderation(db: Session, request: ModerationRequest) -> Optional[Review]:
        review = ReviewService.get_review(db, request.review_id)
        if not review:
            return None
        
        if not review.content.startswith("[MODERATED]"):
            review.content = "[MODERATED] " + review.content
            db.commit()
            db.refresh(review)
        return review

    @staticmethod
    def get_moderated_reviews(db: Session) -> List[Review]:
        return db.query(Review).filter(Review.content.like("[MODERATED]%")).all()
