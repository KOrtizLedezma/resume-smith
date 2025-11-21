import json
from pathlib import Path


def build_prompt(job_description: str, project_file_contents: str) -> str:
    system_prompt = (
        "You are an expert Technical Resume Writer specializing in ATS-optimized bullet points.\n\n"
        "Your task:\n"
        "1) Read the JOB DESCRIPTION.\n"
        "2) Read the PROJECT FILE (JSON array of projects).\n"
        "3) Rewrite ONLY the bullet point texts (the 'text' fields inside 'bullets').\n\n"
        "Rewrite rules:\n"
        "- Keep every project, in the same order.\n"
        "- Do NOT add or remove projects.\n"
        "- Do NOT add or remove bullets.\n"
        "- Do NOT change any fields except 'text' inside each bullet.\n"
        "- Do NOT change 'name', 'technologies', 'id', or any other fields.\n"
        "- Make bullets:\n"
        "  * More impactful and concise.\n"
        "  * Quantitative where possible (%, time saved, users, latency, throughput, etc.).\n"
        "  * Aligned with the job description (skills, responsibilities, tech stack).\n"
        "  * Optimized for ATS by including relevant technical keywords naturally.\n"
        "  * Truthful to the original meaning.\n"
        "  * Professional resume tone.\n\n"
        "OUTPUT RULES (VERY IMPORTANT):\n"
        "- Output MUST be valid JSON.\n"
        "- Preserve the exact overall structure: a JSON array of project objects.\n"
        "- Do NOT wrap the JSON in markdown code fences.\n"
        "- Do NOT include ```json or ``` anywhere.\n"
        "- Do NOT add explanations, comments, or extra text.\n"
        "- The first character of your reply MUST be '['.\n"
    )

    user_prompt = (
        "JOB DESCRIPTION:\n"
        + job_description
        + "\n\nPROJECT FILE (JSON):\n"
        + project_file_contents
        + "\n\nRewrite ONLY the bullet 'text' fields according to the rules above and return the full JSON."
    )

    return system_prompt + "\n\n" + user_prompt


if __name__ == "__main__":
    projects_path = Path("data/outputs/expanded_projects.json")
    jd_path = Path("data/input/job_description.txt")
    prompt_output_path = Path("data/prompts/rewrite_projects_prompt.txt")

    projects_text = projects_path.read_text(encoding="utf-8")
    jd = jd_path.read_text(encoding="utf-8")

    prompt = build_prompt(jd, projects_text)

    prompt_output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_path.write_text(prompt, encoding="utf-8")