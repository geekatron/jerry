# ADR-secscan-hardening-001: Harden and De-Drift the Dependency Security Scanning Pipeline

> Nygard-format Architecture Decision Record. **DESIGN ONLY** — no live `.github/` files are modified by this ADR. It specifies the target design and an implementation plan for a follow-up PR.
>
> - **Status:** Proposed (Revision 2 — adversarial findings PM-001..PM-010 resolved; awaiting owner approval)
> - **Date:** 2026-06-22 (Rev 1) · 2026-06-22 (Rev 2)
> - **Deciders:** @geekatron (repo owner / code owner)
> - **Criticality:** C3 (security-relevant CI/CD change, multi-file, AE-005 auto-escalation)
> - **Project:** PROJ-024-tactical-work
> - **Author:** eng-architect (Solution Architect & Threat Modeler)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Lifecycle state of this decision |
| [Revision 2 — Adversarial Findings Resolved](#revision-2--adversarial-findings-resolved) | PM-001..PM-010 resolution map + cardinal fail-closed constraint |
| [Context](#context) | The drift, the false-green, and the constraints |
| [Threat Model](#threat-model) | STRIDE + attack-surface analysis driving the design |
| [Decision](#decision) | The chosen architecture (5 sub-decisions) |
| [D1 — DRY via Local Composite Action](#d1--dry-via-local-composite-action) | Composite vs reusable-workflow vs script |
| [D2 — Owner Accept-List for Transitive CVEs](#d2--owner-accept-list-for-transitive-cves) | Schema, expiry semantics, approval flow |
| [D3 — Non-Blocking Policy](#d3--non-blocking-policy) | Alert-as-forcing-function, risk tradeoff |
| [D4 — Alerting Design](#d4--alerting-design) | Rolling issue + Dependabot native alerts |
| [D5 — Safety-Check Fix](#d5--safety-check-fix) | Meaningful-audit guard replacing line-count |
| [Composite Action Responsibility Breakdown](#composite-action-responsibility-breakdown) | Inputs, outputs, step contract |
| [Verification Strategy (Red/Green)](#verification-strategy-redgreen) | Test-first proof using today's 9 CVEs |
| [Consequences](#consequences) | Positive, negative, neutral outcomes |
| [File-Change Plan](#file-change-plan) | Every file created/changed at implementation time |
| [Alternatives Considered](#alternatives-considered) | Rejected options with rationale |
| [NIST CSF 2.0 Mapping](#nist-csf-20-mapping) | Control-to-function alignment |
| [Open Questions for Human Verification](#open-questions-for-human-verification) | Items requiring owner confirmation |
| [References](#references) | Cited files and external sources |

---

## Status

**Proposed.** Awaiting code-owner review. Supersedes the informal follow-up items #3 in
`projects/PROJ-024-tactical-work/research/dependabot-merge-analysis-20260622/RECOMMENDATION.md`
(line 89) and recommendation #3 in `PR-298-and-ci-rootcause.md` (line 220), which both flagged
the scheduled-scan blind spot without specifying a fix.

Revision 2 incorporates the resolutions to the adversarial review
(`research/security-scan-hardening-20260622/adversarial-review.md`, findings PM-001..PM-010). The
status remains **Proposed**: one policy decision (D3 / PM-003) is framed for the owner below and
must be confirmed before implementation lands.

---

## Revision 2 — Adversarial Findings Resolved

> The S-004 (Pre-Mortem) + S-002 (Devil's Advocate) review at
> `research/security-scan-hardening-20260622/adversarial-review.md` surfaced 13 findings; the 10
> design-relevant findings (PM-001..PM-010) are resolved here. PM-011 (double install) is a
> wasteful-but-harmless note; PM-012 and PM-013 were verdicts of CONFIRMED-SAFE — no action.
> **The code fixes for the implementation-side findings are being applied in parallel by the
> eng-devsecops agent in the `proposal/` drafts** (`action.yml`, `security-scan.yml.draft`,
> `ci.yml.security-job.draft`, `scripts/security/audit_allowlist.py`); this section records the
> design decision behind each fix so the ADR and the drafts stay in lockstep.

### Cardinal design constraint (binding)

**FAIL-CLOSED ON EVERY ERROR PATH.** Every ambiguous, malformed, missing, or error condition in the
audit pipeline MUST resolve to a loud non-zero exit (or a resurfaced CVE), never to a silent green
or a silent suppression. This is the single principle the review proved was violated in the original
Scan B (a dark detector that exited 0) and in several draft code paths (fail-open suppression). It
is now a **binding constraint on this design and all implementing code**: a reviewer evaluating any
future change to the composite action, the accept-list parser, or the alerting steps MUST reject any
path where an error, a parse failure, or a missing field can produce a passing/clean/suppressed
outcome. Detection failures and suppression failures both fail closed.

### Finding → resolution map

| Finding | Sev | Root issue | Resolution (design) | Code fix (eng-devsecops, parallel) |
|---------|-----|-----------|---------------------|-----------------------------------|
| **PM-001** | Critical | Draft `action.yml` reinstated the `LINE_COUNT >= 1` guard D5 was meant to replace — the meaningful-audit guard was never implemented. | D5 is **binding**: the guard MUST assert (1) a recognizable verdict sentinel (`No known vulnerabilities found` OR `Found N known vulnerabilit…`) AND (2) audited-package count `>= min-audited-packages` (default 20). Absence of either ⇒ `::error::audit did not run meaningfully` + non-zero exit. `min-audited-packages` is added to the action `inputs:` block (it was in the ADR table but missing from the draft). Fail-closed. | Replace `LINE_COUNT` guard in `action.yml` with the verdict+floor check; add `min-audited-packages` input. |
| **PM-002** | Critical | Rolling-issue create/update step is skipped when the `audit` step exits non-zero (default step-skip-on-failure), so the alert is dark exactly when CVEs are found. | The alerting arm is the forcing function (D4) and MUST run on the red path. Create/update step gated `if: always() && steps.audit.outputs.vuln-found == 'true'`. Outputs are written before the audit step exits (already correct in draft), so the value is available after failure. | Add `if: always() && …` to the create/update step in `security-scan.yml.draft`. |
| **PM-003** | Critical | `fail-on-vuln: 'true'` in the CI draft + a draft comment calling CI a "hard gate" **contradict** D3 (non-blocking); and if the owner ever makes `ci-success` a required check, CI becomes a hard merge block on advisory-DB drift. | **Policy decision deferred to the owner** — see the reframed [D3](#d3--non-blocking-policy). Recommendation: **Option A (non-blocking, `fail-on-vuln: 'false'`)**, which is what the drafts implement by default. The contradictory "hard gate" comment is removed. | Set `fail-on-vuln: 'false'` in `ci.yml.security-job.draft`; emit `::warning::` not failure; delete the "hard gate" comment. (Pending owner confirm of A vs B.) |
| **PM-004** | Major | Accept-list parser **fail-opens** on a missing `review_by` — treats it as never-expiring and emits the suppression flag. | Missing `review_by` (or any missing required field) is an **invalid entry ⇒ exit 1**, per the cardinal constraint. The "schema enforces presence" comment was aspirational; a runtime validation pass now enforces it before expiry logic runs. | Replace `continue` with a fail-closed validation error in `audit_allowlist.py`; add a required-field validation pass in `main()`. |
| **PM-005** | Major | Parser fail-opens on malformed YAML (non-dict / bare list / zero-byte) and on empty `id` — entries silently dropped, expiry signal lost. | After load, assert top-level is a dict containing an `accepted` key, else `::error::` + exit 1. Reject entries with empty/missing `id` (loud), do not silently skip. Empty `accepted: []` remains valid (zero suppressions). Fail-closed on structure. | Add structure assertion in `_load_allowlist`; reject empty-`id` entries in the validation pass. |
| **PM-006** | Major | 90-day cap is comment-only; a reviewer could set `review_by: 2099-01-01` and suppress for decades, gutting the temporal forcing function. | Enforce a maximum acceptance window **in code**, exposed as an action input (`max-acceptance-days`, default 90) so the owner tunes it without editing Python. `(review_by - accepted_on).days > max` ⇒ exit 1. This **resolves Open Question #2** (cap is now enforced, default 90, owner-tunable). | Add `MAX_DAYS`/`max-acceptance-days` enforcement to the validation pass in `audit_allowlist.py`; add the input to `action.yml`. |
| **PM-007** | Major | Expiry comparison uses `review_by < today` but the ADR specifies `review_by <= today`; an entry suppresses for one extra day on its stated expiry date. | Code MUST match the documented contract: `review_by <= today` ⇒ expired (no suppression + expiry guard fires). Both comparison sites changed to `<=`. | Change both `<` comparisons to `<=` in `audit_allowlist.py`. |
| **PM-008** | Major | `audit_allowlist.py` is invoked twice (expiry check, then flag build); on the happy path it double-parses, and a transient failure on the second call yields empty `IGNORE_FLAGS` with no signal. | Consolidate to a **single invocation** that emits flags on stdout and signals expiry via exit code; capture both in one step and fail closed on non-zero. Removes the double-parse and the silent-empty-flags window. A missing accept-list file resurfaces CVEs (fail-closed) — acceptable, and now logged. | Merge steps 5 and 6 in `action.yml` into one capture-stdout + check-exit-code step. |
| **PM-009** | Major | Same root cause as PM-002, applied to the **close-on-clean** step as well as the create/update step. | The close-issue step is gated `if: always() && steps.audit.outputs.vuln-found == 'false'` so a clean run after remediation reliably closes the rolling issue. Resolving PM-002 resolves this; both step `if:` conditions updated. | Add `if: always() && …` to the close-issue step in `security-scan.yml.draft`. |
| **PM-010** | Minor | ADR (line 541) wrote CODEOWNERS patterns with a leading backslash (`\.github/…`), which is **not** valid CODEOWNERS gitignore-style syntax; GitHub silently ignores unrecognized patterns, leaving the paths unprotected. | Corrected in the [File-Change Plan](#file-change-plan) to valid anchored gitignore-style patterns with **no** backslash escaping (see correction below). Explicitly: **without these entries the accept-list approval guarantee does not hold.** | CODEOWNERS is a live file changed by the implementation PR (design-only here); the corrected patterns are specified for that PR. |

**Findings outside the PM-001..PM-010 scope (recorded for completeness):** PM-011 (composite action and callers; double uv/Python install is wasteful but harmless — callers already drop their setup steps, action owns its env), and the two CONFIRMED-SAFE notes PM-012 (`shell: bash` correctly set per composite step) and PM-013 (`--no-emit-project` present and comment-consistent). No design change required for these.

### PM-010 — corrected CODEOWNERS guidance

The original ADR text used regex-escape-style patterns (`\.github/actions/`, `\.github/security/`).
CODEOWNERS uses **gitignore-style globs**, where `.` is a literal character and MUST NOT be
escaped. The current live CODEOWNERS already uses the unescaped form (e.g., `.github/workflows/`).
The implementation PR MUST add these **valid** entries:

```gitignore
/.github/actions/   @geekatron
/.github/security/  @geekatron
```

The leading `/` anchors each pattern to the repository root (matching the directory and everything
beneath it) and is the recommended explicit form; the unescaped, unanchored `.github/actions/`
style used elsewhere in the file is equally valid. **What is invalid is the backslash escaping.**

**Why this is load-bearing, not cosmetic:** GitHub silently ignores CODEOWNERS lines it cannot
parse. If the escaped form is copied verbatim, `.github/actions/` and `.github/security/` would
remain **unowned**, code-owner review would **not** be required on accept-list edits, and the entire
D2 approval guarantee ("acceptance = a reviewed, merged PR by a code owner") would **silently not
hold** — anyone with write access could add an `--ignore-vuln` suppression with no second pair of
eyes. **State explicitly: without these CODEOWNERS entries, the accept-list approval guarantee does
not hold.** This was confirmed in the review (Item 7: `.github/actions/` and `.github/security/` are
CONFIRMED OPEN — uncovered today).

---

## Context

Jerry runs **two** independent pip-audit-based supply-chain scans that have **drifted** into
contradictory behavior. They produce opposite verdicts on the **same** committed `uv.lock`.

### Scan A — `ci.yml` job `security` (PR/push triggered) — CORRECT, RED

`.github/workflows/ci.yml` lines 68-89:

```yaml
- run: uv sync --frozen
- run: uv export --no-hashes --frozen --all-extras --no-emit-project > /tmp/requirements.txt
- run: uv run pip-audit --requirement /tmp/requirements.txt --strict --desc
```

Because it audits the **exported requirements file** (every pinned transitive dep), it correctly
finds the live CVEs. Confirmed present in `uv.lock` today (read directly):

| Package | Installed (uv.lock) | Fixed in | Example advisory |
|---------|---------------------|----------|------------------|
| mako | 1.3.10 | 1.3.12 | CVE-2026-44307 (Windows path traversal) |
| urllib3 | 2.6.3 | 2.7.0 | PYSEC-2026-141, PYSEC-2026-142 |
| msgpack | 1.1.2 | 1.2.1 | GHSA-6v7p-g79w-8964 (DoS/SEGV) |
| pydantic-settings | 2.13.1 | 2.14.2 | GHSA-4xgf-cpjx-pc3j (symlink secret read) |
| pip | 26.0 | 26.1.2 | PYSEC-2026-196, CVE-2026-3219, CVE-2026-6357 |

This job reports "Found 9 known vulnerabilities in 5 packages" and exits 1. This is the
**ground-truth detector**. (Note: `main` itself was green on 2026-04-21; these advisories were
published *after* that run — the red is live-advisory-DB drift against a static lockfile, per
`adversarial-review.md` C3. The fix here is about the *scheduled* scan, not silencing Scan A.)

### Scan B — `security-scan.yml` (daily cron) — BROKEN, FALSE GREEN

`.github/workflows/security-scan.yml` lines 62-89:

```yaml
- run: |
    if uv run pip-audit --strict --desc 2>&1 | tee /tmp/pip-audit-output.txt; then
      ...
- name: Verify pip-audit executed         # PM-001 guard
  run: |
    LINE_COUNT=$(wc -l < /tmp/pip-audit-output.txt)
    if [[ "$LINE_COUNT" -lt 1 ]]; then ... ; fi
```

It runs `pip-audit` with **no `--requirement`**. In a `uv run` context this audits the active
environment, where pip-audit emits a single non-fatal note —
`Dependency not found on PyPI and could not be audited: jerry (0.31.5)` — audits effectively
nothing, and exits **0 = FALSE GREEN**. Two latent defects compound:

1. **No `--requirement`** → the local first-party package (`jerry`) is the only thing "seen,"
   and it is unauditable, so the real transitive tree is never checked.
2. **The guard is fooled.** `--strict` is documented as "fail the entire audit if dependency
   *collection* fails on any dependency" — collection of `jerry` does not *fail*, it merely
   reports the package is not on PyPI, so `--strict` never fires. The
   `Verify pip-audit executed` step then only asserts `LINE_COUNT >= 1`; the one-line
   "couldn't find jerry" message satisfies it. **The detector that was created specifically as
   the compensating control for transitive CVEs (per the workflow header citing S-001 RT-002,
   S-004 PM-001, S-012 FM-009) is dark.**

### The structural cause of drift

The two scans were authored separately and **duplicate the audit logic** with subtly different
invocations. There is no single source of truth for "how Jerry audits its dependency tree," so
they drifted. This is the root cause the design must eliminate.

### Dependabot context (`.github/dependabot.yml`)

Lines 201-202: `allow: dependency-type: direct` for the uv ecosystem. By design, transitive
CVEs never get a Dependabot **version-update** PR (only direct deps do). The header (lines 66-83)
explicitly names the scheduled scan as the **compensating detector** for transitive CVEs — which
is exactly the scan that is currently false-green. So today there is an **unmonitored gap**:
transitive CVEs are neither version-bumped by Dependabot nor detected by the scheduled scan.
(Dependabot **security** updates are event-driven and separate — see [D4](#d4--alerting-design).)

### Constraints (owner decisions this ADR designs to)

| # | Constraint |
|---|------------|
| C-1 | DRY: one shared audit logic invoked by both `ci.yml` and the scheduled workflow. |
| C-2 | Owner accept-list for un-fixable transitive CVEs, with **mandatory expiry** that auto-resurfaces. |
| C-3 | Non-blocking: the audit MUST NOT become a required status check; alerting is the forcing function. |
| C-4 | Alerting: one rolling GitHub issue + native Dependabot alerts. |
| C-5 | Safety-check must verify a **meaningful** audit occurred, not merely ≥1 line of output. |
| C-6 | Verification: prove red on today's 9 CVEs, then green after the dependency bumps (test-first). |

### Governance constraints (Jerry framework)

- **AE-005**: security-relevant code → C3 minimum. This is a C3 design.
- **H-04 / P-002**: output persisted to a project file (this ADR).
- **P-022**: limitations disclosed; items needing human verification are flagged explicitly.
- This is **design-only**; the implementation PR is governed separately (H-32 GitHub Issue parity).

---

## Threat Model

STRIDE applied to the data flow "advisory database → audit job → merge/alert decision." The
trust boundary is the GitHub Actions runner ingesting the **external OSV/PyPI advisory DB** and
the **in-repo accept-list** to produce a security verdict.

| STRIDE | Threat against the scanning pipeline | Current state | Mitigation in this design |
|--------|--------------------------------------|---------------|---------------------------|
| **S**poofing | A malformed/forged accept-list entry suppresses a real CVE. | No accept-list exists. | Accept-list edits gated by CODEOWNERS PR review (git-signed audit trail); schema-validated; `--ignore-vuln` only suppresses the *exact aliased ID*, never a package wildcard. |
| **T**ampering | Audit logic silently weakened (e.g., `--requirement` dropped, as already happened in Scan B). | **REALIZED** in Scan B. | Single composite action = one place to review; CODEOWNERS extended to `.github/actions/`; verification test (red/green) detects a neutered audit. |
| **R**epudiation | A CVE is accepted with no record of who/when/why. | No mechanism. | Accept-list requires `accepted_by`, `accepted_on`, `ticket`; approval is a reviewed PR (immutable git history). |
| **I**nformation disclosure | Audit output leaks secrets. | Low — pip-audit hits public DB; jobs are `contents: read`. | Preserve `permissions: contents: read` on the audit job; issue-writer step uses a narrowly-scoped `issues: write` only in the scheduled workflow. |
| **D**enial of service (of the control) | The detector is dark and nobody notices (false green). | **REALIZED** in Scan B. | Meaningful-audit guard (D5) + red/green verification + rolling issue makes a dark detector visible. |
| **E**levation of privilege | Audit job acquires write scope it doesn't need. | Acceptable today. | Least privilege: audit logic stays `contents: read`; only the alerting step in the scheduled workflow gets `issues: write`. Composite action itself requests **no** permissions. |

**Attack-surface note (accept-list as a new surface):** introducing an accept-list creates a
*new* suppression channel. The dominant risk is **T**ampering/**S**poofing (a stale or
over-broad suppression hiding a live CVE). The expiry-with-auto-resurface mechanism (D2) and the
exact-ID match (no wildcards) are the primary controls; CODEOWNERS review is the human gate.

---

## Decision

Adopt five coordinated sub-decisions:

1. **D1** — Extract the audit into a **local composite action** at `.github/actions/security-audit/action.yml`, consumed by both `ci.yml` and the scheduled workflow.
2. **D2** — Introduce an **owner accept-list** at `.github/security/audit-allowlist.yml` with mandatory `review_by` expiry; the action translates unexpired entries into `--ignore-vuln` flags and **fails** on expired entries.
3. **D3** — Keep the audit **non-blocking** (never a required status check); the forcing function is alerting, not a merge block.
4. **D4** — The scheduled scan opens/updates **one rolling GitHub issue**; confirm Dependabot native security updates + vulnerability alerts are enabled.
5. **D5** — Replace the line-count guard with a **meaningful-audit guard** that asserts the audit produced a recognizable clean-or-vulnerable verdict over a non-trivial package count.

---

### D1 — DRY via Local Composite Action

**Decision:** A single **local composite action** at `.github/actions/security-audit/action.yml`
owns the canonical audit logic. Both consumers call it after they already do
`actions/checkout` + `astral-sh/setup-uv` + `uv python install` (both already perform these
steps today — see `ci.yml` lines 72-83 and `security-scan.yml` lines 44-56).

**Options evaluated:**

| Option | How it works | Pros | Cons | Verdict |
|--------|--------------|------|------|---------|
| **A. Local composite action** (`.github/actions/security-audit`) | `uses: ./.github/actions/security-audit` after checkout + uv setup | Caller controls runner/checkout/uv (no duplication of env setup); inputs/outputs are a clean contract; steps render inline in each job's log (good observability); lives in-repo, versioned with the workflows that use it; both callers already checkout + set up uv. | Requires the repo to be checked out before use (already true for both). | **CHOSEN** |
| **B. Reusable workflow** (`workflow_call`) | A separate job invoked via `uses: ./.github/workflows/audit.yml` | Can encapsulate the *entire* job incl. its own checkout/uv setup; can set its own `permissions`. | Runs as a **separate job** (extra runner spin-up, separate log surface); cannot be dropped *inside* the existing `security` job that also does the banned-YAML check — would split that job or force the YAML check to move; harder to share the already-present checkout/uv steps. Heavier than needed when both callers already establish the environment. | Rejected |
| **C. Shared script** (`scripts/security_audit.py` or `.sh`) | Both workflows `run: ...` the script | Simplest mechanically; testable locally via `uv run`. | No declared input/output **contract** (args are positional/env, easy to drift again — the very failure mode we are fixing); no GitHub-native step boundaries/summaries; accept-list parsing + flag translation + guard all become bespoke shell/Python with weaker self-documentation. | Rejected |

**Rationale for A over B:** The `ci.yml` `security` job does **two** things — pip-audit *and* the
banned-YAML-API check (lines 91-106). A composite action lets us replace **only** the audit steps
in-place, leaving the YAML check in the same job (no job topology change, no new required-check
surface, [D3](#d3--non-blocking-policy) preserved trivially). A reusable workflow would force that
job to be split. Both callers already `checkout` + `setup-uv`, so the composite action's
"requires checkout first" constraint costs nothing.

**Rationale for A over C:** The root cause of the current drift is *duplicated logic with no
contract*. A composite action's `inputs:`/`outputs:` block is an explicit, reviewable contract
that resists silent drift (exactly the regression in Scan B where `--requirement` was dropped). A
bare script reintroduces the contract-free coupling we are eliminating.

---

### D2 — Owner Accept-List for Transitive CVEs

**Decision:** A single human-readable YAML file at `.github/security/audit-allowlist.yml`. Each
accepted vulnerability is an entry with mandatory provenance and a mandatory expiry. The composite
action:

1. Parses the file.
2. For each entry whose `review_by` is **in the future**, emits a `--ignore-vuln <id>` flag.
3. For each entry whose `review_by` is **today or in the past**, treats it as **expired**: the
   entry is **NOT** suppressed (so the CVE resurfaces and the audit goes red), **and** the action
   fails its own "expired acceptance" assertion so the cause of the new red is unambiguous.

This makes acceptance a **time-boxed** decision that auto-forces re-review. `--ignore-vuln` is
documented as repeatable and **alias-aware** (a `GHSA-`, `CVE-`, or `PYSEC-` id all match), and
has been available since pip-audit 2.3.0; the lockfile pins `pip-audit>=2.10.0`, so the flag is
available.

**Schema** (`.github/security/audit-allowlist.yml`):

```yaml
# Owner accept-list for KNOWN, currently-unfixable transitive CVEs.
# Editing this file REQUIRES a code-owner-approved PR (see CODEOWNERS).
# Each entry is a TIME-BOXED acceptance. Past `review_by` => CVE resurfaces + audit fails.
version: 1
accepted:
  - id: "PYSEC-2026-XXXX"        # REQUIRED. The vuln id as pip-audit prints it (GHSA/CVE/PYSEC all match via alias).
    package: "examplepkg"         # REQUIRED. Package name (human cross-check; not used for matching).
    reason: >                     # REQUIRED. Why accepted (no fix available / not reachable / etc.).
      No fixed release exists yet; vulnerable code path is not reachable from Jerry
      because <specific justification>.
    accepted_by: "@geekatron"     # REQUIRED. GitHub handle of the accepting code owner.
    accepted_on: "2026-06-22"     # REQUIRED. ISO-8601 date acceptance was granted.
    review_by: "2026-09-22"       # REQUIRED. ISO-8601 EXPIRY. On/after this date the entry stops suppressing.
    ticket: "https://github.com/geekatron/jerry/issues/NNN"  # REQUIRED. Tracking issue (H-32 parity).
```

**Field rules:**

| Field | Required | Validation |
|-------|----------|------------|
| `id` | Yes | Non-empty string; matches `^(GHSA-|CVE-|PYSEC-).+` (advisory id family). |
| `package` | Yes | Non-empty string (cross-check / readability; matching is by `id` only — never by package, to prevent over-broad suppression). |
| `reason` | Yes | Non-empty; ≥ 20 chars (forces a real justification). |
| `accepted_by` | Yes | GitHub handle (`^@`). SHOULD be a code owner (enforced socially via PR review). |
| `accepted_on` | Yes | ISO-8601 date, not in the future. |
| `review_by` | Yes | ISO-8601 date, strictly **after** `accepted_on`. **This is the expiry.** |
| `ticket` | Yes | URL to a tracking issue. |

**Expiry semantics (precise):**

- Comparison is `review_by` vs. the audit run's UTC date.
- `review_by > today` → entry is **active** → contributes one `--ignore-vuln <id>`.
- `review_by <= today` → entry is **expired** → contributes **no** flag (CVE returns to the audit)
  **and** the action records it in an `expired_acceptances` output and **exits non-zero** with a
  clear message: `Acceptance for <id> expired on <review_by>; re-review required.`
- An empty/missing `accepted:` list is valid (zero suppressions).
- **Maximum acceptance window is advisory** (recommend ≤ 90 days); the schema enforces presence of
  an expiry, not its length. (A hard cap can be added to the validator later if desired.)

**Approval flow (= git audit trail):**

1. A code owner opens a PR that **adds/edits** an entry in `.github/security/audit-allowlist.yml`.
2. CODEOWNERS requires code-owner review for that path (this ADR **adds** the path to CODEOWNERS —
   it is not covered today; see [File-Change Plan](#file-change-plan)).
3. The reviewed, approved, merged PR is the immutable record of *who accepted what, why, and until
   when*. No separate approval system is introduced — the existing
   `require_code_owner_review: true` ruleset rule (confirmed in `adversarial-review.md` C2) is the
   gate.

**Why a single YAML file (not pip-audit's native ignore mechanisms):** pip-audit's
`--ignore-vuln` is per-invocation and has **no expiry concept**; a raw ignore in the workflow
would be a permanent, invisible suppression — precisely the anti-pattern we are guarding against.
A first-class file with mandatory `review_by` gives expiry + provenance + a reviewable diff.

---

### D3 — Non-Blocking Policy

> **OWNER DECISION REQUIRED (resolves PM-003).** The adversarial review found a contradiction: the
> CI draft passed `fail-on-vuln: 'true'` and a draft comment called CI a "hard gate," while D3 says
> non-blocking. The two cannot both be true. Below the policy is framed as a single crisp choice for
> the owner, with a recommendation. **The drafts default to Option A.** Status stays **Proposed**
> until the owner confirms.

#### The choice: A (now) vs B (future)

| | **OPTION A — CI security job is NON-BLOCKING** *(RECOMMENDED, default in drafts)* | **OPTION B — Block only on lockfile-changing PRs that ADD a new vuln** *(future enhancement)* |
|---|---|---|
| **Behavior** | The CI `security` job emits a `::warning::` annotation and **always exits 0** (`fail-on-vuln: 'false'`). It never fails the PR. | The CI job **fails the PR** only when (a) the PR changes `uv.lock`/`pyproject.toml` **and** (b) it introduces a vuln **not** already present on `main`. Pre-existing advisory-DB drift stays non-blocking. |
| **Forcing function** | The scheduled scan's rolling auto-issue (D4) + Dependabot alerts. Detection is loud; the merge is never frozen. | Same rolling issue + Dependabot for drift, **plus** a hard PR block for newly-added vulns. |
| **Matches owner intent** | Owner's stated "don't block development" — pre-existing drift on an unrelated branch never blocks unrelated work (the exact pain in the 4 open Dependabot PRs). | Owner's stated "no new security issues when branches go in" — a branch literally cannot ADD a vulnerability. |
| **Cost / complexity** | **Simplest.** One flag (`fail-on-vuln: 'false'`); no ruleset change; no diff logic. | Needs **diff-against-`main`** logic (resolve `main`'s vuln set, compare) **and** likely a conditional `required_status_checks` ruleset scoped to lockfile-changing PRs — repo-settings work outside this PR. |
| **Risk** | A genuinely-fixable, newly-added CVE could be merged past if the owner ignores the alert. Mitigated by the rolling issue + Dependabot (loud, not silent). | More moving parts (diff logic + ruleset) → more places to get the gate subtly wrong; mis-scoped ruleset could re-freeze drift PRs. |
| **Verdict** | **Adopt now.** | **Track as a follow-up**, not adopted here. |

**Recommendation: adopt Option A now; track Option B as a follow-up enhancement.** Option A is the
default the drafts implement (`fail-on-vuln: 'false'` in `ci.yml.security-job.draft`, warning-only,
green job, green `ci-success`). Option B best captures the "no new security issues when branches go
in" goal but is deferred because it requires diff-against-`main` logic and probable ruleset work; it
should be filed as a tracked GitHub Issue + worktracker entity (H-32) so the intent is not lost.
Should the owner prefer B immediately, the implementation scope expands accordingly and this ADR
returns for re-review.

**Decision (under Option A):** The audit remains **advisory at the platform level**. It is **NOT**
added to any `required_status_checks` ruleset. The merge gate stays exactly what it is today: the
`pull_request` rule with `required_approving_review_count: 1` and `require_code_owner_review: true`
(confirmed in `PR-298-and-ci-rootcause.md` lines 170-176 and `adversarial-review.md` C2 — the
ruleset has `required_status_checks: null`).

**How it is preserved:**

- The composite action changes *what* the `security` job runs, not *whether* `ci-success`
  aggregates it. `ci.yml`'s `ci-success` gate (lines 409-449) already aggregates `security`, but
  because no ruleset requires `ci-success`, a red `security` job does **not** block merge today and
  will not after this change.
- We add **no** new `required_status_checks` entry and recommend the owner does not either.
- The scheduled workflow has no bearing on merges (it is cron/dispatch only).

**Risk tradeoff (explicit, per P-022):**

| Aspect | Benefit of non-blocking | Risk accepted | Compensating control |
|--------|------------------------|----------------|----------------------|
| Merge velocity | Live-advisory-DB drift (e.g., a CVE published overnight) cannot freeze unrelated PRs — exactly the situation in the four open Dependabot PRs where the red was environmental, not caused by the change. | A real, newly-fixable CVE could be merged past because red CI is "just advisory." | The **rolling issue** (D4) assigned to the owner + Dependabot native alerts make the CVE visible and tracked even though it does not block; the audit is *loud*, not *silent*. |
| Human judgment | Code owner decides per-PR whether red is environmental drift or a real regression. | Relies on the owner actually reading the audit. | The meaningful-audit guard (D5) + step summary surface the verdict prominently in every run. |

**The forcing function is alerting, not a block.** If a stronger gate is later desired, the
recommended path is **Option B** above — a *blocking required check only on PRs that change
`uv.lock`/`pyproject.toml` and introduce a new vuln* (so drift-only PRs stay unblocked) — captured
as a tracked future enhancement, **not** adopted here.

---

### D4 — Alerting Design

**Decision:** Two complementary channels.

**(a) One rolling GitHub issue (scheduled workflow only).** When the scheduled scan finds
vulnerabilities (or expired acceptances), it **creates or updates a single** issue titled
`Open transitive CVEs` (a stable title used to find-or-create), assigned to `@geekatron`, labeled
`security`, `dependencies`. Behavior:

- **Find:** search for an existing **open** issue with the exact title (and a marker label, e.g.
  `security-rolling`).
- **If found:** edit its body in place with the latest audit table + run timestamp + link (no new
  issue — "rolling").
- **If not found and there are findings:** create it.
- **If found and the audit is clean:** post a closing comment and **close** it (the next finding
  re-opens or re-creates), so a stale "Open transitive CVEs" issue never lingers after remediation.
- Implementation uses the GitHub API via `gh` (the `gh` CLI is preinstalled on GitHub-hosted
  runners) or `actions/github-script`. The **scheduled** job is granted `issues: write`
  **scoped to that job**; the composite action itself requests no permissions and the `ci.yml`
  job stays `contents: read` (it does not open issues — PR feedback there is the red check itself).

**(b) Dependabot native alerts + security updates (repo settings — verify, do not assume).**

- **Vulnerability alerts** surface CVEs in the dependency graph in the Security tab.
- **Dependabot security updates** are **event-driven** (independent of the `allow: direct`
  version-update policy) and will open fix PRs for vulnerable deps when a fix exists — this is the
  remediation arm that complements the detection arm.
- These are **repo-settings** toggles, not `dependabot.yml` config (the file's D4 note, lines
  87-101, says as much). During investigation, `GET /repos/.../automated-security-fixes` returned
  **404** (possibly a token-permission artifact, possibly disabled). **This ADR cannot verify the
  toggle state from CI; it is flagged for human confirmation** in
  [Open Questions](#open-questions-for-human-verification).

**Why a rolling issue and not one-issue-per-CVE:** at Jerry's scale a single owner-assigned issue
is the lowest-noise forcing function; per-CVE issues duplicate what Dependabot's Security tab
already itemizes. The rolling issue answers one question loudly: *"is the transitive tree clean
right now, yes/no, and if no, what?"*

---

### D5 — Safety-Check Fix

**Decision:** Replace the `LINE_COUNT >= 1` guard (`security-scan.yml` lines 84-88) with a
**meaningful-audit guard** that the composite action performs. The audit is considered to have
*genuinely run* only if **both**:

1. The captured output contains a **recognizable verdict** — either the clean sentinel
   `No known vulnerabilities found` **or** a vulnerability table / `Found N known vulnerabilities`
   line; **and**
2. The audit covered a **non-trivial number of packages** — i.e., the audited-package count is at
   or above a small floor (recommended floor: **20**; Jerry resolves well over 100 packages, so a
   count in the single digits means the audit looked at almost nothing — the exact Scan B failure
   signature, where only the unauditable `jerry` package was "seen").

If neither verdict sentinel is present, **or** the audited-package count is below the floor, the
action exits non-zero with `::error::audit did not run meaningfully` — converting today's silent
false-green into a loud failure.

**How the package count is obtained reliably:** the action audits the **exported requirements
file** (the D1 contract guarantees `--requirement` is always passed — see
[Responsibility Breakdown](#composite-action-responsibility-breakdown)), and derives the floor
check from the requirements line count and/or pip-audit's machine-readable output
(`--format=json` / number of audited dependencies). Auditing the requirements file is *also* what
structurally prevents the "only `jerry` is seen" failure in the first place; the floor check is the
**belt-and-suspenders** assertion that the structural fix stayed in place.

**Why both conditions:** condition (1) alone is still spoofable by an empty audit that prints a
clean sentinel; condition (2) alone could pass on a malformed run. Requiring a recognizable
verdict **over a real package set** is the assertion that a *meaningful* audit occurred (C-5).

---

### Composite Action Responsibility Breakdown

`.github/actions/security-audit/action.yml` — `runs.using: "composite"`. It assumes the caller has
already run `actions/checkout`, `astral-sh/setup-uv`, and `uv python install`.

**Inputs:**

| Input | Default | Purpose |
|-------|---------|---------|
| `allowlist-path` | `.github/security/audit-allowlist.yml` | Location of the accept-list. |
| `min-audited-packages` | `20` | D5 floor for the meaningful-audit guard. |
| `extras` | `--all-extras` | Passed to `uv export` so the audited set matches `ci.yml` today. |
| `uv-sync` | `true` | Whether the action runs `uv sync --frozen` (callers that already synced can set `false`). |

**Outputs:**

| Output | Purpose |
|--------|---------|
| `result` | `clean` \| `vulnerable` \| `error` (drives the scheduled workflow's issue logic). |
| `report` | Path to the captured human-readable audit output (for step summary / issue body). |
| `vuln-count` | Number of vulnerabilities found (excluding active suppressions). |
| `expired-acceptances` | Newline list of accept-list `id`s whose `review_by` has passed. |

**Step contract (responsibilities, in order):**

1. **Sync** (if `uv-sync == true`): `uv sync --frozen`.
2. **Export** the canonical requirements set:
   `uv export --no-hashes --frozen ${extras} --no-emit-project > <tmp>/requirements.txt`
   (this is the single canonical line both consumers now share — eliminating the Scan A/Scan B
   divergence).
3. **Parse accept-list** → split into **active** (`review_by` in future) and **expired**
   (`review_by <= today`); build the `--ignore-vuln` flag list from **active** only; collect
   `expired` into `expired-acceptances`.
4. **Audit:** `uv run pip-audit --requirement <tmp>/requirements.txt --strict --desc <ignore-flags> [--format json for counting]`. Capture stdout+stderr to `report`.
5. **Meaningful-audit guard (D5):** assert a recognizable verdict AND audited-package count
   `>= min-audited-packages`; else set `result=error` and fail.
6. **Expiry guard (D2):** if `expired-acceptances` is non-empty, fail with the per-id expiry
   message (the CVEs they used to hide are, by construction, now back in the audit set anyway).
7. **Emit outputs** + write a `$GITHUB_STEP_SUMMARY` block (clean sentinel or vuln table).

**What stays in the *caller*, not the action:**

- `ci.yml`: the **banned-YAML-API check** (lines 91-106) remains a sibling step in the `security`
  job — out of scope for a dependency-audit action.
- `security-scan.yml`: the **find-or-update rolling issue** logic (D4) stays in the scheduled
  workflow because it needs `issues: write` and is alerting policy, not audit logic. The action
  returns `result`/`report`/`vuln-count`; the workflow decides what to do with them.

This split keeps the action **single-responsibility** (audit + accept-list + guard) and leaves
**policy** (blocking? alert how?) to each caller — which is what lets D3 (non-blocking) and D4
(issue) differ per consumer without duplicating audit logic.

---

## Verification Strategy (Red/Green)

**Test-first, using today's live 9 CVEs as the fixture.** The 5 vulnerable packages are currently
in `uv.lock` (verified), so the environment is already a natural "red" fixture — no synthetic
vuln injection needed.

### Phase R (RED — prove the fixed detector detects)

1. On the **scanner-fix branch** (composite action + rewired `security-scan.yml`, accept-list file
   present but with an **empty** `accepted:` list), run the scheduled workflow via
   `workflow_dispatch`.
2. **Expected:** `result=vulnerable`, `vuln-count == 9` (mako, urllib3, msgpack, pydantic-settings,
   pip), the meaningful-audit guard **passes** (it audited the full tree, ≥ floor packages), the
   job exits non-zero, and the rolling issue `Open transitive CVEs` is **created/updated**.
3. This is the proof the **previously-false-green** scan now correctly goes RED on the same
   lockfile that fooled it before. **The `ci.yml` `security` job on this PR will also be legitimately
   RED** for the same reason — this is expected and acceptable per D3 (non-blocking; code-owner
   review is the gate). Reviewers MUST NOT treat that red as a reason to reject the scanner-fix PR.

### Phase G (GREEN — prove the fix + detector together)

4. Land the **separate dependency-bump PR** (mako≥1.3.12, urllib3≥2.7.0, msgpack≥1.2.1,
   pydantic-settings≥2.14.2, pip≥26.1.2) — the remediation already recommended in
   `RECOMMENDATION.md` (Post-Merge Action #2).
5. Re-run the scheduled workflow (and `ci.yml`).
6. **Expected:** `result=clean`, clean sentinel present, meaningful-audit guard **passes**, exit 0,
   rolling issue **closed** with a comment.

### Phase A (ACCEPT-LIST behavior — prove suppression + expiry)

7. **Active-suppression test:** temporarily add one of the 9 CVE ids to the accept-list with
   `review_by` in the **future**; re-run before the bumps land. **Expected:** that vuln is excluded
   from `vuln-count`, audit reflects the suppression (e.g., 8 instead of 9), guard still passes.
8. **Expiry test:** set that same entry's `review_by` to a **past** date; re-run. **Expected:** the
   vuln **resurfaces** (back to 9), `expired-acceptances` lists the id, and the expiry guard
   **fails** with `Acceptance for <id> expired on <date>; re-review required.`

### Phase S (SAFETY-CHECK regression — prove the guard can't be fooled)

9. **Neutered-audit test (negative):** in a throwaway branch, simulate the old failure mode
   (drop `--requirement` / point at an empty requirements file) and confirm the meaningful-audit
   guard now **fails** (`audited-package count < floor`) instead of passing green. This proves D5
   closes the exact hole that produced the original false green.

**Sequencing note (explicit, per P-022):** Phase R necessarily shows red CI on the scanner-fix PR
because the lockfile is still vulnerable; green only arrives after Phase G's dependency bumps. The
scanner-fix PR and the dependency-bump PR are **separate** PRs; the scanner-fix is correct even
while its own CI is red.

---

## Consequences

### Positive

- **Drift eliminated:** one composite action = one canonical `--requirement`-based invocation; the
  Scan A/Scan B contradiction cannot recur silently (any future neuter is caught by D5 + red/green).
- **The dark detector lights up:** the scheduled scan becomes a real compensating control for the
  `allow: direct` transitive gap, as originally intended.
- **Auditable, time-boxed acceptances:** un-fixable CVEs can be accepted *with* provenance and a
  forced re-review date; nothing is suppressed forever or invisibly.
- **Loud but non-blocking:** velocity preserved (drift doesn't freeze unrelated PRs) while the
  owner is actively alerted via a single rolling issue + Dependabot.
- **Least privilege preserved:** audit logic stays `contents: read`; only the scheduled issue step
  gets `issues: write`.

### Negative / costs

- **New suppression surface:** the accept-list is a thing that *can* hide a CVE. Mitigated by
  exact-id-only matching, mandatory expiry with auto-resurface, and CODEOWNERS review — but it is a
  real surface that must be reviewed with care (captured in the threat model).
- **More moving parts:** a composite action + a YAML schema + issue-management logic is more than
  two copy-pasted `run:` blocks. The DRY payoff and drift-resistance justify it for a
  security-critical control.
- **Non-blocking residual:** a genuinely-fixable CVE can still be merged past if the owner ignores
  the alert. This is an accepted tradeoff (D3) with the rolling issue as the mitigation.
- **Settings dependency:** the Dependabot native arm depends on repo-settings toggles this ADR
  cannot verify from CI (404 during testing) — a human must confirm.

### Neutral

- `ci.yml`'s `security` job keeps its banned-YAML check unchanged; only its audit steps are
  swapped for the composite action call.
- The 3-month (recommended) acceptance window is a policy default, tunable later.

---

## File-Change Plan

> **Plan only — no edits performed by this ADR.** Every file the implementation PR will create or
> change, with the reason. Live `.github/` files are listed as *to-be-changed*, not changed here.

### Files to CREATE

| Path | Type | Purpose |
|------|------|---------|
| `.github/actions/security-audit/action.yml` | New composite action | Canonical audit logic (D1): sync → export `--requirement` → parse accept-list → `pip-audit` w/ `--ignore-vuln` → meaningful-audit guard (D5) → expiry guard (D2) → outputs + step summary. |
| `.github/security/audit-allowlist.yml` | New data file | Owner accept-list (D2). Ships with `version: 1` and an **empty** `accepted: []` (no suppressions on day one). |
| `.github/security/README.md` | New doc (optional but recommended) | Explains the accept-list schema, expiry semantics, and the "edit = code-owner PR" approval flow, so future maintainers don't reinvent it. |

### Files to CHANGE

| Path | Change | Reason |
|------|--------|--------|
| `.github/workflows/ci.yml` | In the `security` job, replace the three audit steps (lines 82-89: `uv sync` / `uv export` / `pip-audit`) with `uses: ./.github/actions/security-audit`. **Keep** the banned-YAML-API check (lines 91-106) as a sibling step. **Keep** `permissions: contents: read`. | DRY (D1); preserves non-blocking (D3) and the YAML check. |
| `.github/workflows/security-scan.yml` | Replace the `Run pip-audit` step (lines 62-74) and the broken `Verify pip-audit executed` guard (lines 77-89) with: `uses: ./.github/actions/security-audit`, then a `find-or-update rolling issue` step using the action's `result`/`report` outputs (D4). Add job-scoped `permissions: { contents: read, issues: write }`. | Fixes the false-green (D5) and adds alerting (D4) while sharing one audit logic (D1). |
| `.github/CODEOWNERS` | Add the **valid gitignore-style** entries `/.github/actions/   @geekatron` and `/.github/security/  @geekatron` — **no backslash escaping** (the leading `\.` form in Rev 1 was invalid and would be silently ignored by GitHub; see [PM-010 resolution](#pm-010--corrected-codeowners-guidance)). Currently **uncovered** — verified: CODEOWNERS today covers only `.github/workflows/`, `.github/dependabot.yml`, `.github/CODEOWNERS`, `.pre-commit-config.yaml`, `.context/rules/`, `docs/governance/`. | Makes the D2 approval flow real — accept-list edits and audit-action edits require code-owner review. **Without these entries the accept-list approval guarantee does not hold** (an `--ignore-vuln` suppression could be merged with no code-owner review). |
| `CHANGELOG.md` | Add an `[Unreleased]` entry (the implementation PR will be subject to `ci.yml`'s `changelog-check`, lines 354-402). | Repo policy. |
| `.github/dependabot.yml` | **No functional change.** Optionally update the comment block (lines 66-83) to point at the new composite action as the shared detector. | Keep docs accurate; `allow: direct` policy is unchanged. |

### Repo-SETTINGS actions (not files — human, per D4)

| Action | Where |
|--------|-------|
| Confirm **Dependabot vulnerability alerts** enabled | Settings → Code security |
| Confirm **Dependabot security updates** enabled (the 404 from `GET .../automated-security-fixes` may be permissions, not disabled state) | Settings → Code security |

### Governance artifacts (separate from the security PR, per H-32)

| Item | Note |
|------|------|
| GitHub Issue + worktracker entity for the **scanner-fix** implementation | H-32 parity for jerry-repo work. |
| GitHub Issue + worktracker entity for the **dependency-bump** PR (the Phase-G remediation) | Already recommended in `RECOMMENDATION.md`; needed for Phase G green. |

---

## Alternatives Considered

| Alternative | Why rejected |
|-------------|--------------|
| **Reusable workflow (`workflow_call`)** instead of composite action | Runs as a separate job; cannot sit inside the existing `security` job alongside the banned-YAML check without splitting it; heavier given both callers already checkout + set up uv. (See D1 table.) |
| **Shared script** (`scripts/security_audit.*`) | No declared input/output contract → reintroduces the exact contract-free coupling that allowed Scan B to drift. (See D1 table.) |
| **Just fix `security-scan.yml` in place** (add `--requirement`) without DRY | Fixes today's symptom but leaves two copies of the logic → guaranteed future re-drift. Violates owner decision C-1. |
| **Make the audit a required status check** (blocking) | Would freeze unrelated PRs on live-advisory-DB drift (the precise pain in the 4 open Dependabot PRs). Violates owner decision C-3. Kept as a *future, narrowly-scoped* option (block only on `uv.lock`/`pyproject.toml` changes). |
| **Permanent `--ignore-vuln` in the workflow** for un-fixable CVEs | No expiry, no provenance, invisible suppression — the anti-pattern the accept-list exists to prevent. Violates C-2. |
| **One issue per CVE** | Higher noise; duplicates Dependabot's Security-tab itemization. The rolling single issue is the lowest-noise forcing function. |

---

## NIST CSF 2.0 Mapping

| CSF Function | Control in this design |
|--------------|------------------------|
| **Identify (ID.RA)** | pip-audit over the full exported requirements set = continuous identification of known transitive vulnerabilities. |
| **Protect (PR.PS)** | CODEOWNERS-gated, schema-validated accept-list ensures suppressions are deliberate, justified, and time-boxed. |
| **Detect (DE.CM)** | Scheduled daily scan (now meaningful) + meaningful-audit guard = the compensating detector for the `allow: direct` transitive gap; D5 detects a *dark detector*. |
| **Respond (RS.MA)** | Rolling owner-assigned issue + Dependabot security-update PRs = a defined response path (alert → triage → bump-or-accept). |
| **Recover (RC.RP)** | Expiry auto-resurface forces periodic re-review so accepted risk cannot silently become permanent; green/clean closes the rolling issue. |

---

## Open Questions for Human Verification

> Per P-022, these cannot be confirmed from CI/design and require the owner.

1. **Dependabot security updates / vulnerability alerts toggle state.** `GET /repos/geekatron/jerry/automated-security-fixes` returned **404** during testing — confirm in Settings → Code security whether this is a permissions artifact or the feature is disabled. The transitive-CVE *remediation* arm (D4b) depends on it.
2. **Acceptance window length.** *Resolved by PM-006:* the cap is now **enforced in code** (input `max-acceptance-days`, default 90, owner-tunable). Confirm the default value of 90 days, or set a preferred ceiling.
3. **`min-audited-packages` floor value.** Recommended `20` (Jerry resolves 100+). Confirm or tune.
4. **Issue assignee/labels.** Design assigns `@geekatron`, labels `security` + `dependencies` + `security-rolling`. Confirm the `security-rolling` marker label may be created.
5. **Blocking policy — A vs B (resolves PM-003).** Confirm **Option A** (CI security job non-blocking; the drafts' default) per the [D3 owner-decision table](#the-choice-a-now-vs-b-future), with **Option B** (block only on lockfile-changing PRs that add a new vuln) tracked as a follow-up — or elect B now (expands implementation scope, ADR returns for re-review).

---

## References

| Source | What it establishes |
|--------|---------------------|
| `.github/workflows/ci.yml` (lines 68-106, 409-449) | Scan A correct invocation; `ci-success` aggregator; banned-YAML check to preserve. |
| `.github/workflows/security-scan.yml` (lines 62-89) | Scan B false-green invocation + fooled line-count guard. |
| `.github/dependabot.yml` (lines 66-83, 201-202) | `allow: direct` transitive policy; scheduled scan named as the compensating detector. |
| `.github/CODEOWNERS` | Current coverage (workflows, dependabot, pre-commit, rules, governance) — **does not** cover `.github/actions/` or `.github/security/` today. |
| `uv.lock` (read 2026-06-22) | mako 1.3.10, urllib3 2.6.3, msgpack 1.1.2, pydantic-settings 2.13.1, pip 26.0 present (the red fixture); `pip-audit>=2.10.0`. |
| `projects/PROJ-024-tactical-work/research/dependabot-merge-analysis-20260622/RECOMMENDATION.md` | Consolidated finding; Post-Merge Action #2 (CVE-remediation PR) and #3 (scheduled-scan blind spot). |
| `.../PR-298-and-ci-rootcause.md` (E4, lines 161-176, 220) | Mechanism of the false green; ruleset has no required status checks. |
| `.../adversarial-review.md` (C2, C3, C5) | Code-owner review is the real gate; red is advisory-DB drift; #300 fixes none of the 5 packages. |
| `research/security-scan-hardening-20260622/adversarial-review.md` (PM-001..PM-013) | S-004 Pre-Mortem + S-002 Devil's Advocate review driving Revision 2; PM-001..PM-010 resolved in the [Revision 2 section](#revision-2--adversarial-findings-resolved). |
| `.../PR-300-uv-group.md` | The uv-minor-patch group does not bump any of the 5 flagged packages. |
| pip-audit README (pypa/pip-audit) | `--ignore-vuln` is repeatable and alias-aware (GHSA/CVE/PYSEC); `--strict` fails only on dependency *collection* failure; exit 0 = clean, 1 = vulns found. |
| pip-audit PyPI / GitHub | `--ignore-vuln` available since 2.3.0. |

### External sources

- [pip-audit · PyPI](https://pypi.org/project/pip-audit/)
- [pypa/pip-audit · GitHub](https://github.com/pypa/pip-audit)
- [pip-audit README (raw)](https://raw.githubusercontent.com/pypa/pip-audit/main/README.md)

---

*ADR authored by eng-architect. Design-only; no live `.github/` files modified. Criticality C3 (AE-005). All claims cite files read on 2026-06-22 in `geekatron/jerry-wt/feat/proj-024-tactical-work-5`.*

*Revision 2 (2026-06-22): incorporated adversarial findings PM-001..PM-010 (see [Revision 2 — Adversarial Findings Resolved](#revision-2--adversarial-findings-resolved)); added the cardinal fail-closed-on-every-error-path binding constraint; corrected PM-010 CODEOWNERS guidance to valid gitignore-style syntax; reframed D3 as an owner A-vs-B policy choice (recommend A). Code fixes applied in parallel by eng-devsecops in `proposal/` drafts. Status remains Proposed pending owner approval.*
