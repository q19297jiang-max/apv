#!/usr/bin/env python3
"""
APV Source URL Verification System - Unit Tests

Tests for verify-source-urls.py and check-freshness.py

Usage:
    python test-url-verification.py
    python test-url-verification.py --verbose
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import urllib.request
from datetime import datetime, timedelta

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))


class TestURLVerifier(unittest.TestCase):
    """Unit tests for URL verification functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Import directly from the module file (handles dashes in filename)
        import importlib.util
        spec = importlib.util.spec_from_file_location("verify_source_urls", str(Path(__file__).parent.parent / 'tools' / 'verify-source-urls.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.URLVerifier = module.URLVerifier
        self.verifier = self.URLVerifier(strict_mode=True)

    def test_is_valid_url_well_formed(self):
        """Test that well-formed URLs are recognized as valid."""
        valid_urls = [
            'https://pcisecuritystandards.org',
            'https://mas.gov.sg/regulations',
            'https://aws.amazon.com/pricing/',
            'http://example.com/path?query=value',
        ]
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(self.verifier.is_valid_url(url))

    def test_is_valid_url_malformed(self):
        """Test that malformed URLs are rejected."""
        invalid_urls = [
            'not-a-url',
            'htp://missing-protocol-slash',
            '://missing-protocol',
            'javascript:alert(1)',  # Javascript protocol
            'ftp://server/file',  # Non-HTTP protocol
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(self.verifier.is_valid_url(url))

    def test_trusted_domain_pci_dss(self):
        """Test that PCI-DSS official domain is trusted."""
        pci_urls = [
            'https://pcisecuritystandards.org/documents/PCI_DSS_v4-0.pdf',
            'https://www.pcisecuritystandards.org/',
        ]
        for url in pci_urls:
            with self.subTest(url=url):
                self.assertTrue(self.verifier.is_trusted_domain(url))

    def test_trusted_domain_singapore(self):
        """Test that Singapore regulator domains are trusted."""
        sg_urls = [
            'https://mas.gov.sg/regulations',
            'https://www.mas.gov.sg/',
            'https://imda.gov.sg/',
            'https://pdpc.gov.sg/',
        ]
        for url in sg_urls:
            with self.subTest(url=url):
                self.assertTrue(self.verifier.is_trusted_domain(url))

    def test_trusted_domain_malaysia(self):
        """Test that Malaysia regulator domains are trusted."""
        my_urls = [
            'https://bnm.gov.my/',
            'https://www.bnm.gov.my/regulations',
            'https://pdp.gov.my/',
        ]
        for url in my_urls:
            with self.subTest(url=url):
                self.assertTrue(self.verifier.is_trusted_domain(url))

    def test_trusted_domain_pricing_calculators(self):
        """Test that pricing calculator domains are trusted."""
        pricing_urls = [
            'https://calculator.aws/',
            'https://aws.amazon.com/pricing/',
            'https://azure.microsoft.com/pricing/',
            'https://cloud.google.com/products/calculator',
        ]
        for url in pricing_urls:
            with self.subTest(url=url):
                self.assertTrue(self.verifier.is_trusted_domain(url))

    def test_untrusted_domain(self):
        """Test that unknown domains are not trusted in strict mode."""
        untrusted_urls = [
            'https://example.com/',
            'https://unknown-regulator.gov/',
            'https://blog.example.com/post',
        ]
        for url in untrusted_urls:
            with self.subTest(url=url):
                self.assertFalse(self.verifier.is_trusted_domain(url))

    def test_extract_urls_from_markdown_links(self):
        """Test extraction of URLs from markdown link format."""
        # Create temporary test file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('This is a [PCI-DSS link](https://pcisecuritystandards.org/).\n')
            f.write('And another [MAS link](https://mas.gov.sg/).\n')
            test_file = Path(f.name)

        try:
            urls = self.verifier.extract_urls_from_file(test_file)
            self.assertEqual(len(urls), 2)
            self.assertIn(('https://pcisecuritystandards.org/', 1, 'link: PCI-DSS link'), urls)
            self.assertIn(('https://mas.gov.sg/', 2, 'link: MAS link'), urls)
        finally:
            test_file.unlink()

    def test_extract_urls_from_source_list(self):
        """Test extraction of URLs from source list format."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('Sources:\n')
            f.write('- source: "https://pcisecuritystandards.org/"\n')
            f.write('  - url: https://mas.gov.sg/\n')
            test_file = Path(f.name)

        try:
            urls = self.verifier.extract_urls_from_file(test_file)
            self.assertGreater(len(urls), 0)
            urls_only = [u[0] for u in urls]
            self.assertIn('https://pcisecuritystandards.org/', urls_only)
        finally:
            test_file.unlink()


class TestFreshnessChecker(unittest.TestCase):
    """Unit tests for URL freshness checking functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Import directly from the module file (handles dashes in filename)
        import importlib.util
        spec = importlib.util.spec_from_file_location("check_freshness", str(Path(__file__).parent.parent / 'tools' / 'check-freshness.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.FreshnessChecker = module.FreshnessChecker
        self.checker = self.FreshnessChecker(strict_mode=True)

    def test_detect_url_type_pricing(self):
        """Test detection of pricing-related URLs."""
        pricing_urls = [
            ('https://aws.amazon.com/pricing/', 'link: pricing'),
            ('https://calculator.aws/', 'calculator'),
            ('https://azure.microsoft.com/en-us/pricing/', ''),
        ]
        for url, context in pricing_urls:
            with self.subTest(url=url):
                url_type = self.checker.detect_url_type(url, context)
                self.assertIn(url_type, ['pricing', 'calculator'])

    def test_detect_url_type_compliance(self):
        """Test detection of compliance-related URLs."""
        compliance_urls = [
            ('https://pcisecuritystandards.org/', 'PCI-DSS'),
            ('https://mas.gov.sg/regulations', 'MAS regulation'),
            ('https://bnm.gov.my/', 'compliance'),
        ]
        for url, context in compliance_urls:
            with self.subTest(url=url):
                url_type = self.checker.detect_url_type(url, context)
                self.assertEqual(url_type, 'compliance')

    def test_detect_url_type_general(self):
        """Test detection of general URLs."""
        general_urls = [
            ('https://example.com/page', ''),
            ('https://unknown.org/article', 'general info'),
        ]
        for url, context in general_urls:
            with self.subTest(url=url):
                url_type = self.checker.detect_url_type(url, context)
                self.assertEqual(url_type, 'general')

    def test_freshness_limits(self):
        """Test that correct freshness limits are applied."""
        self.assertEqual(self.checker.get_freshness_limit('pricing'), 30)
        self.assertEqual(self.checker.get_freshness_limit('compliance'), 365)
        self.assertEqual(self.checker.get_freshness_limit('calculator'), 30)
        self.assertEqual(self.checker.get_freshness_limit('general'), 180)


class TestFreshnessCalculation(unittest.TestCase):
    """Tests for freshness age calculation."""

    def setUp(self):
        """Set up test fixtures."""
        # Import directly from the module file (handles dashes in filename)
        import importlib.util
        spec = importlib.util.spec_from_file_location("check_freshness", str(Path(__file__).parent.parent / 'tools' / 'check-freshness.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.FreshnessChecker = module.FreshnessChecker
        self.checker = self.FreshnessChecker(strict_mode=True)

    def test_fresh_pricing_url(self):
        """Test that a recently updated pricing URL is considered fresh."""
        # Pricing URLs: must be < 30 days old
        recent_date = datetime.now() - timedelta(days=15)
        days_old = 15
        self.assertLess(days_old, self.checker.get_freshness_limit('pricing'))

    def test_stale_pricing_url(self):
        """Test that an old pricing URL is considered stale."""
        # Pricing URLs: must be < 30 days old
        old_date = datetime.now() - timedelta(days=45)
        days_old = 45
        self.assertGreater(days_old, self.checker.get_freshness_limit('pricing'))

    def test_fresh_compliance_url(self):
        """Test that a recent compliance URL is considered fresh."""
        # Compliance URLs: must be < 365 days old
        recent_date = datetime.now() - timedelta(days=100)
        days_old = 100
        self.assertLess(days_old, self.checker.get_freshness_limit('compliance'))

    def test_stale_compliance_url(self):
        """Test that an old compliance URL is considered stale."""
        # Compliance URLs: must be < 365 days old
        old_date = datetime.now() - timedelta(days=400)
        days_old = 400
        self.assertGreater(days_old, self.checker.get_freshness_limit('compliance'))

    def test_warning_threshold_pricing(self):
        """Test warning threshold for pricing URLs."""
        # Warning at 80% of limit: 0.8 * 30 = 24 days
        warning_days = 25
        limit = self.checker.get_freshness_limit('pricing')
        self.assertGreater(warning_days, limit * 0.8)
        self.assertLess(warning_days, limit)


class TestIntegration(unittest.TestCase):
    """Integration tests for URL verification system."""

    def test_end_to_end_verification_workflow(self):
        """Test complete workflow from file scanning to report generation."""
        import tempfile
        import importlib.util
        spec = importlib.util.spec_from_file_location("verify_source_urls", str(Path(__file__).parent.parent / 'tools' / 'verify-source-urls.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        URLVerifier = module.URLVerifier

        # Create test file with various URLs
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('# Test Compliance File\n\n')
            f.write('## PCI-DSS Requirements\n')
            f.write('See [PCI-DSS v4.0](https://pcisecuritystandards.org/documents/PCI_DSS_v4-0.pdf) for details.\n\n')
            f.write('## Pricing\n')
            f.write('Calculator: https://calculator.aws/\n')
            test_file = Path(f.name)

        try:
            verifier = URLVerifier(strict_mode=False)  # Don't check actual accessibility in tests
            result = verifier.scan_file(test_file)

            self.assertEqual(result['file'], str(test_file))
            self.assertGreater(result['urls_found'], 0)
            self.assertIsInstance(result['results'], list)

        finally:
            test_file.unlink()

    def test_freshness_check_workflow(self):
        """Test complete freshness checking workflow."""
        import tempfile
        import importlib.util
        spec = importlib.util.spec_from_file_location("check_freshness", str(Path(__file__).parent.parent / 'tools' / 'check-freshness.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        FreshnessChecker = module.FreshnessChecker

        # Create test file with URLs
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('# Pricing Information\n\n')
            f.write('AWS Calculator: https://calculator.aws/\n')
            test_file = Path(f.name)

        try:
            checker = FreshnessChecker(strict_mode=False)
            result = checker.scan_file(test_file)

            self.assertEqual(result['file'], str(test_file))
            self.assertGreater(result['urls_found'], 0)

        finally:
            test_file.unlink()


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestURLVerifier))
    suite.addTests(loader.loadTestsFromTestCase(TestFreshnessChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestFreshnessCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("APV SOURCE URL VERIFICATION - TEST SUMMARY")
    print("="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
