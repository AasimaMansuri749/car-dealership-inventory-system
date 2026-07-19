from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import create_access_token
from app.services import auth_service
from app.exceptions.user_exceptions import UserAlreadyExists, InvalidCredentials

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user. Returns 400 if the email is already taken."""
    try:
        return auth_service.register_user(db, user_data.model_dump())
    except UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password to receive a JWT access token and user info."""
    try:
        user = auth_service.authenticate_user(db, login_data.email, login_data.password)
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
    }

from app.dependencies.auth import get_current_user
from app.models.user import User

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return current_user



