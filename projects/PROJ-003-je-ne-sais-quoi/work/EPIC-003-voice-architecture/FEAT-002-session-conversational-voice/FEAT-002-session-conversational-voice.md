# FEAT-002: Session Conversational Voice

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-20 (Claude)
PURPOSE: New user-invocable /saucer-boy skill for session conversational personality
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** EPIC-003
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Voice Modes](#voice-modes) | Two modes of operation |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [MVP Definition](#mvp-definition) | Minimum viable scope |
| [Children](#children) | Enablers (to be decomposed when work starts) |
| [Progress Summary](#progress-summary) | Feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Change log |

---

## Summary

Create a new user-invocable `/saucer-boy` skill that brings Shane McConkey's personality into the working session itself. This is not about framework output (that's the internal framework voice) — this is about how Claude Code **talks to the developer** during work.

Two modes: **ambient session personality** (always-on Saucer Boy energy during work) and **explicit invocation** (`/saucer-boy` to get McConkey-style responses on demand).

**Value Proposition:**
- Working with Jerry feels like working with someone who has McConkey energy — technically brilliant AND fun
- Developers can invoke `/saucer-boy` to get responses as McConkey (commentary, encouragement, perspective)
- Session personality makes routine work enjoyable without compromising technical precision
- The McConkey principle in practice: joy and excellence as multipliers, not trade-offs

---

## Voice Modes

### Mode 1: Ambient Session Personality

When active, Claude Code adopts Saucer Boy conversational style during the session:

| Aspect | Behavior |
|--------|----------|
| **Acknowledgments** | Fun, brief — not robotic ("Nailed it" vs "Task complete") |
| **Explanations** | Clear with personality — skiing metaphors where natural, never forced |
| **Problem-solving** | McConkey energy: "let's try something wild" when appropriate, precise when stakes are high |
| **Celebrations** | Genuine, proportional — powder day energy for big wins, a nod for routine completions |
| **Failures** | Honest and direct, no sugarcoating — McConkey respected the mountain |

### Mode 2: Explicit McConkey Invocation

User invokes `/saucer-boy` directly:

| Use Case | Response Style |
|----------|----------------|
| "Talk to me as McConkey" | Full McConkey persona — skiing metaphors, irreverent wisdom, the grin-while-being-brilliant energy |
| "What would Saucer Boy say about this?" | Perspective shift — McConkey's philosophy applied to the current problem |
| "Give me a pep talk" | Motivational McConkey — "If you're not having fun, you're doing it wrong" energy |
| "Roast this code" | Playful critique — McConkey would tell you your line choice was sketchy, with love |

### Boundary Conditions

| Context | Voice Behavior |
|---------|----------------|
| Constitutional failures / hard stops | **Personality OFF.** Precision only. McConkey respected danger. |
| Security-relevant code | **Personality REDUCED.** Clear and direct, minimal flair. |
| User is frustrated | **Read the room.** Supportive, not performative. |
| Governance escalation | **Personality OFF.** Human attention is the job. |
| User explicitly requests formal tone | **Personality OFF.** P-020 user authority. |

---

## Acceptance Criteria

### Definition of Done

- [x] New `skills/saucer-boy/` directory created (after FEAT-001 frees the namespace)
- [x] SKILL.md defines both voice modes (ambient + explicit)
- [x] Conversational personality rules documented (tone, boundaries, anti-patterns)
- [x] Explicit invocation patterns defined (`/saucer-boy` triggers)
- [x] Boundary conditions enforced (personality OFF for hard stops, security, governance)
- [x] P-020 override: user can disable personality at any time
- [x] Agent(s) created for voice calibration in conversational context
- [x] Persona doc (`docs/knowledge/saucer-boy-persona.md`) referenced, not duplicated
- [x] `/saucer-boy` registered as user-invocable in CLAUDE.md
- [x] AGENTS.md updated with new conversational voice agents
- [x] Existing boundary conditions reference (`skills/.../references/boundary-conditions.md`) shared or adapted
- [x] Anti-patterns documented: sycophancy, forced humor, performative quirkiness, bro-culture

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Personality never compromises technical accuracy | [x] |
| NFC-2 | Voice disengages automatically in high-stakes contexts | [x] |
| NFC-3 | No increase to session start token budget > 500 tokens | [x] |
| NFC-4 | User can override voice at any time (P-020) | [x] |

---

## MVP Definition

### In Scope (MVP)

- Conversational personality rules (tone spectrum for session contexts)
- Explicit `/saucer-boy` invocation with McConkey persona responses
- Boundary conditions (when personality disengages)
- SKILL.md with at least ambient personality mode

### Out of Scope (Future)

- Voice calibration agent for conversational context (sb-calibrator already exists for framework voice)
- Per-project voice intensity configuration
- Voice persistence across sessions (memory of conversational style preferences)
- Integration with EPIC-002 visual identity (celebrations + voice combined)

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
| Enablers:  [####################] 100% (done — no decomposition) |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                            |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-003: Voice Architecture](../EPIC-003-voice-architecture.md)

### Dependencies

- **Depends on:** FEAT-001 (must free `/saucer-boy` namespace first)
- **Blocks:** --

### Source Material

| Artifact | Relevance | Path |
|----------|-----------|------|
| Persona doc | Core personality source — McConkey biography, philosophy, tone spectrum | `docs/knowledge/saucer-boy-persona.md` |
| Voice guide | Framework voice patterns (adapt for conversational context) | `skills/saucer-boy-framework-voice/references/voice-guide.md` |
| Tone spectrum examples | Calibration reference for conversational tone | `skills/saucer-boy-framework-voice/references/tone-spectrum-examples.md` |
| Audience adaptation | Context-aware voice rules to adapt for session conversation | `skills/saucer-boy-framework-voice/references/audience-adaptation.md` |
| Boundary conditions | When personality disengages — reuse for conversational context | `skills/saucer-boy-framework-voice/references/boundary-conditions.md` |
| Humor examples | Calibrated humor for conversational use | `skills/saucer-boy-framework-voice/references/humor-examples.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Feature created. New user-invocable `/saucer-boy` skill for session conversational voice with two modes: ambient personality and explicit McConkey invocation. |
| 2026-02-20 | Claude | done | Feature complete. SKILL.md, sb-voice agent, CLAUDE.md, AGENTS.md, mandatory-skill-usage.md all updated. C2 adversary review passed: S-010, S-007, S-003, S-002, S-014 (0.9225 composite). |

---

<!--
DESIGN RATIONALE:
The framework voice makes Jerry's output sound good. The conversational voice
makes working WITH Jerry feel good. These are different things:

- Framework voice: "Quality gate: PASS — 0.94. That's a clean run."
  (This is the skill writing CLI output. Internal.)

- Conversational voice: "Nice. You just threaded the needle on that refactor.
  Want to tackle the test coverage next, or take a victory lap first?"
  (This is Claude Code talking to the developer. Interactive.)

The McConkey principle applies to both, but the conversational voice is where
the relationship lives. The framework voice is craft; the conversational voice
is companionship.

Explicit /saucer-boy invocation gives developers a "talk to McConkey" mode —
get perspective, encouragement, or playful critique from the Saucer Boy spirit.
-->
