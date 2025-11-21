import subprocess
import sys

# --------------------Projects Processing--------------------

# Run the project prompt generator script
subprocess.run(["python3", "utils/projects/projects_prompt_generator.py"])
print("Projects prompt generation completed.\n")

# Run the AI Model to review the projects
project_prompt_path = "data/prompts/projects_prompt.txt"

with open("data/outputs/selected_project_ids.txt", "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", project_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT
    )
print("Projects review completed.\n")

# Expand the selected projects to include full details
subprocess.run(["python3", 
                "utils/projects/projects_expander.py",
                "data/json/projects.json",
                "data/outputs/selected_project_ids.txt",
                "data/outputs/expanded_projects.json"])
print("Projects expansion completed.\n")

# Build the prompt for rewriting the project bullet points
subprocess.run(["python3", "utils/projects/rewrite_prompt_generator.py"])
print("Projects rewrite prompt generation completed.\n")

# Run the AI Model to rewrite the project bullet points
rewrite_project_prompt_path = "data/prompts/rewrite_projects_prompt.txt"

with open("data/outputs/expanded_projects.json", "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", rewrite_project_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT
    )
print("Projects rewriting completed.\n")

# Check if JSON is valid
subprocess.run(["python3", "utils/json_validator.py", "data/outputs/expanded_projects.json"])
print("Rewritten Projects JSON validation completed.\n")

# Merge the cleaned tech stack into the resume JSON
subprocess.run(["python3", 
                "utils/projects/merge_projects_into_resume.py", 
                "data/outputs/resume_update_part_1.json", 
                "data/outputs/expanded_projects.json", 
                "data/outputs/resume_updated.json"])
print("Projects merged into resume JSON successfully.\n")

# Remove unnecessary files
files_to_remove = [
    "data/prompts/projects_prompt.txt",
    "data/prompts/rewrite_projects_prompt.txt",
    "data/outputs/selected_project_ids.txt",
    "data/outputs/expanded_projects.json",
    "data/outputs/resume_update_part_1.json",
]

for fp in files_to_remove:
    subprocess.run(["python3", "utils/cleanup_file.py", fp])
print("Projects processing completed.\n")
