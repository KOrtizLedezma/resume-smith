import subprocess

print("Creation of LaTeX resume started...\n")

# Populates latex template with user data
subprocess.run(["python3","utils/latex/latex_resume_filler.py"])
print("LaTeX resume created successfully.\n")

# Validate Latex format
subprocess.run(["python3","utils/latex/latex_validator.py","data/outputs/resume.tex"])
print("LaTeX resume validated successfully.\n")

# Create folder for PDF output with the name of the comany and the date
subprocess.run(["python3","utils/create_output_path.py"])
with open("data/outputs/output_path.txt", "r") as f:
    output_path = f.read().strip()
print(f"Output path created at: {output_path}\n")

# Convert LaTeX to PDF
subprocess.run(["python3","utils/latex/tex_to_pdf.py","data/outputs/resume.tex",output_path])
print("PDF resume generated successfully.\n")

# Populates latex template with user data
subprocess.run(["python3","utils/latex/latex_cover_letter_filler.py"])
print("LaTeX cover letter created successfully.\n")

# Validate Latex format
subprocess.run(["python3","utils/latex/latex_validator.py","data/outputs/cover_letter.tex"])
print("LaTeX cover letter validated successfully.\n")

# Convert LaTeX to PDF
subprocess.run(["python3","utils/latex/tex_to_pdf.py","data/outputs/cover_letter.tex",output_path])
print("PDF cover letter generated successfully.\n")

# Remove unnecessary files
files_to_remove = [
    "data/outputs/company_name.txt",
    "data/outputs/resume_updated.json",
    "data/outputs/resume.tex",
    "data/outputs/job_title.txt",
    "data/outputs/cover_letter_filled.json",
    "data/outputs/cover_letter.tex",
    "data/outputs/output_path.txt"
]

for fp in files_to_remove:
    subprocess.run(["python3", "utils/cleanup_file.py", fp])
print("Unnecessary files removed successfully.\n")

print("Resume and cover letter generation completed.\n")
