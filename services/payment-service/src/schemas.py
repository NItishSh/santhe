from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PaymentRequest(BaseModel):
    user_id: int
    amount: float

class PaymentResponse(PaymentRequest):
    id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RefundRequest(BaseModel):
    payment_id: int
    reason: str

class RefundResponse(BaseModel):
    id: int
    payment_id: int
    reason: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DisputeRequest(BaseModel):
    payment_id: int
    description: str

class DisputeResponse(BaseModel):
    id: int
    payment_id: int
    description: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
