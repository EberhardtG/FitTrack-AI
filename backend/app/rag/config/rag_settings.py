from pydantic_settings import BaseSettings

class RAGSettings(BaseSettings):
    # Ollama configuration
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"

    # Chroma persistent DB
    CHROMA_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "fittrack_docs"

    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Raw + processed document directories
    RAW_DOCS_DIR: str = "/app/app/rag/data/raw_docs"
    PROCESSED_DOCS_DIR: str = "/app/app/rag/data/processed_docs"
    CHUNKS_JSON_PATH: str = "/app/app/rag/data/processed_docs/chunks.json"

    # Retrieval settings
    MAX_CONTEXT_CHUNKS: int = 5
    MAX_LOGS: int = 5

    # Prompt behavior
    INCLUDE_SOURCE_REFERENCES: bool = True
    ENABLE_EXPLAINABILITY: bool = True

    # Chunking settings 
    CHUNK_MIN_LENGTH: int = 40
    CHUNK_MAX_LENGTH: int = 800
    CHUNK_MIN_DENSITY: float = 0.15
    CHUNK_KEYWORD_BOOST: float = 0.1
    CHUNK_FILTER_NOISE: bool = True

    # Header micro‑chunk settings 
    HEADER_MIN_WORDS: int = 40
    HEADER_MAX_WORDS: int = 120

    # Paragraph chunk settings 
    PARAGRAPH_MIN_WORDS: int = 120
    PARAGRAPH_MAX_WORDS: int = 250

    # Retrieval scoring thresholds
    RETRIEVAL_MIN_SCORE: float = 0.15
    RETRIEVAL_MAX_RANKED: int = 5

    model_config = {
    "env_file": ".env",
    "validate_assignment": True
}
