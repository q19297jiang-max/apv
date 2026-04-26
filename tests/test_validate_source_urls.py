from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch


TOOLS_ROOT = Path(__file__).resolve().parents[1] / "tools"
VALIDATOR_PATH = TOOLS_ROOT / "validate-source-urls.py"

spec = spec_from_file_location("validate_source_urls", VALIDATOR_PATH)
validate_source_urls = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validate_source_urls)


def test_extract_urls_from_content_ignores_internal_anchor_links() -> None:
    content = "1. [Executive Summary](#1-executive-summary)\n2. [Compliance](#2-compliance)\n"

    assert validate_source_urls.extract_urls_from_content(content) == []


def test_check_url_accessible_falls_back_to_get_when_head_fails() -> None:
    calls: list[str] = []

    class FakeResponse:
        def __init__(self, status: int):
            self.status = status

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(request, timeout=10):
        calls.append(request.get_method())
        if request.get_method() == "HEAD":
            raise HTTPError(request.full_url, 405, "Method Not Allowed", {}, None)
        return FakeResponse(200)

    with patch.object(validate_source_urls.urllib.request, "urlopen", side_effect=fake_urlopen):
        assert validate_source_urls.check_url_accessible(
            "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
        ) is True

    assert calls == ["HEAD", "GET"]