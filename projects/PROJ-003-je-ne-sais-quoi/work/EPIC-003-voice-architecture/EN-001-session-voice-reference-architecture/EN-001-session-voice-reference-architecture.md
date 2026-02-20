# EN-001: Session Voice Reference Architecture Fix

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-20 (Claude)
PURPOSE: Fix session voice skill so references load and voice quality matches internalized persona
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-003
> **Owner:** --
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this is needed |
| [Business Value](#business-value) | What it unlocks |
| [Technical Approach](#technical-approach) | How to fix it |
| [Children (Tasks)](#children-tasks) | Decomposed work |
| [Progress Summary](#progress-summary) | Overall progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks |
| [Dependencies](#dependencies) | What this depends on and enables |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Summary

Fix the session voice skill's reference architecture so that voice calibration material (before/after pairs, biographical anchors, humor examples) actually reaches the context where voice generation happens. Currently, `/saucer-boy` loads 300 lines of compliance rules but 0 lines of voice examples, producing rule-following behavior instead of personality embodiment.

**Technical Scope:**
- Embed key voice-guide pairs directly in SKILL.md for main-context use
- Create lightweight ambient persona prompt for main-context personality mode
- Add explicit routing: main-context ambient vs. sb-voice subagent for explicit invocations
- Update sb-voice agent to always-load critical reference files
- Investigate `@` import pattern for auto-loading references (as worktracker skill does with `@rules/`)

---

## Problem Statement

The session voice skill was designed and reviewed as a spec for the sb-voice subagent, but the actual usage pattern is main-context skill loading via the Skill tool. This mismatch means:

1. The main context gets rules about the voice but never sees examples of the voice
2. 43KB of reference material (voice-guide pairs, biographical anchors, humor examples) sits unused on disk
3. The main context shifts from personality embodiment to compliance mode when the skill loads
4. There's no routing logic to distinguish ambient (lightweight) from explicit (full subagent) invocation

See [BUG-002](../BUG-002-session-voice-reference-loading/BUG-002-session-voice-reference-loading.md) for detailed root cause analysis.

---

## Business Value

Voice quality is the entire value proposition of the `/saucer-boy` skill. If loading the skill makes the voice worse, the skill has negative value. Fixing the reference architecture turns the skill from a compliance burden into a voice amplifier.

### Features Unlocked

- Main-context `/saucer-boy` produces voice quality matching or exceeding unstructured persona invocation
- Ambient mode works with minimal token cost (~100-150 lines instead of ~300)
- Explicit invocations get full reference loading via sb-voice subagent
- Future skills can follow the same pattern for reference-rich skill loading

---

## Technical Approach

### Architecture: Dual-Mode Loading

```
/saucer-boy invocation
        |
        v
  +------------------+
  | SKILL.md loads   |
  | (with embedded   |
  |  voice examples) |
  +------------------+
        |
   +----+----+
   |         |
   v         v
AMBIENT    EXPLICIT
MODE       MODE
   |         |
   v         v
Main ctx   Task(sb-voice)
uses       subagent reads
embedded   agent def +
examples   loads ALL refs
+ ambient  (voice-guide,
prompt     bio-anchors,
(~150      humor, vocab)
lines)     (~full 43KB)
```

### Key Changes

1. **SKILL.md gains embedded examples** — Move 3-4 best voice-guide pairs into the SKILL.md body (Voice Traits or new "Voice in Action" section). These load automatically when the skill activates.

2. **New ambient persona prompt** — Create `skills/saucer-boy/references/ambient-persona.md` (~100-150 lines): core thesis, 3 biographical anchors, 3-4 voice-guide pairs, 3 key anti-patterns, boundary conditions summary. Optimized for main-context personality, not subagent instruction.

3. **SKILL.md routing instructions** — Add explicit instructions: "For ambient session personality, the main context uses the embedded examples and ambient prompt. For explicit McConkey invocations (pep talks, roasts, deep persona), spawn sb-voice via Task tool for full reference loading."

4. **sb-voice always-load references** — Change sb-voice agent's reference_loading from all-on-demand to always-load `voice-guide.md` + `biographical-anchors.md` (matching sb-rewriter's pattern).

5. **Investigate `@` import for references** — The worktracker SKILL.md uses `@rules/worktracker-behavior-rules.md` to auto-load rule files. Investigate whether this `@` import pattern can be used in SKILL.md to auto-include reference content when the skill loads.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](#task-001) | Embed voice-guide pairs in SKILL.md | pending | 1 | -- |
| [TASK-002](#task-002) | Create ambient persona prompt | pending | 2 | -- |
| [TASK-003](#task-003) | Add dual-mode routing instructions to SKILL.md | pending | 1 | -- |
| [TASK-004](#task-004) | Update sb-voice always-load references | pending | 1 | -- |
| [TASK-005](#task-005) | Investigate `@` import pattern for reference auto-loading | pending | 1 | -- |
| [TASK-006](#task-006) | Validate fix with comparative voice quality test | pending | 1 | -- |

### TASK-001: Embed voice-guide pairs in SKILL.md

**Description:** Select 3-4 of the strongest before/after pairs from `skills/saucer-boy-framework-voice/references/voice-guide.md` and embed them directly in the session voice SKILL.md. Add a new "Voice in Action" section or integrate into Voice Traits. These pairs demonstrate the voice rather than describing it — they're the single highest-value calibration material.

**Candidate pairs:**
- Pair 1 (Quality Gate PASS) — celebration context, shows full energy
- Pair 2 (Quality Gate FAIL REVISE) — encouragement context, shows calibrated warmth
- Pair 5 (Session Start) — presence context, shows routine warmth
- Pair 7 (Celebration) — full energy context, shows powder day energy

**Acceptance Criteria:**
- [ ] 3-4 voice-guide pairs embedded in SKILL.md body
- [ ] Pairs demonstrate the full tone spectrum range
- [ ] Technical information preserved in all pairs
- [ ] SKILL.md still meets H-28 description length limit
- [ ] Navigation table updated

---

### TASK-002: Create ambient persona prompt

**Description:** Create `skills/saucer-boy/references/ambient-persona.md` — a lightweight prompt (~100-150 lines) optimized for main-context personality embodiment. Content: core thesis (verbatim), 3 biographical anchors (banana suit, Spatula invention, "float like a boat"), 3-4 voice-guide pairs (embedded from TASK-001), 3 key anti-patterns (sycophancy, information displacement, under-expression), boundary conditions summary (hard gates only). NO compliance tables, NO integration points, NO P-003 diagrams, NO registration details.

**Design principle:** This file is what the main context needs to *be* the voice, not what a subagent needs to *follow rules about* the voice.

**Acceptance Criteria:**
- [ ] File exists at `skills/saucer-boy/references/ambient-persona.md`
- [ ] Under 150 lines
- [ ] Contains core thesis, biographical anchors, voice-guide pairs, anti-patterns, boundary conditions
- [ ] Does NOT contain compliance tables, integration points, or agent invocation patterns
- [ ] Reads as a personality prompt, not a specification
- [ ] Token budget under 500 tokens (NFC-3 compliance)

---

### TASK-003: Add dual-mode routing instructions to SKILL.md

**Description:** Add explicit routing instructions to the session voice SKILL.md that tell the main context how to handle different invocation patterns:

- **Ambient mode:** Main context reads `skills/saucer-boy/references/ambient-persona.md` and embodies the voice directly. No subagent needed. Used for routine session personality.
- **Explicit invocation mode:** Main context spawns sb-voice via Task tool for deep McConkey channeling (pep talks, roasts, "what would McConkey say" requests). Subagent loads full reference set.

Add this as a new section or integrate into "Invoking an Agent" section.

**Acceptance Criteria:**
- [ ] SKILL.md contains explicit routing instructions for ambient vs. explicit mode
- [ ] Ambient mode points to ambient-persona.md
- [ ] Explicit mode shows Task tool invocation with sb-voice
- [ ] Decision criteria documented (when to use which mode)
- [ ] Navigation table updated

---

### TASK-004: Update sb-voice always-load references

**Description:** Change sb-voice agent's `reference_loading` section to always-load `voice-guide.md` and `biographical-anchors.md` (currently all on-demand). This matches the pattern used by sb-rewriter, which always-loads `voice-guide.md` and `vocabulary-reference.md`. When sb-voice is invoked as a subagent, it should have calibration material immediately available without on-demand decisions.

**Acceptance Criteria:**
- [ ] `skills/saucer-boy/agents/sb-voice.md` reference_loading updated
- [ ] `voice-guide.md` listed as always-load
- [ ] `biographical-anchors.md` listed as always-load
- [ ] Remaining references stay on-demand
- [ ] Agent definition still meets skill-standards requirements

---

### TASK-005: Investigate `@` import pattern for reference auto-loading

**Description:** The worktracker SKILL.md uses `@rules/worktracker-behavior-rules.md` syntax to auto-load rule files when the skill is invoked. Investigate whether this `@` import pattern:

1. Is a Claude Code Skill tool feature or a Jerry convention
2. Can be used in SKILL.md to auto-include reference files
3. Has token budget implications for the session voice use case
4. Would work for selectively loading only key references (not all 43KB)

If the `@` pattern works, recommend which references to auto-include. If it doesn't, document why and recommend the best alternative.

**Acceptance Criteria:**
- [ ] `@` import mechanism investigated and documented
- [ ] Feasibility for session voice reference loading determined
- [ ] If feasible: recommend which files to `@` import
- [ ] If not feasible: document alternative approaches
- [ ] Findings captured in this task or a discovery item

---

### TASK-006: Validate fix with comparative voice quality test

**Description:** After TASK-001 through TASK-004 are complete, run a comparative test:

1. Invoke `/saucer-boy` with the updated skill and ask for Saucer Boy energy on a topic
2. Compare the response quality against the pre-fix baseline (responses from this session before the skill was loaded)
3. Use sb-calibrator to score both responses for voice fidelity
4. Verify the fix achieves the BUG-002 acceptance criterion: "Main-context `/saucer-boy` invocation produces voice quality equal to or better than unstructured persona invocation"

**Acceptance Criteria:**
- [ ] Comparative test executed with updated skill
- [ ] sb-calibrator scores both pre-fix and post-fix responses
- [ ] Post-fix composite score >= pre-fix composite score
- [ ] Test results persisted to `docs/scores/voice/`
- [ ] BUG-002 acceptance criteria verified

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 7 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] Voice-guide pairs embedded in SKILL.md (TASK-001)
- [ ] Ambient persona prompt created and under 150 lines (TASK-002)
- [ ] Dual-mode routing documented in SKILL.md (TASK-003)
- [ ] sb-voice always-loads key references (TASK-004)
- [ ] `@` import pattern investigated (TASK-005)
- [ ] Comparative voice quality test passes (TASK-006)
- [ ] BUG-002 acceptance criteria all verified

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Post-fix voice quality >= pre-fix quality | [ ] |
| TC-2 | Ambient mode token budget under 500 tokens | [ ] |
| TC-3 | All H-25 through H-30 skill standards maintained | [ ] |
| TC-4 | 3299 tests still passing | [ ] |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Embedded pairs bloat SKILL.md beyond useful size | Low | Medium | Limit to 3-4 pairs; keep full set in voice-guide.md |
| `@` import pattern doesn't work for references | Medium | Low | TASK-001/002/003 provide the fix regardless; `@` import is a bonus |
| Ambient prompt is too short to be effective | Low | Medium | Test iteratively; 100-150 lines is a starting point, can adjust |
| Dual-mode routing adds decision overhead | Low | Low | Clear decision criteria: routine = ambient, deep persona = subagent |

---

## Dependencies

### Depends On

- [BUG-002: Session Voice Reference Loading](../BUG-002-session-voice-reference-loading/BUG-002-session-voice-reference-loading.md) — Root cause analysis

### Enables

- Higher-quality `/saucer-boy` responses in all sessions
- Pattern for reference-rich skill loading reusable by future skills
- Ambient mode operational for session personality

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-003: Voice Architecture](../EPIC-003-voice-architecture.md)

### Related Items

- **Related Bug:** [BUG-002: Session Voice Reference Loading](../BUG-002-session-voice-reference-loading/BUG-002-session-voice-reference-loading.md)
- **Related Feature:** [FEAT-002: Session Conversational Voice](../FEAT-002-session-conversational-voice/FEAT-002-session-conversational-voice.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Enabler created with 6 tasks. Addresses BUG-002 root causes: embedded examples, ambient prompt, dual-mode routing, always-load references, `@` import investigation, comparative validation. |

---
