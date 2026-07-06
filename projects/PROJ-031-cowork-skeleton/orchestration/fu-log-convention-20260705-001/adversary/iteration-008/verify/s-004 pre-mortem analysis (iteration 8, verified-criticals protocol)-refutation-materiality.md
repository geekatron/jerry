
# Refutation Panel — Materiality Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-004-findings.md` (S-004 Pre-Mortem Analysis, iteration 8, VERIFIED-CRITICALS protocol)
**Lens:** Materiality — does the finding genuinely block the convention purpose (no lost feedback, burden-free capture, navigable growth, honest metadata)? Improbable edge cases and style points are REFUTED even if technically true. Default REFUTED if uncertain.
**Scope:** Both Criticals in the target report (PM-001-iter8, PM-002-iter8). Majors/Minors out of scope per task instructions.

## Navigation

| Section | Purpose |
|---------|---------|
| [PM-001-iter8](#pm-001-iter8-cp-01-exception-not-in-ssot) | CP-01 exception verdict |
| [PM-002-iter8](#pm-002-iter8-segment-cap-missing-from-templateslive-files) | Segment-cap verdict |
| [Summary](#summary) | Final disposition |

---

## PM-001-iter8: CP-01 exception not in SSOT

**Verdict: REFUTED**

The underlying facts are accurate — `.context/rules/agent-development-standards.md:382` states CP-01 ("File paths only in handoffs, NEVER inline content") with no exception text, while `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:78` and `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:27` both call the inline-candidate allowance "a stated exception to CP-01." But CP-01 is tagged `MEDIUM` in its own table (`agent-development-standards.md:382`), and the framework's own Tier Vocabulary states the override requirement for MEDIUM rules is "Documented justification" (`.context/rules/quality-enforcement.md`, Tier Vocabulary table) — not "the SSOT row itself must be edited." LOG-M-005 supplies exactly that documented justification, in the same governing text a background/worker agent would consult when tasked under this convention (`feedback-decision-logs-standards.md:27`, `design/feedback-decision-log-convention-design.md:78-79`). This is the standard general-rule/specific-exception layering already used throughout this rule corpus, not an unratified override.

The claimed failure mode — a worker "built to the real rule" drops the candidate because it never sees the exception — requires the worker to be handed a task under this convention while somehow lacking the very convention text (LOG-M-005) that instructs it to return the candidate inline; in practice the orchestrator, which does hold both texts, is the one issuing that instruction, and an explicit task-level instruction from the orchestrator governs the worker's turn regardless of what a general default elsewhere says. This is a documentation-consistency/traceability nit (the CP-01 row could cross-reference the exception for tidiness) rather than a path that "genuinely blocks" no-lost-feedback in practice — it does not survive the materiality bar for Critical.

---

## PM-002-iter8: Segment cap missing from templates/live files

**Verdict: REFUTED**

Confirmed by direct read: `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md:16-36` (Log Conventions + Segment Index) and `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md:18-22` (live bootstrap) do not state the "~50 entries or ~800 lines" number; the number lives only at `feedback-decision-logs-standards.md:28` and `feedback-decision-log-convention-design.md:195`. That part of the finding is factually accurate.

It is not, however, a "zero in-file warning" condition as claimed. `FEEDBACK-LOG.template.md:3` (and the live file's own header framing) explicitly cites its SSOT: "Per the Feedback & Decision Log Standards (`feedback-decision-logs-standards.md`)." — a one-hop, in-file pointer straight to LOG-M-006, where the cap lives. This SSOT-plus-pointer pattern (state a value once, point to it elsewhere rather than duplicate it) is the framework's own established practice — e.g. `.context/rules/file-organization.md`, `.context/rules/error-handling-standards.md`, and `.context/rules/tool-configuration.md` each read "CONSOLIDATED: ... rules are now in `{other-file}.md`" with no restatement of the values themselves. Once the standards file installs to `.context/rules/`, it is auto-loaded every session per the `(A)` marker convention (`CLAUDE.md` Navigation table), making the cap available at session start independent of whether the template also states it — the identical resilience mechanism every other numeric HARD/MEDIUM threshold in this framework relies on (thresholds are not re-stated in every artifact that touches them).

The residual this finding is really pointing at — no automated backstop fires if the self-count is forgotten, because AE-006e fires on compaction, not cumulative growth — is already disclosed and accepted as a residual in the design doc itself (`feedback-decision-log-convention-design.md:195`: "the residual is disclosed, not backstopped, until the commit-time lint is wired") and was explicitly closed by disclosure in the prior round (`iteration-007/restore-notes.md`, Step 1 row 3 / Residuals Disclosed table: "PM-001/IN-001 ... disclosure (delete AE-006e overclaim; disclose the gap)"). PM-002-iter8 narrows the framing to "the number itself isn't restated in the template," which is a real, cheap-to-fix redundancy improvement (Major, as the target report itself scores in the Completeness dimension) but not a distinct blocking path beyond what is already disclosed, and not one that leaves the operator with no route to the number. Does not survive the materiality bar for Critical.

---

## Summary

Both Criticals report real, evidenced textual gaps, and both proposed fixes are cheap and worth taking — but neither constitutes a path that genuinely blocks the convention's core purpose (no lost feedback / navigable growth) once the framework's own existing mechanisms (MEDIUM-tier documented-justification override; SSOT-plus-pointer citation; auto-loaded rule corpus) are accounted for. Recommend downgrading both to Major (documentation/traceability hardening) rather than accepting as blocking Criticals.
