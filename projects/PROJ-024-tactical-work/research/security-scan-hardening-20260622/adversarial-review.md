# Adversarial Review: Security-CI Hardening Design (ADR-secscan-hardening-001)

> **Strategy:** S-004 (Pre-Mortem) + S-002 (Devil's Advocate)
> **Criticality:** C3 — Security-relevant CI/CD change, multi-file (AE-005)
> **Scope:** READ-ONLY review of proposal drafts; no live files modified.
> **Executed:** 2026-06-22
> **Deliverable under review:** `ADR-secscan-hardening-001.md` + all files in `proposal/`
> **Reviewer role:** adv-executor (find every way this could break CI or undermine the security guarantee)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Findings Summary](#findings-summary) | Severity-classified table of all findings |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and fix for each finding |
| [Attack Surface Confirmations](#attack-surface-confirmations) | CONFIRMED-SAFE verdicts with evidence |
| [Execution Statistics](#execution-statistics) | Counts and protocol coverage |

---

## Findings Summary

| ID | Severity | Finding | File + Location |
|----|----------|---------|-----------------|
| PM-001 | **Critical** | `action.yml` reinstates the exact `LINE_COUNT >= 1` guard it claims to replace — D5 meaningful-audit guard is NOT implemented in the draft | `action.yml` line 172-180 |
| PM-002 | **Critical** | Auto-issue step silently skips when `audit` step exits non-zero — `if:` condition evaluates output on a failed step | `security-scan.yml.draft` line 80 |
| PM-003 | **Critical** | `fail-on-vuln` defaults to `'true'` in action.yml but `ci.yml.security-job.draft` passes it explicitly as `'true'` — however the ADR says CI should be **non-blocking** for live-advisory drift; these two contradict; worse, any red on `ci.yml`'s `security` job propagates to `ci-success` gate which currently IS a practical merge barrier | `action.yml` line 69, `ci.yml.security-job.draft` line 36, `ci.yml` lines 412-422 |
| PM-004 | **Major** | `audit_allowlist.py` silently FAIL-OPENS when `review_by` is missing from an entry — treats missing date as unexpired and emits the `--ignore-vuln` flag | `audit_allowlist.py` lines 65-68 |
| PM-005 | **Major** | `audit_allowlist.py` silently FAIL-OPENS on YAML parse error (non-dict data) and on malformed/empty `id` — a zero-byte file, a YAML list, or an entry with `id: ""` all produce zero flags and exit 0 | `audit_allowlist.py` lines 48-50, 92-94 |
| PM-006 | **Major** | 90-day cap is comment-only — the ADR states "Maximum acceptance window is advisory"; the schema and validator code enforce no upper bound on `review_by`, contradicting the ADR's D2 table which implies enforcement | `audit-allowlist.yml` line 21, `audit_allowlist.py` (no cap logic anywhere), `ADR-secscan-hardening-001.md` D2 field rules table |
| PM-007 | **Major** | `expiry_check` uses `review_by < today` (strictly less than) but ADR specifies `review_by <= today` as expired — an entry expiring **today** silently suppresses the CVE for one extra day | `audit_allowlist.py` line 69 |
| PM-008 | **Major** | `action.yml` invokes `audit_allowlist.py` **twice** (steps 5 and 6) — first call raises exit 1 on expired entries and halts the composite action before step 6 ever runs; step 6 then calls the script again into `$IGNORE_FLAGS`, but if the file is absent or the script is missing, `IGNORE_FLAGS` is silently empty and pip-audit runs with no flags | `action.yml` lines 138-143, 157-158 |
| PM-009 | **Major** | Auto-issue step has no `if: always()` — when `audit` step exits 1 (vuln found, `fail-on-vuln: true`), the step output `vuln-found` is set, but subsequent steps in the same job that rely on it may be skipped by default step-skip-on-failure; ADR says rolling issue is the forcing function | `security-scan.yml.draft` line 80 |
| PM-010 | **Minor** | CODEOWNERS additions missing trailing slash on `.github/security/` — the ADR text uses `\.github/security/` with a leading backslash (regex-escape style) which is not valid GitHub CODEOWNERS glob syntax | `ADR-secscan-hardening-001.md` line 541 |
| PM-011 | **Minor** | `action.yml` installs uv and Python internally — but so does the draft `ci.yml.security-job.draft`'s caller job? No — the ci.yml draft removes those steps and delegates entirely to the action; the action therefore DOES correctly own uv+python setup. However, in the scheduled job, the live `security-scan.yml` already does `astral-sh/setup-uv` + `uv python install` before the composite call, meaning if the draft is followed faithfully those steps now occur **twice** (once in the action, once removed from caller). Net result: double-install is harmless but wasteful. |`security-scan.yml.draft` lines 56-70, `action.yml` lines 87-97 |
| PM-012 | **Minor** | `action.yml` uses `shell: bash` on every `run:` step — composite actions require `shell:` to be specified on each step (unlike regular jobs); this is correctly handled in the draft. CONFIRMED-SAFE. Noted for completeness. | `action.yml` throughout |
| PM-013 | **Minor** | `uv export` in `action.yml` does NOT include `--no-emit-project` parameter but the step comment says it does (comment says "exclude jerry itself") — actually the flag IS present on line 125; comment and code are consistent. CONFIRMED-SAFE. | `action.yml` lines 121-127 |

---

## Detailed Findings

### PM-001: D5 Meaningful-Audit Guard NOT Implemented — Reinstates Old `LINE_COUNT >= 1` Bug

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **File** | `proposal/action.yml` lines 172-180 |
| **Attack Item** | #5 — Safety-check fix efficacy |

**Evidence:**

`action.yml` lines 172-180:
```bash
LINE_COUNT=$(wc -l < /tmp/pip-audit-output.txt)

if [[ "$LINE_COUNT" -lt 1 ]]; then
  echo "::error::pip-audit produced no output — possible silent failure"
  exit 1
fi
echo "pip-audit executed ($LINE_COUNT lines of output)"
```

The ADR (D5) specifies that the guard must assert **both** (1) a recognizable verdict sentinel AND (2) audited-package count >= 20 floor. The draft action contains **neither** of these checks. It contains only the original `LINE_COUNT >= 1` guard from `security-scan.yml` lines 84-88 that D5 was designed to replace.

This means the D5 fix is specified in the ADR but missing from the implementation draft. The false-green vector from the original Scan B survives: if `uv export` somehow produces a malformed short file, or the `--requirement` flag is ever dropped from a future edit, the `LINE_COUNT >= 1` check is satisfied by a single line of output and the action exits 0.

**Analysis:**

D5's entire value is the belt-and-suspenders structural assertion. The ADR explicitly states the floor check is "the assertion that the structural fix stayed in place" (ADR line 373). Without it, the composite action provides no additional guard against the original failure mode — only the structural change (always passing `--requirement`) provides protection.

**Recommended fix:**

Replace the `LINE_COUNT` guard in `action.yml`'s `Run pip-audit` step with:

```bash
# D5: Meaningful-audit guard — requires recognizable verdict AND package floor
VERDICT_LINE=$(grep -E "(No known vulnerabilities found|Found [0-9]+ known vulnerabilit)" /tmp/pip-audit-output.txt | head -1)
# Count packages from requirements file (guaranteed non-empty; we wrote it)
REQ_COUNT=$(grep -c . ${{ inputs.requirements-path }} || echo 0)

if [[ -z "$VERDICT_LINE" ]]; then
  echo "::error::audit did not produce a recognizable verdict — possible silent failure or neutered invocation"
  exit 1
fi
MIN_PKGS=${{ inputs.min-audited-packages }}
if [[ "$REQ_COUNT" -lt "$MIN_PKGS" ]]; then
  echo "::error::requirements file has only $REQ_COUNT packages (floor: $MIN_PKGS) — audit did not cover the full dependency tree"
  exit 1
fi
echo "Meaningful-audit guard passed: verdict found, $REQ_COUNT packages in scope"
```

Also add `min-audited-packages` as an input to the action (it is specified in the ADR inputs table but missing from the draft `inputs:` block).

---

### PM-002: Auto-Issue Step Fires Only When Audit Step SUCCEEDS — Silently Skips on Real CVEs

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **File** | `proposal/security-scan.yml.draft` line 80 |
| **Attack Item** | #6 — Auto-issue correctness; `if: always()` interaction |

**Evidence:**

`security-scan.yml.draft` lines 67-80:
```yaml
- name: Run security audit
  id: audit
  uses: ./.github/actions/security-audit
  with:
    fail-on-vuln: 'true'

- name: Create or update CVE alert issue
  if: steps.audit.outputs.vuln-found == 'true'
```

When `fail-on-vuln: 'true'` and vulnerabilities are found, the `audit` step exits non-zero. In GitHub Actions, a step that exits non-zero causes **all subsequent steps to be skipped by default** unless they carry `if: always()` or `if: failure()`. The condition `steps.audit.outputs.vuln-found == 'true'` evaluates to `true` for the output value, but the step is **already in skipped state** due to the preceding step failure.

The result is: when the scan finds real CVEs, the job exits 1 (good — it goes red), but the rolling issue is **never created or updated**. The alerting arm of D4 is dark exactly when it is needed most.

The same bug affects the "close issue when clean" step (line 127): when `fail-on-vuln: 'true'` and the audit is clean, the step exits 0 and the close-issue step does fire, but only because the prior step succeeded. The open/update path is broken.

**Analysis:**

This is the devsecops-flagged `if: always()` interaction from the task brief. The ADR (D4) says "the rolling issue is the forcing function." If the issue step never fires on red, the entire alerting arm of the design is non-functional in exactly the failure scenario it was designed for.

**Recommended fix:**

Add `if: always() && steps.audit.outputs.vuln-found == 'true'` to the create/update step, and `if: always() && steps.audit.outputs.vuln-found == 'false'` to the close step. For `vuln-found` to be available after a failed step, GitHub Actions requires outputs to be set before the step exits — which the draft does correctly (the `echo "vuln-found=true" >> "$GITHUB_OUTPUT"` lines run before `exit 1`). The `if: always()` unblocks the skip gate.

```yaml
- name: Create or update CVE alert issue
  if: always() && steps.audit.outputs.vuln-found == 'true'
```

```yaml
- name: Close CVE alert issue when clean
  if: always() && steps.audit.outputs.vuln-found == 'false'
```

---

### PM-003: Contradiction Between D3 Non-Blocking Policy and `fail-on-vuln: 'true'` in CI Draft

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **File** | `proposal/ci.yml.security-job.draft` line 36; `ci.yml` lines 412-422; `action.yml` line 69 |
| **Attack Item** | #1 — Deployment safety; #4 — Non-blocking security gap |

**Evidence:**

`ci.yml.security-job.draft` line 36: `fail-on-vuln: 'true'`

`ci.yml` lines 412-422 (`ci-success` aggregator):
```yaml
if [[ "${{ needs.security.result }}" != "success" ]] || \
```
The `ci-success` job checks `security.result == success`. If `security` fails (red pip-audit, `fail-on-vuln: 'true'`), `ci-success` fails.

`ci.yml` header line 5 (comment): `Permissions: contents:read only (no elevated permissions on any job)` — and crucially, no ruleset requires `ci-success` (confirmed from ADR referencing `required_status_checks: null`).

**Analysis:**

The design has three layers that must be understood together:

1. `fail-on-vuln: 'true'` → the `security` job exits non-zero when CVEs are found.
2. `ci-success` aggregates `security` and exits non-zero if `security` fails.
3. No GitHub branch ruleset requires `ci-success` as a required status check.

Because no ruleset requires `ci-success`, a red `security` job does NOT block merge at the platform level. D3 is technically preserved. However:

- The ADR draft comment in `ci.yml.security-job.draft` (lines 13-17) says "The CI security job is a **hard gate** on PRs" and "Keeping it blocking ensures that any dependency bump that introduces a NEW unfixed CVE fails immediately on the PR." This directly contradicts D3 ("non-blocking"). The comment argues FOR blocking; D3 argues against.
- The comment's claim is also factually incorrect given the confirmed absence of a required status check: red `security` does NOT block the merge gate.
- If the owner later does add `ci-success` as a required status check (a natural operational choice), then `fail-on-vuln: 'true'` in CI immediately becomes a hard merge block — violating D3 for every live-advisory-drift scenario.

This is a design contradiction embedded in the draft that will confuse the implementer and may lead to accidental blocking if operational practices change.

**Recommended fix:**

Decide explicitly on one of two internally-consistent options:

**Option A (true non-blocking, per D3):** Set `fail-on-vuln: 'false'` in `ci.yml.security-job.draft`. The step emits a `::warning::` but exits 0. The `security` job stays green. `ci-success` stays green. A red is visible as a warning annotation on the PR but never blocks. The rolling issue (D4) is the only forcing function. Update the comment to reflect D3 accurately.

**Option B (blocking on new-dep-introduced CVEs, future option from D3):** Keep `fail-on-vuln: 'true'` but document this explicitly as the "future narrowly-scoped blocking option" from D3, and add a ruleset that only adds `ci-success` as a required check on PRs that modify `uv.lock`/`pyproject.toml`. This requires repo ruleset work outside this PR.

The current draft is inconsistent and whichever option the owner intends, the code must match the stated policy.

---

### PM-004: Allowlist Parser FAIL-OPENS When `review_by` Is Missing

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/scripts/security/audit_allowlist.py` lines 65-68 |
| **Attack Item** | #2 — Fail-open vs fail-closed |

**Evidence:**

`audit_allowlist.py` lines 65-68:
```python
review_by_raw = entry.get("review_by", "")
if not review_by_raw:
    continue  # missing date treated as unexpired (allowlist schema enforces presence)
```

And `_build_ignore_flags` lines 86-94 (same pattern): if `review_by_raw` is falsy, the entry is treated as active and the `--ignore-vuln` flag IS emitted.

The comment says "allowlist schema enforces presence" — but no schema validation is invoked by the script or the action. The script is the only runtime validator; YAML schema validation is not implemented anywhere in the draft.

**Analysis:**

An entry with a missing or empty `review_by` silently becomes a **permanent suppression**. A PR that accidentally omits the expiry field (a typo, a YAML merge conflict that drops a line) would be accepted by CODEOWNERS review (human might miss the missing field), and from that point the CVE is permanently hidden.

The schema-enforces-presence comment is aspirational, not operational.

**Recommended fix:**

Change the `continue` to a fail-closed assertion: treat a missing `review_by` as an invalid entry and exit 1:

```python
review_by_raw = entry.get("review_by", "")
if not review_by_raw:
    print(
        f"::error::Accept-list entry {entry.get('id', '(no id)')} is missing required 'review_by' field.",
        file=sys.stderr,
    )
    return 1  # (restructure main to propagate this)
```

Also add a schema validation step to `main()` that checks all required fields before expiry logic runs.

---

### PM-005: Allowlist Parser FAIL-OPENS on Malformed YAML and Empty/Missing `id`

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/scripts/security/audit_allowlist.py` lines 48-50, 92-94 |
| **Attack Item** | #2 — Fail-open vs fail-closed; #3 — Accept-list abuse |

**Evidence:**

`_load_allowlist` lines 48-50:
```python
if not isinstance(data, dict):
    return []  # Non-dict YAML → empty list → zero flags → exit 0
```

`_build_ignore_flags` lines 92-94:
```python
vuln_id = entry.get("id", "").strip()
if vuln_id:
    flags.extend(["--ignore-vuln", vuln_id])
```

**Analysis — three distinct fail-open paths:**

1. **Zero-byte file:** `yaml.safe_load("")` returns `None`. `isinstance(None, dict)` is False → returns `[]` → exits 0 (no flags, no error). A truncated or empty allowlist file does not cause an error; it silently produces a scan with no suppressions. This is actually the correct behavior for an empty allowlist. However —

2. **YAML list instead of dict:** `accepted: []` is valid. But if someone writes the file as a bare YAML list at the top level (e.g., a merge conflict produces `- id: CVE...` without the `accepted:` key), `isinstance(data, list)` is False for dict check → returns `[]` → exits 0. All entries are silently dropped. The audit runs without any suppressions, which means CVEs that were supposed to be suppressed resurface with no error. This is FAIL-CLOSED for the suppression side (CVE resurfaces = red) but FAIL-OPEN for the expiry-enforcement side (no expired-entry error fires).

3. **Entry with `id: ""`:** Empty string id → `if vuln_id:` is False → flag not emitted. No error. The entry is silently ignored. If the id field was intentionally filled and a YAML parse issue left it empty, the entry does nothing — no suppression, no error. This is fail-closed for suppression (CVE is not hidden) but the silent drop means the audit team gets no signal that their entry was ignored.

The most dangerous path is #2: a corrupted top-level structure silently drops all entries, which looks like a working empty list but loses the expiry-enforcement signal for expired entries.

**Recommended fix:**

Add a top-level structure assertion after loading:

```python
if not isinstance(data, dict) or "accepted" not in data:
    print("::error::audit-allowlist.yml is malformed (expected a dict with 'accepted' key)", file=sys.stderr)
    sys.exit(1)
```

Also add a validation pass that rejects entries with empty `id` rather than silently skipping them.

---

### PM-006: 90-Day Cap Is Comment-Only — Not Enforced in Code

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/audit-allowlist.yml` line 21; `proposal/scripts/security/audit_allowlist.py` (no cap logic); ADR D2 field rules table |
| **Attack Item** | #3 — Accept-list abuse |

**Evidence:**

`audit-allowlist.yml` line 21:
```yaml
#     review_by:   <date> REQUIRED. ISO 8601 date by which this entry must be
#                         re-evaluated. The pipeline FAILS if today > review_by.
#                         Maximum: 90 days from accepted_on (team policy).
```

The word "Maximum: 90 days" appears in a comment only. The ADR D2 field rules table says the `review_by` field validation is "ISO-8601 date, strictly after `accepted_on`" — it does NOT include any upper-bound enforcement. `audit_allowlist.py` has no code that computes or enforces a maximum delta between `accepted_on` and `review_by`.

**Analysis:**

A reviewer could accept a CVE with `review_by: 2099-01-01` and the pipeline would happily emit `--ignore-vuln` for 73 years. The entire temporal-forcing-function of D2 is undermined. The cap is real policy but phantom enforcement.

The ADR explicitly acknowledges this in D2: "A hard cap can be added to the validator later if desired." The Open Questions (item 2) asks the owner to confirm. However, the gap between "advisory comment" and "enforced code" means deployment without the cap is a materially weaker design than described in the threat model section (which claims the expiry mechanism is a primary mitigation).

**Recommended fix:**

Add enforcement in `audit_allowlist.py`. This is a 4-line addition to the validation pass:

```python
MAX_DAYS = 90
accepted_on = date.fromisoformat(entry.get("accepted_on", ""))
review_by   = date.fromisoformat(entry.get("review_by", ""))
if (review_by - accepted_on).days > MAX_DAYS:
    print(f"::error::{entry['id']}: review_by exceeds {MAX_DAYS}-day cap", file=sys.stderr)
    return 1
```

Make `MAX_DAYS` an action input (defaulting to 90) so the owner can tune it without touching Python.

---

### PM-007: Off-By-One in Expiry Comparison — Entry Expiring Today Still Suppresses CVE

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/scripts/security/audit_allowlist.py` line 69 |
| **Attack Item** | #3 — Accept-list abuse |

**Evidence:**

`_check_expiry` line 69:
```python
if review_by < today:
    expired.append(entry)
```

`_build_ignore_flags` line 90:
```python
if review_by < today:
    continue  # expired — must not suppress
```

Both use strict less-than (`<`). The ADR D2 specifies: "`review_by <= today` → entry is **expired**." An entry dated `review_by: 2026-09-22` run on `2026-09-22` passes both comparisons (not `< today`) and continues to suppress the CVE for the entire day of its stated expiry date.

**Analysis:**

This is a boundary-condition bug. The ADR's expiry semantics are clear (`<=`); the code implements `<`. A CVE with `review_by: 2026-09-22` suppresses until `2026-09-23`. In practice this is a one-day window, but it contradicts the documented contract and could matter when the scheduled scan runs at 06:00 UTC on the expiry date.

**Recommended fix:**

Change both comparisons to `<=`:

```python
if review_by <= today:
    expired.append(entry)
```

```python
if review_by <= today:
    continue  # expired — must not suppress
```

---

### PM-008: Double-Invocation of `audit_allowlist.py` — Expiry Halt Before Flag Collection

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/action.yml` lines 135-143, 157-158 |
| **Attack Item** | #1 — Deployment safety |

**Evidence:**

`action.yml` Step 5 (lines 135-143):
```yaml
- name: Check accept-list expiry
  shell: bash
  run: |
    uv run python scripts/security/audit_allowlist.py \
      --allowlist ${{ inputs.allowlist-path }}
```
This step exits 1 if any entry is expired, halting the composite action.

`action.yml` Step 6 (lines 157-158):
```bash
IGNORE_FLAGS=$(uv run python scripts/security/audit_allowlist.py \
  --allowlist ${{ inputs.allowlist-path }})
```
This calls the script a second time to capture the `--ignore-vuln` flags.

**Analysis — two distinct issues:**

1. **Halt on expired entry before pip-audit runs:** When an entry is expired, step 5 exits 1 and step 6 never executes. This is the intended behavior for the expiry case: the audit fails before pip-audit even runs. This is intentional and correctly blocks. CONFIRMED-SAFE for this path.

2. **Double-parse on the non-expired path:** When no entry is expired, the script is invoked twice: once for the expiry check (step 5, output discarded), and once for flag building (step 6, stdout captured). Both succeed on the happy path. However, if the script is missing from the repo (the `scripts/security/` directory does not yet exist) or `uv run python` fails for a transient reason on step 6, the `IGNORE_FLAGS` variable is set to empty string, and `pip-audit` runs **with no ignore flags** — effectively treating the allowlist as empty. The pip-audit step then exits 1 (if CVEs are found), which looks like a real finding even if active suppressions should have applied.

   More critically: if the script file is somehow absent (e.g., missed in the PR), step 5 exits 1 with a clear Python `ModuleNotFoundError`-style error. But if the allowlist file is absent at step 6 (after a checkout issue), the script `_load_allowlist` returns `[]` silently (file not found → empty list) and flags are empty. The expiry check step 5 also would have passed (file not found → empty list → no expired entries → exit 0). So a missing allowlist file produces: step 5 succeeds, step 6 produces empty flags, pip-audit runs with no suppressions. CVEs resurface. This is FAIL-CLOSED (good — CVEs are not hidden), but the cause is invisible in the logs.

**Recommended fix:**

Consolidate to a single script invocation that outputs both the flags (stdout) and the expiry result (exit code). Capture the output and check the exit code in one step:

```bash
IGNORE_FLAGS=$(uv run python scripts/security/audit_allowlist.py --allowlist ${{ inputs.allowlist-path }})
ALLOWLIST_EXIT=$?
if [[ "$ALLOWLIST_EXIT" -ne 0 ]]; then
  echo "::error::CVE accept-list has expired entries; see above for details"
  exit 1
fi
```

This eliminates the double-parse and makes the expiry-halt step explicit without a separate step.

---

### PM-009: Auto-Issue Step Missing `if: always()` — Issue Step Skipped After Failed Audit

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `proposal/security-scan.yml.draft` lines 79-80 |
| **Attack Item** | #6 — Auto-issue correctness; `if: always()` interaction |

**Evidence (supporting PM-002):**

This is the root mechanism behind PM-002. Documenting it separately because it applies to both the create/update step AND the close step.

`security-scan.yml.draft` line 79-80:
```yaml
- name: Create or update CVE alert issue
  if: steps.audit.outputs.vuln-found == 'true'
```

GitHub Actions step default behavior: when a preceding step fails (non-zero exit), all subsequent steps are skipped unless they have `if: always()`, `if: failure()`, or `if: success() || failure()`. The `if:` expression `steps.audit.outputs.vuln-found == 'true'` is evaluated ONLY IF the step is not already in skipped state. Because the `audit` step exits 1 when `fail-on-vuln: 'true'` and vulnerabilities are found, the `create or update` step is in skipped state before its `if:` condition is even evaluated.

**Recommended fix:** Same as PM-002. This is the same finding; PM-002 and PM-009 are the same root cause described from two angles. Fix PM-002 to resolve both.

---

### PM-010: CODEOWNERS Pattern Uses Backslash Escape — Invalid Glob Syntax

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `ADR-secscan-hardening-001.md` line 541 |
| **Attack Item** | #7 — CODEOWNERS coverage gap |

**Evidence:**

ADR line 541:
```
Add `\.github/actions/    @geekatron` and `\.github/security/    @geekatron`
```

The leading backslash (`\.github/`) is not valid GitHub CODEOWNERS syntax. CODEOWNERS uses gitignore-style patterns where `.` in a path is literal (not a regex metacharacter); there is no need to escape it. The current live CODEOWNERS (lines 8-10) correctly uses `.github/workflows/` without a backslash.

The correct patterns are:
```
.github/actions/   @geekatron
.github/security/  @geekatron
```

**Analysis:**

If the implementer copies the ADR's escaped form into CODEOWNERS, GitHub may silently fail to match the pattern (behavior of unrecognized patterns in CODEOWNERS is to ignore them). The `.github/actions/` and `.github/security/` paths would then be unprotected, undermining the entire approval-gate guarantee for accept-list edits.

**Recommended fix:**

Remove the leading backslashes in the ADR and the implementation. Use the same pattern style as the current live CODEOWNERS:

```
.github/actions/   @geekatron
.github/security/  @geekatron
```

---

### PM-011: Double uv/Python Install — Wasteful But Not Harmful

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `proposal/action.yml` lines 87-97; `proposal/security-scan.yml.draft` (no pre-install steps in draft) |
| **Attack Item** | #1 — Deployment safety |

**Evidence:**

The live `security-scan.yml` (lines 47-53) runs `astral-sh/setup-uv` and `uv python install` before the audit. The draft `security-scan.yml.draft` removes those steps entirely (lines 53-70 in the draft go directly from `actions/checkout` to `uses: ./.github/actions/security-audit`). The action internally installs uv and Python (lines 87-97).

For the `ci.yml` caller, the draft removes the uv/Python install steps too (they are listed as "REMOVED" in the draft header).

This is actually handled correctly in the draft. The action owns its own environment setup; callers remove their duplicated setup. CONFIRMED-SAFE.

The one risk: the action's `uv-version` input defaults to `"0.10.9"` — the same pin in the current workflows. If future Dependabot bumps update the workflow pins but miss the action's default, the versions diverge. The input allows callers to override this, which is the right design.

**Recommended fix (optional):** Document in the action's header that Dependabot must be configured to update the pin inside `.github/actions/security-audit/action.yml`. Confirm Dependabot's `actions` ecosystem block (`.github/dependabot.yml`) covers this path — it likely does since the whole `.github/` tree is the target, but worth a single-line note.

---

## Attack Surface Confirmations

### Item 1: DEPLOYMENT SAFETY — Checkout Before `uses:` — CONFIRMED-SAFE (with caveat)

Both callers perform `actions/checkout` before invoking the composite action:

- `ci.yml.security-job.draft` line 31: `uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- `security-scan.yml.draft` line 58: `uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`

Local composite action resolution (`uses: ./.github/actions/security-audit`) requires the repo to be checked out. Both callers satisfy this. CONFIRMED-SAFE.

**Caveat:** PM-003 (fail-on-vuln contradiction) and PM-001 (missing D5 guard) are separate issues.

**SHA pins:** All `uses:` lines in both drafts use SHA pins matching the current repo standard (`de0fac2e4500dabe0009e67214ff5f5447ce83dd` for checkout v6.0.2, `08807647e7069bb48b6ef5acd8ec9567f424441b` for setup-uv v8.1.0). CONFIRMED-SAFE per EN-001.

**`permissions:` blocks:**
- `ci.yml.security-job.draft` inherits the workflow-level `permissions: contents: read`. CONFIRMED-SAFE.
- `security-scan.yml.draft` sets `permissions: contents: read\n  issues: write` at the workflow level (lines 44-46). This is slightly broad — `issues: write` applies to all jobs in the workflow, not just the issue-management step. However, there is only one job in the workflow, and the ADR explicitly calls this out as the least-privilege approach for a single-job workflow. CONFIRMED-SAFE (acceptable scope given single-job design).

**`uv export` invocation:** The draft uses `--no-hashes --frozen --all-extras --no-emit-project` — identical to the proven `ci.yml` invocation. CONFIRMED-SAFE.

---

### Item 2: FAIL-OPEN vs FAIL-CLOSED — FLAW-FOUND (PM-001, PM-004, PM-005)

The design has multiple fail-open paths:

- **PM-001 (Critical):** Missing allowlist file → script exits 0 → pip-audit runs with no suppressions → CVEs are NOT hidden (FAIL-CLOSED for CVE suppression), but the structural guard is absent.
- **PM-004 (Major):** Missing `review_by` field → entry treated as never-expiring suppression. FAIL-OPEN.
- **PM-005 (Major):** Non-dict YAML at top level → silent empty list → all entries dropped → CVEs resurface (FAIL-CLOSED for CVE suppression), but no error signal. Ambiguous.
- **Empty requirements file path:** If `uv export` fails with a non-zero exit, the `requirements-path` file either does not exist or is zero-byte. The action does not check for this; pip-audit would then fail with a "file not found" error and exit 1 — FAIL-CLOSED (the job goes red). CONFIRMED-SAFE for this specific path.

---

### Item 7: CODEOWNERS COVERAGE GAP — CONFIRMED OPEN (partially)

Live CODEOWNERS (lines 8-16) covers:
- `.github/workflows/` — covered
- `.github/dependabot.yml` — covered
- `.github/CODEOWNERS` — covered
- `.pre-commit-config.yaml` — covered
- `.context/rules/` — covered
- `docs/governance/` — covered

**NOT covered:**
- `.github/actions/` — CONFIRMED OPEN (ADR claim verified)
- `.github/security/` — CONFIRMED OPEN (ADR claim verified)

The ADR's claim that these paths are currently uncovered is accurate. The planned additions close the gap **if** the correct pattern syntax is used (see PM-010 — the ADR uses escaped patterns that are likely invalid).

---

## Execution Statistics

| Metric | Count |
|--------|-------|
| **Total Findings** | 13 |
| **Critical** | 3 (PM-001, PM-002, PM-003) |
| **Major** | 6 (PM-004, PM-005, PM-006, PM-007, PM-008, PM-009) |
| **Minor** | 4 (PM-010, PM-011, PM-012, PM-013) |
| **CONFIRMED-SAFE** | 4 attack items (checkout ordering, SHA pins, permissions, uv export invocation) |
| **FLAW-FOUND** | 4 attack items (D5 guard, fail-open paths, 90-day cap, off-by-one) |
| **Attack Items Reviewed** | All 8 specified items (plus FMEA-style enumeration in PM-008/PM-011) |
| **Protocol Steps Completed** | 8 of 8 specified attack vectors |

---

*Adversarial review by adv-executor. Strategy: S-004 (Pre-Mortem) + S-002 (Devil's Advocate). No live files modified. All evidence cited by file and line number. 2026-06-22.*

---

## Round-2 Re-verification

> **Executed:** 2026-06-22 (chain-of-verification pass on Revision 2 drafts)
> **Scope:** Per-finding re-verification of PM-001..PM-010; cardinal fail-closed path enumeration; regression check.
> **Method:** Direct file reads at cited lines — no revision summary taken on faith.

### Per-Finding Verdicts

| Finding | Verdict | Evidence (file : line) |
|---------|---------|------------------------|
| PM-001 | **RESOLVED** | `action.yml` lines 228-249: `VERDICT_LINE` grep matches `"No known vulnerabilities found\|Found [0-9]+ known vulnerabilit"` (assertion 1) AND `REQ_COUNT=$(grep -c -v '^\s*#\|^\s*$' …)` with `if [[ "$REQ_COUNT" -lt "$MIN_PKGS" ]]` (assertion 2). `min-audited-packages` input added at `action.yml` line 83 (default 20). Old `LINE_COUNT >= 1` guard is gone — only `wc -l` echo at line 148 is informational, not a gate. Both D5 assertions fail-closed. |
| PM-002 | **RESOLVED** | `security-scan.yml.draft` line 88: `if: always() && steps.audit.outputs.vuln-found == 'true'`. `vuln-found=true` is written to `$GITHUB_OUTPUT` at `action.yml` line 266 **before** the `exit 1` at line 271, so the output is readable after the step fails. The `always()` bypasses the default skip gate. |
| PM-003 | **RESOLVED** | `ci.yml.security-job.draft` line 43: `fail-on-vuln: 'false'`. The contradictory "hard gate" comment from the original draft is absent — header lines 12-22 correctly describe the non-blocking policy and explicitly caution against silently flipping to `'true'`. `action.yml` line 81: default for `fail-on-vuln` is `"false"`. D3 contradiction eliminated. |
| PM-004 | **RESOLVED** | `audit_allowlist.py` line 51: `REQUIRED_FIELDS = ("id", "package", "reason", "accepted_by", "accepted_on", "review_by", "ticket")`. Lines 127-133: loop over all `REQUIRED_FIELDS`; if `not value` or whitespace-only string, appends `::error::` and returns exit 1 via `main()` at line 264. Missing `review_by` is a hard error, not a silent pass. |
| PM-005 | **RESOLVED** | `_load_allowlist` lines 75-81: `yaml.YAMLError` → `return None` → `main()` returns 1 (line 244). Lines 85-92: non-dict or missing `accepted` key → `return None` → exit 1. Lines 94-102: `accepted` not a list → `return None` → exit 1. Zero-byte file returns `None` via `yaml.safe_load("")` returning `None` → `not isinstance(None, dict)` → exit 1. Bare-list top-level exits 1. Empty-id caught by required-field loop at line 129 (`not value` is True for `""`). |
| PM-006 | **RESOLVED** | `audit_allowlist.py` lines 47, 164-168: `MAX_DAYS = 90`; `delta = (review_by - accepted_on).days`; `if delta > MAX_DAYS:` appends error → exit 1. Exactly 90 days (`delta == 90`) passes (`> 90` is False). The cap is enforced in code, not comment-only. |
| PM-007 | **RESOLVED** | `audit_allowlist.py` line 175: `if today >= review_by:` (comment: "off-by-one fix: >= not >"). `_build_ignore_flags` line 205: `if today >= review_by: continue`. Both comparison sites use `>=`. An entry expiring today is expired on today's run. |
| PM-008 | **RESOLVED** | `action.yml` lines 160-182: single `set +e / IGNORE_FLAGS=$(...) / ALLOWLIST_EXIT=$? / set -e` block; `if ALLOWLIST_EXIT -ne 0: exit 1`. The two-invocation pattern is gone — one call captures stdout and checks exit code together. Missing script would cause Python error on the single call → exit non-zero → action halts with `::error::`. |
| PM-009 | **RESOLVED** | `security-scan.yml.draft` line 142: `if: always() && steps.audit.outputs.vuln-found == 'false'`. Both the create/update and the close-issue steps carry `if: always()`. Same root cause as PM-002; both step guards are fixed. |
| PM-010 | **RESOLVED** | `CODEOWNERS.addition` lines 18-19: `.github/actions/ @geekatron` and `.github/security/ @geekatron` — no leading backslash. Pattern matches live CODEOWNERS style (e.g., `.github/workflows/` at live CODEOWNERS line 8). ADR Revision 2 lines 97-99 shows the corrected anchored form `/.github/actions/` (also valid; the unanchored form in the addition file is equally correct per GitHub docs). |

### Cardinal Fail-Closed Enumeration

Every error path in the revised pipeline was traced. Results:

| Path | Behaviour | Verdict |
|------|-----------|---------|
| `audit_allowlist.py` missing from repo | `uv run python …` exits non-zero; `ALLOWLIST_EXIT != 0`; `action.yml` line 177: `exit 1` | FAIL-CLOSED |
| Allowlist file absent | `_load_allowlist` returns `[]` (line 71); empty list → no flags, no error, pip-audit runs with zero suppressions; CVEs surface | FAIL-CLOSED (CVEs not hidden) |
| YAML parse error | `yaml.YAMLError` → `return None` → `main()` returns 1 | FAIL-CLOSED |
| Non-dict top-level (bare list, scalar, null) | `not isinstance(data, dict)` → `return None` → exit 1 | FAIL-CLOSED |
| `accepted` key missing from dict | `"accepted" not in data` → `return None` → exit 1 | FAIL-CLOSED |
| `accepted` not a list | isinstance check lines 95-102 → `return None` → exit 1 | FAIL-CLOSED |
| Entry missing `review_by` (or any required field) | `REQUIRED_FIELDS` loop at line 127 → error appended → exit 1 | FAIL-CLOSED |
| Entry with empty `id: ""` | `not value` is True for `""` at line 129 → error → exit 1 | FAIL-CLOSED |
| `review_by` > 90 days after `accepted_on` | `delta > MAX_DAYS` at line 165 → error → exit 1 | FAIL-CLOSED |
| Entry expired (`review_by <= today`) | `today >= review_by` at line 175 → error → exit 1 | FAIL-CLOSED |
| Invalid ISO-8601 date string | `ValueError` at lines 145-157 → error appended → exit 1 | FAIL-CLOSED |
| pip-audit finds CVEs, `fail-on-vuln: 'true'` | `vuln-found=true` written **before** `exit 1` (lines 266, 271); issue step fires via `always()` | FAIL-CLOSED |
| pip-audit finds CVEs, `fail-on-vuln: 'false'` | `vuln-found=true` written, `::warning::` emitted, exits 0; issue step on close-path fires but `vuln-found != 'false'` so close step is skipped correctly; scheduled scan (with `fail-on-vuln: 'true'`) goes red separately | CORRECT |
| D5 guard: no verdict sentinel | `VERDICT_LINE` empty → `::error::` + `exit 1` at lines 232-235 | FAIL-CLOSED |
| D5 guard: requirements file below floor | `REQ_COUNT < MIN_PKGS` → `::error::` + `exit 1` at lines 242-249 | FAIL-CLOSED |
| `uv export` fails (non-zero) | `requirements-path` file absent or empty; D5 floor check: `grep -c -v '^\s*#\|^\s*$'` on absent file → error or 0; `0 < 20` → exit 1 | FAIL-CLOSED |

**No false-green path found.** Every ambiguous, malformed, missing-field, expired, or error condition terminates with a loud non-zero exit or resurfaces the CVE. The cardinal constraint ("fail-closed on every error path") is satisfied in the revised code.

### Residual Concerns (Non-Blocking)

**RR-001 (Minor — low risk):** `_build_ignore_flags` at lines 200-206 contains a redundant expiry check (`today >= review_by: continue`) that is unreachable after `_validate_entries` has already rejected all expired entries at line 175. This is belt-and-suspenders defense-in-depth, not a flaw, but it means `_build_ignore_flags` will silently skip an entry (no error) if somehow called with stale `today`. Since `main()` always calls `_validate_entries` first and only calls `_build_ignore_flags` when `errors` is empty, this cannot yield a false-green. **Not a blocking issue.**

**RR-002 (Minor — documentation):** `action.yml` line 81 sets `fail-on-vuln` default to `"false"`, which is correct for the CI context. However, `security-scan.yml.draft` line 71 explicitly passes `fail-on-vuln: 'true'` (overriding the default). If a third caller omits the argument it gets `'false'` (non-blocking). This is the intended behaviour, is documented in the action header (lines 13-16), and is not a regression. **Noted, not a finding.**

**RR-003 (Minor — operational):** The `max-acceptance-days` input mentioned in ADR Revision 2 (line 82: `max-acceptance-days`, owner-tunable) is not present as an action input; `MAX_DAYS` is hardcoded to 90 in the Python script. The ADR says it should be "exposed as an action input" but the draft does not implement the input plumbing. This is a gap between ADR text and code. Since 90 days is the correct default and the constant is trivially changed, this is **Minor / informational**; it does not affect security correctness.

### Regression Check

| Change | Prior behaviour | Revised behaviour | Regression? |
|--------|----------------|-------------------|-------------|
| PM-008 refactor: two invocations → one | Double-parse; second call could yield empty `IGNORE_FLAGS` silently | Single call; stdout captured with exit-code check; non-zero halts immediately | No regression — strictly safer |
| `if: always()` added to both issue steps | Issue steps skipped when audit failed | Issue steps fire on both red and clean runs (condition gates select correct branch) | No regression; close step on a clean run correctly finds `vuln-found == 'false'` and closes the issue if open |
| `fail-on-vuln` default changed to `'false'` (action default); `'false'` explicit in CI draft | CI draft had `'true'` (PM-003) | CI: `'false'`; scheduled scan: explicit `'true'` | No regression; scheduled scan retains `fail-on-vuln: 'true'` explicitly (security-scan.yml.draft line 71) |
| D5 guard replaces `LINE_COUNT >= 1` | One-line output satisfied the guard | Verdict sentinel AND package floor both required | No regression; guard is strictly stronger |
| `_validate_entries` replaces per-entry `continue` pattern | Missing `review_by` → silent suppression | Missing `review_by` → exit 1 | No regression; only tightens security |

### Overall Verdict

**SAFE TO IMPLEMENT AS-IS** — with the three Minor residuals noted above (RR-001, RR-002, RR-003), none of which affect the security guarantee. All 10 design-relevant findings (PM-001 through PM-010) are **RESOLVED** with verifiable evidence in the code. The cardinal fail-closed constraint is satisfied across all enumerated error paths. No regression was introduced by the revision.

**One pre-implementation action required (PM-003 / D3 policy gate):** The ADR explicitly defers the D3 non-blocking vs. blocking choice to the owner. `ci.yml.security-job.draft` now correctly implements `fail-on-vuln: 'false'` (non-blocking, Option A), but the ADR requires explicit owner confirmation before the implementation PR is opened. This is a governance gate, not a code defect.

---

*Round-2 re-verification by adv-executor. Strategy: S-011 (Chain-of-Verification). READ-ONLY. All evidence cited by file and line number. 2026-06-22.*
