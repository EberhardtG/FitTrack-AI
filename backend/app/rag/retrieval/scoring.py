# app/rag/retrieval/scoring.py

from sentence_transformers import SentenceTransformer, util
import numpy as np

class RetrievalScorer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def score(self, question: str, chunk: str) -> float:
        """Return semantic similarity score between question and chunk."""
        q_emb = self.model.encode(question, convert_to_tensor=True)
        c_emb = self.model.encode(chunk, convert_to_tensor=True)
        sim = util.cos_sim(q_emb, c_emb).item()
        return float(sim)

    def rank_chunks(self, question: str, chunks: list):
        """Rank chunks by semantic relevance."""
        scored = []
        for c in chunks:
            score = self.score(question, c["text"])
            scored.append({
                "text": c["text"],
                "source": c["source"],
                "score": score
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored
