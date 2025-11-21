import json
import re
import sys
from pathlib import Path


CATEGORIES_JSON_TO_RESUME = {
    "Languages": "languages",
    "Frameworks": "Frameworks",
    "Databases & Libraries": "Databases & Libraries",
    "Development Tools": "Development Tools",
}

def remove_parenthesis_comments(item: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", item).strip()


def clean_item(raw: str) -> str:
    s = remove_parenthesis_comments(raw).strip()
    if not s:
        return ""

    lower = s.lower()

    commentary_markers = [
        "none",
        "no new",
        "already listed",
        "already included",
        "no additional",
        "n/a",
    ]
    if any(marker in lower for marker in commentary_markers):
        return ""

    return s    

def parse_tech_stack_text(text: str) -> dict:
    result = {
        "languages": [],
        "Frameworks": [],
        "Databases & Libraries": [],
        "Development Tools": [],
    }

    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue

        key, values = line.split(":", 1)
        key_norm = key.strip().lower()

        # split commas, clean each item, drop empties
        raw_items = [v.strip() for v in values.split(",") if v.strip()]
        items = []
        for v in raw_items:
            cleaned = clean_item(v)
            if cleaned:
                items.append(cleaned)

        # dedupe while preserving order
        deduped = []
        seen = set()
        for item in items:
            if item not in seen:
                seen.add(item)
                deduped.append(item)

        if key_norm.startswith("language"):
            result["languages"] = deduped
        elif key_norm.startswith("framework"):
            result["Frameworks"] = deduped
        elif "database" in key_norm or "librar" in key_norm:
            result["Databases & Libraries"] = deduped
        elif "tool" in key_norm:
            result["Development Tools"] = deduped

    return result

def load_base_tech_stack(tech_stack_path: Path) -> dict:
    data = json.loads(tech_stack_path.read_text(encoding="utf-8"))

    base = {
        "languages": [],
        "Frameworks": [],
        "Databases & Libraries": [],
        "Development Tools": [],
    }

    for group in data.get("skills", []):
        name = group.get("name")
        items = group.get("items", [])
        resume_key = CATEGORIES_JSON_TO_RESUME.get(name)
        if resume_key:
            base[resume_key].extend(items)

    # Dedupe while preserving order
    for key in base:
        seen = set()
        deduped = []
        for item in base[key]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        base[key] = deduped

    return base

def merge_tech_stack_into_resume(
    resume_path: Path,
    extras_txt_path: Path,
    tech_stack_json_path: Path,
    output_path: Path,
):
    # Load resume
    resume = json.loads(resume_path.read_text(encoding="utf-8"))

    # Load base tech stack from JSON
    base = load_base_tech_stack(tech_stack_json_path)

    # Load extra skills from model output
    extras_text = extras_txt_path.read_text(encoding="utf-8")
    extras = parse_tech_stack_text(extras_text)

    # Combine base + extras per category
    combined = {}
    for key in base.keys():
        seen = set()
        merged_list = []
        for item in base[key] + extras.get(key, []):
            if item and item not in seen:
                seen.add(item)
                merged_list.append(item)
        combined[key] = merged_list

    # Ensure technical_skills exists
    if "technical_skills" not in resume:
        resume["technical_skills"] = {}

    tech_section = resume["technical_skills"]
    tech_section["languages"] = combined["languages"]
    tech_section["Frameworks"] = combined["Frameworks"]
    tech_section["Databases & Libraries"] = combined["Databases & Libraries"]
    tech_section["Development Tools"] = combined["Development Tools"]

    output_path.write_text(json.dumps(resume, indent=2), encoding="utf-8")

if __name__ == "__main__":

    resume_file = Path(sys.argv[1])
    extras_file = Path(sys.argv[2]) 
    tech_stack_file = Path(sys.argv[3])
    output_file = Path(sys.argv[4])

    merge_tech_stack_into_resume(resume_file, extras_file, tech_stack_file, output_file)
