# Walkthrough — Database Setup

## Created Files

| File | Purpose |
|------|---------|
| [database.py](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/app/database/database.py) | SQLAlchemy engine, `SessionLocal`, `Base` (DeclarativeBase), and `init_db()` |
| [user.py](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/app/models/user.py) | `User` model with id, username, email, password_hash, role |
| [vehicle.py](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/app/models/vehicle.py) | `Vehicle` model with id, make, model, category, price, quantity |
| [__init__.py](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/app/models/__init__.py) | Exports `User` and `Vehicle` models |
| [test_database.py](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/tests/test_database.py) | 4 tests covering engine connection, model imports, and table creation |

## Modified Files

| File | Change |
|------|--------|
| [requirements.txt](file:///c:/Users/aasim/OneDrive/Desktop/Incubyte_assesment/car-dealership-inventory-system/backend/requirements.txt) | Replaced bloated 300+ package list with clean project dependencies |

## Deleted Files

| File | Reason |
|------|--------|
| `backend/app/database/session.py` | Temporary file, replaced by `database.py` |
| `backend/app/core/config.py` | Temporary file, no longer needed |

## Database Structure

```
Database: sqlite:///./car_inventory.db

┌─────────────────────────┐      ┌─────────────────────────┐
│         users           │      │        vehicles         │
├─────────────────────────┤      ├─────────────────────────┤
│ id       INTEGER (PK)   │      │ id       INTEGER (PK)   │
│ username STRING  (req)  │      │ make     STRING  (req)  │
│ email    STRING  (uniq) │      │ model    STRING  (req)  │
│ password_hash STRING    │      │ category STRING  (req)  │
│ role     STRING ="CUSTOMER"│   │ price    FLOAT   (req)  │
└─────────────────────────┘      │ quantity INTEGER = 0    │
                                 └─────────────────────────┘
```

## Test Results

```
tests/test_database.py::test_engine_connects_successfully PASSED   [ 20%]
tests/test_database.py::test_user_model_can_be_imported PASSED     [ 40%]
tests/test_database.py::test_vehicle_model_can_be_imported PASSED  [ 60%]
tests/test_database.py::test_tables_are_created_successfully PASSED[ 80%]
tests/test_main.py::test_root_endpoint PASSED                      [100%]

======================== 5 passed in 1.43s =========================
```
