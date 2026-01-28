from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import Role, User
from .schemas import (
    UserCreate, UserUpdate, RoleUpdate, UserResponse,
    PasswordForgot, PasswordReset, Token, LoginRequest
)
from .services import UserService, AuthService
from .dependencies import get_current_user

router = APIRouter()

@router.post("/api/users/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if UserService.get_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if user.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    new_user = UserService.create_user(db, user)
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/api/users/admin-register", status_code=status.HTTP_201_CREATED)
def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'admin' for this endpoint")
    
    return register_user(user, db)

@router.post("/api/auth/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, login_req.username, login_req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/api/auth/logout")
def logout():
    return {"message": "Logout successful"}

@router.get("/api/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/api/users/me", response_model=UserResponse)
def update_user_me(user_update: UserUpdate, 
                        current_user: User = Depends(get_current_user), 
                        db: Session = Depends(get_db)):
    return UserService.update_user(db, current_user, user_update)

@router.get("/api/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/api/roles")
def list_roles():
    return {"roles": [r.value for r in Role]}

@router.patch("/api/users/{user_id}/role")
def update_user_role(user_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if role_update.role not in [r.value for r in Role]:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of {[r.value for r in Role]}")

    updated_user = UserService.update_role(db, user, role_update)
    return {"message": "Role updated successfully", "new_role": updated_user.role}

@router.post("/api/password/forgot")
def forgot_password(request: PasswordForgot):
    # Stub: Send email
    return {"message": "If the email is registered, a reset link has been sent."}

@router.post("/api/password/reset")
def reset_password(request: PasswordReset):
    return {"message": "Password reset successfully (Mock)"}
