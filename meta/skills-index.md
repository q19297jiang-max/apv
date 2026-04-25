---
type: apv-meta
category: documentation
title: "APV Skills Index"
version: "1.0"
created: 2026-04-24
tags: [apv, meta, skills, index]
---

# APV Skills Index

Complete index of all APV (AI-Powered RFP Velocity) skills for documentation and reference.

## Generation Skills (6 skills)

### 1. rfp-brainstorm
**File**: [[rfp-brainstorm-skill]]
**Purpose**: Analyze RFP, generate approach options, identify questions
**Location**: `.claude/skills/rfp-brainstorm/`
**Wiki**: `wiki/apv/skills/rfp-brainstorm.md`
**Execution Time**: 5-10 minutes

### 2. rfp-compliance
**File**: [[rfp-compliance-skill]]
**Purpose**: Map requirements to regulations with source URL enforcement
**Location**: `.claude/skills/rfp-compliance/`
**Wiki**: `wiki/apv/skills/rfp-compliance.md`
**Execution Time**: 10-15 minutes

### 3. rfp-architect
**File**: [[rfp-architect-skill]]
**Purpose**: Design detailed architecture
**Location**: `.claude/skills/rfp-architect/`
**Wiki**: `wiki/apv/skills/rfp-architect.md`
**Execution Time**: 10-15 minutes

### 4. rfp-calculator
**File**: [[rfp-calculator-skill]]
**Purpose**: Calculate precise infrastructure sizing
**Location**: `.claude/skills/rfp-calculator/`
**Wiki**: `wiki/apv/skills/rfp-calculator.md`
**Execution Time**: 5-10 minutes

### 5. rfp-pricer
**File**: [[rfp-pricer-skill]]
**Purpose**: Generate cost estimates with source URL enforcement
**Location**: `.claude/skills/rfp-pricer/`
**Wiki**: `wiki/apv/skills/rfp-pricer.md`
**Execution Time**: 5-10 minutes

### 6. rfp-generator
**File**: [[rfp-generator-skill]]
**Purpose**: Create comprehensive RFP response document
**Location**: `.claude/skills/rfp-generator/`
**Wiki**: `wiki/apv/skills/rfp-generator.md`
**Execution Time**: 10-15 minutes

## Review Skills (1 skill)

### 7. apv-reviewer
**File**: [[apv-reviewer-skill]]
**Purpose**: Unified 15-minute approval verification
**Location**: `.claude/skills/apv-reviewer/`
**Wiki**: `wiki/apv/skills/apv-reviewer.md`
**Execution Time**: 15 minutes

## Orchestrator (1 skill)

### 8. apv (orchestrator)
**File**: [[apv-orchestrator-skill]]
**Purpose**: Chain all skills in sequence
**Location**: `.claude/skills/apv/`
**Wiki**: `wiki/apv/skills/apv-orchestrator.md`
**Execution Time**: 60-90 minutes (all skills)

## Skill Chain Flow

```
RFP Document
    ↓
[rfp-brainstorm] → Approach options
    ↓
[rfp-compliance] → Requirements mapping
    ↓
[rfp-architect] → Architecture design
    ↓
[rfp-calculator] → Component sizing
    ↓
[rfp-pricer] → Cost estimation
    ↓
[rfp-generator] → Response document
    ↓
[apv-reviewer] → Approval decision
    ↓
RFP Response (submission ready)
```

## File Locations

### For Execution (Global)
- **Path**: `~/.claude/skills/`
- **Used by**: Claude Code for skill execution
- **Structure**: Each skill has `skill.md` and `prompt.md`

### For Documentation (Wiki)
- **Path**: `wiki/apv/skills/`
- **Used by**: Knowledge tracking and reference
- **Structure**: Each skill has `.md` documentation file

## Related

- [[apv-implementation-plan-2026-04-24]] - Complete implementation status
- [[apv-accuracy-assurance]] - Accuracy framework requirements
- [[source-url-verification-system]] - Source URL verification
