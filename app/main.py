from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import Login, Token
from app.token import verify_password, create_access_token, hash_password, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
from fastapi import FastAPI, status, Request, Body, Form
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import json
from app.database import get_db
from app.models import User as UserModel  
from app.models import User 
from typing import Optional
from app.database import engine, Base
from app import models
from app.schemas import User, Deliveries
from sqlalchemy.orm import sessionmaker, Session
from app.schemas import User
from app.schemas import Deliveries as Delivery


Base.metadata.create_all(engine)

app = FastAPI(
    title="Delivery Management System API",
    description="A simple Delivery Management API built with FastAPI",
    version="1.0.0"
)

# Exception handler for login endpoint to handle form data
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Only handle login endpoint specially
    if request.url.path == "/login":
        content_type = request.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" in content_type:
            # Try to parse as form data
            try:
                form_data = await request.form()
                username = form_data.get("username")
                password = form_data.get("password")
                if username and password:
                    # Re-route to login logic
                    from app.database import SessionLocal
                    db = SessionLocal()
                    try:
                        user = db.query(UserModel).filter(UserModel.email == username).first()
                        if user and verify_password(password, user.password):
                            access_token = create_access_token(data={"sub": user.email})
                            return JSONResponse(
                                content={"access_token": access_token, "token_type": "bearer"}
                            )
                        else:
                            from fastapi import HTTPException
                            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                    finally:
                        db.close()
            except Exception:
                pass
    # Default validation error response
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
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
    hashed_pw = hash_password(user.password)
    db_user = UserModel(name=user.name, email=user.email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": user}


# Login endpoint - accepts both JSON (Login schema) and form data (OAuth2)
@app.post("/login", response_model=Token, tags=["auth"])
async def login(
    request: Request,
    login_data: Login = Body(...),
    db: Session = Depends(get_db)
):
    # Check content type to handle both JSON and form data
    content_type = request.headers.get("content-type", "")
    
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        # Form data request - parse manually (for Swagger UI OAuth2 flow)
        try:
            form_data = await request.form()
            username = form_data.get("username")
            password = form_data.get("password")
        except Exception:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid form data. Expected 'username' and 'password' fields."
            )
    else:
        # JSON request - use Login schema
        username = login_data.username
        password = login_data.password
    
    if not username or not password:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing username or password"
        )
    
    user = db.query(UserModel).filter(UserModel.email == username).first()
    if not user or not verify_password(password, user.password):
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# JWT-protected example route
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

@app.get("/me", tags=["auth"])
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

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


@app.get("/deliveries/{delivery_id}", status_code=status.HTTP_200_OK, tags=["deliveries"])
def show_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        return {"error": "Delivery not found"}
    return {
        "id": db_delivery.id,
        "item_name": db_delivery.item_name,
        "destination": db_delivery.destination,
        "status": db_delivery.status,
        "tracking_number": db_delivery.tracking_number
    }

@app.post("/deliveries/", status_code=status.HTTP_201_CREATED, tags=["deliveries"])
def create_delivery(delivery: Deliveries, db: Session = Depends(get_db)):
    db_delivery = models.Delivery(
        item_name=delivery.item_name,
        destination=delivery.destination,
        status=delivery.status,
        tracking_number=delivery.tracking_number
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return {"message": "Delivery created successfully", "delivery": delivery}

@app.delete("/deliveries/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["deliveries"])
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        return {"error": "Delivery not found"}
    db.delete(db_delivery)
    db.commit()
    return {"message": f"Delivery with id {delivery_id} deleted successfully"}

@app.put("/deliveries/{delivery_id}", status_code=status.HTTP_200_OK, tags=["deliveries"])
def update_delivery(delivery_id: int, delivery: Delivery, db: Session = Depends(get_db)):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        return {"error": "Delivery not found"}
    db_delivery.item_name = delivery.item_name
    db_delivery.destination = delivery.destination
    db_delivery.status = delivery.status
    db_delivery.tracking_number = delivery.tracking_number
    db.commit()
    db.refresh(db_delivery)
    return {"message": f"Delivery with id {delivery_id} updated successfully", "delivery": delivery}