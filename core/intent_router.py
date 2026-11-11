def detect_intent(request: str) -> str:
    text = (request or "").lower()
    if any(x in text for x in ["explain", "what does", "describe"]): return "explain"
    if any(x in text for x in ["test", "pytest", "unit test"]): return "testing"
    if any(x in text for x in ["style", "lint", "format", "readability"]): return "style"
    return "debug"
