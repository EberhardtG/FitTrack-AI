from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class WorkoutAsk(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="User's workout-related question"
    )

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "question": "Can you suggest a workout plan to improve my chest strength?"
        }
    })


class WorkoutRecommendation(BaseModel):
    recommendation: str
    reasoning: str
    sources: list[str] | None = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "recommendation": "Focus on progressive overload bench press, incline dumbbell press, and dips.",
            "reasoning": "Your workout logs show consistent chest training but limited volume. Increasing volume and adding compound movements will improve strength.",
            "sources": ["user_weight_history", "user_workout_logs"]
        }
    })

