from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from .models import Delivery, Shipping
from .schemas import (
    DeliveryCreate, DeliveryUpdate,
    ShippingCreate, ShippingUpdate,
    LocationUpdate, TrackingResponse
)

class LogisticsService:
    @staticmethod
    def create_delivery(db: Session, delivery: DeliveryCreate) -> Delivery:
        db_delivery = Delivery(
            order_id=delivery.order_id,
            driver_id=delivery.driver_id,
            location=delivery.location
        )
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

    @staticmethod
    def get_delivery(db: Session, delivery_id: int) -> Optional[Delivery]:
        return db.query(Delivery).filter(Delivery.id == delivery_id).first()
    
    @staticmethod
    def get_delivery_by_order_id(db: Session, order_id: int) -> Optional[Delivery]:
        return db.query(Delivery).filter(Delivery.order_id == order_id).first()

    @staticmethod
    def update_delivery(db: Session, delivery: Delivery, update: DeliveryUpdate) -> Delivery:
        if update.status:
            delivery.status = update.status
        if update.location:
            delivery.location = update.location
        if update.driver_id is not None:
            delivery.driver_id = update.driver_id
        db.commit()
        db.refresh(delivery)
        return delivery

    @staticmethod
    def create_shipping(db: Session, shipping: ShippingCreate) -> Shipping:
        new_shipping = Shipping(**shipping.model_dump())
        db.add(new_shipping)
        db.commit()
        db.refresh(new_shipping)
        return new_shipping

    @staticmethod
    def get_shipping(db: Session, shipping_id: int) -> Optional[Shipping]:
        return db.query(Shipping).filter(Shipping.id == shipping_id).first()
    
    @staticmethod
    def get_shipping_by_order_id(db: Session, order_id: int) -> Optional[Shipping]:
        return db.query(Shipping).filter(Shipping.order_id == order_id).first()

    @staticmethod
    def update_shipping(db: Session, shipping: Shipping, update: ShippingUpdate) -> Shipping:
        shipping.status = update.status
        db.commit()
        db.refresh(shipping)
        return shipping

    @staticmethod
    def update_location(db: Session, update: LocationUpdate) -> Optional[Delivery]:
        delivery = LogisticsService.get_delivery_by_order_id(db, update.order_id)
        if not delivery:
            return None
        delivery.location = f"{update.latitude},{update.longitude}"
        db.commit()
        return delivery

    @staticmethod
    def get_combined_tracking(db: Session, order_id: int) -> Optional[TrackingResponse]:
        delivery = LogisticsService.get_delivery_by_order_id(db, order_id)
        shipping = LogisticsService.get_shipping_by_order_id(db, order_id)
        
        if not delivery and not shipping:
            return None
            
        current_status = delivery.status if delivery else (shipping.status if shipping else "unknown")
        location = delivery.location if delivery else None
        
        return TrackingResponse(
            order_id=order_id,
            status=current_status,
            location=location,
            timestamp=datetime.utcnow(), 
            carrier=shipping.carrier if shipping else None,
            tracking_number=shipping.tracking_number if shipping else None
        )
