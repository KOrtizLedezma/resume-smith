import json
from pathlib import Path

def build_prompt(job_description: str) -> str:

    system_prompt = (
        "What is the name of the company described in the job description?\n"
        "Provide ONLY the company name as a single line of text.\n"
    )

    return system_prompt + "\n\n" + job_description


if __name__ == "__main__":
    jd_path = Path("data/input/job_description.txt")
    prompt_output_path = Path("data/prompts/company_name_prompt.txt")

    # Load job description
    job_description = jd_path.read_text(encoding="utf-8")

    # Build prompt
    prompt = build_prompt(job_description)

    # Save prompt
    prompt_output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_path.write_text(prompt, encoding="utf-8")
