from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    notification_type = Column(String, nullable=False)
    status = Column(String, nullable=True)

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, nullable=False, unique=True)
    sms_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
