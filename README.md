# PDF to Text App

Small command-line application that reads a PDF file and writes its text into a `.txt` document.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 pdf_to_text.py /path/to/file.pdf
```

By default, output is written next to the input file with the same name and `.txt` extension.

### Custom output path

```bash
python3 pdf_to_text.py /path/to/file.pdf --output /path/to/output.txt
```
