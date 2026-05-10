"""Tests for the APV orchestrator entrypoint."""

import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import apv as apv_module
from create_snapshot import create_project_snapshot
from apv import (
    add_pricing_item,
    create_new_project,
    extend_pricing_family,
    format_cli_output,
    promote_to_submission,
    refresh_pricing_knowledge,
    route_knowledge_change,
    resume_project,
    run_pipeline,
    run_stage,
    validate_release_readiness,
    validate_sales_brief,
)
from aws_kb_pricing import write_aws_pricing_knowledge

FIXTURES = Path(__file__).parent / "fixtures"


def _offer_payload(
    instance_type: str,
    price: str,
    *,
    instance_key: str = "instanceType",
    extra_attributes: dict | None = None,
) -> dict:
    attributes = {
        instance_key: instance_type,
        "operatingSystem": "Linux",
        "preInstalledSw": "NA",
        "tenancy": "Shared",
        "capacitystatus": "Used",
    }
    if extra_attributes:
        attributes.update(extra_attributes)
    return {
        "products": {
            "SKU123": {
                "sku": "SKU123",
                "attributes": attributes,
            }
        },
        "terms": {
            "OnDemand": {
                "SKU123": {
                    "SKU123.TERM": {
                        "priceDimensions": {
                            "SKU123.TERM.DIM": {"pricePerUnit": {"USD": price}}
                        }
                    }
                }
            }
        },
    }


def _default_public_offer_payloads() -> dict[str, dict]:
    return {
        "EC2": _offer_payload("m6i.large", "0.096"),
        "RDS": _offer_payload("db.m6i.large", "0.188"),
        "ElastiCache": _offer_payload("cache.r6g.large", "0.208", instance_key="cacheNodeType"),
        "CloudHSM": _offer_payload("hsm2.medium", "1.86", instance_key="hsmGeneration"),
    }


def test_bin_apv_help_smoke():
    repo_root = Path(__file__).resolve().parent.parent

    completed = subprocess.run(
        [str(repo_root / "bin" / "apv"), "--help"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "APV V2 orchestrator entrypoint" in completed.stdout
    assert "refresh-pricing" in completed.stdout


def test_bin_apv_new_uses_repo_defaults_for_base_and_knowledge_dirs(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    title = f"defaults {tmp_path.name}"
    title_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    project_dir = repo_root / "apv-projects" / f"demo--{title_slug}--{date.today().isoformat()}"
    if project_dir.exists():
        import shutil

        shutil.rmtree(project_dir)

    completed = subprocess.run(
        [
            str(repo_root / "bin" / "apv"),
            "new",
            "demo",
            title,
            "--raw-dir",
            str(FIXTURES / "raw"),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert project_dir.exists()


def test_bin_apv_promote_to_submission_updates_project_governance_state(tmp_path):
    repo_root = Path(__file__).resolve().parent.parent
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    completed = subprocess.run(
        [
            str(repo_root / "bin" / "apv"),
            "promote-to-submission",
            "--project",
            str(project_dir),
            "--owner",
            "Jane Smith",
            "--strategy",
            "Lead with compliance and low implementation risk",
            "--constraint",
            "Keep baseline under 20k/month",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert (project_dir / "input" / "normalized" / "sales-brief.md").exists()
    run_context = json.loads((project_dir / "working" / "00-run-context.json").read_text(encoding="utf-8"))
    assert run_context["mode"] == "submission"
    assert run_context["promotion_path"] == "full-rerun"


def test_bin_apv_prefers_parent_workspace_venv_when_repo_venv_missing(tmp_path):
    workspace_root = tmp_path / "workspace"
    repo_root = workspace_root / "apv-v2"
    bin_dir = repo_root / "bin"
    tools_dir = repo_root / "tools"
    parent_venv_python = workspace_root / ".venv" / "bin" / "python"

    bin_dir.mkdir(parents=True)
    tools_dir.mkdir(parents=True)
    parent_venv_python.parent.mkdir(parents=True)

    source_wrapper = (Path(__file__).resolve().parent.parent / "bin" / "apv").read_text(encoding="utf-8")
    (bin_dir / "apv").write_text(source_wrapper, encoding="utf-8")
    (bin_dir / "apv").chmod(0o755)

    (tools_dir / "apv.py").write_text(
        "import sys\nprint(sys.executable)\n",
        encoding="utf-8",
    )
    parent_venv_python.write_text(
        "#!/usr/bin/env bash\nprintf '%s\\n' \"$0\"\n",
        encoding="utf-8",
    )
    parent_venv_python.chmod(0o755)

    completed = subprocess.run(
        [str(bin_dir / "apv")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == str(parent_venv_python)


def test_format_cli_output_for_add_item_duplicate_is_human_readable():
    output = format_cli_output(
        command="pricing",
        pricing_command="add-item",
        result={
            "pass": True,
            "provider": "aws",
            "manifest_path": "knowledge/pricing/aws-pricing-manifest.json",
            "entry_kind": "public-offer",
            "added": False,
            "added_savings_plan_rows": [],
        },
    )

    assert "Pricing item already exists in the manifest." in output
    assert "Manifest: knowledge/pricing/aws-pricing-manifest.json" in output


def test_format_cli_output_for_refresh_pricing_summarizes_generation_sync_and_freshness():
    output = format_cli_output(
        command="refresh-pricing",
        pricing_command=None,
        result={
            "pass": True,
            "provider": "aws",
            "region": "ap-southeast-1",
            "refresh": {
                "pass": True,
                "generated_rows": 19,
                "verification_summary": {"public-offer": 3, "formula": 4, "official-page": 12},
            },
            "sync": {"indexed": 57, "errors": 0},
            "freshness": {"stale": 0},
        },
    )

    assert "AWS pricing refresh succeeded for ap-southeast-1." in output
    assert "Generated rows: 19" in output
    assert "Verification mix: public-offer=3, formula=4, official-page=12" in output
    assert "Indexed files: 57" in output
    assert "Stale pricing pages: 0" in output


def test_refresh_pricing_knowledge_runs_refresh_sync_and_freshness(tmp_path, monkeypatch):
    knowledge_dir = tmp_path / "knowledge"
    db_path = tmp_path / "apv-v2.sqlite"

    calls = {"refresh": None, "sync": None, "freshness": None}

    def _fake_refresh(knowledge_dir: Path, region: str = "ap-southeast-1") -> dict:
        calls["refresh"] = {"knowledge_dir": knowledge_dir, "region": region}
        return {
            "pass": True,
            "catalog_path": knowledge_dir / "pricing" / "aws-component-catalog.md",
            "view_path": knowledge_dir / "pricing" / "aws.md",
            "report_path": knowledge_dir / "pricing" / "aws-component-catalog.report.json",
            "generated_rows": 18,
        }

    def _fake_sync(knowledge_dir: Path, db_path: Path) -> dict:
        calls["sync"] = {"knowledge_dir": knowledge_dir, "db_path": db_path}
        return {"total": 3, "indexed": 3, "warnings": 0, "errors": 0}

    def _fake_domain_freshness(db_path: Path, domain: str) -> dict:
        calls["freshness"] = {"db_path": db_path, "domain": domain}
        return {"total_pages": 3, "fresh": 3, "stale": 0, "stale_pages": []}

    monkeypatch.setattr("apv.refresh_aws_pricing", _fake_refresh)
    monkeypatch.setattr("apv.sync_knowledge", _fake_sync)
    monkeypatch.setattr("apv.check_domain_freshness", _fake_domain_freshness)

    result = refresh_pricing_knowledge(
        provider="aws",
        knowledge_dir=knowledge_dir,
        region="ap-southeast-1",
        db_path=db_path,
        sync=True,
        check_freshness=True,
    )

    assert result["pass"] is True
    assert result["refresh"]["generated_rows"] == 18
    assert result["sync"]["indexed"] == 3
    assert result["freshness"]["stale"] == 0
    assert calls["refresh"] == {"knowledge_dir": knowledge_dir, "region": "ap-southeast-1"}
    assert calls["sync"] == {"knowledge_dir": knowledge_dir, "db_path": db_path}
    assert calls["freshness"] == {"db_path": db_path, "domain": "pricing"}


def test_route_knowledge_change_blocks_direct_edits_to_generated_pricing_catalog(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    payloads = _default_public_offer_payloads()
    write_aws_pricing_knowledge(knowledge_dir, offer_loader=lambda service, region: payloads[service])

    result = route_knowledge_change(
        target_path=knowledge_dir / "pricing" / "aws-component-catalog.md",
        knowledge_dir=knowledge_dir,
    )

    assert result["pass"] is True
    assert result["allowed"] is False
    assert result["source_of_truth"] == knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    assert result["regenerate_command"] == "./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness"
    assert any("Direct edits are blocked" in issue for issue in result["issues"])


def test_format_cli_output_for_knowledge_route_change_is_human_readable():
    output = format_cli_output(
        command="knowledge",
        pricing_command="route-change",
        result={
            "pass": True,
            "allowed": False,
            "target_path": "knowledge/pricing/aws-component-catalog.md",
            "source_of_truth": "knowledge/pricing/aws-pricing-manifest.json",
            "regenerate_command": "./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness",
            "issues": ["Direct edits are blocked for generated knowledge files."],
        },
    )

    assert "Direct edit blocked for generated knowledge file." in output
    assert "Target: knowledge/pricing/aws-component-catalog.md" in output
    assert "Source of truth: knowledge/pricing/aws-pricing-manifest.json" in output
    assert "Regenerate with: ./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness" in output


def test_add_pricing_item_updates_manifest_without_editing_python(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    payload = _offer_payload("m6i.xlarge", "0.192")

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="EC2",
        instance_type="m6i.xlarge",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert any(
        row["service"] == "EC2" and row["instance_type"] == "m6i.xlarge"
        for row in payload["public_offer_rows"]
    )


def test_add_pricing_item_auto_adds_matching_savings_plan_rows_for_ec2(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    payload = _offer_payload("m6i.xlarge", "0.192")

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="EC2",
        instance_type="m6i.xlarge",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert "m6i.xlarge" in result["added_savings_plan_rows"]
    assert any(
        row["service"] == "EC2"
        and row["instance_type"] == "m6i.xlarge"
        and row["pricing_model"] == "savings-plans"
        for row in payload["formula_rows"]
    )


def test_add_pricing_item_normalizes_friendly_rds_aliases(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "instanceType": "db.m6i.xlarge",
                }
            }
        },
        "terms": {
            "OnDemand": {
                "SKU1": {
                    "TERM1": {
                        "priceDimensions": {
                            "DIM1": {"pricePerUnit": {"USD": "0.376"}}
                        }
                    }
                }
            }
        },
    }

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="postgresql/rds",
        instance_type="db.m6i.xlarge",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "RDS"
    assert result["entry_kind"] == "public-offer"
    assert any(
        row["service"] == "RDS" and row["instance_type"] == "db.m6i.xlarge"
        for row in payload["public_offer_rows"]
    )


def test_add_pricing_item_auto_adds_matching_savings_plan_rows_for_rds(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "instanceType": "db.m6i.xlarge",
                }
            }
        },
        "terms": {
            "OnDemand": {
                "SKU1": {
                    "TERM1": {
                        "priceDimensions": {
                            "DIM1": {"pricePerUnit": {"USD": "0.376"}}
                        }
                    }
                }
            }
        },
    }

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="postgresql/rds",
        instance_type="db.m6i.xlarge",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert "db.m6i.xlarge" in result["added_savings_plan_rows"]
    assert any(
        row["service"] == "RDS"
        and row["instance_type"] == "db.m6i.xlarge"
        and row["pricing_model"] == "savings-plans"
        for row in payload["formula_rows"]
    )


def test_add_pricing_item_treats_elasticache_component_as_public_offer_instance_type(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "cacheNodeType": "cache.m7g.large",
                }
            }
        },
        "terms": {
            "OnDemand": {
                "SKU1": {
                    "TERM1": {
                        "priceDimensions": {
                            "DIM1": {"pricePerUnit": {"USD": "0.312"}}
                        }
                    }
                }
            }
        },
    }

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="redis",
        component="cache.m7g.large",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "ElastiCache"
    assert result["entry_kind"] == "public-offer"
    assert any(
        row["service"] == "ElastiCache" and row["instance_type"] == "cache.m7g.large"
        for row in payload["public_offer_rows"]
    )


def test_add_pricing_item_auto_adds_matching_savings_plan_rows_for_elasticache(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "cacheNodeType": "cache.m7g.large",
                }
            }
        },
        "terms": {
            "OnDemand": {
                "SKU1": {
                    "TERM1": {
                        "priceDimensions": {
                            "DIM1": {"pricePerUnit": {"USD": "0.312"}}
                        }
                    }
                }
            }
        },
    }

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="redis",
        component="cache.m7g.large",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert "cache.m7g.large" in result["added_savings_plan_rows"]
    assert any(
        row["service"] == "ElastiCache"
        and row["instance_type"] == "cache.m7g.large"
        and row["pricing_model"] == "savings-plans"
        for row in payload["formula_rows"]
    )


def test_add_pricing_item_keeps_non_public_offer_static_services_on_official_static_path(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="waf",
        component="Web ACL",
        title="AWS WAF",
        source_url="https://aws.amazon.com/waf/pricing/",
        billing_unit="per Web ACL-month",
        unit_price=5.0,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "WAF"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "WAF" and row["component"] == "Web ACL"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_falls_back_to_known_static_defaults_for_elasticache_when_public_offer_is_missing(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="redis",
        component="cache.m7g.large",
        unit_price=0.312,
        region="ap-southeast-1",
        offer_loader=lambda service, region: {"products": {}, "terms": {"OnDemand": {}}},
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "ElastiCache"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "ElastiCache"
        and row["component"] == "cache.m7g.large"
        and row["billing_unit"] == "per node-hour"
        and row["source_url"] == "https://aws.amazon.com/elasticache/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_alb_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="alb",
        unit_price=0.0225,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "ALB"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "ALB"
        and row["component"] == "ALB Hourly"
        and row["billing_unit"] == "per ALB-hour"
        and row["source_url"] == "https://aws.amazon.com/elasticloadbalancing/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_guardduty_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="guardduty",
        unit_price=4.0,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "GuardDuty"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "GuardDuty"
        and row["component"] == "CloudTrail Management Events"
        and row["billing_unit"] == "per 1 million events"
        and row["source_url"] == "https://aws.amazon.com/guardduty/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_route53_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="route53",
        unit_price=0.5,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "Route 53"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "Route 53"
        and row["component"] == "Hosted Zone"
        and row["billing_unit"] == "per hosted zone-month"
        and row["source_url"] == "https://aws.amazon.com/route53/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_shield_advanced_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="shield-advanced",
        unit_price=3000.0,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "Shield Advanced"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "Shield Advanced"
        and row["component"] == "Subscription"
        and row["billing_unit"] == "per payer account-month"
        and row["source_url"] == "https://aws.amazon.com/shield/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_resolves_cloudwatch_component_aliases(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="cloudwatch",
        component="logs-ingest",
        unit_price=0.5,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "CloudWatch"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "CloudWatch"
        and row["component"] == "Logs Ingest"
        and row["billing_unit"] == "per GB ingested"
        and row["source_url"] == "https://aws.amazon.com/cloudwatch/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_resolves_nat_gateway_component_aliases(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="nat-gateway",
        component="data-processing",
        unit_price=0.045,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "NAT Gateway"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "NAT Gateway"
        and row["component"] == "Data Processing"
        and row["billing_unit"] == "per GB processed"
        and row["source_url"] == "https://aws.amazon.com/vpc/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_secrets_manager_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="secrets-manager",
        unit_price=0.4,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "Secrets Manager"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "Secrets Manager"
        and row["component"] == "Secret"
        and row["billing_unit"] == "per secret-month"
        and row["source_url"] == "https://aws.amazon.com/secrets-manager/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_sns_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="sns",
        unit_price=0.5,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "SNS"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "SNS"
        and row["component"] == "API Requests"
        and row["billing_unit"] == "per million requests"
        and row["source_url"] == "https://aws.amazon.com/sns/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_sqs_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="sqs",
        unit_price=0.4,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "SQS"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "SQS"
        and row["component"] == "Standard Requests"
        and row["billing_unit"] == "per million requests"
        and row["source_url"] == "https://aws.amazon.com/sqs/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_ecr_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="ecr",
        unit_price=0.1,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "ECR"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "ECR"
        and row["component"] == "Private Repository Storage"
        and row["billing_unit"] == "per GB-month"
        and row["source_url"] == "https://aws.amazon.com/ecr/pricing/"
        for row in payload["official_static_rows"]
    )


def test_add_pricing_item_infers_known_static_defaults_for_api_gateway_with_only_unit_price(tmp_path):
    knowledge_dir = tmp_path / "knowledge"

    result = add_pricing_item(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="api-gateway",
        unit_price=1.0,
        region="ap-southeast-1",
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "API Gateway"
    assert result["entry_kind"] == "official-static"
    assert any(
        row["service"] == "API Gateway"
        and row["component"] == "HTTP API Requests"
        and row["billing_unit"] == "per million requests"
        and row["source_url"] == "https://aws.amazon.com/api-gateway/pricing/"
        for row in payload["official_static_rows"]
    )


def test_extend_pricing_family_adds_matching_public_offer_items_and_savings_plan_variants(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    pricing_dir = knowledge_dir / "pricing"
    pricing_dir.mkdir(parents=True, exist_ok=True)
    (pricing_dir / "aws-pricing-manifest.json").write_text(
        json.dumps(
            {
                "supported_region": "ap-southeast-1",
                "public_offer_rows": [
                    {
                        "service": "EC2",
                        "instance_type": "m6i.large",
                        "family": "m6i",
                        "deployment_mode": "single",
                        "pricing_model": "on-demand",
                        "title": "EC2 Instances",
                    }
                ],
                "formula_rows": [
                    {
                        "service": "EC2",
                        "instance_type": "m6i.large",
                        "deployment_mode": "single",
                        "pricing_model": "savings-plans",
                        "title": "Compute Savings Plans (3yr No Upfront)",
                        "base_service": "EC2",
                        "base_instance_type": "m6i.large",
                        "base_pricing_model": "on-demand",
                        "discount": 0.36,
                        "source_class": "formula-derived",
                        "verification_mode": "formula",
                        "source_url": "https://calculator.aws/",
                        "derivation_basis": "m6i.large on-demand hourly x (1 - 0.36)",
                        "assumptions": "Savings Plans rate modeled from the established 3-year no-upfront discount pattern for m6i family in Singapore.",
                    }
                ],
                "official_static_rows": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "instanceType": "m6i.large",
                    "operatingSystem": "Linux",
                    "preInstalledSw": "NA",
                    "tenancy": "Shared",
                    "capacitystatus": "Used",
                }
            },
            "SKU2": {
                "attributes": {
                    "instanceType": "m6i.xlarge",
                    "operatingSystem": "Linux",
                    "preInstalledSw": "NA",
                    "tenancy": "Shared",
                    "capacitystatus": "Used",
                }
            },
            "SKU3": {
                "attributes": {
                    "instanceType": "m6i.2xlarge",
                    "operatingSystem": "Linux",
                    "preInstalledSw": "NA",
                    "tenancy": "Shared",
                    "capacitystatus": "Used",
                }
            },
        },
        "terms": {"OnDemand": {}},
    }

    result = extend_pricing_family(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="EC2",
        family="m6i",
        region="ap-southeast-1",
        with_savings_plans=True,
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    public_items = {
        row["instance_type"]
        for row in updated["public_offer_rows"]
        if row["service"] == "EC2"
    }
    savings_items = {
        row["instance_type"]
        for row in updated["formula_rows"]
        if row["service"] == "EC2" and row["pricing_model"] == "savings-plans"
    }

    assert result["pass"] is True
    assert {"m6i.large", "m6i.xlarge", "m6i.2xlarge"}.issubset(public_items)
    assert {"m6i.large", "m6i.xlarge", "m6i.2xlarge"}.issubset(savings_items)


def test_extend_pricing_family_auto_adds_matching_savings_plan_variants_without_flag(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    pricing_dir = knowledge_dir / "pricing"
    pricing_dir.mkdir(parents=True, exist_ok=True)
    (pricing_dir / "aws-pricing-manifest.json").write_text(
        json.dumps(
            {
                "supported_region": "ap-southeast-1",
                "public_offer_rows": [
                    {
                        "service": "EC2",
                        "instance_type": "m6i.large",
                        "family": "m6i",
                        "deployment_mode": "single",
                        "pricing_model": "on-demand",
                        "title": "EC2 Instances",
                    }
                ],
                "formula_rows": [
                    {
                        "service": "EC2",
                        "instance_type": "m6i.large",
                        "deployment_mode": "single",
                        "pricing_model": "savings-plans",
                        "title": "Compute Savings Plans (3yr No Upfront)",
                        "base_service": "EC2",
                        "base_instance_type": "m6i.large",
                        "base_pricing_model": "on-demand",
                        "discount": 0.36,
                        "source_class": "formula-derived",
                        "verification_mode": "formula",
                        "source_url": "https://calculator.aws/",
                        "derivation_basis": "m6i.large on-demand hourly x (1 - 0.36)",
                        "assumptions": "Savings Plans rate modeled from the established 3-year no-upfront discount pattern for m6i family in Singapore.",
                    }
                ],
                "official_static_rows": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    payload = {
        "products": {
            "SKU1": {
                "attributes": {
                    "instanceType": "m6i.large",
                    "operatingSystem": "Linux",
                    "preInstalledSw": "NA",
                    "tenancy": "Shared",
                    "capacitystatus": "Used",
                }
            },
            "SKU2": {
                "attributes": {
                    "instanceType": "m6i.xlarge",
                    "operatingSystem": "Linux",
                    "preInstalledSw": "NA",
                    "tenancy": "Shared",
                    "capacitystatus": "Used",
                }
            },
        },
        "terms": {"OnDemand": {}},
    }

    result = extend_pricing_family(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="EC2",
        family="m6i",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert "m6i.xlarge" in result["added_savings_plan_rows"]
    assert any(
        row["service"] == "EC2"
        and row["instance_type"] == "m6i.xlarge"
        and row["pricing_model"] == "savings-plans"
        for row in updated["formula_rows"]
    )


def test_extend_pricing_family_normalizes_friendly_service_aliases(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    pricing_dir = knowledge_dir / "pricing"
    pricing_dir.mkdir(parents=True, exist_ok=True)
    (pricing_dir / "aws-pricing-manifest.json").write_text(
        json.dumps(
            {
                "supported_region": "ap-southeast-1",
                "public_offer_rows": [],
                "formula_rows": [],
                "official_static_rows": [],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    payload = {
        "products": {
            "SKU1": {"attributes": {"instanceType": "db.m6i.large"}},
            "SKU2": {"attributes": {"instanceType": "db.m6i.xlarge"}},
        },
        "terms": {"OnDemand": {}},
    }

    result = extend_pricing_family(
        provider="aws",
        knowledge_dir=knowledge_dir,
        service="postgres",
        family="m6i",
        region="ap-southeast-1",
        offer_loader=lambda service, region: payload,
    )

    manifest_path = knowledge_dir / "pricing" / "aws-pricing-manifest.json"
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result["pass"] is True
    assert result["service"] == "RDS"
    assert {"db.m6i.large", "db.m6i.xlarge"}.issubset(
        {
            row["instance_type"]
            for row in updated["public_offer_rows"]
            if row["service"] == "RDS"
        }
    )


def test_create_new_project_scaffolds_normalizes_and_snapshots(tmp_path):
    result = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )

    project_dir = result["project_dir"]
    assert project_dir.exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "input" / "normalized" / "rfp.md").exists()
    assert (project_dir / "input" / "normalized" / "requirements-summary.md").exists()
    assert (project_dir / "working" / "00-knowledge-snapshot.json").exists()
    assert (project_dir / "working" / "apv-v2-snapshot.sqlite").exists()
    assert result["gate"]["pass"] is True


def test_create_new_project_initializes_default_run_context(tmp_path):
    result = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )

    run_context_path = result["project_dir"] / "working" / "00-run-context.json"

    assert run_context_path.exists()

    run_context = json.loads(run_context_path.read_text(encoding="utf-8"))
    assert run_context["mode"] == "draft"
    assert run_context["release_eligible"] is False
    assert run_context["intent_capture_mode"] == "none"
    assert run_context["urgency"] == "standard"

    readme = (result["project_dir"] / "README.md").read_text(encoding="utf-8")
    assert "Run Mode: draft" in readme
    assert "Release Eligibility: false" in readme


def test_create_new_project_rejects_submission_mode_without_sales_artifacts(tmp_path):
    result = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
        mode="submission",
    )

    assert result["ready"] is False
    assert any("approved sales intent" in issue.lower() for issue in result["issues"])


def test_validate_sales_brief_requires_file(tmp_path):
    result = validate_sales_brief(tmp_path / "input" / "normalized" / "sales-brief.md")

    assert result["pass"] is False
    assert any("sales brief is missing" in issue.lower() for issue in result["issues"])


def test_validate_sales_brief_requires_approval_fields(tmp_path):
    sales_brief = tmp_path / "sales-brief.md"
    sales_brief.write_text(
        "# Sales Brief\n\n"
        "**Deal Owner:** Jane Smith\n"
        "**Win Strategy:** Lead with compliance\n"
        "**Constraints:** Keep baseline under 20k/month\n",
        encoding="utf-8",
    )

    result = validate_sales_brief(sales_brief)

    assert result["pass"] is False
    assert any("approved by" in issue.lower() for issue in result["issues"])
    assert any("approved date" in issue.lower() for issue in result["issues"])


def test_validate_sales_brief_accepts_minimal_valid_brief(tmp_path):
    sales_brief = tmp_path / "sales-brief.md"
    sales_brief.write_text(
        "# Sales Brief\n\n"
        "**Deal Owner:** Jane Smith\n"
        "**Win Strategy:** Lead with compliance\n"
        "**Constraints:** Keep baseline under 20k/month\n"
        "**Approved By:** Jane Smith\n"
        "**Approved Date:** 2026-05-10\n",
        encoding="utf-8",
    )

    result = validate_sales_brief(sales_brief)

    assert result["pass"] is True
    assert result["issues"] == []
    assert result["approved"] is True


def test_promote_to_submission_requires_stage1_rerun_by_default(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)

    result = promote_to_submission(
        project_dir,
        owner="Jane Smith",
        strategy="Lead with compliance and low implementation risk",
        constraint="Keep baseline under 20k/month",
    )

    assert result["pass"] is True
    resume = resume_project(project_dir, from_stage=4)
    assert resume["pass"] is False
    assert any("rerun from stage 1" in issue.lower() for issue in resume["issues"])

    run_context = json.loads((project_dir / "working" / "00-run-context.json").read_text(encoding="utf-8"))
    assert run_context["mode"] == "submission"
    assert run_context["promotion_path"] == "full-rerun"
    assert run_context["sales_brief_present"] is True
    assert run_context["sales_brief_approved"] is True


def test_promote_to_submission_fast_track_preserves_resume_path(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)

    attestation = "Strategy unchanged from draft review; fast-track approved by deal owner."
    result = promote_to_submission(
        project_dir,
        owner="Jane Smith",
        strategy="Lead with compliance and low implementation risk",
        constraint="Keep baseline under 20k/month",
        fast_track_attestation=attestation,
    )

    assert result["pass"] is True
    resume = resume_project(project_dir, from_stage=4)
    assert resume["pass"] is True

    run_context = json.loads((project_dir / "working" / "00-run-context.json").read_text(encoding="utf-8"))
    assert run_context["mode"] == "submission"
    assert run_context["promotion_path"] == "fast-track"
    assert run_context["promotion_attestation"] == attestation


def test_promote_to_submission_generates_valid_sales_brief_from_operator_fields(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = promote_to_submission(
        project_dir,
        owner="Jane Smith",
        strategy="Lead with compliance and low implementation risk",
        constraint="Keep baseline under 20k/month",
        urgency="expedited",
    )

    assert result["pass"] is True
    sales_brief_path = project_dir / "input" / "normalized" / "sales-brief.md"
    assert sales_brief_path.exists()
    validation = validate_sales_brief(sales_brief_path)
    assert validation["pass"] is True

    run_context = json.loads((project_dir / "working" / "00-run-context.json").read_text(encoding="utf-8"))
    assert run_context["urgency"] == "expedited"
    assert run_context["sales_brief_present"] is True
    assert run_context["sales_brief_approved"] is True


def test_resume_project_requires_snapshot_boundary(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "input" / "normalized").mkdir(parents=True)
    (project_dir / "input" / "normalized" / "rfp.md").write_text("# RFP\n")
    (project_dir / "input" / "normalized" / "requirements-summary.md").write_text("# Requirements\n")

    result = resume_project(project_dir, from_stage=1)

    assert result["pass"] is False
    assert "working/00-knowledge-snapshot.json" in result["missing"]
    assert "working/apv-v2-snapshot.sqlite" in result["missing"]


def test_resume_project_rejects_expired_commercial_override(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "input" / "normalized").mkdir(parents=True)
    (project_dir / "input" / "normalized" / "rfp.md").write_text("# RFP\n")
    (project_dir / "input" / "normalized" / "requirements-summary.md").write_text("# Requirements\n")
    (project_dir / "evidence" / "pricing" / "commercial").mkdir(parents=True)
    (project_dir / "evidence" / "pricing" / "commercial" / "quote.pdf").write_text("quote")
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "working" / "05-commercial-overrides.md").write_text(
        "---\napproved_by: Finance\nvalid_until: 2020-01-01\n---\n# Overrides\n"
    )

    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    result = resume_project(project_dir, from_stage=1)

    assert result["pass"] is False
    assert any("expired" in issue.lower() for issue in result["issues"])


def test_run_stage_executes_command_verifies_outputs_and_updates_readme(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'working' / '01-brainstorm-context.md').write_text('# Context\\n'); "
            "(project / 'working' / '05-gap-log.md').write_text('# Gap Log\\n'); "
            "(project / 'outputs' / '01-brainstorm.md').write_text('---\\noutput_class: exploratory\\nstage: 1\\n---\\n# Brainstorm\\n')"
        ),
    ]

    result = run_stage(project_dir, 1, command=command)

    assert result["pass"] is True
    assert result["missing_outputs"] == []
    assert (project_dir / "outputs" / "01-brainstorm.md").exists()
    readme = (project_dir / "README.md").read_text()
    assert "| 1. Brainstorm | completed |" in readme


def test_run_stage_blocks_native_adapter_without_explicit_opt_in(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_stage(project_dir, 1)

    assert result["pass"] is False
    assert result["command_executed"] is False
    assert result["adapter_used"] is None
    assert any("native adapter" in issue.lower() for issue in result["issues"])
    assert not (project_dir / "outputs" / "01-brainstorm.md").exists()


def test_run_stage_reports_missing_project_directory_clearly(tmp_path):
    project_dir = tmp_path / "missing-project"

    result = run_stage(project_dir, 1)

    assert result["pass"] is False
    assert any("project directory does not exist" in issue.lower() for issue in result["issues"])


def test_run_stage_uses_native_adapter_when_explicitly_allowed(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_stage(project_dir, 1, allow_native_adapter=True)

    assert result["pass"] is True
    assert result["command_executed"] is False
    assert result["adapter_used"] == "native"
    brainstorm = (project_dir / "outputs" / "01-brainstorm.md").read_text()
    assert "output_class: exploratory" in brainstorm
    assert "stage: 1" in brainstorm
    assert "run_mode: draft" in brainstorm
    assert "release_eligible: False" in brainstorm


def test_run_stage_blocks_stage_1_for_submission_mode_without_approved_sales_intent(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
        mode="submission",
    )
    project_dir = created["project_dir"]

    result = run_stage(project_dir, 1, allow_native_adapter=True)

    assert result["pass"] is False
    assert any("approved sales intent" in issue.lower() for issue in result["issues"])
    assert not (project_dir / "outputs" / "01-brainstorm.md").exists()


def test_run_stage_5_uses_snapshot_pricing_data_when_no_command(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)
    result = run_stage(project_dir, 5, allow_native_adapter=True)

    assert result["pass"] is True
    pricing_output = (project_dir / "outputs" / "05-pricing.md").read_text()
    pricing_manifest = (project_dir / "working" / "05-pricing-manifest.md").read_text()
    freshness_report = (project_dir / "verification" / "freshness-report.json").read_text()

    assert "m6i.large" in pricing_output
    assert "$0.096" in pricing_output
    assert "m6i.xlarge" in pricing_manifest
    assert '"stale": 0' in freshness_report


def test_run_stage_5_consumes_generated_canonical_pricing_data(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    payloads = {
        "EC2": {
            "products": {"SKU1": {"attributes": {"instanceType": "m6i.large", "operatingSystem": "Linux", "preInstalledSw": "NA", "tenancy": "Shared", "capacitystatus": "Used"}}},
            "terms": {"OnDemand": {"SKU1": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "0.096"}}}}}}},
        },
        "RDS": {
            "products": {"SKU2": {"attributes": {"instanceType": "db.m6i.large"}}},
            "terms": {"OnDemand": {"SKU2": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "0.188"}}}}}}},
        },
        "CloudHSM": {
            "products": {"SKU3": {"attributes": {"hsmGeneration": "hsm2.medium"}}},
            "terms": {"OnDemand": {"SKU3": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "1.86"}}}}}}},
        },
    }
    write_aws_pricing_knowledge(
        knowledge_dir=knowledge_dir,
        region="ap-southeast-1",
        today=date(2026, 5, 2),
        offer_loader=lambda service, region: payloads[service],
    )

    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=knowledge_dir,
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)
    result = run_stage(project_dir, 5, allow_native_adapter=True)

    assert result["pass"] is True
    pricing_output = (project_dir / "outputs" / "05-pricing.md").read_text()
    pricing_manifest = (project_dir / "working" / "05-pricing-manifest.md").read_text()

    assert "multi-az" in pricing_output
    assert "savings-plans" in pricing_output
    assert "multi-az" in pricing_manifest


def test_run_stage_5_renders_unit_priced_rows_with_billing_units(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    payloads = {
        "EC2": {
            "products": {"SKU1": {"attributes": {"instanceType": "m6i.large", "operatingSystem": "Linux", "preInstalledSw": "NA", "tenancy": "Shared", "capacitystatus": "Used"}}},
            "terms": {"OnDemand": {"SKU1": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "0.096"}}}}}}},
        },
        "RDS": {
            "products": {"SKU2": {"attributes": {"instanceType": "db.m6i.large"}}},
            "terms": {"OnDemand": {"SKU2": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "0.188"}}}}}}},
        },
        "CloudHSM": {
            "products": {"SKU3": {"attributes": {"hsmGeneration": "hsm2.medium"}}},
            "terms": {"OnDemand": {"SKU3": {"TERM": {"priceDimensions": {"DIM": {"pricePerUnit": {"USD": "1.86"}}}}}}},
        },
    }
    write_aws_pricing_knowledge(
        knowledge_dir=knowledge_dir,
        region="ap-southeast-1",
        today=date(2026, 5, 2),
        offer_loader=lambda service, region: payloads[service],
    )

    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=knowledge_dir,
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)
    result = run_stage(project_dir, 5, allow_native_adapter=True)

    assert result["pass"] is True
    pricing_output = (project_dir / "outputs" / "05-pricing.md").read_text()
    assert "Billing Unit" in pricing_output
    assert "per GB-month" in pricing_output
    assert "Hosted Zone" in pricing_output


def test_run_stage_native_adapters_derive_content_from_project_inputs(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)

    brainstorm = (project_dir / "outputs" / "01-brainstorm.md").read_text()
    architecture = (project_dir / "outputs" / "03-architecture.md").read_text()
    sizing = (project_dir / "outputs" / "04-sizing.md").read_text()

    assert "ACME Payments" in brainstorm
    assert "500 TPS peak processing capacity" in brainstorm
    assert "Multi-AZ deployment in AWS Singapore" in architecture
    assert "500 TPS" in sizing
    assert "99.99% availability SLA" in sizing


def test_run_stage_fails_when_required_outputs_are_missing(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    command = [sys.executable, "-c", "print('no outputs emitted')"]
    result = run_stage(project_dir, 1, command=command)

    assert result["pass"] is False
    assert "outputs/01-brainstorm.md" in result["missing_outputs"]


def test_run_stage_reports_missing_command_binary_as_structured_failure(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_stage(project_dir, 1, command=["does-not-exist"])

    assert result["pass"] is False
    assert result["command_executed"] is False
    assert result["command_returncode"] is None
    assert any("does-not-exist" in issue or "not found" in issue.lower() for issue in result["issues"])


def test_run_stage_rejects_invalid_output_metadata(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'working' / '01-brainstorm-context.md').write_text('# Context\\n'); "
            "(project / 'working' / '05-gap-log.md').write_text('# Gap Log\\n'); "
            "(project / 'outputs' / '01-brainstorm.md').write_text('---\\noutput_class: derived\\nstage: 99\\n---\\n# Brainstorm\\n')"
        ),
    ]

    result = run_stage(project_dir, 1, command=command)

    assert result["pass"] is False
    assert any("output_class" in issue or "stage metadata" in issue.lower() for issue in result["issues"])


def test_run_stage_7_requires_approval_outputs(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "verification").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n")
    (project_dir / "verification" / "source-url-validation.json").write_text('{"pass": true}')
    (project_dir / "verification" / "freshness-report.json").write_text('{"pass": true}')
    (project_dir / "approvals" / "unified-checklist.md").write_text("# Checklist\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '07-approval.md').write_text('---\\nstage: 7\\ndecision: APPROVED\\n---\\n# Approval\\n'); "
            "(project / 'approvals' / 'release-decision.md').write_text('---\\ndecision: APPROVED\\nstage: 7\\n---\\n# Release\\n')"
        ),
    ]

    result = run_stage(project_dir, 7, command=command)

    assert result["pass"] is False
    assert "approvals/reviewer-notes.md" in result["missing_outputs"]


def test_run_stage_7_requires_verification_artifacts_before_review(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    result = run_stage(project_dir, 7, command=[sys.executable, "-c", "print('should not run')"])

    assert result["pass"] is False
    assert result["command_executed"] is False
    assert "verification/source-url-validation.json" in result["missing"]
    assert "verification/freshness-report.json" in result["missing"]
    assert "approvals/unified-checklist.md" in result["missing"]


def test_run_stage_6_requires_traceable_upstream_sources(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "01-brainstorm.md").write_text("---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n")
    (project_dir / "outputs" / "02-compliance.md").write_text("---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n")
    (project_dir / "outputs" / "03-architecture.md").write_text("---\noutput_class: derived\nstage: 3\n---\n# Architecture\n")
    (project_dir / "outputs" / "04-sizing.md").write_text("---\noutput_class: derived\nstage: 4\n---\n# Sizing\n")
    (project_dir / "outputs" / "05-pricing.md").write_text("---\noutput_class: evidence-backed\nstage: 5\n---\n# Pricing\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '06-response.md').write_text('---\\noutput_class: derived\\nstage: 6\\nsources: [outputs/01-brainstorm.md]\\n---\\n# Response\\n')"
        ),
    ]

    result = run_stage(project_dir, 6, command=command)

    assert result["pass"] is False
    assert any("sources" in issue.lower() for issue in result["issues"])


def test_run_stage_6_rejects_response_url_not_in_upstream_outputs(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "01-brainstorm.md").write_text("---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n")
    (project_dir / "outputs" / "02-compliance.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n\nSee [PCI](https://example.com/pci)\n"
    )
    (project_dir / "outputs" / "03-architecture.md").write_text("---\noutput_class: derived\nstage: 3\n---\n# Architecture\n")
    (project_dir / "outputs" / "04-sizing.md").write_text("---\noutput_class: derived\nstage: 4\n---\n# Sizing\n")
    (project_dir / "outputs" / "05-pricing.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 5\n---\n# Pricing\n\nSee [Calc](https://calculator.aws/)\n"
    )
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '06-response.md').write_text('---\\noutput_class: derived\\nstage: 6\\nsources: [outputs/01-brainstorm.md, outputs/02-compliance.md, outputs/03-architecture.md, outputs/04-sizing.md, outputs/05-pricing.md]\\n---\\n# Response\\n\\nSee [Other](https://example.com/unsupported)\\n')"
        ),
    ]

    result = run_stage(project_dir, 6, command=command)

    assert result["pass"] is False
    assert any("unsupported url" in issue.lower() or "not present in upstream" in issue.lower() for issue in result["issues"])


def test_run_stage_6_requires_response_urls_when_upstream_evidence_has_urls(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "01-brainstorm.md").write_text("---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n")
    (project_dir / "outputs" / "02-compliance.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n\nSee [PCI](https://example.com/pci)\n"
    )
    (project_dir / "outputs" / "03-architecture.md").write_text("---\noutput_class: derived\nstage: 3\n---\n# Architecture\n")
    (project_dir / "outputs" / "04-sizing.md").write_text("---\noutput_class: derived\nstage: 4\n---\n# Sizing\n")
    (project_dir / "outputs" / "05-pricing.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 5\n---\n# Pricing\n\nSee [Calc](https://calculator.aws/)\n"
    )
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '06-response.md').write_text('---\\noutput_class: derived\\nstage: 6\\nsources: [outputs/01-brainstorm.md, outputs/02-compliance.md, outputs/03-architecture.md, outputs/04-sizing.md, outputs/05-pricing.md]\\n---\\n# Response\\n\\nNo citations preserved here.\\n')"
        ),
    ]

    result = run_stage(project_dir, 6, command=command)

    assert result["pass"] is False
    assert any("response urls" in issue.lower() or "no urls" in issue.lower() for issue in result["issues"])


def test_run_stage_6_requires_compliance_and_pricing_sections_with_citations(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "01-brainstorm.md").write_text("---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n")
    (project_dir / "outputs" / "02-compliance.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n\nSee [PCI](https://example.com/pci)\n"
    )
    (project_dir / "outputs" / "03-architecture.md").write_text("---\noutput_class: derived\nstage: 3\n---\n# Architecture\n")
    (project_dir / "outputs" / "04-sizing.md").write_text("---\noutput_class: derived\nstage: 4\n---\n# Sizing\n")
    (project_dir / "outputs" / "05-pricing.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 5\n---\n# Pricing\n\nSee [Calc](https://calculator.aws/)\n"
    )
    (project_dir / "working" / "05-assumption-log.md").write_text("# Assumptions\n\n- Conservative pricing assumption\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '06-response.md').write_text('---\\noutput_class: derived\\nstage: 6\\nsources: [outputs/01-brainstorm.md, outputs/02-compliance.md, outputs/03-architecture.md, outputs/04-sizing.md, outputs/05-pricing.md]\\n---\\n# Response\\n\\n## Executive Summary\\n\\nSummary with [PCI](https://example.com/pci).\\n')"
        ),
    ]

    result = run_stage(project_dir, 6, command=command)

    assert result["pass"] is False
    assert any("compliance section" in issue.lower() for issue in result["issues"])
    assert any("pricing section" in issue.lower() for issue in result["issues"])
    assert any("assumptions" in issue.lower() for issue in result["issues"])


def test_run_stage_6_requires_pricing_and_sizing_facts_from_upstream_outputs(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "01-brainstorm.md").write_text("---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n")
    (project_dir / "outputs" / "02-compliance.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n\nSee [PCI](https://good.com/pci)\n"
    )
    (project_dir / "outputs" / "03-architecture.md").write_text(
        "---\noutput_class: derived\nstage: 3\n---\n# Architecture\n\n- Compute tier for transaction processing\n"
    )
    (project_dir / "outputs" / "04-sizing.md").write_text(
        "---\noutput_class: derived\nstage: 4\n---\n# Sizing\n\nDesign TPS: 750\n"
    )
    (project_dir / "outputs" / "05-pricing.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 5\n---\n# Pricing\n\n| Service | Instance Type | Pricing Model | Hourly ($) | Monthly ($) | Source |\n| --- | --- | --- | --- | --- | --- |\n| EC2 | m6i.large | on-demand | $0.096 | $70.08 | https://calculator.aws/ |\n"
    )
    (project_dir / "working" / "05-assumption-log.md").write_text("# Assumptions\n\n- Conservative pricing assumption\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '06-response.md').write_text('---\\noutput_class: derived\\nstage: 6\\nsources: [outputs/01-brainstorm.md, outputs/02-compliance.md, outputs/03-architecture.md, outputs/04-sizing.md, outputs/05-pricing.md]\\n---\\n# Response\\n\\n## 4. Compliance & Security\\n\\nSee https://good.com/pci\\n\\n## 5. Infrastructure & Sizing\\n\\nGeneric infrastructure statement only.\\n\\n## 6. Pricing\\n\\nPricing source: https://calculator.aws/\\n\\n## 8. Assumptions & Caveats\\n\\n- Conservative pricing assumption\\n')"
        ),
    ]

    result = run_stage(project_dir, 6, command=command)

    assert result["pass"] is False
    assert any("pricing facts" in issue.lower() for issue in result["issues"])
    assert any("sizing facts" in issue.lower() or "architecture facts" in issue.lower() for issue in result["issues"])


def test_run_stage_6_native_adapter_handles_sample_like_pricing_and_assumptions(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    (project_dir / "outputs" / "01-brainstorm.md").write_text(
        "---\noutput_class: exploratory\nstage: 1\n---\n# Brainstorm\n"
    )
    (project_dir / "outputs" / "02-compliance.md").write_text(
        "---\noutput_class: evidence-backed\nstage: 2\n---\n# Compliance\n\nSee [PCI](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf)\n"
    )
    (project_dir / "outputs" / "03-architecture.md").write_text(
        "---\noutput_class: derived\nstage: 3\n---\n# Architecture\n\n- Compute tier for transaction processing\n"
    )
    (project_dir / "outputs" / "04-sizing.md").write_text(
        "---\noutput_class: derived\nstage: 4\n---\n# Sizing\n\nDesign TPS: 750\n"
    )
    (project_dir / "outputs" / "05-pricing.md").write_text(
        "---\ncreated: '2026-05-01'\noutput_class: evidence-backed\nstage: 5\n---\n"
        "# Pricing\n\n"
        "> [!NOTE] All prices sourced from aws-component-catalog.md via https://calculator.aws/\n\n"
        "## 6. Pricing\n\n"
        "Representative compute price: c6i.xlarge at $0.170/hr and $124.10 monthly.\n"
    )
    (project_dir / "working" / "05-assumption-log.md").write_text(
        "---\ncreated: '2026-05-01'\nstage: 5\ntype: working\n---\n"
        "# Pricing Assumption Log\n\n"
        "## Assumptions\n\n"
        "| # | Assumption | Impact | Risk |\n"
        "|---|-----------|--------|------|\n"
        "| 1 | CloudHSM estimated from public pricing page | May vary by region | Medium |\n"
        "| 2 | DR region pricing assumed equal to primary | Actual regional rates may differ | Low |\n"
    )

    result = run_stage(project_dir, 6, allow_native_adapter=True)

    assert result["pass"] is True
    response = (project_dir / "outputs" / "06-response.md").read_text()
    assert "https://calculator.aws/" in response
    assert "Design TPS: 750" in response
    assert "CloudHSM estimated from public pricing page" in response


def test_run_stage_uses_bridge_command_when_configured(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]
    (project_dir / "working" / "00-stage-commands.json").write_text(
        json.dumps(
            {
                "1": [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; project = Path.cwd(); (project / 'working' / '01-brainstorm-context.md').write_text('# Context\\n'); (project / 'working' / '05-gap-log.md').write_text('# Gap Log\\n'); (project / 'outputs' / '01-brainstorm.md').write_text('---\\noutput_class: exploratory\\nstage: 1\\n---\\n# Brainstorm\\nDetailed context.\\n')",
                ]
            }
        ),
        encoding="utf-8",
    )

    result = run_stage(project_dir, 1)

    assert result["pass"] is True
    assert result["command_executed"] is True
    assert result["adapter_used"] == "bridge"


def test_run_stage_7_blocks_expired_commercial_override_before_review(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "verification").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing" / "commercial").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n")
    (project_dir / "verification" / "source-url-validation.json").write_text('{"pass": true}')
    (project_dir / "verification" / "freshness-report.json").write_text('{"pass": true}')
    (project_dir / "approvals" / "unified-checklist.md").write_text("# Checklist\n")
    (project_dir / "evidence" / "pricing" / "commercial" / "quote.pdf").write_text("quote")
    (project_dir / "working" / "05-commercial-overrides.md").write_text(
        "---\napproved_by: Finance\nvalid_until: 2020-01-01\n---\n# Overrides\n"
    )
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    result = run_stage(project_dir, 7, command=[sys.executable, "-c", "print('should not run')"])

    assert result["pass"] is False
    assert any("expired" in issue.lower() for issue in result["issues"])
    assert result["command_executed"] is False


def test_run_stage_7_rejects_invalid_source_url_report(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "verification").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n")
    (project_dir / "verification" / "source-url-validation.json").write_text('{"invalid": 1, "valid": 0}')
    (project_dir / "verification" / "freshness-report.json").write_text('{"stale": 0, "fresh": 10}')
    (project_dir / "approvals" / "unified-checklist.md").write_text("# Checklist\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '07-approval.md').write_text('---\\nstage: 7\\ndecision: REJECTED\\n---\\n# Approval\\n'); "
            "(project / 'approvals' / 'release-decision.md').write_text('---\\ndecision: REJECTED\\nstage: 7\\n---\\n# Release\\n'); "
            "(project / 'approvals' / 'reviewer-notes.md').write_text('---\\ntype: reviewer-notes\\nstage: 7\\n---\\n# Notes\\n')"
        ),
    ]

    result = run_stage(project_dir, 7, command=command)

    assert result["pass"] is False
    assert any("source url" in issue.lower() for issue in result["issues"])


def test_run_stage_7_rejects_stale_freshness_report(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "verification").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n")
    (project_dir / "verification" / "source-url-validation.json").write_text('{"invalid": 0, "valid": 10}')
    (project_dir / "verification" / "freshness-report.json").write_text('{"stale": 2, "fresh": 8}')
    (project_dir / "approvals" / "unified-checklist.md").write_text("# Checklist\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '07-approval.md').write_text('---\\nstage: 7\\ndecision: REJECTED\\n---\\n# Approval\\n'); "
            "(project / 'approvals' / 'release-decision.md').write_text('---\\ndecision: REJECTED\\nstage: 7\\n---\\n# Release\\n'); "
            "(project / 'approvals' / 'reviewer-notes.md').write_text('---\\ntype: reviewer-notes\\nstage: 7\\n---\\n# Notes\\n')"
        ),
    ]

    result = run_stage(project_dir, 7, command=command)

    assert result["pass"] is False
    assert any("freshness" in issue.lower() or "stale" in issue.lower() for issue in result["issues"])


def test_run_stage_7_rejects_placeholder_text_in_response(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "outputs").mkdir(parents=True)
    (project_dir / "verification").mkdir(parents=True)
    (project_dir / "approvals").mkdir(parents=True)
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "outputs" / "06-response.md").write_text("# Response\n\nTODO: fill this in\n")
    (project_dir / "verification" / "source-url-validation.json").write_text('{"invalid": 0, "valid": 10}')
    (project_dir / "verification" / "freshness-report.json").write_text('{"stale": 0, "fresh": 8}')
    (project_dir / "approvals" / "unified-checklist.md").write_text("# Checklist\n")
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")

    command = [
        sys.executable,
        "-c",
        (
            "from pathlib import Path; "
            f"project = Path({str(project_dir)!r}); "
            "(project / 'outputs' / '07-approval.md').write_text('---\\nstage: 7\\ndecision: REJECTED\\n---\\n# Approval\\n'); "
            "(project / 'approvals' / 'release-decision.md').write_text('---\\ndecision: REJECTED\\nstage: 7\\n---\\n# Release\\n'); "
            "(project / 'approvals' / 'reviewer-notes.md').write_text('---\\ntype: reviewer-notes\\nstage: 7\\n---\\n# Notes\\n')"
        ),
    ]

    result = run_stage(project_dir, 7, command=command)

    assert result["pass"] is False
    assert any("todo" in issue.lower() or "placeholder" in issue.lower() for issue in result["issues"])


def test_run_pipeline_stops_at_first_failed_stage(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    stage_commands = {
        1: [
            sys.executable,
            "-c",
            (
                "from pathlib import Path; "
                f"project = Path({str(project_dir)!r}); "
                "(project / 'working' / '01-brainstorm-context.md').write_text('# Context\\n'); "
                "(project / 'working' / '05-gap-log.md').write_text('# Gap Log\\n'); "
                "(project / 'outputs' / '01-brainstorm.md').write_text('---\\noutput_class: exploratory\\nstage: 1\\n---\\n# Brainstorm\\n')"
            ),
        ],
        2: [sys.executable, "-c", "print('missing compliance outputs')"],
    }

    result = run_pipeline(project_dir, from_stage=1, to_stage=2, stage_commands=stage_commands)

    assert result["pass"] is False
    assert result["failed_stage"] == 2
    assert len(result["stages"]) == 2
    assert result["stages"][0]["pass"] is True
    assert result["stages"][1]["pass"] is False


def test_run_pipeline_blocks_native_adapters_by_default(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_pipeline(project_dir, from_stage=1, to_stage=7)

    assert result["pass"] is False
    assert result["failed_stage"] == 1
    assert len(result["stages"]) == 1
    assert result["stages"][0]["adapter_used"] is None
    assert any("native adapter" in issue.lower() for issue in result["stages"][0]["issues"])


def test_run_pipeline_uses_native_adapters_end_to_end_when_explicitly_allowed(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_pipeline(project_dir, from_stage=1, to_stage=7, allow_native_adapter=True)

    assert result["pass"] is False
    assert result["failed_stage"] == 7
    assert len(result["stages"]) == 7
    assert all(stage_result["pass"] is True for stage_result in result["stages"][:6])
    assert result["stages"][6]["pass"] is False
    assert all(stage_result["adapter_used"] == "native" for stage_result in result["stages"])
    assert (project_dir / "outputs" / "07-approval.md").exists()
    assert (project_dir / "approvals" / "release-decision.md").exists()


def test_native_pipeline_outputs_do_not_use_placeholder_evidence(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_pipeline(project_dir, from_stage=1, to_stage=7, allow_native_adapter=True)

    assert result["failed_stage"] == 7
    compliance = (project_dir / "outputs" / "02-compliance.md").read_text()
    response = (project_dir / "outputs" / "06-response.md").read_text()
    assert "example.com" not in compliance
    assert "example.com" not in response


def test_run_pipeline_native_review_requires_manual_approval(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    result = run_pipeline(project_dir, from_stage=1, to_stage=7, allow_native_adapter=True)

    assert result["pass"] is False
    assert result["failed_stage"] == 7
    approval = (project_dir / "outputs" / "07-approval.md").read_text()
    release = (project_dir / "approvals" / "release-decision.md").read_text()

    assert "decision: CONDITIONAL" in approval
    assert "decision: CONDITIONAL" in release


def test_validate_release_readiness_blocks_draft_mode_even_when_quality_artifacts_are_approved(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)
    run_stage(project_dir, 5, allow_native_adapter=True)
    run_stage(project_dir, 6, allow_native_adapter=True)

    (project_dir / "verification" / "source-url-validation.json").write_text(
        json.dumps({"pass": True, "invalid": 0, "manual_review_required": False}, indent=2),
        encoding="utf-8",
    )
    (project_dir / "verification" / "freshness-report.json").write_text(
        json.dumps({"pass": True, "stale": 0}, indent=2),
        encoding="utf-8",
    )
    (project_dir / "outputs" / "07-approval.md").write_text(
        "---\nstage: 7\ndecision: APPROVED\n---\n# Approval\n",
        encoding="utf-8",
    )
    (project_dir / "approvals" / "release-decision.md").write_text(
        "---\nstage: 7\ndecision: APPROVED\n---\n# Release\n",
        encoding="utf-8",
    )
    (project_dir / "approvals" / "reviewer-notes.md").write_text(
        "---\nstage: 7\ntype: reviewer-notes\n---\n# Notes\n",
        encoding="utf-8",
    )

    result = validate_release_readiness(project_dir)

    assert result["pass"] is False
    assert any("draft mode" in issue.lower() for issue in result["issues"])


def test_check_project_readiness_does_not_rewrite_existing_snapshot(tmp_path):
    project_dir = tmp_path / "project"
    (project_dir / "working").mkdir(parents=True)
    (project_dir / "evidence" / "pricing").mkdir(parents=True)
    (project_dir / "evidence" / "pricing" / "pricing-evidence.md").write_text("evidence")

    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES / "knowledge", knowledge_dir)

    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder")
    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha", knowledge_dir=knowledge_dir)

    snapshot_json = project_dir / "working" / "00-knowledge-snapshot.json"
    snapshot_text_before = snapshot_json.read_text(encoding="utf-8")

    result = apv_module.check_project_readiness(project_dir)

    assert result["pass"] is True
    assert snapshot_json.read_text(encoding="utf-8") == snapshot_text_before


def test_native_pipeline_review_does_not_self_attest_url_validation(tmp_path):
    created = create_new_project(
        base_dir=tmp_path,
        customer="Acme Corp",
        title="Payment Gateway",
        raw_dir=FIXTURES / "raw",
        knowledge_dir=FIXTURES / "knowledge",
        knowledge_commit="test-sha",
    )
    project_dir = created["project_dir"]

    run_stage(project_dir, 1, allow_native_adapter=True)
    run_stage(project_dir, 2, allow_native_adapter=True)
    run_stage(project_dir, 3, allow_native_adapter=True)
    run_stage(project_dir, 4, allow_native_adapter=True)
    run_stage(project_dir, 5, allow_native_adapter=True)
    run_stage(project_dir, 6, allow_native_adapter=True)
    result = run_stage(project_dir, 7, allow_native_adapter=True)

    assert result["pass"] is False
    assert any("source url" in issue.lower() or "reviewer" in issue.lower() or "manual" in issue.lower() for issue in result["issues"])
