# Detailed BOM Specifications Enhancement

**Date**: 2026-04-25
**Improvement**: Added mandatory detailed specifications for all BOM components

## Problem

The previous BOM generation was too high-level and lacked the detailed specifications needed for accurate pricing verification:
1. Components listed without exact instance types
2. Missing hardware specifications (vCPU, memory, storage)
3. No unit prices for verification
4. No sizing justification for component choices
5. Generic names without detailed specs

## Solution

### 1. Created AWS Component Catalog

**File**: `wiki/apv/knowledge/pricing/aws-component-catalog.md`

**Content**: Detailed catalog of AWS components with:
- Exact instance types (e.g., m6i.xlarge, db.m6i.xlarge)
- Hardware specifications (vCPU, memory, storage, network)
- Exact unit pricing with source URLs
- Regional multipliers
- Sizing guidelines by deployment size

**Catalog Sections**:
- Compute (EC2): m6i, c6i, r6i instance families
- Database (RDS): PostgreSQL Multi-AZ instances
- Cache (ElastiCache): Redis nodes
- Load Balancing (ALB/NLB): Detailed LCU pricing
- Containers (EKS): Cluster and Fargate pricing
- Storage (EBS, S3): Detailed storage pricing
- Networking (Direct Connect, VPC): Network component pricing
- Security (KMS, Shield): Security component pricing

### 2. Updated rfp-pricer Skill

**File**: `~/.claude/skills/rfp-pricer/prompt.md`

**New Requirements**:

#### MANDATORY AWS Component Details
Each AWS component MUST include:
- **Exact Instance Type**: e.g., "m6i.xlarge"
- **Hardware Specifications**: vCPU, Memory (GiB), Storage type/size
- **Unit Price**: Exact hourly/monthly price
- **Sizing Justification**: Why this size was chosen
- **Source URL**: Direct link to AWS pricing page

#### Example Required Format:
```markdown
| # | Component | Specification | Quantity | Unit | Monthly | Annual | Source |
|---|-----------|---------------|----------|------|---------|--------|--------|
| 1 | EC2 App Server | m6i.xlarge (4 vCPU, 16 GiB, EBS-only) | 2 | ea/month | $280.32 | $3,363.84 | https://aws.amazon.com/ec2/pricing/ |
```

#### Forbidden Practices:
- ❌ Generic names without specifications
- ❌ Pricing without exact unit prices
- ❌ Missing source URLs
- ❌ Missing sizing justification
- ❌ "TBD" or "estimated" without verification

### 3. Updated BOM Generator

**File**: `wiki/apv/tools/generate-bom.py`

**Enhanced Features**:

#### Enhanced BOM Summary Table
Now includes:
- Instance Type column
- Detailed specifications (vCPU, memory)
- Clickable source links
- Proper formatting for verification

#### Detailed Component Specifications Section
Each component now includes:
```markdown
### Component Name

**Specification**:
- Instance Type: m6i.xlarge
- vCPU: 4 cores
- Memory: 16 GiB
- Storage: EBS-only
- Network: Up to 12.5 Gbps

**Pricing**:
- Unit Price: $0.192/hour
- Monthly Cost: $140.16
- Annual Cost: $1,681.92

**Sizing Justification**:
- Medium application server for card processing
- Supports up to 500 TPS
- 2x redundancy for high availability

**Source**:
- Pricing URL: https://aws.amazon.com/ec2/pricing/
- Calculator URL: https://calculator.aws/
- Verified Date: 2026-04-25

**Quantity**: 2 units
**Total Monthly Cost**: $280.32
```

#### Enhanced Pricing Breakdown
Now includes:
- Instance Type column
- Hardware specs (vCPU/memory)
- Source URLs
- Percentage breakdown

#### Enhanced Calculator Verification
Now includes:
- Detailed component table with vCPU/memory
- Unit prices for verification
- Instance type references

## JSON Input Format Update

The enhanced BOM generator now supports detailed specifications:

```json
{
  "components": [
    {
      "name": "EC2 Application Server",
      "instance_type": "m6i.xlarge",
      "spec": "Application server for card processing",
      "detailed_spec": "m6i.xlarge (4 vCPU, 16 GiB, EBS-only, up to 12.5 Gbps)",
      "hardware_spec": {
        "instance_type": "m6i.xlarge",
        "vcpu": 4,
        "memory": 16,
        "storage": "EBS-only",
        "network": "Up to 12.5 Gbps"
      },
      "unit_price": 0.192,
      "quantity": 2,
      "unit": "ea/month",
      "monthly_cost": 280.32,
      "annual_cost": 3363.84,
      "source_url": "https://aws.amazon.com/ec2/pricing/",
      "calculator_url": "https://calculator.aws/",
      "verified_date": "2026-04-25",
      "sizing_justification": "Medium application server for card processing, supports up to 500 TPS, 2x redundancy for HA",
      "notes": "Deployed across 2 AZs for high availability"
    }
  ],
  "pricing": {
    "deployment_model": "Dedicated Infrastructure",
    "cloud_provider": "AWS",
    "region": "ap-southeast-1",
    "components": [...],
    "implementation_services": [...],
    "assumptions": [...]
  }
}
```

## Sizing Guidelines

The AWS Component Catalog includes sizing guidelines:

### Small Deployment (< 1,000 cards)
- EC2: m6i.large (2 vCPU, 8 GiB)
- RDS: db.m6i.large (2 vCPU, 8 GiB)
- ElastiCache: cache.m6g.large (2 vCPU, 5.3 GiB)

### Medium Deployment (1,000 - 10,000 cards)
- EC2: m6i.xlarge (4 vCPU, 16 GiB) × 2
- RDS: db.m6i.xlarge (4 vCPU, 16 GiB) Multi-AZ
- ElastiCache: cache.m6g.xlarge (4 vCPU, 13.5 GiB) × 2

### Large Deployment (> 10,000 cards)
- EC2: m6i.2xlarge (8 vCPU, 32 GiB) × 4
- RDS: db.r6i.xlarge (4 vCPU, 32 GiB) Multi-AZ
- ElastiCache: cache.r6g.xlarge (4 vCPU, 32.3 GiB) × 3

## Verification Requirements

All pricing must be verifiable:
1. **Source URLs**: Direct links to AWS pricing pages
2. **Unit Prices**: Exact hourly/monthly rates
3. **Calculator References**: Links to AWS calculator
4. **Verification Dates**: When pricing was verified
5. **Sizing Justification**: Why each component size was chosen

## Benefits

1. **Accuracy**: Exact specifications prevent ambiguity
2. **Verifiability**: Every cost can be verified with source URLs
3. **Transparency**: Full component breakdown with detailed specs
4. **Professionalism**: Meets fintech industry standards for BOM documentation
5. **Auditability**: Complete traceability from requirement to component to cost

## Example Output

### BOM Summary Table
| # | Component | Instance Type | Specification | Quantity | Monthly | Annual | Source |
|---|-----------|---------------|---------------|----------|---------|--------|--------|
| 1 | EC2 App Server | m6i.xlarge | 4 vCPU, 16 GiB | 2 | $280.32 | $3,363.84 | [AWS Pricing](https://aws.amazon.com/ec2/pricing/) |
| 2 | RDS PostgreSQL | db.m6i.xlarge | 4 vCPU, 16 GiB | 1 | $274.48 | $3,293.76 | [AWS Pricing](https://aws.amazon.com/rds/pricing/) |

### Detailed Component Specification
```markdown
### EC2 Application Server

**Specification**:
- Instance Type: m6i.xlarge
- vCPU: 4 cores
- Memory: 16 GiB
- Storage: EBS-only
- Network: Up to 12.5 Gbps

**Pricing**:
- Unit Price: $0.192/hour
- Monthly Cost: $140.16
- Annual Cost: $1,681.92

**Sizing Justification**:
- Medium application server for card processing
- Supports up to 500 TPS
- 2x redundancy for high availability

**Source**:
- Pricing URL: https://aws.amazon.com/ec2/pricing/
- Calculator URL: https://calculator.aws/
- Verified Date: 2026-04-25

**Quantity**: 2 units
**Total Monthly Cost**: $280.32
```

## Related

- [[bom-generation-improvements]] — Original BOM generation enhancement
- [[rfp-pricer]] — Pricing skill with detailed specs requirement
- [[aws-component-catalog]] — AWS component reference catalog
- [[apv]] — APV orchestrator
