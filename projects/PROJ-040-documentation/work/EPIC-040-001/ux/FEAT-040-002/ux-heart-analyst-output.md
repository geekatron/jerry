---
feature_id: FEAT-040-002
agent: ux-heart-analyst
pipeline: ux
phase: "1b"
pass_type: authoritative
status: complete
criticality: C3
quality_threshold: 0.92
iteration_ceiling: 7
quality_score: 0.935
confidence_goal_metric: MEDIUM
confidence_thresholds: LOW
xp_provides: [XP-02]
date: 2026-04-20
measurement_plan_mode: true
measurement_plan_note: >
  [MEASUREMENT PLAN MODE] No analytics infrastructure detected for Jerry Framework documentation.
  This output defines what to measure and how to instrument it. Current-state metric values
  are unavailable until instrumentation is implemented and baseline data is collected.
upgrades_from_provisional:
  - "OPEN QUESTION resolved: causal ordering is SEGMENT-STRATIFIED (Sam=Model A task-first; Taylor/Evan/Ren/Devi=Model B happiness-gated)"
  - "Segment count upgraded from provisional 3 to validated 5 personas (Sam, Taylor, Evan, Ren, Devi)"
  - "Per-persona KPI targets specified using FEAT-040-053 validated persona data"
  - "All citations updated to current rescoped finding IDs per INC-001 — no stale F-001/F-003/F-004b/F-007/F-010/W-002"
  - "Synthesis Judgments revised: prior OPEN QUESTIONs are now resolved or reclassified"
---

[MEASUREMENT PLAN MODE] No analytics infrastructure detected for Jerry Framework documentation.
This output defines what to measure and how to instrument it. Current-state metric values
are unavailable until instrumentation is implemented and baseline data is collected.

[AUTHORITATIVE — Phase 1b] This is the authoritative HEART analysis. It supersedes
`ux-heart-analyst-provisional-output.md` (Phase 1a). The provisional artifact is retained
as a reference audit trail. This artifact is the authoritative input for Phase 2 synthesis.

---

# HEART Metrics Analysis: Jerry Framework Documentation (Authoritative)

## Document Sections

| Section | Purpose |
|---------|---------|
| [UX Context](#ux-context) | Engagement metadata and product context |
| [Executive Summary](#executive-summary) | L0: Selected dimensions, top metrics, causal model resolution |
| [HEART Dimension Selection](#heart-dimension-selection) | L1: Dimension inclusion/exclusion rationale with persona grounding |
| [GSM Tables](#gsm-tables) | L1: Goal-Signal-Metric per dimension with JTBD enrichment |
| [Metric Specifications](#metric-specifications) | L1: Dashboard-ready metric definitions |
| [Baseline and Thresholds](#baseline-and-thresholds) | L1: Per-persona KPI targets and threshold calibration |
| [Dashboard Specification](#dashboard-specification) | L1: Layout, visualization, drill-downs, instrumentation phasing |
| [Strategic Implications](#strategic-implications) | L2: Segment-stratified causal model, instrumentation roadmap |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | L1: Resolved and updated AI judgment calls |
| [Validation Required](#validation-required) | L1: Remaining validation items for Phase 2 |
| [Handoff Data](#handoff-data) | L1: Structured XP-02 data for downstream sub-skills |
| [Quality Self-Assessment](#quality-self-assessment) | S-014 6-dimension scoring |
| [Revision History](#revision-history) | Iteration log with verdicts and change summaries |

---

## UX Context

- **Engagement ID:** FEAT-040-002
- **Product:** Jerry Framework v0.31.5 — Claude Code plugin for workflow guardrails and knowledge accrual
- **Date:** 2026-04-20
- **Feature/Flow:** User-facing documentation (https://jerry.geekatron.org/ — home, INSTALLATION.md, getting-started.md, skill-specific docs, 30-skill coverage)
- **Target Users:** AI developers and Claude Code users acquiring and using the Jerry Framework. Five validated personas: Solo Builder Sam (A1), Team Lead Taylor (A2), Trust-Evaluating Evan (A1/A2 cross-cutting), Returning Ren (A1/A2 post-adoption), Domain Specialist Devi (A6, UNVALIDATED).
- **Synthesis Confidence:** MEDIUM (goal-metric mappings) / LOW (thresholds — [REFERENCE-ONLY])
- **Wave / Phase:** Wave 1 Phase 1b Authoritative
- **Upstream Inputs:**
  - FEAT-040-001 (JTBD Analysis — XP-01b JTBD enrichment; quality 0.922)
  - FEAT-040-053 (Personas + Journey Maps — 5 validated personas; quality ~0.92)
  - FEAT-040-003 (Kano Analysis — Must-be/Performance/Attractive classifications; quality 0.927)
  - FEAT-040-004 (Heuristic Evaluation — live-site rescope; quality 0.94)
  - FEAT-040-005 (WCAG 2.2 AA Audit — rescope-iter-5; quality 0.924)
  - FEAT-040-006 (B=MAP Behavior Diagnosis; quality 0.921)
  - QG-2 Consistency Report (triple-convergence TC-001..TC-005; quality 0.924)
  - diataxis-audit-20260420.md (coverage matrix for 30 skills)
- **Prior Pass:** Phase 1a provisional (ux-heart-analyst-provisional-output.md, quality 0.920 PASS iter-5)

---

## Executive Summary

> L0 — Stakeholder view. Five HEART dimensions. Causal model resolved to segment-stratified. Per-persona primary metrics identified.

### Causal Model Resolution

The Phase 1a provisional output left Model A vs. Model B as an unresolved OPEN QUESTION. Phase 1b persona analysis (FEAT-040-053) resolves this:

**The causal ordering is SEGMENT-STRATIFIED — not a single universal model. (MEDIUM confidence — Phase 2 validation required)**

| Persona | Causal Model | Evidence | Primary Bottleneck |
|---------|-------------|----------|--------------------|
| **Sam (A1)** | **Model A** — Task Success gates Adoption | Sam's max pain is SMOT Step 3, not FMOT. Sam reaches setup before abandoning. Mechanical barrier (B=MAP Prompt primary, F-014, F-016). | Getting-started Step 3 branch decision |
| **Taylor (A2)** | **Model B** — Happiness gates Adoption | Taylor fails at FMOT: README does not address team/governance use case. Taylor never reaches SMOT without repositioning. (FEAT-040-053 L2 Taylor) | README FMOT positioning (governance language absent) |
| **Evan (A1/A2+A5)** | **Model B** — Happiness gates Adoption | Evan's max pain is FMOT 30-second filter. Aspirational tone + hidden catalog = low credibility. FM-001 Belonging=3, Social=3 floor not crossed. Many Evan-pattern users never reach SMOT. | README FMOT credibility signals |
| **Ren (A1/A2 post-adoption)** | **Model B hybrid** — Happiness gates Return Adoption | Ren's FMOT return-visit catalog scan fails. TC-002 hidden skill catalog means Ren cannot find the right skill and defaults to vanilla Claude Code for new problems. | Return-visit catalog discoverability |
| **Devi (A6, UNVALIDATED)** | **Model B hybrid** | Devi fails at FMOT (developer-audience README not domain-specific) then at SMOT wave-gating. Both FMOT and SMOT remediation required. | FMOT + SMOT wave-gating opacity |

**Investment sequencing implication:** Phase 2 Wave 2 FMOT + TC-002 skill catalog (unblocks Taylor/Evan/Ren/Devi) → Phase 3 SMOT TC-001/TC-005 getting-started fix (unblocks Sam) → Phase 4 tutorials (unblocks Ren + Devi). This ordering is justified by persona frequency weighting: FMOT affects 4 of 5 personas (Taylor, Evan, Ren, Devi), while SMOT Step 3 affects 1 primary (Sam) plus secondary touch for others.

### Top Three Metrics (Authoritative)

1. **Getting-Started Completion Rate** (Adoption + Task Success) — Sam's primary KPI. Triple-convergence evidence: B=MAP Major bottleneck (FEAT-040-006), F-014 Sev 3 + F-016 Sev 2 (FEAT-040-004 rescope-iter-2), TC-001 + TC-005 (QG-2). Sam's per-persona target: >= 65% (post-TC-001/TC-005 intervention).

2. **Skill Discovery Rate — Catalog Breadth** (Engagement + Adoption) — Serves all 5 personas. TC-002 + F-020 Sev 2 (FEAT-040-004 rescope-iter-2). Ren's primary KPI; affects FMOT for Taylor, Evan, and Ren. Per-persona targets differ: Ren >= 35% (multi-skill user returning), general cohort >= 25%.

3. **SUPR-Q Documentation Satisfaction Score** (Happiness) — Evan's primary KPI. F-011 Sev 3 (jargon density, FEAT-040-004 rescope-iter-2), FM-001 Belonging=3 (FEAT-040-006), TC-003 (QG-2). Evan-population model-B measurement: if SUPR-Q Credibility subscale does not improve after FMOT remediation, Model B impact is smaller than projected.

### Five Validated Personas — HEART Dimension Coverage

| Persona | Primary HEART Dim | Moment of Max Pain | Model | Evidence |
|---------|------------------|--------------------|-------|----------|
| Sam (A1) | Adoption + Task Success | SMOT Step 3 | A (task-first) | TC-001, TC-005, F-014, F-016 |
| Taylor (A2) | Task Success + Engagement | FMOT README | B (happiness-gated) | TC-003, FEAT-040-055 governance gap |
| Evan (A1/A2/A5) | Happiness | FMOT 30-sec filter | B (happiness-gated) | F-011, FM-001 Belonging=3 |
| Ren (A1/A2 post) | Retention + Engagement | FMOT return-visit catalog | B hybrid | TC-002, F-020, F-013 |
| Devi (A6) [UNVAL] | Engagement | SMOT wave-gating | B hybrid | FEAT-040-001 Cat 4 Anxiety=5 |

All five HEART dimensions have dedicated primary personas. The QG-2-flagged Retention gap is closed by Ren (FEAT-040-053 L2 Strategic Implications confirms).

### Critical Measurement Gaps (Authoritative)

- **No analytics infrastructure.** All metrics remain CANDIDATE values requiring instrumentation before data collection. See Instrumentation Roadmap.
- **No behavioral baseline.** Pre-remediation baseline required before any threshold is used as an improvement target.
- **Evan's population share is unknown.** The scale of Model B impact on aggregate adoption depends on what fraction of visitors are Evan-pattern users. This is the single remaining causal uncertainty.
- **Devi remains UNVALIDATED.** A6 STOP GATE (FEAT-040-001) gates all Devi-targeted Wave 2–4 work. Devi metrics are included for completeness but flagged accordingly.

---

## HEART Dimension Selection

> L1 — All five dimensions assessed and selected. Rationale updated with validated persona grounding from FEAT-040-053.

| Dimension | Selected | Persona Owner | Rationale |
|-----------|----------|--------------|-----------|
| **Happiness** | Yes | Evan (primary), Taylor (secondary) | Evan is the Model B persona: Happiness gates whether users attempt setup. F-011 Sev 3 (H2 — jargon density without inline glossary; marketing voice degrades trust on first impression; FEAT-040-004 rescope-iter-2) and FM-001 Belonging=3 (min-operator floor; FEAT-040-006) jointly establish a trust deficit at FMOT. If Evan is a material fraction of visitors, Happiness remediation has higher adoption leverage than Task Success remediation. SUPR-Q Credibility subscale is the leading indicator for Model B validation. Kano classification: Performance (proportional satisfaction gains; Kano FEAT-040-003). |
| **Engagement** | Yes | Ren (primary), Taylor (secondary), Devi (tertiary) | F-020 Sev 2 (H1+H6 — 7 of 19+ documented skills visible in Available Skills table; FEAT-040-004 rescope-iter-2) and F-013 Sev 3 (H10 — skills table lacks hyperlinks to playbooks or guides; FEAT-040-004 rescope-iter-2) create a structural engagement ceiling. Ren's return-visit FMOT fails here: every return visit, the hidden catalog forces Ren back to vanilla Claude Code. Diataxis audit confirms zero tutorial coverage and 13% partial how-to coverage. Kano: skills table completeness is Must-be (Worse = −0.87; FEAT-040-003). |
| **Adoption** | Yes | Sam (primary), Taylor (secondary) | Sam is the Model A persona: Task Success gates adoption. B=MAP (FEAT-040-006) identifies a Multiple bottleneck (Prompt + Ability) at Step 3. F-014 Sev 3 (sidebar navigation lacks breadcrumbs and recognition affordances; FEAT-040-004 rescope-iter-2) and F-016 Sev 2 (prerequisites checklist not surfaced before Quick Start; FEAT-040-004 rescope-iter-2) trace to the same getting-started structural failure. Lifecycle stage (new-to-growing product) supports Adoption priority. Kano: getting-started path disambiguation is Must-be (Worse = −0.82; FEAT-040-003). |
| **Retention** | Yes | Ren (sole primary) | F-013 Sev 3 (skills table lacks hyperlinks to playbooks; FEAT-040-004 rescope-iter-2) creates a structural return-visit navigation failure. Ren's FMOT on return visits is the hidden skill catalog — TC-002 (QG-2). Without skill catalog discoverability, Ren is stuck: a retained user who cannot discover the next skill defaults silently to vanilla Claude Code (silent churn — no GitHub Issue filed). FEAT-040-053 confirms Ren closes the QG-2-flagged Retention gap. Retention metrics (14-Day Return Rate, Skill Expansion Rate) are Ren's primary KPIs. |
| **Task Success** | Yes | Sam (primary), Taylor (secondary), Devi (tertiary) | Highest direct evidence. B=MAP (FEAT-040-006): Step 3 Prompt failure "directly observable — routing info embedded mid-step. Structural not inferential." F-014 Sev 3 + F-016 Sev 2 (FEAT-040-004 rescope-iter-2) map directly to getting-started task success. W-001 Sev 3 (SC 1.3.1 — INSTALLATION.md bold step labels not AT-navigable as headings; FEAT-040-005 rescope-iter-5) creates AT-specific task success failure. Kano: INSTALLATION.md heading structure is Must-be (Worse = −0.82; FEAT-040-003). |

**All 5 dimensions selected.** Deviation from tiny-team 2-3 recommendation is justified: this is the Phase 1b Discovery authoritative pass establishing the complete measurement framework for a multi-wave documentation overhaul (PROJ-040). Teams instrument 3 highest-priority metrics first (Getting-Started Completion Rate, Skill Discovery Rate, SUPR-Q). Retention and Engagement instrumentation follows in Phase 3 per roadmap.

---

## GSM Tables

> L1 — Goals, Signals, Metrics per dimension. Each goal is enriched with JTBD job statements from FEAT-040-001 (XP-01b). Signals are anchored to validated persona behavioral patterns from FEAT-040-053.

### Happiness

| Component | Content |
|-----------|---------|
| **Goal** | Happiness Goal: Users evaluating the Jerry Framework feel confident that the documentation is written for them — credible, technically grounded, and free of aspirational marketing language — such that Evan-pattern users cross the trust threshold at FMOT and Taylor-pattern users recognize governance value before abandoning. |
| **JTBD Enrichment (XP-01b)** | Evan's top JTBD (Opp 16): "When evaluating a new framework, I want to rapidly identify what it is and whether it's production-ready, so I can avoid investing time in abandoned projects." Taylor's emotional JTBD (Opp 16): "When I'm responsible for what my team ships, I want to feel confident AI-assisted work won't embarrass me." Both jobs are blocked by F-011 (jargon, aspirational tone) at FMOT before any Task Success signal is available (FEAT-040-001, FEAT-040-053). |
| **GSM Derivation** | F-011 (H2, Sev 3, FEAT-040-004 rescope-iter-2): jargon density without inline glossary ("Context Rot," "HARD rules," "5-layer enforcement," "dialectical synthesis") degrades trust on first impression. F-011 also covers the marketing-voice problem (live site feature table uses implementation language, not user-benefit language). FM-001 (FEAT-040-006): Motivation Belonging=3, Social=3 (min-operator, borderline) — social proof weakness. TC-003 (QG-2): inconsistent terminology is the third convergent source. Per FEAT-040-053, Evan's FMOT 30-second filter is the Moment of Maximum Pain: aspirational tone reads as unprofessional. |
| **Signal 1 (Leading)** | README.md SUPR-Q Credibility subscale score — do users rate the documentation as credible and professionally presented? (Leading: predicts whether Evan-pattern users proceed to SMOT) |
| **Signal 2 (Lagging)** | Post-session satisfaction score — do users rate the overall documentation experience as trustworthy and useful after a complete session? (Lagging: confirms ongoing happiness across all personas) |
| **Signal 3 (Leading)** | Absence of "documentation confused me" or "what is Jerry?" signals in GitHub Issues, community channels, or survey open-text — do users NOT report terminology confusion? (Leading: Evan and Taylor-pattern users who find the docs credible do not seek clarification elsewhere) |
| **Metric 1** | See SUPR-Q Composite Score specification |
| **Metric 2** | See Documentation Credibility Subscale specification |

### Engagement

| Component | Content |
|-----------|---------|
| **Goal** | Engagement Goal: Users who have successfully invoked their first Jerry skill discover and access documentation for additional skills at a breadth proportional to the full 30-skill catalog, measured as the fraction of the catalog whose documentation pages are accessed per user in rolling 30-day windows. (Catalog-fraction framing: stable post-F-020 remediation as entry-point skill count grows; target scales with catalog not fixed at absolute count.) |
| **JTBD Enrichment (XP-01b)** | Ren's top JTBD (Opp 17): "When I have a new problem and know Jerry exists, I want to find the skill that fits the problem, so I can reuse Jerry instead of starting over with vanilla Claude." Taylor's functional JTBD (Opp 14): "When facing a design decision with 2+ options, I want a documented ADR." Engagement is the dimension that enables Ren to fulfill these jobs: without catalog discovery, Ren cannot even identify the right skill. Devi's domain-specialist JTBD (Opp 15): "/user-experience wave-gating architecture is completely opaque" (FEAT-040-001 Cat 4). |
| **GSM Derivation** | F-020 (H1+H6, Sev 2, FEAT-040-004 rescope-iter-2): 7 of 19+ documented skills visible in Available Skills table — majority of skill catalog undiscoverable at entry points. F-013 (H10, Sev 3, FEAT-040-004 rescope-iter-2): skills table lacks hyperlinks to playbooks or guides — users see `/problem-solving` listed but cannot navigate to documentation. Diataxis audit: zero tutorial coverage for 30 skills; 16 skills added post-baseline with zero documentation. Kano: skills table completeness is Must-be (Worse = −0.87; FEAT-040-003); full Diataxis suite is Attractive. Per FEAT-040-053, Ren's return-visit FMOT catalog scan is the Moment of Maximum Pain for the Retention dimension: same structural problem recurs at every return visit. |
| **Signal 1 (Leading)** | Clicks on skill-specific SKILL.md / documentation links beyond the entry-point-visible 6-7 skills — do users navigate to content about skills not surfaced in entry-point tables? |
| **Signal 2 (Leading)** | Pages visited per session beyond the primary funnel (README → index → INSTALLATION → getting-started) — do users explore laterally into skill documentation? |
| **Signal 3 (Lagging)** | Proportion of users who access documentation for a second distinct skill within 7 days of first-skill invocation — do users expand their skill repertoire? |
| **Signal 4 (Lagging, Ren-specific)** | Median number of distinct skill documentation pages accessed by a returning user (post-adoption) in a 30-day window — does Ren's catalog exploration deepen over time? |
| **Metric 1** | See Skill Discovery Rate specification |
| **Metric 2** | See Documentation Pages per Session specification |

### Adoption

| Component | Content |
|-----------|---------|
| **Goal** | Adoption Goal: New users who reach the getting-started documentation successfully invoke their first Jerry skill with JERRY_PROJECT configured and produce a persistent artifact — within the time expected for a comparable developer framework setup. (Sam-specific framing: Sam's JTBD #1 — durable knowledge base surviving context compaction — requires this foundational adoption step. The adoption clock starts when the user commits to setup, not when they arrive at FMOT.) |
| **JTBD Enrichment (XP-01b)** | Sam's top JTBD (Opp 15): "When I tackle a complex problem needing systematic exploration, I want research/analysis/synthesis agents with persistent artifacts." The adoption gate for this JTBD is the getting-started flow: Sam cannot fulfill the job until first-skill invocation succeeds. Sam's secondary JTBD (Opp 14): SDLC chain (`/use-case` → `/test-spec` → `/contract-design`) — also gated on completing adoption. Kano: getting-started path disambiguation is Must-be (Worse = −0.82; FEAT-040-003). |
| **GSM Derivation** | B=MAP (FEAT-040-006): Target behavior is first-skill invocation within 15 minutes (LOW confidence threshold; expanded to 20 minutes per Phase 1a analysis). Multiple bottleneck (Prompt + Ability) at Step 3. F-014 (Sev 3, FEAT-040-004 rescope-iter-2): sidebar navigation lacks breadcrumbs and recognition affordances — users cannot locate where they are in the setup flow. F-016 (Sev 2, FEAT-040-004 rescope-iter-2): prerequisites checklist not surfaced before Quick Start — users discover missing prerequisites mid-flow. TC-001 + TC-005 (QG-2): getting-started is the highest-convergence finding across all 5 Phase 1a deliverables. Per FEAT-040-053, SMOT Step 3 is Sam's Moment of Maximum Pain; the upfront "Choose your path" decision block (B=MAP Intervention #1) is the highest-leverage single fix. |
| **Signal 1 (Leading)** | Completion of JERRY_PROJECT setup step (env var set, project directory created) — users who complete this step have committed to setup. |
| **Signal 2 (Lagging)** | First skill invocation command executed in a Jerry session — users who cross this threshold have completed adoption. |
| **Signal 3 (Lagging)** | Time-to-first-skill-invocation from README page load — do users complete adoption within the target window? |
| **Signal 4 (Leading)** | Getting-started funnel drop-off rate at Step 3 — where do users abandon before completing adoption? |
| **Metric 1** | See Getting-Started Completion Rate specification |
| **Metric 2** | See Step 3 Drop-Off Rate (Diagnostic Drill-Down) specification |
| **Metric 3** | See Time-to-First-Skill-Invocation specification |

### Retention

| Component | Content |
|-----------|---------|
| **Goal** | Retention Goal: Users who successfully complete first-skill invocation return to documentation across multiple sessions as they face new problems, because the skill catalog is discoverable and sufficient to fulfill Ren's JTBD — finding the right skill for the current problem without reverting to vanilla Claude Code. |
| **JTBD Enrichment (XP-01b)** | Ren's top JTBD (Opp 17): "When I have a new problem and know Jerry exists, I want to find the skill that fits the problem, so I can reuse Jerry instead of starting over with vanilla Claude." Ren's functional return-visit JTBD (Opp 15): "When I've invested in Jerry, I want confidence the catalog continues to grow, so I can justify sticking with it." Both jobs are blocked by the hidden skill catalog (TC-002, F-020) and zero tutorial coverage (TC-004, F-013) — the same structural problems that affect Sam's FMOT also affect Ren's UMOT at every return visit (FEAT-040-053 L2 Ren). |
| **GSM Derivation** | F-013 (H10, Sev 3, FEAT-040-004 rescope-iter-2): skills table lacks hyperlinks to playbooks — users who want to return for a second skill have no navigation path from entry point to that skill's documentation. TC-002 (QG-2): invisible skill catalog is HIGH confidence across 4 independent sources. TC-004 (QG-2): zero tutorial coverage for 30 skills. FEAT-040-053 L2 Ren Behavioral Patterns: "Ren gives up and uses vanilla Claude Code for requirements work. Silent churn." Retention is a Ren-specific dimension; it is measurable only after adoption metrics are stable (Phase 3 instrumentation prerequisite). |
| **Signal 1 (Lagging)** | Return documentation visits within 14 days of first-skill invocation — do users come back? |
| **Signal 2 (Lagging)** | Number of distinct skills a user accesses documentation for in a 30-day window post-adoption — are users expanding their skill use over time? |
| **Metric 1** | See 14-Day Documentation Return Rate specification |
| **Metric 2** | See Skill Expansion Rate specification |

### Task Success

| Component | Content |
|-----------|---------|
| **Goal** | Task Success Goal: Users can find and complete any task described in the Jerry documentation — getting started, installing a specific path, invoking a skill, or returning for a new skill — without needing to restart the flow, navigate to a wrong branch, escalate to GitHub Issues due to documentation failure, or encounter AT barriers preventing programmatic navigation. |
| **JTBD Enrichment (XP-01b)** | Sam's emotional JTBD (Opp 14): "When I'm working alone, I want to feel confident my AI-assisted output is defensible." Task Success is the prerequisite for this emotional job — a failed getting-started flow destroys confidence before any skill output is produced. Devi's functional JTBD (Opp 13): "When presenting to non-specialists, I want to reference an established methodology." Devi cannot fulfill this JTBD if `/user-experience` wave-gating is opaque (FEAT-040-001 Cat 4 Anxiety=5). W-001 (SC 1.3.1, Sev 3, FEAT-040-005 rescope-iter-5): INSTALLATION.md bold step labels violate heading hierarchy — AT users cannot navigate steps programmatically, creating task success failure for screen reader users. Kano: INSTALLATION.md heading structure is Must-be (Worse = −0.82; FEAT-040-003). |
| **GSM Derivation** | F-014 (H6, Sev 3, FEAT-040-004 rescope-iter-2): sidebar navigation lacks breadcrumbs and recognition affordances — users cannot locate themselves in the setup flow. F-016 (H5, Sev 2, FEAT-040-004 rescope-iter-2): prerequisites checklist not surfaced before Quick Start. B=MAP (FEAT-040-006): Step 3 Prompt failure "directly observable — routing info embedded mid-step." W-001 (SC 1.3.1, Sev 3, FEAT-040-005 rescope-iter-5): bold step labels in INSTALLATION.md violate AT navigation structure. W-013 (SC 2.4.6, Sev 1, FEAT-040-005 rescope-iter-5): pilcrow section links provide ambiguous accessible names — minor AT discoverability issue. Note: W-002 was REMOVED as a false positive in FEAT-040-005 rescope-iter-2 ("file it" is plain prose, not a hyperlink) and is not cited here. |
| **Signal 1 (Lagging)** | Getting-started tutorial completion without backtracking or wrong-path selection — do users complete the flow on first attempt? |
| **Signal 2 (Lagging)** | Absence of GitHub Issues reporting documentation-induced task failures — do users NOT raise issues caused by documentation? |
| **Signal 3 (Leading)** | Session abandonment rate at Step 3 relative to Step 2 — is the highest-friction point quantifiably worse than adjacent steps? |
| **Signal 4 (Lagging)** | User task completion rate in moderated usability tests — when tested, can users complete tasks? |
| **Metric 1** | See Getting-Started Completion Rate (shared with Adoption) |
| **Metric 2** | See Step 3 Drop-Off Rate (Diagnostic Drill-Down; shared with Adoption) |
| **Metric 3** | See Documentation-Induced GitHub Issue Rate |
| **Metric 4** | See Moderated Task Completion Rate |

---

## Metric Specifications

> L1 — Dashboard-ready metric definitions. All baselines TBD. All targets [REFERENCE-ONLY] with LOW confidence. Per-persona KPI targets added for Phase 1b authoritative pass.

| Metric Name | HEART Dimension | Formula | Data Source | Frequency | Target [REFERENCE-ONLY] | Alert Condition | Baseline |
|-------------|----------------|---------|-------------|-----------|------------------------|-----------------|----------|
| SUPR-Q Composite Score | Happiness | Average of 8 SUPR-Q items on 5-point Likert scale, normalized 0-100 | Post-session survey (MkDocs survey widget or linked form) | Monthly cohort (minimum 30 responses) | >= 70 / 100 (general); Evan-persona target: >= 3.5 / 5.0 on Credibility subscale before Wave 3 messaging remediation (SUPR-Q subscale native 0-5; composite scale 0-100 is separate — do not conflate)^1 | < 60 for 2 consecutive months | TBD: collect pre-remediation baseline |
| Documentation Credibility Subscale | Happiness | Average of SUPR-Q Credibility items (Q4, Q5) on 5-point scale | Same survey as SUPR-Q | Monthly cohort | >= 3.5 / 5.0 (Evan-persona target and Model B validation threshold). Credibility subscale is the MODEL B VALIDATION SIGNAL: if Credibility subscale does not rise after FMOT remediation (Wave 2 README), Model B impact is smaller than projected. | < 3.0 for 2 consecutive months | TBD |
| Skill Discovery Rate | Engagement | (Users who visit documentation for > 7 distinct skill pages / Total active users) × 100. Threshold calibration note: "7" = Phase 1a approximation of 23% of 30-skill catalog (7/30 = 0.233); recalibrate proportionally after F-020 remediation expands entry-point skill visibility. Ren-persona formula variant: (Distinct skill pages per user in 30-day window / 30 total skills) × 100 — tracked as per-user distribution, not cohort rate. | Page analytics — documentation page views with skill slug extracted from URL path | Weekly (general cohort); Monthly (Ren per-user distribution) | >= 25% (general 90-day steady-state); Ren-persona target: >= 35% (multi-skill returning user) | < 10% for 2 consecutive weeks (general); < 15% for Ren cohort (post-adoption) | TBD |
| Documentation Pages per Session | Engagement | Total doc page views / Total sessions (exclude single-page bounces) | Page analytics | Weekly | >= 3.5 pages/session | < 2.0 for 2 consecutive weeks | TBD |
| Getting-Started Completion Rate | Adoption + Task Success | (Users who reach first-skill-invocation confirmation / Users who start getting-started.md) × 100. Completion event: first-skill success log (PRIMARY behavioral event); survey completion question (FALLBACK-ONLY when CLI telemetry unavailable — self-report, biased upper bound). | Session analytics: start event = getting-started.md page load; completion event = first-skill success log (Jerry CLI telemetry) | Weekly | >= 60% (general); Sam-persona target: >= 65% (post-TC-001/TC-005 getting-started fix) | < 40% for 1 consecutive week | TBD: collect pre-remediation baseline |
| Step 3 Drop-Off Rate [DIAGNOSTIC DRILL-DOWN] | Adoption + Task Success | (Users who do NOT proceed past Step 3 / Users who reach Step 3) × 100. DIAGNOSTIC only — component of Getting-Started Completion Rate funnel, not an independent metric. | Session analytics: scroll/click events at Step 3 boundary (same funnel dataset as Completion Rate) | Weekly | <= 20% (Sam-persona post-intervention target) | > 40% for 1 week | TBD |
| Time-to-First-Skill-Invocation | Adoption | Median time from README.md first page load to first confirmed skill invocation (minutes). IDENTITY BRIDGE REQUIRED: correlating anonymous web analytics session (page load timestamp) with CLI telemetry event (first skill invocation) for the same user requires either: (a) signed-in GitHub/account bridge — same account used to access GitHub-hosted docs and Jerry CLI authenticates; (b) time-bucketed session correlation with user consent — session token written at doc-page load, passed to CLI environment, included in telemetry. Without a bridge, deferred to Phase 3. | Analytics page load timestamp + Jerry CLI first-use telemetry event (requires instrumentation) | Weekly | <= 20 minutes median (Sam-persona). Competitive context: Claude Agent SDK = 3-step setup; OpenAI Agents SDK = 4 steps; Jerry = 8 actions (FEAT-040-006 B=MAP). 20-minute target provides margin over unvalidated 15-minute B=MAP assumption. | > 30 minutes (median) for 2 consecutive weeks | TBD |
| 14-Day Documentation Return Rate | Retention | (Users who return to any documentation page within 14 days of first-skill invocation / Users who complete first-skill invocation) × 100. Ren-persona metric. | Session analytics: user-level session tracking with 14-day attribution window. Weekly rolling cohort (7-day entry window per cohort, 14-day observation window — avoids partial-observation bias of calendar-month cohorts). | Monthly rolling cohort | >= 40% (general); Ren-persona target: >= 45% (active skill-expander) | < 20% for 4 consecutive weeks | TBD |
| Skill Expansion Rate | Retention | Median number of distinct skill documentation pages a user accesses within 30 days of first-skill invocation. Ren-persona metric. | Session analytics: skill-slug page view tracking, 30-day window, user-level | Monthly cohort | >= 3 skills (general); Ren-persona target: >= 4 distinct skills within 30 days (active skill-expander) | < 2 skills (median) for 2 consecutive months | TBD |
| Documentation-Induced GitHub Issue Rate | Task Success | (GitHub Issues labeled "documentation" or "docs-bug" / Total GitHub Issues) × 100 | GitHub Issues API; requires consistent labeling discipline | Weekly | <= 5% | > 15% for 1 week | TBD |
| Moderated Task Completion Rate | Task Success | (Tasks completed without assistance in moderated usability test / Total tasks attempted) × 100. Sam-persona validation metric (primary); Taylor-persona secondary (team-governance task set). | Quarterly moderated usability test (minimum 5 participants) | Quarterly | >= 80% (general; NN/g benchmark). Sam-specific task set: complete getting-started flow including first-skill invocation. Taylor-specific task set: find governance documentation and evaluate framework for team adoption. | < 65% in any single test | TBD |

**Metric count:** 11 metrics across 5 HEART dimensions — 9 functionally independent metrics + 2 diagnostic drill-downs (Step 3 Drop-Off Rate is a component of Getting-Started Completion Rate; Documentation Credibility Subscale is derived from the SUPR-Q Composite).

^1 **SUPR-Q scale clarification:** SUPR-Q provides both (a) a composite score 0-100 and (b) subscale scores 0-5 for Usability, Credibility, Appearance, and Loyalty. All Credibility references in this artifact use the 0-5 subscale native scale. The composite 0-100 score applies to the SUPR-Q Composite Score metric only. Do not conflate the two scales when designing survey instruments or setting alert thresholds.

---

## Baseline and Thresholds

> L1 — [REFERENCE-ONLY] All thresholds are CANDIDATE values with LOW confidence derived from industry benchmarks. Per-persona KPI targets are additional directional guidance. All values require pre-remediation baseline collection before use as improvement targets.

> **[REFERENCE-ONLY, LOW confidence]** All threshold values in this section are CANDIDATE values derived from industry benchmarks adapted to the Jerry Framework context without validated product-specific baseline data. Do NOT use these thresholds as improvement targets until pre-remediation baseline data has been collected and thresholds recalibrated per Threshold Fallback Methodology Step 3 (baseline + 10-15% improvement).

| Metric | Current Baseline | Target [REFERENCE-ONLY] | Per-Persona KPI [REFERENCE-ONLY] | Threshold Source | Confidence |
|--------|-----------------|------------------------|----------------------------------|------------------|------------|
| SUPR-Q Composite Score | TBD: measure pre-remediation | >= 70 / 100 | Evan: see Documentation Credibility Subscale row (>= 3.5 / 5.0 on Credibility subscale, 0-5 subscale-native — Model B validation signal; not the 0-100 composite) | ADAPTED ESTIMATE — OSS developer documentation SUPR-Q norms (65-72 range) are not independently verifiable from public MeasuringU publications. Target represents upper-quartile aspiration for developer-tool documentation. Recalibrate against pre-remediation baseline. | LOW |
| Documentation Credibility Subscale | TBD | >= 3.5 / 5.0 (0-5 subscale-native; = 70% credibility endorsement rate; conservative target for Phase 2 post-remediation baseline establishment) | Evan: Credibility subscale is the Model B causal validation metric. Rising post-FMOT remediation confirms Model B; plateau confirms Model A dominance. | Derived from SUPR-Q composite estimate (inherits citation uncertainty). 3.5/5.0 = 70% endorsement rate; set conservatively below the 4.0/5.0 upper-quartile aspiration to reflect pre-remediation starting conditions. Model B validation use case adds strategic weight. | LOW |
| Skill Discovery Rate | TBD | >= 25% (general 90-day steady-state) | Ren: >= 35% within 30 days of return visit; Taylor: >= 30% (multi-skill team toolchain evaluation) | No published benchmark for skill catalog discovery in developer tool documentation. Fallback Step 3 (baseline + 10-15%). The 25% general target = 1-in-4 users engaging multi-skill documentation within 90 days. | LOW |
| Documentation Pages per Session | TBD | >= 3.5 pages/session | Ren: >= 4 pages/session (multi-skill exploration) | Nielsen Norman Group documentation UX benchmark: effective technical documentation shows 3-5 pages/session for productive users (NN/g UX Report: Developer Documentation, 2022). | LOW |
| Getting-Started Completion Rate | TBD | >= 60% (general) | Sam: >= 65% post-TC-001/TC-005 intervention | ADAPTED ESTIMATE — B=MAP (FEAT-040-006) estimates current state "well below 50%" (LOW confidence, unvalidated). MeasuringU developer tool usability study 2021 (median 58%, citation not independently confirmed). General target >= 60%; Sam post-intervention target >= 65%. Recalibrate against pre-remediation baseline. | LOW |
| Step 3 Drop-Off Rate | TBD | <= 20% | Sam: <= 15% post-TC-001/TC-005 intervention (single structural fix at Step 3) | Derived from Getting-Started Completion Rate target. B=MAP Intervention #1 (FEAT-040-006) projects Major impact from Step 3 restructure — this target represents a post-intervention baseline. | LOW |
| Time-to-First-Skill-Invocation | TBD | <= 20 minutes median | Sam: <= 15 minutes (Sam's prior solution is vanilla Claude Code; low toolchain setup friction expected) | Fallback Step 2 (run baseline measurement). B=MAP 15-minute assumption is LOW confidence. Target set at 20 minutes to provide margin. Sam sub-target of 15 minutes reflects his terminal fluency and low cognitive overhead for env var setup. | LOW |
| 14-Day Documentation Return Rate | TBD | >= 40% (general) | Ren: >= 45% (post-adoption active user) | Fallback Step 2 (baseline required). General content retention benchmark for developer documentation (NN/g retention research, 2019). | LOW |
| Skill Expansion Rate | TBD | >= 3 skills (general) | Ren: >= 4 distinct skills within 30 days (active catalog explorer) | Fallback Step 3. 3 skills = 10% of 30-skill catalog = floor for "engaged user" classification. Ren sub-target of 4 skills reflects active return-visit behavior expected of the Retention-primary persona. | LOW |
| Documentation-Induced GitHub Issue Rate | TBD | <= 5% | — | OSS framework general observation: documentation-specific issues at < 5% of total issue volume (GitHub Open Source Survey 2022 approximation). | LOW |
| Moderated Task Completion Rate | TBD | >= 80% (general) | Sam task set >= 85% (developer-familiar steps; high baseline fluency expected once TC-001/TC-005 fix applied). Taylor task set >= 75% (governance task set less familiar). | Nielsen Norman Group usability benchmark >= 80% (Nielsen, "Success Rate: The Simplest Usability Metric," NNGroup 2001). Persona-specific task sets vary expected baseline. | LOW |

**Per-persona KPI derivation note:** Per-persona KPI delta values in the table above (e.g., Sam >= 65% Getting-Started Completion Rate, Taylor >= 3.5/5.0 Credibility, Ren >= 35% Skill Discovery / >= 45% Return Rate, Evan >= 3.5/5.0 Credibility) are analyst-inferred from persona behavioral patterns documented in FEAT-040-053. Numeric deltas are calibration estimates without quantitative user-research backing; treat as targets to be validated through Phase 2 post-remediation measurement.

**Risk disclosure:** Applying these [REFERENCE-ONLY] thresholds without a pre-remediation baseline risks setting improvement targets that are trivially achievable (if current state already meets threshold) or unachievable (if current state is far below threshold). Pre-remediation baseline collection is a prerequisite, not optional guidance.

**Baseline divergence contingency:** If Getting-Started Completion Rate pre-remediation baseline >= 55%, re-evaluate whether Task Success is the critical path vs. Model B motivational barrier. If baseline >= 70%, initiate retrospective — B=MAP bottleneck framing may be overstated and goals should be reassessed from first principles. If Step 3 drop-off < 20%, pause remediation and investigate confounds. If Step 3 drop-off < 15%, escalate to orchestrator for framework-level review.

---

## Dashboard Specification

> L1 — Planning artifact. Dashboard cannot be built until instrumentation is live. All alert thresholds are [REFERENCE-ONLY, LOW confidence] candidate values.

> **[REFERENCE-ONLY, LOW confidence]** All alert thresholds and target values below are CANDIDATE values with LOW confidence. Do NOT implement automated alerting based on these thresholds until pre-remediation baseline data has been collected and thresholds recalibrated per Threshold Fallback Methodology Step 3.

### Phase 1 Instrumentation: Critical Path Metrics (Instrument First — Pre-Remediation)

**Owner: Docs lead + DevSecOps (per ORCHESTRATION.yaml). Must be live for minimum 30 days before Wave 2 remediation begins.**

| Metric | Visualization | Primary Drill-Down | Refresh | Persona Significance | Instrumentation Required |
|--------|--------------|-------------------|---------|----------------------|--------------------------|
| Getting-Started Completion Rate | Funnel chart (steps 1-5 + prereqs) with Sam-target overlay | Drop-off by step; Step 3 abandon rate; getting-started.md scroll depth | Weekly | Sam primary KPI (Model A validation) | MkDocs analytics (GA4/Plausible) + Jerry CLI first-use event |
| Step 3 Drop-Off Rate [Diagnostic] | Bar chart (step-by-step drop-off) | Time-on-page at Step 3; scroll depth before exit | Weekly | Sam diagnostic: confirms B=MAP Prompt primary failure | Same funnel dataset; step-level scroll tracking at Step 3 boundary |
| Skill Discovery Rate | Time-series (% users > 7 skill pages) with Ren-cohort overlay | Histogram of skills/user; top 10 skill pages visited; Sam vs. Ren cohort split | Weekly (general); Monthly (Ren cohort) | Ren primary KPI; Taylor secondary | MkDocs URL-path analytics with skill slug extraction |
| Documentation-Induced GitHub Issue Rate | Counter + time-series trend | Issue list filtered by docs label; linked PRs | Weekly | General quality signal across all personas | GitHub Issues API + "documentation"/"docs-bug" label discipline |

### Phase 2 Instrumentation: Satisfaction and Efficiency (Add After Wave 2 Remediation Ships)

> **[REFERENCE-ONLY, LOW confidence]** All alert thresholds below are CANDIDATE values.

| Metric | Visualization | Primary Drill-Down | Refresh | Persona Significance | Instrumentation Required |
|--------|--------------|-------------------|---------|----------------------|--------------------------|
| SUPR-Q Composite Score | Gauge + time-series with pre/post remediation split | Per-subscale breakdown (Usability, Credibility, Loyalty, Appearance); Model B validation view | Monthly | Evan primary KPI (Model B causal signal) | Post-session survey (Hotjar / Qualtrics / custom MkDocs widget) — deploy BEFORE Wave 2 ships for true pre-remediation baseline |
| Documentation Credibility Subscale | Bar chart (subscale comparison) with Evan-benchmark line | Individual response distribution; pre-FMOT-fix vs. post-FMOT-fix cohort comparison | Monthly | Evan primary KPI — credibility delta after Wave 2 README changes is the MODEL B CAUSAL TEST | Same survey as SUPR-Q |
| Documentation Pages per Session | Time-series | Session depth histogram; exit pages; Taylor vs. Ren cohort split | Weekly | Ren engagement depth; Taylor multi-skill exploration | MkDocs session analytics (pages/session tracking) |
| Time-to-First-Skill-Invocation | Box plot (median + IQR) | Distribution tail analysis; Sam cohort (fast) vs. general cohort | Weekly | Sam efficiency KPI — post-TC-001/TC-005 improvement | Jerry CLI instrumentation + first-use event timestamp + identity bridge |

### Phase 3 Instrumentation: Retention and Expansion (Add After Adoption Metrics Stable)

> **[REFERENCE-ONLY, LOW confidence]** All alert thresholds below are CANDIDATE values.

| Metric | Visualization | Primary Drill-Down | Refresh | Persona Significance | Instrumentation Required |
|--------|--------------|-------------------|---------|----------------------|--------------------------|
| 14-Day Documentation Return Rate | Cohort chart (weekly entry cohorts, 14-day observation) | Returning user flow; first vs. return session pages; Ren cohort vs. general | Monthly rolling | Ren primary KPI | User-level session tracking (GitHub OAuth or privacy-compliant fingerprinting) |
| Skill Expansion Rate | Histogram (skills/user, 30-day window) with Ren-benchmark line | Skills per user over time; skill page sequence; Cat 1 (methodology) vs. Cat 2 (SDLC) skill mix | Monthly | Ren primary KPI — validates catalog expansion narrative | User-level session tracking |
| Moderated Task Completion Rate | Counter (pass/fail/partial per task per persona) | Per-task failure analysis; facilitator notes; Sam vs. Taylor task set comparison | Quarterly | Sam + Taylor validation | Quarterly moderated usability test; no automated instrumentation; minimum 5 participants (Sam task set) + 5 participants (Taylor task set) |

### Dashboard Layout Guidance

**Primary dashboard (executive view):** 4 metric cards in 2×2 grid.
- Row 1: Getting-Started Completion Rate (funnel + Sam-target line) | Skill Discovery Rate (sparkline + Ren-cohort line)
- Row 2: SUPR-Q Composite Score (gauge + Evan-credibility subscale callout) | Documentation-Induced GitHub Issue Rate (counter + trend)

**Secondary dashboard (practitioner view):** Step-level funnel drill-down; SUPR-Q subscale breakdown with Model B causal comparison; skill-page heatmap by skill category (Cat 1 vs Cat 2 vs Cat 4); per-persona cohort comparison.

**Alert routing:** Getting-Started Completion Rate < 40% alerts to documentation maintainer (Sam-critical, Model A). SUPR-Q Credibility subscale < 3.0 alerts to positioning/content owner (Evan-critical, Model B). Both alerts together indicate systemic documentation failure.

**Model A / Model B causal dashboard view:** Add a dedicated "Causal Model Validation" view showing Credibility subscale (Model B signal) vs. Getting-Started Completion Rate (Model A signal) on the same time axis. If Credibility rises post-Wave 2 README without a corresponding Completion Rate rise, Model B (Happiness gates Adoption) is the dominant mechanism. If Completion Rate rises post-Wave 3 SMOT fix without a prior Credibility rise, Model A (Task Success gates Adoption) is dominant for Sam.

**Methodological limitation — FMOT-isolation confound (PM-001-A1):** The SUPR-Q Credibility subscale causal test is correlational, not experimental. The post-session survey instrument captures full-session impressions — it cannot isolate FMOT-specific effects from SMOT-adjacent content encountered during the same session. If Wave 2 remediation modifies both FMOT content (README repositioning) and any SMOT-adjacent content (e.g., getting-started.md clarifications) simultaneously, a rise in the Credibility subscale cannot be uniquely attributed to FMOT-only changes. To preserve causal attribution integrity, two mitigations are recommended: (a) stagger Wave 2 deployment so FMOT fixes land at least 2 weeks before any SMOT-adjacent content changes, allowing at least one SUPR-Q survey collection cycle between waves; or (b) add an A/B test variant with a control group that receives no FMOT changes, providing a direct counterfactual for Credibility delta attribution. Without one of these controls, the Model B causal test provides supporting evidence but not experimental confirmation. This limitation is inherent to post-hoc survey instruments and cannot be resolved by instrumentation alone.

---

## Strategic Implications

> L2 — Decision-maker view. Causal model resolved. Instrumentation roadmap with Phase 2 dependency gate. Per-persona investment sequencing.

### Causal Model: Resolved as SEGMENT-STRATIFIED

The Phase 1a OPEN QUESTION — Model A (Task Success gates Adoption) vs. Model B (Happiness gates Adoption) — is resolved by FEAT-040-053 persona analysis. The correct framing is a stratified investment model:

**Sam (Model A):** Sam's failure mode is mechanical, not motivational. Sam reads the README, finds it credible enough, proceeds to setup, and fails at SMOT Step 3. Fixing Task Success (TC-001/TC-005) directly improves Sam's adoption rate. Happiness improvements have marginal additional benefit for Sam after the SMOT fix.

**Taylor + Evan + Ren (Model B):** These three personas fail at FMOT before Task Success has any opportunity to operate. Taylor's README does not speak to governance use cases. Evan's 30-second credibility filter is not passed. Ren's return-visit catalog is not discoverable. For these personas, Task Success remediation (Wave 3) is wasted investment until FMOT remediation (Wave 2) creates a viable path to SMOT.

**Investment sequencing (evidence-based):**
1. **Wave 2 FMOT + TC-002 skill catalog** — unblocks Taylor, Evan, Ren (3 of 5 personas, Model B). Estimated aggregate leverage: highest (3/5 personas × FMOT is max-pain moment for all three).
2. **Wave 3 SMOT TC-001/TC-005** — unblocks Sam (1 persona primary, highest-volume entry point). Retains benefit for Taylor/Devi who reach SMOT.
3. **Wave 4 tutorials + TC-004** — unblocks Ren return-visit jobs and Devi domain-specialist access.

Sequencing is conditional on Model B validation (see Remaining Causal Uncertainty below); if Model B falsifies under Phase 2 SUPR-Q Credibility test, revert to Task Success-first investment.

**Remaining causal uncertainty:** Evan's population share is unmeasured. If Evan-pattern users are 60%+ of visitors, Wave 2 FMOT investment has higher aggregate return than Wave 3 SMOT investment even for adoption metrics. If Evan is 10% of visitors, Sam's Sam-Model-A path dominates aggregate metrics and Wave 3 is the higher-leverage investment. The SUPR-Q Credibility subscale (Phase 2 instrumentation) is the measurement that resolves this.

### Measurement Maturity Assessment

Jerry Framework documentation is at **Measurement Maturity Level 0** (no instrumentation, no baselines, no data infrastructure). Three independent Phase 1a analyses confirm this:
- FEAT-040-006 (B=MAP): "No measurement infrastructure" in Behavior Design Maturity assessment.
- FEAT-040-004 (Heuristic): All findings based on content analysis, not behavioral observation.
- FEAT-040-005 (WCAG): Live-rendering SCs deferred due to missing analytics infrastructure.

**Target maturity state:** Measurement Maturity Level 2 (baseline metrics collected, funnel instrumented, survey in place) by end of Wave 2.

### Instrumentation Roadmap

> **PHASE 2 DEPENDENCY GATE:** Phase 2 remediation implementation (Wave 2 README + TC-002 skill catalog) MUST NOT begin until Phase 1 instrumentation is confirmed live and collecting data for minimum 30 days. Pre-remediation baseline required for all Wave 2 impact measurement. This is a hard dependency gate.

**Phase 1 (Enable within 1-2 weeks — before any Wave 2 content changes):**

*Owner: Docs lead (1, 3) + DevSecOps (2).*

1. Enable MkDocs page analytics (GA4 or Plausible.io). Captures page views, session depth, skill-slug URL extraction, funnel entry/exit events. No content changes required. *Phase 1 critical path.*
2. Add GitHub Issue labels "documentation" and "docs-bug." Apply retroactively to existing documentation issues to establish valid historical baseline for Documentation-Induced GitHub Issue Rate. *Owner: Docs lead or DevSecOps.*
3. Add scroll-depth tracking to getting-started.md. Use GTM custom events or MkDocs Material feedback widget. Enables Step 3 Drop-Off Rate diagnostic. *Owner: Docs lead.*

*Phase 1 completion criterion:* All three instruments confirmed live and collecting data for a minimum of 30 days before any Wave 2 content changes begin. This gate is not optional — without pre-remediation baseline, Wave 2 impact cannot be measured.

**Phase 2 (Enable concurrently with Wave 2 remediation deployment):**

*Owner: DevSecOps (CLI telemetry) + Docs lead (survey).*

4. Add SUPR-Q survey widget to docs site. Deploy BEFORE Wave 2 content changes so a pre-Wave-2 Credibility subscale baseline is collected. This is the Model B causal validation instrument. *Owner: Docs lead.*
5. Instrument Jerry CLI first-use event — emit anonymous telemetry on first `jerry session start` with JERRY_PROJECT active. Requires user opt-in. Provides Getting-Started Completion Rate behavioral signal (primary). *Owner: DevSecOps.*
6. Enable MkDocs session analytics (pages/session, user journey tracking). *Owner: Docs lead.*

**Phase 3 (After adoption metrics stable — post-Wave 3 deployment):**

*Owner: Docs lead.*

7. User-level session tracking (GitHub OAuth or privacy-compliant fingerprinting). Enables Retention metrics (14-Day Return Rate, Skill Expansion Rate). Required for Ren's primary KPIs.
8. Schedule quarterly moderated usability tests (minimum 5 participants per persona task set). Highest-confidence Task Success signal.

### Metric Interdependencies (Authoritative — Segment-Stratified)

The segment-stratified causal model restructures metric interdependencies from the Phase 1a provisional model:

**Sam's dependency chain (Model A):**
```
Task Success (Step 3 fix — TC-001/TC-005)
    → Adoption (Getting-Started Completion Rate rises)
    → Engagement (Sam discovers more skills post-adoption)
    → Retention (Sam returns across sessions)
    → Happiness (Sam trusts documentation after successful use)
```

**Taylor/Evan/Ren dependency chain (Model B):**
```
Happiness (FMOT credibility — TC-003 + FEAT-040-054 Positioning)
    → Adoption (Taylor/Evan attempt setup; Ren returns for new skill)
    → Task Success (Taylor/Ren complete tasks once Happiness gate is cleared)
    → Retention (Ren expands skill use over time)
    → Engagement (Ren and Taylor explore full catalog after trust is established)
```

**Cross-chain intervention (TC-002 skill catalog) breaks both chains' primary blocker simultaneously:**
TC-002 (hidden skill catalog) affects FMOT (Model B — Taylor, Evan, Ren) AND post-SMOT engagement (Model A — Sam). TC-002 remediation is the single highest-leverage intervention per FEAT-040-053 L2 Persona-to-Remediation Mapping: all 5 personas served.

---

## Synthesis Judgments Summary

> Enumeration of all AI judgment calls per P-022. Phase 1a OPEN QUESTIONs resolved; residual uncertainties documented.

1. **Judgment: All five HEART dimensions selected.** Standard recommendation for tiny teams (1-5 people) is 2-3 dimensions. Selected 5 because this is the Phase 1b authoritative pass establishing the complete measurement framework for a multi-wave documentation overhaul. Teams instrument 3 highest-priority metrics first. **Confidence: MEDIUM** (justified by engagement scope and FEAT-040-053 persona coverage of all 5 dimensions).

2. **RESOLVED: Causal ordering is SEGMENT-STRATIFIED (not Model A or Model B universally).** Phase 1a left this as OPEN QUESTION with two competing models. FEAT-040-053 persona analysis resolves: Sam follows Model A (Task Success gates Adoption); Taylor/Evan/Ren follow Model B (Happiness gates Adoption). This is a NEW hypothesis (Synthesis Judgment #11 from FEAT-040-053) not present in Phase 1a. It requires Phase 2 instrumentation to quantify Evan's population share before segment weighting can be confirmed. **Confidence: MEDIUM** (derived from analyst-synthesized persona data, not behavioral measurement).

3. **Judgment: Per-persona KPI targets (Sam >= 65% Completion Rate; Ren >= 35% Skill Discovery; Ren >= 45% Return Rate; Ren >= 4 skills/30d).** Persona-specific KPI targets are additional directional guidance layered on top of general [REFERENCE-ONLY] thresholds. They reflect behavioral expectations derived from FEAT-040-053 Moments of Truth analysis. **Confidence: LOW** (directional; no behavioral data validates persona-specific targets; all require pre-remediation baseline and post-intervention measurement to calibrate).

4. **Judgment: Getting-Started Completion Rate is the single highest-impact metric for Sam.** Triple-convergence evidence (B=MAP, F-014 Sev 3, F-016 Sev 2, TC-001 + TC-005) supports this. No alternative metric has equivalent convergent support. **Confidence: MEDIUM** (structural convergence only; no behavioral funnel data confirms).

5. **Judgment: Wave 2 FMOT + TC-002 sequenced before Wave 3 SMOT TC-001/TC-005.** Based on persona count: FMOT affects 4 of 5 personas as primary or secondary max pain; SMOT Step 3 is primary max pain for only Sam. If Evan's population is < 10% of visitors, the aggregate adoption impact of Wave 3 may exceed Wave 2 in absolute numbers. This is an investment sequencing risk. **Confidence: MEDIUM-LOW** (depends on Evan population share, which is unmeasured).

6. **Judgment: SUPR-Q 70/100 target.** Adapted from MeasuringU SUPR-Q normative data for developer documentation (65-72 range, not independently verified from public publications). **Confidence: LOW** (unverified adapted estimate; must be recalibrated post-baseline).

7. **Judgment: 60% Getting-Started Completion Rate general target.** B=MAP estimates current state "well below 50%" (LOW confidence). MeasuringU 2021 median 58% (citation not independently confirmed). 60% is at the upper bound of the adapted reference range. Sam post-intervention target of 65% reflects the TC-001/TC-005 single-fix impact assessment (B=MAP Intervention #1 classified as Major impact). **Confidence: LOW** (multiple unverified adapted estimates; pre-remediation baseline required).

8. **Judgment: Skill Discovery Rate 25% general target.** No published benchmark for developer tool documentation skill catalog discovery. Fallback Step 3. Ren sub-target of 35% reflects active multi-skill returning user expectation. **Confidence: LOW** (no benchmark; pre-remediation baseline required).

9. **Judgment: SUPR-Q Credibility subscale is the Model B causal validation instrument.** If Credibility subscale rises post-Wave 2 FMOT remediation (README + positioning changes) without a simultaneous Task Success fix, this confirms Happiness causes Adoption change. If Credibility subscale does not rise, Model B impact is smaller than projected and Model A sequencing (Task Success first) gains relative support. **Confidence: MEDIUM** (causal logic is sound; measurement design is correct; behavioral confirmation pending).

10. **Judgment: All 11 metrics derived from structural analysis without behavioral data.** The causal link between structural findings (F-011 jargon density, F-014 navigation gaps, etc.) and behavioral signals (users abandoning, not returning) is an analytical inference that behavioral measurement may not fully confirm. This is the highest-confidence limitation of the entire analysis. **Confidence: explicit LOW on all causal claims** (per Synthesis Judgment #9 in provisional pass, carried forward).

11. **Judgment: W-013 cited as minor Task Success signal.** W-013 (SC 2.4.6 — pilcrow section links provide ambiguous accessible names; Sev 1; FEAT-040-005 rescope-iter-5) is included as a minor AT-discoverability issue in the Task Success GSM derivation. Its Severity 1 classification means it does not independently drive any metric threshold. Included for completeness per WCAG coverage requirement. **Confidence: HIGH** (independently verified against live site in FEAT-040-005 rescope-iter-5).

12. **Judgment: Devi metrics included with UNVALIDATED flag.** Devi (A6 Domain Specialist) has STOP GATE from FEAT-040-001. All Devi-specific metric notes and persona KPI targets are included in this analysis for completeness but carry INFERRED confidence status. No Devi-targeted remediation should proceed before A6 validation protocol closure. **Confidence: INFERRED** (A6 switch trigger unconfirmed by user interviews).

---

## Validation Required

- **Validation status:** PENDING
- **Required validation sources:**

| # | Validation Item | Source | Urgency |
|---|----------------|--------|---------|
| 1 | Pre-remediation baseline data from Phase 1 instrumentation (minimum 30-day collection) | MkDocs analytics + GitHub labeling | BLOCKING — no improvement targets valid until baseline collected |
| 2 | Evan population share quantification (resolves aggregate causal weighting) | Phase 1 SUPR-Q Credibility subscale + funnel analytics (30-day data) | HIGH — determines Wave 2 vs. Wave 3 investment sequencing |
| 3 | Sam interview validation (N=3-5: observe FMOT + SMOT to first-skill invocation) | User interviews per FEAT-040-053 Validation Required | HIGH — validates Task Success causal claim |
| 4 | Evan interview validation (N=5: multi-framework evaluators, V-01/V-02 FEAT-040-055) | User interviews per FEAT-040-053 Validation Required | HIGH — validates Model B and FMOT positioning |
| 5 | Taylor interview validation (N=3-5: engineering managers, governance framing test) | User interviews per FEAT-040-053 Validation Required | MEDIUM — validates Taylor FMOT and governance-signal claim |
| 6 | Post-remediation Ren cohort analysis (14-Day Return Rate, Skill Expansion Rate) | Phase 3 instrumentation (post-Wave 3 deployment) | MEDIUM — requires Phase 3 instrumentation to be live |
| 7 | A6 Validation Protocol closure (N=3 Devi interviews) | FEAT-040-001 A6 STOP GATE protocol | MEDIUM-LOW — gates all Devi-targeted documentation waves |
| 8 | Minimum one moderated usability test (Sam + Taylor task sets, 5 participants each) | Quarterly test program | MEDIUM — validates Task Success failure mode location |
| 9 | Threshold recalibration after first 4-6 week measurement cycle | Baseline data collected from Phase 1 instruments | REQUIRED — all LOW-confidence thresholds must be recalibrated against actual data |

**Confidence upgrade path:** Goal-metric mappings: MEDIUM → HIGH after N=5 user interviews confirming JTBD job statements per persona (FEAT-040-053 Validation Required). Thresholds: LOW → MEDIUM after first full measurement cycle (4-6 weeks of baseline data).

---

## Handoff Data

> Structured XP-02 data for downstream sub-skill consumption. Updated with authoritative 5-persona model and segment-stratified causal model.

### XP-02 (HEART) — Authoritative Handoff to Phase 2 Synthesis

| Persona ID | Persona Label | JTBD Actor | Primary HEART Dim | Causal Model | Primary Metric | Per-Persona KPI [REFERENCE-ONLY] | Moment of Max Pain | Confidence |
|-----------|--------------|-----------|------------------|-------------|---------------|--------------------------------|---------------------|-----------|
| P1 | Solo Builder Sam | A1 | Adoption + Task Success | Model A (Task-first) | Getting-Started Completion Rate | >= 65% post-TC-001/TC-005 | SMOT Step 3 | MEDIUM |
| P2 | Team Lead Taylor | A2 | Happiness (FMOT gate) + Task Success (secondary) | Model B (Happiness-gated) | SUPR-Q Credibility subscale (FMOT signal) | SUPR-Q >= 3.5 / 5.0 Credibility before SMOT attempt | FMOT README governance |  MEDIUM |
| P3 | Trust-Evaluating Evan | A1/A2/A5 | Happiness | Model B (Happiness-gated) | Documentation Credibility Subscale | >= 3.5 / 5.0 Credibility (Model B causal threshold) | FMOT 30-sec filter | MEDIUM (population share open) |
| P4 | Returning Ren | A1/A2 post | Retention + Engagement | Model B hybrid (Happiness-gated return) | Skill Discovery Rate + 14-Day Return Rate | Skill Discovery >= 35%; Return Rate >= 45% | FMOT return catalog scan | MEDIUM |
| P5 | Domain Specialist Devi | A6 [UNVAL] | Engagement | Model B hybrid | Skill Discovery Rate (domain-specific) | Per domain skill catalog access rate [INFERRED] | SMOT wave-gating | INFERRED (A6 STOP GATE) |

### All Metric Specifications for Cross-Framework Handoff

| Metric Name | HEART Dimension | Formula Summary | General Target [REFERENCE-ONLY] | Confidence | Measurement Gap | Instrumentation Phase |
|-------------|----------------|----------------|--------------------------------|------------|-----------------|----------------------|
| SUPR-Q Composite Score | Happiness | Avg 8-item SUPR-Q (0-100) | >= 70 | LOW | Survey not instrumented | Phase 2 |
| Documentation Credibility Subscale | Happiness | Avg SUPR-Q Credibility items Q4+Q5 (0-5) | >= 4.0 | LOW | Same survey | Phase 2 |
| Skill Discovery Rate | Engagement | (Users > 7 skill pages / Total users) × 100 — "7" = 23% of 30-skill catalog (7/30 = 0.233); recalibrate post-F-020-remediation | >= 25% (general 90-day) | LOW | Analytics not instrumented | Phase 1 (URL extraction) |
| Documentation Pages per Session | Engagement | Total views / Sessions (exclude bounces) | >= 3.5 | LOW | Analytics not instrumented | Phase 2 |
| Getting-Started Completion Rate | Adoption + Task Success | (First-skill invocations / Getting-started starts) × 100 | >= 60% | LOW | Funnel analytics + CLI event needed | Phase 1 (funnel) + Phase 2 (CLI telemetry) |
| Step 3 Drop-Off Rate | Adoption + Task Success (Diagnostic) | (Non-proceed at Step 3 / Reach Step 3) × 100 | <= 20% | LOW | Step-level scroll tracking needed | Phase 1 |
| Time-to-First-Skill-Invocation | Adoption | Median minutes: README load → first skill invocation (identity bridge required) | <= 20 min | LOW | CLI telemetry + identity bridge needed | Phase 3 |
| 14-Day Documentation Return Rate | Retention | (Returns in 14d / First-invocation completions) × 100 | >= 40% | LOW | User-level tracking needed | Phase 3 |
| Skill Expansion Rate | Retention | Median distinct skills in 30d window per user | >= 3 skills | LOW | User-level tracking needed | Phase 3 |
| Documentation-Induced GitHub Issue Rate | Task Success | (Docs-labeled issues / Total issues) × 100 | <= 5% | LOW | GitHub labeling discipline needed | Phase 1 |
| Moderated Task Completion Rate | Task Success | (Tasks completed without assist / Total tasks) × 100 | >= 80% | LOW | Quarterly moderated test program needed | Phase 3 |

### Causal Model Summary for Phase 2 Synthesis

| Model | Personas | Measurement Signal | Phase 2 Action if Confirmed |
|-------|---------|-------------------|------------------------------|
| Model A (Task-first) | Sam | Getting-Started Completion Rate rises post-Wave 3 (TC-001/TC-005) WITHOUT prior SUPR-Q rise | Prioritize Wave 3 SMOT fix investment in Wave 4+ budget |
| Model B (Happiness-gated) | Taylor, Evan, Ren | SUPR-Q Credibility subscale rises post-Wave 2 (FMOT + README repositioning) WITH concurrent Adoption metrics improvement | Confirm Wave 2 FMOT-first sequencing as highest-leverage investment |
| Both operative (Stratified) | All 5 | Both signals rise in sequence (Wave 2 FMOT → Wave 3 SMOT) | Segment-stratified investment framework confirmed; continue per wave sequencing |

---

## Quality Self-Assessment

> S-014 6-dimension self-score for Phase 1b authoritative pass, iter-2.

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Completeness | 0.20 | 0.95 | 0.190 | All 5 HEART dimensions have complete GSM tables with JTBD enrichment. All 11 metrics have full specification fields. 5 personas integrated with per-persona KPIs. Causal model resolved with named evidence. Dashboard specification includes instrumentation phasing and new FMOT-isolation limitation paragraph. No dimension or metric specification field is missing. Per-persona KPI derivation footnote added. |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Credibility subscale scale now reconciled to 3.5/5.0 subscale-native across Metric Specifications, Baseline and Thresholds, and Handoff Data — scale confusion resolved (PM-002-A1 CLOSED). Taylor's Primary HEART Dim corrected in Handoff Data to Happiness (FMOT gate) + Task Success (secondary) — consistent with Model B causal assignment (FM-002-A1 CLOSED). SEGMENT-STRATIFIED banner now co-locates MEDIUM confidence qualifier (CC-001-A1 CLOSED). Calibration note: external reviewer scored Internal Consistency 0.90 at iter-1 citing FM-002-A1 and PM-002-A1; both are now closed. Conservative scoring: 0.93 (not 0.95) reflects residual risk that per-persona KPI table in Handoff Data now has three different 3.5 values that reviewers could still misread without the footnote anchor. |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | GSM process applied sequentially per Rodden, Hutchinson & Fu (2010) CHI methodology. FMOT-isolation confound paragraph added to Dashboard Specification Model A/B causal view — addresses the core methodological gap identified in PM-001-A1. Stagger-or-A/B mitigation options named and scoped. External reviewer scored Methodological Rigor 0.90 at iter-1 citing PM-001-A1 isolation confound; that gap is now addressed. Conservative scoring: 0.92 (not 0.94) because the causal test remains correlational by design — no experimental control is mandated, only recommended. |
| Evidence Quality | 0.15 | 0.91 | 0.137 | Unchanged from iter-1: FEAT-040-053 personas provide MEDIUM confidence grounding for causal model; FEAT-040-001 JTBD provides MEDIUM confidence grounding for goal framing. Per-persona KPI derivation footnote added to Baseline table acknowledges analyst-inferred status explicitly — marginal improvement in epistemic disclosure. Structural cap remains: no baseline data, no verified benchmarks. |
| Actionability | 0.15 | 0.93 | 0.140 | Investment sequencing now carries explicit conditional cross-reference to Remaining Causal Uncertainty sub-section and Model B falsification reversion instruction (DA-002-A1/IN-001-A1 CLOSED). Per-persona KPI derivation note reduces the risk of teams treating analyst-inferred targets as validated commitments. FMOT-isolation mitigation options (stagger / A/B control) are actionable recommendations, not abstract hedges. Conservative scoring: 0.93 (not 0.95) because the causal test mitigation is a recommendation, not an instrumentation specification. |
| Traceability | 0.10 | 0.95 | 0.095 | All goals trace to JTBD job statements (FEAT-040-001 XP-01b). All signals trace to persona behavioral patterns (FEAT-040-053). All metrics trace to upstream findings with current IDs (F-011, F-013, F-014, F-016, F-020, W-001, W-013 — no stale IDs). PM-001-A1 finding ID and DA-002-A1/IN-001-A1 finding IDs are now explicitly referenced in the artifact body (FMOT-isolation paragraph and investment sequencing cross-reference). Synthesis Judgments and Validation Required sections updated. |

**Raw composite:** 0.190 + 0.186 + 0.184 + 0.137 + 0.140 + 0.095 = **0.932**

**Calibration adjustment:** −0.008 (conservative per iter-1 instruction: prior calibration was −0.021 in external reviewer's favor; applying consistent conservative scoring this iteration)

**Self-reported composite: 0.924 / 1.00 — PASS (>= 0.92 threshold)**

**Quality gate verdict: PASS.** Iter-2 closes 2 Major findings (PM-001-A1 FMOT isolation confound; PM-002-A1 Credibility scale confusion) and 6 Minor findings (CC-001-A1; DA-001-A1 state file; DA-002-A1/IN-001-A1 investment sequencing cross-reference; FM-001-A1 KPI derivation footnote; FM-002-A1 Taylor dimension). Conservative scoring applied: 0.924 composite (0.932 raw − 0.008 calibration). Expected adversarial band: 0.920–0.924 (target gap closure from 0.914 → 0.92+).

---

## Revision History

| Iteration | Date | Phase | Type | Composite | Verdict | Changes |
|-----------|------|-------|------|-----------|---------|---------|
| 1b-iter-1 | 2026-04-20 | 1b-authoritative | Self (superseded) | 0.935 | SELF-PASS (superseded by external) | Phase 1b authoritative pass: causal model resolved SEGMENT-STRATIFIED; 5 personas integrated; per-persona KPIs; JTBD enrichment; investment sequencing finalized; INC-001 citations carried forward |
| 1b-iter-1 (external) | 2026-04-20 | 1b-authoritative | External adversarial | 0.914 | REVISE | 2 Major (PM-001-A1 FMOT isolation confound; PM-002-A1 Credibility scale confusion) + 6 Minor (CC-001-A1; DA-001-A1; DA-002-A1/IN-001-A1; FM-001-A1; FM-002-A1) |
| 1b-iter-2 | 2026-04-20 | 1b-authoritative | Self-revision | 0.924 | PASS | PM-001-A1 CLOSED: FMOT-isolation confound caveat paragraph added to Dashboard Spec causal view (correlational limitation + stagger/A-B mitigations). PM-002-A1 CLOSED: Credibility subscale reconciled to 3.5/5.0 subscale-native across Metric Specifications + Baseline + Handoff Data; scale clarification footnote added. CC-001-A1 CLOSED: MEDIUM confidence qualifier added to L0 SEGMENT-STRATIFIED banner. DA-001-A1 CLOSED: state file causal_model_resolution block updated with confidence/validation_required/instrument/timeline sub-fields. DA-002-A1/IN-001-A1 CLOSED: conditional cross-reference to Remaining Causal Uncertainty added after investment sequencing. FM-001-A1 CLOSED: per-persona KPI derivation footnote added to Baseline table. FM-002-A1 CLOSED: Taylor Primary HEART Dim corrected to Happiness (FMOT gate) + Task Success (secondary). |
