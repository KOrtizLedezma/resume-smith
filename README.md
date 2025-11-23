# Resume-Smith

Generate a tailored resume and cover letter from your existing data plus a target job description. The pipeline builds prompts, calls a local LLM via Ollama, merges responses into LaTeX templates, and outputs PDFs.

![Project Flow](docs/project_flow.png)

## Requirements

- Python 3.10+
- `ollama` CLI with `mistral7b-custom` (or adjust model name in `scripts/`)
- TeX engine (`pdflatex`/`xelatex`/`lualatex`) for PDF generation

## Project Structure

- `scripts/`: end-to-end pipeline entrypoints (`main.py` orchestrates everything)
- `utils/`: helpers for prompts, merging JSON, LaTeX, cleanup, LLM client, etc.
- `data/json/`: base resume, projects, tech stack, cover letter fields
- `data/input/job_description.txt`: paste the target job description here
- `data/templates/`: LaTeX templates for resume and cover letter
- `data/output/`: generated intermediates and final PDFs (per company/role/date)
- `docs/project_flow.png`: flow diagram of the process

## Quick Start

1. Update your base data in `data/json/` (`resume.json`, `projects.json`, `tech_stack.json`, `cover_letter.json`).
2. Run the pipeline:
   ```bash
   python3 scripts/main.py
   ```
3. Collect outputs from `data/output/<Company>/<Role_Date>/` (`resume.pdf`, `cover_letter.pdf`).

## Pipeline (overview)

- `scripts/main.py` runs, in order:
  - `job_description.py`: builds prompts and extracts company + title via `utils/llm_client.py`.
  - `tech_stack.py`: selects relevant stack and merges into resume JSON.
  - `projects.py`: selects projects, expands, rewrites bullets via LLM, validates, and merges.
  - `cover_letter.py`: builds cover letter body via LLM and fills cover letter JSON.
  - `generate_resume_and_cover_letter.py`: fills LaTeX, validates, makes dated output folder, converts to PDFs, cleans intermediates.

## Customization Tips

- Change the model name in `scripts/*` if using a different Ollama model.
- Edit LaTeX templates in `data/templates/` for styling.
- Adjust output folder format or filenames in `utils/create_output_path.py` and `scripts/generate_resume_and_cover_letter.py`.

## Troubleshooting

- Missing LaTeX fonts or packages: install a full TeX distribution (e.g., TeX Live).
- LLM call errors: ensure `ollama` is running and `mistral7b-custom` is available locally.
- If PDFs are not created, check logs in `data/output/*.log` for TeX errors.
