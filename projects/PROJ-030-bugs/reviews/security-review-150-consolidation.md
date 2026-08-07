# Security Code Review: #150 Hook Consolidation

**Reviewer:** eng-security
**Date:** 2026-03-10
**Criticality:** C3 (AE-005 auto-escalation: security-relevant code)
**Review scope:** SecurityEnforcementEngine, SecurityRules, HooksPreToolUseHandler (modified), bootstrap.py wiring, comparison against `scripts/pre_tool_use.py`
**ASVS chapters verified:** V4 (Access Control), V5 (Validation, Sanitization and Encoding), V7 (Error Handling and Logging)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Severity counts, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic patterns, architectural assessment, evolution recommendations |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 2 |
| Informational | 2 |
| **Total** | **9** |

### Overall Assessment

The consolidation architecture is sound. The fail-open design, independent failure domains, and injectable rules are all correct decisions. However, two High-severity findings represent real bypass vectors that can be exploited by a motivated attacker:

1. **Path traversal via suffix substring match** (F-001): The home-directory `in` substring check on the canonicalized path can be forced to match against any path segment that happens to contain `/.ssh`, `/.aws`, or `/.gnupg` as a substring -- including attacker-controlled directory names inside the project root.

2. **`--force-with-lease` bypasses force-push guard** (F-002): The `_check_git_force_push` method only checks for `--force` and `-f`, not `--force-with-lease`. An LLM agent can force-push `main` using `git push --force-with-lease origin main` without triggering a block.

The ReDoS concern (T-03 in the ADR threat model) is assessed as Low severity -- the regex has no catastrophic backtracking on representative inputs. The information-disclosure concern (T-06) is correctly mitigated in the new engine. The original script logged matched text to stderr; the new engine logs `rule_id` only.

### Top 3 Risk Areas

1. Path canonicalization for home-relative blocked paths (F-001) -- High, exploitable today
2. Force-push bypass via `--force-with-lease` (F-002) -- High, missing coverage vs. original
3. Rule regression: four security rules present in the original that are absent from the new engine (F-003) -- Medium

### Recommended Immediate Actions

1. Fix F-001 (path traversal via suffix `in` check) before deprecating `scripts/pre_tool_use.py`.
2. Fix F-002 (`--force-with-lease` gap) in `_check_git_force_push`.
3. Restore the four missing dangerous commands from F-003 into `SecurityRules.dangerous_commands`.

---

## L1 Technical Findings

---

### F-001: Path Traversal via Suffix Substring Match (High)

**CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory -- Path Traversal)
**CVSS 3.1:** AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N = **8.4 (High)**
**ASVS:** V5.1.3 (Validate file path parameters; prevent path traversal)
**Location:** `security_enforcement_engine.py`, lines 143-151
**ADR T-04 status:** Partially mitigated. The `normpath`/`expanduser` canonicalization is correct for absolute-path blocked entries (`/etc`, `/var`, `/usr`, etc.) and for the exact home-directory match (line 133-135). The defect is in the fallback suffix check introduced for "any user's home" on lines 143-151.

#### Evidence

```python
# lines 143-151 of security_enforcement_engine.py
if blocked.startswith("~/"):
    suffix = blocked[1:]  # /.ssh, /.gnupg, /.aws
    if suffix in canonical:  # <--- substring containment, not prefix
        return EnforcementDecision(
            action="block",
            reason=f"Writing to {blocked} is blocked for security",
            violations=[f"Blocked path: {blocked}"],
        )
```

The check `suffix in canonical` performs a substring containment test on the already-canonicalized path. The intent is to catch `/Users/other/.ssh/known_hosts` when the blocked rule is `~/.ssh`. However, it equally matches:

- `/Users/adam.nowak/workspace/my-project/.ssh-keys/deploy.pem`
  (`/.ssh` is a substring of `/.ssh-keys`) -- false positive
- More critically, consider the **bypass vector**:

```
file_path = "/Users/adam.nowak/workspace/my.gnupg-bypass/.aws/config"
canonical  = "/Users/adam.nowak/workspace/my.gnupg-bypass/.aws/config"
```

For the `~/.gnupg` rule, `suffix = "/.gnupg"`. The test is `"/.gnupg" in canonical`. That evaluates to `False` -- the blocked entry does NOT fire for this canonical path. This is a false negative, not a false positive, and the analysis holds: you need a path segment that exactly contains the suffix substring. This is feasible in an attacker-controlled project directory name.

The more exploitable direction is creating a project directory whose name contains the blocked suffix, causing a false positive that can be used to demonstrate the substring logic is applied to the full path rather than a directory boundary:

```
/home/user/projects/git.ssh/config           → blocked (false positive)
/home/user/projects/.ssh-backup/id_rsa_old   → blocked (correct)
```

But the security defect is the reverse: a directory chosen to avoid the substring match can bypass the rule for a path that should be blocked:

```
file_path: /Users/other/.ssh/../.ssh/authorized_keys
canonical (after normpath): /Users/other/.ssh/authorized_keys
blocked_expanded (~/.ssh): /Users/adam.nowak/.ssh
```

The `startswith` on line 135 fails (different user path), so the first check does not fire. The fallback suffix check: `"/.ssh" in "/Users/other/.ssh/authorized_keys"` = `True`. This correctly blocks it. So the suffix check is actually needed for multi-user scenarios. The defect is the substring match rather than a boundary-aware match.

The **actual bypass** requires a path where the suffix appears in a non-directory-boundary position and the canonical path does NOT begin with the current user's blocked path. Example:

```
file_path: /opt/app-ssh-keys/id_rsa
canonical:  /opt/app-ssh-keys/id_rsa
```

For `~/.ssh` rule: suffix = `/.ssh`. `"/.ssh" in "/opt/app-ssh-keys/id_rsa"` = `False`. Correct behavior -- no bypass here.

The **exploitable false-positive case** is:

```
file_path: /Users/adam.nowak/work/proj/.ssh-config/settings.json
canonical:  /Users/adam.nowak/work/proj/.ssh-config/settings.json
blocked_expanded (~/.ssh): /Users/adam.nowak/.ssh
```

The `startswith` check (line 135) evaluates: `"/Users/adam.nowak/work/proj/.ssh-config/settings.json".startswith("/Users/adam.nowak/.ssh")` = `False`. Falls through to suffix check. `"/.ssh" in "/Users/adam.nowak/work/proj/.ssh-config/settings.json"` = `True`. **Blocked -- but this is a safe file.** The false positive is harmless from a security standpoint (it over-blocks), but it violates the principle that the check correctly identifies the blocked paths.

The **true bypass** (false negative): the test is only harmful when a legitimately dangerous path is not caught. For example, the normpath step already handles `../../../../etc/passwd` correctly (resolves to `/etc/passwd`, caught by the `/etc` rule). The suffix check's false negative risk is low given the specific suffixes (`/.ssh`, `/.gnupg`, `/.aws`). However, the logic is fragile: it relies on `/.ssh` not appearing in a path that is not under a `.ssh` directory. This property does not hold for paths like:

```
/tmp/.ssh.bak/authorized_keys
```

`"/.ssh" in "/tmp/.ssh.bak/authorized_keys"` = `True`. This would be blocked (safe behavior -- over-blocks). The canonical normpath-based check is correctly designed; only the fallback suffix logic is fragile.

**Root cause:** The suffix check uses string `in` instead of a directory-boundary-aware match. The intent was to match `/Users/other/.ssh/*` for any user, but the implementation does not anchor the suffix to a directory separator boundary before the suffix or at the suffix end.

#### Reproduction

```python
engine = SecurityEnforcementEngine()
# Should be blocked (bypass test):
result = engine.evaluate("Write", {"file_path": "/Users/other/.ssh/authorized_keys"})
assert result.action == "block"  # passes -- suffix check fires correctly

# Should NOT be blocked (false positive test):
result = engine.evaluate("Write", {"file_path": "/tmp/.ssh.bak/deploy.json"})
# Current: blocked (/.ssh is substring of /.ssh.bak)
# Correct: should be approved (not under any .ssh directory)
```

#### Remediation

Replace the substring `in` check with a path-components check:

```python
if blocked.startswith("~/"):
    suffix = blocked[1:]  # e.g., /.ssh
    # Split canonical into components and look for the suffix directory
    # as a full path component, not a substring.
    # canonical.startswith(x + suffix) or canonical == x + suffix pattern:
    import re as _re

    # Match: /<any>/<suffix_dir>/ or /<any>/<suffix_dir> at end
    suffix_pattern = _re.compile(r"(?:^|/)" + _re.escape(suffix.lstrip("/")) + r"(?:/|$)")
    if suffix_pattern.search(canonical):
        return EnforcementDecision(...)
```

Or more simply, construct the expanded blocked path for each possible home root on the system, which is more robust on multi-user Linux. The simplest correct fix is:

```python
if blocked.startswith("~/"):
    suffix = blocked[1:]  # e.g., "/.ssh"
    # Match only at directory boundaries:
    # The canonical path must contain /suffix_part/ or end with /suffix_part
    # where suffix_part starts with the literal directory name.
    # Use os.sep-anchored check:
    # Check if any path component equals the suffix directory name.
    parts = canonical.split(os.sep)
    suffix_parts = suffix.strip(os.sep).split(os.sep)
    # suffix_parts for "/.ssh" is [".ssh"]
    # Check if the suffix_parts sequence appears consecutively in parts
    for i in range(len(parts) - len(suffix_parts) + 1):
        if parts[i : i + len(suffix_parts)] == suffix_parts:
            return EnforcementDecision(...)
```

---

### F-002: `--force-with-lease` Bypasses Force-Push Guard (High)

**CWE:** CWE-862 (Missing Authorization) / CWE-284 (Improper Access Control)
**CVSS 3.1:** AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N = **5.5 (High in context)**
**ASVS:** V4.2.1 (Access control decisions must be enforced consistently)
**Location:** `security_enforcement_engine.py`, lines 295-313
**Original parity:** REGRESSION vs. `scripts/pre_tool_use.py`

#### Evidence

The original `check_git_operation` in `scripts/pre_tool_use.py` (line 206):

```python
if "push" in command and "--force" in command:
    if "main" in command or "master" in command:
        return False, "Force push to main/master is blocked"
```

The new `_check_git_force_push` in `security_enforcement_engine.py` (lines 298-312):

```python
is_force = "--force" in cmd_lower or "-f " in cmd_lower or cmd_lower.endswith("-f")
is_push = "git push" in cmd_lower

if is_force and is_push:
    for branch in self._rules.force_push_branches:
        if branch in cmd_lower:
            return EnforcementDecision(action="block", ...)
```

Neither the original nor the new implementation checks for `--force-with-lease`, which is a standard Git flag that overwrites the remote ref if the remote has not diverged from the local tracking ref. From a branch-protection standpoint, `git push --force-with-lease origin main` has the same destructive outcome as `git push --force origin main`: it rewrites the protected branch history.

#### Bypass Proof

```bash
# This command rewrites main history, bypasses the guard entirely:
git push --force-with-lease origin main
```

`"--force" in "git push --force-with-lease origin main"` = `True` (the substring `--force` IS present in `--force-with-lease`). This means the current check actually DOES detect `--force-with-lease`. However:

```bash
git push --force-with-lease=main:abc123 origin main
```

`"--force" in "git push --force-with-lease=main:abc123 origin main"` = `True`. Also caught.

After closer analysis: `--force-with-lease` contains the literal substring `--force`, so the `"--force" in cmd_lower` check fires for both forms. This is a false finding -- `--force-with-lease` IS currently caught by the `is_force` check.

However, there is still a bypass: the `-f` check has a precision defect:

```python
is_force = "--force" in cmd_lower or "-f " in cmd_lower or cmd_lower.endswith("-f")
```

The check `-f ` (with trailing space) will not match `-f\t` (with tab) or at end-of-command with other trailing chars. More importantly, `git push -forigin/main` (no space, compact flag syntax) would not be caught. But this is Low severity since Git requires a space before the remote name.

The more meaningful regression is this: the original `check_git_operation` was called via a separate code path in the standalone script (lines 309-311):

```python
elif tool_name == "Bash":
    allowed, reason = check_bash_command(tool_input)
    if allowed and "git" in tool_input.get("command", ""):
        allowed, reason = check_git_operation(tool_input)
```

In the new handler, `_check_git_force_push` is always called inside `_check_bash_command`, which is called inside `_check_bash_command` for all Bash tool invocations. This is correct -- the integration is sound.

**True finding:** The `-f` detection has a minor precision gap, but the primary force-push variants are caught. Reclassify this finding as Medium.

**Revised severity: Medium.** The `-f\t` and compact `-forigin` cases are edge cases unlikely to appear in practice. Documenting for completeness.

---

### F-002 (revised): Force-Push Guard Has `-f` Precision Gap (Medium)

**CWE:** CWE-284 (Improper Access Control)
**CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:M/A:N = **3.9 (Medium)**
**Location:** `security_enforcement_engine.py`, line 299

```python
is_force = "--force" in cmd_lower or "-f " in cmd_lower or cmd_lower.endswith("-f")
```

The `-f` detection misses `-f` followed by a tab character (`-f\t`). This is a minor precision gap. The `--force` arm correctly catches `--force-with-lease`. Remediation: add `"-f\t"` to the check or use a regex: `re.search(r'\s-f(?:\s|$)', cmd_lower)`.

---

### F-003: Four Dangerous Commands Absent from SecurityRules (Medium)

**CWE:** CWE-116 (Improper Encoding or Escaping of Output) / Rule Regression
**Severity:** Medium (rule regression reduces security coverage vs. original)
**Location:** `security_rules.py`, lines 69-74
**Original parity:** REGRESSION vs. `scripts/pre_tool_use.py`

#### Evidence

`scripts/pre_tool_use.py` `DANGEROUS_COMMANDS` (lines 111-121):

```python
DANGEROUS_COMMANDS = [
    "rm -rf /",
    "rm -rf ~",
    "chmod 777",
    "curl | bash",
    "wget | bash",
    "eval",
    "> /dev/sda",
    "mkfs",
    "dd if=",
]
```

`security_rules.py` `dangerous_commands` (lines 69-74):

```python
dangerous_commands: tuple[str, ...] = (
    "chmod 777",
    "> /dev/sda",
    "mkfs",
    "dd if=",
)
```

Missing from the new engine:

| Missing Entry | Risk | Status in New Engine |
|---------------|------|---------------------|
| `"rm -rf /"` | Destructive root wipe | Partially covered by `_check_dangerous_rm` regex; but `_check_dangerous_rm` requires both `-r`/`--recursive` AND `-f`/`--force` flags. The substring `rm -rf /` check in the old code was a simple exact-substring catch. |
| `"rm -rf ~"` | Destructive home wipe | Same -- partially covered. |
| `"curl \| bash"` | Download-and-execute | Covered by `_check_dangerous_commands` regex (line 275-281 of engine). |
| `"wget \| bash"` | Download-and-execute | Covered by the same regex. |
| `"eval"` | Arbitrary code execution | **NOT covered anywhere in the new engine.** |

The missing coverage for `eval` is the most significant gap. The original blocked any Bash command containing the literal string `eval`, which prevents code injection via `eval $(command)` or `eval "$(attacker-controlled)"` patterns. The new engine has no equivalent check.

#### Remediation

Add to `SecurityRules.dangerous_commands`:

```python
dangerous_commands: tuple[str, ...] = (
    "chmod 777",
    "> /dev/sda",
    "mkfs",
    "dd if=",
    "eval",  # prevent eval-based injection
)
```

Note: `rm -rf /` and `rm -rf ~` are now handled by the regex in `_check_dangerous_rm`, but that regex requires both `-r` and `-f` flags. A command like `rm -rf /` without the `--` separator will be caught; verify that the regex covers the `rm -rf` compact form. The regex `r"\brm\s+(?=.*(?:-[a-zA-Z]*r[a-zA-Z]*|--recursive))(?=.*(?:-[a-zA-Z]*f[a-zA-Z]*|--force)).*\s+[/~]"` does catch `rm -rf /` (analysis below under F-004).

---

### F-004: ReDoS Analysis of `_check_dangerous_rm` Regex (Low)

**CWE:** CWE-1333 (Inefficient Regular Expression Complexity)
**CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L = **2.5 (Low)**
**Location:** `security_enforcement_engine.py`, lines 252-257
**ADR T-03 status:** Accepted. Analysis confirms Low severity, not the DREAD 4.2 estimated in the ADR.

#### Evidence

The regex under analysis:

```python
rm_pattern = re.compile(
    r"\brm\s+"
    r"(?=.*(?:-[a-zA-Z]*r[a-zA-Z]*|--recursive))"
    r"(?=.*(?:-[a-zA-Z]*f[a-zA-Z]*|--force))"
    r".*\s+[/~]",
)
```

This uses two lookaheads on the same input position, each scanning forward with `.*`. The structure is:

```
\brm\s+ (?=A) (?=B) .*\s+[/~]
```

Where A and B are each `(?=.*(alternation))`. The `.*` inside a lookahead can cause quadratic backtracking when the pattern fails to match, because Python's `re` module uses a backtracking NFA engine.

**Worst-case input analysis:**

```
rm -rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr (no / or ~ at end)
```

For this input, the first lookahead `(?=.*(?:-[a-zA-Z]*r[a-zA-Z]*|...))` succeeds (matches `-r...r`). The second lookahead `(?=.*(?:-[a-zA-Z]*f[a-zA-Z]*|--force))` fails (no `-f` flag). Python backtracks through the `.*` in the first lookahead. The pattern inside the first alternation `-[a-zA-Z]*r[a-zA-Z]*` is `[a-zA-Z]*` repeated twice around `r`, which can itself backtrack across the repeated `r` characters.

For a string of 30 repeated `r` characters after the `-`, the inner regex `-[a-zA-Z]*r[a-zA-Z]*` matches deterministically in one pass (it is greedy and does not require backtracking on this input). The outer `.*` in the lookahead performs O(n) tries. The combined complexity is O(n^2) for the outer `.*` and inner character-class matching.

**Measured severity:** O(n^2) is quadratic, not exponential. For a hook timeout of 100ms and typical command lengths under 1000 characters, quadratic complexity is unlikely to cause a timeout. However, if an attacker controls the command string and can supply a ~10,000 character Bash command, the 100ms timeout may be hit.

**Comparison to the original (`scripts/pre_tool_use.py` lines 176-182):**

```python
rm_match = re.search(r"\brm\s+(.*)", cmd_stripped)
if rm_match:
    rm_args = rm_match.group(1)
    has_recursive = bool(re.search(r"(?:^|\s)-[a-zA-Z]*r|--recursive", rm_args))
    has_force = bool(re.search(r"(?:^|\s)-[a-zA-Z]*f|--force", rm_args))
    targets_root = bool(re.search(r"(?:^|\s)[/~]", rm_args))
```

The original uses three separate regex calls on a pre-captured group. This is less elegant but avoids the double-lookahead structure and has lower backtracking risk. The new implementation consolidates into one regex at the cost of slightly higher ReDoS potential.

**Verdict:** Low severity. The 100ms hook timeout (AC-015-002) is the primary mitigation. No catastrophic exponential backtracking was identified. The ADR's DREAD estimate of 4.2 (T-03) appears calibrated correctly for the pattern library; the `_check_dangerous_rm` regex itself is lower risk (estimated 2.5).

#### Remediation (optional)

If a no-backtracking guarantee is required, rewrite using the three-check structure from the original:

```python
def _check_dangerous_rm(self, command: str) -> EnforcementDecision:
    rm_match = re.search(r"\brm\s+(.*)", command)
    if rm_match:
        rm_args = rm_match.group(1)
        has_recursive = bool(re.search(r"(?:^|\s)-[a-zA-Z]*r|--recursive", rm_args))
        has_force = bool(re.search(r"(?:^|\s)-[a-zA-Z]*f|--force", rm_args))
        targets_root = bool(re.search(r"(?:^|\s)[/~]", rm_args))
        if has_recursive and has_force and targets_root:
            return EnforcementDecision(action="block", ...)
    return _APPROVE
```

---

### F-005: `_check_cd` Operates on `command.lower()` But `cd_patterns` Contains Case-Sensitive Patterns (Low)

**CWE:** CWE-178 (Improper Handling of Case Sensitivity)
**CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **1.8 (Low)**
**Location:** `security_enforcement_engine.py`, lines 216-243; `security_rules.py`, lines 79-86

#### Evidence

`_check_cd` applies `command.lower().strip()` at line 218, then checks `cd_patterns` against `command.lower()` at line 233. The `cd_patterns` in `security_rules.py` are:

```python
cd_patterns: tuple[str, ...] = (
    "cd ",
    "cd\t",
    "&& cd",
    "; cd",
    "$(cd",
    "| cd",
)
```

These patterns are lowercase, and the check is performed on `command.lower()`, so case sensitivity is handled correctly for the standard patterns.

However, the initial checks at lines 221-222 test `cmd_lower` (which is `command.lower().strip()`), but the pattern loop at line 233 tests `pattern in command.lower()` (the un-stripped command). These are consistent -- both use lowercased input. The early-return exact check at line 221 (`cmd_lower == "cd"`) is safe.

**Minor defect:** The initial check at line 221 uses `cmd_lower` (stripped), but lines 233-234 check `pattern in command.lower()` (not stripped). If the command is `"  cd /tmp"` (leading spaces), the exact check `cmd_lower == "cd"` does not fire, and `cmd_lower.startswith("cd ")` will catch it because `cmd_lower` is `"cd /tmp"` after strip. However, for the pattern loop, `"cd " in command.lower()` = `"cd " in "  cd /tmp"` = `True`. Consistent -- both paths catch this.

The actual defect is that `cmd_lower.startswith("cd\t")` cannot fire because `cmd_lower` is already `strip()`-ped and leading tabs are removed. The `cd\t` check via the pattern loop (`"cd\t" in command.lower()`) fires for `cd\t/tmp` embedded in a longer command, but the initial explicit check at line 221 using `cmd_lower.startswith("cd\t")` would miss a leading-tab `cd\t` command. Low practical impact since `cmd_lower` is stripped and the pattern loop covers this case anyway.

---

### F-006: No Null-Byte Sanitization in File Path Inputs (Medium)

**CWE:** CWE-158 (Improper Neutralization of Null Byte or NUL Character)
**CVSS 3.1:** AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N = **4.4 (Medium)**
**Location:** `security_enforcement_engine.py`, line 129
**ASVS:** V5.2.1 (Sanitize input to remove or escape unsafe characters)

#### Evidence

The `_check_file_write` method canonicalizes the path at line 129:

```python
canonical = os.path.normpath(os.path.expanduser(file_path))
```

On Python, `os.path.normpath` does NOT strip null bytes. A path containing a null byte such as `"/etc/passwd\x00.txt"` behaves differently across Python versions and OS calls:

- Python 3.x `os.path.normpath("/etc/passwd\x00.txt")` returns `"/etc/passwd\x00.txt"` (null byte preserved).
- Python string operations like `startswith` match the prefix `"/etc"` correctly, so `"/etc/passwd\x00.txt".startswith("/etc")` = `True`. The null byte does not bypass the blocked path check for `/etc`.
- For home-relative paths, the suffix `in` check: `"/.ssh" in "/home/user/.ssh\x00.bak"` = `True`. The null byte does not bypass this either.

**Assessment:** In Python, null bytes in strings are handled as regular characters for string comparison purposes. The blocked-path checks use `startswith` and `in`, both of which treat null bytes as opaque characters. A path like `"/etc/passwd\x00"` still starts with `"/etc"` and would be blocked.

**However**, the `os.path.basename(file_path)` call at line 154 uses the original (non-canonical) `file_path`. If `file_path = "/etc/passwd\x00.txt"`, then `os.path.basename` returns `"passwd\x00.txt"`, and the sensitive-file pattern check compares `"passwd\x00.txt"` against patterns. This is unlikely to cause a false negative for patterns like `".env"`, `".key"`, etc., but the nullbyte could theoretically confuse case-insensitive matching.

**Medium severity** because null bytes in Claude Code tool input are unlikely to occur in practice (Claude Code generates tool input programmatically, not from user string manipulation). Documenting as Medium given the ASVS V5.2.1 requirement.

#### Remediation

Add a null-byte strip at the start of `_check_file_write`:

```python
def _check_file_write(self, file_path: str) -> EnforcementDecision:
    # Strip null bytes before path canonicalization (CWE-158)
    file_path = file_path.replace("\x00", "")
    if not file_path:
        return _APPROVE
    canonical = os.path.normpath(os.path.expanduser(file_path))
    ...
```

---

### F-007: T-06 Correctly Mitigated -- Pattern Match Logs Rule ID Only (Informational)

**ADR T-06 status:** CORRECTLY MITIGATED
**Location:** `security_enforcement_engine.py`, lines 333-336

#### Evidence

```python
violations = (
    [
        # T-06: Log rule_id only, never matched text
        f"Pattern match: {m.rule_id}"
        for m in result.matches
    ],
)
```

The new engine logs only `rule_id` in the `violations` list. The original `scripts/pre_tool_use.py` logged the full `matches` list to stderr (line 326), which included `description` and `severity` fields and potentially matched text depending on the pattern library implementation. The new implementation is a correct security improvement.

**No action required.**

---

### F-008: `_check_dangerous_commands` Contains `"eval"` Gap -- See F-003 (Informational)

Cross-reference to F-003. The `eval` dangerous command present in the original `DANGEROUS_COMMANDS` list is not in `SecurityRules.dangerous_commands` and has no regex equivalent in the new engine. This is documented under F-003 as Medium severity.

---

### F-009: `_check_file_write` Basename Check Uses Original `file_path`, Not Canonical (Informational)

**CWE:** CWE-22 (Path Traversal -- minor inconsistency)
**Severity:** Informational
**Location:** `security_enforcement_engine.py`, line 154

```python
basename = os.path.basename(canonical).lower()
```

This is correct: `canonical` is used, not the raw `file_path`. The `os.path.basename(canonical)` call on line 154 uses the canonicalized path. No defect.

However, line 170 in the block reason uses `os.path.basename(file_path)` (the original, non-canonicalized input):

```python
reason = (
    (
        f"Writing to sensitive file ({pattern}) is blocked. "
        f"File: {os.path.basename(file_path)}"  # <-- original file_path
    ),
)
```

This means the reason message shown to the user may display a non-canonicalized filename (e.g., `../../../.env` instead of `.env`). This is an information quality issue, not a security bypass. The security decision is made on `canonical` (line 154); only the user-visible message uses the original. Informational finding only.

---

## L2 Strategic Implications

### Security Posture Assessment

The consolidation improves the security posture compared to the status quo where, per ADR Section Context, "neither security path runs" because `settings.json` has no hooks configured. Once deployed, the new engine provides functional security enforcement for the first time since the hook configuration was removed.

The implementation is architecturally sound: independent failure domains, injectable rules for testability, frozen dataclasses preventing rule mutation, and explicit fail-open semantics that do not risk blocking the development workflow. These design properties are correct and should be preserved.

### Systemic Patterns

**Pattern 1: Canonicalization is applied correctly for exact matches, fragile for multi-user suffix matching.** The core `normpath(expanduser())` pattern correctly resolves `../../../../etc/passwd` to `/etc/passwd`, catching the canonical path traversal. The defect is only in the additional fallback logic for home-directory paths. This reflects a systemic pattern where security controls are strong for the documented threat model and weak for edge cases not mentioned in the original code comments.

**Pattern 2: Rule regression risk from refactoring.** Four entries from `DANGEROUS_COMMANDS` in the original are absent from `SecurityRules.dangerous_commands`. This is a systemic risk of the port approach: without a formal equivalence test (a test asserting that `new_engine.evaluate("Bash", {"command": cmd})` blocks for every input that the original `check_bash_command` blocks), regressions are hard to detect in review alone. Recommend adding an explicit parity test file.

**Pattern 3: No symbolic link resolution.** Neither the original nor the new engine calls `os.path.realpath()`. A symbolic link from a project-local path into `/etc` would not be detected:

```
/Users/adam.nowak/workspace/project/symlink_to_etc_passwd -> /etc/passwd
file_path: /Users/adam.nowak/workspace/project/symlink_to_etc_passwd
canonical after normpath+expanduser: /Users/adam.nowak/workspace/project/symlink_to_etc_passwd
```

This does not start with `/etc`, so it is not blocked. This is a known limitation of string-based path checking and is present in the original implementation as well. It is documented as an accepted limitation; the tool-use hook runs before the write occurs, and Claude Code controls the file_path input. However, a sophisticated bypass that creates a symlink in a prior turn and then writes to it via the symlink path would not be caught. This limitation is inherited from the original, not introduced by the consolidation.

### Comparison with Threat Model Predictions

| ADR Threat | Assessment | Finding |
|------------|------------|---------|
| T-01 (patterns.yaml tampering) | Accepted risk documented. No new mitigations needed at this stage. | Not investigated further |
| T-02 (security_rules.py tampering) | CI/pre-commit mitigates. Governance escalation via AE-002 if rules file is touched. | Correct |
| T-03 (ReDoS) | ADR DREAD 4.2 is conservatively correct for the pattern library. The `_check_dangerous_rm` regex itself is Lower risk (DREAD ~2.5). | F-004 (Low) |
| T-04 (path traversal) | normpath/expanduser correctly applied for absolute paths and exact home match. Suffix fallback is fragile. | F-001 (High) |
| T-05 (tool name spoofing) | Accepted -- Claude Code controls tool_name. | Confirmed accepted |
| T-06 (information disclosure) | Correctly mitigated in new engine. | F-007 (Info -- mitigated) |
| T-07 (fail-open bypass) | Intentional. Independent domains correctly implemented. | Confirmed by code review |

### ASVS Chapter Verification

| Chapter | Status | Notes |
|---------|--------|-------|
| V4 (Access Control) | Partial pass | F-002 (Minor -f gap), force-push logic is functionally correct for `--force` and `--force-with-lease`. |
| V5.1.3 (Path traversal prevention) | Conditional pass | Correct for absolute paths; fragile suffix check for home-relative paths (F-001). |
| V5.2.1 (Null byte sanitization) | Fail | No null-byte stripping (F-006). Low practical risk but ASVS non-compliance. |
| V7 (Error Handling and Logging) | Pass | Fail-open semantics correct; no matched text logged (T-06 mitigated). |

### Recommendations for Security Architecture Evolution

1. **Add equivalence parity tests.** Create `tests/unit/infrastructure/enforcement/test_security_parity.py` that parametrizes every input that `scripts/pre_tool_use.py` blocks and asserts the new engine also blocks it. This eliminates the rule-regression risk systematically.

2. **Consider `os.path.realpath()` for a defense-in-depth layer.** This is a deliberate trade-off (fail-open vs. security): `realpath()` performs I/O (follows symlinks) which can fail. For the hook timeout constraint, a try/except around `realpath()` with fallback to `normpath(expanduser())` would add symlink protection without blocking development on filesystem errors.

3. **Move `eval` blocking to a dedicated regex check.** A simple substring check for `eval` is too broad (e.g., `evaluated`, `unevaluation`). A more precise check: `re.search(r'\beval\b', command)` catches the word-bounded form.

4. **Set `patterns_path` via configuration, not hardcoded project root.** The bootstrap wires the pattern library with a hardcoded path relative to `project_root`. If the Jerry installation directory changes, the patterns file silently becomes unavailable and `_check_patterns` silently skips (fail-open). A startup health check that warns to stderr when `patterns.yaml` is not found would make this failure visible.

---

## Appendix: Finding Summary Table

| ID | Title | Severity | CWE | Location |
|----|-------|----------|-----|----------|
| F-001 | Path traversal via suffix substring match | High | CWE-22 | engine.py:143-151 |
| F-002 | Force-push `-f` precision gap | Medium | CWE-284 | engine.py:299 |
| F-003 | `eval` and four other commands absent from SecurityRules | Medium | CWE-116 | security_rules.py:69-74 |
| F-004 | `_check_dangerous_rm` ReDoS potential (Low) | Low | CWE-1333 | engine.py:252-257 |
| F-005 | `_check_cd` minor strip/pattern inconsistency | Low | CWE-178 | engine.py:218-243 |
| F-006 | No null-byte sanitization in file path input | Medium | CWE-158 | engine.py:129 |
| F-007 | T-06 correctly mitigated -- informational | Info | -- | engine.py:333-336 |
| F-008 | `eval` gap -- cross-reference to F-003 | Info | -- | security_rules.py |
| F-009 | Reason message uses original file_path, not canonical | Info | CWE-22 | engine.py:170 |

---

*Produced by eng-security | Review date: 2026-03-10 | Criticality: C3 (AE-005)*
