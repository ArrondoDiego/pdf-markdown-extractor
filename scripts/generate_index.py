#!/usr/bin/env python3
"""Generate index HTML from chunk summaries."""
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMARIES_DIR = os.path.join(PROJECT_ROOT, "dir", "summaries")

def md_to_html(text):
    """Very simple markdown to HTML converter."""
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("")
            continue
        if stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h2 class="chunk-title">{stripped[2:]}</h2>')
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h3 class="chunk-subtitle">{stripped[3:]}</h3>')
        elif stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f'<h4 class="chunk-sub3">{stripped[4:]}</h4>')
        elif stripped.startswith("---"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append('<hr class="chunk-hr">')
        elif stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            html_lines.append(f"<li>{content}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            content = stripped
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            html_lines.append(f"<p>{content}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n        ".join(html_lines)


def main():
    chunks = []
    for i in range(1, 22):
        fname = f"chunk_{i:03d}.md"
        fpath = os.path.join(SUMMARIES_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            chunks.append((i, content))
    print(f"Loaded {len(chunks)} summary chunks successfully.")

if __name__ == "__main__":
    main()
