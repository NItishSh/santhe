from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base
import json

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True, nullable=False)
    payload = Column(Text, nullable=True) # Storing JSON payload as text
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "payload": json.loads(self.payload) if self.payload else None,
            "timestamp": self.timestamp
        }
