from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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
