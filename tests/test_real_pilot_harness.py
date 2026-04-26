from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


TESTS_ROOT = Path(__file__).resolve().parent
HARNESS_PATH = TESTS_ROOT / "run_real_pilot_harness.py"

spec = spec_from_file_location("run_real_pilot_harness", HARNESS_PATH)
run_real_pilot_harness = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run_real_pilot_harness)


def test_compare_selected_files_reports_no_differences_for_matching_projects(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"

    for project_root in (left, right):
        (project_root / "outputs").mkdir(parents=True)
        (project_root / "outputs" / "02-compliance.md").write_text("same compliance\n", encoding="utf-8")
        (project_root / "outputs" / "05-pricing.md").write_text("same pricing\n", encoding="utf-8")
        (project_root / "outputs" / "06-response.md").write_text("same response\n", encoding="utf-8")

    differences = run_real_pilot_harness.compare_selected_files(left, right)

    assert differences == []


def test_compare_selected_files_reports_missing_or_mismatched_files(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"

    (left / "outputs").mkdir(parents=True)
    (right / "outputs").mkdir(parents=True)

    (left / "outputs" / "02-compliance.md").write_text("left compliance\n", encoding="utf-8")
    (right / "outputs" / "02-compliance.md").write_text("right compliance\n", encoding="utf-8")
    (left / "outputs" / "05-pricing.md").write_text("left pricing\n", encoding="utf-8")
    (right / "outputs" / "06-response.md").write_text("right response\n", encoding="utf-8")

    differences = run_real_pilot_harness.compare_selected_files(left, right)

    assert any("outputs/02-compliance.md: content differs" == item for item in differences)
    assert any("outputs/05-pricing.md: missing in comparison project" == item for item in differences)
    assert any("outputs/06-response.md: missing in baseline project" == item for item in differences)