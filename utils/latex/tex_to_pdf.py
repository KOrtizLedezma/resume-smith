import subprocess
import sys
from pathlib import Path


def check_latex_installation():
    # Check which LaTeX compilers are available
    compilers = ['pdflatex', 'xelatex', 'lualatex']
    available = []
    
    for compiler in compilers:
        try:
            result = subprocess.run(
                [compiler, '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                available.append(compiler)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    
    return available


def convert_tex_to_pdf(tex_file, output_dir=None, cleanup=True, compiler=None):
    tex_path = Path(tex_file)

    # Basic checks
    if not tex_path.exists():
        print(f"Error: TeX file not found: {tex_path}")
        return None
    if tex_path.suffix.lower() != ".tex":
        print(f"Error: Not a .tex file: {tex_path}")
        return None

    # Set output directory
    if output_dir is None:
        output_dir = tex_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which compiler to use
    if compiler is None:
        available = check_latex_installation()
        if not available:
            print("Error: No LaTeX compiler found. Install texlive (or similar).")
            return None
        compiler = available[0]  # pick the first available
        # print(f"Using LaTeX compiler: {compiler}")

    # Run LaTeX twice for references, TOC, etc.
    for run in range(2):
        try:
            result = subprocess.run(
                [
                    compiler,
                    "-interaction=nonstopmode",
                    f"-output-directory={output_dir}",
                    str(tex_path),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            if result.returncode != 0:
                print(f"LaTeX error on run {run + 1}:")
                print(result.stdout)
                return None

        except FileNotFoundError:
            print(f"Error: LaTeX compiler '{compiler}' not found in PATH.")
            return None
        except subprocess.TimeoutExpired:
            print("Error: LaTeX compilation timeout (60s).")
            return None

    pdf_file = output_dir / tex_path.with_suffix(".pdf").name

    if pdf_file.exists():
        if cleanup:
            aux_extensions = [".aux", ".log", ".out", ".toc", ".lof", ".lot"]
            for ext in aux_extensions:
                aux_file = output_dir / tex_path.with_suffix(ext).name
                if aux_file.exists():
                    aux_file.unlink()
        return pdf_file
    else:
        print("Error: PDF not created.")
        return None


if __name__ == "__main__":
    tex_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = convert_tex_to_pdf(tex_file, output_dir)
    if result is None:
        sys.exit(1)
    else:
        sys.exit(0)
