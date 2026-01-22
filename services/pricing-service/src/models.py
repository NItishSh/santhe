from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True) # Assuming products table exists elsewhere or we mock it
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    bid_amount = Column(Float)
    bidder_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
