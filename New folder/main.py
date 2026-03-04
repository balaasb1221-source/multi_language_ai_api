from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import os
import sys

app = FastAPI(title="Multi-Language AI Code API")

class CodeRequest(BaseModel):
    language: str
    code: str
    input_data: str = ""

@app.get("/")
def home():
    return {"message": "Multi-Language AI Code API is running!"}

@app.post("/run")
def run_code(request: CodeRequest):
    lang = request.language.lower()
    code = request.code
    input_data = request.input_data

    try:
        # HTML / CSS: just return the code
        if lang in ["html", "css"]:
            return {"output": code}

        with tempfile.TemporaryDirectory() as tmpdir:

            # ================= PYTHON =================
            if lang == "python":
                file_path = os.path.join(tmpdir, "program.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    [sys.executable, file_path],
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )

            # ================= JAVASCRIPT =================
            elif lang == "javascript":
                file_path = os.path.join(tmpdir, "program.js")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    ["node", file_path],
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )

            # ================= PHP =================
            elif lang == "php":
                file_path = os.path.join(tmpdir, "program.php")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    ["php", file_path],
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )

            # ================= COMPILED LANGUAGES =================
            elif lang in ["c", "c++", "java", "kotlin", "c#", "rust"]:

                # Use proper file names and compilation commands
                ext_map = {
                    "c": ("program.c", ["gcc", "program.c", "-o", "program"]),
                    "c++": ("program.cpp", ["g++", "program.cpp", "-o", "program"]),
                    "java": ("Program.java", ["javac", "Program.java"]),
                    "kotlin": ("Program.kt", ["kotlinc", "Program.kt", "-include-runtime", "-d", "Program.jar"]),
                    "c#": ("Program.cs", ["mcs", "Program.cs"]),
                    "rust": ("program.rs", ["rustc", "program.rs", "-o", "program"]),
                }

                file_name, compile_cmd = ext_map[lang]
                file_path = os.path.join(tmpdir, file_name)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)

                # Compile
                compile_process = subprocess.run(
                    compile_cmd,
                    cwd=tmpdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=15
                )

                if compile_process.returncode != 0:
                    return {"output": compile_process.stderr.decode()}

                # Execute compiled code
                if lang == "java":
                    exec_cmd = ["java", "-cp", tmpdir, "Program"]
                elif lang == "kotlin":
                    exec_cmd = ["java", "-jar", os.path.join(tmpdir, "Program.jar")]
                elif lang == "c#":
                    exec_cmd = ["mono", os.path.join(tmpdir, "Program.exe")]
                else:
                    exec_cmd = [os.path.join(tmpdir, "program")]

                result = subprocess.run(
                    exec_cmd,
                    cwd=tmpdir,
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )

            # ================= GO =================
            elif lang == "go":
                file_path = os.path.join(tmpdir, "program.go")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    ["go", "run", "program.go"],
                    cwd=tmpdir,
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )

            # ================= R =================
            elif lang == "r":
                file_path = os.path.join(tmpdir, "program.R")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                result = subprocess.run(
                    ["Rscript", "program.R"],
                    cwd=tmpdir,
                    input=input_data.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )

            else:
                raise HTTPException(status_code=400, detail="Language not supported")

        # Decode stdout and stderr
        output = result.stdout.decode() + result.stderr.decode()
        return {"output": output}

    except subprocess.TimeoutExpired:
        return {"output": "Execution timed out (10 seconds limit)"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}