from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Price, Bid
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class PriceCreate(BaseModel):
    product_id: int
    price: float
    timestamp: str

class PriceUpdate(BaseModel):
    price: float | None = None
    timestamp: str | None = None

class BidCreate(BaseModel):
    product_id: int
    bid_amount: float
    bidder_id: int

@app.post("/api/prices", status_code=status.HTTP_201_CREATED)
async def create_price(price: PriceCreate, db: Session = Depends(get_db)):
    new_price = Price(**price.dict())
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price

@app.get("/api/prices/{price_id}", response_model=Price)
async def get_price(price_id: int, db: Session = Depends(get_db)):
    price = db.query(Price).filter_by(id=price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    return price

@app.patch("/api/prices/{price_id}", response_model=Price)
async def update_price(price_id: int, price_update: PriceUpdate, db: Session = Depends(get_db)):
    price = db.query(Price).filter_by(id=price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    
    for key, value in price_update.dict(exclude_unset=True).items():
        setattr(price, key, value)
    
    db.commit()
    db.refresh(price)
    return price

@app.delete("/api/prices/{price_id}")
async def delete_price(price_id: int, db: Session = Depends(get_db)):
    price = db.query(Price).filter_by(id=price_id).first()
    if not price:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price not found")
    db.delete(price)
    db.commit()
    return {"message": f"Price {price_id} deleted successfully"}

@app.get("/api/prices/history/{product_id}")
async def get_price_history(product_id: int, start_date: str | None = None, end_date: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Price).filter_by(product_id=product_id)
    
    if start_date:
        start_date_obj = datetime.fromisoformat(start_date)
        query = query.filter(Price.timestamp >= start_date_obj)
    if end_date:
        end_date_obj = datetime.fromisoformat(end_date)
        query = query.filter(Price.timestamp <= end_date_obj)
    
    return list(query.order_by(Price.timestamp.asc()).all())

# Add similar endpoints for bids

# Add Swagger UI documentation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to the Pricing Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

