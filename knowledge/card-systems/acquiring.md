---
type: source
category: card-systems
title: Card Acquiring Platform
source_url: "https://www.emvco.com/emv-technologies/emv-secure-card-authorization"
source_document: EMVCo Secure Card Authorization
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [card-systems, acquiring, merchants]
freshness_days: 365
last_verified: 2026-04-24
---

# Card Acquiring Platform

## Definition

A card acquiring platform enables merchants to accept card payments by connecting them to payment networks and card issuers for authorization and settlement.

## Key Components

### Architecture Pattern
```
Acquiring Platform:
├── Merchant Onboarding
│   ├── KYC verification
│   ├── Risk assessment
│   └── Contract management
├── Payment Processing
│   ├── Point of Sale (POS) integration
│   ├── E-commerce gateway
│   └── Mobile payment acceptance
├── Authorization Router
│   ├── Network connectivity (Visa, Mastercard, etc.)
│   ├── Routing logic
│   └── Failover management
├── Clearing and Settlement
│   ├── Batch processing
│   ├── Fee calculation (MDR)
│   └── Merchant funding
└── Risk Management
    ├── Fraud detection
    ├── Chargeback handling
    └── Monitoring
```

## Infrastructure Requirements

### Compute
**Source**: Payment network requirements

| Component | Requirement | Source URL |
|-----------|-------------|------------|
| Payment Gateway | High availability, auto-scaling | Cloud provider docs |
| Settlement Engine | Batch processing capacity | Cloud provider docs |
| Risk Engine | Real-time scoring | EMVCo specs |

### Storage
**Source**: PCI-DSS compliance

| Data Type | Storage Requirement |
|-----------|---------------------|
| Merchant data | Encrypted at rest |
| Transaction data | Encrypted, 7 years retention |
| Settlement data | Immutable append-only |
| Audit logs | Immutable, 1 year minimum |

### Network
**Source**: Payment network specifications

| Requirement | Specification |
|-------------|----------------|
| Authorization latency | <200ms (domestic) |
| Settlement window | Same day / next day |
| Network redundancy | Multiple network providers |

## Acquiring Models

### Merchant Acquiring
**Source**: Industry standards

- POS terminals
- E-commerce gateways
- Mobile payment acceptance
- Recurring payments

### ISO/MSP Model
**Source**: Industry standards

- Independent Sales Organizations
- Merchant Service Providers
- White-label solutions

## RFP Response Template

```
[Company Name] acquiring platform includes:

1. Merchant Services
   - Fast onboarding (KYC in 24 hours)
   - Multi-channel acceptance (POS, e-com, mobile)
   - Competitive MDR rates
   Source: Industry best practices

2. Technology
   - PCI-DSS v4.0 certified
   - 99.9% uptime guarantee
   - Real-time authorization (<100ms)
   - Next-day settlement
   Source: EMVCo and PCI-DSS specifications

3. Features
   - Virtual terminal
   - Recurring billing
   - Chargeback management
   - Real-time reporting
   Source: EMVCo specifications

TPS Rating: 5,000 TPS per instance
Availability: 99.9% uptime SLA
```

## Related
- [[card-systems-issuing]] — Issuing platform
- [[card-systems-gateway]] — Payment gateway
