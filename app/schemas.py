from typing import List, Optional
from pydantic import BaseModel


class DeliveriesBase(BaseModel):  
    id : int
    item_name : str
    destination: str
    status:str
    tracking_number: int

class Deliveries(DeliveriesBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    deliveries: List[deliveries] = []
    class Config():
        orm_mode = True

class ShowDeliveries(BaseModel):
    id : int
    user_id: int
    item_name : str
    destination: str
    status:str
    tracking_number: int

    class Config():
        orm_mode = True


