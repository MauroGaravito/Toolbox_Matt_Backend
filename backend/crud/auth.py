from sqlalchemy.orm import Session
from models import User
from schemas.auth import TokenData
from security import verify_password, hash_password, create_access_token
from fastapi import HTTPException
from datetime import timedelta

def authenticate_user(db: Session, username: str, password: str):
    """Verifies if the user and password are correct."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user: User):
    """Generates a JWT for the authenticated user."""
    access_token_expires = timedelta(minutes=30)
    return create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

def register_user(db: Session, username: str, email: str, password: str):
    """Registers a new user if the email is not in use."""
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
