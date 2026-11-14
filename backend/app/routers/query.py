from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.security.auth import get_current_user
from app.models.users import User


from app.rag.pipeline.pipeline import run_workout_rag

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    route: str
    answer: str
    reason: str
    sources: list | None = None

@router.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest, current_user: User = Depends(get_current_user)):
    print("User ID:", current_user.id)

    # Your pipeline returns (model_output, prompt)
    model_output, prompt = run_workout_rag(
        question=payload.query,
        weights=current_user.weights,      #  store weights per user
        logs=current_user.workout_logs     #  store logs per user
    )

    # Wrap the pipeline output into your API response format
    return QueryResponse(
        route="rag",
        answer=model_output,
        reason=prompt,
        sources=None   #  add sources later if your pipeline returns them
    )
