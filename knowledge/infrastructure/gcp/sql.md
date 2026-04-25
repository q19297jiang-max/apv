---
type: apv-knowledge
category: infrastructure
provider: gcp
title: "GCP Cloud SQL Database"
source_url: "https://cloud.google.com/sql/docs"
source_document: "Cloud SQL Documentation"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [infrastructure, gcp, cloud-sql, database]
---

# GCP Cloud SQL Database Options

## Overview

Cloud SQL provides fully managed relational database services for card processing workloads.

## Database Options

### Cloud SQL for PostgreSQL
**Source**: https://cloud.google.com/sql/docs/postgres/

- Versions 12, 13, 14, 15
- Automatic backups
- High availability (regional)
- Read replicas
- Vertical scaling

### Cloud SQL for MySQL
**Source**: https://cloud.google.com/sql/docs/mysql/

- MySQL 8.0, 5.7
- Automatic backups
- High availability
- Read replicas

## Security Features

- Encryption at rest (AES-256)
- Encryption in transit (TLS)
- Cloud KMS integration
- Private IP (VPC)
- IAM authentication

## High Availability

- Regional HA (3 zones)
- Automatic failover
- Point-in-time recovery (7 days by default)
- Cross-region replication (read replicas)

## RFP Response Template

```
[Company Name] database options:

Primary: Cloud SQL for PostgreSQL
├── Regional HA (3 zones)
├── Automatic backups
├── Point-in-time recovery
└── Read replicas for scaling

Cache: Memorystore (Redis)
├── Regional instances
├── Automatic failover
└── Data persistence

PCI-DSS Certificate: [LINK]
Source: https://cloud.google.com/security/compliance/pci-dss
```

## Related
- [[infrastructure-gcp-gke]] — GCP GKE patterns
