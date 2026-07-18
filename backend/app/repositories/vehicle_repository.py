from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle

def get_all_vehicles(db: Session) -> List[Vehicle]:
    """Retrieve all vehicles from the database."""
    return db.query(Vehicle).all()

def get_vehicle_by_id(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    """Retrieve a vehicle by its ID."""
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

def create_vehicle(db: Session, vehicle_data: dict) -> Vehicle:
    """Create a new vehicle in the database."""
    db_vehicle = Vehicle(**vehicle_data)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle(db: Session, vehicle_id: int, update_data: dict) -> Optional[Vehicle]:
    """Update an existing vehicle's fields. Returns None if vehicle not found."""
    db_vehicle = get_vehicle_by_id(db, vehicle_id)
    if not db_vehicle:
        return None
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int) -> bool:
    """Delete a vehicle from the database. Returns True if deleted, False if not found."""
    db_vehicle = get_vehicle_by_id(db, vehicle_id)
    if not db_vehicle:
        return False
    db.delete(db_vehicle)
    db.commit()
    return True
