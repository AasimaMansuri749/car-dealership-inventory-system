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

client = TestClient(app)


# ── Tests ──────────────────────────────────────────────────────────────────

def test_get_vehicles_returns_200():
    """GET /vehicles must respond with HTTP 200 OK."""
    response = client.get("/vehicles")
    assert response.status_code == 200


def test_get_vehicles_returns_empty_list_when_no_vehicles_exist():
    """GET /vehicles must return an empty list [] when the DB has no vehicles."""
    response = client.get("/vehicles")
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
    response = client.post("/vehicles", json=valid_payload)
    
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
    response = client.post("/vehicles", json=payload_zero_price)
    assert response.status_code == 422

    # Test price < 0
    payload_neg_price = valid_payload.copy()
    payload_neg_price["price"] = -500
    response = client.post("/vehicles", json=payload_neg_price)
    assert response.status_code == 422


def test_create_vehicle_negative_quantity(valid_payload):
    """POST /vehicles must fail with 422 if quantity is negative."""
    payload_neg_qty = valid_payload.copy()
    payload_neg_qty["quantity"] = -1
    response = client.post("/vehicles", json=payload_neg_qty)
    assert response.status_code == 422

