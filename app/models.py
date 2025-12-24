from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    destination = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    tracking_number = Column(String)
    
    user = relationship("User", back_populates="deliveries")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    deliveries = relationship("Delivery", back_populates="owner")

