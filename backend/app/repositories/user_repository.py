from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_data: dict) -> User:
    """Create a new user in the database."""
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
