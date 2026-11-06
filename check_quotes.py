"""
Check that every quotation in a brief appears word for word in the judgment.

This is step 11 of SKILL.md ("Every quotation must appear word for word in
the supplied text"), made checkable. Spacing and line breaks are ignored;
everything else must match exactly.

Usage:  python check_quotes.py BRIEF.md JUDGMENT.(txt|pdf)
        (a PDF needs pdftotext, from Poppler)
"""

import re
import subprocess
import sys
from pathlib import Path


def judgment_text(path):
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True,
                              text=True, check=True).stdout
    return path.read_text(encoding="utf-8")


def squash(text):
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return " ".join(text.split())


def pages(text):
    """Map a position in the squashed text to its page (Indian Kanoon page footers or form feeds)."""
    marks, pos, page = [], 0, 1
    for chunk in re.split(r"(\f)", text):
        if chunk == "\f":
            page += 1
            continue
        marks.append((pos, page))
        pos += len(squash(chunk)) + 1
    return marks


def page_at(marks, i):
    page = 1
    for start, p in marks:
        if start <= i:
            page = p
    return page


def main(brief, judgment):
    raw = judgment_text(judgment)
    text = squash(raw)
    marks = pages(raw)
    brief_text = squash(Path(brief).read_text(encoding="utf-8"))
    quotes = [q.strip() for q in re.findall(r'"([^"]+)"', brief_text)]   # quotes are paired in order
    quotes = [q for q in quotes if len(q.split()) >= 3]                    # skip single words like "law"
    ok = 0
    for q in quotes:
        i = text.find(squash(q))
        if i >= 0:
            ok += 1
            print(f"  FOUND (p. {page_at(marks, i)})  “{q[:70]}{'…' if len(q) > 70 else ''}”")
        else:
            print(f"  NOT FOUND           “{q[:70]}{'…' if len(q) > 70 else ''}”")
    print(f"\n{ok} of {len(quotes)} quotations found word for word in the judgment.")
    return 0 if ok == len(quotes) else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
