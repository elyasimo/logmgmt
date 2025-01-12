from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.api.database import get_db
from Backend.api.models import User, UserCreate, UserUpdate, UserResponse
from typing import List
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to create user: {user.username}")
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            name=user.name,
            role=user.role,
            hashed_password=hashed_password,
            auth_method=user.auth_method,
            external_id=user.external_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created successfully: {user.username}")
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        logger.exception("Traceback:")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to update user with ID: {user_id}")
    logger.info(f"Received update data: {user.dict(exclude_unset=True)}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    try:
        db.commit()
        db.refresh(db_user)
        logger.info(f"User updated successfully: {db_user.username}")
        return db_user
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

