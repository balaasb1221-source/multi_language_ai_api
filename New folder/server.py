from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI(title="Multi-Language Code Runner API")

# Model for input
class CodeRequest(BaseModel):
    language: str  # 'python', 'c', 'cpp', 'java', 'kotlin'
    code: str

# Directory for temporary files
TEMP_DIR = "/app/code_runner"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/run")
def run_code(req: CodeRequest):
    code_file = os.path.join(TEMP_DIR, f"{uuid.uuid4()}")
    output = ""
    try:
        if req.language.lower() == "python":
            code_file += ".py"
            with open(code_file, "w") as f:
                f.write(req.code)
            result = subprocess.run(
                ["python3", code_file], capture_output=True, text=True, timeout=10
            )
            output = result.stdout + result.stderr

        elif req.language.lower() in ["c", "cpp"]:
            ext = ".c" if req.language.lower() == "c" else ".cpp"
            code_file += ext
            exe_file = code_file + ".out"
            with open(code_file, "w") as f:
                f.write(req.code)
            compiler = "gcc" if req.language.lower() == "c" else "g++"
            compile_result = subprocess.run(
                [compiler, code_file, "-o", exe_file],
                capture_output=True, text=True, timeout=10
            )
            if compile_result.returncode != 0:
                return {"output": compile_result.stderr}
            run_result = subprocess.run([exe_file], capture_output=True, text=True, timeout=10)
            output = run_result.stdout + run_result.stderr

        elif req.language.lower() == "java":
            code_file += ".java"
            classname = "Main"
            with open(code_file, "w") as f:
                f.write(req.code)
            compile_result = subprocess.run(
                ["javac", code_file], capture_output=True, text=True, timeout=10
            )
            if compile_result.returncode != 0:
                return {"output": compile_result.stderr}
            run_result = subprocess.run(["java", classname], capture_output=True, text=True, timeout=10)
            output = run_result.stdout + run_result.stderr

        elif req.language.lower() == "kotlin":
            code_file += ".kt"
            exe_file = code_file + ".jar"
            with open(code_file, "w") as f:
                f.write(req.code)
            compile_result = subprocess.run(
                ["kotlinc", code_file, "-include-runtime", "-d", exe_file],
                capture_output=True, text=True, timeout=10
            )
            if compile_result.returncode != 0:
                return {"output": compile_result.stderr}
            run_result = subprocess.run(["java", "-jar", exe_file], capture_output=True, text=True, timeout=10)
            output = run_result.stdout + run_result.stderr

        else:
            return {"output": f"Language {req.language} not supported."}

    except subprocess.TimeoutExpired:
        output = "Execution timed out."

    finally:
        # Clean up temporary files
        try:
            os.remove(code_file)
            if req.language.lower() in ["c", "cpp"]:
                os.remove(exe_file)
            elif req.language.lower() == "java":
                os.remove("Main.class")
            elif req.language.lower() == "kotlin":
                os.remove(exe_file)
        except:
            pass

    return {"output": output}