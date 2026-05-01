import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from lib.frontmatter import parse_frontmatter, parse_file


def test_parse_frontmatter_basic():
    text = "---\ntype: entity\ntags: [a, b]\n---\n# Title\nBody"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "entity"
    assert fm["tags"] == ["a", "b"]
    assert body.strip() == "# Title\nBody"


def test_parse_frontmatter_no_frontmatter():
    text = "# Just a title\nNo frontmatter here"
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body == text


def test_parse_frontmatter_empty_values():
    text = "---\ntype: concept\nsource_url:\ntags: []\n---\nBody"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "concept"
    assert fm["source_url"] is None
    assert fm["tags"] == []


def test_parse_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("---\ntype: source\ncreated: 2026-01-01\n---\n# Test")
    fm, body = parse_file(f)
    assert fm["type"] == "source"
    assert fm["created"] == "2026-01-01"


def test_parse_frontmatter_quoted_strings():
    text = '---\nsource_url: "https://example.com"\ntitle: "A \\"quoted\\" title"\n---\nBody'
    fm, body = parse_frontmatter(text)
    assert fm["source_url"] == "https://example.com"
    assert fm["title"] == 'A "quoted" title'


def test_parse_frontmatter_multiline_ignored():
    text = "---\ntype: entity\ncategory: pricing\n---\n# Content"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "entity"
    assert fm["category"] == "pricing"
