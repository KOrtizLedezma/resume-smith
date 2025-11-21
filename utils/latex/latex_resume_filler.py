import json
from pathlib import Path

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def load_template(path):
    return Path(path).read_text(encoding="utf-8")

def save_output(path, content):
    Path(path).write_text(content, encoding="utf-8")

def replace(template: str, placeholder: str, value: str):
    return template.replace(placeholder, value)


def generate_resume(tex_template_path, data_json_path, output_path):
    tex = load_template(tex_template_path)
    data = load_json(data_json_path)

    # ---------- HEADER ----------
    tex = replace(tex, "@@NAME@@", data["name"])
    tex = replace(tex, "@@PHONE@@", data["contact"]["phone"])
    tex = replace(tex, "@@EMAIL@@", data["contact"]["email"])

    links = {list(d.keys())[0]: list(d.values())[0] for d in data["links"]}
    tex = replace(tex, "@@GITHUB@@", links.get("Github", ""))
    tex = replace(tex, "@@LINKEDIN@@", links.get("LinkedIn", ""))
    tex = replace(tex, "@@PORTFOLIO@@", links.get("Portfolio", ""))

    # ---------- EDUCATION ----------
    edu = data["education"]
    if len(edu) >= 1:
        e = edu[0]
        tex = replace(tex, "@@EDU1_INSTITUTION@@", e.get("institution", ""))
        tex = replace(tex, "@@EDU1_LOCATION@@", e.get("location", ""))
        tex = replace(tex, "@@EDU1_DEGREE@@", e.get("degree", ""))
        tex = replace(tex, "@@EDU1_DATE@@", e.get("graduation_date", ""))

    if len(edu) >= 2:
        c = edu[1]
        tex = replace(tex, "@@EDU2_INSTITUTION@@", c.get("name", ""))
        tex = replace(tex, "@@EDU2_LOCATION@@", c.get("location", ""))
        tex = replace(tex, "@@EDU2_DEGREE@@", c.get("provider", ""))
        tex = replace(tex, "@@EDU2_DATE@@", c.get("date", ""))

    # ---------- PROJECTS ----------
    for i, project in enumerate(data["projects"], start=1):
        tex = replace(tex, f"@@PROJECT{i}_NAME@@", project["name"])
        tex = replace(tex, f"@@PROJECT{i}_TECH@@", project.get("technologies", ""))

        # bullets
        for b_idx, bullet in enumerate(project["bullets"], start=1):
            tex = replace(tex, f"@@PROJECT{i}_BULLET{b_idx}@@", bullet["text"])

    # ---------- EXPERIENCE ----------
    exp = data["experience"][0]
    tex = replace(tex, "@@EXP_TITLE@@", exp["title"])
    tex = replace(tex, "@@EXP_EMPLOYER@@", exp["employer"])
    tex = replace(tex, "@@EXP_LOCATION@@", exp["location"])
    tex = replace(tex, "@@EXP_DATES@@", f'{exp["start_date"]} -- {exp["end_date"]}')

    for i, bullet in enumerate(exp["bullets"], start=1):
        tex = replace(tex, f"@@EXP_BULLET{i}@@", bullet)

    # ---------- SKILLS ----------
    skills = data["technical_skills"]
    tex = replace(tex, "@@SKILL_LANGUAGES@@", ", ".join(skills["languages"]))
    tex = replace(tex, "@@SKILL_FRAMEWORKS@@", ", ".join(skills["Frameworks"]))
    tex = replace(tex, "@@SKILL_DB_LIBS@@", ", ".join(skills["Databases & Libraries"]))
    tex = replace(tex, "@@SKILL_TOOLS@@", ", ".join(skills["Development Tools"]))

    save_output(output_path, tex)

if __name__ == "__main__":
    generate_resume(
        tex_template_path="data/templates/resume_template.tex",
        data_json_path="data/outputs/resume_updated.json",
        output_path="data/outputs/resume.tex"
    )
