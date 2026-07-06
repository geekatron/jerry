# Red Team Report: ADR-PROJ031-004 / adr-standards-rule-draft.md (ADR Identifier, Location & Promotion Convention)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#red-team-report-adr-proj031-004--adr-standards-rule-draftmd-adr-identifier-location--promotion-convention) | Strategy metadata, threat actor |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence and analysis per Critical/Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-001), blind reviewer, iteration 1
**H-16 Compliance:** NOT independently verifiable this iteration. The blind-review protocol forbids reading any file under `.../adversary/` other than this report, which includes any S-003 (Steelman) output. Per user-memory operational convention ("blind agents ... honor the 6-group order: self-refine -> steelman -> challenge -> verify -> decompose -> score"), S-003 is assumed to have run in a prior sequential group before this "challenge" group. **This is a process assumption, not a verified fact** (P-022 disclosure) — the orchestrator, not this reviewer, owns H-16 sequencing verification.
**Threat Actor:** A careless-or-hostile Jerry contributor who wants to (a) avoid ADR-naming friction with minimum effort, (b) intentionally mint a colliding or misleading ADR ID, or (c) exploit the promotion process to orphan or shadow an existing decision. Capability: ordinary (non-admin) contributor with full repo read access, a text editor, and `git` — no special tooling, no insider access beyond what any of the repo's documented 66 concurrent branches (`advocate-external.md:126`, cited at `ADR-PROJ031-004.md:93`) already implies. Motivation: minimize governance overhead, or deliberately confuse provenance/authority of a decision.

---

## Summary

The convention is well-reasoned on paper but its enforcement is **not actually operative**: the L5 CI lint it describes in exhaustive FAIL/WARN detail does not exist anywhere in the repository, is not wired into any of the 6 GitHub Actions workflows, and every FAIL-class rule it does specify carries an unaudited, ungated override annotation — meaning even a future, fully-built lint would not close the door on deliberate collision or misdirection. Live repo evidence (verified this session, not inferred) shows the exact citation-breakage failure this ADR exists to prevent is *already occurring today*, undetected by the proposed lint's scan scope, and the "arbiter" role the standard depends on to prevent domain-slug shadowing is explicitly unresolved (`TBR-2`) at ratification time. **8 attack vectors identified across all 5 categories (3 Critical, 4 Major, 1 Minor). Recommendation: REVISE before ratification** — specifically, treat lint existence + CI wiring as a hard precondition for any status beyond `PROPOSED`, and redesign the override/waiver mechanism before relying on any FAIL rule for collision safety.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260702-i1 | L5 lint (`scripts/lint_adr_convention.py`) does not exist; not wired into any CI workflow; standard is fully unenforced today, not merely "advisory" | Degradation | High | Critical | P0 | Missing | Methodological Rigor |
| RT-002-20260702-i1 | Every FAIL-class lint rule (L-1..L-4) carries an ungated, unaudited `adr-lint: ignore` / waiver-file override | Rule Circumvention | High | Critical | P0 | Missing (override negates the rule) | Internal Consistency |
| RT-003-20260702-i1 | Live dangling `ADR-CI-001` citation in `.github/workflows/ci.yml:2` (verified, not fixed by this standard's design) proves L-7 cannot catch free-text citation breakage | Dependency | High | Critical | P0 | Missing | Evidence Quality |
| RT-004-20260702-i1 | No naming authority/arbiter exists at ratification (TBR-2 unresolved) — near-duplicate domain slugs can shadow an existing domain and pass exact-string L-3 uniqueness | Rule Circumvention | Medium | Major | P1 | Missing | Internal Consistency |
| RT-005-20260702-i1 | Cross-branch/cross-project NNN allocation race for the *same* domain slug is unresolved — replaces one distributed-numbering race (bare `ADR-NNN`) with a structurally identical, only statistically rarer, one | Dependency | Medium | Major | P1 | Partial (post-hoc merge-time only) | Methodological Rigor |
| RT-006-20260702-i1 | Path 2 promotion (rename + tombstone) citation re-pointing is fully manual with no CI-gated verification, re-creating the exact stale-citation harm the standard exists to solve | Degradation | Medium | Major | P1 | Partial (WARN-only, structured fields only) | Traceability |
| RT-007-20260702-i1 | Transient `projects/*/orchestration/**` exemption is a clean, already-populated (11 files verified) hiding spot for colliding/bare IDs never checked by any FAIL rule | Boundary | High | Major | P1 | Missing (explicitly advisory-only) | Completeness |
| RT-008-20260702-i1 | ID-extraction algorithm for `{slug}-NNN` is unspecified when a domain slug itself contains an embedded 3-digit token, creating parser ambiguity for the (currently unbuilt) lint | Ambiguity | Low | Minor | P2 | Missing (spec silent) | Methodological Rigor |

**Finding ID format:** `RT-{NNN}-{execution_id}`, execution_id = `20260702-i1` (iteration 1, this session).

---

## Finding Details

### RT-001: L5 CI lint is entirely unbuilt and unwired — enforcement is not "advisory," it is non-existent [CRITICAL]

**Attack Vector:** The rule draft's [L5 CI Lint Specification](adr-standards-rule-draft.md) section (`design/adr-standards-rule-draft.md:171-186`) describes 7 rules (L-1 FAIL through L-7 WARN) in present-tense, operative language ("MEDIUM-tier means the lint *reports* and can *fail CI*"). In fact, no such script exists anywhere in the repository, and no workflow references it.

**Category:** Degradation (protection erodes to zero the moment enforcement is assumed rather than verified)
**Exploitability:** High — zero adversarial effort required; the gap already exists for every contributor today.
**Severity:** Critical — every claim in either document that a violation "will be rejected," "blocks CI," or is "caught by L-N" is false in the present tense. A hostile contributor today faces zero enforcement of any rule in this standard.
**Existing Defense:** Missing. Verified via `Glob("scripts/lint_adr_convention.py")` -> no files found. Verified via `Grep("adr", .github/workflows/*.yml)` across `ci.yml`, `docs.yml`, `pat-monitor.yml`, `release.yml`, `security-scan.yml`, `version-bump.yml` -> the only match is an unrelated, itself-dangling comment (`ci.yml:2`, see RT-003) — no ADR-lint job exists in any workflow.
**Evidence:** `design/adr-standards-rule-draft.md:171-186` (spec written as though operative); `decisions/ADR-PROJ031-004-adr-identifier-convention.md` Risk table entry "R-5: Lint never gets built; convention stays advisory-only | MED | HIGH" (line ~357); Migration Plan item "M-6 | Implement + wire the L5 CI lint ... | devsecops | **Yes** (prevents FM-1)" (line ~400) — marked gating in prose only, with no CI mechanism that actually blocks anything until M-6 lands, no owner SLA, no linked tracking ticket.
**Dimension:** Methodological Rigor (the standard's central enforcement claim is unverified) and Completeness (a required deliverable component is absent).
**Countermeasure:** See P0 recommendations.
**Acceptance Criteria:** A CI job (e.g., in `.github/workflows/ci.yml`) invokes `uv run` (H-05) against a real `scripts/lint_adr_convention.py`, with at least one green CI run linked as evidence, before this ADR's `Status` may move past `PROPOSED`.

---

### RT-002: Every FAIL-class lint rule has an ungated, unaudited override — the standard defines a universal bypass for its own collision-safety guarantees [CRITICAL]

**Attack Vector:** `design/adr-standards-rule-draft.md:173`: "MEDIUM-tier: FAIL rules block CI but are **overridable via inline `adr-lint: ignore <rule> — <justification>` or a waiver file**; WARN rules are advisory." No schema, minimum-justification-length check, required second-reviewer/CODEOWNERS gate, expiry, or audit ledger is specified for either override mechanism, and neither document states *where* the inline annotation must live (frontmatter? body? PR description?) or what parses it.
**Category:** Rule Circumvention
**Exploitability:** High — once a lint exists (see RT-001), defeating any FAIL rule (L-1 Form, L-2 No-new-bare, L-3 Slug-uniqueness, L-4 Dialect-location) costs one unreviewed comment.
**Severity:** Critical — L-3 is explicitly described elsewhere in the same corpus as "the one non-local B check" (`ADR-PROJ031-004.md:127,133`) that is supposed to guarantee collision-safety for the entire domain-slug scheme; an ungated override on the sole non-local invariant is a defeat of the standard's core safety property, not a minor gap.
**Existing Defense:** Missing in effect — the rule exists syntactically but is negated by the unrestricted override clause.
**Evidence:** `design/adr-standards-rule-draft.md:173` (override clause, quoted above); cross-reference `ADR-PROJ031-004.md:126-127` ("Slug-uniqueness is an uncentralized discipline, not a structural guarantee") and `:338` (Negative consequence #1) which frame L-3 as *the* mitigation for this exact known weakness — the mitigation itself is then shown to be trivially bypassable.
**Dimension:** Internal Consistency — the draft states in the same sentence that FAIL rules "block CI" and that they are simultaneously overridable by an unaudited comment; these two claims are in direct tension and the document does not reconcile them.
**Countermeasure:** See P0 recommendations.
**Acceptance Criteria:** Override mechanism (if retained at all for L-2/L-3) requires a machine-checkable frontmatter field, non-empty justification of minimum length, a required second-reviewer approval, and an append-only audit ledger checked by a separate CI step.

---

### RT-003: A live dangling ADR citation already exists in `.github/workflows/ci.yml`, undetected — and would remain undetected by the proposed lint even once built [CRITICAL]

**Attack Vector:** `.github/workflows/ci.yml:2` contains the comment: `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md`. Verified this session: `Glob("**/ADR-CI-001*")` -> no files found; `Glob("projects/PROJ-001-plugin-cleanup/**")` -> no files found. This is a real, currently-dangling reference to a project and ADR that do not exist anywhere in the repository — the exact "stale citation" failure mode the parent ADR cites as its own motivating harm (the still-unrepaired `ADR-PROJ007-001/002` references, `ADR-PROJ031-004.md:47,123,217,529`).
**Category:** Dependency (the standard's citation-integrity promise depends on a scan scope that does not cover this location) — Boundary aspects also apply (workflow YAML sits outside the surveyed corpus).
**Exploitability:** High — this vector requires zero adversarial effort; it already occurred, by a careless (not even hostile) past contributor, and neither deliverable's design would catch it.
**Severity:** Critical for two independent reasons: (1) it demonstrates the research corpus survey underlying this ADR is incomplete — it names 8 ID families (`ADR-PROJ031-004.md:67-77`) but misses a 9th, CI-scoped family (`ADR-CI-NNN`) that already exists and is already broken; (2) it demonstrates the proposed L-7 rule is insufficient by construction: L-7 ("Tombstone integrity," WARN, `design/adr-standards-rule-draft.md:183`) only validates that `superseded_by`/`promoted_to` **frontmatter fields** resolve — it performs no repo-wide free-text scan for `ADR-*` string citations in prose, comments, or workflow files. The Path 2 promotion process itself claims otherwise: "Re-point citations: `grep -rl \"ADR-PROJ{NNN}-NNN\"` ... The L5 lint (L-7) then flags any *surviving* reference to a tombstoned ID" (`design/adr-standards-rule-draft.md:139`) — this claim is **factually incorrect as specified**; L-7 cannot and does not do this.
**Existing Defense:** Missing.
**Evidence:** `.github/workflows/ci.yml:2` (dangling citation, verified via Glob this session); `design/adr-standards-rule-draft.md:139,183` (L-7 scope and the promotion-process claim about it); `decisions/ADR-PROJ031-004.md:67-77` (corpus family table, 8 families, missing the CI-scoped 9th).
**Dimension:** Evidence Quality (the ADR's own evidentiary survey has a demonstrated blind spot) and Completeness.
**Countermeasure:** See P0 recommendations.
**Acceptance Criteria:** A new lint rule (proposed L-8) performs a repo-wide free-text scan for `ADR-[A-Za-z0-9-]+-\d{3}` tokens that fail to resolve to an existing canonical/dialect ADR file, across all repo files (not just `decisions/`/`docs/design/` frontmatter); the `ADR-CI-001` reference is remediated as the first concrete test case.

---

### RT-004: No naming authority exists for domain slugs at ratification — near-duplicate slugs can shadow an existing domain past exact-string uniqueness checks [MAJOR]

**Attack Vector:** `decisions/ADR-PROJ031-004.md:320` (L2 Architectural Implications) states: "This needs a lightweight index (`docs/design/README.md`) and an arbiter (**TBR-2**)." TBR = "to be resolved" — i.e., explicitly unresolved. L-3 (`design/adr-standards-rule-draft.md:179`) performs `sort | uniq -d` on **exact** `{slug}-NNN` strings only — a purely syntactic check with no semantic or near-duplicate detection (`agent-design` vs. `agent-designs` vs. `agent-desgin`; `oauth-refresh` vs. `oauth2-refresh`). A contributor wanting a project-local decision to *appear* to extend or supersede an existing framework domain can pick a cosmetically distinct slug that passes every FAIL rule while reading, to a human skimming `docs/design/`, as a continuation of that domain.
**Category:** Rule Circumvention (bypasses the intended collision/authority protection via a technically-compliant near-miss).
**Exploitability:** Medium — requires the contributor to know the target slug and intend the confusion; no special access needed.
**Severity:** Major — this is the ADR's own Risk R-3 / Failure Mode FM-4 ("taxonomy sprawl... discoverability... degraded," `ADR-PROJ031-004.md:355,370`) reframed under adversarial intent rather than organic drift; the mitigation named there ("arbiter... periodic audit") is a future intention, not a control that exists today.
**Existing Defense:** Missing — verified via `Glob("docs/design/README.md")` -> no files found; the index that would let a human/tool detect near-duplicates does not exist.
**Evidence:** `decisions/ADR-PROJ031-004.md:320,340,355,370` (TBR-2, R-3, FM-4); `design/adr-standards-rule-draft.md:179` (L-3 exact-match-only definition); `Glob` verification this session confirming absence of `docs/design/README.md`.
**Dimension:** Internal Consistency (the ADR claims collision-safety via L-3 while the actual authority mechanism it depends on is admittedly unresolved).
**Countermeasure:** See P1 recommendations.
**Acceptance Criteria:** `docs/design/README.md` domain index exists, is populated with the 3 current framework domain slugs, and a new-slug reservation step (reviewed by a named owner) is a required part of the authoring process before this standard is treated as collision-safe for cross-project use.

---

### RT-005: Cross-branch NNN allocation for the same domain slug is a structurally-identical, only statistically rarer, restatement of the exact race this ADR rejects Scheme E for [MAJOR]

**Attack Vector:** Constraint c-006 (`decisions/ADR-PROJ031-004.md:93`) requires the scheme be lint-able "without a central registry or global counter (no server process; monorepo, many concurrent branches [66 verified])." ADR-M-005 (`design/adr-standards-rule-draft.md:49`) requires `NNN` be "monotonic within its namespace ... never reused," but no mechanism prevents two concurrent branches from independently minting `ADR-{same-slug}-002` for unrelated decisions before either merges. L-3 (FAIL) only detects this **post-merge** — whichever branch merges second breaks CI — and the only named resolution anywhere is Failure Mode FM-2's one line, "arbiter assigns a disambiguated slug" (`decisions/ADR-PROJ031-004.md:369`), which depends on the same undefined TBR-2 role as RT-004.
**Category:** Dependency (relies on the environmental absence of true concurrency, which the ADR's own evidence — 66 branches — contradicts) with a Degradation aspect (the race gets more likely as corpus/domain reuse grows).
**Exploitability:** Medium — requires two genuinely concurrent authors targeting the same domain slug, but the repo's own cited concurrency level (c-006 evidence) makes this a real, recurring operating condition rather than a theoretical edge case.
**Severity:** Major — the ADR explicitly rejects Scheme E (global monotonic numbering) *because* "it needs a central registry/counter Jerry does not have... precisely what log4brains abandoned after real git-merge pain" (`decisions/ADR-PROJ031-004.md:149-150`); domain-slug NNN narrows the collision surface (same-slug only) but does not structurally solve the identical class of problem it uses to disqualify Scheme E.
**Existing Defense:** Partial — L-3 catches the collision at merge time (after the fact), but there is no pre-merge coordination, reservation, or SLA-bound resolution procedure.
**Evidence:** `decisions/ADR-PROJ031-004.md:93,149-150,369`; `design/adr-standards-rule-draft.md:49,179`.
**Dimension:** Methodological Rigor (a stated design rationale — "no central registry" — is not actually achieved for the chosen scheme, only made statistically less frequent).
**Countermeasure:** See P1 recommendations.
**Acceptance Criteria:** CI failure output for an L-3 violation names the specific conflicting ADR and gives an explicit next-`NNN` instruction so the common case is self-service; only the rarer same-slug-different-subject shadow case (RT-004) requires the arbiter.

---

## Recommendations

### P0 (Critical — MUST mitigate before acceptance)

| ID | Countermeasure | Acceptance Criteria |
|----|-----------------|----------------------|
| RT-001 | Treat lint existence + CI wiring as a hard precondition of any `Status` beyond `PROPOSED`, not a post-hoc migration item (M-6 currently reads as future work, not a gate). | A working `scripts/lint_adr_convention.py`, invoked via `uv run` (H-05) from a named CI job (e.g., in `.github/workflows/ci.yml`), with at least one linked green run, exists before `Status: ACCEPTED`. |
| RT-002 | Redesign the override/waiver mechanism for L-2 and L-3 specifically: machine-checkable frontmatter field, non-empty justification of minimum length, required second-reviewer approval, append-only audit ledger checked by a separate CI step. A bare unreviewed inline comment MUST NOT be sufficient to bypass a collision-safety FAIL rule. | Override schema documented in the rule draft; a CI check verifies the audit ledger is append-only and every override entry has a non-placeholder justification and an approver. |
| RT-003 | Add a new lint rule (L-8) performing a repo-wide free-text scan for `ADR-*-NNN`-shaped tokens that do not resolve to an existing canonical/dialect ADR file or documented alias, across ALL repo files (workflows, rule files, skill docs), not just `decisions/`/`docs/design/` frontmatter. Remediate the discovered `ADR-CI-001` dangling reference in `ci.yml:2` as the first concrete test case. | L-8 exists and runs repo-wide; `ci.yml:2`'s dangling reference is either resolved (file created) or the comment is removed/corrected. |

### P1 (Important — SHOULD mitigate)

| ID | Countermeasure | Acceptance Criteria |
|----|-----------------|----------------------|
| RT-004 | Stand up a minimum-viable arbiter/index before ratification: `docs/design/README.md` as the single source of truth for allocated domain slugs, with a lightweight reservation step (new slug = new indexed row, reviewed by a named owner) required before a genuinely *new* domain slug (not a next-`NNN` within an existing one) may be used. | Index file exists, populated with the 3 current framework slugs; the authoring/promotion process references it as a required step. |
| RT-005 | Document an explicit self-service collision-resolution path in the L-3 CI failure message itself (name the conflicting ADR, instruct the author to bump to the next free `NNN`), reserving the arbiter only for the rarer same-slug-different-subject shadow case. | L-3 failure output includes actionable next-step text, not just a bare FAIL. |
| RT-006 | Make citation re-pointing a required, CI-verifiable check on the promoting PR itself: the PR that flips the old dialect ADR to `SUPERSEDED` must also demonstrate (via the new L-8 from RT-003) zero remaining live references to the pre-promotion ID outside the tombstone fields. | Path 2 promotion PRs are blocked by L-8 if any surviving reference to the old ID is found. |
| RT-007 | Narrow the transient exemption: require any `ADR-*`-named file under `projects/*/orchestration/**` to carry an explicit non-canonical marker, and state plainly that such files MUST NOT be cited as authoritative outside their own orchestration session; add a lint rule flagging external citations of orchestration-path ADR IDs. | Rule draft states the non-citability convention explicitly; a lint rule (or L-8 extension) flags cross-session citation of orchestration-path ADR files. |

### P2 (Monitor — MAY mitigate)

| ID | Countermeasure | Acceptance Criteria |
|----|-----------------|----------------------|
| RT-008 | Specify the exact `{slug}-NNN` identity-extraction algorithm (e.g., "NNN is the LAST `\d{3}` group immediately preceding the optional title-slug and `.md` extension") with one worked example covering a slug containing an embedded digit token, before M-6 implementation begins. | Rule draft's ID Scheme section includes the explicit extraction algorithm and a disambiguating worked example. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-001 (enforcement component absent), RT-003 (corpus survey missed a live 9th ID family), RT-007 (transient exemption is an unbounded gap) |
| Internal Consistency | 0.20 | Negative | RT-002 (FAIL rules described as blocking CI while simultaneously universally overridable — direct self-contradiction); RT-004 (collision-safety claim vs. admittedly unresolved arbiter, TBR-2) |
| Methodological Rigor | 0.20 | Negative | RT-001 (core enforcement claim unverified); RT-005 (the stated rationale for rejecting Scheme E — "no central registry" — is not actually achieved for the chosen scheme); RT-008 (spec ambiguity) |
| Evidence Quality | 0.15 | Negative | RT-003 — the corpus survey, presented as an 11-source review, missed a real, live, currently-dangling citation that directly undercuts the ADR's central motivating claim |
| Actionability | 0.15 | Neutral | Countermeasures proposed above are concrete and independently testable; the ADR's existing Migration Plan is otherwise well-structured, it simply mis-sequences M-6 as non-gating |
| Traceability | 0.10 | Negative | RT-003/RT-006 show the standard's own citation-integrity guarantee — its central promise — is not verifiable end-to-end; L-7 does not do what the Promotion Process narrative says it does |

**Overall assessment:** Major remediation required before ratification beyond `PROPOSED`. The convention's *design* (subject-encoded identity, frontmatter provenance, pure-file-move promotion) is sound and well-argued, but its *enforcement* is currently theoretical — the lint does not exist, and even once built, every FAIL rule as specified has an unrestricted bypass. The standard should not be presented to stakeholders as "lint-enforced" (`design/adr-standards-rule-draft.md:11`) until RT-001/RT-002/RT-003 are closed.

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 3 (RT-001, RT-002, RT-003)
- **Major:** 4 (RT-004, RT-005, RT-006, RT-007)
- **Minor:** 1 (RT-008)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor Definition, Attack Vector Enumeration, Defense Gap Assessment, Countermeasure Development, Synthesis/Scoring)
- **Attack Vector Categories Covered:** 5 of 5 (Ambiguity, Boundary, Rule Circumvention, Dependency, Degradation)
- **H-16 Compliance:** Assumed per orchestration protocol; not independently verifiable under the blind-review constraint (see Header)

---

*Generated by: adv-executor (S-001 Red Team Analysis)*
*Constitutional Compliance: P-001 (all claims cited to file+line or explicit Glob/Grep verification performed this session), P-002 (persisted to file), P-003 (no subagents spawned), P-004 (provenance cited throughout), P-011 (evidence-based), P-020 (no files outside this report edited), P-022 (inference explicitly labeled in Header; no fabricated claims — all dangling-citation and missing-file claims verified via Glob/Grep this session)*
