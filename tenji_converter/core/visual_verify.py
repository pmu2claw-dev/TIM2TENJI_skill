from __future__ import annotations

from pathlib import Path
import shutil
import subprocess


def verify_visual_integrity(excel_path: Path, output_dir: Path) -> tuple[bool, str]:
    soffice = shutil.which("soffice")
    if not soffice:
        return False, "LibreOffice (soffice) not found; skip PDF visual verification"

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        soffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(excel_path),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, f"visual verify failed: {proc.stderr.strip() or proc.stdout.strip()}"

    pdf_path = output_dir / f"{excel_path.stem}.pdf"
    if not pdf_path.exists():
        return False, "PDF not generated"

    if pdf_path.stat().st_size <= 10 * 1024:
        return False, f"PDF too small ({pdf_path.stat().st_size} bytes), possible rendering issue"

    return True, f"PDF generated: {pdf_path} ({pdf_path.stat().st_size} bytes)"
