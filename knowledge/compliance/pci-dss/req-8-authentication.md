---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 8
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, authentication, mfa, requirement-8]
---

# PCI-DSS Requirement 8: Identify and Authenticate Access

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Identify and authenticate access to system components by:
> - Assigning unique ID to each person
> - Implementing multi-factor authentication
> - Using strong cryptography
> - Removing inactive user accounts
> - Managing authentication credentials"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 8)

## Implementation Requirements

### 8.1 Unique Identification
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.1)

- Assign unique ID to each person with computer access
- Prevent shared accounts
- Remove inactive user accounts

### 8.2 Multi-Factor Authentication (MFA)
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.2)

- Implement MFA for all access to cardholder data environment
- MFA required for:
  - Remote network access
  - Administrative access
  - All user access to cardholder data

### 8.3 Strong Authentication
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.3)

- Use strong cryptography for authentication
- Enforce strong password policies
- Protect credentials in transit and at rest

### 8.4 Credential Management
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.4)

- Secure password storage
- Regular password changes
- Prevent password reuse

## Authentication Methods

### MFA Implementation
**Source**: Industry best practices for PCI-DSS compliance

```
MFA Factors (choose two or more):
├── Knowledge: Something you know (password, PIN)
├── Possession: Something you have (token, phone, smart card)
└── Inherence: Something you are (biometric)

Common Implementations:
├── TOTP (Time-based One-Time Password) - Google Authenticator, Authy
├── SMS/Email OTP - One-time password via SMS/email
├── Hardware Token - YubiKey, RSA SecurID
├── Push Notification - Mobile app approval
└── Biometric - Fingerprint, facial recognition
```

### Password Requirements
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.3)

| Requirement | Minimum Standard |
|-------------|------------------|
| Length | 12+ characters |
| Complexity | Mixed case, numbers, symbols |
| Expiration | 90 days (or password-less) |
| History | 24 previous passwords |
| Lockout | 6 failed attempts |

## Implementation in Cloud Infrastructure

### AWS Authentication
**Source**: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable.html

```
Components:
├── AWS IAM MFA - Hardware and virtual MFA
├── AWS SSO - Centralized authentication
├── AWS Directory Service - Managed Active Directory
├── AWS Cognito - User authentication for applications
└── Secrets Manager - Secure credential storage
```

### Azure Authentication
**Source**: https://learn.microsoft.com/en-us/azure/active-directory/

```
Components:
├── Azure AD Multi-Factor Authentication - MFA service
├── Azure AD Password Protection - Password policy enforcement
├── Azure AD Conditional Access - Context-based authentication
├── Azure AD Identity Protection - Threat detection
└── Azure Key Vault - Secure credential storage
```

### GCP Authentication
**Source**: https://cloud.google.com/identity

```
Components:
├── Cloud Identity - Identity and access management
├── Google Cloud MFA - Multi-factor authentication
├── BeyondCorp Enterprise - Zero-trust access
├── Context-Aware Access - Context-based authentication
└── Secret Manager - Secure credential storage
```

## Evidence Required

For PCI-DSS audit of Requirement 8:
- [ ] Authentication policy
- [ ] MFA implementation documentation
- [ ] Password policy documentation
- [ ] User account review reports
- [ ] MFA coverage documentation
- [ ] Authentication testing results

## RFP Response Template

### Question: "How do you authenticate users?"

```
[Company Name] implements PCI-DSS Requirement 8 through:

1. Multi-Factor Authentication
   - MFA required for all access to cardholder data
   - MFA required for all administrative access
   - MFA required for remote access
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.2)

2. Identity Management
   - Unique user IDs for all individuals
   - No shared accounts
   - Automated account provisioning/deprovisioning
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.1)

3. Password Security
   - Strong password policy enforced (12+ characters, complexity)
   - Password expiration every 90 days
   - Password history prevents reuse
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 8.3)

4. Cloud Provider Services
   - [AWS SSO/Azure AD/GCP Cloud Identity] for authentication
   - MFA integration with [platform]
   - Single Sign-On (SSO) for enterprise
   Source: [Cloud provider documentation]

Compliance verified by: [Compliance Officer] on [DATE]
```

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-7]] — Access control requirements
