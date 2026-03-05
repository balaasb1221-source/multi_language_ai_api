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
    input: str = ""

@app.post("/run")
def run_code(request: CodeRequest):

    language = request.language.lower()
    code = request.code
    user_input = request.input

    temp_dir = tempfile.gettempdir()
    unique_id = str(uuid.uuid4())

    try:

        # PYTHON
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

        # C
        elif language == "c":
            file_path = os.path.join(temp_dir, f"{unique_id}.c")
            exe_path = os.path.join(temp_dir, unique_id)

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["gcc", file_path, "-o", exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

            os.remove(file_path)
            os.remove(exe_path)

        # C++
        elif language == "cpp":
            file_path = os.path.join(temp_dir, f"{unique_id}.cpp")
            exe_path = os.path.join(temp_dir, unique_id)

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["g++", file_path, "-o", exe_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

            os.remove(file_path)
            os.remove(exe_path)

        # JAVA
        elif language == "java":
            classname = "Main"
            file_path = os.path.join(temp_dir, f"{classname}.java")

            with open(file_path, "w") as f:
                f.write(code)

            compile_proc = subprocess.run(
                ["javac", file_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                os.remove(file_path)
                return {"error": compile_proc.stderr}

            result = subprocess.run(
                ["java", "-cp", temp_dir, classname],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

            os.remove(file_path)
            os.remove(os.path.join(temp_dir, f"{classname}.class"))

        # PHP
        elif language == "php":
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

        # C#
        elif language == "csharp":

            project_path = os.path.join(temp_dir, unique_id)
            os.makedirs(project_path, exist_ok=True)

            program_file = os.path.join(project_path, "Program.cs")

            with open(program_file, "w") as f:
                f.write(code)

            subprocess.run(
                ["dotnet", "new", "console", "-o", project_path, "--force"],
                capture_output=True,
                text=True
            )

            build_proc = subprocess.run(
                ["dotnet", "build", project_path],
                capture_output=True,
                text=True
            )

            if build_proc.returncode != 0:
                return {"error": build_proc.stderr}

            result = subprocess.run(
                ["dotnet", "run", "--project", project_path],
                capture_output=True,
                text=True,
                input=user_input,
                timeout=5
            )

        # R LANGUAGE
        elif language == "r":

            file_path = os.path.join(temp_dir, f"{unique_id}.R")

            with open(file_path, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["Rscript", file_path],
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)