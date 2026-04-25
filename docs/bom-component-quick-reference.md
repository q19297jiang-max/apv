# BOM Component Quick Reference

**Purpose**: Quick reference for creating detailed BOM components with exact specifications

## AWS Component Specification Template

### Compute (EC2)

```json
{
  "name": "EC2 Application Server",
  "instance_type": "m6i.xlarge",
  "spec": "General purpose application server",
  "detailed_spec": "m6i.xlarge (4 vCPU, 16 GiB, EBS-only, up to 12.5 Gbps network)",
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
  "sizing_justification": "Medium application server, supports up to 500 TPS",
  "notes": "Deployed across 2 AZs"
}
```

### Database (RDS)

```json
{
  "name": "RDS PostgreSQL",
  "instance_type": "db.m6i.xlarge",
  "spec": "PostgreSQL Multi-AZ database",
  "detailed_spec": "db.m6i.xlarge (4 vCPU, 16 GiB, Multi-AZ, gp3 storage)",
  "hardware_spec": {
    "instance_type": "db.m6i.xlarge",
    "vcpu": 4,
    "memory": 16,
    "storage": "gp3",
    "deployment": "Multi-AZ"
  },
  "unit_price": 0.376,
  "quantity": 1,
  "unit": "ea/month",
  "monthly_cost": 274.48,
  "annual_cost": 3293.76,
  "source_url": "https://aws.amazon.com/rds/postgresql/pricing/",
  "calculator_url": "https://calculator.aws/",
  "verified_date": "2026-04-25",
  "sizing_justification": "Medium database for card transaction data",
  "notes": "Multi-AZ deployment for high availability"
}
```

### Cache (ElastiCache)

```json
{
  "name": "ElastiCache Redis",
  "instance_type": "cache.m6g.xlarge",
  "spec": "Redis cache for session data",
  "detailed_spec": "cache.m6g.xlarge (4 vCPU, 13.5 GiB, Redis 7)",
  "hardware_spec": {
    "instance_type": "cache.m6g.xlarge",
    "vcpu": 4,
    "memory": 13.5,
    "engine": "Redis 7"
  },
  "unit_price": 0.312,
  "quantity": 2,
  "unit": "ea/month",
  "monthly_cost": 455.52,
  "annual_cost": 5466.24,
  "source_url": "https://aws.amazon.com/elasticache/pricing/",
  "calculator_url": "https://calculator.aws/",
  "verified_date": "2026-04-25",
  "sizing_justification": "Medium cache for session management",
  "notes": "Redis Cluster mode enabled"
}
```

### Load Balancer (ALB)

```json
{
  "name": "Application Load Balancer",
  "instance_type": "alb",
  "spec": "ALB for application traffic distribution",
  "detailed_spec": "ALB (0.0225/hour, 0.008/LCU-hour)",
  "hardware_spec": {
    "type": "application",
    "hourly_rate": 0.0225,
    "lcu_rate": 0.008
  },
  "unit_price": 0.0225,
  "quantity": 2,
  "unit": "ea/month",
  "monthly_cost": 32.85,
  "annual_cost": 394.20,
  "source_url": "https://aws.amazon.com/elasticloadbalancing/pricing/",
  "calculator_url": "https://calculator.aws/",
  "verified_date": "2026-04-25",
  "sizing_justification": "2 ALBs for high availability across AZs",
  "notes": "Includes LCU consumption charges"
}
```

### Container (EKS)

```json
{
  "name": "EKS Cluster",
  "instance_type": "eks",
  "spec": "Kubernetes control plane",
  "detailed_spec": "EKS Cluster (0.10/hour per cluster)",
  "hardware_spec": {
    "type": "kubernetes",
    "hourly_rate": 0.10
  },
  "unit_price": 0.10,
  "quantity": 1,
  "unit": "cluster/month",
  "monthly_cost": 73.00,
  "annual_cost": 876.00,
  "source_url": "https://aws.amazon.com/eks/pricing/",
  "calculator_url": "https://calculator.aws/",
  "verified_date": "2026-04-25",
  "sizing_justification": "Single EKS cluster for card processing workloads",
  "notes": "Control plane managed by AWS"
}
```

## SaaS Component Template

```json
{
  "name": "Card Management Core",
  "spec": "Standard Tier SaaS Card Management Platform",
  "detailed_spec": "Standard Tier: up to 10 TPS, core lifecycle management, PCI-DSS compliant",
  "quantity": 1,
  "unit": "system",
  "monthly_cost": 500.00,
  "annual_cost": 6000.00,
  "source_url": "Internal SaaS Rate Sheet v2.3",
  "verified_date": "2026-04-25",
  "sizing_justification": "Standard tier supports current volume requirements",
  "notes": "Includes 24/7 support and SLA guarantees"
}
```

## Common Instance Types Reference

### EC2 Instance Families

| Family | Use Case | Instance Types | Price Range |
|--------|----------|----------------|-------------|
| General Purpose | Balanced compute/memory | m6i.large/xlarge/2xlarge | $0.096-$0.384/hr |
| Compute Optimized | High compute requirements | c6i.large/xlarge/2xlarge | $0.085-$0.340/hr |
| Memory Optimized | High memory requirements | r6i.large/xlarge/2xlarge | $0.126-$0.504/hr |

### RDS Instance Families

| Instance | vCPU | Memory | Price/Hour | Use Case |
|----------|------|--------|------------|----------|
| db.m6i.large | 2 | 8 GiB | $0.188 | Small DB |
| db.m6i.xlarge | 4 | 16 GiB | $0.376 | Medium DB |
| db.m6i.2xlarge | 8 | 32 GiB | $0.752 | Large DB |
| db.r6i.large | 2 | 16 GiB | $0.252 | Memory DB |
| db.r6i.xlarge | 4 | 32 GiB | $0.504 | Large Memory |

### ElastiCache Instance Families

| Instance | vCPU | Memory | Price/Hour | Use Case |
|----------|------|--------|------------|----------|
| cache.m6g.large | 2 | 5.3 GiB | $0.156 | Session cache |
| cache.m6g.xlarge | 4 | 13.5 GiB | $0.312 | Medium cache |
| cache.m6g.2xlarge | 8 | 29 GiB | $0.624 | Large cache |
| cache.r6g.large | 2 | 13.3 GiB | $0.208 | Memory cache |
| cache.r6g.xlarge | 4 | 32.3 GiB | $0.416 | Large memory |

## Cost Calculation Formulas

```javascript
// EC2/RDS/ElastiCache
monthly_cost = hourly_price × 730 × quantity
annual_cost = monthly_cost × 12

// ALB/NLB
monthly_cost = (hourly_rate × 730 × quantity) + (lcu_consumption × lcu_rate × 730)

// EKS
monthly_cost = hourly_rate × 730 × cluster_count

// Storage
monthly_cost = price_per_gb × storage_gb

// Total
total_monthly = sum(component_monthly_costs)
total_annual = sum(component_annual_costs)
```

## Regional Multipliers

| Region | Multiplier | Examples |
|--------|------------|----------|
| ap-southeast-1 (Singapore) | 1.00x | Base pricing |
| ap-southeast-3 (Malaysia) | 1.10x | Base × 1.10 |
| ap-northeast-1 (Taiwan) | 1.05x | Base × 1.05 |
| ap-east-1 (Hong Kong) | 1.10x | Base × 1.10 |

## Verification Checklist

For each BOM component, verify:
- [ ] Exact instance type specified
- [ ] Hardware specifications complete (vCPU, memory, storage)
- [ ] Unit price from official source
- [ ] Source URL included and valid
- [ ] Calculator URL included (for AWS)
- [ ] Sizing justification provided
- [ ] Verification date included
- [ ] Quantity and total cost calculated correctly

## Related

- [[detailed-bom-specifications]] — Detailed BOM enhancement documentation
- [[aws-component-catalog]] — AWS component reference catalog
- [[rfp-pricer]] — Pricing skill
