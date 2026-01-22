from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import Delivery

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

@app.post("/api/deliveries", response_model=DeliveryResponse)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)