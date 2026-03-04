import subprocess

# Test GCC
try:
    result = subprocess.run(["gcc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
except Exception as e:
    print("GCC Error:", e)

# Test G++
try:
    result = subprocess.run(["g++", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
except Exception as e:
    print("G++ Error:", e)