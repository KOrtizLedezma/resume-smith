import json
from pathlib import Path


def build_projects_block(projects: list[dict]) -> str:
    lines = []
    for p in projects:
        pid = p.get("id", "").strip()
        name = p.get("name", "").strip()
        brief = p.get("brief", "").strip()
        tech_list = p.get("tech", []) or p.get("tags", [])

        tech_str = ", ".join(tech_list) if tech_list else ""
        line = f"{pid}: {name}"
        if brief:
            line += f" – {brief}"
        if tech_str:
            line += f" ({tech_str})"

        lines.append(line)

    return "\n".join(lines)


def build_prompt(job_description: str, projects: list[dict]) -> str:
    projects_block = build_projects_block(projects)

    system_prompt = (
        "You are a Talent Acquisition Specialist for the company in the job description.\n\n"
        "Your task:\n"
        "1) Read the project list.\n"
        "2) Read the job description.\n"
        "3) Choose EXACTLY 4 projects that best match the role and company needs.\n"
        "4) Select projects based on relevance of technologies, problem domain, and impact.\n\n"
        "STRICT OUTPUT RULES (VERY IMPORTANT):\n"
        "- Output ONLY the 4 selected project IDs.\n"
        "- ONE ID per line.\n"
        "- NO explanations.\n"
        "- NO bullet points.\n"
        "- NO JSON.\n"
        "- NO extra text before or after.\n"
        "Example output (if these were the best projects):\n"
        "docker-manager\n"
        "imdb\n"
        "task-manager\n"
        "huntboard\n"
    )

    user_prompt = (
        "PROJECT LIST (IDs, names, and summaries):\n"
        + projects_block
        + "\n\nJOB DESCRIPTION:\n"
        + job_description
        + "\n\nReturn ONLY the 4 most relevant project IDs as described above."
    )

    return system_prompt + "\n\n" + user_prompt


if __name__ == "__main__":
    projects_path = Path("data/json/projects.json")
    jd_path = Path("data/input/job_description.txt")
    prompt_output_path = Path("data/prompts/projects_prompt.txt")

    # Load projects
    projects = json.loads(projects_path.read_text(encoding="utf-8"))

    # Load job description
    job_description = jd_path.read_text(encoding="utf-8")

    # Build prompt
    prompt = build_prompt(job_description, projects)

    # Save prompt
    prompt_output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_path.write_text(prompt, encoding="utf-8")
