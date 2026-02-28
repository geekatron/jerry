# Quality Score Report: ADR-001 NPT-014 Elimination Policy (I3)

## L0 Executive Summary

**Score:** 0.9445/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.92)
**One-line assessment:** ADR-001 I3 resolves both primary I2 evidence gaps (A-31 full citation, R-QE-001 through R-ADS-003 sub-table) but the I3 fix to Group 1 introduced a verifiable internal inconsistency -- line 277 claims "6 specific upgrade recommendations" while the sub-table contains exactly 5 rows -- dropping Internal Consistency from 0.95 to 0.92 and holding the composite at 0.9445, 0.0055 below the C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C4
- **C4 Threshold:** 0.95 (elevated from standard H-13 threshold of 0.92)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **ADR Gate Checks Applied:** GC-ADR-1 through GC-ADR-5, A-11 check, AGREE-5 check
- **Strategy Findings Incorporated:** Yes -- I2 report (adversary-adr001-i2.md, score 0.9455 REVISE) incorporated as prior context
- **Prior Scores:** I1: 0.9185, I2: 0.9455
- **Iteration:** I3 (third scoring)
- **Scored:** 2026-02-28T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9445 |
| **C4 Threshold** | 0.95 |
| **Standard H-13 Threshold** | 0.92 |
| **Verdict** | REVISE |
| **Distance from C4 Threshold** | 0.0055 |
| **I2 Score** | 0.9455 |
| **Score Delta (I2 -> I3)** | -0.0010 (regression) |
| **Score Trajectory** | I1: 0.9185 -> I2: 0.9455 (+0.0270) -> I3: 0.9445 (-0.0010) |
| **Strategy Findings Incorporated** | Yes (I2 report) |
| **FMEA Arithmetic Verified** | YES -- all 5 RPN values correct (72, 48, 100, 150, 28) |
| **L2 Token Budget Arithmetic Verified** | YES -- 745/850 = 87.6% correct, within ceiling |

---

## Gate Check Results

| Gate | Description | Status | Evidence |
|------|-------------|--------|----------|
| GC-ADR-1 | Nygard format compliance (Title, Status, Context, Decision, Consequences) | PASS | All 5 required sections present; extended with L0/L1/L2, Forces, Options, Compliance |
| GC-ADR-2 | Evidence tier labels on all claims | PASS | A-31 now has full bibliographic entry (Bsharat, Myrzakhan, Shen, arXiv:2312.16171, 2023); A-20 and A-15 fully cited (I2); all claims carry tier labels |
| GC-ADR-3 | PG-003 reversibility assessment present | PASS | Full 5-component reversibility table; HIGH overall; null-framing contingency documented |
| GC-ADR-4 | Phase 2 dependency correctly handled | PASS | Unconditional exception explicitly stated; "Phase 2 outcome irrelevant" sourced to barrier-4/synthesis.md Section 3 |
| GC-ADR-5 | No false validation claims | PASS | MANDATORY EPISTEMOLOGICAL BOUNDARY maintained; UNTESTED label applied to NPT-009 vs. positive framing claim; A-11 absent |
| A-11 check | A-11 (hallucinated citation) absent | PASS | Zero occurrences as evidence citation; only appears in constraint prohibition (lines 107, 541, 557) |
| AGREE-5 check | AGREE-5 not presented as T1/T3 | PASS | Line 64: labeled "internally generated, NOT externally validated"; not cited as peer-reviewed evidence |

---

## I3 Fix Verification

| I2 Fix Target | Applied in I3? | Evidence | Score Impact |
|---------------|---------------|----------|--------------|
| A-31 full bibliographic citation (Priority 1) | YES | Line 505: "Bsharat, Myrzakhan, Shen. 'Principled Instructions Are All You Need for Questioning LLaMA-2, GPT-3.5/4.' [arXiv:2312.16171](https://arxiv.org/abs/2312.16171) (2023)" -- full author list, title, arXiv URL, year | Evidence Quality: 0.93 -> 0.95 |
| VS-001/VS-003 parenthetical disambiguation (Priority 3) | YES | Line 507: parenthetical "(VS-001: 33-instance NEVER/MUST NOT/FORBIDDEN/DO NOT vendor self-practice catalog; VS-003: HARD tier vocabulary as structured negative vocabulary observation)" added to References entry #5 | Evidence Quality: secondary improvement |
| R-QE-001 through R-ADS-003 sub-table in Group 1 (Priority 2) | YES -- with count defect | Lines 279-285: sub-table with ID, Target Rule File, Description columns; 5 rows enumerated; BUT line 277 states "6 specific upgrade recommendations" while sub-table contains 5 rows -- count contradiction introduced by I3 fix | Actionability partially improved; Internal Consistency: 0.95 -> 0.92 (new defect) |

**I3 fix outcome:** Both primary I2 gap-closing fixes were applied. The A-31 citation fix is clean and complete. The R-QE-001 sub-table fix closes the actionability gap but introduces a count inconsistency ("6 stated, 5 enumerated") that regresses Internal Consistency and partially negates the Actionability improvement.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.1920 | All Nygard sections + L0/L1/L2 + 4 adversarial strategies + R-QE-001 through R-ADS-003 sub-table now present; minor count mismatch in text does not represent a completeness gap |
| Internal Consistency | 0.20 | 0.92 | 0.1840 | I3 introduced "6 vs. 5" count contradiction at line 277: text claims 6 recommendations, sub-table shows 5; all other I2 consistency gaps (Pre-Mortem scope, scoring basis) remain resolved |
| Methodological Rigor | 0.20 | 0.95 | 0.1900 | FMEA scale definitions present (I2); all 4 adversarial strategies rigorously applied; arithmetic verified; epistemological discipline maintained; I3 fixes do not affect this dimension |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | A-31 now fully cited (I3); A-20 and A-15 fully cited (I2); VS-001/VS-003 disambiguated (I3); all tier labels accurate; A-11 absent; AGREE-5 not over-cited |
| Actionability | 0.15 | 0.94 | 0.1410 | R-QE-001 through R-ADS-003 sub-table now present (I3) -- substantially closes Group 1 implementer dependency on TASK-012; count mismatch (6 vs. 5) leaves residual implementer doubt about missing entry |
| Traceability | 0.10 | 0.95 | 0.0950 | A-31 arXiv:2312.16171 traceable (I3); VS-001/VS-003 disambiguated (I3); all major claims trace to specific documents with version numbers |
| **TOTAL** | **1.00** | | **0.9445** | |

**H-15 Arithmetic Verification:**
- Completeness: 0.96 x 0.20 = 0.1920
- Internal Consistency: 0.92 x 0.20 = 0.1840; running: 0.1920 + 0.1840 = 0.3760
- Methodological Rigor: 0.95 x 0.20 = 0.1900; running: 0.3760 + 0.1900 = 0.5660
- Evidence Quality: 0.95 x 0.15 = 0.1425; running: 0.5660 + 0.1425 = 0.7085
- Actionability: 0.94 x 0.15 = 0.1410; running: 0.7085 + 0.1410 = 0.8495
- Traceability: 0.95 x 0.10 = 0.0950; running: 0.8495 + 0.0950 = **0.9445** (confirmed)

**Distance from C4 threshold:** 0.95 - 0.9445 = **0.0055**

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

ADR-001 I3 addresses all mandatory requirements with depth:

- All five Nygard sections (Title, Status, Context, Decision, Consequences), extended with L0/L1/L2 levels
- Constraints table: C-001 through C-007 with source citations
- Forces: 4 tensions explicitly reasoned
- Options: 3 options each with steelman (S-003), pros, cons, fit with constraints, and score
- Decision with 4-point rationale and alignment table
- L1 Technical: diagnostic filter, 5-step upgrade procedure (with Step 5 quality gate hook from I2), 4-group sequencing with counts, Phase 2 baseline protocol, L2 token budget analysis
- L2 Architectural: evolution path, systemic consequences, Pre-Mortem (5 failure modes with scope distinction), FMEA (5 failure modes with scale definitions from I2), Inversion analysis
- Consequences: 5 positive, 5 negative, 3 neutral, 6 risk register entries with scope distinction note
- Compliance: PG-003 reversibility (5-component table), evidence tier labels (6 claims), constraint propagation verification (GC-P4-1 through GC-P4-3)
- Related Decisions: 3 downstream ADRs with relationship descriptions
- References: 13 entries
- PS Integration with key findings for downstream handoff
- Self-Review Checklist: 17 checks
- R-QE-001 through R-ADS-003 sub-table: now present in Group 1 section (I3 fix)

The sub-table's count discrepancy (text: "6"; table: 5 rows) is treated as an Internal Consistency issue, not a Completeness gap. The five enumerated IDs represent the substantive content; the completeness requirement (enumerate the recommendations with target file and description) is met.

**Gaps:**

No substantive completeness gaps remain. The count mismatch at line 277 is a minor text error, not a missing content section.

**Improvement Path:**

Correct the text at line 277 from "6 specific upgrade recommendations" to "5 specific upgrade recommendations" (or add a missing 6th row if TASK-012 actually identifies 6 recommendations). This is a one-character edit.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

All I2 consistency gaps remain resolved:
- Pre-Mortem / Risk Register scope distinction: both tables carry explicit scope distinction notes (lines 360, 476)
- Option scoring basis declared at line 194: "architect's synthesis judgment across the three evaluation dimensions"
- Core logical chain fully consistent: T1+T3 evidence -> NPT-014 underperforms -> PG-001 unconditional -> Phase 2 irrelevant -> universal policy. This chain is stated in L0, reinforced in Context/Evidence Base, Decision/Rationale, and Compliance.

**New I3-Introduced Gap:**

Line 277 states: "TASK-012 identified 6 specific upgrade recommendations (R-QE-001 through R-ADS-003)."
The sub-table that follows contains exactly 5 rows: R-QE-001, R-QE-002, R-ADS-001, R-ADS-002, R-ADS-003.

The code range "R-QE-001 through R-ADS-003" spans 5 identifiers. The numeral "6" is inconsistent with both the count of listed IDs (5) and the stated code range. An implementer reads line 277, expects 6 recommendations, then finds 5 in the table. This raises the question: is R-QE-003, R-QE-004, or some other identifier missing from the table? The document cannot resolve this question internally.

This is a specific, verifiable, numerically exact contradiction. The I2 report awarded 0.95 for Internal Consistency noting "No remaining consistency gaps identified." The I3 fix introduced this gap. Per the leniency bias counteraction rule, uncertain scores resolve downward. The gap is real, bounded (one number vs. one table), and actionable.

**Score rationale for 0.92 vs. lower:**

The gap is isolated to one numerical claim. The broader document is highly consistent -- the logical chain, evidence tier assignments, cross-references between sections, FMEA/Pre-Mortem alignment, and constraint table are all internally consistent. 0.92 reflects one specific, bounded inconsistency in an otherwise consistent document. 0.70-0.89 would require "minor inconsistencies" (plural, across dimensions); 0.90+ is appropriate for a single isolated numerical error in otherwise tight consistency.

**Improvement Path:**

Fix line 277 to read "5 specific upgrade recommendations" (matching the 5-row table), or add the missing 6th recommendation row if TASK-012 identifies 6 distinct upgrade targets. This is a single-line correction.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

All I1 and I2 methodological gaps are resolved and I3 makes no changes affecting this dimension:

- **FMEA scale definitions (from I2):** Line 374 provides full 1/5/10 anchor definitions for Severity, Occurrence, and Detection. All 5 S/O/D values can be independently audited against the scale.
- **FMEA arithmetic verified correct:** 4x6x3=72, 8x3x2=48, 5x5x4=100, 6x5x5=150, 7x2x2=28. All five RPNs confirmed.
- **Option 3 "HIGHEST" clarified (from I2):** "(zero-change avoidance, not positive Phase 2 support)" parenthetical present at line 200.
- **Option scoring basis declared (from I2):** 0-3 per dimension, summed, normalized to /10; labeled as architect judgment.
- **All 4 adversarial strategies rigorously applied:** S-003 (steelman per option), S-004 (Pre-Mortem with 5 failure modes), S-012 (FMEA with defined scale), S-013 (Inversion).
- **Epistemological discipline:** MANDATORY EPISTEMOLOGICAL BOUNDARY clearly stated; UNTESTED label on NPT-009 vs. positive framing; T4 inferences labeled as inferences.
- **L2 token budget arithmetic verified:** 745/850 = 87.6%, within ceiling.

**Gaps:**

No remaining methodological rigor gaps identified. I3 fixes do not affect this dimension.

**Improvement Path:**

No improvement needed on this dimension.

---

### Evidence Quality (0.95/1.00)

**Evidence:**

Both I2 evidence quality gaps are resolved in I3:

1. **A-31 full bibliographic citation (I3 fix, line 505):** "Bsharat, Myrzakhan, Shen. 'Principled Instructions Are All You Need for Questioning LLaMA-2, GPT-3.5/4.' [arXiv:2312.16171](https://arxiv.org/abs/2312.16171) (2023)." Full author list, title, arXiv identifier with hyperlink, publication year. The paper is independently verifiable without accessing upstream barrier-1 files. The citation description adds substantive content: "affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4 vs. prohibitions." This is meaningful corroborating data, not a placeholder.

2. **VS-001/VS-003 parenthetical disambiguation (I3 fix, line 507):** "(VS-001: 33-instance NEVER/MUST NOT/FORBIDDEN/DO NOT vendor self-practice catalog; VS-003: HARD tier vocabulary as structured negative vocabulary observation)" -- a reader can now distinguish what VS-001 represents from what VS-003 represents without accessing supplemental-vendor-evidence.md.

3. **A-20 and A-15 (from I2):** Full bibliographic citations with arXiv URLs remain present and unchanged.

4. **Evidence tier assignments remain correct and consistent:** T1 for peer-reviewed (A-20, A-15), T3 for preprint (A-31), T4 for observational/compiled (VS-001 through VS-004, TASK-012, barrier-4/synthesis.md), UNTESTED for Phase 2 framing question.

5. **A-11 absent:** Zero citation occurrences in evidence role. Only appears in constraint prohibition.

6. **AGREE-5 correctly labeled:** "internally generated, NOT externally validated" at line 64; not cited as T1 or T3 anywhere.

**Gaps:**

No remaining evidence quality gaps identified. Both I2 gaps are closed.

**Improvement Path:**

No improvement needed on this dimension.

---

### Actionability (0.94/1.00)

**Evidence:**

The primary I2 actionability gap is substantially resolved:

1. **R-QE-001 through R-ADS-003 sub-table (I3 fix, lines 279-285):** A 3-column table (ID, Target Rule File, Description) enumerates the specific upgrade targets. An implementer executing Group 1 can now identify the 5 enumerated rule file targets (quality-enforcement.md for R-QE-001 and R-QE-002; agent-development-standards.md for R-ADS-001, R-ADS-002, R-ADS-003) without consulting TASK-012.

2. **Step 5 quality gate hook (from I2, line 269):** Connected to H-17 and FMEA RPN 150 mitigation.

3. **Group 2 breakdown (from I2, line 292):** 5 framework-level + 27 agent-level = 32 total, sourced to barrier-4/synthesis.md L1 Recommendation Counts table.

4. **Diagnostic filter:** Binary, implementable. NPT-014 identification requires absence of all three elements (consequence, scope, alternative) -- clear test.

5. **4-group sequencing:** Clear order with rationale and counts for all groups. Groups 3 and 4 explicitly identified as parallelizable after Group 1.

6. **Phase 2 baseline preservation protocol:** 4 numbered steps with specific actions (branch isolation, commit-hash documentation).

**Residual gap:**

The count discrepancy (line 277: "6 specific upgrade recommendations" vs. sub-table: 5 rows) creates residual implementer uncertainty. An implementer noticing the mismatch may spend effort searching for a 6th missing recommendation that may not exist, or may implement only 5 recommendations when 6 were intended. This is a bounded but real actionability impediment.

Score held at 0.94 rather than raised to 0.95. The substantive content (5 specific, implementable targets with file and description) is present. The "6 vs. 5" mismatch does not prevent implementation but introduces unnecessary friction. Uncertain direction resolved downward.

**Improvement Path:**

Correct "6 specific upgrade recommendations" to "5 specific upgrade recommendations" at line 277. This single edit simultaneously resolves the Internal Consistency gap and the Actionability residual friction. If TASK-012 identifies 6 recommendations, add the missing 6th row to the sub-table.

---

### Traceability (0.95/1.00)

**Evidence:**

Both I2 traceability gaps are resolved in I3:

1. **A-31 traceability (I3 fix):** arXiv:2312.16171 provides a stable, publicly accessible identifier. An independent verifier can retrieve the paper without accessing upstream barrier-1 files.

2. **VS-001/VS-003 disambiguation (I3 fix):** The parenthetical in References entry #5 enables a reader to trace which vendor self-practice observation corresponds to which ID without consulting supplemental-vendor-evidence.md.

3. **Primary traceability chains remain fully intact from I2:**
   - PG-001 -> barrier-2/synthesis.md ST-4 (T1+T3 unconditional)
   - 22 NPT-014 instances -> TASK-012 (T4 compiled)
   - 130 total recommendations -> barrier-4/synthesis.md L0
   - 5-domain universal NPT-014 presence -> barrier-4/synthesis.md Themes 1 and 2
   - Phase 2 unconditional exception -> barrier-4/synthesis.md Section 3 (quoted)
   - "5 framework-level" -> barrier-4/synthesis.md L1 Recommendation Counts table
   - Option scoring -> labeled as architect judgment (transparent)

4. **Constraint table (C-001 through C-007):** All 7 constraints have source citations.

5. **Evidence tier table (Compliance section):** All 6 claims mapped to tiers and sources.

**Gaps:**

No remaining traceability gaps identified. The I3 fixes strengthen this dimension.

**Improvement Path:**

No improvement needed on this dimension.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.92 | 0.95 | Fix line 277: change "6 specific upgrade recommendations (R-QE-001 through R-ADS-003)" to "5 specific upgrade recommendations (R-QE-001 through R-ADS-003)". This is a single word change. If TASK-012 actually identifies 6 recommendations, add the missing 6th row to the sub-table instead. This fix simultaneously resolves Internal Consistency (0.92 -> 0.95) and removes the Actionability residual friction (0.94 -> 0.95). |
| 2 | Actionability | 0.94 | 0.95 | See Priority 1 -- the same "6 vs. 5" fix resolves the residual actionability uncertainty. No additional action required if Priority 1 is addressed. |

**Score impact estimate (Priority 1 fix only):**
- Internal Consistency: 0.92 -> 0.95 (+0.03 x 0.20 = +0.0060)
- Actionability: 0.94 -> 0.95 (+0.01 x 0.15 = +0.0015)
- Total composite improvement: +0.0075
- Projected I4 composite: 0.9445 + 0.0075 = **0.9520**, exceeding the 0.95 C4 threshold.

---

## ADR-Specific Gate Check Summary

| Gate | Check | Result | Notes |
|------|-------|--------|-------|
| GC-ADR-1 | Nygard format complete | PASS | Title, Status, Context, Decision, Consequences all present; extended format with L0/L1/L2 |
| GC-ADR-2 | Evidence tier labels present | PASS | All claims carry tier labels; A-31 now fully cited with arXiv:2312.16171; A-20/A-15 fully cited (I2); VS-001/VS-003 disambiguated (I3) |
| GC-ADR-3 | PG-003 reversibility documented | PASS | Full 5-component table; HIGH overall; null-framing contingency analyzed |
| GC-ADR-4 | Phase 2 dependency handled | PASS | Unconditional exception stated; sourced to barrier-4/synthesis.md Section 3 |
| GC-ADR-5 | No false validation claims | PASS | MANDATORY EPISTEMOLOGICAL BOUNDARY enforced; UNTESTED labels applied; A-11 absent |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific line numbers and content cited
- [x] Uncertain scores resolved downward: Internal Consistency held at 0.92 (not 0.95) despite resolving all I2 gaps, because the I3 fix introduced a new verifiable "6 vs. 5" contradiction
- [x] Uncertain scores resolved downward: Actionability held at 0.94 (not 0.95) because the count mismatch creates residual implementer friction even though the sub-table is present
- [x] C4 threshold (0.95) held firm -- score of 0.9445 is correctly below threshold
- [x] Score regression correctly recorded: I3 (0.9445) < I2 (0.9455) by 0.0010, caused by introduced inconsistency
- [x] No dimension scored above 0.95 -- three dimensions at 0.95, one at 0.96, two below 0.95
- [x] FMEA arithmetic independently verified: 4x6x3=72, 8x3x2=48, 5x5x4=100, 6x5x5=150, 7x2x2=28 -- all correct
- [x] L2 token budget arithmetic independently verified: 745/850 = 87.647% -- within 850-token ceiling
- [x] A-11 absence confirmed: zero occurrences in evidence role; only appears in constraint prohibition (lines 107, 541, 557)
- [x] AGREE-5 over-citation checked: correctly labeled at line 64; not cited as T1 or T3 anywhere
- [x] "6 vs. 5" count discrepancy verified independently: line 277 text says "6"; sub-table rows counted = 5 (R-QE-001, R-QE-002, R-ADS-001, R-ADS-002, R-ADS-003); code range "R-QE-001 through R-ADS-003" spans 5 IDs

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.9445
threshold: 0.95
standard_threshold: 0.92
weakest_dimension: Internal Consistency
weakest_score: 0.92
critical_findings_count: 0
iteration: 3
prior_score: 0.9455
score_delta: -0.0010
distance_from_threshold: 0.0055
score_trajectory: "I1: 0.9185 -> I2: 0.9455 (+0.0270) -> I3: 0.9445 (-0.0010)"
top_gap_dimensions:
  - "Internal Consistency (0.92): line 277 states '6 specific upgrade recommendations' but sub-table at lines 279-285 contains exactly 5 rows -- verifiable numerical contradiction introduced by I3 fix"
  - "Actionability (0.94): same '6 vs. 5' count discrepancy creates residual implementer uncertainty about whether a 6th recommendation is missing"
improvement_recommendations:
  - "Fix line 277: change '6 specific upgrade recommendations' to '5 specific upgrade recommendations' (or add missing 6th row if TASK-012 identifies 6). Single-word fix. Simultaneously resolves Internal Consistency gap and Actionability residual friction. Estimated composite impact: +0.0075, reaching 0.9520 (PASS)."
gate_checks_passed: [GC-ADR-1, GC-ADR-2, GC-ADR-3, GC-ADR-4, GC-ADR-5]
gate_checks_with_minor_gap: []
blocking_findings: none
arithmetic_verified: true
i3_fixes_applied: [A-31_full_bibliographic_citation, VS001_VS003_parenthetical_disambiguation, R_QE_001_through_R_ADS_003_subtable]
i3_fix_defects: ["R_QE_001_subtable: text says 6 recommendations, table has 5 rows -- count contradiction introduced"]
i2_score_regression: true
regression_cause: "I3 fix to Group 1 section introduced '6 vs. 5' numerical contradiction at line 277"
fix_for_i4: "Single edit to line 277: '6' -> '5' (or add missing 6th row). Clears Internal Consistency and Actionability gaps."
```

---

*Scored by: adv-scorer*
*Strategy: S-014 (LLM-as-Judge, 6-dimension weighted composite)*
*Criticality: C4 (threshold 0.95)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Workflow: neg-prompting-20260227-001*
*Task: TASK-016 (phase-5 ADR scoring, I3)*
*Created: 2026-02-28*
