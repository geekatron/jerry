# Steelman Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Execution metadata |
| [Summary](#summary) | Assessment and improvement count |
| [Steelman Reconstruction](#steelman-reconstruction) | Strongest form of the design's argument |
| [Findings Summary](#findings-summary) | All findings tabulated by severity |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, recommendation per finding |
| [Scoring Impact](#scoring-impact) | Per-dimension impact of improvements |

---

## Steelman Context

- **Strategy:** S-003 (Steelman Technique)
- **Template:** `.context/templates/adversarial/s-003-steelman.md`
- **Criticality Level:** C4 (AE-003 auto-escalation; AE-005 security-relevant CI; orchestration target >= 0.95)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (Group B — Strengthen) | **Date:** 2026-06-26
- **Iteration:** 2 (post QG-1 remediation — independent blind review)
- **Deliverables Under Review:**
  - `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md`
- **Grounding only (not reviewed):** `research/phase1-skeleton-ci-research.md`, `PLAN.md`

---

## Summary

**Steelman Assessment:** These iteration-2 deliverables represent a technically sophisticated, internally self-consistent design that correctly applies three independent architectural insights (decisive framing, capability inversion, and deterministic tamper-evidence) to achieve supply-chain safety without added complexity. The primary under-statements are in the falsifiability and cross-document traceability of the foundational assumptions, not in the substance of the decisions.

**Improvement Count:** 1 Critical, 5 Major, 2 Minor (8 total)

**Original Strength:** High. The deliverables are well-reasoned and show significant iteration. Most weaknesses are in presentation depth — the ideas are correct but some of the strongest argument threads are not drawn to their full conclusion for a C4 reviewer.

**Recommendation:** Incorporate Critical and Major improvements before critique strategies proceed. Minor improvements are polish.

---

## Steelman Reconstruction

The strongest form of the PROJ-031 Phase 1 design argument runs as follows:

**On skeleton generation (ADR-001):** The design rests on a single empirically-grounded decisive framing: a Claude Code plugin install materializes only the working tree at the branch tip — it does not count, inspect, or process the branch's git history. This claim is not an assumption; it is grounded in observed CoWork behavior (plugins install to `~/.claude/plugins/cache` as a working-tree copy) and in git semantics (a `git clone` checked-out working tree contains only tracked files at HEAD, not pack objects). Under this framing, the entire class of history-rewriting tools (git-filter-repo, subtree split) solve a non-existent problem: they modify history that CoWork never reads. The design therefore correctly selects the simplest possible option (checkout → rm → stub → deterministic commit → force-push), which also happens to be the option with the strongest provenance (parent chain to the exact release tag) and the truest idempotency (bit-identical SHA given the same input).

The bit-identical idempotency property is mathematically sound: since a git commit SHA is a pure function of (tree, parent, author identity, author date, committer date, commit message), and all six inputs are pinned to invariant values for a given release tag (frozen source tree minus fixed strip, tagged release commit SHA, fixed bot identity, source commit date pinned via `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`, static stub content, fixed-template message with full 40-char SHA), the output SHA is a pure function of the release tag. This property makes the published branch tamper-evident without signing: any unauthorized modification of the branch tip changes the SHA away from the independently-recomputable expected value, enabling detection.

**On token strategy (ADR-002):** The credential choice exhibits a rare property: the less-capable credential is also the correct one. The PAT's sole differentiating feature — that its pushes can trigger downstream workflows — is precisely the property the design must exclude (loop-safety). Choosing `GITHUB_TOKEN` therefore gains free loop-safety (third invariant in the over-determined conjunction) rather than needing to architect around the PAT's re-trigger capability. This is not merely a cost-saving decision; it is a positive security argument: the credential that cannot create the primary risk category (infinite regeneration loop) is architecturally superior here even setting aside blast-radius and maintenance considerations.

The loop-safety argument is over-determined across three independent invariants: (1) trigger shape (tag event cannot be fired by a branch push), (2) listener shape (all other workflows listen on `main` or tags, not `cowork-skeleton`), and (3) credential shape (`GITHUB_TOKEN` pushes do not create new workflow runs). Any single invariant failing still leaves two others intact — appropriate robustness for a C4 irreversibility argument.

The integrity-by-detection approach for the unprotected branch is not a security compromise; it is an architectural fit. Branch protection (write prevention) would defend against modifications to a branch whose content is fully deterministic and independently reconstructable — a category error. Detection (pre-publication SHA assertion) provides exactly the right control: it confirms that the published artifact matches what the deterministic process would have produced, and it does so without blocking the `GITHUB_TOKEN` force-push that the design requires.

**On requirements (phase1-requirements.md):** The requirements correctly expand R-001 from a one-dimensional (file count only) to a three-dimensional gate (file count + compressed pack size + clone time), recognizing that the public Anthropic documentation does not specify which mechanism CoWork uses to enforce its limit. REQ-034 is the right engineering response to epistemic uncertainty about an external constraint: measure all three plausible mechanisms before committing to the implementation that satisfies only one. The requirements are further strengthened by REQ-022's pre-push equivalence check, which eliminates the publication window during which a tampered artifact would be available to CoWork users — a subtle but meaningful distinction from post-push checking.

---

## Findings Summary

| ID | Severity | Finding | Target Artifact and Section |
|----|----------|---------|--------------------------|
| SM-001-it2 | Critical | Decisive framing does not state its falsifiability conditions | ADR-001 §Decisive Framing / §Context |
| SM-002-it2 | Major | "Capability inversion" insight not named as a design principle | ADR-002 §Rationale / §L2 point 1 |
| SM-003-it2 | Major | REQ-034 three-dimensional gate does not map dimensions to CoWork limit mechanisms | phase1-requirements.md §WS-5 REQ-034 Rationale |
| SM-004-it2 | Major | R-001 risk row does not reference ADR-001 Option B measurable fallback triggers | phase1-requirements.md §Risk Implications R-001 row |
| SM-005-it2 | Major | "Detection not prevention" is an unnamed security pattern; naming it strengthens the C4 argument | ADR-002 §Branch-Protection Posture / §L2 point 6 |
| SM-006-it2 | Major | NFR-006 staleness detection under-states the specific failure scenario it prevents | phase1-requirements.md §NFR-006 Rationale |
| SM-007-it2 | Minor | REQ-022 pre-push rationale does not explicitly state the publication-window vulnerability it closes | phase1-requirements.md §REQ-022 Rationale |
| SM-008-it2 | Minor | ADR-001 Canonical Plugin-Retention Surface does not document which retained directories are future-strip candidates | ADR-001 §Canonical Plugin-Retention Surface |

---

## Detailed Findings

### SM-001-it2: Decisive Framing Does Not State Its Falsifiability Conditions

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Artifact** | ADR-001 §Decisive Framing (Context section) |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Structural: missing section) |
| **Affected Dimension** | Methodological Rigor, Evidence Quality |

**Evidence (Original):**

ADR-001 §Decisive Framing states: "A Claude Code plugin install **clones the branch and materializes its working tree at the tip commit**, then copies that tree to a cache (`~/.claude/plugins/cache`). Gitignored artifacts (`.venv/`, `site/`, `__pycache__/`) are absent; **history is not part of the checked-out tree.** Therefore the only thing that affects the installed file count is **the tree at the branch tip**."

This claim eliminates the entire history-rewriting option family (Option C). It is the foundational premise of the ADR. However, neither ADR-001 nor the Requirements document explicitly states: (a) what empirical evidence was used to confirm this behavior, or (b) what evidence would falsify the claim.

**Analysis:**

The decisive framing is the single most load-bearing claim in the entire design. If CoWork's plugin installer behaves differently (e.g., if it counts git objects in the `.git` directory rather than just the working tree), the entire branch-stripping approach fails. For a C4 reviewer, the absence of explicit falsifiability conditions weakens the argument: the reviewer cannot assess whether the claim is axiom, observation, or inference.

The strongest form of this argument would include: (1) what source establishes that CoWork materializes a working-tree copy (Anthropic docs reference to cache path, observed install behavior), (2) what git semantics confirm that only tracked files appear in a checked-out working tree (not pack objects), and (3) what specific evidence would overturn the claim (e.g., if R-001 verification shows the limit applies to local `.venv/`-inflated working directory counts, the decisive framing fails).

Notably, R-001 §Verification Approach and REQ-034 DO test this assumption empirically — but neither ADR-001's decisive framing section nor the Requirements' R-001 row cross-references them as "the test that would falsify the decisive framing." Making this connection explicit turns a claim into a testable hypothesis.

**Recommendation:**

Add to ADR-001 §Decisive Framing a two-sentence falsifiability statement: "This claim is grounded in [specific source]. It would be falsified if the R-001 verification (REQ-034) shows that the CoWork limit triggers on a local working-directory count inflated by `.venv/` — in which case branch-stripping has no effect and the strategy pivots per R-001 Fallback."

Additionally, add to ADR-001 §Risks or §L2 an explicit link: "The R-001 multi-dimensional verification gate (REQ-034) is the empirical test of the decisive framing — all three dimensions must pass to confirm the framing holds."

---

### SM-002-it2: "Capability Inversion" Insight Not Named as a Design Principle

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Artifact** | ADR-002 §Rationale and §L2 Architectural Implications point 1 |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Presentation: sound idea, unexploited framing) |
| **Affected Dimension** | Methodological Rigor, Actionability |

**Evidence (Original):**

ADR-002 §Rationale states: "With the pivotal question answered 'no downstream trigger needed,' `GITHUB_TOKEN` **dominates** a PAT on every axis that matters here." The Context section states: "A PAT's *only* differentiating capability over `GITHUB_TOKEN` is that PAT-pushed commits **can** re-trigger workflows; `GITHUB_TOKEN`-pushed commits cannot (an intentional GitHub recursion guard). Since we explicitly want no downstream firing, the PAT's distinguishing feature is not just unnecessary — it is **counter to** the requirement."

**Analysis:**

This is the strongest possible argument for the credential choice, and it is correct. However, it is expressed as a contextual observation rather than a named architectural principle. The design exhibits what can be called "Capability Inversion": the less-capable credential is strictly correct when the capability that distinguishes the more-capable one is specifically the capability you must exclude. This is a generalizable security architecture insight: when the threat model identifies a feature (downstream triggering) as the risk surface, choosing the credential that lacks that feature is not a compromise — it is a positive correctness argument.

Naming this principle would: (a) make the argument more auditable for the C4 reviewer ("the decision satisfies Capability Inversion, which is a documented security architecture pattern"), (b) provide a criterion that would alert maintainers if requirements ever change (if a future requirement adds downstream triggering, the Capability Inversion argument no longer holds and the credential choice must be revisited), and (c) distinguish this decision from the superficially similar `version-bump.yml` case in a principled way.

**Recommendation:**

Add to ADR-002 §Rationale or §L2 point 1 a named framing: "The credential choice satisfies a Capability Inversion property: the sole feature distinguishing Option B (PAT) from Option A (`GITHUB_TOKEN`) is re-trigger capability — and re-trigger capability is specifically what the design must exclude for loop-safety. Option A is therefore not merely 'sufficient' but strictly correct under the current requirements. Future maintainers: if REQ-014's loop-safety requirement is ever relaxed, this inversion no longer holds and the credential choice must be reconsidered."

---

### SM-003-it2: REQ-034 Three-Dimensional Gate Does Not Map Dimensions to CoWork Limit Mechanisms

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Artifact** | phase1-requirements.md §WS-5 REQ-034 Rationale |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Structural: reasoning gap) |
| **Affected Dimension** | Methodological Rigor, Traceability |

**Evidence (Original):**

REQ-034 Rationale states: "R-001 identifies three potential CoWork limit mechanisms (file count, repo size, clone time); the iteration-1 verification approach tested only file count. If the actual CoWork limit is size-based or time-based rather than file-count-based, the branch-stripping strategy would fail and the current verification would not detect it."

REQ-034 then requires a three-dimensional check: (a) tracked file count, (b) compressed pack size, (c) estimated clone time. However, the rationale does not explicitly state which potential CoWork limit mechanism each dimension tests.

**Analysis:**

The three-dimensional verification is the correct engineering response to epistemic uncertainty about an external constraint. The logic is: "we don't know which mechanism CoWork uses, so we test all plausible ones." But the requirement does not make this explicit dimension-to-mechanism mapping, which weakens the traceability argument for the C4 reviewer.

The strongest form of this requirement would state explicitly:
- Dimension (a) tracked file count → tests the hypothesis that CoWork limits by number of tracked files in the working tree
- Dimension (b) compressed pack size → tests the hypothesis that CoWork limits by total git history size (e.g., a transfer-size or disk-quota limit)
- Dimension (c) clone time → tests the hypothesis that CoWork limits by the 120-second `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` git-operation timeout

The gap matters because: if a reviewer asks "why three dimensions, not four or two?", the current rationale does not give a satisfying answer. The dimension-to-mechanism mapping provides that answer.

**Recommendation:**

Expand REQ-034 Rationale with an explicit mapping table or sentence: "Each dimension directly tests one potential CoWork constraint mechanism: (a) file count tests a working-tree cardinality limit; (b) pack size tests a transfer/storage-size limit; (c) clone time tests the documented 120-second `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` timeout. Together they constitute an exhaustive test of the three plausible limit mechanisms identified in the research."

---

### SM-004-it2: R-001 Risk Row Does Not Reference ADR-001 Option B Measurable Fallback Triggers

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Artifact** | phase1-requirements.md §Risk Implications R-001 row |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Structural: cross-document gap) |
| **Affected Dimension** | Completeness, Traceability |

**Evidence (Original):**

Requirements §Risk Implications R-001 row (Mitigation column): "R-001 §Verification Approach + REQ-034: machine-checkable three-dimensional gate (file count, pack size, clone time) MUST pass before Phase 2; fallback scope-pivot strategy defined."

ADR-001 §Decision (not cited in the Requirements risk row) defines the Option B orphan-branch fallback with explicit measurable triggers: "switch to Option B if a clean `git clone` of `cowork-skeleton` (full-provenance, `fetch-depth: 0`) measured on the reference network (a 10 Mbps downlink) exceeds **60 s** wall-clock — 50% of CoWork's 120 s git-operation timeout — **or** its compressed pack (`git count-objects -vH` → `size-pack`) exceeds **250 MB**."

**Analysis:**

The Requirements document's R-001 risk row references the three-dimensional verification gate but does not reference the measurable orphan-branch fallback thresholds (>60s or >250MB) that ADR-001 defines. This creates a cross-document gap: a reader of the Requirements document sees that a fallback exists but does not know its trigger conditions, and a reader of ADR-001 sees the trigger conditions without knowing they feed back into the R-001 risk register.

The strongest risk mitigation statement would close this loop: not just "fallback scope-pivot strategy defined" but "measurable fallback trigger: switch to ADR-001 Option B (orphan branch) if REQ-034 dimension (c) exceeds 60s or dimension (b) exceeds 250MB; otherwise strategy validated."

This is both a completeness improvement (R-001 mitigation is more precisely defined) and a traceability improvement (bidirectional link between requirements risk and ADR decision).

**Recommendation:**

Expand R-001 mitigation column to read: "R-001 §Verification Approach + REQ-034: machine-checkable three-dimensional gate MUST pass before Phase 2; fallback triggers: if REQ-034 dimension (c) clone time > 60s (50% of 120s timeout) OR dimension (b) compressed pack > 250MB, pivot to ADR-001 Option B (orphan branch, O(1) history); if dimension (a) file count fails or CoWork limit is working-directory-based, escalate to user per H-02 (P-020) for strategy pivot."

---

### SM-005-it2: "Detection Not Prevention" Is an Unnamed Security Pattern

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Artifact** | ADR-002 §Branch-Protection Posture "Decision" subsection, §L2 Architectural Implications point 6 |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Presentation: named pattern not invoked) |
| **Affected Dimension** | Methodological Rigor, Evidence Quality |

**Evidence (Original):**

ADR-002 §Branch-Protection Posture states: "The integrity risk is handled by detection, not prevention (below) — a strictly better fit than a write-control rule for a deterministically-regenerated artifact."

ADR-002 §L2 point 6 states: "Integrity is achieved by determinism, not by protection or signing. Pairing ADR-001's recomputable deterministic SHA with a pre-publication integrity gate gives a *verifiable* integrity property that an unprotected, unsigned branch would otherwise lack."

**Analysis:**

The "detection not prevention" approach is a well-established security control pattern (variously named: "Detective Control vs. Preventive Control," "Monitor and Alert vs. Block and Restrict"). The documents correctly identify that detection is the right control category for this case, and they give a compelling reason: "there is nothing worth protecting." But they stop short of naming the pattern and explaining why detection is a structural fit, not a fallback.

The strongest argument is: branch protection (preventive control) would guard against unauthorized writes to a branch whose correct content is fully deterministic and independently recomputable. But "protection" only answers the question "did someone with write access change this?" — it cannot answer "is what CI wrote correct?" Detection (SHA assertion against the deterministic expected value) answers the question that actually matters for supply-chain integrity: "does the published artifact match what the deterministic process should have produced?" For a CI-generated artifact whose generation algorithm is public, detective control is categorically stronger than preventive control at the branch level.

Naming this pattern would allow the C4 reviewer to anchor the argument in established security architecture terminology and confirm the reasoning is principled rather than ad hoc.

**Recommendation:**

Add to ADR-002 §Branch-Protection Posture or §L2 point 6 a named framing: "This applies the detective-control pattern: for a deterministically-generated artifact whose expected value is independently recomputable, a post-generation SHA assertion (detective) provides strictly stronger integrity evidence than a write-access restriction (preventive). Prevention blocks unauthorized writes but cannot confirm that authorized CI writes are correct; detection confirms the latter and can detect the former (any unauthorized modification changes the SHA). The pre-publication integrity gate is therefore not a compensating control for the absence of branch protection — it is the architecturally appropriate control for this artifact type."

---

### SM-006-it2: NFR-006 Staleness Detection Under-States the Specific Failure Scenario It Prevents

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Artifact** | phase1-requirements.md §NFR-006 Rationale |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Structural: incomplete rationale) |
| **Affected Dimension** | Completeness, Methodological Rigor |

**Evidence (Original):**

NFR-006 Rationale states: "REQ-016's `if: failure()` notification step only activates when `cowork-skeleton.yml` runs and fails; it does not fire when the workflow never runs at all (e.g., if the tag trigger silently misfires). Without a scheduled staleness check, the skeleton branch can drift indefinitely with no alert."

**Analysis:**

This rationale correctly identifies the gap but under-specifies the failure scenario and its consequences. The phrase "tag trigger silently misfires" is vague. The concrete failure scenarios that NFR-006 prevents are:

1. **Tag-format regression**: a future release uses a tag format that does not match `v*` (e.g., `release/0.32.0`), causing the trigger not to fire. The skeleton silently stays on the previous release indefinitely.
2. **Workflow disable**: a maintainer disables `cowork-skeleton.yml` to debug something and forgets to re-enable it. All subsequent releases run without updating the skeleton.
3. **Permissions regression**: a future org policy change revokes `GITHUB_TOKEN` branch-push capability, causing `cowork-skeleton.yml` to fail closed — but REQ-016's `if: failure()` only fires when the workflow runs; if the failure is on a `workflow_dispatch` test that wasn't observed, the tag-triggered runs might fail silently if the permissions change was made between runs.
4. **Repository fork/rename**: the skeleton workflow's push target (`geekatron/jerry`) becomes incorrect, causing silent failures.

Without naming concrete scenarios, a C4 reviewer cannot assess whether NFR-006's weekly schedule is sufficient or whether the detection logic (comparing `Source-Commit` trailer to latest `v*` tag) covers all the staleness pathways.

**Recommendation:**

Expand NFR-006 Rationale to enumerate at least two concrete failure scenarios: "Without a scheduled staleness check, two failure modes cause silent indefinite drift: (1) tag-format regression — if a future release uses a non-`v*` tag format, the trigger does not fire and the skeleton is never updated; (2) workflow disable/breakage — if `cowork-skeleton.yml` is disabled or its push step fails on a run that is not manually observed, subsequent releases silently skip the skeleton update. REQ-016's failure notification only fires during an active run; it cannot detect a run that never starts or a breakage that predates the notification step."

---

### SM-007-it2: REQ-022 Pre-Push Rationale Does Not Explicitly Name the Publication Window Vulnerability

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Artifact** | phase1-requirements.md §REQ-022 Rationale |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Presentation: implicit reasoning) |
| **Affected Dimension** | Evidence Quality |

**Evidence (Original):**

REQ-022 Rationale states: "Executing the check pre-push (not post-push) ensures divergent content is never published to `cowork-skeleton`, removing the post-publish window during which compromised content would be available to CoWork users."

**Analysis:**

The rationale correctly states that pre-push removes the publication window. However, it does not make explicit what that window means in practice: between a post-push check's start and its detection of a divergence, any CoWork user who happens to add or refresh the plugin receives the compromised or incorrect artifact. The duration of this window depends on how quickly the post-push check runs and how many users poll during that interval.

For a C4 supply-chain argument, the distinction between pre-push and post-push controls is a first-class security property. Pre-push is a preventive control on the publish action; post-push is a detective control that fires after the artifact is already public. Naming this distinction strengthens the rationale by connecting it to established control-taxonomy thinking.

**Recommendation:**

Add one sentence to REQ-022 Rationale: "A post-push check is a detective control that fires after the artifact is public; during the interval between push and detection, any CoWork user refreshing or installing the plugin receives the unverified content. A pre-push check is a preventive control that blocks publication of unverified content entirely — structurally stronger for a supply-chain gate."

---

### SM-008-it2: ADR-001 Canonical Plugin-Retention Surface Does Not Note Future-Strip Candidates

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Artifact** | ADR-001 §Canonical Plugin-Retention Surface, specifically the final paragraph |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation — Structural: missing forward reference) |
| **Affected Dimension** | Completeness |

**Evidence (Original):**

ADR-001 §Canonical Plugin-Retention Surface states: "By contrast `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/` are **not** load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — but are retained today (1,744 ≪ 5,000)."

This sentence appears only in the final paragraph of the Canonical Plugin-Retention Surface section — not in the table itself, and not in the Consequences §Positive item 6 or the Risks table.

**Analysis:**

The note about future-strip candidates is present and correct. However, its placement at the end of the section means a reader scanning the table for what is retained vs. what is retained-but-not-load-bearing cannot easily distinguish between the two categories. If file-count margin tightens and a future maintainer adds stripping logic, they need to know which retained directories are safe candidates — without this, they might strip a load-bearing directory or retain a non-load-bearing one unnecessarily.

The Steelman improvement would add a "Strip-eligible" column to the Canonical Plugin-Retention Surface table or add a footnote to each row, allowing the table to serve as a complete reference for both current posture and future evolution.

**Recommendation:**

Add a `Strip-eligible` column to the Canonical Plugin-Retention Surface table for non-enumerated retained directories (noting that the 8 enumerated entries are all non-strip-eligible). Alternatively, append a second table immediately after the retention surface:

```
| Directory | Retained Today | Strip-eligible (if margin tightens) |
|-----------|---------------|-------------------------------------|
| `docs/` | Yes | Yes — not load-bearing for plugin function |
| `runbooks/` | Yes | Yes — not load-bearing |
| `overrides/` | Yes | Yes — not load-bearing |
| `scripts/` | Yes | Yes — not load-bearing |
| `tests/` | Yes | Yes — not load-bearing |
```

This makes the architectural intent explicit and actionable for future maintainers.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001-it2 adds falsifiability conditions; SM-004-it2 closes risk-to-ADR cross-reference gap; SM-006-it2 completes NFR-006 failure scenario enumeration; SM-008-it2 adds future-strip candidate documentation |
| Internal Consistency | 0.20 | Positive | SM-004-it2 closes the R-001 risk row / ADR-001 Option B threshold gap; SM-003-it2 aligns REQ-034 dimension list to its underlying rationale |
| Methodological Rigor | 0.20 | Positive | SM-001-it2 converts foundational claim into testable hypothesis; SM-003-it2 maps dimensions to mechanisms; SM-005-it2 names the detective-control pattern; SM-006-it2 enumerates concrete failure scenarios |
| Evidence Quality | 0.15 | Positive | SM-001-it2 surfaces grounding evidence for decisive framing; SM-002-it2 names the Capability Inversion property; SM-007-it2 makes pre-push/post-push distinction explicit |
| Actionability | 0.15 | Positive | All findings include specific before/after with precise locations; recommendations are directly incorporable without structural revision |
| Traceability | 0.10 | Positive | SM-003-it2 adds dimension-to-mechanism mapping; SM-004-it2 adds bidirectional risk-to-ADR link |

**Net assessment:** All six dimensions are positively impacted by the improvements. None introduce new inconsistencies. The deliverables' substance is sound; these improvements surface and complete argument threads that are implicit or cross-document in the current iteration-2 state.

---

## Best Case Scenario

This design is at its strongest under the following conditions:

1. The R-001 three-dimensional verification (REQ-034) passes all three dimensions on a clean clone of `main` and the projected skeleton branch, confirming that branch-stripping is the right lever.
2. The decisive framing is confirmed: CoWork installs by materializing a working-tree copy of the tip, and the limit applies to tracked working-tree files (not pack objects, not local `.venv/`).
3. The orphan-branch fallback (Option B, ADR-001) is never triggered (clone time < 60s, pack size < 250MB) — meaning the stronger-provenance Option A remains in use.
4. The pre-publication integrity gate is implemented and verifiable by any external party, making the unprotected branch posture safe-by-detection in a way that withstands the C4 supply-chain scrutiny.

Under these conditions, the design achieves: CoWork installability, full release provenance, zero long-lived secrets, three-layer loop-safety, tamper-evident distribution without signing, and fully automated CI regeneration — with no technical debt in the current scope.

---

*Generated by: adv-executor (S-003 Steelman Technique)*
*Strategy: S-003 | Template: `.context/templates/adversarial/s-003-steelman.md`*
*Iteration: 2 (Group B — Strengthen, blind independent review)*
*Project: PROJ-031-cowork-skeleton*
*Date: 2026-06-26*
*Workflow: cowork-skeleton-20260626-001 / QG-1 / Iteration 2*
