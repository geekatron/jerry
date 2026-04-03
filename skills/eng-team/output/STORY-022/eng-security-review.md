# Security Code Review: P-003 Agent Tool CI Validation

> **Engagement ID:** STORY-022
> **Reviewer:** eng-security
> **Review Date:** 2026-03-29
> **Scope:** `scripts/validate-agent-frontmatter.py` (lines 151-172) + `scripts/tests/test_validate_agent_frontmatter.py`
> **Review Dimensions:** Bypass vectors, fail-closed behavior, YAML injection, error message quality, Task alias coverage

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, overall posture, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual findings with CWE, CVSS, evidence, remediation |
| [L1 ASVS Verification](#l1-asvs-verification) | Chapter-by-chapter verification status |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic patterns, architectural observations, evolution recommendations |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| CRITICAL  | 0 |
| HIGH      | 1 |
| MEDIUM    | 3 |
| LOW       | 1 |
| INFO      | 2 |
| **Total** | **7** |

### Overall Security Assessment

The P-003 check is correctly designed. The core enforcement logic is sound: `safe_load` is used throughout, the fail-closed pattern is correctly implemented, and the backward-compatible `Task` alias is covered. One HIGH finding exists: the check is entirely bypassed when `tools` is expressed as a YAML comma-separated string (the dominant format across 70+ real agent files), creating a silent no-op rather than an enforced gate. This is not a malicious bypass vector but a structural gap that must be closed before the check can be considered effective.

### Top 3 Risk Areas

1. **String-format `tools` bypass (HIGH):** 70+ existing agent `.md` files use `tools: Read, Write, Edit...` (scalar string). The check is inside `if isinstance(tools, list)`, meaning string-format tools values are never inspected. An agent author could include `Agent, Read, Write` in a comma-string and pass CI cleanly.
2. **`tool_tier` non-string value coercion (MEDIUM):** YAML parses bare `T5` as a string, but a quoted integer or boolean could produce type confusion in the `== "T5"` comparison. The `isinstance(gov, dict)` guard is correct but does not guard the individual field type.
3. **Governance file path assumption (MEDIUM):** The governance path is derived by replacing the `.md` suffix with `.governance.yaml`. An agent file named `agent-name.governance.md` (unlikely but valid) would produce a path collision. More practically: if an agent `.md` file lives in a symlinked directory, `with_suffix` operates on the path as given and the resolved governance file may differ.

### Recommended Immediate Actions

1. **Fix the string-format `tools` gap (HIGH):** Add a pre-check that normalises the `tools` value: if it is a string, split on commas and strip whitespace before the `isinstance(tools, list)` branch. This brings all existing agent files into scope.
2. **Add a test for string-format `tools` containing `Agent` (covers the HIGH finding).**
3. **Guard `tool_tier` type in the governance check (MEDIUM):** Wrap `gov.get("tool_tier")` in `str(...)` or add an `isinstance(..., str)` guard before comparison.

---

## L1 Technical Findings

---

### FINDING-001 -- String-Format `tools` Value Bypasses P-003 Check

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **CWE** | CWE-284 Improper Access Control (logic enforcement bypass) |
| **CVSS 3.1** | 5.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N) -- local actor, low complexity, integrity impact on P-003 constraint |
| **File** | `scripts/validate-agent-frontmatter.py` lines 143-172 |
| **ASVS** | V5.1 -- Input Validation Architecture |

**Evidence:**

The P-003 check is guarded by `if isinstance(tools, list)` at line 144. Claude Code's YAML frontmatter allows `tools` as either a YAML list or a comma-separated scalar string. The majority of existing agent files use the scalar string format:

```
# String format (70+ agents in codebase):
tools: Read, Write, Edit, Glob, Grep, Agent
```

PyYAML's `safe_load` parses this as a Python `str`, not a `list`. Therefore `isinstance(tools, list)` is `False` and lines 155-172 (the entire P-003 check) are never reached. An agent author who writes:

```yaml
tools: Read, Write, Agent
```

in an `.md` file whose companion `.governance.yaml` has `tool_tier: T2` will pass CI with no P-003 error. The `mcp__` MCP tool check on line 145 has the same gap but is lower severity (it is a warning, not an error).

**Data flow trace:**

1. `main()` calls `validate_agent(fm, schema, fp)` where `fm` is the result of `extract_frontmatter(fp)`.
2. `extract_frontmatter` calls `yaml.safe_load` on the raw frontmatter text.
3. For `tools: Read, Write, Agent`, `safe_load` returns `{"tools": "Read, Write, Agent"}`.
4. Line 143: `tools = fm.get("tools")` assigns the string `"Read, Write, Agent"`.
5. Line 144: `isinstance(tools, list)` is `False` -- the entire `if` block is skipped.
6. The delegation tool check never executes.

**Verification:**

```python
import yaml
fm = yaml.safe_load("tools: Read, Write, Agent")
print(type(fm["tools"]))  # <class 'str'>
print(isinstance(fm["tools"], list))  # False
```

**Remediation:**

Normalise the `tools` value before the type check. Add a helper or inline normalisation immediately after line 143:

```python
tools = fm.get("tools")
# Claude Code permits tools as a YAML list OR a comma-separated scalar string.
# Normalise to list before any inspection.
if isinstance(tools, str):
    tools = [t.strip() for t in tools.split(",") if t.strip()]
if isinstance(tools, list):
    ...  # existing checks proceed unchanged
```

This fix also resolves the same gap for the MCP tool warning on line 145.

---

### FINDING-002 -- Missing Test: String-Format `tools` Containing `Agent`

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **CWE** | CWE-1059 Insufficient Test Coverage |
| **CVSS 3.1** | N/A (quality/coverage finding) |
| **File** | `scripts/tests/test_validate_agent_frontmatter.py` |
| **ASVS** | V1.1.1 -- Secure Development Lifecycle; testing for bypass |

**Evidence:**

All five test cases use the `tmp_agent` fixture which always writes tools as a YAML list (`fm["tools"] = tools`; `yaml.dump` serialises a Python list to YAML block sequence). No test exercises the string format. Because FINDING-001 shows the string format bypasses the check, the current test suite provides false assurance: all five tests pass even after the implementation is broken, as long as the list-format path is intact. There is no test that would catch the FINDING-001 gap.

**Remediation:**

Add a test that writes `tools: Read, Write, Agent` as a scalar string in the frontmatter:

```python
def test_non_t5_agent_with_agent_tool_string_format_produces_error(
    self, agent_schema: dict, tmp_path: Path
) -> None:
    """String-format tools field containing Agent must still trigger P-003 error."""
    # String format is the dominant real-world format in this codebase
    fm_text = "name: test-agent\ndescription: Test\ntools: Read, Write, Agent\n"
    md_path = tmp_path / "test-agent.md"
    md_path.write_text(f"---\n{fm_text}---\n\nBody.\n", encoding="utf-8")
    gov_path = tmp_path / "test-agent.governance.yaml"
    gov_path.write_text(yaml.dump({"version": "1.0.0", "tool_tier": "T2"}))
    fm = vaf.extract_frontmatter(md_path)
    errors, _ = vaf.validate_agent(fm, agent_schema, md_path)
    p003_errors = [e for e in errors if "P-003" in e]
    assert len(p003_errors) >= 1, f"String-format tools with Agent must error: {errors}"
```

---

### FINDING-003 -- `tool_tier` Type Not Explicitly Guarded

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **CWE** | CWE-704 Incorrect Type Conversion or Cast |
| **CVSS 3.1** | 3.3 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) -- requires governance file authorship, exploitable only by authorised contributor |
| **File** | `scripts/validate-agent-frontmatter.py` line 163 |
| **ASVS** | V5.1 -- Input Validation; untrusted data type coercion |

**Evidence:**

Line 163: `is_t5 = gov.get("tool_tier") == "T5"`. The `isinstance(gov, dict)` guard on line 162 is correct and protects against `gov` being `None` (YAML null) or a list. However, the `tool_tier` field itself is not type-guarded. YAML parses the following values as non-string Python types:

```yaml
tool_tier: true      # bool True -- "True" == "T5" is False (safe, fails closed)
tool_tier: 5         # int 5 -- 5 == "T5" is False (safe, fails closed)
tool_tier: T5        # str "T5" -- correct
tool_tier: 'T5'      # str "T5" -- correct
```

For the current comparison semantics (`== "T5"`), non-string values all fail closed because Python's `==` is not type-coercing for string comparisons. The risk materialises if someone later changes the comparison to use `.lower()` or `in` without first checking the type, or if the comparison is wrapped in a try/except that silently returns `is_t5 = True`. This is a latent type-safety issue, not an immediately exploitable one.

**Remediation:**

Add explicit type checking before comparison:

```python
tier_value = gov.get("tool_tier")
is_t5 = isinstance(tier_value, str) and tier_value == "T5"
```

This also makes the intent explicit for future readers and eliminates the latent risk of type-confusion bypass if the comparison logic is modified.

---

### FINDING-004 -- Governance Path Derivation Does Not Validate That `.md` Agent File Is Canonical

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **CWE** | CWE-706 Use of Incorrectly-Resolved Name or Reference |
| **CVSS 3.1** | 2.5 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N) -- highly constrained; requires non-standard file naming |
| **File** | `scripts/validate-agent-frontmatter.py` line 157 |
| **ASVS** | V5.3 -- Output Encoding; file path construction |

**Evidence:**

Line 157: `gov_path = file_path.with_suffix(".governance.yaml")`. `Path.with_suffix` replaces only the last suffix. For a file named `agent-name.md`, this produces `agent-name.governance.yaml` correctly. However:

- A file named `my-agent.test.md` produces `my-agent.test.governance.yaml` (not `my-agent.governance.yaml`). Whether this is the intended naming convention is unclear, but it means the check would always fail-closed for such files even if a legitimately T5 agent had the standard governance file.
- More importantly: if the script is invoked with an absolute path from a non-standard working directory, `with_suffix` still operates correctly (it is purely lexicographic). No traversal risk exists here.

The naming convention for governance files is defined as `{agent-name}.governance.yaml` (same stem as the `.md` file), so `with_suffix` is the correct mechanism as long as `.md` files have a single-component suffix. This is consistent with every existing agent file in the codebase.

The risk is low and requires an unusual file name, but the code should document the assumption to prevent silent governance bypass for files with multi-component suffixes.

**Remediation:**

Add an assertion or warning in the check to document the assumption:

```python
gov_path = file_path.with_suffix(".governance.yaml")
# Safety: with_suffix replaces only the last suffix. Assumes agent .md files
# have exactly one suffix component (e.g., "agent-name.md" -> "agent-name.governance.yaml").
# Files with multi-component suffixes (e.g., "agent.test.md") will resolve to an
# unexpected path and fail closed, which is the correct behavior.
```

Alternatively, enforce the single-suffix assumption with an explicit check:

```python
if file_path.suffix != ".md":
    # Unexpected: agent files should always end in .md
    # fail closed
    errors.append(f"  path: unexpected suffix '{file_path.suffix}' (expected .md)")
    return errors, warnings
gov_path = file_path.with_name(file_path.stem + ".governance.yaml")
```

---

### FINDING-005 -- `safe_load` on Governance File Is Correct; No YAML Injection Risk

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **CWE** | CWE-502 Deserialization of Untrusted Data (mitigated) |
| **CVSS 3.1** | 0.0 (mitigated) |
| **File** | `scripts/validate-agent-frontmatter.py` line 161 |
| **ASVS** | V5.5.3 -- Deserialization; safe deserializer usage |

**Evidence:**

Line 161: `gov = yaml.safe_load(gov_path.read_text(encoding="utf-8"))`. PyYAML's `safe_load` only constructs basic Python types (dict, list, str, int, float, bool, None). It does not resolve YAML tags such as `!!python/object` and cannot instantiate arbitrary Python classes. No YAML injection vector exists through this code path. The governance schema defines `tool_tier` as a string enum, and the comparison at line 163 operates only on the resulting Python string value.

The CI pipeline's `security` job (`.github/workflows/ci.yml` lines 98-113) additionally enforces `yaml.safe_load` at the grep level for `src/` Python files. The scripts directory is not covered by that grep but `safe_load` is used correctly here.

**Status:** No action required. Confirmed mitigated. Recommend extending the CI yaml.load grep to `scripts/` as a defence-in-depth measure (see FINDING-007).

---

### FINDING-006 -- Error Message Is Actionable and Does Not Leak Sensitive Information

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **CWE** | CWE-209 Generation of Error Message Containing Sensitive Information (not present) |
| **CVSS 3.1** | 0.0 |
| **File** | `scripts/validate-agent-frontmatter.py` lines 167-172 |
| **ASVS** | V7.4.1 -- Error Handling; informative but non-leaking error messages |

**Evidence:**

The error message at lines 167-172:

```
tools: contains ['Agent'] — only T5 orchestrator agents may have Agent/Task tool access (P-003 violation). Fix: remove ['Agent'] from tools list, or set tool_tier: T5 in {gov_path.name} with documented justification.
```

The message:
- Names the offending tools (`delegation_tools` variable, which contains only `"Agent"` and/or `"Task"` -- no user-controlled injection into the message format string beyond these validated values).
- Provides two concrete remediation paths (remove tool, or set T5 with justification).
- Uses `gov_path.name` (filename only, not full path) -- no absolute path information is leaked.
- Does not disclose internal state, credentials, or stack traces.

The f-string interpolation at line 172 uses `gov_path.name` (not `gov_path` which would be the full path). The `delegation_tools` list is constructed at line 155 by filtering against a hardcoded set `("Agent", "Task")`, so the message cannot be injected by a malicious tools field value.

**Status:** No action required. Error message quality is good.

---

### FINDING-007 -- YAML `safe_load` Enforcement Grep Does Not Cover `scripts/`

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **CWE** | CWE-1350 Weaknesses in the 2023 CWE Top 25 (defence-in-depth) |
| **CVSS 3.1** | 2.0 (informational; defence-in-depth gap, not exploitable via this code) |
| **File** | `.github/workflows/ci.yml` lines 99-113 |
| **ASVS** | V14.2.5 -- Dependency and Redundancy; defence-in-depth controls |

**Evidence:**

The CI security job checks for `yaml.load()` and `yaml.unsafe_load()` but scopes its grep to `src/` only:

```bash
grep -rn 'yaml\.load(' src/ --include='*.py' | grep -v 'yaml\.safe_load('
```

The `scripts/` directory is excluded. While the reviewed file already uses `safe_load` correctly, a future change to `scripts/` could introduce `yaml.load()` without the CI check flagging it. This is a defence-in-depth gap, not a current vulnerability.

**Remediation:**

Extend the grep in `.github/workflows/ci.yml` to include `scripts/`:

```bash
if grep -rn 'yaml\.load(' src/ scripts/ --include='*.py' | grep -v 'yaml\.safe_load('; then
```

Or alternatively, use a single recursive search from the repository root while excluding test fixtures that may intentionally contain the pattern:

```bash
if grep -rn 'yaml\.load(' . --include='*.py' \
    --exclude-dir='.venv' --exclude-dir='__pycache__' \
    | grep -v 'yaml\.safe_load('; then
```

---

## L1 ASVS Verification

Chapters relevant to a CI validation script that reads YAML files and enforces governance constraints.

| ASVS Chapter | Requirement | Status | Evidence |
|---|---|---|---|
| V1.1 -- Architecture | V1.1.1: Verify use of secure development lifecycle in CI | PASS | Frontmatter validation runs in `frontmatter-validation` CI job; check is deterministic and enforced on every PR |
| V5.1 -- Input Validation Architecture | V5.1.3: Verify input validation performed server-side (or in this context: in the authoritative validator, not just in tests) | PARTIAL | FINDING-001: string-format `tools` values are not validated. The check is absent for the dominant real-world input format |
| V5.3 -- Output Encoding | V5.3.4: Verify file paths constructed from user input are sanitised | PASS | `gov_path` is derived from a validated `Path` object using `with_suffix`, not string concatenation; no traversal possible. FINDING-004 notes a minor multi-suffix edge case with LOW risk |
| V5.5 -- Deserialization | V5.5.3: Verify that only safe deserializers are used for YAML | PASS | `yaml.safe_load` used in all three YAML parse calls (frontmatter extraction at line 100, governance load at line 161). FINDING-007 flags the defence-in-depth gap in CI enforcement scope |
| V7.4 -- Error Handling | V7.4.1: Verify error messages do not disclose sensitive information | PASS | FINDING-006 confirms message is informative and non-leaking |
| V14.2 -- Dependency Integrity | V14.2.5: Verify all components are scanned for vulnerabilities | PASS with gap | pip-audit runs in CI; scheduled security scan runs daily. FINDING-007 notes defence-in-depth gap in YAML grep scope |

---

## L2 Strategic Implications

### Security Posture Assessment

The implementation demonstrates good security instincts: `safe_load` is used correctly, the fail-closed design is a principled choice, and the error message is well-crafted. The single HIGH finding is a structural gap rather than a design flaw -- the author wrote a correct check for the list-format case but did not account for the string-format case that dominates the real codebase. This is a test-coverage failure as much as a code failure: had a test been written against a real agent file instead of synthesised fixture data, the gap would have been visible immediately.

### Systemic Pattern: Fixture Data Diverges from Real Data

FINDING-001 and FINDING-002 share a root cause: the test fixture (`tmp_agent`) always produces list-format tools because `yaml.dump` serialises Python lists to YAML block sequences. No test ever exercises the string format because no test ever reads a real agent file. This pattern -- using synthetic fixtures that subtly differ from production data -- is the primary driver of false assurance in this test suite. The mitigation is to add at least one test that uses the literal string format as it appears in the codebase (see FINDING-002 remediation).

### Comparison with Threat Model Predictions

The H-35 constitutional constraint (worker agents MUST NOT include `Agent` in tools) requires a deterministic enforcement layer. The reviewed check is intended to be that L5 CI layer. FINDING-001 means the L5 layer currently has a non-trivial bypass for the majority of real agent file formats. The L3 (pre-tool schema check) enforcement described in `agent-development-standards.md` would partially compensate, but CI enforcement is the primary line of defence against committed violations.

### Recommendations for Security Architecture Evolution

1. **Normalise at extraction time, not at check time.** The `extract_frontmatter` function should return a normalised dict where `tools` is always a list (or absent). This would benefit all callers and centralise the normalisation logic, preventing the same gap from recurring in future checks added to `validate_agent`.

2. **Add real agent file smoke tests.** Supplement the synthetic fixture tests with parametrised tests that load actual agent `.md` files from `skills/*/agents/*.md` and verify they produce no false-positive errors. This would catch format divergences between fixtures and production files.

3. **Consider schema enforcement for governance `tool_tier` field type.** The governance JSON schema already declares `tool_tier` as a string enum. If the JSON Schema validation step (the `jsonschema.Draft202012Validator` run on governance files, which is a separate CI gate) were extended to cover `.governance.yaml` files, it would provide an independent enforcement layer for `tool_tier` type correctness. This does not exist today -- the governance validation runs only on agent `.md` frontmatter, not on `.governance.yaml` files.

4. **Extend YAML safe_load CI grep to `scripts/`** to close the defence-in-depth gap identified in FINDING-007.

---

## Finding Summary

| ID | Severity | Title | File | Lines | Action Required |
|----|----------|-------|------|-------|----------------|
| FINDING-001 | HIGH | String-format `tools` bypasses P-003 check | `validate-agent-frontmatter.py` | 143-155 | Fix normalisation before type check |
| FINDING-002 | MEDIUM | No test for string-format `tools` with Agent | `test_validate_agent_frontmatter.py` | -- | Add test case |
| FINDING-003 | MEDIUM | `tool_tier` field not type-guarded | `validate-agent-frontmatter.py` | 163 | Add `isinstance(..., str)` guard |
| FINDING-004 | MEDIUM | Governance path multi-suffix edge case | `validate-agent-frontmatter.py` | 157 | Document assumption or add guard |
| FINDING-005 | INFO | `safe_load` correctly used -- no injection risk | `validate-agent-frontmatter.py` | 161 | No action |
| FINDING-006 | INFO | Error message is actionable, non-leaking | `validate-agent-frontmatter.py` | 167-172 | No action |
| FINDING-007 | LOW | YAML `safe_load` CI grep excludes `scripts/` | `.github/workflows/ci.yml` | 99-103 | Extend grep scope |

---

*Review Method: Manual data flow tracing, CWE Top 25 2025 checklist, OWASP ASVS 5.0 chapter verification*
*Standards: CWE-284, CWE-502, CWE-704, CWE-706, CWE-1059; ASVS V1.1, V5.1, V5.3, V5.5, V7.4, V14.2*
*Agent: eng-security*
*SSDF Practice: PW.7 (Review and/or analyze human-readable code to identify vulnerabilities)*
