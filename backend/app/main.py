from fastapi import FastAPI

from app.api.vehicles import router as vehicles_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="Car Dealership Inventory System",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(vehicles_router)


@app.get("/")
def root():
    return {
        "message": "Car Dealership API is running"
    }