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
