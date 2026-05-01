"""Post-RFP knowledge promotion tool.

Reads the gap log from a completed project, identifies unresolved knowledge
gaps, and generates suggestions for new knowledge pages.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_gap_log(gap_log_path: Path) -> list[dict]:
    """Parse ``working/00-gap-log.md`` markdown table.

    Returns list of dicts with keys: id, domain, description, severity,
    stage_found, resolved.
    """
    path = Path(gap_log_path)
    if not path.exists():
        return []
    text = path.read_text()
    if not text.strip():
        return []

    gaps: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 6:
            continue
        # Skip header / separator rows
        if cells[0] == "#" or set(cells[0]) <= {"-"}:
            continue
        try:
            gap_id = int(cells[0])
        except ValueError:
            continue
        gaps.append({
            "id": gap_id,
            "domain": cells[1],
            "description": cells[2],
            "severity": cells[3],
            "stage_found": cells[4],
            "resolved": cells[5].strip().lower() == "yes",
        })
    return gaps


def _slugify(text: str) -> str:
    """Convert text to kebab-case slug."""
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60]


def suggest_promotions(gaps: list[dict]) -> list[dict]:
    """Filter unresolved gaps and map to knowledge page suggestions."""
    suggestions: list[dict] = []
    for g in gaps:
        if g["resolved"]:
            continue
        slug = _slugify(g["description"])
        suggestions.append({
            "domain": g["domain"],
            "suggested_path": f"knowledge/{g['domain']}/{slug}.md",
            "title": g["description"],
            "description": g["description"],
            "severity": g["severity"],
        })
    return suggestions


def generate_promotion_report(gap_log_path: Path, output_path: Path) -> dict:
    """Write promotion suggestions to *output_path* and return stats."""
    gaps = parse_gap_log(gap_log_path)
    suggestions = suggest_promotions(gaps)
    unresolved = sum(1 for g in gaps if not g["resolved"])

    lines = ["# Knowledge Promotion Report\n"]
    lines.append(f"- **Total gaps**: {len(gaps)}")
    lines.append(f"- **Unresolved**: {unresolved}")
    lines.append(f"- **Promotions suggested**: {len(suggestions)}\n")

    if suggestions:
        lines.append("## Suggested Pages\n")
        lines.append("| Domain | Title | Severity | Suggested Path |")
        lines.append("|--------|-------|----------|----------------|")
        for s in suggestions:
            lines.append(f"| {s['domain']} | {s['title']} | {s['severity']} | `{s['suggested_path']}` |")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n")

    return {
        "total_gaps": len(gaps),
        "unresolved": unresolved,
        "promotions": len(suggestions),
    }


def main():
    parser = argparse.ArgumentParser(description="Promote knowledge gaps to page suggestions")
    parser.add_argument("--gap-log", required=True, help="Path to gap log markdown file")
    parser.add_argument("--output", default=None, help="Output report path")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    args = parser.parse_args()

    gap_log_path = Path(args.gap_log)
    if not gap_log_path.exists():
        print(f"Error: {gap_log_path} not found", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = gap_log_path.parent / "promotion-report.md"

    stats = generate_promotion_report(gap_log_path, output_path)

    if args.json_output:
        gaps = parse_gap_log(gap_log_path)
        suggestions = suggest_promotions(gaps)
        print(json.dumps({"stats": stats, "suggestions": suggestions}, indent=2))
    else:
        print(f"Promotion report written to {output_path}")
        print(f"  Total gaps: {stats['total_gaps']}")
        print(f"  Unresolved: {stats['unresolved']}")
        print(f"  Promotions: {stats['promotions']}")


if __name__ == "__main__":
    main()
