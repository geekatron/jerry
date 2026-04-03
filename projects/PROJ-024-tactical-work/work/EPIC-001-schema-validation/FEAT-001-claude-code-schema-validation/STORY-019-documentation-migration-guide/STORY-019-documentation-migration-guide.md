# STORY-019: Tier Model Documentation and Migration Guide

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Update all documentation and create migration guide for agent authors
-->

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:** 2026-03-28T23:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Documentation Scope](#documentation-scope) | Files and documentation types needed |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist by skill |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As an** agent author creating or modifying agents in the Jerry Framework

**I want** clear documentation explaining the new tier model, how to select a tier, and what changed from the old model

**So that** I can correctly classify my agents without confusion about the renumbering

---

## Summary

The tier renumbering changes the meaning of T3 and T4. Existing documentation across SKILL.md files, AGENTS.md, and knowledge docs may reference old tier meanings. Additionally, agent authors need two new documents:

1. **Migration guide** (how-to): For authors of existing agents who need to understand the change
2. **Tier selection reference** (reference): Updated authoritative reference for new agent creation

**Skills informing this story:**
- `/diataxis` (diataxis-classifier, diataxis-howto, diataxis-reference): Classify documentation needs, produce how-to guide and reference doc
- `/user-experience` (ux-heuristic-evaluator): DX review of documentation clarity
- `/problem-solving` (ps-researcher): Sweep for all tier references that need updating

---

## Documentation Scope

### P1: Existing File Updates

| File Pattern | Expected Changes | Verification |
|-------------|-----------------|-------------|
| `skills/*/SKILL.md` | Tier references in agent descriptions (~5 UX SKILL.md files, verified) | `grep -rn 'T3\|T4' skills/*/SKILL.md` |
| `AGENTS.md` | Agent tier annotations (1 line, verified) | `grep -n 'T3\|T4' AGENTS.md` |
| `docs/design/ADR-PROJ007-001-agent-design.md` | **31 tier references** (verified) — agent design ADR with extensive tier content | `grep -c 'T[1-5]' docs/design/ADR-PROJ007-001-agent-design.md` |
| `docs/design/ADR-PROJ007-002-routing-triggers.md` | 3 tier references (verified) | `grep -c 'T[1-5]' docs/design/ADR-PROJ007-002-routing-triggers.md` |
| `docs/knowledge/*.md` | 0 matches (verified — no updates needed) | -- |
| `.context/rules/prompt-*.md` | 0 matches (verified — no updates needed) | -- |

### P1: New Documentation

| Document | Diataxis Quadrant | Purpose |
|----------|------------------|---------|
| Tier Migration Guide | **How-to** | Goal-oriented: "How to update your agent's tier after the renumbering." Includes glossary, rollback procedure, and troubleshooting section. |
| Tier Quick-Reference Card | **Reference** | 1-page facts-only lookup: tier name, tools per tier, example agents. No narrative, no teaching. |

> **Diataxis validation note (2026-03-28):** The originally proposed "Tier Selection Reference" was reclassified. Diataxis two-axis analysis showed it was Explanation (Theoretical + Acquisition), not Reference (Theoretical + Application). Since the existing Tier Model Options Explainer already covers the Explanation need, this deliverable was replaced with a genuine Reference artifact (Quick-Reference Card). See `research/validation-diataxis.md`.

---

## Acceptance Criteria

### /diataxis (documentation quality)

- [ ] Migration guide follows how-to format: goal statement, prerequisites, numbered steps, no explanation of why
- [ ] Migration guide includes glossary of tier terms (Short Name/Full Name, MK, tier ceiling)
- [ ] Migration guide includes rollback procedure for agent authors
- [ ] Migration guide includes troubleshooting section for common tier selection mistakes
- [ ] Quick-reference card follows reference format: facts-only table, neutral, no narrative
- [ ] No quadrant mixing: how-to doesn't explain theory; reference doesn't include tutorials
- [ ] Both documents pass diataxis-auditor quality check

### /user-experience (ux-heuristic-evaluator): Documentation DX

- [ ] Migration guide answers "what do I need to do?" in < 2 minutes of reading
- [ ] Tier selection reference provides a decision flowchart or decision table
- [ ] The T3/T4 swap is explained in one paragraph with a before/after comparison
- [ ] No Nielsen severity 3+ findings in documentation DX review
- [ ] Worked examples use real agents (not hypothetical) to illustrate tier selection

### /problem-solving (ps-researcher): Reference Sweep

- [ ] All tier references in `skills/*/SKILL.md` identified and updated
- [ ] All tier references in `AGENTS.md` identified and updated
- [ ] `docs/knowledge/`: confirmed zero tier matches (verified 2026-03-28) — no updates needed
- [ ] `.context/rules/prompt-*.md`: confirmed zero tier matches (verified 2026-03-28) — no updates needed
- [ ] Grep verification: no remaining references to "T3 (External)" or "T4 (Persistent)" with old meanings

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Sweep all files for stale tier references (grep audit) | pending | -- | /problem-solving |
| TASK-002 | Update SKILL.md files with tier reference changes | pending | -- | /eng-team |
| TASK-003 | Update AGENTS.md and other docs with tier references | pending | -- | /eng-team |
| TASK-004 | Write Tier Migration Guide with glossary, rollback, troubleshooting (diataxis how-to) | pending | -- | /diataxis |
| TASK-005 | Write Tier Quick-Reference Card (diataxis reference, 1-page facts-only) | pending | -- | /diataxis |
| TASK-006 | DX review of migration guide and selection reference | pending | -- | /user-experience |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | STORY-017 | Rule files define the canonical tier model that docs reference |
| Partial Depends On | STORY-018 | TASK-001 through TASK-003 (file updates) need STORY-018 complete. TASK-004 and TASK-005 (new docs) can start after STORY-017 alone — content is known from ADR. |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- documentation and DX work for tier renumbering |
| 2026-03-28 | claude | completed | 38 tier ref updates across 10 SKILL.md + AGENTS.md. 2 ADR deprecation notices. Migration guide + quick-reference card created. Explainer updated. |
