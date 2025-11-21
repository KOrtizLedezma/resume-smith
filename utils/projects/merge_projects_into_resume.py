import json
import sys
from pathlib import Path

def merge_projects_into_resume(resume_file, projects_file, output_file):
    resume_file = Path(resume_file)
    projects_file = Path(projects_file)
    output_file = Path(output_file)

    resume = json.loads(resume_file.read_text(encoding="utf-8"))
    selected_projects = json.loads(projects_file.read_text(encoding="utf-8"))

    resume["projects"] = selected_projects

    output_file.write_text(json.dumps(resume, indent=2), encoding="utf-8")


if __name__ == "__main__":
    RESUME_PATH = Path(sys.argv[1])
    PROJECTS_PATH = Path(sys.argv[2])
    OUTPUT_PATH = Path(sys.argv[3])
    merge_projects_into_resume(RESUME_PATH, PROJECTS_PATH, OUTPUT_PATH)
