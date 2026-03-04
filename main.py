from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI(title="Multi-Language Code Runner API")

class CodeRequest(BaseModel):
    language: str
    code: str

@app.post("/run")
def run_code(request: CodeRequest):
    language = request.language.lower()
    code = request.code

    filename = str(uuid.uuid4())

    try:
        if language == "python":
            file = f"{filename}.py"
            with open(file, "w") as f:
                f.write(code)
            result = subprocess.run(["python3", file], capture_output=True, text=True, timeout=5)

        elif language == "c":
            file = f"{filename}.c"
            exe = filename
            with open(file, "w") as f:
                f.write(code)
            subprocess.run(["gcc", file, "-o", exe], check=True)
            result = subprocess.run([f"./{exe}"], capture_output=True, text=True, timeout=5)

        elif language == "cpp":
            file = f"{filename}.cpp"
            exe = filename
            with open(file, "w") as f:
                f.write(code)
            subprocess.run(["g++", file, "-o", exe], check=True)
            result = subprocess.run([f"./{exe}"], capture_output=True, text=True, timeout=5)

        elif language == "java":
            classname = "Main"
            file = f"{classname}.java"
            with open(file, "w") as f:
                f.write(code)
            subprocess.run(["javac", file], check=True)
            result = subprocess.run(["java", classname], capture_output=True, text=True, timeout=5)

        else:
            return {"error": "Language not supported"}

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}