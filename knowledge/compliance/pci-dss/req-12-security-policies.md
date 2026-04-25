---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Requirement 12"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, security-policies, training, requirement-12]
---

# PCI-DSS Requirement 12: Information Security Policy

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Support information security with organizational policies and programs by:
> - Establishing security policies
> - Implementing security awareness programs
> - Performing background checks
> - Maintaining an information security policy
> - Enforcing security policies
> - Maintaining a risk assessment program
> - Conducting regular security reviews"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 12)

## Implementation Requirements

### 12.1 Security Policy
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.1)

- Establish, publish, maintain, and disseminate security policy
- Review at least annually
- Update as needed

### 12.2 Risk Assessment
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.2)

- Implement risk assessment process
- Identify critical assets, threats, and vulnerabilities
- Document and review annually

### 12.3 Security Awareness
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.3)

- Educate personnel upon hire
- Update training regularly
- Require security awareness training for all personnel

### 12.4 Background Checks
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.4)

- Perform background checks (as permitted by law)
- Before personnel are hired into positions that handle cardholder data

### 12.5 Policy Enforcement
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.5)

- Enforce security policies
- Disciplinary action for policy violations

### 12.6 Incident Response
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.6)

- Implement incident response plan
- Employee training on incident response
- Test incident response plan regularly

### 12.7 Security Reviews
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.7)

- Perform regular security reviews
- At least annually
- Include leadership review

## Security Policy Components

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.1)

### Required Policy Elements
```
1. Information Security Policy
   - Purpose and scope
   - Security requirements
   - Roles and responsibilities
   - Policy enforcement

2. Acceptable Use Policy
   - System and network usage
   - Email and internet usage
   - Data handling procedures

3. Data Classification Policy
   - Classification levels
   - Handling requirements
   - Access controls

4. Access Control Policy
   - User access management
   - Privileged access
   - Access review procedures

5. Incident Response Policy
   - Incident classification
   - Response procedures
   - Reporting requirements

6. Change Management Policy
   - Change request process
   - Testing requirements
   - Rollback procedures

7. Business Continuity Policy
   - Business impact analysis
   - Recovery procedures
   - Testing requirements

8. Third-Party Risk Management Policy
   - Vendor assessment
   - Contract requirements
   - Ongoing monitoring
```

## Security Awareness Training

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.3)

### Training Topics
```
1. Initial Training (upon hire)
   - PCI-DSS requirements overview
   - Security policies and procedures
   - Roles and responsibilities
   - Data handling procedures

2. Ongoing Training (at least annually)
   - Security awareness updates
   - New threats and vulnerabilities
   - Policy changes
   - Incident reporting

3. Role-Specific Training
   - Developers: Secure coding practices
   - Operations: Secure configuration
   - Support: Social engineering awareness
   - Management: Risk management
```

### Phishing and Social Engineering
- Regular phishing simulations (quarterly)
- Social engineering awareness training
- Reporting procedures for suspected attacks

## Incident Response

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.6)

### Incident Response Process
```
1. Preparation
   - Incident response team defined
   - Contact list maintained
   - Tools and procedures ready

2. Identification
   - Detect incident
   - Classify severity
   - Notify stakeholders

3. Containment
   - Isolate affected systems
   - Prevent spread
   - Preserve evidence

4. Eradication
   - Remove threat
   - Patch vulnerabilities
   - Clean systems

5. Recovery
   - Restore systems
   - Monitor for recurrence
   - Validate recovery

6. Lessons Learned
   - Post-incident review
   - Update procedures
   - Improve processes
```

### Incident Response Team Roles
| Role | Responsibility |
|------|---------------|
| Incident Response Manager | Overall coordination |
| Security Analyst | Investigation and containment |
| Communications | Stakeholder notifications |
| Legal | Regulatory compliance |
| IT Operations | System recovery |
| Management | Executive communication |

## Evidence Required

For PCI-DSS audit of Requirement 12:
- [ ] Information security policy
- [ ] Security awareness training materials
- [ ] Training records for all personnel
- [ ] Risk assessment documentation
- [ ] Incident response plan
- [ ] Incident response test results
- [ ] Background check procedures
- [ ] Security review meeting minutes

## RFP Response Template

### Question: "What security policies do you have in place?"

```
[Company Name] implements PCI-DSS Requirement 12 through:

1. Information Security Policy
   - Comprehensive security policy covering all PCI-DSS requirements
   - Annual policy review and updates
   - Policy dissemination to all personnel
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.1)

2. Security Awareness Training
   - Mandatory training for all personnel upon hire
   - Annual security awareness updates
   - Role-specific training for technical staff
   - Regular phishing simulations
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.3)

3. Risk Management
   - Formal risk assessment process
   - Annual risk review
   - Risk-based security controls
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.2)

4. Incident Response
   - Documented incident response plan
   - Dedicated incident response team
   - Quarterly incident response testing
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.6)

5. Personnel Security
   - Background checks for all personnel (as permitted by law)
   - Security clearance requirements
   - Separation of duties
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.4)

Compliance verified by: [Compliance Officer] on [DATE]
Next policy review: [DATE + 12 months]
```

## Common Questions

### Q: How often must security training be conducted?
A: All personnel must receive training upon hire and at least annually thereafter. Additional training should be provided when policies change or new threats emerge.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.3)

### Q: What should be included in the incident response plan?
A: The plan must include roles, communication procedures, response steps, containment procedures, eradication steps, recovery procedures, and post-incident review process.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 12.6)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-12/`
- [ ] Security policy documents
- [ ] Training materials and records
- [ ] Risk assessment reports
- [ ] Incident response plan
- [ ] Incident response test results
- [ ] Security review meeting minutes

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-10]] — Logging and monitoring
