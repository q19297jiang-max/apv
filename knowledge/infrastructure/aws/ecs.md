---
type: apv-knowledge
category: infrastructure
provider: aws
title: "AWS ECS Card Processing Architecture"
source_url: "https://docs.aws.amazon.com/ecs/latest/userguide/"
source_document: "Amazon ECS Documentation"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [infrastructure, aws, ecs, containers]
---

# AWS ECS Card Processing Architecture

## Overview

Amazon Elastic Container Service (ECS) provides a highly scalable, high-performance container orchestration service for running card processing applications.

## Reference Architecture

**Source**: https://docs.aws.amazon.com/ecs/latest/userguide/

```
ECS Card Processing Architecture:
├── ECS Cluster
│   ├── Task Definitions
│   ├── Services (long-running)
│   └── Tasks (batch jobs)
├── Compute Options
│   ├── Fargate (serverless)
│   ├── EC2 (self-managed)
│   └── External (on-prem)
├── Data Layer
│   ├── RDS (PostgreSQL/Oracle)
│   ├── ElastiCache (Redis)
│   └── DynamoDB (NoSQL)
└── Networking
    ├── VPC (private subnets)
    ├── Load balancers (ALB, NLB)
    └── Service Connect (service mesh)
```

## Launch Types

### Fargate
**Source**: https://docs.aws.amazon.com/ecs/latest/userguide/Fargate.html

- Serverless containers
- No EC2 management
- Pay per vCPU-hour, GB-hour
- Isolated compute environment

### EC2
**Source**: https://docs.aws.amazon.com/ecs/latest/userguide/ECS_instances.html

- Self-managed EC2 instances
- More control over infrastructure
- Cost-optimized for steady workloads
- Bottlerocket OS option

## Service Mapping

| Function | ECS Service | Source URL | PCI-DSS Certified |
|----------|-------------|------------|-------------------|
| Compute | Amazon ECS | https://docs.aws.amazon.com/ecs/latest/userguide/ | ✅ Yes |
| Database | Amazon RDS | https://docs.aws.amazon.com/rds/ | ✅ Yes |
| NoSQL | Amazon DynamoDB | https://docs.aws.amazon.com/dynamodb/ | ✅ Yes |

## RFP Response Template

```
[Company Name] uses Amazon ECS for card processing:

Architecture:
├── ECS Launch Type: Fargate (serverless)
├── Task Definitions: Microservices architecture
├── Data Layer: RDS + DynamoDB + ElastiCache
└── Networking: ALB + Service Connect

PCI-DSS Certificate: [LINK]
Source: https://aws.amazon.com/compliance/pci-dss-faq/
```

## Related
- [[infrastructure-aws-eks]] — AWS EKS patterns
- [[infrastructure-aws-rds]] — AWS RDS database options
