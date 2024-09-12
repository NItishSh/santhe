# src/main.py

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/order_management_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class OrderBase(BaseModel):
    farmer_id: int
    middleman_id: int
    product_id: int
    quantity: int

class Order(OrderBase):
    order_id: int
    status: str

class OrderUpdate(BaseModel):
    status: str

app = FastAPI()

@app.get("/api/orders")
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [{"order_id": o.order_id, "farmer_id": o.farmer_id, "middleman_id": o.middleman_id, "product_id": o.product_id, "quantity": o.quantity, "status": o.status} for o in orders]

@app.post("/api/orders")
def create_order(order: OrderBase, db: Session = Depends(get_db)):
    db_order = Order(**order.dict(), order_id=None, status="pending")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"order_id": db_order.order_id}

@app.get("/api/orders/{order_id}")
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    return {"order_id": order.order_id, "farmer_id": order.farmer_id, "middleman_id": order.middleman_id, "product_id": order.product_id, "quantity": order.quantity, "status": order.status}

@app.patch("/api/orders/{order_id}")
def update_order(order_id: int, update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    order.status = update.status
    db.commit()
    return {"order_id": order.order_id, "status": order.status}

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@app.get("/api/orders/status")
def read_orders_status(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [{"order_id": o.order_id, "status": o.status} for o in orders]

@app.get("/api/orders/{order_id}/status")
def read_order_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    return {"order_id": order.order_id, "status": order.status}

@app.post("/api/notifications")
def send_notification(notification: dict):
    # Implement notification logic here
    return {"message": "Notification sent successfully"}
