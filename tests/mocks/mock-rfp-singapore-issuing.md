---
type: apv-test
category: mock-rfp
title: "Mock RFP - Digital Issuing Platform for Singapore Bank"
version: "1.0"
created: 2026-04-24
tags: [apv, test, mock-rfp]
---

# Mock RFP: Digital Issuing Platform

## Issuer Information

**Bank**: Acme Bank Singapore
**Type**: Commercial Bank
**Region**: Singapore
**License**: Singapore banking license holder

## Executive Summary

Acme Bank is seeking proposals for a cloud-native digital card issuing platform to support:
- Virtual card issuance for corporate clients
- Physical card issuance for retail customers
- Integration with existing core banking system
- PCI-DSS v4.0 compliance
- Singapore regulatory compliance (MAS, PDPA)

## Business Requirements

### 1. Card Types
- **Virtual Cards**: Corporate expense cards, instant issuance
- **Physical Cards**: Debit cards for retail customers
- **Card Networks**: Visa and Mastercard only

### 2. Transaction Volume
- **Daily Transactions**: 500,000 (peak), 100,000 (average)
- **Peak Period**: 9:00 AM - 1:00 PM SGT (4 hours)
- **Growth**: 20% year-over-year

### 3. Target Customers
- **Corporate**: 500 companies, 50,000 employees
- **Retail**: 100,000 customers in Year 1

## Technical Requirements

### 1. Architecture
- **Cloud Provider**: AWS preferred (Singapore region: ap-southeast-1)
- **Deployment**: Multi-AZ for high availability
- **Disaster Recovery**: Hot standby in secondary region
- **Availability**: 99.99% uptime SLA

### 2. Integration Points
- **Core Banking**: ISO 8583 host-to-host interface
- **Payment Network**: Visa Direct and Mastercard MDES
- **Tokenization**: Network tokenization support required
- **3DS**: 3DS 2.3 authentication for card-not-present

### 3. Security Requirements
- **Encryption at Rest**: AES-256 for all cardholder data
- **Encryption in Transit**: TLS 1.3 minimum
- **Key Management**: HSM-based key management
- **Access Control**: MFA for all administrative access
- **Audit Logging**: All access and changes logged

## Compliance Requirements

### 1. PCI-DSS
- **Version**: PCI-DSS v4.0
- **Validation**: ROC required annually
- **Scope**: Full cardholder data environment

### 2. Singapore Regulations
- **MAS TRM**: Compliance with MAS Technology Risk Management guidelines
- **PSA**: Payment Services Act compliance
- **PDPA**: Personal Data Protection Act compliance
- **CSA**: Cybersecurity Act compliance

### 3. Data Requirements
- **Data Residency**: All Singapore customer data must remain in Singapore
- **Data Retention**: 7 years for transaction records
- **Privacy**: Consent management for PDPA compliance

## Non-Functional Requirements

### 1. Performance
- **Authorization TPS**: 5,000 TPS peak
- **Response Time**: < 100ms for authorization (P95)
- **Batch Processing**: 1 million transactions in < 2 hours

### 2. Scalability
- **Auto-scaling**: Automatically scale based on load
- **Burst Capacity**: Support 2x peak load for 2 hours

### 3. Monitoring
- **Metrics**: Real-time monitoring of all components
- **Alerting**: Automated alerting for failures
- **Dashboards**: Executive dashboards for KPIs

## Implementation Requirements

### 1. Timeline
- **Project Start**: Within 30 days of contract award
- **Phase 1**: Core platform (3 months)
- **Phase 2**: Integration (2 months)
- **Phase 3**: Go-live (1 month)
- **Total**: 6 months

### 2. Deliverables
- Architecture documentation
- Implementation guide
- Operations manual
- Training materials
- PCI-DSS ROC support

### 3. Support
- **Warranty**: 12-month warranty post-go-live
- **SLA**: 99.99% uptime with penalties
- **Support**: 24/7 support with 1-hour response time

## Pricing Requirements

### 1. Pricing Model
Provide pricing for:
- Setup/implementation (one-time)
- Monthly subscription (per 1,000 cards)
- Transaction fees (per transaction)
- Volume discounts (for tiers)

### 2. Comparison
Compare costs for:
- AWS Singapore region
- Alternative cloud providers (if applicable)

## Evaluation Criteria

Proposals will be evaluated on:
1. **Technical Solution** (30%)
2. **Compliance** (25%)
3. **Pricing** (20%)
4. **Implementation Timeline** (15%)
5. **Vendor Experience** (10%)

## Submission Requirements

### 1. Proposal Format
- PDF format
- Maximum 50 pages
- Executive summary (2 pages max)

### 2. Required Sections
1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Technical Architecture
5. Compliance Response
6. Implementation Plan
7. Pricing
8. Assumptions and Qualifications
9. Appendices

### 3. Source Citations
All claims must cite:
- Official documentation sources with URLs
- Regulatory sources with URLs
- Pricing sources with calculator URLs

## Questions

Please address:
1. How does your solution ensure data residency in Singapore?
2. What is your approach to PCI-DSS certification?
3. How do you handle peak loads beyond 5,000 TPS?
4. What is your experience with Singapore banking regulations?
5. Can you provide references for similar implementations?

## Appendix A: Assumptions

- Bank has existing core banking system with ISO 8583 interface
- Bank will provide Visa and Mastercard sponsorship
- Network connectivity to core banking system is available
- Bank has AWS account with proper billing setup

## Appendix B: Glossary

- **TPS**: Transactions Per Second
- **HSM**: Hardware Security Module
- **ROC**: Report on Compliance (PCI-DSS)
- **PSA**: Payment Services Act (Singapore)
- **MAS**: Monetary Authority of Singapore
- **PDPA**: Personal Data Protection Act (Singapore)
