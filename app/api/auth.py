from fastapi import APIRouter, status, Form, HTTPException, Depends, Query
from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User
from app.schemas.auth import Token
from app.api.dependencies import oauth2_scheme, get_current_user
from app.services.email_service import email_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    username: str = Form(..., description="User email address"),
    password: str = Form(..., description="User password"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"user": {"id": current_user.id, "name": current_user.name, "email": current_user.email}}


@router.post("/request-verification")
async def request_email_verification(
    email: str = Form(..., description="Email address to verify"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified")
    
    verification_token = secrets.token_urlsafe(32)
    user.verification_token = verification_token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    email_service.send_verification_email(user.email, verification_token)
    
    return {"message": "Verification email sent"}


@router.get("/verify-email")
async def verify_email_get(
    token: str = Query(..., description="Email verification token"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification token")
    
    if user.verification_token_expires and user.verification_token_expires < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification token expired")
    
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/verify-email")
async def verify_email_post(
    token: str = Form(..., description="Email verification token"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification token")
    
    if user.verification_token_expires and user.verification_token_expires < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification token expired")
    
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/request-password-reset")
async def request_password_reset(
    email: str = Form(..., description="Email address for password reset"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"message": "If the email exists, a password reset link has been sent"}
    
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    email_service.send_password_reset_email(user.email, reset_token)
    
    return {"message": "If the email exists, a password reset link has been sent"}


@router.get("/reset-password")
async def reset_password_get(
    token: str = Query(..., description="Password reset token"),
    db: Session = Depends(get_db)
):
    from fastapi.responses import HTMLResponse
    
    user = db.query(User).filter(User.reset_token == token).first()
    if not user:
        return HTMLResponse(content="""
        <html>
            <body>
                <h2>Invalid Reset Token</h2>
                <p>The password reset token is invalid or has expired.</p>
                <p>Please request a new password reset link.</p>
            </body>
        </html>
        """, status_code=400)
    
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        return HTMLResponse(content="""
        <html>
            <body>
                <h2>Token Expired</h2>
                <p>The password reset token has expired.</p>
                <p>Please request a new password reset link.</p>
            </body>
        </html>
        """, status_code=400)
    
    html_content = f"""
    <html>
        <body>
            <h2>Reset Your Password</h2>
            <form action="/api/auth/reset-password" method="post">
                <input type="hidden" name="token" value="{token}">
                <label for="new_password">New Password:</label><br>
                <input type="password" id="new_password" name="new_password" required><br><br>
                <button type="submit">Reset Password</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/reset-password")
async def reset_password_post(
    token: str = Form(..., description="Password reset token"),
    new_password: str = Form(..., description="New password"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
    
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset token expired")
    
    user.password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Password reset successfully"}
