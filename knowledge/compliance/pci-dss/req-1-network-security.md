---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 1
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, network-security, requirement-1]
---

# PCI-DSS Requirement 1: Network Security Controls

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Install and maintain network security controls to protect cardholder data."
>
> **Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 1)

## Implementation Requirements

### 1.1 Network Security Controls
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.1)

Processes and mechanisms for managing network security controls must include:
- Inventory of system components
- Diagrams showing data flows and connections
- Requirements for network security controls

### 1.2 Secure Firewall Configuration
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.2)

Firewalls and routers must:
- Limit inbound and outbound traffic to only what is necessary
- Restrict connections between untrusted networks and system components in cardholder data environment
- Prevent direct access from untrusted networks to any system component storing cardholder data
- Configure to block all traffic by default and only allow required services

### 1.3 DMZ Configuration
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.3)

- System components storing cardholder data must be isolated from untrusted networks
- DMZ must be implemented to limit inbound traffic to only necessary services

### 1.4 Deny All Traffic
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.4)

- Firewalls must be configured with "deny all" as default
- Only necessary traffic is explicitly allowed

### 1.5 Review Firewall Rules
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.5)

- Review firewall and router rules at least every six months
- Verify rules are documented and business justified

### 1.6 Documentation
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.6)

- Maintain diagram of network connections and data flows
- Document all network security controls

## Implementation in Cloud Infrastructure

### AWS Implementation
**Source**: https://docs.aws.amazon.com/waf/latest/developerguide/web-acl.html

```
Components:
├── VPC (Virtual Private Cloud) - Network isolation
├── Security Groups - Stateful firewall rules
├── Network ACLs - Stateless network controls
├── AWS WAF - Web application firewall
└── AWS Shield - DDoS protection
```

**Security Groups Implementation**:
- Default DENY all inbound traffic
- Allow only necessary ports (HTTPS: 443, custom application ports)
- Restrict sources to known IP ranges
- Separate security groups for each tier

### Azure Implementation
**Source**: https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview

```
Components:
├── VNet (Virtual Network) - Network isolation
├── NSG (Network Security Groups) - Firewall rules
├── Azure Firewall - Centralized network policy
├── Application Gateway WAF - Web application firewall
└── DDoS Protection - DDoS protection
```

### GCP Implementation
**Source**: https://cloud.google.com/firewall/docs/overview

```
Components:
├── VPC Network - Network isolation
├── Firewall Rules - Packet filtering
├── Cloud Armor - Web application firewall
├── Cloud CDN - DDoS protection
└── Armor Policy - Security policies
```

## Evidence Required

For PCI-DSS audit of Requirement 1:
- [ ] Network diagram showing all components and data flows
- [ ] Firewall/router configuration standards
- [ ] Review process documentation (every 6 months)
- [ ] Firewall rules review documentation
- [ ] DMZ architecture documentation
- [ ] Security group rules documentation

## RFP Response Template

### Question: "How do you implement network security controls?"

```
[Company Name] implements PCI-DSS Requirement 1 through:

1. Network Isolation
   - Separate VPC/VNet for cardholder data environment
   - Multi-tier architecture with security zones
   - DMZ isolation for internet-facing components
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.3)

2. Firewall Configuration
   - Default DENY all inbound traffic
   - Explicit ALLOW only for required services
   - Stateful inspection at security group level
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.2)

3. Ongoing Maintenance
   - Quarterly review of all firewall rules
   - Business justification documentation for all rules
   - Automated change management for security controls
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.5)

4. Cloud Provider Services
   - [AWS/Azure/GCP] native firewall services
   - Web Application Firewall (WAF)
   - DDoS protection
   Source: [Cloud provider documentation]

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 6 months]
```

## Common Questions

### Q: Do cloud security groups count as firewalls?
A: Yes. PCI-DSS v4.0 recognizes cloud security groups as firewall controls. Security groups must follow same requirements (deny all, explicit allow, documented, reviewed).

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.2)

### Q: How often must firewall rules be reviewed?
A: At least every six months. Organizations with high change rates may need more frequent reviews.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 1.5)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-1/`
- [ ] Network diagrams
- [ ] Firewall rule reviews
- [ ] Security group configurations
- [ ] Change management records

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-2]] — Secure configuration requirements
- [[infrastructure-aws]] — AWS network security implementation
- [[infrastructure-azure]] — Azure network security implementation
