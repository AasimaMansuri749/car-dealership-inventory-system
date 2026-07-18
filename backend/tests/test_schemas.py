import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError

# These imports will fail because the schemas module or classes do not exist yet (RED Phase)
try:
    from app.schemas.vehicle import VehicleCreate, VehicleResponse
except ImportError:
    VehicleCreate = None
    VehicleResponse = None


# Mocking a vehicle model instance for testing response serialization
class MockVehicleModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def valid_vehicle_data():
    return {
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": Decimal("25000.00"),
        "quantity": 5,
        "description": "Reliable sedan",
        "year": 2023,
        "color": "Silver",
        "mileage": 15,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "image_url": "http://example.com/camry.jpg",
    }


def test_schemas_are_imported():
    """Ensure schemas are defined and can be imported."""
    assert VehicleCreate is not None, "VehicleCreate schema is not implemented"
    assert VehicleResponse is not None, "VehicleResponse schema is not implemented"


def test_vehicle_create_accepts_valid_data(valid_vehicle_data):
    """VehicleCreate should successfully instantiate with valid data."""
    schema = VehicleCreate(**valid_vehicle_data)
    assert schema.make == "Toyota"
    assert schema.price == Decimal("25000.00")
    assert schema.quantity == 5


def test_vehicle_create_rejects_negative_price(valid_vehicle_data):
    """VehicleCreate must reject negative prices."""
    invalid_data = valid_vehicle_data.copy()
    invalid_data["price"] = Decimal("-100.00")
    with pytest.raises(ValidationError) as exc_info:
        VehicleCreate(**invalid_data)
    assert "price" in str(exc_info.value)


def test_vehicle_create_rejects_negative_quantity(valid_vehicle_data):
    """VehicleCreate must reject negative quantities."""
    invalid_data = valid_vehicle_data.copy()
    invalid_data["quantity"] = -1
    with pytest.raises(ValidationError) as exc_info:
        VehicleCreate(**invalid_data)
    assert "quantity" in str(exc_info.value)


@pytest.mark.parametrize("mandatory_field", ["make", "model", "category", "price", "quantity"])
def test_vehicle_create_requires_mandatory_fields(valid_vehicle_data, mandatory_field):
    """VehicleCreate must fail validation if any mandatory fields are missing."""
    invalid_data = valid_vehicle_data.copy()
    del invalid_data[mandatory_field]
    with pytest.raises(ValidationError) as exc_info:
        VehicleCreate(**invalid_data)
    assert mandatory_field in str(exc_info.value)


def test_vehicle_response_serialization(valid_vehicle_data):
    """VehicleResponse should successfully serialize ORM model attributes."""
    created_at_val = datetime.now()
    updated_at_val = datetime.now()

    # Create mock database record
    mock_db_vehicle = MockVehicleModel(
        id=42,
        created_at=created_at_val,
        updated_at=updated_at_val,
        **valid_vehicle_data
    )

    # Serialize using schema
    response_schema = VehicleResponse.model_validate(mock_db_vehicle)
    
    assert response_schema.id == 42
    assert response_schema.make == "Toyota"
    assert response_schema.price == Decimal("25000.00")
    assert response_schema.quantity == 5
    assert response_schema.description == "Reliable sedan"
    assert response_schema.year == 2023
    assert response_schema.color == "Silver"
    assert response_schema.mileage == 15
    assert response_schema.fuel_type == "Petrol"
    assert response_schema.transmission == "Automatic"
    assert response_schema.image_url == "http://example.com/camry.jpg"
    assert response_schema.created_at == created_at_val
    assert response_schema.updated_at == updated_at_val
