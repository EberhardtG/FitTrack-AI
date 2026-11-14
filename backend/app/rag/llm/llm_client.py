import requests
from app.rag.config.rag_settings import RAGSettings

settings = RAGSettings()

def llm_answer(user_query: str, context: str | None = None) -> str:
    """
    Generates an answer using the configured LLM (Ollama or other).
    If context is provided, it performs RAG-style answer synthesis.
    """

    # Build the prompt
    if context:
        prompt = f"""
You are a helpful fitness assistant. Use the provided context to answer the user's question.

RULES:
- Use ONLY the information found in the context.
- If the context does not contain the answer, say:
  "I don't have enough information from the knowledge base to answer that."
- Do NOT invent new facts.
- Do NOT provide medical, legal, or safety-critical advice.
- Do NOT contradict the context.
- If the context is partially relevant, use only the relevant parts.
- If the user asks for something outside the context, answer using general reasoning
  but clearly state that the knowledge base did not contain relevant information.

STRUCTURE:
- Provide a clear, direct answer.
- Keep the tone supportive and practical.
- If helpful, include short bullet points.
- If multiple chunks support the answer, synthesize them.

CONTEXT:
{context}

USER QUESTION:
{user_query}

ANSWER:
"""

    else:
        # General LLM task (no RAG retrieval)
        prompt = f"""
You are a helpful fitness assistant. Answer the user's request clearly and directly.

User request:
{user_query}

Answer:
"""

    # Call Ollama
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        return "The model could not generate a response."

    data = response.json()
    return data.get("response", "").strip()
