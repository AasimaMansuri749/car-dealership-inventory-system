import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database.database import Base
from app.dependencies.db import get_db
from app.models.vehicle import Vehicle  # noqa: F401 — registers Vehicle with Base
from app.models.user import User        # noqa: F401 — registers User with Base


# ── In-memory SQLite with a single shared connection ──────────────────────
# A plain sqlite:///:memory: gives every new connection its own empty DB.
# By sharing one connection we ensure create_all() and test queries see the
# same tables.
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Use a single connection for all test sessions
connection = test_engine.connect()
Base.metadata.create_all(bind=connection)

TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=connection
)


def override_get_db():
    """Yield a session bound to the shared test connection."""
    db: Session = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Apply the override ─────────────────────────────────────────────────────
app.dependency_overrides[get_db] = override_get_db

from app.dependencies.auth import get_current_user, get_admin_user

def override_get_current_user():
    return User(id=1, username="test_user", email="test@example.com", role="CUSTOMER")

def override_get_admin_user():
    return User(id=2, username="admin_user", email="admin@example.com", role="ADMIN")

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_admin_user] = override_get_admin_user

client = TestClient(app)


# ── Tests ──────────────────────────────────────────────────────────────────

def test_get_vehicles_returns_200():
    """GET /vehicles must respond with HTTP 200 OK."""
    response = client.get("/api/vehicles")
    assert response.status_code == 200


def test_get_vehicles_returns_empty_list_when_no_vehicles_exist():
    """GET /vehicles must return an empty list [] when the DB has no vehicles."""
    response = client.get("/api/vehicles")
    assert response.json() == []


@pytest.fixture
def valid_payload():
    return {
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 25000,
        "quantity": 5,
        "description": "Reliable sedan",
        "year": 2025,
        "color": "Black",
        "mileage": 10000,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "image_url": "https://example.com/car.jpg"
    }


def test_create_vehicle_success(valid_payload):
    """POST /vehicles with valid payload should return 201 Created, return vehicle response structure, and save it in DB."""
    response = client.post("/api/vehicles", json=valid_payload)
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify response structure
    assert "id" in data
    assert data["make"] == valid_payload["make"]
    assert data["model"] == valid_payload["model"]
    assert data["category"] == valid_payload["category"]
    assert float(data["price"]) == float(valid_payload["price"])
    assert data["quantity"] == valid_payload["quantity"]
    assert data["description"] == valid_payload["description"]
    assert data["year"] == valid_payload["year"]
    assert data["color"] == valid_payload["color"]
    assert data["mileage"] == valid_payload["mileage"]
    assert data["fuel_type"] == valid_payload["fuel_type"]
    assert data["transmission"] == valid_payload["transmission"]
    assert data["image_url"] == valid_payload["image_url"]
    assert "created_at" in data
    assert "updated_at" in data

    # Verify storage in DB
    db: Session = TestSessionLocal()
    try:
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == data["id"]).first()
        assert db_vehicle is not None
        assert db_vehicle.make == "Toyota"
        assert db_vehicle.model == "Camry"
    finally:
        db.close()


def test_create_vehicle_invalid_price(valid_payload):
    """POST /vehicles must fail with 422 if price is 0 or negative."""
    # Test price = 0
    payload_zero_price = valid_payload.copy()
    payload_zero_price["price"] = 0
    response = client.post("/api/vehicles", json=payload_zero_price)
    assert response.status_code == 422

    # Test price < 0
    payload_neg_price = valid_payload.copy()
    payload_neg_price["price"] = -500
    response = client.post("/api/vehicles", json=payload_neg_price)
    assert response.status_code == 422


def test_create_vehicle_negative_quantity(valid_payload):
    """POST /vehicles must fail with 422 if quantity is negative."""
    payload_neg_qty = valid_payload.copy()
    payload_neg_qty["quantity"] = -1
    response = client.post("/api/vehicles", json=payload_neg_qty)
    assert response.status_code == 422


# ── PUT /vehicles/{id} tests (RED phase) ──────────────────────────────────

def test_update_vehicle_success(valid_payload):
    """PUT /vehicles/{id} must return 200 and persist updated fields in the DB."""
    # First create a vehicle to update
    create_response = client.post("/api/vehicles", json=valid_payload)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Send full update payload with changed price, quantity and description
    update_payload = {
        "make": valid_payload["make"],
        "model": valid_payload["model"],
        "category": valid_payload["category"],
        "price": 27000,
        "quantity": 10,
        "description": "Updated description",
        "year": valid_payload["year"],
        "color": valid_payload["color"],
        "mileage": valid_payload["mileage"],
        "fuel_type": valid_payload["fuel_type"],
        "transmission": valid_payload["transmission"],
        "image_url": valid_payload["image_url"],
    }
    response = client.put(f"/api/vehicles/{vehicle_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert float(data["price"]) == 27000.0
    assert data["quantity"] == 10
    assert data["description"] == "Updated description"

    # Verify the DB record was actually updated
    db: Session = TestSessionLocal()
    try:
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        assert db_vehicle is not None
        assert float(db_vehicle.price) == 27000.0
        assert db_vehicle.quantity == 10
        assert db_vehicle.description == "Updated description"
    finally:
        db.close()


def test_update_vehicle_not_found():
    """PUT /vehicles/{id} with a non-existing ID must return HTTP 404."""
    update_payload = {
        "make": "Honda",
        "model": "Civic",
        "category": "Sedan",
        "price": 20000,
        "quantity": 3,
        "year": 2023,
        "color": "White",
        "mileage": 5000,
        "fuel_type": "Petrol",
        "transmission": "Manual",
    }
    response = client.put("/api/vehicles/99999", json=update_payload)
    assert response.status_code == 404


# ── DELETE /vehicles/{id} tests (RED phase) ───────────────────────────────

def test_delete_vehicle_success(valid_payload):
    """DELETE /vehicles/{id} must return 204 and remove the vehicle from the DB."""
    # Create a vehicle to delete
    create_response = client.post("/api/vehicles", json=valid_payload)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Delete the vehicle
    response = client.delete(f"/api/vehicles/{vehicle_id}")
    assert response.status_code == 204

    # Verify it no longer exists in the DB
    db: Session = TestSessionLocal()
    try:
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        assert db_vehicle is None, "Vehicle should have been deleted from the database"
    finally:
        db.close()


def test_delete_vehicle_not_found():
    """DELETE /vehicles/{id} with a non-existing ID must return HTTP 404."""
    response = client.delete("/api/vehicles/99999")
    assert response.status_code == 404


from app.exceptions.vehicle_exceptions import InvalidVehicleData
from app.services import vehicle_service

def test_vehicle_service_create_negative_price(valid_payload):
    """Directly calling vehicle_service.create_vehicle with a negative price must raise InvalidVehicleData."""
    db: Session = TestSessionLocal()
    try:
        bad_payload = valid_payload.copy()
        bad_payload["price"] = -100
        with pytest.raises(InvalidVehicleData) as exc_info:
            vehicle_service.create_vehicle(db, bad_payload)
        assert "Price cannot be negative" in str(exc_info.value)
    finally:
        db.close()


def test_vehicle_service_create_negative_quantity(valid_payload):
    """Directly calling vehicle_service.create_vehicle with a negative quantity must raise InvalidVehicleData."""
    db: Session = TestSessionLocal()
    try:
        bad_payload = valid_payload.copy()
        bad_payload["quantity"] = -5
        with pytest.raises(InvalidVehicleData) as exc_info:
            vehicle_service.create_vehicle(db, bad_payload)
        assert "Quantity cannot be negative" in str(exc_info.value)
    finally:
        db.close()


def test_vehicle_service_update_negative_price(valid_payload):
    """Directly calling vehicle_service.update_vehicle with a negative price must raise InvalidVehicleData."""
    db: Session = TestSessionLocal()
    try:
        # Create a valid one first
        vehicle = vehicle_service.create_vehicle(db, valid_payload)
        with pytest.raises(InvalidVehicleData) as exc_info:
            vehicle_service.update_vehicle(db, vehicle.id, {"price": -10.50})
        assert "Price cannot be negative" in str(exc_info.value)
    finally:
        db.close()


def test_vehicle_service_update_negative_quantity(valid_payload):
    """Directly calling vehicle_service.update_vehicle with a negative quantity must raise InvalidVehicleData."""
    db: Session = TestSessionLocal()
    try:
        # Create a valid one first
        vehicle = vehicle_service.create_vehicle(db, valid_payload)
        with pytest.raises(InvalidVehicleData) as exc_info:
            vehicle_service.update_vehicle(db, vehicle.id, {"quantity": -1})
        assert "Quantity cannot be negative" in str(exc_info.value)
    finally:
        db.close()


# ── New Tests for Search, Purchase, Restock & Auth Role checks ─────────────

def test_search_vehicles_success(valid_payload):
    """GET /vehicles/search must filter results according to params."""
    # Ensure there's a vehicle in DB
    client.post("/api/vehicles", json=valid_payload)
    
    # Search match
    response = client.get("/api/vehicles/search?make=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["make"] == "Toyota"
    
    # Search no match
    response_empty = client.get("/api/vehicles/search?make=Honda")
    assert response_empty.status_code == 200
    assert response_empty.json() == []

def test_purchase_vehicle_success(valid_payload):
    """POST /vehicles/{id}/purchase must decrement the vehicle's quantity by 1."""
    create_response = client.post("/api/vehicles", json=valid_payload)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]
    original_qty = create_response.json()["quantity"]
    
    purchase_response = client.post(f"/api/vehicles/{vehicle_id}/purchase")
    assert purchase_response.status_code == 200
    assert purchase_response.json()["quantity"] == original_qty - 1

def test_purchase_vehicle_out_of_stock(valid_payload):
    """POST /vehicles/{id}/purchase must return 400 when quantity is 0."""
    no_stock_payload = valid_payload.copy()
    no_stock_payload["quantity"] = 0
    create_response = client.post("/api/vehicles", json=no_stock_payload)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]
    
    purchase_response = client.post(f"/api/vehicles/{vehicle_id}/purchase")
    assert purchase_response.status_code == 400
    assert "out of stock" in purchase_response.json()["detail"]

def test_restock_vehicle_success(valid_payload):
    """POST /vehicles/{id}/restock (Admin only) must increment vehicle quantity."""
    create_response = client.post("/api/vehicles", json=valid_payload)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]
    original_qty = create_response.json()["quantity"]
    
    restock_response = client.post(f"/api/vehicles/{vehicle_id}/restock", json={"quantity": 10})
    assert restock_response.status_code == 200
    assert restock_response.json()["quantity"] == original_qty + 10

def test_restock_vehicle_unauthorized_for_customer(valid_payload):
    """POST /vehicles/{id}/restock must return 403 Forbidden for non-admin user."""
    # Temporarily override get_admin_user to raise HTTP 403 (simulating non-admin)
    from fastapi import HTTPException
    def mock_get_admin_user_forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")
        
    app.dependency_overrides[get_admin_user] = mock_get_admin_user_forbidden
    
    try:
        response = client.post("/api/vehicles/1/restock", json={"quantity": 10})
        assert response.status_code == 403
    finally:
        # Restore override
        app.dependency_overrides[get_admin_user] = override_get_admin_user

def test_create_vehicle_unauthorized_for_customer(valid_payload):
    """POST /vehicles must return 403 Forbidden for non-admin user."""
    from fastapi import HTTPException
    def mock_get_admin_user_forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")
        
    app.dependency_overrides[get_admin_user] = mock_get_admin_user_forbidden
    
    try:
        response = client.post("/api/vehicles", json=valid_payload)
        assert response.status_code == 403
    finally:
        app.dependency_overrides[get_admin_user] = override_get_admin_user



