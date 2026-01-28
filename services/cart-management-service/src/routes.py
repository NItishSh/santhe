from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import Cart, CartItem
from .schemas import CartResponse, CartItemCreate, CartItemUpdate
from .dependencies import get_current_username

router = APIRouter()

@router.get("/api/cart", response_model=CartResponse)
def get_cart(username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.username == username).first()
    if not cart:
        # Auto-create cart on access if not exists? Or return 404?
        # E-commerce usually creates on add, but viewing empty cart is valid.
        # Let's return a transient empty cart structure or create one.
        # Creating one is persistent.
        cart = Cart(username=username)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/api/cart/items", response_model=CartResponse)
def add_item(item: CartItemCreate, username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.username == username).first()
    if not cart:
        cart = Cart(username=username)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if item exists
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    return cart

@router.patch("/api/cart/items/{item_id}", response_model=CartResponse)
def update_item(item_id: int, update: CartItemUpdate, username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.username == username).first()
    if not cart:
         raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    if update.quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = update.quantity
    
    db.commit()
    db.refresh(cart)
    return cart

@router.delete("/api/cart/items/{item_id}", response_model=CartResponse)
def remove_item(item_id: int, username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.username == username).first()
    if not cart:
         raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return cart

@router.delete("/api/cart", response_model=CartResponse) # Reset cart
def clear_cart(username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.username == username).first()
    if cart:
        # Delete items
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
        db.refresh(cart)
    else:
         # Create empty if not exists to satisfy response model
         cart = Cart(username=username)
         db.add(cart)
         db.commit()
         db.refresh(cart)
         
    return cart
