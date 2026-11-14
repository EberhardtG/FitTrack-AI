from fastapi import APIRouter
from app.rag.utils.ingest import ingest

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/reindex")
async def reindex_documents():

    ingest()

    return {
        "message":
        "Documents re-indexed successfully."
    }