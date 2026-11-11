from agents.common import ask_json
SYSTEM = """You are the Test-Writer Agent. Generate pytest tests for the provided Python source.
Cover normal inputs, edge cases and invalid inputs. Do not use external services.
Return JSON: {"summary":string,"tests":string}. tests must be complete pytest source without fences.
Import the submitted module as `submission`."""
def write_tests(code: str, fixed_code: str) -> dict:
    return ask_json(SYSTEM, f"Original source:\n```python\n{code}\n```\nCorrected source:\n```python\n{fixed_code}\n```")
