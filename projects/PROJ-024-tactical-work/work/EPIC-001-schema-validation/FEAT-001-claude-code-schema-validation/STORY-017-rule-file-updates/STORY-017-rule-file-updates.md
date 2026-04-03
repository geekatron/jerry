# STORY-017: Implement P0 Rule File Changes for Tier Renumbering

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Update the two P0 governance files that define the tier model
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:** 2026-03-28T21:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Scope](#scope) | Exactly which files and sections |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist by skill |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework maintainer

**I want** the tier definitions in the governance rule files updated to reflect the new Persistent-First Linear model

**So that** the authoritative documentation matches the intended tier hierarchy and agent authors can select the correct tier for new agents

---

## Summary

Two P0 rule files define the tier model and must be updated before any governance YAML migration:

1. **`.context/rules/agent-development-standards.md`** (30 tier references) -- Rewrite the Tool Security Tiers section: tier table, selection guidelines, tier constraints, cognitive mode table, guardrail selection table.

2. **`.context/rules/mcp-tool-standards.md`** (1 direct tier reference + narrative text) -- Update MK namespace constraint wording, MCP-M-001 text, Agent Integration Matrix context, eng-*/red-* exclusion notes.

**Auto-escalation:** AE-002 applies (modifying `.context/rules/` files). Minimum C3; user has set C4.

**Skills informing this story:**
- `/eng-team` (eng-lead): Implementation standards, secure code review of rule file changes
- `/eng-team` (eng-security): Security review of tier model implications
- `/adversary` (adv-scorer): C4 quality gate per AE-002
- `/user-experience` (ux-heuristic-evaluator): Selection guideline clarity for agent authors

---

## Scope

### agent-development-standards.md Changes

| Section | Change | ADR Reference |
|---------|--------|---------------|
| Tool Security Tiers table | Replace 5-row table with new tier ordering (T3=Persistent, T4=External) | ADR "New tier table" |
| Selection Guidelines | Rewrite 5 guidelines (T1-T5) with risk-ordered rationale, Short Name/Full Name note | ADR "New selection guidelines" |
| Tier Constraints table | Update MK namespace rule from "T4+ agents" to "T3+ agents with Memory-Keeper" | ADR "New tier constraints" |
| Cognitive Mode table | Update tier references in Mode-to-Design Implications (T3+, T1, T2, T2/T3) | ADR scope verification |
| Guardrail Selection table | Update "Research (divergent, T3)" to "Research (divergent, T4)" etc. | ADR scope verification |
| L2-REINJECT comment | Update tier summary in HTML comment | Enforcement architecture |

### mcp-tool-standards.md Changes

| # | Change | ADR Reference |
|---|--------|---------------|
| 1 | Namespace constraint: "T4+ agents" → "T3+ agents with Memory-Keeper" | ADR mcp-tool-standards P0 Draft, Change 1 |
| 2 | MCP-M-001 text: add T4/T3 tier references | ADR Change 2 |
| 3 | Agent Integration Matrix: no row changes; footnote text update only | ADR Change 3 |
| 4 | Exclusion notes: add explicit "T4 permits MK ceiling but eng-*/red-* MUST NOT use" | ADR Change 4 |

---

## Acceptance Criteria

### /eng-team (eng-lead): Implementation Standards

- [ ] All tier references in agent-development-standards.md are updated (verified by `grep -n 'T[1-5]' .context/rules/agent-development-standards.md` producing only new-model references)
- [ ] All 4 mcp-tool-standards.md changes implemented per ADR P0 Draft
- [ ] L2-REINJECT HTML comment updated to reflect new tier ordering
- [ ] No orphaned references to old tier meanings (e.g., "T3 = External" in new file)
- [ ] Changes are atomic: both files updated in the same commit

### /eng-team (eng-security): Security Review

- [ ] New tier selection guidelines maintain principle of least privilege ("always select lowest tier")
- [ ] MK namespace constraint correctly applies to T3+ (not T2)
- [ ] H-35 compliance preserved (Agent tool at T5 only) in all updated text
- [ ] No new permission escalation paths created by the rewording

### /user-experience (ux-heuristic-evaluator): Selection Guideline Clarity

- [ ] Each tier's selection guideline answers "when do I choose this tier?" in one sentence
- [ ] The T3/T4 boundary is explicit: "If your agent also needs web tools, use T4"
- [ ] Short Name / Full Name convention documented with cross-reference to DX rationale
- [ ] Risk-ordering rationale included: "MK is less risky than web; T3 before T4 reflects this"

### /adversary (C4 quality gate)

- [ ] Updated rule files score >= 0.95 on S-014 rubric (C4 per AE-002)
- [ ] No critical findings in adversarial review
- [ ] Diff review confirms no unintended changes outside tier-related sections

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Rewrite agent-development-standards.md Tool Security Tiers section | pending | -- | /eng-team |
| TASK-002 | Update mcp-tool-standards.md (4 changes per ADR) | pending | -- | /eng-team |
| TASK-003 | Update L2-REINJECT HTML comment for new tier ordering | pending | -- | /eng-team |
| TASK-004 | DX review of updated selection guidelines | pending | -- | /user-experience |
| TASK-005 | C4 adversarial review of rule file changes | pending | -- | /adversary |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | STORY-016 | ADR must be finalized with all 5 options before rule files change |
| Blocks | STORY-018 | YAML migration depends on new tier definitions being in place |
| Blocks | STORY-019 | Documentation references new tier definitions |
| Blocks | STORY-020 | Security assessment reviews the implemented tier model |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- P0 rule file changes for Option A implementation |
| 2026-03-28 | claude | completed | Rule files updated: agent-development-standards.md v1.3.0, mcp-tool-standards.md v1.4.0, schema v1.1.0. Scored 0.954 (C4 PASS, 5 iterations). |
