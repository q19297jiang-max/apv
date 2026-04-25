---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Overview"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, overview]
---

# PCI-DSS Overview

## What is PCI-DSS?

Payment Card Industry Data Security Standard (PCI-DSS) is a global security standard designed to ensure that ALL companies that process, store, or transmit credit card information maintain a secure environment.

## Official Source

**Source URL**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf
**Document**: PCI-DSS v4.0
**Managing Organization**: PCI Security Standards Council (PCI SSC)
**Website**: https://www.pcisecuritystandards.org/

## Key Information

### Scope
Applies to ANY organization that accepts, transmits, or stores cardholder data:
- Merchants
- Service Providers
- Payment Processors
- Acquirers
- Issuers

### Validation Levels
| Level | Criteria | Annual Audit |
|-------|----------|--------------|
| 1 | >6M transactions/year | ROC Audit by QSA |
| 2 | 1M-6M transactions/year | SAQ + Vulnerability Scan |
| 3 | 20K-1M e-commerce transactions/year | SAQ + Vulnerability Scan |
| 4 | <20K e-commerce transactions/year | SAQ + Vulnerability Scan |

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Section 1: Overview)

### The 12 Requirements

#### Goal 1: Protect Cardholder Data
- **Requirement 1**: Install and maintain network security controls
- **Requirement 2**: Apply secure configurations to all system components
- **Requirement 3**: Protect stored account data

#### Goal 2: Protect Cardholder Data
- **Requirement 4**: Protect cardholder data in transit

#### Goal 3: Maintain Vulnerability Management
- **Requirement 5**: Protect all systems and networks from malicious software
- **Requirement 6**: Develop and maintain secure systems and software

#### Goal 4: Implement Strong Access Control
- **Requirement 7**: Restrict access to system components and cardholder data
- **Requirement 8**: Identify users and authenticate access
- **Requirement 9**: Restrict physical access to cardholder data

#### Goal 5: Monitor and Test Networks
- **Requirement 10**: Log and monitor all access to system components and cardholder data
- **Requirement 11**: Test security of systems and networks regularly

#### Goal 6: Maintain Information Security
- **Requirement 12**: Support information security with organizational policies and programs

## Cardholder Data Protection

### What Must Be Protected
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 3)

**Primary Account Number (PAN)**: Must be encrypted
**Cardholder Name**: Must be protected if stored with PAN
**Service Code**: Must be protected if stored with PAN
**Expiration Date**: Must be protected if stored with PAN

### What Can Be Displayed
- **First 6 digits** (Issuer Identification Number)
- **Last 4 digits** (for identification)
- **Middle digits MUST be masked**

### Sensitive Authentication Data (NEVER STORE)
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 3.2)

- Full track data from magnetic stripe or chip
- Card Verification Code (CVC2, CVV2, CID)
- PINs or PIN blocks

## RFP Response Template

### Question: "What is your PCI-DSS compliance status?"

```
[Company Name] maintains PCI-DSS v4.0 compliance for all card processing systems.

PCI-DSS Certificate: [LINK TO CERTIFICATE]
Valid from: [DATE] to [DATE]
Issued by: [QUALIFIED SECURITY ASSESSOR]

All systems storing, processing, or transmitting cardholder data are designed and operated in accordance with PCI-DSS v4.0 requirements.

Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf

For detailed compliance mappings, see:
- [[pci-dss-req-1]] — Network Security Controls
- [[pci-dss-req-2]] — Secure Configurations
- [[pci-dss-req-3]] — Stored Data Protection
- [[pci-dss-req-4]] — Data in Transit Protection
- [[pci-dss-req-5]] — Malware Protection
- [[pci-dss-req-6]] — Secure Development
- [[pci-dss-req-7]] — Access Control
- [[pci-dss-req-8]] — Authentication
- [[pci-dss-req-9]] — Physical Access
- [[pci-dss-req-10]] — Logging and Monitoring
- [[pci-dss-req-11]] — Security Testing
- [[pci-dss-req-12]] — Security Policies
```

## Related
- [[pci-dss-req-1]] — Network Security Controls
- [[pci-dss-req-2]] — Secure Configurations
- [[pci-dss-req-3]] — Stored Data Protection
- [[apv-accuracy-assurance]] — Accuracy framework requirements
