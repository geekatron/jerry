# Inversion Report: PROJ-031 Phase 1 Deliverables

**Strategy:** S-013 Inversion Technique
**Deliverable:** phase1-requirements.md, ADR-001-skeleton-derived-branch-strategy.md, ADR-002-ci-token-push-strategy.md
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group E — Decompose)
**H-16 Compliance:** S-003 Steelman confirmed in prior strategy outputs (iteration-001)
**Goals Analyzed:** 6 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and verdict |
| [Step 1: Goal Inventory](#step-1-goal-inventory) | Explicit and implicit goals extracted from deliverables |
| [Step 2: Anti-Goal Inventory](#step-2-anti-goal-inventory) | Inverted goals — what guarantees failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | All explicit and implicit assumptions |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Per-assumption inversion with severity |
| [Findings Summary Table](#findings-summary-table) | All findings at a glance |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and recommendations |
| [Step 5: Mitigations](#step-5-mitigations) | Prioritized mitigation plan |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | S-014 dimension-level impact |

---

## Summary

Inversion analysis of 6 primary goals across 14 mapped assumptions surfaced 8 vulnerable assumptions:
2 Critical, 4 Major, and 2 Minor. The two Critical findings expose a structural supply-chain gap:
(1) the unverified CoWork limit has more dimensions than R-001 acknowledges — specifically, the
`fetch-depth: 0` strategy carries full git history and could trigger a size- or clone-time-based
limit even if the file count is 1,744; (2) the combination of an unprotected branch and a
branch-name install command (`@cowork-skeleton`) means any write-access actor can push directly
to `cowork-skeleton` and every CoWork user receives that content immediately with no automatic
pre-publication gate. The 4 Major findings address: missing file-count margin trajectory
monitoring, absent staleness detection, symlink validation in the wrong environment (CI, not the
CoWork plugin cache), and no ongoing end-to-end CoWork install test. Verdict: ACCEPT with
Critical mitigations required before proceeding.

---

## Step 1: Goal Inventory

Goals extracted from the three deliverables. Implicit goals are inferred from context.

| # | Goal | Type | Source |
|---|------|------|--------|
| G-1 | `cowork-skeleton` tracked file count < 5,000 on a clean clone — CoWork plugin installation succeeds | Explicit | REQ-001, REQ-006, ADR-001 Context |
| G-2 | Skeleton auto-syncs with `main` within one CI workflow run of every `v*` tag push — no manual surgery | Explicit | NFR-003, REQ-011, STK-002 |
| G-3 | Fresh CoWork install is immediately usable — H-04 bootstrap and SessionStart hook function from session 1 | Explicit | REQ-004, REQ-005, REQ-009, REQ-010, STK-003 |
| G-4 | CI automation is secure — no secret leakage, least-privilege tokens, supply-chain integrity | Explicit | REQ-012, REQ-017, REQ-019–REQ-023, STK-004, ADR-002 |
| G-5 | Generation is deterministic and idempotent — same `v*` tag input → same commit SHA output | Explicit | REQ-003, NFR-001, NFR-002, ADR-001 Regeneration Section |
| G-6 | System is maintainable long-term — future developers understand constraints and detect regressions | Implicit | ADR-001 L2 ¶5, ADR-002 Consequences Neutral, REQ-016 |

---

## Step 2: Anti-Goal Inventory

For each goal: "What would guarantee failure?"

| Anti-Goal | Inverted From | Key Enabling Condition | Addressed? |
|-----------|--------------|------------------------|------------|
| AG-1 | G-1 | Let retained directories grow unchecked until the count silently crosses 5,000 between releases | Partially — REQ-006 hard-fails at 5,000 but no warning below that |
| AG-2a | G-2 | Arrange for CI to fail silently so the skeleton stays stale indefinitely | No — no external staleness monitor |
| AG-2b | G-2 | CoWork limit is not file-count-based — stripping projects/ has no effect regardless of CI success | Partially — R-001 raises binary concern; non-file-count limit dimensions not addressed |
| AG-3a | G-3 | Validate symlinks in CI but not in the CoWork plugin cache runtime where they actually resolve | No — REQ-009 tests CI environment only |
| AG-3b | G-3 | Never re-test actual CoWork installation after the one-time pre-Phase-5 empirical check | No — no periodic install test required |
| AG-4 | G-4 | Push malicious content directly to the unprotected `cowork-skeleton` branch; CoWork users receive it immediately because they install via branch name | No — REQ-021 intentionally leaves branch unprotected with no automatic integrity gate on direct pushes |
| AG-5 | G-5 | Edit `projects/README.md` stub to include a timestamp or version string in a future maintenance cycle | Partially — warned in ADR-001 risk table but not a formal requirement |
| AG-6 | G-6 | Carry no trajectory data on file count, clone weight, or installed-version sync across releases so maintainers notice regressions only after they cause failures | No — no release-over-release monitoring requirement |

---

## Step 3: Assumption Map

| ID | Assumption | Type | Confidence | Validated? | Consequence of Failure |
|----|-----------|------|-----------|------------|------------------------|
| A-01 | CoWork's ~5,000-file limit is a **file count** limit on a clean-clone working tree, not a size, object-count, or clone-time limit | Technical | Low | No (R-001 open) | Entire branch-stripping strategy fails; no fix without scope pivot |
| A-02 | `fetch-depth: 0` clone of `cowork-skeleton` (carrying full `main` history) fits within CoWork's 120-second git timeout on user hardware | Technical | Medium | No | Install times out; users cannot install on slow networks |
| A-03 | Relative symlinks `.claude/rules → ../.context/rules` and `.claude/patterns` resolve correctly in CoWork's plugin cache directory (`~/.claude/plugins/cache`) | Technical | Medium | No | Framework rules silently absent in installed plugin; all Jerry behavior breaks |
| A-04 | All 7 verified plugin directories contain functionally complete contents (not just exist) after projects/ is stripped | Technical | High | No | Plugin surface partially missing; silent capability gaps |
| A-05 | `projects/README.md` stub will remain static content with no generated timestamps or version strings in perpetuity | Technical | Medium | No | Bit-identical idempotency breaks on first edit; tamper detection fails |
| A-06 | The cowork-skeleton.yml workflow will never fail silently — either it succeeds or the failure notification reaches a human promptly | Process | Medium | No | Skeleton becomes stale relative to latest tag with no detection |
| A-07 | No authorized repository contributor will push directly to the unprotected `cowork-skeleton` branch outside the CI workflow | Process | Medium | No | Unauthorized or malicious content delivered to all CoWork plugin users |
| A-08 | CoWork plugin resolution behavior (`@cowork-skeleton` branch reference) gives users control over when they receive updates | Process | Low | No | Users receive every CI push (including rollbacks, broken runs) immediately on next update |
| A-09 | The 3,256-file headroom (1,744 current vs 5,000 limit) provides sufficient margin for `main` growth across the project's lifetime | Resource | Medium | No | Future CI hard-fails with no gradual warning |
| A-10 | R-001's one-time empirical verification before Phase 5 is sufficient — the CoWork install mechanism is stable enough that no periodic re-testing is needed | Temporal | Low | No | CoWork API changes silently break the install; no automated detection |
| A-11 | GitHub's `GITHUB_TOKEN` non-retrigger guarantee is a stable platform invariant, not a policy that could change | Environmental | High | Implicitly | Workflow loop risk returns without code changes |
| A-12 | The 120-second `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` timeout is a fixed constant users can observe and override | Environmental | Medium | Partially (research Q3) | Users on slow networks hit opaque failures; override mechanism may not be surfaced |
| A-13 | REQ-022's supply-chain integrity check (`git diff v{N}..cowork-skeleton`) is run automatically and blocks publication of a corrupt skeleton | Process | Medium | No | A corrupt direct push to cowork-skeleton is never auto-detected before reaching users |
| A-14 | Future maintainers will understand that the orphan-branch fallback (Option B) is pre-designed and when to invoke it | Resource | Low | No | Clone weight silently worsens until install timeouts appear; maintainers don't know Option B exists or when to switch |

---

## Step 4: Stress-Test Results

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|-----------|-----------|-------------|----------|--------------------|
| IN-001 | A-01: file-count limit | CoWork limits by total clone size (MB) or clone time — `fetch-depth: 0` full history triggers limit even at 1,744 files | High — limit is undocumented; size-based limits are common in plugin systems | Critical | Completeness, Evidence Quality |
| IN-002 | A-07 + A-08: unprotected branch + branch-name install | A malicious or mistaken push to `cowork-skeleton` reaches all users because: (a) branch is unprotected, (b) users install via branch name not tag, (c) REQ-022 is a post-CI manual check not an automatic gate | High — anyone with repo write access can push | Critical | Methodological Rigor, Traceability |
| IN-003 | A-09: file-count margin | `main` adds 200–400 files per quarter (new skills, agents, hooks, tests); skeleton hits 5,000 within 2–4 years with no warning below hard-fail | High — `main` file count has already grown to 6,344 total | Major | Completeness, Actionability |
| IN-004 | A-06: no silent CI failure | `cowork-skeleton.yml` fails due to org policy change on GITHUB_TOKEN scope; the `if: failure()` notification webhook is not configured; skeleton stays at prior release indefinitely | Medium — CI failures without active notification monitoring are a common operational gap | Major | Completeness, Traceability |
| IN-005 | A-03: symlink resolution | CoWork materializes the plugin via a shallow clone or filesystem virtualization in `~/.claude/plugins/cache`; relative symlinks that resolve in the CI flat-checkout environment do not resolve in the cache path hierarchy | Medium — relative symlinks are fragile across directory structures | Major | Evidence Quality, Actionability |
| IN-006 | A-10: one-time empirical verification | Anthropic updates CoWork's plugin load mechanism (stricter file-count check, changed timeout, new manifest format requirement); the one-time R-001 check is now stale; skeleton builds successfully but fails to install | Medium — CoWork is under active development; plugin API is not formally versioned | Major | Completeness, Methodological Rigor |
| IN-007 | A-05: static stub | A maintainer editing `projects/README.md` in STORY-002 or a future cycle adds a CoWork-installation date or version note, intending to help users; the tree hash changes; bit-identical SHA breaks silently; force-push replaces the prior skeleton undetected | Medium — the helpfulness instinct to add version/date info is natural | Minor | Internal Consistency, Traceability |
| IN-008 | A-14: orphan fallback is known | Clone weight grows across releases; no trigger metric defined ("switch to Option B when X"); maintainers first notice the issue when users report install timeouts; the fallback exists but is undiscoverable without reading ADR-001 carefully | Medium — fallback is documented in ADR-001 but not in operational runbook or acceptance criteria | Minor | Actionability |

---

## Findings Summary Table

| ID | Finding | Type | Confidence | Severity | Affected Artifact + Section | Affected Dimension |
|----|---------|------|-----------|----------|----------------------------|--------------------|
| IN-001 | CoWork limit may be non-file-count-based; `fetch-depth: 0` full history exposes size/clone-time limit | Assumption stress-test (A-01) | Low | **Critical** | ADR-001 §Decisive Framing; phase1-requirements.md R-001 | Completeness, Evidence Quality |
| IN-002 | Unprotected branch + branch-name install = real-time supply-chain exposure with no automatic pre-publication gate | Anti-goal (AG-4) | Medium | **Critical** | REQ-021, REQ-022, REQ-026; ADR-002 §Branch-Protection Posture | Methodological Rigor, Traceability |
| IN-003 | No file-count margin trajectory monitoring; hard-fail at 5,000 is the first signal | Assumption stress-test (A-09) | High | **Major** | REQ-006 §Acceptance Criteria; ADR-001 L2 ¶5 | Completeness, Actionability |
| IN-004 | No staleness detection — silent CI failure leaves skeleton stale indefinitely | Assumption stress-test (A-06) | Medium | **Major** | REQ-016, NFR-003 §Acceptance Criteria | Completeness, Traceability |
| IN-005 | Symlink validation in CI environment does not confirm resolution in CoWork plugin cache runtime | Assumption stress-test (A-03) | Medium | **Major** | REQ-009 §Acceptance Criteria | Evidence Quality, Actionability |
| IN-006 | R-001 empirical check is one-time; no periodic re-test catches CoWork API changes | Anti-goal (AG-3b) | Medium | **Major** | R-001 §Verification Approach; phase1-requirements.md WS-5 | Completeness, Methodological Rigor |
| IN-007 | Static stub determinism constraint not formalized in requirements spec | Assumption stress-test (A-05) | Medium | Minor | ADR-001 §Stub Determinism Constraint; REQ-003 rationale | Internal Consistency, Traceability |
| IN-008 | No clone-weight monitoring threshold or automatic Option-B trigger | Assumption stress-test (A-14) | Medium | Minor | ADR-001 §Negative Consequences; REQ-027 (docs only) | Actionability |

---

## Detailed Findings

### IN-001: CoWork Limit Nature is Broader than R-001's Binary Assumption [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption stress-test |
| **Original Assumption** | The CoWork ~5,000-file limit is a file-count limit on a clean-clone working tree (R-001, phase1-requirements.md) |
| **Inversion** | The limit is size-based (MB of cloned data), object-count-based (total git objects), or clone-time-based (seconds to complete `git clone`) — any of which would be unaffected by reducing the tracked file count to 1,744 |
| **Plausibility** | High — the limit is explicitly noted as "absent from Anthropic's Claude Code plugin documentation" (R-001). Plugin host systems routinely impose size or timeout limits independently of file count. ADR-001 already documents that `fetch-depth: 0` carries `main`'s full git history into the skeleton, which increases clone size and clone time even if the working-tree file count is low. |
| **Confidence** | Low |
| **Consequence** | If CoWork's limit is clone-time-based or size-based, the skeleton would fail to install even at 1,744 files because the full `main` history makes the clone large. The design's provenance-vs-clone-weight tension (ADR-001 Force 2) is partially addressed (Option B orphan fallback exists) but only for the 120-second timeout case — not for a size or object limit. R-001's verification approach tests file count, not clone size or clone time, so this dimension would remain undetected even after R-001 is resolved. |
| **Evidence** | R-001: "Anthropic's public plugin docs do not document any ~5,000-file limit — that limit is a CoWork/Claude-Desktop runtime constraint per the project's settled facts." ADR-001 Context: "fetch-depth: 0 is required only to preserve main's full ancestry in the skeleton — deliberate clone-weight cost." REQ-001 acceptance criterion: "`git ls-files \| wc -l` returns a value less than 5,000" (measures file count only). |
| **Dimension** | Completeness, Evidence Quality |
| **Mitigation** | Expand R-001's verification approach to measure three dimensions during the Phase 5 empirical check: (1) tracked file count (current), (2) total repository size (`git count-objects -vH`; `.git/` directory size), (3) clone time on a reference network connection. If any dimension triggers CoWork's limit, the fallback strategy must address that dimension, not just file count. Add these measurements as explicit acceptance criteria alongside REQ-001's file-count check. |
| **Acceptance Criteria** | R-001's verification approach documents all three measurements; the Phase 5 empirical check records results for all three; the acceptance criteria table for REQ-001 includes clone size and clone time checks alongside the `git ls-files \| wc -l` check. |

---

### IN-002: Unprotected Branch + Branch-Name Install Creates Real-Time Supply-Chain Exposure [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-goal |
| **Original Assumption** | No authorized repository contributor will push directly to `cowork-skeleton` outside the CI workflow; and CoWork users who install `@cowork-skeleton` receive a controlled, CI-derived artifact |
| **Inversion** | Any actor with repository write access can push directly to the unprotected `cowork-skeleton` branch at any time. Because CoWork users install with `claude plugin marketplace add geekatron/jerry@cowork-skeleton` (a branch name), they receive any push to that branch — including a direct unauthorized push — on their next plugin update. There is no automatic gate between an arbitrary push and user delivery. |
| **Plausibility** | High — REQ-021 explicitly and intentionally leaves the branch unprotected. The REQ-022 integrity check (`git diff v{N}..cowork-skeleton`) is a post-CI acceptance test, not an automatic blocker. The design's loop-safety argument correctly addresses workflow-to-workflow loops but does not address the human-to-branch-to-user vector. |
| **Confidence** | Medium |
| **Consequence** | A compromised maintainer account, a mistaken direct push, or an emergency "hotfix" pushed to `cowork-skeleton` outside the CI derivation process would be immediately installed by all CoWork users who update. The content integrity check (REQ-022) is verified by "Analysis + Demonstration after each CI run" — not by an automated gate that runs before or at push time. Supply-chain integrity is therefore contingent on all write-access actors behaving correctly and on the post-hoc check being run promptly after any push. |
| **Evidence** | REQ-021: "The `cowork-skeleton` branch SHALL be configured as a CI-owned, unprotected branch... no branch protection rules, no required status checks, regenerated wholesale on each release." REQ-022: "Verified by Analysis + Demonstration after each CI run" (not at push time). REQ-026: tutorial instructs users to install `claude plugin marketplace add geekatron/jerry@cowork-skeleton` — a branch reference, meaning users track the live branch tip. ADR-002 L0: "no long-lived secret to leak" correctly identifies the credential risk but does not address the push-origin risk on the user side. |
| **Dimension** | Methodological Rigor, Traceability |
| **Mitigation** | Two independent mitigations should be added (not requiring branch protection, which ADR-002 deliberately avoids): (1) Add a GitHub Actions workflow that triggers on any push to `cowork-skeleton` from a non-bot author and immediately runs the REQ-022 `git diff` check, failing loudly if the branch content is not a clean derivative of a tagged release; (2) In the tutorial (REQ-026), document that `@cowork-skeleton` is a live branch reference and advise security-conscious users who want a pinned install to use `@{specific-tag-sha}` or to pin their install to a specific version using CoWork's pinning mechanism if available. |
| **Acceptance Criteria** | (1) A `push`-triggered workflow on `cowork-skeleton` runs REQ-022's integrity check and fails if the branch content is not derived from a `v*` tag; (2) REQ-026 tutorial acknowledges the branch-tracking behavior and provides guidance for users who want version-pinned installs. |

---

### IN-003: No File-Count Margin Trajectory Monitoring [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption stress-test |
| **Original Assumption** | The 3,256-file headroom (1,744 current vs 5,000 limit) provides sufficient margin for `main` growth across the project's lifetime |
| **Inversion** | `main` grows with new skills, agents, hooks, test fixtures, and context files. These files appear in the skeleton because only `projects/` is stripped. The headroom erodes without any monitoring signal; the first explicit notification is a hard CI failure at 5,000. |
| **Plausibility** | High — `main` already grew to 6,344 files prior to this project. Jerry adds skills and agents incrementally. New CoWork documentation adds files. The research notes optional future stripping candidates (test data, docs/archive/) but provides no trigger metric. |
| **Confidence** | High |
| **Consequence** | A CI release fails with a hard exit from the file-count assertion (REQ-006). The failure is detected in CI rather than in user installations, but it is a hard blocker that prevents the skeleton from being published for the failing release. Depending on how many files caused the threshold to be exceeded, the remediation may require a design decision (strip an additional directory, switch to orphan branch) rather than a quick fix. |
| **Evidence** | REQ-006: "Script SHALL assert that the tracked file count of the generated branch tree is less than 5,000 and SHALL exit with a non-zero exit code if this assertion is not satisfied." No corresponding requirement for a soft warning. ADR-001 L2 ¶5: "If clone weight or the file-count margin tightens later, the same generation job can additionally strip... none of which is needed today." No requirement defines when "later" becomes actionable. REQ-016 (job summary) does not require per-release file-count trend reporting. |
| **Dimension** | Completeness, Actionability |
| **Mitigation** | Add a soft-warning check in the generation script that emits a warning to `$GITHUB_STEP_SUMMARY` when the file count exceeds 4,000 (80% of limit). Define the file-count budget line items in the job summary (e.g., "skills/: 245 files, .context/: 312 files, src/: 189 files") so maintainers can see which directories are growing. Update NFR-003's acceptance criteria to include the per-release file count in the job summary. |
| **Acceptance Criteria** | Generation script emits a warning (not failure) at 4,000 files; per-directory file counts appear in every CI run's `$GITHUB_STEP_SUMMARY`; the acceptance criteria table for REQ-006 includes a soft-warning threshold. |

---

### IN-004: No Staleness Detection Mechanism [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption stress-test |
| **Original Assumption** | The `cowork-skeleton.yml` workflow will never fail silently — either it succeeds or the failure notification reaches a human promptly |
| **Inversion** | The workflow fails (e.g., GITHUB_TOKEN scope restricted by org policy change, action SHA revoked, or script error). The `if: failure()` notification step fires, but no external webhook is configured (REQ-016 describes it as "optional"). The failure goes unnoticed. The skeleton remains at the prior release indefinitely. Users installing `@cowork-skeleton` receive a stale plugin without warning. |
| **Plausibility** | Medium — CI failures that go unnoticed for extended periods are a common operational gap, especially for infrequently-checked notification channels. The design correctly adds failure visibility but makes the notification channel optional. |
| **Confidence** | Medium |
| **Consequence** | `cowork-skeleton` diverges from the latest `v*` release by one or more versions. CoWork users do not know the plugin is stale. The stale skeleton may be functionally fine for a time, but security-relevant changes, bug fixes, and new features in `main` are not delivered. NFR-003 ("updated within one workflow run") is violated with no detection. |
| **Evidence** | REQ-016: "SHALL include a dedicated failure-notification step executed only when `if: failure()`" — this fires at job failure. There is no requirement for an external staleness monitor (e.g., a scheduled check that verifies `cowork-skeleton` was updated for the current latest tag). NFR-003 acceptance criterion: "GitHub Actions run history shows `cowork-skeleton.yml` completes within the same release window" — this requires a human to check the Actions UI. No automated cross-check between latest `v*` tag and the tag embedded in `git log -1 cowork-skeleton`. |
| **Dimension** | Completeness, Traceability |
| **Mitigation** | Add a scheduled daily GitHub Actions workflow (cron) that: (a) reads the latest `v*` tag SHA, (b) reads the `Source-Commit:` trailer from `git log -1 cowork-skeleton`, (c) compares them and fails loudly (issue creation or mandatory notification) if they diverge. Alternatively, add the staleness check as a step in the existing `release.yml` workflow that runs after the skeleton push and confirms the deployed skeleton matches the tag. |
| **Acceptance Criteria** | A mechanism exists (scheduled or release-triggered) that automatically compares the skeleton's embedded Source-Commit SHA to the latest `v*` tag SHA and produces a visible failure if they diverge. |

---

### IN-005: Symlink Validation in CI Does Not Confirm CoWork Runtime Resolution [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption stress-test |
| **Original Assumption** | Relative symlinks `.claude/rules → ../.context/rules` and `.claude/patterns` resolve correctly in CoWork's plugin cache directory |
| **Inversion** | CoWork materializes the plugin by cloning to `~/.claude/plugins/cache/{repo-name}/` or a similar path. If CoWork uses `git worktree`, a sparse checkout, or a symlink-stripping clone mode, the relative symlinks may resolve to nonexistent targets. The CI check (`readlink -f` in the CI runner's flat checkout) does not reproduce the CoWork runtime directory layout. |
| **Plausibility** | Medium — CoWork's plugin caching mechanism is not formally documented at the path-resolution level (research Q3). Relative symlinks are filesystem-layout-dependent. The CI environment is a temporary flat checkout, not the same directory layout as a user's `~/.claude/plugins/cache`. |
| **Confidence** | Medium |
| **Consequence** | `.claude/rules/` auto-loading fails silently on CoWork installs. The entire Jerry framework behavioral layer (all HARD rules, auto-loaded context, skill triggers) is absent. The plugin appears installed (file count check passes, agent paths resolve) but Jerry's governance and skill behavior does not function. This is a silent, severe user-facing failure. |
| **Evidence** | REQ-009 acceptance criterion: "`readlink -f .claude/rules` and `readlink -f .claude/patterns` both resolve to non-empty, existing paths" — this tests the CI checkout, not the CoWork cache. Anthropic plugin docs (research Q3): "install copies whole repo to cache" — the layout of that cache and how symlinks are handled is not detailed. REQ-009 rationale: "These symlinks wire the framework rule files into Claude Code's auto-loading path" — confirming the functional criticality. |
| **Dimension** | Evidence Quality, Actionability |
| **Mitigation** | Add the symlink test to R-001's Phase 5 empirical verification: on a real CoWork install of the skeleton branch, confirm that `.claude/rules/` and `.claude/patterns/` auto-loading functions correctly (not just that `readlink -f` resolves in CI). Add this as an explicit acceptance criterion alongside REQ-009's CI-level test. If CoWork uses a clone mode that breaks symlinks, convert symlinks to hard directory copies in the skeleton generation script. |
| **Acceptance Criteria** | R-001's empirical check includes verification that `.claude/rules/` loads correctly in an actual CoWork session (not just in a CI `readlink -f` check). REQ-009 is amended to acknowledge the CI-only scope and requires a corresponding CoWork-runtime test before Phase 5 completion. |

---

### IN-006: R-001 Empirical Check is One-Time; CoWork API Changes Break Installs Silently [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Anti-goal |
| **Original Assumption** | A one-time empirical verification before Phase 5 is sufficient — the CoWork install mechanism is stable enough that no periodic re-testing is needed |
| **Inversion** | Anthropic updates CoWork's plugin loading mechanism after Phase 5 ships — stricter file-count threshold, changed manifest format, new required `plugin.json` field, or altered timeout. Subsequent releases generate valid skeletons (all CI checks pass) but CoWork users cannot install them. No automated detection exists. |
| **Plausibility** | Medium — CoWork is an active product. Plugin APIs evolve. The research notes the install command syntax and manifest format as current facts, not contractual commitments. The project has no mechanism to detect CoWork changes after R-001 is closed. |
| **Confidence** | Medium |
| **Consequence** | CI succeeds, the skeleton is published to the `cowork-skeleton` branch, users attempt to install `@cowork-skeleton` and receive a failure they cannot diagnose. The skeleton appears correct by all CI metrics. The failure is in the CoWork runtime, which the CI never exercises directly. |
| **Evidence** | R-001 Verification Approach: "(a) attempt to install from the current `main` branch on a clean machine... (b) install from a branch with `projects/` stripped and confirm the error is resolved. Both steps must be demonstrated as Phase 1 acceptance criteria before any implementation proceeds." This is explicitly once, not recurring. WS-5 (REQ-030–REQ-033): quality gates address deliverable quality, not ongoing install compatibility. No requirement analogous to R-001 is defined for future releases. |
| **Dimension** | Completeness, Methodological Rigor |
| **Mitigation** | Add a scheduled (monthly or per-release) GitHub Actions workflow that performs an actual CoWork install of `@cowork-skeleton` on a clean environment (GitHub-hosted runner with no cached state) and confirms install success. This can be lightweight — a simple `claude plugin marketplace add geekatron/jerry@cowork-skeleton` invocation followed by a basic smoke test. Add this as a WS-2 or WS-5 requirement. |
| **Acceptance Criteria** | A recurring CI check (scheduled or per-release) exercises an actual CoWork install of `cowork-skeleton` and fails visibly if the install does not succeed. |

---

### IN-007: Static Stub Determinism Constraint is Tacit Knowledge [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption stress-test |
| **Original Assumption** | The `projects/README.md` stub will remain static content with no generated timestamps or version strings |
| **Inversion** | A future maintainer, during routine documentation cleanup, edits `projects/README.md` to add "Last regenerated: {date}" or "Compatible with Jerry {version}" — a natural improvement instinct. The tree hash changes. The bit-identical SHA guarantee (REQ-003/NFR-001/NFR-002) breaks silently. `workflow_dispatch` retries now produce a different SHA than the initial run, breaking the idempotency acceptance test. |
| **Plausibility** | Medium — the stub's static-content constraint is documented in ADR-001's risk table and "Stub determinism constraint" subsection, but it is NOT formalized as a SHALL requirement in the requirements specification. Nothing in WS-1 (REQ-001–REQ-010) prohibits dynamic stub content. |
| **Confidence** | Medium |
| **Consequence** | Bit-identical idempotency breaks. Tamper detection based on SHA comparison becomes unreliable. The breakage is discoverable via the REQ-003 acceptance test but only if that test is run — it is not a CI gate on every commit to `main`. |
| **Evidence** | ADR-001 §Stub Determinism Constraint: "the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility." — This is an ADR-level constraint. REQ-003 acceptance criterion and phase1-requirements.md do not include a corresponding SHALL requirement prohibiting dynamic stub content. STORY-002 is assigned to author the stub, but the static constraint is not listed among the WS-1 requirements the story must satisfy. |
| **Dimension** | Internal Consistency, Traceability |
| **Mitigation** | Add a formal requirement (REQ-011 or as an REQ-003 sub-clause) that states: "The `projects/README.md` sentinel file content SHALL be fully static — no timestamps, version strings, or generated values — to preserve the bit-identical commit SHA guarantee." Add a CI assertion in the generation script that computes the SHA of `projects/README.md` and compares it to a known-good value, failing if the stub content has drifted. |
| **Acceptance Criteria** | A formal SHALL requirement exists in WS-1 prohibiting dynamic stub content; a CI assertion in the generation script detects stub content drift and exits non-zero. |

---

### IN-008: No Clone-Weight Monitoring Threshold or Option-B Trigger Metric [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption stress-test |
| **Original Assumption** | Future maintainers will know when to invoke the orphan-branch fallback (Option B) based on the ADR-001 documentation |
| **Inversion** | Repository history grows over years (more releases, large binary merges, documentation blobs). Clone weight increases silently. Users on slower networks begin experiencing install timeouts but report them as generic CoWork errors. Maintainers do not know the clone-weight trigger point or that Option B exists, because the fallback is documented in ADR-001 but not surfaced in CI or documentation. |
| **Plausibility** | Medium — ADR-001 correctly identifies the risk and the fallback, but no operational runbook, threshold metric, or automated detection is defined. ADR-001 §Negative Consequences notes "clone weight under full provenance" as a risk with "Option B (orphan) escape hatch" as the mitigation, but this remains entirely human-dependent. |
| **Confidence** | Medium |
| **Consequence** | Install timeouts accumulate in user reports before maintainers connect the symptom to the clone-weight cause. Switching to Option B requires understanding ADR-001 in detail, which may not be available to future maintainers unfamiliar with the original design. |
| **Evidence** | ADR-001 §Negative Consequences: "Clone weight under full provenance — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`; on slow networks this risks CoWork's 120-second git-operation timeout... Mitigation: Option B (orphan) escape hatch." REQ-027 documents the timeout and the `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` override in end-user troubleshooting documentation only. No requirement tasks CI with measuring or reporting clone weight per release. |
| **Dimension** | Actionability |
| **Mitigation** | Add to the generation script a step that reports the compressed clone size (`git count-objects -vH`) in `$GITHUB_STEP_SUMMARY` alongside the file-count report. Define a soft-warn threshold (e.g., "repository bundle exceeds 50 MB — consider switching to orphan branch per ADR-001 Option B"). Reference ADR-001 Option B in the operational runbook (STORY-004 or equivalent) so the escape hatch is discoverable. |
| **Acceptance Criteria** | Each CI run includes clone size in `$GITHUB_STEP_SUMMARY`; a soft-warn threshold is defined; the operational runbook references Option B with the trigger metric. |

---

## Step 5: Mitigations

### Critical Findings — MUST Mitigate Before Phase 5

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| IN-001 | Expand R-001 verification to measure clone size and clone time alongside file count. Add clone-size and clone-time measurements as explicit acceptance criteria in REQ-001's acceptance criteria table. | R-001 verification approach documents three measurements; REQ-001 acceptance criteria table includes all three. |
| IN-002 | (a) Add a `push`-triggered integrity check workflow on `cowork-skeleton` that runs REQ-022 and fails loudly for non-CI-derived content. (b) Add language to REQ-026 tutorial acknowledging branch-tracking behavior and guidance for version-pinned installs. | Integrity check workflow exists and is tested; tutorial includes branch-tracking disclosure. |

### Major Findings — SHOULD Mitigate Before Phase 6

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| IN-003 | Add soft-warn threshold at 4,000 files to generation script; include per-directory counts in `$GITHUB_STEP_SUMMARY`. | Script emits warning at 4,000 files; job summary includes directory breakdown. |
| IN-004 | Add scheduled or release-triggered staleness check comparing skeleton's embedded SHA to latest `v*` tag. | Automated mechanism fails visibly if skeleton and latest tag diverge. |
| IN-005 | Include symlink runtime resolution test in R-001's empirical Phase 5 check (real CoWork session, not CI `readlink -f`). Amend REQ-009 acceptance criteria to note CI-only scope and require CoWork-runtime companion test. | REQ-009 amended; CoWork-runtime symlink test documented in R-001 verification approach. |
| IN-006 | Add recurring CI workflow (scheduled or per-release) performing an actual CoWork install of `@cowork-skeleton`. | Recurring install test runs; failure produces visible, actionable alert. |

### Minor Findings — MAY Mitigate

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| IN-007 | Add a formal SHALL requirement prohibiting dynamic stub content; add a CI SHA check on `projects/README.md`. | Requirement added in WS-1; CI assertion detects drift. |
| IN-008 | Report clone size in `$GITHUB_STEP_SUMMARY`; define soft-warn threshold; reference Option B in operational runbook. | Clone size visible per release; runbook references Option B with trigger metric. |

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-001, IN-003, IN-004, IN-006: the deliverables do not cover non-file-count limit dimensions, file-count trajectory monitoring, staleness detection, or recurring install testing. These are structural gaps in requirement coverage. |
| Internal Consistency | 0.20 | Slightly Negative | IN-007: ADR-001 documents the static stub constraint as a MUST, but the requirements spec has no corresponding SHALL. This creates a consistency gap between the ADR and the requirements baseline. |
| Methodological Rigor | 0.20 | Negative | IN-002, IN-006: the supply-chain integrity check (REQ-022) is a post-hoc acceptance test, not an automatic gate. R-001's one-time empirical check is methodologically incomplete for a system expected to evolve alongside an active CoWork platform. |
| Evidence Quality | 0.15 | Slightly Negative | IN-001, IN-005: the file-count assumption rests on undocumented CoWork behavior (R-001 open); the symlink acceptance criterion (REQ-009) tests in an environment that does not replicate the CoWork runtime. Both weaken the evidentiary basis for G-1 and G-3. |
| Actionability | 0.15 | Negative | IN-003, IN-008: the lack of a soft-warn file-count threshold and the absence of a clone-weight monitoring metric leave maintainers without actionable signals before failures occur. IN-006: no recurring test means the action required to detect a broken install is manual and undefined. |
| Traceability | 0.10 | Negative | IN-002, IN-004, IN-007: REQ-022's verification method (Analysis + Demonstration) is not formally linked to an automatic enforcement point; the staleness mechanism is not traced to any requirement; the stub determinism constraint exists in the ADR but not in the requirements. |

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 2
- **Major:** 4
- **Minor:** 2
- **Goals Analyzed:** 6
- **Assumptions Mapped:** 14
- **Protocol Steps Completed:** 6 of 6

---

*Strategy: S-013 Inversion Technique*
*Template: .context/templates/adversarial/s-013-inversion.md v1.0.0*
*Deliverables: phase1-requirements.md, ADR-001-skeleton-derived-branch-strategy.md, ADR-002-ci-token-push-strategy.md*
*Reviewer: adv-executor (Group E — Decompose), blind / independent*
*Date: 2026-06-26*
*Execution ID: 20260626-s013*
*H-15 Self-Review: Applied before persistence — findings have specific evidence, severities are justified, IN-NNN identifiers are consistent, summary table matches detail blocks.*
