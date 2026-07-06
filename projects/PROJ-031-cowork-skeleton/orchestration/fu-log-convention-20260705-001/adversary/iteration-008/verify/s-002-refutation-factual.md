# Factual-Accuracy Refutation Panel — S-002 Devil's Advocate (iteration-008)

> **Lens:** factual-accuracy (does the defect exist at the cited lines in the CURRENT files? misreadings / stale refs / restatements of already-disclosed residuals are REFUTED; default REFUTED if uncertain)
> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-002-findings.md`
> **Scope:** the 2 Critical findings only (DA-001-i8, DA-002-i8), per task instruction.
> **Method:** each cited file+line re-read against the current on-disk deliverable text; cross-checked against `iteration-007/restore-notes.md` (closed-criticals table + Residuals Disclosed table) to determine whether the finding restates an already-disclosed residual.

---

## DA-001-i8: Worktree/branch merge-conflict renumbering breaks external citations to graduated ids

**Verdict: VERIFIED**

The quoted text is accurate at both cited locations. `design/feedback-decision-log-convention-design.md:79` (the git-worktree/branch-isolated bullet) reads verbatim: "if ids collide, renumber the later-merged side to continue after the surviving maximum id and repair any `Superseded by:` / `Related:` references it carries" — confirmed on disk. `design/staging-feedback-logs/feedback-decision-logs-standards.md:27` restates the identical rule ("on conflict, keep both sides' entries in id order and **renumber** (never discard) any colliding id, repairing its `Superseded by:` / `Related:` references"). The "ids never reset" invariant is likewise accurately quoted from `design/feedback-decision-log-convention-design.md:198` ("`next` is written once at seal time — sealed segments never relink; ids never reset, so a reference survives rotation and each log's index resolves *id → file*").

This is not a restatement of an already-disclosed residual. A full-text grep of the design doc and rule file for "renumber", "Reflected in", and "external citation" (and manual review of the iteration-007 `restore-notes.md` Residuals Disclosed table, which lists exactly one accepted residual — PM-001/IN-001, the AE-006e cumulative-size gap, unrelated to this topic) turns up no disclosure that the renumbering rule's repair clause is scoped only to the renumbered entry's own outbound `Superseded by:`/`Related:` fields, and does not (and cannot) reach inbound external citations held by an already-graduated ADR's `Reflected in:` field or a worktracker DECISION's `Source:` field. The disclosed residual at line 79 ("Its failure signature is worse than live clobber... discarded side's entries vanish") covers data loss from *naive* (non-rule-following) conflict resolution; it does not cover the distinct failure this finding raises — that even the *documented, correct* renumbering procedure has no repair path for citations living outside the two log files. This is a genuinely new, non-hypothetical internal-consistency gap, accurately cited.

---

## DA-002-i8: FM-001 inline-doc dedup keys on location only, not content — edited markers silently dropped

**Verdict: VERIFIED**

All three cited quotes are accurate on the current files. `design/staging-feedback-logs/feedback-decision-logs-standards.md:51` states the dedup check keys on "the same `source: inline-doc` `path:line/anchor`" with no content comparison. `design/staging-feedback-logs/FEEDBACK-LOG.template.md:25` restates it identically ("Before minting, it checks for an existing entry with the same `source: inline-doc` path/anchor and does not re-capture a marker already logged"). `design/staging-feedback-logs/examples-appendix.md:169` restates it a third time in the Common Cases worked example ("The assistant checks for an existing entry carrying the same `source: inline-doc` path/anchor before minting; a marker already logged is not re-captured"). In all three, the skip condition is location-only; none specifies a content-match requirement before treating a re-read as a duplicate.

This is distinguishable from the already-disclosed "coverage caveat" at `design/feedback-decision-log-convention-design.md:91` (marker missed because the file is *never revisited* or is read via a partial/offset-limited Read) — that caveat is about a marker never being seen at all, whereas this finding is about a marker that *is* re-read at the same location but whose *text has changed* since the prior capture, which the location-only key silently treats as "already logged." Cross-checking `iteration-007/restore-notes.md` row 5 (FM-001, closed by "check-before-mint dedup on existing sub-field") and its Residuals Disclosed table (residual count = 1, PM-001/IN-001 only) confirms this edited-marker interaction was not identified or disclosed as an accepted residual in the prior closure round. The finding accurately identifies an undisclosed, mechanism-level completeness gap in the current shipped text.

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-i8 | VERIFIED |
| DA-002-i8 | VERIFIED |

Both Criticals cite the current deliverable text accurately, are not misreadings or stale references, and are not restatements of residuals already disclosed in the design doc, rule file, or `iteration-007/restore-notes.md`.
