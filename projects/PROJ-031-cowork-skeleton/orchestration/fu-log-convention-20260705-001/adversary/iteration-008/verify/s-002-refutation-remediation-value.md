# Refutation Panel — S-002 Findings, Remediation-Value Lens

> **Iteration:** 8 · **Lens:** remediation-value · **Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-002-findings.md`
> **Question per Critical:** would fixing it materially change adoption outcomes, or is it churn? Fixes that would ADD machinery against the anti-bloat doctrine are REFUTED. Default REFUTED if uncertain.
> **Scope:** only the 2 Criticals in the target report (DA-001-i8, DA-002-i8). Majors/Minors out of scope per assignment.

## Navigation

| Section | Purpose |
|---------|---------|
| [DA-001-i8](#da-001-i8) | Worktree/branch merge renumbering vs. external-citation durability |
| [DA-002-i8](#da-002-i8) | FM-001 dedup keyed on location only, not content |
| [Summary](#summary) | Disposition table |

---

## DA-001-i8

**Claim:** the worktree/branch merge-conflict renumbering rule (`design/feedback-decision-log-convention-design.md:79`, restated at `design/staging-feedback-logs/feedback-decision-logs-standards.md:27`) contradicts the id-durability invariant ("`next` is written once at seal time... ids never reset, so a reference survives rotation," `design/feedback-decision-log-convention-design.md:198`) for the exact case (graduated ids) that invariant exists to protect, with no repair path for citations held by artifacts *outside* the two log files (ADR `Reflected in:`, DECISION `Source:`).

**VERIFIED.** Confirmed by direct read: `design/feedback-decision-log-convention-design.md:79` states the renumbering rule repairs only "`Superseded by:` / `Related:` references **it carries**" — i.e., the renumbered entry's own outbound fields, not inbound citations held by an already-shipped ADR or worktracker DECISION. Line 198's invariant is stated unqualified at its own point of claim, with no cross-reference to the line-79 exception. The catch-all at line 79's close ("these are named residuals, not covered cases") is a generic disclaimer covering three grouped scenarios (concurrent sessions, hand-edits, worktree merges) and never names the specific external-citation-breakage consequence for graduated ids — this is precisely the "disclosure exists somewhere, not at the point of the claim" defect class the design doc's own Remediation-convergence-trigger section (`design/feedback-decision-log-convention-design.md:262`) names as the *legitimate, recurring* driver of every prior round's score decline, not a novel or manufactured gap. Git-worktree isolation is named as an actively-supported pattern at the same line (79), not a hypothetical.

**Remediation value:** Positive, not churn. The finder's own proposed fix (option b, `s-002-findings.md:77`) is a single disclosure clause added at the point of the line-198 claim — zero new id-format, zero new lint, zero new field. This is the same wording-only remediation style that closed 5 of 6 prior iteration-006 Criticals (`iteration-007/restore-notes.md` "Residuals Disclosed" table). It does not add machinery, and it closes a real internal-consistency gap on the package's central durability claim for the one class of record (graduated/ADR-cross-linked) this project treats as authoritative. Fixing it materially reduces the risk of an operator trusting a silently-broken `Reflected in:` pointer on a ratified ADR.

---

## DA-002-i8

**Claim:** the FM-001 inline-doc dedup check (`design/staging-feedback-logs/feedback-decision-logs-standards.md:51`; restated `FEEDBACK-LOG.template.md:25`; `examples-appendix.md:169`) keys on `path:line/anchor` location only, with no content comparison, so an operator's in-place edit to a marker at the same location is silently treated as an already-logged duplicate and never (re-)captured.

**VERIFIED.** Confirmed by direct read of all three cited artifacts: each states the skip condition purely as a location match ("the same `source: inline-doc` `path:line/anchor`" / "same `path:line/anchor`" / "same `source: inline-doc` path/anchor") with no marker-text comparison anywhere in any of the three restatements, and no hedge elsewhere in the package (checked `examples-appendix.md` Common Cases and the FEEDBACK-LOG.template.md inline-doc bullet) that would independently cover an edited-in-place marker. Markers are explicitly *not* removed from the source document after harvest ("no doc mutated," `examples-appendix.md:169`), so repeat reads of the same annotated document — the very scenario the dedup rule exists to handle — are the normal, expected usage pattern; an in-place text edit at that same line during one of those repeat reads (plausible for a living document, and directly analogous to this very design package's own multi-round `FU:`/`DEC:` marker use) is a real, non-hypothetical trigger, not an edge case invented for the critique.

**Remediation value:** Positive, not churn. This directly attacks the package's own governing principle ("what depends on the model remembering will eventually be forgotten," `design/feedback-decision-log-convention-design.md:38`) via a mechanism (not a memory) failure — the dedup rule as written guarantees the loss regardless of operator diligence. The finder's proposed fix — compare marker text against the existing entry's already-present **Verbatim** field, re-mint only on content mismatch — requires no new field, no new lint, no new file (the Verbatim field already exists in the entry schema at `feedback-decision-logs-standards.md:24`/`FEEDBACK-LOG.template.md:18`). This is a one-clause wording fix consistent with the same anti-bloat remediation style already used to close the *original* "no dedup" finding that FM-001 itself remediated (`iteration-007/restore-notes.md` row 5). Not fixing it leaves a deterministic, silent completeness gap on the exact purpose pillar ("feedback... never lost") the whole convention exists to satisfy.

---

## Summary

| ID | Disposition | Fix requires new machinery? | Materially affects adoption? |
|----|-------------|------------------------------|-------------------------------|
| DA-001-i8 | VERIFIED | No (disclosure clause only) | Yes — silently broken external references on authoritative/graduated artifacts |
| DA-002-i8 | VERIFIED | No (reuse existing Verbatim field) | Yes — deterministic silent loss of edited feedback, contradicts governing principle |
