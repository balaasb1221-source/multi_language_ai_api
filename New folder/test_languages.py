import requests

# FastAPI URL
API_URL = "http://127.0.0.1:8000/run"

# Sample code for each language
sample_codes = {
    "html": "<h1>Hello HTML</h1>",
    "css": "body { background-color: lightblue; }",
    "javascript": "console.log('Hello JavaScript');",
    "python": "for i in range(3): print('Python', i)",
    "java": "public class Program { public static void main(String[] args){ System.out.println(\"Hello Java\"); } }",
    "php": "<?php echo 'Hello PHP'; ?>",
    "c": "#include <stdio.h>\nint main() { printf(\"Hello C\\n\"); return 0; }",
    "c++": "#include <iostream>\nint main() { std::cout << \"Hello C++\" << std::endl; return 0; }",
    "c#": "using System; class Program { static void Main() { Console.WriteLine(\"Hello C#\"); } }",
    "r": "cat('Hello R\\n')",
    "go": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello Go\") }",
    "kotlin": "fun main() { println(\"Hello Kotlin\") }",
    "swift": "print(\"Hello Swift\")",
    "rust": "fn main() { println!(\"Hello Rust\"); }"
}

# Function to test all languages
def test_all_languages():
    for lang, code in sample_codes.items():
        payload = {
            "language": lang,
            "code": code
        }
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                output = response.json().get("output", "")
            else:
                output = f"Error: Status code {response.status_code}"
        except Exception as e:
            output = f"Exception: {str(e)}"

        print(f"\n--- {lang.upper()} ---")
        print(output)

if __name__ == "__main__":
    test_all_languages()