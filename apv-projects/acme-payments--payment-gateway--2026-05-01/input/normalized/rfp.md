
# Request For Proposal

Payment Gateway Infrastructure
**Client:** ACME Payments Pte Ltd
**Date:** 2026-04-15
**Reference:** RFP-2026-0042


## 1. Background

ACME Payments is a licensed Major Payment Institution (MPI) in Singapore
seeking to deploy a cloud-based payment gateway supporting Visa, Mastercard,
and local payment methods (PayNow, GrabPay, ShopeePay) across Southeast Asia.

**Initial launch markets:** Singapore, Malaysia, Philippines.
Expansion markets (Phase 2): Indonesia, Thailand.


## 2. Business Requirements

- Card issuing and acquiring capabilities
- Gateway processing for online and in-store payments
- Tokenization service for recurring payments
- 3D Secure 2.0 authentication
- Digital wallet integration (Apple Pay, Google Pay, GrabPay)
- Real-time settlement and reconciliation


## 3. Technical Requirements

- Cloud-native deployment on AWS (primary) with DR capability
- PCI-DSS v4.0 Level 1 compliance
- 99.99% availability SLA
- Multi-AZ deployment in AWS Singapore (ap-southeast-1)
- API-first architecture with REST and gRPC endpoints
- End-to-end encryption (TLS 1.3, AES-256)
- Comprehensive audit logging per MAS TRM guidelines


## 4. Volume Data

- Monthly transactions: 50,000,000 (Year 1)
- Average transaction value: SGD 85
- Peak multiplier: 3x during festive periods (CNY, Hari Raya, Christmas)
- Expected growth: 40% YoY
- Target peak TPS: 500


## 5. Compliance Requirements

- PCI-DSS v4.0 Level 1 (mandatory)
- Singapore MAS Technology Risk Management Guidelines
- Singapore Personal Data Protection Act (PDPA)
- Singapore Payment Services Act (PSA)
- Malaysia Bank Negara Malaysia Risk Management in Technology (BNM RMiT)
- Malaysia Personal Data Protection Act (PDPA)
- Philippines BSP Circular on Electronic Payments
- Data residency: transaction data must remain in-country where required


## 6. Evaluation Criteria

- Technical architecture and scalability: 30%
- Compliance and security posture: 25%
- Pricing and total cost of ownership: 25%
- Implementation timeline and approach: 10%
- Team experience and references: 10%


## 7. Timeline

- RFP response due: 2026-05-15
- Vendor selection: 2026-06-01
- Implementation start: 2026-07-01
- Go-live target: 2026-12-01
