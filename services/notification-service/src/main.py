from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List
from .database import get_db, engine, Base
from .models import Notification, Preference
import uuid
from .utils import send_sms, send_email, send_in_app_notification

# Create tables if not exist (simplification for now, usually Alembic)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic models
class NotificationBase(BaseModel):
    title: str
    content: str
    recipient_id: int
    notification_type: str

class NotificationResponse(NotificationBase):
    id: uuid.UUID
    status: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class PreferenceBase(BaseModel):
    user_id: int
    sms_enabled: bool
    email_enabled: bool
    in_app_enabled: bool

class PreferenceResponse(PreferenceBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)


@app.post("/api/notifications", response_model=dict)
async def create_notification(notification: NotificationBase, db: Session = Depends(get_db)):
    new_notification = Notification(**notification.model_dump(), id=str(uuid.uuid4()))
    # Default status?
    
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    # Send notification based on type
    try:
        if notification.notification_type == "sms":
            send_sms(notification.recipient_id, notification.title, notification.content)
            new_notification.status = "sent"
        elif notification.notification_type == "email":
            send_email(notification.recipient_id, notification.title, notification.content)
            new_notification.status = "sent"
        elif notification.notification_type == "in-app":
            send_in_app_notification(notification.recipient_id, notification.title, notification.content)
            new_notification.status = "sent"
        else:
             new_notification.status = "unknown_type"
    except Exception as e:
        new_notification.status = "failed"
        # Log error?

    db.commit()
    return {"notification_id": new_notification.id}

@app.get("/api/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, db: Session = Depends(get_db)): # ID is stored as string in model?
    # Model says: id = Column(String(36)
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.patch("/api/notifications/{notification_id}")
async def update_notification_status(notification_id: str, status: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.status = status
    db.commit()
    return {"message": f"Notification {notification_id} status updated to {status}"}

@app.get("/api/preferences/{user_id}", response_model=PreferenceResponse)
async def get_preferences(user_id: int, db: Session = Depends(get_db)):
    preference = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not preference:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preference

@app.patch("/api/preferences/{user_id}")
async def update_preferences(user_id: int, preferences: PreferenceBase, db: Session = Depends(get_db)):
    existing_preference = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not existing_preference:
        new_preference = Preference(**preferences.model_dump(), id=str(uuid.uuid4()))
        db.add(new_preference)
    else:
        existing_preference.sms_enabled = preferences.sms_enabled
        existing_preference.email_enabled = preferences.email_enabled
        existing_preference.in_app_enabled = preferences.in_app_enabled
    
    db.commit()
    return {"message": f"Preferences for user {user_id} updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
