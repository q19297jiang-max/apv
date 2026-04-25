---
type: apv-meta
category: documentation
title: "APV Troubleshooting Guide"
created: 2026-04-24
tags: [apv, documentation, troubleshooting, support]
sources:
  - "[[apv-user-guide]]"
---

# APV Troubleshooting Guide

**Common issues and solutions for the APV system**

---

## Installation Issues

### Issue: Skills Not Found

**Symptoms**:
```
Error: Skill not found: rfp-brainstorm
Error: Unknown skill: apv
```

**Diagnosis**:
```bash
# Check if skills are installed
ls ~/.claude/skills/

# Expected output should include:
# rfp-brainstorm/
# rfp-compliance/
# rfp-architect/
# rfp-calculator/
# rfp-pricer/
# rfp-generator/
# apv-reviewer/
# apv/
```

**Solutions**:
1. Check skills directory exists: `ls -la ~/.claude/skills/`
2. Verify skill folders contain `skill.md` and `prompt.md`
3. Reinstall skills if missing

---

### Issue: Wiki Not Found

**Symptoms**:
```
Error: Wiki file not found: wiki/apv/knowledge/compliance/pci-dss/overview.md
```

**Diagnosis**:
```bash
# Check wiki location
ls /Users/stevenjiang/workspace/mykb/wiki/apv/

# Expected: knowledge/, templates/, skills/, tools/, tests/
```

**Solutions**:
1. Verify wiki directory structure
2. Check `wiki/index.md` lists APV files
3. Update wiki path in skill prompts if moved

---

## Execution Issues

### Issue: Slow Skill Execution

**Symptoms**:
- Skill taking longer than estimated time
- High file read count
- Repeated knowledge file access

**Diagnosis**:
```bash
# Check what files skill is reading
# (Review skill output for "Reading:" messages)

# Count knowledge files accessed
grep -r "Reading:" skill-output.md | wc -l
```

**Solutions**:
1. Optimize skill to read only relevant files
2. Use selective file reading (target countries only)
3. Enable caching for frequently accessed files

---

### Issue: Missing Knowledge

**Symptoms**:
```
No knowledge on [specific country/regulation]
Knowledge gap: [topic] not covered in wiki
```

**Diagnosis**:
```bash
# Check what countries are covered
ls wiki/apv/knowledge/compliance/countries/

# Supported: sg, my, ph, id, th, tw, hk
```

**Solutions**:
1. Verify country is in supported list
2. If new country needed, add to knowledge base:
   - Create country folder
   - Add regulation files with source URLs
   - Update compliance skill
3. Document gap explicitly in output

---

## Source URL Issues

### Issue: Source URL Not Found

**Symptoms**:
```
Source URL not found for [claim]
Missing source_url in frontmatter
```

**Diagnosis**:
```bash
# Check knowledge file frontmatter
head -20 wiki/apv/knowledge/compliance/pci-dss/overview.md

# Should include:
# source_url: "https://..."
```

**Solutions**:
1. Add `source_url` to knowledge file frontmatter
2. Verify URL is accessible
3. Run verification script:
```bash
python wiki/apv/tools/verify-source-urls.py --check <url>
```

---

### Issue: URL Not Accessible

**Symptoms**:
```
Error: URL returned 404/500
Error: Connection timeout
```

**Diagnosis**:
```bash
# Check URL accessibility
python wiki/apv/tools/verify-source-urls.py --check <url>

# Or use curl
curl -I <url>
```

**Solutions**:
1. Verify URL is correct
2. Check if website is accessible
3. Find alternative official source
4. Update `source_url` in knowledge file frontmatter

---

### Issue: URL Not Fresh (Stale)

**Symptoms**:
```
Warning: URL is [X] days old (exceeds limit)
Stale pricing source (limit: 30 days)
Stale compliance source (limit: 365 days)
```

**Diagnosis**:
```bash
# Check URL freshness
python wiki/apv/tools/check-freshness.py --check <url>
```

**Solutions**:
1. **Pricing sources** (30-day limit):
   - Recapture calculator screenshot
   - Update knowledge file with new date
   - Store new evidence in `wiki/apv/evidence/pricing/`

2. **Compliance sources** (365-day limit):
   - Check if regulation updated
   - Verify requirement still applicable
   - Update to new version if needed

3. **Freshness thresholds**:
   - Pricing: 30 days
   - Compliance: 365 days
   - General: 180 days

---

## Output Issues

### Issue: Incomplete Output

**Symptoms**:
- Missing sections in skill output
- Truncated response
- Empty tables

**Diagnosis**:
```bash
# Check skill output file
cat skill-output.md

# Look for "ERROR" or "FAILED" messages
grep -i error skill-output.md
```

**Solutions**:
1. Check if input RFP is complete
2. Verify knowledge files are accessible
3. Re-run skill with more context
4. Check for token limits (break into smaller tasks)

---

### Issue: Poor Formatting

**Symptoms**:
- Tables not rendering correctly
- Markdown errors
- Inconsistent structure

**Diagnosis**:
```bash
# Validate markdown
# (Use markdown linter if available)
```

**Solutions**:
1. Check template adherence
2. Verify markdown syntax
3. Test in markdown previewer
4. Report formatting bugs

---

## Compliance Issues

### Issue: Compliance Not Mapped

**Symptoms**:
```
Warning: Requirement not mapped to regulation
Gap: No compliance source found
```

**Diagnosis**:
```bash
# Check compliance output
cat compliance-output.md | grep -i gap
```

**Solutions**:
1. Verify requirement is in scope
2. Check if country is supported
3. Add missing regulation to knowledge base
4. Document gap explicitly (acceptable if truly unknown)

---

### Issue: Wrong Compliance Mapped

**Symptoms**:
- PCI-DSS requirement incorrectly mapped
- Country regulation applied to wrong country

**Diagnosis**:
```bash
# Review compliance matrix
# Verify requirement mapping is correct
```

**Solutions**:
1. Cross-check with official PCI-DSS document
2. Verify country regulation applies to target country
3. Update knowledge file if error
4. Report documentation bug

---

## Performance Issues

### Issue: Memory/Token Limits

**Symptoms**:
- Response cut off mid-sentence
- Skill stops unexpectedly
- Context length warning

**Diagnosis**:
```bash
# Check response size
wc -l skill-output.md
```

**Solutions**:
1. Break into smaller tasks
2. Run skills individually instead of full chain
3. Optimize prompts (already done in Task 3.4)
4. Clear context and restart

---

### Issue: Chain Execution Fails

**Symptoms**:
```
Error: Skill chain failed at skill [N]
Error: Previous skill output not found
```

**Diagnosis**:
```bash
# Check all previous skill outputs exist
ls brainstorm-output.md
ls compliance-output.md
ls architecture-output.md
# ... etc
```

**Solutions**:
1. Verify previous skills completed successfully
2. Check output file names match expected
3. Re-run failed skill
4. Check for error messages in failed skill output

---

## Verification Issues

### Issue: Verification Script Fails

**Symptoms**:
```bash
$ python wiki/apv/tools/verify-source-urls.py --all
Error: Module not found
SyntaxError
```

**Diagnosis**:
```bash
# Check Python environment
python3 --version

# Check script exists
ls wiki/apv/tools/verify-source-urls.py
```

**Solutions**:
1. Ensure Python 3 installed
2. Install required packages: `pip3 install openpyxl`
3. Check script has execute permissions: `chmod +x script.py`
4. Check for syntax errors in script

---

### Issue: Freshness Check Fails

**Symptoms**:
```
Error: can't subtract offset-naive and offset-aware datetimes
Error: No date information available
```

**Diagnosis**:
```bash
# Check if URL provides Last-Modified header
curl -I <url> | grep -i last-modified
```

**Solutions**:
1. Some URLs don't provide date info (mark as "Unknown")
2. Script handles timezone-aware datetimes (fixed in Task 3.5)
3. Manually verify if needed

---

## Data Issues

### Issue: RFP Not Parsed

**Symptoms**:
```
Error: Could not read RFP file
Error: Unsupported file format
```

**Diagnosis**:
```bash
# Check file format
file path/to/rfp

# Supported: PDF, DOCX, TXT, MD
```

**Solutions**:
1. Convert RFP to supported format
2. Copy text from RFP to text file
3. Use OCR for PDF if needed (manual step)

---

### Issue: Volume Data Missing

**Symptoms**:
- Calculator cannot determine TPS
- Sizing output shows "N/A"

**Diagnosis**:
```bash
# Check if RFP contains transaction volumes
grep -i "transaction\|tps\|volume" rfp-file
```

**Solutions**:
1. If volume not specified, use assumptions:
   - Retail issuing: 10-50 TPS per 1000 cards
   - Low volume: <1 TPS
   - High volume: 100+ TPS
2. Document assumptions in output
3. Ask customer for clarification

---

## Getting Help

### Diagnostic Commands

```bash
# 1. Check APV installation
ls -la ~/.claude/skills/ | grep rfp
ls -la /Users/stevenjiang/workspace/mykb/wiki/apv/

# 2. Verify knowledge base
ls /Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/compliance/countries/

# 3. Run verification
python wiki/apv/tools/verify-source-urls.py --all
python wiki/apv/tools/check-freshness.py --all

# 4. Check recent outputs
ls -lt *.md | head -10
```

### Log Files

```bash
# Check wiki operations log
cat /Users/stevenjiang/workspace/mykb/wiki/log.md

# Check implementation plan
cat /Users/stevenjiang/workspace/mykb/wiki/meta/apv-implementation-plan-2026-04-24.md
```

### Documentation

- [[apv-user-guide]] - Complete user guide
- [[apv-skill-reference]] - Skill quick reference
- [[source-url-verification-system]] - Verification system
- [[apv-implementation-plan-2026-04-24]] - Project status

---

## Error Messages Reference

| Error | Meaning | Solution |
|-------|---------|----------|
| `Skill not found` | Skill not installed | Check `~/.claude/skills/` |
| `Wiki file not found` | Knowledge file missing | Verify wiki path |
| `No knowledge on [topic]` | Topic not in wiki | Add to wiki or document gap |
| `Source URL not found` | Missing `source_url` in frontmatter | Add to knowledge file |
| `URL not accessible` | URL returns error | Check URL, find alternative |
| `URL not fresh` | URL exceeds freshness limit | Update with fresh source |
| `Compliance not mapped` | No regulation found | Check country support, add regulation |

---

## Common Fixes

### Fix 1: Reset Skills

```bash
# Remove and reinstall skills
rm -rf ~/.claude/skills/rfp-*
# (Reinstall from wiki)
```

### Fix 2: Rebuild Knowledge Index

```bash
# Update wiki index
# (Manual step - add new files to wiki/index.md)
```

### Fix 3: Clear Cache

```bash
# Clear Claude Code cache
# (Menu → Clear Cache)
```

### Fix 4: Update Source URLs

```bash
# Find files with missing source_urls
grep -L "source_url" wiki/apv/knowledge/compliance/**/*.md

# Add to frontmatter:
# source_url: "https://..."
```

---

## Known Limitations

1. **Country Coverage**: Only 7 Asian countries (SG, MY, PH, ID, TH, TW, HK)
2. **Card Types**: Issuing, acquiring, gateway, digital wallet
3. **Cloud Providers**: AWS, Azure, GCP only
4. **RFP Languages**: English only
5. **Token Limits**: Very large RFPs may need splitting

---

## Reporting Issues

When reporting issues, include:
1. **Error message**: Full error text
2. **Steps to reproduce**: What you were doing
3. **Input**: RFP file (if possible)
4. **Expected**: What you expected to happen
5. **Actual**: What actually happened

Report via:
- GitHub Issues (if applicable)
- Wiki log: Add entry to `wiki/log.md`

---

**Last Updated**: 2026-04-24
**Version**: 1.0
