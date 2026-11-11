import ast, subprocess, sys, tempfile
from pathlib import Path
def analyze_python(code: str) -> dict:
    result = {"syntax_valid": True, "syntax_error": None, "ruff_output": ""}
    try:
        ast.parse(code)
    except SyntaxError as exc:
        result.update(syntax_valid=False, syntax_error={"line":exc.lineno,"message":exc.msg})
        return result
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"submission.py"
            path.write_text(code, encoding="utf-8")
            proc = subprocess.run([sys.executable,"-m","ruff","check",str(path)],capture_output=True,text=True,timeout=8)
            result["ruff_output"] = (proc.stdout+proc.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        result["ruff_output"] = f"Ruff unavailable or timed out: {exc}"
    return result
