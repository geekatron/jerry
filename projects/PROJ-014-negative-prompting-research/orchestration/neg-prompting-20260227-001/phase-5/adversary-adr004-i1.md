# Quality Score Report: ADR-004 Compaction Resilience (I1)

## L0 Executive Summary

**Score:** 0.874/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.85)

**One-line assessment:** ADR-004 is a strong, well-evidenced engineering document that falls short of the C4 threshold (0.95) primarily due to an unformalized option-scoring rubric, a partially actionable testing requirement, and a minor completeness gap in PG-004 test automation specificity — targeted revisions to these three areas should close the gap.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-004-compaction-resilience.md`
- **Deliverable Type:** ADR
- **Criticality Level:** C4
- **Quality Threshold:** 0.95 (C4)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** I1 (first scoring)
- **Scored:** 2026-02-28

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.874 |
| **Threshold** | 0.95 (C4) |
| **Gap to Threshold** | 0.076 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |

---

## Gate Check Results (ADR-Specific)

| Gate | Description | Result | Notes |
|------|-------------|--------|-------|
| GC-ADR-1 | Nygard format compliance | PASS | All Nygard elements present; extended with L0/L1/L2 sections (additive, not violations) |
| GC-ADR-2 | Evidence tier labels on all claims | PASS | 11 evidence entries with explicit tier labels; EO-001 correctly labeled T5 |
| GC-ADR-3 | PG-003 reversibility assessment present | PASS | Dedicated section with per-decision-component table |
| GC-ADR-4 | Phase 2 dependency correctly handled | PASS | Unconditional/conditional distinction maintained consistently throughout |
| GC-ADR-5 | No false validation claims | PASS | GC-P4-1 compliance verified; all evidence labeled T4 or T5; A-11 explicitly excluded |
| GC-ADR-8 | Token budget arithmetic verified | PASS | 670+35+40=745; 850-745=105 headroom; 559+35+40=634; 634/850=74.6% — all arithmetic verified |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 3 decisions fully addressed with implementation detail; minor gap: PG-004 test specificity deliberately deferred |
| Internal Consistency | 0.20 | 0.90 | 0.180 | No contradictions found; 559/670 discrepancy consistently tracked across both scenarios; before/after headroom clearly distinguished |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | S-003/S-004 applied rigorously; option comparison scoring (A=6, B=8, C=7, D=3) asserted without documented weighting criteria |
| Evidence Quality | 0.15 | 0.85 | 0.1275 | Evidence tier discipline strong; T4 observational basis appropriate for engineering claims; no T1/T2 controlled evidence (acknowledged) |
| Actionability | 0.15 | 0.87 | 0.1305 | Exact marker content provided; 6-step implementation sequence; PG-004 testing actionability limited by deferred automation path |
| Traceability | 0.10 | 0.90 | 0.090 | Full evidence-to-decision chain; constraint IDs tracked throughout; Related Decisions table with status |
| **TOTAL** | **1.00** | | **0.874** | |

---

## H-15 Arithmetic Verification

Step-by-step summation:

| Step | Calculation | Running Total |
|------|-------------|---------------|
| 1 | Completeness: 0.88 × 0.20 | 0.176 |
| 2 | Internal Consistency: 0.90 × 0.20 | +0.180 = 0.356 |
| 3 | Methodological Rigor: 0.85 × 0.20 | +0.170 = 0.526 |
| 4 | Evidence Quality: 0.85 × 0.15 | +0.1275 = 0.6535 |
| 5 | Actionability: 0.87 × 0.15 | +0.1305 = 0.784 |
| 6 | Traceability: 0.90 × 0.10 | +0.090 = 0.874 |

**Verified composite: 0.874** — matches the Score Summary table exactly.

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

All three required deliverables from the TASK-016 specification are fully addressed:
- Decision 1 (PG-004 testing requirement): Coverage extends to 5 artifact types, per-artifact vulnerability/test-condition/pass-criterion table, and U-003 alignment.
- Decision 2 (NPT-012 L2-REINJECT for H-04, H-32): Failure-window comparison table for all 5 Tier B rules, exact marker HTML content, placement file, rank, token arithmetic (both baseline and worst-case), and a 6-step implementation sequence.
- Decision 3 (T-004 failure mode documentation): Template section format with column definitions, enumeration of applicable template categories, and retrofit scope (new/modified only).

Nygard-required sections: Status, Context, Options (4 evaluated), Decision, Consequences (positive/negative/neutral), Risks (5 entries with P/S/M), Compliance, Related Decisions — all present.

**Gaps:**

1. PG-004 test automation specificity: The decision on testing requirements explicitly defers "specific test methodology, pass/fail thresholds, or test automation approach" to Phase 2. This is a justified deferral (U-003 conditions PG-004 on Phase 2 pilot design), but it means Decision 1 is incomplete as an actionable engineering specification. A reader tasked with implementing PG-004 testing has the structure but not the minimum viable test protocol for the interim period before Phase 2 completes. The risk of "documented-but-unenforced" (R-002) is a direct consequence of this gap.

2. Decision 2 implementation step 1 ("Resolve the 559 vs. ~670 token discrepancy by exact counting") is a blocking prerequisite that is not itself specified — no one is assigned to perform the count, no deadline is set, and no mechanism ensures it happens before implementation begins.

**Improvement Path:**
- Add a minimal interim PG-004 test protocol (even a 3-step manual procedure) that implementers can follow before Phase 2 automation is available.
- Add an owner or trigger condition for the token discrepancy resolution step (e.g., "This ADR implementation is blocked until the token count is performed and updated here.").

---

### Internal Consistency (0.90/1.00)

**Evidence:**

The 559 vs. 670 token discrepancy is tracked consistently across all appearances: Forces section presents both figures as a range ("559-670 tokens, ~180-291 tokens of headroom"), Decision 2 arithmetic presents both scenarios, Consequences presents only the worst-case (correct for conservative planning), and the blocking dependency is called out in both the implementation sequence and the Negative Consequences section. No scenario conflates the two figures.

The before/after headroom distinction is maintained: Forces describes current headroom (pre-additions), L2 Implications describes post-implementation headroom. A careful reader can track the state transition.

The unconditional/conditional framing is applied consistently: PG-004 labeled "unconditional" in the L0, Context, Decision 1, PG-003 table, Self-Review. H-04/H-32 mechanism labeled "unconditional," vocabulary labeled "conditional." T-004 documentation labeled "unconditional." No instance reverses these labels.

HARD rule ceiling assertion ("25/25 unchanged," "no new HARD rules proposed") is consistent with the implementation steps, which modify existing entries rather than adding new rules.

**Gaps:**

The option comparison table assigns an overall "Score" of 8 to Option B, 7 to Option C, 6 to Option A, 3 to D. The Forces section establishes 5 forces with no numeric weighting. The connection between the force analysis and the option scores is implicit, not derived. While this is not a contradiction (the scores could be correct), the lack of a visible derivation creates a potential internal consistency concern: a reader cannot verify that the scores follow from the forces analysis.

**Improvement Path:**
- Provide the weighting logic behind the option comparison scores, or replace the opaque scores with a force-by-force option evaluation table.

---

### Methodological Rigor (0.85/1.00)

**Evidence:**

Strengths are substantial:
- S-003 (Steelman) applied to all 4 options before dismissal. Each steelman identifies the strongest version of the argument, not a straw man.
- S-004 (Pre-Mortem) with 3 failure scenarios: compaction never occurs (medium probability), budget exhaustion blocks future rules (low), Phase 2 finds negative vocabulary harms compliance (low). Each includes probability, consequence, and why-still-acceptable analysis.
- Failure window analysis for Tier B rules is structured as a comparative table with explicit failure-window characterization ("Window = entire session" for H-04 and H-32 vs. "Window = narrow" for H-16/H-17/H-18). This is the key methodological support for the selective-2-of-5 decision.
- Evidence tier discipline: every claim cites a source with tier label and confidence rating.
- The unconditional-vs-conditional logic is a methodological contribution — it cleanly separates decisions that can proceed from those that await Phase 2 data.

**Gaps:**

The most significant methodological gap is the option comparison score assignment. The table shows:

```
A: Token cost 150-250, Tier B 5/5, Budget risk HIGH → Score 6
B: Token cost 60-100, Tier B 2/5, Budget risk LOW  → Score 8
C: Token cost 0,     Tier B 0/5, Budget risk NONE  → Score 7
D: Token cost 0,     Tier B 0/5, Budget risk NONE  → Score 3
```

Option C scores 7 while Option A scores 6, implying C is superior to A despite A closing 5/5 Tier B rules vs. C's 0/5. This ranking may be correct given budget risk weighting, but the scoring methodology is not explained. For a C4 ADR, the evaluation methodology must be explicit enough that a second reviewer could reproduce the scores from the stated evidence. The current table does not meet this bar.

Secondary gap: The per-artifact-type test conditions table assigns vulnerability levels (LOW, MEDIUM, LOW-MEDIUM) without a documented assessment framework. The assessments appear reasonable but are asserted rather than derived.

**Improvement Path:**
- Replace the unexplained summary score with a weighted-criteria table: list the evaluation dimensions (token cost, Tier B coverage, budget risk, reversibility, evidence basis), assign weights, score each option on each dimension, derive the summary score from the arithmetic.
- Document the vulnerability assessment framework for the per-artifact table (e.g., "MEDIUM = L1-loaded, no L2 protection, no Tier 2 isolation").

---

### Evidence Quality (0.85/1.00)

**Evidence:**

Positive:
- 11 evidence entries in the Evidence Summary with explicit tier labels and confidence levels. No entry is missing a label.
- T5 evidence (EO-001: "L2 re-injection observed as primary enforcement mechanism in single session") is correctly labeled T5 and described as "LOW (session observation)" — not inflated to T4.
- A-11 is confirmed absent. The "NEVER cite A-11" warning is included in the Evidence Summary, providing an audit trail for the constraint.
- Cross-analysis convergence (GAP-X2: 4 of 5 Phase 4 analyses identified T-004) is a legitimate methodological convergence claim, not an authority claim.
- VS-003 cited for vocabulary choice at "HIGH observational" — this is consistent with T4 direct observation tier.
- The T-004 failure mode is correctly characterized as T4 LOW for "directional reversal" while being "unconditional by failure mode logic" — this distinction is precise and not inflated.

**Gaps:**

1. TASK-012 Finding 3 is labeled "T4 (observational, verified by audit)" with HIGH confidence for budget arithmetic. The "verified by audit" claim is stronger than T4 observational alone — but the ADR then notes the 559 vs. 670 discrepancy and states the exact count "MUST be resolved before implementation." This partially undercuts the HIGH confidence claim: if the audit produced a discrepancy range rather than an exact figure, the arithmetic evidence quality is MEDIUM-HIGH, not HIGH. The confidence label for TASK-012 F3 is slightly over-rated.

2. The "T4 unconditional by failure mode logic" classification for PG-004 is methodologically unusual. PG-004 is presented as a practitioner guidance item elevated to unconditional status by a logical argument, not an evidence tier per se. This blending of evidence tier and reasoning tier is non-standard and could confuse downstream consumers of the evidence table.

**Improvement Path:**
- Downgrade TASK-012 F3 confidence from HIGH to MEDIUM-HIGH for budget arithmetic pending discrepancy resolution, or add a parenthetical note: "HIGH for structural finding, MEDIUM for exact figures."
- Clarify the PG-004 evidence classification: the unconditional nature is a logical property, not an evidence tier. Separate the evidence (T-004: T4 LOW) from the reasoning (unconditional by failure mode logic: logical inference, not an evidence tier).

---

### Actionability (0.87/1.00)

**Evidence:**

Decision 2 implementation is highly actionable:
- Exact H-04 marker text: `<!-- L2-REINJECT: rank=11, content="Active project REQUIRED (H-04)..." -->`
- Exact H-32 marker text: `<!-- L2-REINJECT: rank=12, content="GitHub Issue parity REQUIRED..." -->`
- Placement: quality-enforcement.md (H-04) and project-workflow.md (H-32)
- 6-step implementation sequence with update instructions for Tier A/B counts

Decision 3 (T-004 documentation) provides an actionable template section format and enumerates applicable template categories.

Risks table provides concrete mitigations (R-001: resolve discrepancy first; R-002: integrate into Phase 2 pilot; R-003: include in review checklist; R-004: track DEC-005; R-005: test across models).

**Gaps:**

Decision 1 (PG-004 testing) actionability is the weakest of the three. The ADR specifies what to test (5 artifact types) and what the pass criterion is in general terms, but does not specify:
- Who performs the tests (role assignment absent)
- When tests must be completed relative to the ADR implementation
- What the minimum viable manual test procedure looks like before Phase 2 automation is built
- How test results are documented and where they are stored

A CI engineer reading this ADR to implement PG-004 would need significant interpretation work. The ADR itself acknowledges: "until automated tooling is available, these tests require manual execution, which is time-consuming and may not be performed consistently" (Negative Consequence 2). The risk is well-documented but the mitigation (R-002: integrate into Phase 2 pilot) defers the problem rather than providing an interim solution.

The blocking dependency for Decision 2 (resolve token discrepancy) is identified but has no owner, deadline, or mechanism.

**Improvement Path:**
- For Decision 1: Add a "Minimum Viable Test Protocol" subsection with a 3-5 step manual test procedure that a practitioner can execute immediately, even if it is eventually superseded by automation.
- For Decision 2 blocking dependency: Add an explicit gate: "Implementation of Decision 2 is BLOCKED pending completion of [exact-count task]. Owner: [role]. Output: Updated token table in this ADR."

---

### Traceability (0.90/1.00)

**Evidence:**

The evidence-to-decision chain is explicit and verifiable:
- T-004 -> all three decisions (explicitly cited in each decision's evidence basis)
- TASK-012 F3 -> Decision 2 token arithmetic
- TASK-014 WT-GAP-005 -> Decision 3
- GAP-X2 (4/5 Phase 4 convergence) -> motivates all three decisions
- barrier-2/synthesis.md ST-3 (U-003) -> Decision 1 test integration requirement

Related Decisions table traces lateral relationships to ADR-001, ADR-002, ADR-003, DEC-005, quality-enforcement.md Two-Tier Enforcement Model, and AE-006. Each entry specifies the relationship type (co-developed, open pending, to-be-updated).

Constraint ID tracking: GC-P4-1, GC-P4-2, GC-P4-3, U-003, C-NCA, C-EXP, C-T5T4, C-FRM, C-ARCH all resolved in the Compliance section.

Self-review checklist references specific strategy IDs (S-003, S-002, S-004) and evidence IDs (A-11 absent confirmation).

**Gaps:**

The "rank=11" and "rank=12" assignments for the new L2 markers are stated without tracing to a priority justification. The document says "lower priority than architectural and quality rules" for rank=11 and "lowest priority; scoped to jerry repository only" for rank=12. These are informal justifications, not a documented priority derivation. For C4, the ranking decision should be traceable to a documented ranking framework (e.g., cite quality-enforcement.md's existing rank ordering and explain where H-04 and H-32 fit relative to existing ranks 1-10).

**Improvement Path:**
- Add a paragraph or table showing the existing L2-REINJECT rank assignments (1-10) and justify rank=11 and rank=12 relative to existing content by priority criteria (e.g., "H-04 at rank=11 because it is a session-scoping constraint with lower operational frequency than L2 markers for quality thresholds at rank=2").

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.85 | 0.91 | Replace the opaque option comparison scores (A=6, B=8, C=7, D=3) with a weighted-criteria evaluation table. List dimensions (token cost, Tier B coverage, budget risk, reversibility, evidence basis), assign weights, compute scores derivatively. A reviewer must be able to reproduce the ranking from the arithmetic. |
| 2 | Completeness | 0.88 | 0.93 | Add a "Minimum Viable Manual Test Protocol" subsection under Decision 1 Implementation: a 3-5 step procedure that implementers can follow before Phase 2 automation exists. The per-artifact test conditions table is a what; the MVP protocol is the how. |
| 3 | Actionability | 0.87 | 0.92 | Add an explicit implementation gate for the token discrepancy blocking dependency: "Decision 2 implementation is BLOCKED until an exact token count is performed and this section is updated with the exact figure. Owner: [role]. Mechanism: Read all L2-REINJECT marker content and count tokens with a known tokenizer." |
| 4 | Methodological Rigor | 0.85 | 0.91 | Add a vulnerability assessment framework for the per-artifact-type test conditions table. Define what LOW/MEDIUM/LOW-MEDIUM mean in terms of enforcement layer and failure probability, rather than asserting the levels. |
| 5 | Evidence Quality | 0.85 | 0.89 | Revise TASK-012 F3 confidence from "HIGH for budget arithmetic" to "MEDIUM-HIGH pending exact count resolution," or add a parenthetical qualifier. Separately, clarify that PG-004's "unconditional" status is a logical inference property, not an evidence tier — consider moving it out of the tier column or adding a footnote. |
| 6 | Traceability | 0.90 | 0.93 | Add a rank-justification sentence for L2-REINJECT rank=11 and rank=12 assignments, citing the existing rank 1-10 priority ordering for context. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computation
- [x] Evidence documented for each score — specific sections and quotes cited
- [x] Uncertain scores resolved downward: Methodological Rigor anchored at 0.85 (not 0.87 or 0.88) due to unformalized option scoring; Evidence Quality anchored at 0.85 (not 0.87) due to over-rated TASK-012 F3 confidence
- [x] First-draft calibration: this is I1; the 0.874 composite is consistent with a strong first draft of a C4 ADR (well-researched, structured, evidence-disciplined, but with methodological and actionability gaps typical of first-iteration C4 work)
- [x] No dimension scored above 0.92 — highest is Internal Consistency and Traceability at 0.90
- [x] Score gap from C4 threshold: 0.874 vs 0.95 = 0.076 deficit — requires substantive improvements, not cosmetic edits

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.874
threshold: 0.95
weakest_dimension: Methodological Rigor
weakest_score: 0.85
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Replace option comparison summary scores (A=6/B=8/C=7/D=3) with a weighted-criteria derived table"
  - "Add Minimum Viable Manual Test Protocol for PG-004 (3-5 steps) usable before Phase 2 automation"
  - "Add explicit implementation gate for 559/670 token discrepancy resolution with owner and mechanism"
  - "Document vulnerability assessment framework for per-artifact-type test conditions (LOW/MEDIUM/LOW-MEDIUM)"
  - "Revise TASK-012 F3 evidence confidence from HIGH to MEDIUM-HIGH pending exact count; clarify PG-004 unconditional classification"
  - "Add rank justification for L2-REINJECT rank=11 and rank=12 relative to existing rank 1-10"
```

---

*Scorer: adv-scorer | Strategy: S-014 LLM-as-Judge | SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-02-28 | Iteration: I1 | Deliverable: ADR-004-compaction-resilience.md*
