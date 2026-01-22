from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base
import json

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    action = Column(String, index=True, nullable=False)
    resource = Column(String, nullable=True)
    details = Column(Text, nullable=True) # JSON payload as text
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource": self.resource,
            "details": json.loads(self.details) if self.details else None,
            "timestamp": self.timestamp
        }
