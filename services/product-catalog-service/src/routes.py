from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db
from .schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse
)
from .services import CategoryService, ProductService

router = APIRouter()

@router.post("/api/categories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if CategoryService.get_by_name(db, category.name):
        raise HTTPException(status_code=400, detail="Category already exists")
    return CategoryService.create(db, category)

@router.get("/api/categories", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all(db)

@router.patch("/api/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = CategoryService.get_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryService.update(db, db_category, category)

@router.delete("/api/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = CategoryService.get_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    CategoryService.delete(db, db_category)
    return {"message": "Category deleted successfully"}

@router.post("/api/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create(db, product)

@router.get("/api/products/search", response_model=List[ProductResponse])
def search_products(
    name: Optional[str] = None, 
    description: Optional[str] = None, 
    category_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    return ProductService.search(db, name, description, category_id)

@router.get("/api/products/filter", response_model=List[ProductResponse])
def filter_products(
    min_price: Optional[float] = None, 
    max_price: Optional[float] = None, 
    category_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    return ProductService.filter_products(db, min_price, max_price, category_id)

@router.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.patch("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductService.update(db, product, product_update)

@router.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    ProductService.delete(db, product)
    return {"message": f"Product {product_id} deleted successfully"}
