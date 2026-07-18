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

