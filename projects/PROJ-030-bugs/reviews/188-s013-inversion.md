# Inversion Report: Dependabot Configuration (#188) -- Risk-Tiered Dependency Management

**Strategy:** S-013 Inversion Technique
**Deliverable:** `.github/dependabot.yml`
**Criticality:** C4 (Critical -- full tournament)
**Date:** 2026-03-13
**Reviewer:** adv-executor
**H-16 Compliance:** S-003 Steelman applied 2026-03-12 (confirmed: `projects/PROJ-030-bugs/reviews/188-s003-steelman.md`)
**Goals Analyzed:** 6 | **Assumptions Mapped:** 11 | **Vulnerable Assumptions:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall inversion assessment and recommendation |
| [Step 1: Goals](#step-1-goals) | Explicit and implicit goals extracted from the deliverable |
| [Step 2: Anti-Goals](#step-2-anti-goals) | Inverted goals -- what would guarantee failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | All 11 assumptions with confidence and validation status |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Per-inversion analysis for all 7 prescribed inversions |
| [Step 5: Mitigations](#step-5-mitigations) | Concrete actions for Critical and Major findings |
| [Findings Table](#findings-table) | Consolidated IN-NNN findings |
| [Scoring Impact](#scoring-impact) | Dimension-level assessment |

---

## Summary

Seven prescribed inversions were executed against the Dependabot configuration. Six of the seven current design decisions survive inversion with High confidence -- the configuration's choices are genuinely superior to their inverses in context. One inversion (D3: `allow: direct`) produces a **Major** finding: the transitive CVE detection gap is real and documented in the config itself, but the compensating controls (pip-audit, uv.lock diff review) are not enforced -- they are advisory. The prescribed inversions also surface one **Minor** finding: the weekly schedule creates a predictable 7-day detection window that is documented but not escalated via any alerting path.

**Verdict: ACCEPT with one targeted mitigation.** The configuration is robust under inversion. The current design decisions are each better than their inverses given Jerry's operating context (~20 deps, small team). The critical inversion analysis confirms the design is not hiding structural risks -- the one genuine gap (unalerting transitive CVE window) is known, documented, and proportionate to the project's scale.

**Inversion confidence summary:** 5 decisions defended with High confidence, 1 with Medium confidence (D3/transitive), 1 with Low confidence (D6/limit=10 vs limit=3).

---

## Step 1: Goals

### Explicit Goals (stated in the deliverable)

| Goal | Source |
|------|--------|
| G1: Reduce Dependabot PR volume to ~2-4 PRs/week from ~7+ individual PRs | D1, D2 comments |
| G2: Keep breaking changes (major version bumps) individually visible and reviewable | D1, D2 comments |
| G3: Eliminate transitive dependency noise PRs (e.g., gherkin-official 29→39) | D3 comment |
| G4: Preserve per-CVE visibility for security updates | D4 comment |
| G5: Maintain forward compatibility with Filter B (version-bump.yml) | D5 comment |

### Implicit Goals (unstated but necessary for the deliverable to succeed)

| Goal | Inference |
|------|-----------|
| G6: Catch dependency vulnerabilities before they reach production | Implied by enabling Dependabot at all |
| G7: Keep maintainer cognitive load low enough that PRs are actually reviewed (not queued indefinitely) | Implied by grouping decisions |
| G8: Avoid false confidence -- no security mechanism should create the impression of coverage it does not provide | Implied by the documented CAVEAT in D3 |

---

## Step 2: Anti-Goals

For each goal, what would **guarantee failure**?

| Goal | Anti-Goal Condition | Addressed by deliverable? |
|------|--------------------|-----------------------------|
| G1 (reduce PR volume) | Create individual PRs for every patch bump -- ~7+/week guaranteed | YES -- grouping handles this |
| G2 (breaking changes visible) | Group major version bumps with minor/patch -- individual review bypassed | YES -- majors are ungrouped |
| G3 (no transitive noise) | Allow transitive PRs -- resume the gherkin-official class of noise PRs | YES -- `allow: direct` |
| G4 (per-CVE visibility) | Batch all security updates into one omnibus PR -- specific CVE lost in noise | YES -- security is ungrouped by default |
| G5 (Filter B compat) | Change commit prefix mid-stream -- breaks the `ci:` / `deps:` filter | YES -- prefixes unchanged |
| G6 (catch vulns) | Disable Dependabot or set schedule so infrequent that CVEs age undetected | PARTIAL -- weekly is reasonable but transitive CVE gap exists (IN-001) |
| G7 (low cognitive load) | Flood the PR queue so maintainers stop reviewing -- queue saturation | PARTIAL -- limit=10 may be too permissive at scale (IN-002) |
| G8 (no false confidence) | Document the transitive CVE gap but provide no enforcement path for the compensating controls | PARTIAL -- documented but unenforced (contributes to IN-001) |

---

## Step 3: Assumption Map

| ID | Assumption | Type | Confidence | Validation Status | Consequence of Failure |
|----|-----------|------|------------|-------------------|----------------------|
| A1 | Weekly schedule is frequent enough to detect actionable vulnerabilities before exploitation | Temporal | Medium | Logically inferred (no SLA set) | Major: CVE exposure window of up to 7 days for direct deps; indirect has no upper bound |
| A2 | ~20 direct+transitive deps is the stable operating scale | Environmental | Medium | Observed (current pyproject.toml) | Major: grouping strategy, limit sizing, and skip-on-dev-deps reasoning all assume this |
| A3 | `pip-audit` in CI reliably catches transitive CVEs | Technical | Low | Assumed (no audit coverage verified) | Major: the entire compensating control for the transitive gap depends on this |
| A4 | SemVer minor/patch is always backward-compatible for Jerry's dependencies | Technical | Medium | Partially validated (CI catches exceptions) | Minor: a minor bump with a behavioral change would land in the grouped PR; CI catches it but adds churn |
| A5 | Maintainers will review PRs within the 7-day inter-run window | Process | Medium | Not empirically validated | Major: if PRs queue, the limit=10 becomes effectively limit=∞ for that week |
| A6 | GitHub Advisory Database coverage is sufficient for Jerry's dep stack | Technical | Medium | Not validated -- advisory DB has known gaps for smaller packages | Minor: niche PyPI packages may have CVEs not in the advisory DB |
| A7 | Actions SHA-pinning (EN-001) makes major action bumps a "safe SHA swap" | Technical | Medium | Validated structurally but runtime behavior still changes | Minor: SHA pinning prevents supply chain injection; it does not prevent behavior regressions from the new version |
| A8 | Grouped PR CI failure is always diagnosable to a specific dep | Process | Medium | Assumed (reviewer guide present but untested at scale) | Minor: with many deps in one group, CI failure root cause may require investigation effort |
| A9 | `allow: direct` correctly classifies all Jerry deps | Technical | High | Validated via uv/pip annotation mechanism (documented in D3) | Minor: a misclassified direct dep would silently miss updates |
| A10 | The D7 decision to omit risk-tier labels is stable -- PR title communicates sufficient signal | Process | Medium | Context-valid now; degrades if PR volume grows | Minor: at higher PR volume, no label filter means all PRs have equal visual weight |
| A11 | open-pull-requests-limit=10 provides adequate headroom without enabling queue saturation | Process | Low | Sized by dep count estimate, not by empirical PR volume data | Minor-to-Major: if multiple major bumps arrive simultaneously, limit=10 may queue less-critical PRs behind major-version PRs |

---

## Step 4: Stress-Test Results

Each of the seven prescribed inversions is analyzed below.

---

### Inversion 1: INVERT D1 -- Group MAJOR updates, keep minor/patch individual

**Current decision:** Minor/patch are grouped (`pip-minor-patch`), majors are ungrouped.
**Inverse:** Major updates grouped, minor/patch individual.

**Plausibility:** Medium. Some teams do group majors to reduce noise if they have extensive test coverage and treat CI as the gate.

**Stress-test:** If major version bumps (e.g., `pytest 9→10`, `ruff 1→2`) were grouped, a single PR could contain multiple breaking API changes across unrelated dependencies. A CI failure would require bisecting the group to find the cause. More critically, the rationale for ungrouping majors is **review quality**, not just CI detection: a human needs to read the changelog, assess API removals, and approve the bump consciously. Grouping majors would produce omnibus PRs where changelog review becomes impractical.

**Would the inverse be better?** No. At Jerry's scale (~8 runtime + ~4 dev direct deps), the maximum ungrouped major PR volume is ~12/batch -- a rare event (most deps don't cut majors simultaneously). The review-quality argument is decisive: major bumps warrant individual attention. The current decision is correct.

**Verdict: Current decision is better. Confidence: High.**

---

### Inversion 2: INVERT D2 -- Keep ALL Actions individual (no grouping)

**Current decision:** Actions minor/patch SHA rotations are grouped (`actions-minor-patch`); majors are ungrouped.
**Inverse:** All Actions updates are individual PRs.

**Plausibility:** High. This was the pre-#188 state. The concern was ~7 individual PRs/week for SHA rotations.

**Stress-test:** Jerry uses approximately 7 distinct actions (setup-uv, checkout, upload-artifact, etc.). Weekly SHA rotation for all 7 = 7 individual PRs. Each is a low-signal PR: the diff is a single SHA hash change with no behavioral implications (SHA pinning means the code is identical to what was tagged). Reviewing 7 identical-pattern PRs individually trains maintainers to rubber-stamp them without reading -- perversely reducing review quality for the occasional substantive action change.

**Is ~7 PRs/week actually a problem?** Yes, specifically because the repetitive nature of SHA rotation PRs degrades the signal-to-noise ratio for genuinely important action changes. Grouping the routine noise lets major action bumps (which do carry behavioral risk) stand out.

**Would the inverse be better?** No. The grouped approach is strictly better: lower volume, higher per-PR signal, and majors are still ungrouped for individual review. The D2 comment correctly characterizes SHA rotation PRs as low-risk.

**Verdict: Current decision is better. Confidence: High.**

---

### Inversion 3: INVERT D3 -- REMOVE `allow: direct`, let Dependabot bump transitives

**Current decision:** `allow: dependency-type: direct` -- only direct deps get PRs.
**Inverse:** Remove the `allow` block -- Dependabot raises PRs for all dependencies including transitives.

**Plausibility:** High. This is the default Dependabot behavior and what many projects use.

**Stress-test -- would we catch transitive CVEs faster?**

Yes and no. If a transitive dep has a standalone CVE (e.g., `gherkin-official` CVE), Dependabot would raise a PR immediately. This IS faster for the specific case of a transitive dep with a CVE that has an available fix at the transitive dep level.

However, the documented failure mode is `gherkin-official 29→39`: a transitive PR that conflicted with what `pytest-bdd` expected. The core problem with transitive PRs is that they may propose a version incompatible with the parent dep's declared constraints. Applying the transitive PR breaks the parent.

The current config's compensating control chain for transitive CVEs is:
1. `pip-audit` in CI detects CVEs in transitives (even without a Dependabot PR)
2. `uv.lock` diff on grouped PRs reveals transitive shifts
3. When the parent direct dep is bumped, uv resolves the compatible transitive version

**The gap:** `pip-audit` is a CI gate, but is it run on a schedule? The config only documents it as a CI step, not as a scheduled scan. If `pip-audit` only runs on PRs, a transitive CVE with no active parent dep PR would be undetected until either: (a) a new PR is raised, or (b) a maintainer manually runs `uv run pip-audit`.

**This is a genuine vulnerability in the current configuration's assumption.** The inverse (allow transitives) would catch some CVEs faster at the cost of re-introducing transitive conflict noise. The better path is to enforce the compensating control rather than revert the architecture.

**Would the inverse be better?** Marginally, for one specific scenario (transitive CVE with no parent dep update due). The current approach is architecturally superior but has an unmitigated detection gap.

**Verdict: Current decision is better architecturally, but gap exists. Confidence: Medium.**

**Finding generated: IN-001-20260313 (Major)**

---

### Inversion 4: INVERT D4 -- GROUP security updates

**Current decision:** Security updates are ungrouped (each CVE gets its own PR).
**Inverse:** Group security updates with `applies-to: security-updates`.

**Plausibility:** Low-to-Medium. Some teams do this to reduce security PR volume.

**Stress-test:** Security PRs are event-driven, not schedule-driven. They fire when a CVE is published and a fix is available. At Jerry's scale, CVE bursts (multiple security PRs simultaneously) are rare. More importantly, grouping security updates would batch multiple CVE remediations into one PR. The review quality impact is significant: a maintainer reviewing a grouped security PR cannot easily confirm each CVE is addressed independently or assess whether the combined bump introduces any new instability.

Individual CVE PRs are also the standard GitHub Dependabot design intent for security updates -- the UI surfaces the linked advisory, severity, and affected version range per PR. Grouping would collapse this per-CVE context.

**Would the inverse be better?** No. Individual security PRs are strictly better for clarity, auditability, and per-CVE accountability. The concern about maintainer fatigue from security PR volume is not realistic at Jerry's scale -- security PRs arrive rarely enough that they warrant individual attention.

**Verdict: Current decision is better. Confidence: High.**

---

### Inversion 5: INVERT D6 -- REDUCE open-pull-requests-limit to 3

**Current decision:** `open-pull-requests-limit: 10` for both ecosystems.
**Inverse:** Reduce to 3.

**Plausibility:** Medium. This is the "forced prioritization" model used by some high-discipline teams.

**Stress-test:** With limit=3:
- 1 slot consumed by `pip-minor-patch` group PR (grouped minor/patch)
- 1 slot consumed by `actions-minor-patch` group PR (grouped minor/patch)
- 1 slot remaining for all individual major PRs across both ecosystems

If two major bumps are pending simultaneously (e.g., `pytest 9→10` and `ruff 1→2`), one would be queued until the other is merged or closed. This creates a hidden backlog where Dependabot silently stops raising new PRs rather than surfacing the queue.

**Would forced prioritization improve review quality?** Only if the discipline bottleneck is actually PR volume. At ~2-4 PRs/week (post-grouping), the current volume is already low. Forcing limit=3 would create artificial scarcity that delays routine updates without improving review quality.

**However:** There is a legitimate concern on the upper end. limit=10 with ~12 direct deps means Dependabot could accumulate 10 open PRs (mostly majors) before pausing. A team not actively reviewing would face a PR backlog of 10 unreviewed major version bumps. This is a different failure mode from limit=3 but not trivially better.

**Would the inverse be better?** No -- but the current limit=10 is not obviously optimal either. The sizing rationale (headroom for ~8 runtime + ~4 dev direct deps) is correct but implicitly assumes all major PRs are desirable in the queue simultaneously. In practice, a lower limit like 5-7 would still accommodate normal operations while creating earlier queue pressure that signals "you have a backlog."

**Verdict: Current decision is marginally better than limit=3. But limit=10 may be more permissive than necessary. Confidence: Low.**

**Finding generated: IN-002-20260313 (Minor)**

---

### Inversion 6: INVERT the weekly schedule -- Use DAILY

**Current decision:** `interval: "weekly"`, `day: "monday"`.
**Inverse:** `interval: "daily"`.

**Plausibility:** High. Daily scheduling is used by high-velocity projects.

**Stress-test -- would faster detection outweigh review burden?**

For **security updates**, this question is moot: security PRs are event-driven, not schedule-driven (explicitly documented in D4). The weekly schedule does NOT delay security updates.

For **version updates**, daily detection would catch a new release within ~24 hours vs. up to ~7 days. The practical benefit depends on how often Jerry deps release versions that are both actionable and time-sensitive. For a framework like Jerry with stable dependencies, the marginal detection benefit of daily vs. weekly is low.

The review burden increase would be real: currently ~2-4 PRs/week. Daily scheduling on grouped deps would still produce ~1-2 PRs/day if a new version is released, creating ~7-14 PRs/week. At a small-team project, this approaches the pre-grouping PR volume that motivated the grouping decision in the first place.

**Would the inverse be better?** No for Jerry's context. The weekly + event-driven security model provides the right split: security detects as fast as GitHub Advisory Database updates allow, and version updates run weekly with manageable PR volume.

**Verdict: Current decision is better. Confidence: High.**

---

### Inversion 7: INVERT the entire approach -- NO Dependabot, manual dependency management

**Current decision:** Dependabot enabled with risk-tiered configuration.
**Inverse:** Disable Dependabot entirely; rely on manual `uv update` runs and manual security monitoring.

**Plausibility:** Low for a project of any sustained activity. This was the pre-Dependabot state.

**What would we lose?**

1. **Automatic CVE detection and PR creation** -- the most critical loss. Security advisories would require manual monitoring of GitHub Security Advisories, PyPI advisory databases, or running `pip-audit` on a schedule. There is no automated PR; the maintainer must discover and apply the fix manually.
2. **Version currency signals** -- without Dependabot, deps silently age. A project can unknowingly run year-old versions of actively-maintained deps. Security improvements, bug fixes, and performance gains are missed.
3. **Structured update review** -- Dependabot PRs include diff, changelog link, compatibility score, and CI results. Manual updates lack this review scaffolding.
4. **Audit trail** -- every dep bump is a PR with reviewer, CI result, and merge date. Manual updates may land in larger commits with less traceability.

**Would the inverse be better?** No. Even a minimal Dependabot configuration (like the pre-#188 state) is strictly superior to no automation. The #188 configuration improves on the minimum by adding risk tiering, grouping, and documentation. Removing it would regress security posture significantly.

**Verdict: Current decision is better by a wide margin. Confidence: High.**

---

## Step 5: Mitigations

### IN-001-20260313 (Major): Transitive CVE Detection Gap -- Compensating Controls Are Advisory, Not Enforced

**The gap:** The D3 comment documents that `pip-audit` in CI and `uv.lock` diff review are the compensating controls for transitive CVEs that Dependabot will not surface. However, if `pip-audit` only runs on PR-triggered CI (not on a schedule), a transitive CVE with no pending direct dep PR would be undetected indefinitely.

**Mitigation options (in priority order):**

1. **Add a scheduled `pip-audit` workflow** (PREFERRED): Create a CI workflow that runs `uv run pip-audit` on a schedule (e.g., nightly or weekly), independent of PR activity. This enforces the compensating control rather than relying on PR-driven detection. The workflow should fail and alert when a CVE is found.

2. **Update D3 comment to reflect enforcement gap** (MINIMUM): If a scheduled workflow is not immediately feasible, the D3 comment should be updated to clarify that `pip-audit` currently only runs on PR-triggered CI, not on a schedule. This prevents false confidence that the compensating control provides equivalent coverage to proactive Dependabot transitive PRs.

**Acceptance criteria:** Either (a) a scheduled `pip-audit` workflow exists and triggers alerts on CVE discovery independent of PR activity, OR (b) the D3 CAVEAT comment explicitly states "pip-audit currently runs on PR CI only; scheduled scanning is not implemented."

---

### IN-002-20260313 (Minor): open-pull-requests-limit=10 May Be More Permissive Than Necessary

**The gap:** limit=10 accommodates all direct deps simultaneously in the queue. This is correct for headroom but does not create any pressure signal when PRs accumulate unreviewed. A maintainer could have 8 open Dependabot PRs and not notice the backlog is building.

**Mitigation:** No immediate change required. If PR queue length monitoring is added (e.g., via a GitHub Action that alerts when open Dependabot PRs exceed a threshold), the limit can remain at 10. Alternatively, reduce to 7 (accommodating ~8 direct runtime deps minus the 1 slot consumed by the grouped PR) to create earlier queue pressure while still allowing normal operations.

**Acceptance criteria (for the "reduce limit" path):** limit >= 5 and <= 7, with the sizing rationale updated in the D6 comment to reflect the new value.

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Inversion | Affected Dimension |
|----|------------------------|------|------------|----------|-----------|-------------------|
| IN-001-20260313 | A3: `pip-audit` in CI reliably catches transitive CVEs (assumes scheduled/proactive run) | Assumption | Low | Major | If pip-audit only runs on PR CI, transitive CVEs have unbounded detection latency when no parent dep PR is active | Completeness |
| IN-002-20260313 | A11: limit=10 provides headroom without enabling silent queue saturation | Assumption | Low | Minor | At limit=10 with ~12 direct deps, 8+ unreviewed major PRs can accumulate before Dependabot pauses, no signal emitted | Actionability |

**Inversions that found the current decision is stronger than the inverse (no finding generated):**

| Inversion | Current Decision Defended | Confidence |
|-----------|--------------------------|-----------|
| D1 inverted (group majors) | Ungrouped majors preserve individual review quality | High |
| D2 inverted (all Actions individual) | Grouped SHA rotations reduce noise without losing major visibility | High |
| D4 inverted (group security) | Individual security PRs preserve per-CVE clarity | High |
| D6 inverted (weekly → daily) | Weekly + event-driven security is correct split; daily adds volume without benefit | High |
| D7 inverted (no Dependabot) | Automation is strictly superior to manual management | High |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | IN-001-20260313: The transitive CVE detection gap is documented but the compensating control enforcement path is incomplete. The deliverable does not address what happens if pip-audit is not running on a schedule. Five of seven design decisions are complete; this one has a partial coverage claim. |
| Internal Consistency | 0.20 | Positive | All design decisions are internally coherent and reinforce each other. D3's `allow: direct` + D4's ungrouped security + D5's Filter B compatibility form a consistent risk-tiered model. No contradictions found. |
| Methodological Rigor | 0.20 | Positive | The seven-decision structure, cross-references to FMEA/research/prior reviews, and explicit deviation notes (CONSERVATIVE OVERRIDE on D2, DEVIATION on D1) demonstrate systematic design methodology. |
| Evidence Quality | 0.15 | Positive | Six of seven inversions are decisively defended by documented evidence (dep count, PR volume estimates, EN-001 SHA pinning, Filter B mechanism). The transitive CVE gap is itself documented, which is evidence of honest assessment rather than false confidence. |
| Actionability | 0.15 | Slightly Negative | IN-002-20260313: The reviewer guide (DA-004 annotation) and the operational notes in D3 are actionable. However, the transitive CVE compensating controls are described as capabilities, not procedures with owners and schedules. The mitigation for IN-001 is concrete and actionable if implemented. |
| Traceability | 0.10 | Positive | Cross-references to FMEA, risk analysis, prior review files, Filter B, and EN-001 are thorough. Every design decision traces to its rationale. The IN-001 finding traces to the D3 CAVEAT text directly. |

**Net assessment:** The configuration is strong across four of six dimensions. Two dimensions have minor gaps both traceable to the same root issue: the transitive CVE detection gap documented in D3 is real, but the compensating control chain is advisory rather than enforced. Addressing IN-001 would bring Completeness and Actionability to Positive, making this a clean PASS across all dimensions.

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 0
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6
- **Inversions Executed:** 7 of 7 (all prescribed)
- **Inversions Finding Current Decision Superior:** 5 of 7 with High confidence, 1 of 7 with Medium confidence
- **Assumptions Mapped:** 11 (5 technical, 3 process, 2 environmental, 1 temporal)

---

*Strategy Version: S-013 v1.0.0*
*Template: `.context/templates/adversarial/s-013-inversion.md`*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution ID: 188-s013-20260313*
