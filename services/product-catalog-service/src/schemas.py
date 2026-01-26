from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ProductResponse(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
