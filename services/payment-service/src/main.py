from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .database import get_db, engine, Base
from .models import User, Payment, Refund, Dispute

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class PaymentRequest(BaseModel):
    user_id: int
    amount: float

class RefundRequest(BaseModel):
    payment_id: int
    reason: str

class DisputeRequest(BaseModel):
    payment_id: int
    description: str

class PaymentResponse(PaymentRequest):
    id: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RefundResponse(BaseModel):
    id: int
    payment_id: int
    reason: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DisputeResponse(BaseModel):
    id: int
    payment_id: int
    description: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

@app.post("/api/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    # Check for user existence logic
    user = db.query(User).filter(User.id == payment.user_id).first()
    if not user:
         # Auto-create for simplicity in this microservice demo if not found
         user = User(id=payment.user_id, name="Test User", email=f"test{payment.user_id}@example.com")
         db.add(user)
         db.commit()

    new_payment = Payment(user_id=payment.user_id, amount=payment.amount, status="completed")
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@app.get("/api/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.patch("/api/payments/{payment_id}", response_model=PaymentResponse)
def update_payment_status(payment_id: int, status: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = status
    db.commit()
    db.refresh(payment)
    return payment

@app.get("/api/payments/history/{user_id}", response_model=List[PaymentResponse])
def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    return payments

@app.post("/api/refunds", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
def create_refund(refund: RefundRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == refund.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    new_refund = Refund(payment_id=payment.id, reason=refund.reason, status="pending")
    db.add(new_refund)
    db.commit()
    db.refresh(new_refund)
    return new_refund

@app.get("/api/refunds/{refund_id}", response_model=RefundResponse)
def get_refund(refund_id: int, db: Session = Depends(get_db)):
    refund = db.query(Refund).filter(Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    return refund

@app.post("/api/disputes", response_model=DisputeResponse, status_code=status.HTTP_201_CREATED)
def create_dispute(dispute: DisputeRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == dispute.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    new_dispute = Dispute(payment_id=payment.id, description=dispute.description, status="open")
    db.add(new_dispute)
    db.commit()
    db.refresh(new_dispute)
    return new_dispute

@app.get("/api/disputes/{dispute_id}", response_model=DisputeResponse)
def get_dispute(dispute_id: int, db: Session = Depends(get_db)):
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute

@app.get("/")
def root():
    return {"message": "Welcome to the Payment Service"}
