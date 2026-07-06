# Refutation Panel: S-012 (FMEA) — Remediation-Value Lens

> Iteration-008, remediation-value lens. Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-012-findings.md`.
> Protocol: attempt to REFUTE every Critical; default REFUTED if uncertain. Test: would fixing it materially change adoption outcomes, or is it churn? Fixes that ADD machinery against the anti-bloat doctrine are REFUTED.
> Read: target report, `design/feedback-decision-log-convention-design.md`, `design/staging-feedback-logs/*`, `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md`. No other panel files read.

## Navigation

| Section | Purpose |
|---------|---------|
| [Criticals Under Review](#criticals-under-review) | The 2 Criticals from s-012-findings.md |
| [FM-001-i008fmea](#fm-001-i008fmea) | Segment-Index-overflow / lint-2 claim |
| [FM-002-i008fmea](#fm-002-i008fmea) | Inline-doc dedup key ambiguity |
| [Summary](#summary) | Verdict table |

## Criticals Under Review

Only two Criticals appear in the target report's Findings Table: **FM-001-i008fmea** (RPN 294) and **FM-002-i008fmea** (RPN 294). FM-003 and FM-004 are Major and out of scope for this Critical-only refutation pass.

## FM-001-i008fmea

**Claim:** design doc's "Five safety functions" paragraph asserts lint 2 "detects" Segment-Index-overflow, contradicting the rule file's own Scope-limits disclosure that Segment Index display accuracy is *not* checked by lint 2.

**Verification:** Confirmed by direct read. `design/feedback-decision-log-convention-design.md:264` reads: "The Segment-Index-overflow trigger is explicitly exempt from the Q3-style dated-worktracker forcing function (DA-001): unlike capture, its failure is detected by lint 2's contiguity/orphan check and is fully recoverable by re-reading segment headings, so it needs no owned review date." The overflow trigger itself is defined at `feedback-decision-log-convention-design.md:199` as an index+queue *line-overhead* threshold (~100 lines), unrelated to id sequencing. Lint 2's actual scope (`design/staging-feedback-logs/feedback-decision-logs-standards.md:82`, mirrored in the design doc at line 236) is id uniqueness/monotonicity/contiguity plus on-disk-vs-index orphan detection — it contains no logic that measures or verifies the index table's own size or its displayed-range accuracy. The rule file's own Scope-limits item (e) (`feedback-decision-logs-standards.md:85`) explicitly states Segment Index display accuracy is "not checked" by the lints. The design doc's "detected by lint 2" clause is therefore an unsupported claim about a mechanism that, by the package's own two independent scope statements, does not perform that function — a genuine internal-consistency defect, not a strained reading. A charitable alternate parse ("recoverable by re-reading headings" as the operative, true half of the sentence, with "detected by lint 2" as loose framing) does not rescue the claim: a reader skimming this governance section could reasonably conclude an automated backstop exists where none does, which is the same false-backstop pattern this exact restore round (PM-001/IN-001, `restore-notes.md` row 3) was created to eliminate elsewhere in the same paragraph.

**Remediation value:** The corrective action is a one-sentence wording fix (delete/replace the "detected by lint 2" clause) — zero new machinery, fully consistent with the anti-bloat doctrine already governing this round's other fixes. Given this document is gated for C4 ratification (0.95 threshold) and the false-backstop pattern is the package's own named recurring defect class (already fixed twice this round in the same paragraph), leaving one more instance uncorrected undermines the very doctrine the restore pass was meant to complete. This is not churn: an implementer who trusts the false claim may decline to establish any forcing function for this residual, reproducing exactly the silent-drift risk the document elsewhere works hard to avoid.

**Verdict: VERIFIED.**

## FM-002-i008fmea

**Claim:** the inline-doc dedup key (`path:line/anchor`) that closed the tournament's highest-RPN historical Critical has no defined canonical format and zero worked examples anywhere in the 6-file package.

**Verification:** Confirmed. The key is specified identically and identically vaguely in three places: design doc `feedback-decision-log-convention-design.md:61` ("append the annotation's `path:line/anchor`"), rule file `feedback-decision-logs-standards.md:51` ("the same `source: inline-doc` `path:line/anchor`"), and template `FEEDBACK-LOG.template.md:25` ("the same `source: inline-doc` path/anchor" — note this third site drops "line" entirely, reinforcing the inconsistency). None states whether the key is a raw line number (edit-sensitive) or a heading anchor (edit-stable), or both. The template's own inline comment (`FEEDBACK-LOG.template.md:53`) uses the placeholder `{line-or-anchor}` — direct evidence that even the template author left the choice open rather than fixed. `examples-appendix.md` was checked end to end: both FEEDBACK-LOG worked examples (`:45`, `:68`) use `source: chat`; the "Common cases" section (`:169`) restates the rule in prose with no concrete key value; no line anywhere in the six files shows an actual inline-doc-sourced key (e.g., `source inline-doc research/foo.md:42` or `#anchor`). This directly contradicts the package's own FU.8 doctrine (embedded worked examples for every mechanism, cited at `feedback-decision-logs-standards.md:3` and applied to every other mechanism — segment rotation, ids/aliases, evidence links, LLM-DECISION-LOG) which is not applied to this one, despite it being the fix for the tournament's single highest-RPN historical Critical (FM-001-i6, RPN 336 per `restore-notes.md` row 5).

**Remediation value:** The corrective action is picking one canonical key form and adding one worked example — no new field, lint, or subsystem, and directly satisfies the package's own pre-existing FU.8 doctrine rather than adding new doctrine. This is not churn: an unspecified key format creates real cross-session/cross-model computation-drift risk (one session recording a line number, another an anchor) under which two harvests of the same, unedited marker could fail to match and silently re-mint a duplicate — reproducing the exact defect this mechanism exists to close. Given the historical RPN of the defect this mechanism was built to fix, tightening its own specification has direct, material adoption value.

**Verdict: VERIFIED.**

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| FM-001-i008fmea | VERIFIED | Provable contradiction (file+line), one-sentence wording fix, closes the package's own named false-backstop defect class; not churn. |
| FM-002-i008fmea | VERIFIED | Provable spec ambiguity + total absence of a worked example (file+line across 4 sites), wording+one-example fix, directly serves the package's own FU.8 doctrine; not churn. |

Both Criticals in `s-012-findings.md` survive the remediation-value refutation attempt: each is evidenced with direct file+line citations that hold up under independent re-verification, and each proposed corrective action is wording/example-only — no new lint, field, file, or subsystem — consistent with the anti-bloat doctrine this deliverable is itself built on.

---

*Panel: adv-executor (S-012 refutation, remediation-value lens) | P-003: no subagents invoked | P-020: draft-only, no framework-path writes, no edits to the deliverable or the target report | P-022: all verdicts cite file+line from the current deliverable text; no other iteration-007/008 adversary panel files read except `iteration-007/restore-notes.md` per task scope.*
