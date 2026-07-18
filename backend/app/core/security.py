from passlib.context import CryptContext

# bcrypt hashing context — auto-upgrades hash rounds over time
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a bcrypt hash of the given plain-text password."""
    return _pwd_context.hash(password)
