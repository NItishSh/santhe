from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .models import Price, Bid
from .schemas import PriceCreate, PriceUpdate, BidCreate, BidUpdate

class PricingService:
    @staticmethod
    def create_price(db: Session, price: PriceCreate) -> Price:
        new_price = Price(
            product_id=price.product_id,
            price=price.price,
            timestamp=price.timestamp
        )
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        return new_price

    @staticmethod
    def get_price(db: Session, price_id: int) -> Optional[Price]:
        return db.query(Price).filter(Price.id == price_id).first()

    @staticmethod
    def update_price(db: Session, price: Price, update: PriceUpdate) -> Price:
        update_data = update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(price, key, value)
        db.commit()
        db.refresh(price)
        return price

    @staticmethod
    def delete_price(db: Session, price: Price) -> None:
        db.delete(price)
        db.commit()

    @staticmethod
    def get_price_history(db: Session, product_id: int, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[Price]:
        query = db.query(Price).filter(Price.product_id == product_id)
        if start_date:
            query = query.filter(Price.timestamp >= start_date)
        if end_date:
            query = query.filter(Price.timestamp <= end_date)
        return query.order_by(Price.timestamp.asc()).all()

    @staticmethod
    def create_bid(db: Session, bid: BidCreate) -> Bid:
        new_bid = Bid(
            product_id=bid.product_id,
            bid_amount=bid.bid_amount,
            bidder_id=bid.bidder_id,
            timestamp=datetime.utcnow()
        )
        db.add(new_bid)
        db.commit()
        db.refresh(new_bid)
        return new_bid

    @staticmethod
    def get_bid(db: Session, bid_id: int) -> Optional[Bid]:
        return db.query(Bid).filter(Bid.id == bid_id).first()

    @staticmethod
    def update_bid(db: Session, bid: Bid, update: BidUpdate) -> Bid:
        bid.bid_amount = update.bid_amount
        db.commit()
        db.refresh(bid)
        return bid

    @staticmethod
    def delete_bid(db: Session, bid: Bid) -> None:
        db.delete(bid)
        db.commit()
