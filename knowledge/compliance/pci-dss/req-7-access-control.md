---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Requirement 7"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, access-control, requirement-7]
---

# PCI-DSS Requirement 7: Restrict Access

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Restrict access to system components and cardholder data to only those whose jobs require such access."
>
> **Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 7)

## Implementation Requirements

### 7.1 Access Control Policy
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 7.1)

- Implement access control systems
- Restrict access based on need-to-know
- Default deny all access

### 7.2 Role-Based Access Control
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 7.2)

- Define roles and access requirements
- Assign access based on job function
- Document access privileges

### 7.3 Access Review
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 7.3)

- Review access rights at least every 6 months
- Revoke unnecessary access
- Maintain access logs

## Implementation in Cloud Infrastructure

### AWS IAM
**Source**: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html

```
Components:
├── IAM Users - Individual identities
├── IAM Groups - Role-based access
├── IAM Roles - Temporary credentials
├── IAM Policies - Fine-grained permissions
├── AWS SSO - Centralized access management
└── Access Analyzer - Permission validation
```

**Best Practices**:
- Least privilege principle
- MFA for all human access
- Regular access reviews
- Separate prod/non-prod accounts

## Evidence Required

For PCI-DSS audit of Requirement 7:
- [ ] Access control policy
- [ ] Role definitions and permissions
- [ ] Access review reports (quarterly)
- [ ] Access request procedures
- [ ] Access revocation procedures

## RFP Response Template

### Question: "How do you control access to cardholder data?"

```
[Company Name] implements PCI-DSS Requirement 7 through:

1. Access Control
   - Role-Based Access Control (RBAC) implementation
   - Least privilege principle enforced
   - Multi-factor authentication (MFA) required
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 7.1)

2. Access Management
   - Regular access reviews (quarterly)
   - Automated access provisioning/deprovisioning
   - Access logging and monitoring
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 7.2)

3. Cloud Provider Services
   - [AWS IAM/Azure AD/GCP IAM] for access control
   - Granular permission policies
   - Temporary credentials for elevated access
   Source: [Cloud provider documentation]

Compliance verified by: [Compliance Officer] on [DATE]
```

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-8]] — Authentication requirements
