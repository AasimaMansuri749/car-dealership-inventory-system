from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.vehicle import Vehicle

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/")
def get_vehicles(db: Session = Depends(get_db)):
    """Return all vehicles in the inventory."""
    return db.query(Vehicle).all()
