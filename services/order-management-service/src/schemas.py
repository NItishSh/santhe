from pydantic import BaseModel, ConfigDict

class OrderBase(BaseModel):
    farmer_id: int
    middleman_id: int
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str

class OrderResponse(OrderBase):
    order_id: int
    status: str
    
    model_config = ConfigDict(from_attributes=True)
