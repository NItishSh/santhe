# src/models.py

from sqlalchemy import Column, Integer, String, Enum
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, nullable=False)
    middleman_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum("pending", "in_progress", "completed", "cancelled", name="order_status"), default="pending")

    def __repr__(self):
        return f"Order(order_id={self.order_id}, farmer_id={self.farmer_id}, middleman_id={self.middleman_id}, product_id={self.product_id}, quantity={self.quantity}, status={self.status})"
