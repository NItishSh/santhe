from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
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

class AnalyticsJob(Base):
    __tablename__ = "analytics_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String, index=True)
    status = Column(String, default="pending") # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    result = Column(Text, nullable=True)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String)
    parameters = Column(Text, nullable=True) # JSON
    generated_at = Column(DateTime, default=datetime.utcnow)
    download_url = Column(String, nullable=True)

class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    configuration = Column(Text) # JSON config for layout/widgets
    created_at = Column(DateTime, default=datetime.utcnow)
