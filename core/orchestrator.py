from agents.bug_finder import find_bugs
from agents.style_agent import review_style
from agents.fixer_agent import fix_code
from agents.test_writer import write_tests
from rag.retriever import retrieve_guidance
from tools.code_analyzer import analyze_python
from tools.test_runner import run_pytest_in_docker
from agents.common import ask_json

def review_code(code: str, mode: str = "Full Code Review", language: str = "Python") -> dict:
    if language != "Python":
        raise ValueError("This version currently supports Python only.")
    static = analyze_python(code)
    context = retrieve_guidance(code)
    bugs = {"summary": "Not requested.", "bugs": []}
    style = {"summary": "Not requested.", "style": [], "score": 85}

    if mode in ("Full Code Review", "Debug Code", "Explain Code", "Generate Test Cases"):
        bugs = find_bugs(code, context)
    if mode in ("Full Code Review", "Review Code Style"):
        style = review_style(code, context)

    if mode == "Explain Code":
        explanation = ask_json(
            "Explain this Python code for a student. Return JSON: {\"explanation\": string}.",
            f"Code:\n```python\n{code}\n```\nGuidance:\n{context}"
        )
        fixed = {"fixed_code": code, "explanation": explanation.get("explanation", "")}
    elif mode == "Review Code Style":
        fixed = {"fixed_code": code, "explanation": "Style-only mode: no automatic rewrite was applied."}
    else:
        fixed = fix_code(code, bugs, style, context)

    test_data = write_tests(code, fixed.get("fixed_code", code))
    test_result = run_pytest_in_docker(fixed.get("fixed_code", code), test_data.get("tests", ""))

    severity_penalty = sum({"Critical":30,"High":18,"Medium":9,"Low":3}.get(x.get("severity"),5) for x in bugs.get("bugs", []))
    test_component = 100 if test_result.get("failed", 0) == 0 and not test_result.get("warning") else 50
    score = max(0, min(100, round(style.get("score",85)*0.4 + (100-min(severity_penalty,100))*0.4 + test_component*0.2)))
    return {
        "intent": mode, "static_analysis": static,
        "bug_summary": bugs.get("summary",""), "bugs": bugs.get("bugs",[]),
        "style_summary": style.get("summary",""), "style": style.get("style",[]),
        "fixed_code": fixed.get("fixed_code",code), "fix_explanation": fixed.get("explanation",""),
        "test_summary": test_data.get("summary",""), "generated_tests": test_data.get("tests",""),
        "tests": test_result, "quality_score": score
    }
