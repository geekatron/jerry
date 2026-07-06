# Chain-of-Verification Report: PROJ-031 Phase 1 Deliverables — Iteration 3

**Strategy:** S-011 Chain-of-Verification
**Deliverables:** phase1-requirements.md, ADR-001-skeleton-derived-branch-strategy.md, ADR-002-ci-token-push-strategy.md
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group D — Blind, Independent)
**H-16 Compliance:** S-003 Steelman applied in prior iterations (confirmed via ORCHESTRATION_PLAN; this agent has not read prior adversary outputs per blindness constraint — indirect H-16 compliance accepted per S-011 template)
**Claims Extracted:** 8 | **Verified:** 2 | **Discrepancies:** 6 (0 Critical, 4 Major, 2 Minor)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verification verdict |
| [Findings Table](#findings-table) | All findings with severity |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, recommendation for each finding |
| [Recommendations](#recommendations) | Grouped by severity |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Verification Statistics](#verification-statistics) | Claim-level breakdown |

---

## Summary

Six of eight extracted traceability and claim-soundness checks revealed discrepancies. The four Major findings are concrete: (1) ADR-002's compensating-control table maps CC-6 to REQ-037 when the actual backing requirement is REQ-021, leaving a cross-document gap an implementer can follow to the wrong place; (2) the integrity-monitor workflow is specified with only `issues: write` but also needs `contents: read` to call the GitHub Releases API — a strictly-compliant implementation would fail at the Release-notes lookup step; (3) the R-001 dimension-(d) smoke test requires `geekatron/jerry@cowork-skeleton` to exist, but that branch is created in Phase 5, making the "required before Phase 5" gate self-defeating without a documented resolution; (4) GitHub Release notes are characterised as a "protected surface" against the RT-01 threat actor, but any repository collaborator with Write access (the RT-01 actor by definition) also has release-editing permission, enabling a simultaneous branch-and-notes forgery that the integrity model does not acknowledge. Two Minor findings cover a three-versus-two component mismatch between the blank-input tag-discovery glob and the allow-list regex, and an imprecise REQ-014 acceptance-criterion cross-reference. Verdict: **REVISE** — the four Major findings require targeted correction before the deliverables can be re-scored at >= 0.95.

---

## Findings Table

| ID | Claim (deliverable) | Source | Discrepancy | Severity | Affected Dimension |
|----|---------------------|--------|-------------|----------|--------------------|
| CV-001-it3 | ADR-002 CC table: CC-6 backed by REQ-037 | REQ-021 requirement text; ADR-002 §Compensating Controls | CC-6 (pre-deploy ruleset-coverage check) traces to REQ-021, not REQ-037; ADR-002 CC table says "REQ-037 (or sibling)" — the sibling is the correct answer but is unnamed | Major | Traceability |
| CV-002-it3 | Monitor workflow needs only `issues: write` (REQ-035, NFR-006) | GitHub Actions permissions model | `contents: read` is also required to call the GitHub Releases API (read Release notes SHA); declaring only `issues: write` sets all other permissions to `none` by GitHub's rules, causing the SHA-lookup step to fail with HTTP 403 | Major | Completeness |
| CV-003-it3 | Dimension (d) is "required before Phase 5" (REQ-034, R-001 §Verification Approach) | Phase-structure definition; ADR-001; REQ-034 text | Phase 5 creates the `cowork-skeleton` branch; dimension (d) requires installing `geekatron/jerry@cowork-skeleton`; the branch cannot exist before the Phase 5 scripts execute — the gate is circular with no documented resolution | Major | Internal Consistency |
| CV-004-it3 | GitHub Release notes are a "durable, off-branch, protected surface" for the integrity anchor (ADR-002 §Continuous Integrity Monitoring, ADR-001 §Tamper-Evidence) | GitHub repository permissions model | Any repository collaborator with Write access (the RT-01 actor: "any repository collaborator" per ADR-002 Risks table) also holds release-editing permission; a simultaneous branch-push and Release-notes edit would pass the SHA assertion — this attack vector is not acknowledged in the threat model | Major | Evidence Quality |
| CV-005-it3 | Blank-input tag-discovery glob `v[0-9]*.[0-9]*.[0-9]*` (ADR-001 pseudocode; REQ-036) vs allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` | ADR-001 §Regeneration Commit Determinism pseudocode; REQ-036 text | Discovery glob requires exactly 3 version components; allow-list permits 2 (patch optional); a tag `v1.0` passes validation but is not returned by the discovery command — inconsistency in the blank-input fallback path | Minor | Internal Consistency |
| CV-006-it3 | REQ-014 AC: "three independent guarantees documented in ADR-001/ADR-002" | ADR-001 full text; ADR-002 §Loop-Safety Argument | The Loop-Safety Argument section (all three guarantees numbered and defined) appears only in ADR-002; ADR-001 mentions force-push semantics but does not number or enumerate the three loop-safety guarantees; the joint reference in the AC overstates ADR-001's role | Minor | Traceability |

---

## Detailed Findings

### CV-001-it3: CC-6 Backing Requirement Incorrectly Identified as REQ-037 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-002 §Compensating Controls → Backing Requirements table; REQ-021; REQ-037 |
| **Strategy Step** | Step 4 — Consistency Check (cross-reference claim against source) |

**Claim (from deliverable):**

ADR-002 §Compensating Controls → Backing Requirements table, row CC-6:

> | CC-6 | Pre-deploy ruleset-coverage check (fail-fast on new push-blocking coverage) | **REQ-037** (or sibling) | P1 |

**Source document (REQ-037 requirement text):**

> "The `git push --force origin HEAD:cowork-skeleton` step SHALL be followed by a dedicated failure-detection step that executes on `if: failure()`. This step SHALL emit a structured diagnostic to `$GITHUB_STEP_SUMMARY` that includes: (a) the raw push exit code, (b) the git remote rejection message, and (c) an actionable pointer to ADR-002 §Branch-Protection Posture..."

**Independent verification (REQ-021 requirement text):**

> "The `cowork-skeleton` branch SHALL be configured as a CI-owned, unprotected branch... Pre-deploy verification SHALL confirm no active organization ruleset restricts force-push to `cowork-skeleton`; runtime detection SHALL surface an explicit error message if a newly-added ruleset ever blocks the push."

REQ-021 AC: "Pre-deploy: `gh api orgs/geekatron/rulesets` confirms no active ruleset targets `cowork-skeleton`..."

**Discrepancy:**

CC-6 is the pre-deploy ruleset-coverage check (run BEFORE the push to fail-fast if coverage has appeared). REQ-037 is the runtime failure-detection step that fires on `if: failure()` AFTER the push is rejected — this is CC-5, not CC-6. REQ-021 is the requirement that mandates the pre-deploy check. An implementer following the CC table to REQ-037 will find no language about a pre-deploy API call; the actual pre-deploy check is in REQ-021. The "or sibling" hedge in the ADR implies awareness of the imprecision but leaves the correct requirement unnamed.

The requirements' Traceability Summary does correctly place REQ-021 under STK-004 with the note "org-ruleset pre-check," so the backing requirement exists; the CC table just points to the wrong one.

**Recommendation:**

In ADR-002 §Compensating Controls table, change CC-6's backing requirement from "REQ-037 (or sibling)" to "REQ-021 (pre-deploy org-ruleset check)." Optionally add a cross-reference note: "CC-5 → REQ-037 (runtime detection); CC-6 → REQ-021 (pre-deploy check)." No change to the requirements document is needed.

---

### CV-002-it3: Monitor Workflow Missing `contents: read` Permission [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-035 requirement text and AC; NFR-006 requirement text and AC |
| **Strategy Step** | Step 4 — Consistency Check (claim against GitHub Actions permissions model) |

**Claim (from deliverable):**

REQ-035 (requirement text):

> "The monitor workflow SHALL declare `issues: write` in its `permissions:` block."

NFR-006 (requirement text):

> "The workflow SHALL declare `issues: write` in its `permissions:` block."

REQ-035 AC (e): "Monitor workflow `permissions:` block declares `issues: write`."

**Source document (GitHub Actions permissions model):**

GitHub documentation on the `permissions` key: "If you specify the access for any of these scopes, all of those that are not specified are set to `none`." The GitHub Releases API endpoint `GET /repos/{owner}/{repo}/releases` (used by `gh release view` / `gh release list`) requires the `contents` scope at `read` level to return data. A workflow declaring only `permissions: issues: write` will have `contents: none`; the Releases API call will return HTTP 403.

**Discrepancy:**

The monitor workflow must execute two distinct operations: (1) read the GitHub Release notes for the latest `v*` tag to retrieve the published SHA — requires `contents: read` via the Releases API; (2) create a GitHub issue on mismatch — requires `issues: write`. REQ-035 and NFR-006 only mandate `issues: write`. A strictly-compliant implementation declaring only the specified permission would fail at step (1) with a permissions error, making the entire tamper-detection logic unreachable. The `git rev-parse` and `git clone` operations do not require an explicit permissions scope (they use the GITHUB_TOKEN's inherent repository read access), but the Releases API call does.

**Recommendation:**

Add `contents: read` to the monitor workflow's mandatory permissions specification in REQ-035 and NFR-006. The corrected text should read: "The monitor workflow SHALL declare `contents: read` and `issues: write` in its `permissions:` block." Update both the requirement text and acceptance criterion (e) accordingly. No change to ADR-002 is needed (it does not enumerate the specific YAML fields).

---

### CV-003-it3: R-001 Dimension (d) Circular Dependency Unresolved [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-034 §Verification Approach; R-001 §Verification Approach; ORCHESTRATION_PLAN phase definitions |
| **Strategy Step** | Step 4 — Consistency Check (gate precondition against phase dependency order) |

**Claim (from deliverable):**

REQ-034 (requirement text):

> "(d) a direct CoWork plugin-install smoke test: install `geekatron/jerry@cowork-skeleton` in a running CoWork-compatible client and confirm the plugin loads without error within the 120-second timeout... dimension (d) MAY be deferred to Phase 4 completion if a CoWork runtime is unavailable before Phase 2; the artifact SHALL record 'DEFERRED — required before Phase 5' and Phase 5 is blocked until completed."

REQ-034 AC: "(d) documented result of `claude plugin marketplace add geekatron/jerry@cowork-skeleton`..."

**Source document (phase structure and ADR-001):**

ADR-001 §Related Decisions:
> "STORY-001 (Skeleton Regeneration Script) | REALIZED_BY | Implements the four-command generation + deterministic commit."
> "TASK-002 (Regenerate-and-Push Job) | REALIZED_BY | CI job that runs the generation and force-push."

The Allocation Matrix in requirements assigns STORY-001, TASK-002 to Phase 5/6 implementation. Phase 4 is documentation authoring. The `cowork-skeleton` branch is created by the Phase 5 generation script executing against a `v*` tag in CI (Phase 6).

**Discrepancy:**

Dimension (d) requires the URL `geekatron/jerry@cowork-skeleton` to resolve — meaning the branch must exist as a public GitHub branch. The branch is first created by the Phase 5/6 CI script. The deferred path says "required before Phase 5," but Phase 5 is precisely when the scripts that create the branch are authored and first executed. No documented step exists to create the branch BEFORE Phase 5 without the Phase 5 script. The requirement does not resolve this circularity: it cannot block Phase 5 on a test that requires Phase 5's output.

The practical resolution (manually create a test `cowork-skeleton` branch by running the generation commands locally before the CI integration) is not stated in any deliverable. Without this resolution, the gate is either unenforced (the deferred artifact records "DEFERRED" and Phase 5 proceeds) or circular (Phase 5 can't begin until the branch exists, but the branch requires Phase 5).

**Recommendation:**

Add a resolution clause to REQ-034 dimension (d) and the R-001 §Verification Approach. Recommended text: "Dimension (d) SHALL be performed using a manually-generated `cowork-skeleton` branch created by executing the Phase 5 generation script locally (dry-run, not CI-triggered) against a `v*` release tag, prior to merging the workflow file to `main`." This breaks the circularity by defining the test object as a local/manual branch created in Phase 5 authoring, with the actual CI automation (Phase 6) constituting final acceptance.

---

### CV-004-it3: "Protected Surface" Characterisation Overstated for RT-01 Actor [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-002 §Continuous Integrity Monitoring; ADR-001 §Tamper-Evidence |
| **Strategy Step** | Step 4 — Consistency Check (access-control claim against GitHub permissions model) |

**Claim (from deliverable):**

ADR-002 §Continuous Integrity Monitoring:

> "CI publishes the expected deterministic tip SHA for the release to a **durable, off-branch, protected surface** — the GitHub **Release notes** for the `v*` tag (Releases are governed by `main`/release permissions, not by the unprotected branch)."

ADR-001 §Tamper-Evidence:

> "CI establishes the reference value in a protected surface (Release notes governed by main/release permissions)"

**Source document (GitHub repository permission model):**

GitHub's documentation on repository permission levels: the "Write" permission level grants the ability to push to branches AND to create, edit, and delete releases and their assets. ADR-002 §Risks table describes the RT-01 threat actor as: "Direct malicious/erroneous push to the **unprotected** `cowork-skeleton` (no CI involvement)… **MED (any collaborator/compromised credential)**." A repository collaborator with Write access — the RT-01 actor by the ADR's own definition — therefore holds both branch-push permission and release-editing permission within the same access tier.

**Discrepancy:**

The deliverables characterise Release notes as a surface "governed by `main`/release permissions, not by the unprotected branch," implying Release notes are separately protected from branch write access. In GitHub's permission model, both capabilities (branch push and release edit) are bundled under the same "Write" access tier. An RT-01 actor who can push directly to the unprotected `cowork-skeleton` branch can simultaneously edit the corresponding Release notes to update the published SHA, making the tamper-detection assertion pass for the forged content. This attack path is not acknowledged anywhere in the three deliverables. The documents correctly state this is a detection model rather than prevention, but the characterisation of Release notes as "protected" understates the residual risk by implying a separation of access that does not exist in GitHub's model.

Note: The documents appropriately document the upgrade path (branch protection) for preventing tampering. The gap is specifically the missing acknowledgement that the detection model can be defeated by a motivated RT-01 actor who can edit both the branch and the Release notes in the same access tier.

**Recommendation:**

In ADR-002 §Continuous Integrity Monitoring, revise the characterisation: replace "a durable, off-branch, protected surface — the GitHub **Release notes** for the `v*` tag (Releases are governed by `main`/release permissions, not by the unprotected branch)" with language that acknowledges the shared access tier: "a durable off-branch reference surface — the GitHub Release notes for the `v*` tag. Note: Release editing requires the same Write repository access tier as branch push; an RT-01 actor with Write access can modify both simultaneously, defeating the SHA comparison. This residual attack path is bounded by the event-driven monitor's near-real-time detection window for the branch push; Phase 2 STRIDE decides whether the hook blast radius requires escalating to the prevention control (branch protection)." Add the same note to ADR-001 §Tamper-Evidence.

---

### CV-005-it3: Tag Discovery Glob Requires 3 Components; Allow-List Permits 2 [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Regeneration Commit Determinism (pseudocode); REQ-036 requirement text |
| **Strategy Step** | Step 4 — Consistency Check |

**Claim (from deliverable):**

ADR-001 pseudocode (blank-input path):

```bash
TAG="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1)"
```

REQ-036: "when `inputs.target_tag` is blank — from `git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname \| head -1`"

Allow-list (ADR-001 step 2, REQ-036): `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`

**Independent verification:**

The shell glob `v[0-9]*.[0-9]*.[0-9]*` (in `git tag -l`) uses `[0-9]*` to mean zero-or-more digits and `.` as a literal character; it requires **three** dot-separated numeric components (MAJOR.MINOR.PATCH). The regex allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` makes PATCH optional — it accepts both `v1.0` (two components) and `v1.0.0` (three components). A tag `v1.0` would pass the allow-list validation but would not be returned by the `git tag -l` discovery command in the blank-input path.

**Discrepancy:**

Minor inconsistency: a two-component tag that passes validation would be silently skipped by the blank-input discovery. In practice Jerry uses three-component semantic versioning, so `v1.0` would never be a release tag. The risk is theoretical but the inconsistency means the discovery and validation layers are not co-aligned.

**Recommendation:**

For consistency, align the `git tag -l` glob to match the allow-list: use `v[0-9]*.[0-9]*` (allowing two or three components) or add `(\.[0-9]*)?` to the glob pattern. Alternatively, note in REQ-036 and ADR-001 that the allow-list intentionally permits two-component tags as future-proofing while the discovery command is limited to three-component tags by project convention, and document the acceptable discrepancy.

---

### CV-006-it3: REQ-014 AC References ADR-001 for Loop-Safety Argument Not Present There [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-014 Acceptance Criterion; ADR-001 full text; ADR-002 §Loop-Safety Argument |
| **Strategy Step** | Step 4 — Consistency Check |

**Claim (from deliverable):**

REQ-014 AC:

> "Verified by Analysis (three independent guarantees documented in ADR-001/ADR-002) and Demonstration on a live test run."

**Independent verification (ADR-001 full text scan):**

ADR-001 contains no section titled "Loop-Safety Argument" and does not number or define the three independent guarantees. ADR-001 §Consequences mentions force-push semantics and the `GITHUB_TOKEN` non-retrigger property once in passing, but does not enumerate or argue the loop-safety conjunction. ADR-002 §Loop-Safety Argument is the section that defines guarantee (1) trigger shape, guarantee (2) listener shape, and guarantee (3) credential shape explicitly.

**Discrepancy:**

The REQ-014 AC implies the three guarantees are co-documented in ADR-001 and ADR-002. They are documented only in ADR-002. A reviewer verifying REQ-014 by reading ADR-001 alone would not find the loop-safety argument. The joint reference overstates ADR-001's contribution to this claim.

**Recommendation:**

Revise REQ-014 AC to: "Verified by Analysis (three independent guarantees documented in ADR-002 §Loop-Safety Argument) and Demonstration on a live test run." This is accurate and makes the cross-reference navigable.

---

## Recommendations

### Major (SHOULD correct before advancing to quality re-score)

| ID | Exact correction |
|----|-----------------|
| CV-001-it3 | ADR-002 CC table row CC-6: change "**REQ-037** (or sibling)" to "**REQ-021** (pre-deploy org-ruleset check — `gh api orgs/geekatron/jerry/rulesets/branches/cowork-skeleton` gate)" |
| CV-002-it3 | REQ-035 text and AC; NFR-006 text: add `contents: read` to the mandatory permissions specification. Corrected: "The monitor workflow SHALL declare `contents: read` and `issues: write` in its `permissions:` block." Update REQ-035 AC (e) to match. |
| CV-003-it3 | REQ-034 dimension (d) and R-001 §Verification Approach: add a resolution clause identifying the test object as a manually-generated branch produced by running the Phase 5 generation script locally (dry-run) before merging the CI workflow file. |
| CV-004-it3 | ADR-002 §Continuous Integrity Monitoring and ADR-001 §Tamper-Evidence: replace "protected surface" characterisation with language that acknowledges Write-tier access bundles both branch push and release edit, and explicitly names the simultaneous branch+notes forgery as an acknowledged residual attack path within the detection model. |

### Minor (MAY correct)

| ID | Exact correction |
|----|-----------------|
| CV-005-it3 | Align blank-input discovery glob with allow-list, or document the intentional discrepancy with a comment in the pseudocode. |
| CV-006-it3 | REQ-014 AC: change "ADR-001/ADR-002" to "ADR-002 §Loop-Safety Argument." |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CV-002-it3: monitor workflow permissions spec is incomplete (missing `contents: read`); the tamper-detection logic is unreachable with the specified permissions |
| Internal Consistency | 0.20 | Negative | CV-003-it3: the R-001 Phase 5 gate is internally inconsistent (gate requires output of Phase 5 to test it); CV-005-it3: tag discovery and allow-list use different component counts |
| Methodological Rigor | 0.20 | Neutral | The overall architecture is sound; the flaws are in specification precision, not in the threat model method |
| Evidence Quality | 0.15 | Negative | CV-004-it3: the "protected surface" characterisation of Release notes is unsupported by the GitHub permission model; ADR evidence base misrepresents the access-control separation |
| Actionability | 0.15 | Negative | CV-001-it3: implementers following the CC table to REQ-037 for CC-6 will not find the pre-deploy check implementation mandate; actionability is degraded for Phase 6 |
| Traceability | 0.10 | Negative | CV-001-it3: ADR-002 CC→REQ trace for CC-6 is wrong; CV-006-it3: REQ-014 AC cross-reference points to a document that does not contain the cited argument |

---

## Verification Statistics

| Claim | Question | Result | Finding |
|-------|----------|--------|---------|
| CL-001: CC-6 → REQ-037 | Does REQ-037 text mandate the pre-deploy ruleset-coverage check? | MATERIAL DISCREPANCY | CV-001-it3 (Major) |
| CL-002: Monitor fires on direct push, not GITHUB_TOKEN | Does GitHub's non-retrigger property apply to the event-driven monitor for a separate workflow? | VERIFIED | — |
| CL-003: Release notes are a "protected surface" against RT-01 | Do RT-01 actors (Write-tier collaborators) lack release-editing permission? | MATERIAL DISCREPANCY | CV-004-it3 (Major) |
| CL-004: Dimension (d) executable "before Phase 5" | Does `cowork-skeleton` branch exist before Phase 5 creates it? | MATERIAL DISCREPANCY | CV-003-it3 (Major) |
| CL-005: CC-1 through CC-8 all have backing SHALL requirements | Do all 8 CCs trace to a named backing requirement? | MINOR DISCREPANCY | CV-001-it3 (CC-6 maps to wrong REQ) — CCs are all covered but CC-6 mapping is imprecise |
| CL-006: Monitor only needs `issues: write` | Does a workflow declaring only `issues: write` have access to the GitHub Releases API? | MATERIAL DISCREPANCY | CV-002-it3 (Major) |
| CL-007: Tag discovery glob matches allow-list | Does `v[0-9]*.[0-9]*.[0-9]*` match all tags the allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` would accept? | MINOR DISCREPANCY | CV-005-it3 (Minor) |
| CL-008: Loop-safety argument in ADR-001/ADR-002 | Does ADR-001 contain the three-guarantee loop-safety argument? | MINOR DISCREPANCY | CV-006-it3 (Minor) |

**Verification rate:** 1/8 VERIFIED, 4/8 MATERIAL DISCREPANCY, 3/8 MINOR DISCREPANCY

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 0
- **Major:** 4
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

---

*S-011 Chain-of-Verification execution — adv-executor (Group D, Blind, Independent)*
*Strategy template: `.context/templates/adversarial/s-011-cove.md` v1.0.0*
*Deliverables reviewed: iteration-3 versions only (blindness maintained)*
*Project: PROJ-031-cowork-skeleton / QG-1 Iteration 3*
*H-15 self-review applied before persistence*
