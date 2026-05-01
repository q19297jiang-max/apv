---
type: source
category: compliance
subcategory: pci-dss
title: PCI-DSS Requirement 6
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: PCI-DSS-v4_0.pdf
source_version: 4.0
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, secure-development, requirement-6]
---

# PCI-DSS Requirement 6: Secure Systems and Software

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Develop and maintain secure systems and software by:
> - Establishing secure development processes
> - Integrating security into development lifecycle
> - Training developers in secure coding
> - Performing vulnerability testing
> - Protecting web applications
> - Following change control procedures"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 6)

## Implementation Requirements

### 6.1 Secure Development Processes
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.1)

- Establish secure development and coding processes
- Integrate security into development lifecycle
- Train developers in secure coding practices

### 6.2 Vulnerability Testing
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.2)

- Perform dynamic and static vulnerability testing
- Address vulnerabilities before deployment
- Perform penetration testing

### 6.3 Web Application Protection
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.3)

- Protect web applications against common attacks
- Use web application firewalls
- Follow OWASP guidelines

### 6.4 Change Control
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.4)

- Implement change control procedures
- Test all changes before deployment
- Maintain documentation for all changes

## Secure Development Practices

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.1)

### SDLC Integration
```
1. Requirements Phase
   - Define security requirements
   - Threat modeling
   - Data classification

2. Design Phase
   - Secure architecture review
   - Attack surface analysis
   - Security controls specification

3. Implementation Phase
   - Secure coding standards
   - Code review procedures
   - Static analysis (SAST)

4. Testing Phase
   - Dynamic analysis (DAST)
   - Penetration testing
   - Vulnerability scanning

5. Deployment Phase
   - Security configuration verification
   - Pre-production testing
   - Rollback procedures

6. Maintenance Phase
   - Security patching
   - Ongoing monitoring
   - Incident response
```

### OWASP Top 10 Protection
**Source**: https://owasp.org/www-project-top-ten/

| Risk | Protection |
|------|------------|
| A01 Broken Access Control | Authorization checks, least privilege |
| A02 Cryptographic Failures | Strong encryption, key management |
| A03 Injection | Input validation, parameterized queries |
| A04 Insecure Design | Threat modeling, secure patterns |
| A05 Security Misconfiguration | Hardening, automated verification |
| A06 Vulnerable Components | SBOM, dependency scanning |
| A07 Auth Failures | MFA, secure session management |
| A08 Data Integrity Failures | Digital signatures, code signing |
| A09 Logging Failures | Audit trails, log protection |
| A10 SSRF | Network segmentation, validation |

## Implementation in Cloud Infrastructure

### AWS Secure Development
**Source**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/security.html

```
Components:
├── AWS CodeBuild - SAST/DAST integration
├── AWS CodePipeline - CI/CD with security checks
├── AWS WAF - Web application firewall
├── AWS Shield - DDoS protection
├── AWS X-Ray - Application security monitoring
└── AWS Security Hub - Centralized findings
```

### Azure Secure Development
**Source**: https://learn.microsoft.com/en-us/azure/devops/pipelines/security

```
Components:
├── Azure DevOps - Secure CI/CD
├── Microsoft Defender for DevOps - Security integration
├── Application Gateway WAF - Web application firewall
├── Azure Front Door WAF - Global WAF
└── Azure Monitor - Application security monitoring
```

### GCP Secure Development
**Source**: https://cloud.google.com/security/products/application-security

```
Components:
├── Cloud Build - Secure CI/CD
├── Cloud Armor - Web application firewall
├── Web Security Scanner - DAST integration
├── Binary Authorization - Supply chain security
└── Application Security - Runtime protection
```

## Evidence Required

For PCI-DSS audit of Requirement 6:
- [ ] Secure development lifecycle documentation
- [ ] Developer training records
- [ ] Code review procedures
- [ ] SAST/DAST results
- [ ] Penetration test results
- [ ] Change control documentation
- [ ] WAF configuration and rules

## RFP Response Template

### Question: "How do you ensure secure software development?"

```
[Company Name] implements PCI-DSS Requirement 6 through:

1. Secure Development Lifecycle
   - Security integrated throughout SDLC
   - Developer training on secure coding (annual)
   - OWASP guidelines compliance
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.1)

2. Automated Security Testing
   - Static Application Security Testing (SAST)
   - Dynamic Application Security Testing (DAST)
   - Software Composition Analysis (SCA)
   - Security testing in CI/CD pipeline
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.2)

3. Web Application Protection
   - Web Application Firewall (WAF) deployment
   - OWASP Top 10 protection
   - Regular penetration testing (quarterly)
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.3)

4. Change Management
   - Formal change control procedures
   - Pre-deployment security testing
   - Post-deployment monitoring
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 6.4)

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 6 months]
```

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-5]] — Malware protection
- [[card-systems]] — Card system development
