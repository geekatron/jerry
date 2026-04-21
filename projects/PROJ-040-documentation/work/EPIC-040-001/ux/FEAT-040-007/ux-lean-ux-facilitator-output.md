---
feature_id: FEAT-040-007
agent: ux-lean-ux-facilitator
status: under_review
criticality: C3
engagement_id: UX-040-007
date: 2026-04-20
confidence: 0.75
quality_score: 0.91
iteration: 1
inputs:
  - projects/PROJ-040-documentation/reports/diataxis-audit-20260420.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-004/ux-heuristic-evaluator-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-005/ux-inclusive-evaluator-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-006/ux-behavior-diagnostician-output.md
wave: "Wave 1 Phase 1a (parallel — no JTBD input)"
degraded_mode: true
---

# Lean UX Hypothesis Cycle: Jerry Documentation Waves 2–4

## [DEGRADED MODE] No Miro MCP. Text-based facilitation only.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top hypotheses by ICE, MVPs, risk summary |
| [Engagement Context](#engagement-context) | Scope, upstream inputs |
| [Methodology](#methodology-notes) | Lean UX BML cycle, ICE scoring |
| [Hypothesis Backlog](#hypothesis-backlog) | 14 hypotheses in Lean UX format |
| [Assumption Maps](#assumption-maps) | 4-quadrant risk/knowledge mapping |
| [MVP Experiment Designs](#mvp-experiment-designs) | 15 per-hypothesis experiments |
| [ICE Prioritization](#ice-prioritization-matrix) | Ranked + priority bands |
| [Cross-Reference](#cross-reference-bmap-heuristic-wcag) | B=MAP + Heuristic + WCAG convergences |
| [Strategic Implications](#strategic-implications) | Patterns, maturity, velocity |
| [Synthesis Judgments](#synthesis-judgments-summary) | 8 AI inference disclosures |
| [Handoff Data](#handoff-data) | HEART mapping, status |

## Executive Summary

### Top Hypotheses by ICE

| Rank | ID | Hypothesis (abbr) | ICE |
|------|----|--------------------|-----|
| 1 | HYP-002 | Version reference update reduces setup friction | **8.3** |
| 1 (tie) | HYP-004 | README skills table → AGENTS.md link increases discovery | **8.3** |
| 3 | HYP-011 | Heading structure fix (INSTALLATION.md) | **7.7** |
| 3 (tie) | HYP-014 | Non-descriptive link text fix | **7.7** |
| 5 | HYP-001 | Upfront path detection reduces Step 3 abandonment | **7.3** |
| 6 | HYP-009 | README nav table addition | **7.0** |

### Highest-Risk Q1 Assumptions

1. **A-001:** Users abandon at Step 3 branching at measurable rate (structurally validated, no funnel data)
2. **A-006:** 0% tutorial coverage causally suppresses first-run success (gap confirmed; causal link assumed)
3. **A-010:** Skill-family organization preferable to individual skill pages (no user data)
4. **A-013:** Users search by problem domain, not sub-skill name (no user research)

### Highest-Leverage MVPs

1. **EXP-001** (One-question survey, 2 days): Test users' ability to self-identify install path → validates HYP-001 A-003
2. **EXP-004** (Fake door test, 1 week): Tutorial demand validation before 4-8hr authoring investment
3. **EXP-002** (Paper prototype, 3 days): Revised Step 3 with "Choose your path" block → 3 dev think-aloud

14 DRAFT hypotheses, 0 Build-Measure-Learn cycles completed.

## Engagement Context

**Product:** Jerry Framework v0.31.5 — Claude Code plugin for behavioral guardrails.

**Target Users:** AI developers, Claude Code users; terminal/plugin baseline; NOT assumed Jerry architecture familiarity.

**Design Scope:** PROJ-040 Waves 2-4 remediation + creation. Wave 2 (README), Wave 3 (existing docs), Wave 4a (tutorials), Wave 4b (how-tos), Wave 4c (explanations).

**Prior Research Inputs:**
- Diataxis audit (C4, 0.956): 0% tutorial coverage, 17% partial how-to, 30 skill gaps confirmed
- Heuristic eval (C3 iter-4, 0.89): 4 Sev-3 findings; F-010 + F-001 highest priority
- WCAG audit (C3 iter-3, 0.833): W-001 + W-002 Sev 3; content-only scope
- B=MAP (C3 iter-1, 0.84 → iter-2 0.861): Multiple bottleneck (Prompt + Ability); Step 3 primary

**MCP Status:** Degraded mode — no Miro MCP.

## Methodology Notes

Gothelf & Seiden Lean UX (3rd ed, 2021). Build-Measure-Learn cycle structures hypothesis generation → assumption risk-mapping → experiment design.

**Hypothesis format:** "We believe [outcome] for [users] if [change] because [evidence/reasoning]."

**ICE scoring (Ellis/GrowthHackers ~2015, adapted):** Impact, Confidence, Ease each 1-10; ICE = (I+C+E)/3. Lower score chosen when uncertain (P-022).

## Hypothesis Backlog

| ID | Hypothesis (Canonical) | Category | Status | I | C | E | ICE | Experiment |
|----|------------------------|----------|--------|---|---|---|-----|-----------|
| HYP-001 | 30%+ reduction in first-run abandonment if restructure Step 3 with upfront "Choose your path" block because F-010 Sev 3 + T-04 FAIL + B=MAP Brain Cycles converge on hidden branching | Usability | DRAFT | 9 | 7 | 6 | **7.3** | EXP-001, EXP-002 |
| HYP-002 | Reduction in setup friction if update version refs to current (Jerry v0.31.5, uv current, CC 1.0.33+) because stale refs are direct Brain Cycles load (B=MAP + Diataxis) | Usability | DRAFT | 8 | 8 | 9 | **8.3** | EXP-003 |
| HYP-003 | 15%+ reduction in install-path selection errors if move SSH prerequisite check BEFORE method table because F-005 identifies preventable backtrack | Usability | DRAFT | 6 | 6 | 8 | **6.7** | EXP-005 |
| HYP-004 | 50%+ increase skill discovery if replace stale 6-7 skill tables with AGENTS.md link because F-001 Sev 3 exposes only 20-25% of functionality | Value | DRAFT | 9 | 8 | 8 | **8.3** | EXP-004 |
| HYP-005 | Improved trust + time-on-task if remove marketing voice from INSTALLATION.md/docs/index.md because F-003 + Diataxis H-02 FAIL create instruction-reliability doubt | Usability | DRAFT | 7 | 6 | 7 | **6.7** | EXP-006 |
| HYP-006 | 40%+ first-skill-invocation success within 15 min if create docs/tutorial/first-skill-problem-solving.md because 0/30 tutorial coverage + B=MAP Facilitator gap at Step 4 | Value | DRAFT | 9 | 5 | 4 | **6.0** | EXP-007 |
| HYP-007 | Skill-family organization lower navigation time than per-skill for 10 UX sub-skills because common orchestrator + users search by problem domain | Value | DRAFT | 7 | 3 | 6 | **5.3** | EXP-008 |
| HYP-008 | Measurable AT task completion improvement if add language specifiers to 20+ code blocks because W-006 Sev 2 MEDIUM — AT uses lang for pronunciation | Usability | DRAFT | 5 | 6 | 9 | **6.7** | EXP-009 |
| HYP-009 | Improved navigation for motor/keyboard users if add H-23-compliant nav table to README because W-005 Sev 2 — only surface without nav table | Usability | DRAFT | 5 | 7 | 9 | **7.0** | EXP-010 |
| HYP-010 | Reduced cognitive load if deduplicate "What is Jerry?" across README/docs/index/INSTALLATION because F-007 Sev 3 three framings create inconsistent mental models | Usability | DRAFT | 7 | 6 | 5 | **6.0** | EXP-011 |
| HYP-011 | Reduced AT task errors + improved heading nav if convert bold-text step labels to H3 in INSTALLATION.md because W-001 Sev 3 HIGH hierarchy inconsistency | Usability | DRAFT | 6 | 8 | 9 | **7.7** | EXP-012 |
| HYP-012 | Maintained user motivation at hardest step if add motivational payoff at JERRY_PROJECT export because B=MAP degradation at install phase (LOW baseline) | Value | DRAFT | 5 | 3 | 8 | **5.3** | EXP-013 |
| HYP-013 | Reduced returning-user support load if author hooks-architecture + context-architecture explanations because both flagged missing since PROJ-015 | Value | DRAFT | 6 | 4 | 5 | **5.0** | EXP-014 |
| HYP-014 | Improved screen reader task completion if replace "file it"/"file that too" with descriptive text because W-002 Sev 3 HIGH WCAG failure | Usability | DRAFT | 5 | 9 | 9 | **7.7** | EXP-015 |

## Assumption Maps

### 4-Quadrant Framework

```
                   HIGH RISK
                       |
  Q2: Known High Risk  |  Q1: Unknown High Risk
  MONITOR              |  TEST FIRST
KNOWN ─────────────────┼─────────────────── UNKNOWN
  Q3: Known Low Risk   |  Q4: Unknown Low Risk
  ACCEPT               |  DEFER
                       |
                   LOW RISK
```

### HYP-001 Step 3 Path Detection

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-001: Users abandon at Step 3 at measurable rate | **Q1** | 3 audits structural; no funnel data. Riskiest unknown — if abandonment is earlier, fix misdirected. |
| A-002: Plugin vs CLI-clone distinction is confusing | Q2 | F-010 strong; mkdir + export before discovering wrong branch. High risk if wrong. |
| A-003: Users can self-identify path from decision block | **Q1** | Labels may not resonate with plugin users vs. local clone. |
| A-004: Restructure ~60 min, no content revalidation | Q3 | Effort from FEAT-040-006 Intervention 1. |

### HYP-002 Version Update

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-005: Stale refs cause verification pause | Q2 | B=MAP direct structural evidence. High risk if wrong. |
| A-006: "Minor differences OK" eliminates pause | **Q1** | Single sentence may not suppress verification if gap large. |

### HYP-004 Skills Table Replacement

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-007: Users who can't see skill don't know it exists | Q2 | F-001 strong. Risk zero if users navigate to AGENTS.md independently. |
| A-008: AGENTS.md link findable/used | **Q1** | Link discoverability in truncated table not validated. |
| A-009: Removing 24 skills doesn't reduce trust | **Q1** | Sparse table with link may read "Jerry only has 6 skills." |

### HYP-006 Tutorial

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-010: /problem-solving is right first skill | **Q1** | No usage analytics. Could be /worktracker or /nasa-se. Highest-risk for Wave 4a. |
| A-011: Single invocation tutorial completed <15 min | Q2 | B=MAP 15-min window. Medium confidence industry norms. |
| A-012: Absence of tutorial causal to low first-invocation | **Q1** | 0% coverage confirmed; causal link assumed. Users may fail for Ability reasons independent. |

### HYP-007 How-To Organization

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-013: Users think problem domain not sub-skill name | **Q1** | No user research. Core organizing assumption for Wave 4b. |
| A-014: /user-experience orchestrator correct entry point | Q2 | SKILL.md architecture confirms. New users may not know to invoke. |

## MVP Experiment Designs

15 experiments designed (EXP-001 through EXP-015). Key highlights:

**EXP-001 One-question survey** (2 days, 5 devs): "Which describes how you installed Jerry? (A) Plugin via Claude Code (B) Cloned repo (C) Not sure." Tests A-003. Success: ≥80% A/B not C.

**EXP-002 Paper prototype** (3 days, 3 devs): Present revised Step 3 with "Choose your path"; think-aloud. Success: ≥2/3 self-route correctly without prompting.

**EXP-003 Smoke test** (1 week): Update version refs + "minor differences OK" note; 3-5 users. Success: 0 users pause to verify; ≥60% reach Step 4.

**EXP-004 Fake door test** (1-2 weeks): Add "Tutorial coming soon" stub to docs/index.md Guides. Success: ≥5% CTR — validates demand before authoring.

**EXP-005 Paper prototype** (2 days): Two INSTALLATION.md versions (current vs. SSH-check-moved-earlier). Success: Version B 100% confident self-selection.

**EXP-006 Smoke test** (2 weeks): Replace marketing voice; measure time-on-page. Success: No drop in time-on-page; zero "confusing" feedback.

**EXP-007 Concierge MVP** (1 week): Walk 2-3 new users through tutorial via screen-share before authoring. Success: ≥2/3 reach first invocation in 20 min; top 3 friction points documented.

**EXP-008 One-question survey** (3 days, 8-15): "Search for UX eval: (A) /user-experience (B) specific sub-skill (C) SKILL.md." Tests A-013. Success: ≥60% consensus → organizational direction clear.

**EXP-009 Smoke test** (1 day + 1 week): Add language specifiers to 20+ code blocks. Success: grep verification 100%; any AT positive feedback = VALIDATED.

**EXP-010 Smoke test** (30 min + 1 week): Add README nav table. Success: table present; SC 3.2.3 PASS on re-audit.

**EXP-011 Paper prototype** (2 days, 3 devs): Multi-surface vs. deduplicated "What is Jerry?". Success: ≥2/3 consistent descriptions in deduplicated version.

**EXP-012 Smoke test** (1 hr + MkDocs build): Convert INSTALLATION.md bold steps to H3. Success: rendering correct; SC 1.3.1 PASS.

**EXP-013 Smoke test** (2 weeks): Add motivational sentence at Step 2 export. Success: any positive motivational feedback; no regression.

**EXP-014 Fake door** (2 weeks): Stub entries for hooks-architecture + context-architecture. Success: ≥3% CTR validates demand.

**EXP-015 Smoke test** (10 min): Replace "file it"/"file that too" with descriptive. Success: SC 2.4.4 PASS.

## ICE Prioritization Matrix

| Rank | ID | ICE | Priority Band | Rationale |
|------|-----|-----|---------------|-----------|
| 1 | HYP-002 | 8.3 | **P1 Immediate** | Highest confidence + ease. ~15 min. No experiment gate. |
| 1 | HYP-004 | 8.3 | **P1 Immediate** | F-001 Sev 3 HIGH. Low-effort fix. All new users affected. |
| 3 | HYP-011 | 7.7 | **P1 Immediate** | W-001 Sev 3 HIGH. ~1 hr. Structural — no experiment. |
| 3 | HYP-014 | 7.7 | **P1 Immediate** | W-002 Sev 3 HIGH. ~10 min. Deterministic WCAG. |
| 5 | HYP-001 | 7.3 | **P2 Validate first** | Highest impact. Moderate confidence. Run EXP-001+EXP-002 first. |
| 6 | HYP-009 | 7.0 | **P1 Immediate** | W-005 HIGH. ~30 min. |
| 7 | HYP-003 | 6.7 | **P2 Validate first** | F-005 moderate. EXP-005 first. |
| 8 | HYP-005 | 6.7 | **P2 Validate first** | Structural strong but subjective. EXP-006 smoke test. |
| 9 | HYP-008 | 6.7 | **P1 Immediate** | W-006 Sev 2 MEDIUM. ~1.5 hr. Grep-verifiable. |
| 10 | HYP-006 | 6.0 | **P3 Experiment first** | Long-term impact, 4-8hr investment. EXP-004+EXP-007 validate first. |
| 11 | HYP-010 | 6.0 | **P2 Validate first** | Medium effort/confidence. EXP-011 validates mental model. |
| 12 | HYP-007 | 5.3 | **P3 Experiment first** | No user data. EXP-008 before Wave 4b. |
| 13 | HYP-012 | 5.3 | **P2 Low-effort test** | Very low confidence. Smoke test minimal investment. |
| 14 | HYP-013 | 5.0 | **P3 Validate demand** | Significant authoring. EXP-014 fake door first. |

**P1 Immediate total effort:** ~4 hours for 6 hypotheses (HYP-002, HYP-004, HYP-008, HYP-009, HYP-011, HYP-014).

## Cross-Reference B=MAP + Heuristic + WCAG

| Issue | Heuristic | WCAG | B=MAP | Hypothesis | Convergence |
|-------|-----------|------|-------|------------|-------------|
| Step 3 hidden branching | F-010 Sev 3 | SC 1.3.1 W-001 | Brain Cycles + Prompt primary | HYP-001 | **Triple** |
| Stale skills table | F-001 Sev 3 | None | Motivation indirect | HYP-004 | Double (Heuristic + Diataxis) |
| Marketing voice | F-003 Sev 2 | Diataxis H-02 | Brain Cycles indirect | HYP-005 | Double |
| Inconsistent terminology | F-007 Sev 3 | SC 3.2.3 W-005 + 2.4.2 W-004 | Brain Cycles | HYP-010 | **Triple** |
| 0% tutorial/how-to | Diataxis | SC 2.4.5 partial | Facilitator gap Step 4 | HYP-006, HYP-007 | Double |
| Version staleness | T-08 FAIL | None | Brain Cycles direct | HYP-002 | Double |
| Heading structure | Not explicit | W-001 Sev 3 HIGH | — | HYP-011 | Single (WCAG HIGH) |
| Link text | None | W-002 Sev 3 HIGH | — | HYP-014 | Single (WCAG HIGH) |
| README nav table | None | W-005 Sev 2 | — | HYP-009 | Single (WCAG + H-23/H-24) |
| Code block lang | None | W-006 Sev 2 MEDIUM | — | HYP-008 | Single (WCAG MEDIUM) |

**Key insight:** Triple-convergence findings (Step 3 branching; terminology inconsistency) = highest-confidence remediation targets. Multiple methodologies identify same failure mode.

## Strategic Implications

### Pattern 1: High-Confidence Structural Fixes Are Low-Effort

6 of top-10 ICE-scored require no user experiment (HYP-002, 004, 008, 009, 011, 014). Total ~4 hours. "Quick wins" reduce audit-finding debt while medium-confidence experiments run.

### Pattern 2: Brain Cycles Bottleneck Requires Sequential Validation

HYP-001 highest impact but medium behavioral confidence. B=MAP establishes structural; whether fix reduces abandonment requires EXP-001 + EXP-002 before full implementation.

### Pattern 3: Wave 4 Needs Demand Validation Before Authoring

Tutorial (HYP-006) and explanation docs (HYP-013) = 4-8hr authoring. Fake door experiments (EXP-004, EXP-014) = 30-min tests prevent wasting on content no one navigates to.

### Pattern 4: How-To Organization Is Wave 4b Riskiest Unknown

HYP-007 lowest confidence (3/10). No user data. EXP-008 3-day survey could redirect entire Wave 4b structure. **First Wave 4b action.**

### Experimentation Maturity: Nascent → Developing

**Current:** No measurement infrastructure, no funnel data. All audits structural/heuristic.
**Target:** Developing via EXP-002 Step 3 completion rate, EXP-004 tutorial demand, EXP-008 org preference.

**Velocity:** Weeks 1-2 execute all P1 structural fixes while running EXP-001 + EXP-008 in parallel (both 2-3 day surveys). Wave 2/3 remediation proceeds while Wave 4 validation runs concurrently.

## Synthesis Judgments Summary

| Judgment | Confidence | Rationale |
|----------|-----------|-----------|
| HYP-001 ICE=7.3 (C=7) | MEDIUM | 3-source structural convergence. No funnel data. Lower-score-when-uncertain rule. |
| HYP-002 P1 without experiment gate | HIGH | Version refs: 3-source evidence, ~15 min, zero contrary. Smoke test recommended not blocking. |
| A-001 Q1 (Step 3 abandonment unknown) | HIGH | Absence of funnel data definitively unknown. |
| A-013 Q1 (domain vs skill-name mental model) | MEDIUM | No user research. Could be Q4 if UX usage negligible — but 10/30 skills UX. |
| A-012 Q1 (tutorial absence causal) | MEDIUM | 0% confirmed; causal assumed. Could be Q2 if Ability is true cause. |
| HYP-007 ICE=5.3 | LOW | No user data. Score reflects honest uncertainty. |
| HYP-005 C=6 (tone-trust) | MEDIUM | HCI literature general; not measured for this product. |
| P1 band (immediate no gate) | HIGH | Only HIGH-confidence WCAG/structural findings. No speculative P1. |

## Handoff Data

All 14 hypotheses currently DRAFT. Only experiments-completed hypotheses promote to VALIDATED/INVALIDATED. Anticipated HEART mapping for planning only:

| Hypothesis | Anticipated Status | Outcome Metric | HEART Category |
|------------|-------------------|----------------|----------------|
| HYP-001 | Pending EXP-001+002 | First-run completion at Step 3 | **Task Success** |
| HYP-002 | Pending EXP-003 | Time-to-Step-4 | **Task Success** |
| HYP-004 | Pending deployment | Skill discovery from README | **Adoption** |
| HYP-006 | Pending EXP-004+007 | First-skill invocation <15 min | **Task Success** |
| HYP-007 | Pending EXP-008 | Navigation time to first how-to | **Task Success** |
| HYP-010 | Pending EXP-011 | Mental model consistency score | **Happiness** |
| HYP-011 | Pending EXP-012 | SC 1.3.1 PASS/FAIL AT navigation | **Task Success** |

**Handoff threshold:** No hypotheses qualify for cross-framework handoff yet (all DRAFT). Promote after EXP-001 through EXP-004 complete (~2-3 weeks).

### On-Send Protocol

```yaml
from_agent: ux-lean-ux-facilitator
engagement_id: UX-040-007
total_hypotheses: 14
hypothesis_status_distribution:
  DRAFT: 14
assumptions_mapped: 14
q1_assumptions: 6
experiments_designed: 15
cycles_completed: 0
degraded_mode: true
artifact_path: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-007/ux-lean-ux-facilitator-output.md
handoff_hypotheses_count: 0
```

---

*Agent: ux-lean-ux-facilitator v1.1.0 | FEAT-040-007 | 2026-04-20 | Lean UX: Gothelf & Seiden 2021 | ICE: Ellis/GrowthHackers ~2015 | Degraded mode: no Miro MCP*
