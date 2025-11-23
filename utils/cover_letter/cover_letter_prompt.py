from pathlib import Path

def build_cover_body_prompt(resume_json_str: str, job_description: str) -> str:
    system_prompt = (
        "You are an expert technical cover letter writer.\n\n"
        "Your task:\n"
        "1) Read RESUME_JSON.\n"
        "2) Read JOB DESCRIPTION.\n"
        "3) Write ONLY the body of a cover letter (NO greeting, NO signature).\n"
        "4) The body must:\n"
        "   - Be EXACTLY 3 to 5 paragraphs.\n"
        "   - Contain ONLY the body text (no headers, no titles, no subject lines).\n"
        "   - Start directly with the opening sentence.\n"
        "   - Mention the role and company naturally in paragraph 1.\n"
        "   - Use achievements from the resume.\n"
        "   - Align with the job description.\n"
        "   - End with a strong closing paragraph WITHOUT any sign-off words.\n\n"
        "STRICT FORMAT RULES:\n"
        "- Output MUST be plain text.\n"
        "- NO markdown.\n"
        "- NO LaTeX syntax.\n"
        "- NO headings (e.g., no 'Application for…', no 'Software Engineer Application…').\n"
        "- NO greeting (no 'Dear…').\n"
        "- NO closing or signature (no 'Sincerely', no name).\n"
        "- NO bullet points.\n"
        "- NO more than 5 paragraphs.\n"
        "- Paragraphs must be separated by exactly ONE blank line.\n"
        "- Output ONLY the paragraphs. Nothing before or after.\n"
    )

    user_prompt = (
        "RESUME_JSON:\n"
        + resume_json_str
        + "\n\nJOB DESCRIPTION:\n"
        + job_description
        + "\n\nWrite ONLY the cover letter body, following ALL rules above."
    )

    return system_prompt + "\n\n" + user_prompt

if __name__ == "__main__":
    with open("data/prompts/cover_letter_body_prompt.txt", "w") as out_file:
        prompt = build_cover_body_prompt(
            resume_json_str=Path("data/output/resume_updated.json").read_text(),
            job_description=Path("data/input/job_description.txt").read_text()
        )
        out_file.write(prompt)
