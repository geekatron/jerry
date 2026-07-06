# S-004 Pre-Mortem Analysis — Factual-Accuracy Refutation Panel (iteration-007)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What this panel checks |
| [Critical Findings Reviewed](#critical-findings-reviewed) | PM-001 (the only Critical) |
| [Verdict Summary](#verdict-summary) | Roll-up table |

## Scope

Lens: **factual-accuracy**. Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-004-findings.md` (S-004 Pre-Mortem Analysis, iteration-007). Only the **Critical**-severity finding is in scope per the panel brief (PM-002/PM-003 are Major and excluded). Files checked: `design/feedback-decision-log-convention-design.md`, `FEEDBACK-LOG.md`, `LLM-DECISION-LOG.md`, `restore-notes.md`.

## Critical Findings Reviewed

### PM-001: "Migration instructions and status banner are already stale relative to the live log" — REFUTED

**Cited evidence and its current state:**
- `design/feedback-decision-log-convention-design.md:255` currently reads: "heading suffixes are normalized to the ratified `(alias: X)` form at install time: entries already carrying a `(user label: X)` suffix are renamed in place; of the **8 live entries that currently all carry no suffix** (FU.0–FU.4, DEC-LLM-001..003), 5 receive `(alias: —)`... while FU.0, FU.1, and FU.2 receive their embedded self-label re-derived..." — text confirmed present verbatim.
- `FEEDBACK-LOG.md:4` currently reads "Entries FU.0–FU.9 are real and preserved" — confirmed present verbatim.
- `FEEDBACK-LOG.md:165` and `:176` currently show `### FU.10 diagrams-for-humans (user label: FU.0)` and `### FU.11 fu-log-workflow-crashed (user label: FU.1)` — confirmed present.
- `LLM-DECISION-LOG.md:12-14` nav table confirms exactly 3 entries (DEC-LLM-001..003) — confirmed not stale, as the finder itself notes.

**Why the finding is refuted despite the citations being real:** The finding treats the design doc's own qualifier as if it weren't there. Design doc line 255 does **not** claim "the live entries" number 8 in total — it explicitly scopes the "8" to "**the live entries that currently all carry no suffix**," immediately after stating the *general*, count-independent rule that governs every other case: "entries already carrying a `(user label: X)` suffix are renamed in place." `FEEDBACK-LOG.md:101-183` confirms FU.5 through FU.11 all carry the `(user label: X)` heading suffix (e.g., `FU.5 ... (user label: FU.0.1)` at line 101, `FU.11 ... (user label: FU.1)` at line 176), so every one of them is already covered — mechanically, not as an afterthought — by the general clause that precedes the "8" arithmetic in the same sentence. The set of entries carrying **no** suffix is, still today, exactly the 8 named (`FU.0-FU.4`, `DEC-LLM-001..003`): no entry has been minted without a suffix since that text was written, so the specific worked arithmetic remains textually accurate, not "simply false" as PM-001 asserts in its Likelihood/Severity prose. The finding's own Failure Cause paragraph quotes the qualifier correctly but its Likelihood/Severity analysis drops it, manufacturing an ambiguity that the qualified sentence does not actually contain — this is a misreading, not a defect in the deliverable's migration logic.

The remaining half of PM-001 — that the live `FEEDBACK-LOG.md` banner ("FU.0–FU.9") lags its own body (now through FU.11) — is factually true but targets an artifact the Pre-Mortem's own Execution Notes classify as "read for cross-verification only, **not** a deliverable under review." `FU.10`/`FU.11` were minted into that same live file during this very iteration's Restore pass (`restore-notes.md` Step 2, "Visual Layer (FU.10)"), i.e., normal ongoing operational log-keeping on a file explicitly labeled "ACTIVE bootstrap," not a defect in the reviewed design/staging package's migration plan or logic. A stale self-description banner on an actively-growing operational log is not evidence that the design's install-time migration rule is broken, since the migration rule is re-derivable-by-construction (general suffix-based rule) and does not depend on the banner at all.

**Verdict: REFUTED.** The "now simply false" characterization of the Adoption Plan Step 4 arithmetic is a misreading that drops the sentence's own qualifier; the true banner-staleness observation concerns a non-deliverable, actively-updated operational artifact, not a defect in the reviewed migration design.

## Verdict Summary

| ID | Verdict | Basis |
|----|---------|-------|
| PM-001 | REFUTED | Misreading of the qualified "8 live entries that currently all carry no suffix" clause (still accurate today, `design/feedback-decision-log-convention-design.md:255`); residual banner-staleness claim targets the live bootstrap `FEEDBACK-LOG.md` (`:4`, `:165`, `:176`), explicitly out of scope as "not a deliverable under review" per the Pre-Mortem's own Execution Notes |

---
*Panel: adv-executor (factual-accuracy refutation lens) · iteration-007 · verified-criticals protocol*
