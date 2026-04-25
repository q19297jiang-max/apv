---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Requirement 9"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, physical-access, requirement-9]
---

# PCI-DSS Requirement 9: Physical Access

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Restrict physical access to cardholder data by:
> - Controlling physical access to sensitive areas
> - Monitoring physical access
> - Maintaining visitor logs
> - Securing physical media
> - Destroying media when no longer needed"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 9)

## Implementation Requirements

### 9.1 Physical Access Controls
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.1)

- Control access to sensitive areas
- Use badge readers, biometrics, or other secure methods
- Verify visitor identity before access

### 9.2 Visitor Management
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.2)

- Maintain visitor log
- Authorize visitor access before entry
- Escort visitors at all times

### 9.3 Physical Media Security
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.3)

- Secure physical media containing cardholder data
- Maintain media inventory
- Destroy media when no longer needed

### 9.4 Monitoring
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.4)

- Use video cameras and/or access logs
- Monitor sensitive areas
- Retain footage for at least 90 days

## Cloud-Specific Considerations

**Note**: In cloud environments, physical security is the responsibility of the cloud provider. Customers must verify provider certifications.

### AWS Physical Security
**Source**: https://aws.amazon.com/compliance/pci-dss-faq/

```
AWS Responsibility:
├── Data center physical security
├── Access control to data centers
├── Video surveillance
├── Security personnel
└── Environmental controls (fire, water, power)

Customer Responsibility:
├── Control who can access cloud consoles
├── MFA for all administrative access
├── Secure endpoints (laptops, mobile devices)
└── Monitor access logs
```

### Azure Physical Security
**Source**: https://learn.microsoft.com/en-us/azure/security/fundamentals/physical-security

```
Azure Responsibility:
├── Data center access control
├── Physical security monitoring
├── Personnel screening
└── Compliance with ISO 27001, SOC 2

Customer Responsibility:
├── Secure administrative access
├── Endpoint security
└── Access monitoring
```

### GCP Physical Security
**Source**: https://cloud.google.com/security/physical-security

```
GCP Responsibility:
├── Data center perimeter security
├── Multi-layered access controls
├── 24/7 security personnel
└── Environmental controls

Customer Responsibility:
├── Administrative access security
├── Endpoint protection
└── Access logging and monitoring
```

## Evidence Required

For PCI-DSS audit of Requirement 9:
- [ ] Physical security policy
- [ ] Access control procedures
- [ ] Visitor log templates
- [ ] Media destruction procedures
- [ ] Video retention policy
- [ ] Data center access reports

## RFP Response Template

### Question: "How do you protect physical access?"

```
[Company Name] implements PCI-DSS Requirement 9 through:

1. Cloud Provider Physical Security
   - [AWS/Azure/GCP] data centers PCI-DSS certified
   - Multi-layered physical security controls
   - 24/7 security personnel and monitoring
   Source: [Cloud provider PCI-DSS compliance documentation]

2. Administrative Access Security
   - MFA required for all cloud console access
   - Access logging and monitoring
   - Regular access reviews
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.1)

3. Endpoint Security
   - Full disk encryption on all company devices
   - Anti-malware protection
   - Secure remote access procedures
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.3)

4. Media Management
   - Secure media disposal procedures
   - Media inventory and tracking
   - Certificate of destruction for sensitive media
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 9.3)

Compliance verified by: [Compliance Officer] on [DATE]
```

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-7]] — Access control requirements
