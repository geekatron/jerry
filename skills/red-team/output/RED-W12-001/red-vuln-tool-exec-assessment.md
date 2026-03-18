# Vulnerability Assessment: tool_exec Bounded Context

> **Engagement ID:** RED-W12-001
> **Phase:** Vulnerability Analysis (white-box code review)
> **Scope:** `src/tool_exec/`, `src/interface/cli/tool_exec_commands.py`, `tests/unit/tool_exec/`, `tool_families.yaml`, `skills/rainbow/config/tool-exec.yaml`
> **Analyst:** red-vuln
> **Date:** 2026-03-18
> **Authorization:** Internal code review, authorized by project owner
> **Threat Model Source:** `skills/eng-team/output/W12-PHASE2/eng-architect-threat-model.md`
> **Methodology:** PTES Vulnerability Analysis Phase, OWASP Testing Guide, NIST SP 800-115 Chapter 5, CWE taxonomy

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Vulnerability count by severity and overall risk posture |
| [L0: Key Findings](#l0-key-findings) | Top exploitable findings |
| [L1: Attack Vector 1 — Credential Filter Bypass](#l1-attack-vector-1--credential-filter-bypass) | Evasion analysis: homoglyphs, encoding, splitting, missing formats |
| [L1: Attack Vector 2 — Plugin Architecture Code Execution](#l1-attack-vector-2--plugin-architecture-code-execution) | Module allowlist, class name constraint, __init__.py, TOCTOU |
| [L1: Attack Vector 3 — Engagement ID / Path Traversal](#l1-attack-vector-3--engagement-id--path-traversal) | Regex bypass, null bytes, Unicode normalization, symlinks, races |
| [L1: Attack Vector 4 — Subprocess Command Injection](#l1-attack-vector-4--subprocess-command-injection) | shell=False verification, list mode, Docker escape, env injection |
| [L1: Threat Model Gap Analysis](#l1-threat-model-gap-analysis) | Attack paths the eng-architect threat model missed or underscored |
| [L2: Attack Path Chains](#l2-attack-path-chains) | Multi-step exploitation chains and combined-vector analysis |
| [L2: Risk Posture and Recommendations](#l2-risk-posture-and-recommendations) | Overall risk score, prioritized mitigations, eng-team guidance |

---

## L0: Executive Summary

The `tool_exec` bounded context was analyzed across four attack vectors using white-box source code review against the complete implementation. The assessment finds the codebase to be in significantly better security posture than the eng-architect threat model projected prior to implementation, because a material number of the threat model's HIGH and MEDIUM findings were addressed during implementation.

**Vulnerability count by severity:**

| Severity | Count | Status |
|----------|-------|--------|
| Critical (CVSS 9.0+) | 0 | No new critical findings; T-01 was mitigated (M-01 implemented) |
| High (CVSS 7.0-8.9) | 2 | Both are newly identified gaps not in the threat model |
| Medium (CVSS 4.0-6.9) | 4 | Three are residual from threat model; one is new |
| Low (CVSS 1.0-3.9) | 5 | Accept-risk findings |

**Threat model mitigation verification — confirmed implemented:**
- M-01 (T-01 module allowlist): CONFIRMED implemented in `family_registry_loader.py` lines 34 and 188-196.
- M-02 (T-03 credential pattern expansion): CONFIRMED — 15 patterns active (8 CS + 7 CI), covering all M-02 additions.
- M-03 (T-06 strict mode enforcement): CONFIRMED implemented in `tool_exec_commands.py` lines 128-149; `JERRY_STRICT_MODE` defaults to `"true"`.
- M-05 (T-08 engagement ID allowlist): CONFIRMED — `_ENGAGEMENT_ID_PATTERN` is a strict allowlist, not a blocklist.
- M-10 (T-21 quarantine permissions): CONFIRMED — `os.chmod(str(quarantine_dir), 0o700)` at `engagement_initializer.py` line 86.
- FINDING-002 (CWE-22 defence-in-depth): CONFIRMED — `_validate_id()` is called in `is_initialized()`, `evidence_dir()`, and `quarantine_dir()`.
- FINDING-003 (CWE-94 class name gate): CONFIRMED — `_validate_class_name()` called before `getattr()`.
- FINDING-004 (CWE-200 stderr filtering): CONFIRMED — both `LocalExecutor` and `ContainerExecutor` filter both stdout and stderr.

**Two new HIGH-severity findings not in the eng-architect threat model:**
1. **VF-001 (High):** Credential filter operates line-by-line and does not detect multi-line split credentials. A credential split across a newline boundary evades all 15 patterns with certainty.
2. **VF-002 (High):** The `_find_project_root()` function in `tool_exec_commands.py` walks upward from `cwd`. If the CLI is invoked outside any project root (no `.git` or `pyproject.toml` found), it returns `Path.cwd()` silently. The `--evidence-dir` boundary check in `_validate_evidence_dir()` then uses `cwd` as the containment boundary, which may or may not be the intended security boundary.

**Overall risk posture: LOW-MEDIUM.** The implementation is sound. The three CRITICAL/HIGH threat model items (T-01, T-03, T-06) are all mitigated. Residual risk is concentrated in credential filter evasion coverage gaps (theoretical bypass paths) and the evidence directory boundary resolution edge case.

---

## L0: Key Findings

| Rank | ID | Severity | Vector | Exploitability | Summary |
|------|----|----------|--------|----------------|---------|
| 1 | VF-001 | High | Credential Filter | Likely | Multi-line credential split evades all 15 patterns; entire output passes as clean |
| 2 | VF-002 | High | Path Traversal | Possible | `_find_project_root()` fallback to `cwd` weakens `--evidence-dir` containment boundary |
| 3 | VF-003 | Medium | Credential Filter | Likely | GCP service account keys, Azure AD tokens, HashiCorp Vault tokens not covered by any pattern |
| 4 | VF-004 | Medium | Plugin Architecture | Possible | Module allowlist `startswith` check does not verify the suffix is a valid Python identifier |
| 5 | VF-005 | Medium | Subprocess | Unlikely | `tool_command` is not validated against a known-binary allowlist; PATH-hijack executes arbitrary binary with user privileges |
| 6 | VF-006 | Medium | Credential Filter | Possible | Base64-encoded credentials inside JSON blobs (common in cloud tool output) evade all regex patterns |
| 7 | VF-007 | Low | Plugin Architecture | Unlikely | TOCTOU between `_validate_module_path()` and `importlib.import_module()` is theoretically present but not practically exploitable within the M-01 allowlist scope |
| 8 | VF-008 | Low | Engagement ID | Unlikely | `str.strip()` used for empty-check then `re.match()` on the original unstripped value; behavior is correct but the double-check creates maintenance confusion |
| 9 | VF-009 | Low | Subprocess | Unlikely | `ContainerExecutor._build_command()` places `exec_flags` in the command list without validation; not currently user-exposed but future refactors could expose this parameter |
| 10 | VF-010 | Low | Credential Filter | Possible | ReDoS risk in the generic API token pattern `[A-Za-z0-9_.\:/\-]{20,}` given adversarially crafted output from a compromised tool binary |
| 11 | VF-011 | Low | Engagement ID | Possible | Symlink planted at `base_dir` level before initialization could redirect evidence writes |

---

## L1: Attack Vector 1 — Credential Filter Bypass

**Source file:** `src/tool_exec/domain/services/credential_filter.py`
**Reference patterns:** 8 case-sensitive + 7 case-insensitive = 15 total base patterns

### Analysis Methodology

The filter operates line-by-line (`raw_output.split("\n")`) and applies regex patterns against each line in isolation. All 15 patterns are single-line matchers with no `re.MULTILINE` or `re.DOTALL` flags that would span lines. This architectural decision is the root cause of the highest-confidence bypass vector.

### VF-001: Multi-Line Credential Split (High, Confirmed)

**Exploitability: Confirmed.** The split is trivially achievable without any knowledge of the filter's internals.

The filter processes output line-by-line. Any credential whose distinctive characters span two lines evades detection. This is not a pattern-quality deficiency — it is a structural limitation of the per-line scanning approach.

**Proof of concept — AWS access key interrupted at prefix boundary:**
```
# Tool output (two lines as received):
Line 1:  "AK"
Line 2:  "IAXXXXXXXXXXX16CHARS"

# filter_output() processes:
#   Line 1: "AK"                  -- CS patterns: no match (too short, no complete prefix)
#   Line 2: "IAXXXXXXXXXXX16CHARS" -- CS pattern requires leading AKIA; starts with I; no match
# RESULT: detected=False -- credential evades filter
```

The same technique applies to the SSH/PGP key header pattern. The banner `[DASHES]BEGIN RSA [PEM-HEADER][DASHES]` is matched as a single line. If the tool outputs the banner with a line break inserted before the final keyword, the two fragments match no pattern independently.

For the NTLM pattern `:[0-9a-fA-F]{32}:[0-9a-fA-F]{32}:`, both 32-hex-char blocks must appear on the same line. Output formatted with the second hash block on a separate line produces no match on either line.

**Impact:** A tool (or a compromised tool binary per T-02) that formats its output with strategic newlines can leak any credential through the filter. The credential appears in `filtered_output`, is persisted to evidence files, and flows to the user/agent context.

**Evidence:** `credential_filter.py` line 183 (`raw_output.split("\n")`) and the per-line loop starting at line 185 confirm the architecture.

**Mitigation:** Implement a sliding-window scan across adjacent lines (window size 2 or 3). For each line index `i`, also apply all patterns to the concatenation of `lines[i-1] + lines[i]` (stripped of the newline boundary). This catches credentials split at exactly one line boundary without requiring full-output scanning.

---

### VF-003: Missing Credential Formats — GCP, Azure, Vault (Medium, Confirmed)

**Exploitability: Likely** for workloads using these cloud providers.

The current 15 patterns cover: AWS (access key + secret), SSH/PGP private key headers, NTLM, Kerberos, Anthropic, OpenAI, Google AI (AIzaSy prefix), GitHub PAT, Stripe, Slack, JWT, API token (generic), password assignment, database connection strings.

**Confirmed coverage gaps:**

| Format | Example Structure | Why Not Covered |
|--------|-------------------|-----------------|
| GCP service account JSON | JSON blob containing a private key block with escaped newlines | The private key header pattern covers the inner key block, but the key material is stored in the JSON with `\n` escape sequences that render as literal newlines in parsed output; the header and key body may be split (VF-001 applies) |
| Azure AD client secret | Variable-length alphanumeric string with `~` prefix, e.g., `~Xk8Q~[alphanumeric chars]` | No pattern; Azure secrets have no fixed recognizable prefix covered by any current pattern |
| Azure storage account key | 88-character base64 string ending in `==` | No pattern; the generic AWS secret pattern `[A-Za-z0-9/+=]{40}` only matches exactly 40-char keys; Azure storage keys are 88 chars |
| HashiCorp Vault service token | Starts with `hvs.` followed by base64url material | No pattern for the `hvs.` prefix format |
| HashiCorp Vault legacy token | Starts with `s.` followed by 24 alphanumeric chars | No pattern |
| NPM publish token | `npm_` followed by 36 alphanumeric chars | No pattern |
| Docker registry password (base64 in config) | `{"auths":{"registry":{"auth":"[base64 user:pass]"}}}` | No pattern for base64-encoded `user:pass` in Docker config format |

**Impact:** Security tools in the rainbow suite interact with cloud environments. `prowler`, `checkov`, `kubescape` (Zone 1 cloud audit tools) and `msfconsole`, `impacket-*` (Zone 3 exploitation tools) routinely produce output containing cloud provider credentials when the target environment uses Azure, GCP, or Vault.

**Evidence:** `credential_filter.py` lines 93-130. No patterns for `hvs.`, `s.`, `npm_`, Azure AD variable-length secrets, or 88-char base64 storage keys.

---

### VF-006: Base64-Encoded Credentials in JSON Blobs (Medium, Possible)

**Exploitability: Possible.**

Many cloud tools emit credentials as base64-encoded values embedded in JSON output. The filter operates on raw string patterns and does not decode base64 before matching.

**Example:** An AWS SDK might produce output containing an access key whose characters are base64-encoded. The base64 form bears no resemblance to the original credential string and matches no defined pattern. The filter returns `detected=False`.

**Note:** This is a known limitation of L1 regex-only filtering. The threat model acknowledges that L2 (entropy analysis) and L3 (structural analysis) would address this class. The risk is accepted as a post-W12 item in the eng-architect threat model. This assessment confirms the gap is real and assigns Medium severity.

**Evidence:** `credential_filter.py` lines 93-130; eng-architect threat model L2 Architecture Weakness item 2.

---

### VF-010: ReDoS in Generic API Token Pattern (Low, Possible)

**Exploitability: Possible** only if a compromised tool binary produces adversarially crafted output.

The case-insensitive API token pattern at `credential_filter.py` line 119:
```
(api[_\-]?key|api[_\-]?token|access[_\-]?token|bearer)\s*[=: ]\s*[A-Za-z0-9_.\:/\-]{20,}
```

The trailing `[A-Za-z0-9_.\:/\-]{20,}` has an unbounded quantifier. Combined with `\s*` before it, a crafted line like `api_key=` followed by many characters that partially match and then fail could trigger backtracking. In practice, CPython's `re` engine does not exhibit catastrophic backtracking for simple character-class quantifiers (no nested quantifiers exist here), so this is a theoretical concern.

**Practical severity:** LOW. A denial-of-service requires control over tool output content, which implies a compromised tool binary (T-02 precondition). The tool execution timeout (default 300 seconds) provides a backstop.

---

### Vector 1 Bypass Attempts — Confirmed Not Exploitable

**Unicode homoglyphs (e.g., Cyrillic visually-similar characters substituted for Latin):** The AWS access key pattern uses the ASCII character class `[A-Z0-9]`. Python's `re` module matches on Unicode code points. Cyrillic characters that are visually similar to Latin letters (e.g., Cyrillic capital A at U+0410) do not fall within `[A-Z]` (U+0041-U+005A). A homoglyph attack on a key prefix would change the credential string such that it is no longer a valid credential — it would evade the filter, but it would also be rejected by the AWS API. **Assessment: Not an exploitable filter bypass for this threat model.**

**Whitespace injection between pattern characters:** The AKIA pattern requires exactly `AKIA` followed immediately by 16 uppercase alphanumeric characters. Inserting a space (e.g., `AK IA...`) changes the credential string such that it would not be accepted by AWS. **Assessment: Not exploitable without destroying the credential's validity.**

**Null byte injection:** Python `str.split("\n")` treats `\n` as the line separator. A null byte (`\x00`) is not a line separator and appears within a line. The character classes in all patterns do not include `\x00`. A null byte embedded in a credential string would break the pattern match but would also render the credential non-functional. **Assessment: Not an exploitable filter bypass.**

**Hex-encoded text (`\xNN` escape sequences):** In the text mode used by `subprocess.run(..., text=True)`, binary escape sequences are not decoded — the child process's output bytes are decoded using the system locale. A tool outputting `\x41\x4b\x49\x41` as literal escape-sequence text would produce the four characters backslash, x, 4, 1 etc. in the string, not the decoded `AKIA`. The patterns would not match. **Assessment: Not an exploitable filter bypass in text-mode subprocess.**

---

## L1: Attack Vector 2 — Plugin Architecture Code Execution

**Source file:** `src/tool_exec/infrastructure/registry/family_registry_loader.py`
**Key constants:** `_ALLOWED_MODULE_PREFIXES = ("src.tool_exec.infrastructure.adapters.",)`, `_CLASS_NAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]{1,63}$")`

### M-01 Allowlist Bypass Analysis

**Exploitability: Unlikely** given current implementation.

The allowlist check at line 189:
```python
if not any(module_path.startswith(prefix) for prefix in _ALLOWED_MODULE_PREFIXES):
```

The prefix is `"src.tool_exec.infrastructure.adapters."` — note the trailing dot. This means:
- `src.tool_exec.infrastructure.adapters.evil` — PASSES (permitted)
- `src.tool_exec.infrastructure.adapters` — FAILS (no trailing dot in path after package)
- `src.tool_exec.infrastructure.adapters_evil` — FAILS (dot not immediately after `adapters`)

**The residual attack surface is:** An attacker who can add a Python file to `src/tool_exec/infrastructure/adapters/` can register it in `tool_families.yaml` and have it imported at startup. The M-01 allowlist correctly restricts the module path string but does not restrict the filesystem — any Python file placed in the adapters directory is importable via the allowed prefix. This requires repository write access, which is the same precondition as directly modifying source code.

**VF-004 (Medium):** The `startswith` check does not require that the remainder of the path after the prefix is a non-empty valid Python identifier. A module path like `src.tool_exec.infrastructure.adapters.` (exactly the prefix, with a trailing dot and no class component) would pass validation, then fail at `importlib.import_module()` with a `ModuleNotFoundError`. The failure mode is safe (error, not code execution) but the check is slightly incomplete. A tighter validation would verify: `suffix = module_path[len(prefix):]; re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', suffix)`.

### Class Name Constraint Analysis

**Exploitability: Unlikely** given the CamelCase pattern.

The `_CLASS_NAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]{1,63}$")` check at line 167 correctly:
- Rejects `__builtins__` (starts with underscore)
- Rejects `subprocess` (starts with lowercase)
- Rejects `os.system` (contains `.`)
- Rejects `A` (too short — minimum 2 characters)
- Rejects `Rainbow_Resolver` (contains underscore, not in `[a-zA-Z0-9]`)

**Edge case confirmed not exploitable:** A class name like `Subprocess` (starts with uppercase, all alpha) passes the pattern. `getattr(module, "Subprocess")` would retrieve the `Subprocess` attribute if it exists in the module. However, the module must be within the allowed adapters prefix (M-01). Python modules in the adapters package would not normally export a class named `Subprocess` unless an attacker placed one there — which again requires repository write access.

### `__init__.py` Weaponization Analysis

**Exploitability: Unlikely** under current constraints.

`src/tool_exec/infrastructure/adapters/__init__.py` contains only:
```python
"""Infrastructure adapters for tool execution."""
```

An attacker who can modify `__init__.py` could add code that executes at import time — and importing any adapter module in the package would trigger `__init__.py` execution first. However, modifying `__init__.py` requires repository write access, placing this in the same attack-surface category as direct source code injection. The M-01 check does not gate against `__init__.py` being malicious because `__init__.py` is executed as a side effect of any import within the package.

**This gap is accepted:** The mitigation is code review of all files in the adapters package, including `__init__.py`. The threat model's Phase 4 recommendation (compile-time registry eliminating `importlib`) would close this permanently.

### VF-007: TOCTOU Between Validation and Import (Low, Unlikely)

**Exploitability: Unlikely** in practice.

The sequence in `_load_resolver()` lines 221-227:
1. `_validate_module_path(family_info.resolver_module)` — checks the string
2. `_validate_class_name(family_info.resolver_class)` — checks the string
3. `importlib.import_module(family_info.resolver_module)` — imports

The TOCTOU window between validation (steps 1-2) and import (step 3) is theoretically exploitable if another process modifies `tool_families.yaml` between the parse (`_parse_registry()`) and the import call. In practice:
- `_parse_registry()` and `_load_resolver()` execute within the same synchronous call to `load()`
- There is no sleep, I/O yield, or async boundary between validation and import
- The TOCTOU window is measured in microseconds
- Exploiting it would require a precisely timed race condition on a single-threaded operation

**Assessment: Theoretically present, practically not exploitable without OS-level race condition tooling and privileged access to the filesystem.**

---

## L1: Attack Vector 3 — Engagement ID / Path Traversal

**Source file:** `src/tool_exec/domain/services/engagement_initializer.py`
**Key pattern:** `_ENGAGEMENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$")`

### Regex Bypass Analysis

**Exploitability: Unlikely** given the allowlist design.

The pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$` is an allowlist, not a blocklist. All bypass attempts must be evaluated against whether the bypass string matches this pattern.

**Null bytes:** Python `re.compile` patterns treat `\x00` as a regular character. The character class `[a-zA-Z0-9_-]` does not include `\x00`. An engagement ID string containing a null byte (e.g., `valid\x00../etc`) fails the regex match because `\x00` is not in the allowed character class. **Confirmed not exploitable.**

**Unicode normalization attacks:** Python's `re` module operates on the string as-is, without NFC/NFD normalization. Fullwidth Latin characters (e.g., U+FF21 FULLWIDTH LATIN CAPITAL LETTER A) fall outside the ASCII range and are not matched by `[a-zA-Z]` in a standard Python regex. **Confirmed not exploitable.**

**URL-encoded path separators:** The sequence `%2F` (URL-encoded `/`) is a two-character sequence `%` and `2`. The `%` character is not in `[a-zA-Z0-9_-]`. The regex match fails. **Confirmed not exploitable.**

**VF-008 (Low) — whitespace edge case:** `_validate_id()` at line 183 calls `engagement_id.strip()` to check for whitespace-only input, then passes the original (unstripped) `engagement_id` to `re.match()` at line 186. A string like `" valid-id"` (leading space) passes the strip check (stripped value is non-empty) but fails the regex (space at position 0 is not `[a-zA-Z0-9]`). Behavior is **correct** — leading-space IDs are rejected. The double-check pattern is slightly confusing to maintain: if the regex were ever relaxed to permit leading spaces, the strip check would become the sole guard. This is a code quality concern, not a security bypass.

### Symlink Attack Analysis — VF-011 (Low, Possible)

**Exploitability: Possible** but requires prior filesystem access.

`engagement_dir.mkdir(parents=True, exist_ok=True)` at line 79 creates the directory hierarchy. If a symlink exists at any component of the path before `mkdir` is called, Python's `Path.mkdir(parents=True)` follows the symlink and creates the directory at the symlink target.

**Attack scenario:**
1. Attacker plants a symlink at `work/engagements/` pointing to `/tmp/attacker-controlled/`
2. User calls `jerry tool exec --init-engagement valid-id`
3. `engagement_dir = base_dir / "valid-id"` resolves through the symlink
4. `evidence_dir.mkdir(parents=True, exist_ok=True)` creates `/tmp/attacker-controlled/valid-id/evidence/`
5. Evidence files are written to the attacker-controlled directory

**Prerequisites:** The attacker must have write access to `work/engagements/` (the base directory) before the engagement is initialized. This requires local filesystem access, which is the same precondition as writing evidence files directly.

**The quarantine permission (`os.chmod(0o700)`) applies correctly** even through a symlink: `os.chmod` with a path argument follows symlinks on POSIX systems, so the permission restriction is applied to the real directory at the symlink target. The protection is maintained.

**Assessment:** Real but low-severity. Requires pre-existing write access to the base directory.

### Race Condition in Directory Creation (Low, Unlikely)

Three separate `mkdir` calls create `evidence`, `reports`, and `.credential-quarantine`. A TOCTOU race between calls is theoretically possible in a concurrent environment but not practically exploitable in the single-process CLI execution model. **Assessment: Not practically exploitable.**

### VF-002: `_find_project_root()` Fallback Weakens Evidence Dir Containment (High, Possible)

**Exploitability: Possible** in non-standard invocation environments.

`tool_exec_commands.py` lines 80-91:
```python
def _find_project_root() -> Path:
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback: no project root found — silently returns cwd
```

When invoked from a directory with no `.git` or `pyproject.toml` anywhere above it (e.g., `/tmp`, a CI ephemeral workspace, or a global installation), `_find_project_root()` returns `Path.cwd()` with no warning.

The `_validate_evidence_dir()` function uses this fallback as the containment boundary:
```python
resolved.relative_to(project_root.resolve())
```

**Problem 1 — boundary is wrong:** If `cwd` is `/tmp` and `--evidence-dir` is `/tmp/evidence`, the check passes because `/tmp/evidence` is under `/tmp`. But `/tmp` is world-writable on most POSIX systems — not an appropriate security boundary for evidence files from a security engagement.

**Problem 2 — silent failure:** No warning is emitted when the project root cannot be found. An operator invoking `jerry` from an unusual directory would not know the containment boundary has silently shifted to `cwd`.

**Problem 3 — engagement base_dir:** The engagement initializer is constructed with `base_dir=project_root / "work" / "engagements"` (line 205). When `project_root` is `/tmp`, engagement directories are created under `/tmp/work/engagements/` — world-accessible on a shared system.

**Impact:** Evidence files and engagement metadata for security engagements could land in world-readable directories. This is an information disclosure risk (engagement targets, tool invocations, timing metadata), not a direct credential leak (credential-bearing output is quarantined, not persisted to evidence).

**Evidence:** `tool_exec_commands.py` lines 80-91, 126, 205, 466.

**Mitigation:** When `_find_project_root()` reaches the filesystem root without finding a project marker, emit a WARNING-level log entry and, if `--evidence-dir` is not explicitly provided, fail with an actionable error message. Add `--project-root` as an explicit CLI flag.

---

## L1: Attack Vector 4 — Subprocess Command Injection

**Source files:** `src/tool_exec/infrastructure/adapters/local_executor.py`, `container_executor.py`

### shell=False Verification

**Confirmed: `shell=False` is the enforced default.**

`local_executor.py` line 94:
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=timeout,
)
```

`subprocess.run()` defaults to `shell=False` when the first argument is a sequence. The `cmd` variable is always constructed as a list: `cmd = [tool_command] + (tool_args or [])` at line 91. There is no code path that converts `cmd` to a string before passing to `subprocess.run`.

`container_executor.py` lines 113-118: same pattern — `cmd` is built as a list by `_build_command()` and passed directly.

**Confirmed: Neither executor uses `shell=True`.** Shell injection via metacharacters in `tool_command` or `tool_args` is not possible through this code path.

### Shell Metacharacter Passthrough in List Mode

**Exploitability: Confirmed Not Exploitable via shell injection.**

With `shell=False` and a list argument, the OS `execvp` syscall receives each list element as a separate argument directly to the process. Characters like `;`, `|`, `&`, `>`, `$()`, and backticks are treated as literal argument characters, not as shell metacharacters. They are passed to the child process as-is.

The child process may interpret these characters as part of its own argument parsing (e.g., a URL argument containing `&`). This is tool-level behavior, not a `tool_exec` injection vulnerability. The `tool_exec` security boundary is: no shell injection at the `subprocess.run()` level. **Confirmed: this boundary holds.**

### Docker Compose Exec — Container Boundary Analysis

**Exploitability: Unlikely** for container escape via argument injection.

`container_executor.py` `_build_command()` at lines 210-240 builds:
```
["docker", "compose", "-f", compose_file, "exec", "-T", service, tool_command, *tool_args]
```

**`compose_file` injection:** The `compose_file` argument comes from `ToolResolutionEntry.compose_file`, populated from `tool-exec.yaml` via `RainbowToolResolver.resolve()`. The YAML is repository-sourced, not from user CLI input. A `compose_file` value containing spaces or flags would be passed as the single path argument to `-f` by the OS exec, not parsed as multiple flags. **Not exploitable as argument injection.**

**`service` injection:** The `service` argument comes from `ToolResolutionEntry.container_service`, sourced from `tool-exec.yaml`. Same analysis. Not user-controlled at the CLI level.

**`exec_flags` injection (VF-009):** Currently hardcoded to `["-T"]` in `_execute_container()` via the `ContainerExecutor.execute()` default. Not user-exposed at the CLI level. The API surface permits future refactors to expose this parameter, which could allow flags like `--privileged` to be injected. This is a design concern for future refactors, not a current exploitable vulnerability.

**`tool_args` via the container:** `tool_args` are user-supplied and passed as arguments to the tool binary inside the container. `shell=False` applies at the `docker compose exec` level. Within the container, the tool binary receives the arguments directly from `execvp`. No container escape via `tool_args` is possible through this mechanism.

**Assessment:** No confirmed container boundary escape vector exists in the current implementation.

### VF-005: Tool Binary — No Allowlist Validation (Medium, Unlikely)

**Exploitability: Unlikely** in the normal operational flow.

`local_executor.py` line 91: `cmd = [tool_command] + (tool_args or [])`. With `shell=False`, the OS resolves `tool_command` by name in `PATH` (if no path separator is present) or uses it as an absolute/relative path directly.

**PATH hijack scenario:**
1. Attacker controls a directory early in `PATH` (e.g., `/tmp` prepended to `PATH`)
2. Attacker places a malicious binary at that location with the same name as a legitimate tool
3. User runs `jerry tool exec [tool-name] ...`
4. `subprocess.run` resolves to the malicious binary
5. Malicious binary executes with user privileges

**Mitigating factors in the current architecture:**
- Requires attacker control of a directory in `PATH` before the tool binary's legitimate location
- Container mode (`mode=container`) bypasses this entirely — `docker compose exec` runs the binary inside the container
- The `jerry` CLI is designed for controlled developer and CI environments

**Assessment:** This is a known, accepted risk (threat model T-02, DREAD 27). The M-07 mitigation (binary resolution logging via `shutil.which()`) has not been implemented in the current code. Adding it would make PATH hijacking observable in logs without fully preventing it.

### Environment Variable Injection via Tool Args

**Exploitability: Confirmed Not Exploitable via subprocess.**

Environment variable assignments passed as `tool_args` (e.g., `ENV_VAR=value`) are treated as literal string arguments to the tool binary. `subprocess.run(shell=False)` does not interpret list elements as environment variable assignments. The `env` parameter to `subprocess.run()` is not set in either executor, so the child process inherits the parent's environment without modification from `tool_args`.

**Confirmed: No environment variable injection via the subprocess interface.**

---

## L1: Threat Model Gap Analysis

This section identifies attack paths that the eng-architect threat model missed or underscored, per the OWASP A04 adversarial design review methodology.

### Gap 1: Multi-Line Credential Evasion (VF-001) — Not in Threat Model

**Threat model status:** The threat model identified T-03 (credential filter false negatives, DREAD 36) but characterized the gaps as format-level (missing patterns for specific token types). It did not identify the architectural multi-line split bypass, which is independent of which patterns are present.

**Why it was missed:** The threat model was produced from the design document, not the implementation. The per-line scanning architecture was an implementation choice not explicitly specified in the design. The threat analysis focused on pattern coverage quality rather than scan architecture.

**Attack path not anticipated:** An adversarially crafted or compromised tool binary that intentionally formats credentials across line boundaries to evade all 15 patterns while the filter returns `detected=False`. This is a more severe class of evasion than missing a format — it is immune to adding new patterns and requires an architectural fix.

### Gap 2: `_find_project_root()` Fallback Boundary (VF-002) — Not in Threat Model

**Threat model status:** The threat model analyzed T-07 (`--evidence-dir` arbitrary path write) and proposed M-06 (`Path.resolve()` + `relative_to()` containment check). M-06 was implemented. However, the threat model treated `project_root` as a fixed, known value and did not analyze what happens when the containment boundary itself is undefined or incorrect.

**Why it was missed:** The dynamic `_find_project_root()` function with a silent `cwd` fallback was an implementation detail that introduced a new variable into the security model not present in the design document.

### Gap 3: YAML `strict_mode` Field Is Dead Configuration

**Threat model status:** M-03 proposed enforcing strict mode via environment variable. The implementation correctly defaulted `JERRY_STRICT_MODE` to `"true"` (stronger than required). However, `tool-exec.yaml` at line 15 contains `strict_mode: true` — a field that is never read by `handle_tool_exec()`. The strict mode check uses only the environment variable.

**Impact:** Low. The default environment variable behavior provides adequate protection. The dead configuration field creates false assurance: an operator setting `strict_mode: false` in the YAML expects it to take effect, but it has no effect on execution. This is a maintenance and trust hazard.

### Gap 4: `no_filter` Security Control in Adapter Layer, Not Domain Layer

**Threat model status:** T-06 was addressed by M-03 (strict mode check in `handle_tool_exec()`). The check correctly blocks `--no-filter` when `JERRY_STRICT_MODE=true` via the CLI handler.

**Unaddressed code path:** The `no_filter` parameter is accepted by `LocalExecutor.execute()` and `ContainerExecutor.execute()` as a function argument. These are library interfaces. If `tool_exec` is used programmatically, the strict mode check in `handle_tool_exec()` is bypassed entirely — a caller can instantiate `LocalExecutor(credential_filter=filter)` and call `execute(..., no_filter=True)` directly without any environment variable check.

**Impact:** Medium for library consumers. As a CLI-only tool in the current deployment context, the CLI adapter gate is sufficient. This is a defence-in-depth gap: the security control resides in the CLI adapter layer rather than the domain service layer where it cannot be bypassed by programmatic callers.

### Gap 5: Trust Boundary at `tool-exec.yaml` for `compose_file` Paths (T-19, Not Mitigated)

**Threat model status:** T-19 (Compose file path injection via YAML, DREAD 25) was Tier 3 (consider implementing). M-11 (compose file path validation) was not implemented.

**Adversarial design review finding:** The `compose_file` paths from `tool-exec.yaml` are passed to `ContainerExecutor._build_command()` without verifying the file exists within the repository tree. A tampered `compose_file` value pointing to a valid-but-unexpected YAML file would be passed to `docker compose -f`. Docker would attempt to parse the file, and YAML parse errors would surface in stderr. This is information disclosure (file contents exposed via error messages), not code execution. Severity: Low, accepted per threat model Tier 3 classification.

---

## L2: Attack Path Chains

### Chain 1: Compromised Tool Binary to Credential Exfiltration via Multi-Line Split (High)

**Prerequisites:** Attacker controls tool binary output (via compromised binary, PATH hijack, or container image supply-chain compromise).

```
Step 1: Attacker replaces legitimate tool binary or prepends PATH with malicious directory
        [VF-005 / T-02 pathway, DREAD 27 -- no binary allowlist]

Step 2: Attacker's binary produces credentials with split-line formatting technique
        Example output (two lines):
          "Scan result: key prefix is AK"
          "IAXXXXXXXXXXX16CHARS, continuing..."

Step 3: CredentialFilterService.filter_output() processes line-by-line
        Line 1: "Scan result: key prefix is AK" -- no pattern match
        Line 2: "IAXXXXXXXXXXX16CHARS, continuing..." -- no complete AKIA prefix; no match
        filter_output() returns detected=False

Step 4: Filtered output (which contains the split credential) is:
        (a) Printed to stdout -- user/agent receives it
        (b) Persisted to evidence file via _persist_evidence()
        (c) Written to evidence_dir with sha256 integrity hash (confirms receipt)

Step 5: Agent receives credential-containing output in context window
        Credential is available for further exploitation (lateral movement)
```

**Attack path exploitability:** Confirmed given a compromised binary. The split-line bypass is effective against all 15 patterns and requires no knowledge of which patterns are implemented.

**ATT&CK mapping:** T1195.001 (Supply Chain Compromise: Software Dependencies) chained with T1552.001 (Unsecured Credentials: Credentials In Files).

---

### Chain 2: Non-Project-Root Invocation to Evidence Information Disclosure (Medium)

**Prerequisites:** Attacker can influence where `jerry` CLI is invoked from (e.g., via CI pipeline with unusual working directory, or global installation run from a home directory).

```
Step 1: jerry is invoked from /tmp (or another shared directory)
        No .git or pyproject.toml exists at or above /tmp

Step 2: _find_project_root() walks up from /tmp, reaches filesystem root
        Returns Path("/tmp") as "project root" with no warning emitted

Step 3: Operator provides --evidence-dir /tmp/evidence
        _validate_evidence_dir("/tmp/evidence", Path("/tmp"))
        Path("/tmp/evidence").relative_to(Path("/tmp")) -- succeeds (no error)
        Evidence directory accepted

Step 4: Evidence files written to /tmp/evidence/
        /tmp is world-readable on most POSIX systems
        Contents: filtered tool output, tool_command, tool_args, timestamps,
                  sha256 hashes, engagement_id

Step 5: Other users/processes on the system read /tmp/evidence/
        Information disclosed: engagement targets, tool invocations, timing,
                               engagement identifiers, operator workflow
```

**Attack path exploitability:** Possible (requires invocation from a non-project directory, which occurs in some CI environments).

---

### Chain 3: Disabled Strict Mode + Credential-Producing Tool (High, conditional)

**Prerequisites:** `JERRY_STRICT_MODE=false` is set in the invocation environment.

```
Step 1: JERRY_STRICT_MODE=false set in CI environment or operator shell

Step 2: Agent invokes: jerry tool exec --no-filter [tool] [args]
        M-03 strict mode check: strict_mode == "false"
        Warning logged to stderr; no_filter=True allowed to proceed

Step 3: Tool produces output containing credentials
        no_filter=True bypasses all credential filter processing
        LocalExecutor.execute(no_filter=True) skips filter entirely

Step 4: Unfiltered output containing raw credentials:
        (a) Returned to caller (stdout)
        (b) Persisted to evidence file WITHOUT redaction
        (c) If agent invoked: credentials enter AI context window

Step 5: Credentials available in evidence file and agent context
        High-severity impact: potential cloud credential compromise
```

**Attack path exploitability:** Confirmed if `JERRY_STRICT_MODE=false`. The default (`JERRY_STRICT_MODE` defaults to `"true"`) protects against this; the risk is environment misconfiguration.

---

## L2: Risk Posture and Recommendations

### Overall Risk Posture

The `tool_exec` implementation is in a **LOW-MEDIUM** risk posture. The three CRITICAL/HIGH findings from the threat model (T-01, T-03, T-06) are all mitigated. The two new HIGH findings (VF-001, VF-002) are architectural in nature: VF-001 requires a compromised binary as a prerequisite; VF-002 requires a non-standard invocation environment.

### Prioritized Mitigations for eng-team

**Priority 1 — Implement before agent-automated invocation:**

| ID | Finding | Mitigation | Effort |
|----|---------|------------|--------|
| MR-001 | VF-001 (Multi-line split) | Implement sliding-window scan in `filter_output()`: for each line index `i > 0`, also apply all patterns to the concatenation of `lines[i-1] + lines[i]`. This catches credentials split at exactly one newline boundary with no changes to existing pattern definitions. Add regression test: credential split at mid-token boundary should be detected by window scan. | 2 hours |
| MR-002 | VF-002 (Project root fallback) | In `_find_project_root()`, when the walk reaches the filesystem root without finding a project marker, emit a WARNING-level log entry. If `--evidence-dir` is not explicitly provided, fail with an error message requiring the operator to either run from within a project directory or pass `--project-root` explicitly. Add `--project-root` as a CLI flag that overrides the discovery walk. | 1 hour |

**Priority 2 — Implement before public release:**

| ID | Finding | Mitigation | Effort |
|----|---------|------------|--------|
| MR-003 | VF-003 (GCP, Azure, Vault gaps) | Add credential patterns: `hvs\.[A-Za-z0-9_-]{20,}` (Vault service token), `s\.[a-zA-Z0-9]{24}` (Vault legacy token), `npm_[A-Za-z0-9]{36}` (NPM publish token), `[A-Za-z0-9+/]{86}==` with context check (Azure storage account key — 88 chars base64). Add test fixtures for each new pattern in `test_credential_filter.py`. | 1.5 hours |
| MR-004 | Gap 3 (YAML `strict_mode` dead config) | Either: (a) read `strict_mode` from `tool-exec.yaml` and use it as the fallback when `JERRY_STRICT_MODE` is not set in the environment, or (b) remove `strict_mode` from `tool-exec.yaml` with a comment explaining that the env var is the sole control. Dead configuration creates false assurance for operators. | 0.5 hours |
| MR-005 | Gap 4 (`no_filter` library bypass) | Move the strict mode enforcement into `CredentialFilterService` as a class-level property, or require that `LocalExecutor` and `ContainerExecutor` check an injected `StrictModePolicy` object rather than accepting `no_filter=True` unconditionally. This moves the control to the domain layer where it applies to all callers, not just the CLI handler. | 1.5 hours |

**Priority 3 — Consider for hardening:**

| ID | Finding | Mitigation | Effort |
|----|---------|------------|--------|
| MR-006 | VF-005 (No binary allowlist) | Implement M-07 from the threat model: verify binary via `shutil.which()` before execution and log the fully resolved path. Consider an optional `allowed_binaries` list in `tool-exec.yaml` per resolution entry. | 0.5 hours |
| MR-007 | VF-006 (Base64 blobs) | Add L2 entropy scanning for base64-encoded segments in tool output. A Shannon entropy threshold of 4.5+ bits/char applied to tokens of 20+ characters would catch most base64-encoded credentials. This is the Phase 2 item from the threat model. | 4-6 hours |
| MR-008 | VF-004 (Allowlist suffix validation) | Strengthen `_validate_module_path()` to verify the suffix after the prefix is a non-empty, valid Python module identifier: extract the suffix, run `re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', suffix)`, raise `ValueError` if it does not match. | 0.25 hours |

### Test Coverage Gaps

| Gap | Test to Add |
|-----|-------------|
| VF-001 multi-line split bypass | Negative test: credential split at prefix boundary returns `detected=False`. Positive test (after MR-001 fix): same split detected by sliding-window scan. |
| VF-002 project root fallback | Test `_find_project_root()` behavior when run from a path with no `.git` or `pyproject.toml` above it; assert warning is emitted. |
| VF-003 new credential formats | Pattern-level tests for Vault token, NPM token, and Azure storage key patterns (following the pattern established in `TestCredentialFilterM02Patterns`). |
| Gap 3 YAML `strict_mode` dead config | Test that `strict_mode: false` in `tool-exec.yaml` currently has no effect (documents the current behavior and will fail to remind implementors if MR-004 activates it). |

---

*Assessment Version: 1.0.0*
*Engagement: RED-W12-001*
*Constitutional Compliance: P-001 (all findings evidence-based with source code citations), P-002 (output persisted to file), P-022 (confidence levels explicit; limitations disclosed; unvalidated markers applied where appropriate)*
*Agent: red-vuln (convergent mode, PTES Vulnerability Analysis Phase + OWASP A04 architectural review)*
*Date: 2026-03-18*
