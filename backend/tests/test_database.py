import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.database.database import Base, engine, SessionLocal, init_db
from app.models.user import User
from app.models.vehicle import Vehicle


# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def test_engine_connects_successfully():
    """Test that the database engine can establish a connection."""
    connection = test_engine.connect()
    assert connection is not None
    connection.close()


def test_user_model_can_be_imported():
    """Test that the User model can be imported and has correct table name."""
    assert User.__tablename__ == "users"


def test_vehicle_model_can_be_imported():
    """Test that the Vehicle model can be imported and has correct table name."""
    assert Vehicle.__tablename__ == "vehicles"


def test_tables_are_created_successfully():
    """Test that all tables are created successfully using Base.metadata."""
    Base.metadata.create_all(bind=test_engine)
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "vehicles" in tables
