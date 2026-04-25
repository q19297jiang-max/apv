# BOM Generation Enhancement

**Date**: 2026-04-25
**Improvement**: Added Bill of Materials (BOM) generation to APV pricing workflow

## Problem

Previously, the `rfp-pricer` skill generated pricing output but:
1. Did not create a BOM (Bill of Materials) document
2. Referenced non-existent evidence files (e.g., `saas-pricing-2026-04-24.pdf`)
3. No actual evidence files were created in `evidence/pricing/`

This made it impossible to verify pricing accuracy or provide proper documentation to customers.

## Solution

### 1. Updated rfp-pricer Skill

**File**: `~/.claude/skills/rfp-pricer/prompt.md`

**Changes**:
- Added BOM generation requirement
- Added evidence file creation requirement
- Added support for both SaaS and dedicated infrastructure pricing
- Added quality rules for BOM and evidence files
- Added tool usage instructions

**New Output Format**:
```markdown
## Bill of Materials (BOM)

| # | Component | Specification | Quantity | Unit | Monthly | Annual | Source |
|---|-----------|---------------|----------|------|---------|--------|--------|
| 1 | Card Management System | SaaS Platform | 1 | ea/month | $300 | $3,600 | Internal pricing |
...
```

### 2. Created BOM Generator Tool

**File**: `wiki/apv/tools/generate-bom.py`

**Features**:
- Generates BOM markdown document with full component breakdown
- Creates pricing breakdown with cost analysis
- Creates calculator verification document
- Supports both SaaS and cloud infrastructure pricing

**Usage**:
```bash
python3 wiki/apv/tools/generate-bom.py \
  --project /path/to/project \
  --components '{"components": [...], "pricing": {...}}'
```

**Output Files**:
```
evidence/pricing/YYYY-MM-DD/
├── bom.md                      # Full Bill of Materials
├── pricing-breakdown.md        # Detailed cost breakdown
└── calculator-verification.md  # Pricing verification
```

### 3. Updated APV Orchestrator

**File**: `~/.claude/skills/apv/prompt.md`

**Changes**:
- Added Step 5.5: Generate BOM and Evidence Files
- Instructions to run BOM generator after rfp-pricer skill

**Updated Workflow**:
1. rfp-brainstorm
2. rfp-compliance
3. rfp-architect
4. rfp-calculator
5. rfp-pricer
6. **NEW**: Generate BOM and Evidence Files
7. rfp-generator
8. apv-reviewer

## JSON Input Format

The BOM generator expects the following JSON structure:

```json
{
  "components": [
    {
      "name": "Card Management System",
      "spec": "SaaS Card Management Platform",
      "quantity": 1,
      "unit": "system",
      "monthly_cost": 300,
      "annual_cost": 3600,
      "source_url": "Internal SaaS pricing",
      "notes": "Includes card lifecycle management"
    }
  ],
  "pricing": {
    "deployment_model": "SaaS Multi-Tenant",
    "cloud_provider": "AWS",
    "region": "ap-southeast-1",
    "implementation_services": [
      {
        "name": "System Setup",
        "duration": "5 days",
        "daily_rate": 1000,
        "days": 5,
        "source": "Internal rate"
      }
    ],
    "assumptions": [
      {
        "name": "Currency",
        "value": "USD",
        "justification": "Standard pricing"
      }
    ],
    "alternative_pricing": {
      "Dedicated Infrastructure": {
        "year1": 56000,
        "year3": 128000,
        "difference": "+192%"
      }
    }
  }
}
```

## BOM Document Structure

The generated `bom.md` includes:

1. **Component Summary Table**: All components with specs, quantities, costs, sources
2. **Implementation Services**: One-time costs with daily rates
3. **Cost Summary**: Monthly, annual, and 3-year totals
4. **Component Specifications**: Detailed specs for each component
5. **Assumptions**: All pricing assumptions documented
6. **Evidence**: Evidence file locations and verification status

## Pricing Breakdown Document

The generated `pricing-breakdown.md` includes:

1. **Monthly Recurring Costs**: Cost breakdown by component with percentages
2. **Annual Recurring Costs**: Annual breakdown by component
3. **One-Time Costs**: Implementation services total
4. **3-Year Projection**: Year-by-year cost projection
5. **Cost Comparison**: SaaS vs dedicated infrastructure comparison

## Calculator Verification Document

The generated `calculator-verification.md` includes:

1. **Deployment Model**: SaaS or dedicated infrastructure
2. **Pricing Source**: Internal rate sheet or cloud calculator
3. **Verification Method**: How pricing was verified
4. **Calculator Inputs**: Detailed input data
5. **Freshness Status**: Verification date and currency

## Benefits

1. **Transparency**: Full component breakdown with costs
2. **Verifiability**: Evidence files can be reviewed by customers
3. **Traceability**: Every cost item has a source or reference
4. **Professionalism**: Proper documentation for customer presentations
5. **Accuracy**: Calculator verification ensures pricing accuracy

## Next Steps

1. Test the BOM generator with the BBC Bank RFP
2. Verify evidence files are created correctly
3. Update rfp-generator to reference BOM evidence files
4. Add BOM to apv-reviewer checklist

## Related

- [[rfp-pricer]] - Pricing skill
- [[apv]] - APV orchestrator
- [[apv-reviewer]] - Approval verification
