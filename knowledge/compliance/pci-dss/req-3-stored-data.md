---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 3
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, stored-data, encryption, requirement-3]
---

# PCI-DSS Requirement 3: Protect Stored Account Data

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Protect stored account data by:
> - Keeping storage of cardholder data to a minimum
> - Rendering PAN unreadable anywhere it is stored
> - Securing cryptographic keys
> - Documenting and implementing data retention and disposal policies
> - Retaining audit trail history"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 3)

## Critical Data Protection Rules

### What Can Be Stored
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.3)

| Data Element | Storage Allowed | Protection Required |
|--------------|-----------------|---------------------|
| Primary Account Number (PAN) | YES | Encryption, truncation, hashing, or tokenization |
| Cardholder Name | YES | If stored with PAN, must be protected |
| Expiration Date | YES | If stored with PAN, must be protected |
| Service Code | YES | If stored with PAN, must be protected |

### What Cannot Be Stored
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.2)

**NEVER Store Sensitive Authentication Data (SAD)**:
- Full track data (from magnetic stripe or chip)
- Card Verification Code/Value (CVC/CVV/CID)
- PINs or PIN blocks
- Cardholder data in plaintext

**Even if encrypted** - these must never be stored after authorization

### Display Requirements
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.3)

When displaying PAN:
- Show first 6 and last 4 digits only
- Mask all middle digits
- Maximum displayed: 6••••••••1234

## Implementation Requirements

### 3.1 Data Retention Policy
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.1)

- Retain cardholder data only as long as needed for business
- Implement data retention and disposal policies
- Quarterly review to verify compliance

### 3.2 Sensitive Authentication Data Protection
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.2)

- Securely delete SAD immediately after authorization
- If SAD must be stored temporarily, encrypt with strong cryptography
- Verify no SAD is retained beyond authorization

### 3.3 PAN Display and Storage
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.3)

- Mask PAN when displayed
- Render PAN unreadable when stored
- Use industry-standard methods (encryption, truncation, hashing, tokenization)

### 3.4 Cryptographic Key Management
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.5)

- Secure key generation
- Secure key distribution
- Secure key storage
- Key rotation processes
- Retirement or replacement of keys

### 3.5 Cryptography Standards
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.5)

- Use strong cryptography (industry accepted)
- Follow NIST or equivalent standards
- Document all cryptographic implementations

## Implementation in Cloud Infrastructure

### AWS Data Protection
**Source**: https://docs.aws.amazon.com/encryption/latest/latest/overview.html

```
Encryption Options:
├── AWS KMS (Key Management Service) - Key management
├── AWS CloudHSM - Hardware security module
├── ACM (Certificate Manager) - SSL/TLS certificates
├── S3 Encryption - Server-side and client-side
├── EBS Encryption - Volume encryption
└── RDS Encryption - Database encryption
```

**Tokenization Options**:
- AWS Payment Cryptography (formerly AWS CloudHSM for payments)
- Amazon DynamoDB Encryption Client
- Third-party tokenization services

### Azure Data Protection
**Source**: https://learn.microsoft.com/en-us/azure/security/fundamentals/encryption-overview

```
Encryption Options:
├── Azure Key Vault - Key management
├── Azure Dedicated HSM - Hardware security module
├── Azure Disk Encryption - Volume encryption
├── Azure Storage Service Encryption - Storage encryption
├── SQL Database TDE - Database encryption
└── Azure Confidential Computing - Encrypted compute
```

**Tokenization Options**:
- Azure Payment HSM
- Microsoft PayShield HSM
- Third-party tokenization integrated via Azure

### GCP Data Protection
**Source**: https://cloud.google.com/security/encryption

```
Encryption Options:
├── Cloud KMS - Key management
├── Cloud HSM - Hardware security module
├── Persistent Disk Encryption - Volume encryption
├── Cloud SQL Encryption - Database encryption
├── Cloud Storage Encryption - Storage encryption
└── Application Secret Manager - Secrets management
```

## Tokenization Best Practices

**Source**: Industry practice based on PCI SSC guidelines

Tokenization replaces sensitive data with non-sensitive equivalents:

```
Original PAN: 1234567890123456
Token:        tok_abc123xyz789def

Benefits:
- Reduces PCI-DSS scope significantly
- Tokens can be stored without encryption
- Original data stored in secure token vault
- Reduces risk of data breach exposure
```

**Tokenization vs Encryption**:
| Aspect | Tokenization | Encryption |
|--------|--------------|------------|
| Scope Reduction | Yes, significant | No, same scope |
| Format Preservation | Possible | No |
| Reversibility | Yes, via vault | Yes, via key |
| Data Analytics | Limited | Possible |

## Evidence Required

For PCI-DSS audit of Requirement 3:
- [ ] Data retention and disposal policy
- [ ] Data inventory and classification
- [ ] Encryption key management procedures
- [ ] Tokenization implementation documentation
- [ ] Quarterly data disposal verification
- [ ] Cryptographic documentation
- [ ] Key rotation records

## RFP Response Template

### Question: "How do you protect stored cardholder data?"

```
[Company Name] implements PCI-DSS Requirement 3 through:

1. Data Minimization
   - Store only necessary cardholder data elements
   - Never store sensitive authentication data (CVC, PIN, track data)
   - Automatic data purging per retention policy
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.1)

2. Encryption at Rest
   - All cardholder data encrypted using [AES-256]
   - Key management through [AWS KMS/Azure Key Vault/GCP KMS]
   - Annual key rotation enforced
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.5)

3. Tokenization
   - PAN tokenization for all non-authorization systems
   - Secure token vault with HSM protection
   - Token format: [16-digit format-preserving]
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.3)

4. Display Protection
   - PAN masked in all displays: 6••••••••1234
   - Logs contain only masked PAN
   - Customer service tools display masked data only
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.3)

5. Key Management
   - Hardware Security Module (HSM) for key storage
   - Dual control and split knowledge for key access
   - Automated key rotation every [12 months]
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.5)

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 3 months]
```

## Common Questions

### Q: Can we store the full PAN for recurring transactions?
A: Yes, but it must be protected with strong encryption or tokenization. The storage must be justified by business need and documented.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.1, 3.3)

### Q: Is tokenization required?
A: Not required but highly recommended. Tokenization significantly reduces PCI-DSS scope by protecting the primary account number.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 3.1, 3.3)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-3/`
- [ ] Encryption configuration documents
- [ ] Key management procedures
- [ ] Data retention policy
- [ ] Data disposal records
- [ ] Tokenization architecture

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-1]] — Network security controls
- [[pci-dss-req-4]] — Data in transit protection
- [[card-systems-tokenization]] — Tokenization implementation
