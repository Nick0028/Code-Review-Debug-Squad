from agents.common import ask_json
SYSTEM = """You are the Fixer Agent. Correct the Python code while preserving intended behavior.
Fix justified problems only. Return JSON: {"fixed_code":string,"explanation":string}.
fixed_code must contain complete Python source without markdown fences."""
def fix_code(code: str, bug_report: dict, style_report: dict, context: str = "") -> dict:
    return ask_json(SYSTEM, f"Guidance:\n{context}\nOriginal:\n```python\n{code}\n```\nBug findings:\n{bug_report}\nStyle findings:\n{style_report}")
