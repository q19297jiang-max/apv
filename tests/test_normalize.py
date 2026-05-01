"""Tests for normalize.py — raw RFP input normalizer."""
import tempfile
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from normalize import detect_input_type, normalize_raw_inputs

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "raw"


def test_detect_input_type_text():
    assert detect_input_type(Path("foo.txt")) == "text"


def test_detect_input_type_markdown():
    assert detect_input_type(Path("foo.md")) == "markdown"


def test_normalize_creates_required_outputs():
    with tempfile.TemporaryDirectory() as out:
        out_dir = Path(out)
        result = normalize_raw_inputs(FIXTURES, out_dir)
        rfp = out_dir / "rfp.md"
        assert rfp.exists(), "rfp.md not created"
        content = rfp.read_text()
        assert "Payment Gateway" in content


def test_normalize_text_to_markdown():
    with tempfile.TemporaryDirectory() as out:
        out_dir = Path(out)
        normalize_raw_inputs(FIXTURES, out_dir)
        content = (out_dir / "rfp.md").read_text()
        # Should have markdown headings from numbered sections
        assert "## " in content or "# " in content


def test_normalize_preserves_markdown():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_raw = Path(tmp) / "raw"
        tmp_raw.mkdir()
        tmp_out = Path(tmp) / "out"
        tmp_out.mkdir()
        md_content = "# Existing Header\n\nSome content.\n"
        (tmp_raw / "test.md").write_text(md_content)
        normalize_raw_inputs(tmp_raw, tmp_out)
        content = (tmp_out / "rfp.md").read_text()
        assert "Existing Header" in content
