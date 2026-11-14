from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class WeightCreate(BaseModel):
    """
    Schema for creating a new weight entry.
    """
    value: float = Field(gt=0, lt=700, description="Weight value in kilograms")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "value": 70.5,
                    
                }
            })

class WeightRead(BaseModel):
    """
    Schema for reading weight entries.
    """
    id: int
    user_id: int
    value: float
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "value": 70.5,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        })

class WeightUpdate(BaseModel):
    """
    Schema for updating weight entries.
    """
    value: float | None = Field(default=None, gt=0, lt=700, description="Weight value in kilograms")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "value": 72.0
        }
    })

class WeightDelete(BaseModel):
    """
    Schema for deleting weight entries.
    """
    id: int
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1
        }
    })