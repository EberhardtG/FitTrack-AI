from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, Boolean, func 
from typing import Optional
from app.db import Base
from datetime import datetime



class User(Base):
    """
    SQLAlchemy model for the users table.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
        )
        


    #relationship to Weight model
    weights = relationship("Weight", back_populates="user", cascade="all, delete-orphan")

    #relationship to WorkoutLog model
    workout_logs = relationship(
        "WorkoutLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


    
   