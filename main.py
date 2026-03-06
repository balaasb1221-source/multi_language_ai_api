from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import os
import hashlib

app = FastAPI(title="Multi-Language Async Code Runner API")

# Persistent folder for code execution
BASE_TEMP_DIR = "/tmp/code_runner"
os.makedirs(BASE_TEMP_DIR, exist_ok=True)

class CodeRequest(BaseModel):
    language: str
    code: str
    input: str = ""

async def run_subprocess(cmd, input_text="", timeout=15):
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=input_text.encode()),
            timeout=timeout
        )
        return stdout.decode(), stderr.decode()
    except asyncio.TimeoutError:
        return "", "Execution timed out!"

def hash_code(code: str) -> str:
    """Generate a hash for the code to use as filename for caching compiled binaries"""
    return hashlib.sha256(code.encode()).hexdigest()

@app.post("/run")
async def run_code(request: CodeRequest):
    language = request.language.lower()
    code = request.code
    user_input = request.input
    code_hash = hash_code(code)
    temp_dir = os.path.join(BASE_TEMP_DIR, code_hash)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # ------------------- Python -------------------
        if language == "python":
            file_path = os.path.join(temp_dir, "script.py")
            with open(file_path, "w") as f:
                f.write(code)
            stdout, stderr = await run_subprocess(["python3", file_path], user_input)

        # ------------------- C -------------------
        elif language == "c":
            file_path = os.path.join(temp_dir, "program.c")
            exe_path = os.path.join(temp_dir, "program")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(exe_path):
                compile_stdout, compile_stderr = await run_subprocess(["gcc", file_path, "-o", exe_path], timeout=15)
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess([exe_path], user_input)

        # ------------------- C++ -------------------
        elif language == "cpp":
            file_path = os.path.join(temp_dir, "program.cpp")
            exe_path = os.path.join(temp_dir, "program")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(exe_path):
                compile_stdout, compile_stderr = await run_subprocess(["g++", file_path, "-o", exe_path], timeout=15)
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess([exe_path], user_input)

        # ------------------- Java -------------------
        elif language == "java":
            classname = "Main"
            file_path = os.path.join(temp_dir, f"{classname}.java")
            class_file = os.path.join(temp_dir, f"{classname}.class")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(class_file):
                compile_stdout, compile_stderr = await run_subprocess(["javac", file_path], timeout=15)
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess(["java", "-cp", temp_dir, classname], user_input)

        # ------------------- PHP -------------------
        elif language == "php":
            file_path = os.path.join(temp_dir, "script.php")
            with open(file_path, "w") as f:
                f.write(code)
            stdout, stderr = await run_subprocess(["php", file_path], user_input)

        # ------------------- Go -------------------
        elif language == "go":
            file_path = os.path.join(temp_dir, "program.go")
            with open(file_path, "w") as f:
                f.write(code)
            stdout, stderr = await run_subprocess(["go", "run", file_path], user_input, timeout=15)

        # ------------------- Rust -------------------
        elif language == "rust":
            file_path = os.path.join(temp_dir, "program.rs")
            exe_path = os.path.join(temp_dir, "program")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(exe_path):
                compile_stdout, compile_stderr = await run_subprocess(["rustc", file_path, "-o", exe_path], timeout=15)
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess([exe_path], user_input)

        # ------------------- Kotlin -------------------
        elif language == "kotlin":
            file_path = os.path.join(temp_dir, "Program.kt")
            jar_path = os.path.join(temp_dir, "program.jar")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(jar_path):
                compile_stdout, compile_stderr = await run_subprocess(
                    ["kotlinc", file_path, "-include-runtime", "-d", jar_path], timeout=15
                )
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess(["java", "-jar", jar_path], user_input)

        # ------------------- Swift -------------------
        elif language == "swift":
            file_path = os.path.join(temp_dir, "program.swift")
            with open(file_path, "w") as f:
                f.write(code)
            stdout, stderr = await run_subprocess(["swift", file_path], user_input, timeout=15)

        # ------------------- R -------------------
        elif language == "r":
            file_path = os.path.join(temp_dir, "script.R")
            with open(file_path, "w") as f:
                f.write(code)
            stdout, stderr = await run_subprocess(["Rscript", file_path], user_input)

        # ------------------- C# -------------------
        elif language == "csharp":
            file_path = os.path.join(temp_dir, "program.cs")
            exe_path = os.path.join(temp_dir, "program.exe")
            with open(file_path, "w") as f:
                f.write(code)
            if not os.path.exists(exe_path):
                compile_stdout, compile_stderr = await run_subprocess(["mcs", file_path, "-out:" + exe_path], timeout=15)
                if compile_stderr:
                    return {"error": compile_stderr}
            stdout, stderr = await run_subprocess(["mono", exe_path], user_input)

        else:
            return {"error": "Language not supported yet"}

        return {"output": stdout, "error": stderr}

    except Exception as e:
        return {"error": str(e)}