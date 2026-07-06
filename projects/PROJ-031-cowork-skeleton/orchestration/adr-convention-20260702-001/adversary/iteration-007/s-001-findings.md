# Red Team Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Post-Subtraction-Pass, Iteration 7

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, independent — iteration 7)
**H-16 Compliance:** S-003 embedded throughout the deliverable — every Option A–F in the ADR's "Options Considered" section leads with a steelman case per H-16 (ADR:67, "ST-001"/"ST-002" tags); no standalone S-003 artifact was read by this reviewer (blind protocol forbids reading sibling adversary output), so compliance is confirmed from the deliverable's own self-disclosed evidence, not from an external S-003 report.
**Threat Actor:** A contributor (careless or deliberate) who wants to mint an ADR identifier that collides with, or silently shadows, an existing canonical ID — motivated either to bypass the SHOULD-tier convention with minimal friction, or to demonstrate that the "5-rule core" retained after the subtraction pass still closes the collision/shadowing gap the whole convention exists to prevent. Full source access, no special privileges required (a normal PR).

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence, analysis, countermeasures |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion record |

---

## Summary

Post-subtraction, the package's collision-defense claim rests entirely on one mechanism: L-3 ("No duplicate ID"), which the rule draft labels **"Repo-wide"** twice (rule-draft:175,177) and which the ADR body treats as validated corpus-wide (ADR:389). This review finds that claim is **false as written**: the actual implementing script (the "exactly what L-3 runs in CI" pre-flight command, rule-draft:183-192) hard-codes its scan roots to `find projects docs/design -path '*/decisions/*'` — a narrow allowlist that structurally never reaches the **repository-based topology's own canonical ADR home** (`{RepositoryRoot}/decisions/`, ADR:376, listed "Active", not draft/transient), and never reaches the **permitted, "Active" entity-embedded dialect location** (ADR:378) except for the one already-disclosed historical instance. Where the document DOES disclose a topology-scoping gap, it does so only for L-4 (ADR:383) — never for L-1 or L-3, the two rules that actually determine whether a colliding or malformed ID is caught. A second, independent defect (RT-003) shows the "grandfather regression test" gating figure itself drifted out of sync between the two deliverables after the iteration-6 fix. This is a document that has already closed 10/10 prior Criticals through disciplined disclosure (subtraction-pass-notes.md) — these findings are new gaps in that same disclosure discipline, not a case for reopening deleted machinery. **Recommendation: REVISE (targeted).** Corrections are textual/scope-disclosure fixes (or a scan-path parameterization), not a reason to rebuild lint machinery.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-20260706I7 | "Repo-wide" L-3 duplicate-ID claim is contradicted by its own hard-coded `find projects docs/design` scan roots; the "Active" repository-based-topology canonical home (`{RepositoryRoot}/decisions/`) is structurally unscanned, and — unlike L-4 — this gap is undisclosed | Boundary | High | Critical | P0 | Missing (undisclosed) | Completeness |
| RT-002-20260706I7 | R-10 frames the entity-embedded out-of-scan gap as one bounded legacy file (Probability: LOW) even though "Entity-embedded" is a *permitted, Active* canonical location (ADR:378) that any future contributor can populate with a duplicate/shadow ID with zero L-1/L-3/L-4 coverage | Boundary | Medium | Major | P1 | Partial (narrowly disclosed) | Completeness |
| RT-003-20260706I7 | The ADR's own Migration-Plan M-6 gating row still asserts "16 dialect + 3 canonical = **19** files pass L-1" (ADR:517), contradicting the rule draft's corrected "**18** reachable" figure (rule-draft:94,179) that iteration-6 explicitly narrowed to exclude the out-of-scan `ADR-STORY015-001` — an unrepaired remediation left in the ADR body | Ambiguity | Low | Major | P1 | Missing | Internal Consistency |
| RT-004-20260706I7 | No disclosed residual addresses case-insensitive-but-case-preserving filesystem (macOS/Windows) checkout collisions for *canonical* domain-slug filenames (e.g., `ADR-Agent-Design-001.md` vs `ADR-agent-design-001.md`) — distinct, git-trackable identities that silently collide on contributor checkouts before CI/L-1 ever sees them | Dependency | Low | Minor | P2 | Missing | Completeness |

**Finding ID Format:** `RT-{NNN}-{execution_id}` where `execution_id = 20260706I7` (iteration 7, 2026-07-06), preventing collision with other blind reviewers' concurrent output.

---

## Finding Details

### RT-001: "Repo-wide" Collision Detection Is Actually Scoped to Two Directories — the Endorsed Repository-Based Topology Is Unscanned and Undisclosed [CRITICAL]

**Attack Vector:** A contributor operating a downstream Jerry CoWork/plugin adoption under the **repository-based topology** — explicitly named as PROJ-031's own stated audience (ADR:383, "downstream plugin adopters (PROJ-031's stated audience) may run the repository-based topology") — places two ADRs sharing the same canonical `ADR-{domain-slug}-NNN` identity under that topology's own documented canonical home, `{RepositoryRoot}/decisions/` (ADR:376, table row state = "Active", not draft/transient). Because `{RepositoryRoot}/decisions/` sits at the repo root with no `projects/` or `docs/design/` ancestor by definition of that topology (ADR:383, "there is no `projects/PROJ-NNN-*/` prefix"), it can never be discovered by the actual L-3 implementation.

**Category:** Boundary violation (the scan-path boundary silently excludes a location the document itself certifies as canonical/Active).

**Exploitability:** High — no special access needed; simply author two ADRs with the same domain-slug+NNN in a repository-based-topology repo's `decisions/` folder. Zero lint signal, zero CI failure, because the scan never reaches that root.

**Severity:** Critical — this defeats the single mechanism (L-3) the entire post-subtraction package relies on to prevent the exact collision class the ADR was written to eliminate (the founding `ADR-EPIC002-001` collision, ADR:113), for an entire endorsed deployment topology, while the document's own language ("Repo-wide") asserts unconditional coverage.

**Existing Defense:** Missing, and — critically — undisclosed as missing. Compare with L-4: the ADR explicitly discloses that "the L-4 dialect↔location lint's `projects/PROJ-{NNN}-*/` path assumption is inapplicable (a repository-based repo has no such directory, so L-4 is scoped to project-based repos only" (ADR:383). No equivalent disclosure exists anywhere in either deliverable for L-1 or L-3, even though both carry the identical hard-coded scan-root defect. Grep evidence: rule-draft:175 ("**Repo-wide**"), rule-draft:177 ("**Repo-wide**"), rule-draft:173 (L-1's stated scope: "`projects/*/decisions/`, `docs/design/`." — no topology caveat), and the ADR's own "Testing / verification approach" section explicitly treats the rule draft's "Repo-wide" framing as an accepted premise to reconcile against (ADR:389: "reconciling this line with the rule draft's 'all non-frozen… Repo-wide' scope").

**Evidence:**
- rule-draft:175 — `| **L-3 No duplicate ID** | Extract {slug}-NNN (canonical and uppercase-dialect) of all non-frozen ADRs; sort | uniq -d must be empty. Repo-wide. |`
- rule-draft:183-192 — the pre-flight command, explicitly labeled "exactly what L-3 runs in CI": `find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' ...`
- ADR:376 — Canonical Location Model table row: `Repository-based project (ONE-OF alternative topology) — FM-102, iter-3 | {RepositoryRoot}/decisions/ (repo-root, no projects/ prefix) | ADR-{domain-slug}-NNN | Active`
- ADR:383 — discloses only L-4's inapplicability to this topology; no parallel statement for L-1/L-3.

**Dimension:** Completeness (a stated coverage guarantee — "Repo-wide" — that the implementation does not deliver for an in-scope, endorsed deployment mode); secondarily Internal Consistency (the claim directly contradicts the document's own topology model).

**Countermeasure:** Either (a) correct the "Repo-wide" claim at rule-draft:175,177 and ADR:389 to state the actual scope precisely (e.g., "covers `projects/*/decisions/` + `docs/design/`; the repository-based topology's `{RepositoryRoot}/decisions/` is NOT reached — disclosed residual, parallel to the existing L-4 disclosure at ADR:383"), or (b) parameterize the M-6 lint's scan roots so a repository-based deployment can point L-1/L-3 at its own `decisions/` directory before claiming "Repo-wide" coverage. Given the subtraction doctrine (delete/disclose, don't add machinery), option (a) is the lower-risk fix; it costs one sentence per file and closes the overclaim without rebuilding anything.

**Acceptance Criteria:** Either the "Repo-wide" language is removed/qualified in both files with an explicit repository-based-topology residual disclosure cross-referencing R-9/R-10's disclosure pattern, OR the M-6 lint script's scan-root list is demonstrated (in the eventual implementation) to include the repository-based topology's canonical home and the "Repo-wide" claim is then true.

---

### RT-002: R-10's "Bounded Legacy File" Framing Undersells an Ongoing, Permitted Attack Surface [MAJOR]

**Attack Vector:** The Canonical Location Model table lists "Entity-embedded (permitted)" ADRs (`projects/.../work/.../{ENTITY}/`) as an **"Active (dialect)"** location — a currently-sanctioned place to put a real ADR, not a frozen historical artifact (ADR:378). R-10 (ADR:457) discloses that this location is outside L-1/L-3/L-4's scan path, but frames the entire risk around the one existing instance, `ADR-STORY015-001`, and rates Probability as "LOW" with no stated rationale for why *future* entity-embedded ADRs (which the location model continues to permit going forward) would not recur at the same rate, or be deliberately used to mint a duplicate of an existing canonical `docs/design/` ID with zero lint visibility.

**Category:** Boundary violation.

**Exploitability:** Medium — requires a contributor to place a new ADR inside an entity work-folder (a location the document itself endorses as valid), rather than in `decisions/`; plausible simply by following the STORY015 precedent rather than by any special sophistication.

**Severity:** Major — it does not invalidate the scheme (entity-embedded is a narrow, low-traffic location), but it is a live, structurally-uncovered gap in an actively-permitted location, understated by the existing residual's own severity language.

**Existing Defense:** Partial — the gap is disclosed for the one known instance, but the disclosure's probability/impact framing ("LOW/LOW") reads as though the risk is closed by grandfathering, when in fact any *new* entity-embedded ADR — including one intentionally colliding with a canonical `docs/design/` ID — inherits the identical, permanent exposure.

**Evidence:**
- ADR:378 — Canonical Location Model: `Entity-embedded (permitted) — closed prefix set only | projects/.../work/.../{ENTITY}/ | ADR-{PROJ|EPIC|FEAT|STORY}NNN-NNN | Active (dialect)`
- ADR:457 — R-10 row: `Entity-embedded ADR out-of-scan (FM-002, iter-6) — ADR-STORY015-001 lives in work/.../STORY-015.../ (no decisions/ segment), outside L-1/L-3/L-4's stated scan path | LOW | LOW | [DISCLOSED; grandfathered, out-of-scan].`
- rule-draft:179 — grandfather test text scopes coverage to "the 18 files reachable by the scan path," explicitly excluding entity-embedded ADRs by construction, not just for STORY015 specifically.

**Dimension:** Completeness.

**Countermeasure:** Reword R-10 (and its rule-draft mirror) to state explicitly that the gap is *open-ended*, not a single legacy instance: "Any entity-embedded ADR, present or future, is unreached by L-1/L-3/L-4 by construction; this is a standing, permitted-location residual, not a closed historical exception." No new lint required — this is a disclosure-fidelity fix consistent with the subtraction doctrine.

**Acceptance Criteria:** R-10's text (both files) is revised to describe the gap as applying to the *location class*, not the single known file, with Probability re-assessed against "any future entity-embedded ADR" rather than "recurrence of exactly this historical case."

---

### RT-003: Grandfather-Test Gating Count Regressed After Its Own Iteration-6 Fix (18 vs 19) [MAJOR]

**Attack Vector:** No adversary action required — this is a self-inflicted internal-consistency defect, but it matters for the abuse scenario because it shows the disclosure-repair process itself has a gap: iteration-6 explicitly narrowed the grandfather-test count from 19 to 18 to correctly exclude the out-of-scan `ADR-STORY015-001` (subtraction-pass-notes.md:166, "FM-002-iter6 ... Grandfather test narrowed 19→18 reachable, STORY015 disclosed out-of-scan R-10"), and the rule draft reflects this correctly (rule-draft:94, "the **18 files reachable** by the `projects/*/decisions/` + `docs/design/` scan path pass the grandfather regression test; the entity-embedded `ADR-STORY015-001` is out-of-scan (R-10)"; rule-draft:179, same "18 files reachable" figure). **The ADR body was never updated to match:** its Migration-Plan M-6 row still reads "with the grandfather regression test green (**16 dialect + 3 canonical = 19 files** pass L-1)" (ADR:517) — arithmetic that only totals 19 by implicitly counting STORY015 as one of the 16 "dialect" files subject to the test, directly contradicting R-10's own disclosure two sections earlier in the same document (ADR:457) that STORY015 is structurally unreachable by L-1's scan.

**Category:** Ambiguity (internally contradictory coverage claim within the same deliverable).

**Exploitability:** Low as an "attack," but high as a source of implementer confusion: whoever eventually builds M-6 could read the ADR's own gating criterion literally and either (a) believe the test is satisfied by 19 passing files when only 18 are reachable, silently masking that the 19th was never actually tested, or (b) attempt to widen the scan glob specifically to make STORY015 reachable "to satisfy the 19-count," inadvertently reopening exactly the scope-widening the subtraction doctrine declined to do (rule-draft:179, "Extending the scan glob is a future MAY, not promised").

**Severity:** Major — a stale, uncorrected gating number in a not-yet-built milestone does not currently cause harm, but it directly misstates test coverage for the core lint rule this whole review is stress-testing, and it demonstrates that the iteration-6 remediation pass (which explicitly targeted this exact class of "overclaim not verified against the retained/deleted mechanism," subtraction-pass-notes.md:153) was itself incompletely propagated across the two-file deliverable set.

**Existing Defense:** Missing — no note anywhere flags the ADR-vs-rule-draft count mismatch; subtraction-pass-notes.md's own "Verification (post-edit)" claim (line 147, "grep over the ADR body ... returns zero live references to any deleted rule or to the waiver/CODEOWNERS/two-tier machinery") does not cover numeric gating-criterion consistency, only deleted-machinery references.

**Evidence:**
- ADR:517 — `M-6 | Implement + wire the 5-rule L5 CI lint ... into CI, with the grandfather regression test green (16 dialect + 3 canonical = 19 files pass L-1) plus one named red-then-green fixture per rule.`
- rule-draft:94 — `Of the 16-file dialect corpus + 3 canonical ADRs, the 18 reachable by the projects/*/decisions/ + docs/design/ scan path pass the grandfather regression test; the entity-embedded ADR-STORY015-001 is out-of-scan (R-10).`
- rule-draft:179 — same "18 files reachable" figure, restated at the lint-spec section.
- ADR:457 (R-10) — explicitly discloses STORY015 as "outside L-1/L-3/L-4's stated scan path."
- subtraction-pass-notes.md:166 — the FM-002-iter6 disposition record confirming the intended fix was "19→18," which landed in the rule draft but not the ADR body.

**Dimension:** Internal Consistency.

**Countermeasure:** Correct ADR:517's parenthetical from "(16 dialect + 3 canonical = 19 files pass L-1)" to "(15 dialect files reachable in `decisions/` dirs + 3 canonical = 18 files pass L-1; the entity-embedded `ADR-STORY015-001` remains grandfathered out-of-scan per R-10)" — a one-line text edit, no machinery change, consistent with the subtraction doctrine and with the rule draft's already-correct figure.

**Acceptance Criteria:** ADR:517's file count matches rule-draft:94/179 exactly (18, not 19), and the parenthetical explicitly names the STORY015 exclusion rather than silently implying full coverage.

---

### RT-004: Canonical Slug Case-Fold Collision on Case-Insensitive Filesystems Is Undisclosed [MINOR]

**Attack Vector:** R-9 discloses a case-fold shadowing risk narrowly scoped to the *dialect* prefix (`ADR-proj031-001` shadowing `ADR-PROJ031-001`, ADR:456). No equivalent disclosure covers the *canonical* domain-slug form: two git-distinct, both-lowercase-vs-mixed-case filenames such as `ADR-agent-design-001-x.md` and `ADR-Agent-Design-001-y.md` are different tracked blobs on a case-sensitive filesystem (and `ADR-Agent-Design-001-y.md` would correctly fail L-1's `^[a-z]` canonical-grammar check and also fail dialect grammar, so CI running on a case-sensitive runner would flag it as malformed) — but on a contributor's case-insensitive-but-case-preserving local filesystem (macOS APFS default, Windows NTFS default), a checkout containing both files can silently collide (one overwrites the other, or the checkout errors) *before* the malformed file ever reaches CI for L-1 to reject it.

**Category:** Dependency (host filesystem behavior, not something the convention itself controls).

**Exploitability:** Low — requires a specific host OS/filesystem configuration and two commits/branches adding case-variant filenames; a largely accidental rather than deliberate vector, and CI (presumably Linux) would still correctly reject the malformed variant once it reaches CI.

**Severity:** Minor — narrow blast radius, mitigated by the fact that CI itself is unaffected; the residual is purely a local-development-experience gap.

**Existing Defense:** Missing (undisclosed), though the adjacent R-9 disclosure demonstrates the document is aware of case-fold issues in general.

**Evidence:**
- ADR:456 (R-9) — scoped explicitly to "a lowercase slug that case-folds to a dialect prefix," not to canonical-vs-canonical case variants.
- ID Scheme canonical regex, rule-draft:70 (`^ADR-[a-z][a-z0-9]*...`) — confirms mixed-case canonical filenames are rejected by L-1's grammar check, but only once the file is actually linted (i.e., in CI), not at local-checkout time.

**Dimension:** Completeness.

**Countermeasure:** Add a one-line disclosed residual parallel to R-9 noting this is a general git/filesystem limitation outside the convention's control, not a scheme defect, so it is not silently absent from the residual register the document otherwise maintains meticulously.

**Acceptance Criteria:** A residual note (R-9 extension or new R-12) documents the case-insensitive-filesystem checkout risk for canonical (not just dialect) filenames, with no new lint machinery implied.

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **RT-001:** Correct or close the "Repo-wide" overclaim for L-3 (and L-7, which carries the identical unqualified label at rule-draft:177 and should be checked for the same topology gap) — either via disclosure parity with the existing L-4 caveat, or via scan-root parameterization. Acceptance: no remaining unqualified "Repo-wide" claim that a repository-based-topology reader would reasonably rely on as true.

**P1 (Important — SHOULD mitigate):**
- **RT-002:** Reframe R-10 to describe the entity-embedded scan gap as an open-ended, location-class residual rather than a single bounded legacy instance.
- **RT-003:** Fix ADR:517's stale "19 files" gating figure to match the rule draft's corrected "18 files," and name the STORY015 exclusion explicitly in the same sentence.

**P2 (Monitor — MAY mitigate):**
- **RT-004:** Add a disclosed residual for canonical-slug case-fold checkout collisions on case-insensitive filesystems (informational only; no lint implied).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-001/RT-002/RT-004: the stated collision-detection coverage ("Repo-wide") is materially incomplete for an endorsed topology and an actively-permitted location, and a filesystem-level residual class goes unmentioned |
| Internal Consistency | 0.20 | Negative | RT-003: the ADR's own Migration-Plan gating figure (19) contradicts both the rule draft's corrected figure (18) and the ADR's own R-10 disclosure two sections earlier |
| Methodological Rigor | 0.20 | Neutral | The 5-step S-001 protocol was fully executable against this deliverable; the document's own iteration discipline (10/10 prior Criticals dispositioned) is methodologically strong |
| Evidence Quality | 0.15 | Neutral | Every RT-NNN finding here is grounded in exact file:line citations from both deliverables and the subtraction-pass-notes disposition record |
| Actionability | 0.15 | Neutral | All four countermeasures are text-only corrections consistent with the subtraction doctrine; none requires restoring deleted machinery |
| Traceability | 0.10 | Negative | RT-003 specifically demonstrates a traceability break between the two companion deliverables' own cross-referenced figures |

**Overall assessment:** The post-subtraction package is disciplined and largely self-consistent, but its single load-bearing collision-detection claim ("Repo-wide" L-3) does not hold for the repository-based topology it explicitly endorses, and one prior remediation (18-file grandfather count) did not fully propagate across both deliverable files. Targeted disclosure/text fixes, not new machinery, close all four findings.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 1 (RT-001)
- **Major:** 2 (RT-002, RT-003)
- **Minor:** 1 (RT-004)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor defined; Attack Vectors enumerated across Boundary/Ambiguity/Dependency categories — Circumvention and Degradation categories were explored but yielded no new findings beyond those already dispositioned in prior iterations, e.g., R-6/R-7/R-9/R-11; Defense Gaps assessed; Countermeasures developed for all P0/P1; Impact synthesized and H-15 self-reviewed before persistence)
