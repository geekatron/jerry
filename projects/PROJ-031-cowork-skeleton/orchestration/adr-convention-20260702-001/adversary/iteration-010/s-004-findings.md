# Pre-Mortem Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10 as tagged in the invoking prompt; changelog inspected through the live v1.11 row) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004 execution, iteration 10)
**H-16 Compliance:** Not independently re-run this session (blind protocol excludes iteration-009/010 folders). The deliverable's own text asserts embedded S-003 Steelman coverage for every Option A-F (`ADR-PROJ031-004-adr-identifier-convention.md:67`, tags `ST-001`/`ST-002`) and the package has been through 8 prior tournament rounds. Treated as satisfied by inference from the deliverable's own disclosure, not independently verified — labeled per P-022.
**Failure Scenario:** It is 2027-07-06. The convention was adopted as guidance twelve months ago. No new machinery was ever added (correctly, per the subtraction doctrine) — but two paths that the package neither prevents nor discloses have quietly done real damage: (1) a deleted ADR file's retired number got reused by an unrelated decision, and a reader followed a year-old citation straight into the wrong decision with no error, no broken link, nothing to signal the mistake; (2) the lint (M-6) finally shipped, but its grandfather baseline was reconstructed from current-state-at-build-time rather than the ratification-time snapshot the design calls for, because no one ever captured that snapshot as an artifact — so the "18-file regression test" everyone pointed to as proof of non-regression was quietly checking the wrong set.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence, analysis, mitigation per finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Summary

This package has already absorbed 8 prior adversarial tournament rounds and dispositioned 17 numbered Risks (R-1..R-17) plus 3 lettered residuals (R-A/R-B/R-C) with a documented, verifiable disposition trail. Re-running Pre-Mortem against that corpus, the overwhelming majority of plausible failure paths are already either mitigated or honestly disclosed — this is the most thoroughly self-audited deliverable pair this reviewer has seen in this tournament. Applying the "declare failure, work backward" method against the specific lens of *paths neither prevented nor disclosed*, one **Critical** and one **Major** gap survive that meet that bar; a third **Minor** is noted for completeness. The Critical directly threatens the standard's own headline value proposition (permanent, citation-stable identity) via a mechanism the registry-free design (c-006) cannot detect in principle. Recommendation: **ACCEPT with targeted mitigation** — both substantive findings are disclosure-only fixes consistent with the package's own subtraction doctrine (no new lint rule required for 004-001; a one-line Migration-Plan action item for 004-002), not blockers to the ratified guidance's continued validity.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| 004-001-iter010 | Deleting a canonical/dialect ADR file silently frees its `NNN` for reuse by an unrelated future decision; L-3 and the pre-flight one-liner only diff *currently-existing* files and cannot detect this by design (c-006 forbids a registry) | Technical / Assumption | Medium | Critical | P0 | Internal Consistency, Completeness |
| 004-002-iter010 | The ratification-anchored grandfather baseline (fixed at 2026-07-05/06 per the iteration-9 fix) has no captured artifact (file, tag, or commit reference) — only a prose count — so it cannot actually be reconstructed correctly whenever M-6 is eventually built | Process | Medium-High | Major | P1 | Methodological Rigor, Actionability |
| 004-003-iter010 | The two-clause pre-flight/L-3 scan's `docs/design/ADR-*.md` clause only reaches files directly inside `docs/design/`, not any subdirectory, though the Location Model does not prohibit subdirectories there | Technical | Low | Minor | P2 | Traceability |

---

## Finding Details

### 004-001-iter010: Deletion of an ADR file silently frees its number for reuse, misdirecting old citations to an unrelated decision [CRITICAL]

**Failure Cause:** The convention's entire registry-free design (c-006, `ADR-PROJ031-004-adr-identifier-convention.md:128`: "MUST be deterministically lint-able without a central registry or global counter") makes uniqueness detection a function of *currently-existing files only*. D-1 asserts `NNN` is "a 3-digit, zero-padded, **never-reused** sequence within that domain slug" (`ADR-PROJ031-004-adr-identifier-convention.md:217`), and the companion rule draft repeats this as ADR-M-005: "`NNN` SHOULD be 3-digit, zero-padded, monotonic within its namespace, **never reused** — reversal is by supersession, not renumbering" (`adr-standards-rule-draft.md:50`). The *only* enforcement mechanism for "never reused" is L-3 (`sort | uniq -d` over the currently-scanned corpus, `adr-standards-rule-draft.md:177`; ADR `:688`), which is structurally incapable of remembering an ID that is no longer present in the working tree — there is no append-only history of retired IDs, by explicit design (c-006). If any canonical or dialect ADR file is ever **deleted** (as opposed to superseded-in-place, which keeps the file and only flips `status`), its `NNN` silently becomes available, and nothing — not L-1, L-2, L-3, L-4, or L-7, all of which the ADR and rule draft describe exhaustively — would catch a later, unrelated author minting the same `{slug}-NNN` again. This is worse in kind than a stale citation (which at least 404s visibly): a citation written against the deleted ADR's ID (e.g., "see `ADR-agent-design-003` for why we rejected X") would, after reuse, silently resolve to a **different, unrelated, currently-valid** decision with zero error signal.

**Category:** Technical (no structural detection mechanism exists) / Assumption (the "never reused" claim silently assumes files are never removed, a premise never stated or defended anywhere in either document).

**Likelihood:** Medium — justified by three concrete facts, not speculation: (1) `Status Vocabulary` (`ADR-PROJ031-004-adr-identifier-convention.md:622-649`) defines `REJECTED` ("considered and declined") with no guidance on whether a rejected proposal's file is retained or cleaned up; (2) `Amend vs Supersede Conventions` (`:602-614`) states "Numbers are never reused" as a bare rule-of-thumb (line 612) with **no discussion of file deletion at all** — contrast this with the document's otherwise exhaustive habit of naming every other lifecycle edge case (17 numbered Risks, 3 lettered residuals); (3) this very project's own governing doctrine for the last 5 iterations has been "close findings by **deleting** the exposing claim/mechanism" (`subtraction-pass-notes.md:27`) — a repo culture that has just spent five iterations demonstrating, in this very project, that deleting files/sections to fix problems is the normal, encouraged remediation style. A future maintainer applying that same instinct to a `REJECTED` or otherwise "no-longer-useful" ADR file is not a far-fetched scenario in this specific repository's culture; it is the house style.

**Severity:** Critical — this defeats the standard's own headline selling point. The Decision section's central claim is that Scheme B's value is permanent, promotion-proof, **citation-stable** identity (D-2: "Promotion from the former to the latter is `git mv` with no ID change and no citation churn. This is the decisive property..." `ADR-PROJ031-004-adr-identifier-convention.md:219`; Positive Consequence 1, `:440`, "zero breakage for the bare-ID citation majority"). A silently-reused ID after deletion does not just fail to prevent citation breakage — it actively **misdirects** a citation to wrong content with no detectable symptom, which is categorically worse than the citation-staleness residual the document already discloses (R-B) and directly undermines "collision-free ADR identity" as stated in this review's charge.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:217` (D-1, "never-reused"), `:128` (c-006, no registry), `:602-614` (Amend vs Supersede — no deletion policy), `:622-649` (Status Vocabulary — no deletion-related state or guidance), `:688` (L-3 spec, diffs existing files only), `:461-482` (Risks register R-1..R-17 — none address post-deletion reuse); `adr-standards-rule-draft.md:50` (ADR-M-005), `:177` (L-3 spec), `:92-95` (Frozen and Grandfathered Legacy — addresses *new files in frozen dirs*, not deletion of existing canonical/dialect files, a distinct scenario).

**Dimension:** Internal Consistency (a flat "never reused" normative claim with zero enforcement path or caveat, inconsistent with the document's otherwise scrupulous practice of labeling every unenforced claim as [INHERENT]/[DISCLOSED]) and Completeness (the 17-item Risks register is exhaustive on every other lifecycle transition — creation races (R-6), supersession races (R-17), frozen-dir new-entries (R-14) — but is silent on file removal entirely).

**Mitigation:** No new lint rule required (consistent with the subtraction doctrine — this is a disclosure gap, not a machinery gap). Add: (a) one SHOULD-NOT guidance line to `Amend vs Supersede Conventions` / ADR-M-009: "An ADR file, once canonical, SHOULD NOT be deleted — only tombstoned (`SUPERSEDED`/`REJECTED`/`DEPRECATED`) or grandfathered in place; deletion silently frees its `NNN` for reuse with no lint able to detect the reuse (c-006 precludes a registry)." (b) Register a new Risk (next available `R-18`) naming this exact failure mode, its likelihood, and that it is [INHERENT] to the registry-free design — mirroring the rigor already applied to R-6/R-7/R-17.

**Acceptance Criteria:** A disclosed SHOULD-NOT-delete guidance line exists in both deliverables' Amend/Supersede sections, and a numbered Risk entry documents the residual (no lint required to close this finding — disclosure is sufficient per the package's own established remediation pattern for INHERENT gaps).

---

### 004-002-iter010: The ratification-anchored grandfather baseline has no captured artifact, so the fix it depends on cannot actually be implemented when M-6 ships [MAJOR]

**Failure Cause:** Iteration-9's 012-003 fix re-anchored the grandfather baseline from "when the lint ships" to "**convention-ratification time (2026-07-05/06)**" specifically to prevent a growing post-ratification amnesty window (`ADR-PROJ031-004-adr-identifier-convention.md:693`; rule draft `:183`). This is the *right* fix in principle — but neither deliverable, nor the Migration Plan's M-6 row (`ADR-PROJ031-004-adr-identifier-convention.md:541`), commits to **capturing that baseline as a concrete artifact now**, at ratification time. The baseline is described only as a prose reconciliation (16 whole-dialect-corpus / 15 reachable / 3 canonical / 18 regression-corpus, D-4) — not as a committed file, git tag, or pinned commit SHA. M-6 itself does not exist (`scripts/lint_adr_convention.py` is Glob-verified absent) and carries no committed ship date; the document's own Pre-Mortem row FM-5 rates "nothing lands" as "the single best-evidenced risk in this package" (`:501`). If M-6 is implemented at some indeterminate future date — after further legitimate dialect ADRs have been minted in the interim (permitted, expected, and encouraged by D-3) and, per the still-open M-12, potentially after the unfixed producing agent (`ps-architect.md`) has continued emitting non-canonical IDs into that same gap — the person implementing M-6 has no artifact to anchor "ratification time" to. They must either (a) do ad hoc git archaeology to reconstruct the exact 2026-07-05/06 file-state (an action not scoped anywhere in M-6's task description), or (b) compute the baseline against current-state-at-build-time, which silently re-introduces the exact "growing amnesty window" defect that 012-003 was supposed to have closed.

**Category:** Process (a design fix specified in prose without a corresponding operational artifact or action item to make it executable later).

**Likelihood:** Medium-High — M-6 has no committed date, M-12 (producer fix) is also untracked, and this is now the third consecutive iteration where the grandfather-baseline framing has needed correction (iter-8's FM-001-i8 count reconciliation, iter-8's IN-001 baseline-clause addition, iter-9's 012-003 temporal re-anchor) — a pattern of the baseline logic being fixed on paper each time without ever being operationalized as data.

**Severity:** Major — this does not invalidate the guidance (which the document correctly and repeatedly states stands on its own with zero tooling), but it does mean the enforcement mechanism, whenever built, risks being **built wrong** in a way that is only discoverable after the fact — either wrongly grandfathering post-ratification non-compliant IDs (undermining bare-ID deprecation) or wrongly flagging legitimate pre-existing dialect files as new violations. This affects "adoptable MEDIUM-tier convention" specifically at the point the convention transitions from guidance-only to lint-backed.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:693` (ratification-anchor clause, no artifact named), `:541` (M-6 row — "TBD-Task + GH Issue," no baseline-capture sub-item), `:501` (FM-5, "nothing lands" risk, corroborating the unbounded-gap premise), `:789` (changelog v1.11 row narrating the 012-003 fix as text-only); `adr-standards-rule-draft.md:183` (identical prose-only baseline clause).

**Dimension:** Methodological Rigor (a fix specified as intent without a mechanism to realize that intent later) and Actionability (M-6's task row is not actionable as written for this specific sub-requirement — an implementer would have no data to consume).

**Mitigation:** Add one Migration Plan action item (or a sub-bullet under M-6): "Capture the ratification-time grandfather baseline **now** as a committed data file (e.g., `scripts/adr-grandfather-baseline-20260705.txt`, one path per line, generated by the two-clause `find` already specified) or, at minimum, record the exact commit SHA as of 2026-07-05/06 ratification in this ADR's Changelog, so M-6's eventual implementer has a concrete artifact rather than a prose count to anchor to." This is a zero-machinery, disclosure-plus-one-file fix consistent with the subtraction doctrine — it captures data, not a new rule.

**Acceptance Criteria:** Either a committed baseline-list file exists in the repo, or the exact ratification-time commit SHA is recorded in the ADR Changelog/Migration Plan, such that a future M-6 implementation does not need to reconstruct "what existed at ratification" from git archaeology.

---

### 004-003-iter010: The `docs/design/` scan clause does not reach nested subdirectories [MINOR]

**Failure Cause:** The two-clause pre-flight/L-3 command's second clause, `-path '*docs/design/ADR-*.md'` (`ADR-PROJ031-004-adr-identifier-convention.md:405-421`; identical in `adr-standards-rule-draft.md:188-204`), only matches files whose path literally contains the contiguous substring `docs/design/ADR-...md` — i.e., files directly inside `docs/design/`. A file placed in a subdirectory (e.g., `docs/design/some-domain/ADR-foo-001.md`) would not match this clause (nor the `*/decisions/*` clause, since there is no `decisions/` segment), and would silently fall outside the L-3 collision scan and the grandfather regression test. The Canonical Location Model table (`:382-393`) does not prohibit subdirectories under `docs/design/`, so this is a live (if currently unexercised) gap.

**Category:** Technical.

**Likelihood:** Low — no such subdirectory structure exists in the corpus today (verified: the 3 canonical ADRs sit flat in `docs/design/`), and the convention's own guidance (`docs/design/README.md` as a flat index, M-5) implies a flat model is intended.

**Severity:** Minor — a quality/completeness gap in the scan command's robustness, not a currently-active collision risk.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:405-421`, `:386-393`; `adr-standards-rule-draft.md:188-204`.

**Dimension:** Traceability (the scan command's documented scope silently narrower than the Location Model's stated scope).

**Mitigation:** Note in the Location Model or the scan command's inline comments that `docs/design/` is expected to remain flat (no subdirectories), or widen the second clause to `-path '*docs/design/*/ADR-*.md' -o -path '*docs/design/ADR-*.md'` if subdirectories are ever introduced. Not gating.

**Acceptance Criteria:** A one-line comment disclosing the flat-only assumption, or a widened glob if/when subdirectories are introduced.

---

## Recommendations

**P0 (MUST mitigate before acceptance of the ENFORCEMENT claim; does not block the GUIDANCE, which stands on its own per the package's own repeated framing):**
- 004-001-iter010: Add SHOULD-NOT-delete guidance to Amend-vs-Supersede/ADR-M-009 in both deliverables, and register the residual as a new numbered Risk (`R-18`) in the parent ADR's Risks register, naming the failure mode explicitly (deletion → NNN reuse → silent citation misdirection) as [INHERENT] to the registry-free design (c-006).

**P1 (SHOULD mitigate):**
- 004-002-iter010: Add a Migration Plan sub-action (under or adjacent to M-6) to capture the ratification-time grandfather baseline as a committed artifact (file or recorded commit SHA) now, rather than leaving the baseline as a prose count to be reconstructed whenever M-6 is eventually implemented.

**P2 (MAY mitigate; acknowledge risk):**
- 004-003-iter010: Disclose the flat-only assumption for `docs/design/` in the scan command's comments, or widen the glob if subdirectories are ever introduced.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | 004-001-iter010: the otherwise-exhaustive 17-item Risks register has no entry for post-deletion ID reuse, a materially different failure class from the already-disclosed creation-race (R-6) and supersession-race (R-17) residuals |
| Internal Consistency | 0.20 | Negative | 004-001-iter010: D-1's flat "never reused" (`:217`) is asserted without the [INHERENT]/[DISCLOSED] caveat the document applies consistently to every other unenforced claim elsewhere in the same document |
| Methodological Rigor | 0.20 | Negative | 004-002-iter010: a three-iteration sequence of paper-only fixes to the grandfather-baseline logic (iter-8, iter-8, iter-9) never produced the underlying artifact the fixes depend on |
| Evidence Quality | 0.15 | Neutral | Both substantive findings are grounded in direct citation to the deliverables' own stated mechanisms (c-006, L-3, M-6) rather than external speculation |
| Actionability | 0.15 | Negative | 004-002-iter010: M-6's task row is not actionable as written for the baseline-capture sub-requirement it silently depends on |
| Traceability | 0.10 | Negative | 004-003-iter010: the scan command's actual reach is narrower than the Location Model's stated scope, undocumented |

**Net assessment:** Both substantive findings are disclosure-and-one-artifact fixes, not machinery, and are consistent with — not in tension with — the package's own subtraction doctrine. Estimated composite score impact of full mitigation: +0.02 to +0.04 (closing a genuine Completeness/Internal-Consistency gap on the standard's core value proposition), insufficient alone to move the package from its current tournament trajectory but material to closing out the residual register at the same rigor already applied to R-1..R-17.

---

## Execution Statistics
- **Total Findings:** 3
- **Critical:** 1
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6 (Set the Stage, Declare Failure, Generate Failure Causes, Prioritize, Develop Mitigations, Synthesize/Score)

---

*Blind protocol observed: iteration-009 and iteration-010 sibling files were not read except this output. Prior iterations 001-008 and `subtraction-pass-notes.md` (the full R-1..R-17/R-A/R-B/R-C disposition register) were read and cross-checked to confirm neither 004-001-iter010 nor 004-002-iter010 duplicates an already-dispositioned residual. No subagents invoked (P-003). No deliverable file edited (P-020). All evidence cited by file path (repo-relative) and line number (P-022); H-16 compliance inferred from the deliverable's own embedded-steelman disclosure, labeled as inference, not independently re-verified this session.*
