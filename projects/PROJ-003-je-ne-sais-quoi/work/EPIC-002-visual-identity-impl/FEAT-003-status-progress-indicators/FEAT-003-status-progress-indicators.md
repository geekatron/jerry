# FEAT-003: Status & Progress Indicators

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-20 (Claude)
PURPOSE: Unicode/ASCII status indicators, progress bars, spinners with graceful fallbacks
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

Implement the status indicators, progress bars, and spinner system defined in the design spec. Each visual element has a Unicode version for capable terminals and an ASCII fallback for CI/minimal environments.

**Value Proposition:**
- Consistent status indicators across all CLI output (`✓`/`[PASS]`, `✗`/`[FAIL]`, etc.)
- Progress bars for multi-step operations with number-first design (bar enhances, numbers inform)
- Four-character ASCII spinner for long-running operations
- Full graceful degradation matrix — every indicator works in every environment

---

## Acceptance Criteria

### Definition of Done

- [ ] Unicode status indicators implemented: `✓` (pass), `✗` (fail), `⚠` (warning), `ℹ` (info), `⛷` (celebration)
- [ ] ASCII fallbacks for each: `[PASS]`, `[FAIL]`, `[WARN]`, `[INFO]`, `*`
- [ ] Indicator selection uses rendering tier from FEAT-001
- [ ] Progress bar: `[████████....] 60% (6/10)` with `#` fallback for `█`
- [ ] Progress bar width fixed at 20 characters
- [ ] Spinner: `| / - \` at 100ms per frame
- [ ] Emoji rules enforced: max 1 `⛷` per message, celebrations only, never in errors
- [ ] `→` arrow with `->` fallback
- [ ] `•` bullet with `-` fallback
- [ ] Graceful degradation matrix matches design spec table

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | No Unicode Braille spinners — ASCII spinner only | [ ] |
| NFC-2 | Percentage and count always shown as numbers (bar is enhancement) | [ ] |
| NFC-3 | No emoji as punctuation | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Status indicators (`✓`/`✗`/`⚠` with ASCII fallbacks)
- Progress bar with percentage and count
- Graceful degradation based on FEAT-001 tier detection

### Out of Scope (Future)

- Animated spinner (requires async/threading considerations)
- Skier emoji `⛷` celebrations (deferred to FEAT-004 integration)
- Custom indicator configuration

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

- **Depends on:** FEAT-001 (rendering tier detection)
- **Blocks:** FEAT-004 (integration uses indicators in quality gates, session output)

### Design Spec References

| Section | Design Spec Location |
|---------|---------------------|
| Status indicators | `docs/design/saucer-boy-visual-identity.md` — [Iconography](#) |
| Emoji rules | `docs/design/saucer-boy-visual-identity.md` — [Emoji Rules](#) |
| Progress display | `docs/design/saucer-boy-visual-identity.md` — [Progress Indicators](#) |
| Fallback matrix | `docs/design/saucer-boy-visual-identity.md` — [Graceful Degradation Matrix](#) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. Status indicators and progress display with full graceful degradation. |

---

<!--
DESIGN RATIONALE:
This feature implements the Iconography section of the design spec. The key
principle is that Unicode/emoji indicators are enhancements — the text labels
([PASS], [FAIL]) carry the actual meaning. The progress bar follows the same
principle: numbers are the information, the bar is the visual enhancement.
-->
