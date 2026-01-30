# Playbook: Transcript Skill Execution

<!--
TEMPLATE: Playbook
SOURCE: EN-005 Design Documentation
VERSION: 1.0.0
STATUS: ACTIVE
RELOCATED: 2026-01-26 per DISC-004
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "PB-TRANSCRIPT-001"
title: "Playbook: Transcript Skill Execution"
version: "1.0.0"
status: "ACTIVE"

# === OWNERSHIP ===
owner: "Transcript Skill Team"
author: "ps-architect"

# === CLASSIFICATION ===
classification: "L1"
criticality: "HIGH"
automation_level: "semi-automated"

# === TIMESTAMPS ===
created: "2026-01-26T10:00:00Z"
updated: "2026-01-26T14:00:00Z"

# === TRACEABILITY ===
work_items:
  epic: "EPIC-001"
  feature: "FEAT-001"
  enabler: "EN-005"
```

---

## Table of Contents

1. [Quick Start (L0 - ELI5)](#1-quick-start-l0---eli5)
2. [Overview](#2-overview)
3. [Prerequisites](#3-prerequisites)
4. [Phase 1: Foundation](#4-phase-1-foundation)
5. [Phase 2: Core Extraction](#5-phase-2-core-extraction)
6. [Phase 3: Integration](#6-phase-3-integration)
7. [Phase 4: Validation](#7-phase-4-validation)
8. [Rollback Procedures](#8-rollback-procedures)
9. [Decision Points Summary](#9-decision-points-summary)

---

## 1. Quick Start (L0 - ELI5)

### What This Playbook Does

> **Simple Analogy:** This playbook is like a recipe for cooking a meal - it breaks
> down transcript processing into 4 phases: preparing ingredients (parsing),
> extracting the good stuff (speakers, actions), plating beautifully (formatting),
> and tasting to ensure quality (validation).

**In Plain Terms:**

This playbook guides you through processing meeting transcripts using the Transcript
Skill. By the end, you'll have a structured Markdown packet with action items,
decisions, speakers, and questions - all with citations back to the original transcript.

### Expected Outcome

**Before Running This Playbook:**
- Raw transcript file (VTT, SRT, or plain text)
- Unstructured meeting content

**After Running This Playbook:**
- Structured transcript packet (8 Markdown files)
- Extracted action items with assignees
- Identified speakers with contribution statistics
- Decisions, questions, and topics categorized
- Quality score >= 0.90 verified

### Time Commitment

| Phase | Duration | Can Be Interrupted? |
|-------|----------|---------------------|
| Foundation | ~30 seconds | Yes |
| Core Extraction | ~2-5 minutes | Yes |
| Integration | ~1-2 minutes | Yes |
| Validation | ~30 seconds | Yes |
| **Total** | **~5-10 minutes** | |

---

## 2. Overview

### Purpose

Execute the Transcript Skill workflow following the 4-phase implementation approach.

### Scope

**In Scope:**
- VTT, SRT, and plain text transcript formats
- Speaker identification and extraction
- Action items, decisions, questions, topics
- Markdown packet generation with navigation

**Out of Scope:**
- Audio/video recording processing
- Real-time transcription
- Cross-meeting analysis

---

## 3. Prerequisites

### Prerequisites Checklist

- [ ] Transcript file available (VTT, SRT, or TXT format)
- [ ] File is readable and properly encoded (UTF-8 preferred)
- [ ] Output directory is writable
- [ ] Claude Code session active
- [ ] Required tools available (Read, Write, Glob, Task)

### Input File Verification

```bash
# Verify file exists
ls -la <transcript-file>

# Preview first 10 lines
head -10 <transcript-file>
```

**Expected Format Indicators:**

| Format | Signature |
|--------|-----------|
| VTT | First line: `WEBVTT` |
| SRT | First line: `1` (sequence number) |
| Plain Text | No specific header |

---

## 4. Phase 1: Foundation

### Entry Criteria

- [ ] Input file path known and accessible
- [ ] Format identified (VTT, SRT, or TXT)
- [ ] Output directory configured

### Procedure: Invoke ts-parser

**Invocation:**
```markdown
Invoke ts-parser with:
- Input: <transcript-file-path>
- Format: auto-detect (or specify: vtt, srt, txt)
```

**Verification:**
- [ ] `canonical-transcript.json` created
- [ ] JSON schema validates
- [ ] All utterances captured
- [ ] Timestamps normalized to milliseconds

### Decision Point: DP-1

| Condition | Action |
|-----------|--------|
| All exit criteria met | **PROCEED** to Phase 2 |
| Parse errors but partial output | **REVIEW** errors, then decide |
| Complete parsing failure | **ABORT** - Check input file |

---

## 5. Phase 2: Core Extraction

### Entry Criteria

- [ ] DP-1 decision: PROCEED
- [ ] index.json + chunks/*.json available (v2.0 chunked output)

### Procedure: Invoke ts-extractor

> **⚠️ CRITICAL:** NEVER use `canonical-transcript.json` as input - use chunked files only.

**Invocation:**
```markdown
Invoke ts-extractor with:
- Input: index.json + chunks/*.json (NEVER canonical-transcript.json)
- Confidence threshold: 0.7
```

**Verification:**
- [ ] extraction-report.json created
- [ ] All entity types extracted
- [ ] Confidence scores present (0.0-1.0)
- [ ] Source citations included

### Decision Point: DP-2

| Condition | Action |
|-----------|--------|
| All quality metrics met | **PROCEED** to Phase 3 |
| Quality below threshold but reasonable | **PROCEED** with warnings |
| Critical quality failure | **RETRY** with different settings |

---

## 6. Phase 3: Integration

### Entry Criteria

- [ ] DP-2 decision: PROCEED
- [ ] index.json available (v2.0 metadata)
- [ ] extraction-report.json available

### Procedure: Invoke ts-formatter

> **⚠️ CRITICAL:** NEVER use `canonical-transcript.json` as input - use index.json only.

**Invocation:**
```markdown
Invoke ts-formatter with:
- Input: index.json (NEVER canonical-transcript.json)
- Input: extraction-report.json
- Output directory: ./packet/
```

**Verification:**
- [ ] All 8 files created
- [ ] 00-index.md has navigation links
- [ ] _anchors.json contains all anchor IDs
- [ ] No file exceeds 35K tokens

---

## 7. Phase 4: Validation

### Entry Criteria

- [ ] Phase 3 exit criteria met
- [ ] All packet files accessible

### Procedure: Invoke ps-critic

**Invocation:**
```markdown
Invoke ps-critic with:
- Input: All packet files
- Quality threshold: 0.90
```

**Verification:**
- [ ] Overall score >= 0.90
- [ ] `passed: true`
- [ ] No critical issues

### Decision Point: DP-3

| Condition | Action |
|-----------|--------|
| Score >= 0.90, no critical issues | **COMPLETE** - Output ready |
| Score 0.85-0.90, minor issues only | **COMPLETE** with documented limitations |
| Score < 0.85 or critical issues | **RETRY** - Fix issues and re-validate |

---

## 8. Rollback Procedures

### Intermediate Files Preserved

All intermediate files are preserved for recovery:
- `canonical-transcript.json` - Parser output
- `extraction-report.json` - Extractor output
- `transcript-{id}/` - Formatter output

### Rollback Steps

1. **Phase 1 Rollback:** Delete corrupted JSON, retry parsing
2. **Phase 2 Rollback:** Keep canonical JSON, retry extraction
3. **Phase 3 Rollback:** Keep intermediate files, retry formatting
4. **Phase 4 Rollback:** Keep packet, re-run quality review

---

## 9. Decision Points Summary

| ID | Location | Decision | Options |
|----|----------|----------|---------|
| DP-1 | Phase 1 | Proceed to Extraction? | PROCEED / REVIEW / ABORT |
| DP-2 | Phase 2 | Extraction Quality Acceptable? | PROCEED / PROCEED with warning / RETRY |
| DP-3 | Phase 4 | Quality Gate Passed? | COMPLETE / COMPLETE with limitations / RETRY |

---

## Related Documents

- [SKILL.md](../SKILL.md) - Skill definition
- [RUNBOOK.md](./RUNBOOK.md) - Troubleshooting guide
- [ts-parser.md](../agents/ts-parser.md) - Parser agent
- [ts-extractor.md](../agents/ts-extractor.md) - Extractor agent
- [ts-formatter.md](../agents/ts-formatter.md) - Formatter agent

---

*Playbook Version: 1.0.0*
*Constitutional Compliance: P-002 (persisted), P-003 (single nesting)*
*Created: 2026-01-26*
*Relocated: 2026-01-26 per DISC-004*
