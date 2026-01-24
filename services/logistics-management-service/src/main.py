from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import Delivery, Shipping

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class DeliveryCreate(BaseModel):
    order_id: int
    driver_id: Optional[int] = None
    location: Optional[str] = None

class DeliveryUpdate(BaseModel):
    status: Optional[str] = None
    location: Optional[str] = None
    driver_id: Optional[int] = None

class DeliveryResponse(DeliveryCreate):
    id: int
    status: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class ShippingCreate(BaseModel):
    order_id: int
    carrier: str
    tracking_number: str
    shipping_label_url: Optional[str] = None

class ShippingUpdate(BaseModel):
    status: str

class ShippingResponse(ShippingCreate):
    id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LocationUpdate(BaseModel):
    order_id: int
    latitude: float
    longitude: float

class TrackingResponse(BaseModel):
    order_id: int
    status: str
    location: Optional[str]
    timestamp: datetime
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None

@app.post("/api/deliveries", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = Delivery(
        order_id=delivery.order_id,
        driver_id=delivery.driver_id,
        location=delivery.location
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.get("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_delivery

@app.patch("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, update: DeliveryUpdate, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    if update.status:
        db_delivery.status = update.status
    if update.location:
        db_delivery.location = update.location
    if update.driver_id is not None:
        db_delivery.driver_id = update.driver_id
        
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.get("/api/orders/{order_id}/tracking", response_model=TrackingResponse)
def get_order_tracking(order_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    shipping = db.query(Shipping).filter(Shipping.order_id == order_id).first()
    
    if not delivery and not shipping:
        raise HTTPException(status_code=404, detail="Tracking info not found for order")

    # Merge logic or prioritize delivery if active
    current_status = delivery.status if delivery else (shipping.status if shipping else "unknown")
    location = delivery.location if delivery else None
    
    return TrackingResponse(
        order_id=order_id,
        status=current_status,
        location=location,
        timestamp=datetime.utcnow(), 
        carrier=shipping.carrier if shipping else None,
        tracking_number=shipping.tracking_number if shipping else None
    )

@app.post("/api/orders/{order_id}/track")
def update_order_tracking(order_id: int, status: str, db: Session = Depends(get_db)):
    # This endpoint updates the 'Delivery' status mainly
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if not delivery:
         # Create if not exists? Or 404. Let's create for robustness in this simple logic
         delivery = Delivery(order_id=order_id, status=status)
         db.add(delivery)
    else:
         delivery.status = status
    
    db.commit()
    return {"message": "Tracking status updated"}

@app.post("/api/shipping", response_model=ShippingResponse, status_code=status.HTTP_201_CREATED)
def create_shipping(shipping: ShippingCreate, db: Session = Depends(get_db)):
    new_shipping = Shipping(**shipping.model_dump())
    db.add(new_shipping)
    db.commit()
    db.refresh(new_shipping)
    return new_shipping

@app.get("/api/shipping/{shipping_id}", response_model=ShippingResponse)
def get_shipping(shipping_id: int, db: Session = Depends(get_db)):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping info not found")
    return shipping

@app.patch("/api/shipping/{shipping_id}", response_model=ShippingResponse)
def update_shipping(shipping_id: int, update: ShippingUpdate, db: Session = Depends(get_db)):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping info not found")
    shipping.status = update.status
    db.commit()
    db.refresh(shipping)
    return shipping

@app.post("/api/location-updates")
def update_location(update: LocationUpdate, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.order_id == update.order_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Active delivery not found for order")
    
    delivery.location = f"{update.latitude},{update.longitude}"
    db.commit()
    return {"message": "Location updated"}

@app.get("/")
def root():
    return {"message": "Welcome to the Logistics Management Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)