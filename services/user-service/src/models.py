from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

Base = declarative_base()


class Role(enum.Enum):
    farmer = "farmer"
    middleman = "middleman"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role))

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
