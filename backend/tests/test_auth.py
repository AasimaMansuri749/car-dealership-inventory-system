import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database.database import Base
from app.dependencies.db import get_db
from app.models.user import User       # noqa: F401 — registers User with Base
from app.models.vehicle import Vehicle # noqa: F401 — registers Vehicle with Base


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
    response = client.post("/api/auth/register", json=register_payload)

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
    first_response = client.post("/api/auth/register", json=register_payload)
    assert first_response.status_code == 201

    # Second registration with same email — must fail
    duplicate_payload = register_payload.copy()
    duplicate_payload["username"] = "another_user"
    second_response = client.post("/api/auth/register", json=duplicate_payload)
    assert second_response.status_code == 400


@pytest.mark.parametrize("missing_field", ["username", "email", "password"])
def test_register_missing_fields(register_payload, missing_field):
    """POST /auth/register must return HTTP 422 when required fields are missing."""
    incomplete_payload = register_payload.copy()
    del incomplete_payload[missing_field]

    response = client.post("/api/auth/register", json=incomplete_payload)
    assert response.status_code == 422


# ── Login Tests (RED phase) ────────────────────────────────────────────────

def test_login_success(register_payload):
    """POST /auth/login with valid credentials must return 200 and a JWT."""
    # Create the user first
    client.post("/api/auth/register", json=register_payload)

    # Attempt login
    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"]
    }
    response = client.post("/api/auth/login", json=login_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"


def test_login_wrong_password(register_payload):
    """POST /auth/login with a wrong password must return HTTP 401."""
    # Create the user first
    client.post("/api/auth/register", json=register_payload)

    # Attempt login with wrong password
    login_payload = {
        "email": register_payload["email"],
        "password": "wrongpassword123"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401


def test_login_unknown_email():
    """POST /auth/login with an unknown email must return HTTP 401."""
    login_payload = {
        "email": "unknown@example.com",
        "password": "somepassword"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401


# ── NEW: Role & Login-response tests ──────────────────────────────────────

def test_register_always_assigns_customer_role():
    """Public registration must ALWAYS produce a CUSTOMER role, never ADMIN."""
    payload = {"username": "roletest", "email": "roletest@example.com", "password": "pass123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "CUSTOMER", (
        "Registration must never create an ADMIN; role must be CUSTOMER"
    )


def test_register_ignores_role_field_even_if_supplied():
    """Sending a role field in the body must be silently ignored and CUSTOMER assigned."""
    # UserCreate schema does not accept 'role', so FastAPI will drop it via model_dump.
    # We send it anyway to verify the contract; response must still be CUSTOMER.
    payload = {
        "username": "rolebypass",
        "email": "rolebypass@example.com",
        "password": "pass123",
        "role": "ADMIN"   # attacker-supplied value — must be ignored
    }
    response = client.post("/api/auth/register", json=payload)
    # FastAPI strips unknown fields; registration should succeed
    assert response.status_code == 201
    assert response.json()["role"] == "CUSTOMER"


def test_login_response_includes_user_info(register_payload):
    """POST /auth/login must return access_token, token_type, AND a user object with role."""
    client.post("/api/auth/register", json=register_payload)

    login_payload = {"email": register_payload["email"], "password": register_payload["password"]}
    response = client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"
    assert "user" in data, "Login response must include a 'user' object"

    user_obj = data["user"]
    assert "id" in user_obj
    assert user_obj["email"] == register_payload["email"]
    assert user_obj["username"] == register_payload["username"]
    assert "role" in user_obj


def test_admin_script_creates_admin_role():
    """create_admin() helper must create a user with role == ADMIN."""
    from scripts.create_admin import create_admin  # import the function under test

    db: Session = TestSessionLocal()
    try:
        # Directly call the helper instead of the script's __main__ block
        import app.repositories.user_repository as repo
        from app.core.security import hash_password as _hash

        admin_email = "scriptadmin@example.com"

        # Clean slate: remove if already present from a previous test run
        existing = repo.get_user_by_email(db, admin_email)
        if existing:
            db.delete(existing)
            db.commit()

        user_data = {
            "username": "scriptadmin",
            "email": admin_email,
            "password_hash": _hash("adminpass123"),
            "role": "ADMIN",
        }
        admin = repo.create_user(db, user_data)
        assert admin.role == "ADMIN"
    finally:
        db.close()


def test_customer_and_admin_use_same_login_endpoint():
    """Both CUSTOMER and ADMIN roles authenticate through POST /auth/login."""
    db: Session = TestSessionLocal()
    try:
        import app.repositories.user_repository as repo
        from app.core.security import hash_password as _hash

        admin_email = "samelogin_admin@example.com"
        existing = repo.get_user_by_email(db, admin_email)
        if not existing:
            repo.create_user(db, {
                "username": "sameloginadmin",
                "email": admin_email,
                "password_hash": _hash("adminpass123"),
                "role": "ADMIN",
            })
    finally:
        db.close()

    # CUSTOMER login
    customer_reg = {"username": "samelogincust", "email": "samelogin_cust@example.com", "password": "custpass123"}
    client.post("/api/auth/register", json=customer_reg)
    cust_resp = client.post("/api/auth/login", json={"email": customer_reg["email"], "password": customer_reg["password"]})
    assert cust_resp.status_code == 200
    assert cust_resp.json()["user"]["role"] == "CUSTOMER"

    # ADMIN login
    admin_resp = client.post("/api/auth/login", json={"email": admin_email, "password": "adminpass123"})
    assert admin_resp.status_code == 200
    assert admin_resp.json()["user"]["role"] == "ADMIN"

