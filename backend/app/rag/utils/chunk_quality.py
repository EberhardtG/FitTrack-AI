import re
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once 
settings = RAGSettings()


class ChunkQualityEvaluator:
    def __init__(
        self,
        min_length=None,
        max_length=None,
        min_density=None,
        keyword_boost=None,
        filter_noise=None,
        fitness_keywords=None
    ):
        # Use settings values if not provided
        self.min_length = min_length if min_length is not None else settings.CHUNK_MIN_LENGTH
        self.max_length = max_length if max_length is not None else settings.CHUNK_MAX_LENGTH
        self.min_density = min_density if min_density is not None else settings.CHUNK_MIN_DENSITY
        self.keyword_boost = keyword_boost if keyword_boost is not None else settings.CHUNK_KEYWORD_BOOST
        self.filter_noise = filter_noise if filter_noise is not None else settings.CHUNK_FILTER_NOISE

        self.fitness_keywords = fitness_keywords or [
            "exercise", "workout", "fitness", "rest", "sleep",
            "calories", "training", "cardio", "strength", "health"
        ]

    def is_noise(self, text: str) -> bool:
        noise_patterns = [
            r"copyright",
            r"all rights reserved",
            r"terms of service",
            r"navigation",
            r"header",
            r"footer",
            r"disclaimer"
        ]
        return any(re.search(p, text.lower()) for p in noise_patterns)

    def density_score(self, text: str) -> float:
        words = text.split()
        meaningful = [w for w in words if len(w) > 3]
        return len(meaningful) / max(len(words), 1)

    def keyword_score(self, text: str) -> float:
        text_lower = text.lower()
        return sum(1 for kw in self.fitness_keywords if kw in text_lower)

    def evaluate(self, text: str) -> float:
        # Length filtering
        if len(text) < self.min_length:
            return 0.0
        if len(text) > self.max_length:
            return 0.0

        # Noise filtering
        if self.filter_noise and self.is_noise(text):
            return 0.0

        # Density scoring
        density = self.density_score(text)
        if density < self.min_density:
            return 0.0

        # Final score
        return density + (self.keyword_boost * self.keyword_score(text))
