from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Product, Category
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

@app.post("/api/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/api/products/search", response_model=List[ProductResponse])
async def search_products(name: str | None = None, description: str | None = None, category_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    return list(query.all())

@app.get("/api/products/filter", response_model=List[ProductResponse])
async def filter_products(min_price: float | None = None, max_price: float | None = None, category_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    return list(query.all())

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.patch("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted successfully"}

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
    return {"message": "Welcome to the Product Catalog Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
