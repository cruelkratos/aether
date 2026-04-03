import subprocess
import tempfile
import uuid
import os
from typing import Dict

async def run_python(code: str) -> Dict[str, str]:
    # sandbox to local temporary file; in production use proper container sandboxing.
    tmp_dir = tempfile.gettempdir()
    script_file = os.path.join(tmp_dir, f"aether_python_{uuid.uuid4().hex}.py")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        proc = subprocess.run(["python", script_file], capture_output=True, text=True, timeout=30)
        return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
    except subprocess.TimeoutExpired as e:
        return {"stdout": "", "stderr": "TimeoutExpired", "returncode": -1}
    finally:
        try:
            os.remove(script_file)
        except Exception:
            pass
