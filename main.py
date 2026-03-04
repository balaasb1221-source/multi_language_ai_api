from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid
import tempfile

app = FastAPI(title="Multi-Language Code Runner API")

class CodeRequest(BaseModel):
    language: str
    code: str
    input: str = ""  # optional user input

@app.post("/run")
def run_code(request: CodeRequest):
    language = request.language.lower()
    code = request.code
    user_input = request.input

    # Use system temp directory for safety
    temp_dir = tempfile.gettempdir()
    unique_id = str(uuid.uuid4())

    try:
        if language == "python":
            file_path = os.path.join(temp_dir, f"{unique_id}.py")
            with open(file_path, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["python3", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )
            os.remove(file_path)

        elif language == "c":
            file_path = os.path.join(temp_dir, f"{unique_id}.c")
            exe_path = os.path.join(temp_dir, unique_id)
            with open(file_path, "w") as f:
                f.write(code)
            compile_proc = subprocess.run(["gcc", file_path, "-o", exe_path], capture_output=True, text=True)
            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": f"C COMPILATION ERROR:\n{compile_proc.stderr}"}
            result = subprocess.run([exe_path], capture_output=True, text=True, input=user_input, timeout=5)
            os.remove(file_path)
            os.remove(exe_path)

        elif language == "cpp":
            file_path = os.path.join(temp_dir, f"{unique_id}.cpp")
            exe_path = os.path.join(temp_dir, unique_id)
            with open(file_path, "w") as f:
                f.write(code)
            compile_proc = subprocess.run(["g++", file_path, "-o", exe_path], capture_output=True, text=True)
            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": f"C++ COMPILATION ERROR:\n{compile_proc.stderr}"}
            result = subprocess.run([exe_path], capture_output=True, text=True, input=user_input, timeout=5)
            os.remove(file_path)
            os.remove(exe_path)

        elif language == "java":
            classname = "Main"
            file_path = os.path.join(temp_dir, f"{classname}.java")
            with open(file_path, "w") as f:
                f.write(code)
            compile_proc = subprocess.run(["javac", file_path], capture_output=True, text=True)
            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": f"JAVA COMPILATION ERROR:\n{compile_proc.stderr}"}
            result = subprocess.run(["java", "-cp", temp_dir, classname], capture_output=True, text=True, input=user_input, timeout=5)
            os.remove(file_path)
            os.remove(os.path.join(temp_dir, f"{classname}.class"))

        elif language == "php":
            # PHP execution
            file_path = os.path.join(temp_dir, f"{unique_id}.php")
            with open(file_path, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["php", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )
            os.remove(file_path)

        else:
            return {"error": "Language not supported"}

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out!"}
    except Exception as e:
        return {"error": str(e)}