from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db, engine, Base
from .schemas import OrderCreate, OrderUpdate, OrderResponse
from .services import OrderService

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/api/orders", response_model=List[OrderResponse])
def read_orders(db: Session = Depends(get_db)):
    return OrderService.get_orders(db)

@app.post("/api/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return OrderService.create_order(db, order)

@app.get("/api/orders/status", response_model=List[dict])
def read_orders_status(db: Session = Depends(get_db)):
    # Specific projection not in Service, but simple enough to keep or move.
    # Moving logic to controller for simple projection of all orders is acceptable 
    # if we don't want a specific service method just for "status only".
    # Or strict layering: OrderService.get_all_statuses(db).
    # I'll use get_orders and map here to avoid bloat, or cleaner: keep logic here.
    orders = OrderService.get_orders(db)
    return [{"order_id": o.order_id, "status": o.status} for o in orders]

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.patch("/api/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, update: OrderUpdate, db: Session = Depends(get_db)):
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderService.update_order_status(db, order, update)

@app.delete("/api/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
         raise HTTPException(status_code=404, detail="Order not found")
    OrderService.delete_order(db, order)
    return {"message": "Order deleted successfully"}

@app.get("/api/orders/{order_id}/status", response_model=dict)
def read_order_status(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order_by_id(db, order_id)
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
