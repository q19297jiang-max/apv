---
type: apv-knowledge
category: infrastructure
provider: aws
title: "AWS Database Options for Card Processing"
source_url: "https://docs.aws.amazon.com/rds/latest/userguide/"
source_document: "Amazon RDS Documentation"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [infrastructure, aws, rds, database]
---

# AWS Database Options for Card Processing

## Overview

Amazon RDS provides managed relational database services for card processing workloads with high availability, security, and performance.

## Database Options

### Amazon RDS for PostgreSQL
**Source**: https://docs.aws.amazon.com/rds/latest/userguide/CHAP_PostgreSQL.html

- Open-source PostgreSQL
- PCI-DSS compliant
- Multi-AZ deployment
- Read replicas for scaling
- Versions: 12, 13, 14, 15

### Amazon RDS for Oracle
**Source**: https://docs.aws.amazon.com/rds/latest/userguide/CHAP_Oracle.html

- Oracle Database
- Standard Edition 2
- Enterprise Edition
- Bring Your Own License (BYOL)
- Multi-AZ deployment

### Amazon Aurora
**Source**: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/

- MySQL and PostgreSQL compatible
- 5x performance improvement
- Global Database option
- Serverless v2 option
- Multi-AZ by default

### Amazon DynamoDB
**Source**: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/

- NoSQL database
- Single-digit millisecond latency
- Auto-scaling
- Global Tables
- On-demand capacity mode

## Security Features

### Encryption
**Source**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html

- At-rest encryption (AES-256)
- In-transit encryption (TLS)
- AWS KMS key management
- Transparent Data Encryption (TDE)

### Access Control
**Source**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html

- IAM database authentication
- VPC security groups
- Master user password
- Password rotation

## High Availability

### Multi-AZ Deployment
**Source**: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html

- Synchronous replication
- Automatic failover
- Read replicas for scaling
- Cross-Region Read Replicas

## RFP Response Template

```
[Company Name] database options:

Primary Database:
├── RDS PostgreSQL 15
├── Multi-AZ deployment (high availability)
├── Encryption: AES-256 at rest, TLS in transit
└── Backup: 7-day retention, point-in-time recovery

Cache Layer:
├── ElastiCache Redis 7
├── Cluster mode enabled
└── Automatic failover

NoSQL (if needed):
├── DynamoDB on-demand
├── Global Tables for multi-region
└── Encryption enabled

PCI-DSS Certificate: [LINK]
Source: https://aws.amazon.com/compliance/pci-dss-faq/
```

## Related
- [[infrastructure-aws-eks]] — AWS EKS patterns
- [[infrastructure-aws-dr]] — Multi-region DR
