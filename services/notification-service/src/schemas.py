from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

class NotificationBase(BaseModel):
    title: str
    content: str
    recipient_id: int
    notification_type: str

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: uuid.UUID
    status: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class PreferenceBase(BaseModel):
    user_id: int
    sms_enabled: bool
    email_enabled: bool
    in_app_enabled: bool

class PreferenceCreate(PreferenceBase):
    pass

class PreferenceUpdate(PreferenceBase):
    pass

class PreferenceResponse(PreferenceBase):
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)
