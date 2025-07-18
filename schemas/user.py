import uuid
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class UserRead(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: EmailStr


class UserCreate(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str

    @validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @validator("phone")
    @classmethod
    def validate_phone(cls, v):
        uzbek_pattern = r"^\+?998\d{9}$"
        if not re.match(uzbek_pattern, v):
            raise ValueError("Phone number must be a valid Uzbekistan number starting with +998 or 998")
        return v

class UserUpdate(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    email: Optional[EmailStr]
