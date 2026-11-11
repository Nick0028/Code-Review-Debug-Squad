from agents.common import ask_json
SYSTEM = """You are the Style/Lint Agent. Review readability, naming, maintainability and Python conventions.
Avoid duplicating bug findings. Return JSON:
{"summary":string,"style":[{"rule":string,"message":string,"line":integer|null,"suggestion":string}],"score":integer}.
Score must be between 0 and 100."""
def review_style(code: str, context: str = "") -> dict:
    return ask_json(SYSTEM, f"Guidance:\n{context}\n\nReview this Python code:\n```python\n{code}\n```")
