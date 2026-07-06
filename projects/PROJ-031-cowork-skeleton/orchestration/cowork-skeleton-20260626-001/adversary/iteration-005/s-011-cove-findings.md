# Strategy Execution Report: Chain-of-Verification (S-011)

## Execution Context

- **Strategy:** S-011 (Chain-of-Verification / CoVe)
- **Template:** `.context/templates/adversarial/s-011-cove.md`
- **Deliverable:** 5 design artifacts — ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md
- **Executed:** 2026-06-29T00:00:00Z
- **Iteration:** iteration-005 (Group D, blind tournament)
- **Criticality:** C4
- **H-16 Status:** S-003 indirect compliance (CoVe is verification-oriented); proceeding per template

---

## Step 1: Claim Inventory

All load-bearing factual/technical claims extracted from the 5 artifacts. Claims whose failure would break the design are marked **[LOAD-BEARING]**.

| ID | Claim | Source | Type |
|----|-------|--------|------|
| CL-001 | "Stripping `projects/` and `tests/` yields ~1,417 tracked files" | ADR-001 L0, c-001, c-003; ADR-003 D1; REQ-002 | Numerical value [LOAD-BEARING] |
| CL-002 | "CoWork loads/clones the dedicated repo's DEFAULT branch (no `#ref` needed)" | ADR-003 D1; STRIDE L0 | Behavioral [LOAD-BEARING] |
| CL-003 | "CoWork keeps installed users current when the default branch updates" | ADR-003 D1 (implicit); requirements STK-002 | Behavioral [LOAD-BEARING] |
| CL-004 | "Org-level ruleset cannot be overridden by repo admins (only org-owners can modify it)" | ADR-003 D2; REQ-040 | Platform behavior [LOAD-BEARING] |
| CL-005 | "`gh attestation verify` detects tampering by comparing the live tip SHA against the Sigstore log" | ADR-003 D7; NFR-006; REQ-035 | Behavioral [LOAD-BEARING] |
| CL-006 | "≤6h scheduled read-only poll detects tampering within the stated SLA" | ADR-003 D7; REQ-035; NFR-006 | SLA claim [LOAD-BEARING] |
| CL-007 | "GitHub App installation token lifetime is short-lived (~1 h, ≤ ~8 h)" | ADR-003 D3; STRIDE Area 5 | Numerical value |
| CL-008 | "`git merge-base --is-ancestor ${TAG}^{commit} origin/main` prevents off-main releases" | ADR-003 D5; REQ-038; ADR-001 D5 scope note | Technical claim [LOAD-BEARING] |
| CL-009 | "The org-registration repoint is monitorable at ≤24h cadence (REQ-047 / OQ-047)" | ADR-003 RTB-3; REQ-047 | Behavioral [LOAD-BEARING] |
| CL-010 | "A source-repo GitHub Actions workflow cannot subscribe to push events in a different repository" | ADR-003 D7; REQ-035 redesign note | Platform behavior [LOAD-BEARING] |
| CL-011 | "STRIDE/attack-surface strip set: `git rm -r projects/` (projects/ only)" | STRIDE pipeline; attack-surface.md pipeline | Technical claim [LOAD-BEARING] |
| CL-012 | "GitHub App installation token can be designated as the sole bypass actor on the org-level ruleset" | ADR-003 D3; STRIDE Area 5 | Platform behavior [LOAD-BEARING] |
| CL-013 | "SC-04 (anchor collapse) was found by 5 of 8 Phase-1 adversary strategies" | STRIDE Phase-1 Critical Findings; ADR-003 L0 | Historical assertion |
| CL-014 | "ADR-003 states the Phase-2 STRIDE model uses SC-06 for drift/staleness (GREEN), creating a collision with the trusted-maintainer rogue build" | ADR-003 Threat Basis identifier-collision note | Cross-reference claim |
| CL-015 | "The `Source-Commit:` trailer is forgeable; the tip SHA is non-forgeable" | ADR-001 Tamper-Evidence section | Technical claim [LOAD-BEARING] |
| CL-016 | "REQ-026 tutorial instructs users to run `claude plugin marketplace add geekatron/jerry@cowork-skeleton`" | REQ-026; requirements WS-4 | Behavioral |
| CL-017 | "~5,000-file CoWork ceiling applies to the clean-clone tracked file count, not the local dev working directory" | R-001 statement; ADR-001 L0 | Behavioral [LOAD-BEARING] |
| CL-018 | "Immutable GitHub releases + build-provenance attestation are GA (since Oct 2025)" | ADR-003 D4 references; STRIDE references | Platform behavior [LOAD-BEARING] |
| CL-019 | "Per-job permissions isolation: attestation job gets `id-token: write`, push job gets `contents: write` only" | ADR-003 D4; REQ-020 | Technical claim [LOAD-BEARING] |

---

## Step 2: Verification Questions

| VQ-ID | CL-ID | Verification Question |
|-------|-------|----------------------|
| VQ-001 | CL-001 | Is the ~1,417 file count stated consistently across all 5 artifacts, and does the strip set description match? |
| VQ-002 | CL-003 | Is the update delivery mechanism (how CoWork distributes updates to already-installed users) described anywhere in the 5 artifacts? |
| VQ-003 | CL-006 | Does the design acknowledge the GitHub Actions scheduler's non-deterministic delivery guarantee when asserting the ≤6h detection SLA? |
| VQ-004 | CL-007 | What does GitHub's documentation state about the lifetime of a GitHub App installation token? Does the design correctly state "≤ ~8h"? |
| VQ-005 | CL-009 | Is the API endpoint for querying the org's registered CoWork plugin source identified anywhere in the 5 artifacts, or is it explicitly unknown? |
| VQ-006 | CL-011 | Does the STRIDE threat model's pipeline diagram and REQ-022 change show BOTH `projects/` AND `tests/` being stripped, or only `projects/`? |
| VQ-007 | CL-014 | Does the Phase-2 STRIDE model actually use SC-06 for drift/staleness (as claimed in ADR-003), or is there no collision? |
| VQ-008 | CL-016 | Does REQ-026's tutorial install command reference the Phase-2 dedicated repo `geekatron/jerry-cowork`, or the old in-repo `geekatron/jerry@cowork-skeleton`? |
| VQ-009 | CL-010 | Is the claim that GH Actions cannot subscribe cross-repo correct? |
| VQ-010 | CL-008 | Does the provenance assertion pseudocode correctly fetch `origin/main` before invoking `git merge-base --is-ancestor`? |

---

## Step 3 & 4: Independent Verification and Consistency Check

### VQ-001 / CL-001: Strip set and file count consistency

**Independent verification:**
- ADR-001 L0, Context, c-001, c-003: "~1,417 files" (projects/ AND tests/ stripped)
- ADR-003 D1 pipeline: "`git rm -r projects/ tests/`" → "~1,417 files"
- REQ-002: "approximately 1,417 tracked files; strip set includes projects/ AND tests/"
- STRIDE threat model pipeline: "`git rm -r projects/ ; inject static projects/README.md stub`" — only `projects/`
- STRIDE REQ-022 change: "`git diff "${TAG}..HEAD" -- ':!projects/'`" — only `':!projects/'`
- Attack-surface.md Skeleton Regeneration Job: "strips projects/ directory" — only `projects/`

**Verdict:** CONTRADICTED for the security analysis artifacts. ADR-003 and requirements correctly show both directories being stripped. The STRIDE threat model and attack-surface.md show only `projects/` being stripped. The STRIDE model's faithful-derivative gate specification (`':!projects/'` only) therefore does not match the actual ADR-003/REQ-022 gate (`':!projects/' ':!tests/'`). The file count implied by the STRIDE/attack-surface model (if tests/ is not stripped) would be higher than the asserted ~1,417.

---

### VQ-002 / CL-003: Plugin update delivery mechanism

**Independent verification across all 5 artifacts:**
- ADR-001 L0: "CI rebuilds it on every release" (describes CI action, not user-side update)
- ADR-001 Context: "A Claude Code plugin install clones the branch and materializes its working tree at the tip commit, then copies that tree to a cache (`~/.claude/plugins/cache`)" — INSTALL only
- ADR-003 D1: "An org admin registers that repo once (server-side); it then appears for every user under 'Your organization.'" — registration, not update
- REQ-029 (SHOULD): "The Explanation document SHALL describe the version-alignment mechanism: how `plugin.json.version` is synchronized by `bump-my-version`, how the CoWork client resolves updates, and why users receive one update notification per release." — acknowledges mechanism must be documented but does not describe it
- STK-002: "automatically in sync with `main` on every release, without manual repository surgery" — goal statement, not mechanism description

No artifact describes HOW CoWork updates already-installed plugins (i.e., the update/refresh cycle: does it re-clone on every session, poll periodically, use plugin.json version comparisons, or require manual user action?). The project's primary goal ("automatically in sync") depends entirely on this unverified behavior.

**Verdict:** UNVERIFIED. The update delivery mechanism is a load-bearing behavioral claim (the entire project goal depends on it) that is asserted but never sourced, described, or verified in any of the 5 artifacts. The internal research document (`research/cowork-plugin-install-mechanism.md`) cited as "CONFIRMED" is not in scope for review.

---

### VQ-003 / CL-006: ≤6h detection SLA

**Independent verification:**
- ADR-003 D7: "Detection SLA. Bounded by the poll cadence (≤ 6 h) rather than near-real-time event delivery"
- REQ-035: "scheduled (≤ 6-hourly cadence)" and "Detection SLA ≤ 6 h (aligned with NFR-006 updated cadence)"
- NFR-006: "≤ 6-hourly detection SLA"
- No artifact acknowledges the platform-level scheduling uncertainty

**Known platform behavior (P-022 distinction — believed true but unproven by the design package):** GitHub Actions `schedule` triggers are documented by GitHub as best-effort, not guaranteed to fire at the exact specified time. During periods of high load, scheduled workflows may be delayed by hours beyond the cron interval. GitHub's own documentation warns that scheduled workflows "may be delayed during periods of high load." The 6-hour claim in the design is stated as a hard SLA, not a best-effort target.

**Verdict:** UNVERIFIED. The design presents the ≤6h detection SLA as deterministic when GitHub Actions scheduled workflows have no delivery-time guarantee from the platform. No artifact acknowledges this uncertainty. A tamper event occurring just before a scheduled run could remain undetected for >6h during high-load periods. The meta-monitor (25h) would only alert after >25h of monitor silence — a significantly wider window than the stated SLA.

---

### VQ-004 / CL-007: GitHub App installation token lifetime

**Independent verification:**
- ADR-003 D3: "short-lived (~1 h, ≤ ~8 h)"
- STRIDE Area 5 credential table: "Short-lived (~8 h), minted in-job"
- STRIDE CI-01 mitigation: "GitHub App **installation token minted in-job** (short-lived ≈8 h)"
- ADR-003 L1 Cross-repo credential sketch: "let it expire with the job"

**Known platform behavior (P-022 — believed true, not verified by design package):** GitHub App installation access tokens have a documented expiration of **1 hour** per GitHub's API documentation. There is no documented configuration option for extending App installation token lifetime to 8 hours. GitHub's OIDC-based token mechanisms and `GITHUB_TOKEN` also expire with the job (typically well under 1 hour for most jobs), but these are distinct from App installation tokens.

**Discrepancy:** The STRIDE model states "~8 h" as the primary value; ADR-003 D3 states "~1 h, ≤ ~8 h" as a range. The 1-hour value appears correct for GitHub App installation tokens; the "≤ ~8 h" upper bound is inconsistently stated. Implementers designing workflow steps with 8-hour assumptions could experience unexpected token expiry mid-job for long-running generation pipelines.

**Verdict:** UNVERIFIED with internal inconsistency. The "≤ ~8 h" claim in ADR-003 D3 appears to contradict the known GitHub App installation token lifetime of ~1 hour. The STRIDE model independently states "~8 h" as its value. This internal inconsistency (1h vs ≤8h) in the design package could lead to incorrect implementation assumptions.

---

### VQ-005 / CL-009: OQ-047 — org-registration monitoring endpoint

**Independent verification:**
- REQ-047: "**OPEN QUESTION (OQ-047):** The specific GitHub API endpoint (or CoWork platform API) for querying the org's currently registered CoWork plugin source is not documented in ADR-003 and requires empirical discovery before this requirement can be implemented; this requirement is a binding SHALL placeholder"
- REQ-047 AC: "(a) **OPEN QUESTION (OQ-047) — endpoint not yet identified:** this AC is provisional and SHALL be updated when the API endpoint is empirically discovered before Phase 6."
- ADR-003 RTB-3: "an automated monitor (REQ-047) queries the org's registered CoWork source ≤ daily (target ≤ 24 h)" — asserts monitoring is possible but cites no endpoint
- ADR-003 Consequences Negative #2: "periodic registered-source verification" — cited without specifying mechanism

**Verdict:** EXPLICITLY UNVERIFIED. REQ-047 is a binding MUST-priority requirement (priority: Should, but with binding SHALL language for the automated detection compensator) whose implementation is blocked by an unidentified API endpoint. The design package explicitly labels this OQ-047. The "≤24h detection window" for the org-registration repoint threat is therefore unachievable until the endpoint is discovered.

---

### VQ-006 / CL-011: Strip set in STRIDE and attack-surface

Already fully addressed under VQ-001. The STRIDE model pipeline and attack-surface.md pipeline both show only `projects/` being stripped. The REQ-022 change in the STRIDE model shows `':!projects/'` only. ADR-003 and requirements show `projects/` AND `tests/`.

**Verdict:** CONTRADICTED (same as CL-001 finding above).

---

### VQ-007 / CL-014: SC-06 identifier collision claim

**Independent verification against the STRIDE model:**
STRIDE model Consolidated Threat Register:
- Row 15: "SC-06 | T/R | Trusted-maintainer rogue build (faithful malicious build) | 2×4=8 | Y | **NEW** — provenance + `main` peer review (ADR-003 D5/RTB-2, REQ-051/SC-06)"
- Row 20: "SC-07 | T | Two-repo drift | 2×3=6 | G | carryover (NFR-006)"

STRIDE model Area 4 table:
- SC-06: Trusted-maintainer rogue build (YELLOW 8)
- SC-07: Two-repo drift (GREEN 6)

**ADR-003 claim being verified:**
ADR-003 Threat Basis section:
> "Identifier-collision note (cross-artifact consistency): the Phase-2 STRIDE model already uses the label `SC-06` for a *different* threat (two-repo drift / staleness, banded GREEN). The trusted-maintainer rogue build is tracked as `SC-06` in **this ADR and the requirements mirror (REQ-051)**; the Phase-3 STRIDE update MUST reconcile the collision — renumbering the drift threat — so a single `SC-06` denotes the trusted-maintainer build consistently across all three artifacts."

**Actual STRIDE model state:** SC-06 = trusted-maintainer rogue build (YELLOW 8Y); SC-07 = two-repo drift (GREEN 6G). There is NO collision in the current STRIDE model — both artifacts use SC-06 for the same thing (trusted-maintainer rogue build).

**Verdict:** CONTRADICTED. ADR-003's identifier-collision note is factually incorrect relative to the current STRIDE model document. The STRIDE model does NOT use SC-06 for drift — it uses SC-07 for drift and SC-06 for the trusted-maintainer rogue build, consistent with ADR-003's own usage. The "Phase-3 STRIDE update MUST reconcile" instruction is therefore based on a false premise. However, the UNDERLYING SECURITY DECISIONS (peer review for SC-06) are correct and unaffected by this labeling error.

---

### VQ-008 / CL-016: REQ-026 tutorial command

**Independent verification:**
- REQ-026: "The Tutorial SHALL instruct users to install the marketplace via the Git-based command `claude plugin marketplace add geekatron/jerry@cowork-skeleton` and SHALL NOT suggest adding the marketplace via a direct URL to the `marketplace.json` file."
- ADR-003 D1: "There is no per-user 'add by URL' in the confirmed CoWork build, so org registration is the sole distribution channel."
- ADR-003 D1: Distribution is `geekatron/jerry-cowork` (dedicated repo), not `geekatron/jerry` (source repo).
- STRIDE L0: "no per-user add-by-URL — org-level only; remote/account-managed"

**Contradiction:** Under the Phase-2 architecture:
1. The distribution repo is `geekatron/jerry-cowork` (not `geekatron/jerry`)
2. Distribution is org-admin server-side registration (not per-user install command)
3. REQ-026's command `claude plugin marketplace add geekatron/jerry@cowork-skeleton` references the source repo (`geekatron/jerry`) with the old in-repo branch name (`cowork-skeleton`), not the dedicated repo (`geekatron/jerry-cowork`)
4. If there is truly no per-user add-by-URL path, this user-level command may not apply at all under the Phase-2 model

**Verdict:** CONTRADICTED. REQ-026's tutorial install command references the Phase-1 in-repo model (`geekatron/jerry@cowork-skeleton`) rather than the Phase-2 dedicated repo. Under the confirmed Phase-2 org-registration model, there may be no per-user install command at all — the registration is server-side org-admin only. REQ-026 was not updated when the distribution model changed.

---

### VQ-009 / CL-010: Cross-repo workflow event subscription

**Independent verification (from my knowledge, P-022 labeled):**
A GitHub Actions workflow can only subscribe to events in its own repository. This is a documented platform constraint. You cannot configure a `geekatron/jerry` workflow with `on: push: branches:` targeting events in `geekatron/jerry-cowork`. The design's claim is correct.

**Verdict:** VERIFIED.

---

### VQ-010 / CL-008: Provenance assertion fetch dependency

**Independent verification:**
ADR-001 pseudocode and ADR-003 L1:
```bash
SRC_SHA="$(git rev-parse "${TAG}^{commit}")"
if ! git merge-base --is-ancestor "${SRC_SHA}" origin/main; then
```

For `origin/main` to be accessible, the CI runner must have fetched the `main` branch. With `fetch-depth: 0` (Option A, full history), `origin/main` is available. With `fetch-depth: 1` (shallow), only the tag commit is available; `origin/main` would need an explicit `git fetch origin main` step. The pseudocode does not show this explicit fetch.

ADR-003 L1 § Provenance gate shows the check immediately after tag validation, without an explicit `git fetch origin main` command. Under `fetch-depth: 0` (the default for Option A), this works. But the pseudocode omission creates a latent risk if `fetch-depth` is ever reduced for performance reasons.

**Verdict:** VERIFIED (under Option A `fetch-depth: 0`). Minor gap: no explicit `git fetch origin main` in pseudocode creates a latent dependency on fetch-depth assumption that could silently break provenance assertion if fetch settings change. Not a current defect, but a documentation/robustness gap.

---

### Additional Claims Verified

**CL-002 (CoWork loads DEFAULT branch):** VERIFIED — consistently stated and internally coherent. Rests on confirmed internal research document outside this scope.

**CL-004 (Org-level ruleset cannot be overridden by repo admins):** VERIFIED — GitHub platform behavior is correctly stated. Org-owners (above repo admin) can modify org-level rulesets; the design accurately acknowledges this as RTB-1.

**CL-005 (`gh attestation verify` detects tampering):** VERIFIED — `gh attestation verify` is a real, functioning GitHub CLI command that checks artifact digests against Sigstore attestation records. The mechanism described is technically correct.

**CL-008 (`git merge-base --is-ancestor` semantics):** VERIFIED — the git command exits 0 if the first commit is an ancestor of the second, and exits non-zero otherwise. Correct usage for provenance assertion.

**CL-012 (GitHub App can be sole bypass actor):** VERIFIED — GitHub's ruleset bypass-actor feature supports designating GitHub Apps as bypass actors. Consistent with cited GitHub Changelog entry.

**CL-013 (SC-04 found by 5 of 8 strategies):** VERIFIED (internally consistent) — all 3 documents citing this agree: S-001, S-002, S-011, S-012, S-013 (5 strategies). Cannot independently verify against strategy outputs per blindness constraint.

**CL-015 (Tip SHA non-forgeable, Source-Commit trailer forgeable):** VERIFIED — technically correct. Git SHA derivation makes tip SHA non-forgeable (requires hash preimage collision); commit message trailers are free-form text, forgeable by any push actor.

**CL-018 (Immutable releases + attestation GA):** VERIFIED with caveat. GitHub artifact attestations became available in 2024; immutable releases in 2025. Design correctly mandates empirical confirmation before Phase-5 (Consequences §Negative 4).

**CL-019 (Per-job permissions isolation):** VERIFIED — GitHub Actions per-job `permissions:` blocks override workflow-level permissions, enabling this isolation. The design is technically sound.

**CL-017 (R-001 file-count assumption):** UNVERIFIED (known, acknowledged by design) — explicitly flagged as the project's "primary unresolved risk" in R-001. Some design sections present it as settled fact, creating a minor framing inconsistency.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CV-001-iter005 | **Critical** | Plugin update delivery mechanism is unverified — no artifact describes how CoWork updates already-installed users when the default branch changes | All artifacts (design-wide gap) |
| CV-002-iter005 | **Critical** | Strip set inconsistency: STRIDE model and attack-surface show `projects/` only; ADR-003 and requirements show `projects/` AND `tests/` — security analysis conducted on different artifact composition | STRIDE pipeline; attack-surface pipeline; REQ-022 STRIDE change |
| CV-003-iter005 | **Major** | REQ-026 install command references old Phase-1 in-repo model (`geekatron/jerry@cowork-skeleton`) — contradicts Phase-2 dedicated-repo distribution model where per-user install may not apply | REQ-026 |
| CV-004-iter005 | **Major** | GitHub App token "≤ ~8h" claim contradicts known 1-hour installation token lifetime; STRIDE states "~8h" as primary value while ADR-003 states "~1h, ≤ ~8h" — internal inconsistency | ADR-003 D3; STRIDE Area 5 |
| CV-005-iter005 | **Major** | ≤6h detection SLA presented as deterministic; GitHub Actions scheduled workflows have no guaranteed delivery-time — SLA is best-effort, not hard | ADR-003 D7; REQ-035; NFR-006 |
| CV-006-iter005 | **Major** | OQ-047: API endpoint for monitoring org CoWork registration is explicitly unknown; REQ-047 (≤24h monitoring, binding MUST) is an unimplementable placeholder | REQ-047; ADR-003 RTB-3 |
| CV-007-iter005 | **Major** | ADR-003 claims STRIDE uses SC-06 for drift/staleness (GREEN); actual STRIDE model uses SC-06 for trusted-maintainer rogue build (YELLOW 8) and SC-07 for drift — claimed collision does not exist | ADR-003 Threat Basis identifier-collision note |
| CV-008-iter005 | **Minor** | R-001 ~5,000-file CoWork limit framed inconsistently — some sections present as settled fact, R-001 header explicitly labels it the "primary unresolved risk" | R-001; ADR-001 L0; REQ-001 |

---

## Detailed Findings

### CV-001-iter005: Plugin Update Delivery Mechanism Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Design-wide gap — all 5 artifacts |
| **Strategy Step** | Step 3 (Independent Verification) |

**Evidence (claim in deliverables):**
- ADR-003 D1: "An org admin registers that repo once (server-side); it then appears for every user under 'Your organization.'"
- ADR-001 L0: "CI rebuilds it on every release" (describes CI action, not user-side update)
- Requirements STK-002: "The CoWork distribution must remain automatically in sync with `main` on every release, without manual repository surgery"
- REQ-029 (SHOULD): "The Explanation document SHALL describe the version-alignment mechanism: how the CoWork client resolves updates"

**Analysis:**
The project's primary goal is that CoWork users get automatic updates when a new release triggers skeleton regeneration. But no artifact describes the mechanism by which CoWork delivers updates to users who already have the plugin installed. The only install-time behavior described is: "A Claude Code plugin install clones the branch and materializes its working tree at the tip commit, then copies that tree to a cache (`~/.claude/plugins/cache`)" (ADR-001). This describes INITIAL INSTALL only. The update/refresh cycle is completely unspecified:

- Does CoWork re-clone on every session? On a periodic schedule? Only when `plugin.json.version` changes?
- Is there a background update agent, or does the user need to manually trigger an update?
- Does the dedicated-repo model change the update path vs. the old in-repo model?

REQ-029 acknowledges this mechanism needs documentation, which confirms the design is aware of the gap. But a SHOULD-priority documentation requirement is insufficient for a LOAD-BEARING behavioral assumption that the entire distribution model depends on. If CoWork doesn't auto-update cached plugins, the "automatically in sync" goal fails entirely.

**Recommendation:**
OWNER: nse-requirements — Add a MUST-priority requirement (before Phase-5) to empirically verify and document the CoWork plugin update mechanism as part of the R-001 smoke-test gate. The R-001 verification artifact (`verification/R001-clean-clone-count.md`) should include dimension (e) confirming update delivery: install a plugin, push a skeleton update, and verify the change reaches the installed client within the expected window. Upgrade REQ-029 from SHOULD to MUST.

---

### CV-002-iter005: Strip Set Inconsistency Across Security Artifacts [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | STRIDE model "Architecture Under Analysis" pipeline; STRIDE REQ-022 change; attack-surface.md pipeline |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence (claim being contradicted):**
STRIDE threat model "Architecture Under Analysis" pipeline:
> `2. git rm -r projects/ ; inject static projects/README.md stub`

STRIDE model REQ-022 change:
> `git diff "${TAG}..HEAD" -- ':!projects/'` (only `':!projects/'`)

Attack-surface.md "Skeleton Regeneration Job":
> `- strips projects/ directory`

**Authoritative specification (ADR-003 D1 pipeline and REQ-002):**
ADR-003:
> `3. git rm -r projects/ tests/ ; inject static projects/README.md stub (ADR-001, amended)`

REQ-002:
> "The skeleton generation script SHALL strip the `projects/` directory AND the `tests/` directory entirely"

**Analysis:**
The Phase-2 STRIDE threat model and attack-surface.md both describe an artifact that strips only `projects/` — the Phase-1 strip set. The Phase-2 amendment to ADR-001 (2026-06-28, the same date as both security documents) explicitly added `tests/` to the strip set. Both security analysis documents were written without incorporating this change.

This creates three concrete problems:
1. **Threat model accuracy**: The STRIDE model analyzed an artifact composition with ~1,744 files (projects/ only stripped), not ~1,417 files (both stripped). The threat landscape for the faithful-derivative gate was analyzed against the wrong artifact.
2. **Faithful-derivative gate specification gap**: The STRIDE model's REQ-022 change specifies `':!projects/'` only. If implemented as specified in the STRIDE model rather than per ADR-003/REQ-022, the gate would not exclude `tests/` from comparison — causing false-positive gate failures on the `tests/` directory difference.
3. **Cross-artifact consistency violation**: The security artifacts are not consistent with the generative specification they were supposed to analyze.

**Recommendation:**
OWNER: eng-architect (STRIDE/security documents), nse-requirements (REQ-022 AC) — Update both the STRIDE threat model pipeline diagram (Area 1 / Architecture Under Analysis) and the attack-surface.md pipeline to show `git rm -r projects/ tests/`. Confirm the REQ-022 acceptance criterion in the requirements shows `':!projects/' ':!tests/'` (which it does in the requirements document itself, but the STRIDE model's REQ-022 change shows only `':!projects/'`). This is an internal consistency fix required before Phase-5; the actual ADR-003 and REQ-022 (in requirements) are correct.

---

### CV-003-iter005: REQ-026 Tutorial Command References Phase-1 In-Repo Model [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-026; requirements WS-4 |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence (claim):**
REQ-026:
> "The Tutorial SHALL instruct users to install the marketplace via the Git-based command `claude plugin marketplace add geekatron/jerry@cowork-skeleton`"

**Contradicted by:**
ADR-003 D1:
> "There is no per-user 'add by URL' in the confirmed CoWork build, so org registration is the sole distribution channel."
> "Distribution is ... `geekatron/jerry-cowork`" (dedicated repo)

STRIDE L0:
> "no per-user add-by-URL path — org-level only; remote/account-managed"

**Analysis:**
REQ-026 instructs the Tutorial to document a per-user install command (`claude plugin marketplace add geekatron/jerry@cowork-skeleton`) that:
1. References the source repo (`geekatron/jerry`) not the dedicated repo (`geekatron/jerry-cowork`)
2. References the old in-repo branch name (`cowork-skeleton`) not a dedicated-repo path
3. Is potentially inapplicable under the Phase-2 model where distribution is org-admin server-side registration with no per-user add-by-URL path

If the Phase-2 model truly has no per-user install command, REQ-026 documents a mechanism that doesn't exist. Users following this tutorial would run a command against the wrong target even if the command type is valid.

**Recommendation:**
OWNER: nse-requirements — REQ-026 must be updated to reflect the Phase-2 distribution model. If org-admin registration is the sole install path, the tutorial should document the org-admin registration steps (canonical repo name: `geekatron/jerry-cowork`, registration procedure, runbook ref) rather than a per-user CLI command. The empirical discovery of the org-registration flow (from `research/cowork-plugin-install-mechanism.md`) should be used to rewrite REQ-026 with the correct installation instruction.

---

### CV-004-iter005: GitHub App Token Lifetime "≤ ~8h" Contradicts Platform Documentation [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D3; STRIDE Area 5 credential table; STRIDE CI-01 mitigation |
| **Strategy Step** | Step 3 (Independent Verification) |

**Evidence (claim):**
ADR-003 D3:
> "Minted in-job, short-lived (~1 h, ≤ ~8 h)"

STRIDE threat model Area 5 table:
> "Short-lived (~8 h), minted in-job"

STRIDE CI-01 mitigation:
> "GitHub App **installation token minted in-job** (short-lived ≈8 h)"

**Independent verification (P-022 — believed true, not verified by design package):**
GitHub App installation access tokens have a documented lifetime of **1 hour** per GitHub's App documentation. There is no documented option for 8-hour lifetime GitHub App installation tokens. The 1-hour figure appears in the ADR-003 D3 range ("~1 h, ≤ ~8 h") as the lower bound, which correctly matches GitHub platform behavior.

**Analysis:**
The STRIDE model uses "~8 h" as the primary value (not a range) in two separate places, creating an inconsistency with ADR-003's "~1 h, ≤ ~8 h" range. The correct value is 1 hour. Implementation teams relying on the STRIDE model's "~8 h" figure could design long-running job steps assuming token validity beyond the 1-hour expiry, causing job failures. The "≤ ~8 h" upper bound in ADR-003 is also not substantiated — the source of the 8-hour figure is untraced in any reference.

**Recommendation:**
OWNER: ps-architect (ADR-003) — Update ADR-003 D3 to state the correct GitHub App installation token lifetime ("~1 h, expires with the job") and remove the "≤ ~8 h" upper bound unless a specific GitHub configuration is cited that enables extended token lifetime. Update the STRIDE model Area 5 and CI-01 mitigation to use "~1 h" consistently. Add an empirical confirmation step to Phase-5 gate to verify actual token expiry behavior.

---

### CV-005-iter005: ≤6h Detection SLA Presented as Deterministic [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D7; REQ-035; NFR-006 |
| **Strategy Step** | Step 3 (Independent Verification) |

**Evidence (claim):**
ADR-003 D7:
> "Detection SLA. Bounded by the poll cadence (≤ 6 h) rather than near-real-time event delivery"

REQ-035 acceptance criterion:
> "Detection SLA ≤ 6 h (aligned with NFR-006 updated cadence)"

NFR-006:
> "≤ 6-hourly detection SLA"

**Independent verification (P-022 — believed true, not verified by design package):**
GitHub Actions scheduled workflows (`on: schedule: cron:`) are processed by GitHub's shared scheduler infrastructure. GitHub's own documentation states that scheduled workflows "may experience delays during periods of high load" and notes that scheduled workflows in inactive repositories may be automatically disabled. GitHub does not guarantee scheduled workflows will fire within any specific time window from the configured cron expression.

**Analysis:**
The design presents "≤6h" as a hard detection SLA. In practice:
- The 6h window is a cron interval, not an absolute guarantee
- GitHub scheduler delays can extend actual detection time beyond 6h
- The meta-monitor (REQ-044) alerts after 25h of monitor silence — a 19-hour gap between the stated SLA and the first alert for monitor failure
- No artifact acknowledges this uncertainty, presenting the SLA as deterministic

For a C4 security claim about tamper detection of executable hooks reaching all org users, the difference between "SLA ≤6h" and "best-effort ≤6h with possible delays" is material.

**Recommendation:**
OWNER: nse-requirements — Reframe the detection SLA in REQ-035 and NFR-006 as "target ≤6h (best-effort, subject to GitHub Actions scheduler availability)" and add a hardening note that the meta-monitor (25h) provides the actual upper bound for detection of monitor failure. Consider supplementing with an event-driven trigger where possible (e.g., monitoring via GitHub API polling from a more reliable external service) for the C4 security posture. ADR-003 should acknowledge this scheduling uncertainty in D7.

---

### CV-006-iter005: OQ-047 Monitoring Endpoint Unknown — REQ-047 Unimplementable [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-047; ADR-003 RTB-3 |
| **Strategy Step** | Step 3 (Independent Verification) |

**Evidence (explicit acknowledgment in deliverable):**
REQ-047:
> "**OPEN QUESTION (OQ-047):** The specific GitHub API endpoint (or CoWork platform API) for querying the org's currently registered CoWork plugin source is not documented in ADR-003 and requires empirical discovery before this requirement can be implemented; this requirement is a binding SHALL placeholder"

REQ-047 AC:
> "(a) **OPEN QUESTION (OQ-047) — endpoint not yet identified:** this AC is provisional and SHALL be updated when the API endpoint is empirically discovered before Phase 6."

ADR-003 RTB-3:
> "an automated monitor (REQ-047) queries the org's registered CoWork source ≤ daily (target ≤ 24 h) and alerts on any drift" — asserts monitoring is possible; no endpoint cited

**Analysis:**
REQ-047 (≤24h automated org-registration monitoring) is the primary technical-detection compensator for RTB-3 (org-registration trust boundary). It is labeled "Should" priority with binding SHALL language for the automated detection mechanism. The entire control depends on a platform API endpoint that doesn't exist in any current documentation.

Without this endpoint:
- RTB-3's "detect-and-respond, not prevent" posture has no automated detection mechanism
- The 24h detection window for rogue org registration is unachievable
- The compensating control for REQ-043's process-only two-admin requirement is absent
- A compromised org-owner could re-register to a malicious repo and the drift would only be detected by manual ≤monthly audit (per REQ-043)

This is not just a documentation gap — it is a blocking unknowm for a MUST-priority security control.

**Recommendation:**
OWNER: nse-requirements (REQ-047), eng-architect (security feasibility) — OQ-047 must be resolved before Phase-5. Options:
1. Query the CoWork platform API (if one exists) for the registered plugin source
2. Use GitHub's org audit log API to detect marketplace-settings changes (GitHub Enterprise may expose this)
3. Use a periodic screenshot/diff of the CoWork marketplace admin panel as a manual compensating control if no API exists
4. If no API endpoint is discoverable, downgrade RTB-3's posture to manual-only and explicitly document the detection gap in the project's residual risk register. Add this as a Phase-5 gate blocker.

---

### CV-007-iter005: SC-06 Identifier Collision Claim Contradicted by STRIDE Model [Major]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 Threat Basis identifier-collision note |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence (claim):**
ADR-003 Threat Basis:
> "Identifier-collision note (cross-artifact consistency): the Phase-2 STRIDE model already uses the label `SC-06` for a *different* threat (two-repo drift / staleness, banded GREEN). The trusted-maintainer rogue build is tracked as `SC-06` in **this ADR and the requirements mirror (REQ-051)**; the Phase-3 STRIDE update MUST reconcile the collision — renumbering the drift threat — so a single `SC-06` denotes the trusted-maintainer build consistently across all three artifacts."

**Verified against STRIDE model:**
STRIDE Consolidated Threat Register:
- Row 15: SC-06 = "Trusted-maintainer rogue build (faithful malicious build)" | 2×4=8 | YELLOW
- Row 20: SC-07 = "Two-repo drift" | 2×3=6 | GREEN

STRIDE Area 4 table:
- SC-06 = Trusted-maintainer rogue build (YELLOW 8)

**Analysis:**
The STRIDE model does NOT use SC-06 for drift. It uses SC-06 for the trusted-maintainer rogue build (matching ADR-003's usage) and SC-07 for drift. The collision claimed in ADR-003 does not exist in the current STRIDE model document. ADR-003's "identifier-collision note" is therefore incorrect — it directs a Phase-3 STRIDE update to reconcile a problem that either has already been reconciled (the STRIDE model was updated after ADR-003 was written) or never existed.

The practical consequence is that the Phase-3 STRIDE update's instruction ("renumbering the drift threat") would be acting on a false premise, potentially creating a new inconsistency where drift gets renumbered away from SC-07 unnecessarily.

**Recommendation:**
OWNER: ps-architect (ADR-003) — Remove or correct the identifier-collision note in ADR-003 Threat Basis to reflect the current state: SC-06 is consistently used for the trusted-maintainer rogue build across both ADR-003 and the current STRIDE model; SC-07 is the drift threat in the STRIDE model. The Phase-3 STRIDE update note should be revised to simply confirm SC-06/SC-07 consistency rather than prescribing renumbering.

---

### CV-008-iter005: R-001 Limit Presented Inconsistently [Minor]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 L0; REQ-001; R-001 header |
| **Strategy Step** | Step 4 (Consistency Check) |

**Evidence (inconsistency):**
R-001 header (requirements):
> "**This is the project's primary unresolved risk.** A three-dimensional verification (REQ-034) MUST be completed and its machine-checkable artifact committed BEFORE Phase 2 begins."

ADR-001 L0 (same document set):
> "the ~5,000-file ceiling" presented as the basis for the design without qualification

REQ-001:
> "CoWork enforces a ~5,000-file plugin-load limit" — stated as fact, not assumption

ADR-001 Context:
> "settling fact, well under the ceiling" — regarding ~1,417 files

**Analysis:**
While R-001 correctly flags the 5,000-file limit as the primary unresolved risk, REQ-001 and portions of ADR-001 present the limit as a confirmed constraint. This inconsistency in framing could lead readers of individual sections to underestimate the risk's impact. The design is self-aware (R-001 is prominently flagged), but the inconsistency exists.

**Recommendation:**
OWNER: nse-requirements — Add a consistent qualifier to REQ-001 ("Subject to R-001 verification") and ensure all design language that presents the limit as established fact includes a cross-reference to R-001's unresolved status. This is editorial but important for C4 accuracy.

---

## Verification Summary

| Claim | Verdict | Finding |
|-------|---------|---------|
| CL-001 (strip set yields ~1,417 files) | PARTIALLY CONTRADICTED (STRIDE/attack-surface omit tests/) | CV-002-iter005 |
| CL-002 (CoWork loads DEFAULT branch) | VERIFIED | — |
| CL-003 (CoWork auto-updates installed users) | UNVERIFIED | CV-001-iter005 |
| CL-004 (Org-level ruleset non-overridable by repo admins) | VERIFIED | — |
| CL-005 (`gh attestation verify` detects tampering) | VERIFIED | — |
| CL-006 (≤6h detection SLA) | UNVERIFIED | CV-005-iter005 |
| CL-007 (App token ≤ ~8h) | CONTRADICTED (likely 1h) | CV-004-iter005 |
| CL-008 (`git merge-base --is-ancestor`) | VERIFIED | — |
| CL-009 (OQ-047 monitorable) | EXPLICITLY UNVERIFIED | CV-006-iter005 |
| CL-010 (No cross-repo event subscription) | VERIFIED | — |
| CL-011 (STRIDE strip set matches ADR-003) | CONTRADICTED | CV-002-iter005 |
| CL-012 (App as sole bypass actor) | VERIFIED | — |
| CL-013 (SC-04 found by 5 of 8 strategies) | VERIFIED (internally) | — |
| CL-014 (SC-06 collision in STRIDE model) | CONTRADICTED | CV-007-iter005 |
| CL-015 (Tip SHA non-forgeable) | VERIFIED | — |
| CL-016 (REQ-026 install command) | CONTRADICTED | CV-003-iter005 |
| CL-017 (R-001 file-count assumption) | UNVERIFIED (acknowledged) | CV-008-iter005 |
| CL-018 (Immutable releases GA) | VERIFIED with caveat | — |
| CL-019 (Per-job permissions isolation) | VERIFIED | — |

**Claims Verified:** 11 of 19
**UNVERIFIED:** 3 (CL-003, CL-006, CL-009 + CL-017 acknowledged)
**CONTRADICTED:** 4 (CL-007, CL-011, CL-014, CL-016)
**Verification Rate:** 58% (11/19)

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 2
- **Major:** 5
- **Minor:** 1
- **Total load-bearing claims with UNVERIFIED/CONTRADICTED verdict:** 7 (CL-003, CL-006, CL-007, CL-009, CL-011, CL-014, CL-016)
- **Protocol Steps Completed:** 5 of 5

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CV-001: update delivery mechanism is a design-wide gap; CV-006: OQ-047 is a binding SHALL with no implementation path |
| Internal Consistency | 0.20 | Negative | CV-002: STRIDE/attack-surface strip-set contradiction; CV-007: SC-06 collision claim incorrect; CV-003: REQ-026 references wrong model |
| Methodological Rigor | 0.20 | Negative | CV-005: SLA presented as deterministic without acknowledging scheduler uncertainty; CV-002: security analysis conducted on wrong artifact composition |
| Evidence Quality | 0.15 | Mixed | Most VERIFIED claims are well-sourced; UNVERIFIED claims (CL-003, CL-009) lack any source in the design package |
| Actionability | 0.15 | Positive | All findings include specific, owner-tagged remediation recommendations |
| Traceability | 0.10 | Negative | CV-003: REQ-026 trace breaks (Phase-2 model inconsistency); CV-007: ADR-003 cross-reference to STRIDE is incorrect |

---

*Generated by: adv-executor (S-011 Chain-of-Verification)*
*Strategy: S-011 CoVe | Template: `.context/templates/adversarial/s-011-cove.md`*
*Project: PROJ-031-cowork-skeleton | Iteration: 005 | Group: D*
*Blindness constraint honored: no iteration-005 adversary outputs read*
*Self-review applied per H-15 before persistence*
*Date: 2026-06-29*
