---
type: apv-meta
category: documentation
title: "APV Production Deployment Guide"
created: 2026-04-24
tags: [apv, documentation, deployment, production, operations]
sources:
  - "[[apv-implementation-plan-2026-04-24]]"
---

# APV Production Deployment Guide

**Version**: 1.0
**Last Updated**: 2026-04-24

---

## Pre-Deployment Checklist

### Environment Verification

- [ ] **Claude Code Installed**: Latest version with skill support
- [ ] **Wiki Location**: `/Users/stevenjiang/workspace/mykb/wiki/apv/`
- [ ] **Skills Installed**: All 7 skills in `~/.claude/skills/`
- [ ] **Knowledge Base**: Complete compliance and technical knowledge
- [ ] **Python 3**: Available for verification scripts
- [ ] **File Permissions**: Scripts have execute permissions

### Skills Verification

```bash
# Verify all skills installed
ls ~/.claude/skills/ | grep rfp

# Expected output:
# rfp-brainstorm/
# rfp-compliance/
# rfp-architect/
# rfp-calculator/
# rfp-pricer/
# rfp-generator/
# apv-reviewer/
# apv/
```

### Knowledge Base Verification

```bash
# Verify knowledge structure
ls /Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/

# Expected:
# compliance/ (PCI-DSS + 7 countries)
# card-systems/ (7 card types)
# infrastructure/ (9 patterns)
# sizing/ (calculator + pricing)
# templates/ (5 templates)
```

---

## Production Deployment Steps

### Step 1: Install Skills

Skills are already installed in development. For production:

**Option A: Same Installation (Recommended)**
- Use same `~/.claude/skills/` location
- Skills are user-specific, no system-wide install needed

**Option B: Team Installation**
- Copy skill folders to each user's `~/.claude/skills/`
- Ensure each user has access to wiki

**Verification**:
```bash
# Test skill availability
/skill rfp-brainstorm --help
```

---

### Step 2: Configure Verification Scripts

Make verification scripts executable:

```bash
chmod +x /Users/stevenjiang/workspace/mykb/wiki/apv/tools/verify-source-urls.py
chmod +x /Users/stevenjiang/workspace/mykb/wiki/apv/tools/check-freshness.py
```

**Test Verification**:
```bash
# Test URL verification
cd /Users/stevenjiang/workspace/mykb/wiki/apv
python tools/verify-source-urls.py --check https://pcisecuritystandards.org

# Test freshness check
python tools/check-freshness.py --check https://aws.amazon.com/pricing/
```

---

### Step 3: Set Up Scheduled Verification

Configure automated weekly URL verification:

```bash
# Edit crontab
crontab -e

# Add weekly checks (every Monday at 2 AM)
0 2 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/verify-source-urls.py --all > \
  evidence/url-checks/verification-$(date +\%Y-\%m-\%d).json

0 3 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/check-freshness.py --all > \
  evidence/freshness-reports/freshness-$(date +\%Y-\%m-\%d).json
```

---

### Step 4: Create Evidence Directory Structure

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv/evidence

# Create subdirectories (if not exist)
mkdir -p pricing/{aws,azure,gcp}
mkdir -p compliance/{pci-dss,sg,my,ph,id,th,tw,hk}
mkdir -p url-checks
mkdir -p freshness-reports
```

---

### Step 5: Configure Wiki Index

Ensure `wiki/index.md` includes APV documentation:

```bash
# Check APV is indexed
grep -i "apv" /Users/stevenjiang/workspace/mykb/wiki/index.md
```

Expected: APV skills directory should be listed.

---

## Production Configuration

### Environment Variables (Optional)

Create `.env` file for configuration:

```bash
# APV Configuration
APV_WIKI_PATH="/Users/stevenjiang/workspace/mykb/wiki/apv"
APV_EVIDENCE_PATH="$APV_WIKI_PATH/evidence"
APV_TOOLS_PATH="$APV_WIKI_PATH/tools"

# Verification thresholds
APV_PRICING_FRESHNESS_DAYS=30
APV_COMPLIANCE_FRESHNESS_DAYS=365
```

---

### Alias Setup (Optional)

Add convenient aliases to `~/.zshrc` or `~/.bashrc`:

```bash
# APV Aliases
alias apv-brainstorm="/skill rfp-brainstorm --rfp"
alias apv-compliance="/skill rfp-compliance --rfp"
alias apv-architect="/skill rfp-architect --rfp"
alias apv-calculator="/skill rfp-calculator --rfp"
alias apv-pricer="/skill rfp-pricer --rfp"
alias apv-generator="/skill rfp-generator --rfp"
alias apv-reviewer="/skill apv-reviewer --response"
alias apv-verify="cd ~/workspace/mykb/wiki/apv && python tools/verify-source-urls.py --all"
alias apv-freshness="cd ~/workspace/mykb/wiki/apv && python tools/check-freshness.py --all"
```

Reload shell:
```bash
source ~/.zshrc
```

---

## Deployment Verification

### Test 1: Single Skill Execution

```bash
# Create test RFP
echo "# Test RFP
Card issuing system for Singapore bank.
Volume: 10,000 cards, 100 TPS.
Regions: Singapore.
" > /tmp/test-rfp.md

# Test brainstorm skill
/skill rfp-brainstorm /tmp/test-rfp.md
```

**Expected**: Output file created with brainstorm analysis

---

### Test 2: Full Chain Execution

```bash
# Test full APV chain (if orchestrator available)
/apv rfp /tmp/test-rfp.md
```

**Expected**: All 7 skills execute, final RFP response generated

---

### Test 3: Verification Scripts

```bash
# Test URL verification
python wiki/apv/tools/verify-source-urls.py --all

# Test freshness check
python wiki/apv/tools/check-freshness.py --all
```

**Expected**: Reports generated in `evidence/` directory

---

## Operations Setup

### Log Rotation

Configure log rotation for APV logs:

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/apv

# Content:
/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/*.log {
    weekly
    rotate 52
    compress
    delaycompress
    missingok
    notifempty
    create 644 www-data www-data
}
```

---

### Backup Strategy

Backup critical APV data:

```bash
# Create backup script
cat > ~/backup-apv.sh << 'EOF'
#!/bin/bash
# Backup APV wiki and evidence
DATE=$(date +%Y%m%d)
tar czf ~/apv-backup-$DATE.tar.gz \
  /Users/stevenjiang/workspace/mykb/wiki/apv/ \
  ~/.claude/skills/rfp-* \
  ~/.claude/skills/apv*

# Keep last 30 days
find ~/apv-backup-*.tar.gz -mtime +30 -delete
EOF

chmod +x ~/backup-apv.sh

# Add to crontab (daily at 1 AM)
crontab -e
# Add: 0 1 * * * ~/backup-apv.sh
```

---

## Monitoring Setup

### Source URL Monitoring

Create monitoring script for stale URLs:

```bash
cat > /Users/stevenjiang/workspace/mykb/wiki/apv/tools/monitor-urls.sh << 'EOF'
#!/bin/bash
# Monitor source URLs for freshness

cd /Users/stevenjiang/workspace/mykb/wiki/apv

# Check freshness
python tools/check-freshness.py --all > evidence/freshness-reports/latest.json

# Alert if any stale URLs
STALE=$(grep -c '"status": "stale"' evidence/freshness-reports/latest.json)

if [ "$STALE" -gt 0 ]; then
    echo "WARNING: $STALE stale URLs found"
    echo "Run: python tools/check-freshness.py --all"
fi
EOF

chmod +x /Users/stevenjiang/workspace/mykb/wiki/apv/tools/monitor-urls.sh
```

---

### Daily Manual Health Check

Run these repo-available checks directly:

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv

# 1. Check skills installed
ls ~/.claude/skills/ | grep rfp

# 2. Check wiki accessibility
ls knowledge/

# 3. Check verification scripts
ls tools/*.py

# 4. Run quick verification
python tools/verify-source-urls.py --check https://pcisecuritystandards.org | head -5
```

If you later want scheduled execution, add your own wrapper script outside the APV repo or through local automation tooling.

---

## User Access Setup

### For Individual Users

Each user needs:

1. **Claude Code** installed
2. **Wiki Access**: Read access to `/Users/stevenjiang/workspace/mykb/wiki/apv/`
3. **Skills**: Copy skill folders to `~/.claude/skills/`

```bash
# Copy skills to user home
cp -r /Users/stevenjiang/.claude/skills/rfp-* ~/.claude/skills/
cp -r /Users/stevenjiang/.claude/skills/apv* ~/.claude/skills/
```

---

### For Team Deployment

For team-wide deployment, consider:

1. **Shared Wiki**: Host wiki on shared file server
2. **Shared Skills**: Install skills in shared location
3. **Version Control**: Use git for wiki and skills
4. **Centralized Logging**: Collect logs centrally

---

## Rollback Procedure

If deployment issues occur:

### Rollback Skills

```bash
# Backup current skills
cp -r ~/.claude/skills/rfp-* ~/backup-skills/

# Restore previous version
cp -r ~/backup-apv-skills/* ~/.claude/skills/
```

### Rollback Wiki Changes

```bash
# If using git
cd /Users/stevenjiang/workspace/mykb
git log --oneline -5
git revert HEAD
```

---

## Post-Deployment Tasks

### Task 1: First RFP Processing

Process first real RFP through APV system:

1. Place RFP in working directory
2. Run full APV chain: `/apv rfp rfp-document.pdf`
3. Verify all outputs generated
4. Run reviewer: `/skill apv-reviewer --response rfp-response.md`
5. Check for approval

### Task 2: Collect Initial Evidence

For first RFP response:

1. Capture calculator screenshots
2. Save regulatory document snapshots
3. Store in `evidence/pricing/` and `evidence/compliance/`
4. Document verification dates

### Task 3: Train First Users

Train initial users:
- Pre-sales team (Task 4.2)
- Compliance officer (Task 4.3)

---

## Production Readiness Checklist

- [ ] All 7 skills installed and tested
- [ ] Wiki knowledge base complete
- [ ] Verification scripts configured
- [ ] Scheduled verification set up
- [ ] Evidence directories created
- [ ] Backup strategy configured
- [ ] Monitoring scripts deployed
- [ ] User access configured
- [ ] Documentation distributed
- [ ] First users trained

---

## Contact and Support

### Documentation

- [[apv-user-guide]] - User guide
- [[apv-skill-reference]] - Skill reference
- [[apv-troubleshooting]] - Troubleshooting

### Implementation Status

- [[apv-implementation-plan-2026-04-24]] - Project status

### Issue Reporting

Add issues to:
- `wiki/log.md` - Operations log
- `wiki/meta/apv-implementation-plan-2026-04-24.md` - Project plan

---

## Deployment Complete!

Your APV system is now in production.

**Next Steps**:
1. Process your first real RFP
2. Collect evidence
3. Train your team
4. Iterate and improve

---

**Deployment Date**: 2026-04-24
**Deployed By**: APV Team
**Version**: 1.0
