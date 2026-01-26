from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db, engine, Base
from .schemas import (
    DeliveryCreate, DeliveryUpdate, DeliveryResponse,
    ShippingCreate, ShippingUpdate, ShippingResponse,
    LocationUpdate, TrackingResponse
)
from .services import LogisticsService

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/deliveries", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    return LogisticsService.create_delivery(db, delivery)

@app.get("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = LogisticsService.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@app.patch("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, update: DeliveryUpdate, db: Session = Depends(get_db)):
    delivery = LogisticsService.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    return LogisticsService.update_delivery(db, delivery, update)

@app.get("/api/orders/{order_id}/tracking", response_model=TrackingResponse)
def get_order_tracking(order_id: int, db: Session = Depends(get_db)):
    tracking = LogisticsService.get_combined_tracking(db, order_id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking info not found for order")
    return tracking

@app.post("/api/orders/{order_id}/track")
def update_order_tracking(order_id: int, status: str, db: Session = Depends(get_db)):
    # Simple logic to ensure a delivery record exists and update its status
    delivery = LogisticsService.get_delivery_by_order_id(db, order_id)
    if not delivery:
         # Create implicitly
         delivery_create = DeliveryCreate(order_id=order_id, driver_id=None, location=None)
         delivery = LogisticsService.create_delivery(db, delivery_create)
    
    # Update status via service (requires wrapping status in DeliveryUpdate object)
    update = DeliveryUpdate(status=status)
    LogisticsService.update_delivery(db, delivery, update)
    
    return {"message": "Tracking status updated"}

@app.post("/api/shipping", response_model=ShippingResponse, status_code=status.HTTP_201_CREATED)
def create_shipping(shipping: ShippingCreate, db: Session = Depends(get_db)):
    return LogisticsService.create_shipping(db, shipping)

@app.get("/api/shipping/{shipping_id}", response_model=ShippingResponse)
def get_shipping(shipping_id: int, db: Session = Depends(get_db)):
    shipping = LogisticsService.get_shipping(db, shipping_id)
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping info not found")
    return shipping

@app.patch("/api/shipping/{shipping_id}", response_model=ShippingResponse)
def update_shipping(shipping_id: int, update: ShippingUpdate, db: Session = Depends(get_db)):
    shipping = LogisticsService.get_shipping(db, shipping_id)
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping info not found")
    return LogisticsService.update_shipping(db, shipping, update)

@app.post("/api/location-updates")
def update_location(update: LocationUpdate, db: Session = Depends(get_db)):
    result = LogisticsService.update_location(db, update)
    if not result:
        raise HTTPException(status_code=404, detail="Active delivery not found for order")
    return {"message": "Location updated"}

@app.get("/")
def root():
    return {"message": "Welcome to the Logistics Management Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)