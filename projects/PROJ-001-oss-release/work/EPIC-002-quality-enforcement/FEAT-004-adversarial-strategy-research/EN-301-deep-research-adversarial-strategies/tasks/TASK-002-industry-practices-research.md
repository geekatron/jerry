# TASK-002: Research Industry Practices and LLM-Specific Patterns

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata |
| [Content](#content) | Description and acceptance criteria |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Research industry practices and LLM-specific patterns"
description: |
  Examine adversarial patterns from software engineering (code review), security (penetration
  testing, threat modeling), and AI safety (constitutional AI, RLHF critique). Focus on
  codified practices with documented outcomes and LLM-specific adversarial patterns.
classification: ENABLER
status: DONE
resolution: COMPLETED
priority: CRITICAL
assignee: "ps-researcher"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-301"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - At least 8 strategies identified from industry and LLM sources
  - Each strategy has: name, origin/author, citation (DOI/ISBN), description, mechanism, strengths, weaknesses
  - LLM-specific patterns (Self-Refine, CoV, CRITIC, Reflexion) covered with paper citations
  - L0/L1/L2 output levels present
  - Research artifact persisted to filesystem (P-002)
due_date: null
activity: RESEARCH
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Research adversarial review strategies from industry practice and LLM/AI-specific sources: software engineering review patterns (Fagan, IEEE 1028), design critique methodologies, LLM-specific patterns (Self-Refine, Chain-of-Verification, CRITIC framework, Reflexion, Multi-agent Debate), and QA adversarial patterns. This is the second of three parallel research tasks feeding into the EN-301 synthesis.

### Acceptance Criteria

- [x] At least 8 strategies identified from industry and LLM sources (14 identified across 4 domains)
- [x] Each strategy has: name, origin/author, citation, description, mechanism, strengths, weaknesses
- [x] LLM-specific patterns (Self-Refine, CoV, CRITIC, Reflexion) covered with paper citations
- [x] L0/L1/L2 output levels present
- [x] Research artifact persisted to filesystem (P-002)

### Implementation Notes

Second of three parallel research tasks (with TASK-001 and TASK-003). Feeds into TASK-004 synthesis. Focus on practical industry adoption and LLM-native patterns. 14 strategies documented across SE, Design, LLM-Specific, and QA domains with 35 citations.

### Related Items

- Parent: [EN-301](../EN-301-deep-research-adversarial-strategies.md)
- Feeds into: [TASK-004](./TASK-004-synthesis-unified-catalog.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | -- |
| Remaining Work | -- |
| Time Spent | -- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Industry adversarial research | Research artifact | [TASK-002-industry-adversarial-research.md](../TASK-002-industry-adversarial-research.md) |

### Verification

- [x] Acceptance criteria verified
- [x] 14 strategies across 4 domains: SE, Design, LLM-Specific, QA
- [x] 35 citations provided
- [x] Reviewed by: ps-synthesizer (TASK-004)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
| 2026-02-12 | IN_PROGRESS | ps-researcher agent dispatched (opus model) |
| 2026-02-12 | DONE | Research complete. 14 strategies across 4 domains with 35 citations. 1,097 lines. |
