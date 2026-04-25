---
type: apv-meta
category: documentation
title: "APV Operations Guide"
created: 2026-04-24
tags: [apv, documentation, operations, procedures]
sources:
  - "[[apv-deployment-guide]]"
---

# APV Operations Guide

**Standard Operating Procedures for APV System**

---

## Daily Operations

### Morning Checklist

**Time**: 5 minutes

1. **Check Automated Jobs**
   ```bash
   # Verify overnight verification ran
   ls -lt ~/workspace/mykb/wiki/apv/evidence/url-checks/ | head -5
   ls -lt ~/workspace/mykb/wiki/apv/evidence/freshness-reports/ | head -5
   ```

2. **Review Health Check**
   ```bash
   # Run health check
   ~/workspace/mykb/wiki/apv/tools/health-check.sh
   ```

3. **Check for Alerts**
   - Review any stale URL warnings
   - Check for verification failures

---

### Weekly Tasks

**Day**: Monday

**Time**: 30 minutes

1. **Review Verification Reports**
   ```bash
   cat ~/workspace/mykb/wiki/apv/evidence/url-checks/verification-$(date +%Y-%m-%d --date='Monday last week').json
   cat ~/workspace/mykb/wiki/apv/evidence/freshness-reports/freshness-$(date +%Y-%m-%d --date='Monday last week').json
   ```

2. **Address Stale URLs**
   - Identify stale pricing sources (>30 days)
   - Identify stale compliance sources (>365 days)
   - Update knowledge files with fresh sources
   - Capture new evidence (screenshots, snapshots)

3. **Weekly Summary**
   - Log weekly activities to `wiki/log.md`
   - Note any issues encountered
   - Document improvements made

---

## RFP Processing Workflow

### Standard Operating Procedure

**Trigger**: New RFP received from customer

**Step 1: Triage** (5 minutes)
- Review RFP document
- Identify card type (issuing, acquiring, gateway, wallet)
- Identify target countries
- Estimate complexity (low/medium/high)
- Assign to pre-sales engineer

**Step 2: Process RFP** (60-90 minutes)
```bash
# Copy RFP to working directory
cp /path/to/rfp.pdf ~/workspace/apv/current/

# Run full APV chain
cd ~/workspace/apv/current
/apv rfp rfp.pdf
```

**Step 3: Review Outputs** (15 minutes)
- Check brainstorm output for approach options
- Verify compliance matrix completeness
- Review architecture design
- Check pricing calculations

**Step 4: Approval** (15 minutes)
```bash
# Run reviewer
/skill apv-reviewer --response rfp-response.md
```

**Step 5: Final Polish** (30 minutes)
- Address any "Conditional" or "Reject" items
- Collect evidence if needed
- Final formatting

**Step 6: Submit** (5 minutes)
- Package response with evidence
- Submit to customer
- Log completion

**Total Time**: 2-3 hours (vs 2-3 weeks manual)

---

## Evidence Management

### Evidence Collection Procedures

#### Pricing Evidence

**When**: After generating pricing for RFP response

**Procedure**:
1. Open official calculator (AWS/Azure/GCP)
2. Configure with exact inputs from sizing
3. Capture full-page screenshot
4. Save with naming convention:
   ```
   pricing-{provider}-{card-type}-{tps}-{date}.png
   Example: pricing-aws-issuing-1000tps-2026-04-24.png
   ```
5. Store in: `wiki/apv/evidence/pricing/{provider}/`

**Verification**:
- Calculator URL visible in screenshot
- Configuration inputs visible
- Date captured visible

#### Compliance Evidence

**When**: After generating compliance matrix

**Procedure**:
1. Open official regulatory document
2. Navigate to specific requirement/section
3. Capture screenshot or save PDF
4. Save with naming convention:
   ```
   compliance-{country}-{regulation}-{req}-{date}.pdf
   Example: compliance-sg-mas-trm-sec3-2026-04-24.pdf
   ```
5. Store in: `wiki/apv/evidence/compliance/{country}/`

**Verification**:
- Official source URL visible
- Requirement/section clearly marked
- Capture date visible

---

## Maintenance Procedures

### URL Freshness Monitoring

**Automated**: Weekly via cron

**Manual**: When alerted to stale URLs

**Procedure for Stale Pricing URLs** (>30 days):
1. Open calculator from source URL
2. Re-capture screenshot with current date
3. Update `source_url` in knowledge file if changed
4. Save new evidence in `evidence/pricing/`
5. Document change in `wiki/log.md`

**Procedure for Stale Compliance URLs** (>365 days):
1. Check if regulation updated
2. Open new version from official source
3. Verify requirement still applicable
4. Update knowledge file if needed
5. Document change in `wiki/log.md`

---

### Knowledge Base Updates

**When**: New regulations released, cloud pricing changes

**Procedure**:
1. Create new knowledge file or update existing
2. Include `source_url` in frontmatter
3. Include `source_version` and `last_verified` dates
4. Test with verification scripts
5. Update `wiki/index.md` if new file
6. Log in `wiki/log.md`

---

## Incident Response

### Incident Types

| Severity | Description | Response Time |
|----------|-------------|----------------|
| Critical | Skills not working | 1 hour |
| High | Stale URLs in production RFP | 4 hours |
| Medium | Knowledge base error | 1 day |
| Low | Documentation typo | 1 week |

### Critical Incident: Skills Not Working

**Detection**: User reports skill failure

**Response**:
1. **Immediate** (5 min)
   - Verify skill installation
   - Check wiki accessibility
   - Test with simple RFP

2. **Diagnosis** (15 min)
   - Check error messages
   - Review recent changes
   - Check system logs

3. **Resolution** (30 min)
   - Fix if simple (permissions, paths)
   - Rollback if recent change
   - Escalate if needed

4. **Recovery** (10 min)
   - Verify fix with test RFP
   - Document incident
   - Update log

---

### High Incident: Stale URLs in Production RFP

**Detection**: Automated monitoring alerts

**Response**:
1. **Immediate** (5 min)
   - Identify stale URLs
   - Assess impact (pricing vs compliance)

2. **Pricing Stale** (< 30 days overdue)
   - Recapture calculator screenshot
   - Update knowledge file
   - Document update

3. **Compliance Stale** (< 365 days overdue)
   - Verify regulation still current
   - Update if needed
   - Document research

4. **Customer Communication** (if needed)
   - Inform if material change
   - Provide updated evidence

---

## Backup and Recovery

### Backup Schedule

**Daily**:
- Evidence files (automated via backup script)

**Weekly**:
- Full wiki backup
- Skills backup

**Monthly**:
- Archive old evidence to cold storage

### Recovery Procedures

**Restore from Backup**:
```bash
# List available backups
ls -lt ~/apv-backup-*.tar.gz

# Restore most recent
tar xzf ~/apv-backup-latest.tar.gz -C ~/

# Verify restoration
ls ~/workspace/mykb/wiki/apv/
ls ~/.claude/skills/ | grep rfp
```

---

## Performance Monitoring

### Key Metrics

Track monthly:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| RFP Processing Time | < 3 hours | Time from start to approval |
| Skill Success Rate | > 95% | Skills completing without error |
| Source URL Compliance | 100% | All claims have source URLs |
| Freshness Compliance | > 95% | URLs within freshness limits |
| User Satisfaction | > 4/5 | User feedback |

### Monthly Review

**At end of each month**:

1. **Run Performance Report**
   ```bash
   # Count RFPs processed
   grep -c "RFP Complete" wiki/log.md

   # Check source URL compliance
   python tools/verify-source-urls.py --all | grep "Compliance:"
   ```

2. **Review Issues**
   - Count incidents by type
   - Identify trends
   - Plan improvements

3. **Update Documentation**
   - Document changes in procedures
   - Update guides if needed
   - Log in `wiki/log.md`

---

## User Support

### Common Support Requests

| Request | Resolution Time | Procedure |
|---------|-----------------|------------|
| Skill not found | 5 min | Check installation, verify paths |
| Knowledge gap | 15 min | Explain gap, suggest alternative |
| URL stale | 1 day | Update with fresh source |
| Output question | 30 min | Clarify output section |
| Training request | 1 week | Schedule training session |

### Escalation

**Level 1**: Operations (日常问题)
- Most incidents resolved at this level

**Level 2**: Development (技术问题)
- Skills not working, bugs found
- Escalate if not resolved in 4 hours

**Level 3**: Management (决策问题)
- Strategic decisions, resource allocation
- Escalate for business decisions

---

## Continuous Improvement

### Monthly Improvements

**Review and Improve**:
1. Analyze support requests
2. Identify common issues
3. Implement fixes
4. Update documentation
5. Train users on changes

### Quarterly Reviews

**Quarterly Assessment**:
1. Review performance metrics
2. Assess user satisfaction
3. Identify training gaps
4. Plan system enhancements
5. Update implementation plan

---

## Runbook Quick Reference

### Quick Commands

```bash
# Health check
~/workspace/mykb/wiki/apv/tools/health-check.sh

# Verify all URLs
cd ~/workspace/mykb/wiki/apv && python tools/verify-source-urls.py --all

# Check freshness
cd ~/workspace/mykb/wiki/apv && python tools/check-freshness.py --all

# Process RFP
cd ~/workspace && /apv rfp path/to/rfp.pdf

# Review response
/skill apv-reviewer --response rfp-response.md

# Backup
~/backup-apv.sh
```

### Critical File Locations

| File/Directory | Purpose |
|----------------|---------|
| `~/.claude/skills/rfp-*` | APV skills |
| `~/workspace/mykb/wiki/apv/` | Knowledge base |
| `~/workspace/mykb/wiki/apv/evidence/` | Evidence storage |
| `~/workspace/mykb/wiki/apv/tools/` | Verification scripts |
| `~/workspace/mykb/wiki/log.md` | Operations log |

---

## Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| APV Owner | [Name] | [Email] |
| Operations Lead | [Name] | [Email] |
| Knowledge Maintainer | [Name] | [Email] |
| Pre-sales Lead | [Name] | [Email] |

---

**Operations Guide Version**: 1.0
**Last Updated**: 2026-04-24
**Maintained By**: APV Operations Team
