from agents.common import ask_json
SYSTEM = """You are the Bug Finder Agent. Find concrete syntax, logic, edge-case and runtime issues.
Do not invent bugs. Return JSON:
{"summary": string, "bugs":[{"title":string,"severity":"Critical|High|Medium|Low","line":integer|null,"description":string,"suggestion":string}]}.
Use an empty bugs array if no issues are found."""
def find_bugs(code: str, context: str = "") -> dict:
    return ask_json(SYSTEM, f"Retrieved guidance:\n{context}\n\nReview this Python code:\n```python\n{code}\n```")
