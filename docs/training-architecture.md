---
type: apv-meta
category: documentation
title: "APV Architecture Team Training Guide"
created: 2026-04-24
tags: [apv, documentation, training, architecture]
---

# APV Architecture Team Training Guide

**Audience**: Architecture Team
**Duration**: 30 minutes
**Prerequisites**: Understanding of cloud architecture and payment systems

---

## Learning Objectives

After this training, you will be able to:
1. Understand APV's architecture design process
2. Review architecture recommendations
3. Validate component selections
4. Verify security controls mapping
5. Approve architecture designs

---

## APV Architecture Process

### Skill 3: rfp-architect

**Purpose**: Design detailed payment architecture

**Input**: RFP document + compliance output

**Output**: Architecture design with component specifications

**Time**: 10-15 minutes

**What it does**:
- Analyzes RFP requirements
- Selects cloud provider and region
- Specifies components (compute, database, storage, network)
- Maps security controls to PCI-DSS requirements
- Plans high availability and disaster recovery

---

## Architecture Components

### Card System Types

| Type | Description | Wiki Reference |
|------|-------------|----------------|
| Issuing | Credit/debit card issuance | [[issuing]] |
| Acquiring | Merchant acquisition | [[acquiring]] |
| Gateway | Payment gateway | [[gateway]] |
| Digital Wallet | Mobile wallet integration | [[digital-wallet]] |
| Tokenization | Payment tokenization | [[tokenization]] |
| 3DS | 3-D Secure authentication | [[3ds]] |
| Authorization | Authorization processing | [[authorization]] |

### Cloud Providers

| Provider | Singapore Region | Wiki Reference |
|----------|-----------------|----------------|
| AWS | ap-southeast-1 | [[aws-eks]], [[aws-rds]], [[aws-dr]] |
| Azure | southeastasia | [[azure-aks]], [[azure-db]] |
| GCP | asia-southeast1 | [[gcp-gke]], [[gcp-cloudsql]] |

---

## Architecture Design Checklist

### Step 1: Review Card System Type

**File**: `outputs/03-architecture.md`

**Check**:
- [ ] Correct card type identified (issuing/acquiring/gateway)
- [ ] All required components included
- [ ] Component interactions documented

### Step 2: Validate Cloud Selection

**Check**:
- [ ] Cloud provider appropriate for region
- [ ] Region selected based on data residency
- [ ] Services available in selected region
- [ ] Cost considerations addressed

### Step 3: Verify Security Controls

**Check**:
- [ ] Security controls mapped to PCI-DSS requirements
- [ ] Encryption at rest specified
- [ ] Encryption in transit specified
- [ ] Access control defined
- [ ] Logging and monitoring included

### Step 4: Review High Availability

**Check**:
- [ ] Multi-AZ deployment specified
- [ ] Failover mechanisms defined
- [ ] Backup strategy included
- [ ] RTO/RPO requirements met

### Step 5: Validate Disaster Recovery

**Check**:
- [ ] DR strategy documented
- [ ] Recovery procedures defined
- [ ] DR testing plan included
- [ ] Data replication specified

---

## Architecture Patterns

### Pattern 1: Cloud-Native (EKS/AKS/GKE)

**Best For**: Production deployments, scalability requirements

**Components**:
- Compute: EKS/AKS/GKE (managed Kubernetes)
- Database: RDS/Cloud SQL/Cloud SQL
- Storage: S3/Blob Storage/Cloud Storage
- Network: VPC with private subnets
- Security: Security groups, NACLs, WAF

**Advantages**:
- Managed services
- Auto-scaling
- High availability
- PCI-DSS compliant

**When to Use**: TPS > 1, requires scaling

### Pattern 2: Container-Based (ECS/Cloud Run)

**Best For**: Lower volume, simpler deployments

**Components**:
- Compute: ECS/Cloud Run
- Database: RDS/Cloud SQL
- Storage: S3/Cloud Storage
- Network: VPC with private subnets

**Advantages**:
- Simpler than Kubernetes
- Cost-effective for lower volume
- Still PCI-DSS compliant

**When to Use**: TPS < 5, simpler requirements

### Pattern 3: SaaS Multi-Tenant

**Best For**: Entry-level, low volume

**Components**:
- Shared infrastructure
- Multi-tenant database
- Isolated tenant data

**Advantages**:
- Lowest cost
- Fastest deployment
- Vendor-managed compliance

**When to Use**: TPS < 1, budget constraints

---

## Security Controls Mapping

### PCI-DSS Requirement Mapping

| PCI-DSS Req | Control | Implementation |
|-------------|---------|----------------|
| Req 1: Network Security | Firewall | Security groups, NACLs |
| Req 2: Secure Configuration | Hardened images | CIS benchmarks, AMIs |
| Req 3: Card Data Protection | Encryption | TLS 1.3, AES-256 |
| Req 4: Encryption | Encryption at rest | KMS, Customer-managed keys |
| Req 5: Anti-Malware | Endpoint protection | GuardDuty, Sentinel |
| Req 6: Secure Development | Code scanning | SAST, dependency scanning |
| Req 7: Access Control | IAM | RBAC, least privilege |
| Req 8: Authentication | MFA | AWS IAM, AD integration |
| Req 9: Physical Access | Data center | Cloud provider controls |
| Req 10: Logging | CloudTrail | Audit logging |
| Req 11: Monitoring | CloudWatch | SIEM integration |
| Req 12: Security Policy | Policies | Security documentation |

---

## Architecture Review Process

### 1. Initial Review

**When**: After rfp-architect completes

**What to Check**:
- Card system type correct?
- Cloud provider appropriate?
- All components specified?
- Security controls mapped?

### 2. Detailed Review

**When**: After rfp-calculator completes

**What to Check**:
- Sizing matches architecture?
- Components sized correctly?
- Capacity planning included?
- Growth considered?

### 3. Final Review

**When**: After rfp-generator completes

**What to Check**:
- Architecture consistent in response?
- Diagrams included?
- Justifications provided?
- Alternatives considered?

---

## Common Issues

### Issue 1: Wrong Card System Type

**Symptom**: Architecture doesn't match RFP requirements

**Solution**:
1. Verify card type in RFP (issuing vs acquiring)
2. Check if multiple types needed
3. Re-run rfp-architect with clarification

### Issue 2: Region Not Supported

**Symptom**: Selected region doesn't support required services

**Solution**:
1. Check cloud provider service availability
2. Select alternative region
3. Consider multi-region deployment

### Issue 3: Security Controls Missing

**Symptom**: PCI-DSS requirements not mapped

**Solution**:
1. Review compliance matrix
2. Map missing controls
3. Update architecture design

### Issue 4: Over/Under Provisioned

**Symptom**: Sizing doesn't match requirements

**Solution**:
1. Review TPS calculations
2. Check growth projections
3. Adjust component sizing

---

## Architecture Templates

### Issuing System Template

```
┌─────────────────────────────────────────────────┐
│                   Internet                      │
└─────────────────────────────────────────────────┘
                        │
                    [WAF + CDN]
                        │
              ┌─────────┴─────────┐
              │   Load Balancer  │
              └─────────┬─────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   [Card Mgmt]     [PIN Pad]      [HSM]
        │               │               │
        └───────────────┼───────────────┘
                        │
              ┌─────────┴─────────┐
              │   Authorization   │
              │   Processing     │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │   Database (Enc)  │
              └───────────────────┘
```

### Acquiring System Template

```
┌─────────────────────────────────────────────────┐
│                 Merchants                       │
└─────────────────────────────────────────────────┘
                        │
                    [POS/API]
                        │
              ┌─────────┴─────────┐
              │   Gateway        │
              │   (Multi-tenant) │
              └─────────┬─────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   [Settlement]   [Routing]      [Reporting]
```

---

## Knowledge Base References

### Card Systems

- `wiki/apv/knowledge/card-systems/issuing.md` - Issuing system design
- `wiki/apv/knowledge/card-systems/acquiring.md` - Acquiring system design
- `wiki/apv/knowledge/card-systems/gateway.md` - Gateway design
- `wiki/apv/knowledge/card-systems/digital-wallet.md` - Digital wallet integration

### Infrastructure

- `wiki/apv/knowledge/infrastructure/aws-eks.md` - AWS EKS patterns
- `wiki/apv/knowledge/infrastructure/azure-aks.md` - Azure AKS patterns
- `wiki/apv/knowledge/infrastructure/gcp-gke.md` - GCP GKE patterns
- `wiki/apv/knowledge/infrastructure/aws-rds.md` - AWS RDS patterns
- `wiki/apv/knowledge/infrastructure/aws-dr.md` - AWS DR patterns

---

## Getting Help

### Documentation

- [[apv-user-guide]] - Complete user guide
- [[apv-skill-reference]] - rfp-architect skill details
- [[apv-knowledge-index]] - Architecture knowledge base

### Examples

- `wiki/apv/tests/output/bbc-architecture-output.md` - Sample architecture output

### Support

For architecture questions:
1. Check knowledge base
2. Review past RFP architectures
3. Consult with solution architect

---

**Training Duration**: 30 minutes
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
