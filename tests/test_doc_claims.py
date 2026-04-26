from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PHRASES = {
    "README.md": [
        "100% source URL compliance enforced",
        "Design complete, implementation pending",
    ],
    "meta/system-index.md": [
        "100% source URL compliance: 100%",
    ],
}


def test_top_level_docs_do_not_reintroduce_unqualified_claims() -> None:
    failures: list[str] = []

    for relative_path, phrases in FORBIDDEN_PHRASES.items():
        content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase in content:
                failures.append(f"{relative_path}: contains forbidden phrase: {phrase}")

    assert not failures, "\n".join(failures)