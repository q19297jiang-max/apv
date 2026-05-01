---
type: source
category: pricing
title: Component Catalog Template
created: 2026-04-25
tags: [pricing, template, catalog]
freshness_days: 30
last_verified: null
---

# Component Catalog Template

## Purpose

This template defines the standard format for adding new cloud components to the pricing catalog. Follow this format when adding any new AWS, Azure, or GCP components.

## Standard Table Format

### Instance-Based Components

For components with instance types (EC2, RDS, ElastiCache, etc.):

```markdown
### [Component Category]

**Pricing Source**: [Official Pricing URL]
**Calculator**: [Calculator URL]

> [!NOTE] Pricing Notes
> Any important notes about pricing models, discounts, or regional differences.

| Instance | vCPU | Memory | [Additional Columns] | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|---------------------|------------|----------------|----------------|
| instance.name | 2 | 8 GiB | [specifications] | $0.000 | $000.00 | https://calculator.aws/ |
```

### Flat-Rate Components

For components with flat pricing (EKS, Load Balancers, etc.):

```markdown
### [Component Category]

**Pricing Source**: [Official Pricing URL]

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|----------------|
| component.name | $0.00 | per unit-hour | https://calculator.aws/ |
```

### Storage Components

For storage and data transfer:

```markdown
### [Storage Category]

**Pricing Source**: [Official Pricing URL]

| Storage Type | Price/GB-month | [Additional Columns] | Calculator URL |
|--------------|----------------|---------------------|----------------|
| storage.name | $0.00 | specifications | https://calculator.aws/ |
```

## Required Columns

| Column | Required | Description |
|--------|----------|-------------|
| **Instance/Component** | Yes | Name of the component or instance type |
| **Price/Hour or Price** | Yes | Hourly rate or flat rate |
| **Monthly (730h)** | Yes | Monthly cost (730 hours) |
| **Calculator URL** | Yes | Link to official calculator/pricing page |

## Optional Columns

| Column | When to Use | Description |
|--------|-------------|-------------|
| **vCPU** | Compute instances | Number of virtual CPUs |
| **Memory** | Compute/Database instances | Memory in GiB |
| **Storage** | Compute instances | Storage type and size |
| **Network** | Compute instances | Network performance |
| **Billing Unit** | Flat-rate components | How the component is billed |
| **Savings %** | Discounted pricing | Percentage discount from list price |

## Section Naming Convention

Use descriptive section headers:

```markdown
### [Provider] [Component Type]

## Examples:
### EC2 Instances
### RDS Pricing (Single-AZ)
### RDS Pricing (Verified from Calculator)
### Compute Savings Plans (3yr No Upfront)
### ElastiCache Pricing
### EKS Pricing
### Load Balancer Pricing
### EBS Storage Pricing
```

## Regional Pricing Matrix

Always include regional multipliers at the top of the catalog:

```markdown
## Regional Pricing Matrix

| Region Code | Region Name | Multiplier | Calculator URL |
|-------------|-------------|------------|----------------|
| region-code | Region Name | 1.00x | https://calculator.cloud/ |
```

## Pricing Notes Format

Use callouts for important pricing information:

```markdown
> [!NOTE] Pricing Model
> **Single-AZ pricing**: Standalone deployment
> **Multi-AZ pricing**: High availability deployment (2-3x Single-AZ)

> [!IMPORTANT] Calculator-Verified Pricing
> Verified on YYYY-MM-DD from https://calculator.cloud/
```

## Adding New Components

### 1. Choose Component Type

Determine which category your component fits:
- **Instance-Based**: EC2, RDS, ElastiCache, VMs, etc.
- **Flat-Rate**: EKS, AKS, GKE, Load Balancers, etc.
- **Storage**: EBS, S3, Blob Storage, etc.
- **Networking**: Direct Connect, ExpressRoute, etc.
- **Security**: KMS, Key Vault, Cloud HSM, etc.

### 2. Gather Required Information

- Official pricing page URL
- Calculator URL (if available)
- Instance/component names
- Specifications (vCPU, memory, etc.)
- Pricing (hourly or flat rate)
- Regional availability

### 3. Add to Component Catalog

Follow the appropriate table format from above.

### 4. Update Provider

If adding a new cloud provider (Azure, GCP), create:
- `[provider]-component-catalog.md`
- Update pricing-fetcher.py to parse the new catalog
- Add provider-specific calculator URLs

## Validation Checklist

Before committing, verify:
- [ ] All tables have "Calculator URL" column
- [ ] All pricing has source URL
- [ ] Monthly costs calculated correctly (price × 730)
- [ ] Regional multipliers included
- [ ] Section headers follow naming convention
- [ ] Pricing notes use callout format

## Related

- [[aws-component-catalog]] - AWS component catalog (example)
- [[pricing-workflow]] - Complete pricing workflow guide
