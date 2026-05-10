#!/usr/bin/env python3
"""Minimal APV V2 orchestrator entrypoint."""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from frontmatter import parse_file

from create_snapshot import create_project_snapshot
from aws_pricing_subset import (
    SERVICE_TITLES,
    add_official_static_item,
    add_public_offer_item,
    add_savings_plan_pattern_rows,
    load_aws_pricing_manifest,
    save_aws_pricing_manifest,
)
from aws_public_pricing import _extract_ondemand_price, _load_offer_json, list_public_offer_instance_types
from freshness import check_domain_freshness
from knowledge_audit import audit_directory
from normalize import normalize_raw_inputs
from pricing_fetcher import refresh_aws_pricing
from stage_adapters import run_native_stage_adapter
from sync_db import sync_knowledge
from validate_gates import check_gate
from validate_urls import extract_urls_from_file


PROJECT_DIRS = [
    "input/raw",
    "input/normalized",
    "outputs",
    "working",
    "evidence",
    "verification",
    "approvals",
]

STAGE_NAMES = {
    0: "Intake",
    1: "Brainstorm",
    2: "Compliance",
    3: "Architecture",
    4: "Sizing",
    5: "Pricing",
    6: "Response",
    7: "Review",
}

STAGE_OUTPUTS = {
    0: ["input/normalized/rfp.md", "input/normalized/requirements-summary.md"],
    1: ["working/01-brainstorm-context.md", "working/05-gap-log.md", "outputs/01-brainstorm.md"],
    2: ["working/02-compliance-map.md", "outputs/02-compliance.md", "evidence/compliance/"],
    3: ["working/03-architecture-decision-log.md", "outputs/03-architecture.md"],
    4: ["working/04-sizing-record.md", "outputs/04-sizing.md"],
    5: [
        "working/05-pricing-manifest.md",
        "working/05-assumption-log.md",
        "outputs/05-pricing.md",
        "evidence/pricing/",
        "verification/freshness-report.json",
    ],
    6: ["outputs/06-response.md"],
    7: ["outputs/07-approval.md", "approvals/release-decision.md", "approvals/reviewer-notes.md"],
}

STAGE_PRIMARY_OUTPUT = {
    1: "outputs/01-brainstorm.md",
    2: "outputs/02-compliance.md",
    3: "outputs/03-architecture.md",
    4: "outputs/04-sizing.md",
    5: "outputs/05-pricing.md",
    6: "outputs/06-response.md",
    7: "outputs/07-approval.md",
}

STAGE_OUTPUT_CLASS = {
    1: "exploratory",
    2: "evidence-backed",
    3: "derived",
    4: "derived",
    5: "evidence-backed",
    6: "derived",
}

STAGE_6_REQUIRED_SOURCES = [
    "outputs/01-brainstorm.md",
    "outputs/02-compliance.md",
    "outputs/03-architecture.md",
    "outputs/04-sizing.md",
    "outputs/05-pricing.md",
]

AWS_PUBLIC_OFFER_MANIFEST_SERVICES = {"EC2", "RDS", "CloudHSM"}
AWS_OFFICIAL_STATIC_MANIFEST_SERVICES = set(SERVICE_TITLES) - AWS_PUBLIC_OFFER_MANIFEST_SERVICES
AWS_SERVICE_ALIASES = {
    "ec2": "EC2",
    "compute": "EC2",
    "vm": "EC2",
    "virtual-machine": "EC2",
    "postgres": "RDS",
    "postgresql": "RDS",
    "postgresql/rds": "RDS",
    "rds": "RDS",
    "aurora-postgres": "RDS",
    "cloudhsm": "CloudHSM",
    "hsm": "CloudHSM",
    "redis": "ElastiCache",
    "elasticache": "ElastiCache",
    "elasticache redis": "ElastiCache",
    "alb": "ALB",
    "application-load-balancer": "ALB",
    "application load balancer": "ALB",
    "nlb": "NLB",
    "network-load-balancer": "NLB",
    "network load balancer": "NLB",
    "ebs": "EBS",
    "s3": "S3",
    "kms": "KMS",
    "directconnect": "Direct Connect",
    "direct-connect": "Direct Connect",
    "direct connect": "Direct Connect",
    "vpc-flow-logs": "VPC Flow Logs",
    "vpc flow logs": "VPC Flow Logs",
    "flow-logs": "VPC Flow Logs",
    "waf": "WAF",
    "cloudtrail": "CloudTrail",
    "cloudwatch": "CloudWatch",
    "cloud-watch": "CloudWatch",
    "cloud watch": "CloudWatch",
    "guardduty": "GuardDuty",
    "route53": "Route 53",
    "route-53": "Route 53",
    "route 53": "Route 53",
    "shield": "Shield Advanced",
    "shield-advanced": "Shield Advanced",
    "shield advanced": "Shield Advanced",
    "securityhub": "Security Hub",
    "security-hub": "Security Hub",
    "security hub": "Security Hub",
    "nat": "NAT Gateway",
    "natgateway": "NAT Gateway",
    "nat-gateway": "NAT Gateway",
    "nat gateway": "NAT Gateway",
    "secretsmanager": "Secrets Manager",
    "secrets-manager": "Secrets Manager",
    "secrets manager": "Secrets Manager",
    "sns": "SNS",
    "sqs": "SQS",
    "ecr": "ECR",
    "apigateway": "API Gateway",
    "api-gateway": "API Gateway",
    "api gateway": "API Gateway",
    "private-ca": "ACM Private CA",
    "private ca": "ACM Private CA",
    "acm-private-ca": "ACM Private CA",
    "acm private ca": "ACM Private CA",
}

AWS_STATIC_DEFAULT_COMPONENTS = {
    "Route 53": "Hosted Zone",
    "Shield Advanced": "Subscription",
    "CloudWatch": "Logs Ingest",
    "NAT Gateway": "Gateway Hour",
    "Secrets Manager": "Secret",
    "SNS": "API Requests",
    "SQS": "Standard Requests",
    "ECR": "Private Repository Storage",
    "API Gateway": "HTTP API Requests",
}

AWS_STATIC_COMPONENT_ALIASES = {
    "Route 53": {
        "hosted zone": "Hosted Zone",
        "hosted-zone": "Hosted Zone",
        "zone": "Hosted Zone",
        "dns queries": "Standard DNS Queries",
        "dns-queries": "Standard DNS Queries",
        "queries": "Standard DNS Queries",
    },
    "Shield Advanced": {
        "subscription": "Subscription",
    },
    "CloudWatch": {
        "logs ingest": "Logs Ingest",
        "logs-ingest": "Logs Ingest",
        "ingest": "Logs Ingest",
        "logs archive": "Logs Archive",
        "logs-archive": "Logs Archive",
        "archive": "Logs Archive",
        "custom metrics": "Custom Metrics",
        "custom-metrics": "Custom Metrics",
        "metrics": "Custom Metrics",
        "standard alarm": "Standard Alarm",
        "standard-alarm": "Standard Alarm",
        "alarm": "Standard Alarm",
    },
    "NAT Gateway": {
        "gateway hour": "Gateway Hour",
        "gateway-hour": "Gateway Hour",
        "hourly": "Gateway Hour",
        "data processing": "Data Processing",
        "data-processing": "Data Processing",
    },
    "Secrets Manager": {
        "secret": "Secret",
    },
    "SNS": {
        "api requests": "API Requests",
        "api-requests": "API Requests",
        "requests": "API Requests",
    },
    "SQS": {
        "standard requests": "Standard Requests",
        "standard-requests": "Standard Requests",
        "requests": "Standard Requests",
    },
    "ECR": {
        "private repository storage": "Private Repository Storage",
        "private-repository-storage": "Private Repository Storage",
        "storage": "Private Repository Storage",
    },
    "API Gateway": {
        "http api requests": "HTTP API Requests",
        "http-api-requests": "HTTP API Requests",
        "http api": "HTTP API Requests",
        "requests": "HTTP API Requests",
    },
}

AWS_PRICING_SOURCE_OF_TRUTH = Path("pricing") / "aws-pricing-manifest.json"
AWS_PRICING_REGENERATE_COMMAND = "./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness"
AWS_GENERATED_KNOWLEDGE_ROUTES = {
    "pricing/aws-component-catalog.md": {
        "source_of_truth": AWS_PRICING_SOURCE_OF_TRUTH,
        "regenerate_command": AWS_PRICING_REGENERATE_COMMAND,
    },
    "pricing/aws.md": {
        "source_of_truth": AWS_PRICING_SOURCE_OF_TRUTH,
        "regenerate_command": AWS_PRICING_REGENERATE_COMMAND,
    },
    "pricing/aws-component-catalog.report.json": {
        "source_of_truth": AWS_PRICING_SOURCE_OF_TRUTH,
        "regenerate_command": AWS_PRICING_REGENERATE_COMMAND,
    },
}

NATIVE_ADAPTER_DISABLED_ISSUE = (
    "Native adapter execution is disabled by default; provide an explicit stage command, "
    "configure working/00-stage-commands.json, or opt in with allow_native_adapter for local/test runs."
)


def _load_stage_bridge_command(project_dir: Path, stage: int) -> list[str] | None:
    bridge_path = Path(project_dir) / "working" / "00-stage-commands.json"
    if not bridge_path.exists():
        return None
    try:
        payload = json.loads(bridge_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    command = payload.get(str(stage)) or payload.get(stage)
    if isinstance(command, list) and all(isinstance(item, str) for item in command):
        return command
    return None


def _frontmatter_truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def _resolve_generated_knowledge_route(target_path: Path, knowledge_dir: Path) -> dict | None:
    try:
        relative_target = target_path.relative_to(knowledge_dir).as_posix()
    except ValueError:
        return None

    known_route = AWS_GENERATED_KNOWLEDGE_ROUTES.get(relative_target)
    if known_route:
        return {
            "source_of_truth": knowledge_dir / known_route["source_of_truth"],
            "regenerate_command": known_route["regenerate_command"],
        }

    if target_path.suffix != ".md" or not target_path.exists():
        return None

    try:
        frontmatter, _ = parse_file(target_path)
    except Exception:
        return None

    status = str(frontmatter.get("status") or "").strip().lower()
    if not (_frontmatter_truthy(frontmatter.get("do_not_edit")) or status.startswith("generated-")):
        return None

    source_of_truth = frontmatter.get("source_of_truth")
    regenerate_command = frontmatter.get("regenerate_command")
    if not source_of_truth:
        return None

    route = {
        "source_of_truth": knowledge_dir / Path(str(source_of_truth)),
    }
    if regenerate_command:
        route["regenerate_command"] = str(regenerate_command)
    return route
    return None


def _slugify(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "project"


SALES_BRIEF_REQUIRED_FIELDS = {
    "Deal Owner": "deal_owner",
    "Win Strategy": "win_strategy",
    "Constraints": "constraints",
    "Approved By": "approved_by",
    "Approved Date": "approved_date",
}


def _extract_markdown_label_value(text: str, label: str) -> str | None:
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", text)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def _run_context_path(project_dir: Path) -> Path:
    return Path(project_dir) / "working" / "00-run-context.json"


def _sales_brief_path(project_dir: Path) -> Path:
    return Path(project_dir) / "input" / "normalized" / "sales-brief.md"


def _default_run_context(mode: str = "draft") -> dict[str, object]:
    release_eligible = False
    sales_brief_present = False
    sales_brief_approved = False
    current_blocker = (
        "Missing approved sales intent for submission mode"
        if mode == "submission"
        else "Draft mode is not release-eligible"
    )
    return {
        "mode": mode,
        "promotion_state": "not-eligible",
        "sales_brief_present": sales_brief_present,
        "sales_brief_approved": sales_brief_approved,
        "release_eligible": release_eligible,
        "current_blocker": current_blocker,
        "intent_capture_mode": "none",
        "urgency": "standard",
        "promotion_path": None,
        "promotion_attestation": None,
    }


def load_run_context(project_dir: Path) -> dict[str, object]:
    run_context_path = _run_context_path(project_dir)
    if not run_context_path.exists():
        return _default_run_context()
    return json.loads(run_context_path.read_text(encoding="utf-8"))


def save_run_context(project_dir: Path, run_context: dict[str, object]) -> Path:
    run_context_path = _run_context_path(project_dir)
    run_context_path.parent.mkdir(parents=True, exist_ok=True)
    run_context_path.write_text(json.dumps(run_context, indent=2) + "\n", encoding="utf-8")
    readme_path = Path(project_dir) / "README.md"
    if readme_path.exists():
        lines = readme_path.read_text(encoding="utf-8").splitlines()
        updated: list[str] = []
        for line in lines:
            if line.startswith("Run Mode: "):
                updated.append(f"Run Mode: {run_context.get('mode', 'draft')}")
            elif line.startswith("Release Eligibility: "):
                updated.append(f"Release Eligibility: {str(run_context.get('release_eligible', False)).lower()}")
            elif line.startswith("Current Blocker: "):
                updated.append(f"Current Blocker: {run_context.get('current_blocker', '')}")
            else:
                updated.append(line)
        readme_path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    return run_context_path


def initialize_run_context(project_dir: Path, mode: str = "draft") -> dict[str, object]:
    run_context = _default_run_context(mode)
    save_run_context(project_dir, run_context)
    return run_context


def _write_readme(project_dir: Path, customer: str, title: str, created_on: date) -> None:
    run_context = load_run_context(project_dir)
    (project_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {customer} - {title}",
                f"Created: {created_on.isoformat()}",
                "",
                "## Governance",
                f"Run Mode: {run_context.get('mode', 'draft')}",
                f"Release Eligibility: {str(run_context.get('release_eligible', False)).lower()}",
                f"Current Blocker: {run_context.get('current_blocker', '')}",
                "",
                "## Status",
                "| Stage | Status | Completed |",
                "|-------|--------|-----------|",
                "| 0. Intake | pending | - |",
                "| 1. Brainstorm | pending | - |",
                "| 2. Compliance | pending | - |",
                "| 3. Architecture | pending | - |",
                "| 4. Sizing | pending | - |",
                "| 5. Pricing | pending | - |",
                "| 6. Response | pending | - |",
                "| 7. Review | pending | - |",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def scaffold_project(
    base_dir: Path,
    customer: str,
    title: str,
    created_on: date | None = None,
    mode: str = "draft",
) -> Path:
    created_on = created_on or date.today()
    project_name = f"{_slugify(customer)}--{_slugify(title)}--{created_on.isoformat()}"
    project_dir = Path(base_dir) / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    for rel_dir in PROJECT_DIRS:
        (project_dir / rel_dir).mkdir(parents=True, exist_ok=True)

    initialize_run_context(project_dir, mode=mode)
    _write_readme(project_dir, customer, title, created_on)
    return project_dir


def _validate_submission_sales_intent(project_dir: Path) -> list[str]:
    run_context = load_run_context(project_dir)
    if run_context.get("mode") != "submission":
        return []
    if run_context.get("sales_brief_present") and run_context.get("sales_brief_approved"):
        return []
    return ["Submission mode requires approved sales intent before project creation can succeed."]


def _validate_stage_governance(project_dir: Path, stage: int) -> list[str]:
    run_context = load_run_context(project_dir)
    if stage != 1:
        return []
    if run_context.get("mode") != "submission":
        return []
    if run_context.get("sales_brief_present") and run_context.get("sales_brief_approved"):
        return []
    return ["Submission mode requires approved sales intent before stage 1 can run."]


def _validate_release_governance(project_dir: Path) -> list[str]:
    run_context = load_run_context(project_dir)
    if run_context.get("mode") == "draft":
        return ["Draft mode is not release-eligible even when stage-7 quality artifacts are approved."]
    if run_context.get("mode") == "submission" and not run_context.get("sales_brief_approved"):
        return ["Submission mode requires approved sales intent before release eligibility can be granted."]
    return []


def validate_sales_brief(sales_brief_path: Path) -> dict[str, object]:
    sales_brief_path = Path(sales_brief_path)
    issues: list[str] = []
    fields: dict[str, str] = {}

    if not sales_brief_path.exists():
        return {
            "pass": False,
            "approved": False,
            "issues": ["Sales brief is missing."],
            "fields": fields,
            "path": sales_brief_path,
        }

    text = sales_brief_path.read_text(encoding="utf-8")
    for label, field_key in SALES_BRIEF_REQUIRED_FIELDS.items():
        value = _extract_markdown_label_value(text, label)
        if value is None:
            issues.append(f"Sales brief missing required field: {label}")
            continue
        fields[field_key] = value

    approved = "approved_by" in fields and "approved_date" in fields
    return {
        "pass": len(issues) == 0,
        "approved": approved,
        "issues": issues,
        "fields": fields,
        "path": sales_brief_path,
    }


def _write_sales_brief(
    project_dir: Path,
    owner: str,
    strategy: str,
    constraint: str,
    urgency: str = "standard",
    approved_by: str | None = None,
    approved_date: str | None = None,
) -> Path:
    sales_brief_path = _sales_brief_path(project_dir)
    approver = approved_by or owner
    approval_date = approved_date or date.today().isoformat()
    sales_brief_path.parent.mkdir(parents=True, exist_ok=True)
    sales_brief_path.write_text(
        "# Sales Brief\n\n"
        f"**Deal Owner:** {owner}\n"
        f"**Win Strategy:** {strategy}\n"
        f"**Constraints:** {constraint}\n"
        f"**Approved By:** {approver}\n"
        f"**Approved Date:** {approval_date}\n"
        f"**Urgency:** {urgency}\n",
        encoding="utf-8",
    )
    return sales_brief_path


def _copy_raw_inputs(raw_dir: Path, project_dir: Path) -> None:
    destination = project_dir / "input" / "raw"
    destination.mkdir(parents=True, exist_ok=True)
    for source_file in sorted(Path(raw_dir).iterdir()):
        if source_file.is_file():
            shutil.copy2(source_file, destination / source_file.name)


def _readme_row_prefix(stage: int) -> str:
    return f"| {stage}. {STAGE_NAMES[stage]} |"


def _update_readme_stage(project_dir: Path, stage: int, status: str) -> None:
    readme_path = Path(project_dir) / "README.md"
    if not readme_path.exists():
        return

    completed = datetime.now().strftime("%Y-%m-%d %H:%M") if status == "completed" else "-"
    prefix = _readme_row_prefix(stage)
    replacement = f"{prefix} {status} | {completed} |"

    lines = readme_path.read_text(encoding="utf-8").splitlines()
    updated = []
    found = False
    for line in lines:
        if line.startswith(prefix):
            updated.append(replacement)
            found = True
        else:
            updated.append(line)

    if not found:
        updated.append(replacement)

    readme_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def _path_has_content(project_dir: Path, rel_path: str) -> bool:
    candidate = Path(project_dir) / rel_path.rstrip("/")
    if rel_path.endswith("/"):
        return candidate.exists() and any(p.is_file() for p in candidate.rglob("*"))
    return candidate.exists() and candidate.is_file() and candidate.stat().st_size > 0


def _missing_stage_outputs(project_dir: Path, stage: int) -> list[str]:
    return [rel for rel in STAGE_OUTPUTS.get(stage, []) if not _path_has_content(project_dir, rel)]


def _extract_sources(file_path: Path, frontmatter: dict[str, object]) -> list[str]:
    sources = frontmatter.get("sources")
    if isinstance(sources, list):
        return [str(item) for item in sources]
    if isinstance(sources, str) and sources.strip():
        return [sources.strip()]

    lines = Path(file_path).read_text(encoding="utf-8").splitlines()
    extracted: list[str] = []
    in_sources_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("sources:"):
            in_sources_block = True
            if "[" in stripped and "]" in stripped:
                inner = stripped.split("[", 1)[1].rsplit("]", 1)[0]
                extracted.extend(part.strip() for part in inner.split(",") if part.strip())
                break
            continue
        if in_sources_block:
            if stripped.startswith("-"):
                extracted.append(stripped[1:].strip())
            else:
                break
    return extracted


def _markdown_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current_heading = line[3:].strip()
            sections[current_heading] = []
            continue
        if current_heading is not None:
            sections[current_heading].append(line)
    return {heading: "\n".join(lines).strip() for heading, lines in sections.items()}


def _find_section(sections: dict[str, str], keywords: tuple[str, ...]) -> tuple[str, str] | None:
    lowered_keywords = tuple(keyword.lower() for keyword in keywords)
    for heading, content in sections.items():
        heading_lower = heading.lower()
        if any(keyword in heading_lower for keyword in lowered_keywords):
            return heading, content
    return None


def _extract_pricing_facts(text: str) -> tuple[set[str], set[str]]:
    instance_types = set(re.findall(r"\b(?:db\.)?[cmrt]\d[a-z]?i?\.[a-z0-9]+\b", text, re.IGNORECASE))
    prices = set(re.findall(r"\$\d+(?:\.\d+)?", text))
    return instance_types, prices


def _extract_sizing_facts(text: str) -> tuple[set[str], set[str]]:
    metric_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", text))
    architecture_terms = set()
    for term in ("compute tier", "data tier", "security tier", "transaction processing"):
        if term in text.lower():
            architecture_terms.add(term)
    return metric_numbers, architecture_terms


def _validate_stage_output_metadata(project_dir: Path, stage: int) -> list[str]:
    issues: list[str] = []
    primary_output = STAGE_PRIMARY_OUTPUT.get(stage)
    if not primary_output:
        return issues

    output_path = Path(project_dir) / primary_output
    if not output_path.exists():
        return issues

    try:
        frontmatter, body = parse_file(output_path)
    except Exception as exc:
        return [f"Unable to parse {primary_output}: {exc}"]

    expected_stage = stage
    actual_stage = frontmatter.get("stage")
    if str(actual_stage) != str(expected_stage):
        issues.append(f"Invalid stage metadata in {primary_output}: expected {expected_stage}")

    expected_class = STAGE_OUTPUT_CLASS.get(stage)
    if expected_class and frontmatter.get("output_class") != expected_class:
        issues.append(f"Invalid output_class in {primary_output}: expected {expected_class}")

    if len(body.strip()) < 10:
        issues.append(f"Body content too short in {primary_output}")

    if stage == 6:
        sources = _extract_sources(output_path, frontmatter)
        missing_sources = [source for source in STAGE_6_REQUIRED_SOURCES if source not in sources]
        if missing_sources:
            issues.append(f"Stage 6 sources missing required upstream outputs: {', '.join(missing_sources)}")

        upstream_url_set: set[str] = set()
        upstream_urls_by_source: dict[str, set[str]] = {}
        for source in sources:
            source_path = Path(project_dir) / source
            if not source_path.exists():
                continue
            try:
                source_urls = {entry["url"] for entry in extract_urls_from_file(source_path)}
            except Exception:
                continue
            if source_urls:
                upstream_urls_by_source[source] = source_urls
                upstream_url_set.update(source_urls)

        response_urls = {entry["url"] for entry in extract_urls_from_file(output_path)}
        if upstream_url_set and not response_urls:
            issues.append("Stage 6 response URLs missing despite upstream evidence-backed outputs containing URLs")

        unsupported_urls = sorted(url for url in response_urls if url not in upstream_url_set)
        if unsupported_urls:
            issues.append(
                "Stage 6 response contains unsupported URLs not present in upstream outputs: "
                + ", ".join(unsupported_urls)
            )

        for source, source_urls in sorted(upstream_urls_by_source.items()):
            try:
                source_frontmatter, _ = parse_file(Path(project_dir) / source)
            except Exception:
                continue
            if source_frontmatter.get("output_class") != "evidence-backed":
                continue
            if response_urls.isdisjoint(source_urls):
                issues.append(f"Stage 6 response URLs missing citations from upstream evidence-backed source: {source}")

        sections = _markdown_sections(body)
        compliance_section = _find_section(sections, ("compliance", "security"))
        pricing_section = _find_section(sections, ("pricing", "commercial"))
        assumptions_section = _find_section(sections, ("assumption", "caveat", "gap"))

        compliance_urls = upstream_urls_by_source.get("outputs/02-compliance.md", set())
        pricing_urls = upstream_urls_by_source.get("outputs/05-pricing.md", set())

        if compliance_urls:
            if compliance_section is None:
                issues.append("Stage 6 response missing compliance section")
            elif all(url not in compliance_section[1] for url in compliance_urls):
                issues.append("Stage 6 compliance section missing upstream compliance citation")

        if pricing_urls:
            if pricing_section is None:
                issues.append("Stage 6 response missing pricing section")
            elif all(url not in pricing_section[1] for url in pricing_urls):
                issues.append("Stage 6 pricing section missing upstream pricing citation")

        infrastructure_section = _find_section(sections, ("infrastructure", "sizing"))

        pricing_output_path = Path(project_dir) / "outputs" / "05-pricing.md"
        if pricing_output_path.exists() and pricing_section is not None:
            _, pricing_body = parse_file(pricing_output_path)
            upstream_instances, upstream_prices = _extract_pricing_facts(pricing_body)
            if (upstream_instances or upstream_prices) and pricing_section is not None:
                pricing_text = pricing_section[1]
                if upstream_instances.isdisjoint(set(re.findall(r"\b(?:db\.)?[cmrt]\d[a-z]?i?\.[a-z0-9]+\b", pricing_text, re.IGNORECASE))) and upstream_prices.isdisjoint(set(re.findall(r"\$\d+(?:\.\d+)?", pricing_text))):
                    issues.append("Stage 6 pricing section missing carried pricing facts from upstream pricing output")

        sizing_output_path = Path(project_dir) / "outputs" / "04-sizing.md"
        architecture_output_path = Path(project_dir) / "outputs" / "03-architecture.md"
        sizing_text = ""
        architecture_text = ""
        if sizing_output_path.exists():
            _, sizing_text = parse_file(sizing_output_path)
        if architecture_output_path.exists():
            _, architecture_text = parse_file(architecture_output_path)
        upstream_numbers, _ = _extract_sizing_facts(sizing_text)
        _, upstream_architecture_terms = _extract_sizing_facts(architecture_text)
        if infrastructure_section is not None and (upstream_numbers or upstream_architecture_terms):
            section_text = infrastructure_section[1].lower()
            section_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", infrastructure_section[1]))
            if upstream_numbers.isdisjoint(section_numbers) and upstream_architecture_terms.isdisjoint(set(term for term in upstream_architecture_terms if term in section_text)):
                issues.append("Stage 6 infrastructure and sizing section missing carried sizing facts from upstream outputs")

        assumption_log_path = Path(project_dir) / "working" / "05-assumption-log.md"
        if assumption_log_path.exists() and assumption_log_path.read_text(encoding="utf-8").strip():
            if assumptions_section is None:
                issues.append("Stage 6 response missing assumptions section despite recorded assumptions")
            elif len(assumptions_section[1].strip()) < 10:
                issues.append("Stage 6 assumptions section is too short to surface recorded assumptions")

    return issues


def _validate_stage_7_artifacts(project_dir: Path) -> list[str]:
    issues: list[str] = []
    approval_path = Path(project_dir) / "outputs" / "07-approval.md"
    release_path = Path(project_dir) / "approvals" / "release-decision.md"
    response_path = Path(project_dir) / "outputs" / "06-response.md"
    url_report_path = Path(project_dir) / "verification" / "source-url-validation.json"
    freshness_report_path = Path(project_dir) / "verification" / "freshness-report.json"

    if approval_path.exists() and release_path.exists():
        try:
            approval_fm, _ = parse_file(approval_path)
            release_fm, _ = parse_file(release_path)
        except Exception as exc:
            return [f"Unable to parse stage 7 approval artifacts: {exc}"]

        approval_decision = str(approval_fm.get("decision", "")).strip()
        release_decision = str(release_fm.get("decision", "")).strip()
        if approval_decision and release_decision and approval_decision != release_decision:
            issues.append("Decision mismatch between outputs/07-approval.md and approvals/release-decision.md")
        if approval_decision and approval_decision != "APPROVED":
            issues.append("Release decision remains conditional; manual reviewer approval required")

    if url_report_path.exists():
        try:
            url_report = json.loads(url_report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"Invalid source URL validation report: {exc}")
        else:
            invalid = url_report.get("invalid")
            if invalid is None and "pass" in url_report:
                invalid = 0 if url_report.get("pass") else 1
            if invalid and int(invalid) > 0:
                issues.append("Source URL validation report contains invalid URLs")
            if url_report.get("manual_review_required"):
                issues.append("Source URL validation requires manual reviewer confirmation before release")

    if freshness_report_path.exists():
        try:
            freshness_report = json.loads(freshness_report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"Invalid freshness report: {exc}")
        else:
            stale = freshness_report.get("stale")
            if stale is None and "pass" in freshness_report:
                stale = 0 if freshness_report.get("pass") else 1
            if stale and int(stale) > 0:
                issues.append("Freshness report contains stale entries")

    if response_path.exists():
        _, response_body = parse_file(response_path)
        if re.search(r"\b(TODO|TBD)\b", response_body, re.IGNORECASE):
            issues.append("Final response contains placeholder text (TODO/TBD)")

    return issues


def validate_release_readiness(project_dir: Path) -> dict:
    project_dir = Path(project_dir)
    gate = check_gate(
        project_dir,
        7,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )
    issues = list(gate.get("issues", []))
    issues.extend(_validate_stage_7_artifacts(project_dir))
    issues.extend(_validate_release_governance(project_dir))
    return {
        "pass": len(gate["missing"]) == 0 and len(issues) == 0,
        "stage": 7,
        "missing": list(gate["missing"]),
        "present": list(gate["present"]),
        "issues": issues,
    }


def run_stage(
    project_dir: Path,
    stage: int,
    command: list[str] | None = None,
    allow_native_adapter: bool = False,
) -> dict:
    project_dir = Path(project_dir)
    if not project_dir.exists():
        return {
            "pass": False,
            "stage": stage,
            "gate": {"pass": False, "stage": stage, "missing": [], "present": [], "issues": []},
            "missing": [],
            "present": [],
            "issues": [f"Project directory does not exist: {project_dir}"],
            "missing_outputs": [],
            "command_executed": False,
            "command_returncode": None,
            "stdout": "",
            "stderr": "",
            "adapter_used": None,
        }
    governance_issues = _validate_stage_governance(project_dir, stage)
    gate = check_gate(
        project_dir,
        stage,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )
    result = {
        "pass": False,
        "stage": stage,
        "gate": gate,
        "missing": gate["missing"],
        "present": gate["present"],
        "issues": list(gate.get("issues", [])),
        "missing_outputs": [],
        "command_executed": False,
        "command_returncode": None,
        "stdout": "",
        "stderr": "",
        "adapter_used": None,
    }
    result["issues"].extend(governance_issues)
    if governance_issues:
        _update_readme_stage(project_dir, stage, "failed")
        return result
    if not gate["pass"]:
        _update_readme_stage(project_dir, stage, "failed")
        return result

    if command:
        try:
            completed = subprocess.run(command, cwd=str(project_dir), capture_output=True, text=True)
        except OSError as exc:
            result["issues"].append(f"Stage command could not be launched: {exc}")
        else:
            result["command_executed"] = True
            result["command_returncode"] = completed.returncode
            result["stdout"] = completed.stdout
            result["stderr"] = completed.stderr
            if completed.returncode != 0:
                result["issues"].append(f"Stage command failed with exit code {completed.returncode}")
    else:
        bridge_command = _load_stage_bridge_command(project_dir, stage)
        if bridge_command:
            try:
                completed = subprocess.run(bridge_command, cwd=str(project_dir), capture_output=True, text=True)
            except OSError as exc:
                result["adapter_used"] = "bridge"
                result["issues"].append(f"Stage bridge command could not be launched: {exc}")
            else:
                result["command_executed"] = True
                result["command_returncode"] = completed.returncode
                result["stdout"] = completed.stdout
                result["stderr"] = completed.stderr
                result["adapter_used"] = "bridge"
                if completed.returncode != 0:
                    result["issues"].append(f"Stage command failed with exit code {completed.returncode}")
        else:
            if not allow_native_adapter:
                result["issues"].append(NATIVE_ADAPTER_DISABLED_ISSUE)
            else:
                try:
                    result["adapter_used"] = run_native_stage_adapter(project_dir, stage)
                except Exception as exc:
                    result["issues"].append(f"Native stage adapter failed: {exc}")

    result["missing_outputs"] = _missing_stage_outputs(project_dir, stage)
    result["issues"].extend(_validate_stage_output_metadata(project_dir, stage))
    if stage == 7:
        result["issues"].extend(_validate_stage_7_artifacts(project_dir))

    result["pass"] = (
        result["command_returncode"] in (None, 0)
        and len(result["missing_outputs"]) == 0
        and len(result["issues"]) == 0
    )
    _update_readme_stage(project_dir, stage, "completed" if result["pass"] else "failed")
    return result


def run_pipeline(
    project_dir: Path,
    from_stage: int = 1,
    to_stage: int = 7,
    stage_commands: dict[int, list[str]] | None = None,
    allow_native_adapter: bool = False,
) -> dict:
    stage_commands = stage_commands or {}
    results = []
    for stage in range(from_stage, to_stage + 1):
        stage_result = run_stage(
            project_dir,
            stage,
            command=stage_commands.get(stage),
            allow_native_adapter=allow_native_adapter,
        )
        results.append(stage_result)
        if not stage_result["pass"]:
            return {"pass": False, "stages": results, "failed_stage": stage}
    return {"pass": True, "stages": results, "failed_stage": None}


def prepare_project_knowledge(
    project_dir: Path,
    knowledge_dir: Path,
    db_path: Path | None = None,
    knowledge_commit: str | None = None,
) -> dict:
    project_dir = Path(project_dir)
    knowledge_dir = Path(knowledge_dir)
    db_path = Path(db_path) if db_path else project_dir / "working" / "apv-v2.sqlite"

    sync_stats = sync_knowledge(knowledge_dir, db_path)
    audit_summary = audit_directory(knowledge_dir)
    snapshot = create_project_snapshot(
        project_dir,
        db_path,
        knowledge_commit=knowledge_commit,
        knowledge_dir=knowledge_dir,
    )
    gate = check_gate(
        project_dir,
        0,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )

    return {
        "sync": sync_stats,
        "audit": audit_summary,
        "snapshot": snapshot,
        "gate": gate,
        "ready": audit_summary["stale"] == 0 and audit_summary["fail"] == 0 and gate["pass"],
    }


def create_new_project(
    base_dir: Path,
    customer: str,
    title: str,
    raw_dir: Path,
    knowledge_dir: Path,
    knowledge_commit: str | None = None,
    created_on: date | None = None,
    mode: str = "draft",
) -> dict:
    project_dir = scaffold_project(base_dir, customer, title, created_on=created_on, mode=mode)
    _copy_raw_inputs(raw_dir, project_dir)
    normalize_raw_inputs(project_dir / "input" / "raw", project_dir / "input" / "normalized")
    prepared = prepare_project_knowledge(
        project_dir,
        knowledge_dir,
        knowledge_commit=knowledge_commit,
    )
    gate = check_gate(
        project_dir,
        1,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )
    prepared["project_dir"] = project_dir
    prepared["gate"] = gate
    issues = list(gate.get("issues", []))
    issues.extend(_validate_submission_sales_intent(project_dir))
    prepared["issues"] = issues
    prepared["ready"] = prepared["ready"] and gate["pass"] and len(issues) == 0
    return prepared


def dry_run_project(
    project_dir: Path,
    knowledge_dir: Path,
    db_path: Path | None = None,
    knowledge_commit: str | None = None,
) -> dict:
    project_dir = Path(project_dir)
    for rel_dir in PROJECT_DIRS:
        (project_dir / rel_dir).mkdir(parents=True, exist_ok=True)
    if not (project_dir / "README.md").exists():
        _write_readme(project_dir, project_dir.name, "Dry Run", date.today())
    return prepare_project_knowledge(project_dir, knowledge_dir, db_path=db_path, knowledge_commit=knowledge_commit)


def check_project_readiness(project_dir: Path) -> dict:
    project_dir = Path(project_dir)
    gate = check_gate(
        project_dir,
        0,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )
    return {"pass": gate["pass"], "gate": gate}


def resume_project(project_dir: Path, from_stage: int) -> dict:
    result = check_gate(
        Path(project_dir),
        from_stage,
        check_snapshot_boundary=True,
        check_commercial_override_rules=True,
    )
    run_context = load_run_context(project_dir)
    if run_context.get("mode") == "submission" and run_context.get("promotion_path") == "full-rerun" and from_stage > 1:
        result["pass"] = False
        issues = list(result.get("issues", []))
        issues.append("Submission promotion requires rerun from stage 1 before resuming downstream stages.")
        result["issues"] = issues
    return result


def promote_to_submission(
    project_dir: Path,
    owner: str,
    strategy: str,
    constraint: str,
    urgency: str = "standard",
    fast_track_attestation: str | None = None,
) -> dict[str, object]:
    project_dir = Path(project_dir)
    sales_brief_path = _write_sales_brief(project_dir, owner, strategy, constraint, urgency=urgency)
    validation = validate_sales_brief(sales_brief_path)
    if not validation["pass"]:
        return {
            "pass": False,
            "project_dir": project_dir,
            "issues": list(validation["issues"]),
            "sales_brief_path": sales_brief_path,
        }

    run_context = load_run_context(project_dir)
    promotion_path = "fast-track" if fast_track_attestation else "full-rerun"
    current_blocker = (
        "Submission fast-track recorded; release still requires remaining pipeline and approval checks"
        if fast_track_attestation
        else "Submission promotion recorded; rerun from stage 1 is required before downstream release work"
    )
    run_context.update(
        {
            "mode": "submission",
            "promotion_state": "submission-requested",
            "sales_brief_present": True,
            "sales_brief_approved": bool(validation["approved"]),
            "release_eligible": False,
            "current_blocker": current_blocker,
            "intent_capture_mode": "sales-brief",
            "urgency": urgency,
            "promotion_path": promotion_path,
            "promotion_attestation": fast_track_attestation,
        }
    )
    save_run_context(project_dir, run_context)

    return {
        "pass": True,
        "project_dir": project_dir,
        "sales_brief_path": sales_brief_path,
        "issues": [],
        "promotion_path": promotion_path,
        "rerun_required_from_stage": None if fast_track_attestation else 1,
    }


def refresh_pricing_knowledge(
    provider: str,
    knowledge_dir: Path,
    region: str = "ap-southeast-1",
    db_path: Path | None = None,
    sync: bool = False,
    check_freshness: bool = False,
) -> dict:
    knowledge_dir = Path(knowledge_dir)
    db_path = Path(db_path) if db_path else Path(__file__).parent.parent / "apv-v2.sqlite"

    if provider != "aws":
        return {
            "pass": False,
            "provider": provider,
            "issues": [f"Unsupported pricing refresh provider: {provider}"],
        }

    refresh_result = refresh_aws_pricing(knowledge_dir=knowledge_dir, region=region)
    result = {
        "pass": bool(refresh_result.get("pass")),
        "provider": provider,
        "region": region,
        "knowledge_dir": knowledge_dir,
        "refresh": refresh_result,
    }

    if sync:
        sync_result = sync_knowledge(knowledge_dir, db_path)
        result["sync"] = sync_result
        if sync_result.get("errors", 0) > 0:
            result["pass"] = False

    if check_freshness:
        freshness_result = check_domain_freshness(db_path, "pricing")
        result["freshness"] = freshness_result
        if freshness_result.get("stale", 0) > 0:
            result["pass"] = False

    return result


def route_knowledge_change(target_path: Path, knowledge_dir: Path) -> dict:
    target_path = Path(target_path)
    knowledge_dir = Path(knowledge_dir)
    resolved_target = target_path if target_path.is_absolute() else knowledge_dir.parent / target_path

    route = _resolve_generated_knowledge_route(resolved_target, knowledge_dir)
    if route is None:
        return {
            "pass": True,
            "allowed": True,
            "target_path": resolved_target,
            "knowledge_dir": knowledge_dir,
            "issues": [],
        }

    issues = ["Direct edits are blocked for generated knowledge files."]
    regenerate_command = route.get("regenerate_command")
    if not regenerate_command:
        issues.append("Regenerate this artifact through its owning workflow after updating the source of truth.")

    return {
        "pass": True,
        "allowed": False,
        "target_path": resolved_target,
        "knowledge_dir": knowledge_dir,
        "source_of_truth": route["source_of_truth"],
        "regenerate_command": regenerate_command,
        "issues": issues,
    }


def _aws_offer_loader(offer_loader=None):
    return offer_loader or _load_offer_json


def _normalize_aws_service_name(service: str) -> str:
    raw_service = str(service or "").strip()
    if not raw_service:
        return raw_service
    normalized_key = re.sub(r"[^a-z0-9]+", " ", raw_service.lower()).strip()
    collapsed_key = normalized_key.replace(" ", "")

    canonical = AWS_SERVICE_ALIASES.get(raw_service) or AWS_SERVICE_ALIASES.get(raw_service.lower())
    if canonical:
        return canonical
    canonical = AWS_SERVICE_ALIASES.get(normalized_key) or AWS_SERVICE_ALIASES.get(collapsed_key)
    if canonical:
        return canonical
    if raw_service in SERVICE_TITLES:
        return raw_service
    for known_service in SERVICE_TITLES:
        if known_service.lower() == raw_service.lower():
            return known_service
    return raw_service


def _default_entry_kind_for_aws_service(service: str) -> str:
    if service in AWS_OFFICIAL_STATIC_MANIFEST_SERVICES:
        return "official-static"
    return "public-offer"


def _normalize_component_key(component: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(component or "").lower()).strip()


def _resolve_static_component(service: str, component: str | None) -> str | None:
    if not component:
        return AWS_STATIC_DEFAULT_COMPONENTS.get(service)
    normalized_component = _normalize_component_key(component)
    aliases = AWS_STATIC_COMPONENT_ALIASES.get(service, {})
    return aliases.get(component) or aliases.get(normalized_component) or component


def _known_static_defaults(manifest: dict, service: str, component: str | None = None) -> dict | None:
    candidates = [row for row in manifest.get("official_static_rows", []) if row.get("service") == service]
    if not candidates:
        return None
    resolved_component = _resolve_static_component(service, component)
    if resolved_component is not None:
        for row in candidates:
            if row.get("component") == resolved_component:
                return row
    if len(candidates) == 1:
        return candidates[0]
    default_component = AWS_STATIC_DEFAULT_COMPONENTS.get(service)
    if default_component is not None:
        for row in candidates:
            if row.get("component") == default_component:
                return row
    return None


def _resolve_static_item_fields(
    manifest: dict,
    service: str,
    component: str | None,
    title: str | None,
    source_url: str | None,
    billing_unit: str | None,
    deployment_mode: str | None,
    pricing_model: str | None,
) -> dict | None:
    defaults = _known_static_defaults(manifest, service, component)
    if defaults is None:
        return None
    return {
        "component": _resolve_static_component(service, component) or defaults.get("component"),
        "title": title or defaults.get("title"),
        "source_url": source_url or defaults.get("source_url"),
        "billing_unit": billing_unit or defaults.get("billing_unit"),
        "deployment_mode": deployment_mode or defaults.get("deployment_mode") or "single",
        "pricing_model": pricing_model or defaults.get("pricing_model") or "on-demand",
    }


def _add_matching_commitment_rows(manifest: dict, service: str, instance_types: list[str]) -> list[str]:
    if not instance_types:
        return []
    return add_savings_plan_pattern_rows(manifest, service=service, instance_types=instance_types)


def add_pricing_item(
    provider: str,
    knowledge_dir: Path,
    service: str,
    region: str = "ap-southeast-1",
    instance_type: str | None = None,
    component: str | None = None,
    entry_kind: str = "public-offer",
    deployment_mode: str | None = None,
    pricing_model: str = "on-demand",
    title: str | None = None,
    source_url: str | None = None,
    unit_price: float | None = None,
    billing_unit: str | None = None,
    with_savings_plans: bool = False,
    refresh: bool = False,
    sync: bool = False,
    check_freshness: bool = False,
    offer_loader=None,
) -> dict:
    knowledge_dir = Path(knowledge_dir)
    if provider != "aws":
        return {"pass": False, "issues": [f"Unsupported pricing add-item provider: {provider}"]}

    service = _normalize_aws_service_name(service)
    requested_component = component
    if service == "ElastiCache" and component and not instance_type:
        instance_type = component
        component = None
    if entry_kind == "public-offer" and service in AWS_OFFICIAL_STATIC_MANIFEST_SERVICES and (component or unit_price is not None):
        if service == "ElastiCache" and instance_type:
            pass
        else:
            entry_kind = _default_entry_kind_for_aws_service(service)

    manifest = load_aws_pricing_manifest(knowledge_dir, create_if_missing=True)
    added_savings_rows: list[str] = []

    if entry_kind == "public-offer":
        if not instance_type:
            return {"pass": False, "issues": ["instance_type is required for public-offer items"]}
        offer = _aws_offer_loader(offer_loader)(service, region)
        if _extract_ondemand_price(service, offer, instance_type) is None:
            static_defaults = _resolve_static_item_fields(
                manifest,
                service,
                requested_component or instance_type,
                title,
                source_url,
                billing_unit,
                deployment_mode,
                pricing_model,
            )
            fallback_component = requested_component or instance_type
            if static_defaults and fallback_component and unit_price is not None:
                entry_kind = "official-static"
                added = add_official_static_item(
                    manifest,
                    service=service,
                    component=static_defaults["component"],
                    unit_price=unit_price,
                    billing_unit=static_defaults["billing_unit"],
                    title=static_defaults["title"],
                    source_url=static_defaults["source_url"],
                    deployment_mode=static_defaults["deployment_mode"],
                    pricing_model=static_defaults["pricing_model"],
                )
            else:
                hint = ""
                if static_defaults:
                    hint = "; retry with --unit-price to add it with known service defaults"
                return {
                    "pass": False,
                    "issues": [f"No public-offer price found for {service} {instance_type} in {region}{hint}"],
                }
        else:
            added = add_public_offer_item(
                manifest,
                service=service,
                instance_type=instance_type,
                deployment_mode=deployment_mode,
                pricing_model=pricing_model,
                title=title,
                source_url=source_url,
            )
            added_savings_rows = _add_matching_commitment_rows(manifest, service=service, instance_types=[instance_type])
    elif entry_kind == "official-static":
        resolved_static_fields = _resolve_static_item_fields(
            manifest,
            service,
            component,
            title,
            source_url,
            billing_unit,
            deployment_mode,
            pricing_model,
        )
        if resolved_static_fields is None or unit_price is None:
            return {
                "pass": False,
                "issues": ["component, title, source_url, billing_unit, and unit_price are required for official-static items"],
            }
        added = add_official_static_item(
            manifest,
            service=service,
            component=resolved_static_fields["component"],
            unit_price=unit_price,
            billing_unit=resolved_static_fields["billing_unit"],
            title=resolved_static_fields["title"],
            source_url=resolved_static_fields["source_url"],
            deployment_mode=resolved_static_fields["deployment_mode"],
            pricing_model=resolved_static_fields["pricing_model"],
        )
    else:
        return {"pass": False, "issues": [f"Unsupported add-item entry kind: {entry_kind}"]}

    manifest_path = save_aws_pricing_manifest(knowledge_dir, manifest)
    result = {
        "pass": True,
        "provider": provider,
        "service": service,
        "knowledge_dir": knowledge_dir,
        "manifest_path": manifest_path,
        "entry_kind": entry_kind,
        "added": added,
        "added_savings_plan_rows": added_savings_rows,
    }
    if refresh:
        refresh_result = refresh_pricing_knowledge(
            provider=provider,
            knowledge_dir=knowledge_dir,
            region=region,
            sync=sync,
            check_freshness=check_freshness,
        )
        result["refresh"] = refresh_result
        result["pass"] = bool(result["pass"] and refresh_result.get("pass"))
    return result


def extend_pricing_family(
    provider: str,
    knowledge_dir: Path,
    service: str,
    family: str,
    region: str = "ap-southeast-1",
    with_savings_plans: bool = False,
    refresh: bool = False,
    sync: bool = False,
    check_freshness: bool = False,
    offer_loader=None,
) -> dict:
    knowledge_dir = Path(knowledge_dir)
    if provider != "aws":
        return {"pass": False, "issues": [f"Unsupported pricing extend-family provider: {provider}"]}

    service = _normalize_aws_service_name(service)

    manifest = load_aws_pricing_manifest(knowledge_dir, create_if_missing=True)
    offer = _aws_offer_loader(offer_loader)(service, region)
    instance_types = list_public_offer_instance_types(service, offer, family=family)
    added_items: list[str] = []
    for instance_type in instance_types:
        added = add_public_offer_item(
            manifest,
            service=service,
            instance_type=instance_type,
            title=None,
        )
        if added:
            added_items.append(instance_type)
    added_savings_rows = _add_matching_commitment_rows(manifest, service=service, instance_types=instance_types)

    manifest_path = save_aws_pricing_manifest(knowledge_dir, manifest)
    result = {
        "pass": True,
        "provider": provider,
        "knowledge_dir": knowledge_dir,
        "manifest_path": manifest_path,
        "service": service,
        "family": family,
        "added_items": added_items,
        "added_savings_plan_rows": added_savings_rows,
    }
    if refresh:
        refresh_result = refresh_pricing_knowledge(
            provider=provider,
            knowledge_dir=knowledge_dir,
            region=region,
            sync=sync,
            check_freshness=check_freshness,
        )
        result["refresh"] = refresh_result
        result["pass"] = bool(result["pass"] and refresh_result.get("pass"))
    return result


def format_cli_output(
    command: str,
    pricing_command: str | None,
    result: dict,
    output_json: bool = False,
) -> str:
    if output_json:
        return json.dumps(result, indent=2, default=str)

    issues = result.get("issues") or []
    if command == "knowledge" and pricing_command == "route-change":
        lines: list[str] = []
        if result.get("allowed", True):
            lines.append("Target is not a generated knowledge artifact. No automatic reroute is required.")
        else:
            lines.append("Direct edit blocked for generated knowledge file.")

        target_path = result.get("target_path")
        if target_path:
            lines.append(f"Target: {target_path}")

        source_of_truth = result.get("source_of_truth")
        if source_of_truth:
            lines.append(f"Source of truth: {source_of_truth}")

        regenerate_command = result.get("regenerate_command")
        if regenerate_command:
            lines.append(f"Regenerate with: {regenerate_command}")

        if issues:
            lines.append("")
            lines.extend(f"Issue: {issue}" for issue in issues)
        return "\n".join(lines)

    if command == "pricing" and pricing_command == "add-item":
        lines: list[str] = []
        if result.get("pass"):
            if result.get("added"):
                lines.append("Pricing item added to the manifest.")
            else:
                lines.append("Pricing item already exists in the manifest.")
        else:
            lines.append("Pricing item update failed.")

        manifest_path = result.get("manifest_path")
        if manifest_path:
            lines.append(f"Manifest: {manifest_path}")

        added_savings_plan_rows = result.get("added_savings_plan_rows") or []
        if added_savings_plan_rows:
            lines.append("Savings Plans rows added: " + ", ".join(added_savings_plan_rows))

        refresh = result.get("refresh")
        if refresh:
            lines.append("")
            lines.append(format_cli_output("refresh-pricing", None, refresh))

        if issues:
            lines.append("")
            lines.extend(f"Issue: {issue}" for issue in issues)
        return "\n".join(lines)

    if command == "pricing" and pricing_command == "extend-family":
        lines = []
        if result.get("pass"):
            lines.append("Pricing family extension completed.")
        else:
            lines.append("Pricing family extension failed.")

        manifest_path = result.get("manifest_path")
        if manifest_path:
            lines.append(f"Manifest: {manifest_path}")

        added_items = result.get("added_items") or []
        lines.append(f"New items added: {len(added_items)}")
        if added_items:
            lines.append("Items: " + ", ".join(added_items))

        added_savings_plan_rows = result.get("added_savings_plan_rows") or []
        if added_savings_plan_rows:
            lines.append("Savings Plans rows added: " + ", ".join(added_savings_plan_rows))

        refresh = result.get("refresh")
        if refresh:
            lines.append("")
            lines.append(format_cli_output("refresh-pricing", None, refresh))

        if issues:
            lines.append("")
            lines.extend(f"Issue: {issue}" for issue in issues)
        return "\n".join(lines)

    if command == "refresh-pricing":
        provider = result.get("provider", "pricing").upper()
        region = result.get("region")
        lines = []
        if result.get("pass"):
            lines.append(f"{provider} pricing refresh succeeded for {region}.")
        else:
            lines.append(f"{provider} pricing refresh failed for {region}.")

        refresh = result.get("refresh") or result
        if refresh.get("generated_rows") is not None:
            lines.append(f"Generated rows: {refresh['generated_rows']}")

        verification_summary = refresh.get("verification_summary") or {}
        if verification_summary:
            lines.append(
                "Verification mix: "
                f"public-offer={verification_summary.get('public-offer', 0)}, "
                f"formula={verification_summary.get('formula', 0)}, "
                f"official-page={verification_summary.get('official-page', 0)}"
            )

        sync = result.get("sync")
        if sync:
            lines.append(f"Indexed files: {sync.get('indexed', 0)}")
            lines.append(f"Sync errors: {sync.get('errors', 0)}")

        freshness = result.get("freshness")
        if freshness:
            lines.append(f"Stale pricing pages: {freshness.get('stale', 0)}")

        if issues:
            lines.append("")
            lines.extend(f"Issue: {issue}" for issue in issues)
        return "\n".join(lines)

    if command == "promote-to-submission":
        lines = []
        if result.get("pass"):
            lines.append("Project promoted to submission mode.")
            sales_brief_path = result.get("sales_brief_path")
            if sales_brief_path:
                lines.append(f"Sales brief: {sales_brief_path}")
            if result.get("rerun_required_from_stage") is not None:
                lines.append(f"Rerun required from stage {result['rerun_required_from_stage']}.")
            else:
                lines.append("Fast-track promotion recorded.")
        else:
            lines.append("Submission promotion failed.")

        if issues:
            lines.append("")
            lines.extend(f"Issue: {issue}" for issue in issues)
        return "\n".join(lines)

    if issues:
        return "\n".join(["Command failed.", *(f"Issue: {issue}" for issue in issues)])
    return json.dumps(result, indent=2, default=str)


def main() -> int:
    repo_root = Path(__file__).parent.parent
    parser = argparse.ArgumentParser(description="APV V2 orchestrator entrypoint")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output JSON instead of a human-readable summary")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new APV project and prepare it")
    new_parser.add_argument("customer")
    new_parser.add_argument("title")
    new_parser.add_argument("--base-dir", type=Path, default=repo_root / "apv-projects")
    new_parser.add_argument("--raw-dir", type=Path, required=True)
    new_parser.add_argument("--knowledge-dir", type=Path, default=repo_root / "knowledge")
    new_parser.add_argument("--knowledge-commit")
    new_parser.add_argument("--mode", choices=["draft", "submission"], default="draft")

    promote_parser = subparsers.add_parser("promote-to-submission", help="Promote a draft project into submission mode")
    promote_parser.add_argument("--project", type=Path, required=True)
    promote_parser.add_argument("--owner", required=True)
    promote_parser.add_argument("--strategy", required=True)
    promote_parser.add_argument("--constraint", required=True)
    promote_parser.add_argument("--urgency", default="standard")
    promote_parser.add_argument("--fast-track-attestation")

    dry_run_parser = subparsers.add_parser("dry-run", help="Prepare knowledge and snapshot state for a project")
    dry_run_parser.add_argument("--project", type=Path, required=True)
    dry_run_parser.add_argument("--knowledge-dir", type=Path, required=True)
    dry_run_parser.add_argument("--db", type=Path)
    dry_run_parser.add_argument("--knowledge-commit")

    resume_parser = subparsers.add_parser("resume", help="Validate stage readiness before resume")
    resume_parser.add_argument("--project", type=Path, required=True)
    resume_parser.add_argument("--from-stage", type=int, required=True)

    run_stage_parser = subparsers.add_parser("run-stage", help="Run a single stage and verify its outputs")
    run_stage_parser.add_argument("--project", type=Path, required=True)
    run_stage_parser.add_argument("--stage", type=int, required=True)
    run_stage_parser.add_argument("--allow-native-adapters", action="store_true")
    run_stage_parser.add_argument("stage_command", nargs=argparse.REMAINDER)

    run_pipeline_parser = subparsers.add_parser("run-pipeline", help="Run a sequence of stages with optional commands")
    run_pipeline_parser.add_argument("--project", type=Path, required=True)
    run_pipeline_parser.add_argument("--from-stage", type=int, default=1)
    run_pipeline_parser.add_argument("--to-stage", type=int, default=7)
    run_pipeline_parser.add_argument("--allow-native-adapters", action="store_true")
    run_pipeline_parser.add_argument("--commands-file", type=Path)

    refresh_pricing_parser = subparsers.add_parser("refresh-pricing", help="Refresh pricing knowledge through the repo-owned workflow")
    refresh_pricing_parser.add_argument("--provider", default="aws")
    refresh_pricing_parser.add_argument("--knowledge-dir", type=Path, default=Path(__file__).parent.parent / "knowledge")
    refresh_pricing_parser.add_argument("--region", default="ap-southeast-1")
    refresh_pricing_parser.add_argument("--db-path", type=Path, default=Path(__file__).parent.parent / "apv-v2.sqlite")
    refresh_pricing_parser.add_argument("--sync", action="store_true")
    refresh_pricing_parser.add_argument("--check-freshness", action="store_true")

    knowledge_parser = subparsers.add_parser("knowledge", help="Route generated knowledge changes back to source-of-truth workflows")
    knowledge_subparsers = knowledge_parser.add_subparsers(dest="knowledge_command", required=True)

    route_change_parser = knowledge_subparsers.add_parser("route-change", help="Resolve a knowledge target to its source artifact and regeneration command")
    route_change_parser.add_argument("--knowledge-dir", type=Path, default=Path(__file__).parent.parent / "knowledge")
    route_change_parser.add_argument("--target", type=Path, required=True)

    pricing_parser = subparsers.add_parser("pricing", help="Mutate the pricing manifest through repo-owned commands")
    pricing_subparsers = pricing_parser.add_subparsers(dest="pricing_command", required=True)

    add_item_parser = pricing_subparsers.add_parser("add-item", help="Add one pricing item to the AWS pricing manifest")
    add_item_parser.add_argument("--provider", default="aws")
    add_item_parser.add_argument("--knowledge-dir", type=Path, default=Path(__file__).parent.parent / "knowledge")
    add_item_parser.add_argument("--region", default="ap-southeast-1")
    add_item_parser.add_argument("--service", required=True)
    add_item_parser.add_argument("--entry-kind", default="public-offer", choices=["public-offer", "official-static"])
    add_item_parser.add_argument("--instance-type")
    add_item_parser.add_argument("--component")
    add_item_parser.add_argument("--deployment-mode")
    add_item_parser.add_argument("--pricing-model", default="on-demand")
    add_item_parser.add_argument("--title")
    add_item_parser.add_argument("--source-url")
    add_item_parser.add_argument("--unit-price", type=float)
    add_item_parser.add_argument("--billing-unit")
    add_item_parser.add_argument("--with-savings-plans", action="store_true")
    add_item_parser.add_argument("--refresh", action="store_true")
    add_item_parser.add_argument("--sync", action="store_true")
    add_item_parser.add_argument("--check-freshness", action="store_true")

    extend_family_parser = pricing_subparsers.add_parser("extend-family", help="Add all matching public-offer items for a family to the AWS pricing manifest")
    extend_family_parser.add_argument("--provider", default="aws")
    extend_family_parser.add_argument("--knowledge-dir", type=Path, default=Path(__file__).parent.parent / "knowledge")
    extend_family_parser.add_argument("--region", default="ap-southeast-1")
    extend_family_parser.add_argument("--service", required=True)
    extend_family_parser.add_argument("--family", required=True)
    extend_family_parser.add_argument("--with-savings-plans", action="store_true")
    extend_family_parser.add_argument("--refresh", action="store_true")
    extend_family_parser.add_argument("--sync", action="store_true")
    extend_family_parser.add_argument("--check-freshness", action="store_true")

    args = parser.parse_args()

    if args.command == "new":
        result = create_new_project(
            base_dir=args.base_dir,
            customer=args.customer,
            title=args.title,
            raw_dir=args.raw_dir,
            knowledge_dir=args.knowledge_dir,
            knowledge_commit=args.knowledge_commit,
            mode=args.mode,
        )
    elif args.command == "promote-to-submission":
        result = promote_to_submission(
            project_dir=args.project,
            owner=args.owner,
            strategy=args.strategy,
            constraint=args.constraint,
            urgency=args.urgency,
            fast_track_attestation=args.fast_track_attestation,
        )
    elif args.command == "dry-run":
        result = dry_run_project(
            project_dir=args.project,
            knowledge_dir=args.knowledge_dir,
            db_path=args.db,
            knowledge_commit=args.knowledge_commit,
        )
    elif args.command == "run-stage":
        stage_command = args.stage_command
        if stage_command and stage_command[0] == "--":
            stage_command = stage_command[1:]
        result = run_stage(
            project_dir=args.project,
            stage=args.stage,
            command=stage_command or None,
            allow_native_adapter=args.allow_native_adapters,
        )
    elif args.command == "run-pipeline":
        stage_commands = None
        if args.commands_file:
            payload = json.loads(args.commands_file.read_text(encoding="utf-8"))
            stage_commands = {int(stage): command for stage, command in payload.items()}
        result = run_pipeline(
            project_dir=args.project,
            from_stage=args.from_stage,
            to_stage=args.to_stage,
            stage_commands=stage_commands,
            allow_native_adapter=args.allow_native_adapters,
        )
    elif args.command == "refresh-pricing":
        result = refresh_pricing_knowledge(
            provider=args.provider,
            knowledge_dir=args.knowledge_dir,
            region=args.region,
            db_path=args.db_path,
            sync=args.sync,
            check_freshness=args.check_freshness,
        )
    elif args.command == "knowledge" and args.knowledge_command == "route-change":
        result = route_knowledge_change(
            target_path=args.target,
            knowledge_dir=args.knowledge_dir,
        )
    elif args.command == "pricing" and args.pricing_command == "add-item":
        result = add_pricing_item(
            provider=args.provider,
            knowledge_dir=args.knowledge_dir,
            service=args.service,
            region=args.region,
            instance_type=args.instance_type,
            component=args.component,
            entry_kind=args.entry_kind,
            deployment_mode=args.deployment_mode,
            pricing_model=args.pricing_model,
            title=args.title,
            source_url=args.source_url,
            unit_price=args.unit_price,
            billing_unit=args.billing_unit,
            with_savings_plans=args.with_savings_plans,
            refresh=args.refresh,
            sync=args.sync,
            check_freshness=args.check_freshness,
        )
    elif args.command == "pricing" and args.pricing_command == "extend-family":
        result = extend_pricing_family(
            provider=args.provider,
            knowledge_dir=args.knowledge_dir,
            service=args.service,
            family=args.family,
            region=args.region,
            with_savings_plans=args.with_savings_plans,
            refresh=args.refresh,
            sync=args.sync,
            check_freshness=args.check_freshness,
        )
    else:
        result = resume_project(project_dir=args.project, from_stage=args.from_stage)

    subcommand = getattr(args, "pricing_command", None) or getattr(args, "knowledge_command", None)
    print(format_cli_output(args.command, subcommand, result, output_json=args.output_json))
    return 0 if result.get("ready", result.get("pass", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
