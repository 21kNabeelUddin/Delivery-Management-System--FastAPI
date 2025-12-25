from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.database import Base, engine, SessionLocal
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.api import auth, users, deliveries

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="A simple Delivery Management API built with FastAPI",
    version=settings.APP_VERSION
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if "/login" in request.url.path:
        content_type = request.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" in content_type:
            try:
                form_data = await request.form()
                username = form_data.get("username")
                password = form_data.get("password")
                if username and password:
                    db = SessionLocal()
                    try:
                        user = db.query(User).filter(User.email == username).first()
                        if user and verify_password(password, user.password):
                            access_token = create_access_token(data={"sub": user.email})
                            return JSONResponse(
                                content={"access_token": access_token, "token_type": "bearer"}
                            )
                        else:
                            from fastapi import HTTPException, status
                            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                    finally:
                        db.close()
            except Exception:
                pass
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(deliveries.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to the Delivery Management System!"}
