---
type: source
category: card-systems
title: Card Issuing Platform
source_url: "https://www.emvco.com/emv-technologies/payment-tokenization"
source_document: EMVCo Specifications
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [card-systems, issuing, cards]
freshness_days: 365
last_verified: 2026-04-24
---

# Card Issuing Platform

## Definition

A card issuing platform is a banking system that enables financial institutions to issue payment cards (credit, debit, prepaid) to customers and manage the card lifecycle.

## Key Components

### Architecture Pattern
```
Source: EMVCo specifications and industry standards

Issuing Platform:
├── Card Management System (CMS)
│   ├── Application processing
│   ├── Cardholder management
│   └── Account management
├── Embossing/Personalization
│   ├── Card generation
│   ├── PIN generation
│   └── Secure delivery
├── Authorization Engine
│   ├── Real-time authorization
│   ├── Balance checking
│   └── Fraud scoring
├── Clearing and Settlement
│   ├── Transaction posting
│   ├── Fee calculation
│   └── Reconciliation
└── Customer Service
    ├── Card activation
    ├── PIN reset
    └── Dispute handling
```

## Infrastructure Requirements

### Compute
**Source**: https://www.emvco.com/emv-technologies/payment-tokenization

| Component | Requirement | Source URL |
|-----------|-------------|------------|
| Application Server | High availability, auto-scaling | AWS/Azure/GCP docs |
| Database | Primary/standby, synchronous replication | Database service docs |
| Authorization Engine | Sub-millisecond response time | EMVCo specs |

### Storage
**Source**: Industry best practices for PCI-DSS compliance

| Data Type | Storage Requirement | Retention |
|-----------|---------------------|-----------|
| PAN | Encrypted or tokenized | Per retention policy |
| Cardholder data | Encrypted at rest | Active + 5 years |
| Transaction data | Encrypted | 7 years (typical) |
| Audit logs | Immutable append-only | 1 year minimum |

### Network
**Source**: EMVCo and network requirements

| Requirement | Specification |
|-------------|----------------|
| Authorization latency | <200ms (domestic), <500ms (cross-border) |
| Availability | 99.9% uptime |
| Bandwidth | 1 Gbps minimum for authorization |

### Security
**Source**: PCI-DSS requirements

- PCI-DSS compliance required
- HSM for cryptographic operations
- Key management procedures
- Fraud detection and prevention

## Card Types

### Credit Cards
**Source**: Industry standards

- Revolving credit
- Interest calculation
- Payment processing
- Rewards programs

### Debit Cards
**Source**: Industry standards

- Direct account access
- Real-time balance check
- PIN verification
- Daily transaction limits

### Prepaid Cards
**Source**: Industry standards

- Stored value
- Reload capabilities
- No credit check
- Mobility/travel cards

## RFP Response Template

```
[Company Name] issuing platform includes:

1. Card Management
   - Comprehensive card lifecycle management
   - Real-time authorization engine (<100ms)
   - Fraud detection and prevention
   Source: https://www.emvco.com/emv-technologies/payment-tokenization

2. Technology
   - PCI-DSS v4.0 certified
   - Cloud-native architecture
   - Auto-scaling for peak volumes
   - Multi-region deployment
   Source: EMVCo and PCI-DSS specifications

3. Features
   - Instant card issuance
   - Mobile card provisioning
   - Contactless payment support
   - Rewards program integration
   Source: Industry best practices

TPS Rating: 1,000 TPS per instance
Availability: 99.9% uptime SLA
```

## Related
- [[card-systems-acquiring]] — Acquiring platform
- [[card-systems-gateway]] — Payment gateway
- [[card-systems-tokenization]] — Tokenization
