import subprocess
import sys

# --------------------Job Description Processing--------------------

# Run the job description generator script
subprocess.run(["python3", "utils/job_description/job_description_generator.py"])
print("Job Description generation completed.\n")

# Run the job information prompt creation script
subprocess.run(["python3", "utils/job_description/company_name_prompt.py"])
print("Company name prompt creation completed.\n")

# Run the AI Model to extract company name
company_name_prompt_path = "data/prompts/company_name_prompt.txt"

with open("data/outputs/company_name.txt", "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", company_name_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT
    )
print("Company name extraction completed.\n")

# Run the job information prompt creation script
subprocess.run(["python3", "utils/job_description/job_title_prompt.py"])
print("Job title prompt creation completed.\n")

# Run the AI Model to extract job title
job_title_prompt_path = "data/prompts/job_title_prompt.txt"
with open("data/outputs/job_title.txt", "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", job_title_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT
    )
print("Job title extraction completed.\n")

# Remove unnecessary files
files_to_remove = [
    "data/prompts/company_name_prompt.txt",
    "data/prompts/job_title_prompt.txt"
]
for file_path in files_to_remove:
    subprocess.run(["python3", "utils/cleanup_file.py", file_path])
print("Unnecessary files removed successfully.\n")

print("Job Description processing completed.\n")
