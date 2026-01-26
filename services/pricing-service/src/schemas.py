from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PriceCreate(BaseModel):
    product_id: int
    price: float
    timestamp: datetime

class PriceUpdate(BaseModel):
    price: Optional[float] = None
    timestamp: Optional[datetime] = None

class PriceResponse(PriceCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BidCreate(BaseModel):
    product_id: int
    bid_amount: float
    bidder_id: int

class BidUpdate(BaseModel):
    bid_amount: float

class BidResponse(BidCreate):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
