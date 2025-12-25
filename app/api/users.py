from fastapi import APIRouter, status, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, ShowUser
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
def show_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    name: str = Form(..., description="User's full name"),
    email: str = Form(..., description="User's email address"),
    password: str = Form(..., description="User's password"),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_pw = hash_password(password)
    db_user = User(name=name, email=email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": {"id": db_user.id, "name": db_user.name, "email": db_user.email}}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    name: str = Form(None, description="User's full name"),
    email: str = Form(None, description="User's email address"),
    password: str = Form(None, description="User's password"),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if name is not None:
        db_user.name = name
    if email is not None:
        db_user.email = email
    if password is not None:
        db_user.password = hash_password(password)
    
    db.commit()
    db.refresh(db_user)
    return {"message": f"User with id {user_id} updated successfully", "user": {"id": db_user.id, "name": db_user.name, "email": db_user.email}}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User with id {user_id} deleted successfully"}

