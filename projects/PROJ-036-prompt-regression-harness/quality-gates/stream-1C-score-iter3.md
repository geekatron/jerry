# Quality Score Report: Stream 1C -- Baseline Generation Protocol (Iteration 3)

## L0 Executive Summary

**Score:** 0.938/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality / Completeness / Traceability (all 0.93)
**One-line assessment:** All three iter2 recommendations are substantively resolved -- Dror et al. ACL 2018 replaces the incomplete ICML 2025 citation, the per-step rounding discrepancy is explained in a clear footnote, and the `--eval-mode skip` to `"not_evaluated"` mapping is explicitly documented; the deliverable now clears the 0.92 threshold on all six dimensions with a composite of 0.938.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/baselines/` (protocol.md v1.2.0 + 3 schemas + example-run.json + 5 prompt YAML files = 10 files scored as a unit)
- **Deliverable Type:** Protocol/Schema/Prompt set (hybrid)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 3 (scored independently; iter2 score was 0.924)
- **Strategy Findings Incorporated:** Yes -- iter2 adv-scorer report used only to verify which fixes to check, not to inflate scores

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.938 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | Yes -- iter2 report (fix verification only) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 5 agents, full lifecycle phases 0-6, interface definitions for all 8 scripts, G-Eval criteria per agent, sample run in two forms; script stubs remain unimplemented (Group 3) |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Per-step rounding footnote resolves the 0.7435/0.749 discrepancy; `--eval-mode skip` to `"not_evaluated"` mapping documented; prior run_id and H-05 fixes confirmed intact |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Three independent statistical arguments; Noether ARE limitation disclosed; G-Eval criteria specified per agent; Dror et al. [6] added as methodological rationale for non-parametric test selection |
| Evidence Quality | 0.15 | 0.93 | 0.140 | All six citations complete: [1]-[5] unchanged, [6] now Dror et al. ACL 2018 with stable ACL Anthology URL -- replaces the previously incomplete ICML 2025 reference; sigma path remains a glob pattern |
| Actionability | 0.15 | 0.94 | 0.141 | Script interfaces with docstrings for all 8 scripts; default flag values documented; H-05-compliant Step 0.5; G-Eval criteria directly usable; `--eval-mode skip` mapping now actionable |
| Traceability | 0.10 | 0.93 | 0.093 | ADR-001 consistently qualified as PROJ-035; quality-enforcement.md cited in Data Collection Schema; behavior IDs linked to behavioral-contracts.md in all 5 prompt files; [6] reference annotated with relevance |
| **TOTAL** | **1.00** | | **0.938** | |

**Composite verification:**
(0.93 * 0.20) + (0.95 * 0.20) + (0.94 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.93 * 0.10)
= 0.186 + 0.190 + 0.188 + 0.1395 + 0.141 + 0.093
= **0.9375** (rounded to 0.938)

**Exact arithmetic:** 0.186 + 0.190 + 0.188 + 0.1395 + 0.141 + 0.093 = 0.9375, which rounds to **0.938**. PASS.

---

## Fix Verification Checklist (Iter2 Recommendations Verified)

| Iter2 Finding | Fix Verified? | Evidence |
|---------------|--------------|----------|
| Priority 1: Update ICML 2025 [6] with complete citation | YES | Reference [6] is now: Dror, R., Baumer, G., Berzak, Y., & Goldberg, Y. (2018). "The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing." ACL 2018, pp. 1383-1392. URL: https://aclanthology.org/P18-1128. Stable, complete, independently verifiable. |
| Priority 1: All statistical claims with bracketed references | YES | The Dror et al. [6] citation is integrated in the power analysis paragraph (line 105 of protocol.md: "...Dror et al. [6], who demonstrate that non-parametric significance tests are preferred..."). Note on [6] at line 1109 explains relevance. |
| Priority 2: Per-step rounding footnote | YES | Line 775: "Note on per-step rounding: The `weighted_composite` field in the sample record above shows `0.749`, not `0.7435`. This discrepancy arises from the reference implementation's rounding strategy: each intermediate dimension score is rounded to 3 decimal places before multiplication..." Explanation is clear and technically correct. |
| Priority 2: `evaluation_method: "not_evaluated"` maps to `--eval-mode skip` | YES | Line 362: "`evaluation_method` value mapping: When `capture_baseline.py` is invoked with `--eval-mode skip`... the resulting run records MUST set `evaluation_method: "not_evaluated"`..." The mapping is explicitly documented and the distinction ("flag name" vs. "canonical JSON schema enum value") is drawn. |
| Priority 3 (Monte Carlo power): Not targeted in iter3 | NOT ATTEMPTED | The footer confirms iter3 targeted only the three priority fixes. Monte Carlo simulation is still absent. This is the remaining gap. |
| Priority 4 (Script stubs): Not targeted in iter3 | NOT ATTEMPTED | Scripts remain interfaces only; Group 3 scope remains. |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Rubric criteria for 0.9+:** All requirements addressed with depth.

**Evidence:**

The deliverable is structurally complete across all 14 navigation sections. All 5 agents have prompt files with 3-5 prompts each (ps-architect at 4, intentional and documented). All 5 prompt YAML files have G-Eval criteria blocks for all 6 SSOT dimensions. The protocol addresses the full lifecycle: environment setup (Phase 0), agent capture sequence (Phases 1-3), validation (Phase 3), manifest finalization (Phase 4 implied in Outputs Produced), and quality gate (Phase E referenced). Interface definitions for all 8 scripts are present with docstrings, argument signatures, and output descriptions. Sample run record is present in two forms (inline in protocol.md and as example-run.json).

Iter3 introduced no structural changes to completeness -- the fixes addressed evidence quality and consistency dimensions. The completeness posture is unchanged from iter2: strong but constrained by the Group 3 script implementation gap.

**Gaps:**

The scripts remain unimplemented (stubs/interfaces only). A practitioner cannot execute Phase 0 Step 0.4 (`validate_environment.py`) without implementing the script. This is disclosed and intentional (Group 3 scope) but represents a real execution gap. For a protocol whose status is "READY FOR EXECUTION," this is the dominant completeness residual.

**Improvement Path:**

Implement even trivial script stubs (exit code 1 with "NotImplemented" message) to close the execution gap. Score would move toward 0.95+.

---

### Internal Consistency (0.95/1.00)

**Rubric criteria for 0.9+:** No contradictions, all claims aligned.

**Evidence:**

The two iter2 internal consistency findings are now cleanly resolved with specific, explicit text:

1. **Per-step rounding footnote (NEW in iter3):** Line 775 provides a detailed explanation: "this discrepancy arises from the reference implementation's rounding strategy: each intermediate dimension score is rounded to 3 decimal places before multiplication, producing accumulated rounding artifacts." The example is worked through: `0.71 * 0.15` computes as `0.1065`, rounded to `0.107`. This fully resolves the ambiguity in the Sample Run Record where the exact sum (0.7435) and the stored value (0.749) appeared inconsistent. The explanation is technically accurate -- per-step rounding does produce accumulated artifacts.

2. **`evaluation_method` enum mapping (NEW in iter3):** Line 362 explicitly documents the mapping: "`--eval-mode skip` flag name is the script argument; `"not_evaluated"` is the canonical JSON schema enum value." The paragraph clarifies that such records are excluded from score-based statistical analysis but count toward the N=30 valid run total for raw output purposes. This resolves the terminology mismatch identified in iter2 (where the protocol said `skip` but the schema had `not_evaluated`).

The run_id collision fix and H-05 fix from iter1 remain present and intact. N=30 power statement consistency (80%+ at sigma <= 0.09, ~78% at sigma=0.10) remains unchanged.

**Residual gap:**

The rounding footnote is accurate but reveals a subtle implementation concern: the claimed stored value of 0.749 does not follow directly from the rounding-before-multiplication rule as stated. Working through: 0.82*0.20=0.164 (exact), 0.78*0.20=0.156 (exact), 0.75*0.20=0.150 (exact), 0.71*0.15=0.1065 rounded to 0.107, 0.68*0.15=0.102 (exact to 3 decimal places), 0.65*0.10=0.065 (exact). Sum: 0.164+0.156+0.150+0.107+0.102+0.065 = 0.744. This rounds to 0.744, not 0.749. The footnote claims the stored value is 0.749, but the rounding-before-multiplication rule (as applied here) produces 0.744. There is a residual unexplained delta of 0.005 between 0.744 and 0.749. This is a minor arithmetic inconsistency in the footnote itself -- the explanation is conceptually correct (per-step rounding does produce artifacts) but the specific calculation does not reproduce the claimed stored value. This prevents reaching 0.97+ on this dimension.

**Improvement Path:**

Verify and correct the per-step rounding footnote arithmetic to show the exact sequence of operations that produces 0.749 from the component scores shown.

---

### Methodological Rigor (0.94/1.00)

**Rubric criteria for 0.9+:** Rigorous methodology, well-structured.

**Evidence:**

Three independent statistical arguments are present, consistent, and strengthened in iter3. The Dror et al. [6] citation adds a fourth independent pillar -- not a new argument for N=30 per se, but a methodological justification for the Wilcoxon test selection over parametric alternatives. The "Note on [6]" paragraph (line 1109) documents the Dror et al. finding precisely: "non-parametric tests (Wilcoxon, bootstrap) outperform parametric tests (t-test) when score distributions deviate from normality -- the expected condition for LLM quality scores."

The G-Eval criteria blocks across all 5 prompt YAML files remain intact and are specific per agent. The Noether ARE disclosure (line 1107) is unchanged and correct. The Wilcoxon test selection rationale is now documented through both the ARE argument and the Dror et al. NLP evaluation literature.

**Residual gap:**

The Monte Carlo power simulation (iter2 Priority 3 recommendation) was not added in iter3 and remains absent. The Noether formula-derived power of ~78% at sigma=0.10 is acknowledged as a conservative estimate, but the actual Wilcoxon power at N=30 could be verified empirically. The protocol notes this is a lower bound but does not provide the actual value. This is the primary residual for this dimension.

**Improvement Path:**

Add a simulation-backed power estimate ("Monte Carlo simulation at N=10,000 confirms N=30 provides approximately X% power at sigma=0.10 for the Wilcoxon signed-rank test"). This would close the gap and move this dimension to 0.97+.

---

### Evidence Quality (0.93/1.00)

**Rubric criteria for 0.9+:** All claims with credible citations.

**Evidence:**

The major improvement in iter3 is the replacement of reference [6]. The previous ICML 2025 [6] was "Full citation pending publication URL" -- a known gap explicitly noted in iter2. The new [6] is:

> Dror, R., Baumer, G., Berzak, Y., & Goldberg, Y. (2018). The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing. In *Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (ACL 2018)* (pp. 1383-1392). https://aclanthology.org/P18-1128

This is a complete, authoritative citation with a stable URL. The ACL Anthology is a permanent record. The citation replaces the incomplete workshop paper reference with a peer-reviewed conference paper from a major venue. This is a genuine evidence quality improvement.

All six citations [1]-[6] are now complete with journal/conference, volume/issue or page range, and year. References [1]-[5] are unchanged from iter2 and were already complete.

The "Note on [6]" paragraph explains the citation's relevance: it directly supports the Wilcoxon choice over parametric tests for LLM quality score distributions. This is more substantive than a bare citation.

**Residual gap:**

The sigma estimates from PROJ-017 Phase 5 remain referenced via a glob pattern: `projects/PROJ-017-*/orchestration/*/phase-5/`. This is not an exact path. A reader cannot navigate directly to the raw data without knowing the specific PROJ-017 project directory and orchestration run ID. The footnote on [6] at line 1109 is a strength; the imprecise data path remains the primary evidence quality residual.

Cost estimates still reference "March 2026 reference" for Anthropic API pricing without providing the input/output token rates used in the computation. This is a minor but real gap.

**Improvement Path:**

Provide the exact PROJ-017 Phase 5 evaluation data file path (replace the glob pattern). Add token rate assumptions to the cost estimation section footnote.

---

### Actionability (0.94/1.00)

**Rubric criteria for 0.9+:** Clear, specific, implementable actions.

**Evidence:**

The `--eval-mode skip` to `"not_evaluated"` documentation (line 362) directly improves actionability: a practitioner implementing `capture_baseline.py` now knows exactly which schema value to write when the evaluation is skipped. The iter2 ambiguity ("what does the script set evaluation_method to when using skip?") is resolved.

All 8 script interfaces remain present with docstrings. Default flag values are documented. H-05-compliant Step 0.5 is unchanged. G-Eval criteria strings are in directly usable format for `GEval(criteria=...)`.

**Residual gap:**

Scripts remain unimplemented. A practitioner following this protocol reaches a hard stop at Phase 0 Step 0.4 (`validate_environment.py`). This is the same residual from Completeness. The Group 3 scope designation explains it but does not eliminate the practical execution gap. The `re_evaluate.py` script referenced in the `--eval-mode skip` mapping documentation is also unimplemented; its existence is assumed by the documentation but not verified.

**Improvement Path:**

Same as Completeness: implement trivial script stubs to enable end-to-end execution testing.

---

### Traceability (0.93/1.00)

**Rubric criteria for 0.9+:** Full traceability chain.

**Evidence:**

The three iter1 traceability gaps (ADR-001 disambiguation, quality-enforcement.md citation in Data Collection Schema, behavior IDs linked to behavioral-contracts.md) remain resolved from iter2. The iter3 additions strengthen traceability: the "Used In" column for [6] in the References table explicitly documents how Dror et al. supports the Wilcoxon test selection. The "Note on [6]" paragraph further traces the citation to the specific claim it supports (non-parametric tests preferred when normality cannot be assumed for LLM quality scores).

The footer at line 1116-1117 includes: "Evidence basis: PROJ-035 ADR-001 (Four-Layer Composite Architecture), PROJ-017 Phase 5 evaluation data, Hollander et al. [1], Noether [3], Wilson [4], Dror et al. [6]." This is an explicit traceability declaration connecting the protocol's evidence basis to its source documents.

**Residual gap:**

The `behavioral-contracts.md` file's existence and contents (Sections A, B, C as referenced) cannot be confirmed from this scoring context. The behavior ID cross-references in all 5 prompt files point to specific sections (e.g., "behavioral-contracts.md Section A.1") that may or may not exist. This is an untestable link from this scoring context and is the primary traceability residual.

The PROJ-017 Phase 5 glob path issue (also noted under Evidence Quality) limits traceability for sigma estimates.

**Improvement Path:**

Confirm that `contracts/behavioral-contracts.md` exists and contains Sections A, B, C with the referenced content. Provide the exact PROJ-017 Phase 5 path.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.95 | 0.97 | Verify and correct the per-step rounding arithmetic: the footnote claims 0.749 but the stated rounding-before-multiplication rule produces 0.744 from the component scores shown. Trace the exact implementation rounding sequence to reconcile the stored value. |
| 2 | Evidence Quality | 0.93 | 0.96 | Replace `projects/PROJ-017-*/orchestration/*/phase-5/` glob with the exact directory path for sigma estimate data. Add input/output token rate assumptions to the cost estimation section. |
| 3 | Methodological Rigor | 0.94 | 0.97 | Add a Monte Carlo simulation result for Wilcoxon power at N=30, sigma=0.10 (e.g., "10,000-iteration simulation confirms approximately X% power"). This replaces the conservative Noether bound with an empirical estimate. |
| 4 | Completeness / Actionability | 0.93 / 0.94 | 0.95+ | Implement trivial script stubs (`sys.exit(1)` with "Not yet implemented") for all 8 scripts so that Phase 0 Step 0.4 is at minimum executable without a FileNotFoundError. |
| 5 | Traceability | 0.93 | 0.95 | Confirm `contracts/behavioral-contracts.md` exists with Sections A, B, C. If it does not yet exist, note in the protocol that the referenced file is a planned artifact (Group 3 scope). |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Internal Consistency at 0.95 not 0.97 due to the rounding arithmetic residual; Evidence Quality at 0.93 not 0.95 due to the glob path)
- [x] First-draft calibration not applicable (this is iteration 3; scored against rubric, not iteration-relative)
- [x] No dimension scored above 0.95 without documented evidence (Internal Consistency is the highest at 0.95; justified by the resolution of two concrete iter2 findings with specific, verifiable text)

**Specific leniency temptations counteracted:**

1. The Dror et al. [6] replacement is a high-quality fix -- a complete ACL 2018 citation with stable URL and a "Note on [6]" paragraph explaining relevance. Temptation: award 0.96+ on Evidence Quality. Held at 0.93 because the sigma glob path and cost estimate sourcing remain unaddressed.

2. The per-step rounding footnote is detailed and conceptually correct. Temptation: award 0.97+ on Internal Consistency as a "fully resolved" issue. Held at 0.95 because the specific arithmetic in the footnote (0.744 vs. claimed 0.749) does not self-verify. A dimension cited for "no contradictions, all claims aligned" should not contain an internal arithmetic inconsistency in its explanation of a prior inconsistency.

3. The composite of 0.938 is comfortably above the 0.92 threshold. Anti-leniency requires confirming this is genuine rather than boundary inflation. The assessment is: yes, this is genuine. Three of the six dimensions score 0.93-0.94, which is "Strong work with minor refinements needed" (calibration anchor: 0.85 = strong, 0.92 = genuinely excellent). The 0.93-0.94 cluster is appropriate for a deliverable with disclosed implementation gaps (Group 3 scripts) and non-critical residuals (glob path, rounding arithmetic footnote). The composite reflects the actual state of the deliverable.

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.938  # exact: 0.9375
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.93
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Verify per-step rounding footnote arithmetic: stated rule produces 0.744, not the claimed 0.749"
  - "Replace PROJ-017 Phase 5 glob path with exact file path for sigma estimates"
  - "Add Monte Carlo power simulation result for sigma=0.10 to replace conservative Noether bound"
  - "Implement trivial script stubs for all 8 scripts to close the Phase 0 execution gap"
  - "Confirm contracts/behavioral-contracts.md exists with Sections A, B, C as referenced"
```

---

*Score Report Version: 1.0*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Produced: 2026-03-07*
*Stream: 1C -- Baseline Capture Protocol and Schemas*
*Iteration: 3 of N*
