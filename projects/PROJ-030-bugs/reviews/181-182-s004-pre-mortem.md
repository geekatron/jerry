# Pre-Mortem Report: `.claude/settings.local.json` (#181/#182)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `.claude/settings.local.json` (GitHub Issues #181/#182 implementation)
**Criticality:** C4
**Date:** 2026-03-14
**Reviewer:** adv-executor
**H-16 Compliance:** S-003 Steelman applied 2026-03-14 (confirmed — `reviews/181-182-s003-steelman.md`)
**Failure Scenario:** It is September 2026. The `settings.local.json` configuration has failed spectacularly. Skills are broken or prompting for approval despite being listed, MCP tools are misbehaving, at least one contributor has seen different behavior on their machine, and CI logs show Bash permission errors. The team is investigating what went wrong with the "fixed" configuration.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk assessment and recommendation |
| [Findings Table](#findings-table) | All failure causes with prioritization |
| [Detailed Findings](#detailed-findings) | Expanded analysis for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized mitigation plan (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 quality dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion status |

---

## Summary

The `settings.local.json` implementation is structurally correct at the time of authoring, but its long-term reliability depends on four external stability assumptions that are not documented or monitored: (1) Claude Code permission syntax remains stable, (2) the `Skill(name)` matching form continues to work without namespace qualification, (3) the `mcp__plugin_context7_context7__*` namespace does not change, and (4) new skills added to CLAUDE.md are also added here. The most dangerous failure mode is silent degradation — the configuration stays syntactically valid while gradually losing effectiveness as skills are added or Claude Code updates shift behavior. Eleven failure causes were identified: 2 Critical, 6 Major, 3 Minor.

**Recommendation:** ACCEPT with P0/P1 mitigations. The immediate production risk is low, but without a maintenance contract (drift detection mechanism + update procedure), this configuration will silently degrade within 6 months. P0 mitigations are documentation and tooling additions, not configuration changes.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260314T1500 | Skill registry drift: new skills added to CLAUDE.md without updating settings.local.json causes silent approval prompts | Process | High | Critical | P0 | Completeness |
| PM-002-20260314T1500 | Claude Code update changes `Skill(name)` matching semantics or makes namespace qualification required again | External | Medium | Critical | P0 | Methodological Rigor |
| PM-003-20260314T1500 | The `mcp__plugin_context7_context7__*` wildcard becomes stale when Context7 changes its plugin namespace | External | Medium | Major | P1 | Completeness |
| PM-004-20260314T1500 | No automated validation: nothing verifies that listed skills actually match without approval prompts after any change | Process | High | Major | P1 | Actionability |
| PM-005-20260314T1500 | The `Bash(git push *)` local-allow override silently breaks for a contributor who copies this file, overriding their intended `ask` gate | Process | Medium | Major | P1 | Internal Consistency |
| PM-006-20260314T1500 | `settings.local.json` is gitignored or not committed, so the fix is lost when the developer moves to a new workstation or the worktree is recreated | Assumption | High | Major | P1 | Traceability |
| PM-007-20260314T1500 | Hooks block becomes non-functional when Claude Code changes the hook schema (matcher format, JSON structure, or supported event types) | External | Medium | Major | P1 | Internal Consistency |
| PM-008-20260314T1500 | The precedence ordering assumption fails: a future Claude Code update changes evaluation order for `local` vs `shared` settings, causing unexpected `ask` prompts for skills already in `settings.json` | External | Low | Major | P1 | Evidence Quality |
| PM-009-20260314T1500 | The `Bash(grep *)` allow entry is too broad and is later exploited to construct data exfiltration pipelines combining grep with redirects | Technical | Low | Minor | P2 | Methodological Rigor |
| PM-010-20260314T1500 | The `mcp__memory-keeper__*` wildcard permits `context_batch_delete` which destructively removes all stored cross-session context without a confirmation gate | Technical | Low | Minor | P2 | Actionability |
| PM-011-20260314T1500 | New contributors are confused by the divergence between `settings.local.json` (local, precedence 3) and `settings.json` (shared, precedence 4), leading to cargo-cult changes that break the layered architecture | Resource | Medium | Minor | P2 | Traceability |

---

## Detailed Findings

### PM-001-20260314T1500: Skill Registry Drift [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Priority** | P0 |
| **Affected Dimension** | Completeness |
| **Likelihood** | High |

**Failure Cause:** The deliverable's completeness relies on a manual synchronization between two files: CLAUDE.md (the skill registry) and `settings.local.json` (the permission list). Every time a new skill is added to CLAUDE.md and `settings.local.json` is not updated, that skill silently loses auto-approval. The developer encounters approval prompts and either grants them reflexively (T-05 approval fatigue, identified in the threat model) or the skill's H-22 proactive invocation fails entirely. There is no automated mechanism to detect drift.

**Evidence:** The design document's Decision 2 explicitly tracks that 12 of 19 skills were missing from the original file. This demonstrates the failure mode has already occurred once. The fix adds all 19 skills, but the design document contains no mechanism to keep this list current. The CLAUDE.md skill table is the ground truth, but there is no link from CLAUDE.md to `settings.local.json` and no validation script.

**Scenario:** A developer adds `Skill(devsecops)` to CLAUDE.md in November 2026. Three weeks later they notice `/devsecops` is generating approval prompts on every invocation and H-22 violations are appearing in quality reviews. Investigation reveals `settings.local.json` was not updated. The configuration silently degraded.

**Mitigation:** Add a linting check — either a CI step or a `Makefile` target — that reads the skill list from CLAUDE.md and verifies each is present in `settings.local.json`. The check should run on every CLAUDE.md change.

**Acceptance Criteria:** A script or CI check exists that detects CLAUDE.md-to-settings.local.json skill registry drift and fails noisily with a diff showing missing skills.

---

### PM-002-20260314T1500: `Skill(name)` Syntax Deprecation [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | External |
| **Priority** | P0 |
| **Affected Dimension** | Methodological Rigor |
| **Likelihood** | Medium |

**Failure Cause:** The entire skill permission approach migrates from the undocumented `Skill(jerry:name)` form to the documented `Skill(name)` form, citing GitHub Issue #29360 as evidence of namespace resolution bugs. This is the correct migration at the time of writing. However, the `Skill(name)` form itself could be deprecated, renamed, or superseded by a new namespace-qualified form in a future Claude Code release. Because the issue history (#33595) shows that deprecated syntax can silently fail, a future change to the `Skill()` matching mechanism could cause all 19 skill entries to become ineffective simultaneously — the highest-impact single point of failure in the configuration.

**Evidence:** The design explicitly relies on "The `Skill(name)` form is the only form appearing in official documentation examples" (Decision 1). This is a point-in-time claim about documentation state. The research backing (FINDING-002) and the GitHub issue trail both show that Claude Code's permission syntax is evolving. The `Skill(jerry:name)` form was once used — presumably by someone who believed it was correct — showing that the "documented form" understanding can change.

**Scenario:** Claude Code v1.8.0 ships in July 2026 and moves to a mandatory `{workspace-slug}/{skill-name}` format for all permission entries, deprecating the bare `Skill(name)` form with a 90-day migration window. The settings.local.json file silently stops matching. All 19 skills begin prompting for approval. The developer initially assumes a workstation issue and spends a day debugging before identifying the root cause.

**Mitigation:** Pin the Claude Code version in CLAUDE.md or in a `.claude/version-constraints.md` file that documents the version against which this configuration was validated. Add a session-start check that warns if the running Claude Code version differs from the validated version. Subscribe to the Claude Code changelog for permission syntax changes.

**Acceptance Criteria:** A documented version pinning or monitoring strategy exists that would surface a breaking Claude Code permission syntax change within one session of it taking effect.

---

### PM-003-20260314T1500: `mcp__plugin_context7_context7__*` Namespace Staleness [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | External |
| **Priority** | P1 |
| **Affected Dimension** | Completeness |
| **Likelihood** | Medium |

**Failure Cause:** The configuration retains `mcp__plugin_context7_context7__*` as a wildcard entry specifically to handle the Context7 plugin namespace convention (per Decision 6 and reference to GitHub Issue #29360). This double-namespaced form is itself a workaround for a known Claude Code plugin namespace resolution bug. When that bug is fixed — or when Context7 updates its plugin registration — the `mcp__plugin_context7_context7__*` wildcard either becomes redundant or stops matching. If the fix changes the namespace to a third form (e.g., `mcp__context7_v2__*`), the wildcard silently stops covering Context7 plugin tool calls.

**Evidence:** Decision 6 states "The `mcp__plugin_context7_context7__*` entries exist because of the Context7 plugin namespace convention (GitHub Issue #29360)." This is an explicit acknowledgment that this entry is a workaround for a known bug, not a stable API surface. Workaround entries are inherently time-limited.

**Mitigation:** Document the dependency on GitHub Issue #29360 in a comment within the design document or in a `.claude/mcp-namespace-notes.md` file. Add a TODO to re-evaluate this entry after #29360 is resolved.

**Acceptance Criteria:** The design document or a companion reference file explicitly tracks the `mcp__plugin_context7_context7__*` entry as a workaround with a link to the upstream issue and a review trigger.

---

### PM-004-20260314T1500: No Automated Validation Gate [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Priority** | P1 |
| **Affected Dimension** | Actionability |
| **Likelihood** | High |

**Failure Cause:** The configuration has no automated test or validation. The design document verifies correctness by manual inspection and reasoning. After any change to `settings.local.json`, `settings.json`, or CLAUDE.md, there is no automated check that verifies the permission system functions as intended. This means regressions are discovered at runtime — when a developer notices an unexpected approval prompt or when a CI run fails because a Bash command was not auto-approved.

**Evidence:** The design document's L0 executive summary and L1 technical design sections are entirely manual reasoning artifacts. The threat model identifies the failure modes (T-02, T-03, T-05) but provides no automated check that those mitigations are in place. The existing CI pipeline (`.github/workflows/`) validates code quality but has no settings.local.json validation step.

**Mitigation:** Create a `scripts/validate-settings.sh` (or Python equivalent using `uv run`) that: (1) checks all CLAUDE.md-registered skills are present in `settings.local.json`, (2) verifies no deprecated `:*` Bash syntax is present, (3) validates JSON syntax. This script should run in CI on any change to `.claude/` files or CLAUDE.md.

**Acceptance Criteria:** A validation script exists, is executable, and is invoked in CI. A PR that adds a skill to CLAUDE.md without updating `settings.local.json` fails CI.

---

### PM-005-20260314T1500: `git push` Override Hazard for New Contributors [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Priority** | P1 |
| **Affected Dimension** | Internal Consistency |
| **Likelihood** | Medium |

**Failure Cause:** The `Bash(git push *)` entry in `settings.local.json` is a deliberate local override of the `ask` gate in `settings.json`. This is architecturally correct and is well-documented in the design. However, the file is named `settings.local.json` and has the same structure as `settings.json` — a new contributor who copies it as a starting point for their own local configuration silently inherits the `git push` auto-allow behavior. They may not realize they have bypassed the team safety gate. The design document correctly identifies this as T-01 (MEDIUM) but frames it as "accepted risk" with no onboarding protection.

**Evidence:** Decision 4 explicitly states: "The local `allow` entry intentionally overrides the shared `ask` entry, auto-approving `git push` for this developer. This is a valid developer-specific override." The threat model entry T-01 rates this MEDIUM. The S-003 Steelman (SM-003) notes: "The `git push` decision demonstrates the layered architecture working exactly as designed." All of this is correct — but it assumes the developer copying the file has read the design document, which is not enforced.

**Mitigation:** Add an inline JSON comment (via a `_comments` key or companion README) explaining that `Bash(git push *)` is a deliberate personal override and should be removed if the recipient wants the team safety gate. Alternatively, add a `SETUP.md` or `docs/reference/settings-local-setup.md` with explicit warnings about which entries to remove before sharing the file.

**Acceptance Criteria:** A companion document or inline marker warns that `Bash(git push *)` is a personal override that MUST NOT be shared without review.

---

### PM-006-20260314T1500: Configuration Not Tracked — Lost on Workstation Reset [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Priority** | P1 |
| **Affected Dimension** | Traceability |
| **Likelihood** | High |

**Failure Cause:** `settings.local.json` is committed to the repository in this worktree (`fix/proj-030-bugs`). However, the file's name and location suggest it is intended to be a machine-local file (hence "local"). If the file is listed in `.gitignore` in other branches or contexts, or if a future clean checkout does not include it, all three bugs fixed by #181/#182 will silently return. The developer will be working from a clean worktree with the old broken configuration restored from the committed `settings.json` defaults, or with no local overrides at all.

**Evidence:** The design document does not address the file's persistence strategy — whether it is committed, gitignored, or managed via dotfiles. The `git status` output at the top of the conversation shows `settings.local.json` as untracked (`M .claude/settings.local.json`). This suggests the fix is an uncommitted local modification in the current worktree, which means it exists only in this working tree and could be lost on branch switch, stash pop, or worktree deletion.

**Mitigation:** Explicitly document the persistence strategy for `settings.local.json` in the design document: is this file committed to the repo? If so, which branches? If not, how is it distributed to contributors? If it is committed, add it to CI. If it is not committed, provide a `scripts/setup-local-settings.sh` that generates it from a template.

**Acceptance Criteria:** The design document states whether `settings.local.json` is committed or gitignored, and provides a recovery procedure (script or documentation) for recreating it from scratch on a new workstation.

---

### PM-007-20260314T1500: Hooks Block Schema Rot [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | External |
| **Priority** | P1 |
| **Affected Dimension** | Internal Consistency |
| **Likelihood** | Medium |

**Failure Cause:** The hooks block retains the `PreToolUse` and `PermissionRequest` hook types with `echo`-based command responses. This is the same pattern as the original file (kept by Decision 5). Claude Code's hook system is an extension point that evolves independently of the permission system. If Claude Code changes the expected JSON response format for hook commands, the echo-based responses become invalid and all web tool requests begin failing silently or triggering errors. The `PermissionRequest` hook type in particular uses a deeply nested JSON structure (`hookSpecificOutput.decision.behavior`) that is not self-evident from the Claude Code documentation and could break on a schema change.

**Evidence:** Decision 5 in the design document states "Keep the hooks block. It serves a developer-specific purpose (auto-approving web tools without prompts) and does not duplicate any committed configuration." The rationale is correct, but the hooks block is carried forward from the original file without re-evaluation. The `PermissionRequest` hook structure (`{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}`) uses a schema that is version-dependent and is not documented in the Claude Code public API.

**Mitigation:** Add a version comment to the hooks block noting the Claude Code version against which this hook schema was validated. Alternatively, link to the Claude Code hooks documentation from the design document and flag this as a section to review when Claude Code is updated.

**Acceptance Criteria:** The hooks block has a companion documentation reference tracking its schema version, or the design document explicitly notes that hook schema validation is part of the Claude Code update review checklist.

---

## Recommendations

### P0 — Critical: MUST mitigate before production reliance

**PM-001-20260314T1500: Skill Registry Drift Detection**

Create a drift-detection mechanism between CLAUDE.md skill registrations and `settings.local.json` permissions. At minimum, a script that:
1. Extracts skill names from CLAUDE.md's skill table (grep or AST-based)
2. Checks each skill name appears as `Skill({name})` in `settings.local.json`
3. Fails with a diff showing missing or extra entries

Integrate into CI as a pre-commit hook or GitHub Actions step triggered by changes to either CLAUDE.md or `.claude/settings.local.json`.

Acceptance Criteria: Adding a skill to CLAUDE.md without updating `settings.local.json` produces a CI failure with a human-readable diff.

---

**PM-002-20260314T1500: Claude Code Version Pinning / Change Monitoring**

Document the Claude Code version against which this configuration was validated. Add to the design document or to a `.claude/VERSION-VALIDATED.md` file:
- Claude Code version (or version range) where `Skill(name)` form was confirmed working
- Claude Code changelog subscription method or review cadence
- Validation procedure to re-confirm behavior after a Claude Code update

Acceptance Criteria: A dated record exists of the Claude Code version where this configuration was validated. A process exists (even a manual checklist) to repeat that validation when Claude Code updates.

---

### P1 — Important: SHOULD mitigate

**PM-003-20260314T1500: Track `mcp__plugin_context7_context7__*` Workaround**

In the design document's Decision 6, add a note: "This entry is a workaround for GitHub Issue #29360. When #29360 is resolved upstream, this entry should be removed and tested. If Context7 changes its plugin namespace, this wildcard must be updated." Set a calendar reminder or worktracker task to review this entry when Context7 releases a major update.

Acceptance Criteria: The design document explicitly marks this entry as a workaround with a review trigger.

---

**PM-004-20260314T1500: Automated Validation Script**

Create `scripts/validate-settings-local.sh` (or `scripts/validate_settings_local.py` via `uv run`) that validates:
1. All CLAUDE.md skills are present in `settings.local.json`
2. No `:*` deprecated syntax is present
3. JSON is syntactically valid
4. No `Bash(python3 *)` entries exist (H-05 enforcement)

Acceptance Criteria: Script runs to completion with exit code 0 on the current file. Script fails with exit code 1 and a human-readable error on a file with any of the four violations.

---

**PM-005-20260314T1500: `git push` Override Warning**

Add a `_meta` section to `settings.local.json` (using a JSON convention like a leading comment or a `_documentation` key if Claude Code tolerates it) or create a companion `settings.local.json.md` explaining that `Bash(git push *)` is a personal override. If JSON comments are not supported, add a `PERSONAL-SETTINGS-NOTES.md` to the `.claude/` directory with this warning prominently placed.

Acceptance Criteria: A contributor copying `settings.local.json` will encounter a clear warning about `Bash(git push *)` before they use the file.

---

**PM-006-20260314T1500: Persistence Strategy Documentation**

Document explicitly in the design document or in a `.claude/README.md`:
1. Is `settings.local.json` committed to this repo? If yes, which branches?
2. If the developer recreates this worktree, how do they recover `settings.local.json`?
3. Provide a `scripts/bootstrap-local-settings.sh` or equivalent that generates the file from a template.

Acceptance Criteria: A developer can set up a fresh worktree and know exactly how to obtain a correct `settings.local.json` without reading this design document in full.

---

**PM-007-20260314T1500: Hooks Schema Version Tracking**

Add a comment or companion file noting the hooks JSON schema version and Claude Code version where it was validated. Include the `PermissionRequest` hook structure as a reference in the design document, clearly noting it is version-sensitive.

Acceptance Criteria: A reviewer can identify which Claude Code version the hooks block was validated against and know whether their version matches.

---

**PM-008-20260314T1500: Precedence Ordering Assumption Documentation**

Explicitly document in the design that the deduplication strategy (removing local entries subsumed by shared entries) depends on Claude Code's documented precedence ordering: local (3) > shared (4). If this ordering changes, the deduplication logic becomes wrong and the local file would need to be expanded. Note this as a key assumption in the design's "Assumptions" section.

Acceptance Criteria: The design document has an "Assumptions" section or equivalent that lists "Claude Code settings precedence: local=3 overrides shared=4" as an explicit dependency.

---

### P2 — Monitor: MAY mitigate; acknowledge risk

**PM-009-20260314T1500: `Bash(grep *)` Breadth**

Current threat model entry T-07 correctly scores this LOW (DREAD 1.8). No change required. Document in the design that `grep` is scoped to read-only operations and that the `deny` array blocks exfiltration vectors (`curl`, `wget`). Monitor if additional Bash entries that combine with `grep` are added.

**PM-010-20260314T1500: `mcp__memory-keeper__*` Batch Delete Scope**

Current threat model entry T-04 correctly accepts this risk for developer-local configuration. Note in the design that the `context_batch_delete` operation is covered by the wildcard and confirm this is the intended scope. If the developer's workflow grows to include critical cross-session context that would be unrecoverable after a batch delete, narrow the wildcard to exclude delete operations.

**PM-011-20260314T1500: Contributor Onboarding Confusion**

Create a `.claude/README.md` that explains the two-file settings architecture, the precedence ordering, and the intent of each section in both files. This serves as the onboarding document that prevents cargo-cult changes from contributors unfamiliar with Claude Code's layered permission system.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001 (skill drift) and PM-006 (persistence gap) are completeness failures — the configuration is complete at authoring time but has no mechanism to stay complete. The design document has no "Maintenance" section. |
| Internal Consistency | 0.20 | Negative | PM-005 (git push override hazard) creates an internal consistency risk: the design correctly labels git push as "developer-intentional" but provides no barrier against unintentional propagation. PM-007 (hooks schema) adds a consistency risk if the hooks behavior diverges from the permission behavior silently. |
| Methodological Rigor | 0.20 | Negative | PM-002 (syntax deprecation risk) and PM-004 (no validation gate) represent methodological gaps — the migration is rigorously executed but without a validation procedure or version anchor, the rigor is a one-time property, not an ongoing one. |
| Evidence Quality | 0.15 | Neutral | The evidence base (FINDING-002, FINDING-003, FINDING-004, Issue #33595, Issue #29360) is sound and current. The gaps identified (PM-002, PM-003) are about evidence becoming stale, not about evidence being weak at authoring time. |
| Actionability | 0.15 | Negative | PM-004 (no validation script) and PM-006 (no persistence recovery procedure) reduce actionability for future contributors. A developer encountering this configuration 6 months later cannot easily verify it is correct or recover it if lost. |
| Traceability | 0.10 | Negative | PM-006 (persistence strategy undocumented), PM-003 (workaround not tracked), and PM-008 (precedence assumption implicit) all reduce traceability — a future reviewer cannot tell what was assumed vs. what was confirmed. |

**Net Assessment:** 5 of 6 dimensions show Negative impact from Pre-Mortem findings. This does not mean the configuration is poor — the implementation itself is correct. It means the configuration's **durability** is under-supported. The S-003 Steelman correctly identified that the implementation is production-ready; the Pre-Mortem identifies that the production-ready state is fragile without maintenance infrastructure.

**Estimated score impact of P0/P1 mitigations:** If PM-001 through PM-007 are addressed, Completeness, Methodological Rigor, Actionability, and Traceability shift to Positive or Neutral, representing an estimated +0.08 to +0.12 composite score improvement in a future S-014 scoring.

---

## Execution Statistics

- **Total Findings:** 11
- **Critical:** 2 (PM-001, PM-002)
- **Major:** 6 (PM-003 through PM-008)
- **Minor:** 3 (PM-009, PM-010, PM-011)
- **Protocol Steps Completed:** 6 of 6
- **H-16 Compliance:** S-003 output present at `reviews/181-182-s003-steelman.md` (confirmed)
- **H-15 Self-Review:** Applied before persistence
- **Temporal Perspective Shift:** "It is September 2026" frame applied in Step 2
- **Failure Categories Covered:** Technical (2), Process (2), Assumption (2), External (4), Resource (1)
- **P0 Findings:** 2 (must mitigate)
- **P1 Findings:** 6 (should mitigate)
- **P2 Findings:** 3 (monitor)

---

*Strategy: S-004 (Pre-Mortem Analysis)*
*Template: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Executed: 2026-03-14*
*Criticality: C4*
*Execution ID: 20260314T1500*
