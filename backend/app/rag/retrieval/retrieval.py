from app.rag.vectorstore.chroma_store import chroma_store
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once (required for Pydantic v2)
settings = RAGSettings()


class Retriever:
    """
    Retrieves top-K most relevant chunks from ChromaDB
    using the embedding similarity search.
    """

    def retrieve(self, query: str, top_k: int = None):
        # Use global setting if top_k not provided
        if top_k is None:
            top_k = settings.MAX_CONTEXT_CHUNKS  # Use existing setting

        results = chroma_store.query(query, top_k=top_k)

        # Normalize results into a consistent structure
        formatted = []
        for item in results:
            formatted.append({
                "source": item.get("source"),
                "text": item.get("text")
            })

        return formatted


# retriever instance
retriever = Retriever()

