# FEAT-006: Output Consistency

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-01-31 (Claude Code session)
PURPOSE: Ensure transcript skill output consistency across models
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-31T00:00:00Z
> **Due:** -
> **Completed:** -
> **Parent:** EPIC-001-transcript-skill
> **Owner:** Adam Nowak
> **Target Sprint:** -

---

## Summary

Address critical output inconsistency in the transcript skill when using different LLM models (Sonnet vs Opus). The Opus model produces completely different output format compared to Sonnet, violating ADR-002 packet structure with broken `seg-xxx` citation links, incorrect file numbering, missing navigation links, and altered file structure.

**Value Proposition:**
- Consistent, predictable output regardless of model selection
- Reliable citation/linking system for cross-referencing
- Model-agnostic output format conforming to ADR-002 specification

---

## Problem Statement

### L0 (ELI5)
When we ask different AI assistants (Sonnet vs Opus) to process the same meeting transcript, they produce completely different formats. It's like asking two different people to take notes - one follows our template, the other makes up their own format. We need everyone to follow the same rules.

### L1 (Software Engineer)
The transcript skill's ts-formatter agent produces inconsistent output when invoked with different model profiles:
- **Default (Sonnet)**: Correct 8-file ADR-002 packet with proper `seg-xxx` citations
- **Opus**: Wrong file structure (02-action-items.md instead of 04-action-items.md), broken links pointing to canonical-transcript.json, missing navigation links

### L2 (Principal Architect)
The lack of enforced output templates in agent definitions means model-specific behaviors leak through, violating the principle that output format should be invariant to model selection. This represents a fundamental architectural gap - the ts-formatter agent definition lacks sufficient guardrails to ensure deterministic output structure.

---

## Observed Defects

### File Structure Inconsistency

| Expected (ADR-002) | Default Output | Opus Output |
|--------------------|----------------|-------------|
| 00-index.md | ✓ | ✓ |
| 01-summary.md | ✓ | ✓ |
| 02-transcript.md | ✓ | **02-action-items.md** ❌ |
| 03-speakers.md | ✓ | **03-decisions.md** ❌ |
| 04-action-items.md | ✓ | **04-questions.md** ❌ |
| 05-decisions.md | ✓ | **05-speakers.md** ❌ |
| 06-questions.md | ✓ | **06-timeline.md** ❌ (new!) |
| 07-topics.md | ✓ | **07-topics.md** ✓ |

### Citation Link Defects

**Expected Format:**
```markdown
> *[15:58] Adam Nowak:*
> "I will definitely chase those guys down..."
```

**Opus Output (BROKEN):**
```markdown
> "Great. Thank you very much. I will definitely chase those guys down to find out if they have the capability."

- **Segment**: [seg-241](canonical-transcript.json#seg-241)  ← BROKEN LINK
```

### Navigation Link Defects

**Expected:**
```markdown
[Previous: Speakers](03-speakers.md) | [Index](00-index.md) | [Next: Decisions](05-decisions.md)
```

**Opus Output:**
```markdown
[Back to Index](00-index.md)  ← MISSING PREV/NEXT NAVIGATION
```

---

## Benefit Hypothesis

**We believe that** defining and enforcing a "golden" output template specification

**Will result in** consistent, predictable transcript skill output regardless of model selection

**We will know we have succeeded when** processing the same transcript with economy, balanced, quality, and speed profiles produces byte-identical file structure (differing only in content quality)

---

## Acceptance Criteria

### Definition of Done

- [ ] Golden output template specification documented
- [ ] ADR-007 documents template decisions
- [ ] ts-formatter agent definition updated with enforced templates
- [ ] SKILL.md updated with template specifications
- [ ] All 4 model profiles produce identical file structure
- [ ] Citation links validated across profiles
- [ ] Navigation links validated across profiles
- [ ] ps-critic validation >= 0.90 for all profiles

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | File structure matches ADR-002 (8 files in correct order) | [ ] |
| AC-2 | All `seg-xxx` citations link to correct anchors in 02-transcript.md | [ ] |
| AC-3 | Navigation links present on all files (Prev/Index/Next) | [ ] |
| AC-4 | Output format invariant to model profile selection | [ ] |
| AC-5 | Template specification documented for 3 personas | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Template validation completes in < 5 seconds | [ ] |
| NFC-2 | Documentation covers ELI5, Engineer, Architect personas | [ ] |
| NFC-3 | Industry best practices cited with sources | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Gap analysis between Sonnet and Opus outputs
- Historical research of FEAT-001 template specifications
- Industry research on meeting transcript formats
- Golden template specification design
- ts-formatter agent definition update
- SKILL.md template documentation
- Validation across all 4 model profiles

### Out of Scope (Future)

- Automated template compliance testing in CI
- Retroactive fixing of existing transcript outputs
- Output format versioning system
- User-customizable templates

---

## Children (Stories/Enablers)

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-030 | Enabler | Gap Analysis | pending | high | M |
| EN-031 | Enabler | Historical Research | pending | high | M |
| EN-032 | Enabler | Industry Research | pending | high | L |
| EN-033 | Enabler | Specification Design | pending | high | L |
| EN-034 | Enabler | Implementation | pending | high | M |
| EN-035 | Enabler | Validation & Review | pending | high | M |

### Work Item Links

- [EN-030: Gap Analysis](./EN-030-gap-analysis/EN-030-gap-analysis.md)
- [EN-031: Historical Research](./EN-031-historical-research/EN-031-historical-research.md)
- [EN-032: Industry Research](./EN-032-industry-research/EN-032-industry-research.md)
- [EN-033: Specification Design](./EN-033-specification-design/EN-033-specification-design.md)
- [EN-034: Implementation](./EN-034-implementation/EN-034-implementation.md)
- [EN-035: Validation & Review](./EN-035-validation-review/EN-035-validation-review.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/6 completed)             |
| Tasks:     [....................] 0% (0/? completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 6 |
| **Completed Enablers** | 0 |
| **Total Effort (points)** | TBD |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Orchestration

This feature uses the **orchestration skill** for coordinated multi-agent execution.

**Artifacts:**
- [ORCHESTRATION_PLAN.md](./orchestration/ORCHESTRATION_PLAN.md)
- [ORCHESTRATION_WORKTRACKER.md](./orchestration/ORCHESTRATION_WORKTRACKER.md)
- [ORCHESTRATION.yaml](./orchestration/ORCHESTRATION.yaml)

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: Transcript Skill](../EPIC-001-transcript-skill.md)

### Related Features

- [FEAT-001: Analysis & Design](../FEAT-001-analysis-design/FEAT-001-analysis-design.md) - Contains original template specifications
- [FEAT-002: Implementation](../FEAT-002-implementation/FEAT-002-implementation.md) - ts-formatter agent definition
- [FEAT-005: Skill Compliance](../FEAT-005-skill-compliance/FEAT-005-skill-compliance.md) - Documentation compliance

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| References | ADR-002 | Packet structure specification |
| References | ADR-004 | File splitting rules |
| References | ADR-003 | Anchor registry format |
| Depends On | FEAT-001 | Original template research |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-31 | Claude Code | pending | Feature created to address output inconsistency |
| 2026-01-31 | Claude Code | in_progress | Orchestration plan creation started |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |

---

## Reference Evidence

### Sonnet Output (Default - Correct)
Path: `Downloads/chats/2026-01-30-certificate-architecture/`

### Opus Output (Incorrect)
Path: `Downloads/chats/2026-01-30-certificate-architecture-opus-v2/`
