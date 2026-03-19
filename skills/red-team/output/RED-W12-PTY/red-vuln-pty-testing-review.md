# Vulnerability Analysis: Python pty.openpty() for Zone 3 E2E Testing

**Engagement ID:** RED-W12-PTY
**Analyst:** red-vuln (Vulnerability Analyst, /red-team)
**Date:** 2026-03-19
**Phase:** Vulnerability Analysis
**Scope:** Security review of Python `pty.openpty()` for Zone 3 E2E testing

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Findings overview, severity count, key recommendations |
| [L1 Technical Detail](#l1-technical-detail) | Per-question analysis grounded in actual implementation |
| [L2 Strategic Implications](#l2-strategic-implications) | Attack path analysis, design tradeoffs, hardening recommendations |

---

## L0 Executive Summary

### Findings by Severity

| Severity | Count | Key Finding |
|----------|-------|-------------|
| HIGH | 1 | PTY-TEST-001: TTY presence is a necessary but not sufficient proof of human presence |
| MEDIUM | 2 | PTY-TEST-002: PTY pattern is trivially scriptable outside test context; PTY-TEST-003: Audit trail does not distinguish test PTY from human PTY |
| LOW | 1 | PTY-TEST-004: Test env var bypass inverts the threat model if poorly scoped |
| INFO | 1 | PTY-TEST-005: Current non-interactive auto-deny is a strong and correct primary gate |

### One-Sentence Risk Posture

The PTY test approach correctly satisfies the gate's stated contract (`sys.stdin.isatty() == True`) but the gate contract is weaker than the security objective: any Python script with four lines can produce a TTY and auto-approve Zone 3 tools, meaning the gate is a deterrent against accidental automation rather than a barrier against intentional automation.

### Top Recommendations

1. Upgrade the gate to require a specific confirmation phrase tied to the tool name (e.g., `"APPROVE: impacket-GetADUsers"`). This makes automation harder because the approver must parrot back context they only have if they read the prompt.
2. Add a `source` field to the audit event (`"human"` vs. `"test_pty"` vs. unclassified) controlled by an explicit test env var. This restores audit trail fidelity without changing the gate logic.
3. Accept the PTY approach for E2E testing of the interactive approval path, subject to the scoping constraints in this report. It is the least-bad option among the alternatives.
4. Do not use a `JERRY_ZONE3_TEST_MODE=auto_approve` env var without a compensating fail-closed guard in production-path code.

---

## L1 Technical Detail

### Gate Implementation (Ground Truth)

The gate lives in `_prompt_zone3_approval()` at line 929 of
`src/interface/cli/tool_exec_commands.py`. The relevant logic:

```
auto_deny = not sys.stdin.isatty()
if auto_deny:
    # write audit event with reason="auto-deny: non-interactive stdin"
    return False

answer = input("  Approve? [yes/NO]: ").strip().lower()
approved = answer == "yes"
```

The gate has two parts:

1. **TTY presence check** (`sys.stdin.isatty()`): if stdin is not a TTY, deny immediately without prompting.
2. **Affirmative input check** (`answer == "yes"`): if stdin is a TTY, the operator must type exactly `yes` and press Enter.

The audit write is fail-closed: if the audit write fails for an approved operation, the approval is reversed (lines 1009-1021). This is a meaningful defence-in-depth control and is preserved under all scenarios below.

---

### Question 1: Does Using PTY in Tests Constitute a Security Bypass?

**Verdict: Not a bypass of the gate's stated contract. Is a bypass of the gate's intended security objective. Severity: HIGH (design limitation, not an implementation flaw).**

#### What the Gate Checks vs. What It Intends to Check

The gate checks: `sys.stdin.isatty()`. A PTY slave is a TTY device. Therefore a child process whose stdin is a PTY slave returns `True` from `isatty()`. The test satisfies the check exactly as documented.

The gate intends to ensure: a human being has reviewed and approved this Zone 3 operation. A human is not present in the PTY test. The test script provides the `y\n` bytes automatically.

These two statements are mutually consistent: the gate's stated contract (`isatty()`) is a proxy for human presence, not human presence itself. The proxy has a known gap: any process that can open a PTY master/slave pair can impersonate a human at the gate.

#### Does This Weaken P-020?

P-020 (User Authority) requires that the system does not act without human oversight on destructive operations. The current gate implements P-020 through a hardware-level heuristic: real terminals are attached to human operators, not to automated scripts.

The PTY approach weakens this heuristic in the test context only. In the test context, there is no human, but the gate passes because the physical property (TTY device) is present. This is an acceptable tradeoff for E2E testing if and only if:

- The test is clearly identified in the audit trail as a test event (currently it is not - see Question 4).
- The PTY fixture code does not leak into production paths.
- The test suite documents that this fixture should never be generalised.

**Compared to a human at a real terminal:** The difference is intent and context, not mechanism. The OS cannot distinguish "human pressed Y on a real terminal" from "Python wrote b'y\n' to a PTY master". The distinction exists only at a higher semantic level. This is a fundamental limitation of the TTY-presence check as a human-presence proof.

---

### Question 2: Can the PTY Pattern Be Abused in Production?

**Verdict: YES. Exploitation is trivial. Severity: HIGH (exploitability: easy; requires only stdlib, no privileges).**

#### Exploit Path

An attacker or a misconfigured automation system that can execute Python on the host can bypass the Zone 3 gate with the following four-line script:

```python
import os, pty, subprocess
master_fd, slave_fd = pty.openpty()
proc = subprocess.Popen(["jerry", "tool", "exec", "--mode", "container", "impacket-GetADUsers", "target"], stdin=slave_fd)
os.write(master_fd, b"yes\n")
proc.wait()
```

This script requires:
- Python stdlib only (no third-party packages).
- Ability to run on the same machine as jerry (local code execution).
- No elevated privileges.

**Preconditions for exploitation:**

| Precondition | Notes |
|--------------|-------|
| Local code execution on the jerry host | Required. If an attacker has this, they have much worse problems. |
| jerry installed and in PATH | Required. |
| A valid engagement ID initialized | Required by Zone 3 policy. Also gates the gate. |
| No out-of-band detection layer | Without a monitoring layer watching for PTY-based jerry invocations, this is silent. |

#### Is the TTY Check Sufficient?

No. The TTY check is a deterrent against accidental automation (CI scripts, AI agents that run without PTY allocation, simple `subprocess.run()` calls). It is not a barrier against intentional automation. Any attacker with local code execution who wants to bypass the gate can do so trivially.

**The more meaningful gate is the engagement requirement.** Zone 3 operations require a pre-initialized engagement. An attacker who can initialize a test engagement and run jerry with a PTY has already demonstrated a level of access where Zone 3 tool execution is a secondary concern.

#### Risk Framing

The Zone 3 gate's primary threat model is: "prevent an AI agent (including jerry itself) from autonomously executing exploitation tools without human review." For that threat, the TTY check is correct and effective: AI agents in non-interactive subprocesses do not have TTY access. The threat model does not include: "prevent a human or script with local access from executing jerry after explicitly setting up a PTY." That scenario requires local code execution, which is already a full compromise.

The PTY test pattern does not weaken the primary gate against its primary threat. It does expose a gap against a secondary threat (intentional automation with PTY). Document this gap; do not treat it as a critical finding.

---

### Question 3: Should the Test Write "yes" or Should the Gate Use a Stronger Mechanism?

**Verdict: The gate should be upgraded to require a specific confirmation phrase. Severity: MEDIUM (improvement opportunity, not a blocking defect).**

#### Current Gate Weakness

The current gate accepts a single `yes` string. This string has no context-binding: the same input approves any Zone 3 tool. An automated script that writes `yes\n` to a PTY will always pass, regardless of which tool is being approved.

#### Recommendation: Confirmation Phrase

Require the operator to type the tool name as part of the approval string:

```
Approve? Type "APPROVE: impacket-GetADUsers" to confirm:
```

The operator must type back the exact string `APPROVE: impacket-GetADUsers`. This accomplishes two things:

1. **Context-binding**: the operator must have read the prompt and understood which tool they are approving.
2. **Automation resistance**: a generic automation script cannot guess the confirmation string without parsing the prompt output first. It must implement the full read-parse-respond cycle, which raises the automation cost substantially.

**Implementation note:** The confirmation string is trivially derivable from the tool name, so it is not a secret. Its value is forcing the automation to be context-aware, not to keep the string secret.

#### Alternative: Time Delay

A mandatory time delay (e.g., 5 seconds between prompt and accepted response) makes high-throughput automated approval campaigns slower but does not stop a single targeted attack. Not recommended as a primary control.

#### Alternative: TOTP/Challenge-Response

TOTP or challenge-response provides cryptographic proof that the approver possesses a shared secret. This is disproportionate for a local interactive CLI tool and would break the operator experience. The threat model does not justify this overhead.

#### Impact on E2E Tests

If the gate is upgraded to require `"APPROVE: {tool_name}"`, the PTY test must be updated to write `f"APPROVE: {tool_name}\n"`. This is straightforward. The PTY test fixture would read:

```python
os.write(master_fd, f"APPROVE: {tool_command}\n".encode())
```

This is strictly better: the test now validates that the gate accepts the correct context-bound string and rejects a generic `yes`.

---

### Question 4: Audit Trail Implications

**Verdict: The audit trail currently does NOT distinguish test PTY from human TTY. This is a material gap. Severity: MEDIUM.**

#### Current Audit Event Structure

The `_write_approval_audit()` function (lines 1025-1146) writes a JSON event:

```json
{
  "timestamp": "...",
  "engagement_id": "...",
  "tool_command": "...",
  "zone": "Zone 3",
  "approved": true,
  "reason": "operator input"
}
```

The `reason` field is hardcoded to `"operator input"` for all TTY-path approvals. A PTY-assisted test approval produces an identical event to a human terminal approval. A post-incident reviewer cannot distinguish the two.

#### Attack Scenario Enabled by This Gap

If an attacker uses the PTY bypass to approve a Zone 3 tool, the audit trail shows `"reason": "operator input"`. The SOC analyst investigating the incident sees what appears to be a legitimate human approval. This is an audit trail integrity failure: the trail cannot be used to confirm or deny human involvement.

#### Recommendation: Add a Source Field

Add a `source` field to the audit event that records how the approval was obtained:

| Source Value | Condition |
|---|---|
| `"interactive_tty"` | Default for all TTY-path approvals |
| `"test_pty"` | When `JERRY_ZONE3_TEST_SOURCE=test_pty` is set in environment |
| `"auto_deny"` | For the non-TTY path (already recorded via `reason` field) |

The test fixture sets `env["JERRY_ZONE3_TEST_SOURCE"] = "test_pty"` when constructing the PTY subprocess. The gate reads this env var and includes it in the audit event. This env var is advisory metadata only: it does not change gate behaviour (the TTY check still applies). A production operator who does not set this env var gets the default `"interactive_tty"` label.

This approach does not create a security bypass (the gate still requires a TTY), but it restores audit trail fidelity.

---

### Question 5: Alternative Approach - JERRY_ZONE3_TEST_MODE Env Var

**Verdict: High risk if implemented naively. Acceptable if scoped correctly. Severity: LOW (conditional).**

#### The Naive Implementation Is Dangerous

```python
# DO NOT implement this:
if os.environ.get("JERRY_ZONE3_TEST_MODE") == "auto_approve":
    return True  # Bypass the entire gate
```

This creates a trivial bypass: any script that sets `JERRY_ZONE3_TEST_MODE=auto_approve` completely bypasses the Zone 3 gate. The env var becomes a backdoor. Risk:

- CI pipeline environment variable leakage: if `JERRY_ZONE3_TEST_MODE=auto_approve` is set in a CI job's env block and the job runs on a shared runner, every subsequent job on that runner inherits the bypass until the runner is recycled.
- Container env var injection: if an attacker can inject env vars into a container running jerry, they bypass Zone 3.

#### The Correct Scoped Implementation

The env var should control audit trail annotation only, not gate logic:

```python
# Safe: env var annotates but does not bypass
test_source = os.environ.get("JERRY_ZONE3_TEST_SOURCE", "")
# Gate logic unchanged: still requires TTY + "yes" input
# ...
event = {
    ...,
    "reason": "operator input",
    "source": test_source if test_source else "interactive_tty",
}
```

Or, if you want the env var to control behaviour at all, the safe pattern is fail-closed:

```python
# Safe: env var only activates in an explicitly non-production context
# Requires both the env var AND a build-time flag or a test marker
# Never bypass the TTY check; only affect prompting UI
```

**Security tradeoff comparison:**

| Approach | Automation Resistance | Audit Fidelity | Test Simplicity | Production Risk |
|---|---|---|---|---|
| PTY + "yes" (current proposed) | Low | Low | Medium | Low |
| PTY + "APPROVE: tool_name" | Medium | Low | Medium | Low |
| PTY + "APPROVE: tool_name" + JERRY_ZONE3_TEST_SOURCE annotation | Medium | High | Medium | Low |
| JERRY_ZONE3_TEST_MODE=auto_approve (naive bypass) | None | None | High | CRITICAL |
| JERRY_ZONE3_TEST_MODE=auto_approve (fail-closed scope guard) | None (in test) | Medium | High | Low-Medium |

The PTY approach with a confirmation phrase and audit annotation is the recommended path.

---

## L2 Strategic Implications

### Attack Path Analysis

#### Attack Path 1: Automated Zone 3 Exploitation via PTY (Primary Concern)

```
Prerequisites: Local code execution on jerry host + valid engagement ID
Step 1: Attacker initializes a test engagement (jerry tool exec --init-engagement attacker-eng)
Step 2: Attacker creates a Python script with the PTY pattern
Step 3: Script spawns jerry with PTY-allocated stdin
Step 4: Script writes "yes\n" to PTY master
Step 5: Zone 3 gate passes (isatty() returns True)
Step 6: Exploitation tool executes in container
Step 7: Audit trail shows "reason: operator input" -- no human flag
```

**Mitigating factors:** Step 1 requires legitimate engagement initialization (operator-level access). If an attacker has local code execution and can initialize engagements, they have already bypassed perimeter controls. The PTY bypass is a force multiplier, not an initial access vector.

**CVSS v3.1 estimate:** AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L = **7.8 (High)** - conditional on local access already being obtained.

#### Attack Path 2: Audit Trail Poisoning via PTY

```
Prerequisites: Same as Path 1
Additional step: Attacker is aware that audit trail does not distinguish PTY from human
Outcome: Post-incident analysis cannot confirm or deny human approval
Impact: Incident response credibility degraded; evidence chain broken
```

**CVSS v3.1 estimate:** AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N = **5.5 (Medium)** - integrity impact to audit evidence.

#### Attack Path 3: JERRY_ZONE3_TEST_MODE Env Var Leakage (Conditional)

```
Prerequisites: JERRY_ZONE3_TEST_MODE=auto_approve implemented naively AND env var leaks to production context
Step 1: Env var set in CI job with overly broad scope
Step 2: Shared CI runner inherits env var
Step 3: Subsequent jerry invocations bypass Zone 3 gate entirely
Impact: Complete bypass of Zone 3 gate without any TTY or human interaction
```

**CVSS v3.1 estimate (if naively implemented):** AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L = **8.5 (High)** - scope change because bypass extends to all Zone 3 tools.

**This path only materialises if the naive bypass implementation is chosen.** The scoped annotation-only approach does not have this path.

### Threat Model Gap Analysis

The existing threat model (as documented in the test file comments and implementation docstrings) explicitly states: "AI agents run in non-TTY subprocesses. The auto-deny policy ensures no Zone 3 tool can execute in an automated pipeline without explicit human approval."

This threat model correctly addresses the primary threat (AI agent autonomous execution) but does not address:

1. Intentional automation by a human using the PTY API (acknowledged in this analysis).
2. Audit trail manipulation via TTY-sourced approvals that are not human.

Neither gap requires immediate architectural change. Gap 1 is mitigated by the engagement prerequisite (an attacker needs prior operator-level access). Gap 2 is mitigated by adding the `source` field recommendation above.

### Vulnerability Chaining (Multi-Step Exploitation)

A credible multi-step attack chain leading to unauthorised Zone 3 exploitation:

```
CVE-equivalent: CWE-287 (Improper Authentication -- TTY check as human presence proof)
Chain: Local RCE -> Engagement initialization -> PTY bypass -> Zone 3 tool execution -> Audit trail poisoning
```

Each step requires escalating access. The chain is realistic only when an attacker already has local code execution. The Zone 3 gate is the last control in the chain, not the primary perimeter.

### Recommendations for Red-Exploit Prioritization

**Immediate (blocking test design):**

1. Accept the PTY approach for E2E testing with the following constraints documented in conftest.py:
   - The PTY fixture must be in a clearly named helper (e.g., `pty_approve_fixture`) with a docstring that prohibits reuse outside E2E tests.
   - The fixture must set `JERRY_ZONE3_TEST_SOURCE=test_pty` in the subprocess environment.

**Short-term (next sprint):**

2. Upgrade the gate to require `"APPROVE: {tool_name}"` instead of `"yes"`. Update PTY test fixture accordingly.
3. Add `source` field to the audit event JSON, populated from `JERRY_ZONE3_TEST_SOURCE` env var.
4. Add an assertion in the PTY test that verifies the audit event's `source` field equals `"test_pty"`.

**Medium-term (hardening sprint):**

5. Add a monitoring hook that logs a warning when any approved Zone 3 audit event has `source != "interactive_tty"`. This gives the SOC signal when the test pattern is used outside the test suite.
6. Consider adding a `JERRY_NO_PTY_BYPASS=true` env var that explicitly disables the TTY path and forces the non-interactive auto-deny. This would allow production hardened deployments to opt into a stricter gate.

### Eng-Team Hardening Recommendations

These recommendations are for the engineering team (Integration Point 2, eng-team):

1. **Gate upgrade (CWE-287 partial mitigation):** Replace the single `"yes"` acceptance with a context-bound confirmation phrase. The implementation is a two-line change in `_prompt_zone3_approval()`: replace `answer == "yes"` with `answer == f"approve: {tool_command.lower()}"` and update the prompt string.

2. **Audit trail source field (CWE-778 mitigation):** Add `"source"` to the `event` dict in `_write_approval_audit()`. Read `JERRY_ZONE3_TEST_SOURCE` env var. Default to `"interactive_tty"`. This is a four-line addition.

3. **Test fixture documentation:** In `tests/e2e/tool_exec/conftest.py`, add a `pty_zone3_approve` fixture with an explicit docstring:

   ```python
   # SECURITY: This fixture creates a real PTY to test the Zone 3 interactive
   # approval gate. The PTY pattern MUST NOT be used outside E2E tests.
   # Using this pattern in production scripts defeats the Zone 3 human-in-the-loop
   # requirement. See RED-W12-PTY vulnerability analysis for full details.
   ```

4. **Do not implement JERRY_ZONE3_TEST_MODE=auto_approve** as a gate bypass. The annotation-only variant (`JERRY_ZONE3_TEST_SOURCE`) is safe. The bypass variant is not.

---

## Coverage-Adjusted Scoring

No Coverage Feedback Envelope (CFE) is available for engagement RED-W12-PTY. Standard CVSS + exploitability scoring applies without modification per the graceful degradation protocol.

---

## ATT&CK Technique Mapping

| Finding | ATT&CK Technique | Description |
|---|---|---|
| PTY-TEST-001 (TTY bypass) | T1548 (Abuse Elevation Control Mechanism) | Abusing the interactive-terminal check as a privilege/access gate |
| PTY-TEST-003 (Audit gap) | T1562.006 (Indicator Removal -- Clear Command History) | Leaving ambiguous audit evidence that cannot confirm human vs. automated approval |
| PTY-TEST-004 (Env var bypass risk) | T1574.007 (Hijack Execution Flow -- Path Interception by PATH Variable) | Analogous: env var injection to influence execution flow |

---

## Evidence References

- Source: `src/interface/cli/tool_exec_commands.py`, lines 929-1022 (`_prompt_zone3_approval`)
- Source: `src/interface/cli/tool_exec_commands.py`, lines 1025-1146 (`_write_approval_audit`)
- Source: `tests/e2e/tool_exec/test_exploit.py`, lines 126-196 (`TestZone3AutoDenyNonTTY`)
- Source: `tests/e2e/tool_exec/conftest.py`, lines 250-277 (`_run` fixture - current non-PTY baseline)

*All analysis is grounded in source inspection of the above files. No exploitation was performed. No target systems were modified.*

---

*red-vuln v1.0.0 | Engagement RED-W12-PTY | 2026-03-19*
*PTES Vulnerability Analysis Phase | OWASP Testing Guide v4 | NIST SP 800-115 Chapter 5*
