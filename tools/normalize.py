#!/usr/bin/env python3
"""normalize.py — Convert raw RFP inputs to normalized markdown.

Reads all files in a raw directory, converts to markdown,
writes standard normalized files (rfp.md, requirements-summary.md, volume-summary.md).
"""
import argparse
import re
from pathlib import Path


def detect_input_type(file_path: Path) -> str:
    """Return 'markdown', 'text', or 'csv' based on file extension."""
    ext = file_path.suffix.lower()
    if ext in (".md", ".markdown"):
        return "markdown"
    elif ext in (".csv",):
        return "csv"
    else:
        return "text"


def _text_to_markdown(text: str) -> str:
    """Convert plain text to markdown.

    Detects numbered sections ('1. TITLE'), ALL-CAPS titles, and key:value lines.
    """
    lines = text.splitlines()
    out: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Numbered section heading: "1. BACKGROUND" → "## 1. Background"
        m = re.match(r"^(\d+)\.\s+([A-Z][A-Z\s]+)$", stripped)
        if m:
            num, title = m.group(1), m.group(2)
            out.append(f"\n## {num}. {title.title().strip()}\n")
            continue

        # Standalone ALL-CAPS line (≥3 chars, no leading digit) → heading
        if re.match(r"^[A-Z][A-Z\s]{2,}$", stripped) and not re.match(r"^\d", stripped):
            out.append(f"\n# {stripped.title().strip()}\n")
            continue

        # Key: Value on its own line → **Key:** Value
        km = re.match(r"^([A-Za-z][A-Za-z\s]+):\s+(.+)$", stripped)
        if km and len(km.group(1).split()) <= 4:
            out.append(f"**{km.group(1).strip()}:** {km.group(2).strip()}")
            continue

        out.append(line)

    return "\n".join(out) + "\n"


def _extract_section(md: str, heading_pattern: str) -> str | None:
    """Extract content under a heading matching pattern until next heading."""
    lines = md.splitlines()
    collecting = False
    result: list[str] = []
    for line in lines:
        if re.search(heading_pattern, line, re.IGNORECASE) and line.strip().startswith("#"):
            collecting = True
            result.append(line)
            continue
        if collecting:
            if line.strip().startswith("#"):
                break
            result.append(line)
    return "\n".join(result).strip() if result else None


def normalize_raw_inputs(raw_dir: Path, output_dir: Path) -> dict[str, str]:
    """Process all files in raw_dir, write normalized outputs to output_dir.

    Returns dict of filename → status.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, str] = {}
    all_content: list[str] = []

    for f in sorted(raw_dir.iterdir()):
        if not f.is_file():
            continue
        input_type = detect_input_type(f)
        text = f.read_text(encoding="utf-8")

        if input_type == "markdown":
            md = text
        elif input_type == "text":
            md = _text_to_markdown(text)
        else:
            # CSV: wrap as code block for now
            md = f"# {f.stem}\n\n```csv\n{text}\n```\n"

        all_content.append(md)
        results[f.name] = "ok"

    combined = "\n\n---\n\n".join(all_content)

    # Write rfp.md — full combined content
    (output_dir / "rfp.md").write_text(combined, encoding="utf-8")

    # Extract requirements section if present
    req = _extract_section(combined, r"requirement")
    if req:
        (output_dir / "requirements-summary.md").write_text(
            f"# Requirements Summary\n\n{req}\n", encoding="utf-8"
        )
        results["requirements-summary.md"] = "generated"

    # Extract volume section if present
    vol = _extract_section(combined, r"volume")
    if vol:
        (output_dir / "volume-summary.md").write_text(
            f"# Volume Summary\n\n{vol}\n", encoding="utf-8"
        )
        results["volume-summary.md"] = "generated"

    return results


def main():
    parser = argparse.ArgumentParser(description="Normalize raw RFP inputs to markdown")
    parser.add_argument("--raw-dir", type=Path, required=True, help="Directory with raw input files")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output directory for normalized files")
    args = parser.parse_args()

    results = normalize_raw_inputs(args.raw_dir, args.output_dir)
    for name, status in results.items():
        print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
