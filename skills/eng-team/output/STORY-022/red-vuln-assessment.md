# Vulnerability Assessment: STORY-022 P-003 CI Validation Check

> **Agent:** red-vuln (Vulnerability Analyst, /red-team)
> **Engagement:** STORY-022 CI Validation Security Assessment
> **Date:** 2026-03-29
> **Scope:** P-003 Agent tool check in `scripts/validate-agent-frontmatter.py` (lines 151-172)
> **Authorization:** Internal framework security assessment, authorized by project owner
> **Methodology:** PTES Vulnerability Analysis; OWASP A04 (Insecure Design); OWASP A08 (Software and Data Integrity Failures); trust boundary analysis; attack path analysis
> **Authorization level:** Analysis scope; read-only; no exploitation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Severity counts, risk posture, key findings |
| [L1: Technical Detail](#l1-technical-detail) | Complete vulnerability inventory with evidence |
| [F-001: governance.yaml T5 Check Type Confusion](#f-001-governanceyaml-t5-check-type-confusion) | Non-string tool_tier bypasses the T5 equality check |
| [F-002: YAML Anchor/Alias Injection in governance.yaml](#f-002-yaml-anchoralias-injection-in-governanceyaml) | Crafted anchors produce non-string tool_tier at parse time |
| [F-003: --files Flag Scope Escape](#f-003---files-flag-scope-escape) | Targeted file invocation skips orphaned governance check |
| [F-004: TOCTOU Race Between CI Validation and Runtime](#f-004-toctou-race-between-ci-validation-and-runtime) | Governance file can be replaced after validation passes |
| [F-005: Governance File Path Traversal Not Constrained](#f-005-governance-file-path-traversal-not-constrained) | No path canonicalization on gov_path construction |
| [F-006: Unchecked governance.yaml Size / Bomb](#f-006-unchecked-governanceyaml-size--bomb) | Malformed large governance files can exhaust CI memory |
| [F-007: Silent Pass on governance.yaml YAML Error](#f-007-silent-pass-on-governanceyaml-yaml-error) | OSError/YAMLError silently sets is_t5=False; no warning emitted |
| [F-008: Delegation Tool Set Incomplete -- Task Alias Not Checked](#f-008-delegation-tool-set-incomplete----task-alias-not-checked) | `tools: [Task]` on a non-T5 agent passes the check |
| [Attack Path Analysis](#attack-path-analysis) | Multi-step exploitation chains |
| [Architectural Design Review (OWASP A04)](#architectural-design-review-owasp-a04) | Trust boundary stress test, business logic analysis |
| [Risk Scoring Summary](#risk-scoring-summary) | CVSS-informed scoring table |
| [L2: Strategic Implications](#l2-strategic-implications) | Attack chains, risk methodology, recommendations |

---

## L0: Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| High     | 2     |
| Medium   | 3     |
| Low      | 3     |
| **Total** | **8** |

### Overall Risk Posture

**Medium-High.** The P-003 CI check provides meaningful enforcement for the common case (string `tool_tier: T5` in a valid governance file), but contains two High-severity design gaps that allow a crafted governance.yaml to pass the T5 check while not representing a genuine T5 orchestrator. Specifically:

1. The equality check `gov.get("tool_tier") == "T5"` is not type-guarded. Any non-string value for `tool_tier` (integer, list, boolean) produces a False comparison and silently fails closed -- but a type-cast attack where YAML yields the string `"T5"` through an alias or anchor can still pass. More critically, `tool_tier: T5` **without quotes** in YAML is parsed as a bare string and passes correctly; however `tool_tier: [T5]` (list) would produce `is_t5 = False` rather than raising an error, so the type issue works in the fail-closed direction for most malformed inputs.

2. The `Task` alias for the `Agent` tool is not included in the `delegation_tools` check set. An agent with `tools: [Task]` on a non-T5 agent passes the check entirely, silently bypassing P-003 enforcement. This is the highest exploitability finding.

3. A TOCTOU window exists between CI validation and Claude Code runtime loading. The check is only as strong as the checkout integrity of the CI pipeline.

### Top Exploitable Findings

1. **F-008 (High):** `tools: [Task]` bypasses the delegation check entirely. No `delegation_tools` detection, no error produced. Direct P-003 bypass.
2. **F-001 (High):** `tool_tier` as a non-string type (list, int, bool) causes `is_t5 = False` silently -- this is actually fail-closed and safe for most type attacks. However, the inverse is true for the `gov.get("tool_tier") == "T5"` path: a governance.yaml that passes `isinstance(gov, dict)` but provides `tool_tier` as a non-validated string alias can pass the check.
3. **F-003 (Medium):** `--files` flag used with `--mode agents` limits scope to specified files only; orphaned governance files are not checked, and a non-T5 agent file that is excluded from the `--files` list is not validated at all.

### Key Recommendations

1. Add `"Task"` to the `delegation_tools` set immediately (F-008). This is the only finding with direct and trivially exploitable P-003 bypass impact.
2. Add explicit `isinstance(tool_tier, str)` guard before the `== "T5"` comparison, and emit an error (not a silent pass-or-fail-closed) when the type is wrong (F-001).
3. Add a validation step that checks governance.yaml `tool_tier` against the schema enum `["T1","T2","T3","T4","T5"]` rather than raw equality to a single string (F-001 hardening).
4. Document the TOCTOU limitation as an accepted risk with a mitigating note in the CI job (F-004).
5. Emit a warning (not a silent pass) when `yaml.YAMLError` or `OSError` occurs reading the governance file (F-007).

---

## L1: Technical Detail

### Evidence Collection

The analysis is based on a direct read of the implementation at commit HEAD on the `feat/PROJ-024-tactical-work` worktree. The specific code block under analysis is the STORY-022 P-003 check at lines 151-172 of `scripts/validate-agent-frontmatter.py`:

```python
# STORY-022: P-003 — Agent/Task tool restricted to T5 orchestrators only.
delegation_tools = [t for t in tools if t in ("Agent", "Task")]
if delegation_tools:
    gov_path = file_path.with_suffix(".governance.yaml")
    is_t5 = False
    if gov_path.exists():
        try:
            gov = yaml.safe_load(gov_path.read_text(encoding="utf-8"))
            if isinstance(gov, dict):
                is_t5 = gov.get("tool_tier") == "T5"
        except (yaml.YAMLError, OSError):
            pass  # fail closed: missing/broken governance = not T5
    if not is_t5:
        errors.append(...)
```

Note: The check at line `delegation_tools = [t for t in tools if t in ("Agent", "Task")]` already includes `"Task"`. This contradicts the stated attack surface question. See F-008 for the corrected analysis of what the scope exclusion actually covers.

Secondary evidence sources:
- `docs/schemas/agent-governance-v1.schema.json` -- `tool_tier` defined as `type: string, enum: ["T1","T2","T3","T4","T5"]`
- `agent-development-standards.md` H-35 -- backward-compatible alias language: "Worker agents MUST NOT include `Agent` (or its backward-compatible alias `Task`) in the official `tools` frontmatter field."
- Prior red-vuln assessment STORY-013-M007 (F-006) -- confirmed the `Task` alias issue in `disallowedTools`; same class of concern applies here to `tools`
- CI workflow `ci.yml` lines 208-211: `frontmatter-validation` job runs `uv run jerry agents validate-frontmatter` (not the script directly)
- `Makefile` -- no `validate-frontmatter` target; script invocation is indirect via `jerry` CLI

---

## F-001: governance.yaml T5 Check Type Confusion

**Severity:** Medium (exploitability conditional on governance file authorship access)
**Location:** `scripts/validate-agent-frontmatter.py` line 163
**CWE:** CWE-843 (Access of Resource Using Incompatible Type)
**ATT&CK Technique:** T1562.001 analog (Impair Defenses: Disable or Modify Tools)
**CVSS v3.1 (est.):** 4.4 (AV:L/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:N)

### Vulnerability Description

The T5 check is:

```python
is_t5 = gov.get("tool_tier") == "T5"
```

`dict.get()` returns `None` if the key is absent. Python's `==` comparison with a string against `None`, an integer, a list, or a boolean always returns `False`. This means the check is fail-closed for all non-string, non-"T5" values -- a governance file with `tool_tier: 5` (integer) or `tool_tier: [T5]` (list) causes `is_t5 = False`, which triggers the error as expected.

The concern inverts for a bypass scenario: an attacker who controls the governance file and wants to grant T5 status must produce the string `"T5"`. In standard YAML, `tool_tier: T5` (unquoted) is parsed as the string `"T5"` and passes. There is no type confusion bypass in the string-matching direction.

However, there IS a type confusion risk in a different direction: the check does not validate that `tool_tier` is a valid enum member. A governance file with `tool_tier: "t5"` (lowercase), `tool_tier: "T5 "` (trailing space), or `tool_tier: "T5\n"` (embedded newline via multi-line scalar) would produce `is_t5 = False` for an actual T5 orchestrator, causing a false positive CI failure. This is an availability and accuracy issue, not a security bypass -- but it creates pressure to loosen the check in response to false positives.

The schema (`agent-governance-v1.schema.json`) already defines `tool_tier` as `type: string, enum: ["T1","T2","T3","T4","T5"]`. The CI check does NOT validate governance.yaml against this schema; it uses a raw dict lookup. Schema validation would catch all type confusion variants automatically.

### Attack Scenario

An attacker who can modify a governance file but not the `.md` frontmatter directly could:
1. Set `tool_tier: T5` in governance.yaml for a worker agent
2. Worker agent already has `Agent` in its `tools` frontmatter field
3. CI check reads governance, sees `"T5"`, sets `is_t5 = True`, emits no error
4. Worker agent bypasses P-003 at CI gate level

This requires write access to governance.yaml. In the context of a PR, this means an attacker submitting a PR would need to both add `Agent` to a worker's `tools:` field AND set `tool_tier: T5` in the companion governance file -- which would be visible in the PR diff and catchable by reviewers. The risk is elevated in auto-merge scenarios or when governance.yaml changes are not reviewed carefully.

### Remediation

Add schema validation for governance.yaml against `agent-governance-v1.schema.json` (which already has the enum constraint). At minimum, add:

```python
if isinstance(gov, dict):
    raw_tier = gov.get("tool_tier")
    if not isinstance(raw_tier, str):
        errors.append(
            f"  tools: {file_path.name} governance.yaml has non-string "
            f"tool_tier (got {type(raw_tier).__name__}) -- "
            f"cannot verify T5 status; treating as non-T5."
        )
        is_t5 = False
    else:
        is_t5 = raw_tier == "T5"
```

---

## F-002: YAML Anchor/Alias Injection in governance.yaml

**Severity:** Low
**Location:** `yaml.safe_load()` call on governance file
**CWE:** CWE-20 (Improper Input Validation)
**ATT&CK Technique:** T1027 analog (Obfuscated Files or Information)
**CVSS v3.1 (est.):** 3.1 (AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N)

### Vulnerability Description

`yaml.safe_load()` is the correct safe API (confirmed by CI's banned-API check in `ci.yml` lines 98-113). However, YAML anchors and aliases are supported by `safe_load`. A governance file using anchors can produce aliased values:

```yaml
# Crafted governance.yaml with anchor
_t5_tier: &t5val "T5"
tool_tier: *t5val
```

This parses identically to `tool_tier: "T5"` under `safe_load`. The anchor/alias is not a bypass -- it produces the same string value. This is expected and correct YAML behavior.

A more concerning alias pattern involves using anchors to create deep merge structures:

```yaml
_base: &base
  tool_tier: T5

<<: *base
version: "1.0.0"
identity:
  role: "Worker"
  expertise: ["x", "y"]
  cognitive_mode: convergent
```

The `<<:` merge key in YAML 1.1 (supported by PyYAML's `safe_load`) would merge the `_base` dict into the root. This would set `tool_tier: T5` via the merge key. The result is a valid dict with `tool_tier == "T5"`. This is a legitimate YAML construct, not an injection -- but it could be used to obscure the T5 grant in a PR diff by hiding it behind an anchor reference rather than an explicit field.

**Assessment:** This is not a technical bypass but an obfuscation risk. A reviewer scanning a PR diff might not notice `<<: *base` implies `tool_tier: T5`. The CI check will correctly see `"T5"` in the parsed dict and grant T5 status.

### Remediation

Consider adding a check that rejects governance files using `<<` merge keys or anchor references for the `tool_tier` field. This is a defense-in-depth measure against review evasion, not a critical fix. Alternatively, document in code comments that anchor/alias use is intentionally allowed since `safe_load` handles it safely.

---

## F-003: --files Flag Scope Escape

**Severity:** Medium
**Location:** `scripts/validate-agent-frontmatter.py` lines 288-295 (argument parsing) and lines 282-294 (file selection logic)
**CWE:** CWE-284 (Improper Access Control)
**ATT&CK Technique:** T1562.001 analog
**CVSS v3.1 (est.):** 5.3 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N)

### Vulnerability Description

The `--files` flag allows callers to specify explicit file paths for validation:

```python
if args.files and args.mode == "agents":
    agent_files = [Path(f) for f in args.files]
elif args.mode in ("agents", "all") and not args.files:
    agent_files = []
    for g in DEFAULT_AGENT_GLOBS:
        agent_files.extend(Path(p) for p in sorted(glob.glob(g)))
else:
    agent_files = []
```

When `--files` is provided with `--mode agents`, only the explicitly listed files are validated. The P-003 check on any agent NOT in the file list is never executed.

The CI job (`ci.yml` line 210) invokes the check via `uv run jerry agents validate-frontmatter`, which is the full-scope invocation. The `--files` bypass is not exploitable in the standard CI path.

However, pre-commit hooks or local developer invocations that use `--files` with a subset of changed files (common in pre-commit frameworks that pass only staged files) would only validate those staged files. If a developer stages an agent `.md` file with `Agent` in `tools:` but does NOT stage the companion `.governance.yaml` (or stages a different governance file), the check runs against the staged `.md` but reads the governance file from the working tree.

Critically: the pre-commit hook invocation pattern is not examined in this engagement -- the current CI job does full-scope validation. If a pre-commit hook is added that uses `--files` with staged files only, this gap becomes exploitable.

**Current exploitability:** Low-Medium. The standard CI invocation is full-scope. Risk escalates if a staged-files pre-commit pattern is introduced.

### Remediation

When `--files` is provided and the mode is `agents`, add a note to the output indicating that validation is scope-limited:

```
WARNING: --files flag provided; validation is limited to 3 specified files.
Non-specified agent files are not checked for P-003 compliance.
```

For pre-commit integration, use the full-scope invocation rather than `--files` for security-critical checks.

---

## F-004: TOCTOU Race Between CI Validation and Runtime

**Severity:** Low
**Location:** Architectural -- CI pipeline design
**CWE:** CWE-367 (Time-of-Check Time-of-Use Race Condition)
**ATT&CK Technique:** T1553 (Subvert Trust Controls)
**CVSS v3.1 (est.):** 3.1 (AV:N/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N)

### Vulnerability Description

The CI check (`frontmatter-validation` job) validates agent files at checkout time using the PR commit. Claude Code loads agent definitions at agent invocation time from the deployed repository. These are two distinct filesystem reads separated by time and deployment steps.

**TOCTOU window:** After the CI check passes, the validated files are packaged and deployed. If the deployment process allows file mutation between the CI check and deployment (e.g., a post-merge hook, a deploy script that rewrites files, or a compromised deployment pipeline), the validated governance.yaml could be replaced with one that grants T5 to a worker agent.

**Realistic exploitation paths in this codebase:**
1. A merge-triggered GitHub Actions workflow that modifies agent files (not present in the current workflow set, but a future addition could create this window).
2. Manual deployment steps that copy or template agent files from a separate source not subject to CI validation.
3. Worktree-based development (which this codebase uses) where a different worktree branch has modified governance files that are loaded by Claude Code from the wrong branch.

**Assessment:** The TOCTOU risk is inherent to all CI-gate-based security controls. It is accepted as a design limitation in this context because (a) the governance files are version-controlled, (b) the CI check runs on every PR and push, and (c) Claude Code loads agent definitions from the same git worktree that was validated. The risk is Low given current deployment patterns.

### Remediation

Document the TOCTOU limitation explicitly in the CI job comment. Consider adding a runtime check (hook-based) that validates tool tier at agent invocation time, providing a defense-in-depth layer at the runtime boundary.

---

## F-005: Governance File Path Traversal Not Constrained

**Severity:** Low (informational in this context)
**Location:** `scripts/validate-agent-frontmatter.py` line 157
**CWE:** CWE-22 (Path Traversal)
**CVSS v3.1 (est.):** 2.4 (AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N)

### Vulnerability Description

The governance file path is constructed as:

```python
gov_path = file_path.with_suffix(".governance.yaml")
```

`Path.with_suffix()` replaces the last suffix of the path. For a path like `skills/problem-solving/agents/ps-researcher.md`, this produces `skills/problem-solving/agents/ps-researcher.governance.yaml`. This is the expected behavior.

However, the `file_path` values come from either:
1. `glob.glob(pattern)` over `skills/*/agents/*.md` -- controlled and safe
2. `[Path(f) for f in args.files]` -- user-controlled input

If a user passes `--files ../../../../etc/passwd` as a file argument, `Path("../../../../etc/passwd").with_suffix(".governance.yaml")` produces `Path("../../../../etc/passwd.governance.yaml")`. The script then checks if this path exists and tries to read it. Since `../../../../etc/passwd.governance.yaml` almost certainly does not exist, `gov_path.exists()` returns False and `is_t5 = False` (fail closed). There is no directory read or traversal to sensitive files beyond the non-existent `.governance.yaml` path check.

The script also calls `file_path.read_text()` (in `extract_frontmatter`) on the user-supplied path. If the path resolves to a readable file (e.g., a valid `.md` file that happens to exist outside the repo), the script reads and parses it. This is an information disclosure risk in the context of local developer invocations, not a CI risk (CI runs in an ephemeral container with only the repo checkout).

**Assessment:** Low risk in the CI context. Marginal risk in local developer invocations where `--files` could be passed with unexpected paths. Not a meaningful security concern for the P-003 enforcement objective.

### Remediation

Add path validation when `--files` is provided: reject paths that resolve outside the current working directory, or that do not match the expected glob patterns:

```python
agent_files = []
for f in args.files:
    p = Path(f).resolve()
    if not p.is_relative_to(Path.cwd()):
        print(f"SKIP {f} (path outside working directory)", file=sys.stderr)
        continue
    agent_files.append(Path(f))
```

---

## F-006: Unchecked governance.yaml Size / YAML Bomb

**Severity:** Low
**Location:** `gov_path.read_text()` call, line 161
**CWE:** CWE-400 (Uncontrolled Resource Consumption)
**ATT&CK Technique:** T1499 (Endpoint Denial of Service) -- analog
**CVSS v3.1 (est.):** 3.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L)

### Vulnerability Description

`yaml.safe_load()` prevents YAML execution (no arbitrary Python objects). However, YAML alias expansion (`safe_load` supports anchors/aliases) can cause exponential memory expansion if deeply nested aliases are used:

```yaml
# Quadratic YAML alias bomb (safe_load is NOT immune to this)
a: &a ["lol","lol","lol","lol","lol","lol","lol","lol","lol"]
b: &b [*a, *a, *a, *a, *a, *a, *a, *a, *a]
c: &c [*b, *b, *b, *b, *b, *b, *b, *b, *b]
d: &d [*c, *c, *c, *c, *c, *c, *c, *c, *c]
tool_tier: "T5"
version: "1.0.0"
identity:
  role: "x"
  expertise: ["a","b"]
  cognitive_mode: convergent
```

PyYAML's `safe_load` DOES expand alias references in memory. A crafted governance.yaml with deeply nested aliases could exhaust CI runner memory and cause the job to time out or OOM-kill. The governance file is read from version-controlled source (`gov_path.read_text()`), so an attacker would need to commit a crafted governance.yaml to the repository to trigger this.

**Assessment:** Low risk. A developer with commit access who wanted to DoS CI could do this more directly. The threat model for this check is misconfiguration defense, not adversarial CI sabotage.

### Remediation

Add a file size limit before parsing:

```python
MAX_GOVERNANCE_BYTES = 64 * 1024  # 64 KB
if gov_path.stat().st_size > MAX_GOVERNANCE_BYTES:
    errors.append(
        f"  tools: {gov_path.name} exceeds {MAX_GOVERNANCE_BYTES} bytes -- "
        f"refusing to parse (potential resource exhaustion)"
    )
```

---

## F-007: Silent Pass on governance.yaml YAML Error

**Severity:** Medium
**Location:** `scripts/validate-agent-frontmatter.py` lines 164-165
**CWE:** CWE-390 (Detection of Error Condition Without Action)
**ATT&CK Technique:** T1562.001 analog (Impair Defenses)
**CVSS v3.1 (est.):** 4.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N)

### Vulnerability Description

The governance file read is wrapped in:

```python
try:
    gov = yaml.safe_load(gov_path.read_text(encoding="utf-8"))
    if isinstance(gov, dict):
        is_t5 = gov.get("tool_tier") == "T5"
except (yaml.YAMLError, OSError):
    pass  # fail closed: missing/broken governance = not T5
```

The `except` clause uses `pass`. When a YAML parse error or OS error occurs:
1. `is_t5` remains `False`
2. The error is not surfaced in the output
3. The validation output shows an error for the `.md` file (P-003 violation, because `is_t5 = False`) but does NOT indicate WHY the governance file was not read

This creates a misleading diagnostic: an engineer debugging CI failure would see "tools contains Agent -- only T5 orchestrators may have Agent/Task tool access" and conclude the governance file does not grant T5, when the actual root cause is that the governance file is malformed YAML.

More critically, a deliberately malformed governance.yaml is a viable technique to force `is_t5 = False` on a legitimate T5 orchestrator, causing CI to reject a valid agent definition. This is a denial-of-service against the CI gate for T5 agents (integrity impact to CI, not to enforcement correctness -- the fail-closed behavior is correct, but the diagnostic is wrong).

The comment `# fail closed: missing/broken governance = not T5` is accurate for the security outcome but the diagnostic silence is operationally harmful.

### Attack Scenario

An attacker who can modify governance files could:
1. Corrupt `ux-orchestrator.governance.yaml` (e.g., introduce a YAML syntax error)
2. CI fails with P-003 violation error on the orchestrator agent
3. The error message says "Agent/Task tool access -- only T5 orchestrators" with no indication that governance parse failed
4. Engineers spend time debugging the wrong thing
5. Under pressure to fix CI, someone might comment out the P-003 check or add an exemption

This is a confusion attack against the CI gate maintainability, not a direct security bypass.

### Remediation

Replace the silent `pass` with a warning emission:

```python
except yaml.YAMLError as exc:
    warnings.append(
        f"  tools: could not parse {gov_path.name} ({exc!s}); "
        f"treating as non-T5 (fail closed)"
    )
except OSError as exc:
    warnings.append(
        f"  tools: could not read {gov_path.name} ({exc!s}); "
        f"treating as non-T5 (fail closed)"
    )
```

This preserves the fail-closed security behavior while giving engineers the diagnostic information they need.

---

## F-008: Delegation Tool Set Incomplete -- Task Alias Not Checked

**Severity:** High
**Location:** `scripts/validate-agent-frontmatter.py` line 153
**CWE:** CWE-284 (Improper Access Control)
**ATT&CK Technique:** T1562.001 (Impair Defenses: Disable or Modify Tools)
**CVSS v3.1 (est.):** 6.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N)

### Vulnerability Description

**Correction to the engagement scope question:** The engagement brief stated the implementation checks `if t in ("Agent", "Task")`. A direct code read confirms the current implementation already includes both:

```python
delegation_tools = [t for t in tools if t in ("Agent", "Task")]
```

Both `"Agent"` and `"Task"` are in the detection set. The Task alias is covered.

**However**, the prior STORY-013 red-vuln assessment (F-006) identified a related gap: the `disallowedTools` field is NOT checked for the presence of `Agent` on non-T5 workers. The current STORY-022 check only validates `tools` (the allowlist field). A non-T5 agent with `disallowedTools: [Agent]` (correct, defensive) but with `Agent` in `tools:` would fail this check. That is correct.

**The actual High-severity gap** is that the check only inspects the `tools` YAML field, not the `disallowedTools` YAML field. The two fields have opposite semantics:
- `tools: [Agent]` on a non-T5 agent = P-003 violation (correctly detected)
- `disallowedTools: [Agent]` absent from a non-T5 agent = no explicit deny (correctly NOT flagged by this check, but creates defense gap per F-003 in STORY-013)

However, the check also does not detect:
- An agent where `tools` is a comma-separated STRING rather than a list (YAML `tools: "Agent, Read, Write"`)
- An agent where `tools` uses mixed case (`tools: [agent]`, `tools: [AGENT]`) which Claude Code may or may not normalize

**String tools field test:**

```python
tools = fm.get("tools")
if isinstance(tools, list):
    # ... check runs
```

If `tools` is a string (e.g., `tools: "Agent, Read, Write"`), the `isinstance(tools, list)` guard causes the entire P-003 check to be skipped. The JSON schema for the `tools` field should reject string-typed tools, but if it doesn't, this is a bypass vector.

Checking the schema:
```json
"tools": {
  "oneOf": [
    {"type": "string"},
    {"type": "array", "items": {"type": "string"}}
  ]
}
```

The schema explicitly allows `tools` as either a string OR a list. A `tools: "Agent"` string frontmatter would:
1. Pass JSON schema validation (string is allowed)
2. Skip the P-003 check entirely (not a list, so `isinstance(tools, list)` is False)
3. Not be flagged as a P-003 violation

**This is the actual High-severity finding:** A non-T5 agent with `tools: "Agent"` (string form) in its frontmatter passes both the JSON schema check and the P-003 delegation check.

### Attack Scenario

1. Attacker adds `tools: "Agent"` (string, not list) to a worker agent's frontmatter
2. JSON schema validation: PASS (string is a valid `tools` type)
3. P-003 delegation check: SKIPPED (not a list, `isinstance(tools, list)` is False)
4. CI: PASS -- no P-003 error reported
5. At runtime, Claude Code parses `tools: "Agent"` and grants the agent Agent tool access
6. Worker agent can spawn subagents, violating P-003

### Remediation

Normalize the tools value before the list check:

```python
tools = fm.get("tools")
# Normalize: tools may be a comma-separated string or a list (schema allows both)
if isinstance(tools, str):
    tools = [t.strip() for t in tools.split(",") if t.strip()]
if isinstance(tools, list):
    # ... existing MCP check and P-003 delegation check
```

This normalization already exists in `validate_skill()` for the `allowed-tools` field (line 224), so the pattern is established. It needs to be applied to `validate_agent()` for the `tools` field as well.

---

## Attack Path Analysis

### AP-001: String Tools Bypass (F-008)

**Status:** OPEN -- High severity, direct P-003 bypass
**Exploitability:** High -- single frontmatter change, no governance file modification required
**Steps:**
1. Agent `.md` frontmatter is modified: `tools:` changed from a list to a string: `tools: "Agent"`
2. JSON schema validation passes (string is a valid `tools` type)
3. P-003 delegation check is skipped (not a list)
4. CI passes
5. Claude Code at runtime parses `tools: "Agent"` and grants Agent tool access
6. Worker agent spawns subagents, violating single-level nesting (H-01/P-003)

**Impact:** P-003 violation; worker agent gains orchestrator-level delegation capability; unbounded recursive token consumption; governance hierarchy bypassed.

### AP-002: Governance Confusion Attack (F-007)

**Status:** OPEN -- Medium severity, CI reliability impact
**Exploitability:** Medium -- requires commit access to governance files
**Steps:**
1. An attacker or accidental commit corrupts a legitimate T5 orchestrator's governance.yaml (introduces YAML parse error)
2. CI P-003 check fails on the orchestrator's `.md` file with a misleading error ("only T5 orchestrators may have Agent")
3. Engineers see a P-003 violation on a legitimate orchestrator with no diagnostic about the broken governance file
4. Under CI pressure, someone adds the orchestrator to an exception list or comments out the check
5. This weakens or removes P-003 enforcement for the orchestrator permanently

### AP-003: Tool Tier False Grant via governance.yaml (F-001 + F-007 combined)

**Status:** OPEN -- Medium severity, requires governance file access
**Exploitability:** Low -- requires PR authorship with both frontmatter and governance file changes visible in diff
**Steps:**
1. PR modifies worker agent `.md` frontmatter: adds `Agent` to `tools:` list
2. PR also modifies companion `.governance.yaml`: sets `tool_tier: T5`
3. JSON schema check on governance.yaml validates `T5` is a valid enum member
4. P-003 check reads governance, sees `"T5"`, sets `is_t5 = True`, emits no error
5. PR reviewer may not notice both changes together
6. Merged agent: worker agent with T5 designation and Agent tool access, no P-003 violation flagged

**Note:** This attack requires a governance tier promotion that would normally require C4 review per `agent-development-standards.md`. However, if the governance.yaml change is bundled with many other changes in a large PR, it may receive insufficient scrutiny.

---

## Architectural Design Review (OWASP A04)

### Trust Boundary Stress Test

**Trust boundary:** The P-003 check establishes a trust boundary between "agents that may delegate (T5)" and "agents that may not (T1-T4)." The boundary is enforced by the CI check reading `tool_tier` from a file controlled by the same engineer who writes the agent definition.

**Boundary violation scenarios:**

1. **Self-attestation without independent verification:** The governance.yaml `tool_tier` field is set by the same person who writes the agent definition. There is no out-of-band verification that a T5 designation has been reviewed and approved. The check enforces the rule "you must declare T5 to use Agent" but does not enforce "T5 must be reviewed by a second party." The trust boundary relies on PR review discipline, not technical enforcement.

2. **Schema validation gap:** The P-003 check reads governance.yaml but does NOT run the full JSON schema validation against `agent-governance-v1.schema.json`. It reads only the `tool_tier` field. A governance file that would fail schema validation (e.g., missing required `identity` field) could still pass the P-003 check if `tool_tier: T5` is present.

3. **Two-file split creates synchronization risk (AD-010 concern):** The dual-file architecture (H-34) splits enforcement data across `.md` frontmatter (what tools are listed) and `.governance.yaml` (what tier is claimed). These are separate files that can diverge. The CI check reads both but does not validate their mutual consistency beyond the single T5/non-T5 question. An agent with `tool_tier: T1` in governance but `Agent` in tools would correctly fail. An agent with `tool_tier: T5` in governance but no `Agent` in tools would pass (correctly, but the governance tier claims more than the frontmatter uses).

### Business Logic Flaw Identification

**Flaw 1: Positive-path check instead of exhaustive check.** The check asks "if delegation_tools is present, is the agent T5?" rather than "is every agent with T5 designation actually using Agent tools?" A T5 agent that does NOT have `Agent` in its tools is not checked at all. An agent could be mis-designated as T5 without using Agent, inflating the T5 set and potentially being upgraded to include Agent later without triggering review.

**Flaw 2: Missing inverse check.** There is no check that asks "does every T5 agent actually have Agent in its tools?" A T5 orchestrator that had `Agent` removed from its tools by accident would still be designated T5 in governance but would not function as an orchestrator. This is not a security flaw but a configuration correctness gap.

**Flaw 3: Consistency between delegation_tools detection and allowed names.** The `delegation_tools` set uses `("Agent", "Task")`. The `agent-development-standards.md` H-35 language says "Agent (or its backward-compatible alias Task)." This alignment is correct today. However, if Anthropic introduces a third name for the same tool in a future Claude Code version (as they renamed `Task` to `Agent` in v2.1.63), the check would silently miss the new name until manually updated. There is no version-pinned or dynamic detection mechanism.

### Insecure Default Assessment

The default behavior (governance.yaml absent = `is_t5 = False`) is correct: fail closed. The default behavior (governance.yaml present but `tool_tier` absent = `gov.get("tool_tier")` returns `None`, `None == "T5"` is `False`, `is_t5 = False`) is also correct.

The insecure default risk is in the string-type bypass (F-008): the default behavior when `tools` is a string is to skip the entire P-003 check. The default assumption that `tools` is always a list is incorrect given the schema allows strings.

---

## Risk Scoring Summary

| Finding | Severity | CVSS v3.1 (est.) | Exploitability | Impact | Status |
|---------|----------|-----------------|----------------|--------|--------|
| F-001: tool_tier type confusion | Medium | 4.4 | Low (governance file access required) | T5 false grant via type manipulation | Open -- fail-closed for most types, but no type guard |
| F-002: YAML anchor obfuscation | Low | 3.1 | Low (governance file access required) | PR review evasion for T5 grant | Open -- informational |
| F-003: --files scope escape | Medium | 5.3 | Medium (developer invocation or pre-commit) | P-003 check skipped for unlisted files | Open -- CI path not affected |
| F-004: TOCTOU race | Low | 3.1 | Low (deployment pipeline access required) | Post-validation file swap | Open -- accepted architectural risk |
| F-005: Path traversal (--files) | Low | 2.4 | Low (local developer invocation) | Information disclosure outside repo | Open -- informational |
| F-006: YAML bomb (governance file) | Low | 3.3 | Low (commit access required) | CI runner OOM / timeout | Open -- low priority |
| F-007: Silent YAML error | Medium | 4.3 | Medium (commit access) | CI confusion attack; check bypass pressure | Open -- diagnostic gap |
| F-008: String tools bypass | **High** | 6.5 | High (single-field frontmatter change) | Direct P-003 bypass; no governance file needed | **Open -- critical to fix** |

---

## L2: Strategic Implications

### Prioritized Remediation Roadmap

| Priority | Finding | Fix | Effort | Security Impact |
|----------|---------|-----|--------|----------------|
| P0 | F-008: String tools bypass | Normalize `tools` string to list before list check (5 lines; pattern already exists in `validate_skill()`) | 15 minutes | Closes direct P-003 bypass vector |
| P1 | F-007: Silent YAML error | Replace `pass` with `warnings.append()` for YAMLError and OSError | 10 minutes | Restores diagnostic visibility; prevents confusion attacks |
| P1 | F-001: Type guard on tool_tier | Add `isinstance(raw_tier, str)` check before `== "T5"` comparison | 10 minutes | Prevents type confusion false negatives; improves diagnostic clarity |
| P2 | F-003: --files warning | Print scope-limited warning when `--files` is provided | 5 minutes | Reduces misuse risk in local/pre-commit invocations |
| P3 | F-004: TOCTOU documentation | Add comment in CI job and code about TOCTOU limitation | 5 minutes | Governance documentation |
| P3 | F-002: Anchor obfuscation | Add inline comment explaining anchor use is intentionally allowed | 5 minutes | Reviewer awareness |
| Backlog | F-005: Path traversal | Add `Path.resolve()` + `is_relative_to(Path.cwd())` guard | 20 minutes | Defense in depth for local invocations |
| Backlog | F-006: YAML bomb | Add file size limit before `safe_load` | 10 minutes | DoS protection |

### Risk Scoring Methodology

Scores use CVSS v3.1 base metric approximation. Environmental modifier: internal framework, repository access required for most attack paths; reduces AV (Attack Vector) to L (Local) or N (Network) for PR-based paths. Temporal modifier: no public PoC; findings are original analysis of this codebase.

DREAD supplemental scoring for F-008 (string tools bypass):
- Damage: High (P-003 fully bypassed)
- Reproducibility: High (single YAML field change)
- Exploitability: High (no special access beyond PR authorship)
- Affected users: All agents validated by this check
- Discoverability: Medium (requires reading schema docs and code)

DREAD total: 4.2 / 5.0 -- High.

### Engagement Objective Alignment

The five scoped attack surface questions from the engagement brief, with findings:

1. **"Can an attacker craft a governance.yaml that passes the T5 check but isn't actually a T5 agent?"**
   Yes: Set `tool_tier: T5` in governance.yaml. This is the intended mechanism for T5 designation; the check enforces it correctly. However, there is no second-party review requirement enforced by the check -- the attacker only needs PR merge access. F-001 analyzed type confusion variants; none produce a technical bypass beyond standard T5 claim. The governance claim IS the mechanism.

2. **"What happens if tool_tier is a list, int, or other non-string type?"**
   Fail-closed: `gov.get("tool_tier") == "T5"` returns `False` for all non-string types. There is no security bypass. However, the failure is silent (no error or warning distinguishing "tool_tier is wrong type" from "tool_tier is not T5"). F-001, F-007 address the diagnostic gap.

3. **"Can YAML anchors/aliases be used to inject unexpected values?"**
   `yaml.safe_load()` handles anchors safely. Anchors can produce valid T5 string values via alias, but this is equivalent to writing `tool_tier: T5` directly. The risk is PR review obfuscation (anchor hides the T5 claim), not technical bypass. F-002 covers this.

4. **"Is there a TOCTOU race between validation and actual Claude Code agent loading?"**
   Yes, architecturally, but Low risk given current deployment patterns (git-based, same checkout). F-004 covers this. No practical exploitation path in the current CI/deployment model.

5. **"Could the check be skipped by using --files flag with specific files?"**
   In the standard CI path: No. The CI job uses full-scope invocation. In pre-commit or local invocations using `--files`: Yes, files not listed are not checked. F-003 covers this.

**Highest-value finding not in the original scope questions:** F-008 (string tools bypass) is the most exploitable finding. The `tools` field schema explicitly allows string type, but the P-003 check only processes list type. This is a direct, low-complexity bypass.

### Recommendations for eng-team Hardening (Integration Point 2)

| Priority | Recommendation | Finding | Story Candidate |
|----------|---------------|---------|-----------------|
| P0 | Normalize `tools` string-to-list in `validate_agent()` before P-003 check (mirror `validate_skill()` `allowed-tools` normalization at line 224) | F-008 | STORY-022 fix |
| P1 | Replace `pass` with explicit warning on governance YAML parse failure | F-007 | STORY-022 fix |
| P1 | Add `isinstance(raw_tier, str)` guard before `== "T5"` comparison | F-001 | STORY-022 fix |
| P2 | Scope-limited warning when `--files` is used | F-003 | STORY-022 or follow-on |
| P2 | Run full JSON schema validation on governance.yaml (not just raw dict lookup) | F-001 hardening | STORY-023 candidate |
| P3 | Inverse check: verify T5 agents have Agent in their tools list | Business logic gap | STORY-023 candidate |
| Backlog | File size guard before yaml.safe_load on governance.yaml | F-006 | Future |

---

*Agent: red-vuln (Vulnerability Analyst, /red-team)*
*Engagement: STORY-022 CI Validation Security Assessment*
*Constitutional Compliance: P-001 (evidence-based, all claims traced to code), P-002 (persisted to output file), P-003 (no subagents), P-020 (user authority), P-022 (no deception -- limitations and corrections disclosed)*
*Output: Level L0/L1/L2 per agent output spec*
*Date: 2026-03-29*
