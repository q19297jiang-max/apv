---
type: source
category: infrastructure
provider: aws
title: AWS EKS Card Processing Architecture
source_url: "https://docs.aws.amazon.com/eks/latest/userguide/"
source_document: Amazon EKS Documentation
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [infrastructure, aws, eks, kubernetes]
freshness_days: 90
last_verified: 2026-04-24
---

# AWS EKS Card Processing Architecture

## Overview

Amazon Elastic Kubernetes Service (EKS) provides a managed Kubernetes platform for running containerized card processing applications with high scalability and availability.

## Reference Architecture

**Source**: https://docs.aws.amazon.com/eks/latest/userguide/

```
EKS Card Processing Architecture:
├── Control Plane (AWS Managed)
│   ├── Kubernetes API server
│   ├── Scheduler
│   ├── Controller Manager
│   └── Cloud Controller Manager
├── Worker Nodes (EC2)
│   ├── Application pods (microservices)
│   ├── Sidecar containers (service mesh)
│   └── Node groups (autoscaling)
├── Data Layer
│   ├── Amazon RDS (PostgreSQL/Oracle)
│   ├── Amazon ElastiCache (Redis)
│   └── Amazon DocumentDB (MongoDB)
├── Storage
│   ├── EBS (block storage)
│   └── EFS (shared file system)
└── Networking
    ├── VPC (private subnets)
    ├── Load balancers (ALB, NLB)
    └── VPC Lattice (service-to-service)
```

## Components

### EKS Control Plane
**Source**: https://docs.aws.amazon.com/eks/latest/userguide/control-plane.html

- Fully managed by AWS
- High availability across 3 AZs
- Automatic upgrades and patching
- No additional cost

### Node Groups
**Source**: https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html

| Node Type | Instance Family | Use Case | Source URL |
|-----------|-----------------|----------|------------|
| General purpose | m5, m6i | Application servers | https://docs.aws.amazon.com/eks/latest/userguide/node-groups.html |
| Memory optimized | r5, r6i | Database, cache | https://docs.aws.amazon.com/eks/latest/userguide/node-groups.html |
| Compute optimized | c5, c6i | Authorization engine | https://docs.aws.amazon.com/eks/latest/userguide/node-groups.html |
| Graviton (ARM) | t4g, m6g | Cost-optimized | https://docs.aws.amazon.com/eks/latest/userguide/grpc-fargate.html |

### Fargate (Serverless)
**Source**: https://docs.aws.amazon.com/eks/latest/userguide/fargate.html

- No EC2 management
- Per-pod billing
- Isolated compute environment
- Ideal for variable workloads

## Regional Availability

**Source**: https://docs.aws.amazon.com/eks/latest/userguide/regions.html

| Country | Region | Region Code | EKS Available | Source URL |
|---------|--------|-------------|---------------|------------|
| Singapore | Asia Pacific | ap-southeast-1 | ✅ Yes | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Malaysia | Asia Pacific | ap-southeast-3 | ✅ Yes | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Philippines | Asia Pacific | ap-southeast-1 | ✅ Yes (nearest) | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Indonesia | Asia Pacific | ap-southeast-3 | ✅ Yes | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Thailand | Asia Pacific | ap-southeast-1 | ✅ Yes (nearest) | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Taiwan | Asia Pacific | ap-northeast-1 | ✅ Yes (nearest) | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |
| Hong Kong | Asia Pacific | ap-east-1 | ✅ Yes | https://docs.aws.amazon.com/eks/latest/userguide/regions.html |

## Service Mapping

| Function | EKS Service | Source URL | PCI-DSS Certified |
|----------|-------------|------------|-------------------|
| Compute | Amazon EKS | https://docs.aws.amazon.com/eks/latest/userguide/ | ✅ Yes |
| Database | Amazon RDS | https://docs.aws.amazon.com/rds/ | ✅ Yes |
| Cache | Amazon ElastiCache | https://docs.aws.amazon.com/elasticache/ | ✅ Yes |
| Storage | Amazon EBS | https://docs.aws.amazon.com/ebs/ | ✅ Yes |
| Load Balancing | ALB, NLB | https://docs.aws.amazon.com/elasticloadbalancing/ | ✅ Yes |

## Pricing References

| Service | Calculator URL | Notes |
|---------|----------------|-------|
| EKS Control Plane | https://calculator.aws/ | $0.10/hour per cluster |
| EC2 Instances | https://calculator.aws/ | Per instance-hour |
| Fargate | https://calculator.aws/ | Per vCPU-hour, GB-hour |
| ALB | https://calculator.aws/ | $0.0225/hour + LCU |
| NLB | https://calculator.aws/ | $0.0225/hour + NLCU |

## RFP Response Template

### Question: "Describe your AWS EKS architecture"

```
[Company Name] uses Amazon EKS for card processing:

Region: [COUNTRY] ap-southeast-1 / ap-southeast-3
Source: https://docs.aws.amazon.com/eks/latest/userguide/regions.html

Architecture:
├── Control Plane: AWS-managed (high availability)
├── Compute: EKS with EC2/Fargate
│   ├── Application: m6i.xlarge (general purpose)
│   ├── Database: r6i.2xlarge (memory optimized)
│   └── Authorization: c6i.4xlarge (compute optimized)
├── Data Layer:
│   ├── RDS PostgreSQL (Multi-AZ)
│   ├── ElastiCache Redis (cluster mode)
│   └── DocumentDB (for NoSQL)
└── Networking:
    ├── ALB (external traffic)
    ├── NLB (high performance)
    └── Private VPC subnets

PCI-DSS Certificate: [LINK]
All services listed in AWS PCI-DSS certificate:
https://aws.amazon.com/compliance/pci-dss-faq/

Source URLs:
- EKS: https://docs.aws.amazon.com/eks/latest/userguide/
- RDS: https://docs.aws.amazon.com/rds/
- ElastiCache: https://docs.aws.amazon.com/elasticache/
```

## Related
- [[infrastructure-aws-ecs]] — AWS ECS patterns
- [[infrastructure-aws-rds]] — AWS RDS database options
- [[infrastructure-aws-dr]] — Multi-region DR
