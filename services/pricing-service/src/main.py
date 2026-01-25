from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from .database import get_db, engine, Base
from .models import Price, Bid
from datetime import datetime
from typing import Optional, List

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

class PriceCreate(BaseModel):
    product_id: int
    price: float
    timestamp: datetime

class PriceUpdate(BaseModel):
    price: Optional[float] = None
    timestamp: Optional[datetime] = None

class PriceResponse(PriceCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BidCreate(BaseModel):
    product_id: int
    bid_amount: float
    bidder_id: int

class BidUpdate(BaseModel):
    bid_amount: float

class BidResponse(BidCreate):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

@app.post("/api/prices", status_code=status.HTTP_201_CREATED, response_model=PriceResponse)
def create_price(price: PriceCreate, db: Session = Depends(get_db)):
    # timestamp is already a datetime object thanks to Pydantic
    
    new_price = Price(
        product_id=price.product_id,
        price=price.price,
        timestamp=price.timestamp
    )
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price

@app.get("/api/prices/{price_id}", response_model=PriceResponse)
def get_price(price_id: int, db: Session = Depends(get_db)):
    price = db.query(Price).filter(Price.id == price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return price

@app.patch("/api/prices/{price_id}", response_model=PriceResponse)
def update_price(price_id: int, price_update: PriceUpdate, db: Session = Depends(get_db)):
    price = db.query(Price).filter(Price.id == price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    
    update_data = price_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
         setattr(price, key, value)
    
    db.commit()
    db.refresh(price)
    return price

@app.delete("/api/prices/{price_id}")
def delete_price(price_id: int, db: Session = Depends(get_db)):
    price = db.query(Price).filter(Price.id == price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    db.delete(price)
    db.commit()
    return {"message": f"Price {price_id} deleted successfully"}

@app.get("/api/prices/history/{product_id}", response_model=List[PriceResponse])
def get_price_history(product_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, db: Session = Depends(get_db)):
    query = db.query(Price).filter(Price.product_id == product_id)
    
    if start_date:
        query = query.filter(Price.timestamp >= start_date)
    if end_date:
        query = query.filter(Price.timestamp <= end_date)
    
    return query.order_by(Price.timestamp.asc()).all()

@app.post("/api/bids", status_code=status.HTTP_201_CREATED, response_model=BidResponse)
async def create_bid(bid: BidCreate, db: Session = Depends(get_db)):
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

@app.get("/api/bids/{bid_id}", response_model=BidResponse)
async def get_bid(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid

@app.patch("/api/bids/{bid_id}", response_model=BidResponse)
async def update_bid(bid_id: int, bid_update: BidUpdate, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    bid.bid_amount = bid_update.bid_amount
    db.commit()
    db.refresh(bid)
    return bid

@app.delete("/api/bids/{bid_id}")
async def cancel_bid(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    db.delete(bid)
    db.commit()
    return {"message": "Bid cancelled successfully"}

@app.get("/")
def root():
    return {"message": "Welcome to the Pricing Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

