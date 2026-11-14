from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator
import os

# Load DATABASE_URL from environment (use python-dotenv or os.getenv)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")


#Create the engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} # SQLite requires check_same_thread=False for use with FastAPI

    )
else:
    engine = create_engine(DATABASE_URL)


# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


# TODO: Implement get_db
def get_db() -> Generator[Session, None, None]:
    """Provides a DB session per request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()