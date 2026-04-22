---
feature_id: FEAT-040-007
agent: ux-lean-ux-facilitator
status: complete
criticality: C3
engagement_id: UX-040-007
date: 2026-04-20
confidence: 0.78
quality_score: 0.9220
iteration: 6
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
| [Revision History](#revision-history) | Iteration log: changes, verdicts, scores |

## Executive Summary

### Top Hypotheses by ICE

| Rank | ID | Hypothesis (abbr) | ICE |
|------|----|--------------------|-----|
| 1 | HYP-002 | Version reference update reduces setup friction | **8.3** |
| 2 | HYP-004 | README skills table → AGENTS.md link increases discovery | **7.7** |
| 3 (tie) | HYP-011 | Heading structure fix (INSTALLATION.md) | **7.7** |
| 3 (tie) | HYP-014 | Non-descriptive link text fix | **7.7** |
| 5 | HYP-009 | README nav table addition | **7.0** |
| 6 | HYP-003 | SSH prerequisite order reduces backtrack errors | **6.7** |

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

**Ease dimension definition (iter-2 clarification):** Ease captures both (a) implementation effort and (b) experiment design effort — the cost of setting up the experiment and getting valid signal. For P1 Immediate items where the "experiment" is the implementation itself (e.g., WCAG fixes with deterministic re-audit), E reflects implementation effort only. For behavioral hypotheses requiring user interviews or surveys, E must reflect the full validation cost. HYP-008 E reduced from 9 to 6 on this basis: implementation is trivial (grep, 1 day) but AT interview validation requires recruiting 3-5 screen-reader users, a non-trivial coordination effort.

## Hypothesis Backlog

| ID | Hypothesis (Canonical) | Category | Status | I | C | E | ICE | Experiment |
|----|------------------------|----------|--------|---|---|---|-----|-----------|
| HYP-001 | We believe reduced first-run abandonment at Step 3 for new Jerry users if restructure Step 3 with upfront "Choose your path" block because F-010 Sev 3 + T-04 FAIL + B=MAP Brain Cycles converge on hidden branching — Impact reduced from 9 to 6 (P-022: A-001 is Q1 Unknown; no baseline abandonment rate) | Usability | DRAFT | 6 | 5 | 6 | **5.7** | EXP-001, EXP-002 |
| HYP-002 | We believe reduction in setup friction for new Jerry installers if update version refs to current (Jerry v0.31.5, uv current, CC 1.0.33+) because stale refs are direct Brain Cycles load (B=MAP + Diataxis) | Usability | DRAFT | 8 | 8 | 9 | **8.3** | EXP-003 |
| HYP-003 | We believe 15%+ reduction in install-path selection errors for developers selecting SSH installation if move SSH prerequisite check BEFORE method table because F-005 identifies preventable backtrack pattern common when users encounter SSH prereq mid-flow | Usability | DRAFT | 6 | 6 | 8 | **6.7** | EXP-005 |
| HYP-004 | We believe improved skill discovery for new Jerry users if replace stale 6-7 skill tables with AGENTS.md link because F-001 Sev 3 exposes only 20-25% of 30+ skills — Confidence reduced to 7 (no measurement baseline for discovery rate) | Value | DRAFT | 9 | 7 | 8 | **8.0** | EXP-004 |
| HYP-005 | We believe improved trust and reduced time-on-task for first-time Jerry installers if remove marketing voice from INSTALLATION.md/docs/index.md because F-003 + Diataxis H-02 FAIL demonstrate that promotional framing creates instruction-reliability doubt for users trying to complete procedural steps | Usability | DRAFT | 7 | 6 | 7 | **6.7** | EXP-006 |
| HYP-006 | We believe 40%+ first-skill-invocation success within 15 min for new Jerry users if create docs/tutorial/first-skill-problem-solving.md because 0/30 tutorial coverage + B=MAP Facilitator gap at Step 4 leave users without guided first-run path | Value | DRAFT | 9 | 5 | 4 | **6.0** | EXP-007 |
| HYP-007 | We believe reduced navigation time to relevant how-to documentation for users seeking UX evaluation skills if organize Wave 4b how-to pages by skill family rather than per-skill because /user-experience uses a shared orchestrator and users are expected to search by problem domain rather than sub-skill name | Value | DRAFT | 7 | 3 | 6 | **5.3** | EXP-008 |
| HYP-008 | We believe measurable AT task completion improvement for screen-reader users if add language specifiers to 20+ code blocks because W-006 Sev 2 MEDIUM confirms AT uses language attribute for correct code pronunciation — E reduced to 6 (Lean UX Ease includes experiment validation effort, not just implementation effort) | Usability | DRAFT | 5 | 6 | 6 | **5.7** | EXP-009 |
| HYP-009 | We believe improved navigation for motor/keyboard users if add H-23-compliant nav table to README because W-005 Sev 2 — only surface without nav table | Usability | DRAFT | 5 | 7 | 9 | **7.0** | EXP-010 |
| HYP-010 | We believe reduced cognitive load for new Jerry users if deduplicate "What is Jerry?" across README/docs/index/INSTALLATION because F-007 Sev 3 confirms three inconsistent framings create conflicting mental models that impede task completion | Usability | DRAFT | 7 | 6 | 5 | **6.0** | EXP-011 |
| HYP-011 | We believe reduced AT task errors and improved heading navigation for screen-reader users if convert bold-text step labels to H3 in INSTALLATION.md because W-001 Sev 3 HIGH confirms heading hierarchy inconsistency prevents AT navigation by structure | Usability | DRAFT | 6 | 8 | 9 | **7.7** | EXP-012 |
| HYP-012 | We believe maintained user motivation at hardest step for users at JERRY_PROJECT export if add motivational payoff sentence at Step 2 export because B=MAP identifies motivation degradation at install phase (LOW baseline) creating abandonment risk at precisely the step requiring env-var configuration | Value | DRAFT | 5 | 3 | 8 | **5.3** | EXP-013 |
| HYP-013 | We believe reduced returning-user support load for experienced Jerry users if author hooks-architecture + context-architecture explanations because both flagged missing since PROJ-015 and are the most-asked architectural questions in session logs | Value | DRAFT | 6 | 4 | 5 | **5.0** | EXP-014 |
| HYP-014 | We believe improved screen reader task completion for AT users if replace "file it"/"file that too" with descriptive link text because W-002 Sev 3 HIGH confirms WCAG 2.4.4 failure that prevents link-purpose identification without surrounding context | Usability | DRAFT | 5 | 9 | 9 | **7.7** | EXP-015 |

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
| A-006: "Minor differences OK" eliminates pause | **Q2** | Reclassified from Q1. The causal mechanism (tutorial/procedural gap → failed first run) is theoretically grounded in Diataxis literature (Procida 2021) and accepted at C4 quality in the diataxis audit (0.956). Behavioral magnitude unknown, but causal direction is established: MONITOR not TEST FIRST. Experiment validates magnitude, not existence of the mechanism. |

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

### HYP-009 README Nav Table

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-015: H-23/H-24 compliance requires a nav table on README (structural) | Q3 | Known and low risk. W-005 Sev 2 confirms README is the only primary surface missing a nav table; H-23 rule definition is unambiguous. Implementation is deterministic. ACCEPT — no experiment required. |
| A-016a: A standard markdown nav table at top of README satisfies WCAG 2.4.10 (section headings) and 2.4.1 (bypass blocks) architectural obligation | Q3 | WCAG 2.4.10 and 2.4.1 establish a deterministic structural requirement: a compliant site must provide section heading navigation and bypass blocks. MkDocs renders markdown tables with correct heading hierarchy (per A-017). This is a known, low-risk architectural fact — ACCEPT, no experiment required for this dimension. | | A-016b: Motor/keyboard Jerry users navigate README sequentially via heading structure and derive measurable benefit from the nav table's skip links | **Q1** | The WCAG citations above establish architectural obligation (A-016a, Q3); they do NOT validate this behavioral claim. Whether Jerry's motor/keyboard users actually navigate README via headings in sequence is unobserved — users may enter primarily via docs/index.md or internal links, in which case the behavioral benefit of the README nav table is lower than assumed. This Q1 behavioral unknown is independent of the Q3 architectural compliance. HIGH risk because the behavioral benefit is the claimed user value; LOW current knowledge. TEST FIRST for behavioral dimension — EXP-010 smoke test gates on SC 3.2.3 re-audit (structural proxy for A-016a); behavioral dimension (A-016b) deferred per Sev 2 threshold acceptance in Synthesis Judgments. |
| A-017: SC 3.2.3 re-audit PASS is achievable with a standard markdown table at top of README | Q3 | Known and low risk. MkDocs renders markdown tables with correct heading hierarchy; H-23 nav table format standard is defined. Implementation is ~30 min. ACCEPT. |

### HYP-012 Motivational Payoff Sentence

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-018: JERRY_PROJECT export step has measurably low motivation among current users | **Q1** | B=MAP motivation assessment at this step is structural inference from LOW baseline rating; no direct user survey confirms motivation degradation specifically at Step 2 export. The motivational sentence intervention is premised on this being the critical drop-off point. Unknown and HIGH risk — if motivation degradation is uniform across all install steps (not Step 2 specifically), the targeted intervention will not produce a differential signal. |
| A-019: A motivational payoff sentence is the right type of intervention for an env-var configuration step | **Q1** | The Fogg B=MAP Motivation lever is theoretically applicable here, but the actual intervention type (a payoff sentence) is unvalidated at this friction point. Users encountering env-var configuration may need Ability support (clearer instructions, copy-paste snippet) rather than Motivation support. Unknown and HIGH risk — wrong intervention type wastes authoring effort and produces null EXP-013 result. |
| A-020: 3 users per variant (n=6 total) provides sufficient signal for A/B interview | Q2 | Known limitation with high risk if wrong. n=3 per variant is a very small A/B sample; the bilateral threshold (≥2/3 variant, ≤1/3 control) is designed to compensate, but a single user outlier can swing the result. MONITOR — EXP-013 is explicitly low-confidence (C=3); result interpreted as directional, not conclusive. |

### HYP-013 Explanation Docs

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-021: hooks-architecture and context-architecture are the most-asked architectural questions | Q2 | Supported by session logs and PROJ-015 flagging; acknowledged in hypothesis evidence clause. Known but HIGH risk if the session log sample is biased toward early adopters who ask different questions than the current user base. MONITOR — EXP-014 fake door test validates demand before 4-8hr authoring investment. |
| A-022: Users who ask architectural questions would navigate to a dedicated explanation document | **Q1** | Users who ask questions in session logs may be doing so precisely because no document exists; if a document did exist, they might not find it via standard navigation (search by architecture topic vs. by concept name). Navigation discovery behavior for explanatory content is unknown. TEST FIRST — EXP-014 fake door stub CTR is the test. |
| A-023: Explanation doc format (Diataxis quadrant 4) is the right format for architectural questions | Q3 | Diataxis audit classified both gaps as Explanation quadrant at C4 (0.956). Format classification is known and low risk. ACCEPT. |

### HYP-014 Descriptive Link Text

| Assumption | Quadrant | Rationale |
|-----------|----------|-----------|
| A-024: "file it"/"file that too" link text prevents AT users from identifying link purpose | Q2 | W-002 Sev 3 HIGH confirms WCAG 2.4.4 failure. Direct structural evidence; WCAG 2.4.4 failure is a defined criterion with deterministic audit path. Known and HIGH risk if the contextual reading pattern of Jerry's AT users means surrounding sentence context always resolves ambiguity (2.4.4 allows context as disambiguation). MONITOR — EXP-015 smoke test + SC 2.4.4 re-audit resolves this within 10 min. |
| A-025: Replacing non-descriptive link text requires only text substitution with no content restructuring | Q3 | Known and low risk. The linked targets ("file it" → "open a GitHub issue for this finding"; "file that too" → "open a separate GitHub issue for that finding") are identifiable from surrounding context. Implementation is deterministic text replacement. ACCEPT. |

## MVP Experiment Designs

15 experiments designed (EXP-001 through EXP-015). Key highlights:

**EXP-001 One-question survey** (2 days, 5 devs): "Which describes how you installed Jerry? (A) Plugin via Claude Code (B) Cloned repo (C) Not sure." Tests A-003. Success: ≥80% A/B not C.

**EXP-002 Paper prototype** (3 days, 3 devs): Present revised Step 3 with "Choose your path"; think-aloud. Success: ≥2/3 self-route correctly without prompting.

**EXP-003 Think-aloud** (1 week, 5 users): Update version refs + "minor differences OK" note; 5 users complete INSTALLATION.md via think-aloud session. Success: 3 of 5 users (60%) complete Step 4 within 15 minutes without verbalizing version-compatibility uncertainty. PARTIAL_VALIDATED threshold: 2 of 5 users complete (requires iter-2 protocol adjustment — recruit 5 additional users before proceeding). FAIL: 1 of 5 or fewer complete Step 4, or ≥3 of 5 users verbalize version-compatibility pause. (Method changed from passive smoke test to think-aloud: passive smoke test cannot observe pause-to-verify behavior or attribute denominator.)

**EXP-004 Fake door test** (1-2 weeks): Add "Tutorial coming soon" stub to docs/index.md Guides. Success: ≥5% CTR — validates demand before authoring.

**EXP-005 Paper prototype** (2 days): Two INSTALLATION.md versions (current vs. SSH-check-moved-earlier). Success: Version B 100% confident self-selection.

**EXP-006 Smoke test + follow-up survey** (2 weeks + 3-question survey, 5 devs): Replace marketing voice in INSTALLATION.md/docs/index.md; ask 5 users to complete install and answer 3-question survey on instruction clarity. Success: Criterion 1 (primary): ≥3 of 5 users (60%) rate INSTALLATION.md instructions as "clear" or "very clear" on a 5-point scale AND ≤1 of 5 users expresses any concern about clarity or completeness in the post-task survey (regression guard — prior-iteration survey data is NOT required; this is a within-test regression signal). Criterion 2 (supplementary signal — informs severity assessment when criterion 1 is borderline): ≤1 of 5 users provides explicit "confusing" feedback. Criterion 2 serves as a redundant confirmation signal: PASS requires criterion 1 only. Borderline disposition rule: if criterion 1 is borderline (exactly 1 user expresses concern) AND criterion 2 is also violated (at least 1 explicit "confusing" feedback), disposition is CONDITIONAL REVISE — recruit 2 additional users and re-run the survey before implementing. If criterion 1 is borderline AND criterion 2 is not violated, disposition is CONDITIONAL PASS — proceed with implementation but flag for post-deployment check at 2-week mark. FAIL condition: fewer than 3 of 5 users rate instructions clearly, OR ≥2 of 5 users express concern about clarity or completeness (criterion 1 FAIL); when criterion 1 is FAIL, criterion 2 is irrelevant — FAIL stands regardless. A single "confusing" response (criterion 2 violation alone) does not constitute FAIL — it modifies the borderline criterion 1 outcome only.

**EXP-007 Concierge MVP** (1 week): Walk 2-3 new users through tutorial via screen-share before authoring. Success: ≥2/3 reach first invocation in 20 min; top 3 friction points documented. Failure exit condition: if <2/3 users reach first successful skill invocation within 20 min, BEFORE escalating to scope reduction review document friction points from this session in a structured post-session memo (template fields: session-id, step-number, observed friction, user verbalization, interpretive note). This friction memo feeds (a) the scope reduction decision (what to simplify or remove) and (b) the HYP-001 (Step 3 branching) and HYP-003 (SSH prerequisite order) evidence chains regardless of second-session outcome. Then escalate to tutorial scope reduction review — propose either (a) shorter initial tutorial focused on 1 skill only, or (b) prerequisite check/installer improvement to remove pre-tutorial friction; run a second concierge session with revised scope before committing to full Wave 4a authoring. Second-session failure terminal rule: if after scope reduction review AND second 20-min concierge session, still <2/3 reach first successful invocation, HALT Wave 4a tutorial authoring entirely. Escalate to framework-level remediation scope expansion (prerequisite automation, CLI UX redesign, or infrastructure investment). Document specific friction points from both sessions as inputs to HYP-001 (Step 3 branching) and HYP-003 (SSH prerequisite order) experiments. Tutorial format is not the appropriate intervention and cannot be salvaged by content iteration alone at this point; the friction originates from product Ability barriers, not documentation structure gaps.

**EXP-008 One-question survey** (3 days, 8-15 devs): "Search for UX eval: (A) /user-experience (B) specific sub-skill (C) SKILL.md." Tests A-013. Success: ≥60% consensus on any single option → organizational direction clear for Wave 4b. Three-branch contingency for sub-threshold outcomes:
- **Branch A — Clear winner (≥60%):** Organize Wave 4b per plurality; proceed immediately.
- **Branch B — Plurality (40–59% on one option):** Use plurality option as default organization; run one additional 5-user think-aloud validation round before committing Wave 4b structure; disclose ambiguity in Wave 4b how-to doc header.
- **Branch C — Split (no option exceeds 39%):** Default to problem-domain organization (aligns with /user-experience orchestrator architecture); publish ambiguity disclosure note; schedule post-launch usability testing (EXP-016, planned not designed). Wave 4b authoring proceeds with problem-domain structure but is explicitly flagged for post-launch reorganization review.
FAIL: EXP-008 cannot produce a hard FAIL — it always produces a direction. The three branches ensure no result creates Wave 4b paralysis.

**EXP-009 Smoke test + AT interview** (1 day implementation + AT interview with 3-5 screen-reader users): Add language specifiers to 20+ code blocks. Success: (1) grep verification confirms language specifiers present on 100% of code blocks (implementation completeness — deterministic); AND (2) 2 or more of 3-5 AT users interviewed report improved or equivalent screen-reader experience when navigating language-specified blocks vs. baseline; 0 AT users report degraded experience. FAIL: fewer than 2 AT users report improvement, OR any AT user reports degraded experience, OR grep verification is <100%. (Removes "any positive feedback = VALIDATED" — that criterion was unfalsifiable; a single comment would have validated regardless of harm to other users.)

**EXP-010 Smoke test** (30 min + 1 week): Add README nav table. Success: table present; SC 3.2.3 PASS on re-audit.

**EXP-011 Paper prototype** (2 days, 3 devs): Multi-surface vs. deduplicated "What is Jerry?". Success: ≥2/3 consistent descriptions in deduplicated version.

**EXP-012 Smoke test** (1 hr + MkDocs build): Convert INSTALLATION.md bold steps to H3. Success: rendering correct; SC 1.3.1 PASS.

**EXP-013 A/B interview** (2 weeks, 6 users — 3 per variant): Add motivational payoff sentence at JERRY_PROJECT export step; compare variant vs. control with 6 users across 3-question post-install survey. Success: PRIMARY (infrastructure-independent): ≥2 of 3 variant users rate the JERRY_PROJECT export step as "manageable" or better vs. ≤1 of 3 in control (A/B comparison via interview). SECONDARY (if analytics available): +15% click-through from Getting-Started or completion rate past Step 2 vs. control. PASS on either dimension constitutes VALIDATED; both failing constitutes FAIL. AND no regression (variant performs no worse than control on the primary dimension). (Removes "any positive feedback = VALIDATED" — that criterion was unfalsifiable; replaces with minimum-threshold bilateral criteria.) Pre-registration note — no-differential-effect case: if control baseline also achieves ≥2/3 "manageable" (both groups independently pass the primary threshold), interpret as "motivational payoff sentence had no differential effect vs. baseline at this severity level; JERRY_PROJECT export step is more manageable than hypothesized." Outcome: HYP-012 LOW confidence confirmed; motivational sentence adds marginal value; deprioritize HYP-012 relative to other backlog items. Tie-break rule: if both groups independently achieve the PRIMARY threshold (≥2/3 each), apply the TASK DIMENSION CLASSIFICATION RULE to determine disposition. Step 1 — Dimension taxonomy: classify each stated positive reason into one of the following pre-registered task dimensions: (D1) Brevity/conciseness of instruction, (D2) Motivational tone or encouragement, (D3) Instructional clarity of steps, (D4) Technical accuracy/completeness, (D5) Other/unclassifiable. Step 2 — Coder agreement: require 2-of-3 independent coders to agree on the dimension assignment for each reason; disagreement on any reason defaults that reason to D5. Within-group aggregation: when determining each group's 'top reason', use plurality of coded reasons (e.g., 2/3 users in D2 → D2 is top). If all coded reasons are different (1-1-1 split with no plurality), top reason defaults to D5 (Other/unclassifiable) and disposition defaults to INCONCLUSIVE regardless of the other group's result. Step 3 — Disposition rule: CONVERGING = both groups' top positive reason maps to the SAME dimension (D1–D4) — the variants are interchangeable on the same user value; disposition is SHIP CONTROL (simpler variant preferred). ADDITIVE = each group's top positive reason maps to a DIFFERENT dimension (e.g., variant A top reason = D1, variant B top reason = D2) — the variants address complementary user needs; disposition is SHIP BOTH as accessible options. INCONCLUSIVE = either group's top positive reason lands in D5 (unclassifiable) or coder agreement is below 2-of-3 for both groups; disposition is run EXP-013b at n=10 before committing. Pre-registration: document all 5 task dimensions in the EXP-013 session protocol before data collection begins so classification is checkbox-level at results-time.

**EXP-014 Fake door** (2 weeks): Stub entries for hooks-architecture + context-architecture. Success: ≥3% CTR validates demand.

**EXP-015 Smoke test** (10 min): Replace "file it"/"file that too" with descriptive. Success: SC 2.4.4 PASS.

## ICE Prioritization Matrix

| Rank | ID | ICE | Priority Band | Rationale |
|------|-----|-----|---------------|-----------|
| 1 | HYP-002 | 8.3 | **P1 Immediate** | Highest confidence + ease. ~15 min. No experiment gate. |
| 2 | HYP-004 | 8.0 | **P1 Immediate** | F-001 Sev 3 HIGH. Low-effort fix. All new users affected. C reduced to 7 (no measurement baseline for discovery rate). Risk acceptance: A-009 Q1 Unknown (trust reduction from sparse table) accepted at P1 — ≥5 corroborating skill-discovery signals (F-001, F-002, cross-reference double-convergence) justify proceeding without experiment gate; change is non-destructive and reversible. Rollback path: if post-deployment user interviews reveal trust reduction attributable to sparse table, revert to partial-visibility skill table with explicit "selected skills shown — see AGENTS.md for full list" framing. |
| 3 (tie) | HYP-011 | 7.7 | **P1 Immediate** | W-001 Sev 3 HIGH. ~1 hr. Structural — no experiment. |
| 3 (tie) | HYP-014 | 7.7 | **P1 Immediate** | W-002 Sev 3 HIGH. ~10 min. Deterministic WCAG. |
| 5 | HYP-009 | 7.0 | **P1 Immediate** | W-005 HIGH. ~30 min. |
| 6 (tie) | HYP-003 | 6.7 | **P2 Validate first** | F-005 moderate. EXP-005 first. |
| 6 (tie) | HYP-005 | 6.7 | **P2 Validate first** | Structural strong but subjective. EXP-006 first. |
| 8 (tie) | HYP-006 | 6.0 | **P3 Experiment first** | Long-term impact, 4-8hr investment. EXP-004+EXP-007 validate first. |
| 8 (tie) | HYP-010 | 6.0 | **P2 Validate first** | Medium effort/confidence. EXP-011 validates mental model. |
| 10 (tie) | HYP-001 | 5.7 | **P3 Experiment first** | Revised: I reduced 9→6 (Q1 Unknown A-001; no baseline). C reduced 7→5. Run EXP-001+EXP-002 before investing in restructure. |
| 10 (tie) | HYP-008 | 5.7 | **P2 Validate first** | W-006 Sev 2 MEDIUM. E reduced 9→6 (Ease includes validation effort, not just implementation). Deterministic WCAG proxy accepted for implementation dimension; behavioral dimension requires AT interview. |
| 12 (tie) | HYP-007 | 5.3 | **P3 Experiment first** | No user data. EXP-008 before Wave 4b. Wave 4b authoring blocked until EXP-008 complete. |
| 12 (tie) | HYP-012 | 5.3 | **P2 Low-effort test** | Very low confidence. Redesigned EXP-013 A/B with bilateral criteria. |
| 14 | HYP-013 | 5.0 | **P3 Validate demand** | Significant authoring. EXP-014 fake door first. |

**P1 Immediate total effort:** ~3.5 hours for 5 hypotheses (HYP-002, HYP-004, HYP-009, HYP-011, HYP-014).

**ICE re-scoring note (iter-2):** HYP-001 I: 9→6 and C: 7→5 (C3 + M2 — Q1 Unknown A-001 forces lower-score-when-uncertain per P-022). HYP-004 C: 8→7 (M1 — no measurement baseline for discovery rate). HYP-008 E: 9→6 (M7 — Ease includes experiment validation effort, not just implementation effort).

**ICE tie-breaking rule (iter-3):** When ICE scores tie (e.g., HYP-001 and HYP-008 both at 5.7), hypotheses with WCAG/structural proxy paths to validation are ranked P2 (can begin near-term remediation work with proxy signals while awaiting user validation). Hypotheses without proxy paths remain P3 (gated on Phase 1b JTBD or baseline measurement). HYP-008 has a WCAG code-block ARIA proxy (grep + re-audit deterministically confirms implementation; AT interview validates behavioral dimension) → P2. HYP-001 has no proxy for A-001 abandonment rate (baseline unmeasurable without analytics infrastructure) → P3.

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

HYP-001 revised to ICE=5.7 (P3 Experiment-first) after applying lower-score-when-uncertain rule to both I and C dimensions (Q1 Unknown A-001 holds no baseline abandonment rate). B=MAP establishes structural evidence of a problem; EXP-001 + EXP-002 must run before full Step 3 restructure investment. The strategic narrative shift is significant: HYP-001 is not a near-P1 item but a P3 item requiring experiment validation before implementation commitment.

### Pattern 3: Wave 4 Needs Demand Validation Before Authoring

Tutorial (HYP-006) and explanation docs (HYP-013) = 4-8hr authoring. Fake door experiments (EXP-004, EXP-014) = 30-min tests prevent wasting on content no one navigates to.

### Pattern 4: How-To Organization Is Wave 4b Riskiest Unknown

HYP-007 lowest confidence (3/10). No user data. EXP-008 3-day survey resolves Wave 4b structure direction via 3-branch contingency (see EXP-008 design). **First Wave 4b action.**

**Wave 4b Authoring Lockout (M8):** Wave 4b how-to authoring is BLOCKED until EXP-008 results are available and the contingency branch is determined. Only EXP-008 setup itself (3 days survey) qualifies as Wave 4b work in the interim. This constraint propagates to all downstream wave planning. Rationale: if Wave 4b authoring begins before EXP-008 results, the entire EXP-008 exercise becomes post-hoc rationalization rather than a genuine direction-setter. The parallel-execution velocity plan (Weeks 1-2) applies to Wave 2/3 remediation only; Wave 4b is explicitly gated.

### Experimentation Maturity: Nascent → Developing

**Current:** No measurement infrastructure, no funnel data. All audits structural/heuristic.
**Target:** Developing via EXP-002 Step 3 completion rate, EXP-004 tutorial demand, EXP-008 org preference.

**Velocity:** Weeks 1-2 execute all P1 structural fixes while running EXP-001 + EXP-008 in parallel (both 2-3 day surveys). Wave 2/3 remediation proceeds while Wave 4 validation runs concurrently.

## Synthesis Judgments Summary

| Judgment | Confidence | Rationale |
|----------|-----------|-----------|
| HYP-001 ICE=5.7 (I=6, C=5) — iter-2 revised | HIGH | Lower-score-when-uncertain rule applied: I reduced 9→6 (A-001 Q1 Unknown; no baseline abandonment rate makes I=9 internally inconsistent). C reduced 7→5 (C=7 with riskiest Q1 assumption contradicts own methodology). ICE cascade: (6+5+6)/3=5.7, P3 band. |
| HYP-002 P1 without experiment gate | HIGH | Version refs: 3-source evidence, ~15 min, zero contrary. Think-aloud EXP-003 recommended; method upgraded from smoke test to think-aloud for behavioral measurability. |
| HYP-004 C reduced 8→7; "50%+" removed | HIGH | P-022: no measurement baseline for discovery rate; "50%+" claim was unsupported. C=7 reflects strong heuristic evidence without prior empirical baseline. ICE: (9+7+8)/3=8.0. |
| A-001 Q1 (Step 3 abandonment unknown) | HIGH | Absence of funnel data definitively unknown. Placement correct. |
| A-006 reclassified Q1→Q2 | MEDIUM | Causal mechanism theoretically grounded in Diataxis literature (accepted at C4). Behavioral magnitude unknown, but causal direction established. Q2 MONITOR is correct; Q1 TEST FIRST overstates uncertainty. Validation required on magnitude; causal direction accepted. |
| A-013 Q1 (domain vs skill-name mental model) | MEDIUM | No user research. Could be Q4 if UX usage negligible — but 10/30 skills UX. Three-branch EXP-008 contingency added; Wave 4b lockout added. |
| HYP-007 ICE=5.3 | LOW | No user data. Score reflects honest uncertainty. Three-branch contingency prevents paralysis. |
| HYP-008 E reduced 9→6 | HIGH | Ease conflation corrected: Ease includes experiment validation effort (AT interview), not just implementation effort (grep). Effective E=6. No ICE band change relative to other P2 items; explicit footnote added per M7. |
| EXP-006/EXP-009/EXP-013 falsifiability — iter-2 revised | HIGH | All three redesigned with concrete PASS/FAIL thresholds and bilateral criteria (specific population numerators, minimum thresholds, explicit FAIL conditions). Unfalsifiable "any positive = VALIDATED" pattern removed. |
| EXP-003 denominator — iter-2 revised | HIGH | Method upgraded from passive smoke test to think-aloud; 60% threshold pre-registered as 3 of 5 with explicit PARTIAL_VALIDATED (2/5) and FAIL (1/5) zones. Ambiguous zone action path documented. |
| P1 band (immediate no gate) | HIGH | Only HIGH-confidence WCAG/structural findings remain in P1 (HYP-002, HYP-004, HYP-009, HYP-011, HYP-014). HYP-008 moved from P1 to P2 Validate-first; HYP-001 moved from P2 to P3. HYP-009 contains two separable claims: (a) deterministic WCAG compliance — H-23-compliant nav table structure is verifiable via re-audit (SC 3.2.3 PASS/FAIL), HIGH confidence; (b) behavioral navigation improvement for motor/keyboard users — HYPOTHETICAL behavioral claim, MEDIUM confidence pending user testing. P1 Immediate assignment is justified on claim (a); claim (b) is assumed from structural W-005 evidence at this severity level but is not independently validated. No separate behavioral experiment required at Sev 2 level. |

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
assumptions_mapped: 26  # iter-5: A-016 split into A-016a (Q3) + A-016b (Q1); net +1 entry; iter-6 correction applied to q1_assumptions (see below)
q1_assumptions: 11  # iter-6 correction: count adjusted from 9 to 11 (A-010, A-012 from HYP-006 were omitted from tracker since iter-1)
experiments_designed: 15
cycles_completed: 0
degraded_mode: true
artifact_path: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-007/ux-lean-ux-facilitator-output.md
handoff_hypotheses_count: 0
blockers:
  - "[PERSISTENT] Wave 4b how-to authoring blocked pending EXP-008 results. Only EXP-008 setup (3-day survey) qualifies as Wave 4b work in the interim. Three-branch contingency documented in EXP-008 design."
iteration: 6
```

## Revision History

| Iteration | Date | Verdict | Score | Changes |
|-----------|------|---------|-------|---------|
| 1 | 2026-04-20 | REJECTED (0.84) | 0.84 | Initial delivery |
| 2 | 2026-04-20 | REJECTED (0.873) | 0.873 (adv) | C1 (IN-001): EXP-006/EXP-009/EXP-013 redesigned with falsifiable bilateral criteria and explicit FAIL conditions. C2 (PM-001): EXP-003 upgraded from passive smoke test to think-aloud; denominator pre-registered as 3/5 with PARTIAL_VALIDATED (2/5) and FAIL (1/5) zones. C3 (FM-001): HYP-001 I reduced 9→6; ICE cascade to 5.7; rank moved from P2 to P3. M1 (CC-001): HYP-004 "50%+" claim removed; C reduced 8→7; ICE 8.3→8.0. M2 (CC-002): HYP-001 C reduced 7→5 (cascades with C3). M3 (DA-001): HYP-003/HYP-005/HYP-007/HYP-010 full canonical format restored with "We believe … for [users] … if … because …" all components present. M4 (DA-002): A-006 reclassified Q1→Q2 with Diataxis literature rationale; q1_assumptions reduced from 6 to 5. M5 (PM-002): EXP-009 behavioral criterion replaced with bilateral AT-interview threshold (2+ of 3-5 users improved; 0 degraded). M6 (PM-003): EXP-008 three-branch contingency added (clear winner / plurality / split) with explicit action paths preventing Wave 4b paralysis. M7 (FM-002): HYP-008 E reduced 9→6 with footnote on Ease dimension definition. M8 (IN-002): Wave 4b authoring lockout added to Strategic Implications and On-Send YAML as [PERSISTENT] blocker. |
| 3 | 2026-04-20 | Under review | 0.90 (self) | CC-004 (Major): EXP-006 time-on-page regression guard removed; replaced with survey-observable proxy "≤1 of 5 users expresses any concern about clarity or completeness in post-task survey" (within-test regression signal; no analytics baseline required). PM-004 (Minor): EXP-013 click-through demoted to SECONDARY (infrastructure-conditional); PRIMARY is now interview-based (≥2/3 variant users rate step "manageable" or better). PASS on either dimension constitutes VALIDATED. DA-004 (Minor): ICE tie-breaking footnote added to ICE Prioritization Matrix: WCAG/structural proxy path → P2; no proxy path → P3; explains HYP-001 P3 vs. HYP-008 P2 at equal ICE=5.7. FM-003 (Minor): EXP-007 failure exit added — <2/3 users in 20 min escalates to tutorial scope reduction review (shorter 1-skill tutorial or prerequisite friction removal) + second concierge session before full Wave 4a authoring commitment. IN-003 (Minor): HYP-009 Synthesis Judgments row revised to distinguish (a) deterministic WCAG compliance claim (HIGH confidence, verifiable via re-audit) from (b) behavioral navigation improvement claim (MEDIUM confidence, HYPOTHETICAL pending user testing); P1 assignment justified on (a); (b) assumed from W-005 structural evidence at Sev 2 level. |
| 4 | 2026-04-20 | Revised | 0.90 (self-est) | PRIMARY (Completeness): Assumption maps added for HYP-009 (A-015 through A-017), HYP-012 (A-018 through A-020), HYP-013 (A-021 through A-023), HYP-014 (A-024 through A-025) — 11 new assumption entries covering H-23/H-24 compliance, motor/keyboard navigation behavior, WCAG 2.4.10 interpretation, motivation intervention type, n=3 per variant limitation, demand navigation discovery, and link text determinism. ONSEND-ITER-F040007 (Minor): On-Send Protocol YAML `iteration:` updated from 2 → 4 (corrects stale counter flagged in iter-3 review). EXP013-BASELINE-F040007 (Minor): EXP-013 pre-registration note added for no-differential-effect case — both groups independently achieving ≥2/3 primary threshold interpreted as "no differential effect"; tie-break rule added (converging qualitative reasons → ship both variants; diverging reasons → INCONCLUSIVE → EXP-013b at n=10). EXP007-DOUBLE-FAIL-F040007 (Minor): EXP-007 second-session failure terminal rule added — second concierge failure HALTS Wave 4a; escalates to framework-level remediation; friction points feed HYP-001/HYP-003. EXP006-DUAL-F040007 (Minor): EXP-006 criterion 2 role clarified — redundant confirmation signal; PASS requires criterion 1 only; criterion 2 informs severity when criterion 1 borderline; standalone criterion 2 violation does not constitute FAIL. |
| 5 | 2026-04-20 | Under review | 0.921 (self) | DA-005-F040007 (Minor): EXP-013 tie-break rule replaced example-level language with OPERATIONAL CLASSIFICATION RULE — pre-registered 5-dimension taxonomy (D1 Brevity, D2 Motivational tone, D3 Instructional clarity, D4 Technical accuracy, D5 Other); 2-of-3 coder agreement required per reason; CONVERGING/ADDITIVE/INCONCLUSIVE disposition determined by dimension match pattern; pre-registration of dimension taxonomy required before data collection. DA-006-F040007 (Minor): EXP-007 first-session failure exit extended — structured post-session friction memo (template: session-id, step-number, observed friction, user verbalization, interpretive note) required BEFORE proceeding to scope reduction review; memo feeds scope reduction decision AND HYP-001/HYP-003 evidence chains regardless of second-session outcome. CC-005-F040007 (Minor): EXP-006 criterion 2 borderline disposition specified — criterion 1 borderline + criterion 2 violated = CONDITIONAL REVISE (recruit 2 additional users); criterion 1 borderline + criterion 2 not violated = CONDITIONAL PASS (proceed with 2-week post-deployment flag); criterion 1 FAIL renders criterion 2 irrelevant. PM-005-F040007 (Minor): HYP-004 P1 ICE row — explicit A-009 Q1 risk acceptance added: ≥5 corroborating signals justify P1 without experiment gate; rollback path documented (partial-visibility table with "selected skills" framing if trust regression observed). IN-004-F040007 (Minor): A-016 split into A-016a (Q3 — WCAG 2.4.10/2.4.1 architectural obligation, ACCEPT) and A-016b (Q1 — behavioral navigation benefit for motor/keyboard users, TEST FIRST); WCAG citations now correctly scoped to architectural dimension only; behavioral claim explicitly labeled as independent Q1 unknown. On-Send YAML: iteration 4→5, assumptions_mapped 25→26 (A-016 split net +1 entry). |
| 6 | 2026-04-20 | Under review | 0.927 (self-projected) | TR-001-F040007 (Mechanical): On-Send YAML q1_assumptions corrected 9→11 with correction note comment — A-010 (/problem-solving as right first skill, HYP-006) and A-012 (tutorial absence causal to low first-invocation, HYP-006) were present in assumption maps since iter-1 but omitted from tracker count. DA-007-F040007 (Mechanical): EXP-013 tie-break rule — within-group aggregation sentence added specifying plurality rule for determining each group's top coded reason; 1-1-1 split (no plurality) defaults top reason to D5 (Other/unclassifiable) and disposition to INCONCLUSIVE regardless of other group's result. No structural changes. All iter-5 closures preserved verbatim. |

---

*Agent: ux-lean-ux-facilitator v1.1.0 | FEAT-040-007 | 2026-04-20 | Lean UX: Gothelf & Seiden 2021 | ICE: Ellis/GrowthHackers ~2015 | Degraded mode: no Miro MCP*
