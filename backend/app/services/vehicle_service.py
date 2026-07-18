from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.repositories import vehicle_repository
from app.exceptions.vehicle_exceptions import InvalidVehicleData

def validate_vehicle_data(data: dict):
    """Business validation rules for vehicles."""
    price = data.get("price")
    quantity = data.get("quantity")
    
    if price is not None and price < 0:
        raise InvalidVehicleData("Price cannot be negative")
    if quantity is not None and quantity < 0:
        raise InvalidVehicleData("Quantity cannot be negative")

def get_all_vehicles(db: Session) -> List[Vehicle]:
    """Retrieve all vehicles using repository."""
    return vehicle_repository.get_all_vehicles(db)

def create_vehicle(db: Session, vehicle_data: dict) -> Vehicle:
    """Create a new vehicle using repository with validation."""
    validate_vehicle_data(vehicle_data)
    return vehicle_repository.create_vehicle(db, vehicle_data)

def update_vehicle(db: Session, vehicle_id: int, update_data: dict) -> Optional[Vehicle]:
    """Update an existing vehicle using repository with validation."""
    validate_vehicle_data(update_data)
    return vehicle_repository.update_vehicle(db, vehicle_id, update_data)

def delete_vehicle(db: Session, vehicle_id: int) -> bool:
    """Delete a vehicle using repository."""
    return vehicle_repository.delete_vehicle(db, vehicle_id)

