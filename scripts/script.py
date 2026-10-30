import sys
import os
import pymupdf4llm
import pymupdf

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(PROJECT_ROOT, "book.pdf")
PAGES_PER_CHUNK = 20
CHUNKS_DIR = os.path.join(PROJECT_ROOT, "dir", "files")


def main():
    if not os.path.exists(PDF_PATH):
        print(f"Error: '{PDF_PATH}' not found")
        sys.exit(1)

    os.makedirs(CHUNKS_DIR, exist_ok=True)

    doc = pymupdf.open(PDF_PATH)
    total_pages = doc.page_count
    total_parts = (total_pages + PAGES_PER_CHUNK - 1) // PAGES_PER_CHUNK
    print(f"PDF: {total_pages} pages -> {total_parts} chunks of {PAGES_PER_CHUNK}")

    for start in range(0, total_pages, PAGES_PER_CHUNK):
        end = min(start + PAGES_PER_CHUNK, total_pages)
        part = start // PAGES_PER_CHUNK + 1
        pages_label = f"{start + 1}-{end}"

        chunk_file = os.path.join(CHUNKS_DIR, f"chunk_{part:03d}.md")

        print(f"[{part}/{total_parts}] Converting pages {pages_label}...")
        md_text = pymupdf4llm.to_markdown(PDF_PATH, pages=list(range(start, end)))
        if isinstance(md_text, list):
            md_text = "\n".join(str(item) for item in md_text)
        elif not isinstance(md_text, str):
            md_text = str(md_text)
        with open(chunk_file, "w", encoding="utf-8") as f:
            f.write(md_text)

    doc.close()
    print("Done!")


if __name__ == "__main__":
    main()
