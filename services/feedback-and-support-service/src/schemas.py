from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    user_id: int
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: str

class TicketResponse(TicketCreate):
    id: int
    status: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class TopicCreate(BaseModel):
    name: str

class TopicResponse(TopicCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ArticleCreate(BaseModel):
    topic_id: int
    title: str
    content: str

class ArticleResponse(ArticleCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    user_id: int
    message: str

class EmailSupportRequest(BaseModel):
    user_id: int
    subject: str
    body: str

class SocialMediaPostRequest(BaseModel):
    platform: str
    message: str
