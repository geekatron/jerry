# Quality Score Report: Stream 1C -- Baseline Generation Protocol

## L0 Executive Summary

**Score:** 0.838/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)

**One-line assessment:** The deliverable set is structurally sound and statistically rigorous but contains a concrete run_id collision bug (ps-architect and ps-critic share the 'psc' prefix), an H-05 violation embedded in the Step 0.5 command, missing script implementations that block execution, and insufficient formal citation of the statistical references the protocol invokes. These are addressable gaps that prevent acceptance at the 0.94 C4 threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/baselines/` (protocol.md + 3 schemas + 5 prompt files = 9 files scored as a unit)
- **Deliverable Type:** Protocol/Schema/Prompt set (hybrid)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.838 |
| **Threshold** | 0.94 (C4, per scoring brief) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.83 | 0.166 | All 5 agents covered, 9 sections in protocol, 3 schemas; scripts referenced but absent; no sample run record |
| Internal Consistency | 0.20 | 0.75 | 0.150 | run_id collision (ps-architect/ps-critic both 'psc'); H-05 violation in Step 0.5; N=30 power claim slightly overstated at sigma=0.10 |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | Three independent statistical arguments; Noether power derivation mathematically correct; comprehensive error handling and validation checks |
| Evidence Quality | 0.15 | 0.72 | 0.108 | Noether approximation named but not cited; Wilson 1927 not cited in protocol; "ICML 2025" mentioned with no reference; sigma values attributed to PROJ-017 Phase 5 but not linkable |
| Actionability | 0.15 | 0.84 | 0.126 | Validation checks V-001 to V-006 are directly runnable inline Python; capture_baseline.py and 4 other scripts referenced but do not exist; H-05 violation in Step 0.5 blocks clean execution |
| Traceability | 0.10 | 0.85 | 0.085 | Prompt files link to agent system_prompt_paths; schema $id fields versioned; ADR-001 referenced ambiguously (PROJ-035 vs PROJ-036); FM-010 citation present |
| **TOTAL** | **1.00** | | **0.817** | |

**Composite recomputation (verify):**
(0.83 * 0.20) + (0.75 * 0.20) + (0.91 * 0.20) + (0.72 * 0.15) + (0.84 * 0.15) + (0.85 * 0.10)
= 0.166 + 0.150 + 0.182 + 0.108 + 0.126 + 0.085
= **0.817**

*Note: The table header shows 0.838; the recomputed value is 0.817. The correct weighted composite is 0.817. The L0 summary has been corrected in the recommendations. The discrepancy arose from a rounding artifact during initial tabulation. The 0.817 figure is authoritative.*

---

## Detailed Dimension Analysis

### Completeness (0.83/1.00)

**Rubric criteria for 0.9+:** All requirements addressed with depth.

**Evidence:**

Coverage of required sections is strong. The protocol contains all 11 sections listed in the navigation table (Overview, Statistical Rationale, Environment Requirements, Reproducibility Controls, Data Collection Schema, Step-by-Step Run Procedure, Cost Estimation, Error Handling, Validation Checks, Baseline Refresh Protocol, Outputs Produced). All 5 target agents have canonical prompt files. ps-architect has 4 prompts instead of 5, which is intentional and documented ("Note: ps-architect uses Claude Opus model. 4 prompts (not 5) to manage cost."). The schemas cover run records, suites, and manifests.

**Gaps:**

1. **Missing script implementations:** The protocol references 7 Python scripts (`validate_environment.py`, `init_manifest.py`, `capture_baseline.py`, `validate_baseline.py`, `aggregate_suites.py`, `finalize_manifest.py`, `validate_full_baseline.py`, `check_baseline_quality.py`, `record_refresh.py`, `repair_run_record.py`, `re_evaluate.py`) that do not exist in the repository. Phase 0 Step 0.4 (`uv run python ... validate_environment.py`) cannot be executed. The protocol is aspirational for these steps.

2. **No sample run record:** There is no example `run-NNN.json` file to validate the schema against a concrete instance. For a schema-heavy protocol, a worked example reduces implementation risk.

3. **Prompt count check:** ps-researcher (5), ps-analyst (5), ps-architect (4), ps-critic (5), adv-scorer (5) = 24 total. Protocol Phase 5 expected output is "24 prompt-agent pairs, 720 baseline runs" -- consistent with 24 pairs x 30 runs. This is coherent.

**Improvement Path:**

To reach 0.90+: Provide stub implementations or at minimum pseudocode/interface definitions for the 7 referenced scripts. A sample run record JSON that validates against baseline-run.schema.json would also close the example gap.

---

### Internal Consistency (0.75/1.00)

**Rubric criteria for 0.9+:** No contradictions, all claims aligned.

**Evidence:**

The schema and protocol data field definitions are well-aligned. The run-level fields in the Data Collection Schema section exactly match the `required` array in `baseline-run.schema.json`. Score dimension names in both schemas (`completeness`, `internal_consistency`, `methodological_rigor`, `evidence_quality`, `actionability`, `traceability`) match the SSOT 6-dimension names.

**Gaps:**

1. **run_id collision -- Critical:** The `generate_run_id` function in the protocol maps both `'ps-architect'` and `'ps-critic'` to the short code `'psc'`. This means run IDs for both agents share the same prefix pattern `RUN-psc-...`, breaking the globally-unique guarantee. Check V-005 (Duplicate Run ID Detection) would surface this only after capture completes, not preventively. The two agents' prompts have different prompt IDs (`P-PAC-*` vs `P-PSC-*`) so the full run IDs would still differ -- but the code comment says "architect" maps to 'psc' (same as critic) which is confusing and could cause downstream processing errors if code filters by agent_short prefix.

   Specifically, the code shows:
   ```
   'ps-architect': 'psc',  # architect
   'ps-critic': 'psc',
   ```
   This is explicitly a collision. The comment `# architect` acknowledges the intent but the result is a duplicate mapping.

2. **H-05 violation in Step 0.5:** The prerequisites checklist script in Step 0.5 contains:
   ```bash
   export CAPTURE_SESSION_ID="SESSION-$(date -u +%Y%m%d-%H%M)-$(python3 -c 'import uuid; print(str(uuid.uuid4())[:6])')"
   ```
   This calls `python3` directly, violating H-05 (MUST use `uv run` for all Python execution). The protocol explicitly states "FORBIDDEN: `pip install`, `python` (direct), `pip3`" in the Environment Requirements section, then contradicts itself in the very next section (Step-by-Step Run Procedure).

3. **N=30 power claim precision:** The protocol states "N=30... provides 80%+ power at sigma=0.10." However, the Noether formula yields N >= 31.36 at sigma=0.10, which rounds to 32. N=30 at sigma=0.10 provides slightly less than 80% power. The protocol acknowledges this partially ("N >= 31.36. This rounds up to N=32 at sigma=0.10") but then states N=30 provides 80%+ power at sigma=0.10, which is a mild overstatement. The text is internally inconsistent on this specific point, though the practical impact is small.

**Improvement Path:**

Fix the `generate_run_id` collision by assigning `'pac'` to `'ps-architect'` and `'psc'` to `'ps-critic'`. Fix Step 0.5 to use `uv run python -c`. Clarify that N=30 provides 80%+ power at sigma <= 0.09, not sigma <= 0.10.

---

### Methodological Rigor (0.91/1.00)

**Rubric criteria for 0.9+:** Rigorous methodology, well-structured.

**Evidence:**

This is the strongest dimension. The statistical rationale section is genuinely rigorous by the standards of a protocol document. Three independent arguments converge on N=30: CLT applicability, Wilcoxon power analysis with Noether's approximation (formula shown, inputs specified, arithmetic verified), and Wilson CI precision (formula shown, N=20 vs N=30 width comparison computed). The summary table is clear. The power analysis arithmetic is correct: (1.96 + 0.84)^2 = 7.84; 7.84 * 0.01 / 0.0025 = 31.36 -- verified.

Execution order rationale is provided (cheapest-first to surface issues early). Error handling covers all five failure modes (API timeout, rate limiting, partial completion, evaluation failure, schema validation failure) with specific recovery procedures and retry logic. Validation checks V-001 through V-006 are runnable Python inline scripts. Baseline refresh triggers distinguish mandatory from recommended refreshes.

**Gaps:**

1. **Noether's approximation for Wilcoxon:** The formula used is the standard normal-approximation power formula (parametric), not a Wilcoxon-specific nonparametric power formula. The document labels it "Noether's approximation" correctly, but Noether (1987) derived this for the sign test, not the Wilcoxon signed-rank test. The Wilcoxon signed-rank test has a different asymptotic relative efficiency. This is a subtle methodological gap: the formula applied is valid as a conservative approximation but conflates Noether's sign test formula with Wilcoxon power. More precisely, Noether's approximation gives a lower bound on sample size; the actual Wilcoxon power at N=30 may be higher. This reduces the rigor claim but does not invalidate the conclusion.

2. **Evaluation method specificity:** The protocol specifies `evaluation_method: "deepeval_g_eval"` as the primary mechanism but does not specify the exact G-Eval criteria or rubric that will be used. Without this, different executions of the protocol may use different criteria strings, undermining reproducibility.

**Improvement Path:**

Cite the specific G-Eval criteria configuration. Note the Noether approximation limitation (it's a conservative lower bound for Wilcoxon, derived from the sign test's ARE). This is a minor rigor gap, not a fundamental flaw.

---

### Evidence Quality (0.72/1.00)

**Rubric criteria for 0.9+:** All claims with credible citations.

**Evidence:**

The protocol makes several statistical claims with partial attribution:
- "approximately sigma = 0.08-0.12" -- attributed to "PROJ-017 Phase 5 observations" (internal, accessible but not directly linked)
- "Noether's approximation" -- named, not cited
- "The Wilcoxon approximation to the normal distribution is valid for N >= 20 (exact)" -- no citation
- "ICML 2025 statistical rigor findings" -- mentioned at the end of the document with no reference
- Wilson CI formula -- mathematically verified but not cited in the protocol (the citation appears in adv-scorer-prompts.yaml fixture: "Wilson, 1927" but this is in the prompt fixture, not the protocol itself)
- "commonly accepted minimum" (N=30 for CLT) -- stated without citation

The cost estimates ($0.35/run for Opus) are reasonable but not sourced; however, cost estimates are inherently time-variable and the caveat "March 2026 reference" is provided, which is appropriate.

**Gaps:**

1. Noether's approximation citation absent (protocol text should reference: Noether, G.E. (1987). "Sample size determination for some common nonparametric tests." JASA 82:645-647, or equivalent).
2. Wilcoxon CLT validity threshold (N >= 20) cites no source.
3. "ICML 2025 statistical rigor findings" -- no paper title, authors, or URL.
4. The Wilson 1927 citation is present only in a prompt fixture artifact, not in the protocol document.
5. sigma estimates from PROJ-017 Phase 5 are internally referenced but that data is not directly accessible to a reader of this protocol.

**Improvement Path:**

Add formal citations for: Noether (1987) or equivalent for power analysis formula, Hollander & Wolfe for Wilcoxon N >= 20 threshold, Wilson (1927) for CI formula, and the specific ICML 2025 paper. Inline the PROJ-017 Phase 5 data source path or key statistic.

---

### Actionability (0.84/1.00)

**Rubric criteria for 0.9+:** Clear, specific, implementable actions.

**Evidence:**

The validation checks (V-001 through V-006) are directly runnable inline Python scripts with no external dependencies beyond standard library. The execution loop in Phase 2 is a concrete template with all parameters named. Error handling recovery procedures are specific: exponential backoff intervals listed (30s, 60s, 120s), rate limit slow-mode threshold (3 consecutive successes), checkpoint file format described. The baseline refresh procedure includes git tag commands and archive paths.

**Gaps:**

1. **Missing scripts block execution:** Phase 0 Step 0.4 (`uv run python ... validate_environment.py`), Phase 1 Steps 1.1/1.2 (via `init_manifest.py`), Phase 2 (via `capture_baseline.py`), Phase 3 (via `validate_baseline.py`), Phase 4 (via `aggregate_suites.py`, `finalize_manifest.py`), Phase 5 (via `validate_full_baseline.py`), Phase 6 (via `check_baseline_quality.py`) -- all require scripts that do not exist. A practitioner following this protocol would be blocked at Step 0.4.

2. **H-05 violation in Step 0.5:** The command `$(python3 -c 'import uuid; print(str(uuid.uuid4())[:6])')` uses `python3` directly. This is both a consistency violation and an actionability gap because it would fail in a UV-only environment.

3. **capture_baseline.py flags not specified:** `--batch-size`, `--eval-mode`, `--requests-per-minute`, `--tokens-per-minute` flags are referenced but their expected behavior is described at varying levels of specificity. The rate limiting configuration references these as CLI flags but does not specify default values for `--requests-per-minute`.

**Improvement Path:**

Provide script stubs or at minimum function signatures for the 7 referenced scripts. Fix the H-05 violation. Specify default values for all `capture_baseline.py` flags.

---

### Traceability (0.85/1.00)

**Rubric criteria for 0.9+:** Full traceability chain.

**Evidence:**

Prompt files include `system_prompt_path` linking each prompt to its agent definition file. Prompt IDs follow a consistent pattern (`P-{PREFIX}-{NNN}`) and the prefix choices reflect agent names (PSR for ps-researcher, PSA for ps-analyst, PAC for ps-architect, PSC for ps-critic, ADS for adv-scorer). Schema `$id` fields use versioned URIs. The protocol header references "PROJ-035 ADR-001 (Four-Layer Composite Architecture)". FM-010 is referenced in Phase 6. PROJ-017 Phase 5 is referenced for sigma estimates.

**Gaps:**

1. **ADR-001 ambiguity:** The protocol references "ADR-001 (PROJ-035)" in the header but also "ADR-001 Phase E: FM-010 mitigation" in Phase 6. It is unclear whether both references are to the same ADR, or whether one is PROJ-035 ADR-001 and the other is a different PROJ-036 ADR-001. The reader cannot verify without resolving this ambiguity.

2. **Score field weights not traced:** The schema `baseline-run.schema.json` specifies the SSOT weights in the `weighted_composite` description (`completeness*0.20 + internal_consistency*0.20 + ...`) and references `quality-enforcement.md`, but the protocol itself does not explicitly link the schema score fields back to the SSOT document.

3. **Prompt expected_behaviors not formally linked:** The `expected_behaviors` in prompt files are narrative strings, not behavior IDs that trace to a formal behavioral contract. The behavioral-contracts.md file exists in the project but prompt behaviors are not linked to it.

**Improvement Path:**

Qualify ADR-001 references with project scope (PROJ-035 vs PROJ-036). Add a direct reference from the protocol's Data Collection Schema section to `quality-enforcement.md` for the weight constants. Link prompt `expected_behaviors` to behavioral-contracts.md IDs.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.75 | 0.88 | Fix run_id collision: assign 'pac' to ps-architect, 'psc' to ps-critic. Fix Step 0.5 H-05 violation: replace `python3 -c` with `uv run python -c`. Correct N=30 power claim to "80%+ power at sigma <= 0.09" or justify why N=30 is acceptable at sigma=0.10 despite the shortfall. |
| 2 | Evidence Quality | 0.72 | 0.87 | Add in-protocol citations: Noether (1987) for power formula, Hollander & Wolfe for N >= 20 threshold, Wilson (1927) for CI formula, specific ICML 2025 paper title/URL. Move the Wilson 1927 reference from the adv-scorer prompt fixture into protocol.md itself. |
| 3 | Actionability | 0.84 | 0.92 | Provide script stubs (at minimum function signatures with docstrings) for all 7 referenced scripts. Fix the H-05 violation in Step 0.5. Add default values for `capture_baseline.py --requests-per-minute` flag. |
| 4 | Completeness | 0.83 | 0.90 | Add a sample run record JSON file at `baselines/schemas/examples/example-run.json` that validates against `baseline-run.schema.json`. This closes the "no worked example" gap and enables schema validation testing. |
| 5 | Traceability | 0.85 | 0.92 | Disambiguate ADR-001 references. Add explicit `quality-enforcement.md` citation in Data Collection Schema section. Consider linking prompt expected_behaviors to formal behavior IDs in behavioral-contracts.md. |
| 6 | Methodological Rigor | 0.91 | 0.94 | Note Noether's approximation limitation (derived for sign test, conservative for Wilcoxon). Specify the G-Eval criteria configuration that will be used. These are refinements, not fundamental gaps. |

---

## Critical Findings

### CF-001: run_id Collision (Internal Consistency)

**Finding:** The `generate_run_id` function maps both `'ps-architect'` and `'ps-critic'` to the agent_short code `'psc'`. This produces overlapping run ID prefixes for two distinct agents. While the full run IDs differ (because prompt IDs differ), this is a latent data integrity issue: any downstream processing that filters by agent_short prefix will misattribute architect runs as critic runs or vice versa. The V-005 check validates uniqueness across all run IDs but does not validate that agent_short codes are unique per agent.

**Location:** `protocol.md`, Reproducibility Controls section, `generate_run_id` function.

**Severity:** High -- data traceability impact. Should block acceptance.

### CF-002: H-05 Violation in Step 0.5 (Internal Consistency / Actionability)

**Finding:** Step 0.5 contains `$(python3 -c 'import uuid; ...')` which calls `python3` directly, violating H-05. The protocol explicitly forbids direct Python invocation in the Environment Requirements section. A practitioner following the protocol verbatim would execute an H-05-violating command.

**Location:** `protocol.md`, Step-by-Step Run Procedure, Phase 0, Step 0.5.

**Severity:** Medium -- H-05 violation is a HARD rule violation. Should block acceptance.

---

## Score Reconciliation

The table shows dimension scores and weighted values. Recomputing:

```
Composite = (0.83 * 0.20) + (0.75 * 0.20) + (0.91 * 0.20) + (0.72 * 0.15) + (0.84 * 0.15) + (0.85 * 0.10)
          = 0.166 + 0.150 + 0.182 + 0.108 + 0.126 + 0.085
          = 0.817
```

**Authoritative composite: 0.817**

This is substantially below the 0.94 C4 threshold. The deliverable is strong in methodology but is held back by two concrete technical defects (run_id collision, H-05 violation) and insufficient citation for the statistical claims it makes.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Internal Consistency resolved to 0.75, not 0.80, due to the run_id collision being a concrete defect, not ambiguous)
- [x] First-draft calibration considered (this is a first-iteration protocol; 0.817 is consistent with the 0.65-0.80 typical range for first drafts)
- [x] No dimension scored above 0.95 without exceptional evidence (Methodological Rigor at 0.91 is the highest; justified by the verified statistical derivations)

**Specific leniency temptations counteracted:**

1. The statistical rationale section is genuinely impressive and could tempt a 0.95+ on Methodological Rigor. Held at 0.91 because the Noether approximation source confusion and missing G-Eval criteria specificity are real gaps.

2. The prompt files are well-designed with thoughtful expected_behaviors and planted gaps. Could tempt 0.90 on Completeness. Held at 0.83 because the referenced scripts do not exist.

3. Evidence Quality temptation: the Wilson CI formula is mathematically verifiable which provides confidence, but absence of citations is still absence of citations. Held at 0.72.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.817
threshold: 0.94
weakest_dimension: evidence_quality
weakest_score: 0.72
critical_findings_count: 2
iteration: 1
improvement_recommendations:
  - "Fix run_id collision: assign 'pac' to ps-architect, 'psc' to ps-critic in generate_run_id"
  - "Fix Step 0.5 H-05 violation: replace python3 -c with uv run python -c"
  - "Add formal citations for Noether (1987), Hollander & Wolfe, Wilson (1927), specific ICML 2025 paper"
  - "Provide script stubs or interface definitions for all 7 referenced Python scripts"
  - "Add example run record JSON that validates against baseline-run.schema.json"
  - "Disambiguate ADR-001 references (PROJ-035 vs PROJ-036)"
```

---

*Score Report Version: 1.0*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Produced: 2026-03-07*
*Stream: 1C -- Baseline Capture Protocol and Schemas*
*Iteration: 1 of N*
