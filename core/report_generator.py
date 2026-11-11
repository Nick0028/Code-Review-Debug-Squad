import json
def build_markdown_report(original_code: str, result: dict) -> str:
    lines = ["# Code Review & Debug Squad Report", "",
        f"**Mode:** {result.get('intent')}",
        f"**Quality score:** {result.get('quality_score')}/100", "",
        "## Original code", "```python", original_code, "```", "",
        "## Bug analysis", result.get("bug_summary","")]
    for bug in result.get("bugs", []):
        lines.append(f"- **{bug.get('severity')} — {bug.get('title')}**: {bug.get('description')}")
    lines += ["", "## Style review", result.get("style_summary","")]
    for item in result.get("style", []):
        lines.append(f"- **{item.get('rule')}**: {item.get('message')}")
    lines += ["", "## Corrected code", "```python", result.get("fixed_code",""), "```",
        "", "## Fix explanation", result.get("fix_explanation",""),
        "", "## Generated tests", "```python", result.get("generated_tests",""), "```",
        "", "## Test execution", "```text", result.get("tests",{}).get("output",""), "```",
        "", "## Static analysis", "```json", json.dumps(result.get("static_analysis",{}), indent=2), "```"]
    return "\n".join(lines)
