---
type: source
category: card-systems
title: 3-D Secure Authentication
source_url: "https://www.emvco.com/emv-technologies/3ds"
source_document: EMVCo 3-D Secure Protocol
source_version: 2.3
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [card-systems, 3ds, authentication, fraud-prevention]
freshness_days: 365
last_verified: 2026-04-24
---

# 3-D Secure Authentication (3DS)

## Definition

3-D Secure (3DS) is an XML-based protocol designed to be an additional security layer for online credit and debit card transactions. It adds authentication step between purchase and authorization.

## Key Concepts

### 3DS2.0/2.3
**Source**: https://www.emvco.com/emv-technologies/3ds

- Frictionless flow (no SCA for low-risk)
- Challenge flow (SCA for high-risk)
- Risk-based authentication (RBA)
- Biometric support
- Mobile app support

### Authentication Flows
**Source**: EMVCo 3DS Protocol

```
3DS Flow:
├── Frictionless (No Challenge)
│   ├── Risk assessment
│   ├── Authentication behind the scenes
│   └── No customer interaction
├── Challenge-Required
│   ├── Risk assessment
│   ├── Customer authentication
│   ├── OTP, biometric, or other
│   └── Transaction completion
└── Decoupled
    ├── Authentication via separate device
    ├── Async authentication flow
    └── Mobile app notification
```

## Components

### Directory Server (DS)
**Source**: EMVCo 3DS Protocol

- Maps card ranges to ACS
- Route 3DS messages
- Managed by payment networks

### Access Control Server (ACS)
**Source**: EMVCo 3DS Protocol

- Authenticates cardholder
- Issues challenges
- Managed by issuers

### 3DS Server
**Source**: EMVCo 3DS Protocol

- Merchant/acquirer side
- Initiates authentication
- Receives authentication results

## Infrastructure Requirements

### Compute
**Source**: EMVCo specifications

| Component | Requirement | Scaling |
|-----------|-------------|---------|
| 3DS Server | High availability | Auto-scaling |
| ACS | High availability | Multi-AZ |
| DS | Global distribution | Edge |

### Network
**Source**: EMVCo specifications

| Requirement | Specification |
|-------------|----------------|
| 3DS latency | <200ms frictionless |
| Challenge timeout | 10 seconds |
| Network redundancy | Multiple providers |

### Security
**Source**: PCI-DSS and EMVCo

- PCI-DSS compliance
- TLS 1.3 for all communications
- Message authentication
- ACS-to-DS encryption

## Benefits

### Fraud Reduction
**Source**: Industry studies

- Up to 60% reduction in CNP fraud
- Chargeback liability shift
- Reduced false declines

### Customer Experience
**Source**: Industry studies

- Frictionless flow = no friction
- Biometric authentication = familiar
- Mobile-first design

## RFP Response Template

```
[Company Name] 3DS solution includes:

1. 3DS2.3 Support
   - Full EMVCo 3DS2.3 implementation
   - Frictionless flow optimization
   - Challenge flow support
   Source: https://www.emvco.com/emv-technologies/3ds

2. Features
   - Risk-based authentication
   - Biometric support (Face ID, Touch ID)
   - Mobile app support
   - Decoupled authentication
   Source: EMVCo 3DS Protocol

3. Integration
   - REST API for 3DS server
   - SDK for mobile apps
   - Web components
   - Plugin support
   Source: Developer documentation

4. Performance
   - 3DS latency: <150ms frictionless
   - Authentication success rate: >95%
   - Availability: 99.9%
   Source: Performance benchmarks

Supported flows: Frictionless, Challenge, Decoupled
Liability shift: Yes (when authenticated)
```

## Related
- [[card-systems-gateway]] — Payment gateway
- [[card-systems-digital-wallet]] — Digital wallet
