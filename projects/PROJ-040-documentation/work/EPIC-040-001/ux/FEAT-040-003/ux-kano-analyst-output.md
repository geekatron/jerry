---
feature_id: FEAT-040-003
agent: ux-kano-analyst
engagement_id: UX-040-003
status: complete
criticality: C3
date: 2026-04-20
confidence: MEDIUM
quality_score: 0.927
iteration: 1
inputs:
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-001/ux-jtbd-analyst-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-004/ux-heuristic-evaluator-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-005/ux-inclusive-evaluator-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-007/ux-lean-ux-facilitator-output.md
  - projects/PROJ-040-documentation/work/EPIC-040-001/research/FEAT-040-056/ps-researcher-output.md
  - projects/PROJ-040-documentation/orchestration/reviews/qg-2-consistency-report.md
classification_mode: inferred
survey_data: none
respondent_count: 0
statistical_adequacy: provisional_pending_survey
xp_provides: [XP-01]
---

# Kano Model Feature Classification: Jerry Documentation

> **Survey Data Disclosure (P-022):** No user survey data is available. All classifications are **PROVISIONAL — inferred** from Phase 1a discovery evidence (JTBD opportunity scores, B=MAP bottleneck analysis, heuristic evaluation, WCAG audit, Lean UX hypothesis rankings, OSS research best practices, and QG-2 triple-convergence findings). CS coefficients are computed from inferred response distributions, not respondent data.
>
> **Statistical adequacy:** Directional only — classification confidence is contingent on inferred proxies. All entries are flagged `[PROVISIONAL — PENDING SURVEY VALIDATION]`. Validation recommended at N=20+ target users per Berger et al. (1993).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | L0: Feature counts by category, top priorities, confidence disclosure |
| [Engagement Context](#engagement-context) | L1: Product, users, feature list source, inference methodology |
| [Inferred Classification Methodology](#inferred-classification-methodology) | L1: How inferred Kano categories are derived from discovery evidence |
| [Feature Classification Table](#feature-classification-table) | L1: Per-feature category, inferred response distribution, confidence |
| [CS Coefficient Analysis](#cs-coefficient-analysis) | L1: Per-feature Better/Worse coefficients, quadrant assignments |
| [Priority Matrix](#priority-matrix) | L1: Better vs. \|Worse\| scatter with quadrant labels |
| [Split Classification Analysis](#split-classification-analysis) | L1: Ambiguous features requiring expert resolution |
| [Feature Lifecycle Assessment](#feature-lifecycle-assessment) | L2: Migration trajectories, competitive dynamics |
| [Strategic Implications](#strategic-implications) | L2: Phase 2 roadmap guidance, competitive positioning |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: AI judgment calls with confidence classifications |
| [Handoff Data](#handoff-data) | L1: Structured data for Phase 2 synthesis |
| [Revision History](#revision-history) | L1: Iteration log with blocker closure tracking |

---

## Executive Summary

### Feature Counts by Kano Category (Inferred)

| Category | Count | Features |
|----------|-------|---------|
| Must-be (M) | 4 | Tutorial coverage, Skills table completeness, INSTALLATION.md heading structure, Getting-started path disambiguation |
| Performance (O) | 4 | Cross-linking (skill → playbook), Jargon glossary / plain-language framing, Authoritative Jerry one-liner, Breadcrumbs + search preview |
| Attractive (A) | 4 | WCAG compliance enhancements, Getting-started split Path A/B (full), Diataxis-structured documentation suite, Code block language specifiers |
| Indifferent (I) | 0 | — |
| Reverse (R) | 0 | — |
| Split / Ambiguous | 1 | Getting-started Path A/B split (possible M↔A boundary) |

**Total features classified:** 13 (4 M + 4 O + 4 A + 1 Split; the Path A/B split entry is counted separately from the 4 Attractive rows — the Attractive row covers Scope B full implementation, the Split row covers the unresolved Scope A vs. Scope B boundary)

### Top 3 Must-be Features (Implement Immediately)

1. **Tutorial coverage (TC-004)** — 0/30 skills have tutorials. Absence is confirmed activation barrier at scale (JTBD Cat 4 Anxiety=5; FEAT-040-004 F-013 Sev 3; HYP-006; FEAT-040-056 D-03). Worse = −0.85. *(Arithmetic proof: Worse = −(O+M)/(A+O+M+I) = −(3+14)/20 = −17/20 = −0.85; inferred distribution M=14, O=3, A=2, I=1.)*
2. **Skills table completeness (TC-002)** — 7/19+ skills visible on homepage. Confirmed hidden-catalog anti-pattern (F-020 Sev 2; HYP-004 ICE=8.0; competitive AP-02). Worse = −0.80. *(Arithmetic proof: −(4+12)/20 = −16/20 = −0.80; M=12, O=4, A=3, I=1.)*
3. **INSTALLATION.md heading structure (W-001 / HYP-011)** — Bold step labels not AT-navigable; triple convergence (WCAG SC 1.3.1 + Heuristic + B=MAP). Worse = −0.85. *(Arithmetic proof: −(4+13)/20 = −17/20 = −0.85; M=13, O=4, A=2, I=1.)*

### Top 3 Attractive Features (Differentiation Opportunities)

1. **WCAG compliance enhancements (W-013, W-014, W-011)** — Resolves AA non-conformance; differentiator among OSS AI tools (FEAT-040-056 finding A-03: EAA 2025 compliance now required for EU audiences).
2. **Diataxis-structured documentation suite** — Full four-quadrant tutorial/how-to/reference/explanation coverage differentiates Jerry from all six competitive frameworks (FEAT-040-055 AP-05; FEAT-040-056 D-01).
3. **Getting-started split Path A/B (full implementation)** — Removing 100% of install-path friction is a qualitative UX leap; partial fix is Must-be, full experience is delightful.

### Sample Size and Confidence Disclosure

- **Respondent count:** 0 (no user survey administered)
- **Statistical adequacy:** Anecdotal / provisional — NOT for final design decisions without validation
- **Confidence classification:** MEDIUM (directional signal grounded in 5 triple-convergence findings from 9 independent Phase 1a deliverables; each category assignment traces to 2–4 corroborating evidence sources)
- **Validation path:** Administer Kano questionnaire (Phase 2 recommendation) at N=20+ target users (A1 Solo Engineer, A2 Technical Lead, A6 Domain Specialist) per Berger et al. (1993)

### Overall Prioritization Recommendation

**Immediate (Must-be):** Tutorial coverage, skills table, INSTALLATION.md heading structure, and getting-started routing must be addressed as foundational table stakes — their absence causes measurable activation failure.

**High priority (Performance):** Cross-linking, jargon reduction, canonical Jerry definition, and breadcrumb/search navigation drive proportional satisfaction gains with each improvement.

**Differentiation (Attractive):** WCAG compliance, full Diataxis suite, and polished path-split experience are competitive differentiators that create delight when present but do not directly cause abandonment when absent.

---

## Engagement Context

**Product:** Jerry Framework v0.31.5 — Claude Code plugin for behavioral guardrails, ~30 skills, no user-facing documentation for 25/29 skills.

**Target Users:**
- A1 Solo Engineer — vanilla Claude Code → structured Jerry methodology
- A2 Technical Lead — ad-hoc review → auditable orchestration
- A6 Domain Specialist — specialist SaaS (Dovetail, Figma) → /user-experience UX suite

**Feature List Source:** FEAT-040-003 dispatch scope + QG-2 triple-convergence seeding (TC-001 through TC-005), cross-referenced with:
- FEAT-040-001 (JTBD Analyst): 5 JTBD job categories, Tier A/B/C rankings
- FEAT-040-004 (Heuristic Evaluator): 11 active findings (3 Sev-3, 6 Sev-2)
- FEAT-040-005 (Inclusive Evaluator): WCAG 2.2 AA findings (W-001, W-006, W-011–W-014)
- FEAT-040-007 (Lean UX Facilitator): 14 hypotheses with ICE rankings
- FEAT-040-056 (PS Researcher): 11 ranked OSS documentation recommendations
- QG-2 Consistency Report: 5 triple-convergence findings TC-001–TC-005

**Survey Administration:** No survey administered. Phase 1a discovery data used as classification proxy per "inferred classification" mode.

---

## Inferred Classification Methodology

In the absence of user survey data, Kano classifications are inferred from four proxy evidence types:

| Proxy Type | Maps To | Rationale |
|-----------|---------|-----------|
| JTBD "Push force" (pain-state density, unmet basic jobs) | **Must-be (M)** | High push force = user explicitly suffers from absence; maps to Kano M where absence causes dissatisfaction. Ulwick ODI: underserved jobs with I−S > 4 points. |
| B=MAP bottleneck severity (Primary/Secondary/Minor) | **Must-be or Performance (M/O)** | Primary bottleneck = absence blocks task completion → M. Secondary bottleneck = degrades performance → O. |
| Lean UX ICE score (P1 Immediate vs. P3 Experiment-first) | **Performance (O)** | P1 Immediate (ICE ≥ 7.0) with high Confidence = proportional satisfaction return → O. |
| Competitive differentiation / best-practice gap (FEAT-040-055, FEAT-040-056) | **Attractive (A)** | Features absent across competitive set but present in best-in-class → Attractive (delight when present, not missed when absent). |

**Inferred response distribution construction:** For each feature, I assign respondent proportions M/O/A/I based on the proxy signal strength:
- A finding with 3+ corroborating evidence sources → dominant category ≥ 65% share
- A finding with 2 corroborating sources → dominant category ≥ 55% share
- A finding with 1 source → dominant category ≥ 50% share (split threshold; flagged)

CS coefficients (Berger et al., 1993) are then calculated from these inferred distributions, excluding R and Q responses (both zero in inferred mode).

**Formula:**
```
Better  = (A + O) / (A + O + M + I)    [range 0 to 1]
Worse   = -(O + M) / (A + O + M + I)   [range -1 to 0]
```

All entries labeled `[PROVISIONAL]`. For features where proxy signals conflict, the conservative (lower confidence) category is assigned per P-022.

**Persona heterogeneity limitation:** Inferred response distributions are constructed as aggregate across A1 Solo Engineer, A2 Technical Lead, and A6 Domain Specialist personas without segment-level differentiation. This aggregation may mask important segment divergences — notably, A6 Domain Specialist users in EU enterprise contexts may classify WCAG compliance as Must-be where A1/A2 classify it as Attractive, and A6 users may have different urgency weightings for accessibility and compliance-adjacent features. **The survey design should segment responses by persona** (collect persona-coded responses) to surface segment-level Kano categories. Aggregate classifications in this analysis should be treated as blended estimates that may mask A6 Must-be sub-populations.

---

## Feature Classification Table

All 12 features. `[PROVISIONAL — PENDING SURVEY VALIDATION]` applies to all rows.

| Feature | ID(s) | Inferred Category | M | O | A | I | R | Q | M% | O% | A% | I% | Confidence | Split? | Evidence Sources |
|---------|-------|-------------------|---|---|---|---|---|---|----|----|----|----|------------|--------|-----------------|
| Tutorial coverage (0/30 skills) | TC-004, HYP-006, F-013 | **Must-be (M)** | 14 | 3 | 2 | 1 | 0 | 0 | 70 | 15 | 10 | 5 | MEDIUM | No | JTBD Cat4 Anxiety=5; F-013 Sev-3; HYP-006; D-03; TC-004 triple |
| Skills table completeness (7/19+) | TC-002, F-020, HYP-004 | **Must-be (M)** | 12 | 4 | 3 | 1 | 0 | 0 | 60 | 20 | 15 | 5 | MEDIUM | No | JTBD 25/29 zero; F-020 Sev-2; HYP-004 ICE=8.0; AP-02; TC-002 triple |
| INSTALLATION.md heading structure (bold→H3) | W-001, HYP-011 | **Must-be (M)** | 13 | 4 | 2 | 1 | 0 | 0 | 65 | 20 | 10 | 5 | HIGH | No | W-001 Sev-3; HYP-011 ICE=7.7 P1; B=MAP Ability; TC-001 triple |
| Getting-started path disambiguation (Step 3 routing) | TC-001, TC-005, HYP-001 | **Must-be (M)** | 11 | 5 | 2 | 2 | 0 | 0 | 55 | 25 | 10 | 10 | MEDIUM | No | B=MAP Prompt primary; TC-001/TC-005 triple; F-016 Sev-2; HYP-001 |
| Cross-linking (skill → playbook) | F-013, HYP-004 | **Performance (O)** | 4 | 11 | 4 | 1 | 0 | 0 | 20 | 55 | 20 | 5 | MEDIUM | No | F-013 Sev-3; HYP-004 ICE=8.0; D-03 tutorial/how-to discovery; TC-004 |
| Jargon glossary / plain-language framing | TC-003, F-011, HYP-010 | **Performance (O)** | 3 | 12 | 3 | 2 | 0 | 0 | 15 | 60 | 15 | 10 | MEDIUM | No | F-011 Sev-3 triple-eval; Brain Cycles (a); TC-003; HYP-010 ICE=6.0 |
| Authoritative Jerry one-liner / canonical definition | F-011, HYP-010, TC-003 | **Performance (O)** | 3 | 10 | 5 | 2 | 0 | 0 | 15 | 50 | 25 | 10 | LOW-MEDIUM | No | F-011/F-007; TC-003 voice-drift 0.54; FEAT-040-056 C-03/C-04 |
| Sidebar breadcrumbs + search preview | F-014, HYP-009 | **Performance (O)** | 3 | 11 | 4 | 2 | 0 | 0 | 15 | 55 | 20 | 10 | MEDIUM | No | F-014 Sev-3 all-3-evaluators; SD-01/SD-03 navigation; HYP-009 ICE=7.0 |
| WCAG compliance enhancements (W-011, W-013, W-014) | W-011, W-013, W-014 | **Attractive (A)** | 2 | 4 | 11 | 3 | 0 | 0 | 10 | 20 | 55 | 15 | MEDIUM | No | W-013/W-014 Sev-2; EAA 2025 compliance differentiator; A-03 (056) |
| Getting-started split Path A/B (full experience) | HYP-002, HYP-003, TC-005 | **Attractive (A)** | 3 | 5 | 10 | 2 | 0 | 0 | 15 | 25 | 50 | 10 | LOW | Yes | TC-005 HIGH; HYP-002 ICE=8.3; A-003 Q1 unknown; EXP-001/EXP-002 gated |
| Diataxis-structured documentation suite | TC-004, D-01, AP-05 | **Attractive (A)** | 2 | 4 | 11 | 3 | 0 | 0 | 10 | 20 | 55 | 15 | MEDIUM | No | D-01 Diataxis at scale; AP-05 all 6 competitors missing; TC-004 depth |
| Code block language specifiers (WCAG W-006) | W-006, HYP-008 | **Attractive (A)** | 1 | 3 | 9 | 7 | 0 | 0 | 5 | 15 | 45 | 35 | LOW | No | W-006 Sev-2 MEDIUM; HYP-008 P2; AT-specific; general users indifferent |

**Notes on construction:**
- All response counts are synthetic (inferred from evidence proxies, not actual respondents). Counts represent a normalized pool of N=20 hypothetical respondents for coefficient comparability.
- INSTALLATION.md heading structure (W-001/HYP-011) receives HIGH confidence because three independent frameworks (WCAG Sev-3, Heuristic Sev-3, B=MAP Ability bottleneck) converge on the same root cause with consistent direction.
- Getting-started Path A/B "full experience" is flagged Split because the basic routing fix (Step 3 "Choose your path" block) is Must-be (see row 4), while the full polished two-tutorial experience is Attractive — the boundary depends on implementation scope.

---

## CS Coefficient Analysis

CS coefficients computed from inferred distributions, R=0 and Q=0 excluded per Berger et al. (1993).

**Formula applied:** Better = (A+O)/(A+O+M+I); Worse = −(O+M)/(A+O+M+I)

All entries `[PROVISIONAL]`.

| Feature | A | O | M | I | Better | Worse | \|Worse\| | Quadrant | Priority Rank |
|---------|---|---|---|---|--------|-------|----------|----------|--------------|
| Tutorial coverage | 2 | 3 | 14 | 1 | 0.25 | −0.85 | 0.85 | Must-be | 1 |
| Skills table completeness | 3 | 4 | 12 | 1 | 0.35 | −0.80 | 0.80 | Must-be | 2 |
| INSTALLATION.md heading structure | 2 | 4 | 13 | 1 | 0.30 | −0.85 | 0.85 | Must-be | 3 |
| Getting-started path disambiguation | 2 | 5 | 11 | 2 | 0.35 | −0.80 | 0.80 | Must-be | 4 |
| Cross-linking (skill → playbook) | 4 | 11 | 4 | 1 | 0.75 | −0.75 | 0.75 | Performance | 5 |
| Sidebar breadcrumbs + search preview | 4 | 11 | 3 | 2 | 0.75 | −0.70 | 0.70 | Performance | 6 |
| Jargon glossary / plain-language | 3 | 12 | 3 | 2 | 0.75 | −0.75 | 0.75 | Performance | 5 (tie) |
| Authoritative Jerry one-liner | 5 | 10 | 3 | 2 | 0.75 | −0.65 | 0.65 | Performance | 7 |
| WCAG compliance enhancements | 11 | 4 | 2 | 3 | 0.75 | −0.30 | 0.30 | Attractive | 8 |
| Diataxis documentation suite | 11 | 4 | 2 | 3 | 0.75 | −0.30 | 0.30 | Attractive | 8 (tie) |
| Getting-started Path A/B (full) | 10 | 5 | 3 | 2 | 0.75 | −0.40 | 0.40 | Attractive | 9 [SPLIT FLAG] |
| Code block language specifiers | 9 | 3 | 1 | 7 | 0.60 | −0.20 | 0.20 | Attractive | 10 |

**CS Summary Statistics (provisional):**
- Better range: 0.25 (tutorial coverage — must-be anchor) to 0.75 (all Performance/Attractive features)
- Worse range: −0.85 (tutorial coverage, heading structure) to −0.20 (code block specifiers)
- Must-be cluster: Better 0.25–0.35, \|Worse\| 0.80–0.85 — high dissatisfaction risk, low delight potential
- Performance cluster: Better 0.75, \|Worse\| 0.65–0.75 — symmetric satisfaction impact
- Attractive cluster: Better 0.60–0.75, \|Worse\| 0.20–0.40 — high delight, low absence pain

---

## Priority Matrix

Text-based scatter plot. X-axis = Better coefficient (0.0 → 1.0). Y-axis = \|Worse\| coefficient (0.0 → 1.0).

```
|Worse|
 1.00 |
 0.90 |
 0.85 |...[M1-Tutorial]............[M3-Headings]
 0.80 |...[M2-Skills table]........[M4-Step3 routing]
 0.75 |                    [O1-Cross-link][O2-Jargon]
 0.70 |                    [O3-Breadcrumbs]
 0.65 |                    [O4-Jerry one-liner]
 0.50 |
 0.40 |                              [A3-Path A/B split*]
 0.30 |                    [A1-WCAG][A2-Diataxis suite]
 0.20 |                    [A4-Code blocks]
 0.10 |
 0.00 +-----+-----+-----+-----+-----+-----+-----+-----+--
      0.0  0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  Better

            MUST-BE          PERFORMANCE       ATTRACTIVE

QUADRANT LABELS:
  Top-Left   (High|Worse|, Low Better) = MUST-BE: implement immediately
  Top-Right  (High|Worse|, High Better) = PERFORMANCE: invest proportionally
  Bottom-Right (Low|Worse|, High Better) = ATTRACTIVE: invest for differentiation
  Bottom-Left  (Low|Worse|, Low Better) = INDIFFERENT: deprioritize

* A3-Path A/B split is flagged [SPLIT] — see Split Classification Analysis.

FEATURE KEY:
  M1 = Tutorial coverage (TC-004)              Better=0.25, |Worse|=0.85
  M2 = Skills table completeness (TC-002)      Better=0.35, |Worse|=0.80
  M3 = INSTALLATION.md heading structure       Better=0.30, |Worse|=0.85
  M4 = Getting-started path disambiguation     Better=0.35, |Worse|=0.80
  O1 = Cross-linking skill→playbook            Better=0.75, |Worse|=0.75
  O2 = Jargon glossary / plain language        Better=0.75, |Worse|=0.75
  O3 = Sidebar breadcrumbs + search preview    Better=0.75, |Worse|=0.70
  O4 = Authoritative Jerry one-liner           Better=0.75, |Worse|=0.65
  A1 = WCAG compliance enhancements            Better=0.75, |Worse|=0.30
  A2 = Diataxis documentation suite            Better=0.75, |Worse|=0.30
  A3 = Getting-started Path A/B (full)         Better=0.75, |Worse|=0.40  [SPLIT]
  A4 = Code block language specifiers          Better=0.60, |Worse|=0.20
```

**Quadrant Boundary:** Split between Must-be and Performance occurs at approximately Better=0.55 / \|Worse\|=0.55 (midpoint of range). Must-be cluster is consistently below Better=0.40 and above \|Worse\|=0.75. Performance cluster occupies Better≈0.75, \|Worse\| 0.65–0.75. No features land in Indifferent quadrant (all have positive delight and/or strong dissatisfaction risk).

**Conflict indicators:**
- M1 and M3 share identical \|Worse\|=0.85 — near-equal dissatisfaction risk; prioritize in parallel, not sequentially.
- O1 and O2 share identical coordinates — treat as a single implementation cluster (cross-linking + jargon reduction are stylistically linked).
- A1 and A2 share identical coordinates — differentiation cluster, implement together in Wave 4/5.

---

## Split Classification Analysis

### Feature with Split Flag

**Feature: Getting-started Path A/B — Full Split Experience (HYP-002, HYP-003)**

| Category | Inferred % | Rationale |
|----------|-----------|-----------|
| Must-be | 15 | The step-3 routing block itself ("Choose your path") is Must-be (see row M4 above) |
| Performance | 25 | Partial implementation (routing block only) incrementally satisfies |
| Attractive | 50 | Full polished two-tutorial experience (separate plugin tutorial + CLI tutorial) is a delight |
| Indifferent | 10 | Users who already know their path are unaffected |

**Split rationale:** This feature has a scope-dependent classification. The Kano category depends on implementation granularity:
- **Scope A (Minimal):** Add "Choose your path: Plugin vs. Local Clone" decision block at Step 3 → Must-be (absence causes cognitive overhead; presence resolves B=MAP Prompt primary bottleneck). Better=0.35, \|Worse\|=0.80.
- **Scope B (Full):** Create two completely separate tutorials (INSTALLATION-plugin.md + INSTALLATION-clone.md), each with path-specific prerequisites, commands, and verification steps → Attractive (unexpected quality delight when present; Step 3 routing still works without it). Better=0.75, \|Worse\|=0.40.

**[DOMAIN EXPERT REQUIRED]:** Determine which scope is in scope for Phase 2 Wave 2/3 implementation before treating this feature as either M or A. QG-2 TC-001 recommendation is Scope A minimum; Scope B is Wave 4a candidate.

**[DOMAIN EXPERT REQUIRED]:** EXP-001 and EXP-002 (from HYP-001) should complete before committing to Scope B. A-001 (step-3 abandonment rate) is a Q1 unknown. If abandonment is minimal, Scope A satisfies; if abandonment is severe, Scope B becomes Performance (O) rather than Attractive.

---

## Feature Lifecycle Assessment

**Available product history:** Jerry v0.31.5, pre-1.0 OSS release, all documentation gaps are founding gaps (not regression gaps). Lifecycle stage = early-stage, pre-maturity.

### Migration Trajectories (Kano et al., 1984; Matzler & Hinterhuber, 1998)

**Attractive → Performance → Must-be migration timeline estimates are PROVISIONAL** (practitioner estimate; Kano et al. 1984 establishes migration direction but not quantitative thresholds; timing depends on competitive dynamics).

| Feature | Current Stage | Migration Risk | Trigger | Estimated Timeline |
|---------|--------------|---------------|---------|--------------------|
| Tutorial coverage (M1) | Must-be (born as table-stakes from user expectations) | N/A — already M | — | Immediate |
| Skills table completeness (M2) | Must-be | N/A | — | Immediate |
| WCAG compliance (A1) | Attractive now; approaching Performance | HIGH — EAA 2025 compliance | European Accessibility Act (Directive 2019/882/EU) transposition deadline June 2025 (A-03, FEAT-040-056; see OSS scope caveat below) | 6–12 months to Performance for EU enterprise context; conditional on EAA applicability to Jerry's distribution model |
| Diataxis suite (A2) | Attractive — differentiation gap | MEDIUM | When 2+ AI framework competitors adopt Diataxis (currently zero per FEAT-040-055) | 12–24 months; competitive adoption accelerating |
| Jargon glossary (O2) | Performance | LOW — structural, not rapidly commoditized | Baseline for professional documentation | Stable at Performance indefinitely |
| Cross-linking (O1) | Performance | LOW | Baseline expectation in developer documentation (Stripe, Kubernetes patterns per F-013) | Stable at Performance; table stakes for professional docs |
| Breadcrumbs + search (O3) | Performance; approaching Must-be | MEDIUM | MkDocs Material implements breadcrumbs natively; developer expectation rising | 6–12 months migration to Must-be as developer tool bar rises |
| INSTALLATION.md headings (M3) | Must-be (regulatory + AT expectation) | N/A | — | Immediate; EAA 2025 adds urgency |

**A6 persona heterogeneity note:** A6 Domain Specialist users in EU enterprise contexts subject to EAA (e.g., UX consultants, enterprise tool administrators) may already classify WCAG compliance as Must-be rather than Attractive, due to EAA enforcement requirements binding their organizations. A1 Solo Engineers and A2 Technical Leads are less likely to perceive WCAG as Must-be given their individual developer context. The aggregate "Attractive" classification reflects the A1/A2 majority in the inferred response pool; a segment-differentiated survey may surface A6 as a WCAG Must-be sub-population. **The survey design should segment responses by persona to surface this distinction before committing to WCAG investment tier.**

**EAA OSS scope caveat:** EAA Directive 2019/882/EU (per A-03, FEAT-040-056 synthesis; primary directive source not independently verified in this analysis) applies to products and services offered in the EU market. Open-source CLI tools distributed on GitHub without direct commercial sale may qualify for the microenterprise exemption or fall outside EAA's commercial product scope. EAA enforcement directly applies to commercial providers; OSS projects have a separate compliance scope — the lifecycle migration to Performance is indirect (driven by enterprise adopters' downstream requirements, not direct OSS project obligation). Treat the 6–12 month migration timeline as conditional on Jerry's adoption by EAA-regulated enterprises, not as a universal OSS obligation. Per FEAT-040-056 synthesis A-03: primary EAA directive source was not independently verified in Phase 1a research; this citation should be treated as a secondary-source finding pending independent verification.

**Key lifecycle insight:** WCAG compliance (currently Attractive) is approaching Performance classification faster than any other feature in the set for EU enterprise adoption contexts, driven by EAA 2025 applicability. Teams should treat the WCAG cluster as a rising-Performance item for A6 Domain Specialist contexts, while remaining Attractive for the broader A1/A2 developer population. The lifecycle migration is conditional on distribution context — validate before committing to Wave 3 urgency framing.

---

## Strategic Implications

### Implication 1: Documentation Debt Is a Must-be Debt, Not a Nice-to-Have

All four Must-be features (M1 tutorial coverage, M2 skills visibility, M3 heading structure, M4 step routing) have \|Worse\| ≥ 0.80. This means the **absence of these features creates measurable dissatisfaction** among the A1/A2/A6 actor segments identified in FEAT-040-001. The JTBD analysis confirms: 25/29 skills have zero documentation coverage, which maps directly to JTBD Anxiety=5 for Cat 4 (UX Suite) and Anxiety=5 for Cat 2 (SDLC Chain). These are not product enhancements — they are foundational requirements for user activation.

**Phase 2 roadmap implication:** Must-be features constitute Wave 2/3 priorities (remediation). Wave 4 (tutorial creation) addresses M1 directly. No feature in the Attractive quadrant should be implemented before M1–M4 are resolved. **Survey-contingency caveat:** If survey validation confirms TC-002 and TC-004 as Performance (O) rather than Must-be (M), the O1-O4 Performance cluster runs co-equal with M1-M4 in Wave 2 — the current sequencing (Must-be first, then Performance) would shift to parallel investment across both clusters. Re-sequence upon survey validation; do not treat this prioritization as definitive before user survey evidence is collected.

### Implication 2: Performance Features Are Disproportionately High ROI

The Performance cluster (O1–O4) occupies Better≈0.75 and \|Worse\| 0.65–0.75 — the highest combined satisfaction leverage of any quadrant. These features:
- Are individually achievable in 20–90 minutes per FEAT-040-004 remediation estimates (F-011 medium; F-013 medium; F-014 medium-high; F-018 low)
- Map directly to QG-2 TC-003 (jargon barrier), TC-002 (skill discovery), and TC-001 (navigation friction)
- Are already specified in HYP-002 (ICE=8.3), HYP-004 (ICE=8.0), HYP-009 (ICE=7.0) — the top P1 Immediate hypotheses

**Phase 2 implication:** After Must-be items are addressed (Wave 2/3), Performance features represent the highest-density ROI cluster for Wave 2 README and docs/index.md revisions.

### Implication 3: Attractive Features Create the Jerry Brand Story

The Diataxis documentation suite (A2) and WCAG compliance (A1) together constitute what distinguishes Jerry documentation from all six competitive frameworks (FEAT-040-055 AP-05; FEAT-040-056 D-01). FEAT-040-056 finding M-04 establishes that no OSS project applies HEART to its docs rigorously — adding full Diataxis structure + HEART-tracked metrics + WCAG AA conformance would make Jerry's documentation model a genuine competitive differentiator.

**Phase 2 implication:** Frame Wave 4/5 as "documentation-as-product" positioning story for XP-04 (Positioning) — the documentation experience itself is differentiated, not just the underlying framework.

### Implication 4: QG-2 Seed Attributes Validated

QG-2 recommended seeding Kano with TC-002 and TC-004 as known Performance attributes. This analysis confirms:
- TC-002 (skill catalog invisibility) classifies as **Must-be (M)**, not Performance — the absence is more damaging than QG-2 estimated because the hidden-catalog pattern (AP-02) directly blocks user activation, not merely reducing it.
- TC-004 (zero tutorial coverage) classifies as **Must-be (M)**, consistent with QG-2 recommendation — this is the single highest-priority implementation target.

**Upward reclassification note:** QG-2 used "Performance" as a conservative seed. The Kano evidence from JTBD Anxiety=5 scores, triple-convergence, and FEAT-040-056 D-03 ("tutorials weakest quadrant") supports elevating both to Must-be. The practical difference: Must-be items are non-negotiable prerequisites for any meaningful user activation; Performance items improve activation proportionally. TC-002 and TC-004 are prerequisites, not proportional improvements.

---

## Synthesis Judgments Summary

| # | Judgment | Type | Confidence | Rationale |
|---|----------|------|------------|-----------|
| SJ-001 | Tutorial coverage (TC-004) classified as Must-be rather than Performance despite QG-2 seed of "Performance" | Classification | MEDIUM | JTBD Anxiety=5 (Cat 4), triple-convergence TC-004 in 5 independent deliverables, D-03 "tutorials weakest quadrant" — all point to table-stakes absence, not proportional improvement. Three independent frameworks agree on Must-be direction. **CAVEAT (PROVISIONAL Must-be or Performance):** The dysfunctional question evidence required to distinguish Must-be (absence causes abandonment) from Performance (absence causes proportional friction) is unavailable in Phase 1a — JTBD Anxiety=5 establishes urgency, not the Kano M/O threshold. Users who find zero tutorials may use alternative paths (reading source code, community channels, CLAUDE.md) and experience proportional frustration rather than abandoning Jerry entirely. Must-be classification is an inference from JTBD urgency signals; pending user-survey validation, treat as "PROVISIONAL Must-be or Performance." Survey required to resolve. |
| SJ-002 | Skills table completeness (TC-002) classified as Must-be rather than Performance | Classification | MEDIUM | AP-02 hidden-catalog anti-pattern (FEAT-040-055) confirms this is a discovery-reducing issue. HYP-004 ICE=8.0 with P1 Immediate classification reflects high practitioner confidence. Reclassification from QG-2 seed is justified. **CAVEAT (confirmed Performance candidate):** TC-002 is Performance-degrading — users can activate on the 7 visible skills. Must-be classification is an inference; the 7/19+ discovery gap reduces the quality of skill discovery but does not create a zero-discovery state. The "25/29 skills have zero documentation pages" evidence is a separate gap from the homepage catalog table being incomplete (F-020 is Sev-2, not Sev-3). If survey confirms users accept the 7-skill catalog without abandonment, TC-002 validates as Performance (O) rather than Must-be (M). The survey dysfunctional question is the required instrument to resolve this boundary. |
| SJ-003 | Getting-started Path A/B (full experience) flagged as Split (M↔A boundary) | Classification | MEDIUM | Scope ambiguity is genuine — routing block alone is Must-be (M4 row), full two-tutorial experience is Attractive. Without knowing Phase 2 scope commitment, the classification cannot be resolved. EXP-001/EXP-002 results needed. |
| SJ-004 | Code block language specifiers (W-006) classified as Attractive (not Performance) | Classification | LOW-MEDIUM | HYP-008 is P2 (validate first), not P1 Immediate. AT-specific impact; general users indifferent. Confidence score (C=6) in ICE reflects that benefit is real but narrow. Attractive is the more conservative assignment (P-022: lower score when uncertain). |
| SJ-005 | Inferred response distributions constructed from N=20 hypothetical respondent pool | CS Interpretation | LOW | No survey data exists. Distributions reflect evidence-weighted proxies, not actual user responses. CS coefficients are directional indicators, not validated measures. All downstream use must be labeled provisional. |
| SJ-006 | WCAG compliance classified as Attractive (not Performance) given current EAA 2025 lifecycle | Lifecycle | LOW-MEDIUM | EAA 2025 legal effect means WCAG is transitioning from Attractive to Performance faster than the 12-24 month estimate for EU enterprise contexts. Conservative classification as Attractive is appropriate for current aggregate state (A1/A2 majority). **Citation caveat:** EAA lifecycle claim traces to FEAT-040-056 synthesis finding A-03, which is a secondary synthesis source, not a primary regulatory citation. Per FEAT-040-056 synthesis of EAA 2025 discussion (A-03); primary EAA Directive 2019/882/EU source not independently verified in Phase 1a research. **OSS scope caveat:** EAA enforcement applies to commercial providers offering products/services in the EU market; OSS projects distributed on GitHub have a separate compliance scope — lifecycle migration for Jerry OSS is indirect (via enterprise adopter requirements). Treat 6-12 month migration estimate as conditional on enterprise adoption context, not as a universal OSS obligation. Confidence downgraded from MEDIUM to LOW-MEDIUM to reflect secondary-source limitation and OSS scope uncertainty. |
| SJ-007 | Jargon glossary and authoritative Jerry one-liner classified as separate Performance features | Classification | LOW-MEDIUM | These could be a single feature (TC-003 reframe covers both). Separated to allow independent prioritization. If treated as one feature, the combined Better coefficient rises to ~0.78 and \|Worse\| to ~0.77. |
| SJ-008 | No features classified as Indifferent | Classification | MEDIUM | All 12 features were drawn from Phase 1a discovery evidence, which is inherently biased toward high-priority problems. True Indifferent items (e.g., cosmetic typographic changes, non-user-visible infrastructure) were not in scope. A full Kano survey would likely surface Indifferent candidates. |
| SJ-009 | Priority matrix positions all features in three quadrants (none in Indifferent quadrant) | Priority | MEDIUM | Consistent with SJ-008. Selection bias from discovery-driven feature scope. The absence of Indifferent items reflects scoping, not a claim that all Jerry documentation items are satisfaction-relevant. |
| SJ-010 | Breadcrumbs + search preview classified as Performance (not Must-be) despite F-014 Sev-3 rating | Classification | MEDIUM | F-014 Sev-3 reflects cognitive burden severity, not activation-blocking severity. Users CAN complete tasks without breadcrumbs (they must recall rather than recognize). Must-be classification requires absence to cause active dissatisfaction, not merely friction. |

---

## Handoff Data

```yaml
from_agent: ux-kano-analyst
engagement_id: UX-040-003
feature_count_total: 13   # 4M + 4O + 4A + 1Split (Split counted separately from 4 Attractive)
handoff_feature_count_confirmed: 12  # 13 total minus 1 SPLIT feature pending domain expert resolution
respondent_count: 0
statistical_adequacy: provisional_pending_survey
sample_size_confidence: LOW
provisional_warning: "ALL classifications inferred from Phase 1a proxy evidence — no survey data; validate at N=20+ before roadmap commitments (Berger et al. 1993). See classification_mode field on each entry."
classification_mode_global: inferred_provisional
category_distribution:
  must_be: 4
  performance: 4
  attractive: 4
  split: 1
  indifferent: 0
  reverse: 0
split_count: 1
conflict_count: 2
lifecycle_features_assessed: 8
artifact_path: projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-003/ux-kano-analyst-output.md

feature_classifications:
  - feature: "Tutorial coverage (TC-004)"
    category: M
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    classification_caveat: "PROVISIONAL Must-be or Performance — dysfunctional survey question required to distinguish abandonment (M) from proportional friction (O)"
    confidence: MEDIUM
    better: 0.25
    worse: -0.85
    quadrant: Must-be
    evidence: [TC-004, HYP-006, F-013, D-03, JTBD-Cat4-Anxiety5]

  - feature: "Skills table completeness (TC-002)"
    category: M
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    classification_caveat: "PROVISIONAL Must-be — confirmed Performance candidate if survey shows users accept 7-skill catalog without abandonment; F-020 is Sev-2 not Sev-3"
    confidence: MEDIUM
    better: 0.35
    worse: -0.80
    quadrant: Must-be
    evidence: [TC-002, F-020, HYP-004, AP-02, JTBD-25-of-29]

  - feature: "INSTALLATION.md heading structure (W-001)"
    category: M
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    classification_caveat: "PROVISIONAL — strongest evidence basis of Must-be cluster (3-framework convergence); still requires survey validation"
    confidence: HIGH
    better: 0.30
    worse: -0.85
    quadrant: Must-be
    evidence: [W-001, HYP-011, B-MAP-Ability, TC-001]

  - feature: "Getting-started path disambiguation (TC-001/TC-005)"
    category: M
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    classification_caveat: "PROVISIONAL Must-be — B=MAP primary bottleneck drives classification; survey validation required"
    confidence: MEDIUM
    better: 0.35
    worse: -0.80
    quadrant: Must-be
    evidence: [TC-001, TC-005, B-MAP-Prompt, F-016, HYP-001]

  - feature: "Cross-linking skill→playbook (F-013)"
    category: O
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: MEDIUM
    better: 0.75
    worse: -0.75
    quadrant: Performance
    evidence: [F-013, HYP-004, D-03, TC-004]

  - feature: "Jargon glossary / plain-language (TC-003/F-011)"
    category: O
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: MEDIUM
    better: 0.75
    worse: -0.75
    quadrant: Performance
    evidence: [F-011, TC-003, HYP-010, Brain-Cycles-a]

  - feature: "Authoritative Jerry one-liner (F-011/HYP-010)"
    category: O
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: LOW-MEDIUM
    better: 0.75
    worse: -0.65
    quadrant: Performance
    evidence: [F-011, TC-003, C-03-C-04-FEAT-040-056]

  - feature: "Sidebar breadcrumbs + search preview (F-014)"
    category: O
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: MEDIUM
    better: 0.75
    worse: -0.70
    quadrant: Performance
    evidence: [F-014, HYP-009, SD-01-SD-03]

  - feature: "WCAG compliance enhancements (W-011/W-013/W-014)"
    category: A
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    classification_caveat: "PROVISIONAL Attractive (aggregate A1/A2/A6); A6 Domain Specialist may classify as Must-be under EAA obligation — segment survey required"
    confidence: MEDIUM
    better: 0.75
    worse: -0.30
    quadrant: Attractive
    evidence: [W-013, W-014, W-011, A-03-FEAT-040-056, EAA-2025]

  - feature: "Getting-started Path A/B full split [SPLIT]"
    category_split:
      scope_a: M   # Step-3 routing block only — Must-be; resolves B=MAP Prompt bottleneck
      scope_b: A   # Full two-tutorial experience (INSTALLATION-plugin.md + INSTALLATION-clone.md) — Attractive
      resolution: domain_expert_required
      split_context: "Scope A (minimal routing block) is Must-be (M4 row). Scope B (full polished two-tutorial experience) is Attractive. See Split Classification Analysis section."
    category: A   # Default to Scope B (Attractive) pending domain expert scope decision
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: LOW
    better: 0.75
    worse: -0.40
    quadrant: Attractive
    evidence: [HYP-002, HYP-003, TC-005, EXP-001, EXP-002]
    split_flag: true
    domain_expert_required: true

  - feature: "Diataxis documentation suite (TC-004/D-01)"
    category: A
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: MEDIUM
    better: 0.75
    worse: -0.30
    quadrant: Attractive
    evidence: [D-01, AP-05, TC-004, FEAT-040-055]

  - feature: "Code block language specifiers (W-006)"
    category: A
    kano_classification_provisional: true
    classification_mode: inferred_provisional
    confidence: LOW
    better: 0.60
    worse: -0.20
    quadrant: Attractive
    evidence: [W-006, HYP-008]

phase2_synthesis_inputs:
  must_be_prerequisites:
    - "Tutorial coverage — Wave 4a immediate; no Wave 4b/5 work before this"
    - "Skills table — Wave 2 README update; P1 Immediate from ICE matrix"
    - "INSTALLATION.md H3 headings — Wave 3 remediation; ~1hr effort"
    - "Step 3 routing block — Wave 2/3 remediation; EXP-001 gates full scope"
  performance_investments:
    - "Cross-linking + jargon cluster (O1+O2+O4) — Wave 2 README/docs/index.md"
    - "Breadcrumbs + search (O3) — Wave 3 site-level; MkDocs Material config"
  attractive_differentiation:
    - "WCAG enhancements — Wave 3 (W-001, W-011); Wave 5 (W-013, W-014, W-006)"
    - "Diataxis suite — Wave 4a/b/c/d progressive delivery"
    - "Path A/B full split — Wave 4a after EXP-001/EXP-002 validate"
  validation_recommended:
    survey_design: true
    min_respondents: 20
    target_segments: ["A1 Solo Engineer", "A2 Technical Lead", "A6 Domain Specialist"]
    priority_features_to_validate:
      - "Tutorial coverage (M1) — validate Must-be vs Performance boundary"
      - "Getting-started Path A/B scope (SPLIT) — validate scope boundary"
      - "Code block specifiers (A4) — validate Attractive vs Indifferent boundary"
```

---

## Self-Score (S-014 LLM-as-Judge)

**Criticality: C3. Threshold: 0.92. Iteration: 2.**

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.93 | All 12 features classified; lifecycle assessed for 8/12 features; all output artifacts specified. Arithmetic proof rows added to Executive Summary resolving the N=20 distribution → Worse value chain. YAML handoff now carries PROVISIONAL flags on all 12 entries and structured split-feature fields. Scope expansion (W-001 addition) is documented inline. Minor residual gap: WCAG text partially read in iter-1 (acknowledged in iter-1 score); unchanged in iter-2. |
| Internal Consistency | 0.20 | 0.93 | CS coefficient arithmetic inconsistency resolved: Executive Summary Worse values now match coefficient table for all three Must-be features (Tutorial -0.85, Skills table -0.80, INSTALLATION.md -0.85). Arithmetic proof rows added. YAML handoff values match. SJ-001/SJ-002 confidence levels updated (HIGH → MEDIUM for SJ-001; MEDIUM-HIGH → MEDIUM for SJ-002) to reflect M/O boundary caveat. No remaining arithmetic contradiction across sections. |
| Methodological Rigor | 0.20 | 0.93 | M/O boundary caveat added to SJ-001 and SJ-002: both explicitly acknowledge that the Kano dysfunctional question pair is the required instrument and that JTBD Anxiety=5 establishes urgency but not the abandonment threshold required for Must-be. Proxy methodology limitations now stated in the methodology section. Persona heterogeneity note added to methodology section. The caveat preserves the classification while accurately representing its provisional nature. |
| Evidence Quality | 0.15 | 0.92 | EAA citation updated in SJ-006 and lifecycle table: now cites Directive 2019/882/EU explicitly, acknowledges A-03/FEAT-040-056 as secondary synthesis source not independently verified, and adds OSS scope caveat. SJ-006 confidence downgraded from MEDIUM to LOW-MEDIUM to reflect secondary-source limitation. Arithmetic inconsistency in Executive Summary citations resolved. Residual gap: EAA primary source not independently accessed in this analysis (secondary-source citation limitation remains, but is now disclosed). |
| Actionability | 0.15 | 0.93 | Survey-contingency caveat added to Strategic Implications Implication 1: explicitly states that if TC-002/TC-004 validate as Performance, O1-O4 runs co-equal in Wave 2. Wave sequencing is now framed as provisional recommendation contingent on survey validation rather than definitive conclusion. Survey-designed-by-persona note added. All 7 Major blockers addressed. |
| Traceability | 0.10 | 0.93 | EAA Directive 2019/882/EU now cited with explicit acknowledgment of secondary-source limitation. YAML PROVISIONAL flags and structured split-feature fields added. Revision history appended with 7 closure records traceable to adv-review finding IDs. All SJ confidence changes documented with rationale cross-referencing adv-review finding IDs. |

**Weighted composite (iter-2):**
```
Completeness:         0.93 × 0.20 = 0.186
Internal Consistency: 0.93 × 0.20 = 0.186
Methodological Rigor: 0.93 × 0.20 = 0.186
Evidence Quality:     0.92 × 0.15 = 0.138
Actionability:        0.93 × 0.15 = 0.140
Traceability:         0.93 × 0.10 = 0.093

COMPOSITE: 0.186 + 0.186 + 0.186 + 0.138 + 0.140 + 0.093 = 0.929
```

**Self-Score: 0.929 (PASS — above 0.92 threshold for C3)**

**Confidence in self-score:** MEDIUM. Evidence Quality scores 0.92 (not 0.93) because the EAA primary-source citation remains secondary — the EAA Directive 2019/882/EU reference is now disclosed as such but the actual directive was not independently accessed in this analysis. All seven Major blockers from iter-1 adv-review are closed. Expected adversarial band: 0.91–0.93.

**Leniency check:** Internal Consistency raised from 0.86 (iter-1 adv-review score) to 0.93 — justified because the specific arithmetic failure (−0.93 vs −0.85) is fully corrected with arithmetic proofs. Methodological Rigor raised from 0.90 to 0.93 — justified because the M/O boundary caveat directly addresses the gap cited by adv-review (missing discussion of dysfunctional question reliance). Actionability raised from 0.90 to 0.93 — justified by the explicit survey-contingency caveat in Implication 1. Evidence Quality held at 0.92 (not 0.93) because the EAA primary source was not independently verified. Traceability raised from 0.91 to 0.93 — YAML PROVISIONAL flags and Directive citation added.

---

## References

- Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). "Attractive quality and must-be quality." *Journal of the Japanese Society for Quality Control*, 14(2), 39–48.
- Berger, C., Blauth, R., Boger, D., et al. (1993). "Kano's methods for understanding customer-defined quality." *Center for Quality Management Journal*, 2(4), 3–36.
- Matzler, K. & Hinterhuber, H.H. (1998). "How to make product development projects more successful by integrating Kano's model." *Technovation*, 18(1), 25–38.
- Nielsen, J. (1994). "Usability Inspection Methods." *CHI '94 Proceedings.*
- Ulwick, A. (2005). *What Customers Want.* McGraw-Hill. (ODI framework)
- Gothelf, J. & Seiden, J. (2021). *Lean UX* (3rd ed.). O'Reilly. (Hypothesis format, ICE scoring)
- W3C (2023). WCAG 2.2, https://www.w3.org/TR/WCAG22/
- Procida, D. (2021). Diataxis framework, https://diataxis.fr
- European Parliament and Council (2019). Directive 2019/882/EU on the accessibility requirements for products and services (European Accessibility Act). *Official Journal of the European Union.* *(Cited via secondary synthesis A-03/FEAT-040-056; primary directive not independently verified in this analysis.)*

---

## Revision History

| Iteration | Date | Score | Verdict | Changes |
|-----------|------|-------|---------|---------|
| iter-1 | 2026-04-20 | 0.930 (self) | PASS claimed by self; REVISE by adv-review (0.894) | Initial inferred classification. 12 features. TC-002/TC-004 elevated from QG-2 seed (Performance) to Must-be. INSTALLATION.md heading structure added from triple-convergence. Getting-started Path A/B flagged SPLIT. |
| iter-2 | 2026-04-20 | 0.929 (self) | PASS (self-score above 0.92) | **7 Major blockers closed:** (1) CC-001/FM-001/DA-004: Arithmetic correction — Executive Summary Worse values reconciled with coefficient table for all 3 Must-be features (-0.93→-0.85, -0.87→-0.80, -0.82→-0.85); arithmetic proof rows added. (2) DA-001/IN-001: SJ-001 Must-be caveat — "PROVISIONAL Must-be or Performance" language added; JTBD Anxiety≠Kano dysfunctional question acknowledged; confidence HIGH→MEDIUM. (3) DA-002: SJ-002 TC-002 reframe — confirmed Performance candidate language added; F-020 Sev-2 vs Sev-3 distinction made explicit; confidence MEDIUM-HIGH→MEDIUM. (4) PM-001: Strategic Implications Implication 1 — survey-contingency caveat added ("if TC-002/TC-004 validate as Performance, O1-O4 runs co-equal"). (5) PM-002: A6 persona heterogeneity — note added to WCAG lifecycle section and methodology section; segment-by-persona survey recommendation added. (6) DA-003/IN-002/PM-003: EAA citation — SJ-006 updated with Directive 2019/882/EU reference, A-03 secondary-source disclosure, OSS scope caveat, confidence MEDIUM→LOW-MEDIUM. (7) FM-002/FM-003: YAML PROVISIONAL flags — `kano_classification_provisional: true` and `classification_mode: inferred_provisional` added to all 12 feature entries; structured `category_split` fields added to Path A/B split entry; `provisional_warning` top-level field added. |

---

*Agent: ux-kano-analyst v1.1.0 | Engagement: UX-040-003 | FEAT-040-003 | 2026-04-20*
*Classification mode: Inferred (no survey data) | Provisional — pending user survey validation*
*Upstream: FEAT-040-001, 004, 005, 007, 056, QG-2 | Phase 1b dispatch*
*Iter-2: 7 Major blockers closed (CC-001, DA-001, DA-002, PM-001, PM-002, DA-003/IN-002/PM-003, FM-002/FM-003)*
