#!/usr/bin/env python3
"""Extract text from a PDF file and save it as a .txt document."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read a PDF file and convert its text content into a text document."
    )
    parser.add_argument("input_pdf", type=Path, help="Path to the source PDF file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output text file path (default: same name as input with .txt extension)",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding for the output text file (default: utf-8)",
    )
    return parser


def extract_pdf_text(input_pdf: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency 'pypdf'. Install with: pip install -r requirements.txt"
        ) from exc

    reader = PdfReader(str(input_pdf))

    chunks: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        chunks.append(f"\n\n--- Page {index} ---\n\n{page_text}")

    return "".join(chunks).lstrip()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_pdf: Path = args.input_pdf
    if not input_pdf.exists() or not input_pdf.is_file():
        parser.error(f"Input PDF does not exist or is not a file: {input_pdf}")

    output_path: Path = args.output or input_pdf.with_suffix(".txt")

    try:
        text = extract_pdf_text(input_pdf)
    except Exception as exc:
        parser.error(str(exc))

    output_path.write_text(text, encoding=args.encoding)
    print(f"Saved extracted text to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
