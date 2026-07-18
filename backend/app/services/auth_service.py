from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.core.security import hash_password, verify_password
from app.exceptions.user_exceptions import UserAlreadyExists, InvalidCredentials


def register_user(db: Session, user_data: dict):
    """
    Register a new user.
    """

    existing_user = user_repository.get_user_by_email(
        db,
        user_data["email"]
    )

    if existing_user:
        raise UserAlreadyExists("Email already registered")

    hashed_password = hash_password(
        user_data["password"]
    )

    user_data["password_hash"] = hashed_password
    del user_data["password"]

    return user_repository.create_user(
        db,
        user_data
    )


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate user during login.
    """

    user = user_repository.get_user_by_email(
        db,
        email
    )

    if not user:
        raise InvalidCredentials("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise InvalidCredentials("Invalid email or password")

    return user