"""Zero-dependency YAML frontmatter parser for markdown files."""

import re
from pathlib import Path


def _parse_value(raw: str):
    """Parse a YAML scalar value."""
    val = raw.strip()
    if not val or val in ("null", "~"):
        return None
    if val == "true":
        return True
    if val == "false":
        return False
    # Bracket array
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_parse_value(item) for item in _split_array(inner)]
    # Quoted string
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        s = val[1:-1]
        if val[0] == '"':
            s = s.replace('\\"', '"').replace("\\\\", "\\")
        return s
    # Number
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        pass
    # Date-like strings: keep as string
    return val


def _split_array(s: str) -> list[str]:
    """Split comma-separated array items, respecting quotes."""
    items = []
    current = []
    in_quote = None
    for ch in s:
        if ch in ('"', "'") and in_quote is None:
            in_quote = ch
            current.append(ch)
        elif ch == in_quote:
            in_quote = None
            current.append(ch)
        elif ch == "," and in_quote is None:
            items.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        items.append("".join(current))
    return items


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown text. Returns (frontmatter_dict, body)."""
    if not text.startswith("---"):
        return {}, text
    # Find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    yaml_block = text[4:end]  # skip "---\n"
    body = text[end + 4:]  # skip "\n---"
    if body.startswith("\n"):
        body = body[1:]

    fm = {}
    for line in yaml_block.split("\n"):
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        if key:
            fm[key] = _parse_value(val)
    return fm, body


def parse_file(path: Path) -> tuple[dict, str]:
    """Read a markdown file and parse its frontmatter."""
    return parse_frontmatter(Path(path).read_text(encoding="utf-8"))
