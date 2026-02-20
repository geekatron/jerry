# FEAT-004: Visual Identity Integration

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-20 (Claude)
PURPOSE: Apply visual identity system to all existing CLI output
-->

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-002
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children](#children) | Enablers (to be decomposed when work starts) |
| [Progress Summary](#progress-summary) | Feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Change log |

---

## Summary

Apply the rendering engine (FEAT-001), logo system (FEAT-002), and status indicators (FEAT-003) across all existing Jerry CLI output. This is the integration feature that connects the visual infrastructure to the actual user-facing commands.

**Value Proposition:**
- Quality gate messages with colored state, bold scores, and dim dimension detail
- Session start with compact logo, session end with celebration tiers (Powder Day/Clean Run/Nod)
- Error messages with appropriate visual restraint (no decoration, just clarity)
- Visual energy proportional to the moment (Visual Tone Spectrum)

---

## Acceptance Criteria

### Definition of Done

- [ ] Quality gate PASS: green state + bold score + optional dimension breakdown
- [ ] Quality gate FAIL (REVISE): yellow state + bold score + dim dimension detail
- [ ] Quality gate FAIL (REJECTED): red state + bold score + priority-ordered action path
- [ ] Constitutional failure: red "Hard stop" + trigger + escalation level + no decoration
- [ ] Session start: compact logo + default color
- [ ] Session complete (all items): Celebration Tier 1 — box-art + `⛷` + tagline
- [ ] Session complete (partial): Tier 3 — plain text acknowledgment
- [ ] Error messages: no emoji, no decoration, precision only
- [ ] Maximum 2 colors per message enforced
- [ ] Line length <= 78 characters enforced
- [ ] All output fully readable in Minimal tier (no ANSI, no Unicode)
- [ ] Tested in both light and dark terminal themes

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | No visual regression in existing CLI behavior | [ ] |
| NFC-2 | CI log output remains clean (no ANSI artifacts) | [ ] |
| NFC-3 | Backward compatible — existing scripts parsing CLI output not broken | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Quality gate message formatting (PASS/REVISE/REJECTED)
- Session start with logo
- Basic celebration (session complete with all items)
- Error message visual restraint

### Out of Scope (Future)

- Streak detection and streak-specific visuals
- First-ever quality gate pass detection
- Temporal easter egg integration with visual system
- Onboarding/welcome flow visual treatment

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
| Enablers:  [....................] 0% (0/0)                        |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-002: Visual Identity Implementation](../EPIC-002-visual-identity-impl.md)

### Dependencies

- **Depends on:** FEAT-001 (rendering engine), FEAT-002 (logo), FEAT-003 (indicators)
- **Blocks:** --

### Design Spec References

| Section | Design Spec Location |
|---------|---------------------|
| Tone spectrum | `docs/design/saucer-boy-visual-identity.md` — [Visual Tone Spectrum](#) |
| Celebration tiers | `docs/design/saucer-boy-visual-identity.md` — [Celebration Tiers](#) |
| Diagnostic tiers | `docs/design/saucer-boy-visual-identity.md` — [Diagnostic Tiers](#) |
| Brand guidelines | `docs/design/saucer-boy-visual-identity.md` — [Brand Guidelines Summary](#) |
| Anti-patterns | `docs/design/saucer-boy-visual-identity.md` — [Anti-Patterns](#) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. Fan-in integration feature — depends on all 3 preceding features. Applies visual system to quality gates, sessions, errors, celebrations. |

---

<!--
DESIGN RATIONALE:
This is the fan-in feature that connects all the infrastructure to the actual
user experience. It implements the Visual Tone Spectrum — the mapping from
context (celebration, routine, failure, hard stop) to visual treatment
(box-art, clean text, color signals, plain text).

The celebration tiers (Powder Day, Clean Run, Nod) are the most visible
expression of the Saucer Boy spirit in the CLI.
-->
