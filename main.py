from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid
import tempfile
import shutil

app = FastAPI(title="Multi-Language Code Runner API")


class CodeRequest(BaseModel):
    language: str
    code: str
    input: str = ""


@app.post("/run")
def run_code(request: CodeRequest):

    language = request.language.lower()
    code = request.code
    user_input = request.input

    temp_dir = tempfile.mkdtemp()

    try:

        result = None

        # ================= PYTHON =================
        if language == "python":

            file_path = os.path.join(temp_dir, "script.py")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["python3", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= C =================
        elif language == "c":

            file_path = os.path.join(temp_dir, "program.c")
            exe_path = os.path.join(temp_dir, "program")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["gcc", file_path, "-o", exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= C++ =================
        elif language == "cpp":

            file_path = os.path.join(temp_dir, "program.cpp")
            exe_path = os.path.join(temp_dir, "program")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["g++", file_path, "-o", exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= JAVA =================
        elif language == "java":

            classname = "Main"
            file_path = os.path.join(temp_dir, "Main.java")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["javac", file_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                ["java", "-cp", temp_dir, classname],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= PHP =================
        elif language == "php":

            file_path = os.path.join(temp_dir, "script.php")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["php", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= C# =================
        elif language == "csharp":

            file_path = os.path.join(temp_dir, "program.cs")
            exe_path = os.path.join(temp_dir, "program.exe")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["mcs", file_path, "-out:" + exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                ["mono", exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= R =================
        elif language == "r":

            file_path = os.path.join(temp_dir, "script.R")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["Rscript", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= KOTLIN =================
        elif language == "kotlin":

            file_path = os.path.join(temp_dir, "Program.kt")
            jar_path = os.path.join(temp_dir, "program.jar")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["kotlinc", file_path, "-include-runtime", "-d", jar_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                ["java", "-jar", jar_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= GO =================
        elif language == "go":

            file_path = os.path.join(temp_dir, "program.go")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["go", "run", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= RUST =================
        elif language == "rust":

            file_path = os.path.join(temp_dir, "program.rs")
            exe_path = os.path.join(temp_dir, "program")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["rustc", file_path, "-o", exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # ================= SWIFT =================
        elif language == "swift":

            file_path = os.path.join(temp_dir, "program.swift")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["swift", file_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        else:
            return {"error": "Language not supported"}

        return {
            "output": result.stdout if result else "",
            "error": result.stderr if result else ""
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)