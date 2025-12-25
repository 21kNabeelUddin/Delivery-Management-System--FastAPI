from typing import Optional
from pydantic import BaseModel, Field


class DeliveryBase(BaseModel):
    item_name: str
    destination: str
    status: str
    tracking_number: str


class DeliveryCreate(DeliveryBase):
    user_id: Optional[int] = None


class DeliveryUpdate(BaseModel):
    item_name: Optional[str] = None
    destination: Optional[str] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None


class Delivery(DeliveryBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True


class ShowDelivery(BaseModel):
    id: int
    user_id: int
    item_name: str
    destination: str
    status: str
    tracking_number: str

    class Config:
        from_attributes = True

