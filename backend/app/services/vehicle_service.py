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

def search_vehicles(
    db: Session,
    make: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[Vehicle]:
    """Search for vehicles using the repository layer."""
    return vehicle_repository.search_vehicles(
        db, make=make, model=model, category=category, min_price=min_price, max_price=max_price
    )

def purchase_vehicle(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    """Decrease a vehicle's quantity by 1."""
    vehicle = vehicle_repository.get_vehicle_by_id(db, vehicle_id)
    if not vehicle:
        return None
    if vehicle.quantity <= 0:
        raise InvalidVehicleData("Vehicle is out of stock")
    return vehicle_repository.purchase_vehicle(db, vehicle_id)

def restock_vehicle(db: Session, vehicle_id: int, quantity: int) -> Optional[Vehicle]:
    """Increase a vehicle's quantity by a positive amount."""
    if quantity <= 0:
        raise InvalidVehicleData("Restock quantity must be greater than zero")
    return vehicle_repository.restock_vehicle(db, vehicle_id, quantity)



