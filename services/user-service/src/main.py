from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .services import create_access_token, verify_token

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user_data = user.model_dump()
    password = user_data.pop("password")
    new_user = User(**user_data)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@app.post("/login")
async def login_for_access_token(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(verify_token)):
    return {"username": token["sub"]}
