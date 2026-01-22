from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import FeedbackTicket

# Create tables
Base.metadata.create_all(bind=engine)

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

@app.post("/api/feedback", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = FeedbackTicket(
        user_id=ticket.user_id,
        subject=ticket.subject,
        description=ticket.description
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.get("/api/feedback", response_model=List[TicketResponse])
def get_tickets(
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

@app.patch("/api/feedback/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, update: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db_ticket.status = update.status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)