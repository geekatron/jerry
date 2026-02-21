# EN-006: Ambiguity Clarification Rule (H-31)

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-21
> **Completed:** 2026-02-21
> **Parent:** EPIC-001-oss-release
> **Owner:** Claude
> **Effort:** 3

---

## Summary

Add H-31 "Clarify Before Acting When Ambiguous" as a HARD rule to the quality enforcement framework. When requirements have multiple valid interpretations, unclear scope, or imply destructive action, Claude MUST ask clarifying questions before proceeding. Reconcile TOOL_REGISTRY.yaml AskUserQuestion constraints which previously discouraged clarification.

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | H-31 added to HARD Rule Index in `quality-enforcement.md` | PASS |
| AC-2 | H-31 added to Quality Gate Rule Definitions with rationale | PASS |
| AC-3 | L2-REINJECT marker added at rank=2 for context-rot immunity | PASS |
| AC-4 | Nav table updated (H-01 through H-31) | PASS |
| AC-5 | Tier Vocabulary HARD max count updated (<= 35) | PASS |
| AC-6 | TOOL_REGISTRY.yaml AskUserQuestion constraints reconciled with H-31 | PASS |
| AC-7 | CLAUDE.md Critical Constraints table includes H-31 | PASS |
| AC-8 | All existing tests pass (no regressions) | PASS |

## Evidence

- **Files modified:** `quality-enforcement.md` (5 edits), `TOOL_REGISTRY.yaml` (1 edit), `CLAUDE.md` (1 edit)
- **L2-REINJECT:** rank=2, tokens=50 (~242 total vs 600 budget)
- **Test results:** All enforcement, hook integration, and quality framework e2e tests pass

## History

| Date | Author | Event |
|------|--------|-------|
| 2026-02-21 | Claude | Created. H-31 added to quality-enforcement.md (L2 marker, HARD Rule Index, Quality Gate Rule Definitions, nav table, tier vocabulary). TOOL_REGISTRY.yaml AskUserQuestion constraints reconciled. CLAUDE.md updated. |
