# Quality Score Report: TASK-014 Templates Update Analysis (I2)

## L0 Executive Summary

**Score:** 0.940/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness / Internal Consistency (tied, 0.93)
**One-line assessment:** Substantial revision from I1 (0.887 -> 0.940) — all six I1 improvement recommendations and all three new findings (NF-001, NF-002, NF-003) are fully resolved; the deliverable falls 0.010 short of the 0.95 C4 threshold due to one residual minor inconsistency (DT-REC-001/DT-REC-002 omitted from Phase 5 reversibility statement) and the inherent TDD.template.md content gap that cannot be closed without a Phase 5 tool call.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-4/templates-update-analysis.md`
- **Deliverable Type:** Framework Application Analysis (Phase 4 sub-task)
- **Criticality Level:** C4
- **Quality Threshold:** 0.95 (orchestration directive, C4)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-02-28T00:00:00Z
- **Iteration:** I2 (second scoring pass, post-revision)
- **Prior Score:** I1 = 0.887 (REVISE)
- **I1 Gaps Declared Fixed:** 9 (FEATURE.md scope+analysis, E-014 forward trace, ST-5 citations, DT-REC-003 procedure, ENABLER.md template text, NF-001 resolution, NF-002 citation, NF-003 ST-5 references, priority derivation rubric)

---

## Phase 4 Gate Check Results

| Gate | Requirement | Verdict | Evidence |
|------|-------------|---------|----------|
| **GC-P4-1** | Artifact does NOT claim enforcement tier vocabulary is experimentally validated | **PASS** | Cross-Template Pattern 3 retains the "MANDATORY EPISTEMIC CAVEAT (Barrier 2 constraint ST-5, Constraint 3)" block (line 450). Language is unambiguous: "The claim that the HARD/MEDIUM/SOFT tier vocabulary is superior to positive alternatives due to vocabulary choice itself is NOT experimentally validated... The causal contribution of MUST NOT vs. MUST to behavioral compliance is UNTESTED pending Phase 2 experimental design." The mandatory epistemic note in L0 is unchanged and continues to label PG-003 as "T4 observational only." Gate compliant. |
| **GC-P4-2** | Recommendations do NOT make Phase 2 experimental conditions unreproducible | **PASS** | Phase 5 Input 2 now includes explicit ST-5 Constraint citations on each prohibition: "(ST-5, Constraint 1; `barrier-2/synthesis.md`)", "(ST-5, Constraint 2; `barrier-2/synthesis.md`)", "(ST-5, Constraint 3; `barrier-2/synthesis.md`)". All HIGH priority recommendations (WT-REC-001, WT-REC-004, REQ-REC-001) target template addition — new constraint blocks added to templates — not modification of enforcement vocabulary or mechanisms. Gate compliant. |
| **GC-P4-3** | PG-003 contingency path documented with explicit reversibility plan | **PASS** | PG-003 Contingency Plan section is unchanged from I1 and was already compliant. Trigger condition (Phase 2 C4 vs C5 comparison, p > 0.05 McNemar test) is defined. Consequence behavior (downgrade NPT-011 priority to OPTIONAL, retain as style improvements) is stated. Five recommendations NOT affected by the contingency are enumerated. Reversibility chain: "NPT-011 additions can be cleanly reverted to NPT-009 if Phase 2 finds null framing effects." Gate compliant. |

**Gate Check Summary:** All three gates PASS. No gate-based automatic REVISE override triggered. Score-based verdict (REVISE, 0.940 < 0.95) governs.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.940 |
| **Threshold** | 0.95 (C4, orchestration directive) |
| **Verdict** | REVISE |
| **I1 Composite** | 0.887 |
| **Score Delta** | +0.053 |
| **Strategy Findings Incorporated** | No (no prior adv-executor report available) |

---

## Dimension Scores

| Dimension | Weight | I1 Score | I2 Score | Weighted | Evidence Summary |
|-----------|--------|----------|----------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.93 | 0.186 | FEATURE.md fully resolved via scope note + E-009-F entry; TDD gap remains as acknowledged tool limitation with forward trace |
| Internal Consistency | 0.20 | 0.88 | 0.93 | 0.186 | FEATURE.md inconsistency and reversibility claim both resolved; minor residual: DT-REC-001/DT-REC-002 omitted from Phase 5 Input 2 reversibility scope |
| Methodological Rigor | 0.20 | 0.93 | 0.96 | 0.192 | AGREE-5 rank anchor table added (lines 65-82); priority derivation criteria added (lines 83-91); both I1 gaps fully resolved |
| Evidence Quality | 0.15 | 0.91 | 0.94 | 0.141 | E-016 added for Architectural Finding 2 operational consequence claim (NF-002 resolved); VS-003 evidence tier labeling consistent in summary table |
| Actionability | 0.15 | 0.88 | 0.94 | 0.141 | DT-REC-003 now has concrete 4-step chunked Read procedure with line counts; ENABLER.md-specific template text block added to WT-REC-002 |
| Traceability | 0.10 | 0.80 | 0.94 | 0.094 | All three I1 traceability gaps resolved: E-014 forward trace, FEATURE.md traceability chain, ST-5 Constraint citations on all three MUST NOT prohibitions |
| **TOTAL** | **1.00** | **0.887** | | **0.940** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**I1 gap — FEATURE.md missing from analysis. Status: FULLY RESOLVED.**
- Methodology "FEATURE.md Scope Note" section (lines 53-55) explicitly addresses the omission: FEATURE.md exhibits the identical structural pattern as TASK.md and BUG.md; consolidation under shared gaps is documented and justified.
- FEATURE.md appears in the MUST NOT inventory table (line 202) with E-009-F as its evidence reference.
- WT-GAP-002 now explicitly names FEATURE.md as one of the four affected templates.
- WT-REC-002 covers FEATURE.md with both the shared template block and the statement "The same block applies to all four templates."
- E-009-F is added to the Evidence Summary (line 577): "NPT-008 (contrastive BAD/GOOD) present; no NPT-009 declarative constraint; no creation constraint block — identical pattern to TASK.md and BUG.md."

**Residual gap: TDD.template.md analysis incomplete.**
This is an inherent tool limitation, not a writing gap. The analysis correctly:
- Acknowledges TDD as "BLOCKED" in Phase 5 Input 1 priority table.
- Provides a concrete forward trace via Phase 5 Input 3 and DT-REC-003.
- Notes explicitly: "this is a distinct task from the reversible template changes — TDD.template.md has no changes proposed."
The completeness score is capped at 0.93 because the primary design documentation template (by the analysis's own description) remains unanalyzed. This is correctly documented and fully acknowledged, which limits the penalty, but the content gap is real.

**Evidence supporting 0.93:**
All 4 required template families are now consistently represented in scope, analysis body, gap inventory, and recommendations. The per-family gap inventory (4+5+3+3 = 15 gaps) is exhaustive for analyzed content. MUST NOT inventory tables demonstrate clause-level analysis. Cross-template L2 patterns are architecturally coherent.

**Gaps not fully addressable in this iteration:**
TDD.template.md analysis — requires Phase 5 tool execution. No writing improvement can resolve this.

**What would raise to 0.95+:**
Completing TDD.template.md analysis via chunked reads. Per the DT-REC-003 procedure, this requires approximately 3 Read tool calls. Not feasible within the current artifact; deferred to Phase 5.

---

### Internal Consistency (0.93/1.00)

**I1 gap — Reversibility scope tension. Status: FULLY RESOLVED.**
Phase 5 Input 2 (lines 519-527) now reads: "Recommended template changes in this analysis for **Worktracker, Adversarial, and Requirements families** are reversible within 1 day (C2 criticality)." The blanket "all changes" claim is replaced with explicit family scoping. The TDD BLOCKED qualification is added directly beneath (lines 521-522).

**I1 gap — FEATURE.md scope inconsistency. Status: FULLY RESOLVED.**
Methodology scope declaration, per-template analysis body, gap tables, recommendations, and evidence summary are now internally consistent regarding FEATURE.md. The scope note explicitly resolves the omission with a documented consolidation rationale.

**Residual inconsistency (new finding NF-I2-001 — Minor):**
Phase 5 Input 2 reversibility scoping ("Worktracker, Adversarial, and Requirements families") correctly excludes TDD.template.md. However, DT-REC-001 (PLAYBOOK.template.md — add consequence clause to STOP instruction) and DT-REC-002 (RUNBOOK.template.md — surface role-based contact constraint) are both concrete, LOW priority Design family recommendations that are also reversible within 1 day. The reversibility statement omits the Design family non-blocked recommendations. A Phase 5 implementer looking at DT-REC-001 or DT-REC-002 cannot confirm their criticality classification from Phase 5 Input 2.

**Why this warrants a score cap at 0.93 rather than 0.95:**
The inconsistency is minor — DT-REC-001/DT-REC-002 are LOW priority and the omission does not affect downstream decision-making significantly. But for a C4 deliverable where precise reversibility classification matters, the Design family non-blocked recommendations should be explicitly covered.

**What would raise to 0.95+:**
Add one sentence to Phase 5 Input 2: "Design family recommendations DT-REC-001 and DT-REC-002 (PLAYBOOK and RUNBOOK additions) are also reversible within 1 day (C2 criticality)."

---

### Methodological Rigor (0.96/1.00)

**I1 gap — Missing AGREE-5 rank anchor table. Status: FULLY RESOLVED.**
Lines 65-82 add a complete "AGREE-5 Rank Anchor Table" in the Methodology section. The table maps NPT-007 through NPT-014 to their AGREE-5 hierarchy ranks with pattern names and evidence tiers. The note at line 81 correctly flags the rank 9-11 cluster ordering as "T4-evidenced only; the specific effectiveness advantage of any one over another is UNVALIDATED pending Phase 2." This is methodologically precise.

**I1 gap — Priority derivation statement missing. Status: FULLY RESOLVED.**
Lines 83-91 add an explicit "Priority Derivation" section with four criteria:
1. HIGH: Zero constraints OR unconditional per PG-001/PG-002 (T1+T3, T1+T4)
2. MEDIUM: AGREE-5 rank reduction OR PG-003 conditional finding (T4)
3. LOW: Consequence clause addition to existing sound NPT-009 constraint
4. BLOCKED: Precondition unmet

This derivation is specific, independently verifiable, and aligns with the actual priority assignments throughout the analysis. Checking against WT-GAP-001 (HIGH — EPIC.md has zero constraints, criterion 1 applies), WT-GAP-002 (MEDIUM — NPT-008 to NPT-009 upgrade, criterion 2 applies), WT-GAP-003 (LOW — consequence clause to existing NPT-009, criterion 3 applies): all consistent.

**Why score does not reach 1.00:**
The AGREE-5 rank anchor table includes NPT-014 (anti-pattern) with "—" in the rank column. Including an anti-pattern in a rank effectiveness table without distinguishing it as a separate category could create confusion. This is a minor presentational ambiguity, not an analytical error.

**What would raise to ~0.97+:**
Move NPT-014 from the main rank table to a footnote or separate "Anti-Pattern Note" to clarify it is not an effectiveness tier but an avoidance category. Minor presentational fix.

---

### Evidence Quality (0.94/1.00)

**I1 gap — NF-002: Un-cited causal claim in Architectural Finding 2. Status: FULLY RESOLVED.**
Line 435 now reads: "Errors have immediate, observable consequences in production environments — outages, data loss, and service degradation manifest within the change window. STOP/ABORT framing is natural and expected. Operators under incident pressure have high motivation to read constraints. (T4: consistent with standard operational change management practice, E-016)"

E-016 is added to the Evidence Summary (line 584): "Domain context | Operational change management practice (T4, industry-standard) | Operational template errors (Playbook/Runbook) manifest immediately as production failures; cited in Architectural Finding 2 | T4, observational."

The evidence tier (T4, observational) is appropriate for this claim type and is labeled correctly.

**I1 improvement path item — VS-003 "(T4 observational)" in Cross-Template Pattern 3 body text.**
This was listed as an improvement path in I1 but was NOT listed as one of the 9 declared fixes. The Cross-Template Pattern 3 narrative (line 448) does not add an explicit "(T4 observational)" tag to the VS-003 usage in the body text. However, the comprehensive MANDATORY EPISTEMIC CAVEAT block (lines 450-451) immediately follows and addresses the evidential limitation of all claims in that section, including VS-003. This is a partial resolution: the evidence summary E-006 correctly labels VS-003 as "T4, observational," and the section-level caveat covers the claim, but the in-line citation in the sentence itself does not carry the tag. This is a minor residual gap.

**Evidence completeness:**
All 16 evidence items (E-001 through E-016, including new E-009-F and E-016) are in the Evidence Summary with type, source, claim supported, and tier. E-009-F distinguishes FEATURE.md as a separate evidence entry from E-009 (TASK.md/BUG.md/ENABLER.md), which is precise and correct.

**What would raise to 0.96+:**
Add "(T4, observational)" parenthetical to the VS-003 citation in the Cross-Template Pattern 3 body text (line 448 vicinity) to match the precision of the evidence summary table. One-word fix.

---

### Actionability (0.94/1.00)

**I1 gap — DT-REC-003 unblocking path too vague. Status: FULLY RESOLVED.**
Lines 337-344 add a concrete numbered unblocking procedure:
1. `Read(file_path="..../TDD.template.md", offset=0, limit=300)` — lines 1-300
2. `Read(file_path="..../TDD.template.md", offset=300, limit=300)` — lines 301-600
3. `Read(file_path="..../TDD.template.md", offset=600, limit=300)` — lines 601-900
4. Continue in 300-line increments until EOF

The estimated call count (3 Read calls based on 69.1KB ≈ 700-750 lines) is calculated explicitly. The fallback condition ("Continue in 300-line increments until EOF is reached") is defined. The note about the reversibility inapplicability of TDD.template.md is added at line 344.

**I1 gap — ENABLER.md template text missing from WT-REC-002. Status: FULLY RESOLVED.**
Lines 251-263 add an ENABLER.md-specific template text block with enabler-appropriate phrasing:
- "Acceptance Criteria MUST NOT be generic or reference implementation details that belong in child story tasks."
- Includes a BAD/GOOD contrast pair specific to enabler outcomes ("The enabler is implemented" vs. a specific authentication middleware integration test).

This is distinct from the TASK.md/BUG.md generic block (lines 243-249) and correctly reflects the different nature of enabler acceptance criteria.

**Phase 5 Input 3 forward trace (E-014):**
Lines 533-538 add a structured Phase 5 Task entry with mechanism, estimated effort, precondition, sequencing, and owner. This makes the TDD analysis gap actionable for Phase 5.

**Remaining gap (minor):**
The 13 numbered recommendations are all present and concrete. Each has NPT basis, evidence basis, priority, and target template. No material actionability gaps remain beyond the TDD tool limitation.

**What would raise to 0.96+:**
The actionability is very strong. The remaining gap is that DT-REC-001 and DT-REC-002 are not included in Phase 5 Input 2 reversibility scope (this overlaps with Internal Consistency), leaving a slight ambiguity about their criticality classification for Phase 5.

---

### Traceability (0.94/1.00)

**I1 gap — E-014 forward trace incomplete. Status: FULLY RESOLVED.**
Lines 533-538 add a dedicated "Phase 5 Task — TDD Analysis Completion (Forward trace from E-014)" section with five fields:
- Mechanism: Execute DT-REC-003 chunked Read procedure (cross-referenced)
- Estimated effort: 3 Read tool calls at 300 lines per call for ~750-line file
- Precondition: None — no dependencies
- Sequencing: MUST execute before any TDD.template.md modification
- Owner: Phase 5 ps-analyst agent, first task before template modification work

E-014 in the Evidence Summary (line 582) now explicitly states the forward trace: "forward trace: Phase 5 Input 3, DT-REC-003 chunked read procedure." The traceability chain from the gap to its resolution path is now complete.

**I1 gap — NF-001: FEATURE.md traceability gap. Status: FULLY RESOLVED.**
The Methodology "FEATURE.md Scope Note" (lines 53-55) provides the forward-and-backward traceability chain:
- Scope declaration includes FEATURE.md (line 49)
- Scope Note explains consolidation rationale (lines 53-55): "rather than duplicate the TASK.md analysis body, FEATURE.md is explicitly consolidated under those shared gaps"
- E-009-F added to evidence summary as direct evidence source
- WT-GAP-002 explicitly includes FEATURE.md in affected templates
- WT-REC-002 explicitly covers FEATURE.md
- WT-REC-004 coverage of FEATURE.md is confirmed with citation: "its NPT-008-only pattern (E-009-F) confirms the same gap exists as in TASK.md and BUG.md"

**I1 gap — NF-003: Missing ST-5 Constraint citations. Status: FULLY RESOLVED.**
Lines 525-527 now cite the originating constraint for each prohibition:
- "(ST-5, Constraint 1; `barrier-2/synthesis.md`)" on the HARD/MEDIUM/SOFT vocabulary prohibition
- "(ST-5, Constraint 2; `barrier-2/synthesis.md`)" on the L2-REINJECT mechanism prohibition
- "(ST-5, Constraint 3; `barrier-2/synthesis.md`)" on the WTI_RULES.md / entity template separation prohibition

This closes the traceability loop from Barrier 2 governance constraints to their Phase 4 implementation.

**Why score does not reach 0.97+:**
The traceability improvement is substantial. One minor residual gap: NF-I2-001 (DT-REC-001/DT-REC-002 omitted from Phase 5 Input 2 reversibility scope) leaves a small traceability gap for the Design family non-blocked recommendations. A Phase 5 implementer cannot trace the criticality classification of DT-REC-001/DT-REC-002 from Phase 5 Input 2.

**What would raise to 0.96+:**
Add explicit criticality trace for DT-REC-001 and DT-REC-002 in Phase 5 Input 2 (one sentence).

---

## I1 Gap Resolution Summary

| I1 Gap | Status | Resolution |
|--------|--------|------------|
| FEATURE.md missing from analysis | RESOLVED | Scope Note + E-009-F + WT-GAP-002 + WT-REC-002 + Evidence Summary entry |
| E-014 forward trace incomplete | RESOLVED | Phase 5 Input 3 task block with mechanism/effort/owner; E-014 summary updated |
| ST-5 citations missing | RESOLVED | All three MUST NOT prohibitions in Phase 5 Input 2 now cite "(ST-5, Constraint N; barrier-2/synthesis.md)" |
| DT-REC-003 unblocking path vague | RESOLVED | Concrete 4-step Read procedure with offset/limit values and estimated call count added |
| ENABLER.md template text missing from WT-REC-002 | RESOLVED | ENABLER.md-specific template block with enabler-appropriate phrasing added (lines 251-263) |
| NF-001: FEATURE.md scope coverage gap | RESOLVED | Per FEATURE.md gap above — full traceability chain established |
| NF-002: Un-cited Architectural Finding 2 claim | RESOLVED | E-016 added with T4, observational tier label; cited inline at line 435 |
| NF-003: Missing ST-5 source citations | RESOLVED | Per ST-5 citations above |
| Priority derivation rubric missing | RESOLVED | Priority Derivation section added to Methodology (lines 83-91) |

All 9 declared I1 fixes verified as complete. No partial resolutions.

---

## New Findings (I2)

**NF-I2-001 (Minor, Internal Consistency / Traceability):**
Phase 5 Input 2 reversibility statement (lines 519-527) scopes explicitly to "Worktracker, Adversarial, and Requirements families." This correctly excludes TDD.template.md (BLOCKED). However, DT-REC-001 (PLAYBOOK.template.md — add consequence clause) and DT-REC-002 (RUNBOOK.template.md — surface role-based contact constraint) are concrete LOW-priority Design family recommendations that are also reversible within 1 day (C2 criticality: adding text to an existing template section). A Phase 5 implementer cannot determine the criticality classification for these two recommendations from Phase 5 Input 2.

**Fix:** Add one sentence to Phase 5 Input 2 after the existing scope statement: "Design family recommendations DT-REC-001 (PLAYBOOK.template.md) and DT-REC-002 (RUNBOOK.template.md) are also reversible within 1 day (C2 criticality); only DT-REC-003 (TDD.template.md) is excluded from the reversibility assessment per the BLOCKED status above."

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency + Traceability | 0.93 / 0.94 | 0.95 | Add one sentence to Phase 5 Input 2 covering DT-REC-001/DT-REC-002 reversibility scope (NF-I2-001). Resolves the residual omission at both internal consistency and traceability levels. Estimated 30-word addition. |
| 2 | Evidence Quality | 0.94 | 0.96 | Add "(T4, observational)" parenthetical to the VS-003 inline usage in Cross-Template Pattern 3 body text (line ~448). Matches the precision of the Evidence Summary E-006 label. One-word fix. |
| 3 | Methodological Rigor | 0.96 | 0.97 | Move NPT-014 from the main AGREE-5 rank anchor table to a footnote or separate "Anti-Pattern Note" below the table, making clear it is not an effectiveness tier. Eliminates potential confusion about where NPT-014 sits relative to ranked patterns. |
| 4 | Completeness | 0.93 | 0.97+ | Complete TDD.template.md analysis using DT-REC-003 chunked Read procedure (3 Read calls). This is a Phase 5 task, not a current-iteration fix. When complete, TDD gap becomes a resolved finding rather than an acknowledged content hole. |

---

## Composite Verification

```
completeness      = 0.93 * 0.20 = 0.186
internal_consistency = 0.93 * 0.20 = 0.186
methodological_rigor = 0.96 * 0.20 = 0.192
evidence_quality  = 0.94 * 0.15 = 0.141
actionability     = 0.94 * 0.15 = 0.141
traceability      = 0.94 * 0.10 = 0.094

composite = 0.186 + 0.186 + 0.192 + 0.141 + 0.141 + 0.094 = 0.940
```

**Composite: 0.940 / Threshold: 0.95 / Delta to threshold: -0.010**

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific line numbers and section references used
- [x] Uncertain scores resolved downward (Completeness was uncertain between 0.93 and 0.94; resolved to 0.93 because TDD content gap is real, not just documented)
- [x] No dimension scored above 0.95 without exceptional evidence (Methodological Rigor at 0.96 is justified by complete resolution of both I1 gaps and demonstrated systematic multi-framework application)
- [x] Leniency counteraction applied: I2 revised deliverable is strong, but the 0.95 C4 threshold is a high bar. Score of 0.940 accurately reflects near-threshold quality with one identified new gap
- [x] I2 calibration: Good revised deliverable with minor remaining issues scores 0.93-0.95. Score of 0.940 is consistent with this band.

---

## Handoff Context (adv-scorer to orchestrator)

```yaml
verdict: REVISE
composite_score: 0.940
threshold: 0.95
weakest_dimension: Completeness  # tied with Internal Consistency at 0.93
weakest_score: 0.93
critical_findings_count: 0
iteration: 2
i1_score: 0.887
score_delta: +0.053
gate_checks:
  GC-P4-1: PASS
  GC-P4-2: PASS
  GC-P4-3: PASS
i1_gaps_resolved: 9  # all declared fixes verified complete
new_findings:
  - "NF-I2-001 (Minor): DT-REC-001/DT-REC-002 omitted from Phase 5 Input 2 reversibility scope"
improvement_recommendations:
  - "Add one sentence to Phase 5 Input 2 covering DT-REC-001/DT-REC-002 reversibility (NF-I2-001) — resolves both IC and Traceability residual"
  - "Add (T4, observational) parenthetical to VS-003 inline usage in Cross-Template Pattern 3 body text"
  - "Move NPT-014 from AGREE-5 rank anchor table to footnote/anti-pattern note"
  - "Complete TDD.template.md analysis in Phase 5 via DT-REC-003 chunked Read procedure (not addressable in current iteration)"
delta_to_threshold: -0.010
note: "Gap to threshold is minimal (0.010). NF-I2-001 fix alone would raise IC and Traceability each by ~0.01, potentially reaching 0.950. Recommend I3 targeting only NF-I2-001 + VS-003 parenthetical (Priority 1 and 2 fixes)."
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*Score Version: I2*
*Date: 2026-02-28*
*SSOT: `.context/rules/quality-enforcement.md`*
*Threshold override: 0.95 (orchestration directive, C4)*
