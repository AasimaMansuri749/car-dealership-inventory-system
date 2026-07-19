from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

# bcrypt hashing context
# _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False
)
# JWT Constants
SECRET_KEY = "my_super_secret_key_for_jwt_tokens"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def hash_password(password: str) -> str:
#     """Return a bcrypt hash of the given plain-text password."""
#     return _pwd_context.hash(password)

def hash_password(password: str) -> str:
    """Return a bcrypt hash of the given plain-text password."""
    return _pwd_context.hash(password[:72])


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a plain-text password against a bcrypt hash."""
#     return _pwd_context.verify(plain_password, hashed_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return _pwd_context.verify(
        plain_password[:72],
        hashed_password
    )

def create_access_token(data: dict) -> str:
    """Create a new JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
