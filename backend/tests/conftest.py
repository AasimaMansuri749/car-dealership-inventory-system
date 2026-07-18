import pytest
from sqlalchemy import text
from app.main import app
from app.dependencies.db import get_db
import sys

@pytest.fixture(autouse=True)
def fix_test_pollution(request):
    # Depending on which test module is running, grab its override_get_db
    module = request.module
    if hasattr(module, 'override_get_db'):
        app.dependency_overrides[get_db] = module.override_get_db
    
    yield
    
    # After each test, clear the users and vehicles tables to prevent pollution
    if hasattr(module, 'connection'):
        try:
            module.connection.execute(text("DELETE FROM users;"))
            module.connection.execute(text("DELETE FROM vehicles;"))
            module.connection.commit()
        except Exception:
            pass
