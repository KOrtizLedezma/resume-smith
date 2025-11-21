import subprocess
from pathlib import Path

# Build the cover letter prompt
subprocess.run(["python3", "utils/cover_letter/cover_letter_prompt.py"])
print("Cover letter prompt generation completed.\n")

# Run the AI Model to generate the cover letter body
cover_letter_prompt_path = "data/prompts/cover_letter_body_prompt.txt"
with open("data/outputs/cover_letter_body.txt", "w") as out_file:
    subprocess.run(
        ["python3", "utils/llm_client.py", cover_letter_prompt_path, "mistral7b-custom"],
        stdout=out_file,
        stderr=subprocess.STDOUT
    )
print("Cover letter body generation completed.\n")

# Fill the cover letter JSON with the generated body
subprocess.run(["python3", "utils/cover_letter/fill_cover_letter_fields.py"])
print("Cover letter JSON filling completed.\n")

# Remove unnecessary files
files_to_remove = [
    "data/prompts/cover_letter_body_prompt.txt",
    "data/outputs/cover_letter_body.txt"
]

for file_path in files_to_remove:
    subprocess.run(["python3", "utils/cleanup_file.py", file_path])
print("Unnecessary files removed successfully.\n")

print("Cover Letter processing completed.\n")
