# Step1: Install tectonic & Import deps
from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil
import re


def _sanitize_latex(latex_content: str) -> str:
    """Strip common LLM artifacts that silently break LaTeX compilation.

    1. Removes ```latex / ``` ... ``` markdown code fences, in case the
       model wrapped the .tex source in one.
    2. Removes a stray, standalone `\\` that the model places somewhere
       in the preamble (before \\begin{document}) -- most commonly
       glued directly onto `\\documentclass{...}` or sitting alone on
       the next line.

       `\\` ("end this line") only makes sense once LaTeX is already in
       horizontal/paragraph mode. In the preamble there is no current
       line to end, so TeX raises:
           LaTeX Error: There's no line here to end.
       which halts compilation -- this is why no PDF gets produced.
    """
    content = latex_content.strip()

    fence_match = re.match(r"^```(?:latex|tex)?\s*\n(.*)\n```$", content, re.DOTALL)
    if fence_match:
        content = fence_match.group(1).strip()

    if "\\begin{document}" in content:
        preamble, marker, rest = content.partition("\\begin{document}")
        preamble = "\n".join(
            line for line in preamble.split("\n") if line.strip() != "\\\\"
        )
        content = preamble + marker + rest

    content = re.sub(
        r"(\\documentclass(?:\[[^\]]*\])?\{[^}]*\})[ \t]*\\\\",
        r"\1",
        content,
        count=1,
    )

    return content


@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document
    """
    if shutil.which("tectonic") is None:
        raise RuntimeError(
            "tectonic is not installed. Install it first on your system."
        )

    latex_content = _sanitize_latex(latex_content)

    try:
        # Step2: Create directory
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)
        # Step3: Setup filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"
        # Step4: Export as tex & pdf
        tex_file = output_dir / tex_filename
        print("RAW START:")
        print(repr(latex_content[:200]))
        tex_file.write_text(latex_content, encoding="utf-8")

        result = subprocess.run(
                    ["tectonic", tex_filename, "--outdir", str(output_dir)],
                    cwd=output_dir,
                    capture_output=True,
                    text=True,
                )
        
        final_pdf = output_dir / pdf_filename
        
        if result.returncode == 0 and final_pdf.exists():
             return str(final_pdf)
        
        print("RETURN CODE:", result.returncode)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)

        final_pdf = output_dir / pdf_filename
        if not final_pdf.exists():
            # Surface tectonic's *actual* error instead of a generic
            # message, so it's visible in logs/UI and -- if this
            # exception is turned into a tool result for the agent --
            # Gemini has a chance to see why compilation failed and
            # correct the LaTeX on its next attempt.
            return(
                "LATEX_COMPILATION_FAILED\n\n"
                 + result.stderr[-3000:]
            )

        print(f"Successfully generated PDF at {final_pdf}")
        return str(final_pdf)

    except Exception as e:
        print(f"Error rendering LaTeX: {str(e)}")
        raise