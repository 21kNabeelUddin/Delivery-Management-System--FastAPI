from fastapi import FastAPI, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Delivery Management System API",
    description="A simple Delivery Management API built with FastAPI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Delivery Management System!"}

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def show_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}

@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: BaseModel):
    return {"message": "User created successfully", "user": user}

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int):
    return {"message": f"User with id {user_id} deleted successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def update_user(user_id: int, user: BaseModel):
    return {"message": f"User with id {user_id} updated successfully", "user": user}
