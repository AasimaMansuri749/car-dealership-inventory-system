from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/")
def get_vehicles(db: Session = Depends(get_db)):
    """Return all vehicles in the inventory."""
    return db.query(Vehicle).all()


@router.post("/", response_model=VehicleResponse, status_code=201)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    """Create a new vehicle in the inventory."""
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse, status_code=200)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing vehicle. Only provided fields are changed."""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    updated_fields = vehicle_data.model_dump(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.delete("/{vehicle_id}", status_code=204)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Delete a vehicle by ID. Returns 204 No Content on success."""
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(db_vehicle)
    db.commit()
    return Response(status_code=204)



