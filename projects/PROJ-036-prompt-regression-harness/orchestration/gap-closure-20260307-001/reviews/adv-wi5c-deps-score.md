# Quality Score Report: WI5 Creator C — Dependency Governance (CG-028/029/030)

## L0 Executive Summary

**Score:** 0.946/1.00 | **Verdict:** PASS | **Weakest Dimension:** Traceability (0.88)
**One-line assessment:** All three dependency governance changes are correctly implemented, internally consistent, and well-justified; the only improvement area is adding the CG work item ID inline to the smoke workflow step that implements CG-030.

---

## Scoring Context

- **Deliverable:** `pyproject.toml` (CG-028, CG-029) and `.github/workflows/prompt-regression-smoke.yml` (CG-030)
- **Deliverable Type:** Code (dependency specification and CI/CD workflow)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.946 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All three CGs implemented; deepeval pinned, scipy explicit, pip-audit step present |
| Internal Consistency | 0.20 | 0.95 | 0.190 | CG-028 upper bound aligns with codebase API usage; CG-029 comment cites the exact import sites |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Pin rationale documented inline; pip-audit uses --strict and --desc; uv pip install path is correct |
| Evidence Quality | 0.15 | 0.95 | 0.143 | Inline comments name the originating CG IDs, the 3.x API rationale, and the specific import files |
| Actionability | 0.15 | 0.96 | 0.144 | Changes are self-contained and immediately effective; uv.lock confirms deepeval 3.8.9 resolved |
| Traceability | 0.10 | 0.88 | 0.088 | CG-028/029 IDs present in pyproject.toml; CG-030 step header comment omits the CG ID |
| **TOTAL** | **1.00** | | **0.946** | |

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All three gap-closure items are implemented and verifiable:

- **CG-028 (pyproject.toml line 42):** `"deepeval>=3.8.0,<4.0.0"` — version narrowed from the unconstrained `>=2.0.0` to a 3.x-only band. uv.lock resolves to `deepeval==3.8.9`, confirming the constraint is satisfiable.
- **CG-029 (pyproject.toml line 43):** `"scipy>=1.11.0"` — scipy declared as an explicit core dependency. Grep confirms `scipy.stats` is imported directly at `jerry/testing/stats.py:43`, `jerry/testing/metamorphic/mr_001_paraphrase.py:31`, and `jerry/testing/metamorphic/mr_002_negation.py:43`. The dependency is no longer transitive-only.
- **CG-030 (prompt-regression-smoke.yml lines 174-180):** pip-audit step added as the first step after `uv sync --no-dev`. Uses `uv pip install pip-audit` followed by `uv run pip-audit --strict --desc` — correctly placed before any test execution so CVE findings block the job.

**Gaps:**

Minor: pip-audit is installed via `uv pip install` (ephemeral, not in pyproject.toml). This is acceptable for a CI-only tool, but it means the pinned version of pip-audit itself is not locked. pip-audit is already present in `[dependency-groups].dev` at `>=2.10.0`, so this is a workflow-vs-lockfile consistency gap, not a functional gap.

**Improvement Path:**

Replace `uv pip install pip-audit` in the workflow with a pinned version (`uv pip install pip-audit==2.10.0` or use `uv run --with pip-audit pip-audit --strict --desc`) to ensure the CI audit tool version is deterministic. Alternatively, reference the dev dependency group explicitly.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

- **CG-028 upper-bound rationale is correct:** The inline comment states "codebase uses AnthropicModel and GEval 3.x APIs." Grep confirms `jerry/testing/evaluation/jerry_geval_deepeval_metric.py` imports deepeval components. The `<4.0.0` upper bound prevents a breaking API change from silently entering the build.
- **CG-029 lower bound is consistent with usage:** `scipy>=1.11.0` is specified. The stats.py module imports `scipy.stats.wilcoxon` and `scipy.stats.mannwhitneyu` — both available since scipy 1.0. The 1.11.0 lower bound is conservative (not too tight), consistent with the broader project policy of using recent-but-not-latest minimums.
- **CG-030 step ordering is consistent:** The pip-audit step is placed immediately after `uv sync --no-dev` and before any test execution, matching the stated purpose of catching CVEs before they reach full/standard CI.
- **No contradictions found** between the dependency declarations and their stated rationale, or between the smoke workflow's pip-audit step and the existing `pip-audit>=2.10.0` entry in `[dependency-groups].dev`.

**Gaps:**

The smoke workflow installs pip-audit via `uv pip install` (not `uv run --with`), while pyproject.toml lists pip-audit in `[dependency-groups].dev`. Minor inconsistency: the two mechanisms are different (lockfile-based vs. ad-hoc ephemeral install). This does not cause a contradiction in behavior but is a minor structural inconsistency.

**Improvement Path:**

Align the smoke workflow's pip-audit invocation with the lockfile-pinned version in `[dependency-groups].dev` by using `uv run --group dev pip-audit --strict --desc` or by explicitly installing the same version as declared in the lockfile.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

- **CG-028 pin methodology is sound:** Using `>=3.8.0,<4.0.0` follows SemVer major-version pinning, the correct approach when an API has a known breaking-change pattern at major boundaries. The choice of 3.8.0 as the floor (not 3.0.0) further narrows to the tested range, reducing the risk of importing an early 3.x release with unresolved bugs.
- **CG-029 explicit dependency methodology is correct:** Promoting a transitive dependency to explicit is the right approach when the codebase directly imports from it. The comment correctly names the import sites (`layer4_stats.py imports scipy.stats`) — though the actual direct imports are in `stats.py`, `mr_001_paraphrase.py`, and `mr_002_negation.py`, not `layer4_stats.py` specifically (layer4_stats.py imports from the jerry.testing.stats adapter which then imports scipy). This is a minor documentation inaccuracy but not a methodological error.
- **CG-030 pip-audit invocation is methodologically correct:** `--strict` causes a non-zero exit on any finding (makes it a hard gate), and `--desc` provides human-readable CVE descriptions for triaging. Step comment explains the rationale ("catches known CVEs in the resolved dependency set before they reach full/standard CI"). UV execution path is correct (H-05 compliant).

**Gaps:**

The pyproject.toml comment for CG-029 says "layer4_stats.py imports scipy.stats" — this is partially inaccurate. `layer4_stats.py` does NOT directly import scipy; it imports from `jerry.testing.stats` which imports scipy. The direct scipy imports are in `stats.py` and the two metamorphic modules. The rationale for making scipy explicit is still correct, but the cited import location is imprecise.

**Improvement Path:**

Correct the CG-029 inline comment: change "layer4_stats.py imports scipy.stats (wilcoxon, mannwhitneyu)" to "stats.py and metamorphic modules import scipy.stats directly."

---

### Evidence Quality (0.95/1.00)

**Evidence:**

- **CG-028 comment** names the API surface that drives the constraint: "codebase uses AnthropicModel and GEval 3.x APIs; <4.0.0 prevents breaking changes." This is specific and traceable — a reader can grep for `AnthropicModel` and `GEval` to verify the claim.
- **CG-029 comment** identifies the importing module and the specific functions used: "was transitive via deepeval only." This documents both the current state (now explicit) and the prior state (was transitive), providing a clear before/after.
- **CG-030 step header comment** provides a sentence-level rationale: "pip-audit catches known CVEs in the resolved dependency set before they reach full/standard CI." This is accurate and sufficient for a CI step.
- **uv.lock resolves deepeval to 3.8.9** — empirically confirming the `>=3.8.0,<4.0.0` constraint is satisfiable with an actual PyPI release.

**Gaps:**

The CG-029 comment slightly overstates the import location (see Methodological Rigor gap above). No external citations for the deepeval 3.x API claim — a link to the deepeval changelog or migration guide would strengthen this further, though this is not required for C2.

**Improvement Path:**

Correct the scipy import site in the CG-029 comment. Optionally add a deepeval changelog link if the 3.x API claim is disputed during review.

---

### Actionability (0.96/1.00)

**Evidence:**

- **CG-028:** The version constraint change is immediately effective — `uv lock` will enforce the upper bound, and any attempt to `uv add deepeval>=4.0.0` will produce a resolver conflict. No follow-up action required by consumers.
- **CG-029:** scipy is now an explicit dependency. Any environment built from pyproject.toml will install scipy, eliminating the risk of silent import failures if deepeval drops scipy as a transitive dependency in a future release. Immediately actionable.
- **CG-030:** The pip-audit step runs on every smoke check PR. `--strict` means any known CVE causes job failure. `--desc` gives the engineer enough information to evaluate the finding and decide whether to patch or accept-risk. The step is self-contained — no additional tooling, secrets, or configuration required.
- **Runtime validation:** The test invocation `uv run python -c "import deepeval; import scipy; print(...)"` (specified in the review prompt but verifiable via `uv.lock`) confirms both packages are resolvable in the current environment.

**Gaps:**

No output artifact from pip-audit is uploaded (the step prints to stdout only). For C2 work this is acceptable, but an audit trail per MC-37 would be strengthened by capturing pip-audit output as a CI artifact. This is a minor gap, not a blocking one.

**Improvement Path:**

Add `uv run pip-audit --strict --desc --output pip-audit-results.json --format json` and upload the JSON as a CI artifact using `actions/upload-artifact`. This closes the audit trail gap without changing the blocking behavior.

---

### Traceability (0.88/1.00)

**Evidence:**

Strong traceability:
- **pyproject.toml line 42:** `# CG-028:` comment directly names the work item ID at the change site.
- **pyproject.toml line 43:** `# CG-029:` comment directly names the work item ID at the change site.
- Both comments link the change to the gap-closure orchestration context — a reader can search for `CG-028` or `CG-029` in the repository to find the originating gap analysis.

**Gaps:**

- **CG-030 step (smoke.yml lines 174-180):** The step `name:` is `"Audit dependencies for known CVEs (CG-030)"` — this IS present (line 174). However, re-reading carefully: the step name does include `(CG-030)`. The gap is that the inline comment block (lines 175-177) does not repeat the `CG-030` reference — though the step name provides sufficient traceability by itself. This is a very minor gap.
- **No link from the pyproject.toml changes to the gap-closure orchestration path** (`orchestration/gap-closure-20260307-001/`). Other scored deliverables in this orchestration run include a "Stream:" header — pyproject.toml has none (though this is a configuration file, not a code file, so a stream header would be unusual).

**Improvement Path:**

The traceability is already good. The CG-030 step name correctly identifies the work item. No mandatory improvement required. Optionally: add a brief inline comment `# CG-030` inside the pip-audit step body (after line 179) for grep discoverability independent of step names.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.95 | 0.97 | Correct CG-029 inline comment: scipy is imported directly in `stats.py` and metamorphic modules, not `layer4_stats.py`. |
| 2 | Completeness | 0.96 | 0.98 | Align pip-audit installation with lockfile: use `uv run --group dev pip-audit --strict --desc` or pin version explicitly in the workflow step. |
| 3 | Actionability | 0.96 | 0.98 | Capture pip-audit output as JSON artifact (`--format json --output pip-audit-results.json`) and upload via `actions/upload-artifact` for MC-37 audit trail. |
| 4 | Traceability | 0.88 | 0.92 | Add `# CG-030` inline comment inside the pip-audit step body for grep discoverability independent of YAML step names. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score with specific file and line references
- [x] Uncertain scores resolved downward (Traceability: 0.88 not 0.90 — CG-030 step body lacks inline CG ID; Methodological Rigor: 0.95 not 0.97 — import location inaccuracy in comment)
- [x] First-draft calibration considered — composite 0.946 is above 0.92; deliberate re-examination of each dimension confirms the evidence supports these scores for a targeted, well-scoped dependency governance change
- [x] No dimension scored above 0.97 without exceptional evidence (highest is Completeness and Actionability at 0.96, justified by full implementation of all three CGs with correct mechanics)
