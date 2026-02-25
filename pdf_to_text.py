#!/usr/bin/env python3
"""Extract text from a PDF file and save it as a .txt document.

Supports OCR for scanned/image-only PDFs.
"""

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
    parser.add_argument(
        "--ocr",
        choices=("off", "auto", "force"),
        default="auto",
        help="OCR mode: off, auto (OCR only pages with little/no text), or force (OCR all pages). Default: auto",
    )
    parser.add_argument(
        "--ocr-lang",
        default="eng",
        help="OCR language for Tesseract (default: eng)",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=20,
        help="In auto mode, OCR a page when extracted text has fewer than this many non-space characters (default: 20)",
    )
    return parser


def _ocr_pdf_page(input_pdf: Path, page_index: int, language: str) -> str:
    try:
        import pypdfium2 as pdfium
        import pytesseract
    except ImportError as exc:
        raise RuntimeError(
            "OCR dependencies are missing. Install with: pip install -r requirements.txt"
        ) from exc

    pdf_doc = pdfium.PdfDocument(str(input_pdf))
    page = pdf_doc[page_index]
    image = page.render(scale=2).to_pil()
    try:
        ocr_text = pytesseract.image_to_string(image, lang=language) or ""
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract binary not found. Install it first (example on macOS: brew install tesseract)."
        ) from exc
    finally:
        if hasattr(page, "close"):
            page.close()
        if hasattr(pdf_doc, "close"):
            pdf_doc.close()
    return ocr_text


def _should_ocr(page_text: str, ocr_mode: str, min_chars: int) -> bool:
    if ocr_mode == "force":
        return True
    if ocr_mode == "off":
        return False
    return len("".join(page_text.split())) < min_chars


def extract_pdf_text(
    input_pdf: Path, ocr_mode: str, ocr_language: str, min_chars: int
) -> str:
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
        if _should_ocr(page_text, ocr_mode=ocr_mode, min_chars=min_chars):
            page_text = _ocr_pdf_page(
                input_pdf=input_pdf,
                page_index=index - 1,
                language=ocr_language,
            )
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
        text = extract_pdf_text(
            input_pdf,
            ocr_mode=args.ocr,
            ocr_language=args.ocr_lang,
            min_chars=args.min_chars,
        )
    except Exception as exc:
        parser.error(str(exc))

    output_path.write_text(text, encoding=args.encoding)
    print(f"Saved extracted text to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
