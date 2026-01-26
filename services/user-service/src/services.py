from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from config.settings import settings
from .models import User, Role
from .schemas import UserCreate, UserUpdate, RoleUpdate

class AuthService:
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = UserService.get_by_username(db, username)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user

class UserService:
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        user_data = user.model_dump()
        password = user_data.pop("password")
        
        # Role validation usually handled by Pydantic, but explicit check here is extra safety
        # user.role is a string in UserCreate, User model expects Enum or string depending on SQLA setup.
        # implementation in main.py line 50 checked against [r.value for r in Role]
        
        new_user = User(**user_data)
        new_user.set_password(password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(db: Session, user: User, update_data: UserUpdate) -> User:
        data = update_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_role(db: Session, user: User, role_update: RoleUpdate) -> User:
        user.role = role_update.role
        db.commit()
        db.refresh(user)
        return user
