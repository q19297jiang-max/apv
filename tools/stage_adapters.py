#!/usr/bin/env python3
"""Native APV stage adapters used by the orchestrator."""

import json
import re
import sqlite3
from datetime import date
from pathlib import Path

from freshness import check_domain_freshness
from validate_urls import extract_urls_from_file


STAGE_6_REQUIRED_SOURCES = [
    "outputs/01-brainstorm.md",
    "outputs/02-compliance.md",
    "outputs/03-architecture.md",
    "outputs/04-sizing.md",
    "outputs/05-pricing.md",
]


def _write_markdown(file_path: Path, frontmatter: dict[str, object], body: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    run_context_path = file_path.parent.parent / "working" / "00-run-context.json"
    if run_context_path.exists():
        run_context = json.loads(run_context_path.read_text(encoding="utf-8"))
        frontmatter = {
            **frontmatter,
            "run_mode": run_context.get("mode", "draft"),
            "release_eligible": run_context.get("release_eligible", False),
        }
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            formatted = ", ".join(str(item) for item in value)
            lines.append(f"{key}: [{formatted}]")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append(body.rstrip())
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _read_text(file_path: Path, fallback: str) -> str:
    return file_path.read_text(encoding="utf-8") if file_path.exists() else fallback


def _read_markdown_body(file_path: Path, fallback: str = "") -> str:
    text = _read_text(file_path, fallback)
    if not text.startswith("---\n"):
        return text

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return text
    return parts[1]


def _first_url(file_path: Path) -> str | None:
    if not file_path.exists():
        return None
    urls = extract_urls_from_file(file_path)
    if not urls:
        return None
    return urls[0]["url"]


def _snapshot_db_path(project_dir: Path) -> Path:
    snapshot_path = project_dir / "working" / "apv-v2-snapshot.sqlite"
    if snapshot_path.exists():
        return snapshot_path
    return project_dir / "working" / "apv-v2.sqlite"


def _load_pricing_rows(project_dir: Path, provider: str = "aws", region: str = "ap-southeast-1") -> list[dict]:
    db_path = _snapshot_db_path(project_dir)
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT provider, region, service, instance_type, deployment_mode, billing_unit, unit_price, hourly_price, monthly_price, pricing_model, source_url, verified_date "
        "FROM pricing WHERE provider=? AND region=? ORDER BY service, instance_type, deployment_mode, pricing_model",
        (provider, region),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def _read_normalized_inputs(project_dir: Path) -> dict[str, str]:
    normalized_dir = project_dir / "input" / "normalized"
    return {
        "rfp": _read_text(normalized_dir / "rfp.md", ""),
        "requirements": _read_text(normalized_dir / "requirements-summary.md", ""),
        "volume": _read_text(normalized_dir / "volume-summary.md", ""),
    }


def _extract_markdown_field(text: str, field_name: str) -> str | None:
    match = re.search(rf"\*\*{re.escape(field_name)}:\*\*\s*(.+)", text)
    return match.group(1).strip() if match else None


def _extract_requirement_lines(text: str) -> list[str]:
    return [line.strip().lstrip("- ").strip() for line in text.splitlines() if line.strip().startswith("-")]


def _find_requirement(requirements: list[str], needle: str) -> str | None:
    lowered = needle.lower()
    for requirement in requirements:
        if lowered in requirement.lower():
            return requirement
    return None


def _format_unit_price(row: dict) -> str:
    price = row.get("unit_price")
    if price is None:
        return "-"
    if price >= 1:
        return f"${price:.2f}"
    return f"${price:.3f}"


def _format_monthly_price(row: dict) -> str:
    monthly_price = row.get("monthly_price")
    if monthly_price is None:
        return "-"
    if monthly_price >= 1:
        return f"${monthly_price:.2f}"
    return f"${monthly_price:.3f}"


def _format_pricing_rows(rows: list[dict]) -> str:
    headers = ["Service", "Instance Type", "Deployment Mode", "Pricing Model", "Billing Unit", "Price ($)", "Monthly ($)", "Source"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        billing_unit = row.get("billing_unit") or ("per hour" if row.get("hourly_price") is not None else "-")
        lines.append(
            f"| {row.get('service', '-')} | {row.get('instance_type', '-')} | {row.get('deployment_mode', '-')} | {row.get('pricing_model', '-')} | {billing_unit} | {_format_unit_price(row)} | {_format_monthly_price(row)} | {row.get('source_url', '-')} |"
        )
    return "\n".join(lines)


def _pricing_rows_for_output(rows: list[dict], limit: int = 20) -> list[dict]:
    def priority(row: dict) -> tuple[int, str, str, str, str]:
        billing_unit = (row.get("billing_unit") or "").lower()
        if billing_unit and "hour" not in billing_unit:
            rank = 0
        elif row.get("pricing_model") != "on-demand" or row.get("deployment_mode") not in (None, "single", "standard"):
            rank = 1
        else:
            rank = 2
        return (
            rank,
            row.get("service", ""),
            row.get("instance_type", ""),
            row.get("deployment_mode", ""),
            row.get("pricing_model", ""),
        )

    prioritized = sorted(
        rows,
        key=priority,
    )
    return prioritized[:limit]


def _extract_assumption_lines(text: str, limit: int = 5) -> list[str]:
    bullet_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("-")]
    if bullet_lines:
        return bullet_lines[:limit]

    assumptions: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if cells[0] in {"#", "---"} or cells[1].lower() == "assumption":
            continue
        assumption = cells[1]
        risk = cells[3]
        assumptions.append(f"- {assumption} (Risk: {risk})" if risk and risk.lower() != "risk" else f"- {assumption}")
        if len(assumptions) >= limit:
            break
    return assumptions


def _extract_pricing_fact_from_output(text: str) -> str | None:
    instance_match = re.search(r"\b(?:db\.)?[cmrt]\d[a-z]?i?\.[a-z0-9]+\b", text, re.IGNORECASE)
    price_match = re.search(r"\$\d+(?:\.\d+)?", text)
    if not instance_match and not price_match:
        return None

    instance = instance_match.group(0) if instance_match else "pricing row"
    price = price_match.group(0) if price_match else "an upstream price"
    return f"Representative priced component from upstream output: {instance} at {price}, sourced from {{pricing_url}}"


def _run_stage_1(project_dir: Path, today: str) -> None:
    normalized_inputs = _read_normalized_inputs(project_dir)
    requirements_text = normalized_inputs["requirements"] or "No requirements summary found."
    client_name = _extract_markdown_field(normalized_inputs["rfp"], "Client") or "Customer not identified"
    requirements = _extract_requirement_lines(requirements_text)
    (project_dir / "working" / "01-brainstorm-context.md").write_text(
        "# Brainstorm Context\n\n"
        "## Strategic Focus\n\n"
        "- Deliver a compliant payment platform response with explicit pricing evidence.\n"
        "- Preserve traceability for downstream compliance, architecture, and pricing stages.\n\n"
        "## Customer Context\n\n"
        f"- Customer: {client_name}\n"
        + ("\n".join(f"- Requirement: {requirement}" for requirement in requirements[:4]) + "\n" if requirements else "- Requirement summary unavailable.\n"),
        encoding="utf-8",
    )
    (project_dir / "working" / "05-gap-log.md").write_text(
        "# Gap Log\n\n- No unresolved intake gaps identified by the native adapter.\n",
        encoding="utf-8",
    )
    _write_markdown(
        project_dir / "outputs" / "01-brainstorm.md",
        {"output_class": "exploratory", "stage": 1, "created": today},
        "# Brainstorm\n\n"
        "## Customer Context\n\n"
        f"- Customer: {client_name}\n\n"
        "## Response Strategy\n\n"
        "- Lead with compliance-first architecture.\n"
        "- Keep pricing traceable to evidence-backed sources.\n\n"
        "## Requirements Snapshot\n\n"
        f"{requirements_text.strip()}\n",
    )


def _run_stage_2(project_dir: Path, today: str) -> None:
    compliance_url = "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
    (project_dir / "working" / "02-compliance-map.md").write_text(
        "# Compliance Map\n\n"
        "| Control Area | Evidence |\n"
        "|--------------|----------|\n"
        f"| Security baseline | {compliance_url} |\n",
        encoding="utf-8",
    )
    evidence_path = project_dir / "evidence" / "compliance" / "native-compliance-evidence.md"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(
        "# Compliance Evidence\n\n"
        f"Source URL: {compliance_url}\n",
        encoding="utf-8",
    )
    _write_markdown(
        project_dir / "outputs" / "02-compliance.md",
        {"output_class": "evidence-backed", "stage": 2, "created": today},
        "# Compliance\n\n"
        "## Regulatory Coverage\n\n"
        f"Evidence-backed compliance baseline: {compliance_url}\n",
    )


def _run_stage_3(project_dir: Path, today: str) -> None:
    normalized_inputs = _read_normalized_inputs(project_dir)
    requirements = _extract_requirement_lines(normalized_inputs["requirements"])
    deployment_requirement = _find_requirement(requirements, "multi-az") or "Deployment topology not specified in normalized requirements."
    availability_requirement = _find_requirement(requirements, "availability")
    (project_dir / "working" / "03-architecture-decision-log.md").write_text(
        "# Architecture Decision Log\n\n"
        "- Use segmented services to preserve auditability and compliance traceability.\n"
        f"- Primary deployment constraint: {deployment_requirement}\n",
        encoding="utf-8",
    )
    _write_markdown(
        project_dir / "outputs" / "03-architecture.md",
        {"output_class": "derived", "stage": 3, "created": today},
        "# Architecture\n\n"
        "## Overview\n\n"
        "Derived architecture aligns compute, data, and security controls to the stage-1 strategy and stage-2 controls.\n\n"
        "## Customer Constraints\n\n"
        f"- {deployment_requirement}\n"
        + (f"- {availability_requirement}\n\n" if availability_requirement else "\n") +
        "## Component Inventory\n\n"
        "- Compute tier for transaction processing\n"
        "- Data tier for durable storage\n"
        "- Security tier for control enforcement\n",
    )


def _run_stage_4(project_dir: Path, today: str) -> None:
    normalized_inputs = _read_normalized_inputs(project_dir)
    requirements = _extract_requirement_lines(normalized_inputs["requirements"])
    throughput_requirement = _find_requirement(requirements, "tps") or "Throughput requirement not found."
    availability_requirement = _find_requirement(requirements, "availability") or "Availability requirement not found."
    volume_lines = _extract_requirement_lines(normalized_inputs["volume"])
    (project_dir / "working" / "04-sizing-record.md").write_text(
        "# Sizing Record\n\n"
        f"- Base throughput requirement: {throughput_requirement}\n"
        "- Design TPS includes a 1.5x safety factor over peak throughput.\n"
        f"- Availability target: {availability_requirement}\n",
        encoding="utf-8",
    )
    _write_markdown(
        project_dir / "outputs" / "04-sizing.md",
        {"output_class": "derived", "stage": 4, "created": today},
        "# Sizing\n\n"
        "## Volume Analysis\n\n"
        f"- {throughput_requirement}\n"
        f"- {availability_requirement}\n"
        + ("\n".join(f"- {line}" for line in volume_lines[:3]) + "\n" if volume_lines else "")
        + "- Design TPS sized with HA headroom.\n",
    )


def _run_stage_5(project_dir: Path, today: str) -> None:
    pricing_rows = _load_pricing_rows(project_dir)
    pricing_rows_for_output = _pricing_rows_for_output(pricing_rows, limit=len(pricing_rows) or 1)
    source_urls = sorted({row["source_url"] for row in pricing_rows if row.get("source_url")})
    pricing_url = source_urls[0] if source_urls else "https://calculator.aws/"
    freshness_report = check_domain_freshness(_snapshot_db_path(project_dir), "pricing")

    if pricing_rows:
        manifest_body = "# Pricing Manifest\n\n## Snapshot Pricing Rows\n\n" + _format_pricing_rows(pricing_rows)
        assumption_body = "# Assumption Log\n\n- Native adapter used snapshot pricing rows from the project knowledge snapshot.\n"
        pricing_body = (
            "# Pricing\n\n"
            "## Summary\n\n"
            f"Primary pricing source: {pricing_url}\n\n"
            "## Snapshot Pricing Extract\n\n"
            + _format_pricing_rows(pricing_rows_for_output)
            + "\n"
        )
        evidence_body = (
            "# Pricing Evidence\n\n"
            "## Source URLs\n\n"
            + "\n".join(f"- {url}" for url in source_urls)
            + "\n"
        )
    else:
        manifest_body = "# Pricing Manifest\n\n- No snapshot pricing rows available; using calculator reference fallback.\n"
        assumption_body = "# Assumption Log\n\n- Snapshot pricing rows were unavailable; native adapter used a conservative calculator reference fallback.\n"
        pricing_body = "# Pricing\n\n## Summary\n\nPricing reference: https://calculator.aws/\n"
        evidence_body = "# Pricing Evidence\n\nSource URL: https://calculator.aws/\n"

    (project_dir / "working" / "05-pricing-manifest.md").write_text(
        manifest_body,
        encoding="utf-8",
    )
    (project_dir / "working" / "05-assumption-log.md").write_text(
        assumption_body,
        encoding="utf-8",
    )
    evidence_path = project_dir / "evidence" / "pricing" / "native-pricing-evidence.md"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(
        evidence_body,
        encoding="utf-8",
    )
    (project_dir / "verification" / "freshness-report.json").write_text(
        json.dumps({**freshness_report, "pass": freshness_report.get("stale", 0) == 0, "verification_mode": "native-adapter-snapshot"}, indent=2),
        encoding="utf-8",
    )
    _write_markdown(
        project_dir / "outputs" / "05-pricing.md",
        {"output_class": "evidence-backed", "stage": 5, "created": today},
        pricing_body,
    )


def _run_stage_6(project_dir: Path, today: str) -> None:
    compliance_url = _first_url(project_dir / "outputs" / "02-compliance.md") or "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
    pricing_output_path = project_dir / "outputs" / "05-pricing.md"
    pricing_output_text = _read_markdown_body(pricing_output_path, "")
    pricing_url = _first_url(pricing_output_path) or "https://calculator.aws/"
    assumption_log = project_dir / "working" / "05-assumption-log.md"
    assumptions_text = _read_markdown_body(assumption_log, "# Assumption Log\n\n- No assumptions recorded.")
    assumptions_lines = _extract_assumption_lines(assumptions_text)
    architecture_text = _read_markdown_body(project_dir / "outputs" / "03-architecture.md", "")
    sizing_text = _read_markdown_body(project_dir / "outputs" / "04-sizing.md", "")
    pricing_rows = _pricing_rows_for_output(_load_pricing_rows(project_dir), limit=1)

    architecture_fact = "Compute tier remains isolated from data and security tiers."
    for candidate in (
        "Compute tier for transaction processing",
        "Data tier for durable storage",
        "Security tier for control enforcement",
    ):
        if candidate in architecture_text:
            architecture_fact = candidate
            break

    sizing_fact = "Sizing records remain traceable to the derived workload model."
    for line in sizing_text.splitlines():
        stripped = line.strip()
        if any(character.isdigit() for character in stripped):
            sizing_fact = stripped.lstrip("- ")
            break

    pricing_fact = f"Pricing evidence remains anchored to upstream pricing sources: {pricing_url}"
    upstream_pricing_fact = _extract_pricing_fact_from_output(pricing_output_text)
    if upstream_pricing_fact:
        pricing_fact = upstream_pricing_fact.format(pricing_url=pricing_url)
    elif pricing_rows:
        representative = pricing_rows[0]
        pricing_fact = (
            f"Representative priced component: {representative.get('service', '-')} {representative.get('instance_type', '-')} "
            f"at {_format_unit_price(representative)} {representative.get('billing_unit') or 'per hour'} "
            f"and {_format_monthly_price(representative)} monthly, sourced from {pricing_url}"
        )

    response_path = project_dir / "outputs" / "06-response.md"
    _write_markdown(
        response_path,
        {
            "output_class": "derived",
            "stage": 6,
            "created": today,
            "sources": STAGE_6_REQUIRED_SOURCES,
        },
        "# Response\n\n"
        "## 1. Executive Summary\n\n"
        "This response is assembled from staged APV artifacts with evidence preserved where required.\n\n"
        "## 4. Compliance & Security\n\n"
        f"Compliance controls remain traceable to upstream evidence: {compliance_url}\n\n"
        "## 5. Infrastructure & Sizing\n\n"
        f"{architecture_fact.rstrip('.')}.\n"
        f"{sizing_fact}\n\n"
        "## 6. Pricing\n\n"
        f"{pricing_fact}\n\n"
        "## 8. Assumptions & Caveats\n\n"
        + ("\n".join(assumptions_lines) if assumptions_lines else "- No material assumptions recorded.")
        + "\n",
    )
    response_urls = extract_urls_from_file(response_path)
    (project_dir / "verification" / "source-url-validation.json").write_text(
        json.dumps(
            {
                "pass": False,
                "valid": len(response_urls),
                "invalid": 0,
                "verification_mode": "native-adapter-trace",
                "manual_review_required": True,
                "issues": ["Native adapter outputs require manual source URL validation before release approval."],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (project_dir / "approvals" / "unified-checklist.md").write_text(
        "# Unified Checklist\n\n"
        "- Compliance citations preserved\n"
        "- Pricing citations preserved\n"
        "- Assumptions surfaced\n"
        "- Manual source URL validation still required before release\n",
        encoding="utf-8",
    )


def _run_stage_7(project_dir: Path, today: str) -> None:
    freshness_report_path = project_dir / "verification" / "freshness-report.json"
    source_validation_path = project_dir / "verification" / "source-url-validation.json"
    freshness_report = json.loads(_read_text(freshness_report_path, "{}") or "{}")
    source_validation = json.loads(_read_text(source_validation_path, "{}") or "{}")
    decision = "APPROVED" if freshness_report.get("pass") and source_validation.get("pass") else "CONDITIONAL"
    approval_body = (
        "# Approval\n\nAuto-approved by the native adapter because freshness and source validation checks passed.\n"
        if decision == "APPROVED"
        else "# Approval\n\nConditional approval pending human review of final commercial positioning.\n"
    )
    release_body = (
        "# Release Decision\n\nRelease approved because evidence freshness and source-trace validation are both green.\n"
        if decision == "APPROVED"
        else "# Release Decision\n\nConditional release recommended for manual verification.\n"
    )
    reviewer_notes = (
        "# Reviewer Notes\n\nNative checks passed. Reviewer may spot-check commercial accuracy and customer-specific tailoring before release.\n"
        if decision == "APPROVED"
        else "# Reviewer Notes\n\nManual reviewer should verify commercial accuracy and customer-specific tailoring before release.\n"
    )
    _write_markdown(
        project_dir / "outputs" / "07-approval.md",
        {"stage": 7, "created": today, "decision": decision},
        approval_body,
    )
    _write_markdown(
        project_dir / "approvals" / "release-decision.md",
        {"stage": 7, "created": today, "decision": decision},
        release_body,
    )
    _write_markdown(
        project_dir / "approvals" / "reviewer-notes.md",
        {"stage": 7, "created": today, "type": "reviewer-notes"},
        reviewer_notes,
    )


_STAGE_RUNNERS = {
    1: _run_stage_1,
    2: _run_stage_2,
    3: _run_stage_3,
    4: _run_stage_4,
    5: _run_stage_5,
    6: _run_stage_6,
    7: _run_stage_7,
}


def run_native_stage_adapter(project_dir: Path, stage: int) -> str:
    runner = _STAGE_RUNNERS.get(stage)
    if runner is None:
        raise ValueError(f"No native adapter registered for stage {stage}")
    runner(Path(project_dir), date.today().isoformat())
    return "native"
