# EPIC-003: Voice Architecture

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
CREATED: 2026-02-20 (Claude)
PURPOSE: Split voice into internal framework voice + user-invocable session conversational voice
-->

> **Type:** epic
> **Status:** in-progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** PROJ-003-je-ne-sais-quoi
> **Owner:** --
> **Target Quarter:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this epic is about |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Why voice architecture matters |
| [Children (Features)](#children-features) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Change log |

---

## Summary

EPIC-001 produced a single `/saucer-boy` skill that handles framework output voice (quality gate messages, error messages, CLI personality). This epic splits voice into two distinct concerns:

1. **Framework Output Voice** (internal) — The existing `/saucer-boy` skill refactored into `/saucer-boy-framework-voice`, an internal-only skill that Claude Code loads automatically when producing framework output. Not user-invocable.

2. **Session Conversational Voice** (user-facing) — A new user-invocable `/saucer-boy` skill that gives Claude Code the McConkey personality during work sessions. Makes working with Jerry fun. Can be explicitly invoked to get responses in McConkey's voice.

**Key Objectives:**
- Separate framework output voice (deterministic, internal) from session conversational voice (interactive, user-facing)
- Rename existing skill to reflect its internal role
- Create a new conversational skill that brings Saucer Boy energy to the working session itself
- Ensure the conversational voice knows when to be fun and when to be precise

---

## Business Outcome Hypothesis

**We believe that** splitting voice into an internal framework voice and a user-invocable conversational voice

**Will result in** a working experience where Jerry is both technically rigorous in its output AND genuinely fun to work with — the McConkey principle applied to the developer relationship, not just the CLI messages

**We will know we have succeeded when** developers invoke `/saucer-boy` to get McConkey-style commentary, enjoy the session personality, and describe working with Jerry as fun alongside rigorous

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Dependencies | Progress |
|----|-------|--------|----------|--------------|----------|
| [FEAT-001](./FEAT-001-framework-voice-internal-skill/FEAT-001-framework-voice-internal-skill.md) | Framework Voice Internal Skill Refactor | done | high | -- | 100% |
| [FEAT-002](./FEAT-002-session-conversational-voice/FEAT-002-session-conversational-voice.md) | Session Conversational Voice | in-progress | high | FEAT-001 | 0% |

### Feature Links

- [FEAT-001: Framework Voice Internal Skill Refactor](./FEAT-001-framework-voice-internal-skill/FEAT-001-framework-voice-internal-skill.md) — Rename existing `skills/saucer-boy/` to `skills/saucer-boy-framework-voice/`. Remove from user-invocable skills list. Configure as internal auto-loaded skill for framework output (quality gates, errors, session hooks). Update all references in CLAUDE.md, AGENTS.md, and skill cross-references.
- [FEAT-002: Session Conversational Voice](./FEAT-002-session-conversational-voice/FEAT-002-session-conversational-voice.md) — New user-invocable `/saucer-boy` skill for session conversational personality. Defines how Claude Code talks during work sessions with McConkey energy. Includes explicit invocation mode for on-demand McConkey responses. Boundaries for when personality is appropriate vs when precision takes over.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [##########..........] 50% (1/2 complete)              |
+------------------------------------------------------------------+
| Overall:   [##########..........] 50%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 2 |
| **Completed Features** | 1 |
| **In Progress Features** | 1 |
| **Pending Features** | 0 |
| **Feature Completion %** | 50% |

---

## Related Items

### Hierarchy

- **Parent Project:** [PROJ-003: Je Ne Sais Quoi](../../WORKTRACKER.md)

### Related Epics

- [EPIC-001: Je Ne Sais Quoi — The Saucer Boy Spirit](../EPIC-001-je-ne-sais-quoi/EPIC-001-je-ne-sais-quoi.md) — Produced the original `/saucer-boy` skill and persona doc that this epic refactors
- [EPIC-002: Visual Identity Implementation](../EPIC-002-visual-identity-impl/EPIC-002-visual-identity-impl.md) — Visual identity pairs with voice; EPIC-002 FEAT-004 integration may consume framework voice

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EPIC-001 FEAT-001 | Saucer Boy persona doc (`docs/knowledge/saucer-boy-persona.md`) |
| Depends On | EPIC-001 FEAT-002 | Existing `/saucer-boy` skill (`skills/saucer-boy/`) |

### Key Artifacts

| Artifact | Purpose | Path |
|----------|---------|------|
| Framework voice skill (refactored) | Internal framework output voice | `skills/saucer-boy-framework-voice/` |
| Persona doc | Source personality for conversational voice | `docs/knowledge/saucer-boy-persona.md` |
| Voice guide reference | Framework voice patterns | `skills/saucer-boy-framework-voice/references/voice-guide.md` |
| Tone spectrum examples | Voice calibration reference | `skills/saucer-boy-framework-voice/references/tone-spectrum-examples.md` |
| Audience adaptation | Context-aware voice rules | `skills/saucer-boy-framework-voice/references/audience-adaptation.md` |
| Boundary conditions | When NOT to use personality | `skills/saucer-boy-framework-voice/references/boundary-conditions.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Epic created. Splits voice into internal framework voice (refactor of existing `/saucer-boy`) and user-invocable session conversational voice (new `/saucer-boy` skill). 2 features. |
| 2026-02-20 | Claude | in-progress | FEAT-001 complete: renamed `skills/saucer-boy/` to `skills/saucer-boy-framework-voice/`, updated all references in CLAUDE.md, AGENTS.md, mandatory-skill-usage.md, skill-standards.md, and agent files. |

---

<!--
DESIGN RATIONALE:
The original /saucer-boy skill serves double duty: it gates framework output
voice quality AND provides persona enforcement. These are two different concerns:

1. Framework voice is deterministic — quality gates, error messages, hook output.
   This should be internal, auto-loaded, invisible to the user.

2. Session conversational voice is interactive — how Claude Code talks during
   work. This should be user-invocable, fun, and have McConkey personality.

Splitting them allows the framework voice to be always-on without requiring
user invocation, while the conversational voice can be invoked explicitly
for on-demand McConkey energy.
-->
