---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 4
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, data-in-transit, tls, requirement-4]
---

# PCI-DSS Requirement 4: Protect Cardholder Data in Transit

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Protect cardholder data in transit by:
> - Using strong cryptography and security protocols
> - Authenticating all transmissions
> - Protecting sensitive data during transmission over open, public networks
> - Verifying security protocols and configurations before transmission"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 4)

## Implementation Requirements

### 4.1 Strong Cryptography and Security Protocols
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

- Use strong cryptography (TLS 1.2 or higher)
- Use secure protocols (HTTPS, SSH, SFTP, etc.)
- Disable weak protocols (SSL, TLS 1.0, TLS 1.1)
- Configure cipher suites appropriately

### 4.2 Secure Authentication
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.2)

- Authenticate all transmissions of cardholder data
- Use secure authentication mechanisms
- Protect credentials during transmission

### 4.3 Protection Over Public Networks
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.3)

- Encrypt cardholder data during transmission over open, public networks
- Use only trusted security keys/certificates
- Implement certificate management

### 4.4 Protocol and Configuration Verification
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.4)

- Verify security protocols and configurations are active
- Perform periodic testing to verify security
- Document all configurations

## Approved Protocols

### TLS Versions
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

| Protocol | Status | Action Required |
|----------|--------|-----------------|
| TLS 1.3 | ✅ Approved | Use when available |
| TLS 1.2 | ✅ Approved | Minimum required |
| TLS 1.1 | ❌ Deprecated | Disable |
| TLS 1.0 | ❌ Deprecated | Disable |
| SSL 3.0 | ❌ Deprecated | Disable |
| SSL 2.0 | ❌ Deprecated | Disable |

### Cipher Suites
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

**Approved**: AES-GCM, ChaCha20-Poly1305, ECDHE, DHE
**Deprecated**: RC4, DES, 3DES, CBC-mode ciphers

## Implementation in Cloud Infrastructure

### AWS TLS Implementation
**Source**: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html

```
Components:
├── Application Load Balancer - TLS termination
├── Network Load Balancer - TLS passthrough
├── AWS Certificate Manager (ACM) - Certificate management
├── AWS CloudFront - Global TLS for CDN
├── AWS API Gateway - TLS for APIs
└── AWS S3 - HTTPS only enforcement
```

**Configuration**:
- TLS 1.2 and 1.3 only
- Forward secrecy cipher suites
- Perfect Forward Secrecy (PFS) required
- Certificate auto-renewal via ACM

### Azure TLS Implementation
**Source**: https://learn.microsoft.com/en-us/azure/web-application-security/managed-certificates

```
Components:
├── Application Gateway - TLS termination
├── Azure Front Door - Global TLS for CDN
├── Azure Key Vault - Certificate management
├── Azure API Management - TLS for APIs
├── Azure CDN - HTTPS enforcement
└── Azure Load Balancer - TLS options
```

**Configuration**:
- TLS 1.2 and 1.3 only
- Policy-based TLS configuration
- Certificate auto-rotation
- OCSP stapling support

### GCP TLS Implementation
**Source**: https://cloud.google.com/load-balancing/docs/ssl-certificates

```
Components:
├── Cloud Load Balancing - TLS termination
├── Cloud CDN - Global TLS for CDN
├── Certificate Manager - Certificate management
├── Cloud Endpoints - TLS for APIs
├── Cloud Storage - HTTPS enforcement
└── Identity-Aware Proxy - TLS with authentication
```

**Configuration**:
- TLS 1.2 and 1.3 only
- Modern TLS profile
- Google-managed certificates
- Automatic certificate provisioning

## Certificate Management

### Certificate Lifecycle
**Source**: Industry best practices for PCI-DSS compliance

```
1. Certificate Authority Selection
   - Use trusted public CAs (DigiCert, Let's Encrypt, etc.)
   - Or implement private CA for internal services

2. Certificate Issuance
   - Generate key pair (minimum 2048-bit RSA or 256-bit ECC)
   - Submit Certificate Signing Request (CSR)
   - Validate domain ownership
   - Install certificate

3. Certificate Monitoring
   - Track expiration dates
   - Set alerts for renewal
   - Monitor certificate transparency logs

4. Certificate Renewal
   - Auto-renew before expiration (recommended 30 days)
   - Test new certificates
   - Deploy without service disruption

5. Certificate Revocation
   - Revoke compromised certificates
   - Update CRL/OCSP
   - Replace with new certificates
```

### Perfect Forward Secrecy (PFS)
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

PFS ensures that compromise of long-term keys does not compromise past session keys:

**Supported Cipher Suites**:
- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
- TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384

**Key Exchange**: ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)

## Evidence Required

For PCI-DSS audit of Requirement 4:
- [ ] TLS configuration documentation
- [ ] Certificate inventory and tracking
- [ ] Periodic penetration test results
- [ ] Configuration verification reports
- [ ] Certificate management procedures
- [ ] TLS testing documentation

## RFP Response Template

### Question: "How do you protect data in transit?"

```
[Company Name] implements PCI-DSS Requirement 4 through:

1. TLS Encryption
   - TLS 1.2 minimum, TLS 1.3 preferred for all services
   - Perfect Forward Secrecy (PFS) cipher suites only
   - Disabled weak protocols (SSL, TLS 1.0, TLS 1.1)
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

2. Certificate Management
   - Automated certificate provisioning via [ACM/Azure Certificate Manager/GCP Certificate Manager]
   - Auto-renewal 30 days before expiration
   - Regular certificate inventory and monitoring
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.3)

3. Network Security
   - Force HTTPS for all external-facing services
   - Load balancer TLS termination at network edge
   - Internal service-to-service encryption
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.2)

4. Verification and Testing
   - Quarterly TLS configuration verification
   - Continuous SSL/TLS monitoring
   - Annual penetration testing
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.4)

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 3 months]
```

## Common Questions

### Q: Do internal communications need encryption?
A: Yes. PCI-DSS v4.0 requires encryption of cardholder data in transit over all networks, including internal networks.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.1)

### Q: Can we use self-signed certificates?
A: Generally no for external-facing services. Use certificates from trusted public CAs. Internal services may use a private CA with proper governance.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 4.3)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-4/`
- [ ] TLS configuration documents
- [ ] Certificate inventory
- [ ] Penetration test results
- [ ] SSL/TLS scan reports

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-1]] — Network security controls
- [[pci-dss-req-3]] — Stored data protection
- [[infrastructure-aws]] — AWS TLS implementation
