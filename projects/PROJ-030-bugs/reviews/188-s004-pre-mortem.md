# Pre-Mortem Report: Dependabot Configuration (#188) -- Risk-Tiered Dependency Management

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `.github/dependabot.yml` (PR #188 -- risk-tiered Dependabot configuration)
**Criticality:** C4 (Critical -- full tournament)
**Date:** 2026-03-13
**Reviewer:** adv-executor (S-004 execution)
**H-16 Compliance:** S-003 Steelman applied on 2026-03-12 (188-s003-20260312 confirmed)
**Execution ID:** 188-s004-20260313
**Failure Scenario:** It is September 2026. The Dependabot configuration merged in PR #188 has
failed in production. Multiple incidents have occurred across the six failure vectors declared
below. Maintainer confidence in the automated dependency process has eroded. We are now
investigating what went wrong — from the retrospective frame.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall risk assessment and recommendation |
| [Failure Scenario Declaration](#failure-scenario-declaration) | Temporal perspective shift statement |
| [Findings Table](#findings-table) | All PM-NNN findings with severity and priority |
| [Detailed Findings](#detailed-findings) | Expanded analysis for Critical and Major findings |
| [Prioritized Recommendations](#prioritized-recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Summary

The Pre-Mortem analysis of the #188 Dependabot configuration identified 2 Critical and 7 Major
failure causes across 5 category lenses. The two Critical findings are structurally distinct:
PM-001 exposes an unacknowledged single-point-of-failure where `pip-audit` failing silently in CI
removes the primary detection mechanism for transitive CVEs — leaving the `allow: direct` policy
uncompensated. PM-002 exposes the `allow: direct` classification boundary as a latent assumption
that Dependabot's direct/indirect classification always matches `pyproject.toml` reality, which
it does not for all edge cases.

The overall risk posture is ACCEPT WITH MITIGATIONS. The underlying design is sound (S-003
confirmed: HIGH original strength). The failure modes are not design failures — they are
documentation gaps, operational assumptions not hardened into verifiable constraints, and
configuration brittleness that the current inline docs acknowledge but do not prevent.

**Recommendation:** ACCEPT WITH P0 AND P1 MITIGATIONS. The 2 Critical and 4 highest-impact
Major findings require mitigation before the configuration can be considered production-hardened
at C4 criticality.

---

## Failure Scenario Declaration

> "It is September 2026. The Dependabot configuration merged in PR #188 has failed in ways its
> authors did not anticipate. We are now in a post-incident review. The failures were not caused
> by bad design — the design was sound when shipped. They were caused by the gap between what
> the configuration assumed and what the operational environment delivered. We are working
> backward to enumerate those gaps now, so we can close them before shipping."

Temporal perspective shift established. The analysis below proceeds from the retrospective frame.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-188-s004-20260313 | `pip-audit` silent failure removes transitive CVE detection entirely | Assumption | Medium | Critical | P0 | Completeness |
| PM-002-188-s004-20260313 | Dependabot `direct` classification diverges from `pyproject.toml` reality for edge cases | Technical | Medium | Critical | P0 | Internal Consistency |
| PM-003-188-s004-20260313 | Grouped PR merged with a silently breaking patch-level dep; no per-dep CI signal | Process | High | Major | P1 | Methodological Rigor |
| PM-004-188-s004-20260313 | Transitive supply chain compromise undetected for up to 7 days; blast radius spans all installations | External | Low | Major | P1 | Evidence Quality |
| PM-005-188-s004-20260313 | `allow: direct` false security — maintainer believes transitive CVEs are covered; they are not self-remediating | Assumption | Medium | Major | P1 | Completeness |
| PM-006-188-s004-20260313 | Comment documentation rots; maintainer makes wrong grouping decision based on stale dep counts | Process | High | Major | P1 | Actionability |
| PM-007-188-s004-20260313 | Dependabot behavior changes in GitHub platform update; config silently stops working as designed | External | Low | Major | P1 | Traceability |
| PM-008-188-s004-20260313 | Major version bump accidentally included in grouped patch/minor PR due to SemVer violation by upstream | Technical | Medium | Major | P1 | Methodological Rigor |
| PM-009-188-s004-20260313 | Security update queue saturated by `open-pull-requests-limit`; CVE fix delayed | Process | Low | Minor | P2 | Actionability |

---

## Detailed Findings

---

### PM-001: `pip-audit` Silent Failure Removes Transitive CVE Detection [CRITICAL]

**Failure Cause:** The `allow: direct` policy intentionally excludes transitive dependencies
from Dependabot PRs. The sole compensating detection mechanism is `pip-audit` running in CI.
If `pip-audit` silently exits 0 on error (network timeout, advisory database unavailable,
corrupted venv) or if its CI step is misconfigured to `continue-on-error: true`, the entire
transitive CVE detection layer disappears with no alert to the maintainer. The configuration
documents `pip-audit` as a compensating control (D3, SM-003) but nowhere verifies that it is
running correctly or that its failure is surfaced as a CI failure.

**Category:** Assumption

**Likelihood:** Medium — `pip-audit` is a Python tool with network dependencies (GitHub Advisory
Database). Transient failures occur. The failure mode is not hypothetical: PyPI ecosystem tooling
has known cases of silent success on partial data (e.g., when the advisory database is
temporarily unreachable, some versions return partial results without non-zero exit codes).

**Severity:** Critical — If `pip-audit` fails silently and Dependabot does not generate PRs for
transitive deps (by design), a compromised transitive package like `urllib3`, `gherkin-official`,
or `certifi` can enter the dependency tree and remain undetected indefinitely. The compensating
control architecture described in D3 becomes a single point of failure with no backup.

**Evidence:** D3 CAVEAT (lines 57-69 of dependabot.yml): "CAVEAT: Transitive dep compromises
will NOT generate a Dependabot PR. Compensating DETECTION controls: `pip-audit` in CI catches
known CVEs." SM-003 (S-003 steelman) foregrounded `pip-audit` as a first-class mitigation but
did not add any verification that `pip-audit` is correctly configured to fail-hard. The
configuration assumes `pip-audit` is running but does not document the CI step configuration,
the expected exit codes, or what happens when it fails.

**Affected Dimension:** Completeness (0.20)

**Mitigation:** Document in D3 that `pip-audit` MUST be configured as `continue-on-error: false`
(the default, but must be confirmed) and that its exit code must be non-zero on any CVE finding.
Add a verification note: "Verify `pip-audit` step in CI does not use `continue-on-error: true` —
if it does, the transitive CVE detection layer has no effect." Optionally add a reference to the
specific workflow file and step name so a future maintainer can verify the configuration.

**Acceptance Criteria:** D3 references the specific CI workflow step and confirms it is
configured to fail the build on any CVE finding. A future reader can verify the compensating
control is active without reading the CI workflow file.

---

### PM-002: Dependabot `direct` Classification Diverges from `pyproject.toml` Reality [CRITICAL]

**Failure Cause:** The `allow: dependency-type: direct` policy relies on Dependabot correctly
classifying every relevant package as "direct" (listed in pyproject.toml) vs. "indirect" (not
listed, resolved transitively by uv). D3 documents the classification mechanism: packages
listed in `pyproject.toml [dependencies]` are direct; packages in `requirements*.txt` with
`# via <parent>` annotations are indirect. However, this creates an edge case: if `uv export`
generates a requirements file that does NOT include `# via` annotations for some packages (e.g.,
because uv's export format changed, or because the package appears both as direct and transitive),
Dependabot may classify a direct dep as indirect (suppressing its PR) or an indirect dep as
direct (generating an unexpected PR). The configuration documents how Dependabot classifies deps
but does not document how to verify the classification is correct.

**Category:** Technical

**Likelihood:** Medium — uv's lock file format and export behavior has changed across minor
versions (the project recently upgraded from v4->v7 of setup-uv). If uv changes its
`requirements.txt` export format to omit `# via` annotations, or if a package is declared
explicitly in both `pyproject.toml` and appears as a transitive dep of another package,
Dependabot's classification diverges from the maintainer's mental model.

**Severity:** Critical — Two failure modes: (a) a security-relevant direct dep is silently
excluded from Dependabot PRs because Dependabot misclassified it as indirect — the maintainer
believes the dep is covered but it is not; (b) a transitive dep generates unexpected PRs because
Dependabot classified it as direct, and the maintainer merges it without understanding it is
a transitive constraint update that may break uv's resolution.

**Evidence:** D3 "HOW IT WORKS" section (lines 54-60): "Dependabot classifies deps as
direct/indirect via two mechanisms: (1) packages listed in pyproject.toml [dependencies] or
[dependency-groups] are always classified as direct; (2) packages in requirements*.txt with
`# via <parent>` annotations are indirect." This explanation is accurate but describes
Dependabot's algorithm, not a verification procedure. The debug note ("if an unexpected PR
appears, check both pyproject.toml") is reactive, not proactive.

**Affected Dimension:** Internal Consistency (0.20)

**Mitigation:** Add a proactive verification step to D3: "Periodically run `dependabot-cli
local` or review a Dependabot dry-run to confirm the direct/indirect classification matches
expectations. At minimum, verify after any uv version upgrade (setup-uv major bump) that
`uv export` still generates `# via` annotations in requirements files." Alternatively, note
that the current Jerry project does not use requirements*.txt files (uv uses uv.lock directly),
which means the `# via` annotation mechanism does not apply — Dependabot uses only
`pyproject.toml` for classification. If this is the case, documenting it eliminates the edge
case entirely.

**Acceptance Criteria:** D3 either (a) documents a verification procedure for the
direct/indirect classification, or (b) documents that Jerry does not generate requirements*.txt
files and therefore the classification is based solely on pyproject.toml, eliminating the
annotation-based edge case.

---

### PM-003: Grouped PR Merges a Silently Breaking Patch-Level Dependency [MAJOR]

**Failure Cause:** The `pip-minor-patch` group batches all patch and minor updates into a
single PR. When CI passes, the maintainer merges the entire batch. However, CI catching a
*regression* is not the same as CI revealing *which dependency caused it*. If a patch-level
update contains a breaking change (SemVer violations are common — `click 8.1.x` -> `8.1.y`
subtle behavior change on argument parsing; `pyyaml 6.0.x` -> `6.0.y` serialization edge case),
CI may pass on the Dependabot PR's green status but fail 24 hours later when a specific code
path exercised in a real invocation hits the regression. The maintainer has no easy path back:
the grouped PR merged 5-8 deps at once, and git bisect across a Dependabot merge requires
re-running Dependabot artificially.

**Category:** Process

**Likelihood:** High — Patch-level SemVer violations occur regularly across the Python
ecosystem. The test suite achieving 90% coverage (H-20) still leaves 10% of code paths
untested. Runtime behaviors (CLI output formatting, error messages, file encoding edge cases)
may not be exercised by unit tests.

**Severity:** Major — The REVIEWER GUIDE (lines 185-196 of dependabot.yml) documents the
process for handling grouped PR CI failures, but this process assumes CI fails on the
Dependabot PR itself. It does not address the harder case: CI passes, PR merges, regression
surfaces in production use 24-48 hours later. The rollback path is now a new commit that
manually pins the breaking dep, which requires knowing which dep in the batch broke.

**Evidence:** REVIEWER GUIDE section (dependabot.yml lines 185-196): "If a grouped PR fails CI:
1. Check which dep broke: read the test failure output. 2. Comment `@dependabot ignore <pkg>
minor version` to exclude it." This guide handles CI failure at merge time. No equivalent
guidance exists for post-merge regression discovery.

**Affected Dimension:** Methodological Rigor (0.20)

**Mitigation:** Add a ROLLBACK GUIDE section alongside the REVIEWER GUIDE: "If a post-merge
regression is suspected from a grouped dep update: 1. Check the merged PR's uv.lock diff to
identify all deps that changed. 2. Run `uv pip install <suspect-dep>==<prior-version>` to
isolate. 3. If confirmed, pin the offending dep in pyproject.toml with `<dep> >= <safe>, < <breaking>`
until the upstream fix is available. 4. File a Dependabot `ignore` for that dep's version range."

**Acceptance Criteria:** A post-merge regression rollback procedure exists alongside the
pre-merge CI failure procedure. A maintainer encountering a silent regression has a documented
path to isolation and remediation.

---

### PM-004: Transitive Supply Chain Compromise Undetected for Up to 7 Days [MAJOR]

**Failure Cause:** The configuration documents its maximum transitive CVE detection latency as
"up to 7 days (next weekly Dependabot run triggers parent bump -> CI runs pip-audit)." This
framing is misleading in two ways. First, `pip-audit` runs on every PR and push to main — so
the detection latency for an *existing installation* is the next PR or push, not 7 days.
Second, but more critically: if a transitive package is compromised (typosquat, maintainer
account takeover, malicious publish) but the GitHub Advisory Database has NOT yet issued a
CVE, `pip-audit` will not detect it. The 7-day window cited assumes the CVE exists; the
actual undetected window for a novel supply chain attack before a CVE is issued can be weeks
or months.

**Category:** External

**Likelihood:** Low — Novel supply chain attacks (pre-CVE window) are uncommon against
small projects. However, the Python ecosystem has had high-profile supply chain incidents
(PyPI malicious packages, dependency confusion attacks). Jerry's use of `uv.lock` with frozen
installs reduces (but does not eliminate) this risk: a compromised package in the lockfile
would propagate on the next `uv sync`.

**Severity:** Major — The configuration confidently states compensating controls are adequate
("adequate at current scale" per SM-003). This confidence may lead a maintainer to deprioritize
manual supply chain hygiene (periodic `uv sync` + inspection, SBOM generation). If a
pre-CVE compromise occurs, the "adequate" compensating controls provide zero detection
capability. The blast radius is every installation and every CI run that executes compromised
code.

**Evidence:** D3 lines 65-69: "Maximum transitive CVE detection latency: up to 7 days (next
weekly Dependabot run triggers parent bump -> CI runs pip-audit). For faster detection, run
`uv run pip-audit` locally." This is accurate for known CVEs but silent on pre-CVE attacks.

**Affected Dimension:** Evidence Quality (0.15)

**Mitigation:** Add a scope boundary to the D3 compensating controls statement: "SCOPE:
`pip-audit` detects CVEs listed in the GitHub Advisory Database. Pre-CVE supply chain attacks
(compromised packages before a CVE is issued) are outside the detection scope of both
Dependabot and `pip-audit`. Mitigations for this threat class are: (a) `uv.lock` lockfile
enforcement (prevents silent dep resolution changes), (b) periodic review of `uv.lock` diffs
on grouped PRs for unexpected hash changes, (c) monitoring the PyPI security mailing list
for ecosystem-wide advisories."

**Acceptance Criteria:** D3 distinguishes between CVE-covered supply chain risks (detected by
`pip-audit`) and pre-CVE supply chain risks (not detected by any automated mechanism in this
configuration). A maintainer reading D3 has an accurate model of what the compensating controls
do and do not cover.

---

### PM-005: `allow: direct` Creates a False Sense of Security [MAJOR]

**Failure Cause:** A new maintainer reads D3 and concludes: "Dependabot handles direct deps,
`pip-audit` handles transitive deps — I'm covered." This mental model is approximately correct
but has a critical gap: `pip-audit` detects CVEs in transitive deps but does NOT automatically
remediate them. The remediation path for a transitive CVE is "bump the parent direct dep" —
which requires the maintainer to (a) identify which direct dep's constraint is pulling in the
vulnerable transitive version, (b) check if a newer version of the direct dep resolves the
transitive constraint, (c) manually update the direct dep, and (d) verify the transitive dep
upgraded. This is non-trivial and not documented. A maintainer who sees a `pip-audit` CI
failure from a transitive CVE may not know the correct remediation path.

**Category:** Assumption

**Likelihood:** Medium — This failure mode targets future maintainers rather than the current
author. The configuration's inline docs are addressed to someone who understands the design;
a maintainer arriving 12 months later may not have the FMEA context.

**Severity:** Major — The gap between detection (pip-audit CI failure) and remediation
(manual parent dep bump) is not documented. A maintainer may attempt workarounds (adding a
`dependabot.yml` explicit override for the transitive dep, which conflicts with the `allow:
direct` policy) or simply suppress the CI failure while investigating.

**Evidence:** D3 lines 61-69: "CAVEAT: Transitive dep compromises will NOT generate a
Dependabot PR. Compensating DETECTION controls: `pip-audit` in CI catches known CVEs;
`uv.lock` diff review on grouped PRs reveals transitive shifts. These are detectors, not
remediators — a transitive CVE still requires manual intervention (bump the parent dep or add
an explicit override)." The last sentence acknowledges the gap but does not document the
remediation procedure.

**Affected Dimension:** Completeness (0.20)

**Mitigation:** Extend D3's "detectors, not remediators" statement with a brief remediation
procedure: "TRANSITIVE CVE REMEDIATION: (1) Run `uv tree <vulnerable-dep>` to identify which
direct dep pulls in the vulnerable version. (2) Check if a newer version of the direct dep
has a constraint that resolves to a safe transitive version. (3) Bump the direct dep in
pyproject.toml or add an explicit override: `[dependency-groups.overrides]
<transitive-dep> = '>= <safe-version>'`. (4) Run `uv sync` and verify `pip-audit` passes."

**Acceptance Criteria:** D3 documents the transitive CVE remediation procedure. A maintainer
encountering a `pip-audit` CI failure has a documented path from detection to resolution.

---

### PM-006: Comment Documentation Rots; Wrong Decision Based on Stale Dep Counts [MAJOR]

**Failure Cause:** The configuration documents concrete dep counts in multiple places: "~20
direct+transitive" (D1), "~7 runtime deps" (D1), "~8 direct runtime deps plus ~4 direct dev
deps" (D6), "~7 distinct actions" (D6). These counts are marked as "verified #188" with an
instruction to "update when dep count changes." Six months from now, a maintainer adds 3 new
direct deps for a new feature, does not update the counts (the instruction is easy to miss in a
150-line comment block), and makes a grouping decision ("the dep count is still low enough to
keep runtime and dev deps together") based on the stale D1 rationale. The dep count is now 25,
past the informal 20-dep mental model but not yet at the documented 40-dep threshold — the
ambiguous middle zone where the decision is non-obvious and the stale count misleads.

**Category:** Process

**Likelihood:** High — Comment documentation rot is one of the most reliable failure modes in
long-lived configuration files. The instruction "update when dep count changes" is a manual
maintenance step with no automated enforcement. In a project where the primary focus is
application code, CI config maintenance will be deprioritized.

**Severity:** Major — A wrong grouping decision based on stale counts could mean: (a) a
runtime dep breakage is masked by a dev dep in the same group (D1 explicitly identified this
as a risk that is "accepted at current scale" but would require splitting above ~40 deps);
(b) the PR limit (D6) becomes inadequate, queuing security PRs during a CVE burst; (c) the
maintainer splits groups when they don't need to (creating unnecessary complexity) or doesn't
split when they do (missing the risk separation that was the whole point of the FMEA analysis).

**Evidence:** D1 lines 13-14: "(verified #188; update when dep count changes)". D6 lines 97-98:
"(verified #188; update when dep count changes)". These instructions are maintenance-required
annotations without any automated verification. The entire D1 and D6 rationale depends on the
count being accurate.

**Affected Dimension:** Actionability (0.15)

**Mitigation:** Replace the manual "update when dep count changes" instruction with a
verification command: add a note like "CURRENT DEP COUNT (auto-check): run
`uv run python -c 'import tomllib; t=tomllib.load(open(\"pyproject.toml\",\"rb\")); deps=t[\"project\"].get(\"dependencies\",[])+list(t.get(\"dependency-groups\",{}).values().__class__([])); print(len(deps))'`
or simply `uv tree --depth 1 | wc -l` to get the current direct dep count before updating
D1 or D6 rationale." Even better: document the specific `pyproject.toml` section where deps
are declared so a future maintainer can count directly. The threshold triggers (D1: reconsider
at ~40; D6: reconsider at >15 direct deps; SM-006: reassess labels at >8 PRs/week) should be
collected into a REVISIT TRIGGERS section so they are not scattered across comments.

**Acceptance Criteria:** A REVISIT TRIGGERS section consolidates all documented thresholds with
the commands or locations needed to check current values against the thresholds. A maintainer
doing a quarterly review has a single place to look.

---

### PM-007: Dependabot Platform Change Silently Breaks Config [MAJOR]

**Failure Cause:** GitHub has changed Dependabot's configuration schema and behavior at least
twice since the v2 format was introduced (groups were added in 2023; `allow` with
`dependency-type` behavior changed between 2022 and 2024 releases). The configuration uses
several features that are relatively recent additions: `groups:`, `allow: dependency-type:
direct`, and the interaction between `groups:` and security updates. If GitHub deprecates or
changes the behavior of `allow: dependency-type: direct` (e.g., changing the classification
algorithm, deprecating the `allow` stanza in favor of a different filtering mechanism, or
changing how `groups:` interacts with `allow:`), the configuration may silently produce
incorrect behavior: unexpected transitive dep PRs, missing direct dep PRs, or grouped PRs that
include the wrong deps.

**Category:** External

**Likelihood:** Low — GitHub's Dependabot configuration schema is stable for established
features. However, the combination of `groups:` + `allow:` is a relatively new composition
that has less community validation than the older formats.

**Severity:** Major — Silent behavior changes are worse than outright errors: the configuration
continues to run, Dependabot continues to generate PRs, but the PRs no longer implement the
intended policy. A maintainer trusting the documented behavior could merge a grouped PR
that includes a transitive dep, or miss a direct dep PR that was suppressed by a changed
classification algorithm.

**Evidence:** D3 "Debug" note (lines 57-60): "Debug: if an unexpected PR appears, check both
pyproject.toml (is it a declared dependency?) and requirements-*.txt (does it have a `# via`
annotation?)." This reactive debug guidance is the only mechanism for detecting behavior
changes. The REFERENCES section links to GitHub's Dependabot options reference page but does
not document the version or date of the feature behavior that was validated.

**Affected Dimension:** Traceability (0.10)

**Mitigation:** Add a behavior validation note to D3 with the Dependabot version/date when the
`allow: dependency-type: direct` + `groups:` behavior was validated: "BEHAVIOR VALIDATED: As
of [date], `allow: dependency-type: direct` combined with `groups:` excludes all packages not
in pyproject.toml [dependencies]. Re-validate after any Dependabot feature announcement in the
GitHub changelog." Also add to the REFERENCES section: a pointer to the specific GitHub
Dependabot changelog URL for monitoring breaking changes.

**Acceptance Criteria:** D3 includes a date-stamped behavior validation note. The REFERENCES
section includes a GitHub Dependabot changelog URL. A future maintainer has a starting point
for detecting platform changes.

---

### PM-008: Major Version Bump Accidentally Included in Grouped Patch/Minor PR [MAJOR]

**Failure Cause:** The `pip-minor-patch` group uses `update-types: ["minor", "patch"]`.
This instructs Dependabot to use the version string's first two segments to classify the
update type. However, some packages in the Python ecosystem publish version numbers that do
not follow strict SemVer: `0.x.y` packages treat `x` as the major version (so `0.1.0` ->
`0.2.0` is treated as "minor" by Dependabot but is semantically major for the package).
Examples relevant to Jerry's dep set: `ruff` uses `0.x.y` versioning where minor (`x`) bumps
include breaking lint rule changes; `pytest-bdd` has historically used `0.x.y` for major
releases. Dependabot classifies these as "minor" updates and includes them in the
`pip-minor-patch` group — but they can contain breaking changes that require code changes.

**Category:** Technical

**Likelihood:** Medium — `ruff` is a direct dep of Jerry and uses `0.x.y` versioning. Each
`0.x` -> `0.(x+1)` bump has historically introduced new default-enabled lint rules that cause
CI failures. Dependabot would classify `ruff 0.4.x` -> `ruff 0.5.0` as "minor" and include
it in the grouped PR, potentially causing a CI failure or — worse — requiring linting rule
updates that the maintainer did not expect in a "patch/minor" PR.

**Severity:** Major — A grouped PR that unexpectedly contains a breaking lint configuration
change (ruff), a behavior-changing BDD parser update (pytest-bdd), or a CLI interface change
(any `0.x.y` tool) fails CI. The REVIEWER GUIDE documents the process for splitting these
out, but this requires recognizing that the failure is a semantic-major bump masquerading as
a Dependabot "minor" update — a non-obvious diagnosis for a maintainer unfamiliar with the
project's `0.x.y` dep landscape.

**Evidence:** D1 (lines 5-24) documents the grouped PR rationale but does not mention `0.x.y`
versioning exceptions. REVIEWER GUIDE (lines 185-196) documents CI failure handling but does
not mention the `0.x.y` semantic-major masquerade case. The configuration assumes SemVer
compliance from all grouped deps; this assumption is not documented or defended.

**Affected Dimension:** Methodological Rigor (0.20)

**Mitigation:** Add a `0.x.y` exception note to D1: "EXCEPTION: Packages using `0.x.y`
pre-1.0 versioning (e.g., ruff) treat minor (`x`) bumps as breaking changes even though
Dependabot classifies them as 'minor'. These will appear in grouped PRs. Review `0.x.y`
minor bumps with the same care as major version bumps — check the package changelog for
breaking changes before merging." Alternatively, add explicit `ignore` rules for known
`0.x.y` packages to exclude them from the group and treat them as individual PRs.

**Acceptance Criteria:** D1 documents the `0.x.y` versioning exception. The REVIEWER GUIDE
includes a note about semantic-major updates appearing as grouped "minor" updates and the
diagnostic to check. Known `0.x.y` deps (ruff at minimum) are either excluded from the group
or flagged for enhanced review.

---

### PM-009: Security PR Queue Saturated by `open-pull-requests-limit` [MINOR]

**Failure Cause:** D4 notes: "`open-pull-requests-limit` applies to security PRs too (CC-005).
At Jerry's scale this is unlikely to saturate." However, `open-pull-requests-limit: 10` (for
pip) is a combined ceiling for both version update PRs and security update PRs. If multiple
major dep versions are pending (e.g., pytest 9->10, ruff 1->2, click 9->10, pyyaml 7->8
simultaneously during an ecosystem transition), 4-6 of the 10 slots may be occupied by
version PRs. A burst of CVEs (3-4 critical security PRs) competing for the remaining 4-6
slots could cause some security PRs to be queued or suppressed until version PRs are merged
or closed.

**Category:** Process

**Likelihood:** Low — At Jerry's current scale (12 direct deps, ~7 distinct actions), the
10-PR limit has adequate headroom under normal conditions. A simultaneous major-version
transition epoch (Python 4.0 release, major pytest jump) combined with a CVE burst is an
unlikely but not implausible convergence.

**Severity:** Minor — A delayed security PR is not the same as undetected vulnerability:
`pip-audit` in CI still detects the CVE. The delay is operational (the automated PR takes
longer to appear) not a security detection failure. The risk is human attention: a maintainer
who relies on Dependabot PRs as their security awareness signal may not notice the queue is
saturated.

**Evidence:** D4 lines 80-82: "Note: `open-pull-requests-limit` applies to security PRs too
(CC-005). At Jerry's scale this is unlikely to saturate, but a burst of CVEs could compete
with version update PRs for queue slots." This documents the risk accurately but provides no
monitoring guidance.

**Affected Dimension:** Actionability (0.15)

**Mitigation:** Add a monitoring note to D4: "MONITOR: If version update PRs are accumulating
(more than 5 open simultaneously), close or merge them before the next scheduled run to
prevent security PRs from being queued. As an alternative, reduce `open-pull-requests-limit`
for pip version updates and set a separate higher limit for security updates by splitting the
pip block into two ecosystem entries." (P2: acknowledge and monitor; no immediate action
required at current scale.)

**Acceptance Criteria:** D4 documents the PR limit saturation scenario and its operational
consequence. The monitoring signal (>5 simultaneous version PRs) is documented.

---

## Prioritized Recommendations

### P0 -- Critical: MUST mitigate before acceptance at C4

**PM-001: Verify `pip-audit` CI configuration (Critical -- Completeness)**

The `allow: direct` policy is uncompensated if `pip-audit` silently fails. Verify and document:
- Confirm the `pip-audit` CI step has `continue-on-error: false` (or equivalent)
- Add a note in D3 referencing the specific workflow file and step: "VERIFIED: `pip-audit` runs
  at `<workflow-file>/<step-name>` with non-zero exit on CVE detection. If this step is changed
  to `continue-on-error: true`, the transitive CVE detection layer is disabled."
- Acceptance criteria: D3 references the CI step and confirms fail-hard behavior.

**PM-002: Clarify `direct` classification mechanism for Jerry's actual setup (Critical -- Internal Consistency)**

The `# via` annotation mechanism may not apply if Jerry does not generate `requirements*.txt`
files. Determine and document the actual classification path:
- If Jerry uses only `uv.lock` and `pyproject.toml` (no `requirements*.txt`): document that
  Dependabot uses `pyproject.toml` as the sole classification source, eliminating the annotation
  edge case.
- If `requirements*.txt` files exist: confirm `uv export` generates `# via` annotations and
  document a periodic verification step.
- Acceptance criteria: D3 documents the actual classification mechanism for Jerry's toolchain
  with no ambiguity about whether `requirements*.txt` annotations apply.

---

### P1 -- Important: SHOULD mitigate

**PM-003: Add post-merge regression rollback procedure (Major -- Methodological Rigor)**

Extend REVIEWER GUIDE with a ROLLBACK GUIDE for post-merge regressions:
- Add steps: check uv.lock diff for changed deps; isolate via `uv pip install <dep>==<prior>`;
  pin with pyproject.toml constraint; add Dependabot ignore for version range.
- Acceptance criteria: A maintainer encountering a silent post-merge regression has a
  documented isolation and remediation path.

**PM-004: Add CVE detection scope boundary (Major -- Evidence Quality)**

Extend D3 compensating controls to distinguish CVE-covered vs. pre-CVE supply chain risks:
- Add scope boundary statement: `pip-audit` covers known CVEs; pre-CVE attacks are out of scope.
- Document the pre-CVE risk mitigations: lockfile enforcement, uv.lock diff review, PyPI
  security monitoring.
- Acceptance criteria: D3 accurately describes what the compensating controls detect and what
  they do not detect.

**PM-005: Add transitive CVE remediation procedure (Major -- Completeness)**

Extend D3's "detectors, not remediators" sentence with a remediation procedure:
- `uv tree <vulnerable-dep>` to identify parent; bump parent or add explicit override.
- Acceptance criteria: A maintainer encountering a `pip-audit` CI failure has a documented
  path from detection to resolution.

**PM-006: Add REVISIT TRIGGERS section consolidating all thresholds (Major -- Actionability)**

Create a REVISIT TRIGGERS section below the REFERENCES block with:
- D1 trigger: dep count > 40 (check: `uv tree --depth 1 | wc -l`)
- D6 trigger: direct dep count > 15 (check: count `[project.dependencies]` in pyproject.toml)
- SM-006 trigger: weekly PR volume > 8 (check: GitHub Insights > PR history)
- D1 count verification: current count and date verified
- Acceptance criteria: A quarterly reviewer can verify all thresholds against current values
  from a single location without reading the full comment block.

**PM-007: Add behavior validation note with date stamp (Major -- Traceability)**

Add to D3 a date-stamped behavior validation note for `allow: dependency-type: direct` +
`groups:` composition, plus a GitHub Dependabot changelog URL in REFERENCES:
- Acceptance criteria: A future maintainer has a starting point for detecting Dependabot
  platform changes.

**PM-008: Add `0.x.y` versioning exception to D1 and REVIEWER GUIDE (Major -- Methodological Rigor)**

Document that packages using `0.x.y` pre-1.0 versioning (especially `ruff`) may have
breaking changes appear as Dependabot "minor" updates in the group:
- Identify known `0.x.y` deps in Jerry's direct dep set.
- Add to REVIEWER GUIDE: check changelogs for `0.x.y` minor bumps before merging.
- Optionally: add explicit Dependabot `ignore` rules for known `0.x.y` packages to exclude
  them from the group and treat them as individual major-equivalent PRs.
- Acceptance criteria: D1 and REVIEWER GUIDE both acknowledge the `0.x.y` exception.
  Known affected packages (ruff at minimum) are identified.

---

### P2 -- Monitor: MAY mitigate; acknowledge and monitor

**PM-009: Document PR limit saturation monitoring signal (Minor -- Actionability)**

Add a monitoring note to D4: if more than 5 version update PRs are open simultaneously,
close or merge them proactively to preserve queue capacity for security PRs.
Monitor signal: >5 open Dependabot version PRs at any point.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001 (pip-audit silent failure leaves D3 uncompensated), PM-005 (transitive CVE remediation undocumented). The steelman (S-003) foregrounded compensating controls but did not verify their operational integrity. Two completeness gaps remain that S-003 did not address. |
| Internal Consistency | 0.20 | Negative | PM-002 (direct classification mechanism ambiguous for Jerry's actual toolchain). The configuration claims a classification algorithm that may not apply to Jerry's uv-only setup. This is a factual inconsistency between the documentation and the toolchain reality. |
| Methodological Rigor | 0.20 | Negative | PM-003 (no post-merge regression procedure), PM-008 (`0.x.y` versioning not addressed). The REVIEWER GUIDE is half a methodology: it handles CI failures at merge time but not silent post-merge regressions or semantic-major updates masquerading as minor. |
| Evidence Quality | 0.15 | Negative | PM-004 (CVE detection scope overstated). The D3 claim that compensating controls ensure "no transitive CVE silently enters the dependency tree" conflates CVE-database coverage with complete supply chain protection. The evidence quality for this claim is lower than the confidence level expressed. |
| Actionability | 0.15 | Negative | PM-006 (stale dep count documentation with no verification command), PM-009 (PR limit saturation signal undocumented). The configuration is highly actionable for its initial deployment but degrades in actionability over time as dep counts change and the manual maintenance instructions are missed. |
| Traceability | 0.10 | Negative | PM-007 (no date-stamped behavior validation). The REFERENCES section links to documentation but does not record when the feature behavior was validated, making it impossible to assess whether a future behavior change has occurred. |

**Overall Assessment:** All six dimensions register Negative impact from Pre-Mortem findings.
This does not indicate a weak deliverable — the S-003 steelman correctly assessed it as HIGH
strength. It indicates that the Pre-Mortem temporal perspective shift is revealing operational
brittleness that the forward-looking design correctly did not prioritize but that becomes
significant at C4 criticality over a 6-month operational horizon.

**Projected improvement from mitigations:** Addressing P0 + P1 findings (PM-001 through
PM-008) would flip all six dimensions from Negative to Positive or Neutral, estimated composite
score improvement: +0.06 to +0.09 toward the 0.92 threshold.

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 2 (PM-001, PM-002)
- **Major:** 6 (PM-003 through PM-008)
- **Minor:** 1 (PM-009)
- **Protocol Steps Completed:** 6 of 6
- **H-16 Compliance:** VERIFIED (S-003 executed 2026-03-12; output at 188-s003-20260312)
- **Failure Categories Explored:** 5 of 5 (Technical, Process, Assumption, External, Resource)
- **Failure Causes Generated:** 9 (exceeds 5-cause minimum)
- **P0 Findings:** 2 (MUST mitigate before C4 acceptance)
- **P1 Findings:** 6 (SHOULD mitigate)
- **P2 Findings:** 1 (MAY mitigate; acknowledge risk)

---

*Pre-Mortem By: adv-executor (S-004 Execution)*
*Strategy: S-004 Pre-Mortem Analysis*
*Template: .context/templates/adversarial/s-004-pre-mortem.md*
*Execution ID: 188-s004-20260313*
*Date: 2026-03-13*
*SSOT: .context/rules/quality-enforcement.md*
*H-16 Status: Compliant -- S-003 (188-s003-20260312) confirmed before S-004 execution.*
