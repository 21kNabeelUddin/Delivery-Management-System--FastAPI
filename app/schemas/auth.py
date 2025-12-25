from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class EmailVerificationRequest(BaseModel):
    email: str


class EmailVerification(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    token: str
    new_password: str

