import json
import re
import sys
from pathlib import Path


def fix_json_string(content):
    # Remove any text after the first complete JSON structure
    bracket_count = 0
    brace_count = 0
    in_string = False
    escape_next = False
    end_pos = 0
    
    for i, char in enumerate(content):
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if not in_string:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            
            if bracket_count == 0 and brace_count == 0 and (char == ']' or char == '}'):
                end_pos = i + 1
                break
    
    if end_pos > 0:
        content = content[:end_pos]
    
    content = re.sub(r'\[\s*"([^"]+)"\s*,\s*(\[.+\])\s*\]', r'{"\\1": \\2}', content, flags=re.DOTALL)
    
    # Fix escaped quotes that should be regular objects
    content = re.sub(r'"\{\\\"', '{\"', content)
    content = re.sub(r'\\\"\}"', '"}', content)
    content = re.sub(r'\\\":', '":"', content)
    content = re.sub(r':\s*\\\"', '":"', content)
    content = re.sub(r'\\\",', '",', content)
    
    # Remove comments
    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Replace single quotes with double quotes
    content = content.replace("'", '"')
    
    # Fix trailing commas
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Add quotes to unquoted keys
    content = re.sub(r'(\{|\,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', content)
    
    # Fix missing commas
    content = re.sub(r'"\s*\n\s*"', '",\n"', content)
    content = re.sub(r'}\s*\n\s*{', '},\n{', content)
    content = re.sub(r']\s*\n\s*\[', '],\n[', content)
    
    return content


def fix_json_file(input_file):
    input_path = Path(input_file)
    
    if not input_path.exists():
        sys.exit(1)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        sys.exit(1)
    
    # Try to parse as-is first
    try:
        data = json.loads(content)
        fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        # Apply fixes
        fixed_content = fix_json_string(content)
        
        # Try to parse fixed content
        try:
            data = json.loads(fixed_content)
            fixed_content = json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            sys.exit(1)
    
    # Write fixed content
    try:
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    
    fix_json_file(sys.argv[1])