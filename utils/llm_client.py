import sys
import subprocess
from pathlib import Path

def run_model(prompt_path, model):
    with open(prompt_path, "r", encoding="utf-8") as f:
        result = subprocess.run(
            ["ollama", "run", model],
            stdin=f,
            capture_output=True,
            text=True,
        )
    print(result.stdout)

if __name__ == "__main__":
    prompt_path = sys.argv[1]
    model = sys.argv[2]
    run_model(prompt_path, model)
