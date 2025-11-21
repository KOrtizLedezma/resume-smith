def get_job_description():
    print("Type the position description here, include the Company information if available.")
    print("When you're done, type a single line with END and press Enter.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


job_description = get_job_description()
with open("data/input/job_description.txt", "w") as file:
    file.write(job_description)
