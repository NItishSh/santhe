from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import Role, User
from .schemas import (
    UserCreate, UserUpdate, RoleUpdate, UserResponse,
    PasswordForgot, PasswordReset, Token, LoginRequest
)
from .services import UserService, AuthService
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = AuthService.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = UserService.get_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.post("/api/users/register", status_code=status.HTTP_201_CREATED, response_model=dict)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if UserService.get_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if user.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    new_user = UserService.create_user(db, user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/api/users/admin-register", status_code=status.HTTP_201_CREATED)
async def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    # Security: Ensure only admins can be created via this endpoint? 
    # Original logic just enforced that the payload REQUESTED admin role.
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'admin' for this endpoint")
    
    return await register_user(user, db)

@app.post("/api/auth/login", response_model=Token)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, login_req.username, login_req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/logout")
async def logout():
    return {"message": "Logout successful"}

@app.get("/api/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.patch("/api/users/me", response_model=UserResponse)
async def update_user_me(user_update: UserUpdate, 
                        current_user: User = Depends(get_current_user), 
                        db: Session = Depends(get_db)):
    return UserService.update_user(db, current_user, user_update)

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.get("/api/roles")
async def list_roles():
    return {"roles": [r.value for r in Role]}

@app.patch("/api/users/{user_id}/role")
async def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if role_update.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    updated_user = UserService.update_role(db, user, role_update)
    return {"message": "Role updated successfully", "new_role": updated_user.role}

@app.post("/api/password/forgot")
async def forgot_password(request: PasswordForgot):
    # Stub: Send email
    return {"message": "If the email is registered, a reset link has been sent."}

@app.post("/api/password/reset")
async def reset_password(request: PasswordReset):
    return {"message": "Password reset successfully (Mock)"}

@app.get("/")
async def root():
    return {"message": "User Service API"}
