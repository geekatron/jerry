# S-014 Post-Remediation Quality Score: BUG-002 Hook Schema Validation Fixes

> **Agent:** adv-scorer
> **Scoring ID:** bug002-hookfix-20260217-001 / Phase 5 Post-Remediation
> **Date:** 2026-02-17
> **Deliverable:** BUG-002 Hook Schema Validation Fixes (Phase 5 remediation commit 52e3015)
> **Prior tournament score:** 0.9125 (REVISE, Phase 4)
> **Scoring method:** S-014 LLM-as-Judge, 6-dimension weighted rubric
> **Leniency bias note:** Actively counteracted throughout. A score of 0.92 means genuinely excellent.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Remediation Summary](#remediation-summary) | What P1-P5 changed and what was verified |
| [Dimension-by-Dimension Scoring](#dimension-by-dimension-scoring) | Pre/post comparison with critical assessment |
| [Weighted Composite Calculation](#weighted-composite-calculation) | Arithmetic score derivation |
| [Remaining Unaddressed Findings](#remaining-unaddressed-findings) | Minor findings not addressed by P1-P5 |
| [Final Verdict](#final-verdict) | PASS or REVISE determination |

---

## Remediation Summary

Phase 5 targeted the five Priority items identified by the Phase 4 C4 tournament verdict.

### P1: DA-001 / CC-002 -- Missing test suite for `subagent_stop.py`

**Action taken:** Created `tests/hooks/test_subagent_stop.py` with 32 tests across 6 classes:
- `TestParseAgentOutput` (8 tests): handoff signal parsing for `##HANDOFF:##`, `##WORKITEM:##`, `##STATUS:##`
- `TestDetermineHandoff` (9 tests): HANDOFF_RULES matching, known-agent/unknown-condition, unknown-agent, no-condition paths
- `TestLogHandoff` (2 tests): file creation and content format verification
- `TestHookOutputAllow` (3 tests): subprocess allow path via live hook invocation
- `TestHookOutputBlock` (4 tests): subprocess block path, systemMessage inclusion, no hookSpecificOutput
- `TestErrorHandling` (4 tests): invalid JSON exit 2, missing fields graceful defaults
- `TestHandoffRulesWarnings` (2 tests): PM-001/FM-001 warning output to stderr

**Assessment:** Tests cover the stated scope. Both the unit-level functions (`parse_agent_output`, `determine_handoff`) and the subprocess-level behavior are tested. The warning system introduced by P5 is tested by the last class.

**Gaps identified:**
- `log_handoff()` tests (2 tests) use `monkeypatch` to redirect `__file__`, causing logs to write outside `tmp_path` to `tmp_path.parent/docs/experience/`. The test cleans up manually. This is a test-isolation weakness: if cleanup fails (e.g., test timeout), it leaves a directory artifact outside tmp_path. Not a correctness issue but a test hygiene concern.
- The `TestLogHandoff` class does not test the `OSError` fallback path (file cannot be opened). That path is present in the implementation but unverified by any test.
- `HANDOFF_RULES` data integrity tests (`test_all_handoff_rules_keys_are_strings`, `test_all_handoff_rules_values_are_tuples`) are present and valuable.

**P1 Verdict:** Substantially addressed. The primary gap (zero business-logic tests) is eliminated. Residual gaps are minor.

---

### P2: CC-001 / SR-001 -- Shebang H-05 violations

**Action taken:** All three scripts fixed to `#!/usr/bin/env -S uv run python`:
- `scripts/pre_tool_use.py` line 1: `#!/usr/bin/env -S uv run python` (confirmed)
- `scripts/subagent_stop.py` line 1: `#!/usr/bin/env -S uv run python` (confirmed)
- `scripts/validate_schemas.py` line 1: `#!/usr/bin/env -S uv run python` (confirmed)

**Assessment:** H-05 violation is fully remediated. All hook scripts now use consistent UV-compliant shebangs. The inconsistency surfaced by SR-001 is resolved.

**P2 Verdict:** Fully addressed.

---

### P3: RT-003 -- Path traversal normalization in `pre_tool_use.py`

**Action taken:** `check_file_write()` now applies `os.path.normpath(os.path.expanduser(file_path))` before sensitive path matching (line 130). Blocked paths are also normalized via `os.path.normpath(os.path.expanduser(blocked))` (line 134). Windows uses `os.path.normcase` for case-insensitive comparison (line 136).

**Assessment:** The normpath application prevents the most practical traversal bypass vectors (e.g., `~/../../../.ssh/authorized_keys`, `/tmp/../../../etc/passwd`). A `resolve()` call would be stronger (resolves symlinks), but `normpath` addresses the stated finding (RT-003 cited normpath specifically).

**Residual concern:** `os.path.normpath` does not resolve symlinks. A path like `/safe/../.ssh/` normalizes to `/.ssh/` correctly, but a symlink-based bypass (e.g., `/tmp/safe_link` pointing to `/root/.ssh/`) would still pass. This was not identified in the tournament and is a known limitation of the approach. For the scope of the finding, the remediation is correct.

**P3 Verdict:** Adequately addressed per finding scope.

---

### P4: RT-004 -- `rm` flag variation detection

**Action taken:** `check_bash_command()` now uses regex-based detection (lines 172-179):
```python
rm_match = re.search(r"\brm\s+(.*)", cmd_stripped)
if rm_match:
    rm_args = rm_match.group(1)
    has_recursive = bool(re.search(r"(?:^|\s)-[a-zA-Z]*r|--recursive", rm_args))
    has_force = bool(re.search(r"(?:^|\s)-[a-zA-Z]*f|--force", rm_args))
    targets_root = bool(re.search(r"(?:^|\s)[/~]", rm_args))
    if has_recursive and has_force and targets_root:
        return False, "Command contains dangerous rm pattern targeting root or home"
```

Five regression tests added to `tests/hooks/test_pre_tool_use.py`:
- `test_bash_rm_split_flags_blocked` (`rm -r -f /`)
- `test_bash_rm_long_flags_blocked` (`rm --recursive --force /`)
- `test_bash_rm_fr_root_blocked` (`rm -fr /`)
- `test_bash_rm_rf_home_blocked` (`rm -rf ~`)
- (The original `test_bash_rm_rf_root_blocked` for `rm -rf /` pre-existed)

**Assessment of regex correctness:**

| Variant | `has_recursive` | `has_force` | `targets_root` | Blocked? |
|---------|----------------|-------------|----------------|----------|
| `rm -rf /` | matches `-[a-zA-Z]*r` via `-rf` (r present) | matches `-[a-zA-Z]*f` via `-rf` (f present) | matches `/` | YES |
| `rm -r -f /` | matches `-[a-zA-Z]*r` via `-r` | matches `-[a-zA-Z]*f` via `-f` | matches `/` | YES |
| `rm --recursive --force /` | matches `--recursive` | matches `--force` | matches `/` | YES |
| `rm -fr /` | `-fr` contains `r` → matches | `-fr` contains `f` → matches | matches `/` | YES |
| `rm -rf ~` | YES | YES | matches `~` | YES |

**Residual concern (not a finding, assessment only):** The `targets_root` regex `(?:^|\s)[/~]` matches any argument beginning with `/` or `~` — this includes valid targets like `rm -rf /tmp/build`. However, `rm -rf /tmp/build` would be blocked. This is a false positive for legitimate deep-clean operations. The original DANGEROUS_COMMANDS list already blocked `"rm -rf /"` and `"rm -rf ~"` specifically; the new regex broadens the block scope significantly. The tournament finding (RT-004) asked for variant detection targeting root/home — the intent was to block `/` and `~` as targets, but the implementation blocks any absolute or home-relative path. This is potentially over-broad but errs on the side of safety, which is appropriate for a security guardrail.

**Important note:** The old `DANGEROUS_COMMANDS` list check at line 182 still runs after the new regex check. `rm -rf /` would be caught first by the new regex (line 178) and independently by the old string match (line 183-184). The double-check is redundant but not harmful.

**P4 Verdict:** Addressed. Flag variation detection works for all test-covered variants. The over-broad targeting scope is an acceptable trade-off for a security hook.

---

### P5: PM-001 / FM-001 -- HANDOFF_RULES mismatch warning logging

**Action taken:** `determine_handoff()` in `subagent_stop.py` now has a warning branch at lines 125-143. When a condition is signaled but no rule matches, it distinguishes two cases:
1. Agent name not found in `HANDOFF_RULES` at all: logs `"Agent '{from_agent}' not found in HANDOFF_RULES — possible misconfiguration"`
2. Agent found but condition does not match any rule: logs `"Condition '{condition}' from agent '{from_agent}' has no matching rule"`

Both warnings are written to stderr as JSON.

**Assessment:** The PM-001 finding asked for a runtime check that validates `HANDOFF_RULES` keys against an agent registry. The implementation provides a weaker version: it warns only when a mismatch is detected at runtime (an agent stops with a signal that has no matching rule). It does NOT proactively validate HANDOFF_RULES against an agent registry at startup. The FMEA recommended "log a warning when a stopping agent is not found in HANDOFF_RULES" — this is exactly what was implemented. The stronger "validate against agent registry" was noted as a recommendation, not a required action for this priority item.

**P5 Verdict:** Adequately addressed for the stated requirement. The proactive registry validation remains unimplemented but was not a hard requirement for REVISE-to-PASS advancement.

---

## Dimension-by-Dimension Scoring

### Dimension 1: Completeness (weight 0.20)

**Pre-remediation score:** 0.87
**Primary drivers of 0.87:** DA-001 (no test suite for subagent_stop.py) + RT-003 (path normalization gap) + RT-004 (rm flag variant gap)

**Post-remediation assessment:**

P1 delivers 32 tests covering the previously untested subagent_stop.py business logic. Coverage of the business logic functions is now substantive: `parse_agent_output`, `determine_handoff`, and `log_handoff` all have direct unit tests. The subprocess-level behavior is verified via live hook invocations. H-21 (90% coverage) is now plausible for `subagent_stop.py`, though exact coverage was not reported.

P3 and P4 address the security coverage gaps that depressed Methodological Rigor and Completeness.

Remaining completeness gaps post-remediation:
- `log_handoff()` OSError fallback is untested
- SubagentStop block path live schema compliance (IN-001) is not added to `test_hook_schema_compliance.py`
- The post-tool-use and permission-request schemas remain without live-hook compliance tests (DA-004, pre-existing)
- SR-004 (subprocess timeouts in TestLiveHookOutputCompliance) not addressed
- Exact coverage percentage for `subagent_stop.py` not stated in remediation summary

The completeness gap reduced from "zero business logic tests" to "minor gaps in error path and live compliance." This is a material improvement. The main risk (DA-001/CC-002 combined) is resolved.

**Post-remediation score: 0.93**

Rationale: The primary completeness driver (0.03-level drag from missing test suite) is resolved. Residual gaps are individually minor. Scoring at 0.93 rather than higher because exact coverage is unverified and the OSError path, IN-001 live compliance gap, and SR-004 timeout gap are still open.

---

### Dimension 2: Internal Consistency (weight 0.20)

**Pre-remediation score:** 0.91
**Primary drivers of 0.91:** Shebang inconsistency (SR-001/CC-001) prevented a higher score.

**Post-remediation assessment:**

P2 resolves the shebang inconsistency fully. All three scripts now use `#!/usr/bin/env -S uv run python`. The hook protocol consistency (PreToolUse uses hookSpecificOutput, SubagentStop uses top-level fields) was already verified as correct and remains unchanged.

The new test suite for `subagent_stop.py` is internally consistent with the existing `test_pre_tool_use.py` structure: both use subprocess-based testing with a `run_hook()` helper and verify JSON output. The `test_subagent_stop.py` `test_block_output_has_no_hookspecificoutput` test (line 403) explicitly enforces the SubagentStop schema contract, which is good.

Minor internal consistency observation: `test_subagent_stop.py` imports the hook module directly (`from subagent_stop import ...`) using `sys.path.insert(0, str(HOOK_SCRIPT.parent))`. This works but ties tests to the scripts directory layout. The same approach is used elsewhere (consistent with existing practice), so this is not a new inconsistency.

No new inconsistencies introduced. The shebang fix resolves the main pre-remediation driver.

**Post-remediation score: 0.94**

Rationale: The single identified inconsistency (shebang) is fully resolved. No new inconsistencies introduced. Scoring at 0.94 rather than higher because the warning system added in P5 uses a two-branch structure (unknown agent vs. known agent with unknown condition) but the HANDOFF_RULES dict itself is never validated at startup — a silent asymmetry in the defense model. Not a significant issue but prevents scoring at 0.96+.

---

### Dimension 3: Methodological Rigor (weight 0.20)

**Pre-remediation score:** 0.90
**Primary drivers of 0.90:** FMEA identified 4 high-RPN failure modes; RT-003/RT-004 security gaps in enforcement methodology.

**Post-remediation assessment:**

P3 (normpath normalization) and P4 (regex-based rm detection) directly address the security methodology gaps that drove the Methodological Rigor score down from its preliminary 0.93. The normpath fix is correct and defense-in-depth. The regex-based rm detection is technically correct and covers the specified variants.

The test methodology for P1 (32 tests for subagent_stop.py) is sound: unit tests for function-level behavior, subprocess tests for end-to-end behavior, and stderr verification for warning system. The use of `capsys` for unit-level warning verification and subprocess stderr capture for integration-level warning verification demonstrates appropriate methodology.

Remaining methodological concerns:
- FM #6 (RPN 147: PreToolUse matcher scope undocumented) is unaddressed. The decision to match only `Write|Edit|MultiEdit|Bash` is still implicit.
- FM #9 (RPN 120: malformed `##HANDOFF:` signal) is unaddressed. The signal parsing still uses string operations (`line.index("##HANDOFF:")`, `line.index("##", start)`) that will throw `ValueError` if a line contains `##HANDOFF:` but no closing `##`. The `index()` calls will raise `ValueError` for malformed signals rather than silently failing — this is caught by the outer `except Exception: exit 2` handler, which is better than silent failure, but differs from the "ignore malformed signals" behavior implied by the FMEA recommendation.
- FM #10 (RPN 147: spec divergence) remains unaddressed.

The P4 regex implementation does improve rigor over the simple string match, but the over-broad `targets_root` check means `rm -rf /tmp/build` is now blocked (false positive). This represents a rigor trade-off.

**Post-remediation score: 0.92**

Rationale: RT-003 and RT-004 are addressed, resolving the primary drivers. FMEA high-RPN findings FM #6 and FM #10 (combined RPN 294) remain open. FM #9 is partially improved (malformed signals now raise ValueError caught by error handler, vs. silent miss). The regex approach for P4 is directionally correct but has over-broad targeting. Scoring at 0.92 reflects improvement from 0.90 but recognizes the high-RPN findings that remain unaddressed.

---

### Dimension 4: Evidence Quality (weight 0.15)

**Pre-remediation score:** 0.95
**Primary drivers of 0.95:** All findings cited specific files and line numbers. Test pass/fail ratio (3159/0) was concrete evidence.

**Post-remediation assessment:**

Post-remediation evidence is similarly concrete:
- 3195 tests pass, 0 fail (up from 3159 — 36 new tests added: 32 subagent_stop + 4 new rm variant tests in test_pre_tool_use.py, accounting for the original `rm -rf /` test pre-existing)
- 8/8 schema validation PASS maintained
- All pre-commit hooks pass
- Git commit 52e3015 provides a verifiable artifact
- Code inspection confirms each P item is implemented at specific lines (verified above)

The test count arithmetic: 3195 - 3159 = 36 new tests. The context states "32 tests in test_subagent_stop.py" and "5 new rm variant tests." 32 + 5 = 37, but the original `rm -rf /` test pre-existed, so new tests = 32 + 4 = 36. This is consistent.

No reduction warranted. Evidence quality is maintained at the pre-remediation level. The specific line references in the assessment above are independently verifiable from the file reads conducted.

**Post-remediation score: 0.95**

---

### Dimension 5: Actionability (weight 0.15)

**Pre-remediation score:** 0.94
**Primary drivers of 0.94:** All findings had specific, implementable recommendations. FMEA RPN table provided prioritization.

**Post-remediation assessment:**

Actionability reflects the quality of the tournament's recommendations and the deliverable's completeness. Post-remediation, the five P-item recommendations from the tournament were actionable and were acted upon. The remaining findings (minor) continue to have specific recommendations:
- SR-004: Add `timeout=10` to subprocess calls in TestLiveHookOutputCompliance
- IN-001: Add live SubagentStop block path compliance test
- DA-002: Document PreToolUse matcher scope decision
- FM #6: Consider `.*` matcher with fast-exit for read-only tools
- FM #10: Pin Claude Code spec version in schema metadata

These are all specific and implementable. No vague recommendations exist in either the tournament or the post-remediation state.

The post-remediation state itself is actionable: the PASS determination (if granted) provides clear closure. Any REVISE would need to specify what remains, which this document does in the Remaining Findings section.

**Post-remediation score: 0.94**

---

### Dimension 6: Traceability (weight 0.10)

**Pre-remediation score:** 0.93
**Primary drivers of 0.93:** Root causes RC-1 through RC-7 traceable to tasks; findings used execution_id 20260217.

**Post-remediation assessment:**

Each remediation item (P1-P5) is explicitly traced to the finding IDs that drove it (DA-001/CC-002 for P1, CC-001/SR-001 for P2, etc.). The finding IDs trace back to tournament strategies (S-002, S-007, S-010, S-004, S-012). The git commit 52e3015 provides a traceability anchor for the remediation.

The test file for P1 (`test_subagent_stop.py`) explicitly references the finding IDs in its docstring (lines 12-15): `DA-001`, `CC-002`, `PM-001`, `FM-001`. The test file for P4 references `RT-004` in test names and docstrings. This is good practice and directly traceable.

One traceability gap: the exact coverage percentage for `subagent_stop.py` post-remediation is not reported. H-21 (90%) was a stated concern (CC-002) and its resolution is asserted but not measured. A CI coverage report would complete the evidence chain.

**Post-remediation score: 0.94**

Rationale: Improvement from 0.93 due to explicit finding-ID references in test docstrings and the commit anchor. The coverage measurement gap prevents scoring higher.

---

## Weighted Composite Calculation

### Pre-Remediation vs. Post-Remediation Comparison

| Dimension | Weight | Pre-Score | Pre-Contribution | Post-Score | Post-Contribution | Delta |
|-----------|--------|-----------|-----------------|------------|------------------|-------|
| Completeness | 0.20 | 0.87 | 0.174 | 0.93 | 0.186 | +0.012 |
| Internal Consistency | 0.20 | 0.91 | 0.182 | 0.94 | 0.188 | +0.006 |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | 0.92 | 0.184 | +0.004 |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | 0.95 | 0.1425 | 0.000 |
| Actionability | 0.15 | 0.94 | 0.141 | 0.94 | 0.141 | 0.000 |
| Traceability | 0.10 | 0.93 | 0.093 | 0.94 | 0.094 | +0.001 |
| **TOTAL** | **1.00** | **--** | **0.9125** | **--** | **0.9355** | **+0.023** |

### Arithmetic Verification

```
Completeness:          0.93 × 0.20 = 0.1860
Internal Consistency:  0.94 × 0.20 = 0.1880
Methodological Rigor:  0.92 × 0.20 = 0.1840
Evidence Quality:      0.95 × 0.15 = 0.1425
Actionability:         0.94 × 0.15 = 0.1410
Traceability:          0.94 × 0.10 = 0.0940
                                    --------
Total:                              0.9355
```

**Post-Remediation Composite Score: 0.9355**

**Threshold: 0.92**

**Delta above threshold: +0.0155**

---

## Remaining Unaddressed Findings

The following findings from the Phase 4 tournament were not addressed by P1-P5. Per the tournament verdict, minor findings SHOULD be addressed before final release but do not block REVISE-to-PASS advancement.

### High-RPN FMEA Items Still Open (not required for PASS, but notable)

| Finding | RPN | Status | Risk |
|---------|-----|--------|------|
| FM #6: PreToolUse matcher misses new tool types | 147 | Open | If Claude Code adds a new file-writing tool, the security hook is not invoked |
| FM #9: Malformed `##HANDOFF:` signal (no closing `##`) | 120 | Partially mitigated (ValueError now caught; exit 2 is surfaced rather than silent miss) | Handoff not triggered; hook exits with error |
| FM #10: Spec divergence (Claude Code protocol update) | 147 | Open | All schemas become silently invalid |

### Minor Findings Still Open

| ID | Summary | Recommendation |
|----|---------|----------------|
| SR-004-20260217 | Live compliance tests in TestLiveHookOutputCompliance have no subprocess timeout | Add `timeout=10` to all subprocess.run() calls in TestLiveHookOutputCompliance |
| DA-002-20260217 | PreToolUse matcher scope undocumented (why not `".*"`?) | Add inline comment or ADR explaining tool-specific matcher scope decision |
| DA-003-20260217 | `cd` blocking conflates security and policy enforcement | Consider returning `"ask"` for policy violations, `"deny"` for genuine security threats |
| DA-004-20260217 | PostToolUse and PermissionRequest schemas have no implementing hooks | Add comments documenting forward-looking intent |
| PM-002-20260217 | Claude Code spec version not pinned in schema metadata | Document spec version in schema `description` fields |
| PM-003-20260217 | `${CLAUDE_PLUGIN_ROOT}` unset behavior undocumented | Document in README or CLAUDE.md |
| IN-001-20260217 | SubagentStop block path not tested as live compliance test | Add `TestLiveHookOutputCompliance.test_subagent_stop_block_output_schema` |
| CV-002-20260217 | "8 schemas" claim is ambiguous (9 files total including root config) | Clarify as "8 hook output schemas" in docs |
| RT-001-20260217 | Hook bypass via tool name case variation unverified | Verify Claude Code matcher case sensitivity behavior |
| RT-002-20260217 | AST enforcement scope unclear | Add scope clarification comment to pre_tool_use.py |

### Findings Partially Addressed (not fully resolved)

| ID | Status |
|----|--------|
| PM-001-20260217 | Reactive warning implemented (P5); proactive HANDOFF_RULES validation against agent registry at startup NOT implemented |
| SR-003-20260217 | `docs/experience/` directory creation issue: `log_handoff()` does call `os.makedirs(log_dir, exist_ok=True)` at line 151 in the current code — this finding was already resolved in the base code before remediation |

---

## Final Verdict

### Score Summary

| Metric | Value |
|--------|-------|
| Pre-Remediation Score | 0.9125 (REVISE) |
| Post-Remediation Score | **0.9355** |
| Threshold | 0.92 |
| Delta above threshold | +0.0155 |
| Band | **PASS** |

### Verdict: PASS

The BUG-002 Hook Schema Validation Fixes deliverable, after Phase 5 remediation, scores **0.9355** against the S-014 weighted composite rubric. This exceeds the 0.92 threshold by 15.5 thousandths. The PASS verdict is warranted.

### What Drove the Score Above Threshold

The three dimensions that were below or near threshold pre-remediation all improved materially:

1. **Completeness (0.87 -> 0.93, +0.06):** The primary driver. Creation of `test_subagent_stop.py` with 32 tests eliminating the zero-coverage gap for `subagent_stop.py` business logic (DA-001/CC-002) is the single largest contributor to score recovery.

2. **Internal Consistency (0.91 -> 0.94, +0.03):** Shebang alignment across all three scripts (P2) resolves the H-05 violation and the visual inconsistency that depressed this dimension.

3. **Methodological Rigor (0.90 -> 0.92, +0.02):** Path normalization (P3) and regex-based rm detection (P4) address the security methodology gaps identified by RT-003 and RT-004.

### Confidence Assessment

The 0.9355 score carries moderate-high confidence. The primary uncertainty is the unverified coverage percentage for `subagent_stop.py` (CC-002 resolution is stated but not measured). If coverage falls below 90%, the Completeness and Traceability scores would be revised downward, potentially as follows:

- Completeness: 0.93 -> 0.90 (coverage not actually meeting H-21)
- Traceability: 0.94 -> 0.92 (H-21 resolution unverified)
- Revised composite: ~0.928 (still PASS, but margin narrows to +0.008)

The PASS verdict is robust to this uncertainty — even the conservative estimate remains above threshold.

### Conditions on PASS

This PASS verdict applies to the Phase 5 remediation state (commit 52e3015). It does not imply the remaining minor and high-RPN open findings are acceptable for permanent deferral. They SHOULD be addressed before final OSS release.

---

*Generated by adv-scorer agent*
*Scoring ID: bug002-hookfix-20260217-001 / Phase 5 Post-Remediation*
*Date: 2026-02-17*
*Rubric: S-014 LLM-as-Judge, 6-dimension weighted composite (quality-enforcement.md)*
*Constitutional compliance: H-13 threshold enforced (0.9355 >= 0.92 -> PASS)*
