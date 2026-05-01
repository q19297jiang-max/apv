"""Tests for validate_urls tool."""
import json
import tempfile
from pathlib import Path

from validate_urls import extract_urls_from_file, validate_url_format, validate_directory


def _write_md(tmp: Path, name: str, content: str) -> Path:
    p = tmp / name
    p.write_text(content, encoding="utf-8")
    return p


def test_extract_urls_from_frontmatter(tmp_path):
    f = _write_md(tmp_path, "a.md", "---\nsource_url: https://example.com/page\n---\nBody text.\n")
    urls = extract_urls_from_file(f)
    assert len(urls) == 1
    assert urls[0]["url"] == "https://example.com/page"
    assert urls[0]["location"] == "frontmatter"


def test_extract_urls_from_body(tmp_path):
    f = _write_md(tmp_path, "b.md", "---\ntitle: Test\n---\nSee [link](https://example.com/doc) and http://bare.url/path for details.\n")
    urls = extract_urls_from_file(f)
    body_urls = [u for u in urls if u["location"] == "body"]
    found = {u["url"] for u in body_urls}
    assert "https://example.com/doc" in found
    assert "http://bare.url/path" in found


def test_validate_url_format_valid():
    r = validate_url_format("https://example.com/path?q=1")
    assert r["valid"] is True
    assert r["issue"] is None


def test_validate_url_format_invalid():
    r = validate_url_format("not-a-url")
    assert r["valid"] is False
    assert r["issue"] is not None


def test_validate_directory(tmp_path):
    _write_md(tmp_path, "good.md", "---\nsource_url: https://good.com\n---\n")
    _write_md(tmp_path, "bad.md", "---\nsource_url: not-a-url\n---\n")
    result = validate_directory(tmp_path)
    assert result["total_files"] == 2
    assert result["total_urls"] == 2
    assert result["valid"] == 1
    assert result["invalid"] == 1
