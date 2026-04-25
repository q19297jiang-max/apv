---
type: apv-knowledge
category: sizing
title: "Infrastructure Sizing Methodology"
source_url: "https://docs.aws.amazon.com/whitepapers/latest/database-migration-landing-page/working-on-databases-schemas/"
source_document: "Infrastructure Sizing Best Practices"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [sizing, infrastructure, capacity-planning]
---

# Infrastructure Sizing Methodology

## Overview

Sizing card processing infrastructure requires analysis of transaction volumes, performance requirements, and service level agreements.

## Sizing Inputs

### Transaction Volume
- **TPS (Transactions Per Second)**: Peak concurrent transactions
- **TPH (Transactions Per Hour)**: Average hourly volume
- **TPD (Transactions Per Day)**: Daily batch volume

### Card System Type
| Type | Base TPS Ratio | Source URL |
|------|----------------|------------|
| Issuing | 1:100 | Industry standard |
| Acquiring | 1:200 | Industry standard |
| Gateway | 1:500 | Industry standard |
| Wallet | 1:1000 | Industry standard |

### SLA Requirements
| Metric | Standard | High Availability | Mission Critical |
|--------|----------|-------------------|------------------|
| Availability | 99.9% | 99.95% | 99.99% |
| RTO | 4 hours | 1 hour | 15 minutes |
| RPO | 1 hour | 15 minutes | 5 minutes |

## Sizing Methodology

```
Source: Industry best practices for card processing

Step 1: Calculate Base Compute
  Peak TPS × Safety Margin (2x) × Growth Factor (1.5x)

Step 2: Add Database Capacity
  Compute × Database Ratio (1:2 for OLTP)

Step 3: Add Network Bandwidth
  TPS × Average Transaction Size (2KB) × 8

Step 4: Add Storage
  TPD × Data Retention (7 years) × Compression (0.3)

Step 5: Add Redundancy
  All components × HA Multiplier (2x for Multi-AZ)
```

## Instance Selection

### AWS Instance Sizing
| TPS Range | Instance Family | Recommended Instance | Source URL |
|-----------|-----------------|---------------------|------------|
| 1-100 | General purpose | m6i.xlarge (4 vCPU) | https://docs.aws.amazon.com/ec2/ |
| 100-500 | Compute optimized | c6i.2xlarge (8 vCPU) | https://docs.aws.amazon.com/ec2/ |
| 500-2000 | Compute optimized | c6i.8xlarge (32 vCPU) | https://docs.aws.amazon.com/ec2/ |
| 2000+ | Memory optimized | r6i.16xlarge (64 vCPU) | https://docs.aws.amazon.com/ec2/ |

### Azure VM Sizing
| TPS Range | Series | Recommended VM | Source URL |
|-----------|--------|----------------|------------|
| 1-100 | Dsv5 | Standard_D4s_v5 | https://learn.microsoft.com/azure/virtual-machines/ |
| 100-500 | Fsv5 | Standard_F8s_v2 | https://learn.microsoft.com/azure/virtual-machines/ |

### GCP Sizing
| TPS Range | Machine Family | Recommended Machine | Source URL |
|-----------|----------------|---------------------|------------|
| 1-100 | E2 | e2-highmem-4 | https://cloud.google.com/compute/docs/machine-types |
| 100-500 | C2 | c2-standard-8 | https://cloud.google.com/compute/docs/machine-types |

## RFP Sizing Questionnaire

```markdown
# RFP Sizing Questionnaire

Please provide:

1. **Card System Type**: [ ] Issuing [ ] Acquiring [ ] Gateway [ ] Wallet
2. **Peak TPS**: ______ transactions/second
3. **Average TPH**: ______ transactions/hour
4. **Daily Volume**: ______ transactions/day
5. **Growth Projection**: ______% per year
6. **SLA Required**:
   - Availability: _____%
   - RTO: _____ hours/minutes
   - RPO: _____ hours/minutes
7. **Target Region**: [Singapore|Malaysia|Philippines|Indonesia|Thailand|Taiwan|Hong Kong]
8. **Cloud Preference**: [AWS|Azure|GCP|Any]

Source: Industry best practices for card processing
```

## Related
- [[sizing-guide]] — Detailed sizing methodology
- [[pricing-guide]] — Cost calculation
