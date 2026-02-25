# PDF to Text App

Small command-line application that reads a PDF file and writes its text into a `.txt` document.
It also supports OCR for scanned/image-only PDFs.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Tesseract OCR on your machine:

```bash
# macOS (Homebrew)
brew install tesseract
```

## Usage

```bash
python3 pdf_to_text.py /path/to/file.pdf
```

By default, output is written next to the input file with the same name and `.txt` extension.
Default OCR mode is `auto`, which OCRs pages where little/no embedded text is found.

### Custom output path

```bash
python3 pdf_to_text.py /path/to/file.pdf --output /path/to/output.txt
```

### OCR options

```bash
# Disable OCR
python3 pdf_to_text.py /path/to/file.pdf --ocr off

# Force OCR on every page
python3 pdf_to_text.py /path/to/file.pdf --ocr force

# Use a different OCR language (Tesseract language code)
python3 pdf_to_text.py /path/to/file.pdf --ocr-lang fin
```
