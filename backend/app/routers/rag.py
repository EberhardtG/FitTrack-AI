from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas.weight import WeightRead
from app.schemas.workout_log import WorkoutLogRead
from app.rag.pipeline import run_workout_rag
from app.rag.config.rag_settings import RAGSettings


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class RAGRequest(BaseModel):
    question: str
    weights: list[WeightRead] = Field(default_factory=list)
    logs: list[WorkoutLogRead] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "question": "what is good rest?",
                "weights": [
                    {
                        "created_at": "2023-01-01T12:00:00Z",
                        "id": 1,
                        "updated_at": "2023-01-01T12:00:00Z",
                        "user_id": 1,
                        "value": 70.5
                    }
                ],
                "logs": [
                    {
                        "exercise_name": "Running",
                        "workout_type": "Running",
                        "duration_minutes": 30.5,
                        "calories_burned": 300,
                        "created_at": "2023-01-01T12:00:00Z",
                        "updated_at": "2023-01-01T12:00:00Z",
                        "id": 1,
                        "user_id": 1
                    }
                ]
            }
        }

class RAGResponse(BaseModel):
    answer: str
    reasoning_prompt: str
    used_chunks: int
    model_used: str
    ollama_url: str
    explainability_enabled: bool
    source_references_enabled: bool



@router.post("/", response_model=RAGResponse)

def rag_endpoint(payload: RAGRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer, prompt = run_workout_rag(
            question=payload.question,
            weights=payload.weights,
            logs=payload.logs
        )

        return RAGResponse(
    answer=answer,
    reasoning_prompt=prompt,
    used_chunks=RAGSettings.MAX_CONTEXT_CHUNKS,
    model_used=RAGSettings.OLLAMA_MODEL,
    ollama_url=RAGSettings.OLLAMA_URL,
    explainability_enabled=RAGSettings.ENABLE_EXPLAINABILITY,
    source_references_enabled=RAGSettings.INCLUDE_SOURCE_REFERENCES
)


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
