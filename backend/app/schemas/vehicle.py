from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class VehicleBase(BaseModel):
    make: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    category: str = Field(..., max_length=30)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    quantity: int = Field(..., ge=0)
    description: Optional[str] = None
    year: int = Field(...)
    color: str = Field(..., max_length=30)
    mileage: int = Field(..., ge=0)
    fuel_type: str = Field(..., max_length=20)
    transmission: str = Field(..., max_length=20)
    image_url: Optional[str] = Field(None, max_length=255)

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class VehicleUpdate(BaseModel):
    """All fields are optional — only provided fields will be updated."""
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = Field(None, max_length=30)
    mileage: Optional[int] = Field(None, ge=0)
    fuel_type: Optional[str] = Field(None, max_length=20)
    transmission: Optional[str] = Field(None, max_length=20)
    image_url: Optional[str] = Field(None, max_length=255)
    make: Optional[str] = Field(None, max_length=50)
    model: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=30)


class VehicleRestock(BaseModel):
    quantity: int = Field(..., gt=0)



