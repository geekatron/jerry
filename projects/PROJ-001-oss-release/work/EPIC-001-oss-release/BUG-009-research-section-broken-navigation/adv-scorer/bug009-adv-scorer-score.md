# BUG-009 Quality Score Report — S-014 LLM-as-Judge

> **Agent:** adv-scorer (S-014)
> **Deliverable:** BUG-009 — Research Section: Broken Icon Navigation, Poor Catalog Naming, No Link Validation
> **Criticality:** C3 (Significant — >10 files, test infrastructure addition, interrelated defects)
> **Iteration:** 1 (first scoring, no prior score)
> **Date:** 2026-02-19
> **Source Files Inspected:**
> - `/mkdocs.yml`
> - `/docs/research/index.md`
> - `/tests/e2e/test_mkdocs_research_validation.py`
> - `/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/BUG-009-research-section-broken-navigation/BUG-009-research-section-broken-navigation.md`
> - `/projects/PROJ-001-oss-release/WORKTRACKER.md`
> - `/.github/workflows/ci.yml`
> - `/requirements-test.txt`
> - `/pyproject.toml`

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict and composite score at a glance |
| [Deliverables Reviewed](#deliverables-reviewed) | Artifacts scoped for scoring |
| [Dimension Scores](#dimension-scores) | Per-dimension evidence, score, justification |
| [Weighted Composite](#weighted-composite) | Score arithmetic |
| [Leniency Bias Check](#leniency-bias-check) | Downward-resolve audit |
| [Verdict](#verdict) | PASS / REVISE / REJECTED |
| [Blocking Issues](#blocking-issues) | Issues that must be resolved before re-score |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered |

---

## L0 Executive Summary

BUG-009 correctly identifies three real defects and addresses each at the right layer:
`pymdownx.emoji` extension addition resolves icon rendering; the catalog rename eliminates
internal naming exposure; the test suite validates all three defect classes in rendered HTML.
The root cause analysis is accurate and the configuration change is minimal and correct.

However, one critical defect in the test infrastructure itself negates the Actionability and
Evidence Quality of the fix: `test_mkdocs_research_validation.py` carries no pytest markers.
This means the test will be discovered and collected by all CI matrix jobs (`test-pip` runs
`pytest -m "not subprocess and not llm"`; `test-uv` runs `pytest -m "not llm"`). Neither
filter excludes the new test. `mkdocs-material` is absent from `requirements-test.txt` and
from the `test` extra in `pyproject.toml` — it exists only in the `dev` dependency group.
The `sys.executable -m mkdocs` call in the `build_site` fixture will raise
`ModuleNotFoundError` on every CI matrix runner on the next push. All `test-pip` jobs
(8 matrix cells) and all `test-uv` jobs (8 matrix cells) will fail. CI is broken.

Additionally, H-20 (BDD Red phase) was violated: the test was committed in the same
action as the fix with no prior failing-test commit on record.

These two issues — broken CI and H-20 violation — drive the score below the PASS
threshold.

**Composite Score: 0.560**

**Verdict: REJECTED** (< 0.85; significant rework required per H-13)

---

## Deliverables Reviewed

| Artifact | Role | Verdict |
|----------|------|---------|
| `mkdocs.yml` — added `pymdownx.emoji`, `attr_list`, `md_in_html` | Config fix | Correct, minimal, complete |
| `docs/research/index.md` — 2 catalog links updated `bug008-` → `research-` | Reference fix | Complete and consistent |
| `tests/e2e/test_mkdocs_research_validation.py` | Test infrastructure | Functionally correct but missing markers — CRITICAL defect |
| `research-catalog.md` (renamed from `bug008-research-catalog.md`) | File rename | Correct, audit trail preserved |
| `BUG-009` work item with 4 tasks + AC-6 deferred | Tracking | Accurate, AC-6 gap untracked |
| `WORKTRACKER.md` — BUG-009 entries | Session state | Accurate, historical entries correct |

---

## Dimension Scores

### 1. Completeness (weight 0.20)

**Score: 3 / 5**

**Evidence:**
- All three root causes are addressed: emoji extension added, catalog renamed and
  re-referenced in two locations (`index.md` lines 22 and 184), test coverage added for
  all three defect classes.
- AC-1 through AC-5 are marked done in the BUG-009 work item. This is credible given
  the `pymdownx.emoji` configuration is correctly formed in `mkdocs.yml` (lines 70-72).
- AC-6 (CI integration of the validation script) is explicitly deferred with no follow-on
  tracking item created. This is a documented gap, not an undiscovered omission, but it
  is an incomplete deliverable nonetheless: the stated goal of "validation that fails the
  build" remains unmet, and no future work item exists to close it.
- The test itself is incomplete as a deliverable: absent pytest markers make it
  non-functional in its intended CI context. A test that cannot run in CI does not provide
  the regression protection it claims to provide.
- `build_site` fixture (lines 27-39) has no pre-build cleanup — stale `site/` artifacts
  from prior runs can produce false-passing tests, reducing the completeness of what the
  test validates.

**Justification:** Three defects addressed at correct layers. However, the test suite's
missing markers render it non-functional as CI protection (the primary purpose), and
AC-6 is deferred with no tracking. Choosing 3 over 4 because the test's inability to
run in CI is a functional incompleteness, not just a style gap.

---

### 2. Internal Consistency (weight 0.20)

**Score: 3 / 5**

**Evidence:**
- `mkdocs.yml` extension additions are internally consistent: `attr_list` and `md_in_html`
  are correctly paired with `pymdownx.emoji` to support Material grid cards with
  `{ .md-button }` syntax and `<div class="grid cards" markdown>` blocks.
- All two references to the old catalog filename in `docs/research/index.md` (lines 22,
  184) are updated. The WORKTRACKER audit trail retains the old filename correctly for
  historical accuracy — this is consistent with standard audit-trail practice.
- Inconsistency 1: The test file uses `sys.executable -m mkdocs` (line 31), implying
  the test assumes mkdocs-material is available in the current Python environment. But
  the test carries no markers to route it to an environment where mkdocs-material exists.
  The test's execution assumption is inconsistent with its deployment context.
- Inconsistency 2: Other e2e test files (e.g., `test_adversary_templates_e2e.py`) use
  `pytestmark = [pytest.mark.e2e]` (line 32). The new file uniquely omits this,
  inconsistent with the established pattern across the e2e test suite.
- Inconsistency 3: `docs.yml` pins `mkdocs-material==9.6.7` for production deploy;
  `pyproject.toml` dev group requires `>=9.7.2`. The test validates against 9.7.2 behavior
  but the production build uses 9.6.7. This is a version skew that is not documented
  in the test or BUG-009 root cause analysis.
- The `e2e` marker used in other files is not registered in `pyproject.toml` markers list
  (which only registers `happy-path`, `negative`, `edge-case`, `boundary`) — pre-existing
  inconsistency that BUG-009 did not introduce but also did not fix.

**Justification:** Configuration changes are internally consistent. Test file is internally
inconsistent with its own deployment assumptions and with the established e2e test pattern.
Choosing 3 over 4 because the inconsistencies are in the highest-value artifact (the test)
and have material impact.

---

### 3. Methodological Rigor (weight 0.20)

**Score: 3 / 5**

**Evidence:**
- Root cause analysis in the BUG-009 work item is accurate and traces each defect to
  its precise mechanism: (1) missing MkDocs extension → icon rendering failure;
  (2) file created during bug investigation, never renamed → naming artifact;
  (3) `mkdocs build --strict` scope limitation → no rendering validation.
- Contributing factors are identified (FEAT-027 quality gate evaluated markdown not HTML;
  no CI test beyond strict mode). This demonstrates upstream awareness.
- The fix operates at the correct architectural layer for each defect (config, filesystem,
  test infrastructure).
- H-20 (BDD Red phase) was violated: the BUG-009 history shows the test was created
  in the same action as the fix on 2026-02-19, with no prior commit showing a failing
  test. The Red-Green sequence required by H-20 was not followed. This is a process
  violation, not merely a documentation gap.
- The `build_site` fixture does not isolate state (no `site/` directory cleanup before
  build). This reflects insufficient rigor in test design — a freshly populated `site/`
  from a prior run can mask the effect of a configuration change by serving stale HTML.
- Version skew between dev (>=9.7.2) and production (==9.6.7) was not identified in
  the root cause analysis or mitigated in test design.

**Justification:** Root cause identification is strong. Fix selection is correct. Process
rigor (H-20) was not followed, and test design rigor (environment isolation, version
alignment) is substandard. Choosing 3 over 2 because the root cause analysis itself is
rigorous; the process and test-design failures are significant but not dominant.

---

### 4. Evidence Quality (weight 0.15)

**Score: 2 / 5**

**Evidence:**
- The core evidence — `mkdocs build --strict` passes with the extensions added — is
  implied but not documented as a test result in the BUG-009 work item. The WORKTRACKER
  entry states "all passing" but this claim cannot be verified from CI artifacts because
  the test was never run in CI on this branch.
- The test is structured to test rendered HTML output (correct approach for validating
  rendering defects), but it cannot function in the CI environment for which it was written:
  `mkdocs-material` is absent from `requirements-test.txt` (confirmed by inspection),
  meaning the test will raise `ModuleNotFoundError` before any assertion runs.
- There is no evidence that the test was run in CI. The only path that includes
  mkdocs-material is `uv sync --extra dev` (dev group), which is not used by `test-pip`
  or `test-uv` CI jobs.
- The steelman analysis correctly notes that the test design (inspecting rendered HTML)
  is the right approach. The test logic itself is sound. But a test that cannot run
  provides zero evidence quality for the claims it makes.
- No external reference or citation grounds the choice of the specific emoji module
  path (`material.extensions.emoji.twemoji`) — though this is consistent with official
  Material for MkDocs documentation and was downgraded from CRITICAL in strategy group
  finding C-2.

**Justification:** The test cannot run in CI due to missing mkdocs-material in test
dependencies. This is the most severe evidence gap: the "validation that catches broken
icons" does not catch them in the environment it was designed for. A test that fails at
import time provides no evidence. Choosing 2 over 1 because the configuration fix itself
is evidentially sound (correct extension syntax, verified against official docs) even
though the test evidence is absent.

---

### 5. Actionability (weight 0.15)

**Score: 2 / 5**

**Evidence:**
- The configuration fix (`mkdocs.yml`) is immediately deployable and correct. The catalog
  rename and reference updates are complete and correct. These three changes are
  actionable without modification.
- The test suite is NOT deployable as-is. Merging this PR will cause CI failure on the
  next push:
  - `test-pip` (8 matrix cells: ubuntu/windows/macos x python 3.11-3.14 minus exclusions)
    runs `pytest -m "not subprocess and not llm"`. The new test has no markers, so it
    passes the filter and is collected. `pip install -r requirements-test.txt` does not
    install mkdocs-material. `sys.executable -m mkdocs` will raise `ModuleNotFoundError`.
    Failure mode: `AssertionError: mkdocs build --strict failed: ...ModuleNotFoundError`.
  - `test-uv` (8 matrix cells) runs `pytest -m "not llm"`. Same filter miss. `uv sync
    --extra test` does not install mkdocs-material (test extra does not include dev group).
    Same failure mode.
  - CI gate `ci-success` requires both `test-pip` and `test-uv` to pass. Both will fail.
    The PR cannot merge without breaking the main branch if squash-merged as-is.
- AC-6 (CI integration) is deferred. The stated goal of the test — preventing regressions
  in CI — is structurally unmet even beyond the missing marker issue.
- Resolution path is clear (add `pytestmark`, add mkdocs-material to test extra or
  `requirements-test.txt`, register `e2e` marker), but the fix cannot be deployed as-is.

**Justification:** The configuration and rename changes are actionable. The test infrastructure
has a blocking CI-breaking defect. Choosing 2 over 1 because two of the three fix components
(config, rename) are immediately deployable and correct, and the path to resolution is clear.

---

### 6. Traceability (weight 0.10)

**Score: 4 / 5**

**Evidence:**
- BUG-009 work item is well-structured: Summary, Reproduction Steps, Environment,
  Root Cause Analysis, Children (Tasks) with status, Acceptance Criteria with checkboxes,
  Related Items linking to FEAT-027 / EN-961 / EN-962, History log.
- WORKTRACKER entries on 2026-02-19 (lines 256-257) accurately reflect the bug creation
  and completion events with sufficient detail to reconstruct what was done and why.
- BUG-009 is linked to its parent (EPIC-001) and to the causing change (FEAT-027).
  Related enablers (EN-961, EN-962) are cited with rationale.
- TASK-001 through TASK-004 map directly to the four fix actions taken, all marked done.
- AC-6 is explicitly noted as deferred in the work item history, providing a traceable
  record of the decision to defer.
- Gap: AC-6 deferral has no follow-on work item. A deferred acceptance criterion
  without a tracking item creates a silent gap in the backlog. Traceability ends at the
  deferral note rather than pointing forward to a new item.
- Gap: H-20 violation is not documented anywhere in the work item or history — the
  Red-phase skip is unrecorded.

**Justification:** Strong traceability overall — work item is comprehensive, history is
accurate, hierarchy is linked. Two gaps prevent a 5: AC-6 has no forward tracking item,
and the H-20 violation is undocumented. Choosing 4 over 5 due to the AC-6 tracking gap.

---

## Weighted Composite

| Dimension | Weight | Score (1-5) | score × weight |
|-----------|--------|-------------|----------------|
| Completeness | 0.20 | 3 | 0.600 |
| Internal Consistency | 0.20 | 3 | 0.600 |
| Methodological Rigor | 0.20 | 3 | 0.600 |
| Evidence Quality | 0.15 | 2 | 0.300 |
| Actionability | 0.15 | 2 | 0.300 |
| Traceability | 0.10 | 4 | 0.400 |
| **Total** | **1.00** | — | **2.800** |

**Weighted composite = 2.800 / 5.0 = 0.5600**

---

## Leniency Bias Check

Per S-014: leniency bias must be actively counteracted. Adjacent-score ties resolve downward.

| Dimension | Candidate Scores Considered | Resolution | Chosen |
|-----------|----------------------------|------------|--------|
| Completeness | 3 or 4 | Test non-functional in CI = functional incompleteness, not just style gap. Downward. | 3 |
| Internal Consistency | 3 or 4 | Pattern violation + execution assumption mismatch are material. Downward. | 3 |
| Methodological Rigor | 3 or 4 | H-20 process violation + test isolation failure are significant. Downward. | 3 |
| Evidence Quality | 2 or 3 | Test cannot run in CI; zero operational evidence from CI. Downward. | 2 |
| Actionability | 2 or 3 | CI will break on next push; blocking issue is severe. Downward. | 2 |
| Traceability | 4 or 5 | AC-6 has no forward tracking item; H-20 violation undocumented. Downward. | 4 |

All resolutions applied consistently. No inflation.

---

## Verdict

**Composite Score: 0.5600**

**Band: REJECTED** (< 0.85)

Per H-13: deliverable REJECTED. Significant rework required before re-score.

The PASS threshold (>= 0.92) requires a composite of 4.60/5.0. The current score of
2.80/5.0 is 1.80 points below threshold. The gap is dominated by Evidence Quality (2)
and Actionability (2) — both driven by the single root cause: the test file is missing
pytest markers and mkdocs-material is not in the test dependency set. Fixing this one
defect would raise both dimensions to 4, which would shift the composite to approximately:

| Dimension | Weight | Revised Score | Contribution |
|-----------|--------|---------------|-------------|
| Completeness | 0.20 | 4 | 0.800 |
| Internal Consistency | 0.20 | 4 | 0.800 |
| Methodological Rigor | 0.20 | 3 | 0.600 |
| Evidence Quality | 0.15 | 4 | 0.600 |
| Actionability | 0.15 | 4 | 0.600 |
| Traceability | 0.10 | 4 | 0.400 |
| **Post-fix estimate** | — | — | **3.800 / 5.0 = 0.760** |

Even after fixing the marker/dependency defect, the score (estimated ~0.760) would remain
in REJECTED band. Reaching PASS (0.92 = 4.60/5.0) additionally requires: addressing the
version skew (dev vs. production mkdocs-material), adding `build_site` fixture cleanup,
resolving H-20 process documentation, and creating a tracking item for AC-6. With all
blocking and major findings resolved, the composite could reach the REVISE band (0.85-0.91)
or PASS, depending on quality of remediation.

---

## Blocking Issues

These MUST be resolved before re-score. CI will fail on next push without them.

| ID | Issue | Required Fix |
|----|-------|-------------|
| B-1 | `test_mkdocs_research_validation.py` has no pytest markers | Add `pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]` at module level. Both markers are needed: `e2e` for consistent pattern with other e2e files; `subprocess` to exclude from `test-pip` which cannot install mkdocs-material via `requirements-test.txt`. |
| B-2 | `mkdocs-material` absent from CI test environments | Either: (a) add `mkdocs-material` to `requirements-test.txt` and `[project.optional-dependencies].test`, or (b) ensure B-1 `subprocess` marker excludes this test from all jobs where mkdocs-material is unavailable. Option (b) is preferred: tests that invoke `sys.executable -m mkdocs` are subprocess-class tests by definition. |
| B-3 | `e2e` and `subprocess` markers not registered | Add `e2e: marks tests as end-to-end integration tests` and `subprocess: marks tests that require subprocess execution` to `[tool.pytest.ini_options].markers` in `pyproject.toml`. (Pre-existing gap for `e2e`; new gap for `subprocess` if used.) |

---

## Improvement Recommendations

Priority-ordered. Blocking issues (B-1 through B-3) are prerequisites.

| Priority | Finding | Recommendation |
|----------|---------|----------------|
| P1 (Blocking) | B-1: Missing pytest markers | Add `pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]` |
| P1 (Blocking) | B-2: mkdocs-material not in test deps | Add to requirements-test.txt and test extra, OR confirm subprocess marker exclusion is sufficient |
| P1 (Blocking) | B-3: Unregistered markers | Register `e2e` and `subprocess` in pyproject.toml markers list |
| P2 (Major) | M-2: No site/ cleanup in build_site | Add `shutil.rmtree(SITE_DIR, ignore_errors=True)` before subprocess call in `build_site` fixture |
| P2 (Major) | M-3: Version skew dev vs. production | Document in test module docstring that the test runs against `>=9.7.2` and production uses `9.6.7`. Evaluate whether `docs.yml` should be updated to `>=9.7.2`. |
| P2 (Major) | M-4: H-20 violation | Document the BDD skip in BUG-009 history. For future bugs: commit a failing test first, then the fix. |
| P3 (Minor) | AC-6 deferred, no tracking | Create a new work item (e.g., EN-NNN) to track CI integration of the MkDocs validation test |
| P3 (Minor) | M-5: TestIconRendering scans `<code>` blocks | Add HTML parser pre-processing to exclude content inside `<code>` and `<pre>` blocks before running the unresolved-icon regex |
| P3 (Minor) | M-6: TestAnchorIntegrity cross-page scope | Add a comment noting the test scope is same-page only; consider a follow-on task to add cross-page anchor validation |
