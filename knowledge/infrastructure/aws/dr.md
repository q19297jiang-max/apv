---
type: apv-knowledge
category: infrastructure
provider: aws
title: "AWS Multi-Region Disaster Recovery"
source_url: "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/"
source_document: "AWS Disaster Recovery Whitepaper"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [infrastructure, aws, disaster-recovery, dr]
---

# AWS Multi-Region Disaster Recovery

## Overview

AWS provides multiple options for implementing disaster recovery (DR) strategies for card processing systems, from pilot light to multi-site active-active.

## DR Strategies

### Pilot Light
**Source**: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/

- Minimal resources in DR region
- Critical services only
- Fast activation (minutes to hours)
- Lowest cost option

### Warm Standby
**Source**: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/

- Full infrastructure in DR region
- Scaled down but ready
- Faster activation (minutes)
- Moderate cost

### Multi-Site Active-Active
**Source**: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/

- Full infrastructure in both regions
- Active traffic to both
- Zero downtime activation
- Highest cost

## Regional Pairs

**Source**: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/

| Primary Region | DR Region | Latency | Source URL |
|----------------|-----------|---------|------------|
| ap-southeast-1 (Singapore) | ap-south-1 (Mumbai) | ~50ms | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/ |
| ap-southeast-3 (Malaysia) | ap-southeast-1 (Singapore) | ~30ms | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/ |

## Data Replication

### Database Replication
**Source**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html

- RDS Multi-AZ (synchronous, same region)
- RDS Cross-Region Read Replicas (asynchronous)
- Aurora Global Database (fast replication)

### Storage Replication
**Source**: https://docs.aws.amazon.com/efs/latest/userguide/backup-workloads.html

- EFS Cross-Region Replication
- S3 Cross-Region Replication (CRR)

## RTO/RPO Targets

| DR Strategy | RTO | RPO | Cost | Source URL |
|-------------|-----|-----|------|------------|
| Pilot Light | 1-4 hours | 1 hour | Low | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/ |
| Warm Standby | 10-30 mins | 5-15 mins | Medium | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/ |
| Active-Active | 0 mins | 0-5 mins | High | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/ |

## RFP Response Template

```
[Company Name] disaster recovery strategy:

DR Strategy: Warm Standby

Primary Region: ap-southeast-1 (Singapore)
DR Region: ap-southeast-3 (Malaysia)

RTO: 15 minutes
RPO: 10 minutes

Data Replication:
├── RDS Cross-Region Read Replicas
├── ElastiCache Cross-Cluster
└── S3 Cross-Region Replication

Failover: Automated (Route53 health checks)

Cost: ~50% of primary region

PCI-DSS Certificate: [LINK]
Source: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/
```

## Related
- [[infrastructure-aws-eks]] — AWS EKS patterns
- [[infrastructure-aws-rds]] — AWS RDS database options
