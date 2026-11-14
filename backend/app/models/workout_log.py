from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from app.db import Base
from datetime import datetime


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    
    workout_type = Column(String, nullable=True)
    calories_burned = Column(Float, nullable=True)

    
    exercise_name = Column(String, nullable=True)
    duration_minutes = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="workout_logs")

    def __repr__(self):
        return f"<WorkoutLog id={self.id} type={self.workout_type} duration={self.duration_minutes} calories={self.calories_burned}>"
