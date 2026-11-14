import logging
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session


from app.security.config import settings
from app.models.users import User
from app.db import get_db




# -----------------------------------
# Logging
# -----------------------------------
logger = logging.getLogger(__name__)

# -----------------------------------
# JWT Setup
# -----------------------------------
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# -----------------------------------
# Password Hashing
# -----------------------------------
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

http_bearer = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256."""
    logger.info("Hashing password")
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password using pbkdf2_sha256."""
    logger.info("Verifying password")
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """Create a JWT access token with expiration."""
    logger.info("Creating JWT access token")

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("JWT created successfully")
    return token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),
    db: Session = Depends(get_db),
):
    """Extract token, decode JWT, and return the authenticated user."""
    token = credentials.credentials
    logger.info("Authenticating current user from JWT")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            logger.warning("JWT missing 'sub' field")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

    except JWTError as e:
        logger.warning(f"JWT decode failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        logger.error(f"Token references non-existent user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    logger.info(f"Authenticated user_id={user.id}")
    return user