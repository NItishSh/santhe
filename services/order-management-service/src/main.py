# src/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List
from .database import get_db
from .models import Order as OrderModel

# Pydantic models
class OrderBase(BaseModel):
    farmer_id: int
    middleman_id: int
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    order_id: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    status: str

app = FastAPI()

@app.get("/api/orders", response_model=List[OrderResponse])
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    return orders

@app.post("/api/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderModel(**order.model_dump(), status="pending")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/api/orders/status", response_model=List[dict])
def read_orders_status(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).all()
    return [{"order_id": o.order_id, "status": o.status} for o in orders]

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.patch("/api/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = update.status
    db.commit()
    db.refresh(order)
    return order

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
         raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@app.get("/api/orders/{order_id}/status", response_model=dict)
def read_order_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order.order_id, "status": order.status}

@app.post("/api/notifications")
def send_notification(notification: dict):
    # Implement notification logic here
    return {"message": "Notification sent successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
