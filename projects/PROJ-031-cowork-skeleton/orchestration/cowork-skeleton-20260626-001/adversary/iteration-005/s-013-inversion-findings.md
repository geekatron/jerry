# Inversion Report: PROJ-031 CoWork Skeleton Distribution Design

**Strategy:** S-013 Inversion Technique
**Deliverable:** ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md
**Criticality:** C4
**Date:** 2026-06-29T00:00:00Z
**Reviewer:** adv-executor (iteration-005)
**H-16 Compliance:** S-003 Steelman applied in prior tournament iterations (confirmed per ADR-003 S-010 note and ADR-001 footer)
**Goals Analyzed:** 5 | **Assumptions Mapped:** 18 | **Vulnerable Assumptions:** 9

---

## Summary

Applying full goal-inversion and assumption stress-testing against the five design artifacts, the Inversion reveals two Critical and seven Major/Minor vulnerable assumptions. The most structurally dangerous finding is not in the threat model (which is well-constructed) but in the *monitoring architecture*: the D7 integrity monitor is designed to detect **tampering** (unauthorized tip-SHA replacement) but is **blind to regeneration failure** — if the CI generation job fails for a release, the monitor reports GREEN because the stale prior-release skeleton still has a valid attestation. This silent-failure path has no current implemented control; the liveness monitor (REQ-049) that would catch it is still a draft requirement. A second Critical is that the entire branch-stripping strategy rests on a file-count-measurement basis (tracked files in clean clone vs. local working directory) that has never been empirically confirmed. ACCEPT with mitigations: Critical findings must be resolved before Phase 5 authorization.

---

## Findings Summary

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-i005 | CoWork limit basis unverified: entire strategy may be measuring the wrong thing | Assumption | Low | Critical | ADR-001 L2 §4, R-001, REQ-034 | Methodological Rigor |
| IN-002-i005 | Regeneration-failure invisibility: monitor validates attestation existence, not generation completeness | Assumption | Medium | Critical | ADR-003 D7, REQ-035, REQ-049 (DRAFT) | Internal Consistency |
| IN-003-i005 | Prevention posture unvalidated: bypass-actor ruleset semantics not yet empirically confirmed | Assumption | Medium | Major | ADR-003 D2, Negative §4, S-010 note | Evidence Quality |
| IN-004-i005 | All Phase-2 security controls are DRAFT: go-live may precede implementation of REQ-038–REQ-051 | Anti-Goal | N/A | Major | phase1-requirements.md Status column (all "Draft"), ADR-003 Status "Proposed" | Completeness |
| IN-005-i005 | Session-start hooks + ≤6h SLA = bounded-but-real harm window if CoWork auto-refreshes plugins | Assumption | Medium | Major | ADR-003 L2 §3, D7, RTB-5 | Actionability |
| IN-006-i005 | CoWork plugin update cadence undocumented — "automatically in sync" claim is unjustified | Assumption | Low | Major | ADR-001 L0, phase1-requirements.md STK-002, no REQ for update cadence | Completeness |
| IN-007-i005 | Trusted-maintainer rogue build currently unconstrained — REQ-051 is DRAFT | Assumption | Medium | Major | ADR-003 RTB-2, SC-06 (STRIDE score 8 Y), REQ-051 (DRAFT) | Methodological Rigor |
| IN-008-i005 | Stub static-content constraint has no CI enforcement gate | Assumption | Medium | Minor | ADR-001 §Stub Determinism Constraint, REQ-004a AC, REQ-003 | Traceability |
| IN-009-i005 | Retention surface definition lists only "must include" — shipped content is larger and undocumented | Anti-Goal | N/A | Minor | ADR-001 Canonical Plugin-Retention Surface, note on docs/, scripts/ etc. | Completeness |

---

## Detailed Findings

### IN-001-i005: CoWork File-Count Limit Measurement Basis Is Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-001 L2 §4; phase1-requirements.md R-001; REQ-034 |
| **Strategy Step** | Step 4 — Stress-test Assumptions |

**Original Assumption:** The CoWork plugin-load limit of approximately 5,000 files applies to the **tracked file count of a clean-clone working tree** (no `.venv/`, no `__pycache__`, no untracked files). R-001 explicitly calls this the project's "primary unresolved risk" — the limit "is a CoWork/Claude-Desktop runtime constraint per the project's settled facts and still warrants empirical confirmation."

**Inversion:** What if CoWork measures the **local working directory** (including `.venv/` ≈ 24,636 additional files) rather than the tracked-file clean-clone count? If so, branch-stripping has zero effect on the load failure — the skeleton branch would show ~1,417 tracked files and still fail to install because the local Python environment inflates the count beyond any safe threshold.

**Plausibility:** Moderate-High. The limit is undocumented by Anthropic. The "decisive framing" (ADR-001 Context §Decisive Framing) establishes that install materializes the tip working tree and excludes gitignored artifacts — but this reasoning applies to a clean clone, and CoWork's actual runtime measurement method is extrapolated from vendor behavior, not confirmed. ADR-001 explicitly states: "if CoWork instead counts a local working directory (`.venv/` ≈ 24,636 files), branch-stripping is the wrong lever." REQ-034 dimension (d) — the CoWork smoke test — "MAY be deferred to Phase 4 if a CoWork runtime is unavailable," leaving open the possibility of reaching Phase 5 without this confirmation.

**Consequence:** If this assumption is false, the ENTIRE engineering effort (deterministic strip, CI pipeline, attestation anchor, dedicated repo) solves the wrong problem. The correct solution would pivot to local-plugin configuration guidance. No control currently in place would detect this false assumption — only the Phase 5 go-live would surface it, at which point significant irreversible work would already have been done (org registration, credential provisioning, repo creation).

**Evidence:**
- ADR-001 L2 §4: "The strategy's validity rests on an external, still-unverified assumption."
- ADR-001 Risks table: "R-001: ~5,000-file (or size/time-based) CoWork limit is undocumented/unverified; strategy may not yield installability — MED probability, HIGH impact."
- ADR-001 adds to IN-001 scope: "a file-count-only check would falsely 'pass' a size/time failure and must not be the sole gate."
- phase1-requirements.md R-001: "A three-dimensional verification (REQ-034) MUST be completed and its machine-checkable artifact committed BEFORE Phase 2 begins."

**Dimension:** Methodological Rigor — the design's central method (branch stripping) rests on an unvalidated measurement assumption.

**Mitigation:** Execute REQ-034 dimension (a–d) in full, including dimension (d) (CoWork smoke test on a live runtime) BEFORE AG-02/AG-04 approval rather than deferring to Phase 4/5. Create machine-checkable artifact `verification/R001-clean-clone-count.md` with all four dimensions recorded as verified. Additionally: confirm whether the limit is file-count-based vs. size-based vs. time-based by testing against a minimal and a maximal repo.

**Acceptance Criteria:** `verification/R001-clean-clone-count.md` exists with all four dimensions showing PASS, including a successful CoWork install smoke test on a clean clone of `geekatron/jerry-cowork`. The document must be reviewed and committed before Phase 5 authorization.

**Owner:** nse-requirements

---

### IN-002-i005: Regeneration-Failure Invisibility — Monitor Is Blind to Stale Deployments [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-003 D7; REQ-035; REQ-049 (DRAFT); NFR-006; phase2-stride-threat-model.md SC-07 |
| **Strategy Step** | Step 2 — Invert Goals; Step 4 — Stress-test Assumptions |

**Original Assumption:** The D7 backstop monitor detects both (a) tampering (unauthorized modification of the deployed tip) AND (b) generation failure (the regeneration job not running or failing for a new release). The design goal is that the skeleton "remains automatically in sync with main on every release" (STK-002).

**Inversion:** The D7 monitor does NOT detect generation failure. The monitor architecture:
1. Reads the dedicated repo's live default-branch tip SHA via `git ls-remote` / `gh api`
2. Runs `gh attestation verify <that-tip-SHA> --repo geekatron/jerry`
3. If attestation exists for that SHA → returns PASS

**Failure path:** Release v0.32.0 is tagged. The `cowork-skeleton.yml` generation job fails (e.g., GitHub Actions quota exhausted, workflow file syntax error from a recent commit, transient API error). The dedicated repo tip remains v0.31.5's skeleton SHA. That SHA has a valid v0.31.5 attestation. The monitor runs → `gh attestation verify <v0.31.5-SHA>` → PASS. The meta-monitor confirms the monitor ran successfully → PASS. CoWork users install v0.31.5 indefinitely. No alert fires.

**Plausibility:** High. GitHub Actions jobs fail transiently. The monitoring design is explicitly scoped to tamper-detection: ADR-003 D7 describes the monitor as a "reduced backstop integrity monitor" for "residual credential-theft / admin-suppression attack paths" — not for generation-failure detection. The distinction between "valid attestation for stale tip" and "valid attestation for current tip" is exactly the gap.

REQ-049 (phase1-requirements.md) addresses this: "A liveness monitor SHALL verify the latest source `v*` tag produced a dedicated-repo deployment within **2 h** of the tag-push timestamp." However, REQ-049 status is **DRAFT** — it is not yet implemented. There is no currently-implemented control that detects generation failure for a specific release.

**Consequence:** Security patches or breaking-change fixes in a new release silently fail to reach users. Users believe they are running the current version (the plugin shows "installed"), but they are running a stale release. If the fix addresses an adversarial finding discovered post-release (e.g., a prompt injection vulnerability in a skill file), the vulnerability remains live in production indefinitely until someone manually notices the staleness.

**Evidence:**
- ADR-003 D7: Monitor's purpose is "residual backstop detection for DR-02, CR-03 (post-prevention)" — credential-theft and admin-suppression paths, not generation failure.
- phase2-stride-threat-model.md SC-07: "Two-repo drift — Dedicated default branch silently drifts from latest source release (CI failed/pushed stale)" — scored GREEN (6) with mitigation "Lazy-staleness via `Source-Commit` trailer." BUT: the trailer is explicitly labeled FORGEABLE in ADR-001 (cannot detect targeted tampering); it detects CI-never-regenerated laziness, NOT a CI failure that fires and fails silently.
- phase1-requirements.md REQ-049: Status "Draft" — no implementation exists.

**Dimension:** Internal Consistency — the system claims to keep the skeleton in sync, but the monitoring architecture only detects unauthorized replacement, not authorized-but-failed regeneration.

**Mitigation:** Implement REQ-049 before Phase 5: a liveness monitor that checks whether the latest `v*` tag (from `git ls-remote --tags geekatron/jerry`) has produced a matching deployment to the dedicated repo within 2 hours of the tag-push timestamp. This requires comparing: (a) the timestamp of the newest `v*` tag on the source repo, vs. (b) the committer date embedded in the skeleton's deterministic commit (retrievable via `git show` or `gh api`). Mismatch → open GitHub issue with specific gap: "Tag v0.32.0 pushed at {time} but dedicated repo still shows v0.31.5 skeleton at {time+2h}."

**Acceptance Criteria:** REQ-049 implemented and tested: trigger a generation failure (syntax error in workflow, mocked API timeout) and confirm a GitHub issue opens within 2 hours identifying the specific missing release. Monitor distinguishes "monitor self-failure" from "generation did not fire."

**Owner:** nse-requirements

---

### IN-003-i005: Prevention Posture Is Empirically Unvalidated — Could Silently Revert to Detection-Only [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D2, Consequences §Negative 4, S-010 Self-Refine note |
| **Strategy Step** | Step 4 — Stress-test Assumptions |

**Original Assumption:** The org-level ruleset on `geekatron/jerry-cowork` with the GitHub App / deploy key as the sole bypass actor ACTUALLY prevents non-CI principals from pushing to the dedicated repo's default branch.

**Inversion:** GitHub's bypass-actor and org-level ruleset semantics might not behave exactly as documented for this specific configuration (App-as-sole-bypass on an org-level ruleset, non-overridable by repo admins). ADR-003 S-010 Self-Refine Note explicitly states: "the immutable-release / attestation mechanics and the ruleset bypass-actor configuration are validated against current (2025–2026) GitHub vendor documentation as cited in the Phase-2 model, not yet exercised on `geekatron/jerry-cowork`. They SHOULD be confirmed empirically before Phase-5."

**Plausibility:** Moderate. GitHub ruleset bypass actors are confirmed in changelog (Sep 2025) but are a relatively new feature; edge cases in org-level vs. repo-level precedence, or App permission model specifics, could produce unexpected behavior. The gap between "documented behavior" and "observed behavior on this specific repo" is real until tested.

**Consequence:** If the prevention posture is misconfigured or doesn't work as expected, the design reverts to detection-only — the Phase-1 unprotected-branch Critical (R-007b) would be re-opened without anyone knowing. This would not be detected by the D7 monitor (which checks tip SHA, not permission configuration). Detection would only occur if a push is attempted and unexpectedly succeeds.

**Evidence:** ADR-003 Consequences §Negative 4: "Dependence on current GitHub features. Immutable releases, build-provenance attestations, and ruleset bypass-actor semantics are recent (2025–2026). Mitigation: confirm empirically before Phase-5; fall back to deploy-key + scheduled-monitor posture if a feature is unavailable."

**Mitigation:** Add a Phase-2 / pre-Phase-5 gate to empirically verify: (1) create `geekatron/jerry-cowork`, (2) apply the org-level ruleset with the App/deploy-key as sole bypass actor, (3) attempt a direct push from a collaborator-level credential and confirm rejection with the expected error, (4) confirm the App/deploy key CAN push. Document the observed behavior in a verification artifact. Add REQ-046 extension: include ruleset presence and bypass-actor count verification in the weekly scheduled monitor.

**Acceptance Criteria:** Verification artifact recorded confirming that (a) collaborator-level push is rejected, (b) App/deploy-key push succeeds, (c) ruleset cannot be overridden by a repo-admin credential. Weekly monitor (REQ-046) checks that bypass-actor list has exactly one entry.

**Owner:** ADR→ps-architect; implementation→eng-architect

---

### IN-004-i005: All Phase-2 Security Controls Are DRAFT Status — Go-Live May Precede Implementation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | phase1-requirements.md Status column (all "Draft"); ADR-003 Status "Proposed" |
| **Strategy Step** | Step 2 — Invert Goals |

**Original Assumption:** All security requirements (REQ-038 through REQ-051, plus changes to REQ-020/035/042/043/NFR-006) are implemented before Phase 5 authorization and go-live.

**Inversion:** The orchestration plan gates implementation on AG-04 user approval. However, there is no explicit pre-Phase-5 checklist that maps each DRAFT security requirement to a verified implementation. A go-live gating document could be created and approved without each sub-requirement being independently verified. The path from "Draft" to "Implemented and Tested" is not itself guarded by an automated control.

**Plausibility:** Moderate. The orchestration plan includes quality gates (QG-2) but these are adversarial quality reviews of the DESIGN artifacts, not verification that IMPLEMENTATIONS exist. It's structurally possible for QG-2 to PASS (the design is sound) while the actual implementation is incomplete.

**Consequence:** The dedicated repo goes live with:
- No provenance assertion (D5/REQ-038) → rogue-tag attack possible
- No `v*` tag protection (REQ-039) → any collaborator can push a rogue tag
- No liveness monitor (REQ-049) → generation failures invisible
- No main-branch peer review enforcement (REQ-051) → trusted-maintainer rogue build unconstrained

This would not be immediately detected — the system would *appear* to work, but the attack surface would be the same as if no Phase-2 STRIDE work had been done.

**Evidence:** All WS-3 requirements in phase1-requirements.md (REQ-019 through REQ-051) have Status = "Draft." ADR-003 Status = "Proposed" pending AG-04.

**Mitigation:** Create an explicit "Phase-5 Authorization Checklist" that maps each REQ-038–REQ-051 to a verifiable CI or audit artifact. The checklist should be a committed document that the orchestrator verifies before AG-05 (Phase 5 go-live authorization). Consider adding REQ-034d-equivalent CI gate for security control verification: a scheduled job that checks for presence of the org ruleset, tag protection, liveness monitor workflow, and peer-review enforcement.

**Acceptance Criteria:** A committed checklist document with every Phase-2 security requirement marked with either "Verified by test X" or "Confirmed by inspection of Y" before Phase 5 begins.

**Owner:** requirements→nse-requirements; orchestration→orch-planner

---

### IN-005-i005: Session-Start Hooks + ≤6h Detection SLA = Real Harm Window During Tamper Window [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 L2 §3, RTB-5, D7; phase2-stride-threat-model.md SC-03 |
| **Strategy Step** | Step 3 — Map Assumptions |

**Original Assumption:** The ≤6h detection SLA is an acceptable residual risk because CoWork users install on-demand and tampered hooks would only harm a bounded number of sessions before the alert fires and the skeleton is reverted.

**Inversion:** The assumption that "bounded sessions" implies acceptable harm rests on an undocumented assumption about CoWork's update behavior. If CoWork auto-updates installed org plugins on any of: (a) new session start, (b) background refresh, (c) org-admin push, then within the ≤6h detection window every org user who starts a CoWork session could execute tampered `hooks/session-start.py`. The blast radius is the full org user base, not a subset.

**Plausibility:** High. The artifact "executes on every session start" (ADR-003 L2 §3). The update mechanism is undocumented. If CoWork periodically refreshes the installed plugin cache from the dedicated repo (similar to how a package manager auto-updates), the tamper window could trigger mass execution. RTB-5 explicitly acknowledges: "a tampered tree installed by a user between tampering and the next ≤6h monitor cycle is not verified client-side."

**Consequence:** The primary-prevention posture (D2 branch protection) makes direct-push tampering LOW probability, but for the residual cases (credential theft, org-owner suppression), the harm within the 6h window could be org-wide. The design does not include a mechanism to recall or invalidate cached plugin content from user workstations after tamper detection — the monitor only opens a GitHub issue and reverts the dedicated repo, but cannot force-update already-installed plugins.

**Evidence:** ADR-003 RTB-5: "CoWork's `claude plugin marketplace add` flow does not invoke `gh attestation verify`; the D4 attestation is not checked at the point of distribution to the end user." ADR-003 L2 §3: "The artifact is not data — it is code that runs on every user's session start." No requirement addresses auto-update behavior.

**Mitigation:** (1) Add a requirement to document and test CoWork's plugin-update trigger mechanism (when does a user get a new version?). (2) Consider adding a "plugin version sentinel" that `hooks/session-start.py` checks against a canonical published value, refusing to execute if the installed version predates the sentinel — creating a software tripwire against stale/tampered installs. (3) Reduce the monitor cadence from ≤6h to ≤1h for the credential-theft case where execution-at-scale is most likely (this is a cost/complexity tradeoff).

**Acceptance Criteria:** A documented, empirically verified answer to: "When does a CoWork user's installation update to reflect a new version of `geekatron/jerry-cowork`'s default branch?" This answer must inform the detection SLA.

**Owner:** requirements→nse-requirements; security→eng-architect

---

### IN-006-i005: CoWork Plugin Update Cadence Is Undocumented — "Automatically in Sync" Goal May Be Unjustified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | phase1-requirements.md L0, STK-002; ADR-001 L0 |
| **Strategy Step** | Step 3 — Map Assumptions |

**Original Assumption:** Stakeholder Need STK-002 states: "The CoWork distribution must remain **automatically in sync** with `main` on every release, without manual repository surgery." The design achieves sync at the repository level (dedicated repo is force-pushed on each release), implying users automatically receive updates.

**Inversion:** Repository sync does NOT equal user sync. If CoWork caches the plugin at install time and only updates on explicit user-initiated action (e.g., re-running `claude plugin marketplace add`), then users who installed v0.31.5 continue running v0.31.5 even after v0.40.0 is released. The "automatically in sync" goal is met at the distribution level but not at the consumption level.

**Plausibility:** High. Plugin caching is common behavior (CoWork research confirms "copies that tree to a cache `~/.claude/plugins/cache`"). The research does not document any auto-update mechanism. No requirement in phase1-requirements.md asks whether users receive automatic updates or must manually reinstall.

**Consequence:** Security fixes and capability updates silently fail to reach installed users. Jerry maintainers believe they are delivering updated skills/agents/rules on each release, but the majority of the user base continues running old versions. The entire "in sync" value proposition of the design is undermined if updates are not automatically received.

**Evidence:** phase1-requirements.md STK-002: "remain automatically in sync with main on every release" — stated as a stakeholder need but not validated against CoWork's actual update mechanism. No REQ verifies CoWork's update behavior.

**Mitigation:** Add a requirement: "REQ-XXX: The project SHALL document and empirically verify whether CoWork auto-updates org-installed plugins when the default branch of the registered repo is updated, or whether users must manually trigger an update." This verification must precede Phase 5. If auto-update is NOT the default, the user-facing documentation (WS-4) must include explicit instructions for how users stay current.

**Acceptance Criteria:** Documented and empirically tested answer to: "Does CoWork auto-refresh the local plugin cache when the default branch of the registered org plugin repo is force-pushed to?" Result committed to `verification/cowork-update-mechanism.md`.

**Owner:** requirements→nse-requirements; documentation→diataxis

---

### IN-007-i005: Trusted-Maintainer Rogue Build Is Currently Unconstrained — REQ-051 Is DRAFT [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 RTB-2, SC-06; phase2-stride-threat-model.md SC-06; phase1-requirements.md REQ-051 (DRAFT) |
| **Strategy Step** | Step 4 — Stress-test Assumptions |

**Original Assumption:** The trusted-maintainer rogue-build path (SC-06) is controlled by peer-review enforcement on `main` (REQ-051): "require at least one independent approving review for every commit to main, enforced for all principals holding `v*` tag-create rights."

**Inversion:** REQ-051 status is **DRAFT**. Until it is implemented as a branch-protection ruleset on `geekatron/jerry`'s `main`, a single maintainer holding both `main`-write and `v*` tag-create rights CAN: (1) commit malicious content to `main` without a review, (2) push a `v*` tag, (3) have CI faithfully build and attest the malicious tree, (4) have the D7 monitor return PASS (the tip IS attested, by CI, faithfully). All five defenses (D2 branch protection, D4 attestation, D5 provenance assertion, D7 monitor) PASS on a trusted-maintainer rogue build.

**Plausibility:** Moderate. This requires a malicious or compromised maintainer with dual rights. The threat is explicitly ranked SC-06 (STRIDE score 8 Y) in the STRIDE model. The compensating control (REQ-051) is the ONLY technical mitigation — but it doesn't exist yet.

**Consequence:** This is the highest-consequence unmitigated attack path that bypasses all implemented controls. The attack delivers executable hooks to every CoWork org user via the attested, monitored, protection-compliant pipeline. Detection occurs only after the fact (delivery to users, then manual review), by which point the blast radius is the full org user base.

**Evidence:** ADR-003 RTB-2: "A maintainer holding both `main`-write and `v*` tag-create rights can legitimately land a malicious commit on `main` (passing the ancestor check) and tag it; CI then faithfully builds AND faithfully attests the malicious tree." phase1-requirements.md REQ-051: Status = "Draft".

**Mitigation:** Implement REQ-051 as a blocking pre-Phase-5 requirement: configure a branch-protection ruleset on `geekatron/jerry`'s `main` requiring at least one independent approving review before any commit lands. This must be enforced for all principals who also hold `v*` tag-create rights, preventing any single maintainer from both authoring and releasing content. Confirm via test: attempt to bypass peer review with a test commit and confirm rejection.

**Acceptance Criteria:** Ruleset active on `geekatron/jerry`'s `main`. Test confirms that a principal with tag-create rights cannot bypass peer review. REQ-051 status = Verified.

**Owner:** security→eng-architect; requirements→nse-requirements

---

### IN-008-i005: Stub Static-Content Constraint Has No CI Enforcement Gate [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Stub Determinism Constraint; phase1-requirements.md REQ-004a |
| **Strategy Step** | Step 4 — Stress-test Assumptions |

**Original Assumption:** The `projects/README.md` stub contains only static prose (no timestamps, version strings, build identifiers, run numbers) forever.

**Inversion:** A well-intentioned future maintainer adds a "Generated for Jerry v{VERSION}" string or a build date to the stub (e.g., to help users identify which release their install corresponds to). This silently breaks the bit-identical SHA guarantee (REQ-003/c-002). The CI pipeline does NOT detect this because: REQ-003's acceptance criterion requires TWO separate `workflow_dispatch` runs — this test would only be run during active validation, not on every commit.

**Plausibility:** Moderate. The constraint is documented in ADR-001 §Stub Determinism Constraint and REQ-004a, but there is no automated gate in the generation script that checks the stub for dynamic-content patterns before committing. REQ-004a's acceptance criterion is "grep for patterns matching ISO 8601 timestamps, GITHUB_RUN_ID…" — this grep check EXISTS in the acceptance criteria but is not part of a continuous CI gate.

**Consequence:** Idempotency silently breaks. Two runs of the same tag produce different skeleton SHAs. The deterministic-SHA tamper-evidence property is invalidated (an attacker could plausibly claim "the SHAs differ because idempotency was broken by a stub change, not because of tampering"). The D7 monitor's comparison against the attestation still works, but the "independently recomputable expected SHA" property that gives the tamper-evidence its strength is gone.

**Evidence:** ADR-001 §Stub Determinism Constraint: "the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility." REQ-004a lists grep patterns but does not add this as a CI gate requirement.

**Mitigation:** Add an automated static-content check of `projects/README.md` as a required step in the generation script, before the deterministic commit. The check should grep for ISO 8601 timestamps, `GITHUB_RUN_ID`, `GITHUB_SHA`, `GITHUB_REF_NAME`, and common version-string patterns (`v[0-9]`, `Version:`, `Build:`). Any match → non-zero exit before commit. This makes a dynamic-content violation a CI failure rather than a silent idempotency break.

**Acceptance Criteria:** Generation script includes a pre-commit check. Test: inject a timestamp into stub → confirm CI job exits non-zero before commit.

**Owner:** requirements→nse-requirements; implementation→STORY-002

---

### IN-009-i005: Retention Surface Definition Lists "Must Include" But Not "Must Exclude" — Shipped Content Is Larger Than Documented [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 Canonical Plugin-Retention Surface; phase1-requirements.md REQ-005 |
| **Strategy Step** | Step 2 — Invert Goals |

**Original Assumption:** The 8-directory canonical plugin-retention surface is a complete accounting of what the skeleton ships to users. The definition provides clear clarity on the plugin's content.

**Inversion:** The retention surface definition is intentionally a "MUST retain" list, not an exhaustive inventory. The skeleton actually ships EVERYTHING from `main` minus `projects/` and `tests/`. This includes: `.github/workflows/cowork-skeleton.yml`, `release.yml`, `version-bump.yml`, `docs.yml`, `docs/`, `runbooks/`, `overrides/`, `scripts/`, `pyproject.toml`, `uv.lock`, `CHANGELOG.md`, `CLAUDE.md`, and other top-level files. ADR-001 explicitly acknowledges: "The remaining non-load-bearing directories `docs/`, `runbooks/`, `overrides/`, `scripts/` ARE retained today."

The specific concern: **the skeleton ships all `.github/workflows/*.yml` files** to every CoWork user. These files expose the full CI pipeline implementation (credential fetch patterns, deploy key usage, attestation steps) in a public repo. An adversary reading the delivered workflow files gains a detailed map of the pipeline's attack surface.

**Plausibility:** Confirmed fact — not a theoretical inversion. The strip is `projects/` and `tests/` only; everything else in `main` is retained.

**Consequence:** Current risk is primarily information disclosure: the CI pipeline's implementation details are shipped to all users and publicly visible in `geekatron/jerry-cowork`. This is LOW severity today because the pipeline is already in a public source repo. However, if a future CoWork version were to execute workflow files discovered in installed plugins, this would escalate to a code-execution vector. Additionally, shipping `uv.lock`, `pyproject.toml`, and `CLAUDE.md` to users adds unexpected surface area not related to CoWork plugin function.

**Evidence:** ADR-001 canonical retention surface note: "The remaining non-load-bearing directories `docs/`, `runbooks/`, `overrides/`, `scripts/` ARE retained today (~1,417 ≪ 5,000) and MAY be stripped later if the file-count margin tightens (R-002)."

**Mitigation:** Add to ADR-001 an "explicit retained non-load-bearing surface" section that lists what IS shipped beyond the 8 directories. Evaluate whether `.github/workflows/` should be stripped (adding to the strip set alongside `projects/` and `tests/`) to reduce information disclosure. Since stripping `.github/` would reduce file count further (providing additional margin), this is likely beneficial with no functional loss to CoWork users.

**Acceptance Criteria:** ADR-001 updated with a complete inventory of what is shipped. A decision is recorded on whether `.github/workflows/` should be added to the strip set.

**Owner:** ADR→ps-architect

---

## Execution Statistics

| Metric | Count |
|--------|-------|
| **Total Findings** | 9 |
| **Critical** | 2 |
| **Major** | 5 |
| **Minor** | 2 |
| **Goals Analyzed** | 5 |
| **Assumptions Mapped** | 18 |
| **Vulnerable Assumptions** | 9 |
| **Protocol Steps Completed** | 6 of 6 |

---

## Scoring Impact

Mapping Inversion findings to S-014 scoring dimensions (6 dimensions, weights from quality-enforcement.md):

| Dimension | Weight | Impact | Finding(s) | Rationale |
|-----------|--------|--------|------------|-----------|
| Completeness | 0.20 | Negative | IN-004-i005, IN-006-i005, IN-009-i005 | Missing: go-live implementation checklist; CoWork update cadence verification requirement; explicit "shipped content" accounting beyond the 8-directory retention surface. |
| Internal Consistency | 0.20 | Negative | IN-002-i005 | The design claims the skeleton "remains automatically in sync" (STK-002) and that the monitor provides integrity assurance, but the monitor architecture is blind to the most likely failure mode (generation job failure on a release). |
| Methodological Rigor | 0.20 | Negative | IN-001-i005, IN-007-i005 | Core method (branch stripping) rests on an unvalidated measurement assumption (R-001). Trusted-maintainer rogue-build path has no currently-implemented technical control (REQ-051 is DRAFT). |
| Evidence Quality | 0.15 | Negative | IN-003-i005 | Prevention posture is claimed on the basis of vendor documentation rather than empirical verification. The claim "direct push is prevented" cannot be asserted before the ruleset is configured and tested on `geekatron/jerry-cowork`. |
| Actionability | 0.15 | Positive | IN-001–IN-009-i005 | Each finding includes a specific mitigation with verifiable acceptance criteria and an owner assignment. Remediations are incremental and do not require redesign. The overall design is architecturally sound; the gap is in implementation completeness and empirical validation gates. |
| Traceability | 0.10 | Positive | All | Findings trace to specific sections in the deliverables. Owner tags map to the relevant agent types (ps-architect, nse-requirements, eng-architect). IN-NNN-i005 identifiers are consistent. |

**Overall Assessment:** ACCEPT with mitigations. The design is architecturally sound and the STRIDE model is thorough. The Inversion reveals that the gap is not in design quality but in the **transition from design to validated implementation**: (1) the foundational measurement assumption (R-001/IN-001-i005) needs empirical confirmation before Phase 5 authorization, (2) the monitoring architecture has a structural blind spot for generation failure (IN-002-i005), and (3) several Phase-2 security controls that the design depends on are still draft requirements. Addressing Critical findings (IN-001, IN-002) and the Major findings IN-003 (prevention validation) and IN-007 (REQ-051 implementation) before Phase 5 authorization would close the most significant assumption vulnerabilities.

---

## Recommendations

### Critical (MUST mitigate before Phase 5 authorization)

| Finding | Mitigation | Acceptance Criteria | Owner |
|---------|-----------|---------------------|-------|
| IN-001-i005: CoWork limit basis unverified | Execute REQ-034 all 4 dimensions including smoke test before AG-02/AG-04 | `verification/R001-clean-clone-count.md` with all 4 dimensions PASS | nse-requirements |
| IN-002-i005: Regeneration-failure invisibility | Implement REQ-049 liveness monitor BEFORE Phase 5 go-live | Liveness monitor alerts within 2h of a generation-job failure for any v* tag | nse-requirements |

### Major (SHOULD mitigate before Phase 5 authorization)

| Finding | Mitigation | Acceptance Criteria | Owner |
|---------|-----------|---------------------|-------|
| IN-003-i005: Prevention posture unvalidated | Empirical test of bypass-actor ruleset on `geekatron/jerry-cowork` before Phase 5 | Collaborator push rejected; App push succeeds; documented in verification artifact | ps-architect / eng-architect |
| IN-004-i005: Draft security requirements may not be implemented at go-live | Phase-5 Authorization Checklist mapping each REQ-038–051 to verified implementation | Committed checklist with all requirements verified before Phase 5 | nse-requirements |
| IN-005-i005: ≤6h SLA + session-start hooks = harm window | Verify CoWork auto-update behavior; reduce monitor cadence to ≤1h | Documented and tested answer to update cadence question | nse-requirements / eng-architect |
| IN-006-i005: CoWork update cadence undocumented | Add requirement to verify and document update mechanism | `verification/cowork-update-mechanism.md` committed | nse-requirements |
| IN-007-i005: Trusted-maintainer rogue build unconstrained | Implement REQ-051 (peer review on main) before Phase 5 | Ruleset confirmed active; bypass attempt rejected | eng-architect / nse-requirements |

### Minor (MAY mitigate)

| Finding | Mitigation | Acceptance Criteria | Owner |
|---------|-----------|---------------------|-------|
| IN-008-i005: Stub static-content constraint unenforced | Add pre-commit grep check in generation script | Dynamic-content injection causes CI failure | nse-requirements / STORY-002 |
| IN-009-i005: Shipped content larger than documented retention surface | Update ADR-001 with complete shipped-content inventory; evaluate .github/ strip | ADR-001 amended; decision on .github/ stripping recorded | ps-architect |

---

*Strategy: S-013 Inversion Technique*
*Execution ID: i005*
*Template: .context/templates/adversarial/s-013-inversion.md v1.0.0*
*Deliverables analyzed: ADR-001 (Phase-2 amended), ADR-003, phase1-requirements.md (iteration 5), phase2-stride-threat-model.md, phase2-attack-surface.md*
*Blindness constraint honored: no files read from adversary/iteration-001 through iteration-004*
*Constitutional compliance: P-003 (no subagents invoked), P-022 (residuals disclosed), P-002 (report persisted), P-011 (all findings cite specific evidence)*
