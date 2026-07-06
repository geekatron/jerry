# Refutation Panel — S-001 (iteration-007, VERIFIED-CRITICALS protocol) — Materiality Lens

> Panel: adv-executor (refutation role) · Lens: **materiality** — does the finding genuinely block the convention's purpose (no lost feedback, burden-free capture, navigable growth, honest metadata)? Improbable edge cases and style points are REFUTED even if the underlying textual claim is accurate.
> Target report: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-001-findings.md`
> Scope: this panel reviewed **only** the Critical-severity finding(s) in the target report, per instructions. The target report contains exactly one Critical: **RT-001-20260706-iter7**.

## Navigation

| Section | Purpose |
|---------|---------|
| [Method](#method) | What was read/compared |
| [RT-001-20260706-iter7](#rt-001-20260706-iter7-the-one-sanctioned-edit-to-a-sealed-entry-claimed-twice) | Verdict + evidence |
| [Summary](#summary) | Final structured output |

## Method

Read the target findings report in full, the restore notes (`.../iteration-007/restore-notes.md`), and the four deliverable files the finding cites directly: `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`, `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md`, and `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/LLM-DECISION-LOG.template.md`. Every citation below was checked against the current file text at the cited line.

## RT-001-20260706-iter7: "The one sanctioned edit to a sealed entry" claimed twice

**Verdict: REFUTED (materiality).**

The textual collision is accurate as quoted: `staging-feedback-logs/feedback-decision-logs-standards.md:24` calls redaction "the **one sanctioned edit to a sealed entry**," and the same file's line 53 calls the `Superseded by:` status pointer "the one sanctioned edit to a sealed entry" — a genuine phrase collision, and the design doc's L1.1→L1.4 cross-reference (`feedback-decision-log-convention-design.md:65` → `:197`) does land on a passage naming only the status pointer. However, materiality requires more than a verified inconsistency: it requires that the inconsistency actually block one of the convention's four purposes (no lost feedback, burden-free capture, navigable growth, honest metadata). It does not. Both mechanisms are independently and unambiguously authorized by their own local instruction text regardless of the "the one" phrasing: LOG-M-002 (`feedback-decision-logs-standards.md:24`) directly instructs redacting secrets "before appending," and the Corrections bullet (`:53`) directly instructs marking the old entry `Superseded by: FU.N` on correction/reopen. Neither permission depends on, or is undercut by, the redundant emphatic phrase "the one" — a single-operator reading the rule file top-to-bottom (the convention's validated adoption profile, `feedback-decision-log-convention-design.md:101`) is told, in each local section, exactly what to do; nothing about "no lost feedback," "burden-free capture," "navigable growth," or "honest metadata" turns on whether the doc counts one or two sanctioned edit types in a summary noun phrase.

The finding's own severity argument is built on a hypothetical "compliance-literalist" adversary disputing after the fact whether a given edit was "sanctioned" — the Threat Actor Profile names this explicitly as the goal ("challenge the legitimacy of an inconvenient edit after the fact"). That is precisely the class of improbable-edge-case reasoning the materiality lens is instructed to refute even where the textual premise holds: this is a single-operator, cowork-scoped convention (not a multi-party compliance regime), both edit types are affirmatively instructed in their own sections independent of the "the one" phrase, and no operational path in the deliverable actually turns on resolving whether "the one" means one type or two. This is Internal-Consistency wording debt, not a block on the convention's stated purposes.

## Summary

- **Lens:** materiality
- **Verified:** none
- **Refuted:** RT-001-20260706-iter7
- **File:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/verify/s-001 red team analysis (iteration-007, verified-criticals protocol) executed against the fu/dec-log convention design doc + 5 staging artifacts. re-verified all 9 iteration-006 critical/major findings closed against current text (zero regression), then hunted specifically for new instances of the package's own recurring "claim contradicts an adjacent/cross-referenced disclosure" failure class.-refutation-materiality.md`
