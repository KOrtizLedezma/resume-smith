import json
from pathlib import Path


def fill_cover_letter_fields(template_path, company_file, body_file, output_path):
    """Load template JSON, inject company and body content, and persist."""
    data = json.loads(Path(template_path).read_text(encoding="utf-8"))

    company_raw = Path(company_file).read_text(encoding="utf-8").strip()
    data["company"] = company_raw

    body_raw = Path(body_file).read_text(encoding="utf-8").strip()
    data["body"] = body_raw

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    fill_cover_letter_fields(
        template_path="data/json/cover_letter.json",
        company_file="data/output/company_name.txt",
        body_file="data/output/cover_letter_body.txt",
        output_path="data/output/cover_letter_filled.json"
    )
