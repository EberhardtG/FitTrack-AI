from datetime import datetime

def format_timestamp(ts: float):
    """Convert a timestamp into a readable format."""
    return datetime.fromtimestamp(ts).strftime("%b %d, %Y • %I:%M %p")

def trim(text: str):
    """Remove extra whitespace from model output."""
    return text.strip() if text else ""
