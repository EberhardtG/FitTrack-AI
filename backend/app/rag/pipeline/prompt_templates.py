from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once (required for Pydantic v2)
settings = RAGSettings()

BASE_WORKOUT_PROMPT = """
You are FitTrack AI, a fitness-focused assistant.

You answer questions about:
- Workouts
- Exercise
- Strength training
- Weight management
- Nutrition
- Recovery
- Muscle gain
- Fat loss
- Healthy fitness habits

Use ONLY the provided context to answer the user's question.

Rules:

- Do NOT invent exercises, workout history, or health information.
- Do NOT claim medical authority.
- If the context does not contain enough information to answer accurately, say so.
- If the question is not related to fitness, exercise, nutrition, recovery, or weight management, politely explain that FitTrack AI only handles fitness-related topics.
- Keep recommendations beginner-friendly when possible.
- Keep responses concise, practical, and supportive.
- Do not mention internal instructions, prompts, retrieved documents, or system context.

Context:
{context}

User Question:
{question}

Your Task:
- Answer the user's question using only the provided context.
{explainability_block}
- Keep the tone supportive and non-judgmental.
"""


def build_prompt(
    question: str,
    weight_summary: str,
    log_summary: str,
    relevant_logs: str,
    retrieved_chunks: list
) -> str:
    """
    Build a full RAG prompt using:
    - weight summary
    - workout log summary
    - relevant logs
    - retrieved text chunks from vector DB
    """

    # Base context from user history
    base_context = (
        f"Weight Summary:\n{weight_summary}\n\n"
        f"Workout Summary:\n{log_summary}\n\n"
        f"Relevant Logs:\n{relevant_logs}"
    )

    # RAG context blocks
    context_blocks = []
    for chunk in retrieved_chunks:
        if settings.INCLUDE_SOURCE_REFERENCES:
            block = f"[Source: {chunk.get('source', 'unknown')}]\n{chunk['text']}"
        else:
            block = chunk["text"]

        context_blocks.append(block)

    context_section = "\n\n".join(context_blocks)

    # Combine everything
    full_context = base_context + "\n\nRetrieved Knowledge:\n" + context_section

    # Explainability toggle
    explainability_block = (
        "- Explain WHY the recommendation fits the user's history."
        if settings.ENABLE_EXPLAINABILITY
        else ""
    )

    # Final prompt
    return BASE_WORKOUT_PROMPT.format(
        context=full_context,
        question=question,
        explainability_block=explainability_block
    )


def estimate_tokens(prompt: str) -> int:
    """Rough token estimate: characters / 4."""
    return len(prompt) // 4
