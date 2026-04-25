---
type: apv-knowledge
category: compliance
subcategory: pci-dss
title: "PCI-DSS Requirement 10"
source_url: "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf"
source_document: "PCI-DSS-v4_0.pdf"
source_version: "4.0"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [pci-dss, compliance, logging, monitoring, audit-trail, requirement-10]
---

# PCI-DSS Requirement 10: Logging and Monitoring

## Official Requirement

> [!quote] From PCI-DSS v4.0
> "Log and monitor all access to system components and cardholder data by:
> - Implementing audit trails
> - Logging all system and network activity
> - Securing audit logs
> - Retaining logs for at least one year
> - Reviewing logs regularly
> - Protecting log integrity"

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Requirement 10)

## Implementation Requirements

### 10.1 Audit Trails
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.1)

- Implement audit trails for all system components
- Link audit trails to individual users
- Include timestamp, source, destination, and outcome

### 10.2 Logging Requirements
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.2)

**What to Log**:
- All user access to cardholder data
- All privileged access
- All administrative actions
- Access to audit logs
- Invalid logical access attempts
- Use of and changes to identification mechanisms
- Creation and deletion of system-level objects
- Changes to security configurations

### 10.3 Log Protection
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.3)

- Protect logs from tampering
- Restrict log access to authorized personnel only
- Promptly back up log files

### 10.4 Log Retention
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.4)

- Retain audit trail history for at least one year
- Keep at least 3 months available for immediate analysis

### 10.5 Log Review
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.5)

- Review logs for all system components at least daily
- Follow up on exceptions and anomalies
- Document review findings

### 10.6 Time Synchronization
**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.6)

- Use time synchronization technology (NTP)
- Synchronize all critical systems

## Implementation in Cloud Infrastructure

### AWS Logging
**Source**: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/

```
Components:
├── CloudWatch Logs - Centralized logging
├── CloudWatch Insights - Log analytics
├── CloudTrail - Audit trail of API calls
├── VPC Flow Logs - Network traffic logging
├── AWS Config - Configuration change tracking
└── S3 - Long-term log archival
```

**Implementation**:
- All services log to CloudWatch Logs
- CloudTrail enabled for all regions
- VPC Flow Logs enabled for all VPCs
- Logs archived to S3 Glacier (1-year retention)

### Azure Logging
**Source**: https://learn.microsoft.com/en-us/azure/azure-monitor/

```
Components:
├── Azure Monitor Logs - Centralized logging
├── Log Analytics - Log analytics
├── Azure Activity Log - Audit trail
├── NSG Flow Logs - Network traffic logging
├── Azure Storage - Long-term archival
└── Microsoft Sentinel - SIEM/SOAR
```

### GCP Logging
**Source**: https://cloud.google.com/logging/docs

```
Components:
├── Cloud Logging - Centralized logging
├── Log Router - Log routing and export
├── Cloud Audit Logs - Audit trail
├── VPC Flow Logs - Network traffic logging
├── Cloud Storage - Long-term archival
└── Chronicle - SIEM/SOAR
```

## Log Data Requirements

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.1)

### Minimum Log Fields
| Field | Description | Example |
|-------|-------------|---------|
| User ID | Who performed the action | jdoe@company.com |
| Event Type | What action was performed | Read cardholder data |
| Timestamp | When the action occurred | 2026-04-24T10:15:30Z |
| Source | Where the action originated | IP: 192.168.1.100 |
| Destination | Target of the action | Database: prod-db-01 |
| Outcome | Success or failure | Success/Failure |
| Reason | Why action was performed | Customer service inquiry |

## SIEM Integration

**Source**: Industry best practices for PCI-DSS compliance

```
SIEM (Security Information and Event Management):
├── Log Aggregation - Centralize logs from all sources
├── Correlation - Detect patterns across systems
├── Alerting - Notify on suspicious activity
├── Dashboards - Real-time monitoring
├── Reporting - Compliance reports
└── Retention - Long-term log storage
```

### Popular SIEM Solutions
- **Cloud-native**: AWS Security Hub + Detective, Azure Sentinel, GCP Chronicle
- **Commercial**: Splunk, IBM QRadar, LogRhythm
- **Open-source**: Elastic Stack (ELK), Graylog

## Evidence Required

For PCI-DSS audit of Requirement 10:
- [ ] Logging policy and procedures
- [ ] Log configuration documentation
- [ ] Sample log outputs showing all required fields
- [ ] Log retention policy and proof of retention
- [ ] Log review procedures and review records
- [ ] Time synchronization documentation
- [ ] SIEM configuration

## RFP Response Template

### Question: "How do you log and monitor access?"

```
[Company Name] implements PCI-DSS Requirement 10 through:

1. Comprehensive Logging
   - All system access logged with user ID, timestamp, action
   - All privileged access logged
   - All security events logged
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.2)

2. Centralized Log Management
   - [CloudWatch/Azure Monitor/GCP Cloud Logging] for centralized logging
   - SIEM implementation for log analysis and correlation
   - Real-time alerting on suspicious activity
   Source: [Cloud provider documentation]

3. Log Protection and Retention
   - Logs protected from tampering (write-once storage)
   - Log retention: 1 year (3 months immediately available)
   - Regular log backups to immutable storage
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.3, 10.4)

4. Continuous Monitoring
   - 24/7 security monitoring via SOC
   - Daily log review of critical systems
   - Automated threat detection and response
   Source: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.5)

Compliance verified by: [Compliance Officer] on [DATE]
```

## Common Questions

### Q: Do logs containing PAN need special protection?
A: Yes. Logs must not display full PAN. Mask middle digits (6••••••••1234). If PAN must be logged, it must be encrypted or tokenized.

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.2, 3.3)

### Q: How long must logs be retained?
A: At least one year, with at least 3 months immediately available for analysis (not archived offline).

**Source**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf (Req 10.4)

## Evidence Storage
- `wiki/apv/knowledge/evidence/pci-dss/req-10/`
- [ ] Logging policy
- [ ] Log sample outputs
- [ ] Log review reports
- [ ] SIEM dashboards
- [ ] Retention policy documentation

## Related
- [[pci-dss-overview]] — PCI-DSS framework overview
- [[pci-dss-req-11]] — Security testing requirements
