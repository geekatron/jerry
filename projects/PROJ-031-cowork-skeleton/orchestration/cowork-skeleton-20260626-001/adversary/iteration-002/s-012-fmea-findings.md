# FMEA Report: PROJ-031 Phase 1 Design Package — Iteration 2

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (iteration 2)
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` (iteration 2)
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` (iteration 2)
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group E — Decompose; blind independent review)
**H-16 Compliance:** S-003 Steelman applied in iteration-002 sequence (confirmed by presence of `s-003-steelman-findings.md` in `iteration-002/`)
**Elements Analyzed:** 9 | **Failure Modes Identified:** 13 | **Total RPN:** 2,087

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Element Inventory](#element-inventory) | 9 decomposed elements |
| [Findings Table](#findings-table) | All 13 failure modes with S/O/D/RPN |
| [Detailed Findings](#detailed-findings) | Expanded analysis for Critical and Major findings |
| [Recommendations](#recommendations) | Corrective actions by severity |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

The iteration-2 design package substantially addresses the structural gaps identified in iteration 1 — specifically the canonical plugin-retention surface reconciliation, the three-dimensional R-001 verification gate, stub static-content constraint, staleness detection, inputs.target_tag, and the org-ruleset empirical inventory. Nine discrete elements were analyzed across 13 failure modes.

Three Critical findings remain after iteration-2 remediation: (1) a pre-publication SHA integrity gate described in the ADRs has no corresponding SHALL requirement in the requirements document, leaving it implementation-optional (RPN 280); (2) the R-001 three-dimensional gate measures proxies — not actual CoWork runtime behavior — creating a detection-escape path where all three gate dimensions pass while CoWork still rejects installation (RPN 252); and (3) the staleness-detection workflow specified in NFR-006 uses only the `Source-Commit:` commit-message trailer, which is trivially forgeable by a direct push to the unprotected branch and provides no tree-content verification (RPN 224).

Nine Major findings cover: no CI lint gate enforcing static stub content on every build (FM-004, RPN 196), absence of a continuous SHA-assertion requirement (FM-005, RPN 168), no periodic post-job tree-integrity monitoring (FM-006, RPN 168), clone-time estimate using an optimistic 10 Mbps reference (FM-007, RPN 168), undefined "blank inputs.target_tag → latest tag" resolution behavior (FM-008, RPN 144), marketplace.json relative-path resolution not verified at CoWork runtime (FM-009, RPN 144), missing explicit requirement for inputs.target_tag allow-list validation (FM-010, RPN 108), validation-step ordering not specified relative to force-push (FM-012, RPN 105), and pre-deploy ruleset check querying only org rulesets, not repo rulesets (FM-011, RPN 90).

**Recommendation: REVISE.** The Critical findings (FM-001, FM-002, FM-003) require corrective action before acceptance. At least FM-001 and FM-003 can be resolved with targeted requirements additions; FM-002 requires an architectural acknowledgment or scope commitment to direct CoWork empirical testing.

---

## Element Inventory

| ID | Element | Source |
|----|---------|--------|
| E-01 | R-001 Assumption and Verification Gate | requirements §Stated Assumption, REQ-034 |
| E-02 | Idempotency Chain | REQ-003, REQ-004a, NFR-001, NFR-002 |
| E-03 | Skeleton Generation Logic | REQ-001–REQ-010, ADR-001 Option A |
| E-04 | CI Workflow Automation | REQ-011–REQ-018, NFR-003–NFR-005 |
| E-05 | Security Controls and Loop-Safety | REQ-019–REQ-023, ADR-002 §Loop-Safety |
| E-06 | Staleness Detection | NFR-006 |
| E-07 | Metadata Pinning and Commit Determinism | ADR-001 §Regeneration Commit Determinism |
| E-08 | Branch-Protection and Integrity Posture | ADR-002 §Branch-Protection Posture, c-107 |
| E-09 | Canonical Plugin-Retention Surface | ADR-001 c-003, REQ-005, REQ-010 |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260626T1700 | E-08 | Pre-publication SHA integrity gate described in ADRs has no SHALL requirement in requirements doc | 7 | 5 | 8 | 280 | Critical | Add REQ-035: the CI workflow SHALL assert the published branch tip SHA equals the independently-recomputable deterministic SHA before advertising the branch as installable | Completeness |
| FM-002-20260626T1700 | E-01 | R-001 three-dimensional gate uses proxies; CoWork rejects even when all three dimensions pass (detection escape) | 9 | 4 | 7 | 252 | Critical | Add REQ-034d: one of the three gate dimensions SHALL be a direct CoWork plugin install attempt on a test machine, not only a mathematical estimate | Methodological Rigor |
| FM-003-20260626T1700 | E-06 | Staleness-check (NFR-006) verifies only Source-Commit trailer; trailer is forgeable by direct push; no tree-content verification | 7 | 4 | 8 | 224 | Critical | Revise NFR-006 to additionally compare `git diff $(git ls-remote origin cowork-skeleton \| cut -f1) $expected_sha` or check committer identity, not only the trailer | Methodological Rigor |
| FM-004-20260626T1700 | E-07 | Static stub constraint (REQ-004a) lacks CI lint gate; STORY-002 author may introduce dynamic content without CI catching it | 7 | 4 | 7 | 196 | Major | Add a CI step (in generation script or pre-push validation) that greps stub file for known dynamic patterns (ISO-8601, GITHUB_RUN_ID, GITHUB_SHA, {{ }}, version string patterns) and exits non-zero on match | Completeness |
| FM-005-20260626T1700 | E-02 | No SHA-assertion requirement on every CI run; REQ-003 AC is a V&V acceptance test, not a continuous CI gate | 6 | 4 | 7 | 168 | Major | Promote ADR-001's aspirational "CI assertion where feasible" to a SHALL: add a generation-script final step that recomputes the expected SHA from the known inputs and asserts it matches the generated commit SHA | Internal Consistency |
| FM-006-20260626T1700 | E-08 | No periodic post-job tree-content monitoring; after CI completes, a direct collaborator push can replace branch content; not caught until next CI run | 7 | 3 | 8 | 168 | Major | Add NFR for a post-publication tree-integrity check to the staleness workflow: compute expected SHA from latest tag and assert live branch tip matches, using the same deterministic generator logic | Completeness |
| FM-007-20260626T1700 | E-01 | Clone-time estimate uses 10 Mbps reference network; CoWork users on slower connections (2–5 Mbps) may timeout even when gate passes | 7 | 4 | 6 | 168 | Major | Revise REQ-034 to require testing at multiple bandwidths (10 Mbps and 2 Mbps reference); or require a direct CoWork install-timing test; reference CoWork timeout as 120 s absolute, not just against 10 Mbps | Methodological Rigor |
| FM-008-20260626T1700 | E-04 | inputs.target_tag blank behavior "defaults to latest pushed tag" is undefined; which mechanism resolves "latest" and whether it races with concurrent tag pushes is unspecified | 6 | 4 | 6 | 144 | Major | REQ-011 SHALL specify the resolution mechanism when inputs.target_tag is blank: either git describe --tags --abbrev=0 --match 'v*', or equivalent, and require that the resolved tag undergoes the same allow-list validation as GITHUB_REF_NAME | Actionability |
| FM-009-20260626T1700 | E-09 | marketplace.json `source: "./"` relative-path resolution not verified at CoWork runtime; REQ-005 AC verifies file presence but not that path resolves in a CoWork plugin load | 8 | 3 | 6 | 144 | Major | Add to REQ-026 AC (or a new REQ): a STORY-003 acceptance test SHALL attempt a full CoWork plugin install from the generated branch in a test environment and confirm the marketplace resolution succeeds (not only that the file is present in git ls-files) | Evidence Quality |
| FM-010-20260626T1700 | E-05 | inputs.target_tag is attacker-influenceable (write-access workflow_dispatch trigger) but no requirement explicitly mandates allow-list validation for this input (ADR-001 §Tag-name sanitization refers to GITHUB_REF_NAME) | 6 | 3 | 6 | 108 | Major | Extend ADR-001 §Tag-name sanitization and add an explicit requirement: the generation script SHALL validate inputs.target_tag against the same allow-list regex `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` as GITHUB_REF_NAME before using it in any shell expansion or commit message | Methodological Rigor |
| FM-012-20260626T1700 | E-09 | Validation step ordering for REQ-005/REQ-010 (directory presence, agent-path checks) not specified relative to force-push; a script bug stripping .claude-plugin/ could be pushed before checks run | 7 | 3 | 5 | 105 | Major | REQ-005 and REQ-010 SHALL explicitly state that the validation asserts run as automated in-workflow steps BEFORE the force-push (matching the REQ-022 pre-push diff gate pattern) | Completeness |
| FM-011-20260626T1700 | E-05 | REQ-021 AC queries only org rulesets (`gh api orgs/geekatron/rulesets`); a future repo-level ruleset targeting cowork-skeleton would not be caught by the pre-deploy check | 5 | 3 | 6 | 90 | Major | Revise REQ-021 AC to also check repo-level rulesets: `gh api repos/geekatron/jerry/rulesets/branches/cowork-skeleton` or `gh ruleset check cowork-skeleton`; both org and repo scopes must be clean | Completeness |
| FM-013-20260626T1700 | E-03 | git rm -r edge cases (symlinks in projects/, pathological file names); very low risk given git rm -r semantics operate on git index entries not filesystem paths | 4 | 2 | 5 | 40 | Minor | Document in STORY-001: generation script SHALL use `git rm -r --force projects/` (not rm -rf) to operate on the git index; note that git rm follows index entries, not filesystem symlinks | Methodological Rigor |

**Total RPN:** 280 + 252 + 224 + 196 + 168 + 168 + 168 + 144 + 144 + 108 + 105 + 90 + 40 = **2,087**

---

## Detailed Findings

### FM-001-20260626T1700: Integrity Gate Without a Requirement

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-08 — Branch-Protection and Integrity Posture (ADR-002 §Branch-Protection Posture, c-107) |
| **S / O / D** | 7 / 5 / 8 |
| **RPN** | 280 |
| **Strategy Step** | Step 2 (Missing lens) |

**Evidence:**
ADR-002 c-107 states: "artifact integrity MUST rest on a compensating control (deterministic-SHA tamper-evidence + pre-publication integrity gate)." ADR-001 §Tamper-Evidence says: "add a pre-publication integrity gate that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable." ADR-002 §Branch-Protection Posture states: "Pre-publication integrity gate (required)."

However, `phase1-requirements.md` contains no SHALL requirement that corresponds to this gate. REQ-022 requires an in-workflow pre-push equivalence check on the GENERATED tree (before pushing). REQ-033 requires user approval before irreversible actions. Neither captures the post-push, pre-advertisement integrity assertion the ADR design mandates.

**Analysis:**
The ADRs design an integrity property whose operationalization lives in a requirement that does not exist. Without a SHALL, STORY-001/TASK-002 implementers are not contractually required to build this gate. Additionally, the ADR-001 description of the pre-publication gate as an assertion "inside the CI job immediately after force-push" means it is effectively a self-check: the job asserting its own push succeeded. The more valuable assertion — independently recomputing the expected SHA and comparing — is described as publishing the expected SHA in GitHub Release notes, but no REQ requires this either.

**Recommendation:**
Add REQ-035 (WS-5 or WS-2): "Before `cowork-skeleton` is referenced as installable in any GitHub Release body or plugin registry entry, the CI workflow SHALL assert that `git rev-parse origin/cowork-skeleton` equals the independently-recomputed deterministic SHA for the triggering release tag. The independent SHA SHALL be computed by re-running the generation logic offline against the same source tag and comparing." Acceptance criterion: demonstrate that a direct push to `cowork-skeleton` (simulating RT-01) causes the next pre-publication assertion to fail and the release note is NOT updated.

**Post-correction RPN estimate:** 7 × 2 × 5 = 70 (Major → Minor)

---

### FM-002-20260626T1700: R-001 Three-Dimensional Gate — Detection Escape

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-01 — R-001 Assumption and Verification Gate (requirements §Stated Assumption, REQ-034) |
| **S / O / D** | 9 / 4 / 7 |
| **RPN** | 252 |
| **Strategy Step** | Step 2 (Insufficient lens) |

**Evidence:**
REQ-034 requires a three-dimensional verification: (a) tracked file count `git ls-files | wc -l` < 5,000; (b) compressed pack size `git count-objects -vH size-pack` in MB; (c) estimated clone time in seconds vs. 120s threshold. ADR-001 §L2 ¶4 says: "if and only if clone timing becomes a problem, switching to Option B is a one-line, pre-designed change." R-001 §Statement says: "The CoWork plugin-load file-count limit is approximately 5,000 files, and that limit applies to the tracked file count of a clean-clone working tree."

**Analysis:**
All three gate dimensions are measurements or estimates made on the implementer's test environment — none requires executing an actual CoWork plugin installation. The gate can pass (file count < 5,000, pack < 250 MB, estimated time < 120s) while CoWork still fails to install because:
1. The actual limit may not be exactly 5,000 — it is described as "approximately 5,000"; a binary-round limit of 4,096 or a true limit of 4,999 would make the ~1,744-file skeleton pass but expose cases where the margin is consumed by future additions.
2. CoWork may measure "files in the checkout plus .git directory overhead" or "files visible to the file watcher" rather than `git ls-files` tracked files.
3. The clone-time estimate is mathematical (pack size / bandwidth), not measured against CoWork's actual git client behavior, which includes negotiation, delta computation, and checkout phases.
4. CoWork may apply the limit per-plugin-agent-load or during a caching phase, not during the initial git clone.

REQ-034's three dimensions are necessary but not sufficient to confirm CoWork will accept installation.

**Recommendation:**
Add REQ-034d: "One dimension of the R-001 verification SHALL be a direct CoWork plugin-install attempt: install `geekatron/jerry@cowork-skeleton` in a Claude Desktop environment (or equivalent CoWork simulator) and confirm the plugin loads without error, within the 120-second timeout, on a reference machine with a measured 10 Mbps connection." Without this, the gate provides detection for the proxy measurements but not for the actual installability criterion the project depends on. The R-001 score should remain 3×5=15 YELLOW until this direct test is added.

**Post-correction RPN estimate:** 9 × 2 × 3 = 54 (drops from Critical once direct test is performed)

---

### FM-003-20260626T1700: Staleness-Check Forgeability

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-06 — Staleness Detection (NFR-006) |
| **S / O / D** | 7 / 4 / 8 |
| **RPN** | 224 |
| **Strategy Step** | Step 2 (Insufficient lens) |

**Evidence:**
NFR-006 states: "It SHALL compare the `Source-Commit:` trailer in `git log -1 cowork-skeleton` to the full SHA of the latest `v*` tag on `main` and SHALL fail visibly — producing a GitHub Actions job failure or creating a GitHub issue — if they diverge." The Source-Commit trailer is part of the commit message, which is controlled entirely by whoever authored the commit.

**Analysis:**
The `cowork-skeleton` branch is explicitly unprotected (ADR-002 Decision: "keep `cowork-skeleton` UNPROTECTED"). A repository collaborator with push access can create a commit with any commit message they choose, including a forged `Source-Commit: <latest-v*-tag-sha>` trailer. The staleness-detection workflow would then:
1. Read `git log -1 cowork-skeleton | grep "Source-Commit:"` → returns the forged value
2. Compare to latest v* tag SHA → matches (because it was forged)
3. Report: no staleness detected

The workflow would pass even though the branch content is entirely wrong (stale, tampered, or arbitrary). The staleness check as specified by NFR-006 is a commit-message-based check, not a tree-content check. This is a significant detection gap for the RT-01 threat (direct-push attack) that ADR-002 acknowledges.

**Recommendation:**
Revise NFR-006 to require at minimum one content-based verification alongside the trailer check. Options:
1. Compare `git rev-parse cowork-skeleton` to the independently-recomputed deterministic SHA for the latest `v*` tag (same as FM-001's recommended gate, combined). This catches any content deviation.
2. Alternatively, compare `git log -1 --format="%ae" cowork-skeleton` to `41898282+github-actions[bot]@users.noreply.github.com` to verify committer identity. A direct push by a human committer would have a different email, regardless of commit message.

Option 1 is stronger and aligns with the deterministic SHA design. Combined with FM-001's integrity gate, both the CI publication check and the weekly staleness check would verify tree content, not just message content.

**Post-correction RPN estimate:** 7 × 2 × 3 = 42 (drops to Minor when content-based check added)

---

### FM-004-20260626T1700: Generator Non-Determinism — No CI Lint on Stub Content

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-07 — Metadata Pinning and Commit Determinism (ADR-001 §Regeneration Commit Determinism) |
| **S / O / D** | 7 / 4 / 7 |
| **RPN** | 196 |
| **Strategy Step** | Step 2 (Missing lens) |

**Evidence:**
REQ-004a states: "The `projects/README.md` sentinel file SHALL contain only static prose — no timestamps, version strings, build identifiers, run numbers, or any generated value." REQ-004a AC: "grep for patterns matching ISO 8601 timestamps, `GITHUB_RUN_ID`, `GITHUB_RUN_NUMBER`, `GITHUB_SHA`, `{{ }}`, or build identifiers returns empty." This is an inspection AC — it verifies the stub ONCE (during STORY-002 authoring and V&V). There is no CI gate that runs this grep on every generation invocation. ADR-001 §Stub Determinism Constraint says: "Stub authoring is STORY-002; this ADR fixes only its determinism property."

**Analysis:**
If STORY-002 correctly authors a static stub, the constraint is satisfied at authorship time. But if the generation script ever writes the stub dynamically (e.g., including a build date as "helpful context" for users), no CI mechanism catches this before the bit-identical SHA guarantee silently breaks. The SHA would differ between runs for the same tag, invalidating tamper-detection. The only existing detection path is the REQ-003 AC (two workflow_dispatch runs for the same tag), which is a V&V test run manually, not a per-run CI assertion.

**Recommendation:**
Add a generation-script step (owned by STORY-001/TASK-002) that runs before `git commit`: `grep -E '([0-9]{4}-[0-9]{2}-[0-9]{2}|GITHUB_RUN|GITHUB_SHA|\{\{)' projects/README.md && { echo "Stub contains dynamic content; failing."; exit 1; }`. This converts the one-time inspection AC into a continuous per-run guard.

**Post-correction RPN estimate:** 7 × 4 × 2 = 56 (O unchanged; D drops to 2 with CI gate)

---

### FM-005-20260626T1700: No Continuous SHA-Assertion Requirement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-02 — Idempotency Chain (REQ-003, NFR-001) |
| **S / O / D** | 6 / 4 / 7 |
| **RPN** | 168 |
| **Strategy Step** | Step 2 (Missing lens) |

**Evidence:**
ADR-001 §Regeneration Commit Determinism states: "Pin all metadata in the generation script; CI SHA assertion; do not GPG-sign." Under Risks: "Idempotency drift from un-pinned commit metadata — LOW — Pin all metadata in the generation script; CI SHA assertion where feasible." REQ-003 AC requires two separate workflow_dispatch runs returning an identical SHA — this is a one-time V&V acceptance test. No REQ or NFR mandates an automated SHA assertion on every single generation run.

**Analysis:**
The bit-identical SHA guarantee has five pinned inputs: tree, parent, identity, author/committer dates, and commit message. A future maintenance change to the commit message template (e.g., adding a helpful line) silently breaks idempotency. Without a per-run SHA assertion, this drift is invisible until the next manual V&V acceptance re-run. The ADR recognizes this ("CI SHA assertion") but expresses it as aspirational rather than required.

**Recommendation:**
Add a requirement: "The generation script SHALL, on every invocation, recompute the expected commit SHA from its known fixed inputs (source tag SHA, fixed message template, pinned dates, fixed identity, fixed parent) and assert equality with the actual commit SHA produced, emitting a non-zero exit if they differ." This converts the aspirational ADR note into a deterministic CI gate.

**Post-correction RPN estimate:** 6 × 4 × 2 = 48 (D drops to 2 with on-every-run assertion)

---

### FM-006-20260626T1700: No Periodic Post-Job Tree-Content Monitoring

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-08 — Branch-Protection and Integrity Posture |
| **S / O / D** | 7 / 3 / 8 |
| **RPN** | 168 |
| **Strategy Step** | Step 2 (Missing lens) |

**Evidence:**
ADR-002 §Integrity for unsigned, unprotected branch: "Pre-publication integrity gate (required). Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>` for the release tag." This gate runs INSIDE the CI job. After the job completes, the branch is publicly accessible. NFR-006 runs weekly but checks only the Source-Commit trailer (see FM-003). No requirement mandates a post-job tree-content integrity check.

**Analysis:**
The threat RT-01 (direct malicious/erroneous push to unprotected `cowork-skeleton`) produces content visible to CoWork users between the direct push and the next CI regeneration (up to the next release cycle). The staleness check (NFR-006) would not catch this if the forged commit has the correct trailer (FM-003). The pre-publication gate inside the CI job is a one-time check at generation time, not an ongoing monitor. Between releases, tampered content on `cowork-skeleton` persists with no automated detection.

**Recommendation:**
Extend NFR-006 to require, in addition to the staleness trailer comparison: compare `git rev-parse origin/cowork-skeleton` to the deterministic SHA recomputable from `Source-Tag:` (extracted from the latest trailer). If the SHA does not match, fail visibly. This adds continuous tree-content integrity monitoring to the weekly staleness run, not only a trailer-based freshness check.

**Post-correction RPN estimate:** 7 × 3 × 3 = 63 (D drops with tree-content check)

---

### FM-007-20260626T1700: Clone-Time Estimate Uses Optimistic 10 Mbps Reference

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-01 — R-001 Assumption and Verification Gate |
| **S / O / D** | 7 / 4 / 6 |
| **RPN** | 168 |
| **Strategy Step** | Step 3 (Insufficient rating for detection) |

**Evidence:**
ADR-001 Consequences §Negative: "Measurable fallback trigger: switch to Option B (orphan) at >60 s clean-clone (50% of 120 s) or >250 MB pack on a 10 Mbps reference link." REQ-034 requires recording "estimated clone time on a reference network connection in seconds, compared against CoWork's documented 120-second threshold." R-001 §Verification Approach references "a reference network connection." The reference is stated as 10 Mbps in ADR-001.

**Analysis:**
10 Mbps is approximately the 30th–40th percentile of US broadband speeds and is above typical rural, mobile, or international connections. A user on a 2 Mbps connection (common outside urban US) would experience clone times 5× longer than the 10 Mbps reference. If the pack size is 60 MB (which passes the 250 MB threshold comfortably), the 10 Mbps estimate is 60/10 × 8 ≈ 48 s (well under 120 s) but the 2 Mbps actual time would be 240 s, exceeding CoWork's timeout. The gate would PASS at 10 Mbps reference while CoWork times out for a significant fraction of real-world users. The fallback trigger (>60 s on 10 Mbps or >250 MB pack) has asymmetric user coverage.

**Recommendation:**
Revise REQ-034 to require clone-time estimation at both 10 Mbps AND 2 Mbps (representing the bottom quartile of global broadband). Alternatively, accept that Option B (orphan branch) may be necessary to serve low-bandwidth users regardless of the 10 Mbps gate result, and note this in the R-001 documented fallback. Document the bandwidth coverage explicitly: "this gate passes for users with >= 10 Mbps connections; users below this bandwidth will experience longer clone times up to [X] seconds at [Y] Mbps."

**Post-correction RPN estimate:** 7 × 3 × 4 = 84 (O drops once explicit coverage statement is added; D improves)

---

### FM-008-20260626T1700: inputs.target_tag Blank-Resolution Behavior Undefined

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-04 — CI Workflow Automation |
| **S / O / D** | 6 / 4 / 6 |
| **RPN** | 144 |
| **Strategy Step** | Step 2 (Ambiguous lens) |

**Evidence:**
REQ-011 declares: "The `workflow_dispatch` trigger SHALL declare an optional `inputs.target_tag` parameter (description: 'v* release tag to regenerate from; defaults to latest pushed tag if blank')." No requirement or ADR specifies the mechanism that resolves "latest pushed tag" when `inputs.target_tag` is blank. The REQ-011 description is in the parameter description string, not in the requirement body.

**Analysis:**
When `workflow_dispatch` is triggered via the GitHub UI with `inputs.target_tag` blank, the workflow must determine which tag to build from. Possible resolutions: `git describe --tags --abbrev=0 --match 'v*'` (latest reachable tag), `git tag -l 'v*' --sort=-version:refname | head -1` (latest by version sort), or `GITHUB_REF_NAME` (which for workflow_dispatch is the branch ref, not a tag). If the resolution uses GITHUB_REF_NAME and the dispatch is triggered from branch `main`, GITHUB_REF_NAME is `main`, not a tag — causing the allow-list validation to fail and the job to abort. Alternatively, if the blank behavior uses `git describe --tags`, it would return the most recent tag from the checkout's commit history, which may not be the latest pushed tag if the checkout is at `fetch-depth: 1`.

**Recommendation:**
REQ-011 SHALL explicitly specify the blank-target-tag resolution: "When `inputs.target_tag` is blank, the workflow SHALL resolve the tag by executing `git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1` against a full `fetch-depth: 0` clone, and SHALL validate the resolved tag against the same allow-list regex as GITHUB_REF_NAME before proceeding." This must be in the requirement body (not only the parameter description) and must require allow-list validation of both the blank-resolved and explicitly-provided cases.

**Post-correction RPN estimate:** 6 × 2 × 4 = 48

---

### FM-009-20260626T1700: marketplace.json Relative-Path Resolution Not Verified at CoWork Runtime

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-09 — Canonical Plugin-Retention Surface |
| **S / O / D** | 8 / 3 / 6 |
| **RPN** | 144 |
| **Strategy Step** | Step 2 (Insufficient lens) |

**Evidence:**
REQ-026 states: "The Tutorial SHALL instruct users to install the marketplace via `claude plugin marketplace add geekatron/jerry@cowork-skeleton` and SHALL NOT suggest adding the marketplace via a direct URL." REQ-026 rationale: "`source: './'` in `plugin.json` is a relative path that resolves only when added via the Git-based form; a raw-URL marketplace add silently fails." REQ-005 AC: "`git ls-files .claude-plugin/marketplace.json` returns non-empty." REQ-010 AC: "Every `path:` entry in `.claude-plugin/plugin.json` agent declarations resolves to a file present in `git ls-files` on `cowork-skeleton`."

**Analysis:**
REQ-005 verifies `marketplace.json` EXISTS in the generated branch tree. REQ-010 verifies plugin.json agent path entries exist. Neither requirement verifies that `source: "./"` in `marketplace.json` RESOLVES correctly when CoWork loads the plugin. The resolution depends on CoWork's implementation of the relative-path semantics during plugin registration. If CoWork resolves `./` relative to a working directory OTHER than the git-clone root (e.g., relative to a cache path or a temporary extraction directory), the relative path fails silently. The existing documentation REQ-026 prevents the wrong install command, but no requirement verifies that the CORRECT install command produces a working plugin in an actual CoWork environment.

**Recommendation:**
Add to STORY-003 (Validation and Acceptance) a mandatory direct-install V&V step: "Execute `claude plugin marketplace add geekatron/jerry@cowork-skeleton` in an actual Claude Desktop or CoWork environment and verify the plugin registers successfully with all agent paths resolved." This requirement should appear in REQ-034 or as a new REQ-035 V&V step rather than remaining implicit in STORY-003. The `marketplace.json` relative-path resolution gap is the same risk that REQ-026's install-command restriction mitigates at the documentation level, but it requires an integration test to verify, not only a presence check.

**Post-correction RPN estimate:** 8 × 1 × 4 = 32 (O drops to 1 once direct install test passes)

---

### FM-010-20260626T1700: inputs.target_tag Allow-List Validation Not Explicitly Required

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-05 — Security Controls and Loop-Safety |
| **S / O / D** | 6 / 3 / 6 |
| **RPN** | 108 |
| **Strategy Step** | Step 2 (Missing lens) |

**Evidence:**
ADR-001 §Tag-name sanitization (RT-04): "The generation script MUST validate the tag against the strict allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and abort on any non-match." The text refers specifically to `github.ref_name` and `GITHUB_REF_NAME` throughout. REQ-011 describes `inputs.target_tag` as an input parameter but does not include a security validation requirement. No WS-3 requirement explicitly names `inputs.target_tag` as a surface requiring allow-list validation.

**Analysis:**
`inputs.target_tag` enters the workflow via `${{ inputs.target_tag }}` — the same GitHub expression expansion that ADR-001's sanitization section warns about for `github.ref_name`. If the generation script conditionally sets `TAG="${{ inputs.target_tag }}"` (when not blank) and this expression is embedded directly in the `run:` block shell script BEFORE the allow-list validation fires, it is susceptible to the same shell-injection vector described in ADR-001's RT-04 analysis. A write-access collaborator could pass `; malicious_command; echo v0` as the target_tag to inject shell commands (before validation runs, if the value is evaluated in the wrong order). The allow-list validation must be applied BEFORE the value is used in any shell context.

**Recommendation:**
Extend ADR-001 §Tag-name sanitization to explicitly include `inputs.target_tag`: "Both `GITHUB_REF_NAME` (for tag-push trigger) and `inputs.target_tag` (for workflow_dispatch trigger) SHALL be validated against the allow-list regex before any other use. The value SHALL be assigned to a shell variable and the validation SHALL run before the variable is referenced in any other command." Add a corresponding WS-3 or WS-2 requirement to enforce this in the CI workflow YAML.

**Post-correction RPN estimate:** 6 × 2 × 3 = 36

---

### FM-012-20260626T1700: Manifest/Directory Validation Timing Not Specified Relative to Force-Push

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-09 — Canonical Plugin-Retention Surface |
| **S / O / D** | 7 / 3 / 5 |
| **RPN** | 105 |
| **Strategy Step** | Step 2 (Missing / Ambiguous lens) |

**Evidence:**
REQ-022 explicitly requires: "This equivalence check SHALL run as an automated in-workflow step BEFORE the force-push step." REQ-005 (8-directory presence check + marketplace.json) AC and REQ-010 (plugin.json agent paths) AC specify what to verify but do NOT state when the check runs relative to the force-push. REQ-006 (file-count assertion: exit non-zero if count >= 5,000) is part of the generation SCRIPT and implicitly runs before push. REQ-009 (symlink resolution) AC does not specify timing.

**Analysis:**
If REQ-005 and REQ-010 are implemented as post-push V&V acceptance tests (run by the STORY-003 team after the branch exists), a script bug that accidentally executes `git rm -r .claude-plugin/` (quoting or globbing error in the generation script) would: (1) run, (2) produce a commit missing .claude-plugin/, (3) force-push successfully (REQ-022's diff gate verifies against source tag minus projects/ — but if the equivalence check doesn't catch .claude-plugin/ absence because the diff comparison may itself be confused), (4) users install a broken plugin, (5) V&V then detects the issue post-publication.

The risk is moderate: REQ-022's pre-push diff gate (`git diff v{N}..cowork-skeleton -- ':!projects/'`) WOULD catch missing .claude-plugin/ because it would show a deletion in the diff, causing a non-empty diff and aborting the push. But this depends on REQ-022's diff command including all retained directories in scope.

**Recommendation:**
REQ-005 and REQ-010 SHALL explicitly state: "This validation SHALL run as an automated in-workflow step BEFORE the force-push step (same timing requirement as REQ-022)." Alternatively, explicitly note that REQ-022's pre-push diff gate subsumes REQ-005/REQ-010 validation and close these as redundant-but-explicit. Either resolution removes the ambiguity.

**Post-correction RPN estimate:** 7 × 3 × 2 = 42

---

### FM-011-20260626T1700: Pre-Deploy Ruleset Check Queries Only Org Rulesets

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-05 — Security Controls |
| **S / O / D** | 5 / 3 / 6 |
| **RPN** | 90 |
| **Strategy Step** | Step 2 (Insufficient lens) |

**Evidence:**
REQ-021 AC: "Pre-deploy: `gh api orgs/geekatron/rulesets` confirms no active ruleset targets `cowork-skeleton` (current empirical result: the only active ruleset 'Don't fuck with main' targets `~DEFAULT_BRANCH` only)." The empirical inventory in ADR-002 correctly checked BOTH org rulesets (`HTTP 404`) AND repo rulesets (one ruleset: `"Don't fuck with main"` targeting `~DEFAULT_BRANCH`). However, the REQ-021 AC only names the org-level API endpoint (`gh api orgs/geekatron/rulesets`), not the repo-level endpoint.

**Analysis:**
A future repository admin could add a repo-level ruleset targeting `cowork-skeleton` (e.g., adding `non_fast_forward` protection) without adding an org-level ruleset. The pre-deploy check in REQ-021 AC would query org rulesets → 404 (no org rulesets) → conclude "no blocking ruleset" → proceed to force-push → fail at the actual push → runtime push-failure detection (second compensating control in REQ-021) catches it. The gap is not catastrophic (runtime detection fires), but the pre-deploy check would give a false "clear" result, meaning the warning comes from the actual push failure rather than the cleaner pre-deploy diagnosis. The REQ-021 AC should specify checking both org and repo scopes.

**Recommendation:**
Revise REQ-021 AC to: "Pre-deploy: `gh api orgs/geekatron/rulesets` returns 404 AND `gh api repos/geekatron/jerry/rulesets` lists no ruleset whose conditions include `cowork-skeleton` (currently: only `"Don't fuck with main"` targeting `~DEFAULT_BRANCH` — `cowork-skeleton` is excluded). Both checks must pass." This aligns the AC with the empirical inventory methodology used in ADR-002.

**Post-correction RPN estimate:** 5 × 3 × 3 = 45

---

### FM-013-20260626T1700: git rm -r Edge Cases

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Element** | E-03 — Skeleton Generation Logic |
| **S / O / D** | 4 / 2 / 5 |
| **RPN** | 40 |
| **Strategy Step** | Step 2 (Missing lens — low risk) |

**Evidence:**
REQ-002 states: "The skeleton generation script SHALL strip the `projects/` directory entirely." ADR-001 Option A: "run `git rm -r projects/`." No requirement or ADR addresses git rm behavior with respect to git-tracked symlinks inside `projects/` or pathological file names.

**Analysis:**
`git rm -r projects/` operates on git index entries whose path begins with `projects/`, not on filesystem paths. Git does not follow symlinks when building index paths; a symlink `projects/LINK -> ../.context/rules/` would produce an index entry at `projects/LINK` pointing to the symlink object, and `git rm` would remove the symlink entry without touching `.context/rules/`. No collateral damage to retained directories is possible through this mechanism. The risk is limited to rare edge cases involving very long path names or special characters (which `git` handles correctly on Linux CI runners). Multiple detection mechanisms (REQ-005 directory presence, REQ-006 file count, REQ-022 diff gate) would catch any unexpected strip outcome.

**Recommendation:**
Document in STORY-001 implementation notes: "Use `git rm -r --force projects/` (not `rm -rf`) to ensure the operation is on the git index, not the filesystem. Note that git rm does not follow symlinks — a symlink inside `projects/` pointing outside `projects/` only removes the symlink's index entry, not the target." No change to formal requirements is needed.

**Post-correction RPN estimate:** 4 × 2 × 3 = 24

---

## Recommendations

### Critical Findings (mandatory corrective action)

| ID | Finding | Corrective Action | Estimated RPN Reduction |
|----|---------|-------------------|------------------------|
| FM-001-20260626T1700 | Integrity gate has no SHALL requirement | Add REQ-035: CI SHALL assert published tip SHA equals independently-recomputed deterministic SHA before advertising as installable | 280 → 70 |
| FM-002-20260626T1700 | R-001 gate is proxy-based; CoWork may still reject | Add REQ-034d: one gate dimension SHALL be a direct CoWork install attempt on a reference machine | 252 → 54 |
| FM-003-20260626T1700 | Staleness check is trailer-only; forgeable | Revise NFR-006 to additionally compare live branch tip SHA to recomputed deterministic SHA for the Source-Tag | 224 → 42 |

### Major Findings (recommended corrective action)

| ID | Finding | Corrective Action | Estimated RPN Reduction |
|----|---------|-------------------|------------------------|
| FM-004-20260626T1700 | No CI lint for static stub content | Add generation-script step: grep stub for dynamic patterns; exit non-zero on match | 196 → 56 |
| FM-005-20260626T1700 | No per-run SHA assertion requirement | Promote ADR-001 aspirational note to SHALL: script recomputes and asserts expected SHA on every run | 168 → 48 |
| FM-006-20260626T1700 | No post-job tree monitoring | Extend NFR-006 to compare live tip SHA to deterministic expected SHA (subsumes FM-003 fix) | 168 → 63 |
| FM-007-20260626T1700 | Clone-time estimate at 10 Mbps only | Add 2 Mbps reference requirement to REQ-034; document bandwidth coverage | 168 → 84 |
| FM-008-20260626T1700 | Blank target_tag resolution undefined | REQ-011 SHALL specify resolution mechanism and require allow-list validation of resolved tag | 144 → 48 |
| FM-009-20260626T1700 | marketplace.json path not verified at CoWork runtime | Add direct CoWork install-test to STORY-003 V&V; promote to REQ | 144 → 32 |
| FM-010-20260626T1700 | inputs.target_tag not required to undergo allow-list | Extend ADR-001 RT-04 and add WS-3 requirement for target_tag validation | 108 → 36 |
| FM-012-20260626T1700 | Validation timing unspecified relative to push | REQ-005 and REQ-010 SHALL explicitly run before force-push (same timing as REQ-022) | 105 → 42 |
| FM-011-20260626T1700 | Pre-deploy check queries org rulesets only | Revise REQ-021 AC to query both org and repo rulesets | 90 → 45 |

### Minor Findings (improvement opportunity)

| ID | Finding | Corrective Action |
|----|---------|-------------------|
| FM-013-20260626T1700 | git rm -r edge cases (very low risk) | Document `git rm -r --force` in STORY-001; no formal requirement change needed |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001 (integrity gate not required), FM-004 (no CI lint for stub), FM-006 (no post-job monitoring), FM-011 (incomplete ruleset scope), FM-012 (validation timing unspecified): five missing-lens findings |
| Internal Consistency | 0.20 | Negative | FM-005 (SHA assertion aspirational in ADR but no matching REQ), FM-003 (staleness check inconsistent with the tamper-evidence design in ADR-001/002): design says one thing, requirements say another |
| Methodological Rigor | 0.20 | Negative | FM-002 (R-001 gate uses proxies not direct CoWork test), FM-007 (single bandwidth reference), FM-010 (target_tag validation gap in security methodology), FM-013 (minor): four rigor findings affecting the systematic approach |
| Evidence Quality | 0.15 | Negative | FM-009 (marketplace.json resolution unverified), FM-008 (blank-tag behavior undocumented): claims about install behavior lack empirical backing |
| Actionability | 0.15 | Negative | FM-008 (operator has no defined procedure for blank target_tag recovery scenario); FM-001 (no concrete REQ to implement integrity gate) |
| Traceability | 0.10 | Neutral | All requirements trace to stakeholders; ADR-001/002 reference requirements by ID; FM-012 is a timing trace gap but overall traceability is present |

---

## Execution Statistics

- **Total Findings:** 13
- **Critical:** 3 (FM-001, FM-002, FM-003)
- **Major:** 9 (FM-004 through FM-012)
- **Minor:** 1 (FM-013)
- **Total RPN:** 2,087
- **Highest Single RPN:** FM-001 at 280
- **Most Failure-Prone Element:** E-08 (Branch-Protection and Integrity Posture) + E-01 (R-001 Gate) — each contributing 448 and 420 to total RPN respectively
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-012 FMEA*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Reviewer: adv-executor (BLIND Group E)*
*Executed: 2026-06-26*
*H-15 Self-Review: Applied before persistence*
