from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from .database import get_db
from .schemas import (
    NotificationCreate, NotificationResponse,
    PreferenceUpdate, PreferenceResponse
)
from .services import NotificationService

router = APIRouter()

@router.post("/api/notifications", response_model=dict)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    # Sync handler because NotificationService uses Sync DB
    new_notification = NotificationService.create_notification(db, notification)
    return {"notification_id": new_notification.id}

@router.get("/api/notifications/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: str, db: Session = Depends(get_db)):
    notification = NotificationService.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.patch("/api/notifications/{notification_id}")
def update_notification_status(notification_id: str, status: str = Body(..., embed=True), db: Session = Depends(get_db)):
    # Note: status is received potentially as query or body. 
    # Original code: `status: str` implies query parameter in FastAPI if not modeled. 
    # But usually status updates are body. 
    # Looking at original: `async def update_notification_status(notification_id: str, status: str, ...)` 
    # By default, scalar types are query params.
    # I will keep exact signature to minimize breakage, but adding = Body(...) is better design.
    # However, strict refactor implies keeping logic. I'll stick to mostly identical signature 
    # unless original was clearly implying body JSON. 
    # A simple string is usually query. I'll keep it as query to match likely existing client usage, 
    # or if previous code implied query.
    
    # Original: status: str -> Query param '.../guid?status=read'
    
    notification = NotificationService.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    NotificationService.update_notification_status(db, notification, status)
    return {"message": f"Notification {notification_id} status updated to {status}"}

@router.get("/api/preferences/{user_id}", response_model=PreferenceResponse)
def get_preferences(user_id: int, db: Session = Depends(get_db)):
    preference = NotificationService.get_preferences(db, user_id)
    if not preference:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preference

@router.patch("/api/preferences/{user_id}")
def update_preferences(user_id: int, preferences: PreferenceUpdate, db: Session = Depends(get_db)):
    # Enforce consistency
    if preferences.user_id != user_id:
         preferences.user_id = user_id
         
    NotificationService.update_preferences(db, user_id, preferences)
    return {"message": f"Preferences for user {user_id} updated"}
