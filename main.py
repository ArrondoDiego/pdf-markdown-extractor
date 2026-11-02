#!/usr/bin/env python3
"""Script to extract PDF to markdown chunks and generate a clean HTML file from a template."""
import os
import sys
import re
import warnings
import pymupdf

# Suppress warnings globally
warnings.filterwarnings("ignore")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNKS_DIR = os.path.join(PROJECT_ROOT, "dir", "files")
SUMMARIES_DIR = os.path.join(PROJECT_ROOT, "dir", "summaries")
TEMPLATE_HTML = os.path.join(PROJECT_ROOT, "template.html")
OUTPUT_HTML = os.path.join(PROJECT_ROOT, "index.html")
PAGES_PER_CHUNK = 50

def md_to_html(text):
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
        if stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            content = stripped[2:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
            content = re.sub(r'__(.+?)__', r'\1', content)
            content = re.sub(r'\*(.+?)\*', r'\1', content)
            content = re.sub(r'_(.+?)_', r'\1', content)
            html_lines.append(f'<h3 class="chunk-title">{content}</h3>')
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            content = stripped[3:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
            content = re.sub(r'__(.+?)__', r'\1', content)
            content = re.sub(r'\*(.+?)\*', r'\1', content)
            content = re.sub(r'_(.+?)_', r'\1', content)
            html_lines.append(f'<h4 class="chunk-subtitle">{content}</h4>')
        elif stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            content = stripped[4:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
            content = re.sub(r'__(.+?)__', r'\1', content)
            content = re.sub(r'\*(.+?)\*', r'\1', content)
            content = re.sub(r'_(.+?)_', r'\1', content)
            html_lines.append(f'<h5 class="chunk-sub3">{content}</h5>')
        elif stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:].strip()
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'__(.+?)__', r'<strong>\1</strong>', content)
            html_lines.append(f"<li>{content}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            content = stripped
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'__(.+?)__', r'<strong>\1</strong>', content)
            if content.startswith("_") and content.endswith("_") and content.count("_") == 2:
                content = f"<em>{content[1:-1]}</em>"
            elif content.startswith("*") and content.endswith("*") and content.count("*") == 2:
                content = f"<em>{content[1:-1]}</em>"
            html_lines.append(f"<p>{content}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n            ".join(html_lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract PDF to HTML summary book.")
    parser.add_argument("--quiet", action="store_true", help="Suppress terminal warning and info outputs")
    args = parser.parse_args()

    if args.quiet:
        sys.stderr = open(os.devnull, 'w')

    pdf_files = [f for f in os.listdir(PROJECT_ROOT) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print(f"Error: No PDF files found in '{PROJECT_ROOT}'.")
        sys.exit(1)
    elif len(pdf_files) == 1:
        pdf_path = os.path.join(PROJECT_ROOT, pdf_files[0])
        if not args.quiet:
            print(f"Found single PDF: {pdf_files[0]}")
    else:
        print("Multiple PDF files found:")
        for idx, pdf in enumerate(pdf_files, 1):
            print(f"  [{idx}] {pdf}")
        while True:
            try:
                choice = input("Select the number of the PDF to process: ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(pdf_files):
                    pdf_path = os.path.join(PROJECT_ROOT, pdf_files[choice_idx])
                    break
                else:
                    print("Invalid selection. Please try again.")
            except (ValueError, EOFError):
                print("Invalid input. Please enter a valid number.")

    if not os.path.exists(TEMPLATE_HTML):
        print(f"Error: Template file '{TEMPLATE_HTML}' not found.")
        sys.exit(1)

    os.makedirs(CHUNKS_DIR, exist_ok=True)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    total_pages = doc.page_count
    total_parts = (total_pages + PAGES_PER_CHUNK - 1) // PAGES_PER_CHUNK
    
    if not args.quiet:
        print(f"Processing PDF: {total_pages} pages -> {total_parts} parts.")

    import pymupdf4llm
    for start in range(0, total_pages, PAGES_PER_CHUNK):
        end = min(start + PAGES_PER_CHUNK, total_pages)
        part = start // PAGES_PER_CHUNK + 1
        
        if not args.quiet:
            print(f"[{part}/{total_parts}] Converting pages {start+1}-{end}...")
            
        md_text = pymupdf4llm.to_markdown(pdf_path, pages=list(range(start, end)))
        if isinstance(md_text, list):
            md_text = "\n".join(str(x) for x in md_text)
        
        for target_dir in [CHUNKS_DIR, SUMMARIES_DIR]:
            with open(os.path.join(target_dir, f"chunk_{part:03d}.md"), "w", encoding="utf-8") as f:
                f.write(f"# Part {part:03d} (Pages {start+1}-{end})\n\n" + str(md_text))
    doc.close()

    with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
        html_template = f.read()

    doc_meta = pymupdf.open(pdf_path)
    meta = doc_meta.metadata
    book_title = meta.get("title", "Unknown Title") if isinstance(meta, dict) else "Unknown Title"
    book_author = meta.get("author", "Unknown Author") if isinstance(meta, dict) else "Unknown Author"
    doc_meta.close()

    chunks = []
    for i in range(1, total_parts + 1):
        fpath = os.path.join(SUMMARIES_DIR, f"chunk_{i:03d}.md")
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                chunks.append((i, f.read()))

    toc_html = "\n            ".join([f'<a href="#detail-{i}"><span class="n">{i:03d}</span> Part {i:03d}</a>' for i, _ in chunks])
    details_html = "\n".join([f'<section class="chunk detail" id="detail-{i}">\n        {md_to_html(content)}\n        <div class="back-top"><a href="#top">Back to top</a></div>\n    </section>' for i, content in chunks])

    final_html = html_template.replace("<!-- BOOK_TITLE -->", book_title)
    final_html = final_html.replace("<!-- BOOK_AUTHOR -->", book_author)
    final_html = final_html.replace("<!-- TOC_PLACEHOLDER -->", toc_html)
    final_html = final_html.replace("<!-- DETAILS_PLACEHOLDER -->", details_html)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(final_html)

    if not args.quiet:
        print("Successfully completed! Generated index.html from template.html.")

if __name__ == "__main__":
    main()
