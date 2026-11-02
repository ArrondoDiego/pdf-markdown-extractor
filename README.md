# PDF Book Processor & Summarizer

A Python-based toolkit for extracting text from large PDF documents (such as novels or long-form books), chunking them by pages, converting them to Markdown using PyMuPDF / `pymupdf4llm`, and generating structured HTML summary pages with responsive navigation from an HTML template.

## Features

- **PDF Chunking & Extraction**: Splits large PDF files into manageable page ranges (e.g., 50 pages per chunk) and converts them into structured Markdown (`dir/files/`).
- **Structured Summaries**: Organizes summaries into markdown files (`dir/summaries/`).
- **Interactive HTML Viewer**: Generates beautiful, responsive dark-themed HTML documentation (`index.html`) using `template.html` complete with tables of contents, theme toggles, and bookmark links.

## Project Structure

```text
├── book.pdf             # Source PDF document (ignored in git)
├── index.html           # Generated interactive HTML summary & reader interface (ignored in git)
├── template.html        # HTML template used to generate index.html
├── main.py              # PDF text extraction and HTML generation script
├── dir/
│   ├── files/           # Extracted markdown chunks (chunk_001.md, etc.)
│   └── summaries/       # Structured markdown summaries
├── requirements.txt     # Python dependencies
└── .gitignore           # Git ignore rules
```

## Usage

1. Place your target PDF file in the root directory as `book.pdf`.

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the extraction and generation script:
   ```bash
   python main.py
   ```
5. Open `index.html` in your web browser to explore the processed book and summaries.
