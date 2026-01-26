import uuid
from sqlalchemy.orm import Session
from typing import Optional
from .models import Notification, Preference
from .schemas import NotificationCreate, PreferenceUpdate
from .utils import send_sms, send_email, send_in_app_notification

class NotificationService:
    @staticmethod
    def create_notification(db: Session, notification: NotificationCreate) -> Notification:
        new_notification = Notification(**notification.model_dump(), id=str(uuid.uuid4()))
        db.add(new_notification)
        # Commit to save initial state? Or wait.
        # Original logic saved first, then updated status.
        # We can replicate:
        db.commit()
        db.refresh(new_notification)

        # Logic to send
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
        except Exception:
            new_notification.status = "failed"
            # Log error ideally
        
        db.commit()
        db.refresh(new_notification)
        return new_notification

    @staticmethod
    def get_notification(db: Session, notification_id: str) -> Optional[Notification]:
        return db.query(Notification).filter(Notification.id == notification_id).first()

    @staticmethod
    def update_notification_status(db: Session, notification: Notification, status: str) -> Notification:
        notification.status = status
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_preferences(db: Session, user_id: int) -> Optional[Preference]:
        return db.query(Preference).filter(Preference.user_id == user_id).first()

    @staticmethod
    def update_preferences(db: Session, user_id: int, preferences_data: PreferenceUpdate) -> Preference:
        existing_preference = NotificationService.get_preferences(db, user_id)
        if not existing_preference:
            new_preference = Preference(**preferences_data.model_dump(), id=str(uuid.uuid4()))
            db.add(new_preference)
            db.commit()
            db.refresh(new_preference)
            return new_preference
        else:
            existing_preference.sms_enabled = preferences_data.sms_enabled
            existing_preference.email_enabled = preferences_data.email_enabled
            existing_preference.in_app_enabled = preferences_data.in_app_enabled
            db.commit()
            db.refresh(existing_preference)
            return existing_preference
