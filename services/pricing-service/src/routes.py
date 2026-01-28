from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .database import get_db
from .schemas import (
    PriceCreate, PriceUpdate, PriceResponse,
    BidCreate, BidUpdate, BidResponse
)
from .services import PricingService

router = APIRouter()

@router.post("/api/prices", status_code=status.HTTP_201_CREATED, response_model=PriceResponse)
def create_price(price: PriceCreate, db: Session = Depends(get_db)):
    return PricingService.create_price(db, price)

@router.get("/api/prices/{price_id}", response_model=PriceResponse)
def get_price(price_id: int, db: Session = Depends(get_db)):
    price = PricingService.get_price(db, price_id)
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return price

@router.patch("/api/prices/{price_id}", response_model=PriceResponse)
def update_price(price_id: int, price_update: PriceUpdate, db: Session = Depends(get_db)):
    price = PricingService.get_price(db, price_id)
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return PricingService.update_price(db, price, price_update)

@router.delete("/api/prices/{price_id}")
def delete_price(price_id: int, db: Session = Depends(get_db)):
    price = PricingService.get_price(db, price_id)
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    PricingService.delete_price(db, price)
    return {"message": f"Price {price_id} deleted successfully"}

@router.get("/api/prices/history/{product_id}", response_model=List[PriceResponse])
def get_price_history(product_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, db: Session = Depends(get_db)):
    return PricingService.get_price_history(db, product_id, start_date, end_date)

@router.post("/api/bids", status_code=status.HTTP_201_CREATED, response_model=BidResponse)
def create_bid(bid: BidCreate, db: Session = Depends(get_db)):
    return PricingService.create_bid(db, bid)

@router.get("/api/bids/{bid_id}", response_model=BidResponse)
def get_bid(bid_id: int, db: Session = Depends(get_db)):
    bid = PricingService.get_bid(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid

@router.patch("/api/bids/{bid_id}", response_model=BidResponse)
def update_bid(bid_id: int, bid_update: BidUpdate, db: Session = Depends(get_db)):
    bid = PricingService.get_bid(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return PricingService.update_bid(db, bid, bid_update)

@router.delete("/api/bids/{bid_id}")
def cancel_bid(bid_id: int, db: Session = Depends(get_db)):
    bid = PricingService.get_bid(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    PricingService.delete_bid(db, bid)
    return {"message": "Bid cancelled successfully"}
