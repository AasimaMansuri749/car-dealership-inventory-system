"""
Developer-only script to create an ADMIN user in the database.

This script is intentionally NOT exposed through any public API endpoint.
Admin accounts should only be created by developers with direct database access.

Usage:
    python scripts/create_admin.py

You will be prompted for the admin's username, email, and password.
Alternatively, set the following environment variables to skip prompts:
    ADMIN_USERNAME
    ADMIN_EMAIL
    ADMIN_PASSWORD
"""

import sys
import os

# Ensure the backend/app package is importable regardless of where the
# script is called from.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database.database import SessionLocal, init_db
from app.repositories import user_repository
from app.core.security import hash_password
from app.exceptions.user_exceptions import UserAlreadyExists


def create_admin(username: str, email: str, password: str) -> None:
    """
    Insert an ADMIN user into the database.

    Raises:
        UserAlreadyExists: if the email is already registered.
    """
    init_db()
    db = SessionLocal()

    try:
        existing = user_repository.get_user_by_email(db, email)
        if existing:
            raise UserAlreadyExists(f"A user with email '{email}' already exists.")

        user_data = {
            "username": username,
            "email": email,
            "password_hash": hash_password(password),
            "role": "ADMIN",
        }

        admin_user = user_repository.create_user(db, user_data)
        print(
            f"\n✅  Admin user created successfully!\n"
            f"   ID       : {admin_user.id}\n"
            f"   Username : {admin_user.username}\n"
            f"   Email    : {admin_user.email}\n"
            f"   Role     : {admin_user.role}\n"
        )
    finally:
        db.close()


if __name__ == "__main__":
    username = os.environ.get("ADMIN_USERNAME") or input("Admin username : ").strip()
    email    = os.environ.get("ADMIN_EMAIL")    or input("Admin email    : ").strip()
    password = os.environ.get("ADMIN_PASSWORD") or input("Admin password : ").strip()

    if not username or not email or not password:
        print("❌  All fields (username, email, password) are required.")
        sys.exit(1)

    try:
        create_admin(username, email, password)
    except UserAlreadyExists as exc:
        print(f"❌  {exc}")
        sys.exit(1)
