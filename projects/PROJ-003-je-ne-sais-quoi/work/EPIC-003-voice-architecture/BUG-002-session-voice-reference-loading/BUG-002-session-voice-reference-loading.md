# BUG-002: Session Voice Skill Loads Rules Without Examples — Voice Quality Degrades

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-20 (Claude)
PURPOSE: Document reference loading architecture failure in session voice skill
-->

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-003
> **Owner:** --
> **Found In:** 1.0.0
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What the bug is |
| [Steps to Reproduce](#steps-to-reproduce) | How to reproduce |
| [Environment](#environment) | Where it occurs |
| [Root Cause Analysis](#root-cause-analysis) | Why it happens |
| [Acceptance Criteria](#acceptance-criteria) | When it's fixed |
| [Children (Tasks / Decisions)](#children-tasks-decisions) | Tasks and decisions |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Summary

When `/saucer-boy` is invoked, the Skill tool loads the full SKILL.md (~300 lines of rules, compliance tables, boundary conditions, anti-patterns, integration points) into the main context. However, none of the 10 reference files (~43KB of calibration material) are loaded. The main context receives a compliance manual for the voice but never sees the voice itself — no before/after pairs, no biographical anchors, no humor examples, no vocabulary reference. The result is rule-following behavior instead of personality embodiment, producing measurably worse conversational output than when the main context operates from internalized persona knowledge without the skill loaded.

**Key Details:**
- **Symptom:** Responses with `/saucer-boy` loaded are more cautious, less direct, and offer menus of options instead of confident single responses. Quality degrades compared to pre-skill persona invocation.
- **Frequency:** Every `/saucer-boy` invocation via main context
- **Workaround:** Don't load the skill. Ask for "Saucer Boy energy" without `/saucer-boy` invocation, relying on internalized persona knowledge from session context.

---

## Steps to Reproduce

### Prerequisites

- Jerry Framework session active with PROJ-003
- `/saucer-boy` skill available in skills registry

### Steps to Reproduce

1. Start a session where the main context has absorbed persona context through working on voice-related tasks (e.g., building the skill, reviewing persona doc)
2. Ask for "Saucer Boy energy on [topic]" WITHOUT invoking `/saucer-boy` — observe confident, direct, personality-rich response
3. Invoke `/saucer-boy` via the skill system, loading the full SKILL.md
4. Ask for the same kind of Saucer Boy response — observe more cautious, rule-aware, compliance-mode response
5. Compare: the pre-skill response embodies the voice; the post-skill response follows rules about the voice

### Expected Result

Loading `/saucer-boy` should produce equal or better voice quality than unstructured persona invocation. The skill should enhance the voice, not constrain it.

### Actual Result

Loading `/saucer-boy` degrades voice quality. The main context shifts from embodying the personality to following compliance rules about the personality. Boundary #8 (NOT Mechanical Assembly) is triggered — the output passes checklists but reads as assembled, not written from conviction.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Skill Version** | saucer-boy v1.0.0 |
| **Agent Model** | Claude Opus 4.6 (main context) |
| **Invocation Method** | `/jerry:saucer-boy` Skill tool |
| **Reference Files** | 10 files, ~43KB total in `skills/saucer-boy-framework-voice/references/` |
| **SKILL.md Size** | ~300 lines loaded into main context |

---

## Root Cause Analysis

### Investigation Summary

The root cause is an architectural mismatch between the skill design (optimized for subagent invocation) and the actual usage pattern (main context skill loading).

### Root Cause

**Three compounding failures:**

1. **SKILL.md is all rules, no examples.** The SKILL.md contains voice traits as definitions, boundary conditions as tables, anti-patterns as prohibitions — but zero examples of the voice in action. The 9 before/after calibration pairs in `voice-guide.md` that demonstrate the voice are classified as "on-demand references" and never load. Rules tell you what to avoid; examples teach you what to do. For a voice skill, examples ARE the instruction.

2. **Reference loading is designed for subagent, not main context.** The sb-voice agent definition specifies `reference_loading` with on-demand files. When sb-voice runs as a Task tool subagent, it reads its agent definition and loads references. But when `/saucer-boy` loads via the Skill tool, only the SKILL.md enters context — the agent never runs, so references never load. The 43KB of calibration material sits on disk unused.

3. **No routing instruction for explicit vs. ambient invocation.** The SKILL.md doesn't tell the main context: "For explicit `/saucer-boy` invocations, spawn sb-voice via Task tool so references load. For ambient mode, use lightweight persona prompt." The main context treats the loaded SKILL.md as its own operating instructions, which overwrites internalized persona knowledge with rule-following behavior.

### Contributing Factors

- The skill was designed and adversary-reviewed as a *spec for agents*, not as a *prompt for main context*
- The Skill tool loading mechanism only loads SKILL.md — no mechanism for auto-including referenced files
- The `@rules/` import pattern used in worktracker SKILL.md (which auto-loads rule files) was not applied to reference files in the saucer-boy skill
- The ambient mode implementation note acknowledges the main-context responsibility but provides no lightweight persona content

---

## Acceptance Criteria

### Fix Verification

- [ ] Main-context `/saucer-boy` invocation produces voice quality equal to or better than unstructured persona invocation
- [ ] Key voice-guide before/after pairs are available in context when skill loads
- [ ] Biographical anchors are available for McConkey plausibility calibration
- [ ] Explicit invocations route to sb-voice subagent with full reference loading
- [ ] Ambient mode has a lightweight persona prompt (not the full compliance apparatus)
- [ ] Skill loading does not exceed 500 additional tokens for ambient mode (NFC-3 compliance)

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] SKILL.md structural standards (H-25 through H-30) maintained

---

## Children (Tasks / Decisions)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| [TASK-001](./TASK-001-ab-test-voice-configuration/TASK-001-ab-test-voice-configuration.md) | A/B Test Voice Configuration Matrix | done | 2 |
| [DEC-001](./DEC-001-voice-configuration/DEC-001-voice-configuration.md) | Voice Configuration — opus + all 10 refs | accepted | -- |

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-003: Voice Architecture](../EPIC-003-voice-architecture.md)

### Related Items

- **Related Feature:** [FEAT-002: Session Conversational Voice](../FEAT-002-session-conversational-voice/FEAT-002-session-conversational-voice.md)
- **Related Enabler:** [EN-001: Session Voice Reference Architecture Fix](../EN-001-session-voice-reference-architecture/EN-001-session-voice-reference-architecture.md) (architecture fix — complete)
- **Related Skill:** `skills/saucer-boy/SKILL.md` (primary affected file)
- **Related References:** `skills/saucer-boy-framework-voice/references/` (10 files, never loaded)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Bug filed. Root cause: SKILL.md loads rules without examples; 43KB of calibration references never reach main context; no routing for explicit vs. ambient invocation patterns. |

---
