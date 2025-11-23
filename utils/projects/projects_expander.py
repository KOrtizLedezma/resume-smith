import json
from pathlib import Path
import sys


def load_projects(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_selected_ids(path: Path):
    text = path.read_text(encoding="utf-8")
    ids = [line.strip() for line in text.splitlines() if line.strip()]

    seen = set()
    result = []
    for pid in ids:
        if pid not in seen:
            seen.add(pid)
            result.append(pid)
    return result


def expand_selected_projects(projects_file: Path, selected_ids_file: Path, output_file: Path):
    projects = load_projects(projects_file)
    selected_ids = load_selected_ids(selected_ids_file)

    projects_by_id = {p["id"]: p for p in projects}

    expanded = []

    for pid in selected_ids:
        project = projects_by_id.get(pid)
        if not project:
            continue

        project_copy = {k: v for k, v in project.items() if k != "brief"}
        expanded.append(project_copy)

    output_file.write_text(json.dumps(expanded, indent=2), encoding="utf-8")


if __name__ == "__main__":
    projects_path = Path("data/json/projects.json")
    selected_ids_path = Path("data/output/selected_project_ids.txt")
    output_path = Path("data/output/expanded_projects.json")

    expand_selected_projects(projects_path, selected_ids_path, output_path)
