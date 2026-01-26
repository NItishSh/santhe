from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .schemas import (
    NotificationCreate, NotificationResponse,
    PreferenceUpdate, PreferenceResponse
)
from .services import NotificationService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/notifications", response_model=dict)
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = NotificationService.create_notification(db, notification)
    return {"notification_id": new_notification.id}

@app.get("/api/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(notification_id: str, db: Session = Depends(get_db)):
    notification = NotificationService.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.patch("/api/notifications/{notification_id}")
async def update_notification_status(notification_id: str, status: str, db: Session = Depends(get_db)):
    notification = NotificationService.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    NotificationService.update_notification_status(db, notification, status)
    return {"message": f"Notification {notification_id} status updated to {status}"}

@app.get("/api/preferences/{user_id}", response_model=PreferenceResponse)
async def get_preferences(user_id: int, db: Session = Depends(get_db)):
    preference = NotificationService.get_preferences(db, user_id)
    if not preference:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preference

@app.patch("/api/preferences/{user_id}")
async def update_preferences(user_id: int, preferences: PreferenceUpdate, db: Session = Depends(get_db)):
    # Note: Logic in main.py was "update or create". Service handles this.
    # We should ensure the route/schema aligns. preferences model has user_id, 
    # but route param also has user_id. We trust route param or body?
    # Original main.py used body user_id in PreferenceBase.
    
    # We should enforce consistency or override body user_id with path param
    if preferences.user_id != user_id:
         # Optional: raise error or overwrite. Overwriting is safer for path consistency.
         preferences.user_id = user_id
         
    NotificationService.update_preferences(db, user_id, preferences)
    return {"message": f"Preferences for user {user_id} updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
