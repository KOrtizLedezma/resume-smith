import subprocess
import sys

# --------------------Tech Stack Processing--------------------

# 1) Run the tech stack prompt generator script
subprocess.run(["python3", "utils/tech_stack/tech_stack_prompt_generator.py"], check=True)
print("Tech Stack prompt generation completed.\n")

# 2) Run the AI Model to review the tech stack
tech_stack_prompt_path = "data/prompts/tech_stack_prompt.txt"
selected_tech_stack_output = "data/outputs/selected_tech_stack.txt"

with open(selected_tech_stack_output, "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", tech_stack_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT,
        check=True,
    )

print("Tech Stack selection completed.\n")

# 3) Merge the selected tech stack into the resume JSON
subprocess.run(
    [
        "python3",
        "utils/tech_stack/merge_tech_stack_into_resume.py",
        "data/json/resume.json",
        "data/outputs/selected_tech_stack.txt",
        "data/json/tech_stack.json",
        "data/outputs/resume_update_part_1.json",
    ],
    check=True,
)

print("Tech Stack merged into resume.\n")

# 4) Remove unnecessary files
files_to_remove = [
    "data/prompts/tech_stack_prompt.txt",
    "data/outputs/selected_tech_stack.txt",
]

for fp in files_to_remove:
    subprocess.run(["python3", "utils/cleanup_file.py", fp], check=False)
print("Tech Stack processing completed.\n")
