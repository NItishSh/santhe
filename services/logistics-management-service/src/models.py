from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True, nullable=False)
    driver_id = Column(Integer, index=True, nullable=True)
    status = Column(String, default="pending", index=True) # pending, in_transit, delivered
    location = Column(String, nullable=True) # Could be JSON or just string "lat,long"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Establish a relationship if tracking history is needed, but we can keep it simple.
    
    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "driver_id": self.driver_id,
            "status": self.status,
            "location": self.location,
            "timestamp": self.timestamp
        }

class Shipping(Base):
    __tablename__ = "shipping"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, unique=True, index=True)
    carrier = Column(String)
    tracking_number = Column(String)
    shipping_label_url = Column(String)
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
