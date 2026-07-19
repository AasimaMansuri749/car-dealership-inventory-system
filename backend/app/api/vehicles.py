from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user, get_admin_user
from app.models.user import User
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate, VehicleRestock
from app.services import vehicle_service
from app.exceptions.vehicle_exceptions import InvalidVehicleData

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/")
def get_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return all vehicles in the inventory."""
    return vehicle_service.get_all_vehicles(db)


@router.get("/search", response_model=List[VehicleResponse])
def search_vehicles(
    make: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search for vehicles in the inventory."""
    return vehicle_service.search_vehicles(
        db, make=make, model=model, category=category, min_price=min_price, max_price=max_price
    )


@router.get("/{vehicle_id}")
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vehicle = vehicle_service.get_vehicle_by_id(
        db,
        vehicle_id
    )

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.post("/", response_model=VehicleResponse, status_code=201)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
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
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
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
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Delete a vehicle by ID. Returns 204 No Content on success."""
    success = vehicle_service.delete_vehicle(db, vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return Response(status_code=204)


@router.post("/{vehicle_id}/purchase", response_model=VehicleResponse, status_code=200)
def purchase_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Purchase a vehicle, decreasing its quantity by 1."""
    try:
        db_vehicle = vehicle_service.purchase_vehicle(db, vehicle_id)
    except InvalidVehicleData as e:
        raise HTTPException(status_code=400, detail=str(e))
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@router.post("/{vehicle_id}/restock", response_model=VehicleResponse, status_code=200)
def restock_vehicle(
    vehicle_id: int,
    restock_data: VehicleRestock,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Restock a vehicle, increasing its quantity."""
    try:
        db_vehicle = vehicle_service.restock_vehicle(db, vehicle_id, restock_data.quantity)
    except InvalidVehicleData as e:
        raise HTTPException(status_code=400, detail=str(e))
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle





