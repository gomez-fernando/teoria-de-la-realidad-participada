#!/usr/bin/env python
"""
Convert all Markdown files in a tree to PDFs using pandoc.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


EXCLUDE_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__"}


def iter_markdown_files(root: Path) -> list[Path]:
    md_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith(".md"):
                md_files.append(Path(dirpath) / name)
    return md_files


def run_pandoc(
    pandoc: str, md_path: Path, pdf_path: Path, pdf_engine: str | None
) -> subprocess.CompletedProcess:
    cmd = [
        pandoc,
        "--from",
        "markdown",
        "--to",
        "pdf",
        "-o",
        str(pdf_path),
        str(md_path),
    ]
    if pdf_engine:
        cmd.extend(["--pdf-engine", pdf_engine])
    return subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert all Markdown files under a directory to PDFs using pandoc."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root folder to search (default: current directory).",
    )
    parser.add_argument(
        "--pandoc",
        default="pandoc",
        help="Pandoc executable name or full path (default: pandoc).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PDFs.",
    )
    parser.add_argument(
        "--pdf-engine",
        default=None,
        help="PDF engine to use (e.g., pdflatex, xelatex, lualatex, wkhtmltopdf).",
    )
    args = parser.parse_args()

    pandoc_path = shutil.which(args.pandoc)
    if not pandoc_path:
        print(
            "No se encontró 'pandoc' en PATH. Instálalo o indica la ruta con --pandoc.",
        )
        return 1

    root = Path(args.root).resolve()
    md_files = iter_markdown_files(root)
    if not md_files:
        print("No se encontraron archivos .md.")
        return 0

    converted = 0
    skipped = 0
    failed = 0

    for md_path in md_files:
        pdf_path = md_path.with_suffix(".pdf")
        if pdf_path.exists() and not args.overwrite:
            skipped += 1
            continue
        result = run_pandoc(pandoc_path, md_path, pdf_path, args.pdf_engine)
        if result.returncode == 0:
            converted += 1
        else:
            failed += 1
            print(f"Error convirtiendo: {md_path}")
            if result.stderr:
                print(result.stderr.strip())

    print(
        f"Listo. Convertidos: {converted}, omitidos: {skipped}, errores: {failed}."
    )
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
