from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User, Payment, Refund, Dispute

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

@app.post("/api/payments")
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_payment = Payment(user=user, amount=payment.amount)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return {"payment_id": new_payment.id}

@app.get("/api/payments/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.patch("/api/payments/{payment_id}")
def update_payment_status(payment_id: int, status: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = status
    db.commit()
    return {"status": "updated"}

@app.get("/api/payments/history/{user_id}")
def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    return payments

@app.post("/api/refunds")
def create_refund(refund: RefundRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == refund.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    new_refund = Refund(payment=payment, reason=refund.reason)
    db.add(new_refund)
    db.commit()
    db.refresh(new_refund)
    return {"refund_id": new_refund.id}

@app.get("/api/refunds/{refund_id}")
def get_refund(refund_id: int, db: Session = Depends(get_db)):
    refund = db.query(Refund).filter(Refund.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    return refund

@app.post("/api/disputes")
def create_dispute(dispute: DisputeRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == dispute.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    new_dispute = Dispute(payment=payment, description=dispute.description)
    db.add(new_dispute)
    db.commit()
    db.refresh(new_dispute)
    return {"dispute_id": new_dispute.id}

@app.get("/api/disputes/{dispute_id}")
def get_dispute(dispute_id: int, db: Session = Depends(get_db)):
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute
