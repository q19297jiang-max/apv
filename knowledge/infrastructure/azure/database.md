---
type: source
category: infrastructure
provider: azure
title: Azure Database Options
source_url: "https://learn.microsoft.com/en-us/azure/azure-sql/database/"
source_document: Azure Database Documentation
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [infrastructure, azure, database, sql]
freshness_days: 90
last_verified: 2026-04-24
---

# Azure Database Options for Card Processing

## Overview

Azure provides multiple managed database services for card processing workloads.

## Database Options

### Azure Database for PostgreSQL
**Source**: https://learn.microsoft.com/en-us/azure/postgresql/

- Flexible Server (recommended)
- Single Server
- Hyperscale (Citus) option
- Multi-AZ HA

### Azure SQL Database
**Source**: https://learn.microsoft.com/en-us/azure/azure-sql/database/

- Single Database
- Elastic Pool
- vCore-based purchasing model
- Geo-replication

### Azure Cosmos DB
**Source**: https://learn.microsoft.com/en-us/azure/cosmos-db/

- Globally distributed NoSQL
- 5 consistency levels
- Multi-model (SQL, MongoDB, etc.)
- Auto-scaling

## Security Features

- Encryption at rest (AES-256)
- Encryption in transit (TLS)
- Azure Key Vault integration
- Private endpoints

## RFP Response Template

```
[Company Name] database options:

Primary: Azure Database for PostgreSQL (Flexible Server)
├── Multi-AZ HA
├── Zone redundant
└── Point-in-time restore

Cache: Azure Cache for Redis
├── Premium tier
├── Cluster mode
└── Geo-replication

PCI-DSS Certificate: [LINK]
Source: https://www.microsoft.com/en-us/trust-center/compliance/pci
```

## Related
- [[infrastructure-azure-aks]] — Azure AKS patterns
