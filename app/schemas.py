from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(UserCreate):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    id: Optional[str] = None
    token: Optional[str] = None
