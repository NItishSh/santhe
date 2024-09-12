from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from config.settings import settings
import uuid
from notification_service.utils import send_sms, send_email, send_in_app_notification

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class NotificationBase(BaseModel):
    title: str
    content: str
    recipient_id: int
    notification_type: str

class Notification(NotificationBase):
    id: uuid.UUID

class PreferenceBase(BaseModel):
    user_id: int
    sms_enabled: bool
    email_enabled: bool
    in_app_enabled: bool

class Preference(PreferenceBase):
    id: uuid.UUID

@app.post("/api/notifications")
async def create_notification(notification: NotificationBase, db: Session = Depends(get_db)):
    new_notification = Notification(**notification.dict(), id=uuid.uuid4())
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    # Send notification based on type
    if notification.notification_type == "sms":
        send_sms(notification.recipient_id, notification.title, notification.content)
    elif notification.notification_type == "email":
        send_email(notification.recipient_id, notification.title, notification.content)
    elif notification.notification_type == "in-app":
        send_in_app_notification(notification.recipient_id, notification.title, notification.content)

    return {"notification_id": new_notification.id}

@app.get("/api/notifications/{notification_id}")
async def get_notification(notification_id: uuid.UUID, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"id": notification.id, "title": notification.title, "content": notification.content, "recipient_id": notification.recipient_id}

@app.patch("/api/notifications/{notification_id}")
async def update_notification_status(notification_id: uuid.UUID, status: str, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.status = status
    db.commit()
    return {"message": f"Notification {notification_id} status updated to {status}"}

@app.get("/api/preferences/{user_id}")
async def get_preferences(user_id: int, db: Session = Depends(get_db)):
    preference = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not preference:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return {
        "id": preference.id,
        "user_id": preference.user_id,
        "sms_enabled": preference.sms_enabled,
        "email_enabled": preference.email_enabled,
        "in_app_enabled": preference.in_app_enabled
    }

@app.patch("/api/preferences/{user_id}")
async def update_preferences(user_id: int, preferences: PreferenceBase, db: Session = Depends(get_db)):
    existing_preference = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not existing_preference:
        new_preference = Preference(**preferences.dict(), id=uuid.uuid4())
        db.add(new_preference)
    else:
        existing_preference.sms_enabled = preferences.sms_enabled
        existing_preference.email_enabled = preferences.email_enabled
        existing_preference.in_app_enabled = preferences.in_app_enabled
    
    db.commit()
    return {"message": f"Preferences for user {user_id} updated"}
