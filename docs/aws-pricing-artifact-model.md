---
type: apv-meta
category: design
title: "APV V2 AWS Pricing Artifact Model"
created: 2026-04-29
tags: [apv, v2, aws, pricing, evidence]
---

# APV V2 AWS Pricing Artifact Model

## Goal

Define how AWS pricing is captured, stored, refreshed, reused, and promoted in APV V2.

## Design Position

AWS pricing is a first-class project artifact set.

APV V2 should not depend on undocumented calculator memory or hidden spreadsheet logic. It should store the pricing basis as markdown artifacts plus captured evidence.

## Artifact Types

### Reusable Pricing Knowledge

Location:
- `wiki/apv-v2/knowledge/pricing/`

Examples:
- `aws-pricing-rules.md`
- `aws-region-guidance.md`
- `aws-savings-plans-guidance.md`
- `aws-component-catalog.md`

Purpose:
- store reusable reference pricing logic and curated component knowledge

### Project Pricing Manifest

Location:
- `apv-projects/.../working/05-pricing-manifest.md`

Purpose:
- list the exact pricing inputs used for this RFP

Required sections:
- provider
- target region
- service/component
- size/SKU
- HA model
- licensing assumptions
- utilization assumptions
- commitment model
- storage/network assumptions

### Project Pricing Evidence Record

Locations:
- `apv-projects/.../evidence/pricing/aws/pricing-evidence.md`
- `apv-projects/.../evidence/pricing/aws/*.png`
- `apv-projects/.../evidence/pricing/aws/*.pdf`

Purpose:
- connect pricing claims to calculator or official pricing captures

Required fields:
- source URL
- capture date
- parameter summary
- screenshot or export path
- reviewer note if manual judgment was applied

### Project Pricing Freshness Record

Location:
- `apv-projects/.../verification/freshness-report.json`
- optional human summary: `apv-projects/.../evidence/pricing/aws/freshness-summary.md`

Purpose:
- determine whether pricing is still valid for release

Default rule:
- pricing older than 30 days must be refreshed or explicitly approved as an exception

## Promotion Rules

Promote project pricing artifacts into reusable knowledge only when:

- the pricing pattern is reusable across multiple proposals
- the calculation logic is stable enough to document
- the promoted content is stripped of project-specific noise
- source URLs and verification date are preserved

Do not promote:

- one-off calculator screenshots
- project-only commercial assumptions
- transient exploratory comparisons

## Output Relationship

`outputs/05-pricing.md` should be generated from:

- architecture output
- sizing output
- pricing manifest
- pricing evidence record
- freshness state

This ensures the final pricing document is supported by project artifacts rather than free-form reconstruction.

## Minimum AWS Pricing Bundle Per RFP

Every AWS-based RFP should contain at least:

- `working/05-pricing-manifest.md`
- `working/05-assumption-log.md`
- `evidence/pricing/aws/pricing-evidence.md`
- one calculator capture or official pricing capture per major priced component class
- freshness validation output
- `outputs/05-pricing.md`