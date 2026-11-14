from sentence_transformers import SentenceTransformer
from typing import List
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once (required for Pydantic v2)
settings = RAGSettings()


class Embedder:
    """
    Wrapper around SentenceTransformer for generating embeddings.
    """

    def __init__(self, model_name: str = None):
        # Use instance settings if no model name provided
        if model_name is None:
            model_name = settings.EMBEDDING_MODEL

        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string and return a vector.
        """
        return self.model.encode(text).tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple text strings at once.
        """
        return self.model.encode(texts).tolist()


# Global embedder instance
embedder = Embedder()
