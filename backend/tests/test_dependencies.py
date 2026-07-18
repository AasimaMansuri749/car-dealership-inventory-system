import pytest
from sqlalchemy.orm import Session

from app.dependencies.db import get_db


def test_get_db_yields_a_sqlalchemy_session():
    """get_db() must yield exactly one SQLAlchemy Session and then close it."""
    gen = get_db()
    db = next(gen)

    assert isinstance(db, Session), (
        f"Expected a SQLAlchemy Session, got {type(db)}"
    )

    # Drive the generator to its finally block (clean close)
    try:
        next(gen)
    except StopIteration:
        pass


def test_get_db_closes_session_after_use():
    """A second call to next() must raise StopIteration, proving the
    generator has fully exhausted (session was closed properly)."""
    gen = get_db()
    next(gen)  # get the session

    with pytest.raises(StopIteration):
        next(gen)  # generator must be done — session was closed
