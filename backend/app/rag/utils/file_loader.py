import os
from typing import List, Dict
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once 
settings = RAGSettings()


def load_raw_documents(directory: str = None) -> List[Dict]:
    """
    Load all .txt documents from the raw_docs directory.
    Returns: [{"source": filename, "text": content}]
    """

    # Use instance settings if no directory provided
    if directory is None:
        directory = settings.RAW_DOCS_DIR

    docs = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({
                    "source": filename,
                    "text": f.read()
                })

    return docs
