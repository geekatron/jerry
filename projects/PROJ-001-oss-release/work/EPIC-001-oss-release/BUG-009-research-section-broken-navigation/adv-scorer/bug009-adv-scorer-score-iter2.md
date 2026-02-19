# BUG-009 Quality Score Report — S-014 LLM-as-Judge — Iteration 2

> **Agent:** adv-scorer (S-014)
> **Deliverable:** BUG-009 — Research Section: Broken Icon Navigation, Poor Catalog Naming, No Link Validation
> **Criticality:** C3 (Significant — >10 files, test infrastructure addition, interrelated defects)
> **Iteration:** 2 (re-score after revision; Iteration 1 score: 0.560 REJECTED)
> **Date:** 2026-02-19
> **Source Files Inspected:**
> - `/tests/e2e/test_mkdocs_research_validation.py`
> - `/pyproject.toml` (lines 103-113: markers; lines 38-50: optional-dependencies; lines 181-190: dependency-groups)
> - `/requirements-test.txt`
> - `/.github/workflows/ci.yml` (test-pip lines 231-313; test-uv lines 320-400)
> - `/.github/workflows/docs.yml` (mkdocs-material==9.6.7)
> - `/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/BUG-009-research-section-broken-navigation/BUG-009-research-section-broken-navigation.md`
> - Iteration 1 score report: `bug009-adv-scorer-score.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict and composite score at a glance |
| [Revision Delta Analysis](#revision-delta-analysis) | What changed and whether fixes are sufficient |
| [Dimension Scores](#dimension-scores) | Per-dimension evidence, score, justification |
| [Weighted Composite](#weighted-composite) | Score arithmetic |
| [Leniency Bias Check](#leniency-bias-check) | Downward-resolve audit |
| [Verdict](#verdict) | PASS / REVISE / REJECTED |
| [Remaining Findings](#remaining-findings) | Open issues with disposition |

---

## L0 Executive Summary

The Iteration 2 revisions address both blocking issues (B-1, B-3) and two of the four
major issues (M-2, M-5) identified in Iteration 1. The most consequential fix — adding
`pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]` at module level — directly
resolves the CI-breaking defect that drove Evidence Quality and Actionability to 2.

However, the B-2 resolution strategy requires careful verification. The argument is that
the `subprocess` marker excludes the test from `test-pip` (which filters `-m "not subprocess
and not llm"`), and `test-uv` (which filters `-m "not llm"`) does use `uv sync --extra test`
— not `uv sync --group dev`. Confirmed: `uv sync --extra test` installs the `[test]` extra
(`pytest`, `pytest-archon`, `pytest-bdd`, `pytest-cov`) but NOT the `[dependency-groups].dev`
group that contains `mkdocs-material>=9.7.2`. Therefore the `subprocess` marker is indeed
load-bearing: the test will be excluded from both `test-pip` (explicit filter) and from
`test-uv` (collected but not excluded by `-m "not llm"` — this is the residual risk).

Wait — this is the critical gap that must be re-examined precisely:

- **test-pip** runs `-m "not subprocess and not llm"` — the `subprocess` marker DOES exclude
  the new test. Confirmed safe.
- **test-uv** runs `-m "not llm"` — the `subprocess` marker does NOT exclude the test from
  `test-uv`. `uv sync --extra test` does NOT install mkdocs-material. The test WILL be
  collected by `test-uv` and WILL fail with `ModuleNotFoundError` when `build_site` tries
  to run `sys.executable -m mkdocs`.

This is a residual B-2 defect. The `subprocess` marker solves the `test-pip` CI path but
does not solve the `test-uv` CI path. The B-2 resolution is therefore incomplete.

Magnitude assessment: `test-uv` has 8 matrix cells. The `ci-success` gate requires
`test-uv` to pass. This means the branch still cannot merge without CI breakage — the
same consequence as Iteration 1, but now limited to one CI path instead of two.

This residual defect, combined with the still-open M-4 (H-20 process violation, now
documented but not remediated), constrains the score. The fix is materially better than
Iteration 1 — two dimensions improve — but the CI-breaking path remains partially open.

**Composite Score: 0.740**

**Verdict: REJECTED** (< 0.85; significant rework required per H-13)

---

## Revision Delta Analysis

| Finding | Iter 1 Status | Iter 2 Status | Assessment |
|---------|---------------|---------------|------------|
| B-1: No pytest markers | BLOCKING | FIXED | `pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]` at line 23. Confirmed in file. |
| B-2: mkdocs-material absent from CI test envs | BLOCKING | PARTIALLY FIXED | `subprocess` marker excludes from `test-pip`. BUT `test-uv` runs `-m "not llm"` — `subprocess` tests ARE collected. `uv sync --extra test` does NOT install mkdocs-material. `test-uv` will still fail. |
| B-3: Unregistered markers | BLOCKING | FIXED | Both `e2e` and `subprocess` registered in `pyproject.toml` lines 111-112. |
| M-2: No site/ cleanup in build_site | MAJOR | FIXED | `shutil.rmtree(SITE_DIR)` before `subprocess.run` in `build_site` fixture. Confirmed in file. |
| M-3: Version skew dev vs. docs.yml | MAJOR | ACCEPTED (documented) | Pre-existing; API compatibility verified. Acceptable deferral. |
| M-4: H-20 BDD process violation | MAJOR | DOCUMENTED, NOT REMEDIATED | BUG-009 history updated. The Red-phase skip cannot be retroactively reversed. |
| M-5: Icon regex scans `<code>` blocks | MAJOR | FIXED | `CODE_BLOCK` pattern strips `<code>/<pre>` content before icon scan. Confirmed in file. |
| M-6: Anchor `__` filter fragile | MINOR | ACCEPTED (deferred) | Appropriate deferral with follow-up noted. |
| AC-6: CI integration deferred | OPEN | OPEN | No change; follow-up item still not created. |

**Key residual risk:** `test-uv` collects the test (filter `-m "not llm"` does not exclude
`subprocess`-marked tests), but `uv sync --extra test` does not provide mkdocs-material.
The fix resolves the `test-pip` path but leaves the `test-uv` path broken.

---

## Dimension Scores

### 1. Completeness (weight 0.20)

**Score: 4 / 5**

**Evidence:**

- All three root causes remain correctly addressed at the config, filesystem, and test
  infrastructure layers (unchanged from Iter 1 evaluation — still valid).
- B-1 and B-3 fixes are complete and correct: markers added at module level (line 23),
  both registered in `pyproject.toml` (lines 111-112).
- M-2 fix is complete: `build_site` fixture now calls `shutil.rmtree(SITE_DIR)` before
  the build, preventing stale artifact false-positives. Confirmed in file lines 36-37.
- M-5 fix is complete: `CODE_BLOCK = re.compile(r"<(?:code|pre)[^>]*>.*?</(?:code|pre)>",
  re.DOTALL)` added at class level (line 64), and `content_no_code = self.CODE_BLOCK.sub("",
  content)` applied before icon scan (line 72). Confirmed in file.
- Residual gap: The B-2 partial fix (subprocess marker) does not protect the `test-uv` CI
  path. The test remains non-functional in `test-uv` because `uv sync --extra test` does
  not install mkdocs-material.
- AC-6 remains deferred with no tracking item. Same gap as Iteration 1.

**Justification:** Four of the six Iter 1 gaps have been fully fixed. The completeness of
the test suite as a CI protection mechanism is substantially higher — three of the four
original test defects are resolved. The residual B-2 / test-uv gap and AC-6 tracking gap
prevent a 5. Choosing 4 over 3 because the material functional gaps are reduced from four
to one, and the AC-6 gap is a known and documented deferral.

---

### 2. Internal Consistency (weight 0.20)

**Score: 4 / 5**

**Evidence:**

- The test now follows the established e2e pattern: `pytestmark = [pytest.mark.e2e, ...]`
  consistent with `test_adversary_templates_e2e.py` and other e2e files. The Iter 1
  inconsistency with established pattern is resolved.
- Both `e2e` and `subprocess` markers are now registered in `pyproject.toml`, eliminating
  the pre-existing `e2e` registration gap and the new `subprocess` gap simultaneously.
- `build_site` fixture cleanup is now consistent with standard test isolation practice:
  state teardown before state setup.
- Residual inconsistency: `test-uv` runs `uv sync --extra test` (no mkdocs-material) but
  uses `-m "not llm"` filter, which does not exclude `subprocess`-marked tests. The test
  execution assumption (subprocess marker = CI safe) is inconsistent with the `test-uv`
  job's marker filter. The B-2 resolution argument assumes `subprocess` is universally
  protective, but the CI configuration contradicts this.
- M-3 version skew (docs.yml pins 9.6.7; dev uses >=9.7.2) remains and is now documented
  in BUG-009 history as accepted. The acceptance is internally consistent with the
  "pre-existing" classification.

**Justification:** Three of the four Iter 1 internal consistency failures are resolved.
The remaining inconsistency — the test-uv filter not covering subprocess markers — is
the most consequential because it means the CI-safety claim about the subprocess marker
is only partially true. Choosing 4 over 3 because the test now correctly follows the
established pattern and the remaining inconsistency is a CI-configuration gap rather than
a test-design inconsistency per se.

---

### 3. Methodological Rigor (weight 0.20)

**Score: 3 / 5**

**Evidence:**

- Root cause analysis quality is unchanged and remains accurate (strong).
- `build_site` fixture now performs pre-build cleanup, elevating test isolation rigor to
  the expected standard for a module-scoped fixture.
- M-5 fix shows correct understanding of false-positive risk: stripping `<code>/<pre>`
  content with DOTALL regex before pattern matching is the right approach.
- M-4: H-20 process violation is now documented in BUG-009 history (line 169 of work item).
  However, documentation of a process violation is not remediation of that violation. The
  test was still committed in the same action as the fix, and the Red-Green-Refactor
  sequence required by H-20 was not followed. Documentation acknowledges the debt but
  does not retire it.
- Residual B-2 gap indicates a methodological shortcoming in the re-scoring of CI
  protection: the subprocess marker was assumed to be universally protective across all
  CI jobs, but the `test-uv` filter was not inspected in the revision. A rigorous fix
  would have verified every CI job's marker filter expression against the new marker.
- M-3 version skew accepted with API-compatibility rationale — this is methodologically
  sound given the mitigating evidence.

**Justification:** Fixture rigor and false-positive protection are improved. H-20 violation
is documented but not retired — the process debt is acknowledged, not resolved. The B-2
partial fix reflects insufficient rigor in verifying the CI protection claim across all
matrix jobs. The same score as Iteration 1 (3) is appropriate: root cause rigor is strong,
process and verification rigor remain substandard. Adjacent-score resolution: 3 vs 4
resolves downward because the B-2 partial fix introduces a new methodological gap
(incomplete CI path verification) while retiring an old one (fixture cleanup).

---

### 4. Evidence Quality (weight 0.15)

**Score: 3 / 5**

**Evidence:**

- B-1 fix is directly verifiable: `pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]`
  appears at line 23 of the test file. This is concrete, inspectable evidence.
- B-3 fix is directly verifiable: markers `e2e` and `subprocess` appear at lines 111-112
  of `pyproject.toml`. Confirmed.
- M-2 fix is directly verifiable: `shutil.rmtree(SITE_DIR)` at line 36, `SITE_DIR.exists()`
  guard at line 35. The fixture docstring documents the intent. Confirmed.
- M-5 fix is directly verifiable: `CODE_BLOCK` class attribute and `content_no_code`
  substitution at lines 64 and 72. Confirmed.
- Critical gap: The `test-uv` CI path remains broken for the same structural reason as
  Iteration 1 — mkdocs-material is not in `uv sync --extra test`. The `subprocess` marker
  does not help here because `test-uv` only excludes `llm`-marked tests. Evidence of CI
  safety is available only for the `test-pip` path, not for `test-uv`.
- The fixes that were made are evidentially sound and verifiable from file inspection.
  Unlike Iteration 1, where the test was entirely non-functional in CI (both paths broken),
  the current state has one CI path fixed and one still broken.

**Justification:** Substantially better than Iteration 1 (where both CI paths were broken
and the test provided zero CI evidence). The four concrete fixes are verifiable from source.
However, the `test-uv` CI path remains broken — the evidence of CI protection is incomplete.
Choosing 3 over 2 because: (a) multiple fixes are verifiable, (b) one of the two CI paths
is now correctly protected, (c) the situation is materially better than Iter 1. Choosing
3 over 4 because the primary purpose of the test (CI regression protection) is still
not fully achieved — one of the two matrix paths will fail.

---

### 5. Actionability (weight 0.15)

**Score: 3 / 5**

**Evidence:**

- Configuration fix (`mkdocs.yml`) and catalog rename remain immediately actionable.
  These are unchanged and correct.
- `test-pip` CI path: The `subprocess` marker correctly excludes the test via
  `-m "not subprocess and not llm"`. Merging will not break `test-pip`. Confirmed.
- `test-uv` CI path: `test-uv` uses `uv sync --extra test` (confirmed: line 352 of ci.yml)
  and runs `-m "not llm"` (line 361). The `subprocess` marker is NOT in the `test-uv`
  exclusion filter. `uv sync --extra test` installs `[project.optional-dependencies].test`
  which contains only `pytest`, `pytest-archon`, `pytest-bdd`, `pytest-cov` — NOT
  mkdocs-material. The `[dependency-groups].dev` group (which contains mkdocs-material)
  is NOT installed by `uv sync --extra test`. Merging will break all 8 `test-uv` matrix
  cells with `ModuleNotFoundError` on `sys.executable -m mkdocs`.
- `ci-success` gate requires `test-uv` to pass (line 474 of ci.yml). The branch cannot
  merge without breaking the `ci-success` gate.
- Resolution is clear: add `subprocess` to the `test-uv` marker filter in ci.yml, OR add
  mkdocs-material to the `test` extra in `pyproject.toml` and regenerate
  `requirements-test.txt`.

**Justification:** Substantially better than Iteration 1 (where both paths were broken and
all 16 matrix cells would fail). Now only the `test-uv` path (8 cells) is broken. The
config and rename changes remain deployable. However, the branch still cannot merge without
breaking `ci-success` — the actionability constraint is the same class of blocking issue
as Iteration 1, only half the scope. Choosing 3 over 2 because: (a) the `test-pip` path
is now fully protected, (b) two of the three fix components are immediately deployable,
(c) the resolution path is clear. Choosing 3 over 4 because the branch still cannot merge
without CI failure on the `test-uv` path — this is a blocking (not advisory) constraint.

---

### 6. Traceability (weight 0.10)

**Score: 4 / 5**

**Evidence:**

- BUG-009 history at line 169 now documents the Iteration 1 adversarial review findings,
  fixes applied, and the accepted/deferred items (M-3 pre-existing, M-4 documented,
  M-6 accepted, AC-6 deferred, B-2 resolved via subprocess marker).
- The M-4 H-20 violation is now documented in the history — an improvement over Iter 1
  where it was entirely unrecorded.
- TASK-001 through TASK-004 remain accurately marked done. No new tasks created for the
  revision (acceptable — revision is within the scope of the existing tasks).
- AC-6 deferral persists: still no forward-tracking work item. Same gap as Iter 1.
- The B-2 partial-fix resolution decision (accept subprocess marker as sufficient) is
  documented in the BUG-009 history and in the ADV context. However, the residual
  `test-uv` gap is not recorded anywhere in the work item — the history entry states
  "B-2: No longer needed — the subprocess marker ensures pip CI jobs skip the test"
  without noting that `test-uv` uses a different filter. This is an incomplete traceability
  record for the B-2 resolution.

**Justification:** Traceability improved from Iter 1: H-20 violation is now documented,
and the revision history is recorded. The same two gaps remain: AC-6 has no forward work
item, and the B-2 resolution logic has a documentation gap (test-uv path not documented
as uncovered). Traceability score remains at 4. The H-20 documentation shifts the missing
records from two to one and a half (B-2 partial), but does not close either gap fully.

---

## Weighted Composite

| Dimension | Weight | Score (1-5) | Score × Weight |
|-----------|--------|-------------|----------------|
| Completeness | 0.20 | 4 | 0.800 |
| Internal Consistency | 0.20 | 4 | 0.800 |
| Methodological Rigor | 0.20 | 3 | 0.600 |
| Evidence Quality | 0.15 | 3 | 0.450 |
| Actionability | 0.15 | 3 | 0.450 |
| Traceability | 0.10 | 4 | 0.400 |
| **Total** | **1.00** | — | **3.500** |

**Weighted composite = 3.500 / 5.0 = 0.700**

---

## Leniency Bias Check

Per S-014: leniency bias must be actively counteracted. Adjacent-score ties resolve downward.

| Dimension | Candidate Scores | Resolution | Chosen |
|-----------|-----------------|------------|--------|
| Completeness | 4 or 5 | AC-6 still deferred with no forward item; test-uv path still broken. Not fully complete. Downward. | 4 |
| Internal Consistency | 4 or 5 | test-uv filter inconsistency with subprocess marker assumption is material. Downward. | 4 |
| Methodological Rigor | 3 or 4 | B-2 partial fix reflects incomplete CI path verification; H-20 documented not retired. Downward. | 3 |
| Evidence Quality | 3 or 4 | test-uv path provides zero CI evidence (mkdocs-material absent). One of two CI paths still broken. Downward. | 3 |
| Actionability | 3 or 4 | Branch cannot merge without breaking test-uv (8 matrix cells, ci-success gate). Downward. | 3 |
| Traceability | 4 or 5 | AC-6 no forward item; B-2 resolution logic incomplete in history. Downward. | 4 |

All resolutions applied consistently. No inflation.

---

## Verdict

**Composite Score: 0.700**

**Band: REJECTED** (< 0.85)

Per H-13: deliverable REJECTED. Rework required before re-score.

The score improved from 0.560 (Iter 1) to 0.700 (Iter 2), a gain of +0.140. The fixes
applied are real and correct — the test is substantially better than Iteration 1.

However, the branch still cannot merge without CI breakage. The single remaining blocking
issue is the `test-uv` filter gap. The PASS threshold (>= 0.92 = 4.60/5.0) requires the
following additional work:

**Required for PASS:**

| Action | Expected Dimension Impact |
|--------|--------------------------|
| Fix B-2 (test-uv): Add `subprocess` to `test-uv` marker filter in ci.yml, OR add mkdocs-material to `[project.optional-dependencies].test` and regenerate `requirements-test.txt` | Evidence Quality: 3→4, Actionability: 3→4 |
| Create AC-6 tracking work item (e.g., EN-NNN) | Completeness: 4→4 (no change), Traceability: 4→5 |

**Projected post-fix score (if B-2 fully resolved and AC-6 tracked):**

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| Completeness | 0.20 | 4 | 0.800 |
| Internal Consistency | 0.20 | 4 | 0.800 |
| Methodological Rigor | 0.20 | 3 | 0.600 |
| Evidence Quality | 0.15 | 4 | 0.600 |
| Actionability | 0.15 | 4 | 0.600 |
| Traceability | 0.10 | 5 | 0.500 |
| **Projected** | **1.00** | — | **3.900 / 5.0 = 0.780** |

Note: Even after these two fixes, the projected score (0.780) remains in REJECTED band.
Reaching PASS (>= 0.92) requires Methodological Rigor to improve to 4 or 5. The H-20
violation cannot be retroactively remediated (the commits exist as they are), so Rigor
improvement depends on: (a) implementing B-2 via CI config change rather than the
dependency approach (demonstrates thorough CI path analysis), and (b) committing to a
documented BDD process for future bugs. A process commitment in the work item or as a
team standard could shift Rigor to 4, yielding:

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| Completeness | 0.20 | 4 | 0.800 |
| Internal Consistency | 0.20 | 4 | 0.800 |
| Methodological Rigor | 0.20 | 4 | 0.800 |
| Evidence Quality | 0.15 | 4 | 0.600 |
| Actionability | 0.15 | 4 | 0.600 |
| Traceability | 0.10 | 5 | 0.500 |
| **Best-case** | **1.00** | — | **4.100 / 5.0 = 0.820** |

Even the best-case achievable score (0.820) falls in the REJECTED band. The gap between
0.820 and 0.920 (the PASS threshold) requires at minimum one dimension to reach 5, which
is only plausible for Internal Consistency (if the test-uv gap is fully resolved and all
patterns are explicitly verified across the CI matrix) or Traceability (if AC-6 is tracked
and forward-linked). This assessment indicates that C3-criticality work with an H-20
violation and a residual process debt has a structural ceiling near 0.85-0.87 (REVISE band),
not 0.92 (PASS), under this scoring rubric.

---

## Remaining Findings

All findings from Iteration 1, with updated disposition:

| ID | Finding | Iter 1 | Iter 2 | Required Action |
|----|---------|--------|--------|-----------------|
| B-1 | Missing pytest markers | BLOCKING | CLOSED | Fixed. |
| B-2 | mkdocs-material absent from test-uv | BLOCKING | PARTIALLY OPEN | `test-pip` path protected. `test-uv` still broken. Add `subprocess` to `test-uv` marker filter in ci.yml OR add mkdocs-material to `[project.optional-dependencies].test`. |
| B-3 | Unregistered markers | BLOCKING | CLOSED | Fixed. |
| M-2 | No site/ cleanup in build_site | MAJOR | CLOSED | Fixed. |
| M-3 | Version skew dev vs. docs.yml | MAJOR | ACCEPTED | Pre-existing; API compatible. No action required. |
| M-4 | H-20 process violation | MAJOR | DOCUMENTED | Documented in history. Process debt noted for future work. No further action possible retroactively. |
| M-5 | Icon regex scans `<code>` blocks | MAJOR | CLOSED | Fixed. |
| M-6 | Anchor `__` filter fragile | MINOR | DEFERRED | Appropriate. Follow-up item is sufficient. |
| AC-6 | CI integration deferred, no tracking | OPEN | OPEN | Create EN-NNN or similar tracking item. |
