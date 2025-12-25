from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.schemas.delivery import Delivery


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    is_verified: bool
    deliveries: List[Delivery] = []
    
    class Config:
        from_attributes = True

