# FMEA Report: ADR Identifier, Location, and Promotion Convention (Post-Subtraction Package, Iteration 6)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-05
**Reviewer:** adv-executor (S-012, blind independent reviewer, iteration 6)
**H-16 Compliance:** S-003 Steelman embedded in Options A–F (per the ADR's own disclosure at the top of the document); confirmed present in the reviewed artifact.
**Elements Analyzed:** 13 | **Failure Modes Identified:** 12 | **Total RPN:** 2,438

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All 12 findings with S/O/D/RPN and severity |
| [Finding Details (Critical and Major)](#finding-details-critical-and-major) | Expanded evidence for each Critical/Major finding |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Authoritative finding counts |

---

> **Scope note (per invoking instructions).** This FMEA evaluates the package **as slimmed** by the user-authorized subtraction pass (FU.1, 2026-07-05; see `subtraction-pass-notes.md`). None of the findings below ask for restoration of deleted machinery (waiver ledger, 18-rule lint, CODEOWNERS gate, two-tier ratification, producer-drift monitor L-14) — that deletion is treated as the valid, MEDIUM-tier-appropriate design posture it is. Every finding here is either (a) a defect in content that **survived** the slimming (the 5 retained lint rules, the companion-document pair, the migration table), or (b) a **side-effect of the slimming itself** (a stale cross-reference, an undisclosed disposition gap) — not a demand to re-grow the lint.

---

## Summary

Twelve failure modes were identified across 13 decomposed lifecycle elements (creation, frontmatter, ID-grammar/lint scan-scope, cross-reference/relationship-integrity, amend, supersede, promotion Path 1, promotion Path 2, the 5-rule lint as a whole, onboarding, producer-agent compliance, migration-plan tracking, and companion-document consistency). Three findings are **Critical** (RPN >= 200): a dangling cross-reference to a "New-Project-Onboarding section" that no longer exists in the slimmed rule draft (FM-001, RPN 504); a structural blind spot in the 5-rule lint's own stated file-scan scope that silently excludes the real, currently-cited `ADR-STORY015-001` from grammar/duplicate/location checking while the grandfather-regression test claims to cover it (FM-002, RPN 576); and an iteration-4 finding (RT-007) whose sole supporting control (`L-4b`) was deleted in the subtraction pass with **no corresponding disposition entry** in `subtraction-pass-notes.md`, breaking the pass's own stated completeness bar ("no Critical left without a disposition") (FM-005, RPN 336). Five Majors concern incomplete relationship-field checking (L-7 verifies only 3 of 6 frontmatter relationship fields), an internal inconsistency between the two companion documents over how PROJ-014's bare ADRs are characterized, an unbacked enforcement claim (the M-9 "review checklist" cites no actual PR-template artifact), an open H-32 GitHub-Issue-parity gap across the entire Migration Plan, and under-specified ownership for the two disclosed manual-audit residuals (R-B, R-C). Four Minors are cosmetic/traceability items. **Recommendation: REVISE — targeted, document-only corrections (no new machinery) before acceptance at the 0.95 gate.**

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|---------------------|
| FM-001-20260705T-i6 | Onboarding | Migration-Plan row M-14 and Changelog v1.2/v1.3 assert a "New-Project-Onboarding section added to Deliverable 2" that does not exist in the current rule draft | 7 | 9 | 8 | 504 | Critical | Either restore a short Onboarding section in the rule draft, or edit M-14/Changelog to stop asserting it exists | Internal Consistency |
| FM-002-20260705T-i6 | ID Grammar & Lint Scan Scope | L-1/L-3/L-4's stated scan scope (`projects/*/decisions/`, `docs/design/`) structurally excludes the real, live `ADR-STORY015-001` (entity-embedded dialect, lives in `work/.../STORY-015.../`, no `decisions/` in path) — yet the grandfather-regression test claims to validate all "16 live dialect files" including `STORY015×1` | 8 | 9 | 8 | 576 | Critical | Add an explicit entity-embedded scan-path clause to L-1/L-3/L-4 (e.g. `projects/**/{PROJ,EPIC,STORY,FEAT}[0-9][0-9][0-9]-*/ADR-*.md`), or disclose the exclusion as a named residual and drop STORY015 from the "files that pass L-1" claim | Methodological Rigor |
| FM-003-20260705T-i6 | Cross-Reference / Supersede / Amend | L-7 "Relationship target resolves" checks only `superseded_by`/`promoted_to`/`promoted_from` — the frontmatter schema also defines `supersedes`, `amends`, `amended_by`, which are never verified to resolve | 6 | 5 | 6 | 180 | Major | Extend L-7's field list to all 6 relationship fields, or explicitly disclose the 3-of-6 asymmetry as a residual | Methodological Rigor |
| FM-004-20260705T-i6 | Companion-Document Consistency | Rule draft's "Frozen and Grandfathered Legacy" section calls PROJ-014's bare `ADR-001..004` drafts "valid in place, extendable within their dialect," while the ADR's own Migration Plan describes the identical set as transient, colliding with frozen `docs/adrs/`, and using the deprecated bare-numbering format (Scheme E degenerate) | 4 | 6 | 6 | 144 | Major | Reword the rule-draft sentence to separate "grandfathered dialect families" from "PROJ-014 bare drafts (transient, not a dialect)" | Internal Consistency |
| FM-005-20260705T-i6 | Migration-Plan / Disposition Tracking | Changelog v1.5 records new FAIL rule L-4b (repository-based-topology dialect rejection) as closing finding RT-007; the subtraction pass deletes L-4b among "13 lower-value rules," but `subtraction-pass-notes.md`'s Critical and Major disposition tables (10 + 10 entries) contain **no RT-007 entry at all** — the pass's own completeness bar ("no Critical left without a disposition") is not met for this finding | 6 | 8 | 7 | 336 | Critical | Add an explicit RT-007 disposition row (CLOSED-BY-DELETION + residual, or REBUTTED) to `subtraction-pass-notes.md`, mirroring the treatment given to every other closed finding | Traceability |
| FM-006-20260705T-i6 | Migration-Plan Tracking | The Migration-Plan table retains a "Gating?" column with Yes/No/"Enhancement" values inherited from the deleted two-tier ratification-gate model; since ratification (M-1) is now unconditionally DONE and decoupled from all other rows, no text defines what a bare "Yes" (e.g. M-3, M-4, M-8, M-9, M-12, M-13, M-14) now gates | 3 | 5 | 4 | 60 | Minor | Add one sentence defining "Gating" post-ratification (e.g., "gates this ADR's own eventual Path-2 self-promotion, M-9") or rename the column | Actionability |
| FM-007-20260705T-i6 | 5-Rule Lint (Traceability) | Retained lint rule IDs (L-1, L-2, L-3, L-4, L-7) skip L-5/L-6 with no footnote in either deliverable explaining the numbering gap is inherited from the pre-subtraction 18-rule scheme | 2 | 6 | 4 | 48 | Minor | Add a one-line note: "L-5/L-6 retired in the subtraction pass; numbering preserved for changelog traceability" | Traceability |
| FM-008-20260705T-i6 | Frontmatter (dual mechanism) | The coexisting YAML `---` block (lint-parsed) and blockquote header (`jerry ast`-parsed) have no cross-consistency check (R-8, already disclosed); confirmed still true and still unowned in the slimmed package | 4 | 4 | 3 | 48 | Minor | No new mechanism needed; add a one-line reviewer checklist item at PR time (matches the M-9 checklist idea in FM-010) | Internal Consistency |
| FM-009-20260705T-i6 | Amend / Cross-Reference | R-B (citation staleness) and R-C (in-place amendment mutation) are disclosed as SHOULD-NOT-backed residuals, but neither has a named owner or review cadence (contrast M-5b, which at least names an owner and "per-ADR-creation" cadence for taxonomy) | 5 | 6 | 5 | 150 | Major | Assign R-B/R-C a review owner and cadence (even "governance, reviewed at each promotion") so the disclosure is actionable, not just honest | Actionability |
| FM-010-20260705T-i6 | Promotion Path 2 (M-9 self-promotion) | M-9's atomicity enforcement is described as "a review checklist item on the promoting PR," but no `.github/PULL_REQUEST_TEMPLATE.md` (or any file) exists to carry that checklist item — Glob-verified absent | 5 | 6 | 6 | 180 | Major | Either create the PR template checklist item now (a document-only, zero-machinery fix) or downgrade the claim to "intended, not yet instrumented" | Actionability |
| FM-011-20260705T-i6 | Supersede | No rule (in the 5-rule core or in prose) prevents a supersession cycle (A supersedes B, B supersedes A) or two ADRs both claiming `superseded_by` the same terminal target; Status Vocabulary states terminal states "do not transition further" but nothing checks this structurally | 4 | 3 | 6 | 72 | Minor | Note the gap as an inherent residual alongside R-A/R-B/R-C, or add a one-line SHOULD-NOT clause to Amend vs Supersede | Methodological Rigor |
| FM-012-20260705T-i6 | Migration-Plan / H-32 Parity | Zero worktracker Task entities exist under `projects/PROJ-031-cowork-skeleton/work/` for any of the 14 Migration-Plan rows (verified 2026-07-05, unchanged since the ADR's own P-022 disclosure); 3 rows (M-6, M-12, M-13) explicitly require "+ GH Issue (H-32)" and none is confirmed to exist | 5 | 7 | 4 | 140 | Major | Open the worktracker Tasks (and matching GH Issues per H-32) for at least the 3 explicitly-flagged rows before treating the ADR as fully actioned | Traceability |

**Finding ID Format:** `FM-{NNN}-20260705T-i6` (iteration-6 execution marker).

---

## Finding Details (Critical and Major)

### FM-001 — Dangling "New-Project-Onboarding section" cross-reference

- **Element:** Onboarding
- **Failure Mode:** Missing + Inconsistent (two of the 5 FMEA lenses)
- **Evidence:** `decisions/ADR-PROJ031-004-adr-identifier-convention.md:516` (Migration Plan, row M-14): *"Paired with the New-Project-Onboarding section added to Deliverable 2."* Changelog v1.2 (`:738`) and v1.3 (`:739`) both narrate adding this section. `Grep` over `design/adr-standards-rule-draft.md` for `Onboarding|onboarding` returns **zero matches**; the rule draft's own 14-entry nav table (`:11-28`) lists no such section.
- **Effect:** A reader following M-14's own pointer, or a new-project author looking for onboarding guidance in the rule draft, hits a dead cross-reference — precisely the citation-integrity failure class this ADR exists to prevent, now self-inflicted by the subtraction pass. The subtraction-pass-notes' own verification step (`subtraction-pass-notes.md:145`, "grep over the ADR body... returns zero live references to any deleted rule or to the waiver/CODEOWNERS/two-tier machinery") explicitly checked for stale references to deleted *rules/machinery* but not for stale references to a deleted *section*, so this gap escaped its own closing verification.
- **S/O/D rationale:** S=7 (a direct, confirmed self-referential dead link in a document whose central thesis is citation integrity); O=9 (already present, confirmed by Grep, not hypothetical); D=8 (survived the subtraction pass's own targeted verification and 5 prior iterations).
- **Corrective Action:** Either (a) restore a short "New-Project Onboarding" section in the rule draft (a document-only addition, not new machinery — it can be as brief as "declare `scope:` at authoring time; pick canonical over dialect under uncertainty; see Canonical Location Model for your topology"), or (b) edit M-14 and the two changelog rows to stop asserting the section exists.
- **Acceptance Criteria:** `Grep -i onboarding` over the rule draft returns a match if (a) is chosen, or the ADR no longer asserts the section's existence if (b) is chosen.
- **Post-Correction RPN estimate:** ~30 (S=5, O=2, D=3) once either fix lands.

### FM-002 — Entity-embedded dialect ADR structurally excluded from the lint's scan scope

- **Element:** ID Grammar & Lint Scan Scope
- **Failure Mode:** Insufficient (scan scope narrower than the location model it is meant to enforce) + Inconsistent (contradicts the grandfather-regression claim)
- **Evidence:** Both `decisions/ADR-PROJ031-004...md:648` and `design/adr-standards-rule-draft.md:171` state L-1's scope as `` `projects/*/decisions/`, `docs/design/` ``. The Canonical Location Model table (ADR `:372-384`) legitimizes a fourth home, `` projects/.../work/.../{ENTITY}/ `` ("Entity-embedded (permitted)"). `Glob "**/ADR-STORY015-001*.md"` resolves to `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` — no `decisions/` segment anywhere in the path. The rule draft's own count (`:94`, "Grandfathered dialect families... `STORY015`×1... The 16-file dialect corpus + 3 canonical `docs/design/` ADRs (19 total) must all pass the lint's grandfather regression test before it ships") explicitly includes this file in the 16/19 that must "pass L-1" — but L-1's own stated `find`-style scan path would never enumerate it.
- **Effect:** The one currently-cited, real, framework-relevant entity-embedded ADR in the corpus is invisible to grammar (L-1), duplicate-ID (L-3), and location (L-4) checking, both today (as guidance) and once M-6 ships (as CI). The grandfather-regression test as specified cannot actually be green against its own stated 19-file target, because 1 of the 19 is unreachable by the described file glob.
- **S/O/D rationale:** S=8 (undermines the core enforcement claim for a real, SSOT-cited file, not a hypothetical); O=9 (the exclusion is already true today, verified); D=8 (missed across 5 prior iterations and the subtraction pass's own corpus-count reconciliation work).
- **Corrective Action:** Extend the L-1/L-3/L-4 scan-path spec to include entity-embedded dialect ADRs (a glob pattern keyed on the closed `{PROJ|EPIC|FEAT|STORY}\d{3}` prefix set already defined for the dialect grammar), or explicitly narrow the "16 live dialect files... must pass L-1" claim to 15, disclosing STORY015 as an out-of-scan residual.
- **Acceptance Criteria:** The grandfather-regression test's file-discovery step actually enumerates all 19 named files (verifiable by running the stated `find` command and diffing against the 19-file list), or the claim is corrected to match what the command actually finds.
- **Post-Correction RPN estimate:** ~48 (S=6, O=2, D=4) once the scan-path spec or the claim is corrected.

### FM-005 — RT-007 finding has no disposition record after its supporting control was deleted

- **Element:** Migration-Plan / Disposition Tracking (spans the "5-rule lint" and "promote" elements)
- **Failure Mode:** Missing (a disposition entry that the pass's own methodology requires)
- **Evidence:** ADR Changelog v1.5 (`decisions/ADR-PROJ031-004...md:741`): *"new FAIL rule **L-4b** lint-rejects the dialect under repository-based topology"* attributed to finding **RT-007**. `subtraction-pass-notes.md:56` lists `L-4b` among "13 of 18 lint rules" deleted in the subtraction pass, closing findings "IN-013-005, RT-001, FM-001, FM-002, FM-005, FM-006, FM-004" — **RT-007 is not among them**. The notes' Critical Findings Disposition table (10 rows, `:82-93`) and Major Findings Disposition table (10 rows, `:104-114`) were each checked for an RT-007 entry — neither contains one.
- **Effect:** The subtraction pass explicitly states its own completeness bar as "Per mandate: no Critical left without a disposition" (`subtraction-pass-notes.md:80`). RT-007's sole supporting control was deleted in the very same pass that makes this promise, yet RT-007 itself was never re-dispositioned (closed, rebutted, or named as a residual). This is a process-integrity gap in the disclosure mechanism itself — not a demand that L-4b be rebuilt, but a demand that its removal be accounted for with the same rigor given to every other deleted control.
- **S/O/D rationale:** S=6 (a broken promise about disposition completeness, in a document whose entire value proposition is honest, complete disclosure); O=8 (already true — confirmed by checking both disposition tables); D=7 (requires cross-referencing the ADR's own changelog history against the notes file to catch; the notes' internal "verification" step did not perform this cross-check).
- **Corrective Action:** Add an RT-007 row to `subtraction-pass-notes.md`'s Major (or Critical) Findings Disposition table, e.g. "RT-007 | S-001 | CLOSED-BY-DELETION | L-4b (its sole supporting control) is deleted with the 13-rule cull; residual unmitigated SHOULD-NOT guidance for repository-based dialect misuse, named as [new residual]."
- **Acceptance Criteria:** `Grep RT-007` over `subtraction-pass-notes.md` returns a disposition entry.
- **Post-Correction RPN estimate:** ~40 (S=4, O=2, D=5) once logged.

### FM-003 — L-7 verifies only 3 of 6 frontmatter relationship fields

- **Element:** Cross-Reference / Supersede / Amend
- **Failure Mode:** Insufficient
- **Evidence:** Both L5-lint specs (ADR `:652`; rule draft `:175`) define L-7 identically: *"`superseded_by`/`promoted_to`/`promoted_from` targets resolve to an existing ADR."* The Frontmatter Schema (ADR `:338-358`; rule draft `:100-117`) defines six relationship fields: `supersedes`, `superseded_by`, `amends`, `amended_by`, `promoted_from`, `promoted_to`. `supersedes`, `amends`, and `amended_by` are absent from L-7's checked-field list in both documents.
- **Effect:** A newly authored ADR can declare `supersedes: [ADR-nonexistent-999]` or a stale `amends`/`amended_by` value and no lint — today or after M-6 ships — will catch it. This is asymmetric exactly on the "Supersede" and "Amend" lifecycle mechanisms this FMEA was asked to examine.
- **S/O/D rationale:** S=6 (moderate: only the forward-authoring direction is unchecked; the tombstoned/superseded side, which is where the historically-demonstrated PROJ-007 failure occurred, is still checked via `superseded_by`); O=5 (plausible hand-typed-ID error, not yet observed); D=6 (not disclosed as a residual anywhere; requires a field-by-field diff of the schema against L-7 to notice).
- **Corrective Action:** Extend L-7 to all 6 relationship fields (a one-line spec change, not new machinery — the check pattern is identical), or explicitly disclose the 3-of-6 asymmetry alongside R-A/R-B/R-C.
- **Acceptance Criteria:** L-7's stated field list matches the Frontmatter Schema's full relationship-field set, or the omission is named.
- **Post-Correction RPN estimate:** ~40.

### FM-009 — R-B/R-C residuals have no named owner or cadence

- **Element:** Amend / Cross-Reference
- **Failure Mode:** Insufficient (disclosure present, but not actionable)
- **Evidence:** R-B (citation staleness, ADR `:655`) and R-C (in-place amendment mutation, ADR `:581`) are both framed as "SHOULD-NOT guidance... not backed by a mechanism," with a suggested "manual `grep`/`gh issue list` sweep" — but no row in the Migration Plan assigns an owner or a recurrence cadence to actually running that sweep. Contrast M-5b (taxonomy coherence), which explicitly names an owner ("governance") and cadence ("per-ADR-creation") for its equivalent manual, non-lint check.
- **Effect:** Two of the three named [INHERENT] residuals (R-B, R-C) are honestly disclosed as *existing* but not operationalized as *checked-somehow*; without an owner/cadence they are indistinguishable in practice from an unstated residual, despite the prose disclosure.
- **S/O/D rationale:** S=5, O=6 (both residuals are permanent by design, not one-time), D=5.
- **Corrective Action:** Add "owner: governance; cadence: at each Path-1/Path-2 promotion" (or similar) to R-B and R-C's table rows, mirroring M-5b's pattern.
- **Post-Correction RPN estimate:** ~40.

### FM-010 — M-9's "review checklist" cites no actual PR-template artifact

- **Element:** Promotion Path 2 (self-promotion)
- **Failure Mode:** Missing
- **Evidence:** Migration Plan row M-9 (ADR `:511`): *"a review checklist item on the promoting PR"* is the stated atomicity-enforcement mechanism for the reciprocal M-2/M-9 link repair. `Glob ".github/PULL_REQUEST_TEMPLATE*"` returns **no files** — there is no PR template in the repository to carry this checklist item.
- **Effect:** The claimed close-condition ("M-9 cannot be marked closed until M-2's reciprocal edit is verified present in the same PR diff") has no artifact enforcing it; it is currently pure prose intent, one step short of the "checkable close-condition" the finding (FM-004, iter-4) was meant to produce.
- **S/O/D rationale:** S=5, O=6 (the gap is already true, and M-9 has not yet executed so the checklist has never been exercised), D=6 (easy to overlook since the prose reads as if the mechanism already exists).
- **Corrective Action:** Either create `.github/PULL_REQUEST_TEMPLATE.md` with the checklist item now (small, document-only, zero new lint), or reword M-9 to "intended reviewer checklist item (not yet instrumented in a PR template)."
- **Post-Correction RPN estimate:** ~36.

### FM-012 — Zero worktracker Tasks / unconfirmed GH Issues across the entire Migration Plan

- **Element:** Migration-Plan / H-32 Parity
- **Failure Mode:** Missing
- **Evidence:** `Glob "projects/PROJ-031-cowork-skeleton/work/**"` returns 23 files, none referencing the ADR-convention Migration Plan (all are EPIC-001 skeleton-distribution work items). The ADR's own Claim-Status note (`:497`) states this was true as of 2026-07-05 ("zero worktracker Task entities and zero GitHub Issues exist for any Migration-Plan row"); re-verified unchanged in this review, same date. Rows M-6, M-12, and M-13 explicitly require "+ GH Issue (H-32)."
- **Effect:** The ADR is `ACCEPTED` and its own Migration Plan is described as "the post-ratification execution plan," but H-32 (GitHub Issue parity for jerry-repo work items) is unsatisfied for the three rows that name it, with no target date attached to opening them.
- **S/O/D rationale:** S=5, O=7 (confirmed, unchanged since ratification), D=4 (already disclosed by the ADR itself, so moderately easy to detect — this is a "the disclosure is honest but the gap persists past its own stated point of urgency" finding, not a hidden one).
- **Corrective Action:** Open worktracker Task entities + matching GH Issues for M-6, M-12, and M-13 at minimum before treating the ratified ADR as under active execution.
- **Post-Correction RPN estimate:** ~20 once opened.

### FM-004 — PROJ-014 dialect characterization inconsistency

- **Element:** Companion-Document Consistency
- **Failure Mode:** Inconsistent
- **Evidence:** Rule draft `:94`: *"**Grandfathered** dialect families (...) and **PROJ-014 drafts** remain valid in place, extendable within their dialect."* ADR Migration Plan (`:488`): PROJ-014's bare `ADR-001..004` are "Transient, colliding with `docs/adrs/`" with action "Low priority; rename... only if promoted" — and D-4/L-2 (both documents) classify bare `ADR-NNN` numbering as the deprecated Scheme-E collision source, not a "dialect."
- **Effect:** A reader of the rule draft alone would conclude PROJ-014's bare-numbered files are a legitimate, extendable dialect class; a reader of the ADR's Migration Plan would conclude the opposite (transient, collision-prone, to be renamed if it ever matters). The two companion documents disagree on the status of the same named file set.
- **S/O/D rationale:** S=4, O=6, D=6.
- **Corrective Action:** Reword the rule-draft sentence to separate "grandfathered canonical/dialect families" from "PROJ-014 bare drafts (transient, not a recognized dialect; low-priority rename if promoted)."
- **Post-Correction RPN estimate:** ~40.

---

## Recommendations

**Critical (fix before acceptance):**
1. FM-002 — Correct the lint's scan-scope claim vs. the grandfather-regression file count (STORY015 blind spot).
2. FM-005 — Add RT-007's missing disposition entry to `subtraction-pass-notes.md`.
3. FM-001 — Resolve the dangling "New-Project-Onboarding section" cross-reference (add the section, or stop citing it).

**Major (recommended before acceptance, targeted document edits only):**
4. FM-003 — Extend L-7 to all 6 relationship fields, or disclose the 3-of-6 asymmetry.
5. FM-010 — Back the M-9 "review checklist" with an actual PR-template artifact, or downgrade the claim.
6. FM-012 — Open the H-32-flagged worktracker Tasks/GH Issues for M-6/M-12/M-13.
7. FM-009 — Assign owner + cadence to R-B/R-C.
8. FM-004 — Reconcile the PROJ-014 characterization between the two documents.

**Minor (improvement opportunities, optional):**
9. FM-006 — Define what "Gating?" means post-ratification.
10. FM-007 — Footnote the L-5/L-6 numbering gap.
11. FM-008 — Add a PR checklist line for YAML/blockquote frontmatter sync.
12. FM-011 — Note the supersession-cycle gap as a residual.

None of the above requires re-introducing the waiver ledger, the 18-rule lint, the CODEOWNERS gate, the two-tier ratification gate, or a producer-drift monitor. All are document-only edits (prose corrections, one schema-field extension, one small artifact file, or worktracker/GH-Issue bookkeeping) consistent with the subtraction doctrine's own stated mechanism ("the standard MEDIUM mechanism... no ledger, no CODEOWNERS gate, no enum").

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001 (dangling onboarding reference), FM-002 (entity-embedded scan gap) both represent gaps between what the package claims to cover and what it actually covers |
| Internal Consistency | 0.20 | Negative | FM-001 (M-14 vs. rule draft), FM-004 (PROJ-014 characterization) are direct disagreements between/within the companion documents |
| Methodological Rigor | 0.20 | Negative | FM-002 (grandfather-regression claim unreachable by its own stated method), FM-003 (asymmetric relationship-field checking), FM-011 (no supersession-cycle guard) |
| Evidence Quality | 0.15 | Neutral | Every retained claim checked against the live filesystem (STORY015 path, PR-template absence, worktracker Task absence) was independently reproducible; no fabricated-evidence findings surfaced |
| Actionability | 0.15 | Negative | FM-009 (residuals lack owner/cadence), FM-010 (checklist without artifact), FM-006 (undefined "Gating?" semantics) all reduce the package's operational actionability despite honest disclosure |
| Traceability | 0.10 | Negative | FM-005 (RT-007 missing disposition) is a direct traceability break in the subtraction pass's own accounting; FM-012 (H-32 parity) is an open traceability gap between the ratified ADR and the worktracker |

---

## Execution Statistics
- **Total Findings:** 12
- **Critical:** 3 — FM-001, FM-002, FM-005
- **Major:** 5 — FM-003, FM-004, FM-009, FM-010, FM-012
- **Minor:** 4 — FM-006, FM-007, FM-008, FM-011
- **Total RPN:** 2,438 (sum of the Findings Table RPN column)
- **Protocol Steps Completed:** 5 of 5 (Decompose, Enumerate, Rate, Prioritize, Synthesize)
