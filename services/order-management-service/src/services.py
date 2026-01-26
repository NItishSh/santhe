from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Order as OrderModel
from .schemas import OrderCreate, OrderUpdate

class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate) -> OrderModel:
        db_order = OrderModel(**order.model_dump(), status="pending")
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def get_orders(db: Session) -> List[OrderModel]:
        return db.query(OrderModel).all()

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Optional[OrderModel]:
        return db.query(OrderModel).filter(OrderModel.order_id == order_id).first()

    @staticmethod
    def update_order_status(db: Session, order: OrderModel, update_data: OrderUpdate) -> OrderModel:
        order.status = update_data.status
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete_order(db: Session, order: OrderModel) -> None:
        db.delete(order)
        db.commit()
