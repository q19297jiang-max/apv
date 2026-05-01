---
type: source
category: card-systems
title: Card Authorization Engine
source_url: "https://www.emvco.com/emv-technologies/emv-secure-card-authorization"
source_document: EMVCo Secure Card Authorization
captured_date: 2026-04-24
verified_by: Infrastructure Architect
tags: [card-systems, authorization, processing]
freshness_days: 365
last_verified: 2026-04-24
---

# Card Authorization Engine

## Definition

An authorization engine processes card transactions in real-time, validating card details, checking balances/limits, and approving or declining transactions based on business rules.

## Key Components

### Architecture Pattern
```
Authorization Engine:
├── Transaction Router
│   ├── Message normalization
│   ├── Protocol conversion (ISO8583, JSON)
│   └── Load balancing
├── Validation Engine
│   ├── Card verification
│   ├── PIN/cryptogram validation
│   └── Velocity checks
├── Business Rules Engine
│   ├── Balance/limit checks
│   ├── Fraud scoring
│   ├── Risk assessment
│   └── Authorization logic
├── Account Management
│   ├── Balance inquiry
│   ├── Limit management
│   └── Account lock/unlock
└── Integration
    ├── Card network connectivity
    ├── Issuer/acquirer systems
    └── Switch/processor interfaces
```

## Authorization Flow

**Source**: EMVCo and payment network specifications

```
1. Transaction Request
   ├── Card details (PAN, expiry, CVV)
   ├── Transaction amount
   ├── Merchant details
   └── Security data (PIN, cryptogram)

2. Card Verification
   ├── PAN validation (Luhn check)
   ├── Card status check (active, blocked)
   ├── Expiry validation
   └── CVV/cryptogram verification

3. Account Validation
   ├── Balance check (debit/prepaid)
   ├── Limit check (credit)
   ├── Velocity check (transaction count)
   └── Fraud scoring

4. Authorization Decision
   ├── Approve (within limits, low risk)
   ├── Decline (insufficient funds, high risk)
   └── Refer (requires additional verification)

5. Response
   ├── Authorization code (if approved)
   ├── Response code
   └── Balance (if requested)
```

## Infrastructure Requirements

### Compute
**Source**: Payment network requirements

| Component | Requirement | Scaling |
|-----------|-------------|---------|
| Authorization Engine | Sub-millisecond latency | In-memory processing |
| Fraud Engine | Real-time scoring | Machine learning |
| Database | Primary/standby | Multi-AZ |

### Storage
**Source**: PCI-DSS compliance

| Data Type | Storage Requirement |
|-----------|---------------------|
| Account balances | In-memory + persistent |
| Transaction logs | Encrypted, 7 years |
| Authorization records | Encrypted, 7 years |

### Network
**Source**: Payment network specifications

| Requirement | Specification |
|-------------|----------------|
| Authorization latency | <100ms (domestic) |
| Network connectivity | Multiple providers |
| Uptime | 99.9% availability |

## Authorization Logic

### Credit Cards
**Source**: Industry standards

- Credit limit check
- Available balance calculation
- Velocity checks (transaction count, amount)
- Fraud scoring

### Debit Cards
**Source**: Industry standards

- Account balance check
- Daily limit enforcement
- PIN verification
- Real-time availability

### Prepaid Cards
**Source**: Industry standards

- Available balance check
- No negative balance
- Load/reload limits
- Expiry validation

## RFP Response Template

```
[Company Name] authorization engine includes:

1. Performance
   - Sub-millisecond authorization logic
   - <100ms end-to-end latency
   - 10,000+ TPS capacity
   Source: EMVCo and network specifications

2. Features
   - Real-time fraud scoring
   - Velocity checks
   - Business rules engine
   - Multi-currency support
   Source: Industry best practices

3. Integration
   - ISO8583 support
   - REST APIs
   - Direct network connectivity
   - Processor/switch integration
   Source: Developer documentation

4. Availability
   - 99.9% uptime SLA
   - Multi-region deployment
   - Disaster recovery
   Source: Service level agreements

Supported card types: Credit, Debit, Prepaid
Latency: <100ms p95
Throughput: 10,000 TPS
```

## Related
- [[card-systems-issuing]] — Issuing platform
- [[card-systems-acquiring]] — Acquiring platform
