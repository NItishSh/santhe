from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

class RoleUpdate(BaseModel):
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class PasswordForgot(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
