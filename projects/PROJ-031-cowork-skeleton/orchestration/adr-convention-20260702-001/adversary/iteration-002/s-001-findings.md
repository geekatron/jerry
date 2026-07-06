# Red Team Report: ADR-PROJ031-004 / adr-standards-rule-draft.md (iteration 2)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata and threat actor |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence per Critical/Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |
| [Blind-Protocol and Scope Notes](#blind-protocol-and-scope-notes) | What was and was not read |

---

## Header

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95, above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration 2, S-001 assignment)
**H-16 Compliance:** Not independently verifiable under the blind protocol — this session was instructed not to read any file under `.../adversary/` except its own output file, which precludes reading an S-003 Steelman output artifact even if one exists from a prior tournament group. Per the user's documented tournament design (6-group order: self-refine -> steelman -> challenge -> verify -> decompose -> score, S-001 is in the "challenge" group), S-003 is assumed to have already executed in an earlier group. **This is an inference, not a verified fact (P-022 label).** If S-003 did not in fact run before this S-001 execution, this report is itself an H-16 violation and MUST be re-run after S-003 evidence is available to the orchestrator.
**Threat Actor:** A contributor to the Jerry monorepo — ranging from *careless* (an agent or human authoring an ADR quickly, unaware of the new convention's fine print) to *hostile* (a bad-faith actor deliberately trying to mint a colliding/misleading ADR identity, orphan a superseded decision, or bypass the CI lint) — with full read/write access to the repo, no special privileges, and knowledge that the convention is enforced only by a not-yet-built CI lint (`scripts/lint_adr_convention.py`, confirmed absent — see RT-001). Motivation: ship a decision quickly, avoid taxonomy governance overhead, or deliberately shadow/orphan an inconvenient prior decision.

---

## Summary

The two deliverables (ADR + companion MEDIUM-tier rule draft) present a well-reasoned, honestly-caveated identity/promotion scheme (Scheme B, subject-encoded IDs) with an unusually thorough self-critique culture (the ADR already documents and remediates 5 findings from adversarial iteration 1). However, Red Team analysis emulating a careless-to-hostile contributor finds that **the entire deterministic enforcement layer this convention depends on does not exist in the repository today** (verified: no `scripts/lint_adr_convention.py`, no `adr-lint-waivers.yaml`, no `adr-grandfather-allowlist.txt`), and even on paper the lint specification contains multiple concrete, exploitable gaps: an unenforced "freeze" of legacy directories (new bare IDs can still be added there because those directories are *exempted* from the anti-collision checks, not *blocked* from new entries), a case-sensitivity loophole that lets a lowercase project-ID-shaped domain slug evade the one location-integrity check that exists, a self-approvable waiver mechanism, a one-directional tombstone check that permits silent orphaning of superseded ADRs, an unauthorized-promotion path with no approval gate, and an internal inconsistency (an undefined `FEAT` dialect prefix accepted by the lint regex but never defined in policy) plus a likely false-positive in the one location check that does exist (STORY015 filename vs. STORY-015 folder hyphenation). 4 Critical and 6 Major findings identified across all 5 attack-vector categories (11 total, exceeding the template's 4-vector minimum). **Recommendation: REVISE.** The convention's *design* is sound and low-regret by its own admission, but its *enforcement claims* are materially overstated relative to what is actually built and what the lint spec, as written, would actually catch. Ratification (P-020) should not proceed on the belief that M-6 makes this "gated" until the gate is a real, tested CI check — today it is a paragraph of intent.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260702iter2 | L5 lint (`scripts/lint_adr_convention.py`), waiver ledger, and allowlist do not exist in the repo; "ratification blocker" (M-6) has no technical gate against premature P-020 ratification | Dependency | High | Critical | P0 | Missing | Methodological Rigor |
| RT-002-20260702iter2 | Frozen-dir "freeze" is implemented as an *exemption* from L-1/L-2/L-3, not a block on new entries — new bare `ADR-NNN` files can still be added to `docs/adrs/`/`docs/archive/` and pass CI | Boundary / Circumvention | High | Critical | P0 | Missing | Completeness |
| RT-003-20260702iter2 | Case-split grammar (L-1a lowercase vs. L-1b uppercase) permits a lowercase project-ID-shaped domain slug (e.g. `ADR-proj031-005-x.md`) that passes as "canonical," evades the L-4 dialect-location check entirely, and evades case-sensitive citation/grep tooling | Ambiguity / Boundary | Medium | Critical | P0 | Missing | Internal Consistency |
| RT-004-20260702iter2 | Waiver-ledger self-approval bypass: only check is `approved_by != author` (string mismatch); no verification the named approver is a real, authorized second reviewer | Circumvention | Medium | Critical | P0 | Partial (structural fields, no identity check) | Methodological Rigor |
| RT-005-20260702iter2 | One-directional tombstone check (L-7, WARN) validates forward links resolve but never validates that a promoted ADR's origin was reciprocally marked `SUPERSEDED` -- silent orphaning on a half-completed Path-2 promotion | Dependency / Degradation | Medium | Major | P1 | Partial (WARN only, one-directional) | Traceability |
| RT-006-20260702iter2 | Semantic/near-duplicate slug collisions (`agent-design` vs `agent-definition`) are the ADR's own top disclosed residual risk (R-3/FM-4), yet the only mitigation (M-5b fuzzy match) is explicitly non-gating ("soft process") and not part of any FAIL lint rule | Ambiguity / Degradation | Medium | Major | P1 | Partial (advisory only) | Completeness |
| RT-007-20260702iter2 | Path 1 promotion ("pure git mv") has no approval gate distinct from ordinary code review; L-5 is WARN-only and checks the wrong direction, permitting unauthorized promotion of a PROPOSED/REJECTED project ADR to shadow framework doctrine | Boundary / Circumvention | Medium | Major | P1 | Missing | Internal Consistency |
| RT-008-20260702iter2 | L-4 entity-dialect location check likely false-positives against the live grandfathered `ADR-STORY015-001` file: filename token `STORY015` is not a literal substring of its folder `STORY-015-tier-model-renumbering` | Boundary | Medium | Major | P1 | Missing (spec ambiguity) | Internal Consistency |
| RT-009-20260702iter2 | L-1b regex silently accepts an undefined `ADR-FEAT###-###` dialect (never introduced in ADR-M-003 or the parent ADR's D-3 narrative) — an unauthorized-but-lint-legal ID family | Circumvention / Ambiguity | Low | Major | P1 | Missing | Internal Consistency |
| RT-010-20260702iter2 | Self-compliance gap: the parent ADR itself has no YAML frontmatter (`id`/`scope`/`origin_project`) it prescribes -- only blockquote header metadata -- undisclosed unlike the parallel M-11 gap for the 3 framework ADRs | Ambiguity | Low | Major | P1 | Missing | Internal Consistency |
| RT-011-20260702iter2 | Canonical-ID squatting window: `ADR-adr-convention-001` is declared as this ADR's intended identity (Meta-Note) but not reserved; a same-slug file committed before M-9 executes is only caught post-hoc, and only once M-6 exists | Dependency | Low | Minor | P2 | Missing (narrow window, requires insider knowledge) | Traceability |

**Finding ID Format:** `RT-{NNN}-20260702iter2` (execution_id `20260702iter2` distinguishes this iteration-2 blind S-001 run from other tournament executions).

---

## Finding Details

### RT-001: The Enforcement Layer Does Not Exist [CRITICAL]

**Attack Vector:** A careless-to-hostile contributor exploits the fact that, as of 2026-07-02, none of the L-1 through L-8 lint rules are implemented anywhere in the repository. Every collision-safety, dialect-preservation, and waiver-audit guarantee in both deliverables is aspirational text describing a CI job that has not been written.

**Category:** Dependency
**Exploitability:** High — no action is even required to "exploit" this; it is the default state today. Any new ADR of any shape (bare, colliding, misleading) can be committed right now with zero CI friction.
**Severity:** Critical — every other finding in this report (RT-002 through RT-009) assumes the lint exists and evaluates its *specification*; RT-001 establishes that none of those specified defenses are currently active at all. This is the root vulnerability underlying all the others.
**Existing Defense:** Missing. Verified via direct filesystem search: `Glob("scripts/lint_adr_convention.py")` -> no files found; `Glob("scripts/adr-lint-waivers.yaml")` -> no files found; `Glob("scripts/adr-grandfather-allowlist.txt")` -> no files found (searches run 2026-07-02 against this exact checkout).
**Evidence:** Migration Plan itself lists M-6 as "TBD-Task + GH Issue (H-32)" and "Yes — ratification blocker" (`ADR-PROJ031-004-adr-identifier-convention.md:431`), i.e. the plan concedes the lint is not yet built. R-5 in the Risks table explicitly names this exact failure mode ("Lint never gets built; convention stays advisory-only", probability MED, impact HIGH) and its stated mitigation is a *process* claim — "M-6 is now a ratification blocker requiring independently-verified completion... not an optional follow-up" (`ADR-PROJ031-004-adr-identifier-convention.md:383`) — not a technical one. The Status Vocabulary's transition table shows `PROPOSED -> ACCEPTED` triggers on "Ratified (P-020)" alone (`ADR-PROJ031-004-adr-identifier-convention.md:509`); nothing in either deliverable describes an automated check that would block a human from setting `status: ACCEPTED` while `scripts/lint_adr_convention.py` is absent from the repo. "Ratification blocker" is therefore a documentation instruction to whoever ratifies, not a system property.
**Dimension:** Methodological Rigor (a convention whose central enforcement claim is unbuilt cannot be assessed as methodologically complete)
**Countermeasure:** Before this ADR's status can move past `PROPOSED`, require a machine-checkable precondition: a CI job (or even a simple pre-ratification checklist script) that verifies `scripts/lint_adr_convention.py` exists, is wired into `.github/workflows/`, and the mandatory 16-file grandfather regression test (already specified in the rule draft, line 203) passes green — and treat the *absence* of that verification as an automatic block on the ratification PR, not a documentation reminder.
**Acceptance Criteria:** `scripts/lint_adr_convention.py` exists in the repo, is invoked by a `.github/workflows/*.yml` job, the regression test asserting all 16 live dialect/canonical files pass is present and green in CI, and a CI check (not just a Markdown note) prevents `status: ACCEPTED` from merging on this ADR until the above is true.

---

### RT-002: Frozen Directories Are Exempted, Not Blocked [CRITICAL]

**Attack Vector:** A contributor adds a brand-new file such as `docs/adrs/ADR-007-sneaky-decision.md` (bare `ADR-NNN`, the exact collision-prone Scheme-E pattern the whole convention exists to deprecate) directly into the "frozen" `docs/adrs/` directory, or a similar new file into `docs/archive/`. Both deliverables describe these directories as **frozen** in prose ("Freeze. Add `docs/adrs/README.md` frozen-legacy banner. Do not renumber", `ADR-PROJ031-004-adr-identifier-convention.md:414`; "Frozen (legacy): `docs/adrs/ADR-NNN`... Do not extend", `adr-standards-rule-draft.md:67,86`) — but the *lint rules that would enforce "do not extend"* explicitly carve these directories out of scope rather than adding a rule against new entries.

**Category:** Boundary violation / Rule circumvention
**Exploitability:** High — requires no special knowledge, just adding a file to a path that is currently home to 7 existing files (verified: `docs/adrs/ADR-001-agent-architecture.md`, `ADR-001-amendment-001-python-preprocessing.md`, `ADR-002-artifact-structure.md`, `ADR-003-bidirectional-linking.md`, `ADR-004-file-splitting.md`, `ADR-005-agent-implementation.md`, `ADR-006-mindmap-pipeline-integration.md` — all confirmed present via Glob 2026-07-02).
**Severity:** Critical — this directly recreates the exact bare-`ADR-NNN` collision problem (three prior live collisions cited by the ADR itself, `ADR-PROJ031-004-adr-identifier-convention.md:82`) that the entire convention exists to close, and it does so *inside the one place the convention claims is safe from that failure mode*.
**Existing Defense:** Missing/backwards. Both L-1 (canonical/dialect form) and L-2 (no new bare) rules are defined with the frozen directories as an **allowlist exemption**: "**Frozen-dir allowlist** (L-1/L-2/L-3 exempt): `docs/adrs/`, `docs/archive/`" (`adr-standards-rule-draft.md:201`; identically restated `ADR-PROJ031-004-adr-identifier-convention.md:542`). L-2 itself is scoped as "everywhere except frozen dirs" (`adr-standards-rule-draft.md:191`). An exemption from a check is the absence of a check — it is not a rule that specifically detects and blocks *new git-added files* landing inside a directory tagged frozen. Nowhere in either deliverable's lint table (L-1 through L-8) is there a rule of the shape "FAIL if a new file is added under a frozen directory."
**Evidence:** `adr-standards-rule-draft.md:191,201`; `ADR-PROJ031-004-adr-identifier-convention.md:414,534,542`; live directory listing confirming the frozen set is not empty/immutable-by-tooling (7 files, `docs/adrs/*.md`, Glob 2026-07-02).
**Dimension:** Completeness (the enforcement design has a named gap in coverage of its own stated "frozen" claim)
**Countermeasure:** Add an explicit new FAIL rule, e.g. **L-9 Frozen-dir immutability:** "A git-added (new) file under `docs/adrs/` or `docs/archive/` is rejected outright, non-waivable" — distinct from, and in addition to, the current allowlist which should continue to exempt *existing* files from L-1/L-2/L-3 re-validation but must not exempt *new* files from a dedicated no-new-entries check.
**Acceptance Criteria:** A test asserting that a synthetic new file under `docs/adrs/` (e.g., `docs/adrs/ADR-999-test.md`) is rejected by the lint with a non-waivable FAIL, while the 7 existing files continue to pass unaffected.

---

### RT-003: Case-Sensitive Grammar Split Creates a Location-Check Evasion Loophole [CRITICAL]

**Attack Vector:** A contributor deliberately (or carelessly, via a lowercase-by-default text editor habit) names a new project-local ADR `ADR-proj031-005-something-unrelated.md` — visually resembling the legitimate uppercase dialect `ADR-PROJ031-005` but written entirely in lowercase.

**Category:** Ambiguity exploitation / Boundary violation
**Exploitability:** Medium — requires the author to notice the case-sensitivity gap, but no special tooling or privilege; a single character-case choice at file-creation time is sufficient.
**Severity:** Critical — the file is misleading (visually near-identical to a legitimate scope-prefixed dialect ID, differing only in case) and it structurally evades the one lint rule (L-4) designed to catch exactly this class of misfiled/misleading dialect ADR, while still passing the canonical FAIL check (L-1a) cleanly. This is a genuine identity-confusion vector the deliverables do not consider.
**Existing Defense:** Partial-to-missing. Trace through the actual regex: L-1a (canonical) is `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` (`adr-standards-rule-draft.md:71`). The token `proj031` is composed entirely of lowercase letters and digits, so it satisfies `[a-z0-9]+` — meaning `ADR-proj031-005-something.md` parses as a syntactically valid **canonical domain-slug** ADR under L-1a with domain-slug `proj031` and sequence `005`. It does **not** match L-1b (`^ADR-(PROJ|EPIC|FEAT|STORY)\d{3}-\d{3}...`, `adr-standards-rule-draft.md:72`), which requires the literal uppercase tokens `PROJ`/`EPIC`/`FEAT`/`STORY`. Because the file is classified as "canonical" rather than "dialect," **L-4 (Dialect<->location) does not apply to it at all** — L-4's stated scope is explicitly the dialect grammar ("For `ADR-PROJ{NNN}-NNN`: `PROJ{NNN}` equals the containing `projects/PROJ-{NNN}-*/` dir", `adr-standards-rule-draft.md:193`). The file can therefore be placed in *any* `decisions/` directory, in any project, with zero location-consistency check, while visually masquerading as the well-governed `PROJ031` dialect. Additionally, because grep-based citation/discovery tooling recommended elsewhere in the ADR (`grep -r "ADR-PROJ031"`, the pre-flight collision one-liner at `ADR-PROJ031-004-adr-identifier-convention.md:328-337`) is case-sensitive by default, a search for the legitimate uppercase dialect will not surface this lowercase file and vice versa — the two identities silently coexist, invisible to each other under standard tooling.
**Evidence:** `adr-standards-rule-draft.md:71-72,190,193`; `ADR-PROJ031-004-adr-identifier-convention.md:328-337` (case-sensitive grep example).
**Dimension:** Internal Consistency (the grammar's case-based classification boundary is not accompanied by any rule preventing a domain-slug from being a case-variant of a reserved dialect prefix)
**Countermeasure:** Add a FAIL rule that rejects any domain-slug (L-1a match) whose value, case-folded, equals a reserved dialect prefix token (`proj`, `epic`, `feat`, `story`) followed immediately by digits — i.e., ban domain slugs of the shape `^(proj|epic|feat|story)\d+$` outright, forcing genuinely scope-shaped tokens through the dialect grammar (L-1b) regardless of case.
**Acceptance Criteria:** A synthetic test file `ADR-proj999-001-x.md` is rejected (or reclassified/forced through L-1b + L-4) by the lint, and the L-4 location check is demonstrated to apply to it once reclassified.

---

### RT-004: Waiver Ledger Is Self-Approvable [CRITICAL]

**Attack Vector:** A contributor who wants to bypass a waivable FAIL rule (L-1a, L-1b, or L-4) adds a single-commit entry to `scripts/adr-lint-waivers.yaml` naming a plausible but fabricated `approved_by` value that merely differs textually from the commit author's own identity string.

**Category:** Rule circumvention
**Exploitability:** Medium — requires knowing the waiver-file schema (which is fully documented in the deliverable itself, making it trivial to reproduce), but no cryptographic or organizational barrier stops a single actor from writing two different name strings into one YAML entry.
**Severity:** Critical — this defeats the deliverable's own stated design goal for the override mechanism ("machine-checkable, audited... supersedes the bare-comment design", `ADR-PROJ031-004-adr-identifier-convention.md:525-528`) for exactly the three waivable FAIL rules that matter (L-1a/L-1b/L-4); only the non-waivable L-2/L-3 remain genuinely un-bypassable.
**Existing Defense:** Partial. The specification requires six fields and states: "The lint... fails if a claimed waiver is missing any field, if `approved_by` equals the commit author, or if `expires` has passed" (`adr-standards-rule-draft.md:185`, restated `ADR-PROJ031-004-adr-identifier-convention.md:528`). The *only* identity check described is a string-inequality test (`approved_by` != commit author). There is no described cross-reference to a CODEOWNERS file, a required GitHub PR-review approval via the GitHub API, a second git-signed commit, or any other mechanism that verifies `approved_by` names an actual, distinct, authorized human who reviewed the specific waiver. Nothing prevents the same individual from committing a waiver entry naming a colleague, a bot, or a fictitious reviewer, in the same PR, with no independent action required from that named party. Additionally, "append-only ledger" is asserted (`adr-standards-rule-draft.md:185`) but no enforcement mechanism for append-only-ness (e.g., a CI diff check disallowing edits/deletions to prior lines) is specified — a prior waiver's `expires` date could be silently extended or a record silently removed with no described detection.
**Evidence:** `adr-standards-rule-draft.md:185`; `ADR-PROJ031-004-adr-identifier-convention.md:525-528`.
**Dimension:** Methodological Rigor (the override model's stated goal — "audited," "reviewed" — is not actually achieved by the described check, which is a string-inequality test, not an identity/authorization verification)
**Countermeasure:** (1) Require the waiver PR to carry an actual GitHub "Approved" review from an account distinct from the author, verified via the GitHub API/branch-protection required-reviewers setting, not a free-text YAML field. (2) Enforce true append-only-ness with a CI diff check that fails if any existing line in `scripts/adr-lint-waivers.yaml` is modified or removed (only pure line-appends permitted).
**Acceptance Criteria:** A synthetic waiver PR with no independent GitHub review approval is rejected by CI even though the YAML `approved_by` field names a different string than the author; a synthetic PR that edits an existing waiver's `expires` field is rejected by the append-only check.

---

### RT-005: One-Directional Tombstone Check Permits Silent Orphaning [MAJOR]

**Attack Vector:** A careless (not necessarily hostile) contributor performs a Path-2 promotion (dialect ADR -> canonical framework ADR) but only completes half of the required two-file edit: they author the new `docs/design/ADR-{domain-slug}-NNN-*.md` with `promoted_from` set correctly, but never go back and set the *original* project ADR's `status: SUPERSEDED` + `promoted_to`. The original file is left silently orphaned, still reading as `ACCEPTED` (or whatever its prior status was) — appearing current and authoritative to any reader or agent who lands on it first (a stale bookmark, a stale citation, a search result ranked by recency, etc.).

**Category:** Dependency / Degradation
**Exploitability:** Medium — this is the *easier*, not the harder, path: authoring the new file is the salient, visible half of the task; editing the old file's frontmatter is an easy-to-forget second step with no build/test failure if skipped.
**Severity:** Major — this is precisely the "orphan a decision" failure mode the task's adversarial question names directly, and it defeats the ADR's own headline claim that promotion "removes the recurring... class of work that BUG-006 represents" (`ADR-PROJ031-004-adr-identifier-convention.md:343`) and its explicit evidence that this exact failure has already happened once (the still-stale `ADR-PROJ007-001/002` references, `ADR-PROJ031-004-adr-identifier-convention.md:48,64,127,221,247,581`).
**Existing Defense:** Partial, WARN-only, and one-directional. L-7 "Tombstone integrity (structured)" checks: "`superseded_by`/`promoted_to` frontmatter targets resolve to an existing ADR" (`adr-standards-rule-draft.md:196`; restated `ADR-PROJ031-004-adr-identifier-convention.md:539`). This validates the forward direction only — *if* `promoted_to` is set, does the target exist — but never validates the reverse: that a new ADR carrying `promoted_from: ADR-PROJ{NNN}-NNN` implies the referenced source file *must* carry a reciprocal `status: SUPERSEDED` + `promoted_to` pointing back. Because L-7 is WARN (not FAIL) and one-directional, a half-completed promotion produces no CI signal in either direction: the new file is internally consistent (no dangling `promoted_to`, since it wasn't set on the old file at all — there is simply nothing to check), and the old file, having no `promoted_to`/`SUPERSEDED` fields touched, looks like an ordinary unpromoted ADR, not an orphan.
**Evidence:** `adr-standards-rule-draft.md:145-147,196`; `ADR-PROJ031-004-adr-identifier-convention.md:467-469,539`; the ADR's own disclosure that this exact failure class has already occurred and remains unrepaired 2.5 months later: `ADR-PROJ031-004-adr-identifier-convention.md:48` ("all three framework ADRs were born inside projects and renamed on promotion; the resulting broken citations remain unrepaired") and `:127` ("stale citations to the extinct `ADR-PROJ007-001/002` IDs still sit in PROJ-007's own `ORCHESTRATION.yaml:228,242`... as of 2026-07-02").
**Dimension:** Traceability (a broken back-link is precisely a traceability failure, and this class of failure is empirically the ADR's own motivating evidence, yet the corresponding lint check remains WARN/one-directional even in the newly-designed system meant to prevent recurrence)
**Countermeasure:** Add a FAIL-class L-7b rule: for every ADR carrying `promoted_from: X`, verify that file `X` exists and its frontmatter carries `status: SUPERSEDED` and `promoted_to` pointing back to the new file's own ID. Treat a mismatch (new file promoted-from an old file that does not reciprocally point forward) as a blocking, non-waivable defect, since — like L-2/L-3 — this is a correctness/consistency defect, not a style preference.
**Acceptance Criteria:** A synthetic test pair (new file with `promoted_from` set, old file *without* the reciprocal `SUPERSEDED`/`promoted_to`) fails CI; the same pair with the reciprocal fields correctly set passes.

---

## Recommendations

**P0 (Critical — MUST mitigate before ratification/acceptance):**
- **RT-001:** Do not treat M-6 as satisfied by intent. Require a verifiable CI artifact (lint script + wired workflow + green 16-file regression test) to exist *before* `status` may move to `ACCEPTED`; block ratification technically, not just procedurally.
- **RT-002:** Add a non-waivable "no new files under frozen dirs" rule (L-9) distinct from the current exemption, which currently only suppresses re-validation of existing files rather than blocking new ones.
- **RT-003:** Ban domain slugs shaped like case-folded dialect prefixes (`^(proj|epic|feat|story)\d+$`) so a lowercase project-ID-look-alike cannot masquerade as a canonical, unchecked identity.
- **RT-004:** Replace the self-reported `approved_by` string field with a real, API-verified second-reviewer approval (branch protection / CODEOWNERS), and add an append-only enforcement check for the waiver ledger itself.

**P1 (Important — SHOULD mitigate):**
- **RT-005:** Make tombstone integrity bidirectional and FAIL-class (a `promoted_from` link demands a reciprocal `promoted_to`/`SUPERSEDED` on the source, verified, not just WARN-checked one way).
- **RT-006:** Promote the taxonomy fuzzy-match (M-5b) from an advisory "SHOULD run" agent behavior into an actual CI check (even a simple Levenshtein-distance gate against the `docs/design/README.md` registry) so semantic collisions produce a WARN or FAIL signal, not silence.
- **RT-007:** Add an explicit promotion-authorization gate to Path 1 (e.g., require `status: ACCEPTED` on the source before a `git mv` into `docs/design/` is lint-legal; currently nothing checks the source's status before or during the move).
- **RT-008:** Clarify and test the L-4 entity-path-matching normalization rule against the live `STORY015`/`STORY-015-...` naming mismatch before treating L-4 as ready to ship as a FAIL rule.
- **RT-009:** Either formally define and govern the `FEAT` dialect (add it to ADR-M-003/D-3 narrative text, with its own L-4 location semantics) or remove it from the L-1b regex until it is.
- **RT-010:** Add real YAML frontmatter to this very ADR (or explicitly disclose the gap the way M-11 discloses it for the 3 framework ADRs) so the self-compliance claim in the Meta-Note is not silently false today.

**P2 (Monitor — MAY mitigate):**
- **RT-011:** Consider a lightweight "reserved canonical ID" note or placeholder stub for `ADR-adr-convention-001` to close the narrow squatting window before M-9 executes; low priority given the narrow exploit window and insider-knowledge requirement.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002 (frozen-dir new-entry gap) and RT-006 (unenforced semantic-collision mitigation) leave named, self-disclosed risks (R-3/FM-4, R-5) without an actual corresponding control |
| Internal Consistency | 0.20 | Negative | RT-003 (case-split evasion), RT-008 (STORY015 hyphen mismatch), RT-009 (undefined FEAT prefix), and RT-010 (this ADR's own missing frontmatter) are all self-contradictions between the deliverables' stated grammar/claims and their actual, verifiable state |
| Methodological Rigor | 0.20 | Negative | RT-001 (enforcement layer entirely unbuilt) and RT-004 (waiver self-approval) mean the "deterministic, audited" enforcement claim central to the MEDIUM-tier justification (c-002) is not yet true in practice |
| Evidence Quality | 0.15 | Neutral-to-Positive | The deliverables are unusually well-evidenced (filesystem-verified counts, git commit citations, explicit P-022 disclosures); this Red Team pass independently confirmed several factual claims (the dangling `ci.yml:2` citation, the missing framework-ADR frontmatter, the STORY015 file's existence and exact path) |
| Actionability | 0.15 | Neutral | Countermeasures above are concrete and independently testable; the deliverables' own existing recommendations (M-1 through M-11) are similarly specific, so this dimension is not materially harmed by these findings |
| Traceability | 0.10 | Negative | RT-005 (one-directional tombstone check) directly undermines the one property (citation/back-link integrity) the entire convention exists to guarantee |

**Overall assessment:** Targeted remediation required before ratification. The convention's *design rationale* (Scheme B, subject-encoded identity, MEDIUM-tier, sensitivity-analyzed) is not undermined by these findings — but its *enforcement claims* are materially ahead of its *enforcement reality*, and several concrete, low-effort-to-fix loopholes (RT-002, RT-003, RT-008, RT-009) would allow a careless or hostile contributor to defeat the standard's stated guarantees today, in ways the current draft does not anticipate.

---

## Blind-Protocol and Scope Notes

- Per the tournament's blind protocol, this session did **not** read any file under `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/` other than its own output file (this one), and did not read any other reviewer's findings from any iteration.
- This session **did** read, as permitted evidence: the two deliverables under review in full; the S-001 strategy template (`.context/templates/adversarial/s-001-red-team.md`); and, for verification only, live repository state via `Glob`/`Read` (existence checks for `scripts/lint_adr_convention.py`, `scripts/adr-lint-waivers.yaml`, `scripts/adr-grandfather-allowlist.txt`; `.github/workflows/ci.yml` line 1-5; `docs/design/*.md`; `docs/adrs/*.md`; `projects/*/decisions/*.md`; the `ADR-STORY015-001` file path) — no files under the `explore/` directory were required beyond what is already cited inline by the deliverables themselves, since the deliverables' own citations were independently checked directly against the live filesystem rather than trusted at face value, per P-011/P-022.
- No file was edited. This report is observation-only, consistent with the adversary mandate (owner edits, adversaries report).
