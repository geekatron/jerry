# FEAT-001: Framework Voice Internal Skill Refactor

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-20 (Claude)
PURPOSE: Rename and refactor existing /saucer-boy skill to internal framework voice
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-003
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Scope of Changes](#scope-of-changes) | What gets renamed, moved, and updated |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children](#children) | Enablers (to be decomposed when work starts) |
| [Progress Summary](#progress-summary) | Feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Change log |

---

## Summary

Refactor the existing `/saucer-boy` skill into `/saucer-boy-framework-voice` — an internal-only skill that Claude Code loads automatically when producing framework output. This skill is NOT user-invocable; it governs how quality gate messages, error messages, session hooks, and other framework output maintain the Saucer Boy voice.

**Value Proposition:**
- Clears the `/saucer-boy` namespace for the new conversational voice skill
- Makes framework voice always-on without requiring user invocation
- Preserves all existing voice quality enforcement (sb-reviewer, sb-rewriter, sb-calibrator agents)
- Clean separation of concerns: framework output vs session conversation

---

## Scope of Changes

### Rename Operations

| From | To |
|------|----|
| `skills/saucer-boy/` | `skills/saucer-boy-framework-voice/` |
| `skills/saucer-boy/SKILL.md` | `skills/saucer-boy-framework-voice/SKILL.md` |
| `skills/saucer-boy/agents/` | `skills/saucer-boy-framework-voice/agents/` |
| `skills/saucer-boy/references/` | `skills/saucer-boy-framework-voice/references/` |
| `skills/saucer-boy/assets/` | `skills/saucer-boy-framework-voice/assets/` |

### Reference Updates

| File | Change |
|------|--------|
| `CLAUDE.md` | Remove `/saucer-boy` from user-invocable skills table |
| `AGENTS.md` | Rename "Saucer Boy Skill Agents" section, update paths to `saucer-boy-framework-voice` |
| `SKILL.md` (internal) | Update skill name, mark as internal (not user-invocable), update agent paths |
| `.context/rules/mandatory-skill-usage.md` | Add trigger for auto-loading framework voice on output generation |
| Cross-references in worktracker | Update any paths referencing `skills/saucer-boy/` |

### SKILL.md Updates

| Change | Detail |
|--------|--------|
| Skill name | `saucer-boy` → `saucer-boy-framework-voice` |
| Invocation | Remove from user-invocable list; add auto-load trigger |
| Purpose | Narrow to framework output voice only (not conversational) |
| Agent paths | Update all `skills/saucer-boy/agents/` → `skills/saucer-boy-framework-voice/agents/` |

---

## Acceptance Criteria

### Definition of Done

- [x] `skills/saucer-boy/` renamed to `skills/saucer-boy-framework-voice/` via `git mv`
- [x] SKILL.md updated: name, purpose narrowed to framework output, marked as internal
- [x] `/saucer-boy` removed from user-invocable skills in CLAUDE.md
- [x] AGENTS.md updated with new paths and section name
- [x] `mandatory-skill-usage.md` updated with auto-load trigger for framework output
- [x] All agent files (sb-reviewer, sb-rewriter, sb-calibrator) updated with new paths
- [x] All cross-references in worktracker docs updated
- [x] No broken links remain referencing old `skills/saucer-boy/` path
- [x] Existing tests still pass (voice enforcement unchanged, just renamed)

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Git history preserved via `git mv` (not delete + create) | [x] |
| NFC-2 | No functional changes to agents — rename only | [x] |
| NFC-3 | Framework voice behavior unchanged after rename | [x] |

---

## Children

> Enablers and tasks will be decomposed when implementation begins.

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| -- | -- | -- | -- | -- |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [####################] 100% (all complete)             |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-003: Voice Architecture](../EPIC-003-voice-architecture.md)

### Dependencies

- **Depends on:** --
- **Blocks:** FEAT-002 (conversational voice needs `/saucer-boy` namespace freed)

### Current Skill Inventory

| File | Purpose | Action |
|------|---------|--------|
| `skills/saucer-boy/SKILL.md` | Skill definition (26KB) | Rename + update |
| `skills/saucer-boy/agents/sb-reviewer.md` | Voice compliance review | Rename path |
| `skills/saucer-boy/agents/sb-rewriter.md` | Voice transformation | Rename path |
| `skills/saucer-boy/agents/sb-calibrator.md` | Voice fidelity scoring | Rename path |
| `skills/saucer-boy/references/` (10 files) | Voice guide, examples, boundaries | Rename path |
| `skills/saucer-boy/assets/` | Visual assets | Rename path |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. Refactors existing `/saucer-boy` to internal `/saucer-boy-framework-voice`. Rename + reference updates only — no functional changes to voice enforcement. |
| 2026-02-20 | Claude | done | Implemented: git mv, SKILL.md updated (name, version 1.1.0, internal marker), all 3 agent identities updated, CLAUDE.md/AGENTS.md/mandatory-skill-usage.md/skill-standards.md references updated, EPIC-003 and FEAT-001 worktracker docs updated. All tests pass. |

---

<!--
DESIGN RATIONALE:
The existing /saucer-boy skill was built for framework output voice enforcement.
It should remain exactly as it is functionally — only the name and invocation
model change. It becomes internal (auto-loaded for framework output) rather
than user-invocable, freeing the /saucer-boy namespace for the conversational
voice skill.

Git mv preserves history. No functional changes means no risk to existing
voice quality gates.
-->
