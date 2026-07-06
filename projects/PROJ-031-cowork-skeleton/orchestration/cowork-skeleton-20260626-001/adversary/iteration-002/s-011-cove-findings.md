# Strategy Execution Report: Chain-of-Verification (S-011)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy metadata and blindness declaration |
| [Findings Summary](#findings-summary) | All CV findings at a glance |
| [Claim Inventory](#claim-inventory) | CL-NNN extracted claims with verification questions |
| [Detailed Findings](#detailed-findings) | CV-001 through CV-006 with evidence and analysis |
| [Execution Statistics](#execution-statistics) | Counts, verification rate, scoring impact |

---

## Execution Context

- **Strategy:** S-011 (Chain-of-Verification)
- **Finding Prefix:** CV-NNN
- **Template:** `.context/templates/adversarial/s-011-cove.md`
- **Deliverables reviewed:**
  - `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (iteration 2)
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` (iteration 2)
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` (iteration 2)
- **Grounding sources read:** `research/phase1-skeleton-ci-research.md` (claim corroboration); `.github/workflows/*.yml` (first-party trigger verification)
- **Executed:** 2026-06-26
- **Iteration:** QG-1 Iteration 2 — Group D (Verify, blind)
- **Blindness declaration:** No files read under `adversary/iteration-001/`, `adversary/iteration-002/` (prior runs), or `_discarded-contaminated-run/`.

---

## Findings Summary

| ID | Severity | Finding | Artifact |
|----|----------|---------|---------|
| [CV-001](#cv-001-pre-publication-integrity-gate-has-no-backing-req-xxx) | Major | Pre-publication integrity gate (post-push SHA equality check) is a named required control in ADR-001/ADR-002 but has no backing REQ-xxx | ADR-001 §Tamper-Evidence; ADR-002 §Branch-Protection Posture |
| [CV-002](#cv-002-tag-name-sanitization-security-control-has-no-backing-req-xxx) | Major | Tag-name sanitization against `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` (ADR-001 RT-04 security control) has no backing REQ-xxx | ADR-001 §Regeneration Commit Determinism |
| [CV-003](#cv-003-r-001-three-dimensional-gate-verifies-proxies-not-actual-cowork-installability) | Major | R-001 three-dimensional gate verifies measurement proxies only; no acceptance criterion tests actual CoWork installation | REQ-034; REQ-001 AC; STK-001 |
| [CV-004](#cv-004-staleness-check-compares-forgeable-trailer-text) | Minor | NFR-006 staleness check compares a forgeable `Source-Commit:` trailer (commit message text) rather than a structural git property; bypassable by a targeted direct-push | NFR-006 AC |
| [CV-005](#cv-005-idempotency-proof-pure-function-of-t-is-imprecise-for-lightweight-tags) | Minor | ADR-001 idempotency proof states "`regenerate(T)` is a pure function of T" without stating the required implicit assumption: tag `T` must be immutable (not deleted-and-recreated) | ADR-001 §Regeneration Commit Determinism |
| [CV-006](#cv-006-loop-safety-guarantee-2-does-not-enumerate-all-6-workflows) | Minor | ADR-002 loop-safety guarantee #2 names 3 of 6 workflows in the repo; ci.yml, pat-monitor.yml, security-scan.yml are unmentioned; all 6 are independently verified safe, but the argument is incomplete | ADR-002 §Loop-Safety Argument |

---

## Claim Inventory

Claims extracted and verification questions generated per S-011 Step 1–2.

| ID | Claim (exact source) | Claim Type | Source | VQ |
|----|---------------------|------------|--------|----|
| CL-001 | "add a **pre-publication integrity gate** that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable (owned by ADR-002)" | Cross-reference / control existence | ADR-001 §Tamper-Evidence | VQ-001 |
| CL-002 | "**Pre-publication integrity gate (required).** Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>`" | Behavioral claim / control existence | ADR-002 §Branch-Protection Posture | VQ-001 |
| CL-003 | Tag-name sanitization: "Validate the tag against the strict allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and abort (non-zero exit, **no push**) on any non-match" | Control existence (security) | ADR-001 §Tag-name sanitization (RT-04) | VQ-002 |
| CL-004 | "All three dimensions must be within acceptable bounds before any Phase 5 implementation script may execute" — the three dimensions are tracked file count, compressed pack size, and estimated clone time | Behavioral claim / sufficiency | REQ-034 | VQ-003 |
| CL-005 | "`regenerate(T)` is referentially transparent and yields one fixed SHA; re-running `T`... reproduces it exactly" (idempotency proof) | Behavioral claim | ADR-001 §Regeneration Commit Determinism | VQ-004 |
| CL-006 | "Listener shape: `version-bump.yml` and `docs.yml` listen on **`main` only**, and `release.yml` listens on **`push: tags: 'v*'` only**; a push to `cowork-skeleton` (neither `main` nor a tag) is invisible to all three watched workflows named in REQ-014" | Behavioral claim / factual | ADR-002 §Loop-Safety Argument | VQ-005 |
| CL-007 | NFR-006: "It SHALL compare the `Source-Commit:` trailer in `git log -1 cowork-skeleton` to the full SHA of the latest `v*` tag on `main`" | Behavioral claim / mechanism | NFR-006 | VQ-006 |
| CL-008 | "The `Source-Commit:` trailer is... an in-place modification of the published branch — a malicious direct push, a corrupted regeneration — changes the tip SHA away from the deterministically expected value and is **detectable**" | Behavioral claim | ADR-001 §Tamper-Evidence | VQ-007 |
| CL-009 | "`projects/` accounts for 4,600 of 6,344 tracked files (72%)" | Quoted value | REQ-002 rationale; ADR-001 L0 | VQ-008 |
| CL-010 | "targeting approximately 1,744 tracked files" / "~1,745 including the sentinel stub" | Quoted value | REQ-002; REQ-001 AC; L0 Exec Summary | VQ-009 |

**Verification questions:**

| ID | Question | Linked Claim |
|----|----------|--------------|
| VQ-001 | Which REQ-xxx in phase1-requirements.md requires implementing a post-push SHA equality check asserting the live cowork-skeleton tip SHA equals the independently recomputed deterministic SHA? | CL-001, CL-002 |
| VQ-002 | Which REQ-xxx in phase1-requirements.md requires the skeleton generation script to validate the tag against an allow-list regex and to use safe environment-variable passing instead of direct `${{ github.ref_name }}` interpolation? | CL-003 |
| VQ-003 | Does any REQ-xxx or STK acceptance criterion require a successful actual CoWork installation (not a proxy measurement) as evidence that STK-001 is satisfied? | CL-004 |
| VQ-004 | Does the idempotency proof state the assumption that tag T must resolve to the same commit SHA on every execution (i.e., tag immutability)? | CL-005 |
| VQ-005 | Do all GitHub Actions workflow files in the repository avoid triggering on a push to the `cowork-skeleton` branch? | CL-006 |
| VQ-006 | Is the `Source-Commit:` trailer value in a commit message a forgeable (writable by any actor who can push to the branch) value or a structural git property? | CL-007 |
| VQ-007 | If a direct-push attacker writes a commit to cowork-skeleton with a `Source-Commit:` trailer matching the latest tag SHA, does the tamper-detection described in ADR-001 §Tamper-Evidence detect it? | CL-008 |
| VQ-008 | Does the research corroborate the 4,600-of-6,344 file count claim? | CL-009 |
| VQ-009 | Is the "approximately 1,744 tracked files" figure consistent across deliverables, or does it conflict with the "~1,745 including sentinel" claim? | CL-010 |

---

## Independent Verification Results

### VQ-001: Post-push SHA check backed by requirements?

**Source examined:** `phase1-requirements.md` — complete requirements scan, WS-1 through WS-5 and all NFRs.

**Independent answer:** REQ-022 requires "a pre-push equivalence check" — specifically, `git diff v{N}..cowork-skeleton -- ':!projects/'` BEFORE the force-push, failing the job if diff is non-empty. This is a **tree content diff**, not a SHA equality check. No REQ-xxx requires: (a) computing the expected deterministic SHA after pushing, (b) asserting `git rev-parse cowork-skeleton == <expected SHA>`, or (c) blocking publication if they differ. The "pre-publication integrity gate" described in ADR-001 §Tamper-Evidence (operationalization bullet) and ADR-002 §Branch-Protection Posture (as a "required" control) is absent from requirements.

**Result:** MATERIAL DISCREPANCY — ADR-002 calls this control "required" but no requirement mandates it.

---

### VQ-002: Tag-name sanitization backed by requirements?

**Source examined:** `phase1-requirements.md` — WS-2 (CI), WS-3 (Security), and all REQ-xxx texts scanned.

**Independent answer:** REQ-011 describes the workflow trigger and `inputs.target_tag` parameter. REQ-019 requires no secret leakage. REQ-020 requires least-privilege permissions. REQ-022 requires a pre-push equivalence check. None of these require: (a) validating `github.ref_name` against `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`, (b) aborting on non-match, or (c) using safe environment-variable passing instead of direct `${{ github.ref_name }}` string interpolation. The security control RT-04 documented in ADR-001 §Tag-name sanitization has no corresponding REQ-xxx.

**Result:** MATERIAL DISCREPANCY — security control in ADR-001 has no backing requirement.

---

### VQ-003: Actual CoWork installation tested anywhere in requirements?

**Source examined:** `phase1-requirements.md` — all acceptance criteria for WS-1 through WS-5, all NFR acceptance criteria.

**Independent answer:**
- REQ-001 AC: "`git ls-files | wc -l`... returns a value less than 5,000" — proxy measurement.
- REQ-034 AC: records `git ls-files | wc -l`, `git count-objects -vH` size-pack MB, and estimated clone time — three proxy measurements.
- No acceptance criterion anywhere says: "install Jerry via `claude plugin marketplace add geekatron/jerry@cowork-skeleton` in a running CoWork session and confirm success."
- STK-001 need ("Jerry must install in Claude CoWork without triggering the plugin-load file-count limit") has no direct, non-proxy acceptance test.
- R-001 explicitly acknowledges: "the ~5,000 ceiling is a CoWork/Claude-Desktop runtime constraint... still warrants empirical confirmation."

**Dimension (b)** of REQ-034 (compressed pack size) has no documented threshold — only the 120-second timeout is referenced. The pack size measurement has no explicit PASS/FAIL criterion against CoWork behavior.

**Result:** MATERIAL DISCREPANCY — the deliverables do not misstate the limitation (R-001 is honestly disclosed), but REQ-034's sufficiency claim ("all three dimensions must pass before Phase 5") implies the gate establishes readiness. It does not: the gate passes even if CoWork still refuses to install (different limit metric or threshold than assumed).

---

### VQ-004: Idempotency proof states tag immutability assumption?

**Source examined:** ADR-001 §Regeneration Commit Determinism, idempotency proof sketch.

**Independent answer:** The proof sketch reads: "Given tag `T` resolving to source commit `S` with committer date `D`, the regenerated commit's preimage `(tree, parent=S, identity, author_date=D, committer_date=D, message(T,S))` is a pure function of `T`. Therefore `regenerate(T)` is referentially transparent." No caveat is stated about tag mutability. The proof conflates "pure function of T" (the tag name string) with "pure function of (T→S)" (the tag-name-to-commit-SHA resolution). A lightweight git tag is mutable: deleting and recreating `T` to point to a different commit `S'` would make `regenerate(T)` produce a different SHA, contradicting "referentially transparent." The proof holds only if T is treated as immutable (i.e., the (tag-name, target-SHA) pair, not just the tag-name string).

For the CI trigger path (push tag event), the tag SHA is captured at trigger time — this is safe. For the `workflow_dispatch` path with `inputs.target_tag`, the tag is re-resolved at runtime — if the tag has been moved, the proof breaks.

**Result:** MINOR DISCREPANCY — the proof is sound for the CI trigger path; the `workflow_dispatch` re-resolution edge case with mutable tags is an unstated boundary condition.

---

### VQ-005: All 6 workflows safe against cowork-skeleton push?

**Source examined:** All six `.github/workflows/*.yml` files, specifically their `on:` trigger blocks.

**Independent answer (first-party verification):**

| Workflow | `on:` trigger | Triggered by push to cowork-skeleton? |
|----------|--------------|---------------------------------------|
| `ci.yml` | `push: branches: [main, master]` + `pull_request: branches: [main, master, claude/**]` | No |
| `docs.yml` | `push: branches: [main]` + `paths:` filter | No |
| `pat-monitor.yml` | `schedule: cron` + `workflow_dispatch` | No |
| `release.yml` | `push: tags: ['v*']` (verified in research) | No |
| `security-scan.yml` | `schedule: cron` + `workflow_dispatch` | No |
| `version-bump.yml` | `push: branches: [main]` + `workflow_dispatch` | No |

ADR-002 guarantee #2 mentions three workflows by name. The repo contains six. The unmentioned three (ci.yml, pat-monitor.yml, security-scan.yml) are all confirmed safe.

**Result:** MINOR DISCREPANCY — guarantee #2 argument is incomplete (names 3 of 6 workflows; the other 3 are not argued from listener-shape). The claim "invisible to all three watched workflows named in REQ-014" contains a minor error: REQ-014 names FOUR workflows (adding cowork-skeleton.yml, which is addressed by guarantee #1 not guarantee #2). Functionally safe because guarantee #3 (GITHUB_TOKEN) provides categorical coverage for ALL workflows regardless.

---

### VQ-006: Is Source-Commit: trailer forgeable?

**Source examined:** git commit message mechanics; ADR-002 §Branch-Protection Posture; NFR-006.

**Independent answer:** A git commit message is arbitrary UTF-8 text authored by the committer. Any actor who can push a commit to `cowork-skeleton` (currently unprotected per ADR-002) can write any `Source-Commit:` trailer value, including one matching the latest tag SHA. The commit message is not a cryptographically protected field. The tip SHA (`git rev-parse cowork-skeleton`) IS a structural property — it is the SHA-1 of the entire commit object including tree, parent, and metadata — and cannot be forged without matching ALL inputs. NFR-006 compares the forgeable trailer text, not the unforgeable tip SHA.

**Result:** VERIFIED as a MINOR DISCREPANCY — the staleness check uses forgeable text for detection. This is adequate for detecting lazy staleness (CI failure to regenerate) but bypassable by a targeted direct-push attacker.

---

### VQ-007: Does ADR-001 tamper detection catch a direct-push with matching Source-Commit trailer?

**Source examined:** ADR-001 §Tamper-Evidence and Supply-Chain Integrity; ADR-002 §Branch-Protection Posture.

**Independent answer:** ADR-001 §Tamper-Evidence states: "Any in-place modification of the published branch — a malicious direct push, a corrupted regeneration, a man-in-the-middle rewrite — changes the tip SHA away from the deterministically expected value and is **detectable** by anyone who recomputes it."

This is accurate: a direct-push commit (even one with a matching `Source-Commit:` trailer) will have a different tree, different parent, or different identity, producing a different tip SHA. The pre-publication integrity gate (SHA comparison) would detect this. However, per VQ-001's finding, the pre-publication integrity gate has no backing REQ-xxx. NFR-006 (staleness check) would NOT detect a targeted direct-push that spoofs the `Source-Commit:` trailer.

**Result:** VERIFIED claim in ADR-001 (the tip SHA is non-forgeable and tamper-detectable) but the tamper detection mechanism (pre-publication integrity gate) has no backing REQ-xxx (CV-001), meaning the detection described is not required to be implemented.

---

### VQ-008: File count claim corroborated?

**Source examined:** `research/phase1-skeleton-ci-research.md` §Settled facts and L0 §Problem.

**Independent answer:** Research L0 §Settled facts: "strip `projects/` → 1,744 tracked files." Research L0 §Problem: "6,344 tracked files vs CoWork's ~5,000 limit." The 4,600-of-6,344 figure (72%) is consistent: 6,344 − 1,744 = 4,600. The research confirms these numbers were established as settled facts (not re-investigated in this session).

**Result:** VERIFIED — numbers are internally consistent and corroborated by research document.

---

### VQ-009: 1,744 vs 1,745 file count consistency?

**Source examined:** `phase1-requirements.md` L0 Exec Summary, REQ-002 text, REQ-002 AC, ADR-001 L0.

**Independent answer:**
- L0 Exec Summary: "approximately 1,744 tracked files (~1,745 including the `projects/README.md` sentinel stub)" — explicitly distinguishes the two counts.
- REQ-002 text: "targeting approximately 1,744 tracked files" — appears to mean pre-sentinel.
- REQ-002 AC: "`git ls-files projects/` returns only `projects/README.md`; `git ls-files` total is approximately 1,744" — the total count with the sentinel should be approximately 1,745, but AC says 1,744.
- ADR-001 L0: "~1,744 files" — consistent with the rounded pre-sentinel count.

The REQ-002 AC says total `git ls-files` is "approximately 1,744" but the sentinel README.md is included in `git ls-files` output (it is a tracked file). The correct total is ~1,745. The AC would fail by 1 file under strict reading.

**Result:** MINOR DISCREPANCY — REQ-002 AC is off-by-one: states "approximately 1,744" for the total but the sentinel adds 1, making the correct total ~1,745. The L0 Exec Summary correctly states both numbers; the REQ-002 AC did not carry the correction.

---

## Detailed Findings

### CV-001: Pre-publication integrity gate has no backing REQ-xxx

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §Tamper-Evidence; ADR-002 §Branch-Protection Posture; REQ-022 |
| **Strategy Step** | Step 4 — Consistency Check (VQ-001) |

**Evidence:**

ADR-002 §Branch-Protection Posture states: "**Pre-publication integrity gate (required).** Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>` for the release tag."

ADR-001 §Tamper-Evidence operationalization bullet: "add a **pre-publication integrity gate** that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable (owned by ADR-002 §Branch-Protection Posture)."

The closest requirement is REQ-022: "This equivalence check SHALL run as an automated in-workflow step BEFORE the force-push step" — this is a **pre-push tree diff** (content equality), not a **post-push SHA equality** check. REQ-022 AC: "`git diff v{N}..cowork-skeleton -- ':!projects/'` is executed as an automated in-workflow step BEFORE the force-push step."

No REQ-xxx covers: compute expected SHA, assert `git rev-parse cowork-skeleton == expected SHA` after the push, block publication on mismatch.

**Analysis:**

The pre-publication integrity gate and the pre-push diff gate (REQ-022) are distinct controls serving distinct threats:
- REQ-022 (pre-push diff): Detects incorrect generation output BEFORE publishing. Stops a bad push.
- Pre-publication integrity gate (no REQ): Detects direct-push tampering AFTER publishing. Detects unauthorized writes between CI runs.

ADR-002 explicitly labels the integrity gate as "required" and says it "converts 'unprotected' from a write-control gap into a verifiable-integrity property." Without a backing requirement, Phase 5/6 implementers can omit this control without violating any REQ-xxx. Since NFR-006's staleness check uses forgeable text (CV-004), the integrity gate is currently the only mechanism that provides non-forgeable tamper detection — and it has no backing requirement.

**Recommendation:**

Add a REQ-xxx to WS-5 (or WS-3) requiring the CI workflow to compute and assert the expected deterministic SHA after force-pushing cowork-skeleton, before marking the run as publishable. This closes the traceability gap and ensures Phase 5/6 implementers have a formal mandate for the control ADR-002 declares required. Alternatively, publish expected SHAs in GitHub Release notes (as ADR-001 suggests) and add a verification REQ.

---

### CV-002: Tag-name sanitization security control has no backing REQ-xxx

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §Regeneration Commit Determinism §Tag-name sanitization (RT-04); WS-3 Security Requirements |
| **Strategy Step** | Step 4 — Consistency Check (VQ-002) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism states: "**Tag-name sanitization (security — RT-04).** `github.ref_name` is **attacker-influenceable**... The generation script MUST therefore: (1) Validate the tag against the strict allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and abort... on any non-match... (2) Pass it as an environment variable (`TAG="${GITHUB_REF_NAME}"`) consumed only by **quoted** expansions — **never** interpolate `${{ github.ref_name }}` directly into a `run:` shell string."

WS-3 Security Requirements (REQ-019 through REQ-023) cover: secrets in logs (REQ-019), minimal permissions (REQ-020), branch protection posture (REQ-021), pre-push equivalence check (REQ-022), no cowork-skeleton branch trigger (REQ-023). None address tag-name sanitization.

**Analysis:**

Tag-name sanitization is explicitly identified as a security control (RT-04) in ADR-001. `${{ github.ref_name }}` is a GitHub Actions script-injection vector — interpolating it directly into a `run:` shell block allows an attacker controlling the tag name to inject arbitrary shell commands. This is a well-documented GitHub Actions security vulnerability class.

Without a requirement mandating this control, a Phase 5/6 implementer who reads the ADR cursorily or uses a script template with direct interpolation introduces a shell-injection surface. WS-3 (Security Requirements) is the natural home for this requirement — it already covers supply-chain hardening and least-privilege.

**Recommendation:**

Add a REQ-xxx to WS-3 requiring: (a) the generation script validates `GITHUB_REF_NAME` against `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and exits non-zero on non-match; (b) the validated tag is consumed only via a shell variable (not via `${{ github.ref_name }}` direct string expansion in the `run:` block). The REQ-xxx should cite ADR-001 RT-04 as rationale.

---

### CV-003: R-001 three-dimensional gate verifies proxies, not actual CoWork installability

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-034; REQ-001 AC; STK-001; R-001 §Verification Approach |
| **Strategy Step** | Step 4 — Consistency Check (VQ-003) |

**Evidence:**

STK-001: "Jerry must install in Claude CoWork without triggering the plugin-load file-count limit." (The project's primary goal.)

REQ-001 AC: "`git ls-files | wc -l`... returns a value less than 5,000." (Proxy: file count.)

REQ-034 requires three-dimensional verification: (a) tracked file count, (b) compressed pack size in MB, (c) estimated clone time vs 120-second threshold. AC requires "a PASS/FAIL determination for each of the three dimensions."

R-001 §Verification Approach: "the ~5,000 ceiling is a CoWork/Claude-Desktop runtime constraint per the project's settled facts and **still warrants empirical confirmation**."

No acceptance criterion anywhere requires: "execute `claude plugin marketplace add geekatron/jerry@cowork-skeleton` in a running CoWork client and confirm successful plugin installation."

**Analysis:**

The three-dimensional gate in REQ-034 provides three proxy measurements:
- Dimension (a): Tests a file-count assumption that is itself unverified (R-001). If CoWork's limit applies to the local working directory (including `.venv/`, 24,636 files) rather than the clean-clone tree, all three dimensions pass but CoWork still refuses to install.
- Dimension (b): Pack size has no documented CoWork threshold — only the 120-second timeout is referenced. The PASS/FAIL criterion for MB is unspecified in REQ-034 AC.
- Dimension (c): Clone time against 120 seconds is the best-grounded dimension (CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS is documented).

REQ-034's sufficiency claim — "All three dimensions must be within acceptable bounds before any Phase 5 implementation script may execute" — implies the gate establishes Phase 5 readiness. But the gate can PASS while CoWork still fails to install if the underlying assumptions about the limit's mechanism are wrong.

Dimension (b)'s PASS/FAIL threshold is undefined: REQ-034 says "pack size in MB" but its AC does not specify what constitutes a passing MB value — only the 120-second clone-time threshold is explicit. This creates an unverifiable acceptance criterion for dimension (b).

**Recommendation:**

(1) Add a direct-installation acceptance criterion to STK-001 or REQ-001: if CoWork plugin testing capability is available, require it as part of R-001 verification; if not, explicitly document it as out-of-scope with a formal risk acceptance statement. (2) Define the PASS/FAIL threshold for dimension (b) pack size in REQ-034 AC — either in MB against a documented CoWork limit, or as "within the Option B orphan-fallback trigger (250 MB)" from ADR-001.

---

### CV-004: Staleness check compares forgeable trailer text

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NFR-006; ADR-001 §Tamper-Evidence |
| **Strategy Step** | Step 4 — Consistency Check (VQ-006, VQ-007) |

**Evidence:**

NFR-006: "It SHALL compare the `Source-Commit:` trailer in `git log -1 cowork-skeleton` to the full SHA of the latest `v*` tag on `main`."

NFR-006 AC: "manually simulate a staleness condition (e.g., temporarily set `git log -1 cowork-skeleton` to a SHA not matching the latest tag)."

The `Source-Commit:` trailer is text in a commit message. Any actor who can push to the unprotected `cowork-skeleton` branch can write any value in this field, including a value that matches the current latest tag SHA, causing the staleness check to report clean when the branch is tampered.

ADR-001 §Tamper-Evidence provides a non-forgeable alternative: "anyone can recompute the expected SHA and detect an in-place modification" — the tip SHA is non-forgeable. This stronger mechanism is the pre-publication integrity gate (CV-001, no backing REQ-xxx).

**Analysis:**

The staleness check's primary purpose — detecting when CI failed to regenerate the branch after a new release — is adequately served by the trailer text comparison. A lazy-staleness scenario (CI failure to run) would show a mismatched `Source-Commit:` trailer. For this purpose, the trailer text is sufficient and the forgeable nature is not a practical issue.

The forgeable nature becomes a gap only for tamper-detection. Since CV-001 establishes that the stronger non-forgeable mechanism (pre-publication integrity gate) also lacks a backing REQ-xxx, NFR-006's staleness check is currently the only required periodic detection mechanism, and it does not detect targeted direct-push tampering. Both issues should be resolved together.

**Recommendation:**

Either (1) enhance NFR-006 to compare the tip SHA against the independently recomputable expected SHA (if a lightweight recomputation step is feasible in the scheduled workflow), or (2) keep NFR-006 as-is for lazy-staleness detection and ensure CV-001's pre-publication integrity gate is added to requirements for tamper detection. Document that NFR-006 detects lazy staleness, not targeted tampering.

---

### CV-005: Idempotency proof's "pure function of T" is imprecise for lightweight tags

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Regeneration Commit Determinism (idempotency proof sketch) |
| **Strategy Step** | Step 4 — Consistency Check (VQ-004) |

**Evidence:**

ADR-001 idempotency proof sketch: "Given tag `T` resolving to source commit `S` with committer date `D`, the regenerated commit's preimage `(tree, parent=S, identity, author_date=D, committer_date=D, message(T,S))` is a pure function of `T`. Therefore `regenerate(T)` is referentially transparent and yields one fixed SHA."

The commit message template embeds both T (tag name) and S (40-char source SHA). The parent is S. The author/committer dates are copied from S. All inputs are fixed given a stable (T → S) resolution.

A lightweight git tag `T` is mutable: `git tag -d T && git tag T <different-commit>` can make `T` resolve to a different commit `S'`. If a workflow_dispatch is triggered with `inputs.target_tag: T` after the tag has been moved, the script resolves `SRC_SHA="$(git rev-parse "${TAG}^{commit}")"` to `S'`, producing a completely different commit SHA — contradicting "referentially transparent."

**Analysis:**

For the CI tag-push trigger path, the tag SHA is captured at trigger time by GitHub Actions (via `github.sha` or `github.ref`), making tag mutability irrelevant. For the `workflow_dispatch` path with `inputs.target_tag`, the tag is re-resolved at runtime. If the tag has been force-moved between CI runs (non-standard but possible), the idempotency guarantee breaks silently.

The proof is practically sound for the intended use case (production release tags are treated as immutable per convention), but the proof sketch should state this assumption explicitly to be complete.

**Recommendation:**

Add a note to the ADR-001 idempotency proof: "This proof assumes tag `T` is immutable after initial creation (i.e., not deleted-and-recreated pointing to a different commit). For the CI push-tag trigger path this is guaranteed by event capture semantics. For the `workflow_dispatch` path, operators must not re-use tag names on different commits."

---

### CV-006: Loop-safety guarantee #2 does not enumerate all 6 workflows

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-002 §Loop-Safety Argument; REQ-014 |
| **Strategy Step** | Step 4 — Consistency Check (VQ-005) |

**Evidence:**

ADR-002 §Loop-Safety Argument guarantee #2: "`version-bump.yml` and `docs.yml` listen on **`main` only**, and `release.yml` listens on **`push: tags: 'v*'` only**; a push to `cowork-skeleton` (neither `main` nor a tag) is invisible to all three watched workflows named in REQ-014."

REQ-014 names FOUR workflows (not three): "cowork-skeleton.yml, release.yml, version-bump.yml, and `docs.yml`."

The repository contains SIX workflow files: `ci.yml`, `docs.yml`, `pat-monitor.yml`, `release.yml`, `security-scan.yml`, `version-bump.yml`. Guarantee #2 discusses three; `cowork-skeleton.yml` (addressed by guarantee #1) and `ci.yml`, `pat-monitor.yml`, `security-scan.yml` are not discussed.

**First-party verification (independent):**

| Workflow | `on:` trigger (verified by reading file) | Triggers on cowork-skeleton branch push? |
|----------|------------------------------------------|------------------------------------------|
| `ci.yml` | `push: branches: [main, master]` + `pull_request` | No |
| `docs.yml` | `push: branches: [main]` + `paths:` | No |
| `pat-monitor.yml` | `schedule: cron` + `workflow_dispatch` | No |
| `release.yml` | `push: tags: ['v*']` | No |
| `security-scan.yml` | `schedule: cron` + `workflow_dispatch` | No |
| `version-bump.yml` | `push: branches: [main]` + `workflow_dispatch` | No |

All 6 workflows are safe. Guarantee #3 (`GITHUB_TOKEN` non-retrigger) provides categorical safety regardless.

**Analysis:**

The loop-safety argument's guarantee #2 is factually correct for the 3 workflows it covers, but: (a) it says "three watched workflows named in REQ-014" when REQ-014 actually names four; (b) it does not acknowledge ci.yml, pat-monitor.yml, or security-scan.yml as in-scope workflows that were considered. The functional risk is zero because guarantee #3 provides the categorical backstop. The documentation gap could mislead a future reviewer into thinking the listener-shape argument only covers specific known workflows rather than all 6.

**Recommendation:**

Revise ADR-002 guarantee #2 to: (a) correctly state REQ-014 names four workflows (adding cowork-skeleton.yml handled by guarantee #1); (b) note that ci.yml, pat-monitor.yml, and security-scan.yml were checked and confirmed non-triggering on branch pushes; (c) note that guarantee #3 provides categorical safety for any future workflows added. This makes the argument complete and future-proof.

---

## Execution Statistics

- **Total Claims Extracted:** 10 (CL-001 through CL-010)
- **Verification Questions Generated:** 9 (VQ-001 through VQ-009)
- **Protocol Steps Completed:** 5 of 5

| Result | Count | CL IDs |
|--------|-------|--------|
| VERIFIED | 3 | CL-007 (partially), CL-008 (claim true, gate untraced), CL-009 |
| MINOR DISCREPANCY | 3 | CL-005, CL-006, CL-010 |
| MATERIAL DISCREPANCY | 4 | CL-001, CL-002, CL-003, CL-004 |
| UNVERIFIABLE | 0 | — |

**Verification rate:** 3 verified / 10 claims = 30% clean. Material discrepancy rate: 40%.

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| Critical | 0 | — |
| Major | 3 | CV-001, CV-002, CV-003 |
| Minor | 3 | CV-004, CV-005, CV-006 |

**Scoring dimension impact:**

| S-014 Dimension | Weight | Impact | Finding IDs |
|-----------------|--------|--------|-------------|
| Completeness | 0.20 | -0.06 | CV-001 (pre-pub gate missing), CV-002 (tag sanitization missing), CV-003 (no install AC) |
| Internal Consistency | 0.20 | -0.03 | CV-005 (proof imprecision), CV-006 (workflow count) |
| Methodological Rigor | 0.20 | -0.04 | CV-003 (proxy-only verification), CV-004 (forgeable detection) |
| Evidence Quality | 0.15 | -0.02 | CV-003 (dimension (b) threshold unspecified) |
| Actionability | 0.15 | -0.02 | CV-001, CV-002 (untraced controls unclearable without new REQs) |
| Traceability | 0.10 | -0.05 | CV-001 (ADR control without REQ), CV-002 (ADR control without REQ) |

**Overall assessment:** Corrections required for CV-001, CV-002, CV-003 before the deliverable set is complete. The three Major findings represent ADR controls stated as "required" that have no backing requirements — implementers in Phases 5/6 would have no formal mandate to build them.

---

*Generated by: jerry:adv-executor (S-011 Chain-of-Verification)*
*Project: PROJ-031-cowork-skeleton*
*Iteration: QG-1 Iteration 2*
*Date: 2026-06-26*
*Group: D (Verify — blind)*
