from pydantic import BaseModel, EmailStr
from typing import Optional
from models import RoleEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None  # No obligatorio para edición

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
