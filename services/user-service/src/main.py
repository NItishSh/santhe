from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import User, Role
from .services import create_access_token, verify_token
from typing import List, Optional

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None

class RoleUpdate(BaseModel):
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str # Keeping as str to match model Enum if serialized, or we can use Enum

    model_config = ConfigDict(from_attributes=True)

class PasswordForgot(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

@app.post("/api/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if user.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    user_data = user.model_dump()
    password = user_data.pop("password")
    new_user = User(**user_data)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/api/users/admin-register", status_code=status.HTTP_201_CREATED)
async def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    # In a real app, this should be protected or have specific admin validation logic
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'admin' for this endpoint")
    
    return await register_user(user, db)

@app.post("/api/auth/login")
async def login_for_access_token(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
async def logout():
    return {"message": "Logout successful"}

@app.get("/api/users/me", response_model=UserResponse)
async def read_users_me(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    username = token.get("sub")
    user = db.query(User).filter_by(username=username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.patch("/api/users/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    username = token.get("sub")
    user = db.query(User).filter_by(username=username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.get("/api/roles")
async def list_roles():
    return {"roles": [r.value for r in Role]}

@app.patch("/api/users/{user_id}/role")
async def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if role_update.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    # SQLAlchemy Enum type handling might need object or string depending on driver, assuming string works with set_attr logic or explicit
    user.role = role_update.role # If using Enum object in model, might need conversion: Role(role_update.role)
    db.commit()
    db.refresh(user)
    return {"message": "Role updated successfully", "new_role": user.role}

@app.post("/api/password/forgot")
async def forgot_password(request: PasswordForgot):
    # Stub: In production, send email here
    return {"message": "If the email is registered, a reset link has been sent."}

@app.post("/api/password/reset")
async def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    # Stub: Verify token logic would go here.
    # For now, we assume token gives us a username/user_id (mocked)
    # This is a critical logical gap without a real token service, so we will just return a mock success
    # In real impl: user = verify_reset_token(request.token)
    return {"message": "Password reset successfully (Mock)"}

@app.get("/")
async def root():
    return {"message": "User Service API"}
