from typing import List, Optional
from pydantic import BaseModel, Field


class DeliveriesBase(BaseModel):
    id: Optional[int] = None
    item_name: str
    destination: str
    status: str
    tracking_number: int

class Deliveries(DeliveriesBase):
    class Config():
        from_attributes = True


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name: str
    email: str
    deliveries: List[Deliveries] = Field(default_factory=list)
    class Config():
        from_attributes = True

class ShowDeliveries(BaseModel):
    id: int
    user_id: int
    item_name: str
    destination: str
    status: str
    tracking_number: int

    class Config():
        from_attributes = True


class Login(BaseModel):
    username: str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
