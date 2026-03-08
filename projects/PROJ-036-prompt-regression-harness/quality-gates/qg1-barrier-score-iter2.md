# Barrier Gate Report: QG-1 Foundations Cross-Consistency Check (Iteration 2)

## L0 Executive Summary

**Score:** 0.956/1.00 | **Verdict:** PASS | **Weakest Dimension:** Terminological Consistency (0.93)

**One-line assessment:** All seven targeted fixes from iteration 1 are confirmed effective; the three MR tolerance divergences are resolved, layer4_stats.py is present in 1B, Bonferroni k cross-references are anchored in both 1A and 1B, and FR-013's contract path is reconciled in its body text — two residual path echoes in the 1A allocation matrix and NFR-008 rationale are minor documentation-consistency issues that do not create implementation ambiguity, and the package clears the C4 barrier gate threshold of 0.95.

---

## Scoring Context

- **Gate Type:** QG-1 Sync Barrier (cross-deliverable consistency)
- **Criticality Level:** C4
- **Threshold:** 0.95 (H-13 at C4)
- **Streams Assessed:** 1A (requirements), 1B (design), 1C (protocol + baselines), 1D (contracts)
- **Scoring Strategy:** S-014 (LLM-as-Judge, 4-dimension barrier rubric)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.881 (iteration 1, REVISE)
- **Scored:** 2026-03-07

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.956 |
| **Threshold** | 0.95 (C4 barrier gate) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No (barrier gate is cross-deliverable only; no adv-executor reports) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Terminological Consistency | 0.25 | 0.93 | 0.2325 | Bonferroni k cross-references now anchored in 1A (NFR-003, NFR-007) and 1B (Pattern 3); dual-verdict taxonomy mapping explicit in 1B; minor self-review section in 1A still references superseded registry path |
| Structural Alignment | 0.25 | 0.96 | 0.2400 | FR-013 body and Path note fully reconciled; layer4_stats.py present in 1B module tree and H-10 table; two residual path echoes (allocation matrix, NFR-008 rationale) do not block implementation |
| Quantitative Consistency | 0.25 | 0.98 | 0.2450 | All three MR tolerance divergences resolved: MR-003=0.03 (both), MR-004=0.05 (both), MR-005=0.06 (both); N=30, N=20, 0.92 threshold, Wilcoxon alpha=0.05 remain unanimous; k=13 confirmed authoritative in 1D D.3 |
| Architectural Coherence | 0.25 | 0.96 | 0.2400 | Req→Design→Protocol→Contracts stack intact; hexagonal architecture consistently applied; IMPROVEMENT classification noted in 1D D.1 but still absent from 1A FR-015/FR-018 acceptance criteria; adversarial MR threat still absent from 1B threat model |
| **TOTAL** | **1.00** | | **0.956** | |

---

## Detailed Dimension Analysis

### Terminological Consistency (0.93/1.00)

**Evidence of improvement:**

- **Bonferroni k cross-references added to 1A:** NFR-003 now contains an explicit cross-reference note: "The K=10 value used here is specific to this NFR's performance benchmark scope... The full evaluation suite uses k=13 per the behavioral contracts (contracts/behavioral-contracts.md Section D.3)." NFR-007 contains the parallel note for K=5. Both notes correctly frame their local k values as mode-specific and point to 1D D.3 as authoritative. An implementer reading only 1A now has a clear path to the canonical k.

- **Bonferroni k cross-references added to 1B:** Pattern 3 (Layer 3 feeds Layer 4) now explicitly reads: "(k=13 for full evaluation suite per contracts D.3; k=10 for benchmark runs per NFR-003; k=5 for simplified statistical runs per NFR-007)." This is a complete, attributed disambiguation of the three k values used across the document stack.

- **Dual-verdict taxonomy:** 1B continues to use TestVerdict (PASS/WARN/FAIL) as the CI gate verdict and REGRESSION/MARGINAL/NO_REGRESSION as Wilcoxon classification labels. This dual-layer taxonomy is architecturally intentional. The mapping is explicit in 1B Pattern 4 comments (PASS -> No regression, WARN -> Marginal, FAIL -> Regression). No new ambiguity introduced.

**Residual gap:**

The self-review (S-010) section at the bottom of 1A contains the following check (line 1633): "FINDING-4 RESOLVED: FR-013 now includes a 'Behavioral Property Registry Specification' block defining the registry location (`tests/prompt-regression/contracts/{agent-id}.yaml`), file format..." — this self-review text references the pre-fix registry path (`tests/prompt-regression/contracts/`) rather than the post-fix path (`contracts/per-agent/{agent-name}.contract.yaml`). The self-review section describes a previous state of FR-013, not the current state. This is a documentation consistency gap within 1A's self-review: the body of FR-013 is correct but the self-review audit trail describes a superseded version.

This gap is minor: the self-review is a historical audit log, not an authoritative specification. It does not create implementation ambiguity because FR-013's body text is authoritative. But it does reduce terminological grounding from 0.96 to 0.93.

**Improvement Path:**
- Update the FINDING-4 RESOLVED line in the 1A self-review section to describe the current FR-013 state (contract path `contracts/per-agent/{agent-name}.contract.yaml` with Path note reconciling runtime vs. source locations).

---

### Structural Alignment (0.96/1.00)

**Evidence of improvement:**

- **FR-013 contract path reconciled in body text:** FR-013 now contains a "Behavioral Property Registry Specification" block stating: "per-agent YAML files stored at `contracts/per-agent/{agent-name}.contract.yaml`." The Path note immediately below the spec block provides explicit reconciliation: "`contracts/per-agent/` is the authoritative location for behavioral contract files (Stream 1D deliverable). The `tests/prompt-regression/` directory contains test execution artifacts (YAML test cases, benchmark scripts, result files) but not the contracts themselves. FR-013 coverage computation reads contract files from `contracts/per-agent/` and writes coverage results to the test execution report." An implementer reading FR-013 now has an unambiguous, reconciled specification.

- **layer4_stats.py added to 1B module tree:** The module decomposition in 1B section 1.3 now shows `layer4_stats.py` with the annotation: "[ADAPTER] Layer 4 pipeline orchestration; imports from stats.py (one-way dependency); handles report formatting and GitHub Actions status API integration (see FR-019 Module Architecture Note)." The H-10 compliance table includes the row: "`layer4_stats.py` | Layer4Pipeline class (orchestrates stats.py; imports from stats, not vice versa)." The dependency direction is explicit. This resolves the structural alignment gap identified in iteration 1.

- **FR-013 -> 1D trace:** 1D per-agent YAML contracts are confirmed at `contracts/per-agent/` (five files verified: adv-scorer, ps-researcher, ps-analyst, ps-architect, ps-critic). The actual deliverable structure matches the path specified in FR-013's body. The cross-deliverable path is now consistent.

**Residual gaps:**

1. **Allocation matrix echo (1A line 1406):** The allocation matrix row for FR-013 reads: "Coverage computed against behavioral property registry at `tests/prompt-regression/contracts/`." This is the old path. FR-013's body text has been updated but the allocation table summary was not. An implementer using the allocation table alone (a summary view) would see the old path. However, the allocation table is explicitly a summary and implementers are expected to reference the full FR for authoritative details. This residual path echo does not block implementation but is a documentation consistency issue.

2. **NFR-008 rationale echo (1A line 1036):** The NFR-008 rationale references "the behavioral property registry naming scheme (per-agent files at `tests/prompt-regression/contracts/{agent-id}.yaml`) to ensure consistent agent identifier usage across all test artifacts." This path reference was not updated during the FR-013 fix. NFR-008 governs test case YAML file naming (`{agent-id}-regression.yaml`) in `tests/prompt-regression/`; its reference to the contract registry path is contextual (explaining why agent IDs are used consistently), not normative. The residual path does not make NFR-008 unimplementable.

These two residual echoes prevent a score of 1.00 but do not rise to implementation-blocking inconsistency. The authoritative FR-013 text is clear; the allocation table and NFR-008 are summary/contextual references.

**Improvement Path:**
- Update 1A allocation matrix FR-013 row: change `tests/prompt-regression/contracts/` to `contracts/per-agent/`.
- Update 1A NFR-008 rationale path reference to match: `contracts/per-agent/{agent-name}.contract.yaml`.

---

### Quantitative Consistency (0.98/1.00)

**Evidence of full resolution:**

All three MR tolerance divergences from iteration 1 are confirmed resolved:

- **MR-003 (Irrelevant Context Appendation):** 1D C.3 now reads "Max delta | 0.03". 1B design table reads "MR-003 | 0.03". Both agree. The per-agent YAML (ps-researcher.contract.yaml) MR-003 entry also shows `tolerance: 0.03`. Unanimous across 1B, 1D Section C.3, and 1D per-agent YAMLs.

- **MR-004 (Formatting Perturbation):** 1D C.4 now reads "Max delta | 0.05". 1B design table reads "MR-004 | 0.05". 1A FR-010 specifies "default: ±0.05". All three agree. Per-agent YAML ps-researcher.contract.yaml shows `tolerance: 0.05` for MR-004.

- **MR-005 (Language Round-Trip):** 1D C.5 now reads "Max delta | 0.06". 1B design table reads "MR-005 | 0.06". Per-agent YAML ps-researcher.contract.yaml shows `tolerance: 0.06` for MR-005. Both agree (1A FR-010's "default ±0.15" is the requirement-level ceiling; the design/contracts refinement to 0.06 is consistent).

**Continuing unanimous values (confirmed unchanged):**

- **N=30 Full mode:** 1A FR-003/FR-005/FR-028, 1B EvaluationTier enum, 1C protocol section title, 1D D.1 all read N=30. No divergence.
- **N=20 Wilcoxon minimum:** 1A FR-014 (`MIN_STATISTICAL_SAMPLE_SIZE = 20`), 1B Pattern 3, 1C argument 1, 1D D.1 all read N=20. No divergence.
- **Quality threshold 0.92:** 1A FR-016 (`QUALITY_PASS_THRESHOLD = 0.92`), 1B Pattern 3, 1D B.2 and D.2 all read 0.92. No divergence.
- **Wilcoxon alpha=0.05:** Consistent across all four deliverables.
- **Bonferroni k=13:** 1D D.3 is the authoritative source; 1A NFR-003 and NFR-007 cross-reference it with correctly differentiated mode-specific k values; 1B Pattern 3 cites it explicitly. No contradiction — the k differentiation is now attributed and correct.

**Minor remaining note:**

The G.2 reverse trace in 1D (Section G) lists FR-013 without noting the path update. This is a traceability table issue, not a quantitative inconsistency. It does not affect the quantitative score.

**Why 0.98 not 1.00:** The scoring deducts a minimal amount for the residual path echoes in 1A (allocation table, NFR-008 rationale) that could, in theory, confuse quantitative lookup of where contract files live — though this is a structural rather than purely quantitative issue. The quantitative values themselves (numeric thresholds, sample sizes, alpha levels, k values) are internally consistent across all four deliverables. A perfect 1.00 would require zero residual path inconsistencies anywhere in the stack.

---

### Architectural Coherence (0.96/1.00)

**Evidence of coherence maintained:**

- **Req→Design→Protocol→Contracts stack:** The causal chain remains intact and the fixes have not introduced any new architectural inconsistency. Requirements (1A) set what the system must do; design (1B) specifies the hexagonal module structure and interface types; protocol (1C) governs how baselines are captured; contracts (1D) define behavioral properties against which captures are evaluated. Each layer adds specificity without contradicting layers above.

- **No contradictory architectural decisions:** All fixes addressed numeric values and path labels within existing architectural decisions. No fix changed a design decision (layer boundaries, tool choices, statistical method selection, git-hash versioning, Docker isolation). The architectural non-contradiction property from iteration 1 is preserved.

- **layer4_stats.py dependency direction explicit:** The one-way dependency (layer4_stats.py imports from stats.py, not vice versa) is now confirmed in three locations in 1A (FR-019 Module Architecture Note, FR-019 acceptance criteria, FR-030 allocation table), in 1B module tree annotations, and in 1B H-10 compliance table. The shared module architecture is structurally coherent and fully documented.

- **Score array as inter-layer contract:** 1A FR-009 score array JSON format, 1B ScoreArray type in types.py, 1C data collection schema, and 1D D.2 Wilson CI computation all reference score arrays as the Layer 2→Layer 4 data contract. This continues to be unanimously consistent.

**Residual gaps (unchanged from iteration 1):**

1. **IMPROVEMENT classification absent from 1A FR-015/FR-018:** 1D Section D.1 pseudocode defines an IMPROVEMENT classification (scores_b statistically significantly higher than scores_a — logged, does not block merge). This fourth Wilcoxon outcome is not listed in 1A FR-015 ("p < 0.05 AND mean(scores_b) < mean(scores_a) → REGRESSION; p < 0.10 → MARGINAL; otherwise → NO_REGRESSION") or FR-018's acceptance criteria verdict list. The iteration 1 improvement recommendation (Priority 7) was not addressed in the seven declared fixes. The gap remains: an implementer reading only 1A would build a three-outcome classifier; an implementer reading 1D would implement four outcomes. This is an architectural coherence issue for the regression classification logic.

2. **Adversarial MR violation threat absent from 1B threat model:** The iteration 1 observation (Priority not listed, noted as "completeness note") remains unaddressed. 1B's 40-threat STRIDE model does not cover adversarial paraphrase crafting to trigger false MR-001 violations. This is a threat completeness gap, not an inconsistency between deliverables.

These two gaps prevent a score of 1.00 but do not undermine the package's implementation readiness. The IMPROVEMENT classification gap is the higher-priority of the two: it produces a divergence between what 1A requires and what 1D specifies. However, IMPROVEMENT (allow merge, log only) is an additive enhancement with no merge-blocking consequence; the core regression detection logic (REGRESSION/MARGINAL/NO_REGRESSION) is fully consistent.

**Improvement Path:**
- Add IMPROVEMENT as a fourth Wilcoxon classification in 1A FR-015 acceptance criteria: "p < 0.05 AND mean(scores_b) > mean(scores_a) → IMPROVEMENT; logged, does not block merge."
- Add IMPROVEMENT to 1A FR-018 overall verdict list: "NO_REGRESSION / MARGINAL / REGRESSION / IMPROVEMENT / STRUCTURAL ONLY."
- Add threat T-41 (adversarial MR paraphrase crafting) to 1B threat model with mitigation.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific line citations and file-level observations)
- [x] Uncertain scores resolved downward (Terminological Consistency held at 0.93 due to self-review echo, not rounded up to 0.95)
- [x] C4 calibration applied: the 0.95 threshold is the governing bar; the 0.956 composite clears it with a margin of 0.006, consistent with the targeted residual gaps
- [x] No dimension scored above 0.98 without exceptional evidence (Quantitative Consistency at 0.98 reflects full resolution of all numeric divergences with only trace residuals)
- [x] Anti-leniency: Residual path echoes (allocation matrix, NFR-008 rationale, self-review audit trail) are documented as evidence for score deductions rather than dismissed as cosmetic; the IMPROVEMENT classification gap was not forgiven merely because it was in iteration 1's Priority 7 recommendation

**Calibration anchor check:**
- 0.92 = strong work with minor refinements needed — below this would be REVISE
- 0.95 = the threshold; the composite 0.956 represents "above threshold with documented residual items"
- 1.00 = essentially perfect — not warranted given the four documented residual gaps across three dimensions

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Issue | Current State | Target State | Specific Action |
|----------|-----------|-------|--------------|-------------|-----------------|
| 1 | Architectural Coherence | IMPROVEMENT classification absent from 1A | 1A FR-015/FR-018: three-outcome classifier; 1D D.1: four-outcome classifier | Both=four outcomes | Add "p < 0.05 AND mean(scores_b) > mean(scores_a) → IMPROVEMENT (logged, allows merge)" to 1A FR-015 acceptance criteria and FR-018 verdict list |
| 2 | Structural Alignment | Allocation matrix FR-013 row path echo | Line 1406: `tests/prompt-regression/contracts/` | `contracts/per-agent/` | Update 1A allocation table FR-013 notes column to reference `contracts/per-agent/` |
| 3 | Structural Alignment | NFR-008 rationale path echo | Line 1036: `tests/prompt-regression/contracts/{agent-id}.yaml` | `contracts/per-agent/{agent-name}.contract.yaml` | Update NFR-008 rationale path reference |
| 4 | Terminological Consistency | Self-review FINDING-4 audit trail references superseded registry path | Line 1633: describes pre-fix FR-013 state | Describes post-fix FR-013 state | Update FINDING-4 RESOLVED text to describe current FR-013 body (path `contracts/per-agent/{agent-name}.contract.yaml` with Path note reconciliation) |
| 5 | Architectural Coherence | Adversarial MR violation threat absent from 1B | 1B threat model: 40 threats, none cover MR paraphrase exploitation | T-41 added with mitigation | Add threat T-41: "Attacker crafts paraphrase inputs to trigger false MR-001 violations and block legitimate merges"; mitigation: "paraphrase generation uses trusted separate model; MR violations require statistical significance across N runs, not a single failure" |

---

## PASS Verdict Rationale

The QG-1 barrier gate threshold is 0.95 for C4 criticality. The iteration 2 composite score is **0.956**, clearing the threshold by 0.006.

**Why PASS and not REVISE:**

1. All seven declared fixes are confirmed effective. The primary blocking issue from iteration 1 — three MR tolerance divergences creating implementation-branching numeric inconsistencies — is fully resolved. An implementer across all four deliverables now gets unanimous numeric values for all five MR tolerances.

2. The residual gaps are documentation-consistency issues, not implementation-blocking inconsistencies. The residual path echoes (allocation table, NFR-008, self-review) point to locations that are explicitly labeled as summaries or audit trails; the authoritative specification text (FR-013 body) is correct and unambiguous. The IMPROVEMENT classification gap is additive (it adds a fourth outcome that allows merges) and does not conflict with the core regression-blocking logic.

3. The four deliverables together provide a complete implementation specification: module paths, type signatures, data schemas, statistical parameters, behavioral properties, and acceptance criteria are all consistent and non-contradictory at the level that governs Group 3 implementation.

**What the 0.006 margin means:**

The margin is intentionally narrow — the residual gaps are real and documented, not dismissed. A wider margin (0.97+) would require addressing the IMPROVEMENT classification and path echo issues identified above. The current score accurately reflects a package that clears the barrier gate while carrying four documented improvement items into Group 3 as non-blocking technical debt.

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.956
threshold: 0.95
weakest_dimension: Terminological Consistency
weakest_score: 0.93
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add IMPROVEMENT classification (four-outcome Wilcoxon) to 1A FR-015 and FR-018 acceptance criteria"
  - "Update 1A allocation matrix FR-013 row path from tests/prompt-regression/contracts/ to contracts/per-agent/"
  - "Update 1A NFR-008 rationale path reference to contracts/per-agent/{agent-name}.contract.yaml"
  - "Update 1A self-review FINDING-4 text to describe current FR-013 state (not pre-fix state)"
  - "Add threat T-41 (adversarial MR paraphrase exploitation) to 1B STRIDE threat model"
```
