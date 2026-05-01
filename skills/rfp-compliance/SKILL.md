---
name: rfp-compliance
description: Stage 2 — Map RFP requirements to compliance regulations with evidence-backed citations
version: 2.0
created: 2026-05-01
tags: [apv, v2, compliance, stage-2]
output_class: evidence-backed
---

# RFP Compliance Mapping (Stage 2)

## Purpose

Map RFP requirements to applicable compliance regulations (PCI-DSS, country-specific data protection, financial regulations). Every claim must cite a source URL — no unsupported assertions.

**Output class: `evidence-backed`** — all claims must reference verified `source_url` entries.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 2`

Required:
- `outputs/01-brainstorm.md`
- `input/normalized/requirements-summary.md`

## Process

### 1. Read Upstream Context
- `outputs/01-brainstorm.md` — target regions, business type, compliance needs
- `input/normalized/requirements-summary.md` — explicit customer requirements

### 2. Identify Applicable Frameworks
Based on regions and business type:
- **Always**: PCI-DSS v4.0 (if handling card data)
- **Per-country**: data protection (PDPA variants), financial regulations, cybersecurity laws
- Read from: `knowledge/compliance/pci-dss/` and `knowledge/compliance/countries/[CC]/`

### 3. Map Requirements to Regulations
For each customer requirement:
1. Identify the applicable regulation(s)
2. Find the specific requirement/section
3. Extract the `source_url` from knowledge frontmatter
4. Document the compliance mapping

### 4. Generate Evidence Artifacts
For each compliance claim:
- Create evidence reference in `evidence/compliance/`
- Link source URL to the specific regulation document
- Note any gaps where source URLs are missing

### 5. Log Gaps
If regulations are referenced but no knowledge page exists:
- Append to `working/00-gap-log.md`
- Set severity: BLOCKER (if missing PCI-DSS), HIGH (if missing country reg), LOW (if advisory)

## Outputs

### Primary Output: `outputs/02-compliance.md`
```markdown
---
output_class: evidence-backed
stage: 2
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
---

# Compliance Mapping: [Customer]

## Applicable Frameworks

| Framework | Scope | Source |
|-----------|-------|--------|
| PCI-DSS v4.0 | Card data handling | [source_url] |
| Singapore PDPA | Personal data in SG | [source_url] |
| MAS TRM | Technology risk in SG | [source_url] |

## Requirement-to-Regulation Map

### [Customer Requirement 1]
- **PCI-DSS Req 1**: Network security controls — [source_url]
- **MAS TRM 5.1**: Network architecture — [source_url]
- **Implementation**: [how to satisfy both]

### [Customer Requirement 2]
...

## Compliance Gaps
| Gap | Severity | Impact |
|-----|----------|--------|
| [description] | HIGH | [what this blocks] |

## Evidence References
- `evidence/compliance/pci-dss-mapping.md`
- `evidence/compliance/[country]-regulations.md`
```

### Working Artifact: `working/02-compliance-map.md`
Detailed mapping table with all regulation cross-references.

## Source URL Enforcement

**MANDATORY**: Every compliance claim MUST include a `source_url`.
- If a knowledge page has `source_url` in frontmatter → use it
- If no `source_url` available → mark claim as UNVERIFIED, log to gap log
- NEVER fabricate or guess URLs

## Knowledge Sources

- `knowledge/compliance/pci-dss/*.md` — 13 PCI-DSS requirement files
- `knowledge/compliance/countries/[CC]/*.md` — 7 countries × 3-4 regulations each
- `apv-v2.sqlite` — indexed compliance table for fast lookup

## Integration

- **Upstream**: `rfp-brainstorm` (Stage 1)
- **Downstream**: `rfp-architect` (Stage 3) uses compliance constraints for architecture decisions
