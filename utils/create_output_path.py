from pathlib import Path
from datetime import datetime

def get_company_name():
    path = Path("data/output/company_name.txt")
    if not path.exists():
        raise FileNotFoundError("company_name.txt does not exist.")
    company_name = path.read_text().strip().replace(" ", "_")
    return company_name

def get_position_title():
    path = Path("data/output/job_title.txt")
    if not path.exists():
        raise FileNotFoundError("job_title.txt does not exist.")
    position_title = path.read_text().strip().replace(" ", "_")
    return position_title

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    base_dir = Path("data/output")
    base_dir.mkdir(parents=True, exist_ok=True)

    company = get_company_name()
    job_title = get_position_title()
    stamp = get_timestamp()
    file_name = f"{job_title}_{stamp}"
    output_path = Path(f"data/output/{company}/{file_name}")
    with open("data/output/output_path.txt", "w") as f:
        f.write(str(output_path))
    output_path.mkdir(parents=True, exist_ok=True)
