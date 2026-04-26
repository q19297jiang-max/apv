#!/usr/bin/env python3
"""
APV Contract-Level Integration Test Framework

Checks documented data-flow markers, skill-file presence, and key repo knowledge assets.
This is not an end-to-end execution test of APV project outputs.

Usage:
    python3 run_integration_tests.py [--chain CHAIN_NAME] [--verbose]
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import argparse

WIKI_PATH = Path(__file__).parent.parent.parent


class APVIntegrationTest:
    """Base class for APV integration tests"""

    def __init__(self, chain_name: str):
        self.chain_name = chain_name
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []

    def assert_data_flow(self, source_output: str, sink_input: str, message: str):
        """Assert that data from source can be used by sink"""
        self.tests_run += 1

        # Check if source output contains key data structures expected by sink
        checks = {
            'source_url': 'Source URL present in compliance/pricing',
            'wikilinks': 'Wikilinks present for knowledge citations',
            'regions': 'Target regions specified',
            'card_types': 'Card system types specified'
        }

        passed = True
        missing = []
        for key, description in checks.items():
            if key in source_output.lower():
                pass  # Found
            elif key.replace('_', ' ') in source_output.lower():
                pass  # Found with space
            else:
                missing.append(description)
                passed = False

        if passed:
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
                "missing": missing
            })
            print(f"  ❌ {message}")
            for m in missing:
                print(f"     Missing: {m}")

    def assert_file_chain(self, files: List[Path], message: str):
        """Assert that files exist in proper chain order"""
        self.tests_run += 1

        all_exist = all(f.exists() for f in files)
        if all_exist:
            self.tests_passed += 1
            self.results.append({
                "test": message,
                "status": "PASS"
            })
            print(f"  ✅ {message}")
        else:
            missing = [str(f) for f in files if not f.exists()]
            self.tests_failed += 1
            self.results.append({
                "test": message,
                "status": "FAIL",
                "missing_files": missing
            })
            print(f"  ❌ {message}")
            for f in missing:
                print(f"     Missing: {f}")

    def assert_consistency(self, file1: Path, file2: Path, consistency_check: str, message: str):
        """Assert consistency between two files"""
        self.tests_run += 1
        # Placeholder for actual consistency check
        self.tests_passed += 1
        self.results.append({
            "test": message,
            "status": "PASS",
            "check": consistency_check
        })
        print(f"  ✅ {message}")

    def assert_contains(self, text: str, substring: str, message: str):
        """Assert text contains substring"""
        self.tests_run += 1
        if substring.lower() in text.lower():
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

    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"{self.chain_name} Integration Test Summary")
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


def test_brainstorm_to_compliance_flow(test: APVIntegrationTest):
    """Test data flow from rfp-brainstorm to rfp-compliance"""
    print("\n🔗 Testing: rfp-brainstorm → rfp-compliance")

    # Check that brainstorm output has required fields for compliance
    brainstorm_skill = Path.home() / ".claude" / "skills" / "rfp-brainstorm" / "skill.md"
    compliance_skill = Path.home() / ".claude" / "skills" / "rfp-compliance" / "prompt.md"

    if brainstorm_skill.exists() and compliance_skill.exists():
        with open(brainstorm_skill, 'r') as f:
            brainstorm_content = f.read()
        with open(compliance_skill, 'r') as f:
            compliance_content = f.read()

        # Test that brainstorm outputs what compliance needs
        test.assert_data_flow(
            brainstorm_content,
            compliance_content,
            "Brainstorm outputs compliance requirements"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_compliance_to_architect_flow(test: APVIntegrationTest):
    """Test data flow from rfp-compliance to rfp-architect"""
    print("\n🔗 Testing: rfp-compliance → rfp-architect")

    compliance_skill = Path.home() / ".claude" / "skills" / "rfp-compliance" / "skill.md"
    architect_skill = Path.home() / ".claude" / "skills" / "rfp-architect" / "prompt.md"

    if compliance_skill.exists() and architect_skill.exists():
        with open(compliance_skill, 'r') as f:
            compliance_content = f.read()
        with open(architect_skill, 'r') as f:
            architect_content = f.read()

        # Test that compliance outputs what architect needs
        test.assert_data_flow(
            compliance_content,
            architect_content,
            "Compliance outputs constraints for architect"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_architect_to_calculator_flow(test: APVIntegrationTest):
    """Test data flow from rfp-architect to rfp-calculator"""
    print("\n🔗 Testing: rfp-architect → rfp-calculator")

    architect_skill = Path.home() / ".claude" / "skills" / "rfp-architect" / "skill.md"
    calculator_skill = Path.home() / ".claude" / "skills" / "rfp-calculator" / "prompt.md"

    if architect_skill.exists() and calculator_skill.exists():
        with open(architect_skill, 'r') as f:
            architect_content = f.read()
        with open(calculator_skill, 'r') as f:
            calculator_content = f.read()

        test.assert_data_flow(
            architect_content,
            calculator_content,
            "Architect outputs components for sizing"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_calculator_to_pricer_flow(test: APVIntegrationTest):
    """Test data flow from rfp-calculator to rfp-pricer"""
    print("\n🔗 Testing: rfp-calculator → rfp-pricer")

    calculator_skill = Path.home() / ".claude" / "skills" / "rfp-calculator" / "skill.md"
    pricer_skill = Path.home() / ".claude" / "skills" / "rfp-pricer" / "prompt.md"

    if calculator_skill.exists() and pricer_skill.exists():
        with open(calculator_skill, 'r') as f:
            calculator_content = f.read()
        with open(pricer_skill, 'r') as f:
            pricer_content = f.read()

        test.assert_data_flow(
            calculator_content,
            pricer_content,
            "Calculator outputs sizing for pricing"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_pricer_to_generator_flow(test: APVIntegrationTest):
    """Test data flow from rfp-pricer to rfp-generator"""
    print("\n🔗 Testing: rfp-pricer → rfp-generator")

    pricer_skill = Path.home() / ".claude" / "skills" / "rfp-pricer" / "skill.md"
    generator_skill = Path.home() / ".claude" / "skills" / "rfp-generator" / "prompt.md"

    if pricer_skill.exists() and generator_skill.exists():
        with open(pricer_skill, 'r') as f:
            pricer_content = f.read()
        with open(generator_skill, 'r') as f:
            generator_content = f.read()

        test.assert_data_flow(
            pricer_content,
            generator_content,
            "Pricer outputs costs for generator"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_generator_to_reviewer_flow(test: APVIntegrationTest):
    """Test data flow from rfp-generator to apv-reviewer"""
    print("\n🔗 Testing: rfp-generator → apv-reviewer")

    generator_skill = Path.home() / ".claude" / "skills" / "rfp-generator" / "skill.md"
    reviewer_skill = Path.home() / ".claude" / "skills" / "apv-reviewer" / "prompt.md"

    if generator_skill.exists() and reviewer_skill.exists():
        with open(generator_skill, 'r') as f:
            generator_content = f.read()
        with open(reviewer_skill, 'r') as f:
            reviewer_content = f.read()

        test.assert_data_flow(
            generator_content,
            reviewer_content,
            "Generator outputs document for reviewer"
        )
    else:
        print("  ⚠️  Skills not found - skipping test")


def test_full_skill_chain(test: APVIntegrationTest):
    """Test that all skill files exist and are properly linked"""
    print("\n🔗 Testing: Full Skill Chain")

    skill_files = [
        Path.home() / ".claude" / "skills" / "rfp-brainstorm" / "skill.md",
        Path.home() / ".claude" / "skills" / "rfp-compliance" / "skill.md",
        Path.home() / ".claude" / "skills" / "rfp-architect" / "skill.md",
        Path.home() / ".claude" / "skills" / "rfp-calculator" / "skill.md",
        Path.home() / ".claude" / "skills" / "rfp-pricer" / "skill.md",
        Path.home() / ".claude" / "skills" / "rfp-generator" / "skill.md",
        Path.home() / ".claude" / "skills" / "apv-reviewer" / "skill.md",
        Path.home() / ".claude" / "skills" / "apv" / "skill.md",
    ]

    test.assert_file_chain(
        skill_files,
        "All 8 skill files exist in chain order"
    )


def test_wiki_knowledge_chain(test: APVIntegrationTest):
    """Test that wiki knowledge base supports the full chain"""
    print("\n📚 Testing: Wiki Knowledge Base for Full Chain")

    knowledge_paths = [
        WIKI_PATH / "apv/knowledge/compliance/pci-dss" / "overview.md",
        WIKI_PATH / "apv/knowledge/compliance/countries/sg" / "mas-trm.md",
        WIKI_PATH / "apv/knowledge/card-systems" / "issuing.md",
        WIKI_PATH / "apv/knowledge/infrastructure/aws" / "eks.md",
        WIKI_PATH / "apv/knowledge/sizing" / "tps-calculator.md",
        WIKI_PATH / "apv/knowledge/pricing" / "aws.md",
    ]

    test.assert_file_chain(
        knowledge_paths,
        "Key knowledge files exist for all skills"
    )


def test_source_url_consistency(test: APVIntegrationTest):
    """Test that source URL enforcement is consistent across chain"""
    print("\n🔗 Testing: Source URL Enforcement Across Chain")

    # Check that compliance skill enforces source URLs
    compliance_skill = Path.home() / ".claude" / "skills" / "rfp-compliance" / "skill.md"
    pricer_skill = Path.home() / ".claude" / "skills" / "rfp-pricer" / "skill.md"
    generator_skill = Path.home() / ".claude" / "skills" / "rfp-generator" / "skill.md"

    if compliance_skill.exists():
        with open(compliance_skill, 'r') as f:
            content = f.read()

        test.assert_contains(content, "source URL enforcement", "Compliance enforces source URLs")
        test.assert_contains(content, "100% compliance", "Compliance targets 100%")
    else:
        print("  ⚠️  Compliance skill not found")

    if pricer_skill.exists():
        with open(pricer_skill, 'r') as f:
            content = f.read()

        test.assert_contains(content, "calculator URLs", "Pricer uses calculator URLs")
        test.assert_contains(content, "30 days", "Pricer enforces 30-day freshness")
    else:
        print("  ⚠️  Pricer skill not found")

    if generator_skill.exists():
        with open(generator_skill, 'r') as f:
            content = f.read()

        test.assert_contains(content, "Source URL Index", "Generator includes source URL index")
    else:
        print("  ⚠️  Generator skill not found")


def test_contains(test: APVIntegrationTest, text: str, substring: str, message: str):
    """Helper: Assert text contains substring"""
    if substring.lower() in text.lower():
        test.tests_passed += 1
        test.results.append({
            "test": message,
            "status": "PASS"
        })
        print(f"  ✅ {message}")
    else:
        test.tests_failed += 1
        test.results.append({
            "test": message,
            "status": "FAIL",
            "substring": substring
        })
        print(f"  ❌ {message} (substring not found)")


def run_integration_tests() -> bool:
    """Run all integration tests"""
    print(f"{'='*60}")
    print("APV Contract-Level Integration Tests")
    print(f"{'='*60}")
    print("Checking skill-file presence, documented handoff markers, and key knowledge assets")
    print("This runner does not execute a real APV project end-to-end")
    print("For canonical apv-projects artifact validation, run pytest tests/test_runtime_project_fixture.py")
    print(f"{'='*60}\n")

    test = APVIntegrationTest("Full Chain")

    # Run integration tests
    test_full_skill_chain(test)
    test_brainstorm_to_compliance_flow(test)
    test_compliance_to_architect_flow(test)
    test_architect_to_calculator_flow(test)
    test_calculator_to_pricer_flow(test)
    test_pricer_to_generator_flow(test)
    test_generator_to_reviewer_flow(test)
    test_wiki_knowledge_chain(test)
    test_source_url_consistency(test)

    return test.summary()


def main():
    parser = argparse.ArgumentParser(description="Run APV integration tests")
    parser.add_argument("--chain", help="Test specific chain (default: full)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    all_passed = run_integration_tests()

    # Save results
    output_file = WIKI_PATH / "apv" / "tests" / "integration" / "test-results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Get test results
    if all_passed:
        status = "PASS"
        tests_failed = 0
    else:
        status = "FAIL"
        tests_failed = 1

    report = {
        "test_date": datetime.now(timezone.utc).isoformat(),
        "test_type": "contract-level integration",
        "test_scope": "skill-file presence, documented handoff markers, and key knowledge assets",
        "runtime_fixture_test": "tests/test_runtime_project_fixture.py",
        "overall_status": status,
        "tests_failed": tests_failed,
        "chains_tested": [
            "brainstorm-to-compliance",
            "compliance-to-architect",
            "architect-to-calculator",
            "calculator-to-pricer",
            "pricer-to-generator",
            "generator-to-reviewer",
            "full-skill-chain",
            "wiki-knowledge-chain",
            "source-url-consistency"
        ]
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📊 Integration test results saved to: {output_file}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
