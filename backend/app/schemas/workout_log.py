from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class WorkoutLogCreate(BaseModel):
    # Old fields (optional)
    workout_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z ]+$",
        description="Type of workout"
    )
    
    calories_burned: float | None = Field(
        default=None,
        description="Calories burned during the workout"
    )

    # New fields (optional)
    exercise_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z ]+$",
        description="Name of the exercise"
    )
    duration_minutes: float | None = Field(
        default=None,
        gt=0,
        description="Duration of the exercise in minutes"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "exercise_name": "Running",
                "duration_minutes": 30.5,
                "workout_type": "Cardio",
                "calories_burned": 300
            }
        }
    )



class WorkoutLogRead(BaseModel):
    id: int
    user_id: int
    workout_type: str | None
    exercise_name: str | None
    duration_minutes: float | None
    calories_burned: float | None
    created_at: datetime
    updated_at: datetime

    


    model_config = ConfigDict(from_attributes=True, json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "workout_type": "Running",
                "duration_minutes": 30.5,
                "calories_burned": 300.0,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        })

class WorkoutLogUpdate(BaseModel):
    """
    Schema for updating workout log entries.
    """
    workout_type: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"^[A-Za-z ]+$", description="Type of workout")
    duration_minutes: float | None = Field(default=None, gt=0, description="Duration of the workout in minutes")
    calories_burned: float | None = Field(default=None, description="Calories burned during the workout")
    exercise_name: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"^[A-Za-z ]+$", description="Name of the exercise")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "workout_type": "Cycling",
            "duration_minutes": 45.0,
            "calories_burned": 400.0
        }
    })

class WorkoutLogDelete(BaseModel):
    """
    Schema for deleting workout log entries.
    """
    id: int
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1
        }
    })  

class WorkoutLogSuggest(BaseModel):
    """
    Request body for workout suggestion queries.
    Used by the AI/RAG endpoint to generate personalized workout advice.
    """
    question: str = Field(min_length=3, max_length=500, description="User's workout question", pattern=r"\S")
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "question": "What is a good 3-day workout split for fat loss?"
        }
    })