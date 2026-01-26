from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Product, Category
from .schemas import ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate

class CategoryService:
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def get_all(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def create(db: Session, category: CategoryCreate) -> Category:
        new_category = Category(name=category.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def update(db: Session, category: Category, update_data: CategoryUpdate) -> Category:
        category.name = update_data.name
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(db: Session, category: Category) -> None:
        db.delete(category)
        db.commit()

class ProductService:
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create(db: Session, product: ProductCreate) -> Product:
        new_product = Product(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def update(db: Session, product: Product, update_data: ProductUpdate) -> Product:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()

    @staticmethod
    def search(db: Session, name: Optional[str] = None, description: Optional[str] = None, category_id: Optional[int] = None) -> List[Product]:
        query = db.query(Product)
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if description:
            query = query.filter(Product.description.ilike(f"%{description}%"))
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.all()

    @staticmethod
    def filter_products(db: Session, min_price: Optional[float] = None, max_price: Optional[float] = None, category_id: Optional[int] = None) -> List[Product]:
        query = db.query(Product)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        return query.all()
