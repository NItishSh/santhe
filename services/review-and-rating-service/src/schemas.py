from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

class ReviewBase(BaseModel):
    rating: int
    content: str
    reviewer_id: int
    reviewed_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: str # UUID stored as string
    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    content: Optional[str] = None

class Rating(BaseModel):
    rating: int
    rated_user_id: int

class ModerationRequest(BaseModel):
    review_id: str
    reason: str
