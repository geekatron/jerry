# Devil's Advocate Report: FU/DEC Log Convention (Design Doc + 5 Staging Artifacts)

> **Type:** adversarial-strategy-execution-report
> **Strategy:** S-002 Devil's Advocate
> **Iteration:** 008 (VERIFIED-CRITICALS protocol)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Deliverable, criticality, H-16 note |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical + Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-002 Devil's Advocate
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/LLM-DECISION-LOG.template.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/examples-appendix.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/hook-design-note.md`
- **Criticality:** C4 (gate 0.95)
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-002, iteration-008)
- **H-16 compliance note (disclosed, per P-022):** `iteration-008/s-003-findings.md` exists on disk (confirmed via directory listing), evidencing S-003 (Steelman) executed for this iteration ahead of this S-002 pass — the tournament's own group ordering (self-refine -> steelman -> challenge -> verify -> decompose -> score) satisfies H-16 at the orchestration layer. Per this iteration's explicit BLIND PROTOCOL instruction, this execution did **not** read `iteration-008/s-003-findings.md`'s content (each strategy in this tournament runs blind to sibling current-round outputs to prevent cross-contamination). This is a documented, task-authorized deviation from the template's default Step 1 procedure (which reads the S-003 output directly) — flagged transparently, not concealed. Findings below were built solely from the deliverable text plus the readable disposition history (`iteration-007/restore-notes.md`, iterations 001-006 findings).
- **Scope discipline:** only findings that block the convention's stated purpose (feedback/decisions never lost; operator-burden-free capture; navigable growth; honest metadata) are reported. Findings that restate an already-disclosed residual (explicitly named as accepted in the design doc's Revision Changelog, "Residuals Disclosed," or `iteration-007/restore-notes.md`) are excluded per this iteration's instructions.

---

## Summary

5 counter-arguments identified (2 Critical, 2 Major, 1 Minor). All 5 attack mechanisms that were *added or left unexamined* in prior remediation rounds rather than re-litigating any of the 9 already-closed iteration-006/007 criticals (zero regression confirmed against `iteration-007/restore-notes.md`). The two Criticals are: (1) the git-worktree/branch merge-conflict id-renumbering rule contradicts the id scheme's own headline invariant ("ids never reset, a reference survives rotation") for exactly the externally-cited (graduated ADR/DECISION) case that invariant exists to protect, with no repair path for citations outside the log files themselves; (2) the FM-001 inline-doc dedup check keys on `path:line/anchor` location only, with no content comparison, so an operator's in-place edit to a marker at the same location is silently treated as an already-logged duplicate and never captured -- a direct, mechanism-level violation of "feedback ... never lost," not a remembered-to-log failure. Both are fixable by wording/disclosure alone, consistent with this package's own established remediation style (zero new machinery required). Recommend REVISE to address the two Criticals; the two Majors and one Minor may proceed with acknowledgment per this project's own precedent for MEDIUM-tier disclosed residuals.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i8 | Worktree/branch merge-conflict id-renumbering breaks external citations to graduated ids | Critical | `design/feedback-decision-log-convention-design.md:79`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:27` | Internal Consistency |
| DA-002-i8 | FM-001 inline-doc dedup keys on location only, not content -- edited markers silently dropped | Critical | `design/staging-feedback-logs/feedback-decision-logs-standards.md:51`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:25`; `design/staging-feedback-logs/examples-appendix.md:169` | Completeness |
| DA-003-i8 | H-31 bare-alias enumeration has no bound/fallback for candidate-list size at scale | Major | `design/feedback-decision-log-convention-design.md:74`; `design/staging-feedback-logs/examples-appendix.md:170` | Actionability |
| DA-004-i8 | `Related: <id>` cross-log citation omits the `<scope>:FU.N` prefix the design itself defines, leaving cross-scope citation ambiguous | Major | `design/feedback-decision-log-convention-design.md:73,190`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:69` | Traceability |
| DA-005-i8 | Nav table (H-23/NAV-004) coverage undefined for a growing log's per-entry headings | Minor | `design/staging-feedback-logs/FEEDBACK-LOG.template.md:7-14`; `.context/rules/markdown-navigation-standards.md` NAV-004 | Traceability |

**Finding ID Format:** `DA-{NNN}-i8` (iteration 8 execution).

---

## Finding Details

### DA-001-i8: Worktree/branch merge-conflict renumbering silently invalidates external citations to graduated ids [CRITICAL]

**Claim Challenged:** The id scheme's headline invariant, stated at `design/.../feedback-decision-log-convention-design.md:198`: *"`next` is written once at seal time -- sealed segments never relink; ids never reset, so a reference survives rotation and each log's index resolves *id -> file* (the id *is* the join key, FU.6's payoff)."* This durability guarantee is precisely why `LOG-M-004` (graduation) lets an external ADR or worktracker DECISION entity permanently cross-link to a `DEC-LLM-NNN` id (`Reflected in:` / `Source:`).

**Counter-Argument:** The design's own conflict-resolution rule for the git-worktree/branch-isolated case directly contradicts that invariant. Quote, `design/.../feedback-decision-log-convention-design.md:79`: *"if ids collide, renumber the later-merged side to continue after the surviving maximum id and repair any `Superseded by:` / `Related:` references it carries."* The rule file restates this at `design/staging-feedback-logs/feedback-decision-logs-standards.md:27`: *"on conflict, keep both sides' entries in id order and **renumber** (never discard) any colliding id, repairing its `Superseded by:` / `Related:` references."*

"Repairing its `Superseded by:`/`Related:` references" repairs only the fields the renumbered entry itself carries -- i.e., in-log, outbound references. It does **nothing** for **inbound** references held by artifacts *outside* the two log files: a worktracker DECISION entity's `Source:` field, an ADR's `Reflected in:` cross-link, a *different* already-sealed segment's `Related: DEC-LLM-012` citation, a prior commit message, or a human's notes -- all of which the design explicitly designed the id scheme to support as **durable, never-changing** identifiers (`design/.../feedback-decision-log-convention-design.md:33`: *"a crisp boundary to worktracker `DEC-NNN` and ADRs (cross-link, never duplicate)"*; `LOG-M-004`: *"graduates into a worktracker DECISION and/or a Scheme-B ADR, with a bidirectional cross-link"*).

Crucially, this is not a hypothetical: the design doc itself names git-worktree/branch-isolated sessions as **"the framework's own `isolation: worktree` capability, into which a background task can be dispatched"** (`design/.../feedback-decision-log-convention-design.md:79`) -- an actively supported Jerry pattern, not a remote edge case. A decision graduating to an ADR on branch A (`Reflected in: DEC-LLM-012`), followed by a later merge where branch B *also* independently minted `DEC-LLM-012`, will -- per this exact rule -- renumber one side's id (say, to `DEC-LLM-018`), leaving the already-shipped ADR's `Reflected in: DEC-LLM-012` pointing at either the wrong entry or nothing, with no disclosed mechanism to detect or repair it. This directly attacks "does the rotation/id/alias design survive real multi-session use?" for the one usage pattern (worktree isolation) the design names by name.

**Evidence:** `design/feedback-decision-log-convention-design.md:79`, `:198`, `:33`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:27,89`.

**Impact:** A silently broken provenance trail on a *graduated, formally-cross-linked* artifact -- the exact class of record (ADR / worktracker DECISION) this project treats as authoritative ("Authority on conflict: Wins (ratified)," design doc L1.2 boundary table). This is a "decisions... lost" failure in the sense that matters most: the record still exists, but the pointer to it silently breaks.

**Dimension:** Internal Consistency (the id-durability invariant and the merge-renumbering rule cannot both be true for a graduated id).

**Response Required:** Either (a) forbid renumbering entirely for ids that have graduated (carry a `Reflected in:`/external cross-link) -- reconcile worktree merges for graduated ids by a different mechanism (e.g., a compound scope-qualified id for the losing branch's colliding range, consistent with the `<scope>:FU.N` global-reference format the design already defines), or (b) keep renumbering but add an explicit disclosed-residual clause: *"a renumbered id may silently invalidate any external citation (ADR `Reflected in:`, DECISION `Source:`, another log's `Related:`) made before the merge; the operator resolving the conflict MUST grep the repository for the old id string and update external citations -- this is not automatic and is not covered by lint 2."* Option (b) is a one-clause disclosure, zero new machinery, and consistent with every other Critical this package has closed to date.

**Acceptance Criteria:** The worktree-merge conflict rule (design L1.1 + rule LOG-M-005) explicitly states whether graduated/externally-cross-linked ids are exempt from renumbering, or explicitly discloses the external-citation-breakage residual and assigns the repair step to the operator performing the merge.

---

### DA-002-i8: FM-001 inline-doc dedup keys on location only; an edited marker at the same location is silently never captured [CRITICAL]

**Claim Challenged:** `design/staging-feedback-logs/feedback-decision-logs-standards.md:51`: *"Before minting, check for an existing entry carrying the same `source: inline-doc` `path:line/anchor` -- if one exists, do not re-mint (skip, or note the re-encounter on the existing entry) -- this dedups repeat reads of the same marker via the existing sub-field, no new field or doc-mutation (FM-001)."* Restated verbatim in `design/staging-feedback-logs/FEEDBACK-LOG.template.md:25` and `design/staging-feedback-logs/examples-appendix.md:169`.

**Counter-Argument:** The dedup key is purely **locational** (`path:line/anchor`), not content-based. Inline `FU:`/`DEC:` markers are single lines living inside documents that are, by the convention's own design, expected to be revised iteratively (this very design package is such a document, under active multi-round revision). If an operator edits a marker's text in place at the same line -- e.g., `FU: fix the diagram` -> `FU: also add a legend` -- the dedup rule as written treats the second read as "an existing entry carrying the same `path:line/anchor`" and instructs "do not re-mint." The updated feedback is never captured. This is not a remembered-to-log failure (which the MEDIUM-tier posture already accepts); it is a **deterministic, mechanism-level drop** that will fire every time a marker is edited in place rather than added as a new line -- the more common editing pattern for a one-line annotation.

This finding is materially different from every already-disclosed residual around inline-doc harvest (`design/.../feedback-decision-log-convention-design.md:91`'s "coverage caveat," about a marker never being *revisited*): here the document **is** revisited and read, and the harvest mechanism itself is what drops the update. It is also a fresh regression introduced by the very fix (FM-001, iteration-006) that closed the *previous* "no dedup" finding (`iteration-007/restore-notes.md` row 5) -- solving over-capture created a silent under-capture path that was not re-examined in the iteration-007 RESTORE pass (which only re-verified the *original* 6 iteration-006 Criticals against current text, not new interactions the fix itself introduced).

**Evidence:** `design/staging-feedback-logs/feedback-decision-logs-standards.md:51`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:25`; `design/staging-feedback-logs/examples-appendix.md:169`.

**Impact:** Direct violation of the package's own governing principle stated at `design/.../feedback-decision-log-convention-design.md:38`: *"what depends on the model remembering will eventually be forgotten... only judgment fields... remain model/human-authored."* Here, correctly re-capturing an edited marker requires no memory at all -- it requires only a content comparison the rule never specifies -- yet the design as written guarantees the loss regardless of diligence.

**Dimension:** Completeness (the capture-trigger / dedup procedure is incomplete: it specifies the skip condition but not the re-mint condition for changed content).

**Response Required:** Amend the FM-001 rule (in the rule file, both templates, and the appendix) to key the dedup check on `path:line/anchor` **and** marker text: skip only if both location and content are unchanged from the existing entry; if content differs, mint a new entry (optionally noting `Related: <old id>` as an update, consistent with the existing `Superseded by:` pattern already used elsewhere in this same document). This is a one-clause wording fix, zero new field/lint/file.

**Acceptance Criteria:** All three artifacts that state the FM-001 dedup rule (rule file LOG-M-006/FEEDBACK-LOG section, FEEDBACK-LOG.template.md, examples-appendix.md Common Cases) require content match, not location match alone, before skipping a mint.

---

### DA-003-i8: H-31 bare-alias enumeration has no bound or fallback for candidate-list size at scale [MAJOR]

**Claim Challenged:** `design/.../feedback-decision-log-convention-design.md:74`: *"Back-reference disambiguation (H-31)... The assistant **enumerates the candidates and asks which one is meant** (per H-31), rather than silently inferring from recency... Where the user's own reference carries disambiguating context..., use it to narrow or rank candidates before presenting the list."*

**Counter-Argument:** The design's own worked example of normal operator behavior (`FEEDBACK-LOG.template.md:20`: *"you will typically restart at `FU.0` every turn and every document you review"*) guarantees that the single most common alias token (`FU.0`, or any other frequently-reused label) accumulates one candidate per turn the operator reused it. Across a long-running, multi-session project -- precisely the use case this convention targets -- a bare query like `examples-appendix.md:170`'s own worked example ("What's the status of FU.0?") will, absent operator-supplied disambiguating context, enumerate a candidate list whose size grows unboundedly with project age. The design specifies *how* to narrow the list *if* the operator volunteers context, but specifies no fallback for the far more common case where they do not (as in the example itself, which supplies none). At scale this makes the flagship disambiguation mechanism (the mechanism this project's own tournament has hardened across DA-002/FM-008/H-31-axes in prior rounds) practically unusable for exactly the query pattern it was built to answer -- inverting "navigable growth" into "growth makes navigation harder."

**Evidence:** `design/.../feedback-decision-log-convention-design.md:74`; `design/staging-feedback-logs/examples-appendix.md:170`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:20`.

**Impact:** Degrades the "operator-burden-free" and "navigable growth" purpose pillars at the exact scale (long multi-session use) the convention is designed for, though it does not lose data (every candidate is still a real, findable entry).

**Dimension:** Actionability (the enumeration procedure lacks a concrete fallback step when no disambiguating context is offered).

**Response Required:** Add a lightweight fallback, consistent with the design's own near-cap heuristic style (e.g., `feedback-decision-logs-standards.md:28`'s "at or near cap... derive the next id"): if the candidate count exceeds a small threshold (e.g., ~5), ask the operator for narrowing context (turn recency, topic word, or scope) **before** enumerating the full list, rather than presenting an unbounded list first.

**Acceptance Criteria:** The H-31 enumeration procedure (design L1.1 + examples-appendix Common Cases) names a candidate-count threshold above which narrowing is requested before listing.

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- DA-001-i8: State explicitly whether graduated/externally-cross-linked ids are exempt from worktree-merge renumbering, or disclose the external-citation-breakage residual and assign the repair step. One clause in design L1.1 + rule LOG-M-005.
- DA-002-i8: Key the FM-001 dedup check on location **and** content, not location alone, across all three artifacts that state it (rule file, FEEDBACK-LOG.template.md, examples-appendix.md).

**P1 (Major -- SHOULD resolve; require justification if not):**
- DA-003-i8: Add a candidate-count threshold that triggers a narrowing question before the H-31 enumeration lists candidates.
- DA-004-i8: Either require the `<scope>:FU.N` prefix in `Related:` fields when the citation crosses scope, or explicitly disclose that `Related:` is intra-scope-only and cross-scope citation is unsupported (name it alongside the existing multi-scope discovery caveat, design L1.1).

**P2 (Minor -- MAY resolve; acknowledgment sufficient):**
- DA-005-i8: Add a one-line clarification that the nav table lists structural sections only (not one row per `## FU.N`/`## DEC-LLM-NNN` entry), and that entry discovery relies on the Segment Index + `grep`, not nav-table completeness.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002-i8: the inline-doc dedup procedure omits the content-comparison step needed to avoid silently dropping edited feedback. |
| Internal Consistency | 0.20 | Negative | DA-001-i8: the worktree-merge renumbering rule contradicts the id scheme's own "ids never reset" durability invariant for graduated ids. |
| Methodological Rigor | 0.20 | Neutral | The 6-artifact package's remediation methodology (per-round propagation sweeps) is otherwise sound and evidenced; these findings are gaps in specific mechanisms, not the overall method. |
| Evidence Quality | 0.15 | Neutral | Findings are drawn directly from the shipped text with file+line citations; no evidence-quality defect identified in the deliverable itself beyond DA-001/DA-002. |
| Actionability | 0.15 | Negative | DA-003-i8: the H-31 enumeration procedure lacks a concrete fallback for the unbounded-candidate-list case. |
| Traceability | 0.10 | Negative | DA-004-i8: `Related:` field citations are not reliably resolvable across scope boundaries despite a global-reference format existing for exactly this purpose. |

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 2
- **Major:** 2
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Assume Role; Document & Challenge Assumptions; Construct Counter-Arguments; Require Substantive Responses; Synthesize & Score Impact)
