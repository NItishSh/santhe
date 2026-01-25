from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import FeedbackTicket, Topic, Article

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# Support Tickets
@app.post("/api/support/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_support_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = FeedbackTicket(
        user_id=ticket.user_id,
        subject=ticket.subject,
        description=ticket.description,
        status="open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.get("/api/support/tickets", response_model=List[TicketResponse])
def get_support_tickets(
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(FeedbackTicket)
    if status:
        query = query.filter(FeedbackTicket.status == status)
    if user_id:
        query = query.filter(FeedbackTicket.user_id == user_id)
    return query.all()

@app.get("/api/support/tickets/{ticket_id}", response_model=TicketResponse)
def get_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@app.patch("/api/support/tickets/{ticket_id}", response_model=TicketResponse)
def update_support_ticket(ticket_id: int, update: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db_ticket.status = update.status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.delete("/api/support/tickets/{ticket_id}")
def close_support_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db_ticket.status = "closed"
    db.commit()
    return {"message": "Ticket closed successfully"}

# Feedback
# Mapping feedback endpoints to support tickets with specific subject prefix or separate model? 
# For now, simplistic mapping to same ticket system or separate if needed. README implied distinct but structure is similar.
# Let's verify existing implement... "FeedbackTicket" model was used for /api/feedback.
# We will alias /api/feedback to creating a ticket with subject prefix "[Feedback]" to keep it simple or distinct 
# actually README says /api/feedback => Submit feedback. We can use the same model.

@app.post("/api/feedback", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(ticket: TicketCreate, db: Session = Depends(get_db)):
    # Same logic as tickets, maybe distinct status or type field if we extended model, but strictly following schema request:
    db_ticket = FeedbackTicket(
        user_id=ticket.user_id,
        subject=f"[Feedback] {ticket.subject}",
        description=ticket.description,
        status="new"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.get("/api/feedback/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    total = db.query(FeedbackTicket).count()
    open_count = db.query(FeedbackTicket).filter(FeedbackTicket.status == "open").count()
    return {"total_feedback": total, "open_feedback": open_count}

# Knowledge Base
@app.get("/api/knowledge-base/topics", response_model=List[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return db.query(Topic).all()

@app.post("/api/knowledge-base/topics", response_model=TopicResponse)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    new_topic = Topic(name=topic.name)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@app.get("/api/knowledge-base/articles/{topic_id}", response_model=List[ArticleResponse])
def list_articles(topic_id: int, db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.topic_id == topic_id).all()

@app.post("/api/knowledge-base/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    new_article = Article(**article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# Multi-channel Support Stub
@app.post("/api/support/chat")
def initiate_chat(request: ChatRequest):
    # Stub
    return {"message": "Chat initiated", "session_id": "mock-session-123"}

@app.post("/api/support/email")
def send_email_support(request: EmailSupportRequest):
    # Stub
    return {"message": "Email sent to support team"}

@app.post("/api/support/social-media")
def post_social_media_support(request: SocialMediaPostRequest):
    # Stub
    return {"message": f"Posted to {request.platform}"}

@app.get("/")
def root():
    return {"message": "Welcome to the Feedback and Support Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)