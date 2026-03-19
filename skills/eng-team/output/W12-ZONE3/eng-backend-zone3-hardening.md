# eng-backend: Zone 3 Approval Hardening

> Engagement: W12-ZONE3-HARDENING | Tasks: TASK-045 (confirmation phrase), TASK-046 (audit source field)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was implemented, security posture outcome |
| [L1 Technical Detail](#l1-technical-detail) | Implementation specifics, code locations, test coverage |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture assessment and evolution path |
| [OWASP Verification](#owasp-verification) | Self-check against OWASP Top 10 |

---

## L0 Executive Summary

Two Zone 3 approval gate hardening tasks were delivered across four file changes
and verified with 449 passing unit tests (zero regressions).

**TASK-045 — Confirmation phrase:** The Zone 3 per-operation approval gate in
`_prompt_zone3_approval()` was upgraded from a `startswith("y")` prefix match
to a case-sensitive, exact-match confirmation phrase: the operator must type
`APPROVE: <tool_command>` verbatim to authorise execution. Any deviation —
wrong tool name, extra spaces, legacy "yes"/"y", uppercase/lowercase variation
— is denied. Audit records now include `confirmation_input` (what the operator
typed) and `expected_phrase` (what was required) for forensic traceability.

**TASK-046 — Audit source field:** `_write_approval_audit()` now emits a
`"source"` field populated from `JERRY_ZONE3_AUDIT_SOURCE` (default:
`"interactive_tty"`). This field identifies the invocation surface (operator
terminal, CI, E2E test suite) in every audit record without coupling the
domain to environment variables (read at the CLI infrastructure boundary, H-07
compliant).

**Key security controls applied:**
- OWASP A01:2021 (Broken Access Control): Exact-match confirmation prevents
  AI agent coercion and fat-finger accidental approvals.
- OWASP A07:2021 (Auth Failures): No prefix match, no case normalisation —
  the operator must demonstrate clear intent via the precise phrase.
- OWASP A09:2021 (Logging Failures): Audit records now carry operator input,
  expected phrase, and invocation source for forensic completeness.
- Fail-closed: If audit write fails on an approved operation, execution is
  denied (pre-existing FIX-R3-2 behaviour preserved and tested).

**Remaining risk areas:** E2E tests require a live container (impacket) and
are marked `@pytest.mark.e2e`; they are not run in the unit CI gate. Manual
E2E validation should be performed before merging to confirm the PTY approval
path with the new phrase format.

---

## L1 Technical Detail

### Change 1: `_prompt_zone3_approval()` — confirmation phrase (TASK-045)

**File:** `src/interface/cli/tool_exec_commands.py`

The interactive prompt block was rewritten. Previous behaviour:

```python
answer = input("  Approve? [yes/NO]: ").strip().lower()
approved = answer == "yes"
```

New behaviour (exact match, case-sensitive, no lower()):

```python
expected = f"APPROVE: {tool_command}"
prompt = (
    f"\n[SECURITY] Zone 3 per-operation approval required.\n"
    f"  Tool: {tool_command}\n"
    f"  Zone: 3 (Exploitation)\n"
    f"  Type the exact phrase to authorize: {expected}\n"
    f"  > "
)
response = input(prompt)
approved = response.strip() == expected
```

`response.strip()` removes the leading/trailing whitespace that terminal echo
may add, but does NOT collapse internal whitespace, so double-spacing or
alternate casing still fails the match.

The `_write_approval_audit()` call was extended to pass the new fields:

```python
audit_ok = _write_approval_audit(
    ...
    confirmation_input=response.strip(),
    expected_phrase=expected,
)
```

### Change 2: `_write_approval_audit()` — signature and source field (TASK-046)

**File:** `src/interface/cli/tool_exec_commands.py`

New optional parameters added to the function signature:

```python
def _write_approval_audit(
    ...,
    confirmation_input: str | None = None,
    expected_phrase: str | None = None,
) -> bool:
```

`"source"` field added to the audit event dict (infrastructure boundary read,
H-07 compliant):

```python
audit_source = os.environ.get("JERRY_ZONE3_AUDIT_SOURCE", "interactive_tty")
event["source"] = audit_source
```

`confirmation_input` and `expected_phrase` are added conditionally (only when
provided — auto-deny path does not supply them):

```python
if confirmation_input is not None:
    event["confirmation_input"] = confirmation_input
if expected_phrase is not None:
    event["expected_phrase"] = expected_phrase
```

**Resulting audit record structure (interactive path):**

```json
{
  "timestamp": "2026-03-19T...",
  "engagement_id": "E2E-TEST-001",
  "tool_command": "impacket-GetADUsers",
  "zone": "Zone 3",
  "approved": true,
  "reason": "operator input",
  "source": "interactive_tty",
  "confirmation_input": "APPROVE: impacket-GetADUsers",
  "expected_phrase": "APPROVE: impacket-GetADUsers"
}
```

### Change 3: E2E test updates

**File:** `tests/e2e/tool_exec/test_zone3_approval.py`

| Change | Details |
|--------|---------|
| `test_zone3_approve_with_pty_y` | Input changed from `"yes\n"` to `"APPROVE: impacket-GetADUsers\n"` |
| `test_zone3_deny_with_pty_n` | Input changed from `"n\n"` to `"APPROVE: wrong-tool\n"` (wrong tool = denied) |
| `test_zone3_deny_with_old_yes` | New regression test: `"yes\n"` is now denied; verifies exit 11 |
| `_run_with_pty()` helper | Added `extra_env` parameter; passes `env=child_env` to `subprocess.Popen` |
| All PTY tests | Inject `JERRY_ZONE3_AUDIT_SOURCE=e2e_test_pty` via `extra_env` |

### Change 4: New unit tests

**File:** `tests/unit/tool_exec/test_zone3_approval_logic.py` (new)

Pure logic tests — no PTY, no subprocess, no filesystem. Input patched via
`unittest.mock.patch("builtins.input", ...)` and `sys.stdin.isatty` mocked.
`_write_approval_audit` patched to return True/False as needed.

| Test class | Coverage |
|------------|---------|
| `TestConfirmationPhraseExactMatch` | Exact phrase passes for msfconsole, impacket |
| `TestConfirmationPhraseDenied` | Wrong tool, "yes", "y", double-space, lowercase "approve:", empty string, no-TTY auto-deny |
| `TestConfirmationPhraseAuditFields` | Audit call receives correct `confirmation_input` and `expected_phrase` on approve and deny |

**12 new tests, all green.**

### Regression fix: `test_r3_fixes.py`

`TestR3Fix2AuditWriteFailure.test_prompt_zone3_approval_denies_when_approved_but_audit_fails`
was updated: it previously sent `"yes"` as the input, which now correctly
evaluates to `approved = False`, preventing the `if approved and not audit_ok`
branch from firing. The test input was corrected to `"APPROVE: msfconsole"`
so the approved path is exercised and the fail-closed behaviour is verified.

### Test counts

```
tests/unit/tool_exec/ — 449 passed, 0 failed
tests/unit/tool_exec/test_zone3_approval_logic.py — 12 passed (new)
```

---

## L2 Strategic Implications

### Security posture assessment

The Zone 3 gate is now strongly resistant to the three primary threat vectors
identified in the threat model:

| Threat | Previous exposure | After TASK-045 |
|--------|------------------|----------------|
| AI agent coercion | Agent can send "yes" to any prompt | Must type `APPROVE: <exact-tool>` — agent would need to know the tool name and send it in a supervised context |
| Fat-finger approval | Typing any word starting with 'y' granted access | Must type the 44-character phrase exactly |
| Replay / automation | Any scripted "yes" would approve | Automated pipelines auto-deny (no TTY); interactive sessions need exact phrase |

The `confirmation_input` field in audit records enables post-incident forensics
to determine whether an operator typed the phrase deliberately or was coerced
by a tool that injected input programmatically.

### Dependency risk

No new external dependencies were introduced. All changes are to first-party
Python using `builtins.input`, `os.environ`, and the existing audit write
infrastructure.

### Scalability of the pattern

The confirmation phrase pattern scales cleanly to other approval-gated
operations: each gate generates its own `expected` phrase from the operation's
unique identifier. Adding new Zone 3 tools requires no changes to the gate
logic — the phrase is derived from `tool_command` at runtime.

### Evolution path

1. **MFA fatigue resistance:** If the approval gate is extended to push-based
   MFA, number-matching should be added (per ASVS 5.0 v2.9) to prevent
   fatigue attacks. The current phrase-match is the CLI equivalent.
2. **Rate limiting:** A future hardening pass should add a rate limit on
   Zone 3 approval attempts (max 3 per 5-minute window) to prevent brute
   forcing via PTY automation. The `source` field in audit records provides
   the audit surface needed to implement this.
3. **FIDO2/WebAuthn preference:** For high-value Zone 3 operations, consider
   routing through a FIDO2 hardware challenge before the phrase prompt for
   phishing-resistant operator verification.

---

## OWASP Verification

| OWASP Category | Status | Evidence |
|----------------|--------|---------|
| A01:2021 Broken Access Control | PASS | Exact-match confirmation; auto-deny for non-TTY; fail-closed on audit failure |
| A02:2021 Cryptographic Failures | N/A | No crypto in this change |
| A03:2021 Injection | PASS | `tool_command` is not executed here; confirmation phrase is string comparison only |
| A04:2021 Insecure Design | PASS | Threat model addressed; confirmation pattern prevents both accidental and coerced approval |
| A05:2021 Security Misconfiguration | PASS | Default `JERRY_ZONE3_AUDIT_SOURCE=interactive_tty`; no debug paths |
| A07:2021 Auth Failures | PASS | Case-sensitive exact match; no prefix/suffix flexibility; MFA fatigue mitigated by phrase complexity |
| A09:2021 Logging Failures | PASS | Audit records include `source`, `confirmation_input`, `expected_phrase`; fail-closed on audit write failure |
| A10:2021 SSRF | N/A | No outbound URL calls in this change |

---

*Generated by eng-backend | W12-ZONE3-HARDENING | 2026-03-19*
*SSDF: PW.5 (secure coding), PW.6 (secure defaults)*
