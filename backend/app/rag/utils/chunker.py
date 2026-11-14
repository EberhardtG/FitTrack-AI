from typing import List, Dict
import re
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once 
settings = RAGSettings()


def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs based on blank lines.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def split_by_headers(text: str) -> List[str]:
    """
    Split text into header-based micro-chunks.
    Headers are lines starting with '#', '##', or '###'.
    """
    lines = text.split("\n")
    chunks = []
    current_chunk = []

    for line in lines:
        if re.match(r"^#{1,3}\s", line):  # header detected
            if current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                current_chunk = []
        current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    return chunks


def hybrid_chunk(text: str) -> List[Dict]:
    """
    Hybrid chunking strategy using RAGSettings:
    - Paragraph chunks (120–250 words)
    - Header micro-chunks (40–120 words)
    """
    chunks = []

    # -----------------------------
    # Header-based micro-chunks
    # -----------------------------
    header_chunks = split_by_headers(text)
    for chunk in header_chunks:
        word_count = len(chunk.split())
        if (
            settings.HEADER_MIN_WORDS
            <= word_count
            <= settings.HEADER_MAX_WORDS
        ):
            chunks.append({"text": chunk})

    # -----------------------------
    # Paragraph-based chunks
    # -----------------------------
    paragraphs = split_into_paragraphs(text)
    for p in paragraphs:
        word_count = len(p.split())
        if (
            settings.PARAGRAPH_MIN_WORDS
            <= word_count
            <= settings.PARAGRAPH_MAX_WORDS
        ):
            chunks.append({"text": p})

    return chunks
