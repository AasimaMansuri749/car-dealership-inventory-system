import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.database.database import Base

# Import models
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.order import Order
from app.models.order_item import OrderItem


# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def test_engine_connects_successfully():
    """Test that the database engine can establish a connection."""
    connection = test_engine.connect()
    assert connection is not None
    connection.close()


def test_user_model_has_all_attributes():
    """Test that the User model has the updated fields (created_at, updated_at)."""
    assert User.__tablename__ == "users"
    # New fields check
    assert hasattr(User, "created_at")
    assert hasattr(User, "updated_at")


def test_vehicle_model_has_all_attributes():
    """Test that the Vehicle model has all schema fields (year, transmission, description, etc.)."""
    assert Vehicle.__tablename__ == "vehicles"
    # Existing fields
    assert hasattr(Vehicle, "make")
    assert hasattr(Vehicle, "model")
    assert hasattr(Vehicle, "category")
    assert hasattr(Vehicle, "price")
    assert hasattr(Vehicle, "quantity")
    # New fields
    assert hasattr(Vehicle, "description")
    assert hasattr(Vehicle, "year")
    assert hasattr(Vehicle, "color")
    assert hasattr(Vehicle, "mileage")
    assert hasattr(Vehicle, "fuel_type")
    assert hasattr(Vehicle, "transmission")
    assert hasattr(Vehicle, "image_url")
    assert hasattr(Vehicle, "created_at")
    assert hasattr(Vehicle, "updated_at")


def test_order_models_exist():
    """Test that Order and OrderItem models are implemented."""
    assert Order is not None, "Order model is not implemented"
    assert OrderItem is not None, "OrderItem model is not implemented"
    assert Order.__tablename__ == "orders"
    assert OrderItem.__tablename__ == "order_items"


def test_tables_are_created_successfully():
    """Test that all tables (including orders and order_items) are created successfully."""
    from app.models import User, Vehicle, Order, OrderItem  # noqa: F401

    Base.metadata.create_all(bind=test_engine)
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    
    assert "users" in tables
    assert "vehicles" in tables
    assert "orders" in tables
    assert "order_items" in tables

