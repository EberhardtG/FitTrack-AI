import re

def validate_user_input(user_query: str):
    """
    Validates and classifies user input before sending it into the RAG pipeline.

    Returns:
        {
            "is_valid": bool,
            "reason": str,
            "normalized": str,
            "route": "rag" | "llm" | "reject" | "clarify"
        }
    """

    # -------------------------
    # 1. Empty / whitespace
    # -------------------------
    if not user_query or not user_query.strip():
        return {
            "is_valid": False,
            "reason": "Empty input is not allowed.",
            "normalized": "",
            "route": "reject"
        }

    # Normalize early
    normalized = user_query.strip()

    # -------------------------
    # 2. Too short
    # -------------------------
    if len(normalized) < 3:
        return {
            "is_valid": False,
            "reason": "Your question is too short to understand.",
            "normalized": normalized,
            "route": "clarify"
        }

    # -------------------------
    # 3. Too long
    # -------------------------
    if len(normalized) > 5000:
        return {
            "is_valid": False,
            "reason": "Your input is too long. Please shorten your question.",
            "normalized": normalized[:200] + "...",
            "route": "clarify"
        }

    # -------------------------
    # 4. Non-semantic noise
    # -------------------------
    noise_patterns = [
        r"^[!?.,]+$",          # only punctuation
        r"^\d+$",              # only numbers
        r"^[\W_]+$",           # symbols/emojis
        r"^[a-zA-Z]{1,2}$",    # single letters
        r"^(haha|lol)+$",      # chat noise
    ]

    for pattern in noise_patterns:
        if re.fullmatch(pattern, normalized.lower()):
            return {
                "is_valid": False,
                "reason": "Your input doesn't contain meaningful language.",
                "normalized": normalized,
                "route": "clarify"
            }

    # -------------------------
    # 5. Prompt-injection detection
    # -------------------------
    suspicious_patterns = [
        "ignore previous instructions",
        "forget all earlier messages",
        "you are now",
        "system prompt",
        "act as an admin",
        "override safety",
        "repeat the context verbatim",
        "show me the hidden text",
        "developer instructions",
        "bypass restrictions",
        "jailbreak",
    ]

    lowered = normalized.lower()
    for pattern in suspicious_patterns:
        if pattern in lowered:
            return {
                "is_valid": False,
                "reason": f"Suspicious pattern detected: '{pattern}'",
                "normalized": normalized,
                "route": "reject"
            }

    # -------------------------
    # 6. Safety / harmful content
    # -------------------------
    unsafe_keywords = [
        "kill myself",
        "suicide",
        "harm someone",
        "make a bomb",
        "illegal drugs",
        "commit a crime",
        "hack into",
        "steal",
        "weapon instructions",
    ]

    for keyword in unsafe_keywords:
        if keyword in lowered:
            return {
                "is_valid": False,
                "reason": "Your request involves unsafe or harmful content.",
                "normalized": normalized,
                "route": "reject"
            }

    # -------------------------
    # 7. Detect non-RAG tasks (LLM-only)
    # -------------------------
    llm_tasks = [
        "write a poem",
        "tell me a joke",
        "generate code",
        "draft an email",
        "create a story",
        "summarize this",
        "translate this",
    ]

    for task in llm_tasks:
        if task in lowered:
            return {
                "is_valid": True,
                "reason": "General LLM task detected.",
                "normalized": normalized,
                "route": "llm"
            }

    # -------------------------
    # 8. Default: RAG route
    # -------------------------
    return {
        "is_valid": True,
        "reason": "Input is safe and meaningful.",
        "normalized": normalized,
        "route": "rag"
    }
