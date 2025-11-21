from pathlib import Path
import sys


def cleanup_file(file_path: str):
    """Delete file if it exists."""
    target = Path(file_path)
    if target.exists():
        target.unlink()
    else:
        print(f"File {target} not found.")


if __name__ == "__main__":
    file_path = sys.argv[1]
    cleanup_file(file_path)
