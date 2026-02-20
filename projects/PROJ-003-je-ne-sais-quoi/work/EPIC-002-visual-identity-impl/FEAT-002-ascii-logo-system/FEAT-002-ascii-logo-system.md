# FEAT-002: ASCII Logo System

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-20 (Claude)
PURPOSE: Logo selection, rendering, and integration into CLI commands
-->

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
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

Implement the ASCII logo system defined in the design spec. Three logo options are proposed (The Peak, The Ridgeline, The Drop-In) — a user decision is required to select the final logo. Each logo has compact (3-4 line) and full (8-10 line) variants for different contexts.

**Value Proposition:**
- Visual identity for Jerry in the terminal — first impression at session start
- Context-appropriate rendering (compact for headers, full for splash/version)
- Pure ASCII characters — works everywhere without Unicode dependencies

### Open Decision

**Logo selection required.** The design spec proposes three options:

| Option | Name | Style |
|--------|------|-------|
| A | The Peak | Mountain/peak motif, clean geometry |
| B | The Ridgeline | Twin peaks, wider profile |
| C | The Drop-In | Box-framed, compact |

Recommendation from design spec: **Option A** for most contexts.

---

## Acceptance Criteria

### Definition of Done

- [ ] Logo option selected (user decision)
- [ ] Compact variant renders correctly at session start
- [ ] Full variant renders correctly for `jerry --version`
- [ ] Logo respects terminal width (80-column minimum compatibility)
- [ ] Tagline "Quality with soul." included in full variant
- [ ] Logo suppressed in `NO_COLOR`/Minimal tier (or rendered without any ANSI codes)
- [ ] No logo in error states (per design spec: "Logo is for positive moments, not interruptions")

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | ASCII characters only in logo (no Unicode box-drawing) | [ ] |
| NFC-2 | Compact variant fits in 4 lines or fewer | [ ] |
| NFC-3 | Full variant fits in 10 lines or fewer | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Selected logo in compact variant at session start
- Full variant for `jerry --version`
- Plain ASCII rendering (no color in logo itself)

### Out of Scope (Future)

- Animated logo rendering
- Color-enhanced logo variants
- Custom user logos

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

- **Depends on:** FEAT-001 (rendering engine for tier-aware output)
- **Blocks:** FEAT-004 (integration uses logo in session start, version)

### Design Spec References

| Section | Design Spec Location |
|---------|---------------------|
| Logo options | `docs/design/saucer-boy-visual-identity.md` — [ASCII Art Logo](#) |
| Selection guidance | `docs/design/saucer-boy-visual-identity.md` — [Logo Selection Guidance](#) |
| Implementation notes | `docs/design/saucer-boy-visual-identity.md` — [Logo Implementation Notes](#) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. Requires user decision on logo selection (Option A/B/C) before implementation can begin. |

---

<!--
DESIGN RATIONALE:
The logo is the most visible piece of the visual identity. It appears at session
start and in --version output. The design spec provides three options — a human
decision is needed to pick one. Implementation is straightforward once the
choice is made: pure ASCII string rendering with context-aware variant selection.
-->
