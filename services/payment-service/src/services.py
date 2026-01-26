from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .models import Payment, Refund, Dispute, User
from .schemas import PaymentRequest, RefundRequest, DisputeRequest

class PaymentService:
    @staticmethod
    def create_payment(db: Session, payment: PaymentRequest) -> Payment:
        # Check for user existence
        user = db.query(User).filter(User.id == payment.user_id).first()
        if not user:
             # Auto-create for simplicity as per original logic
             user = User(id=payment.user_id, name="Test User", email=f"test{payment.user_id}@example.com")
             db.add(user)
             db.commit()

        new_payment = Payment(user_id=payment.user_id, amount=payment.amount, status="completed")
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment

    @staticmethod
    def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def update_payment_status(db: Session, payment: Payment, status: str) -> Payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_user_history(db: Session, user_id: int) -> List[Payment]:
        return db.query(Payment).filter(Payment.user_id == user_id).all()

    @staticmethod
    def create_refund(db: Session, refund: RefundRequest) -> Optional[Refund]:
        payment = PaymentService.get_payment(db, refund.payment_id)
        if not payment:
            return None
        
        new_refund = Refund(payment_id=payment.id, reason=refund.reason, status="pending")
        db.add(new_refund)
        db.commit()
        db.refresh(new_refund)
        return new_refund

    @staticmethod
    def get_refund(db: Session, refund_id: int) -> Optional[Refund]:
        return db.query(Refund).filter(Refund.id == refund_id).first()

    @staticmethod
    def create_dispute(db: Session, dispute: DisputeRequest) -> Optional[Dispute]:
        payment = PaymentService.get_payment(db, dispute.payment_id)
        if not payment:
            return None

        new_dispute = Dispute(payment_id=payment.id, description=dispute.description, status="open")
        db.add(new_dispute)
        db.commit()
        db.refresh(new_dispute)
        return new_dispute
    
    @staticmethod
    def get_dispute(db: Session, dispute_id: int) -> Optional[Dispute]:
        return db.query(Dispute).filter(Dispute.id == dispute_id).first()
