import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.security.auth import get_current_user, hash_password, verify_password, create_access_token 
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import LoginRequest, TokenResponse 
from app.db import get_db
from app.models.users import User


router = APIRouter()

# Module-level logger
logger = logging.getLogger(__name__)

FAILED_LOGINS = {}
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 10


# -----------------------------
# REGISTER
# -----------------------------

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    logger.info(f"Attempting to register user: {user.email}")
    email = user.email.lower()
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        logger.warning(f"User with email {user.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    hashed_password = hash_password(user.password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        name=user.name
    )
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during registration: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    db.refresh(new_user)
    logger.info(f"User registered successfully: {new_user.id}")
    return new_user

# -----------------------------
# LOGIN
# -----------------------------


@router.post("/token", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db))-> TokenResponse:
    email = data.email.lower()

    # Check lockout
    record = FAILED_LOGINS.get(email)
    if record:
        attempts, lockout_until = record
        if lockout_until and datetime.now(timezone.utc) < lockout_until:
            logger.warning(f"Lockout triggered for {email}")
            raise HTTPException(
                status_code=429,
                detail="Too many failed attempts. Try again later."
            )


    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        # Update failed attempts
        attempts = record[0] + 1 if record else 1

        if attempts >= MAX_ATTEMPTS:
            FAILED_LOGINS[email] = (
                attempts,
                datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_MINUTES)
            )
        else:
            FAILED_LOGINS[email] = (attempts, None)

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Reset failed attempts on success
    FAILED_LOGINS[email] = (0, None)

    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")

# -----------------------------
# CURRENT USER
# -----------------------------
@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user))-> UserRead:
    """Endpoint to get the current authenticated user's information."""
    logger.info(f"/me endpoint accessed by user_id={current_user.id}")
    return current_user

