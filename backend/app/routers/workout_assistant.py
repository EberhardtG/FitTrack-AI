import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta



from app.security.auth import get_current_user
from app.schemas.user import UserRead

from app.db import get_db
from app.models.users import User
from app.schemas.workout_assistant import WorkoutRecommendation, WorkoutAsk
from app.models.weight import Weight
from app.models.workout_log import WorkoutLog
from app.rag.pipeline.pipeline import run_workout_rag

router = APIRouter(
    prefix="/workouts",
    tags=["Workout Assistant"]
)
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=WorkoutRecommendation)
async def ask_workout(
    request: WorkoutAsk,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Workout assistant invoked by user_id={current_user.id}")

    # 1. Sanitize input
    question = request.question.strip()
    if not question:
        raise HTTPException(400, "Question cannot be empty")
    
    forbidden_phrases = ["ignore previous", "system:", "override", "bypass", "jailbreak"]
    if any(p in question.lower() for p in forbidden_phrases):
     raise HTTPException(400, "Invalid or unsafe question")

    # 2. Retrieve user context (weights + logs)
    weights = db.query(Weight).filter(Weight.user_id == current_user.id).all()
    logs = db.query(WorkoutLog).filter(WorkoutLog.user_id == current_user.id).all()

    if not weights and not logs:
        raise HTTPException(400, "You must log at least one weight or workout before asking for recommendations.")
    
    if len(question.split()) < 3:
        raise HTTPException(400, "Please ask a more detailed workout-related question.")


    for w in weights:
        if w.value <= 0 or w.value > 1000:
            raise HTTPException(400, "Invalid weight data detected. Please correct your weight logs.")

    # 3. Run your RAG pipeline 
    try:
        recommendation, reasoning = run_workout_rag(question, weights, logs)
    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        raise HTTPException(500, "Workout assistant failed to generate a recommendation.")


    return WorkoutRecommendation(
        recommendation=recommendation,
        reasoning=reasoning,
        sources=["weights", "workout_logs"]
    )
    