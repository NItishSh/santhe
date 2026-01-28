from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse] = []

    class Config:
        from_attributes = True
