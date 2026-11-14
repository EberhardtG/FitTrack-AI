import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.security.auth import get_current_user
from app.schemas.user import UserRead
from app.db import get_db
from app.models.users import User
from app.models.weight import Weight
from app.schemas.weight import WeightCreate, WeightRead, WeightUpdate



router = APIRouter(
    prefix="/weights",
    tags=["Weights"]
)

# Module-level logger
logger = logging.getLogger(__name__)


#---Post /weights---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WeightRead)
async def create_weight(
    weight_in: WeightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
)-> WeightRead:
    logger.info(f"Creating weight entry for user_id={current_user.id} with value={weight_in.value}")

    if weight_in.value <= 0:
        logger.error("Invalid weight value provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be a positive number"
        )
    if weight_in.value > 1000:
        logger.error("Weight value is unrealistic")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight value is unrealistic"
        )


    new_weight = Weight(
        user_id=current_user.id,
        value=weight_in.value
    )
    
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    

    existing = db.query(Weight).filter(
    Weight.user_id == current_user.id,
    Weight.created_at >= today_start
    ).first()


    if existing:
        logger.warning(f"User_id={current_user.id} attempted to log weight again today")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight already logged today"
        )


    try:
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while creating weight entry: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    logger.info(f"Weight entry created successfully with id={new_weight.id}")
    return new_weight


#---Get /weights---
@router.get("/", response_model=list[WeightRead])
async def get_weights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[WeightRead]:

    logger.info(f"Fetching weight history for user_id={current_user.id}")

    weights = (
        db.query(Weight)
        .filter(Weight.user_id == current_user.id)
        .order_by(Weight.created_at.desc())
        .all()
    )

    if not weights:
        logger.info(f"No weight entries found for user_id={current_user.id}")

    return weights

#---Patch /weights/{weight_id}---
@router.patch("/{weight_id}", response_model=WeightRead)
async def update_weight(
    weight_id: int,
    weight_in: WeightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> WeightRead:
    logger.info(f"Updating weight entry id={weight_id} for user_id={current_user.id}")

    weight_entry = db.query(Weight).filter(
        Weight.id == weight_id,
        Weight.user_id == current_user.id
    ).first()

    if not weight_entry:
        logger.error(f"Weight entry id={weight_id} not found for user_id={current_user.id}")
        raise HTTPException(404, "Weight entry not found")

    if weight_in.value is None:
        raise HTTPException(400, "No fields provided for update")

    # Duplicate-day protection
    today_start = datetime.utcnow().replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0
)

    if weight_entry.created_at < today_start:
        existing_today = db.query(Weight).filter(
            Weight.user_id == current_user.id,
            Weight.created_at >= today_start
        ).first()

        if existing_today:
            raise HTTPException(400, "You already logged a weight today")

    # Update value
    weight_entry.value = weight_in.value

    try:
        db.commit()
        db.refresh(weight_entry)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while updating weight entry id={weight_id}: {e}")
        raise HTTPException(500, "Internal server error")

    logger.info(f"Weight entry id={weight_id} updated successfully")
    return weight_entry


#---DELETE /weights/{weight_id}---
@router.delete("/{weight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weight(
    weight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Deleting weight entry id={weight_id} for user_id={current_user.id}")

    weight_entry = db.query(Weight).filter(
        Weight.id == weight_id,
        Weight.user_id == current_user.id
    ).first()

    if not weight_entry:
        logger.error(f"Weight entry id={weight_id} not found for user_id={current_user.id}")
        raise HTTPException(404, "Weight entry not found")
    
    today_start = datetime.utcnow().replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0
)

    if weight_entry.created_at >= today_start:
        logger.warning(f"User attempted to delete today's weight entry id={weight_id}")


    try:
        db.delete(weight_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error while deleting weight entry id={weight_id}: {e}")
        raise HTTPException(500, "Internal server error")

    logger.info(f"Weight entry id={weight_id} deleted successfully")

    return None