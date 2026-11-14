import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.security.auth import get_current_user
from app.schemas.user import UserRead, UserUpdate
from app.db import get_db
from app.models.users import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Module-level logger
logger = logging.getLogger(__name__)


#---/users/me---
@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user))-> UserRead:
    """Fetch the currently authenticated user's information."""
    logger.info(f"Fetching current user: {current_user.email}")
    if not current_user:
        logger.error("Current user not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return current_user


#-----/users/{user_id}---
@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
)-> UserRead:
    """Fetch a user by ID. Only the authenticated user can access their own data."""
    logger.info(f"Fetching user with ID: {user_id}")

    # Authorization: users can only access themselves
    if current_user.id != user_id:
        logger.warning(
            f"Unauthorized access attempt by user_id={current_user.id} "
            f"for user_id={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user"
        )

    # Fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

#---patch /users/{user_id}---
@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,   # <-- IMPORTANT: must NOT be UserRead
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserRead:
    """Update user information. Only the authenticated user can update their own data."""
    logger.info(f"Updating user with ID: {user_id}")

    # Authorization: users can only update themselves
    if current_user.id != user_id:
        logger.warning(
            f"Unauthorized update attempt by user_id={current_user.id} "
            f"for user_id={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user"
        )

    # Fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    if user_update.email:
     existing = db.query(User).filter(User.email == user_update.email).first()
    if existing and existing.id != user_id:
        raise HTTPException(400, "Email already in use")

    try:
        db.commit()
        db.refresh(user)
        logger.info(f"User with ID {user_id} updated successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during update of user_id={user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    return user

#---Delete /users/{user_id}---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a user. Only the authenticated user can delete their own account."""
    logger.info(f"Deleting user with ID: {user_id}")

    # Authorization: users can only delete themselves
    if current_user.id != user_id:
        logger.warning(
            f"Unauthorized delete attempt by user_id={current_user.id} "
            f"for user_id={user_id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this user"
        )

    # Fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        db.delete(user)
        db.commit()
        logger.info(f"User with ID {user_id} deleted successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during deletion of user_id={user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )