# utils/tech_stack/tech_stack_prompt_generator.py

import json
from pathlib import Path


CATEGORIES = [
    "Languages",
    "Frameworks",
    "Databases & Libraries",
    "Development Tools",
]


def format_existing_skills(tech_stack: dict) -> str:
    by_cat = {cat: [] for cat in CATEGORIES}

    for group in tech_stack.get("skills", []):
        name = group.get("name")
        items = group.get("items", [])
        if name in by_cat:
            by_cat[name].extend(items)

    # Dedupe while preserving order
    lines = []
    for cat in CATEGORIES:
        seen = set()
        deduped = []
        for item in by_cat[cat]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        if deduped:
            lines.append(f"{cat}: {', '.join(deduped)}")
        else:
            lines.append(f"{cat}:")
    return "\n".join(lines)


def build_prompt(job_description: str, tech_stack: dict) -> str:
    existing_skills_text = format_existing_skills(tech_stack)

    system_prompt = (
        "You are a senior technical recruiter and resume optimization expert.\n\n"
        "Your task:\n"
        "1) Read the EXISTING TECH STACK (the candidate's current skills).\n"
        "2) Read the JOB DESCRIPTION.\n"
        "3) Propose ONLY NEW skills that are clearly relevant to the job.\n"
        "   - NEW means: they MUST NOT already appear in the existing tech stack list.\n"
        "4) Organize ONLY these NEW skills into EXACTLY these categories:\n"
        "   - Languages\n"
        "   - Frameworks\n"
        "   - Databases & Libraries\n"
        "   - Development Tools\n\n"
        "STRICT OUTPUT RULES (VERY IMPORTANT):\n"
        "- Output MUST be plain text.\n"
        "- DO NOT use JSON.\n"
        "- DO NOT use markdown.\n"
        "- DO NOT explain your reasoning.\n"
        "- DO NOT add commentary or notes like '(nice to have)'.\n"
        "- DO NOT use parentheses in any skill name.\n"
        "- DO NOT add extra categories.\n"
        "- DO NOT add blank lines before or after.\n"
        "- If a category has no new skills, still output the category name followed by a colon with nothing after it.\n"
        "- Output MUST follow EXACTLY this format (categories in this order):\n"
        "  Languages: item1, item2\n"
        "  Frameworks: item1, item2\n"
        "  Databases & Libraries: item1, item2\n"
        "  Development Tools: item1, item2\n"
    )

    user_prompt = (
        "EXISTING TECH STACK (DO NOT REPEAT THESE ITEMS):\n"
        + existing_skills_text
        + "\n\nJOB DESCRIPTION:\n"
        + job_description
    )

    return system_prompt + "\n\n" + user_prompt


if __name__ == "__main__":
    tech_stack_path = Path("data/json/tech_stack.json")
    jd_path = Path("data/input/job_description.txt")
    prompt_output_path = Path("data/prompts/tech_stack_prompt.txt")

    tech_data = json.loads(tech_stack_path.read_text(encoding="utf-8"))
    job_description = jd_path.read_text(encoding="utf-8")

    prompt = build_prompt(job_description, tech_data)

    prompt_output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_output_path.write_text(prompt, encoding="utf-8")
