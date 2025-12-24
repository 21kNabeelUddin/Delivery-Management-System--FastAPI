from fastapi import FastAPI, status
from fastapi import Depends
from app.database import get_db
from app.models import User as UserModel  
from app.models import User 
from typing import Optional
from app.database import engine, Base
from app import models
from app.schemas import User 
from sqlalchemy.orm import sessionmaker, Session
from app.schemas import User



Base.metadata.create_all(engine)

app = FastAPI(
    title="Delivery Management System API",
    description="A simple Delivery Management API built with FastAPI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Delivery Management System!"}

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def show_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return {"error": "User not found"}
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email
    }
@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": user}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return {"error": "User not found"}
    db.delete(db_user)
    db.commit()
    return {"message": f"User with id {user_id} deleted successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return {"error": "User not found"}
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return {"message": f"User with id {user_id} updated successfully", "user": user}


