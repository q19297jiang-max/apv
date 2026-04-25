#!/usr/bin/env python3
"""
APV Unit Test Framework

Tests each APV skill independently with mock data.

Usage:
    python3 run_unit_tests.py [--skill SKILL_NAME] [--verbose]
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import argparse

# Add wiki path to Python path
WIKI_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WIKI_PATH))

class APVUnitTest:
    """Base class for APV unit tests"""

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def assert_true(self, condition: bool, message: str):
        """Assert that condition is True"""
        self.tests_run += 1
        if condition:
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL"
            })
            print(f"  ❌ {message}")

    def assert_equals(self, actual: Any, expected: Any, message: str):
        """Assert that actual equals expected"""
        self.tests_run += 1
        if actual == expected:
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL",
                "expected": expected,
                "actual": actual
            })
            print(f"  ❌ {message}")
            print(f"     Expected: {expected}")
            print(f"     Actual: {actual}")

    def assert_not_empty(self, value: str, message: str):
        """Assert that string is not empty"""
        self.tests_run += 1
        if value and len(value.strip()) > 0:
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL"
            })
            print(f"  ❌ {message} (value is empty)")

    def assert_contains(self, text: str, substring: str, message: str):
        """Assert that text contains substring"""
        self.tests_run += 1
        if substring in text:
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL",
                "substring": substring
            })
            print(f"  ❌ {message} (substring not found)")

    def assert_file_exists(self, file_path: Path, message: str):
        """Assert that file exists"""
        self.tests_run += 1
        if file_path.exists():
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL",
                "path": str(file_path)
            })
            print(f"  ❌ {message} (file not found: {file_path})")

    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"{self.skill_name} Unit Test Summary")
        print(f"{'='*60}")
        print(f"Tests Run: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        if self.tests_failed == 0:
            print(f"Result: ✅ ALL TESTS PASSED")
        else:
            print(f"Result: ❌ {self.tests_failed} TESTS FAILED")
        print(f"{'='*60}")
        return self.tests_failed == 0


def test_skill_file_exists(test: APVUnitTest, skill_path: Path):
    """Test that skill files exist"""
    print("\n📁 Testing Skill Files Existence:")
    test.assert_file_exists(skill_path / "skill.md", "skill.md exists")
    test.assert_file_exists(skill_path / "prompt.md", "prompt.md exists")


def test_skill_frontmatter(test: APVUnitTest, skill_path: Path):
    """Test that skill files have valid frontmatter"""
    print("\n📝 Testing Skill Frontmatter:")

    skill_md = skill_path / "skill.md"
    if skill_md.exists():
        with open(skill_md, 'r') as f:
            content = f.read()
        test.assert_contains(content, "---", "Frontmatter delimiter exists")
        test.assert_contains(content, "name:", "name field exists")
        test.assert_contains(content, "description:", "description field exists")
        test.assert_contains(content, "version:", "version field exists")
        test.assert_contains(content, "created:", "created field exists")
        test.assert_contains(content, "tags:", "tags field exists")


def test_skill_documentation_exists(test: APVUnitTest, skill_name: str):
    """Test that skill has wiki documentation"""
    print("\n📚 Testing Wiki Documentation:")

    wiki_skill = WIKI_PATH / "apv" / "skills" / f"{skill_name}.md"
    test.assert_file_exists(wiki_skill, f"Wiki documentation exists for {skill_name}")


def run_skill_tests(skill_name: str) -> APVUnitTest:
    """Run all tests for a skill"""
    print(f"\n{'='*60}")
    print(f"Testing: {skill_name}")
    print(f"{'='*60}")

    test = APVUnitTest(skill_name)
    skill_path = Path.home() / ".claude" / "skills" / skill_name

    # Run tests
    test_skill_file_exists(test, skill_path)
    test_skill_frontmatter(test, skill_path)

    # Special handling for orchestrator
    if skill_name == "apv":
        test_skill_documentation_exists(test, "apv-orchestrator")
    else:
        test_skill_documentation_exists(test, skill_name)

    test.summary()
    return test


def main():
    parser = argparse.ArgumentParser(description="Run APV unit tests")
    parser.add_argument("--skill", help="Test specific skill only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    skills = [
        "rfp-brainstorm",
        "rfp-compliance",
        "rfp-architect",
        "rfp-calculator",
        "rfp-pricer",
        "rfp-generator",
        "apv-reviewer",
        "apv"
    ]

    if args.skill:
        skills = [args.skill]

    all_passed = True
    results = {}

    for skill in skills:
        test_result = run_skill_tests(skill)
        results[skill] = {
            "total": test_result.tests_run,
            "passed": test_result.tests_passed,
            "failed": test_result.tests_failed,
            "status": "PASS" if test_result.tests_failed == 0 else "FAIL"
        }
        if test_result.tests_failed > 0:
            all_passed = False

    # Overall summary
    print(f"\n{'='*60}")
    print("OVERALL UNIT TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Skills Tested: {len(skills)}")
    print(f"Overall Status: {'✅ PASS' if all_passed else '❌ FAIL'}")
    print(f"\nDetailed Results:")
    for skill, result in results.items():
        status = "✅" if result["status"] == "PASS" else "❌"
        print(f"  {status} {skill}: {result['passed']}/{result['total']} passed")
    print(f"{'='*60}")

    # Save results
    output_file = WIKI_PATH / "apv" / "tests" / "unit" / "test-results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "test_date": datetime.now(timezone.utc).isoformat(),
        "test_type": "unit",
        "skills_tested": len(skills),
        "overall_status": "PASS" if all_passed else "FAIL",
        "results": results
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📊 Test results saved to: {output_file}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
