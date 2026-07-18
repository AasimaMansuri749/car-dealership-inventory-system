import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database.database import Base
from app.dependencies.db import get_db
from app.models.user import User       # noqa: F401 — registers User with Base
from app.models.vehicle import Vehicle # noqa: F401 — registers Vehicle with Base
from app.models.order import Order     # noqa: F401 — registers Order with Base
from app.models.order_item import OrderItem  # noqa: F401 — registers OrderItem with Base


# ── In-memory SQLite with a single shared connection ──────────────────────
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

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


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ── Tests ──────────────────────────────────────────────────────────────────

@pytest.fixture
def register_payload():
    return {
        "username": "john",
        "email": "john@example.com",
        "password": "securepassword"
    }


def test_register_user_success(register_payload):
    """POST /auth/register with valid data must return 201 and store user in DB."""
    response = client.post("/auth/register", json=register_payload)

    assert response.status_code == 201
    data = response.json()

    # Verify response fields
    assert "id" in data
    assert data["username"] == register_payload["username"]
    assert data["email"] == register_payload["email"]
    assert "role" in data
    assert "created_at" in data
    assert "updated_at" in data

    # Verify password is NOT returned in the response (security check)
    assert "password" not in data
    assert "password_hash" not in data

    # Verify user is actually stored in the DB
    db: Session = TestSessionLocal()
    try:
        db_user = db.query(User).filter(User.email == register_payload["email"]).first()
        assert db_user is not None
        assert db_user.username == "john"
        # Verify password is stored as hash, NOT plain text
        assert db_user.password_hash != register_payload["password"]
    finally:
        db.close()


def test_register_duplicate_email(register_payload):
    """POST /auth/register with a duplicate email must return HTTP 400."""
    # First registration — must succeed
    first_response = client.post("/auth/register", json=register_payload)
    assert first_response.status_code == 201

    # Second registration with same email — must fail
    duplicate_payload = register_payload.copy()
    duplicate_payload["username"] = "another_user"
    second_response = client.post("/auth/register", json=duplicate_payload)
    assert second_response.status_code == 400


@pytest.mark.parametrize("missing_field", ["username", "email", "password"])
def test_register_missing_fields(register_payload, missing_field):
    """POST /auth/register must return HTTP 422 when required fields are missing."""
    incomplete_payload = register_payload.copy()
    del incomplete_payload[missing_field]

    response = client.post("/auth/register", json=incomplete_payload)
    assert response.status_code == 422
