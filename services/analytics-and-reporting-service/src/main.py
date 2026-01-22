from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import AnalyticsEvent
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class EventCreate(BaseModel):
    event_type: str
    payload: Optional[Dict[str, Any]] = None

class EventResponse(BaseModel):
    id: int
    event_type: str
    timestamp: datetime

@app.post("/api/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = AnalyticsEvent(
        event_type=event.event_type,
        payload=json.dumps(event.payload) if event.payload else None
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/api/reports/daily", response_model=List[Dict[str, Any]])
def get_daily_report(db: Session = Depends(get_db)):
    # Aggregating events by type
    results = db.query(
        AnalyticsEvent.event_type, 
        func.count(AnalyticsEvent.id).label("count")
    ).group_by(AnalyticsEvent.event_type).all()
    
    return [{"event_type": r[0], "count": r[1]} for r in results]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)