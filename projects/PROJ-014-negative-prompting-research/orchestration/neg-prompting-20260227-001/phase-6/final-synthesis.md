# PROJ-014 Negative Prompting Research: Final Synthesis and Implementation Roadmap

> **Agent:** ps-synthesizer | **Task:** TASK-018 | **Phase:** 6 | **Date:** 2026-02-28
> **Version:** 1.1.0 (I2 revision — 2026-02-28)
> **Criticality:** C4 (architecture/governance impact, multi-phase research culmination)
> **Quality Threshold:** >= 0.95
> **Self-review:** H-15 applied per constitutional compliance
> **Input artifacts synthesized:** 12 primary artifacts across 6 phases + 5 barrier syntheses
> **Constitutional compliance:** P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings and verdict in plain language |
| [L1: Technical Synthesis](#l1-technical-synthesis) | Evidence landscape, findings, and NPT taxonomy summary |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Jerry Framework impact, implementation roadmap, risk register, and recommendations |
| [1. Hypothesis Verdict](#1-hypothesis-verdict) | Decomposed verdict on both research claims |
| [2. Evidence Landscape Summary](#2-evidence-landscape-summary) | Evidence by tier with citation discipline |
| [3. Key Findings](#3-key-findings) | 14 numbered findings from the full research pipeline |
| [4. NPT Taxonomy Summary](#4-npt-taxonomy-summary) | 14-pattern negative prompting taxonomy |
| [5. Jerry Framework Impact Assessment](#5-jerry-framework-impact-assessment) | Four ADRs, their implementation status, and ADR approval process |
| [6. Implementation Roadmap](#6-implementation-roadmap) | 6-stage ordering with dependencies |
| [7. Phase 2 Experimental Design](#7-phase-2-experimental-design) | McNemar design with conditions C1-C7 |
| [8. PG-003 Contingency Plan](#8-pg-003-contingency-plan) | Null-finding scenario and reversibility |
| [9. Risk Register](#9-risk-register) | 7 risks with mitigation posture |
| [10. Recommendations](#10-recommendations) | R-001 through R-012 prioritized |
| [Source Summary](#source-summary) | All input artifacts with contribution summary |
| [Constitutional Compliance Checklist](#constitutional-compliance-checklist) | Evidence citation discipline verification |

---

## L0: Executive Summary

### What This Research Found

PROJ-014 conducted a six-phase investigation into a two-part hypothesis about negative prompting — the practice of using NEVER, MUST NOT, and FORBIDDEN vocabulary in LLM behavioral enforcement:

**Claim 1:** Negative unambiguous prompting reduces hallucination by 60%.
**Verdict: UNTESTED.** No published evidence substantiates a 60% reduction. The number is not disproven, but it is also not evidenced. The hypothesis requires experimental testing to resolve.

**Claim 2:** Negative prompting achieves better results than explicit positive prompting.
**Verdict: PARTIALLY SUPPORTED with significant qualification.** One claim component is supported by T1 evidence: *blunt* negative prompting (a standalone NEVER statement without consequence or scope) demonstrably *underperforms* structured alternatives. For *structured* negative prompting (NEVER + consequence + scope), the comparison against structurally equivalent positive instructions remains untested.

### What the Research Did Establish

Three findings are high-confidence and actionable now, independent of further experiments:

1. **Blunt prohibition is the worst form of negative constraint.** Peer-reviewed evidence (AAAI 2026, EMNLP 2024, arXiv T3) establishes that standalone NEVER/MUST NOT statements without consequence documentation produce inferior behavioral outcomes versus structured alternatives. Jerry Framework currently has 22 instances of this pattern (61% of all negative constraints). Eliminating these is unconditionally warranted.

2. **Anthropic uses structured negative prompting in its own tools.** The Claude Code rule files contain 33 NEVER/MUST NOT/DO NOT instances across 10 files, all in the HARD enforcement tier and all using structured format with consequence or scope. This is working-practice evidence that the framework's own authors consider structured negative prompting the appropriate tool for HARD-tier behavioral constraints.

3. **Context compaction is a real constraint resilience risk.** L1-loaded rules (session-start only) are silently dropped on context compaction. L2-re-injected rules (per-prompt) survive compaction. Five HARD rules currently have no L2 protection. This is a structural resilience gap that does not depend on Phase 2 experimental outcomes to address.

### What Comes Next

A controlled experiment (270 matched prompt pairs, McNemar's test, 7 conditions C1-C7) is the linchpin of resolving the remaining untested claims. Before that experiment begins, the current Jerry Framework state must be preserved as a baseline — no production constraint modifications until the baseline snapshot is captured.

The 6-stage implementation roadmap (9-20 weeks depending on Phase 2 timeline) sequences what can be done before Phase 2, what must wait for Phase 2 results, and what is unconditionally actionable.

---

## L1: Technical Synthesis

### Research Pipeline Overview

| Phase | Task(s) | Output | Quality Score |
|-------|---------|--------|---------------|
| Phase 1 — Literature Survey | TASK-001 through TASK-004 | 75 unique sources across academic, industry, context7 surveys | 0.953 PASS (R4) |
| Phase 1 — Supplemental Vendor Evidence | TASK-004 (supplement) | VS-001–VS-004, 33-instance catalog; A/B design; EO-001–EO-003 | 0.951 PASS (R4) |
| Phase 2 — Claim Validation | TASK-005 | Research question bifurcation; null finding on 60% claim | 0.959 PASS (R4) |
| Phase 2 — Comparative Effectiveness | TASK-006 | 5-dimension effectiveness analysis; A-23 T1 confirmation | 0.933 (R5, max-iter) |
| Barrier 2 — Synthesis | TASK-007 | PG-001–PG-005, AGREE-5 hierarchy, confidence tiers | 0.953 PASS (v3.0.0) |
| Phase 3 — Taxonomy | TASK-008 | NPT-001 through NPT-014 (13 distinct patterns) | 0.957 PASS (v3.0.0) |
| Phase 4 — Skills Analysis | TASK-010 | 37 recommendations across 13 skills | 0.951 PASS (v2.0.0) |
| Phase 4 — Agents Analysis | TASK-011 | 32 recommendations across 9 families | 0.951 PASS (v3.0.0) |
| Phase 4 — Rules Analysis | TASK-012 | 36 instances cataloged; 14 recommendations across 17 files | 0.953 PASS |
| Phase 4 — Patterns Analysis | TASK-013 | 34 recommendations across 12 categories | 0.950 PASS (v5.0.0) |
| Phase 4 — Templates Analysis | TASK-014 | 13 named recommendations across 4 families | 0.955 PASS (v3.0.0) |
| Barrier 4 — Synthesis | TASK-015 | 130 total recommendations; 6 cross-cutting themes | 0.950 PASS (v4.0.0) |
| Phase 5 — ADR-001 | TASK-016 | NPT-014 elimination policy (PROPOSED) | 0.952 PASS |
| Phase 5 — ADR-002 | TASK-016 | Constitutional upgrade policy (PROPOSED) | 0.951 PASS |
| Phase 5 — ADR-003 | TASK-016 | Routing disambiguation standard (PROPOSED) | 0.957 PASS |
| Phase 5 — ADR-004 | TASK-016 | Compaction resilience policy (PROPOSED) | 0.955 PASS |
| Barrier 5 — ADR Synthesis | TASK-016 | 6-stage implementation ordering, 13 cross-ADR actions, 8 risks | 0.956 PASS (v1.1.0) |

All adversary-gate scores are >= 0.950 except TASK-006 (0.933, reached at max-iter=5, directional findings accepted).

---

## 1. Hypothesis Verdict

### Primary Hypothesis

> "Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting."

This hypothesis decomposes into two independently assessable claims.

---

### Claim A: 60% Hallucination Reduction

**Verdict: NULL FINDING — UNTESTED, NOT DISPROVEN**

**Status:** The 60% figure has no primary source in any reviewed publication. Research conducted across 75 unique sources (academic T1/T2/T3, industry practitioner, vendor documentation) found zero controlled evidence for a 60% hallucination reduction attributable to negative prompting. The absence of evidence is not evidence of absence (SE-1, barrier-2/synthesis.md). The claim was not produced by experimentation; it entered research as a hypothesis requiring validation.

**Evidence FOR Claim A:**
- E-FOR-A-001: ABSENT — no study reporting this specific effect size was found
- E-FOR-A-002: ABSENT — no primary source for the "60%" figure was identified

**Evidence AGAINST Claim A (partial):**
- Varshney et al. (T3, arXiv): Negation vocabulary can *increase* hallucination in multiple-choice QA contexts
- Gandhi et al. (T3, arXiv): Negative sentiment framing reduces accuracy by 8.4% in some tasks
- McKenzie et al. (T2): Inverse scaling — negation-containing instructions show worse performance at scale for some task types

**Warning (preserved from claim-validation.md):** NEVER cite this research as evidence that negative prompting does not reduce hallucinations. The evidence is against the specific 60% claim, not against all forms of negative prompting.

**Resolution path:** Phase 2 experimental pilot (TASK-019, n=270 matched pairs, McNemar's test) directly tests this claim. See Section 7.

---

### Claim B: Negative > Positive Prompting

**Verdict: PARTIALLY SUPPORTED — COMPONENT-SPECIFIC**

**Component B-1: Blunt negative prompting > positive prompting**
**Verdict: REFUTED.** T1 evidence establishes that standalone blunt prohibition (NEVER X, without consequence, scope, or alternative) produces *worse* behavioral compliance than structured alternatives. This is PG-001 (HIGH, unconditional, T1+T3). Sources:
- A-20: Liu et al., AAAI 2026 — instruction hierarchy failure under blunt constraint
- A-15: Wen et al., EMNLP 2024 — +7.3-8% compliance with structured vs. blunt negative framing
- A-31: arXiv, T3 — 55% improvement for affirmative directive pairing vs. standalone negation

**Component B-2: Structured negative prompting > positive prompting**
**Verdict: UNTESTED.** A-23 (Barreto & Jana, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761) confirmed +25.14% negation reasoning accuracy for structured negation conditions — but this measures negation *comprehension accuracy*, not behavioral compliance rate vs. positive instruction equivalents. No controlled A/B comparison of NPT-009/NPT-010/NPT-011 (structured negative) versus structurally equivalent positive instructions has been published. This is the Phase 2 research target.

**Component B-3: Vendor self-practice alignment**
**Verdict: HIGH CONFIDENCE OBSERVATIONAL.** Anthropic uses structured prohibitive vocabulary (NEVER/MUST NOT) in 33 instances across 10 Claude Code rule files (VS-001). All 33 instances are in the HARD enforcement tier (VS-003). Three competing explanations exist for why (VS-002): (1) audience specificity — Anthropic's rule files target LLM agents under L2 re-injection, not human readers; (2) genre convention — prohibitions are idiomatic in behavioral rule documents; (3) engineering discovery — practice evolved from experience. NEVER assert explanation (3) as established.

**Summary Table:**

| Component | Verdict | Evidence Tier | Resolution |
|-----------|---------|---------------|-----------|
| 60% hallucination reduction | UNTESTED | Absent (null finding) | Phase 2 experiment |
| Blunt negative > positive | REFUTED | T1+T3, HIGH | Unconditional: upgrade all NPT-014 instances |
| Structured negative > positive | UNTESTED | T4 observational only | Phase 2 experiment |
| Vendor alignment with structured negative | SUPPORTED | T4 observational | Working practice; causal mechanism contested |

---

## 2. Evidence Landscape Summary

### Evidence Tiers Defined

| Tier | Label | Source Type | Epistemological Status |
|------|-------|-------------|----------------------|
| T1 | Established | Peer-reviewed (NeurIPS, AAAI, ACL, EMNLP) | Causal claims admissible |
| T2 | Established venue | Established conferences, workshops | High credibility, not always causal |
| T3 | Provisional | arXiv preprints, unreviewed | Directional; requires T1 replication |
| T4 | Working practice | Vendor docs, practitioner surveys, session observations | Valid observational evidence; causation not established |
| T5 | Single session | Isolated session-level observation | Corroborating only; NEVER treat as generalizable |

### Evidence Tier Distribution (75 Unique Sources)

Source counts from barrier-1/synthesis.md (R4, 0.953 PASS) — L1: Evidence Tier Analysis section, line-level arithmetic verification completed in R4 self-review.

| Tier | Count | % of Total | Representative Examples |
|------|-------|-----------|------------------------|
| T1 — Peer-reviewed (top venues) | 13 | 17.3% | A-1 (IJCAI), A-3 (EMNLP), A-7 (NeurIPS), A-8 (CVPR), A-13 (ICLR), A-15 (EMNLP), A-20 (AAAI), A-22 (ACL), A-23 (EMNLP), A-24 (ICLR), A-25 (Nature), A-27 (ACL), A-28 (ICLR) |
| T2 — Established venues / workshops | 5 | 6.7% | A-4 (*SEM), A-9 (TMLR), A-12 (IJCAI symposium), A-26 (EACL), A-30 (MIT Press CL) |
| T3 — arXiv preprints / unreviewed | 15 | 20.0% | A-2, A-5, A-6, A-10, A-11 (hallucinated — NEVER CITE), A-14, A-16 (rejected ICLR), A-17, A-18, A-19, A-21, A-29, A-31, C-13, C-19 |
| T4 — Vendor docs, practitioner, framework | 42 | 56.0% | All I-series (I-1 through I-32, minus A/C overlaps) + all C-series (C-2, C-3, C-6 through C-12, C-14, C-20) |
| **Total** | **75** | **100%** | 31 academic (incl. A-31 added R2) + 31 industry-unique + 13 context7-unique |

> **Note:** A-11 is included in the T3 count for arithmetic completeness (75 total) but is a confirmed hallucinated citation. NEVER cite A-11 in any downstream document. T4 dominance (56%) reflects the structural reality that controlled academic evidence on negative prompting is sparse; the practitioner evidence base is substantially larger than the peer-reviewed base.

### T1 Evidence (Peer-Reviewed, Causal)

| Citation ID | Source | Key Finding | PROJ-014 Application |
|-------------|--------|-------------|---------------------|
| A-20 | Liu et al., AAAI 2026 | Instruction hierarchy failure under standalone negative constraint | Establishes NPT-014 underperformance; supports PG-001 unconditionally |
| A-15 | Wen et al., EMNLP 2024 | +7.3–8% compliance with structured framing vs. blunt negation | Establishes NPT-014 < NPT-009 for compliance dimension |
| A-23 | Barreto & Jana, EMNLP 2025 Findings | +25.14% negation reasoning accuracy | Supports negation accuracy improvement; NOT behavioral compliance vs. positive equivalents |

**NEVER cite A-11** — confirmed hallucinated citation (arXiv ID not independently retrievable; TASK-013 I5 removed it; no matching paper exists). NEVER use it in any downstream document.

### T3 Evidence (Provisional, Directional)

| Citation ID | Source | Key Finding | Confidence |
|-------------|--------|-------------|-----------|
| A-31 | arXiv (T3) | 55% improvement for affirmative directive pairing vs. standalone negation | Directional; requires T1 replication |
| Varshney et al. | arXiv (T3) | Negation vocabulary can increase hallucination in MCQA contexts | Counter-evidence to naive negative prompting; MCQA-specific |
| Gandhi et al. | arXiv (T3) | Negative sentiment reduces accuracy 8.4% | Counter-evidence; sentiment ≠ behavioral constraint framing |

### T4 Evidence (Working Practice, Observational)

| Evidence ID | Source | Finding | Confidence |
|-------------|--------|---------|-----------|
| VS-001 | Anthropic Claude Code rule files | 33 NEVER/MUST NOT/DO NOT instances across 10 files | HIGH observational (directly verified) |
| VS-002 | Anthropic published guidance vs. self-practice | Engineering practice diverges from published guidance — 3 competing explanations | LOW causal (ambiguous) |
| VS-003 | Anthropic HARD/MEDIUM/SOFT tier vocabulary | HARD tier vocabulary is definitionally prohibitive | HIGH observational |
| VS-004 | Anthropic constitutional constraints in rule files | P-003/P-020/P-022 expressed as prohibitions in production rule files | HIGH observational |
| EO-001 | PROJ-014 session observations | Preliminary directional signal on structured vs. blunt constraints | T5 corroborating; NOT T4 generalized |

### AGREE-5 Hierarchy (Internally Generated — NOT Externally Validated)

The AGREE-5 12-level effectiveness hierarchy was produced as an internally generated synthesis narrative (adversary gate 0.953). It summarizes cross-survey practitioner consensus. **NEVER cite AGREE-5 rank ordering as T1 or T3 evidence.** It is a working-practice synthesis, not an experimental result.

| AGREE-5 Rank | Pattern | Evidence Support |
|-------------|---------|-----------------|
| 1–4 | Model-internal interventions (RLHF, fine-tuning, constitutional AI training) | T1 — established as most effective |
| 5–6 | L2 re-injected constraints (NPT-012); structured enforcement tiers (NPT-013) | T4 — vendor self-practice, mechanism verified |
| 7 | Unoccupied (no technique warrants this position) | — |
| 8–9 | Declarative behavioral negation with consequence (NPT-009); paired prohibition with positive alternative (NPT-010); justified prohibition (NPT-011) | T3/T4 — practitioners recommend; causal comparison untested |
| 10–11 | Contrastive illustration with positive redirect (NPT-008) | T3 — moderate cross-survey agreement (E-007, AGREE-9) |
| 12 | Positive framing only (NPT-007) | Untested as baseline |
| Avoid | Standalone blunt prohibition (NPT-014) | T1+T3 unconditional: underperforms all structured alternatives |

### Key Epistemological Constraints

**NEVER violate these constraints in any downstream document:**

1. NEVER claim the 60% hallucination reduction is validated or even directionally supported by current evidence
2. NEVER cite A-11 — confirmed hallucinated citation
3. NEVER cite AGREE-5 rank ordering as T1 or T3 evidence — it is internally generated synthesis
4. NEVER conflate VS-001 vendor self-practice with controlled experimental evidence
5. NEVER treat absence of evidence for a positive effect as evidence of a negative effect (SE-1)
6. NEVER present NPT-009/NPT-010/NPT-011 effectiveness as experimentally established — causal comparison against positive equivalents is UNTESTED

---

## 3. Key Findings

### KF-001: The 60% Hallucination Reduction Claim Has No Evidential Basis

The primary research claim entered the project without a primary source. A systematic search across 75 unique sources found zero controlled evidence for this specific effect size. The claim is unverifiable from existing literature. It is not disproven — it is simply unestablished. All downstream decision-making must treat this claim as a testable hypothesis, not a known finding.

**Source:** phase-2/claim-validation.md (TASK-005, R4, 0.959 PASS); barrier-1/synthesis.md (R4, 0.953 PASS)

### KF-002: Blunt Prohibition Is Unconditionally the Worst Constraint Formulation

Standalone NEVER/MUST NOT statements without consequence documentation, scope specification, or positive behavioral alternative are designated NPT-014 (standalone blunt prohibition) in the Phase 3 taxonomy. T1+T3 evidence establishes these underperform structured alternatives. This finding is unconditional — it does not depend on Phase 2 experimental results. It applies regardless of whether structured negative or structured positive framing is ultimately superior.

**Source:** A-20 (AAAI 2026), A-15 (EMNLP 2024), A-31 (arXiv T3); PG-001 (barrier-2/synthesis.md); phase-3/taxonomy-pattern-catalog.md

### KF-003: Jerry Framework Has 22 NPT-014 Instances (61% of All Negative Constraints)

A detailed audit of 17 rule files found 36 negative constraint instances. Of these, 22 (61%) are NPT-014 format — standalone NEVER/MUST NOT without consequence documentation. An additional 8 instances (22%) are NPT-009 quality (consequence present). Zero instances match NPT-010 (paired prohibition with positive alternative) or NPT-011 (justified prohibition with contextual reason).

**Source:** phase-4/rules-update-analysis.md (TASK-012, 0.953 PASS); barrier-1/supplemental-vendor-evidence.md VS-001 baseline

### KF-004: Anthropic Uses Structured Prohibitive Vocabulary in Its Own Production Tools

The Claude Code rule files contain 33 instances of NEVER/MUST NOT/DO NOT across 10 files (VS-001). All are in the HARD enforcement tier (VS-003). The constitutional constraints P-003, P-020, P-022 are expressed as prohibitive statements in Anthropic's production rule files (VS-004). Anthropic's published guidance to LLM users differs from its own engineering practice — three competing explanations exist but none is established as causal.

**Source:** barrier-1/supplemental-vendor-evidence.md (R4, 0.951 PASS); VS-001 through VS-004

### KF-005: Context Compaction Silently Eliminates L1-Only Constraints

L1-loaded rules (session-start via `.claude/rules/`) are vulnerable to context compaction (T-004 failure mode). When compaction occurs, L1 content is compressed and constraints expressed only at session-start may be silently dropped. L2 re-injection (per-prompt HTML comment re-injection) survives compaction. Five HARD rules currently have no L2 protection: H-04, H-16, H-17, H-18, H-32 (Tier B HARD rules). This is a structural resilience gap.

**Source:** phase-4/rules-update-analysis.md; phase-5/ADR-004-compaction-resilience.md; barrier-5/synthesis.md; supplemental-vendor-evidence.md (T-004 failure mode documentation)

### KF-006: The Research Question Was Bifurcated Into Two Independent Sub-Questions

Phase 2 analysis produced a formal research question bifurcation:
- **Primary RQ:** Does structured negative prompting reduce LLM hallucination rate compared to structurally equivalent positive instructions?
- **Secondary RQ:** Does structured negative prompting improve behavioral constraint adherence rate compared to structurally equivalent positive instructions?

These are independently testable and may have different answers. The Phase 2 experimental design (Section 7) tests both.

**Source:** phase-2/claim-validation.md (TASK-005, R4, 0.959 PASS)

### KF-007: A-23 Supports Negation Comprehension Accuracy, Not Behavioral Compliance

The highest-quality positive evidence for negative prompting found in this research is A-23 (Barreto & Jana, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761): +25.14% negation reasoning accuracy improvement for structured negation conditions. This is a T1 finding — but it measures how accurately an LLM *understands* negation, not how well it *complies with* behavioral constraints expressed negatively. The distinction is critical: negation comprehension accuracy and behavioral compliance rate are different outcome variables.

**Source:** phase-2/comparative-effectiveness.md (TASK-006, R5, D2 analysis)

### KF-008: The NPT Taxonomy Identifies 13 Distinct Techniques in 14 Named Patterns

Phase 3 produced a 14-pattern taxonomy (NPT-001 through NPT-014) representing 13 distinct techniques. NPT-007 (positive-framing baseline) and NPT-014 (standalone blunt prohibition) are dual entries for conceptually related but structurally distinct positions in the AGREE-5 hierarchy. NPT-007 is the positive-only baseline; NPT-014 is the negative-only baseline — both are "untreated control" positions relative to structured approaches. Rank 7 in the AGREE-5 hierarchy is unoccupied — no technique warrants placement between NPT-013 and NPT-009 without additional evidence.

**Source:** phase-3/taxonomy-pattern-catalog.md (TASK-008, v3.0.0, 0.957 PASS)

### KF-009: The IG-002 Taxonomy Classifies Four Types of Negative Prompting

The supplemental vendor evidence produced IG-002: a four-type classification of negative prompting implementations, distinct from the NPT technique taxonomy:
- **Type 1:** Naive blunt prohibition (NEVER X — no structure)
- **Type 2:** Structured prohibition (NEVER X + consequence + scope)
- **Type 3:** L2 re-injected prohibition (surviving context compaction)
- **Type 4:** Constitutional triplet (P-003/P-020/P-022 expressed as prohibition cluster)

This classification cross-cuts the NPT taxonomy: NPT-014 is exclusively Type 1; NPT-009/NPT-010/NPT-011 are Type 2; NPT-012 is Type 3; NPT-013 is Type 4.

**Source:** barrier-1/supplemental-vendor-evidence.md (IG-002 definition)

### KF-010: Phase 4 Produced 130 Recommendations Across Five Jerry Framework Domains

The Phase 4 application analyses identified 130 specific upgrade recommendations distributed across: Skills (37 across 13 skills), Agents (32 across 9 families), Rules (14 across 17 rule files), Patterns (34 across 12 categories), and Templates (13 across 4 families). All carry T4 observational evidence with UNTESTED causal label against positive-framing equivalents. No recommendation is experimentally validated. All are reversible under PG-003 null Phase 2 outcome.

**Source:** barrier-4/synthesis.md (TASK-015, v4.0.0, 0.950 PASS); TASK-010 through TASK-014

### KF-011: Six Cross-Cutting Themes Appear in 3+ of 5 Phase 4 Analyses

Barrier 4 synthesis identified 6 universal cross-cutting themes: (1) NPT-009 as universal upgrade target; (2) NPT-014 as universal diagnostic baseline; (3) NPT-013 constitutional triplet as governance enforcement pattern; (4) VS-003 enforcement tier vocabulary as working-practice standard; (5) PG-003 reversibility as universal constraint; (6) Evidence tier discipline (T4 observational, UNTESTED causal) as binding meta-constraint. Themes 5 and 6 are research design constraints, not evidence-graded findings.

**Source:** barrier-4/synthesis.md (Section 2: Cross-Cutting Theme Analysis)

### KF-012: The A-11 Citation Was Confirmed as Hallucinated

An arXiv citation (A-11, "Contrastive Prompting Improves Code Generation Quality") used in Phase 1 literature survey and initially propagated to TASK-013 (patterns analysis) was confirmed as a hallucinated citation in TASK-013 I5. Web search found no matching paper. The citation was removed entirely. NPT-008 evidence now rests exclusively on E-007 (AGREE-9, 2-of-3 cross-survey agreement). All downstream documents must cite E-007 for NPT-008 support; NEVER cite A-11.

**Source:** patterns-update-analysis.md (TASK-013, v5.0.0 I5 revision); barrier-4/synthesis.md (Section 6: A-11 Resolution)

### KF-013: The Three-Tier Maturity Pattern Appears Across All Five Artifact Domains

Every Phase 4 analysis independently identifies a high/mid/low constraint maturity distribution within its domain. High-maturity artifacts govern high-consequence operations. Mid-maturity artifacts have the constitutional triplet plus partial NPT-009. Low-maturity artifacts use flat NPT-014 or have no negative constraints. The maturity distribution correlates with operational risk level (T4 observational). NEVER treat this as causal.

**Source:** barrier-4/synthesis.md (L2 Strategic Synthesis: The Maturity Stack)

### KF-014: Two Implementation Coverage Gaps Exist in the ADR Portfolio

The four Phase 5 ADRs leave two recommendation groups without dedicated ADR coverage:
- **GAP 1:** 28 SHOULD/MAY recommendations from TASK-013 (patterns analysis) address pattern catalog anti-pattern section upgrades — no ADR explicitly governs pattern catalog modifications
- **GAP 2:** Five recommendations from TASK-014 (template analysis — ADV-REC-001–003, WT-REC-003, WT-GAP-005) touch template improvements not covered by ADR-001 through ADR-004

These gaps do not invalidate the ADRs — they identify scope that requires additional governance documents if the full 130-recommendation set is to be implemented.

**Source:** barrier-5/synthesis.md (Coverage Gap Analysis, v1.1.0, 0.956 PASS)

---

## 4. NPT Taxonomy Summary

### Overview

The Phase 3 taxonomy (TASK-008, v3.0.0, 0.957 PASS) produced 14 named patterns (13 distinct techniques) across the NPT-001 to NPT-014 namespace. Methodology: deductive framework extension (NOT Braun & Clarke inductive thematic analysis — the inductive method was used in Phase 1 literature synthesis; Phase 3 applied a deductive taxonomy against pre-established pattern dimensions). NPT-007 and NPT-014 are dual entries addressing the same construct (Type 1 blunt prohibition) from opposite analytical directions.

### Pattern Catalog (Abbreviated)

| Pattern | Name | Evidence Tier | AGREE-5 Rank | When to Use | When NOT to Use |
|---------|------|--------------|--------------|-------------|-----------------|
| NPT-001 | Model-Internal Behavioral Intervention | T1 | 1 | Foundation model fine-tuning, RLHF | Prompt-level constraint enforcement — requires model access |
| NPT-002 | Instruction Hierarchy Prioritization | T1 | 2 | System prompt structural enforcement | User-turn constraints — hierarchy is system-level only |
| NPT-003 | Hard-Coded Constraint Integration | T4 | 3 | Non-negotiable limits baked into inference infrastructure | Soft constraints — code enforcement is disproportionate |
| NPT-004 | Output Filter and Validation | T4 | 4 | Post-generation constraint enforcement | Preventing behavior at generation time — filters are post-hoc |
| NPT-005 | Warning-Based Meta-Prompt | T3/T4 | 5 | Pre-task constraint priming | Task-level constraint enforcement — meta-prompt is orientation, not binding |
| NPT-006 | Atomic Decomposition of Constraints | T4 | 6 | Breaking compound constraints into non-overlapping sub-constraints | Simple single-behavior constraints — decomposition adds no value |
| NPT-007 | Positive-Only Framing | Untested baseline | 12 | Default without specific constraint need | Any situation requiring behavioral prohibition — positive-only lacks constraint anchoring |
| NPT-008 | Contrastive Example Pairing | T3 (E-007, AGREE-9) | 10–11 | Pattern documentation; training materials | Runtime behavioral enforcement — contrastive examples are educational, not behavioral |
| NPT-009 | Declarative Behavioral Negation | T3/T4 | 9 | HARD-tier constraint enforcement where consequence is known | Low-stakes constraints — overhead exceeds benefit |
| NPT-010 | Paired Prohibition with Positive Alternative | T3/T4 | 9 | Routing disambiguation; constraints requiring positive redirect | Absolute prohibitions with no valid alternative path |
| NPT-011 | Justified Prohibition with Contextual Reason | T4 | 9 | Constitutional compliance; high-cost prohibitions needing rationale | Trivial constraints — justification overhead is not warranted |
| NPT-012 | L2 Re-Injected Negation | T4 | 8 | HARD-tier rules requiring compaction survival | Soft constraints; agent/skill files (architectural exclusion: L2 operates only on `.context/rules/`) |
| NPT-013 | Constitutional Triplet | T1/T3 | 7 | Agent governance; P-003/P-020/P-022 enforcement cluster | Domain-specific behavioral constraints — constitutional triplet is governance, not domain |
| NPT-014 | Standalone Blunt Prohibition | T1+T3 (avoid) | Avoid | DIAGNOSTIC ONLY — identifies upgrade candidates | All production contexts — T1+T3 establishes this is the worst formulation |

**Critical notes:**
- NPT-014 is an anti-pattern designation, not a technique. Its inclusion provides a diagnostic label for the problematic formulation the taxonomy recommends eliminating.
- Rank 7 in AGREE-5 is unoccupied — the taxonomy does not force a technique into this position.
- Evidence tiers for ranks 9–11 (NPT-009/NPT-010/NPT-011) are T4 observational for the pattern itself; causal comparison against positive equivalents is UNTESTED pending Phase 2.

### Evidence Distribution

| Evidence Tier | Pattern Count | Which Patterns |
|--------------|---------------|----------------|
| T1 established (peer-reviewed causal) | 2 | NPT-001, NPT-002 |
| T3 provisional (preprint/directional) | 2 | NPT-005, NPT-008 |
| T4 working practice (observational) | 7 | NPT-003, NPT-004, NPT-006, NPT-010, NPT-011, NPT-012, NPT-013 |
| T1+T3 (NPT-014 underperformance) + T3/T4 (NPT-009) | 3 | NPT-009, NPT-014, NPT-007 |
| Untested baseline | 1 | NPT-007 |

---

## L2: Strategic Synthesis

*Audience: Principal Architects and Framework Maintainers. Strategic themes, ADR governance, implementation roadmap, risk posture, and actionable recommendations.*

Sections 5 through 10 constitute the L2 strategic synthesis layer. They address: how the research findings translate into governance decisions for the Jerry Framework (Section 5), the sequenced implementation plan with dependency ordering (Section 6), the experimental design that resolves the remaining untested claims (Section 7), the reversibility contingency if Phase 2 yields a null finding (Section 8), the risk posture (Section 9), and the prioritized recommendation set (Section 10).

**Strategic framing:** Three unconditional actions are warranted now regardless of Phase 2 outcome: (1) eliminate NPT-014 blunt prohibitions from rule files, (2) add L2 re-injection for Tier B HARD rules exposed to compaction, and (3) document the T-004 compaction failure mode. All Phase 2-conditional changes are explicitly gated on Stage 0 baseline capture before any production file modification.

---

## 5. Jerry Framework Impact Assessment

### Overview: Four Architecture Decision Records (PROPOSED)

Phase 5 produced four ADRs governing Jerry Framework evolution. All are currently PROPOSED status (pre-approval, pre-Phase-2-completion). Implementation sequencing is governed by the Stage ordering in Section 6.

**Critical constraint (NEVER override):** MUST NOT apply any ADR-specified file changes to production Jerry Framework files until the Phase 2 experimental baseline is captured (Stage 0 in Section 6).

---

### ADR-001: NPT-014 Elimination Policy

**File:** `phase-5/ADR-001-npt014-elimination.md` | **Score:** 0.952 PASS

**Decision:** Mandate universal upgrade from NPT-014 (standalone blunt prohibition) to NPT-009 (declarative behavioral negation with consequence documentation, scope specification, and behavioral context) across all Jerry Framework artifacts.

**Evidence:** T1+T3, HIGH, unconditional. PG-001 (barrier-2/synthesis.md): blunt prohibition demonstrably underperforms structured alternatives. A-20 (AAAI 2026), A-15 (EMNLP 2024), A-31 (arXiv T3). Does NOT require Phase 2 outcome — the evidence for NPT-014 underperformance is already established.

**Scope:** ~22 instances in rule files (61%), plus equivalent instances in skills, agents, patterns, and templates as identified in Phase 4 analyses.

**Upgrade pattern example:**
- BEFORE (NPT-014): `"NEVER hardcode values"`
- AFTER (NPT-009): `"NEVER hardcode configuration values in source files. Consequence: credential exposure risk; testability failure; CI environment mismatch. Scope: all files in src/. Instead: use environment variables via src/shared_kernel/config.py."`

**Phase 2 dependency:** NONE for drafting. Phase 2 baseline capture required before production file modification.

**Options evaluated:** Option 1 (Universal elimination, 9/10) > Option 2 (Rule files only, 6/10) > Option 3 (Defer all, 3/10).

---

### ADR-002: Constitutional Constraint Upgrades

**File:** `phase-5/ADR-002-constitutional-upgrades.md` | **Score:** 0.951 PASS

**Decision:** Three-component upgrade to constitutional constraint expression:
1. **Phase 5A (Unconditional):** Add constitutional triplet (P-003/P-020/P-022 as NEVER-framed NPT-013 prohibitions) to SKILL.md files; update agent-development-standards.md guardrails template minimum example from NPT-014 to NPT-009 format
2. **Phase 5B (Conditional on Phase 2):** Add NPT-010 (paired prohibition with positive alternative) and NPT-011 (justified prohibition) framing to HARD-tier rules in rule files; upgrade mid- and low-maturity agent forbidden_actions entries

**Evidence:** VS-004 (Anthropic expresses P-003/P-020/P-022 as NEVER statements — T4 observational); A-15 (structured compliance improvement — T1). Phase 5B components are contingent on Phase 2 because they test whether structured negative framing outperforms structurally equivalent positive framing.

**Current state:** 22 NPT-014 in rule files (61%); 0 NPT-010 instances; 0 NPT-011 instances across all audited files.

---

### ADR-003: Routing Disambiguation Standard

**File:** `phase-5/ADR-003-routing-disambiguation.md` | **Score:** 0.957 PASS

**Decision:** Two-component standard for routing constraint expression in SKILL.md files:
- **Component A (Unconditional):** Add consequence documentation to "Do NOT use when:" sections in all skills currently missing it — 13 skills need updates (7 missing routing disambiguation entirely, 6 with partial sections lacking consequence)
- **Component B (Conditional on Phase 2):** Express routing prohibitions as NPT-010 MUST NOT framing with consequence (currently positive redirect language)

**Evidence gap acknowledged:** No controlled evidence establishes that "MUST NOT use when:" framing outperforms positive routing guidance. Component B's motivation is working-practice alignment with VS-003 and AGREE-5 hierarchy; it is not T1-validated. Component B is explicitly Phase 2-conditional.

**Skills missing routing disambiguation entirely:** bootstrap, nasa-se, problem-solving, transcript, worktracker, architecture, eng-team (7 skills)

---

### ADR-004: Compaction Resilience

**File:** `phase-5/ADR-004-compaction-resilience.md` | **Score:** 0.955 PASS

**Decision:** Three unconditional actions:
1. **PG-004 testing:** Add multi-turn context compaction test conditions to the Phase 2 experimental pilot (condition C7 covers compaction scenario)
2. **NPT-012 L2-REINJECT for H-04 and H-32:** Add L2 re-injection markers for the two highest-priority Tier B HARD rules (H-04: active project REQUIRED; H-32: GitHub Issue parity). Token budget: ~180 tokens headroom available; ~60-100 tokens needed for these two additions
3. **T-004 documentation:** Document the context compaction failure mode in constraint-bearing artifacts so practitioners understand the risk

**Why unconditional:** The T-004 failure mode is mechanically verifiable and independent of framing vocabulary preference. Context compaction dropping L1-only constraints is a structural resilience gap regardless of whether negative or positive framing is ultimately superior.

**Tier B HARD rules without L2 protection (5 total):** H-04, H-16, H-17, H-18, H-32. ADR-004 Option B adds L2 protection to H-04 and H-32 only (worst-case budget ~790/850 tokens).

---

### Cross-ADR Coherence Summary

The four ADRs are internally coherent with no direct conflicts (barrier-5/synthesis.md). Key cross-ADR dependencies:

| Dependency | Description |
|-----------|-------------|
| ADR-001 → ADR-002 | NPT-014 elimination (ADR-001) is the prerequisite for constitutional upgrade (ADR-002) — you cannot upgrade framing without first establishing the baseline minimum |
| ADR-004 → all ADRs | Phase 2 baseline capture (Stage 0, driven by ADR-004's PG-004 testing requirement) gates all production file changes |
| ADR-002 Phase 5A → ADR-003 Component A | Both are unconditional; can execute in parallel after Stage 0 |

---

### ADR Approval Process

All four ADRs are currently PROPOSED status. PROPOSED means the decision rationale, options analysis, and consequences have been documented but the ADR has not been ratified by the framework owner. The following process governs transition from PROPOSED to APPROVED (or REJECTED/SUPERSEDED).

**Approver:** Framework maintainer / project owner (the human authority for the Jerry Framework governance).

**Approval triggers by ADR type:**

| ADR | Type | Approval Trigger | Timeline |
|-----|------|-----------------|----------|
| ADR-001 (NPT-014 elimination) | Unconditional | Stage 0 baseline capture documented in worktracker. No Phase 2 dependency — evidence is already T1+T3. | Approve before Stage 1 begins (target: days 1–2 of implementation) |
| ADR-002 Phase 5A (constitutional upgrade) | Unconditional component | Stage 0 baseline capture documented. Phase 5A components do not depend on Phase 2. | Approve concurrently with ADR-001 |
| ADR-002 Phase 5B (framing upgrade) | Phase 2-conditional component | Phase 2 experimental verdict delivered. Only applicable if Phase 2 finds structured negative > structured positive. | Approve after Phase 2 verdict (Stage 6 gate) |
| ADR-003 Component A (consequence documentation) | Unconditional component | Stage 0 baseline capture documented. | Approve concurrently with ADR-001 |
| ADR-003 Component B (MUST NOT routing framing) | Phase 2-conditional component | Phase 2 experimental verdict delivered. | Approve after Phase 2 verdict (Stage 6 gate) |
| ADR-004 (compaction resilience) | Unconditional | Stage 0 baseline capture documented. T-004 is mechanically verifiable; no experimental dependency. | Approve concurrently with ADR-001 |

**Approval action:** Approver updates the `status` field in each ADR file from `PROPOSED` to `APPROVED` (or `REJECTED` / `SUPERSEDED`) and adds an approval date and rationale. Worktracker entry for the relevant Stage must be updated to reference the approved ADR.

**Rejection path (PG-003 alignment):** If an ADR is rejected — either at initial review or because Phase 2 yields a null or negative finding for Phase 2-conditional ADRs:
1. Update ADR status to `REJECTED` with documented rationale.
2. For Stage 1–4 changes already implemented under a subsequently rejected conditional component: revert the framing-preference elements only. Consequence documentation additions (Component A elements) retain value and SHOULD NOT be reverted unless they introduced substantive errors.
3. Document the rejection as a research finding per PG-003 Section 8 guidance.
4. Update AGREE-5 hierarchy and PG-001 through PG-005 practitioner guidance to reflect the verdict.

**Escalation:** If the framework maintainer is unavailable or the ADR touches shared governance (e.g., ADR-002 modifications to `agent-development-standards.md` used across projects), escalate to C4 review per AE-001 through AE-004 auto-escalation rules in `quality-enforcement.md`.

---

## 6. Implementation Roadmap

### 6-Stage Sequence (barrier-5/synthesis.md)

This ordering has no circular dependencies. All stage boundaries are verified. Calendar estimates assume sustained part-time effort; Phase 2 timeline is the primary uncertainty.

```
Stage 0: Phase 2 Baseline Capture (1–2 days) — PREREQUISITE
    ↓
Stage 1: Rule Files + L2 Markers + T-004 Documentation (1 week)
    ↓
Stage 2: Agent Definition Standards (1 week, coordinated single commit)
    ↓ (parallel with Stage 2)
Stage 3: SKILL.md + Routing Disambiguation (2–3 weeks)
    ↓ (parallel with Stages 2–3, after Stage 0)
Stage 4: Pattern and Template Documentation (2–3 weeks)
    ↓
Stage 5: Phase 2 Experimental Pilot (4–12 weeks — primary uncertainty)
    ↓
Stage 6: Phase 2-Conditional Changes (1–2 weeks after Phase 2 verdict)
```

**Total calendar estimate:** 9–20 weeks (variance driven by Phase 2 timeline)

---

### Stage 0: Phase 2 Baseline Capture (PREREQUISITE)

**Duration:** 1–2 days
**Owner:** PROJ-014 research lead
**Blocking:** ALL subsequent stages that modify production files

**Actions:**
- CX-A-001: Snapshot all Jerry Framework constraint artifact files (commit hash recorded in worktracker)
- CX-A-002: Export VS-001 instance inventory with line numbers for production change tracking
- CX-A-003: Document the current state of the 5 Tier B HARD rules without L2 protection

**Why first:** All Phase 4 analyses uniformly prohibit production file changes before Phase 2 experimental conditions are established. Modifying NPT-014 instances before capturing baseline makes the experimental conditions (C1 = current Jerry Framework constraint style) unreproducible.

**Output:** A tagged commit or snapshot document preserving the pre-intervention state.

---

### Stage 1: Rule Files + L2 Markers + T-004 Documentation

**Duration:** 1 week
**ADR:** ADR-001 (NPT-014 elimination for rule files), ADR-004 (L2 markers + T-004 docs)
**Blocked by:** Stage 0

**Actions (from cross-ADR action register):**
- CX-A-004: Apply NPT-009 upgrade to 22 NPT-014 instances in `.context/rules/` (starting with highest-density files: python-environment.md × 5, architecture-standards.md × 3, testing-standards.md × 2)
- CX-A-005: Add L2-REINJECT markers for H-04 (active project) and H-32 (GitHub Issue parity) — ~60-100 token budget consumption
- CX-A-006: Add T-004 failure mode documentation to quality-enforcement.md and agent-development-standards.md

**Dependency:** Stage 1 must complete before Stage 2 (rule standards govern agent guardrails template; agent updates must mirror rule file improvements, not precede them).

**Evidence:** T1+T3 unconditional for NPT-009 upgrades (PG-001); T4 observational for L2 marker additions.

---

### Stage 2: Agent Definition Standards (Coordinated)

**Duration:** 1 week
**ADR:** ADR-002 Phase 5A (guardrails template upgrade in agent-development-standards.md)
**Blocked by:** Stage 1

**Actions:**
- CX-A-007: Update guardrails template minimum example in `agent-development-standards.md` from `"Spawn recursive subagents (P-003)"` (NPT-014) to NPT-009 format with consequence documentation
- CX-A-008: Add REC-YAML-001 forbidden_action_format tracking field to agent-governance-v1.schema.json (additive, non-breaking)
- CX-A-009: Update VIOLATION label format guidance in agent-development-standards.md (REC-F-002)

**Must execute as a coordinated single commit** to prevent intermediate states where the schema has a new tracking field but the guardrails template has not been updated.

**MUST NOT apply to individual agent files yet** — agent-level updates (upgrading forbidden_actions entries in .governance.yaml) wait until Stage 6 (Phase 2-conditional) or are addressed by a separate ADR-002 Phase 5B implementation.

---

### Stage 3: SKILL.md and Routing Disambiguation (Parallel with Stage 2)

**Duration:** 2–3 weeks
**ADR:** ADR-002 Phase 5A (constitutional triplet in SKILL.md), ADR-003 Component A (consequence documentation)
**Blocked by:** Stage 0; can run parallel with Stage 2

**Actions:**
- CX-A-010: Add NPT-013 NEVER-framed constitutional compliance tables to all 13 SKILL.md files (replacing positive framing "Agents are workers, not orchestrators" with "NEVER invoke recursive subagents...")
- CX-A-011: Add consequence documentation to "Do NOT use when:" sections in all 13 skills missing it (ADR-003 Component A — consequence documentation motivation is auditability, not framing preference)
- CX-A-012: Add routing disambiguation sections to 7 skills that are completely missing them (architecture, nasa-se, problem-solving, transcript, worktracker, bootstrap, eng-team)

**Phase 2 conditional:** NPT-010 MUST NOT framing for routing prohibitions (ADR-003 Component B) waits until Stage 6.

---

### Stage 4: Pattern and Template Documentation (Parallel, after Stage 0)

**Duration:** 2–3 weeks
**ADR:** GAP 1 and GAP 2 coverage (no dedicated ADR — requires supplemental governance)
**Blocked by:** Stage 0; can run parallel with Stages 2–3

**Actions:**
- Apply "MUST NOT omit" (Group 1) pattern catalog recommendations: ARCH-R1 (hexagonal architecture boundary constraint), ARCH-R4 (anti-pattern table consequence upgrades), TEST-R1 (BDD cycle "Never Write Code Without Failing Test" NPT-009 upgrade) — 6 total
- Apply EPIC.md creation constraint block (WT-REC-001 — zero current constraints, PG-001 HIGH priority)
- Apply worktracker template NPT-009 upgrades (WT-REC-002 for TASK.md, BUG.md, ENABLER.md, FEATURE.md)
- Document A-11 hallucination in pattern catalog revision history (governance record)

**Conditional:** "SHOULD add" and "MAY add" pattern recommendations (28 + 10 items) wait until Phase 2 verdict and possible supplemental governance.

---

### Stage 5: Phase 2 Experimental Pilot

**Duration:** 4–12 weeks (primary uncertainty source)
**Blocked by:** Stage 0 (baseline must be captured before pilot begins)
**Owner:** Research lead + external IRB/ethical review if using human participants

**This stage is the fulcrum of the entire roadmap.** Stage 6 is contingent on its outcome.

**Design summary:** n=270 matched pairs, McNemar's test, p_12=0.20, p_21=0.10.
**Pilot first:** n=30 with go/no-go criteria before full experiment.
See Section 7 for full experimental design.

---

### Stage 6: Phase 2-Conditional Changes

**Duration:** 1–2 weeks after Phase 2 verdict
**ADR:** ADR-002 Phase 5B, ADR-003 Component B

**If Phase 2 finds structured negative framing > structured positive:**
- Implement ADR-002 Phase 5B (agent forbidden_actions upgrade to NPT-009 across all 30+ agents)
- Implement ADR-003 Component B (routing prohibition MUST NOT framing)
- Confirm all Group 2 (SHOULD add) recommendations from Phase 4

**If Phase 2 finds null framing effect (PG-003 scenario):**
- Do NOT implement ADR-002 Phase 5B framing-motivated changes
- Do NOT implement ADR-003 Component B
- Retain Stage 1–4 changes (consequence documentation retains independent auditability value)
- Revise practitioner guidance to reflect convention-driven framing choice

**If Phase 2 finds structured negative framing < structured positive:**
- Revert all framing changes from Stages 1–4
- Update AGREE-5 hierarchy and PG-001–PG-005 practitioner guidance
- Document as a major research finding and update ADRs accordingly

---

## 7. Phase 2 Experimental Design

### Research Questions

- **Primary RQ:** Does structured negative prompting reduce LLM hallucination rate compared to structurally equivalent positive instructions?
- **Secondary RQ:** Does structured negative prompting improve behavioral constraint adherence rate compared to structurally equivalent positive instructions?

### Design Parameters

| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Design | Matched pairs (within-subject) | Controls for prompt-level confounds |
| Statistical test | McNemar's test (binary paired outcomes) | Appropriate for matched binary outcomes |
| Total pairs | n=270 | Power calculation: p_12=0.20, p_21=0.10, α=0.05, power=0.80, continuity correction applied |
| Pilot phase | n=30 | Go/no-go before full experiment |
| Conditions | C1–C7 (7 conditions) | Covers NPT-007 through NPT-012 effectiveness hierarchy |

### Experimental Conditions (C1–C7)

| Condition | Label | Description | NPT Equivalent |
|-----------|-------|-------------|----------------|
| C1 | Positive baseline | Structurally equivalent positive instruction (MUST do X) | NPT-007 |
| C2 | Blunt prohibition | Standalone NEVER/MUST NOT without consequence | NPT-014 |
| C3 | Behavioral negation | NEVER/MUST NOT with consequence documentation | NPT-009 |
| C4 | Paired prohibition | NEVER X + "Instead: do Y" alternative | NPT-010 |
| C5 | Justified prohibition | NEVER X + "Reason: Z" justification clause | NPT-011 |
| C6 | L2 re-injected | Per-prompt re-injected constraint (surviving context compaction) | NPT-012 |
| C7 | Post-compaction | Same as C3/C4, measured after simulated context compaction event | Compaction resilience test |

### Pilot Go/No-Go Criteria

| Pilot Outcome | Criterion | Action |
|--------------|-----------|--------|
| GO | ≤4 failures on n=30 | Proceed to full experiment |
| NO-GO | ≥7 failures on n=30 | Redesign protocol before proceeding |
| BORDERLINE | 5–6 failures | Evaluate remaining criteria; proceed if at least 2 of 3 secondary criteria pass |

### Outcome Metrics

| Task Category | Hallucination Metric | Behavioral Compliance Metric |
|--------------|---------------------|------------------------------|
| Factual claim generation | Fact verification rate (external gold standard) | Citation accuracy rate |
| Code generation | Functional test pass rate | Style rule compliance rate |
| Constraint-adherent summarization | Constraint violation rate | Scope adherence rate |
| Multi-turn dialogue | Instruction drift rate | Character/persona consistency |
| Structured output generation | Schema compliance rate | Format constraint adherence |

### Independence and Reflexivity Constraints

Per supplemental-vendor-evidence.md (L-1, L-2, L-3):
- **L-1 (Researcher-System Independence):** The researcher observing PROJ-014 is also the primary user of the Jerry Framework being tested — this creates a reflexivity limitation. External evaluators or automated metrics are required for at least one measurement instrument.
- **L-2 (Observation Confound):** Session observations (EO-001 through EO-003) used to inform design may introduce expectation bias. Pilot results must be evaluated blind to condition labels where possible.
- **L-3 (Replication Constraint):** Conditions C1–C7 must be fully documented and reproducible by a third-party researcher.

---

## 8. PG-003 Contingency Plan

### What PG-003 Covers

PG-003 is the practitioner guidance addressing the scenario where Phase 2 finds a null framing effect: structured negative prompting produces equivalent behavioral outcomes to structurally equivalent positive framing. If this occurs, the motivation for preferring NEVER/MUST NOT vocabulary shifts from effectiveness (UNTESTED) to convention (established by VS-003 working practice).

### PG-003 Null Scenario Actions

**If Phase 2 finds null framing effect at ranks 9–11 (NPT-009/NPT-010/NPT-011 vs. positive equivalents):**

| Action Category | Action | Rationale |
|----------------|--------|-----------|
| Retain Stage 1–4 changes | Keep consequence documentation additions | Consequence documentation retains auditability and human readability value independent of framing preference |
| Do not revert L2 markers | Retain NPT-012 additions (Stage 1 ADR-004 actions) | Context compaction resilience is structural, not vocabulary-dependent |
| Do not implement Stage 6 framing changes | ADR-002 Phase 5B and ADR-003 Component B are cancelled | Without effectiveness evidence, mandatory NEVER/MUST NOT framing is unnecessary burden |
| Update AGREE-5 hierarchy | Mark ranks 9–11 as "equivalent to positive alternatives" | Prevents future misuse of the hierarchy as effectiveness evidence |
| Revise practitioner guidance | Update PG-001 through PG-005 to reflect convention-driven framing | PG-001 (blunt prohibition underperformance) survives — it is unconditional regardless of null finding |
| Document as positive finding | A null finding is a scientifically valid outcome | Practitioner guidance: choose framing by convention or team preference; structural elements (consequence, scope, positive pairing) add value regardless |

### What Survives PG-003 Null Finding

**These recommendations retain their value regardless of Phase 2 outcome:**

1. NPT-014 elimination (PG-001, unconditional) — blunt prohibition underperforms structured alternatives whether those alternatives are negative or positive
2. Consequence documentation additions — auditability value is independent of vocabulary
3. Scope specification additions — precision value is independent of vocabulary
4. L2 re-injection for Tier B rules — compaction resilience is structural
5. T-004 failure mode documentation — factual and structural, not vocabulary-dependent

### What Depends on Phase 2 Outcome

| Contingent Element | Depends On | Status if Null |
|-------------------|-----------|----------------|
| NEVER/MUST NOT framing in constitutional compliance tables | Phase 2 C3 vs C1 outcome | Reverts to positive framing |
| ADR-002 Phase 5B agent forbidden_actions upgrades | Phase 2 C3 vs C1 outcome | Not implemented |
| ADR-003 Component B MUST NOT routing framing | Phase 2 C4 vs C1 outcome | Not implemented |
| AGREE-5 hierarchy ranks 9–11 ordering | Phase 2 C3/C4/C5 vs C1 outcomes | Becomes "equivalent" zone |

---

## 9. Risk Register

### Risk Assessment Framework

| Severity Label | Definition |
|---------------|-----------|
| CRITICAL | Could invalidate entire research program or produce irreversible Jerry Framework harm |
| HIGH | Could significantly delay implementation or compromise research validity |
| MEDIUM | Could require rework but is recoverable within reasonable effort |
| LOW | Minor impact; self-correcting with normal oversight |

---

### R-001: Phase 2 Experimental Confound — Jerry Framework as Subject and Observer

**Type:** Research validity | **Severity:** CRITICAL | **Probability:** HIGH

**Description:** The researcher observing PROJ-014 is the primary user of the Jerry Framework being tested. Session observations (EO-001–EO-003) that informed design were conducted in the researcher's own system. This violates the independence requirement for causal inference.

**Mitigation:**
- Use automated evaluation metrics (not researcher judgment) as primary outcome measures
- Include at least one measurement instrument evaluated by external rater or automated oracle
- Document L-1 limitation explicitly in all experimental outputs
- Consider third-party replication before treating Phase 2 results as generalizable

**Status:** ACCEPTED with mitigation required in experimental design

---

### R-002: Production File Modification Before Phase 2 Baseline Capture

**Type:** Research design contamination | **Severity:** CRITICAL | **Probability:** MEDIUM

**Description:** If any NPT-014 instances in production rule files are modified before the Phase 2 baseline snapshot is captured, the experimental condition C1 (current Jerry Framework constraint style) becomes unreproducible. This would invalidate the within-subject comparison.

**Mitigation:**
- Stage 0 (baseline capture) is mandatory and gates all other stages
- Stage 0 completion must be documented in worktracker with a verifiable artifact (commit hash or snapshot file)
- Any urgent production constraint fix during Phase 2 must be quarantined as a separate commit NOT merged into the baseline snapshot

**Status:** BLOCKED by Stage 0 gate (deterministic prevention)

---

### R-003: Context Compaction Directional Reversal During Phase 2

**Type:** Experimental outcome validity | **Severity:** HIGH | **Probability:** LOW

**Description:** TASK-006 identified a potential directional reversal scenario: D1 (constraint adherence) findings may be reversed under context compaction conditions. If structured negative constraints are effective in fresh context but fail under compaction while structured positive constraints do not, the Phase 2 result is condition-dependent, not generalizable.

**Mitigation:**
- C7 experimental condition explicitly tests post-compaction performance
- Pilot must include multi-turn context compaction test (Assumption U-003, barrier-2/synthesis.md)
- Report C7 results separately from C1–C6 to enable compaction-stratified analysis

**Status:** MITIGATED by experimental design (C7 condition)

---

### R-004: A-11 Citation Contamination in Downstream Documents

**Type:** Research integrity | **Severity:** HIGH | **Probability:** LOW (risk is contained)

**Description:** The confirmed-hallucinated A-11 citation was removed from TASK-013 in I5 but may have been propagated to other documents via copy-paste before the correction was made. Any downstream document citing A-11 for NPT-008 support has an invalid evidence basis.

**Mitigation:**
- Document the A-11 hallucination prominently in this synthesis (KF-012) and barrier-4 synthesis
- Any Phase 6 document citing NPT-008 must use E-007 (AGREE-9, 2-of-3 cross-survey) as the sole evidence source
- Run a text search on all PROJ-014 documents for "A-11" references before finalizing implementation guidance
- NEVER introduce A-11 in any future document

**Status:** MITIGATED by documented prohibition; requires verification sweep

---

### R-005: L2 Token Budget Exhaustion

**Type:** Technical constraint | **Severity:** MEDIUM | **Probability:** LOW

**Description:** The L2 re-injection token budget is 850 tokens. Current consumption is estimated at 559–670 tokens (discrepancy documented in TASK-012). ADR-004 adds L2 markers for H-04 and H-32 (~60-100 tokens). If the actual current consumption is at the high estimate (670 tokens), worst-case after ADR-004 additions is ~790 tokens — within budget but with only ~60 tokens remaining. Any additional L2 marker additions beyond ADR-004 scope risk budget exhaustion.

**Mitigation:**
- Resolve the 559 vs. ~670 token discrepancy before implementing ADR-004 L2 additions
- Use conservative (670) estimate for budget calculations
- Do not add Tier B rules H-16, H-17, H-18 L2 markers without a separate budget audit
- Monitor L2 budget after each addition

**Status:** MONITOR — requires budget audit in Stage 1

---

### R-006: Phase 4 Recommendation Volume Exceeds Implementation Capacity

**Type:** Implementation feasibility | **Severity:** MEDIUM | **Probability:** MEDIUM

**Description:** 130 recommendations across 5 domains is a substantial implementation scope. Without explicit prioritization gates, the temptation to implement broadly before Phase 2 could lead to baseline contamination (R-002) or incomplete partial implementations that create inconsistent constraint quality across domains.

**Mitigation:**
- Stage sequence (Section 6) gates implementation by evidence tier: Group 1 ("MUST NOT omit") in Stages 1–4; Group 2 ("SHOULD add") in Stage 6 after Phase 2; Group 3 ("MAY add") post-Stage 6
- NEVER begin Stage 2/3/4 work before Stage 0 is documented
- Assign each recommendation to exactly one stage to prevent double-counting or omission

**Status:** MITIGATED by Stage sequencing

---

### R-007: AGREE-5 Hierarchy Misuse as T1 Evidence

**Type:** Research integrity | **Severity:** MEDIUM | **Probability:** MEDIUM

**Description:** The AGREE-5 12-level effectiveness hierarchy is an internally generated synthesis narrative (adversary gate 0.953). It is not externally validated. It is not based on controlled experiments. If any downstream document cites AGREE-5 rank ordering as if it were T1 or T3 evidence, it misrepresents the evidence base.

**Mitigation:**
- NEVER cite AGREE-5 as T1 or T3 evidence in any Phase 5, Phase 6, or implementation document
- When citing AGREE-5 rank ordering, always append: "(internally generated synthesis narrative, adversary gate 0.953, NOT externally validated)"
- barrier-4/synthesis.md Section 4 Group 2 and Group 3 notes include this caveat; ensure it is preserved in all downstream citations

**Status:** MONITOR — requires citation discipline in all future documents

---

## 10. Recommendations

These recommendations are produced by ps-synthesizer (convergent cognitive mode, C4 criticality synthesis). All recommendations are grounded in the evidence presented in this synthesis. Evidence tiers are explicitly stated. NEVER treat T4 observational recommendations as experimentally validated.

### Priority: Unconditional (T1+T3, Act Now)

---

**R-001: Capture Phase 2 Baseline Before Any Production Changes**

**Priority:** MUST (IMMEDIATE) — prerequisite for all other recommendations
**Evidence:** T1+T3 unconditional; all 5 Phase 4 analyses unanimous
**Action:** Create a tagged git commit or snapshot document preserving the current state of all `.context/rules/`, `skills/`, `skills/*/agents/`, and `.context/templates/` files before implementing any Phase 4 or Phase 5 recommendations. Record the commit hash in a PROJ-014 worktracker entry.
**NEVER omit this step** — without a documented baseline, Phase 2 experimental conditions cannot be reproduced.

---

**R-002: Eliminate All NPT-014 Instances in Rule Files (Stage 1)**

**Priority:** MUST (HIGH) — unconditional per PG-001
**Evidence:** T1+T3 (A-20, A-15, A-31); PG-001 HIGH
**Action:** Apply ADR-001 NPT-014 elimination policy to the 22 identified instances in `.context/rules/` files. Priority order: python-environment.md (5 instances), architecture-standards.md (3 instances), quality-enforcement.md (5 instances). Each upgrade must include: consequence statement, scope specification, and behavioral context. Pattern: `"NEVER [X]. Consequence: [Y]. Scope: [Z]. Instead: [W]."`
**Do NOT wait for Phase 2** for this recommendation — NPT-014 underperformance is established independently of the structured-negative vs. structured-positive comparison.

---

**R-003: Add L2 Re-Injection for H-04 and H-32 (Stage 1)**

**Priority:** MUST (HIGH) — structural resilience gap
**Evidence:** T4 observational (T-004 failure mode, mechanically verified); PG-004
**Action:** Add L2-REINJECT HTML comment markers to quality-enforcement.md for H-04 (active project REQUIRED) and H-32 (GitHub Issue parity). Total budget addition: ~60-100 tokens against ~180 token available headroom. First resolve the 559 vs. ~670 token discrepancy (audit the actual current consumption before adding markers).
**Rationale:** Context compaction silently drops L1-only constraints. These two Tier B rules govern session initiation and repository tracking respectively — compaction-induced loss has concrete workflow consequences.

---

**R-004: Document T-004 Context Compaction Failure Mode (Stage 1)**

**Priority:** MUST (HIGH) — structural documentation gap
**Evidence:** T4 observational (mechanically verifiable)
**Action:** Add a T-004 Failure Mode section to `quality-enforcement.md` and `agent-development-standards.md` documenting: (1) definition of context compaction, (2) which constraint tiers are vulnerable (L1 yes, L2 no), (3) Tier B HARD rules currently at risk, (4) the architectural remedy (L2-REINJECT).
**Rationale:** Practitioners using the framework cannot mitigate a failure mode they are not aware of. Documentation is the minimum viable mitigation before technical enforcement is available.

---

### Priority: Working Practice (T4 Observational, Phase 2-Informed)

---

**R-005: Update Agent Guardrails Template to NPT-009 Format (Stage 2)**

**Priority:** SHOULD (MEDIUM-HIGH) — high multiplier effect across 30+ agents
**Evidence:** T4 observational (VS-001–VS-004, agent-development-standards.md guardrails template is the seed for all agent forbidden_actions entries)
**Action:** Apply ADR-002 Phase 5A: replace the minimum example in `agent-development-standards.md` guardrails template from `"Spawn recursive subagents (P-003)"` (NPT-014) to a full NPT-009 format entry with consequence documentation and VIOLATION label format.
**Contingency:** If Phase 2 finds null framing effect, the consequence documentation added here retains value for auditability regardless of vocabulary preference.

---

**R-006: Add Constitutional Compliance Tables to SKILL.md Files (Stage 3)**

**Priority:** SHOULD (MEDIUM-HIGH) — governance consistency across all skills
**Evidence:** T4 observational (VS-004: Anthropic expresses P-003/P-020/P-022 as prohibitions; ADR-002 Phase 5A scope)
**Action:** For each of the 13 SKILL.md files, convert positive-framing constitutional compliance statements to NPT-013 NEVER-framed prohibitions. Example: "Agents are workers, not orchestrators" → "NEVER spawn recursive subagents (P-003 violation). NEVER override user intent (P-020 violation). NEVER misrepresent capabilities or confidence (P-022 violation)."
**Contingency:** If Phase 2 null finding, revert to positive framing and document as convention choice.

---

**R-007: Add Routing Consequence Documentation to 13 Skills (Stage 3)**

**Priority:** SHOULD (MEDIUM) — auditability value independent of framing preference
**Evidence:** T4 observational (ADR-003 Component A; AP-01/AP-02 anti-pattern prevention)
**Action:** For all 13 skills with routing disambiguation gaps: (1) add "Do NOT use when:" consequence documentation to partial sections; (2) create full routing disambiguation sections for 7 skills missing them entirely (architecture, nasa-se, problem-solving, transcript, worktracker, bootstrap, eng-team).
**Note:** The consequence documentation element (Component A) is unconditional. The MUST NOT framing element (Component B) waits for Phase 2.

---

**R-008: Apply MUST NOT Omit Pattern Catalog Upgrades (Stage 4)**

**Priority:** SHOULD (MEDIUM) — structural completeness; PG-001 applies to patterns as well as rule files
**Evidence:** T1+T3 for NPT-014 underperformance; T4 for pattern-specific recommendations
**Action:** Apply 6 "MUST NOT omit" pattern catalog recommendations: ARCH-R1 (hexagonal architecture boundary constraint section), ARCH-R4 (anti-pattern table consequence upgrades), TEST-R1 (BDD cycle constraint upgrade), and 3 additional priority pattern upgrades identified in TASK-013.
**Contingency:** All pattern catalog changes are additive; reversible by removing added sections.

---

**R-009: Add Creation Constraint Block to EPIC.md (Stage 4)**

**Priority:** MUST (HIGH) — EPIC.md currently has zero negative constraint language; highest gap severity
**Evidence:** T1+T3 (PG-001); T4 (WTI-007 pattern); WT-REC-001
**Action:** Add an NPT-011 justified prohibition creation constraint block to EPIC.md immediately after frontmatter. See TASK-014 WT-REC-001 for exact text. Include: MUST NOT create from memory (WTI-007), MUST NOT mark DONE without child completion (WTI-002), and a "Why" justification explaining that EPIC errors cascade to all children.
**EPIC.md priority:** EPIC is the highest-level entity; a malformed EPIC produces cascading errors to all child features, stories, and tasks. Zero constraint guidance at creation time is the highest-severity template gap in the system.

---

### Priority: Post-Phase 2 (Experimental Outcome-Dependent)

---

**R-010: Execute Phase 2 Experimental Pilot (Stage 5)**

**Priority:** MUST (FOUNDATIONAL) — all UNTESTED claims depend on this
**Evidence:** Required by research design; UNTESTED hypothesis
**Action:** Execute the n=30 pilot (go/no-go criteria in Section 7) followed by the n=270 full experiment across conditions C1–C7 including the C7 post-compaction condition. Use automated evaluation metrics as primary outcome measure. Report results stratified by condition (not collapsed), including C7 separately for compaction-aware analysis.
**Independent of outcome:** The research is valuable regardless of whether Phase 2 finds positive, null, or negative effect for structured negative prompting vs. positive equivalents.

---

**R-011: Implement Phase 2-Conditional Changes Based on Verdict (Stage 6)**

**Priority:** SHOULD (DEPENDENT) — conditional on Phase 2 outcome; override by omitting if Phase 2 null finding per PG-003
**Evidence:** Phase 2 experimental results
**Action (if structured negative > positive):** Implement ADR-002 Phase 5B (agent forbidden_actions upgrade) and ADR-003 Component B (routing prohibition MUST NOT framing). Apply remaining Group 2 (SHOULD add) recommendations from Phase 4 analysis.
**Action (if null finding):** Apply PG-003 contingency plan (Section 8). Retain Stage 1–4 changes. Do not implement Stage 6 framing changes. Update AGREE-5 hierarchy to mark ranks 9–11 as "equivalent" zone.
**Action (if structured positive > negative):** Revert Stages 1–4 framing changes. Update all practitioner guidance. Document as major research finding.

---

**R-012: Develop Supplemental Governance for Pattern Catalog and Template Coverage Gaps**

**Priority:** MAY (LOW-MEDIUM) — coverage gaps do not block the ADR portfolio
**Evidence:** KF-014 (two coverage gaps identified)
**Action:** Create two supplemental governance documents: (1) a pattern catalog negative constraint standard governing the 28 "SHOULD add" recommendations from TASK-013 that have no dedicated ADR; (2) a template constraint standard governing the 5 template recommendations from TASK-014 not covered by ADR-001 through ADR-004.
**Timing:** After Stage 6 Phase 2 verdict; the content of these standards depends on Phase 2 outcome for framing preference.

---

## Source Summary

| Source | Type | Key Contribution | Patterns/Findings |
|--------|------|-----------------|-------------------|
| `barrier-1/synthesis.md` (R4, 0.953) | Phase 1 research synthesis | 75 unique sources; AGREE-5 hierarchy; null finding on 60% claim; 9 cross-survey agreements | KF-001, KF-002, KF-008 |
| `barrier-1/supplemental-vendor-evidence.md` (R4, 0.951) | Vendor evidence | VS-001–VS-004 (33-instance catalog); IG-002 taxonomy; A/B design parameters; EO-001–EO-003 | KF-004, KF-009, Section 7 |
| `phase-2/claim-validation.md` (R4, 0.959) | Claim analysis | Null finding on 60%; research question bifurcation; pilot go/no-go criteria | KF-001, KF-006 |
| `phase-2/comparative-effectiveness.md` (R5, 0.933) | Effectiveness analysis | A-23 confirmation (T1, +25.14% negation accuracy); 5-dimension analysis; D5 HIGH vendor adoption | KF-007, Section 1 |
| `barrier-2/synthesis.md` (v3.0.0, 0.953) | Research synthesis | PG-001–PG-005; confidence tier framework; ST-5 Phase 4 constraints | Section 1, Section 8 |
| `phase-3/taxonomy-pattern-catalog.md` (v3.0.0, 0.957) | Taxonomy | NPT-001 through NPT-014; 13 distinct techniques; IG-002 cross-reference | Section 4, KF-008 |
| `phase-4/skills-update-analysis.md` (v2.0.0, 0.951) | Skills audit | 37 recommendations; 3-tier maturity classification; NPT-012 exclusion from SKILL.md | KF-010, KF-013 |
| `phase-4/agents-update-analysis.md` (v3.0.0, 0.951) | Agents audit | 32 recommendations; 9 families; GAP-001–GAP-005 in H-34/H-35 | KF-010, KF-013 |
| `phase-4/rules-update-analysis.md` (0.953) | Rules audit | 36 instances cataloged; 22 NPT-014 (61%); L2 token budget analysis | KF-003, KF-005 |
| `phase-4/patterns-update-analysis.md` (v5.0.0, 0.950) | Patterns audit | 34 recommendations; A-11 hallucination discovery and removal; methodology scope ceiling 0.84 | KF-012, KF-010 |
| `phase-4/templates-update-analysis.md` (v3.0.0, 0.955) | Templates audit | 13 recommendations; rules-template separation finding; EPIC.md zero constraint gap | KF-014, R-009 |
| `barrier-4/synthesis.md` (v4.0.0, 0.950) | Phase 4 synthesis | 130 total recommendations; 6 cross-cutting themes; dependency map; A-11 citation resolution | KF-010, KF-011, KF-012 |
| `phase-5/ADR-001-npt014-elimination.md` (0.952) | ADR | Universal NPT-014 elimination policy (PROPOSED) | Section 5, R-002 |
| `phase-5/ADR-002-constitutional-upgrades.md` (v2.1.0, 0.951) | ADR | Constitutional constraint upgrade policy (PROPOSED) | Section 5, R-005, R-006 |
| `phase-5/ADR-003-routing-disambiguation.md` (v1.3.0, 0.957) | ADR | Routing disambiguation standard (PROPOSED) | Section 5, R-007 |
| `phase-5/ADR-004-compaction-resilience.md` (v2.1.0, 0.955) | ADR | Compaction resilience policy (PROPOSED) | Section 5, R-003, R-004 |
| `barrier-5/synthesis.md` (v1.1.0, 0.956) | ADR synthesis | 6-stage implementation ordering; CX-A-001–CX-A-013; CX-R-001–CX-R-008 | Section 6, Section 9 |

---

## Constitutional Compliance Checklist

**Self-review per H-15 before completion:**

### Evidence Citation Discipline (NEVER Violations)

- [x] NEVER cited A-11 — confirmed absent from all sections
- [x] NEVER cited AGREE-5 as T1 or T3 — all AGREE-5 references include "(internally generated synthesis narrative, NOT externally validated)"
- [x] NEVER claimed 60% hallucination reduction validated — Claim A verdict: UNTESTED, NULL FINDING
- [x] NEVER conflated VS-001 vendor self-practice with controlled experimental evidence — VS-001 labeled T4 observational throughout
- [x] NEVER treated absence of evidence as evidence of absence — SE-1 criterion applied (KF-001 and Section 2)
- [x] NEVER presented NPT-009/NPT-010/NPT-011 as experimentally superior to positive equivalents — all labeled UNTESTED causal comparison

### Structural Compliance

- [x] P-002 (file persistence): Synthesis persisted to `phase-6/final-synthesis.md`
- [x] P-003 (no recursive subagents): This agent is a worker; no Task tool invocations
- [x] P-004 (provenance): All patterns cite contributing source documents
- [x] P-011 (evidence-based): All themes grounded in source evidence with tier labels
- [x] P-022 (no deception): Contradictions and tensions disclosed (Sections 1, 2, 8)
- [x] H-23 (navigation table): Present at document start
- [x] L0/L1/L2 output levels: Present (Executive Summary, Technical Synthesis, Strategic Synthesis) — `## L2: Strategic Synthesis` heading added in I2 revision (was missing in v1.0.0 despite being declared in navigation table)
- [x] Source summary table: Present (Source Summary section)

### Orchestration Directive Compliance

- [x] Directive 1: All constraint framing uses NEVER/MUST NOT (no positive prompting in constraint expressions)
- [x] Directive 2: Supplemental vendor evidence included (VS-001 through VS-004 throughout)
- [x] Directive 3: Practitioner evidence not dismissed — T4 labeled as valid category throughout
- [x] Directive 4: Absence of published evidence not treated as evidence of absence
- [x] Directive 5: Enforcement tier vocabulary not presented as experimentally validated
- [x] Directive 6: No changes recommended that would make Phase 2 conditions unreproducible (Stage 0 is mandatory prerequisite)
- [x] Directive 7: PG-003 contingency explicitly addressed (Section 8)

---

*Final Synthesis Version: 1.1.0 (I2 revision)*
*I2 changes: (1) Added `## L2: Strategic Synthesis` heading; (2) Mapped R-001–R-012 priority labels to MUST/SHOULD/MAY framework vocabulary; (3) Added evidence tier distribution table to Section 2; (4) Added ADR approval process subsection to Section 5.*
*PROJ-014 Negative Prompting Research — Phase 6 Deliverable*
*Research Pipeline Complete Through Phase 5*
*Phase 2 Experimental Design Ready for Execution (Section 7)*
*Next Action: R-001 (Stage 0 baseline capture) — PREREQUISITE for all implementation*
