# Quality Score Report: Stream 3E — CI/CD Pipeline Setup (Iteration 2 Re-Score)

## L0 Executive Summary

**Score:** 0.920/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.90)
**One-line assessment:** All three mandated fixes are verified present in the code; the pipeline now meets the H-13 baseline threshold (0.92) but falls short of the 0.94 stream-level gate — the two remaining gaps (placeholder Docker SHA credibility and the `2>/dev/null` silent-failure risk in cost-monitor ceiling checks) prevent acceptance at stream standard.

---

## Scoring Context

- **Deliverable:** `.github/workflows/prompt-regression-smoke.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-full.yml`, `.github/actions/cost-monitor/action.yml`, `.github/actions/artifact-publish/action.yml`
- **Deliverable Type:** Code (GitHub Actions CI/CD Pipeline)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 PASS (stream-level, above H-13 baseline of 0.92)
- **H-13 Threshold:** 0.92 PASS
- **Prior Score (Iter 1):** 0.848 REJECTED
- **Scored:** 2026-03-07T00:00:00Z

---

## Fix Verification (Mandatory Pre-Score Check)

Before scoring, each mandated fix was verified against the actual file content:

| Fix | Claim | Verified? | Evidence |
|-----|-------|-----------|---------|
| H-05 / FR-023 | All `python3` calls in composite actions replaced with `uv run python` | YES — CONFIRMED | `cost-monitor/action.yml` lines 128, 160, 202, 219, 252: all `uv run python`. `artifact-publish/action.yml` lines 266, 438: all `uv run python`. No `python3` residue found in either file. |
| FR-027 smoke | `validate-yaml` step changed from `exit 1` to `::warning::` + `exit 0` | YES — CONFIRMED | `smoke.yml` lines 181–184: three `::warning::` annotations followed by `exit 0`. The `exit 1` from iter1 is gone. |
| Cost monitor header | "$20 Full" corrected to "$50 Full" | YES — CONFIRMED | `cost-monitor/action.yml` line 27: `MC-20: Per-workflow budget ceiling ($5 Standard, $50 Full)` — matches the actual `COST_CEILING_USD: "50.00"` in `prompt-regression-full.yml`. |

All three fixes are confirmed present. No new issues introduced by the fixes (the warning annotations in the smoke `validate-yaml` step are correctly formatted GHA annotations; the `uv run python` replacements carry the same `2>/dev/null || echo 0` / `2>/dev/null` patterns as before; the header text update is a documentation-only change).

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.920 |
| **Stream Threshold** | 0.94 (PASS) |
| **H-13 Threshold** | 0.92 (PASS) |
| **Verdict** | REVISE — meets H-13 baseline but misses stream gate by 0.020 |
| **Strategy Findings Incorporated** | No — standalone scoring |
| **Iter 1 Score** | 0.848 |
| **Score Delta** | +0.072 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | H-05/FR-023 fully resolved in both composite actions; FR-027 smoke behavior now coherent across both jobs |
| Internal Consistency | 0.20 | 0.93 | 0.186 | $20/$50 discrepancy resolved; FR-027 job 1/job 2 alignment restored; all N values, action pins, permission blocks consistent |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | All MC controls intact; H-05 fully cleared; `2>/dev/null` silent-failure risk in ceiling checks remains unaddressed |
| Evidence Quality | 0.15 | 0.84 | 0.126 | FR/MC headers thorough; Docker SHA still shows sequential-pattern placeholder digest — substantive evidence gap for MC-08 |
| Actionability | 0.15 | 0.90 | 0.135 | All workflows fully executable; `uv run python` compliance now uniform; one residual operational risk in ceiling check error path |
| Traceability | 0.10 | 0.90 | 0.090 | Full bidirectional FR/MC traceability in all files; FR-019 and FR-001 forward-references still lack explicit stream cross-references |
| **TOTAL** | **1.00** | | **0.920** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

All three workflow tiers are present and structurally complete as in iter1. The two primary completeness gaps from iter1 have been resolved:

1. **FR-023 / H-05 FIXED:** Every `python3` call in both composite actions has been replaced with `uv run python`. Specific verification:
   - `cost-monitor/action.yml`: Token extraction (line 128), cost estimation (line 160), token ceiling check (line 202), cost ceiling check (line 219), structured record write (line 252) — all `uv run python`.
   - `artifact-publish/action.yml`: Metadata generation (line 266), verdict extraction (line 438) — all `uv run python`.

2. **FR-027 smoke contradiction FIXED:** The smoke workflow `validate-yaml` step (job 2, lines 177–184) now emits three `::warning::` annotations and exits 0, matching FR-027's "warning, not blocking failure" specification and the behavior established in job 1's `check-test-authorship` step. The workflow comment ("FR-027: Missing test case authorship is a WARNING, not a blocking failure") is now accurate and consistent with the implementation.

**Gaps:**

1. **FR-025 Docker SHA placeholder (unchanged from iter1):** The promptfoo image SHA (`sha256:4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2`) continues to exhibit a sequential hex pattern inconsistent with real cryptographic digests. This was noted in iter1 and was not among the three mandated fixes. FR-025 acceptance criteria ("Docker image version shall be pinned in the workflow YAML") is met formally but not substantively if this is a placeholder.

**Improvement Path:**

Replace the placeholder Docker SHA with the actual published digest for the target promptfoo version. No completeness gaps remain that are not shared with Evidence Quality.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

All consistency issues from iter1 are resolved:

1. **Cost monitor header fixed:** `cost-monitor/action.yml` line 27 now reads `MC-20: Per-workflow budget ceiling ($5 Standard, $50 Full)`, matching the `COST_CEILING_USD: "50.00"` in `prompt-regression-full.yml` with its documented rationale ("N=30 x 5 agents x ~$5-8 per agent = up to $40 under normal conditions. $50 ceiling provides safety margin").

2. **FR-027 consistency restored:** Both job 1 (`check-test-authorship`) and job 2 (`validate-yaml`) in smoke.yml now produce `::warning::` annotations and exit 0 for missing test YAML. The workflow header comment ("FR-027: Test case authorship enforcement (CI warning, not blocking)") is now accurate for both jobs.

Remaining consistent across all files (unchanged from iter1): N values (smoke=0, standard=10, full=30), permission blocks (`contents: read`, `pull-requests: write`, `checks: write`), action version pins (all four actions SHA-pinned at the same hashes), `QUALITY_PASS_THRESHOLD: "0.92"`, `STATISTICAL_ALPHA: "0.05"`, `HARNESS_MODEL_VERSION: "claude-sonnet-4-20250514"`, Docker SHA (same across all three main workflows), API key injection pattern (absent in smoke, present in standard/full).

**Gaps:**

No new internal consistency issues introduced by the fixes. The `2>/dev/null` pattern appears consistently across all Python invocations in the composite actions — this is internally consistent even if operationally risky.

**Improvement Path:**

No internal consistency gaps remain. Score reflects the strong post-fix state.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

All MC security controls verified as in iter1 (MC-07, MC-08, MC-09, MC-25, MC-28, MC-29, MC-31, MC-32, MC-33). The primary methodological standards violation is fully resolved:

**H-05 / FR-023 FIXED:** All Python invocations in composite actions now use `uv run python`. The main workflow files (`smoke.yml`, `standard.yml`, `full.yml`) already used `uv run python` in iter1. The composite actions now match. Full H-05 compliance is achieved across all five deliverable files.

Methodological patterns across the three tiers are sound:
- Smoke: structural-only, no API key, Docker `--network=none`, `fail-fast: false`
- Standard: N=10, Wilcoxon + Wilson + Bonferroni, fork-safe fallback, cost monitoring
- Full: N=30, all four layers, metamorphic relations, model migration mode, baseline update gate

**Gaps:**

1. **`2>/dev/null` silent-failure risk in cost-monitor ceiling checks (unchanged from iter1):** The two ceiling check commands in `cost-monitor/action.yml` (lines 202–216 and 219–233) pipe `uv run python` output through `2>/dev/null`. If the Python command fails (unexpected: `uv` unavailable, malformed float input), stderr is suppressed, the pipeline produces no "BREACH" token, `grep -q "BREACH"` returns non-zero, and the `&&` block does not execute — meaning a ceiling breach is silently missed. This was identified in iter1 and was not among the three mandated fixes. The `|| echo 0` fallback in the cost estimation step mitigates the data-computation path, not the breach-detection path.

2. **MC-12 (single-process container) reliance on Dockerfile (unchanged from iter1):** MC-12 is documented in workflow headers but its implementation lives in `docker/promptfoo/Dockerfile`, which is a Stream 3B deliverable outside this stream's scope. The workflow YAML cannot verify MC-12 in isolation.

**Improvement Path:**

Replace `2>/dev/null | grep -q "BREACH"` with an explicit subshell that handles Python failure gracefully: if the Python command fails, emit a warning rather than silently skipping the ceiling check.

---

### Evidence Quality (0.84/1.00)

**Evidence:**

The header-level FR and MC traceability documentation remains thorough and unchanged in quality from iter1 (all five deliverable files have structured FR/MC reference lists; inline step comments reference specific controls). This dimension was 0.84 in iter1 and the fixes did not address either of its gaps.

**Gaps:**

1. **Docker SHA placeholder credibility (unchanged and critical):** The SHA `sha256:4d8e9f6b2a1c3d5e7f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2` shows regularities inconsistent with real SHA-256 digests (sequential byte patterns: 4d, 8e, 9f, 6b, 2a, 1c, 3d, 5e, ...). This is the single most significant evidence quality gap. If this is a placeholder:
   - The evidence that MC-08 ("Docker image pinned to digest") is implemented is formal only — the pin references a non-existent image layer, making the digest pinning security control non-functional in practice.
   - Any reader attempting to verify MC-08 compliance by checking the digest against the registry would find the lookup fails.
   - The comment `# MC-08: Image pinned to SHA digest (not :latest)` is misleading because a non-existent digest provides no security.

2. **FR-022 (license verification) absence (unchanged from iter1):** No cross-reference to where FR-022 is addressed. Scope-appropriate for Stream 3E but unannounced.

3. **MC-19 implementation reference (unchanged from iter1):** MC-19 (API retry) is listed in headers but documented as residing in `deepeval_adapter.py`, which is outside Stream 3E's deliverable scope.

**Improvement Path:**

Replace the placeholder Docker SHA with the actual published digest for the target promptfoo version, and add a version comment (e.g., `# promptfoo v0.84.0, digest verified 2026-03-07`). This is the highest-impact improvement remaining and would allow this dimension to score 0.92+.

---

### Actionability (0.90/1.00)

**Evidence:**

The fixes improve actionability meaningfully. All five deliverable files are structurally valid and executionally correct:

- `uv run python` compliance is now uniform across all five files — the H-05 violation no longer creates a divergence between the runner's system Python version and the project's pinned UV-managed Python, eliminating a class of potential runtime failures.
- The smoke workflow `validate-yaml` step now correctly does not block PRs for missing test YAML, so the workflow executes according to its documented FR-027 behavior.
- All three main workflows handle all verdict cases (REGRESSION, MARGINAL, NO_REGRESSION, INSUFFICIENT_SAMPLES, ERROR/UNKNOWN) with appropriate exit codes.
- The artifact-publish action's agent identity resolution (agent_id primary, agent_name fallback), auto-discovery, tier-aware retention, and PR comment integration are all sound.

**Gaps:**

1. **`2>/dev/null` silent-failure risk in cost-monitor ceiling checks (unchanged):** As documented under Methodological Rigor, the ceiling breach detection can be silently swallowed if the Python command fails. This is a latent operational risk — the ceiling is not enforced in that failure path, though the failure mode is unlikely under normal conditions.

2. **Standard workflow FR-027 behavior difference (minor):** The Standard workflow's `validate-test-yaml-exists` step (lines 247–256 of `standard.yml`) uses `exit 1` for missing test YAML, making it a hard failure. This is intentional per the Standard tier's higher enforcement standard (Full tier also uses `exit 1`), and is consistent with FR-027's statement that the warning-only mode applies to the Smoke tier. The per-tier behavior is correct and internally consistent; this is not a gap.

**Improvement Path:**

Address the silent ceiling-check failure path in `cost-monitor/action.yml` with explicit Python error handling.

---

### Traceability (0.90/1.00)

**Evidence:**

Bidirectional FR/MC traceability unchanged in coverage from iter1 — all five files declare Stream 3E, list FR and MC references in headers, and reference controls inline. The fixes did not affect traceability structure.

**Gaps:**

1. **FR-019 module architecture trace indirect (unchanged from iter1):** FR-019 specifies `layer4_stats.py` must import from `stats.py` and not reimplement statistical logic. The workflows invoke `jerry.testing.layer4_stats` as a module — satisfying the invocation trace — but the internal module structure cannot be verified from workflow YAML alone. The traceability claim is structurally present but not demonstrable from the CI/CD deliverables.

2. **FR-001 test case YAML forward-reference only (unchanged from iter1):** Smoke and standard workflows reference FR-001 but the actual test case YAML files are Stream 3B deliverables. No cross-reference comment indicates which stream delivers FR-001 compliance.

**Improvement Path:**

Add comments in workflow headers cross-referencing FR-001 (Stream 3B) and FR-019 (Stream 3C) to complete the traceability chain without requiring readers to know the stream map from memory.

---

## Composite Calculation (Self-Review)

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.93 | 0.186 |
| Internal Consistency | 0.20 | 0.93 | 0.186 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.84 | 0.126 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **TOTAL** | **1.00** | | **0.909** |

**Arithmetic re-check:**
- 0.93 × 0.20 = 0.186
- 0.93 × 0.20 = 0.186
- 0.93 × 0.20 = 0.186
- 0.84 × 0.15 = 0.126
- 0.90 × 0.15 = 0.135
- 0.90 × 0.10 = 0.090
- Sum: 0.186 + 0.186 + 0.186 + 0.126 + 0.135 + 0.090 = **0.909**

**Score correction:** The mathematically precise composite is **0.909**, not 0.920 as stated in the L0 summary. The L0 summary contained an arithmetic error. The correct score is 0.909.

**Verdict adjustment:** 0.909 < 0.920 (H-13 baseline) and < 0.940 (stream threshold). Verdict is **REVISE**.

---

## Corrected Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | **0.909** |
| **Stream Threshold** | 0.94 (PASS) |
| **H-13 Threshold** | 0.92 |
| **Verdict** | **REVISE** — below H-13 baseline; stream gate not met |
| **Gap to H-13** | 0.011 |
| **Gap to stream** | 0.031 |

**Corrected L0 assessment:** The three mandated fixes are all confirmed present and correctly implemented. The pipeline score has improved from 0.848 to 0.909 (+0.061). The remaining gap to the stream threshold (0.031) is driven predominantly by the unaddressed Docker SHA placeholder (Evidence Quality held at 0.84) and the `2>/dev/null` silent-failure risk in ceiling checks. Addressing these two issues would bring Evidence Quality to ~0.91 and Actionability to ~0.93, yielding a projected composite of ~0.940 — on the stream threshold boundary.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.84 | 0.91+ | Replace placeholder Docker SHA (`sha256:4d8e9f6b...`) with the actual published digest for the target promptfoo version. Verify with `docker manifest inspect ghcr.io/promptfoo/promptfoo:<version> --format '{{json .Config.Digest}}'`. Add version string in comment (e.g., `# promptfoo v0.84.0, digest verified 2026-03-07`). Affects all three main workflow files. Impact on composite: ~+0.010. |
| 2 | Actionability + Methodological Rigor | 0.90 / 0.93 | 0.93+ | Add explicit error handling to `cost-monitor/action.yml` ceiling checks. Replace the `2>/dev/null \| grep -q "BREACH" && { ... }` pattern with: `BREACH_RESULT=$(uv run python -c "..." 2>&1); if echo "$BREACH_RESULT" \| grep -q "BREACH"; then ...`. If Python fails, emit `::warning::` rather than silently skipping. Impact on composite: ~+0.005. |
| 3 | Traceability | 0.90 | 0.92+ | Add stream cross-reference comments to workflow headers: "FR-001 test case YAML: Stream 3B deliverable" and "FR-019 stats.py shared module: Stream 3C deliverable". This closes the forward-reference gap without requiring readers to know the stream map. Impact on composite: ~+0.002. |

---

## Score Delta Analysis (Iter 1 → Iter 2)

| Dimension | Iter 1 | Iter 2 | Delta | Driver |
|-----------|--------|--------|-------|--------|
| Completeness | 0.82 | 0.93 | +0.11 | FR-023/H-05 cleared; FR-027 contradiction resolved |
| Internal Consistency | 0.83 | 0.93 | +0.10 | $20/$50 discrepancy fixed; FR-027 job consistency restored |
| Methodological Rigor | 0.86 | 0.93 | +0.07 | H-05 fully cleared across all five files |
| Evidence Quality | 0.84 | 0.84 | 0.00 | No fix applied to placeholder SHA or FR-022/MC-19 gaps |
| Actionability | 0.87 | 0.90 | +0.03 | H-05 compliance removes Python version risk; FR-027 behavior now correct |
| Traceability | 0.90 | 0.90 | 0.00 | No fix applied to forward-reference gaps |
| **Composite** | **0.848** | **0.909** | **+0.061** | |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file locations and line references
- [x] Uncertain scores resolved downward (Completeness/Internal Consistency/Methodological Rigor: chose 0.93 over 0.95 — the Docker SHA placeholder and `2>/dev/null` risk are not yet resolved; Evidence Quality: held at 0.84 — no fix applied, same substantive gap)
- [x] No dimension scored above 0.95 — highest are Completeness, Internal Consistency, Methodological Rigor at 0.93, reflecting fully resolved primary gaps with two secondary gaps remaining unaddressed
- [x] Arithmetic verified manually before persisting — discovered and corrected a 0.011 arithmetic error in the draft L0 summary (stated 0.920, correct is 0.909)
- [x] Fix verification performed before scoring — each of the three mandated fixes confirmed present in specific file lines before any dimension scores were assigned
- [x] New issues check performed — no new defects introduced by the three fixes

---

## Handoff Schema

```yaml
verdict: REVISE
composite_score: 0.909
threshold: 0.94
weakest_dimension: Evidence Quality
weakest_score: 0.84
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Replace placeholder Docker SHA in all three main workflows with actual published promptfoo image digest — eliminates the primary Evidence Quality gap (+0.010 projected composite impact)"
  - "Add explicit Python error handling to cost-monitor ceiling checks — prevents silent budget ceiling bypass on Python failure (+0.005 projected composite impact)"
  - "Add stream cross-reference comments to workflow headers for FR-001 (Stream 3B) and FR-019 (Stream 3C) (+0.002 projected composite impact)"
```
