#!/usr/bin/env python3
"""
APV Document to Markdown Converter - Uses Microsoft markitdown to convert files.

This tool wraps Microsoft's markitdown to convert various document formats
(PDF, DOCX, XLSX, PPTX, etc.) to Markdown for APV processing.

Usage:
    python convert-to-markdown.py <input-file> [output-file]
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


def get_markitdown_path():
    """Find the markitdown executable."""
    # Common user installation paths
    possible_paths = [
        "/Users/stevenjiang/Library/Python/3.14/bin/markitdown",
        "/usr/local/bin/markitdown",
        os.path.expanduser("~/.local/bin/markitdown"),
        "markitdown",  # Try from PATH
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Try to find via 'which'
    try:
        result = subprocess.run(["which", "markitdown"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass

    return None


def convert_to_markdown(input_file, output_file=None):
    """
    Convert a document to markdown using Microsoft markitdown.

    Args:
        input_file: Path to input file (PDF, DOCX, XLSX, PPTX, etc.)
        output_file: Path to output markdown file (optional)

    Returns:
        str: Markdown content or output file path
    """
    markitdown_path = get_markitdown_path()

    if not markitdown_path:
        raise RuntimeError(
            "markitdown not found. Install it with:\n"
            "  pip3 install --user --break-system-packages markitdown\n"
            "Or: pipx install markitdown"
        )

    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.with_suffix('.md')

    output_path = Path(output_file)

    # Run markitdown
    cmd = [markitdown_path, str(input_path), "-o", str(output_path)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )

        if result.returncode != 0:
            raise RuntimeError(f"markitdown failed: {result.stderr}")

        # Read the output file
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add APV metadata header
        metadata = f"""---
type: apv-meta
category: rfp-document
title: "Converted from {input_path.name}"
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
tags: [apv, rfp, converted, markitdown]
source_file: {input_path.name}
---

"""

        # Prepend metadata
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(metadata + content)

        return str(output_path)

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"markitdown timed out after 60 seconds")
    except Exception as e:
        raise RuntimeError(f"Error running markitdown: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-to-markdown.py <input-file> [output-file]")
        print("\nSupported formats: PDF, DOCX, XLSX, PPTX, TXT, HTML, and more")
        print("\nExamples:")
        print("  python convert-to-markdown.py document.pdf")
        print("  python convert-to-markdown.py document.docx output.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result_path = convert_to_markdown(input_file, output_file)
        print(f"✅ Converted to markdown: {result_path}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
