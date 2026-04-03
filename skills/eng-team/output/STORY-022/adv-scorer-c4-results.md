# Quality Score Report: STORY-022 -- P-003 Agent Tool CI Validation

## L0 Executive Summary
**Score:** 0.82/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.72)
**One-line assessment:** The P-003 check is correctly implemented in the standalone script with solid tests, but the check was NOT ported to the CLI command handler that the CI `frontmatter-validation` job actually invokes -- AC-2 is unmet as written, which is the primary revision target.

---

## Scoring Context
- **Deliverable:** STORY-022 implementation: `scripts/validate-agent-frontmatter.py` (lines 146-167), `scripts/tests/test_validate_agent_frontmatter.py`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-29T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.82 |
| **Threshold** | 0.95 (C4 override) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes -- red-vuln F-006 (STORY-013-M007) and DISC-001 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.72 | 0.144 | P-003 check absent from CLI command handler; CI job uses CLI not the script directly |
| Internal Consistency | 0.20 | 0.82 | 0.164 | Script logic consistent internally; DISC-001 reasoning sound; but CLI/script split contradicts AC-2 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | H-20 BDD Red/Green cycle documented; 5 test cases cover all acceptance conditions; fail-closed design sound |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | red-vuln F-006 cited; DISC-001 validated via Context7; 89-agent sweep documented; test pass evidence stated but not a machine-readable artifact |
| Actionability | 0.15 | 0.80 | 0.120 | Fix path is clear (port check to CLI handler); tests and script are correct and can be adopted with targeted correction |
| Traceability | 0.10 | 0.88 | 0.088 | AC traceability table present in story; DISC-001 scoping decision documented; red-vuln F-006 linked; missing explicit AC-2 status annotation |
| **TOTAL** | **1.00** | | **0.82** | |

---

## Detailed Dimension Analysis

### Completeness (0.72/1.00)

**Evidence:**

AC-1 (error if `Agent` appears in non-T5 `tools` field): Met. Lines 151-172 of `scripts/validate-agent-frontmatter.py` implement the check. The check reads `.governance.yaml` for `tool_tier: T5`, falls closed on missing/malformed governance, and produces an actionable P-003 error message.

AC-3 (89 existing agents pass): Stated as met (89/89 pass). Acceptance per the implementation context; no machine-readable CI run artifact provided, but the logic is sound and the test for the negative path (`test_agent_without_agent_tool_no_error`) confirms no false positives on clean agents.

**Gaps:**

AC-2 (CI pipeline runs the check on every PR): NOT MET.

The CI `frontmatter-validation` job (`.github/workflows/ci.yml`, line 210) invokes `uv run jerry agents validate-frontmatter` -- the CLI command handler at `src/agents/application/commands/validate_frontmatter_command.py`. That handler was read in full (lines 427-516). It contains zero P-003/Agent/Task/tool_tier logic. The P-003 check implemented in `scripts/validate-agent-frontmatter.py` is not invoked by the CI pipeline's frontmatter validation job. No other CI job directly calls the script either -- the `plugin-validation` and `template-validation` jobs are unrelated.

The `test-pip` and `test-uv` matrix jobs run `pytest -m "not subprocess and not llm"` against `src/`. The new tests live in `scripts/tests/test_validate_agent_frontmatter.py` -- outside the `src/` or `tests/` directories that the CI test matrix runs. There is no evidence the script tests are picked up by the CI coverage/test jobs.

This gap means: the P-003 check exists in the script and passes tests, but the actual enforcement layer the CI uses does not contain it. A non-T5 agent with `Agent` in its `tools` list would pass `jerry agents validate-frontmatter` silently.

**Improvement Path:**
Port the P-003 check logic to `ValidateFrontmatterCommandHandler._validate_agent_file()` in `src/agents/application/commands/validate_frontmatter_command.py`. The logic is proven -- copy the `delegation_tools` detection and `.governance.yaml` T5 lookup. Alternatively, integrate the script's output into the `frontmatter-validation` CI step alongside `jerry agents validate-frontmatter`. Either path closes the AC-2 gap.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

The standalone script logic is internally consistent. DISC-001 establishes that `disallowedTools` is redundant when `tools` is explicitly declared (89/89 agents do), correctly scoping the CI check to only verify `tools` (allowlist). The choice of fail-closed on missing governance.yaml is correctly documented in the inline comment (`# fail closed: missing/broken governance = not T5`). Test case names match the acceptance criteria language. The `delegation_tools` filter covers both `Agent` and `Task` (the backward-compatible alias), consistent with the STORY-022 scope item "Backward-compatible Task alias covered."

**Gaps:**

The primary inconsistency is structural: the deliverable claims "CI pipeline runs the check on every PR" (AC-2) but the check does not exist in the code path that CI actually executes. This is not a logical contradiction within the script itself, but it is a material inconsistency between the stated AC-2 outcome and the observable implementation state.

A minor inconsistency: the script's `AGENT_FIELDS` set includes `"color"` (line 73) while the CLI handler's `_AGENT_KNOWN_FIELDS` frozenset includes `"effort"` and `"initialPrompt"` but not `"color"`. This divergence between the two validators is a maintenance concern, though not material to the P-003 check.

**Improvement Path:**
Port the P-003 check to the CLI handler (closes the primary inconsistency). Reconcile `AGENT_FIELDS` between the script and the CLI handler to prevent future drift.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

H-20 BDD Red/Green cycle is documented: "H-20 BDD Red/Green cycle followed (3 fail -> 5 pass)." Five test cases are present covering: non-T5 with Agent (positive), non-T5 with Task alias (positive), T5 with Agent (negative -- no error), agent without Agent (negative -- no error), and missing governance.yaml (fail-closed). This is a complete coverage matrix for the stated acceptance criteria. The fail-closed design (`except (yaml.YAMLError, OSError): pass  # fail closed`) is correct security engineering -- defaulting to the stricter interpretation on uncertainty. /eng-team and /red-team were run in parallel, following the multi-review methodology for C4 work.

**Gaps:**

The test file uses `importlib.util.spec_from_file_location` to import the hyphenated script filename (lines 14-23). This is a valid approach but represents a fragile test setup -- if the script is renamed or relocated, the import silently breaks with a confusing error rather than a clear test failure. The `agent_schema` fixture uses a relative path (`Path("docs/schemas/claude-code-frontmatter-v1.schema.json")`) rather than resolving from `__file__`, meaning tests fail if not run from the repo root. These are not blocking issues but represent test hygiene gaps.

Coverage evidence for the 89-agent sweep is stated but not a verified artifact (no test result file provided, no CI run linked). At C4 criticality, machine-readable verification is expected.

**Improvement Path:**
Add a conftest.py fixture that resolves the repo root from `__file__` for schema path. Add a pytest marker (`unit`) to the test class for CI matrix discovery. Provide a CI run artifact or test output log as evidence for the 89-agent AC-3 claim.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

The primary causal chain is well-evidenced. red-vuln F-006 (STORY-013-M007) is a thorough vulnerability report identifying the CI enforcement gap with CVSS scoring and attack path analysis. DISC-001 provides Context7-validated technical evidence (Claude Code docs, empirical grep count) for the scoping decision. The `delegation_tools = [t for t in tools if t in ("Agent", "Task")]` implementation is directly traceable to the schema comment cited in red-vuln F-001: "The subagent spawning tool was renamed from 'Task' to 'Agent' in v2.1.63. Both names work as aliases."

The implementation evidence (5 tests, script code) is present and readable.

**Gaps:**

AC-3 ("All 89 existing agents pass") is asserted but not proved by a reproducible artifact. At C4, the standard is evidence that can be independently verified, not just stated. No test output file, CI run link, or pytest XML report is provided for the 89-agent sweep. The claim is plausible (the logic is sound) but not verified by included evidence.

The test result "5/5 tests pass (GREEN)" is stated but no pytest output or CI run is attached. For C4, this should be a machine-readable artifact.

**Improvement Path:**
Attach a pytest run output (even a trimmed `pytest -v` terminal capture saved as a text file) as evidence for the 5-test GREEN claim. Run `uv run python scripts/validate-agent-frontmatter.py --mode agents` and capture the output as an evidence artifact for AC-3.

---

### Actionability (0.80/1.00)

**Evidence:**

The error message in the implementation is genuinely actionable: `"Fix: remove {delegation_tools} from tools list, or set tool_tier: T5 in {gov_path.name} with documented justification."` This follows the standard for actionable error messages (H-11 guidelines: include entity type, ID, suggested action). The T5 detection mechanism is clear -- check `tool_tier` in the companion `.governance.yaml`. The test cases are directly exercisable by any developer reproducing the check.

The improvement path for the AC-2 gap is specific and achievable: port approximately 22 lines of logic from the script's `validate_agent()` to the CLI handler's `_validate_agent_file()`.

**Gaps:**

The score is reduced because the primary defect (AC-2 not met) means the deliverable cannot be acted upon in its current state without a specific targeted correction. The CI pipeline currently provides no enforcement for P-003 via tools lists -- the check exists but is unreachable through the CI path.

There is no migration note or flag in the deliverable acknowledging the CLI handler gap. A developer accepting this PR would not know, without this score report, that the CI enforcement is incomplete.

**Improvement Path:**
Add a note to the STORY-022 acceptance criteria tracking acknowledging the CLI handler porting as a prerequisite to AC-2 closure. This makes the remaining work visible without requiring a reader to trace the two code paths themselves.

---

### Traceability (0.88/1.00)

**Evidence:**

The STORY-022 work item contains a complete Related Items table tracing to STORY-013 M-007, red-vuln F-006, and DISC-001. The inline comment in the script (lines 151-154) cites the constraint by name: "STORY-022: P-003", references the enforcement layer design decision "(DISC-001)", and links to the standard "(H-01)". The test class docstring cites the story: `"""STORY-022: Error if non-T5 agent has Agent in tools."""`. The test module docstring is precise: `"""Tests for validate-agent-frontmatter.py P-003 Agent tool check (STORY-022)."""`.

**Gaps:**

The three acceptance criteria in STORY-022 are all marked `[ ]` (unchecked) -- the story status is "pending." There is no explicit AC-2 failure note. For C4 work, completion status should be self-evident from the story entity. A reviewer cannot determine from the story alone whether AC-2 was intentionally deferred or accidentally missed.

The `validate_frontmatter_command.py` CLI handler has no reference to STORY-022, P-003, or the tool-tier check. Since the check needs to be added there, the absence of any placeholder or TODO creates a traceability gap: the code path that needs updating has no signal pointing to the required change.

**Improvement Path:**
Update STORY-022 acceptance criteria: mark AC-1 and AC-3 as `[x]`, keep AC-2 as `[ ]` with a note "Blocked: P-003 check not yet ported to CLI handler." Add a `# TODO STORY-022: port P-003 check here` comment to line 492 of `validate_frontmatter_command.py` (the location after MCP tools warning where delegation_tools check belongs).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.72 | 0.88 | Port P-003 delegation_tools check to `ValidateFrontmatterCommandHandler._validate_agent_file()` in `src/agents/application/commands/validate_frontmatter_command.py`. Copy lines 155-172 logic from the script. Add companion `.governance.yaml` T5 lookup. This closes AC-2 (CI pipeline enforcement). |
| 2 | Completeness | 0.72 | 0.88 | Verify `scripts/tests/test_validate_agent_frontmatter.py` is discovered by CI test matrix (add `tests/` location or configure pytest path in `pyproject.toml`). The tests currently live outside the `src/` and `tests/` tree that CI runs against. |
| 3 | Internal Consistency | 0.82 | 0.90 | Reconcile `AGENT_FIELDS` in `scripts/validate-agent-frontmatter.py` with `_AGENT_KNOWN_FIELDS` in the CLI handler. The script has `"color"` but not `"effort"` or `"initialPrompt"`; the handler has the inverse. |
| 4 | Evidence Quality | 0.87 | 0.93 | Capture and persist a `uv run python scripts/validate-agent-frontmatter.py --mode agents` run output (89/89 PASS evidence) and a `pytest scripts/tests/test_validate_agent_frontmatter.py -v` output (5/5 GREEN evidence) as files in `skills/eng-team/output/STORY-022/`. |
| 5 | Traceability | 0.88 | 0.93 | Mark AC-1 and AC-3 `[x]` in the STORY-022 story entity; annotate AC-2 as blocked pending CLI handler port. Add `# TODO STORY-022` comment to `validate_frontmatter_command.py` at the delegation_tools insertion point (after line ~492). |
| 6 | Methodological Rigor | 0.88 | 0.93 | Resolve test fixture fragility: use `Path(__file__).parent.parent.parent / "docs/schemas/..."` for schema path in `agent_schema` fixture, removing reliance on CWD. Add `@pytest.mark.unit` to `TestP003AgentToolCheck`. |

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness uncertain between 0.72-0.78; chose 0.72 given AC-2 is structurally unmet, not just partially met)
- [x] First-draft calibration considered (this is an implementation deliverable, not a document; calibration applied to code quality not document structure)
- [x] No dimension scored above 0.95 without exceptional evidence

**Anti-leniency notes applied:**

The implementation summary states "CI pipeline runs the check on every PR" (AC-2 met). This claim was tested by reading the CI workflow and the CLI command handler. The claim is false -- the check is absent from the code path CI actually invokes. Completeness was scored at 0.72 (not the 0.85 it would receive if AC-2 were taken at face value) because the AC is materially unmet, not merely incomplete. This is the single most significant quality gap.

The test quality is good (5 cases, correct BDD structure, fail-closed tested) but the test discovery gap (tests outside CI's test path) reduces rigor confidence. Methodological Rigor was held at 0.88, not 0.92, to reflect this.

The deliverable is well-conceived and the script-level check is correctly implemented. The REVISE verdict reflects a targeted, addressable gap (port to CLI handler + test discovery) rather than fundamental design problems.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.82
threshold: 0.95
weakest_dimension: Completeness
weakest_score: 0.72
critical_findings_count: 1
iteration: 1
improvement_recommendations:
  - "Port P-003 delegation_tools check to ValidateFrontmatterCommandHandler._validate_agent_file() -- closes AC-2"
  - "Verify scripts/tests/ discovered by CI test matrix (pytest path configuration)"
  - "Reconcile AGENT_FIELDS divergence between script and CLI handler"
  - "Capture and persist 89-agent sweep output and pytest GREEN evidence as artifacts"
  - "Update STORY-022 AC checkboxes: AC-1 [x], AC-3 [x], AC-2 [ ] with blocking note"
  - "Fix schema fixture path in test to not depend on CWD"
```

---

*Agent: adv-scorer v1.0.0*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-022 (no deception -- leniency bias actively counteracted)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-29*
