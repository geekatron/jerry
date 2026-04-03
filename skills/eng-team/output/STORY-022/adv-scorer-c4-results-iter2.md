# Quality Score Report: STORY-022 -- P-003 Agent Tool CI Validation (Iteration 2)

## L0 Executive Summary
**Score:** 0.88/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.85)
**One-line assessment:** The HIGH security finding (string-format tools bypass) and AC-2 gap are both resolved in this iteration, raising the composite from 0.82 to 0.88 -- but four gaps block the 0.95 C4 threshold: test discovery (tests not in CI testpaths), story admin status not updated, FINDING-004 unresolved, and no machine-readable evidence artifacts.

---

## Scoring Context
- **Deliverable:** STORY-022 implementation (Iteration 2): `scripts/validate-agent-frontmatter.py`, `scripts/tests/test_validate_agent_frontmatter.py`, `.github/workflows/ci.yml`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.82 (Iteration 1, REVISE)
- **Scored:** 2026-03-29T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.88 |
| **Threshold** | 0.95 (C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes -- eng-security 7 findings (3 HIGH/MEDIUM remediated, 2 remaining, 2 INFO confirmed clean); Iteration 1 adv-scorer 6 recommendations (AC-2 gap closed) |

---

## Delta from Iteration 1

| Dimension | Iter 1 Score | Iter 2 Score | Delta | Driver |
|-----------|-------------|-------------|-------|--------|
| Completeness | 0.72 | 0.88 | +0.16 | AC-2 closed: CI line 213 invokes script directly |
| Internal Consistency | 0.82 | 0.88 | +0.06 | CLI/script split contradiction resolved |
| Methodological Rigor | 0.88 | 0.88 | 0.00 | FINDING-001 test added; test discovery gap persists |
| Evidence Quality | 0.87 | 0.87 | 0.00 | Remediation traceable; AC-3 evidence gap persists |
| Actionability | 0.80 | 0.90 | +0.10 | Primary blocker resolved; remaining items are improvements |
| Traceability | 0.88 | 0.85 | -0.03 | Story ACs still all unchecked after explicit Iter 1 recommendation |
| **Composite** | **0.82** | **0.88** | **+0.06** | |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | AC-1/AC-2/AC-3 all substantively met; test discovery gap and FINDING-004 unresolved |
| Internal Consistency | 0.20 | 0.88 | 0.176 | CLI/script contradiction resolved; story "pending" with all ACs unchecked is minor inconsistency |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | 6 BDD tests, HIGH finding remediated with test; scripts/tests/ not in testpaths |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | Remediation traceable to eng-security findings; no machine-readable AC-3 artifact |
| Actionability | 0.15 | 0.90 | 0.135 | Deliverable is now mergeable; remaining items are well-described improvements |
| Traceability | 0.10 | 0.85 | 0.085 | Strong inline citations; story AC checkboxes not updated per Iter 1 recommendation |
| **TOTAL** | **1.00** | | **0.878** | |

> **Note on rounding:** Raw composite is 0.8785; reported as 0.88.

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

AC-1 (error if Agent in non-T5 tools): Met and now robust. Lines 143-178 of `scripts/validate-agent-frontmatter.py` implement the check. String normalization at lines 146-147 (`if isinstance(tools, str): tools = [t.strip() for t in tools.split(",") if t.strip()]`) closes the HIGH bypass found in eng-security FINDING-001. The `isinstance(tier, str) and tier == "T5"` guard at line 170 closes FINDING-003. Fail-closed behavior on missing governance confirmed.

AC-2 (CI runs check on every PR): Met. `.github/workflows/ci.yml` line 213 adds `uv run python scripts/validate-agent-frontmatter.py` as a second step in the `frontmatter-validation` job. The step comment "Validate P-003 Agent tool restriction (STORY-022)" is specific and traceable. This directly invokes the script -- the check will run on every PR touching the repo.

AC-3 (89 agents pass): Substantively met. The logic is correct and the 89/89 pass claim is consistent with the implementation (the check only errors on delegation_tools in non-T5 agents, and no existing agent has this combination). However, no machine-readable CI output artifact is provided.

**Gaps:**

The 6 tests in `scripts/tests/test_validate_agent_frontmatter.py` are not discovered by the standard `pytest` invocation. `pyproject.toml` at `[tool.pytest.ini_options]` sets `testpaths = ["tests"]`. The CI test matrix (`uv run pytest -m "not llm and not subprocess"`) picks up only the `tests/` directory. The 6 STORY-022 tests run zero times in CI. This means: test GREEN status is not verified by CI; coverage from these tests does not contribute to the coverage threshold; a future regression in the P-003 check would not be caught by CI tests.

FINDING-004 (MEDIUM) is unresolved. The `file_path.with_suffix(".governance.yaml")` derivation correctly handles all current agent files, but the assumption (single `.md` suffix) is undocumented. This is a maintenance/documentation gap, not a current defect.

**Improvement Path:**

Add `"scripts/tests"` to `testpaths` in `pyproject.toml`, or symlink / copy the test file to `tests/unit/scripts/`. Add a `@pytest.mark.unit` marker and ensure the test file is discoverable by the coverage job. Resolve FINDING-004 with a one-line inline comment documenting the single-suffix assumption.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

The CLI/script split inconsistency that drove the 0.82 score in Iteration 1 is resolved. The CI pipeline now runs both `uv run jerry agents validate-frontmatter` (schema validation via CLI) and `uv run python scripts/validate-agent-frontmatter.py` (P-003 check via script). These are complementary, not contradictory. The string normalization fix makes the script's behavior consistent with the real-world agent file format (70+ string-format files). The `isinstance(tier, str)` type guard makes the T5 detection semantically unambiguous.

The two implemented checks are internally consistent with each other: the CLI command checks schema validity; the script checks semantic P-003 governance. DISC-001 scoping (disallowedTools redundant when tools is explicit) is consistently applied -- neither the CLI nor the script validates disallowedTools.

**Gaps:**

The story entity has `Status: pending` and all three AC checkboxes `[ ]` unchecked. The Iteration 1 score report explicitly recommended updating these. The stated implementation outcome ("89/89 agents pass, 6/6 tests pass") is inconsistent with the story status indicating no acceptance criteria have been verified. This is an administrative inconsistency rather than a technical one, but at C4 criticality, story status accuracy is part of the quality bar.

The `AGENT_FIELDS` set in the script includes `"color"` (line 73) while the CLI handler's `_AGENT_KNOWN_FIELDS` frozenset includes `"effort"` and `"initialPrompt"`. This divergence persists from Iteration 1. It is a maintenance risk, not a current defect.

**Improvement Path:**

Update STORY-022 story entity: mark AC-1 `[x]`, AC-2 `[x]`, AC-3 `[x]`, update Status to `in_progress` or `completed` per worktracker rules. Reconcile `AGENT_FIELDS` with `_AGENT_KNOWN_FIELDS` (one PR comment to track).

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

The BDD Red/Green/Refactor cycle is documented and expanded: "H-20 BDD Red/Green cycle followed (3 fail -> 5 pass)" for Iteration 1, plus the string-format test (test 6) added after FINDING-001 remediation. The test structure is correct: the new test (`test_string_format_tools_with_agent_produces_error`) writes the frontmatter as a literal string `"tools: Read, Write, Agent"` rather than using `yaml.dump` on a list, directly exercising the bypass path. This is the correct regression test pattern.

The security review methodology (eng-security) applied manual data-flow tracing, CWE Top 25, and OWASP ASVS 5.0 -- rigorous for a C4 engagement. Three of seven findings were remediated this iteration. The fail-closed design is correctly implemented and tested.

**Gaps:**

`pyproject.toml` `testpaths = ["tests"]` means all 6 tests are invisible to CI. A developer running `uv run pytest` from the repo root would not execute these tests. The test quality is good but the test delivery is broken -- the tests exist outside the enforced test path. This is not a minor gap for a C4 deliverable; it means the BDD Red/Green cycle claim cannot be verified by any automated process.

The `agent_schema` fixture uses `Path("docs/schemas/claude-code-frontmatter-v1.schema.json")` (relative, CWD-dependent). Tests fail if run from any directory other than the repo root. This fragility was noted in Iteration 1 and remains unresolved.

FINDING-004 (MEDIUM) and FINDING-007 (LOW) from eng-security are unresolved. FINDING-004 is an edge-case path derivation assumption; FINDING-007 is a defence-in-depth CI gap. These reduce rigor at the margins.

**Improvement Path:**

Add `"scripts/tests"` to `testpaths` in `pyproject.toml`. Fix the schema path in `agent_schema` fixture to `Path(__file__).parent.parent.parent / "docs/schemas/claude-code-frontmatter-v1.schema.json"`. Resolve FINDING-007 by extending the yaml.load grep to `scripts/` in `.github/workflows/ci.yml`.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The remediation chain is well-evidenced. Each fix is directly traceable to an eng-security finding number:
- FINDING-001 (HIGH) -> string normalization at lines 146-147
- FINDING-002 (MEDIUM) -> test 6 (`test_string_format_tools_with_agent_produces_error`)
- FINDING-003 (MEDIUM) -> `isinstance(tier, str)` guard at line 170

The eng-security review (7 findings, CVSS scores, ASVS chapter verification, data-flow traces) is a high-quality evidence artifact. The CI workflow change at line 213 is directly readable and verifiable.

**Gaps:**

AC-3 ("All 89 existing agents pass") remains asserted but not proved by a reproducible artifact. No `uv run python scripts/validate-agent-frontmatter.py` output capture is present in `skills/eng-team/output/STORY-022/`. No `pytest scripts/tests/test_validate_agent_frontmatter.py -v` output is provided.

For C4 criticality, evidence that can be independently verified is expected -- not just evidence that is plausible given the code. The code is correct and the claim is plausible, but the evidence standard is not met.

The eng-security review was completed at the same timestamp as the deliverable (2026-03-29). There is no evidence that the review was conducted on the Iteration 2 state (post-string-normalization) vs. the Iteration 1 state. The review documents FINDING-001 as present (identifying the gap) but the current script has it fixed. The security review evidence therefore partially applies to a prior state.

**Improvement Path:**

Capture and persist two artifacts to `skills/eng-team/output/STORY-022/`:
1. `validate-agent-sweep-89-agents.txt`: output of `uv run python scripts/validate-agent-frontmatter.py --mode agents` from the repo root (89/89 PASS evidence)
2. `test-run-story-022-iter2.txt`: output of `uv run pytest scripts/tests/test_validate_agent_frontmatter.py -v` (6/6 GREEN evidence)

---

### Actionability (0.90/1.00)

**Evidence:**

The deliverable is now mergeable. The CI pipeline has a working P-003 enforcement step. Any future agent file that includes `Agent` or `Task` in tools without T5 governance will fail the `frontmatter-validation` CI job (at line 213). The error message is specific and actionable: it names the offending tool, explains the constraint, and provides two concrete remediation paths.

The remaining work (test discovery, story status, FINDING-004, FINDING-007) is improvement work, not blocker work. The core acceptance criteria are substantively met in the code.

The Iteration 1 improvement recommendations were implemented correctly and completely for the primary gap (AC-2, FINDING-001, FINDING-002, FINDING-003). This demonstrates that the improvement path from scoring is actionable and followed.

**Gaps:**

The test discovery gap (tests outside CI testpaths) means the 6 tests provide zero CI enforcement value. A future regression in the string normalization or type guard would not be caught by automated testing. This limits actionability confidence -- the check is deployed but the tests that verify it are not running.

**Improvement Path:**

Add `"scripts/tests"` to `testpaths` to convert the 6 existing tests from dead code to active regression guards. This is a one-line `pyproject.toml` change.

---

### Traceability (0.85/1.00)

**Evidence:**

The CI step comment at line 212 (`"Validate P-003 Agent tool restriction (STORY-022)"`) creates a direct link from the CI step to the story. The inline script comment at lines 151-154 cites "STORY-022: P-003", "(DISC-001)", and "(H-01)" -- three independent reference chains. The test module docstring cites STORY-022. The test class docstring cites STORY-022. The eng-security finding IDs (FINDING-001 through FINDING-007) are referenced in the context description with explicit status annotations (remediated / unresolved).

**Gaps:**

The STORY-022 story entity (`projects/PROJ-024-tactical-work/work/.../STORY-022-ci-task-agent-check.md`) still shows:
- `Status: pending`
- All three AC checkboxes `[ ]`

The Iteration 1 score report explicitly recommended: "Update STORY-022 AC checkboxes: AC-1 [x], AC-3 [x], AC-2 [ ] with blocking note." This recommendation was not actioned. The story status now misrepresents the implementation state -- a reader examining the worktracker entity cannot determine that AC-1, AC-2, and AC-3 are met. This is a traceability regression from Iteration 1 expectations.

Additionally, the Iteration 1 recommendation to add `# TODO STORY-022` to `validate_frontmatter_command.py` was not acted upon (though this is less critical now that the CI step approach was used instead of porting to the CLI handler).

**Improvement Path:**

Update STORY-022 story entity:
- `Status: in_progress` (or `completed` if all ACs are considered met)
- `[x] validate-agent-frontmatter.py errors if Agent appears in any non-T5 agent's tools field`
- `[x] CI pipeline runs the check on every PR touching skills/*/agents/*.md` (via line 213)
- `[x] All 89 existing agents pass the new check`
- `Completed:` field with timestamp

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness + Methodological Rigor | 0.88 | 0.93 | Add `"scripts/tests"` to `testpaths` in `pyproject.toml`. One-line change. Converts 6 existing tests from unreachable to CI-enforced. Closes the single largest structural gap remaining. |
| 2 | Traceability | 0.85 | 0.93 | Update STORY-022 story entity: mark all 3 ACs `[x]`, set Status to `in_progress`/`completed`, add `Completed:` timestamp. This was explicitly recommended in Iteration 1 and not actioned. |
| 3 | Evidence Quality | 0.87 | 0.92 | Capture and persist two text artifacts: (a) `validate-agent-sweep-89-agents.txt` (89/89 PASS output), (b) `test-run-story-022-iter2.txt` (6/6 GREEN pytest output). Place in `skills/eng-team/output/STORY-022/`. |
| 4 | Methodological Rigor | 0.88 | 0.92 | Fix `agent_schema` fixture path: replace `Path("docs/schemas/...")` with `Path(__file__).parent.parent.parent / "docs/schemas/..."`. Removes CWD dependency. |
| 5 | Methodological Rigor | 0.88 | 0.91 | Resolve FINDING-007: extend the yaml.load grep in `.github/workflows/ci.yml` (line 102) from `src/` to `src/ scripts/`. One-line change. Defence-in-depth gap closed. |
| 6 | Internal Consistency + Completeness | 0.88 | 0.90 | Document FINDING-004 assumption: add one inline comment to `validate-agent-frontmatter.py` at line 157 confirming `with_suffix` assumes single `.md` suffix, and that multi-suffix files fail closed. |

---

## Remaining Eng-Security Finding Status

| Finding | Severity | Status | Evidence |
|---------|----------|--------|----------|
| FINDING-001 -- String-format tools bypass | HIGH | REMEDIATED | Lines 146-147 add string normalization before isinstance check |
| FINDING-002 -- No test for string-format tools | MEDIUM | REMEDIATED | Test 6 (`test_string_format_tools_with_agent_produces_error`) exercises literal string format |
| FINDING-003 -- tool_tier type not guarded | MEDIUM | REMEDIATED | Line 170: `isinstance(tier, str) and tier == "T5"` |
| FINDING-004 -- Governance path multi-suffix edge case | MEDIUM | UNRESOLVED | No comment or guard added; acceptable as LOW-risk but should be documented |
| FINDING-005 -- safe_load correctly used | INFO | CONFIRMED CLEAN | No action required; confirmed in review |
| FINDING-006 -- Error message quality | INFO | CONFIRMED CLEAN | No action required; confirmed in review |
| FINDING-007 -- yaml.load grep excludes scripts/ | LOW | UNRESOLVED | CI grep scope not extended |

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Traceability uncertain between 0.85-0.88; chose 0.85 because the Iteration 1 explicit recommendation to update story AC checkboxes was not actioned -- this is a concrete evidence-based downward signal, not impression)
- [x] Delta from Iteration 1 explicitly documented per dimension with drivers
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] C4 threshold calibration applied (0.95, not 0.92): at C4 criticality, machine-readable artifacts and verified story status are expected, not optional
- [x] Anti-leniency note: The score could have been justified at 0.90+ by treating test discovery as a trivial configuration gap. It was held at 0.88 because: (a) tests outside testpaths means zero CI verification of the 6 remediation tests, which is not trivial at C4; (b) the story status update was explicitly recommended in Iteration 1 and ignored, which is a fidelity signal; (c) the C4 threshold is 0.95, meaning 0.88 is still substantially below the bar and the remaining gaps are non-trivial.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.88
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.85
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add scripts/tests to testpaths in pyproject.toml -- converts 6 tests from unreachable to CI-enforced"
  - "Update STORY-022 story entity: mark all 3 ACs [x], update Status"
  - "Capture and persist 89-agent sweep output and pytest -v output as evidence artifacts"
  - "Fix agent_schema fixture path to use __file__-relative path (remove CWD dependency)"
  - "Resolve FINDING-007: extend yaml.load grep to scripts/ in ci.yml"
  - "Document FINDING-004 single-suffix assumption with inline comment"
```

---

*Agent: adv-scorer v1.0.0*
*Constitutional Compliance: P-001 (evidence-based scoring), P-002 (persisted to file), P-003 (no subagents spawned), P-022 (no deception -- leniency bias actively counteracted; Traceability scored downward on concrete evidence)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-29T00:00:00Z*
*Prior iteration: 0.82 (Iter 1) -> 0.88 (Iter 2), delta +0.06*
