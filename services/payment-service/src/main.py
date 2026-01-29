from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db, engine, Base
from .schemas import (
    PaymentRequest, PaymentResponse, 
    RefundRequest, RefundResponse, 
    DisputeRequest, DisputeResponse
)
from .services import PaymentService

# Tables managed by Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    return PaymentService.create_payment(db, payment)

@app.get("/api/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.patch("/api/payments/{payment_id}", response_model=PaymentResponse)
def update_payment_status(payment_id: int, status: str, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return PaymentService.update_payment_status(db, payment, status)

@app.get("/api/payments/history/{user_id}", response_model=List[PaymentResponse])
def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    return PaymentService.get_user_history(db, user_id)

@app.post("/api/refunds", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
def create_refund(refund: RefundRequest, db: Session = Depends(get_db)):
    result = PaymentService.create_refund(db, refund)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result

@app.get("/api/refunds/{refund_id}", response_model=RefundResponse)
def get_refund(refund_id: int, db: Session = Depends(get_db)):
    refund = PaymentService.get_refund(db, refund_id)
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    return refund

@app.post("/api/disputes", response_model=DisputeResponse, status_code=status.HTTP_201_CREATED)
def create_dispute(dispute: DisputeRequest, db: Session = Depends(get_db)):
    result = PaymentService.create_dispute(db, dispute)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result

@app.get("/api/disputes/{dispute_id}", response_model=DisputeResponse)
def get_dispute(dispute_id: int, db: Session = Depends(get_db)):
    dispute = PaymentService.get_dispute(db, dispute_id)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute

@app.get("/")
def root():
    return {"message": "Welcome to the Payment Service"}
