# Barrier Gate Report: QG-1 Foundations Cross-Consistency Check

## L0 Executive Summary

**Score:** 0.881/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Quantitative Consistency (0.78)

**One-line assessment:** The four foundational deliverables share a coherent architecture and strong structural alignment, but three unresolved MR tolerance discrepancies between the system design (1B) and behavioral contracts (1D) — along with a contract path inconsistency and unanchored Bonferroni k references — prevent the cross-deliverable package from meeting the C4 barrier gate threshold of 0.95. Fixing these targeted numeric and path mismatches should bring the package to PASS without requiring substantive rework.

---

## Scoring Context

- **Gate Type:** QG-1 Sync Barrier (cross-deliverable consistency)
- **Criticality Level:** C4
- **Threshold:** 0.95 (H-13 at C4)
- **Streams Assessed:** 1A (requirements), 1B (design), 1C (protocol + baselines), 1D (contracts)
- **Scoring Strategy:** S-014 (LLM-as-Judge, 4-dimension barrier rubric)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.881 |
| **Threshold** | 0.95 (C4 barrier gate) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (barrier gate is cross-deliverable only; no adv-executor reports) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Terminological Consistency | 0.25 | 0.88 | 0.220 | Layer names, agent names, MR IDs consistent; verdict taxonomy dual-layer is intentional; NFR Bonferroni references unanchored |
| Structural Alignment | 0.25 | 0.91 | 0.228 | Cross-references mostly correct; one path discrepancy: FR-013 points to `tests/prompt-regression/contracts/` but 1D delivers at `contracts/per-agent/` |
| Quantitative Consistency | 0.25 | 0.78 | 0.195 | Three MR tolerance divergences (MR-003, MR-004, MR-005) between 1B and 1D are genuine implementation-blocking inconsistencies |
| Architectural Coherence | 0.25 | 0.95 | 0.238 | Req -> Design -> Protocol -> Contracts stack is coherent; hexagonal architecture consistently applied; interface contracts align; Group 3 can proceed with targeted fixes |
| **TOTAL** | **1.00** | | **0.881** | |

---

## Detailed Dimension Analysis

### Terminological Consistency (0.88/1.00)

**Evidence of consistency:**

- **Layer names (L1/L2/L3/L4):** All four deliverables use "Layer 1 (promptfoo CI/CD gate)", "Layer 2 (DeepEval evaluation backend)", "Layer 3 (Metamorphic Relation Framework)", and "Layer 4 (Statistical comparison engine)" with no variation. 1A FR-001 through FR-005 label Layer 1; 1B section 1.3 module decomposition uses identical layer labels; 1C protocol.md references `jerry/testing/stats.py` as Layer 4; 1D Section D.5 references all four layers.
- **Agent names:** ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer appear identically in 1A (FR-007 criteria list, NFR-008), 1B (module decomposition `criteria/ps_researcher.py`, `criteria/adv_scorer.py`), 1C (protocol execution order), and 1D (contracts scope table, per-agent invariant sections A.2 through A.6).
- **MR identifiers:** MR-001 through MR-005 are labeled identically across all four deliverables. 1A FR-010 defines them; 1B system-design.md section 1.5 Pattern 2 specifies tolerance values; 1D contracts Section C.1 through C.5 parameterizes them.
- **Module names:** `jerry/testing/stats.py` named in 1A FR-019/FR-014 (as the constant `MIN_STATISTICAL_SAMPLE_SIZE` location), 1B module decomposition, 1C protocol.md line 46, and 1D G.2 reverse trace. `layer4_stats.py` named in 1A FR-018/FR-030, 1B module decomposition. No divergence found.
- **Statistical terms:** Wilcoxon signed-rank, Wilson score, Bonferroni correction are named consistently. `InsufficientSamplesError`, `RegressionResult`, `QUALITY_PASS_THRESHOLD` are named consistently between 1A (FR-014, FR-015, FR-016) and 1B (types.py code block).

**Gaps:**

1. **Dual-verdict taxonomy appearance (minor, intentional):** 1B uses `TestVerdict` enum (PASS/WARN/FAIL) as the CI/CD gate verdict, while 1A FR-015 and 1D Section D.1 use REGRESSION/MARGINAL/NO_REGRESSION as the Wilcoxon classification labels. These are two distinct layers of a two-stage classification that 1B correctly differentiates (REGRESSION -> FAIL, MARGINAL -> WARN, NO_REGRESSION -> PASS). This is architecturally intentional per 1B Pattern 4 and is NOT a true inconsistency. However, the mapping is implicit and not explicitly cross-referenced in 1A FR-018 where it lists verdict values as "NO_REGRESSION / MARGINAL / REGRESSION / STRUCTURAL ONLY" without noting the translation to CI gate verdicts.

2. **Bonferroni k references in 1A NFR are unanchored to 1D's authoritative k=13:** 1D Section D.3 establishes k=13 as the "authoritative comparison-set count" for full evaluation. However, 1A NFR-003 uses K=10 (as a performance benchmark parameter) and NFR-007 uses K=5 (as a Type I error simulation parameter). Both are labeled as benchmark-specific hypotheticals, not claiming the authoritative k value. But the documents do not cross-reference 1D Section D.3 as the source of truth for the operational k. An implementer reading only 1A might not know where to find k=13. This is a traceability gap rather than a true inconsistency, but it weakens terminological anchoring.

**Improvement Path:**
- Add a note in FR-017 (1A) and FR-018 (1A) cross-referencing 1D Section D.3 as the authoritative source for the full evaluation k=13 value.
- Add a note in 1B Pattern 4 or types.py comments mapping TestVerdict.FAIL -> REGRESSION classification, WARN -> MARGINAL, PASS -> NO_REGRESSION, to make the two-taxonomy translation explicit.

---

### Structural Alignment (0.91/1.00)

**Evidence of alignment:**

- **1A -> 1B references:** FR-019 in 1A specifies `jerry/testing/stats.py` and `jerry/testing/layer4_stats.py`; 1B module decomposition at section 1.3 shows both modules at exactly those paths. FR-030 in 1A specifies `jerry/testing/layer1_promptfoo.py`, `layer2_deepeval.py`, `layer3_metamorphic.py`, `layer4_stats.py`, `stats.py`; 1B section 1.3 shows all five in the module tree. Perfect alignment.
- **1A -> 1D references:** FR-013 in 1A defines the behavioral property registry format. 1D Section A provides the full per-agent behavioral invariant catalog. 1D Section G provides bidirectional traceability matrix back to 1A requirement IDs. The G.2 reverse trace covers every FR relevant to behavioral contracts (FR-001 through FR-030 with explicit "not covered by contracts" explanations for infrastructure FRs). The trace is complete and accurate.
- **1A -> 1C references:** 1C protocol.md references `jerry/testing/stats.py` for regression comparison (line 46), references behavioral contract IDs per the linking convention (data collection schema section), and references N=30 from 1A FR-005 Full mode. The linkage is explicit and correct.
- **1B -> 1D references:** 1B module decomposition includes `evaluation/criteria/adv_scorer.py` and similar per-agent criteria files; 1D provides the behavioral bounds these criteria must enforce. The MR tolerance values in 1B are the "initial" values subject to calibration; 1D Section C is the calibrated specification. This framing is consistent.
- **1D -> 1A references:** 1D Section G explicitly maps all contract sections to requirement IDs. The mapping is extensive and accurate (all FR IDs cited resolve to real requirements in 1A).

**Gaps:**

1. **Contract path discrepancy (FR-013 vs. 1D actual structure):** FR-013 in 1A specifies: "The behavioral property registry shall consist of per-agent YAML files stored at `tests/prompt-regression/contracts/{agent-id}.yaml`." However, 1D delivers behavioral contracts at `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md` and the stream 1D scope includes `contracts/per-agent/`. The `tests/prompt-regression/contracts/` path in FR-013 is where the MR coverage tracking tool reads per-agent YAML files at runtime; the `contracts/per-agent/` directory in 1D is where the design-time per-agent contract YAML files live. These may be intended to be the same files, or the `tests/prompt-regression/contracts/` path may be a symlink target, but this is not explicitly reconciled in any of the four deliverables. An implementer following only FR-013 would create files in `tests/prompt-regression/contracts/` while the 1D directory structure suggests `contracts/per-agent/` is the authoritative location.

2. **1B module decomposition missing `layer4_stats.py` explicit orchestration description:** FR-030 in 1A says `layer4_stats.py` handles pipeline orchestration and imports from `stats.py`. 1B section 1.3 lists `stats.py` but the module tree does not show `layer4_stats.py` as a separate file — it shows `stats.py` directly under `jerry/testing/`. The H-10 compliance table in 1B attributes `stats.py` to "StatisticalEngine class", but FR-019 in 1A distinguishes `stats.py` (pure computation) from `layer4_stats.py` (pipeline orchestration). This is a minor gap: 1B's module tree does not explicitly show `layer4_stats.py` as a separate file, though the text elsewhere in 1B (FR-018 note, FR-030 references in 1A) confirms it should exist.

**Improvement Path:**
- Reconcile the `tests/prompt-regression/contracts/{agent-id}.yaml` path in FR-013 with the `contracts/per-agent/` directory structure in 1D. Either update FR-013 to reflect the 1D directory or add a note that the 1D YAML files are symlinked/copied to the `tests/` path at test time.
- Add `layer4_stats.py` explicitly to the module tree in 1B section 1.3 with a comment noting it orchestrates `stats.py` (per FR-019 architecture note).

---

### Quantitative Consistency (0.78/1.00)

**Evidence of consistency:**

- **N=30 baseline count:** All four deliverables consistently specify N=30 for Full mode. 1A FR-003 ("Full=30"), FR-005 ("Full mode: N=30"), FR-028 ("N=30 evaluations"); 1B EvaluationTier enum ("N>=30, all layers"); 1C protocol.md title "Statistical Rationale for N=30" (entire section); 1D Section D.1 ("Recommended N per version: 30"). Unanimous.
- **N=20 minimum:** All four use N=20 as the Wilcoxon minimum. 1A FR-014 (`MIN_STATISTICAL_SAMPLE_SIZE = 20`); 1B Pattern 3 ("N >= 20 for Standard/Full"); 1C argument 1 ("N >= 20 absolute floor"); 1D Section D.1 ("Minimum N per version: 20"). Unanimous.
- **Quality threshold 0.92:** All four use 0.92 as the PASS threshold. 1A FR-016 (`QUALITY_PASS_THRESHOLD = 0.92`); 1B Pattern 3 ("count(s >= 0.92)"); 1C data schema (`scores.weighted_composite`); 1D Section B.2 ("PASS >= 0.92") and D.2 ("Threshold for pass classification: score >= 0.92"). Unanimous.
- **Wilcoxon alpha=0.05:** All four use 0.05 as uncorrected alpha. Consistent.
- **Bonferroni k=13 and corrected alpha=0.004:** 1D establishes these authoritatively. 1C does not reference Bonferroni directly (correct — protocol.md does not cover regression comparison). 1A FR-017 treats k as a variable "K" without specifying the authoritative value. 1B treats k as a variable "K metrics" in Pattern 3 ("Apply Bonferroni correction for K metrics"). Neither 1A nor 1B contradict k=13, but neither affirms it either. This is a traceability gap (not an inconsistency) noted in Terminological Consistency above.

**Gaps — genuine numeric inconsistencies:**

1. **MR-003 (Irrelevant Context Appendation) tolerance: 1B says 0.03, 1D says 0.04.**
   - 1A FR-010 specifies default ±0.10 (a different unit — this is for MR-003 in FR-010 the "configurable tolerance (default: ±0.10)"), but then 1B design refines this to 0.03 and 1D contracts specify 0.04. So there is a three-way split: 1A=0.10, 1B=0.03, 1D=0.04. The 1A value of 0.10 is the requirement-level "configurable default"; 1B and 1D are design-level refinements. But 1B and 1D themselves disagree: 0.03 vs. 0.04. Implementation will have to choose one value without a clear authoritative source.

2. **MR-004 (Formatting Perturbation) tolerance: 1B says 0.05, 1D says 0.06; 1A says default ±0.05.**
   - 1A FR-010: default ±0.05. 1B design table: 0.05. 1D contracts: 0.06. Here 1A and 1B agree (0.05) but 1D deviates (0.06). 1D's rationale is "slightly higher tolerance than MR-001 because formatting changes can subtly affect LLM tokenization." The contracts document is presumably the more recent authoritative specification at the design level, but it contradicts both the requirements and the system design.

3. **MR-005 (Language Round-Trip) tolerance: 1B says 0.06, 1D says 0.07; 1A says default ±0.15.**
   - 1A FR-010: default ±0.15. 1B design table: 0.06. 1D contracts: 0.07. 1B and 1D are closer (0.06 vs. 0.07) but still disagree. The 1A value of 0.15 is the requirement-level default; the design and contracts both tighten this, but disagree with each other by 0.01.

4. **MR-001 and MR-002 are consistent:** MR-001 tolerance = 0.05 across 1A FR-010, 1B design table, and 1D C.1 (all agree). MR-002 effect size >= 0.40 (Cohen's d) is consistent across 1B and 1D.

**Quantitative score rationale:** The N, alpha, and quality threshold values — the most frequently referenced quantitative constants — are fully consistent. The MR tolerance divergences are the only numeric inconsistencies, but they affect three of the five MRs and could produce different test outcomes depending on which document implementers follow. This justifies a substantial deduction from a perfect score.

**Improvement Path:**
- Resolve three-way: designate 1D contracts as the authoritative source for MR tolerance values (they have the most detailed rationale and are the most recent). Update 1B design table to match: MR-003=0.04, MR-004=0.06, MR-005=0.07.
- Add a note in 1A FR-010 that the "configurable tolerance defaults" are the requirement-level ceilings and that the exact calibrated values are specified in 1D contracts Section C.
- Verify MR-002 minimum N=15 (1D C.2) is consistent with the design: 1B does not explicitly state MR-002 minimum N, so no conflict, but 1B should acknowledge the MR-002 exception to the N>=20 rule.

---

### Architectural Coherence (0.95/1.00)

**Evidence of coherence:**

- **Req -> Design -> Protocol -> Contracts stack integrity:** The causal chain is intact. Requirements (1A) identify what the system must do; design (1B) specifies how the domain is structured (hexagonal, module decomposition, interface types); protocol (1C) specifies how baselines are captured against this structure; contracts (1D) specify what behavioral properties the captured data must exhibit. Each layer adds specificity without contradicting the layer above.
- **No contradictory architectural decisions:** All four deliverables agree on: (1) four-layer architecture (CI/CD gate / evaluation backend / metamorphic relations / statistical engine); (2) hexagonal ports-and-adapters separation; (3) promptfoo-in-Docker isolation from Python UV environment; (4) score array as the inter-layer data contract; (5) git commit hash as baseline version key; (6) Langfuse as optional observability. No deliverable reverses or contradicts any of these decisions.
- **Interface boundaries align:** 1A FR-009 defines the score array JSON format; 1B defines `ScoreArray` type in `types.py`; 1C references score arrays in data collection schema; 1D references score arrays for Wilson CI computation (D.2). The score array is consistently the Layer 2 -> Layer 4 data contract. 1A IF-001 through IF-005 interface specifications are consistent with 1B port definitions (EvaluationPort, BaselinePersistencePort).
- **Sufficient for Group 3 implementation:** The combination of 1A (FR/NFR acceptance criteria), 1B (module decomposition, type definitions, port interfaces, test file structure), 1C (script interfaces, execution procedure, data schema), and 1D (per-agent behavioral properties, MR tolerances, regression thresholds) provides a complete implementation specification. An engineer starting Group 3 has: exact module paths, type signatures, data schemas, acceptance criteria, and behavioral expectations.
- **FMEA traceability:** 1A, 1B, and 1C all reference FM-001 through FM-010 failure modes from PROJ-035 ADR-001. 1D Section C design principles reference FM-009 (MR calibration). The failure mode mitigations are traceable from requirement rationales through to behavioral contract design choices.

**Gaps:**

1. **IMPROVEMENT vs. NO_REGRESSION classification not in 1A requirements:** 1D Section D.1 defines an IMPROVEMENT classification ("scores_b statistically significantly HIGHER than scores_a — logged but does not block merge"). This classification does not appear in 1A FR-015 or FR-018 requirement acceptance criteria. FR-015 specifies NO_REGRESSION / MARGINAL / REGRESSION only; FR-018 lists the same three plus STRUCTURAL ONLY. The IMPROVEMENT class is an additive refinement (a fourth statistical outcome) that the contracts introduce without a corresponding requirement. This is a minor gap: IMPROVEMENT does not block merges and does not contradict any existing requirement, but it is an undocumented behavioral property from 1A's perspective.

2. **1B threat model does not cover MR violation exploitation:** 1B Part 3 (STRIDE threat model) covers 40 threats across 6 attack surfaces. However, no threat explicitly covers adversarial input crafting to trigger false MR violations (i.e., generating paraphrase inputs that produce MR-001 violations to deny CI clearance). This is a gap in the threat model's completeness relative to the MR framework designed in Layer 3. It does not undermine architectural coherence but is a completeness note.

**Improvement Path:**
- Add IMPROVEMENT to 1A FR-015 and FR-018 as a fourth Wilcoxon classification (with the same parameterization as in 1D D.1 pseudocode: allows merge, logged only).
- Add a threat to 1B addressing adversarial MR violation crafting (T-41: attacker crafts paraphrase inputs designed to trigger MR-001 violations to block legitimate merges) with mitigation (paraphrase generation uses a separate trusted model, MR violations require statistical significance not single failures).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Issue | Current State | Target State | Specific Action |
|----------|-----------|-------|--------------|-------------|-----------------|
| 1 | Quantitative Consistency | MR-003 tolerance divergence | 1B=0.03, 1D=0.04 | Both=0.04 | Update 1B system-design.md MR tolerance table row for MR-003 from 0.03 to 0.04; add cross-reference to 1D Section C.3 as authoritative |
| 2 | Quantitative Consistency | MR-004 tolerance divergence | 1B=0.05, 1D=0.06, 1A=0.05 | All=0.06 | Update 1B design table row for MR-004 from 0.05 to 0.06; add note in 1A FR-010 that design/contracts refine the requirement-level default |
| 3 | Quantitative Consistency | MR-005 tolerance divergence | 1B=0.06, 1D=0.07 | Both=0.07 | Update 1B design table row for MR-005 from 0.06 to 0.07; align with 1D C.5 rationale |
| 4 | Structural Alignment | Contract path discrepancy | FR-013: `tests/prompt-regression/contracts/` vs. 1D: `contracts/per-agent/` | Explicit reconciliation | Add note in 1A FR-013 that per-agent YAML files in `contracts/per-agent/` are the source; `tests/prompt-regression/contracts/` is the runtime read location (symlink or copy during CI) |
| 5 | Terminological Consistency | Bonferroni k unanchored in 1A | NFR-003 uses K=10, NFR-007 uses K=5 as benchmark params; no cross-reference to 1D k=13 | FR-017 explicitly cites 1D D.3 as authoritative | Add sentence to 1A FR-017: "The authoritative full-evaluation k value (k=13) is specified in `contracts/behavioral-contracts.md` Section D.3." |
| 6 | Structural Alignment | `layer4_stats.py` absent from 1B module tree | 1B section 1.3 module tree shows `stats.py` but not `layer4_stats.py` | Explicit entry added | Add `layer4_stats.py` to 1B module decomposition diagram with note: "[ADAPTER] Layer 4 pipeline orchestration; imports from stats.py; handles report formatting and GitHub status API" |
| 7 | Architectural Coherence | IMPROVEMENT classification missing from 1A | 1D D.1 defines IMPROVEMENT; 1A FR-015/FR-018 do not | FR-015 and FR-018 list IMPROVEMENT as fourth classification | Add IMPROVEMENT outcome to 1A FR-015 and FR-018 acceptance criteria: "scores_b statistically significantly higher than scores_a -> IMPROVEMENT classification: logged, does not block merge" |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific file locations and line-level observations)
- [x] Uncertain scores resolved downward (Quantitative Consistency: resolved to 0.78 not 0.82 due to three confirmed numeric divergences)
- [x] C4 calibration applied: this is a barrier gate requiring 0.95; the 0.881 composite is significantly below threshold, consistent with the identified concrete discrepancies
- [x] No dimension scored above 0.95 without exceptional evidence (Architectural Coherence at 0.95 is justified by demonstrated stack coherence, consistent decision non-contradiction, and complete implementation specification)
- [x] Anti-leniency: The MR tolerance divergences were not scored as "minor" despite being small numeric differences, because they directly determine test pass/fail boundaries and the documents provide conflicting authoritative values

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.881
threshold: 0.95
weakest_dimension: Quantitative Consistency
weakest_score: 0.78
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Update 1B MR-003 tolerance from 0.03 to 0.04 (align with 1D C.3)"
  - "Update 1B MR-004 tolerance from 0.05 to 0.06 (align with 1D C.4)"
  - "Update 1B MR-005 tolerance from 0.06 to 0.07 (align with 1D C.5)"
  - "Reconcile FR-013 contract path (tests/prompt-regression/contracts/) with 1D directory (contracts/per-agent/)"
  - "Add cross-reference in 1A FR-017 to 1D D.3 as authoritative Bonferroni k=13 source"
  - "Add layer4_stats.py to 1B module decomposition tree"
  - "Add IMPROVEMENT classification to 1A FR-015 and FR-018 acceptance criteria"
```

---

## Assessor Notes

**Why this gates as REVISE and not ESCALATE:** All seven identified issues are targeted, concrete, and fixable without restructuring any deliverable. The architectural coherence is strong — the four streams together form a complete, non-contradictory specification. The gaps are limited to: three numeric values in one table in 1B, one path reference in 1A, and two cross-reference omissions. These are revision-cycle issues, not fundamental design problems.

**Why Quantitative Consistency is the gating dimension:** The MR tolerance discrepancies are not cosmetic. MR-003 at 0.03 would fire 33% more violations than at 0.04; MR-004 at 0.05 vs. 0.06 changes which reformatted prompts trigger regression alarms; MR-005 at 0.06 vs. 0.07 affects translation sensitivity. An implementer following 1B would build a tighter harness than one following 1D, and the two implementations would produce different test outcomes for the same agent. This is an implementation-blocking inconsistency.

**Expected post-revision score:** If the seven recommendations are addressed, the estimated barrier gate score would be 0.96-0.97, clearing the 0.95 threshold. The architectural coherence dimension is already at 0.95 and would improve marginally with the IMPROVEMENT classification and threat model additions. The quantitative and structural dimensions would reach 0.96+ with the numeric alignments and path reconciliation.
