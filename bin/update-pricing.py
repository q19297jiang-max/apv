#!/usr/bin/env python3
"""
APV Pricing Knowledge Base Updater

UPGRADE NOTICE: This script now orchestrates the 4-step pricing update workflow:

Step 0: pricing-api-fetcher.py - Fetch from AWS Pricing API (NEW)
Step 1: pricing-fetcher.py     - Generate summary from catalog
Step 2: pricing-verify.py      - Interactive verification
Step 3: pricing-commit.py      - Commit to knowledge base

Or use this script for automated execution of all steps.

Usage:
    python update-pricing.py --provider aws                # Full workflow
    python update-pricing.py --provider aws --auto         # Auto-mode with API fetch
    python update-pricing.py --provider aws --step 1       # Run specific step
    python update-pricing.py --all                         # Update all providers

Files updated:
    - wiki/apv/knowledge/pricing/aws-component-catalog.md (Step 0)
    - wiki/apv/knowledge/pricing/aws.md                   (Step 3)
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Script paths
BIN_DIR = Path(__file__).parent
API_FETCHER_SCRIPT = BIN_DIR / 'pricing-api-fetcher.py'
FETCHER_SCRIPT = BIN_DIR / 'pricing-fetcher.py'
VERIFY_SCRIPT = BIN_DIR / 'pricing-verify.py'
COMMIT_SCRIPT = BIN_DIR / 'pricing-commit.py'

# Temp and evidence directories
TEMP_DIR = Path('/tmp/apv-pricing-updates')
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')


def run_step(script: Path, provider: str, step_name: str, extra_args: list = None) -> bool:
    """Run a single step in the workflow"""
    print()
    print("=" * 70)
    print(f"STEP: {step_name}")
    print("=" * 70)
    print()

    try:
        cmd = [sys.executable, str(script), '--provider', provider]
        if extra_args:
            cmd.extend(extra_args)

        result = subprocess.run(
            cmd,
            check=False,
            cwd=BIN_DIR
        )

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running {step_name}: {e}")
        return False


def run_full_workflow(provider: str, auto_mode: bool = False) -> bool:
    """Run the complete 4-step workflow"""
    workflow_type = "AUTOMATED (API-FETCH)" if auto_mode else "INTERACTIVE"

    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     APV PRICING UPDATE WORKFLOW: {provider.upper():<4} [{workflow_type}]           ║
║                                                                          ║
║  This will update the pricing knowledge base for {provider.upper():<4}              ║
║                                                                          ║
║  Steps:                                                                   ║
║    0. Fetch from AWS Pricing API (update component catalog)              ║
║    1. Generate summary from component catalog                            ║
║    2. Verify pricing against official calculators                         ║
║    3. Commit verified pricing to knowledge base                           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    response = input("Continue? [Y]es [N]o: ").strip().upper()
    if response != 'Y':
        print("Cancelled.")
        return False

    # Step 0: API Fetch (if auto-mode)
    if auto_mode and provider == 'aws':
        if not run_step(API_FETCHER_SCRIPT, provider, "FETCH FROM AWS PRICING API", ['--verify']):
            print()
            print("⚠️  API fetch failed. Continue with manual mode?")
            response = input("Continue? [Y]es [N]o: ").strip().upper()
            if response != 'Y':
                print("Cancelled.")
                return False

    # Step 1: Generate summary from catalog
    if not run_step(FETCHER_SCRIPT, provider, "GENERATE SUMMARY FROM CATALOG"):
        print("❌ Fetch failed. Aborting.")
        return False

    # Step 2: Verify
    if not run_step(VERIFY_SCRIPT, provider, "VERIFY PRICING"):
        print()
        print("⚠️  Verification failed or incomplete.")
        response = input("Commit anyway? [Y]es [N]o: ").strip().upper()
        if response != 'Y':
            print("Cancelled.")
            return False

    # Step 3: Commit
    if not run_step(COMMIT_SCRIPT, provider, "COMMIT PRICING"):
        print("❌ Commit failed.")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Update APV pricing knowledge base (orchestrates API fetch/generate/verify/commit)',
        epilog="""
Examples:
  python update-pricing.py --provider aws                # Full workflow
  python update-pricing.py --provider aws --auto         # Auto-mode with API fetch
  python update-pricing.py --provider aws --step 1       # Run specific step
  python update-pricing.py --all                         # Update all providers

Individual Scripts:
  python pricing-api-fetcher.py --provider aws --verify  # Step 0: Fetch from AWS API
  python pricing-fetcher.py --provider aws               # Step 1: Generate from catalog
  python pricing-verify.py --provider aws                # Step 2: Interactive verify
  python pricing-commit.py --provider aws                # Step 3: Commit to KB

Workflow:
  0. API Fetch → Updates component catalog from AWS API
  1. Generate  → Creates summary from component catalog
  2. Verify   → Interactive verification against calculators
  3. Commit   → Writes to wiki/apv/knowledge/pricing/
        """
    )
    parser.add_argument('--provider', choices=['aws', 'azure', 'gcp'],
                        help='Cloud provider')
    parser.add_argument('--all', action='store_true',
                        help='Update all providers')
    parser.add_argument('--auto', action='store_true',
                        help='Auto-mode: fetch from AWS Pricing API first')
    parser.add_argument('--step', type=int, choices=[0, 1, 2, 3],
                        help='Run specific step only (0=API fetch, 1=generate, 2=verify, 3=commit)')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else ['aws', 'azure', 'gcp']

    print("=" * 70)
    print("APV PRICING KNOWLEDGE BASE UPDATER")
    print("=" * 70)
    print()

    all_passed = True
    for provider in providers:
        if args.step is not None:
            # Run specific step only
            if args.step == 0:
                script = API_FETCHER_SCRIPT
                step_name = "FETCH FROM AWS PRICING API"
                extra_args = ['--verify']
            elif args.step == 1:
                script = FETCHER_SCRIPT
                step_name = "GENERATE SUMMARY FROM CATALOG"
                extra_args = None
            elif args.step == 2:
                script = VERIFY_SCRIPT
                step_name = "VERIFY PRICING"
                extra_args = None
            else:  # args.step == 3
                script = COMMIT_SCRIPT
                step_name = "COMMIT PRICING"
                extra_args = None

            if not run_step(script, provider, step_name, extra_args):
                all_passed = False
        else:
            # Run full workflow
            if not run_full_workflow(provider, auto_mode=args.auto):
                all_passed = False

        print()

    if all_passed:
        print("=" * 70)
        print("✅ PRICING UPDATE COMPLETE")
        print("=" * 70)
        print()
        print("Updated Files:")
        print("  - wiki/apv/knowledge/pricing/aws-component-catalog.md (if auto-mode)")
        print("  - wiki/apv/knowledge/pricing/aws.md")
        print()
        print("Next Steps:")
        print("  1. Review updated pricing in wiki/apv/knowledge/pricing/")
        print("  2. Run freshness check: python check-freshness.py wiki/apv/knowledge/pricing/")
        print("  3. Commit changes to git if satisfied")
        print()
        sys.exit(0)
    else:
        print("=" * 70)
        print("⚠️  SOME UPDATES FAILED")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
