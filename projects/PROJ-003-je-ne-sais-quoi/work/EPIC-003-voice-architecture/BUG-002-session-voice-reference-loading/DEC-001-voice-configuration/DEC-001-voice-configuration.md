# BUG-002:DEC-001: Voice Configuration — Model and Reference Count

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-20 (Claude)
PURPOSE: Capture optimal sb-voice agent configuration based on A/B test evidence
-->

> **Type:** decision
> **Status:** accepted
> **Priority:** high
> **Created:** 2026-02-20
> **Parent:** BUG-002
> **Owner:** Claude
> **Related:** TASK-001 (A/B Test Voice Configuration Matrix)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decision |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured D-001 entry |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Captured the optimal sb-voice agent configuration for explicit McConkey invocations, based on TASK-001 A/B test results (2x2 matrix: model x reference count).

**Decisions Captured:** 1

**Key Outcomes:**
- sb-voice agent model changed from sonnet to opus
- Reference loading changed from 2 files (on-demand) to all 10 files (always-load)
- Composite voice fidelity score: 0.882 (highest in test matrix)

---

## Decision Context

### Background

BUG-002 identified that the session voice skill loads rules without examples — the 43KB of calibration references never reach the sb-voice agent in practice. EN-001 fixed the reference architecture, but the original sb-voice configuration (sonnet model, 2 always-loaded reference files) left the Occasionally Absurd trait underperforming (0.55-0.76 range across tests vs 0.88 baseline target).

The user questioned why we wouldn't load all 10 reference files for sb-voice, prompting a systematic A/B test to determine the optimal configuration.

### Constraints

- Explicit invocations are user-initiated and infrequent — latency is acceptable
- Voice quality (especially Occasionally Absurd trait) is the primary optimization target
- Model cost (opus vs sonnet) is secondary to quality for infrequent invocations
- All configurations must maintain P-003 compliance (single-level worker agent)

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Decision authority (P-020) | Voice quality for on-demand McConkey responses |
| Claude | Implementer | Optimal agent configuration backed by evidence |

---

## Decisions

### D-001: sb-voice Model and Reference Configuration

**Date:** 2026-02-20
**Participants:** User, Claude

#### Question/Context

The user asked: "When using the sb-voice agent, why wouldn't we pass it the `saucer-boy-framework-voice/references/*` and tell it to parse all of this? Wouldn't that increase the score? Did we try and A/B test this?"

This prompted TASK-001: a 2x2 A/B test matrix isolating model (sonnet/opus) and reference count (2/10) as independent variables, with sb-calibrator scoring each configuration on the 5 voice traits.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | sonnet + 2 refs | Fastest, lowest cost. 0.878 composite. Warm: 0.87 (highest). | Absurd: 0.76 (below target). |
| **B** | sonnet + 10 refs | More material for calibration. | 0.844 composite — sonnet gets *more conservative* with more material (-0.034). Warm drops to 0.74. |
| **C** | opus + 2 refs | Stronger model. Absurd: 0.80 (improvement). | 0.83 composite — matches baseline but doesn't exceed. Direct: 0.78. |
| **D** | opus + 10 refs | Highest composite: 0.882. Absurd: 0.88 (highest in any test). Most balanced profile — no trait below 0.83. | Slower, costlier than sonnet. |

#### Decision

**We decided:** Configuration D — opus model + all 10 reference files.

#### Rationale

The interaction effect dominates: opus benefits from rich calibration material (+0.052 composite with all refs), while sonnet becomes more conservative with more material (-0.034). Configuration D produces:

- Highest composite score: 0.882 (vs 0.83 baseline, +0.052)
- Highest Occasionally Absurd: 0.88 (the primary gap trait)
- Most balanced profile: no trait below 0.83
- The only configuration where Occasionally Absurd exceeds 0.85

Explicit invocations are infrequent (user-initiated), so opus latency and cost are acceptable trade-offs for quality.

**Full results:**

| Config | Model | Refs | Composite | Direct | Warm | Confident | Absurd | Precise |
|--------|-------|------|-----------|--------|------|-----------|--------|---------|
| Baseline | opus (main ctx) | internalized | 0.83 | 0.88 | 0.82 | 0.88 | 0.72 | 0.85 |
| A | sonnet | 2 | 0.878 | 0.91 | 0.87 | 0.92 | 0.76 | 0.93 |
| B | sonnet | 10 | 0.844 | 0.92 | 0.74 | 0.91 | 0.74 | 0.91 |
| C | opus | 2 | 0.83 | 0.78 | 0.74 | 0.92 | 0.80 | 0.93 |
| **D** | **opus** | **10** | **0.882** | 0.85 | 0.83 | 0.93 | **0.88** | 0.92 |

#### Implications

- **Positive:** Voice quality exceeds baseline by +0.052; Occasionally Absurd trait reaches 0.88 (primary gap closed)
- **Negative:** Opus is slower and costlier than sonnet for each explicit invocation
- **Follow-up required:** Update sb-voice.md (model + always-load), SKILL.md (invocation example + agents table)

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Use opus model + all 10 reference files for sb-voice explicit invocations | 2026-02-20 | Accepted |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [BUG-002](../BUG-002-session-voice-reference-loading.md) | Session voice reference loading bug |
| Evidence | [TASK-001](../TASK-001-ab-test-voice-configuration/TASK-001-ab-test-voice-configuration.md) | A/B test matrix with full results |
| Score Report | `docs/scores/voice/ab-test/test-a-sonnet-2refs.md` | Test A score (0.878) |
| Score Report | `docs/scores/voice/ab-test/test-b-sonnet-allrefs.md` | Test B score (0.844) |
| Score Report | `docs/scores/voice/ab-test/test-c-opus-2refs.md` | Test C score (0.83) |
| Score Report | `docs/scores/voice/ab-test/test-d-opus-allrefs.md` | Test D score (0.882) |
| Affected File | `skills/saucer-boy/agents/sb-voice.md` | Agent definition updated per decision |
| Affected File | `skills/saucer-boy/SKILL.md` | Skill file updated per decision |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-20 | Claude | Created decision document. Extracted from inline BUG-002 decision to proper DEC entity per user feedback. |

---
