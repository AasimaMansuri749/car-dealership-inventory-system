from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str

