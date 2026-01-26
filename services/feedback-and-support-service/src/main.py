from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db, engine, Base
from .schemas import (
    TicketCreate, TicketUpdate, TicketResponse,
    TopicCreate, TopicResponse,
    ArticleCreate, ArticleResponse,
    ChatRequest, EmailSupportRequest, SocialMediaPostRequest
)
from .services import FeedbackService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Support Tickets
@app.post("/api/support/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_support_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_ticket(db, ticket)

@app.get("/api/support/tickets", response_model=List[TicketResponse])
def get_support_tickets(
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return FeedbackService.get_tickets(db, status, user_id)

@app.get("/api/support/tickets/{ticket_id}", response_model=TicketResponse)
def get_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = FeedbackService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.patch("/api/support/tickets/{ticket_id}", response_model=TicketResponse)
def update_support_ticket(ticket_id: int, update: TicketUpdate, db: Session = Depends(get_db)):
    ticket = FeedbackService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return FeedbackService.update_ticket(db, ticket, update)

@app.delete("/api/support/tickets/{ticket_id}")
def close_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = FeedbackService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    FeedbackService.close_ticket(db, ticket)
    return {"message": "Ticket closed successfully"}

# Feedback
@app.post("/api/feedback", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(ticket: TicketCreate, db: Session = Depends(get_db)):
    return FeedbackService.submit_feedback(db, ticket)

@app.get("/api/feedback/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    return FeedbackService.get_feedback_stats(db)

# Knowledge Base
@app.get("/api/knowledge-base/topics", response_model=List[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return FeedbackService.list_topics(db)

@app.post("/api/knowledge-base/topics", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_topic(db, topic)

@app.get("/api/knowledge-base/articles/{topic_id}", response_model=List[ArticleResponse])
def list_articles(topic_id: int, db: Session = Depends(get_db)):
    return FeedbackService.list_articles(db, topic_id)

@app.post("/api/knowledge-base/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    return FeedbackService.create_article(db, article)

# Multi-channel Support Stub
@app.post("/api/support/chat")
def initiate_chat(request: ChatRequest):
    return FeedbackService.initiate_chat(request)

@app.post("/api/support/email")
def send_email_support(request: EmailSupportRequest):
    return FeedbackService.send_email_support(request)

@app.post("/api/support/social-media")
def post_social_media_support(request: SocialMediaPostRequest):
    return FeedbackService.post_social_media(request)

@app.get("/")
def root():
    return {"message": "Welcome to the Feedback and Support Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)