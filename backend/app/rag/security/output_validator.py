import re

def validate_output(answer: str, route: str, context: str | None = None):
    """
    Validates the LLM's output before returning it to the user.

    Returns:
        {
            "is_valid": bool,
            "reason": str,
            "answer": str
        }
    """

    # -------------------------
    #  Empty or meaningless output
    # -------------------------
    if not answer or not answer.strip():
        return {
            "is_valid": False,
            "reason": "Empty or missing model output.",
            "answer": "I wasn’t able to generate a response."
        }

    normalized = answer.strip()

    # -------------------------
    #  Safety scan
    # -------------------------
    unsafe_patterns = [
        r"kill yourself",
        r"suicide",
        r"make a bomb",
        r"harm someone",
        r"illegal activity",
        r"hack into",
        r"weapon instructions",
        r"medical diagnosis",
        r"prescription medication",
    ]

    for pattern in unsafe_patterns:
        if re.search(pattern, normalized.lower()):
            return {
                "is_valid": False,
                "reason": "Unsafe content detected.",
                "answer": (
                    "I can’t provide information on that topic. "
                    "Try asking something else."
                )
            }

    # -------------------------
    #  RAG-specific validation
    # -------------------------
    if route == "rag" and context:
        # If the answer says "I don't know", that's fine.
        # But if it confidently states facts not in context, flag it.
        context_lower = context.lower()
        answer_lower = normalized.lower()

        # Simple hallucination heuristic:
        # If answer contains nouns not present in context, flag it.
        # (This is a lightweight check, not perfect.)
        important_words = [
            w for w in answer_lower.split()
            if len(w) > 6  # long words are more likely to be factual nouns
        ]

        hallucinations = [
            w for w in important_words
            if w not in context_lower
        ]

        if len(hallucinations) > 8:  # threshold to avoid false positives
            return {
                "is_valid": False,
                "reason": "Possible hallucination detected.",
                "answer": (
                    "I may not have enough reliable information to answer that. "
                    "Try asking your question in a different way."
                )
            }

    # -------------------------
    #  Relevance check
    # -------------------------
    irrelevant_patterns = [
        r"here is a poem",
        r"once upon a time",
        r"let me tell you a joke",
        r"as an ai language model",
    ]

    for pattern in irrelevant_patterns:
        if pattern in normalized.lower():
            return {
                "is_valid": False,
                "reason": "Irrelevant or off-topic response.",
                "answer": (
                    "I wasn’t able to generate a relevant answer. "
                    "Try rephrasing your question."
                )
            }

    # -------------------------
    #  Formatting check
    # -------------------------
    if normalized.count("```") % 2 != 0:
        return {
            "is_valid": False,
            "reason": "Broken formatting detected.",
            "answer": (
                "I wasn’t able to format the answer correctly. "
                "Try asking again."
            )
        }

    # -------------------------
    #  Passed all checks
    # -------------------------
    return {
        "is_valid": True,
        "reason": "Output is valid.",
        "answer": normalized
    }
