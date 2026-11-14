from asyncio.log import logger
from typing import List, Tuple
from datetime import datetime
import requests

from app.models.weight import Weight
from app.models.workout_log import WorkoutLog
from app.rag.pipeline.prompt_templates import build_prompt
from app.rag.retrieval.retrieval import retriever
from app.rag.retrieval.scoring import RetrievalScorer
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once 
settings = RAGSettings()

# Scorer now uses instance settings
scorer = RetrievalScorer(settings.EMBEDDING_MODEL)


def _sanitize_question(question: str) -> str:
    return " ".join(question.strip().split())


def _score_log_relevance(question: str, log: WorkoutLog) -> float:
    if not log.exercise_name:
        return 0.0
    q_tokens = set(question.lower().split())
    e_tokens = set(log.exercise_name.lower().split())
    overlap = q_tokens & e_tokens
    return float(len(overlap))


def _select_top_logs(question: str, logs: List[WorkoutLog]) -> List[WorkoutLog]:
    scored = [(log, _score_log_relevance(question, log)) for log in logs]
    scored = [pair for pair in scored if pair[1] > 0.0]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [log for log, _ in scored[:settings.MAX_LOGS]]


def _summarize_weights(weights: List[Weight]) -> str:
    if not weights:
        return "No weight history available."

    sorted_weights = sorted(weights, key=lambda w: w.created_at or datetime.min, reverse=True)
    latest = sorted_weights[0]
    values = [w.value for w in sorted_weights]
    avg = sum(values) / len(values)

    return (
        f"Latest recorded weight: {latest.value:.1f}. "
        f"Average recorded weight: {avg:.1f} over {len(values)} entries."
    )


def _summarize_logs(logs: List[WorkoutLog]) -> str:
    if not logs:
        return "No workout logs available."

    sorted_logs = sorted(logs, key=lambda l: l.created_at or datetime.min, reverse=True)
    recent = sorted_logs[:settings.MAX_LOGS]

    parts = []
    for log in recent:
        parts.append(f"- {log.exercise_name} for {log.duration_minutes} minutes")

    return "Recent workouts:\n" + "\n".join(parts)

def _is_fitness_question(question: str) -> bool:

    fitness_keywords = [
        "workout",
        "exercise",
        "fitness",
        "weight",
        "muscle",
        "strength",
        "training",
        "cardio",
        "nutrition",
        "diet",
        "recovery",
        "fat loss",
        "weight loss",
        "muscle gain",
        "gym",
        "bench",
        "squat",
        "deadlift",
        "chest",
        "back",
        "legs",
        "shoulders",
        "arms",
        "protein",
        "calories"
    ]

    question = question.lower()

    return any(
        keyword in question
        for keyword in fitness_keywords
    )



def run_workout_rag(
    question: str,
    weights: List[Weight],
    logs: List[WorkoutLog]
) -> Tuple[str, str]:
    if not _is_fitness_question(question):
        return (
            "I'm FitTrack AI and I'm designed to answer questions about fitness, workouts, nutrition, weight management, recovery, and exercise. Please ask a fitness-related question.",
            "Question filtered as non-fitness related."
        )

    # 1. Clean question
    clean_question = _sanitize_question(question)

    # 2. Select relevant logs
    top_logs = _select_top_logs(clean_question, logs)

    # 3. Build summaries
    weight_summary = _summarize_weights(weights)
    log_summary = _summarize_logs(logs)
    relevant_log_summary = (
        _summarize_logs(top_logs) if top_logs else "No highly relevant workouts found."
    )

    # 4. Retrieve chunks from ChromaDB
    retrieved_chunks = retriever.retrieve(
        clean_question,
        top_k=settings.MAX_CONTEXT_CHUNKS
    )

    # 4b. Rank chunks using semantic similarity scoring
    ranked_chunks = scorer.rank_chunks(clean_question, retrieved_chunks)

    # 4c. Select top N most relevant chunks
    top_chunks = ranked_chunks[:settings.MAX_CONTEXT_CHUNKS]

    # 5. Build the full RAG prompt
    prompt = build_prompt(
        question=clean_question,
        weight_summary=weight_summary,
        log_summary=log_summary,
        relevant_logs=relevant_log_summary,
        retrieved_chunks=top_chunks
    )

    # 6. Send prompt to Ollama
    ollama_response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    logger.info(ollama_response.text)

    model_output = ollama_response.json().get("response", "")

    # 7. Return model output + reasoning (prompt)
    return (
        model_output,
        f"Generated using {len(weights)} weight entries and {len(logs)} workout logs."
    )
