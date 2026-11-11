import os
import re
import subprocess
import tempfile
from pathlib import Path

def run_pytest_in_docker(source_code: str, test_code: str) -> dict:
    """Run generated tests in a disposable, network-isolated Docker container."""
    timeout = int(os.getenv("SANDBOX_TIMEOUT", "10"))
    image = os.getenv("SANDBOX_IMAGE", "code-review-sandbox:latest")
    try:
        with tempfile.TemporaryDirectory(prefix="crds_") as tmp:
            root = Path(tmp)
            (root / "submission.py").write_text(source_code, encoding="utf-8")
            (root / "test_submission.py").write_text(test_code, encoding="utf-8")
            cmd = [
                "docker", "run", "--rm", "--network", "none",
                "--memory", "256m", "--cpus", "1", "--pids-limit", "64",
                "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
                "-v", f"{root}:/work:ro", "-w", "/work",
                image, "python", "-m", "pytest", "-q"
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            output = (proc.stdout + "\n" + proc.stderr).strip()
            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)
            return {
                "passed": int(passed_match.group(1)) if passed_match else 0,
                "failed": int(failed_match.group(1)) if failed_match else (1 if proc.returncode else 0),
                "output": output[-6000:],
                "warning": None if proc.returncode == 0 else "Tests failed or sandbox returned a non-zero status."
            }
    except FileNotFoundError:
        return {"passed": 0, "failed": 0, "output": "", "warning": "Docker was not found. Install and start Docker Desktop."}
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 1, "output": "", "warning": "Sandbox execution timed out."}
    except Exception as exc:
        return {"passed": 0, "failed": 0, "output": "", "warning": f"Sandbox error: {exc}"}
