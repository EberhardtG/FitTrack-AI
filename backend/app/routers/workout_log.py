import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta



from app.security.auth import get_current_user
from app.db import get_db
from app.models.users import User
from app.models.workout_log import WorkoutLog
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogRead, WorkoutLogUpdate
    

router = APIRouter(
    prefix="/workout_logs",
    tags=["Workout Logs"]
)

# Module-level logger
logger = logging.getLogger(__name__)

#-----Create workout log entry---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutLogRead)
async def create_workout_log(
    workout_log_in: WorkoutLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Creating workout log entry for user_id={current_user.id}")

    new_workout_log = WorkoutLog(
        user_id=current_user.id,
        workout_type=workout_log_in.workout_type,
        calories_burned=workout_log_in.calories_burned,
        exercise_name=workout_log_in.exercise_name,
        duration_minutes=workout_log_in.duration_minutes
    )


    try:
        db.add(new_workout_log)
        db.commit()
        db.refresh(new_workout_log)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during workout log creation: {e}")
        raise HTTPException(500, "Internal server error")

    logger.info(f"Workout log entry created successfully for user_id={current_user.id}")
    return new_workout_log


#---Get workout logs for current user---
@router.get("/", response_model=list[WorkoutLogRead])
async def get_workout_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Fetching workout logs for user_id={current_user.id}")

    workout_logs = (
        db.query(WorkoutLog)
        .filter(WorkoutLog.user_id == current_user.id)
        .order_by(WorkoutLog.created_at.desc())
        .all()
    )

    if not workout_logs:
        logger.info(f"No workout logs found for user_id={current_user.id}")

    return workout_logs

#---Patch workout log entry---
@router.patch("/{log_id}", response_model=WorkoutLogRead)
async def update_workout_log(
    log_id: int,
    workout_log_in: WorkoutLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Updating workout log entry id={log_id} for user_id={current_user.id}")

    workout_log_entry = db.query(WorkoutLog).filter(
        WorkoutLog.id == log_id,
        WorkoutLog.user_id == current_user.id
    ).first()

    if not workout_log_entry:
        raise HTTPException(404, "Workout log entry not found")

    if (
    workout_log_in.exercise_name is None and
    workout_log_in.duration_minutes is None and
    workout_log_in.workout_type is None and
    workout_log_in.calories_burned is None
):
     raise HTTPException(400, "No fields provided for update")

    
    if workout_log_in.duration_minutes is not None and workout_log_in.duration_minutes > 1000:
        raise HTTPException(400, "Duration value unrealistic")


    if workout_log_in.exercise_name is not None:
        workout_log_entry.exercise_name = workout_log_in.exercise_name

    if workout_log_in.duration_minutes is not None:
        workout_log_entry.duration_minutes = workout_log_in.duration_minutes

    if workout_log_in.workout_type is not None:
        workout_log_entry.workout_type = workout_log_in.workout_type

    if workout_log_in.calories_burned is not None:
        workout_log_entry.calories_burned = workout_log_in.calories_burned


    try:
        db.commit()
        db.refresh(workout_log_entry)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while updating workout log entry id={log_id}: {e}")
        raise HTTPException(500, "Internal server error")

    return workout_log_entry



#---Delete workout log entry---
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Deleting workout log entry id={log_id} for user_id={current_user.id}")

    workout_log_entry = db.query(WorkoutLog).filter(
        WorkoutLog.id == log_id,
        WorkoutLog.user_id == current_user.id
    ).first()

    if not workout_log_entry:
        logger.error(f"Workout log entry id={log_id} not found for user_id={current_user.id}")
        raise HTTPException(404, "Workout log entry not found")

    try:
        db.delete(workout_log_entry)
        db.commit()
        logger.info(f"Workout log entry id={log_id} deleted successfully for user_id={current_user.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error during deletion of workout log entry id={log_id}: {e}")
        raise HTTPException(500, "Internal server error")

    return None