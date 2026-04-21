# Adversarial Review Report: FEAT-040-001 JTBD Analysis (Iteration 1)

> **Feature:** FEAT-040-001
> **Agent Reviewed:** ux-jtbd-analyst v0.2.0
> **Deliverable:** `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-001/ux-jtbd-analyst-output.md`
> **Criticality:** C3 (Wave 1 Discovery DAG root)
> **Threshold:** >= 0.92 | Self-reported: 0.92 | Self-reported confidence: 0.75
> **Strategies executed:** S-007, S-002 (S-003 skipped per C3 per-feature optional rule), S-004, S-012, S-013, S-014 sanity complement
> **H-16 compliance note:** S-003 not run; S-002 executed alone. H-16 constraint satisfied because S-003 is optional at C3 per-feature and the ordering rule ("S-003 MUST precede S-002 **if both run**") was not triggered.
> **Reviewer:** adv-executor
> **Date:** 2026-04-17

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Verdict, top blockers, cascading risk |
| [S-007: Constitutional AI Critique](#s-007-constitutional-ai-critique) | HARD rule and governance compliance |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against key claims |
| [S-004: Pre-Mortem Analysis](#s-004-pre-mortem-analysis) | Future failure causes |
| [S-012: FMEA](#s-012-fmea) | Component-level failure mode enumeration |
| [S-013: Inversion Technique](#s-013-inversion-technique) | Anti-goal and assumption stress-testing |
| [S-014: LLM-as-Judge Sanity Complement](#s-014-llm-as-judge-sanity-complement) | Dimensional scoring estimate |
| [Consolidated Finding Register](#consolidated-finding-register) | All findings by severity |
| [Revision Recommendations](#revision-recommendations) | Actionable per-finding guidance |
| [Verdict and Score Estimate](#verdict-and-score-estimate) | PASS / REVISE / REJECT |

---

## Executive Summary

The JTBD analysis is structurally well-formed, methodologically documented, and honest about its secondary-research limitations. Its self-reported MEDIUM confidence is appropriate. However, three significant issues threaten the reliability of the downstream Phase 1b handoff data (XP-01, XP-01b, XP-02, XP-04):

1. **Opportunity score methodology is undocumented and unreproducible.** The Importance and Satisfaction values that generate Opp scores (15, 14, 12, 13, 11) are stated but never derived. No rater can verify them. Downstream Kano (XP-01) and Positioning (XP-04) will treat these numbers as ODI-quality data — they are not.

2. **Job distinctness fails probe 1: three SDLC skills collapse to a single job.** `/test-spec`, `/contract-design`, and `/use-case` share the same core situation, motivation, and outcome — "I have upstream artifacts and need downstream artifacts." The analysis treats them as three distinct jobs to hit the 30-skill count, but this conflates skill boundary with job boundary. The pipeline IS the job, not each skill.

3. **The "switch from vanilla Claude Code" claim is stated as a universal fact across all 30 skills.** It is plausible for Category 1 skills but is untested and potentially wrong for Category 3 (UX methodology) and Category 5 (professional domains). Domain specialists switching to Jerry's UX skills are more likely switching from Figma + Notion + their own methodology templates — not from unstructured Claude. Stating the switch trigger as universal overstates the evidence.

**Cascading risk:** This deliverable is the DAG root for XP-01, XP-01b, XP-02, XP-04. Weak opportunity scores propagate directly into Kano feature prioritization and into positioning messaging. A Major revision here prevents four downstream features from inheriting flawed foundational data.

**Verdict: REVISE**

---

## S-007: Constitutional AI Critique

**Finding Prefix:** CC | **Execution ID:** r1-20260417

### Applicable Principles Evaluated

| Principle | Tier | Applicable | Rationale |
|-----------|------|-----------|-----------|
| P-001 (Truth/Accuracy) | HARD | Yes | Analytical deliverable making factual claims |
| P-022 (No Deception) | HARD | Yes | Confidence must match evidence |
| P-020 (User Authority) | HARD | Yes | Worker agent; no user-override risk |
| P-003 (No Recursion) | HARD | Yes | Worker agent compliance |
| H-15 (Self-Review) | HARD | Yes | Deliverable self-review before presentation |
| H-17 (Quality Scoring) | HARD | Yes | C3 requires quality scoring |
| P-011 (Evidence-Based) | MEDIUM | Yes | Every claim must cite evidence |
| NAV-001 (Navigation table) | HARD | Yes | 30+ line document |
| H-23 (Anchor links) | HARD | Yes | Navigation table present |

### Findings

**CC-001-r1 [Minor]**
- **Principle:** P-001 (Truth/Accuracy)
- **Location:** L2: Top 5 Job Categories — Opportunity Score formula
- **Evidence:** "Opportunity Score (inferred): Importance=9, Satisfaction=3 → Score=9+max(9-3,0)=15 (UNDERSERVED)" — The formula `Importance + max(Importance - Satisfaction, 0)` is presented without sourcing. Ulwick's canonical ODI formula is `Importance + (Importance - Satisfaction)` when Satisfaction < Importance, which gives the same result only if both agree. However, the Importance=9 and Satisfaction=3 figures themselves are undocumented — they appear without derivation, SKILL.md reference, or any other verifiable source.
- **Severity:** Minor (claim is disclosed as "inferred" in Synthesis Judgments §3, but the disclosure is buried; the L2 section presents the numbers as if computed from data)
- **Dimension:** Evidence Quality

**CC-002-r1 [Minor]**
- **Principle:** P-001 (Truth/Accuracy)
- **Location:** L0 Executive Summary — "16 of 30 skills have zero documentation coverage"
- **Evidence:** The executive summary states 16 skills have zero coverage. The per-skill table summary (line 132-138) states 26 skills have `doc-gap: none` and 4 have `partial-how-to`. 16 + 14 does not equal 30; 26 + 4 = 30. The L0 number (16) contradicts the L2 number (26).
- **Severity:** Major — This is a factual internal inconsistency in the most-consumed section (L0) of the DAG-root deliverable. Downstream consumers reading only L0 will carry wrong coverage data into XP-01/XP-01b.
- **Dimension:** Internal Consistency

**CC-003-r1 [Compliant]**
- **Principle:** P-022 (No Deception)
- **Evidence:** The deliverable consistently labels confidence as MEDIUM, includes a Synthesis Judgments Summary with 9 explicit AI inference disclosures, and includes a Validation Required table. The agent correctly reports P-003/P-020/P-022 compliance in the footer. COMPLIANT.

**CC-004-r1 [Compliant]**
- **Principle:** P-003 (No Recursion)
- **Evidence:** Footer states "P-003 (no sub-agents dispatched)." No evidence of subagent invocation in a document-only deliverable. COMPLIANT.

**CC-005-r1 [Compliant]**
- **Principle:** NAV-001 / H-23
- **Evidence:** Navigation table present at document top with anchor links. All major sections covered. COMPLIANT.

### Constitutional Score

- Critical violations: 0
- Major violations: 1 (CC-002)
- Minor violations: 1 (CC-001)
- Score: `1.00 - (0 × 0.10 + 1 × 0.05 + 1 × 0.02)` = **0.93** → PASS constitutional gate

---

## S-002: Devil's Advocate

**Finding Prefix:** DA | **Execution ID:** r1-20260417
**H-16 note:** S-003 not run; S-002 executing against original deliverable as permitted by C3 per-feature optional rule.

### Step 1: Role and Scope

Deliverable under challenge: ux-jtbd-analyst-output.md — JTBD analysis for 30 Jerry skills.
Central claims under challenge: (1) 30 skills yield 30 distinct jobs, (2) six actor segments are the right segmentation, (3) "switch from vanilla Claude" is the universal trigger, (4) opportunity scores rank the categories correctly, (5) the analysis is MEDIUM confidence throughout.

### Step 2: Challenged Assumptions

| # | Assumption | Challenge |
|---|-----------|-----------|
| A1 | Each skill = one distinct job | Probe 1: multiple skills may share the same job |
| A2 | SKILL.md descriptions = user intent signals | SKILL.md is authored by framework builders, not users — it reflects intended use, not revealed use |
| A3 | Skill count = user demand signal (ranking criterion) | Skill count reflects framework investment decisions, not usage frequency |
| A4 | All users switch FROM vanilla Claude Code | Domain specialists and security practitioners may have completely different prior solutions |
| A5 | Opportunity scores are derived from the same source tier as job statements | Opportunity scores require I/S data from users; no users were consulted |

### Findings

**DA-001-r1 [Major]**
- **Claim:** "30 skills — 30 distinct jobs"
- **Counter-argument:** `/test-spec` (Row 16), `/contract-design` (Row 5), and `/use-case` (Row 18) share the same situational frame ("When I am elaborating/building a feature") and the same motivation/outcome structure ("produce traceable software artifacts"). The three job statements differ only in the input artifact name. If the user's actual job is "traverse the use-case-to-API pipeline," then documenting it as three separate jobs inflates job diversity artificially and misrepresents the hiring unit. The Category 2 analysis actually acknowledges this is a pipeline — but the per-skill job statements pretend it is three independent hires.
- **Evidence:** Compare Row 5, 16, and 18 job statements: all three begin in the same situation (building a feature), hire for the same outcome (traceable artifacts), and differ only in technology. The Category 2 description explicitly calls this a "connected pipeline."
- **Dimension:** Methodological Rigor
- **Affected downstream:** XP-01 Kano — if these are classified as separate jobs, the Kano survey will double-count satisfaction signals for a single pipeline job.

**DA-002-r1 [Major]**
- **Claim:** "Users switch FROM unstructured vanilla Claude Code prompting" — stated as the universal switch trigger (key_finding[2], L0, Switch Force Analysis for all 5 categories)
- **Counter-argument:** For Category 3 (UX Methodology Suite), the actor is A6 Domain Specialist — a UX practitioner, PM, or technical writer. These users typically have existing methodology tools (Notion templates, Figma FigJam, Miro boards, established PM processes). The "switch from vanilla Claude" framing fits Category 1 and Category 4, but for professional domain practitioners the prior solution is their domain practice, not Claude. The switch trigger is different: "I want AI augmentation of MY existing methodology" not "I want to stop freestyle prompting." This distinction matters for XP-04 Positioning — the messaging to A6 is different from the messaging to A1.
- **Evidence:** A6 profile (lines 312-324): "Domain-expert, not necessarily a software engineer... Evaluates Jerry against the professional standards of their domain (Kano, JTBD, Diataxis, HEART)." A domain expert with existing methodology loyalty is NOT primarily switching from vanilla Claude prompting.
- **Dimension:** Evidence Quality
- **Affected downstream:** XP-04 Positioning — universal switch trigger will produce wrong messaging for A6 segment.

**DA-003-r1 [Major]**
- **Claim:** Skill count is a valid user demand signal (ranking criterion #1)
- **Counter-argument:** Skill count reflects framework investment by the framework authors — not user demand. Jerry has 11 UX sub-skills (Category 3 ranked #3) because a UX wave was built; it does not mean users demand UX methodology more than SDLC methodology. The ranking criterion conflates supply-side investment with demand-side hiring intent. A framework author who builds 11 UX skills may simply be interested in UX; that does not mean users are more likely to hire Category 3 over Category 2. This is a category-3 fallacy in JTBD demand-side analysis: author skill count is not user hiring frequency.
- **Evidence:** Synthesis Judgment §7 notes "A strict functional job analysis would create a separate 'Session Experience' category" and "Category ranking uses a composite criterion, not a single ODI formula." The defense acknowledges the ranking is a judgment call, but does not acknowledge that skill count is a supply-side, not demand-side, signal.
- **Dimension:** Methodological Rigor
- **Affected downstream:** XP-01 (Kano) will use category rankings to sequence which features to evaluate first. A mis-ranked #3 category could deprioritize UX features incorrectly.

**DA-004-r1 [Minor]**
- **Claim:** A3 Framework Contributor is a primary actor segment (alongside A1 and A2)
- **Counter-argument:** The L0 states "Three actor segments drive 90% of hiring intent: Solo Engineer, Technical Lead, Framework Contributor." But A3's primary skills (`ast`, `diataxis`, `saucer-boy-framework-voice`, `bootstrap`) are all internal tooling and governance skills — not user-facing skills. A3 is the framework's own development persona, not an end-user hiring Jerry for external work. Including A3 as primary alongside A1 and A2 overstates the internal-contributor segment's representativeness and risks producing XP-02 personas that are skewed toward contributor use cases at the expense of end-user use cases.
- **Evidence:** Synthesis Judgment §9 notes "`saucer-boy-framework-voice` classified as A3 Framework Contributor" and is "the only skill where the primary actor is not a skill consumer." But all of A3's primary skills share this property — they are maintenance skills, not application skills.
- **Dimension:** Completeness

**DA-005-r1 [Minor]**
- **Claim:** Force ratings (1-5) are derived from SKILL.md language patterns
- **Counter-argument:** The methodology for extracting ratings from language is not documented. How does "opens with pain state" translate to PUSH=5 vs PUSH=4? This is an uncalibrated subjective interpretation presented as systematic methodology. A second analyst using the same SKILL.md files could produce different ratings with equal justification.
- **Evidence:** Switch Force Analysis for Category 1: "PUSH (current pain) | 5 | SKILL.md Purpose sections... all lead with pain state." Category 4: "PUSH (current pain) | 5" with same rationale. Both are rated 5; the distinguishing criterion that separates 5 from 4 is not documented.
- **Dimension:** Methodological Rigor

### Summary

5 counter-arguments (3 Major, 2 Minor). The deliverable's core finding (methodology enforcement is the dominant hire reason) is sound and well-evidenced. The structural weaknesses are: (1) job granularity conflates skill boundary with job boundary for the SDLC chain, (2) switch trigger universality is overstated for domain specialist actors, (3) skill count as a demand signal is supply-side proxy. None invalidate the core thesis, but all affect downstream XP-01/XP-04 quality.

---

## S-004: Pre-Mortem Analysis

**Finding Prefix:** PM | **Execution ID:** r1-20260417

### Failure Declaration

> It is 2026-10-17. The PROJ-040 documentation sprint has been running for 6 months. The JTBD analysis from FEAT-040-001 was used as the authoritative input for Kano prioritization (XP-01), Positioning (XP-04), and Persona creation (XP-02). The project failed: the documentation produced does not match how users actually hire Jerry skills, the Kano features are misranked, and the Positioning messaging resonates with contributors but not with the target new OSS user audience. We are investigating why this happened.

### Failure Causes

**PM-001-r1 [Critical — Likelihood: High]**
- **Category:** Assumption
- **Cause:** Opportunity scores derived from inferred Importance/Satisfaction values (not from actual user data) were treated as ODI-quality data by XP-01 Kano. The Kano survey prioritized Category 1 features as "Must-be" based on Opp=15, but the Opp score was generated by assuming Importance=9 with no user validation. The Kano results are only as valid as the opportunity inputs.
- **Effect:** Kano classifications for all 30 skills are grounded in assumed rankings. If the actual user-surveyed opportunity for Category 2 (SDLC chain) is higher than Category 1, the Kano "Must-be" classification for methodology enforcement features is wrong, and the documentation is built to serve the wrong priority.
- **Dimension:** Evidence Quality
- **Likelihood:** High (no primary data will exist at XP-01 execution time; assumed values propagate as-is)

**PM-002-r1 [Major — Likelihood: Medium]**
- **Category:** Assumption
- **Cause:** Actor segments A1-A6 were derived from SKILL.md audience tables, not from actual users. The Personas deliverable (XP-02) built on these segments produces fictional personas. When documentation is written for A6 Domain Specialist as framed, it may not resonate with actual non-engineering users because the A6 profile assumptions were never tested.
- **Effect:** Documentation written for inferred personas fails engagement when users encounter it. Adoption metrics disappoint. The UX suite docs in particular target A6 heavily — if A6 does not reflect reality, 11 skill docs are miscalibrated.
- **Dimension:** Evidence Quality

**PM-003-r1 [Major — Likelihood: Medium]**
- **Category:** Process
- **Cause:** The SDLC pipeline invisibility claim ("documenting it is the highest single unlock") drives a significant documentation investment, but the claim rests on inferring user non-discovery from zero documentation coverage, not from observed user behavior. Users may already be chaining these skills from README discovery, GitHub issues, or word of mouth. If the pipeline is not actually invisible, the documentation investment is misallocated.
- **Effect:** PROJ-040 invests disproportionate effort in documenting the use-case → test-spec → contract-design chain while neglecting skills that users are actually confused about (possibly worktracker, bootstrap, or problem-solving).
- **Dimension:** Actionability

**PM-004-r1 [Major — Likelihood: Medium]**
- **Category:** Assumption
- **Cause:** Switch Force ratings for HABIT are the "lowest-evidence inferences" by the agent's own admission (Synthesis Judgment §4). If HABIT forces are underestimated (e.g., engineers deeply habituated to "write tests first without use cases"), the switch condition for Category 2 moves from BLOCKED to "harder than BLOCKED." The force balance assessment drives documentation strategy — if BLOCKED is actually STRONGLY BLOCKED, tutorial content (not just how-to) is needed.
- **Effect:** Documentation type chosen for each category may be wrong. A category assessed as "needs how-to to unblock" may actually need a tutorial because the habit force is higher than inferred.
- **Dimension:** Actionability

**PM-005-r1 [Minor — Likelihood: Low]**
- **Category:** External
- **Cause:** The 30-skill count is a snapshot. If Jerry adds 5 skills during PROJ-040 (plausible given the project's active development), the JTBD analysis is stale on completion. The deliverable has no versioning or change-trigger clause.
- **Effect:** Partial staleness of per-skill job statements if new skills launch before documentation is complete.
- **Dimension:** Completeness

### Priority Matrix

| ID | Priority | Likelihood × Severity | Action Required |
|----|---------|----------------------|----------------|
| PM-001 | P0 | High × Critical | Opportunity score derivation MUST be explicitly bounded or revised |
| PM-002 | P1 | Medium × Major | Actor segments should be marked as "hypotheses for validation" in state file key_findings |
| PM-003 | P1 | Medium × Major | Pipeline invisibility claim should be qualified; alternative evidence sources identified |
| PM-004 | P1 | Medium × Major | Habit force ratings should be explicitly flagged as lowest-confidence in key_findings |
| PM-005 | P2 | Low × Minor | Add versioning note and re-evaluation trigger (e.g., "re-run if >3 new skills added") |

---

## S-012: FMEA

**Finding Prefix:** FM | **Execution ID:** r1-20260417

### Element Decomposition

| Element | ID | Description |
|---------|-----|-------------|
| L0 Executive Summary | E1 | Compressed findings for downstream consumption |
| L1 Methodology | E2 | Framework, actor segmentation, ranking criteria |
| L2 Per-Skill Job Statements (30 rows) | E3 | Job statements, switch triggers, doc coverage |
| L2 Top 5 Job Categories | E4 | Category analysis, opportunity scores, XP signals |
| L2 Actor Segments (A1-A6) | E5 | Situational profiles |
| L2 Switch Force Analysis | E6 | Four-forces per category |
| Synthesis Judgments Summary | E7 | AI inference disclosures |
| Validation Required | E8 | Pending validation items |
| State File key_findings | E9 | Compressed handoff data for XP-01/XP-01b/XP-02/XP-04 |

### Failure Mode Register (High-RPN Items)

| FM ID | Element | Failure Mode | Effect | S | O | D | RPN | Sev |
|-------|---------|-------------|--------|---|---|---|-----|-----|
| FM-001-r1 | E1 (L0 Summary) | INCORRECT: L0 states 16 skills zero coverage; L2 states 26 skills | Downstream consumers reading only L0 carry wrong coverage figure into all 4 XP features | 8 | 10 | 7 | 560 | Critical |
| FM-002-r1 | E4 (Categories) | INSUFFICIENT: Opportunity score I/S values stated without derivation | Scores appear data-backed when they are inferred; downstream treats as ODI data | 8 | 9 | 6 | 432 | Critical |
| FM-003-r1 | E9 (State file) | INCORRECT: key_findings[4] states "26 of 30 skills have zero doc coverage" — correct, but key_findings implicitly confirms the L0 16-count as separate content | Two contradictory coverage numbers now exist in two consumed artifacts | 7 | 8 | 6 | 336 | Major |
| FM-004-r1 | E3 (Per-skill) | AMBIGUOUS: `/test-spec`, `/contract-design`, `/use-case` job statements share situational frame but are presented as three distinct jobs | XP-01 Kano survey treats them as independent features; opportunity counted three times | 7 | 7 | 7 | 343 | Major |
| FM-005-r1 | E6 (Switch Forces) | INSUFFICIENT: HABIT ratings underdocumented — no criterion distinguishes HABIT=3 from HABIT=2 | Switch condition assessments (BLOCKED vs. NET POSITIVE) are sensitive to HABIT values; ratings unverifiable | 6 | 8 | 8 | 384 | Major |
| FM-006-r1 | E5 (Actors) | INCORRECT: L0 claims "three actor segments drive 90% of hiring" as A1, A2, A3 — but A3 (Framework Contributor) hires internal governance skills, not end-user skills | Personas built on A3 as primary segment produce contributor-centric, not user-centric, documentation strategy | 7 | 7 | 5 | 245 | Major |
| FM-007-r1 | E2 (Methodology) | MISSING: No criterion documented for how SKILL.md language "intensity" maps to a numeric force rating | Force analysis is unreproducible by a second analyst | 5 | 9 | 8 | 360 | Major |
| FM-008-r1 | E4 (Categories) | AMBIGUOUS: `eng-team` counted in both Category 2 and Category 5 ("counted in Category 2 for pipeline completeness, noted here for standalone hiring by A4") | Opportunity scores for both categories may double-count this skill's demand signal | 5 | 6 | 6 | 180 | Minor |
| FM-009-r1 | E8 (Validation) | MISSING: No minimum confidence upgrade path defined for the key_findings that feed XP handoffs | Downstream XP agents don't know when to re-request updated findings from FEAT-040-001 | 4 | 7 | 7 | 196 | Minor |
| FM-010-r1 | E7 (Synthesis) | INSUFFICIENT: Synthesis Judgment §8 notes `saucer-boy` is grouped with Category 1 for "actor breadth" but this is called a precision trade-off. No signal is provided to downstream Kano about this grouping. | Kano may classify `saucer-boy` as a Must-be methodology tool rather than an Attractive engagement tool | 5 | 6 | 6 | 180 | Minor |

### RPN Summary

- RPN >= 200 (Critical): FM-001 (560), FM-002 (432) — 2 Critical failure modes
- RPN 80-199 (Major): FM-003 (336), FM-004 (343), FM-005 (384), FM-006 (245), FM-007 (360) — 5 Major
- RPN < 80 (Minor): FM-008, FM-009, FM-010 — 3 Minor

**Systemic observation:** 7 of 10 failure modes involve Elements E4 (Categories) and E2 (Methodology) — the two sections that generate the quantitative outputs downstream XP features consume. This is the highest-density failure cluster.

---

## S-013: Inversion Technique

**Finding Prefix:** IN | **Execution ID:** r1-20260417

### Goal Inventory

| Goal ID | Goal (specific) | Explicit/Implicit |
|---------|----------------|-------------------|
| G1 | Provide 30 distinct, grounded JTBD job statements for use in downstream documentation planning | Explicit |
| G2 | Rank the 30 skills into 5 categories by strategic opportunity score so XP-01/XP-01b/XP-02/XP-04 can prioritize correctly | Explicit |
| G3 | Identify actor segments with sufficient specificity for XP-02 Personas | Explicit |
| G4 | Surface the switch trigger in a form directly usable for XP-04 Positioning | Explicit |
| G5 | Flag documentation gaps in a form that helps PROJ-040 prioritize writing effort | Explicit |
| G6 | Maintain MEDIUM confidence throughout — not overstate certainty | Implicit (disclosed) |
| G7 | Provide key_findings compressed sufficiently for cross-pollination handoffs (XP-01, XP-01b, XP-02, XP-04) | Implicit (state file role) |

### Anti-Goals

**IN-001-r1 [Major]**
- **Goal inverted:** G2 — "To guarantee categories are ranked WRONG, we would: rank by proxy metrics that do not reflect user demand"
- **Anti-goal condition:** Using skill count (supply-side) as the primary demand signal guarantees rankings reflect framework author investment preferences, not user hiring intensity. Currently: Category 3 (UX, 11 skills) ranks #3 partly because of skill count. But skill count is purely a framework investment decision.
- **Current address by deliverable:** PARTIAL — Synthesis Judgment §7 acknowledges it, but the ranking itself is not recalculated without the skill-count criterion.
- **Finding:** The deliverable is vulnerable to this anti-goal. Removing skill count as a ranking criterion could change Category 3's rank.
- **Severity:** Major

**IN-002-r1 [Major]**
- **Goal inverted:** G4 — "To guarantee Positioning messaging fails, we would: produce a single universal message that ignores actor-segment differences"
- **Anti-goal condition:** key_finding[2] states the universal switch trigger as canonical for all categories. XP-04 will receive this as the single positioninganchor. But different actors switch from different prior solutions. If XP-04 uses the universal framing as-is, it produces a positioning statement that resonates with A1/A2 but alienates A6 and A4.
- **Current address:** NOT addressed — the deliverable does not provide actor-differentiated switch trigger statements; it provides one universal statement with category-level force analysis that is not surfaced in key_findings.
- **Severity:** Major

**IN-003-r1 [Critical]**
- **Goal inverted:** G7 — "To guarantee downstream XP handoffs use wrong data, we would: put contradictory numbers in the L0 summary vs. the per-skill analysis"
- **Anti-goal condition:** L0 says 16 skills zero coverage; L2 says 26 skills zero coverage. key_findings[4] says 26. L0 is the fast-consumption entry point for downstream agents and stakeholders. If an XP agent reads only the state file key_findings and cites "26 skills no coverage," but another reads the L0 and cites "16 skills no coverage," the cross-pollination data is internally inconsistent.
- **Current address:** NOT addressed — this is an active factual inconsistency in the deliverable.
- **Severity:** Critical

**IN-004-r1 [Minor]**
- **Goal inverted:** G6 — "To guarantee overconfidence, we would: state qualitative judgments in quantitative form without calibration"
- **Anti-goal condition:** Force ratings (1-5) and opportunity scores (Opp=15, 14, 12, 13, 11) are presented in numerical form. Numbers imply precision calibration that was not performed. A reader who scans the tables will perceive the analysis as more quantitative than it is.
- **Current address:** PARTIAL — Synthesis Judgment disclosures exist, but they are in a section most downstream agents will not read; the tables themselves carry no uncertainty markers.
- **Severity:** Minor

**IN-005-r1 [Minor]**
- **Goal inverted:** G3 — "To guarantee personas are wrong, we would: include internal tool users as primary personas"
- **Anti-goal condition:** A3 Framework Contributor skills are internal governance tools. Including A3 as a primary actor in the "90% of hiring intent" claim means XP-02 will model an internal user as primary when the target audience is external users building products.
- **Severity:** Minor (overlaps with DA-004, reinforced here via inversion)

### Assumption Stress-Test

| Assumption | Confidence | Inversion | Consequence if Wrong |
|-----------|-----------|----------|---------------------|
| SKILL.md descriptions reflect user intent accurately | Low (Synthesis §1) | SKILL.md reflects author intent, not user intent | All 30 job statements could be mis-framed from the user's perspective |
| Six actor segments cover the full hiring population | Medium | There may be a significant segment not covered (e.g., "enterprise team embedding Jerry") | XP-02 misses a primary user type; documentation has a gap |
| Users who hire Category 2 (SDLC chain) progress through all three skills | Medium | Most users hire `/use-case` then stop when they hit the learning curve | Pipeline opportunity is overstated; individual skill discoverability is the actual problem |
| doc-gap: none correctly identifies zero UX sub-skill coverage | High (sourced from audit) | Audit was conducted 2026-04-20; some docs may exist in development | Low risk; audit is recent and C4-approved |
| Opportunity score formula produces valid relative rankings | Low | Formula Opp = I + max(I-S,0) with inferred I and S could reverse rankings | Category rankings could be reversed, changing all downstream XP prioritizations |

**Critical assumption under stress:** The opportunity score assumption is Low confidence AND high consequence. If actual user survey data produces Importance and Satisfaction values different from the inferred values, Category 2 could rank above Category 1 or Category 4 could rank above Category 3. The entire documentation priority sequence would change.

---

## S-014: LLM-as-Judge Sanity Complement

*Note: adv-scorer will execute the authoritative S-014 pass. This section provides a pre-score estimate to identify dimensional weakness before adv-scorer runs.*

### Dimensional Assessment

| Dimension | Weight | Estimated Score | Primary Issue |
|-----------|--------|----------------|---------------|
| Completeness | 0.20 | 0.85 | DA-004 (A3 as primary actor), FM-010 (saucer-boy mis-grouped), PM-005 (no versioning trigger) reduce completeness |
| Internal Consistency | 0.20 | 0.72 | CC-002 / IN-003 / FM-001 (L0 says 16, L2 says 26 zero-coverage skills) — direct contradiction in most-consumed section |
| Methodological Rigor | 0.20 | 0.83 | DA-001 (job granularity), DA-003 (skill count as demand signal), FM-007 (force rating derivation undocumented), IN-001 (anti-goal-vulnerable ranking) |
| Evidence Quality | 0.15 | 0.80 | CC-001 / FM-002 (opportunity scores stated without derivation), DA-002 (switch trigger overstated universally), PM-001 (inferred I/S treated as data) |
| Actionability | 0.15 | 0.88 | Per-category XP signals are useful and specific; recommendation for each downstream consumer. Reduced by PM-003/PM-004 (switch condition and habit undercalibration) |
| Traceability | 0.10 | 0.92 | Strong: doc-gap flags trace to named audit source, SKILL.md references present, AI inferences disclosed in Synthesis Judgments |

**Estimated composite:**
`(0.85 × 0.20) + (0.72 × 0.20) + (0.83 × 0.20) + (0.80 × 0.15) + (0.88 × 0.15) + (0.92 × 0.10)`
= `0.170 + 0.144 + 0.166 + 0.120 + 0.132 + 0.092`
= **0.824** (pre-revision estimate)

**Primary score suppressors:**
1. Internal Consistency dimension (0.72) — the L0/L2 coverage number contradiction is a direct numerical inconsistency
2. Evidence Quality (0.80) — opportunity scores and switch trigger universality lack adequate evidence grounding
3. Methodological Rigor (0.83) — job granularity and ranking methodology have documentable weaknesses

The self-reported 0.92 score does not survive adversarial review. The Internal Consistency failure alone (L0 ≠ L2 on coverage count) suppresses the weighted composite below threshold.

---

## Consolidated Finding Register

### Critical Findings

| ID | Strategy | Finding | Dimension |
|----|---------|---------|-----------|
| CC-002-r1 | S-007 | L0 states 16 skills zero-coverage; L2 table states 26 skills zero-coverage — numerical contradiction in most-consumed section | Internal Consistency |
| FM-001-r1 | S-012 | Same L0/L2 contradiction — FMEA RPN=560, highest in analysis | Internal Consistency |
| FM-002-r1 | S-012 | Opportunity score I/S values stated without derivation; RPN=432 | Evidence Quality |
| IN-003-r1 | S-013 | L0/L2 coverage contradiction creates contradictory compressed handoff data | Internal Consistency |
| PM-001-r1 | S-004 | Inferred opportunity scores will be treated as ODI data by downstream XP-01 Kano | Evidence Quality |

### Major Findings

| ID | Strategy | Finding | Dimension |
|----|---------|---------|-----------|
| DA-001-r1 | S-002 | `/test-spec`, `/contract-design`, `/use-case` share same job; presenting as 3 distinct jobs inflates diversity | Methodological Rigor |
| DA-002-r1 | S-002 | Switch trigger universality overstated for A6 Domain Specialist segment | Evidence Quality |
| DA-003-r1 | S-002 | Skill count as demand signal is supply-side proxy, not demand-side data | Methodological Rigor |
| FM-003-r1 | S-012 | State file key_findings consistent with 26-count but creates contradiction with L0 | Internal Consistency |
| FM-004-r1 | S-012 | SDLC pipeline skills treated as 3 independent jobs in per-skill table; counted as 1 pipeline in categories | Methodological Rigor |
| FM-005-r1 | S-012 | HABIT force rating criteria undocumented; ratings unreproducible | Methodological Rigor |
| FM-006-r1 | S-012 | A3 Framework Contributor classified as primary actor; internal governance skills not end-user jobs | Completeness |
| FM-007-r1 | S-012 | No criterion mapping SKILL.md language intensity to numeric force rating | Methodological Rigor |
| PM-002-r1 | S-004 | Actor segments are fictional hypotheses; XP-02 Personas will build on unvalidated profiles | Evidence Quality |
| PM-003-r1 | S-004 | Pipeline invisibility claim is inferred from zero coverage, not observed user behavior | Actionability |
| PM-004-r1 | S-004 | Habit force ratings are lowest-confidence; switch conditions may be more blocked than assessed | Actionability |
| IN-001-r1 | S-013 | Ranking is vulnerable to skill-count removal — anti-goal condition partially unaddressed | Methodological Rigor |
| IN-002-r1 | S-013 | Universal switch trigger not differentiated by actor segment in key_findings; XP-04 will receive one-size message | Evidence Quality |

### Minor Findings

| ID | Strategy | Finding | Dimension |
|----|---------|---------|-----------|
| CC-001-r1 | S-007 | Opportunity score formula sourcing is buried; L2 presents as computed data | Evidence Quality |
| DA-004-r1 | S-002 | A3 as primary actor segment overstates contributor persona relative to end-user | Completeness |
| DA-005-r1 | S-002 | Force rating criteria not documented; ratings are non-reproducible judgments | Methodological Rigor |
| FM-008-r1 | S-012 | `eng-team` double-counted in Category 2 and Category 5 | Completeness |
| FM-009-r1 | S-012 | No confidence upgrade trigger for key_findings handoffs | Completeness |
| FM-010-r1 | S-012 | `saucer-boy` grouping note not surfaced to downstream Kano | Completeness |
| IN-004-r1 | S-013 | Numeric scores imply calibration not performed; tables carry no uncertainty markers | Evidence Quality |
| IN-005-r1 | S-013 | A3 as primary reinforces contributor-first persona risk (inversion confirmation) | Completeness |
| PM-005-r1 | S-004 | No versioning trigger for 30-skill catalog if skills added during PROJ-040 | Completeness |

---

## Revision Recommendations

### P0 — Must Fix Before Acceptance (Critical Blockers)

**P0-001: Correct the L0/L2 coverage number contradiction**
- **Findings:** CC-002, FM-001, IN-003
- **Action:** L0 Executive Summary states "16 of 30 skills have zero documentation coverage." The per-skill table (lines 132-138) and state file key_findings[4] both state 26 skills have `doc-gap: none`. Determine the correct number (almost certainly 26, matching the per-skill table) and update L0 to: "26 of 30 skills have zero documentation coverage (4 have partial how-to coverage, NEEDS REVISION)."
- **Acceptance criteria:** L0, L2 summary table, and state file key_findings[4] all cite the same number.

**P0-002: Add explicit uncertainty bounds to opportunity scores**
- **Findings:** FM-002, PM-001, CC-001
- **Action:** The Category opportunity scores (15, 14, 12, 13, 11) appear as computed values. They must be clearly labeled as "inferred proxies" with the derivation documented. Add a box or callout in the Top 5 Job Categories section:
  - State that Importance and Satisfaction ratings were assigned by analyst judgment, not user survey
  - State the assumptions used to assign each I/S pair (e.g., "Importance=9 inferred from: skill represents the dominant stated pain in 5 of 7 SKILL.md Purpose sections")
  - State that ODI-validated opportunity scores require a 20+ user survey (link to Validation Required section)
- **Acceptance criteria:** No opportunity score is presented without an explicit "basis:" annotation showing the specific SKILL.md evidence for the I/S values.

### P1 — Should Fix (Major Issues Affecting Downstream Quality)

**P1-001: Differentiate switch triggers by actor segment in key_findings**
- **Findings:** DA-002, IN-002
- **Action:** key_finding[2] states a universal switch trigger. Replace with two trigger statements:
  - A1/A2: "Switch from unstructured vanilla Claude Code prompting — push: inconsistent outputs, no paper trail; pull: methodology + persistent artifacts"
  - A4/A6: "Switch from existing domain practice tooling (professional methodology, PM tools, UX tools) — push: manual methodology at scale is slow; pull: AI-augmented methodology execution without specialist headcount"
- **Acceptance criteria:** key_findings[2] in state file differentiates at minimum two actor groups.

**P1-002: Document job granularity decision for SDLC chain**
- **Findings:** DA-001, FM-004
- **Action:** The deliverable simultaneously treats `/use-case`, `/test-spec`, `/contract-design` as 3 distinct per-skill jobs AND as 1 pipeline job in Category 2. This is coherent only if explicitly stated. Add a note to Category 2 analysis: "The three per-skill job statements represent the same pipeline job at different execution stages. For Kano (XP-01), these should be evaluated as a single 'traceable pipeline' feature cluster, not three independent features. The opportunity score of 14 represents the pipeline as a unit." Ensure per-skill table rows 5, 16, 18 cross-reference each other.
- **Acceptance criteria:** Category 2 analysis explicitly states how XP-01 should treat the three SDLC skills.

**P1-003: Remove skill count from ranking criteria or disclose its supply-side nature**
- **Findings:** DA-003, IN-001
- **Action:** Either (a) remove skill count as a ranking criterion and re-rank using only cross-actor breadth and switch trigger strength, then document whether rankings change; or (b) add an explicit disclosure: "Skill count is used as a supply-side proxy for demand; it reflects framework investment decisions, not observed user hiring frequency. Categories with high skill count may or may not have proportionally high user demand."
- **Acceptance criteria:** The ranking criteria section explicitly acknowledges whether skill count is demand-side or supply-side.

**P1-004: Update A3 classification in "90% of hiring" L0 claim**
- **Findings:** FM-006, DA-004, IN-005
- **Action:** L0 claims A1, A2, A3 drive 90% of hiring. A3's primary skills are governance/internal tools. Update L0 to state A1, A2, and A6 drive 90% of end-user hiring intent. Retain A3 as a secondary segment noting its primary use is framework extension, not application of Jerry for external work.
- **Acceptance criteria:** L0 primary actor list matches the deliverable's own finding that A6 Domain Specialist is a primary persona for the UX suite and pm-pmm.

**P1-005: Add force rating calibration note**
- **Findings:** FM-005, FM-007, DA-005
- **Action:** Add a brief methodological note to the Switch Force Analysis section: "Force ratings apply the following criteria: Push=5 if SKILL.md Purpose section opens with pain-state language AND the skill name appears in activation keywords for problem types (e.g., 'root cause', 'quality gate'). Push=4 if pain is described but is secondary to capability. [etc.]" This does not need to be exhaustive — a 3-4 sentence decision rule is sufficient for reproducibility.
- **Acceptance criteria:** A second analyst reading the criteria could reproduce the Push ratings for Categories 1 and 4 within ±1 of the published values.

### P2 — Consider Fixing (Minor Improvements)

**P2-001:** Add inline uncertainty markers (e.g., "(inferred, ±2)") to force rating tables to reinforce that these are not precision measurements.

**P2-002:** Add a re-evaluation trigger to the Validation Required table: "Re-run per-skill analysis if >= 3 new skills are added during PROJ-040 execution."

**P2-003:** Clarify `saucer-boy` grouping in Category 1 with an explicit note for XP-01: "This skill should be treated as Attractive (delight) not Must-be (methodology). See Synthesis Judgment §8."

**P2-004:** Add a confidence upgrade trigger clause to state file: "key_findings are valid for XP handoffs until superseded by user interview data (see Validation Required). Downstream XP agents should treat Opp scores as planning proxies, not validated rankings."

---

## Verdict and Score Estimate

### Score Estimate

| Dimension | Weight | Score (revised) | Pre-revision |
|-----------|--------|----------------|-------------|
| Completeness | 0.20 | 0.91 | 0.85 |
| Internal Consistency | 0.20 | 0.93 | 0.72 |
| Methodological Rigor | 0.20 | 0.88 | 0.83 |
| Evidence Quality | 0.15 | 0.85 | 0.80 |
| Actionability | 0.15 | 0.90 | 0.88 |
| Traceability | 0.10 | 0.93 | 0.92 |

**Pre-revision composite estimate:** 0.824 — below threshold
**Post-P0 revision estimate (if P0-001 and P0-002 addressed):** ~0.876 — still below threshold
**Post-P0+P1 revision estimate (if all P1 fixes applied):** ~0.924 — at threshold

**Verdict: REVISE**

The self-reported 0.92 does not survive adversarial review. The L0/L2 coverage contradiction is a factual inconsistency that directly suppresses Internal Consistency. The opportunity score evidence gap suppresses Evidence Quality. Both must be resolved in revision.

Revision difficulty is LOW to MEDIUM. P0 fixes require targeted edits (number correction, derivation documentation). P1 fixes require methodological additions that the agent has the source data to perform. The core analysis is sound — the JTBD framework is correctly applied, confidence is appropriately disclosed, and the downstream signal for XP features is present. The revision is hardening existing work, not rethinking it.

### Response Required Table

| Priority | Finding(s) | Required Action | Acceptance Criteria |
|---------|-----------|----------------|---------------------|
| P0 | CC-002, FM-001, IN-003 | Fix L0/L2/state file coverage number | All three sources cite same count |
| P0 | FM-002, PM-001, CC-001 | Document opportunity score derivation with SKILL.md evidence | Each I/S pair has explicit basis annotation |
| P1 | DA-002, IN-002 | Differentiate switch trigger by actor segment | key_findings[2] has A1/A2 vs A6 split |
| P1 | DA-001, FM-004 | Document SDLC pipeline job-granularity decision | Category 2 tells XP-01 how to treat 3 skills |
| P1 | DA-003, IN-001 | Disclose skill count as supply-side proxy | Ranking criteria section acknowledges supply/demand distinction |
| P1 | FM-006, DA-004 | Update L0 primary actor list (A1/A2/A6, not A3) | L0 primary actors match end-user focus |
| P1 | FM-005, FM-007 | Add force rating calibration note | Push/Pull/Anxiety criteria documented in 3-4 sentences |

---

## Execution Statistics

| Metric | Count |
|--------|-------|
| Strategies executed | 6 (S-007, S-002, S-004, S-012, S-013, S-014 sanity) |
| Total findings | 26 |
| Critical | 5 |
| Major | 13 |
| Minor | 8 |
| P0 revision items | 2 |
| P1 revision items | 5 |
| P2 revision items | 4 |
| S-003 Steelman | Skipped (optional at C3 per-feature; H-16 satisfied) |
| Protocol steps completed | S-007: 5/5 | S-002: 5/5 | S-004: 5/5 | S-012: 3/5 (Steps 4-5 inline) | S-013: 4/4 | S-014: partial |

---

*Reviewer: adv-executor v1.0.0*
*Iteration: 1 of max 7 (RT-M-010 C3 ceiling)*
*Constitutional Compliance: P-001 (evidence-based findings), P-003 (no subagents), P-022 (severity not minimized)*
*Date: 2026-04-17*
