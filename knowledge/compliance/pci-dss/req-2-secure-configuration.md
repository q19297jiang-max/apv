---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Requirement 2"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, secure-configuration, requirement-2]
---

# PCI-DSS Requirement 2: Secure Configurations

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Apply secure configurations to all system components as follows:
> - Establish and implement configuration standards
> - Develop configuration standards for all system components
> - Configure security parameters
> - Maintain inventory of system components
> - Remove unnecessary functionality and software"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 2)

## Implementation Requirements

### 2.1 Configuration Standards
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.1)

Configuration standards must include:
- Approved configuration settings
- Requirements for installing new systems
- Verification processes for configurations

### 2.2 System Components Inventory
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.2)

Maintain up-to-date inventory of:
- Hardware components
- Software applications
- Virtual systems and containers

### 2.3 Default Security Settings
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.3)

- Change default vendor passwords before deploying systems
- Remove/disable unnecessary default accounts
- Configure security settings according to standards

### 2.4 Shared System Components
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.4)

For systems shared with other entities:
- Ensure only required processes and protocols are allowed
- Implement authentication and access controls

### 2.5 Encryption Configuration
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.5)

- Use strong cryptography for all cryptographic operations
- Follow NIST or equivalent standards
- Document all encryption configurations

### 2.6 Documentation
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.6)

- Document all configuration standards
- Review and update at least annually
- Verify all systems adhere to standards

## Implementation in Cloud Infrastructure

### AWS Secure Configuration
**Source**: https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards.html

```
Configuration Management:
├── AWS Config - Configuration tracking and compliance
├── AWS Systems Manager - Configuration management
├── Security Hub - Centralized security compliance
├── IAM Access Analyzer - Permission validation
└── AWS Control Tower - Landing zone governance
```

**Key Configurations**:
- S3 buckets: Block public access, encryption enabled
- EC2 instances: No public IP for database tier, IMDSv2 required
- RDS: Encryption at rest, enforce SSL/TLS
- VPC: No internet gateway for private subnets

### Azure Secure Configuration
**Source**: https://learn.microsoft.com/en-us/azure/security/fundamentals/network-best-practices

```
Configuration Management:
├── Azure Policy - Enforce organizational standards
├── Azure Security Center - Security posture management
├── Azure Blueprints - Repeatable deployments
├── Azure Monitor - Configuration drift detection
└── Microsoft Defender for Cloud - Threat protection
```

**Key Configurations**:
- Storage accounts: Require HTTPS, disable public access
- Virtual Machines: Azure Disk Encryption, NSG-protected
- SQL Database: Transparent Data Encryption (TDE)
- Key Vault: Bring Your Own Key (BYOK) support

### GCP Secure Configuration
**Source**: https://cloud.google.com/security/best-practices

```
Configuration Management:
├── Security Command Center - Security posture
├── Organization Policy - Constraints enforcement
├── Config Controller - Policy-as-code
├── Cloud Asset Inventory - Resource tracking
└── Recommender - Security optimization
```

**Key Configurations**:
- Cloud Storage: Uniform bucket-level access, encryption
- Compute Engine: Shielded VMs, OS Login
- Cloud SQL: Automatic encryption, authorized networks
- Organization Policy: Domain-restricted sharing

## Evidence Required

For PCI-DSS audit of Requirement 2:
- [ ] Configuration standards documentation
- [ ] System component inventory
- [ ] Configuration review reports (annual)
- [ ] Change management records
- [ ] Hardening guidelines
- [ ] Encryption configuration documentation

## RFP Response Template

### Question: "How do you ensure secure system configurations?"

```
[Company Name] implements PCI-DSS Requirement 2 through:

1. Configuration Standards
   - Documented security configuration standards for all systems
   - Automated compliance checking using [AWS Config/Azure Policy/GCP Organization Policy]
   - Annual review and update of all standards
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.1)

2. System Inventory
   - Automated discovery and tracking of all system components
   - Configuration drift detection and alerting
   - Change logging and approval workflows
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.2)

3. Hardening Procedures
   - Vendor defaults changed before deployment
   - Unnecessary services and features removed
   - Regular vulnerability scanning
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.3)

4. Encryption Configuration
   - All data encrypted at rest using [AES-256]
   - All data encrypted in transit using [TLS 1.3]
   - Key management through [AWS KMS/Azure Key Vault/GCP KMS]
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.5)

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 12 months]
```

## Common Questions

### Q: What are "system components"?
A: Any network device, server, application, or virtual system that stores, processes, or transmits cardholder data. This includes virtual machines, containers, serverless functions, and cloud services.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Glossary)

### Q: How often must configurations be reviewed?
A: Configuration standards must be reviewed at least annually. Actual configurations should be continuously monitored for compliance using automated tools.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 2.1, 2.6)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-2/`
- [ ] Configuration standards documents
- [ ] System inventory reports
- [ ] Compliance scan results
- [ ] Configuration change logs

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-1]] — Network security controls
- [[pci-dss-req-3]] — Stored data protection
- [[infrastructure-aws]] — AWS secure configurations
