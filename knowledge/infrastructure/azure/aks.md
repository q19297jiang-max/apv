---
type: apv-knowledge
category: infrastructure
provider: azure
title: "Azure AKS Card Processing Architecture"
source_url: "https://learn.microsoft.com/en-us/azure/aks/"
source_document: "Azure Kubernetes Service Documentation"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [infrastructure, azure, aks, kubernetes]
---

# Azure AKS Card Processing Architecture

## Overview

Azure Kubernetes Service (AKS) provides a managed Kubernetes platform for running containerized card processing applications.

## Reference Architecture

**Source**: https://learn.microsoft.com/en-us/azure/aks/

```
AKS Card Processing Architecture:
├── AKS Control Plane (Azure Managed)
│   ├── Kubernetes API server
│   ├── Scheduler
│   └── Controller Manager
├── Node Pools (Virtual Machines)
│   ├── System node pools
│   └── User node pools
├── Data Layer
│   ├── Azure Database for PostgreSQL
│   ├── Azure Cache for Redis
│   └── Azure Cosmos DB
└── Networking
    ├── Azure VNet
    ├── Application Gateway
    └── Azure Front Door
```

## Regional Availability

| Country | Region | Region Code | AKS Available | Source URL |
|---------|--------|-------------|---------------|------------|
| Singapore | Southeast Asia | southeast-asia | ✅ Yes | https://learn.microsoft.com/en-us/azure/aks/regions/ |
| Malaysia | Southeast Asia | southeast-asia | ✅ Yes (nearest) | https://learn.microsoft.com/en-us/azure/aks/regions/ |
| Hong Kong | East Asia | east-asia | ✅ Yes | https://learn.microsoft.com/en-us/azure/aks/regions/ |

## Service Mapping

| Function | AKS Service | Source URL | PCI-DSS Certified |
|----------|-------------|------------|-------------------|
| Compute | Azure AKS | https://learn.microsoft.com/en-us/azure/aks/ | ✅ Yes |
| Database | Azure Database for PostgreSQL | https://learn.microsoft.com/en-us/azure/postgresql/ | ✅ Yes |
| Cache | Azure Cache for Redis | https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/ | ✅ Yes |

## Pricing References

| Service | Calculator URL | Notes |
|---------|----------------|-------|
| AKS | https://azure.microsoft.com/pricing/calculator/ | Free for managed control plane |
| VMs | https://azure.microsoft.com/pricing/calculator/ | Per VM-hour |
| Database | https://azure.microsoft.com/pricing/calculator/ | Per vCore-hour |

## RFP Response Template

```
[Company Name] uses Azure AKS for card processing:

Region: [COUNTRY] southeast-asia / east-asia
Source: https://learn.microsoft.com/en-us/azure/aks/regions/

Architecture:
├── AKS: Managed Kubernetes (free control plane)
├── Compute: VMs (Dsv5 series)
├── Data: Azure PostgreSQL + Redis + Cosmos DB
└── Networking: Application Gateway + Front Door

PCI-DSS Certificate: [LINK]
Source: https://www.microsoft.com/en-us/trust-center/compliance/pci
```

## Related
- [[infrastructure-azure-database]] — Azure database options
