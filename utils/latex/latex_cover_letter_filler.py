import json
from pathlib import Path


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_template(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def save_text(path: str | Path, content: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def replace(template: str, key: str, value: str) -> str:
    # looks for @@KEY@@ and replaces with `value`
    return template.replace(f"@@{key}@@", value)


def escape_for_latex(text: str) -> str:
    """Basic LaTeX escaping for body text."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def generate_cover_letter_single_tex(
    template_path: str | Path,
    json_path: str | Path,
    output_path: str | Path = "data/output/cover_letter.tex",
):
    data = load_json(json_path)
    tex = load_template(template_path)

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    location = data.get("location", "")
    linkedin = data.get("linkedin", "")
    company = data.get("company", "")
    body_raw = data.get("body", "")

    # Only escape the body (header fields are usually URL-safe already)
    body = escape_for_latex(body_raw)

    tex = replace(tex, "NAME", name)
    tex = replace(tex, "EMAIL", email)
    tex = replace(tex, "PHONE", phone)
    tex = replace(tex, "LOCATION", location)
    tex = replace(tex, "LINKEDIN", linkedin)
    tex = replace(tex, "COMPANY", company)
    tex = replace(tex, "BODY", body)

    output_path = Path(output_path)
    save_text(output_path, tex)
    return output_path

if __name__ == "__main__":
    generate_cover_letter_single_tex(
        template_path="data/templates/cover_letter_template.tex",
        json_path="data/output/cover_letter_filled.json",
        output_path="data/output/cover_letter.tex",
    )
