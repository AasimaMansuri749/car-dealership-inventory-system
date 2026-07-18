from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services import vehicle_service
from app.exceptions.vehicle_exceptions import InvalidVehicleData

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/")
def get_vehicles(db: Session = Depends(get_db)):
    """Return all vehicles in the inventory."""
    return vehicle_service.get_all_vehicles(db)


@router.post("/", response_model=VehicleResponse, status_code=201)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    """Create a new vehicle in the inventory."""
    try:
        return vehicle_service.create_vehicle(db, vehicle.model_dump())
    except InvalidVehicleData as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{vehicle_id}", response_model=VehicleResponse, status_code=200)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing vehicle. Only provided fields are changed."""
    try:
        db_vehicle = vehicle_service.update_vehicle(
            db, vehicle_id, vehicle_data.model_dump(exclude_unset=True)
        )
    except InvalidVehicleData as e:
        raise HTTPException(status_code=400, detail=str(e))
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@router.delete("/{vehicle_id}", status_code=204)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Delete a vehicle by ID. Returns 204 No Content on success."""
    success = vehicle_service.delete_vehicle(db, vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return Response(status_code=204)





