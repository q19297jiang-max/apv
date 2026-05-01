---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 11
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, security-testing, penetration-testing, vulnerability-scanning, requirement-11]
---

# PCI-DSS Requirement 11: Security Testing

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Test security of systems and networks regularly by:
> - Performing vulnerability scanning
> - Conducting penetration testing
> - Implementing intrusion detection
> - Testing intrusion prevention systems
> - Performing internal and external penetration testing"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 11)

## Implementation Requirements

### 11.1 Vulnerability Scanning
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.1)

- Run external vulnerability scans at least quarterly
- Run internal vulnerability scans at least quarterly
- After any significant change
- Use PA-QSA approved scanning vendor

### 11.2 Penetration Testing
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.2)

- Conduct external penetration testing at least annually
- Conduct internal penetration testing at least annually
- After any significant change
- Test from both inside and outside the network
- Cover entire cardholder data environment
- Use qualified penetration tester

### 11.3 Intrusion Detection
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.3)

- Implement intrusion detection systems
- Monitor system components
- Alert personnel to suspected compromises
- Maintain detection systems

### 11.4 Intrusion Prevention
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.4)

- Implement intrusion prevention systems
- Automatically block malicious activity
- Maintain prevention systems

### 11.5 Methodology Testing
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.5)

- Test methodology and penetration testing procedures
- Ensure methodology detects vulnerabilities
- Update methodology based on testing results

## Testing Types and Frequencies

| Test Type | Frequency | Provider | Coverage |
|-----------|-----------|----------|----------|
| External Vulnerability Scan | Quarterly | ASV | External-facing systems |
| Internal Vulnerability Scan | Quarterly | Internal or external | All systems |
| External Penetration Test | Annual | QSA or qualified tester | External attack surface |
| Internal Penetration Test | Annual | QSA or qualified tester | Internal network and systems |
| Network Segmentation Test | Annual | QSA or qualified tester | Network controls |
| Application Security Test | Annual | Qualified tester | Web applications |

## Implementation in Cloud Infrastructure

### AWS Security Testing
**Source**: https://docs.aws.amazon.com/inspector/latest/userguide/

```
Components:
├── Amazon Inspector - Automated vulnerability scanning
├── AWS WAF - Web application firewall with testing
├── Amazon GuardDuty - Threat detection
├── AWS Security Hub - Centralized security findings
├── AWS Trusted Advisor - Security best practices
└── Third-party tools - Qualys, Tenable, Rapid7
```

### Azure Security Testing
**Source**: https://learn.microsoft.com/en-us/azure/defender-for-cloud/

```
Components:
├── Microsoft Defender for Cloud - Vulnerability assessment
├── Azure Web Application Firewall - WAF with testing
├── Microsoft Defender for Endpoint - Threat protection
├── Azure Security Center - Centralized security
└── Third-party tools - Qualys, Tenable, Rapid7
```

### GCP Security Testing
**Source**: https://cloud.google.com/security-command-center

```
Components:
├── Security Command Center - Vulnerability scanning
├── Web Security Scanner - DAST for web apps
├── Cloud Armor - WAF with security policies
├── Security Health Analytics - Best practice checks
└── Third-party tools - Qualys, Tenable, Rapid7
```

## Penetration Testing Process

**Source**: Industry best practices for PCI-DSS compliance

```
Penetration Testing Lifecycle:

1. Scoping
   - Define cardholder data environment scope
   - Identify all systems and networks
   - Document testing rules of engagement

2. Reconnaissance
   - Gather information about target systems
   - Identify potential attack vectors
   - Map network topology

3. Vulnerability Identification
   - Scan for known vulnerabilities
   - Identify misconfigurations
   - Analyze application security

4. Exploitation
   - Attempt to exploit vulnerabilities
   - Test security controls
   - Verify actual risk vs theoretical

5. Post-Exploitation
   - Test lateral movement
   - Attempt privilege escalation
   - Test data exfiltration

6. Reporting
   - Document all findings
   - Assign risk levels
   - Provide remediation recommendations

7. Remediation
   - Fix identified vulnerabilities
   - Re-test to verify fixes
   - Document remediation
```

## Evidence Required

For PCI-DSS audit of Requirement 11:
- [ ] Vulnerability scan reports (quarterly)
- [ ] Penetration test reports (annual)
- [ ] Remediation plans and status
- [ ] Intrusion detection/prevention configuration
- [ ] Testing methodology documentation
- [ ] Qualified tester credentials (ASV, QSA)

## RFP Response Template

### Question: "How do you test security?"

```
[Company Name] implements PCI-DSS Requirement 11 through:

1. Vulnerability Scanning
   - External scans: Quarterly by ASV (Approved Scanning Vendor)
   - Internal scans: Quarterly by internal security team
   - Automated scanning via [Amazon Inspector/Azure Defender/GCP SCC]
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.1)

2. Penetration Testing
   - External pen test: Annual by [QSA/qualified tester]
   - Internal pen test: Annual by [QSA/qualified tester]
   - Network segmentation verification: Annual
   - Application security testing: Annual
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.2)

3. Intrusion Detection and Prevention
   - [GuardDuty/Azure Defender/GCP SCC] for threat detection
   - Automatic blocking of malicious activity
   - 24/7 SOC monitoring and response
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.3, 11.4)

4. Continuous Security Monitoring
   - Real-time vulnerability detection
   - Automated security posture assessment
   - Regular compliance verification
   Source: [Cloud provider documentation]

Compliance verified by: [Compliance Officer] on [DATE]
Next penetration test: [DATE]
```

## Common Questions

### Q: What's the difference between vulnerability scanning and penetration testing?
A: Vulnerability scanning identifies known vulnerabilities automatically. Penetration testing involves human testers attempting to exploit vulnerabilities to assess actual risk.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.1, 11.2)

### Q: Can internal staff conduct penetration testing?
A: For PCI-DSS, penetration testing must be conducted by a qualified internal resource or third-party organization independent of the tested systems.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 11.2)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-11/`
- [ ] Vulnerability scan reports (quarterly)
- [ ] Penetration test reports (annual)
- [ ] Remediation plans and status
- [ ] ASV attestation reports
- [ ] QSA credentials

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-10]] — Logging and monitoring
- [[pci-dss-req-6]] — Secure development
