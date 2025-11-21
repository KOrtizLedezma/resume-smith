import sys
import re
from pathlib import Path


def fix_latex_chars(text):
    text = text.replace('C#', r'C\#')
    text = text.replace('%', r'\%')
    
    text = re.sub(r'(^|[\s\(])"', r'\1``', text, flags=re.MULTILINE)
    text = text.replace('"', "''")
    
    text = re.sub(r"(^|[\s\(])'", r'\1`', text, flags=re.MULTILINE)
    text = re.sub(r"(\w)'", r"\1'", text)
    
    return text


if __name__ == "__main__":

    tex_file = Path(sys.argv[1])

    if not tex_file.exists():
        sys.exit(1)

    with open(tex_file, 'r', encoding='utf-8') as f:
        text = f.read()

    fixed_text = fix_latex_chars(text)

    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(fixed_text)