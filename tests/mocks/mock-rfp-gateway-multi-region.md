---
type: apv-test
category: mock-rfp
title: "Mock RFP - Payment Gateway Multi-Region"
version: "1.0"
created: 2026-04-24
tags: [apv, test, mock-rfp]
---

# Mock RFP: Multi-Region Payment Gateway

## Issuer Information

**Company**: PayTech Asia
**Type**: Payment Service Provider
**Regions**: Singapore, Malaysia, Thailand
**License**: PSP license in all three countries

## Executive Summary

PayTech Asia is seeking a multi-region payment gateway solution to support:
- Online payment processing for merchants
- Multiple payment methods (cards, wallets, FPX)
- Cross-border transactions
- Local payment methods in each country

## Business Requirements

### 1. Transaction Volume
- **Total Daily**: 2 million transactions
- **Peak TPS**: 10,000 TPS
- **Growth**: 30% year-over-year

### 2. Regional Distribution
| Country | % of Volume | Daily Transactions |
|---------|-------------|-------------------|
| Singapore | 40% | 800,000 |
| Malaysia | 35% | 700,000 |
| Thailand | 25% | 500,000 |

### 3. Payment Methods
- **Cards**: Visa, Mastercard, Amex
- **Wallets**: GrabPay, Touch 'n Go, TrueMoney
- **Bank Transfer**: FAST (SG), FPX (MY), PromptPay (TH)

## Technical Requirements

### 1. Architecture
- **Multi-region**: Deploy in all three countries
- **Cloud Provider**: Best-fit for each region
- **Data Residency**: Transaction data must remain in country of origin
- **Cross-border**: Settlement system for cross-border transactions

### 2. Compliance by Country
- **Singapore**: MAS, PSA, PDPA, CSA
- **Malaysia**: BNM, PSA (MY), PDPA (MY)
- **Thailand**: BOT, PDPA (TH), Financial Act

### 3. Performance
- **Response Time**: < 50ms for authorization (P95)
- **Availability**: 99.99% uptime
- **Disaster Recovery**: Active-active across regions

## Pricing Requirements

Provide comparison of:
- AWS pricing for all three regions
- Azure pricing for all three regions
- Best-fit recommendation

## Questions

1. How do you handle different regulations across three countries?
2. What is your approach to cross-border settlements?
3. How do you ensure data residency compliance?
