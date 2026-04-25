---
type: apv-knowledge
category: card-systems
title: "Payment Gateway"
source_url: "https://www.emvco.com/emv-technologies/3ds"
source_document: "EMVCo 3-D Secure Specifications"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [card-systems, gateway, payments]
---

# Payment Gateway

## Definition

A payment gateway is an e-commerce service that processes credit card payments for online businesses, acting as an intermediary between merchants and payment networks.

## Key Components

### Architecture Pattern
```
Payment Gateway:
├── API Layer
│   ├── REST APIs
│   ├── SDKs (mobile, web)
│   └── Webhooks
├── Payment Processing
│   ├── Card tokenization
│   ├── 3DS authentication
│   ├── Authorization routing
│   └── Settlement processing
├── Security
│   ├── PCI-DSS compliance
│   ├── Fraud prevention
│   ├── Encryption (TLS, AES)
│   └── Tokenization
└── Integration
    ├── Shopping cart plugins
    ├── Mobile SDKs
    └── Hosted payment pages
```

## Infrastructure Requirements

### Compute
**Source**: Cloud provider best practices

| Component | Requirement | Scaling |
|-----------|-------------|---------|
| API Gateway | Auto-scaling | Burst to 10x |
| 3DS Server | High availability | Multi-AZ |
| Settlement Engine | Batch processing | Scheduled scaling |

### Storage
**Source**: PCI-DSS compliance

| Data Type | Storage Requirement |
|-----------|---------------------|
| Tokenized PAN | Encrypted or HSM-protected |
| Transaction logs | Immutable, 7 years |
| 3DS data | Encrypted, per PCI-DSS |
| Merchant configs | Encrypted at rest |

### Network
**Source**: Payment network requirements

| Requirement | Specification |
|-------------|----------------|
| API response time | <200ms p95 |
| 3DS timeout | 10 seconds |
| Uptime | 99.9% availability |

## Security Features

### PCI-DSS Compliance
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf

- SAQ A-EP or SAQ D depending on implementation
- Tokenization reduces scope
- 3DS2.0 for strong authentication

### Fraud Prevention
**Source**: Industry best practices

- Device fingerprinting
- Velocity checks
- Behavioral analysis
- Machine learning fraud scoring

## Integration Patterns

### Hosted Payment Page
**Source**: Industry standard

- Simplest PCI compliance (SAQ A)
- Redirect to gateway, back to merchant
- Limited customization

### Direct API Integration
**Source**: Industry standard

- More control over UX
- Higher PCI burden (SAQ A-EP or D)
- Tokenization recommended

### SDK Integration
**Source**: Industry standard

- Mobile apps
- Native experience
- Tokenization built-in

## RFP Response Template

```
[Company Name] payment gateway includes:

1. Features
   - REST API with comprehensive SDKs
   - 3DS2.0 support
   - Tokenization for card-on-file
   - Recurring payments
   Source: https://www.emvco.com/emv-technologies/3ds

2. Security
   - PCI-DSS v4.0 certified (SAQ A-EP)
   - PCI-validated tokenization
   - Fraud prevention included
   - 24/7 security monitoring
   Source: PCI-DSS v4.0

3. Performance
   - API response: <200ms p95
   - Availability: 99.9%
   - Auto-scaling for peak loads
   Source: Cloud provider SLAs

4. Integrations
   - Shopify, WooCommerce, Magento
   - iOS and Android SDKs
   - React, Angular libraries
   Source: Developer documentation

Supported TPS: 10,000 TPS
Settlement: T+1 (next day)
```

## Related
- [[card-systems-issuing]] — Issuing platform
- [[card-systems-acquiring]] — Acquiring platform
- [[card-systems-3ds]] — 3DS authentication
