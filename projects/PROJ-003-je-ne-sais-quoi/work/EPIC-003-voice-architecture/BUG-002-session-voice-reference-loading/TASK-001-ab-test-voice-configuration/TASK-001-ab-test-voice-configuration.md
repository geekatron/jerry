# TASK-001: A/B Test Voice Configuration Matrix

> **Type:** task
> **Status:** done
> **Priority:** high
> **Activity:** RESEARCH
> **Created:** 2026-02-20
> **Parent:** BUG-002
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task investigates |
| [Test Matrix](#test-matrix) | 4-configuration A/B test design |
| [Acceptance Criteria](#acceptance-criteria) | When this task is done |
| [Results](#results) | Test scores and analysis |
| [Evidence](#evidence) | Score report links |
| [History](#history) | Change log |

---

## Description

The sb-voice explicit path scored 0.73 composite (vs 0.83 baseline) with the worst gap in Occasionally Absurd (0.25). Two hypotheses explain the underperformance:

1. **Model hypothesis:** Sonnet is more conservative with personality than Opus
2. **Reference hypothesis:** Loading only 2 of 10 reference files starves the agent of calibration material

This task runs a 2x2 A/B test matrix to isolate which factor matters more and determine the optimal sb-voice configuration.

---

## Test Matrix

All tests use the same prompt to ensure fair comparison:

> "We just finished implementing the entire voice architecture — two features, an enabler with 6 tasks, and a C2 adversary review that passed at 0.92. Give me some Saucer Boy energy about this achievement."

| Test | Model | References | Hypothesis Tested |
|------|-------|-----------|-------------------|
| A | sonnet | 2 files (voice-guide, bio-anchors) | Baseline (current config) |
| B | sonnet | all 10 reference files (~43KB) | Does more material help sonnet? |
| C | opus | 2 files (voice-guide, bio-anchors) | Is model the dominant factor? |
| D | opus | all 10 reference files (~43KB) | Best possible explicit path? |

**Reference files (all 10):**
1. `voice-guide.md` — 9 before/after calibration pairs
2. `biographical-anchors.md` — McConkey biographical facts
3. `humor-examples.md` — Humor deployment modes
4. `cultural-palette.md` — In-bounds/out-of-bounds references
5. `tone-spectrum-examples.md` — Per-energy-level examples
6. `boundary-conditions.md` — Detailed boundary explanations
7. `audience-adaptation.md` — Context-specific voice rules
8. `vocabulary-reference.md` — Term substitutions
9. `visual-vocabulary.md` — Formatting guidance
10. `implementation-notes.md` — FEAT-004/006/007 guidance

**Scoring:** sb-calibrator scores each response on 5 voice traits (Direct, Warm, Confident, Occasionally Absurd, Technically Precise) with equal-weighted composite.

---

## Acceptance Criteria

- [x] All 4 tests executed with identical prompt
- [x] All 4 responses scored by sb-calibrator
- [x] Results table populated with per-trait and composite scores
- [x] Dominant factor identified (model vs references vs both)
- [x] Recommendation for optimal sb-voice configuration documented
- [x] Score reports persisted to `docs/scores/voice/ab-test/`

---

## Results

| Test | Model | Refs | Composite | Direct | Warm | Confident | Absurd | Precise |
|------|-------|------|-----------|--------|------|-----------|--------|---------|
| Baseline | opus (main ctx) | internalized | 0.83 | 0.88 | 0.82 | 0.88 | 0.72 | 0.85 |
| EN-001 ambient | opus (main ctx) | persona prompt | 0.81 | 0.92 | 0.82 | 0.88 | 0.55 | 0.87 |
| **A** | **sonnet** | **2** | **0.878** | 0.91 | 0.87 | 0.92 | 0.76 | 0.93 |
| **B** | **sonnet** | **10** | **0.844** | 0.92 | 0.74 | 0.91 | 0.74 | 0.91 |
| **C** | **opus** | **2** | **0.83** | 0.78 | 0.74 | 0.92 | 0.80 | 0.93 |
| **D** | **opus** | **10** | **0.882** | 0.85 | 0.83 | 0.93 | **0.88** | 0.92 |

### Analysis

**Interaction effect dominates.** Neither model nor reference count alone predicts the winner — they interact:

| | 2 refs | 10 refs | Delta |
|---|---|---|---|
| **Sonnet** | 0.878 | 0.844 | -0.034 (more refs hurt) |
| **Opus** | 0.83 | 0.882 | +0.052 (more refs helped) |

**Key findings:**

1. **Sonnet gets more conservative with more material.** Loading all 10 files dropped sonnet's Warm from 0.87 to 0.74 and Absurd from 0.76 to 0.74. The compliance/boundary material overwhelmed the personality signal.

2. **Opus benefits from rich calibration material.** Full references pushed Opus's Occasionally Absurd from 0.80 to 0.88 — the highest Absurd score in any test, including baselines. The humor-examples.md and cultural-palette.md files gave Opus more to work with.

3. **All explicit configurations beat both baselines** except C (which matches):
   - D: 0.882 vs 0.83 baseline (+0.052)
   - A: 0.878 vs 0.83 baseline (+0.048)
   - B: 0.844 vs 0.83 baseline (+0.014)
   - C: 0.83 vs 0.83 baseline (match)

4. **The original sb-voice test (0.73) underperformed due to weaker prompt**, not just configuration. The EN-001 improved invocation pattern fixed the baseline.

5. **Opus + all refs (D) has the most balanced profile** — no trait below 0.83, the only configuration where Occasionally Absurd exceeds 0.85.

### Recommendation

**Winner: Configuration D — opus + all 10 reference files (0.882 composite)**

| Factor | Recommendation | Rationale |
|--------|---------------|-----------|
| **Model** | Change sb-voice from sonnet to opus | Opus handles rich personality material better; sonnet becomes conservative |
| **References** | Always-load all 10 reference files | Full set benefits opus; the +0.052 delta is the largest improvement in the matrix |
| **Trade-off** | Opus is slower/costlier than sonnet | Explicit invocations are infrequent (user-initiated); quality matters more than latency for on-demand McConkey responses |

**Alternative: Configuration A (sonnet + 2 refs, 0.878) if latency is critical.** Only 0.004 below D on composite, and its Warm trait (0.87) is the highest in any test. The trade-off: Occasionally Absurd stays at 0.76 instead of D's 0.88.

**Implementation:** Update `skills/saucer-boy/agents/sb-voice.md` frontmatter `model: opus`, change always-load to include all 10 reference files, and update SKILL.md Task tool invocation example to use `model="opus"`.

---

## Evidence

| Deliverable | Type | Link |
|-------------|------|------|
| Test A score | Score report | `docs/scores/voice/ab-test/test-a-sonnet-2refs.md` |
| Test B score | Score report | `docs/scores/voice/ab-test/test-b-sonnet-allrefs.md` |
| Test C score | Score report | `docs/scores/voice/ab-test/test-c-opus-2refs.md` |
| Test D score | Score report | `docs/scores/voice/ab-test/test-d-opus-allrefs.md` |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | in-progress | Task created. 2x2 A/B test matrix: model (sonnet/opus) x references (2/10). |
| 2026-02-20 | done | All 4 tests executed and scored. Winner: D (opus + all refs, 0.882). Key insight: interaction effect dominates — opus benefits from more material (+0.052), sonnet gets more conservative (-0.034). |

---
