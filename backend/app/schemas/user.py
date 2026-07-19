from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(...)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):  
        # Check for special characters (only allow alphanumeric, underscore, and spaces)
        if not re.match(r'^[a-zA-Z0-9_ ]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and spaces')
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password should be at least 6 characters long")
        return v 


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

