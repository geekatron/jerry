# Refutation Panel — Materiality Lens — S-004 Pre-Mortem Analysis (iteration-007)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Target report, lens, scope |
| [Critical Disposition](#critical-disposition) | Per-Critical verdict with evidence |
| [Summary](#summary) | Verified/refuted counts |

## Context

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-004-findings.md`
**Lens:** Materiality — does the finding genuinely block the convention's purpose (no lost feedback, burden-free capture, navigable growth, honest metadata)? Default REFUTED if uncertain; improbable edge cases and style points are REFUTED even if true.
**Criticals in target report:** 1 (PM-001). PM-002 and PM-003 are Major and out of scope for this Critical-only refutation pass.

## Critical Disposition

### PM-001: "Migration instructions and status banner are already stale relative to the live log" — REFUTED

**Finder's claim:** Design doc Adoption Plan Step 4 (`design/feedback-decision-log-convention-design.md:255`) allegedly gives a stale, false arithmetic ("8 live entries") that "undermines confidence the plan was re-verified," and the live `FEEDBACK-LOG.md:4` banner ("FU.0–FU.9") is stale against the body (`FEEDBACK-LOG.md:165,176` show FU.10/FU.11 exist).

**Why this is REFUTED on materiality grounds:**

1. **The finder misreads the scope of the "8 live entries" clause.** `design/feedback-decision-log-convention-design.md:255` reads: "entries already carrying a `(user label: X)` suffix are renamed in place; **of the 8 live entries that currently all carry no suffix** (FU.0–FU.4, DEC-LLM-001..003), 5 receive `(alias: —)`... while FU.0, FU.1, and FU.2 receive their embedded self-label re-derived..." The "8 live entries" phrase is explicitly scoped to entries **carrying no suffix at all** — a closed, historically-fixed set (FU.0–FU.4 predate the "review round" labeling convention). It is not a claim about the total live entry count. This scoped statement remains accurate today: FU.0–FU.4 still carry no `(user label: X)` suffix in the live file. The finder's claim that this arithmetic is "now simply false" conflates a scoped subset (no-suffix entries) with the full entry count (all entries) — a category error, not a factual staleness.

2. **The general rule already mechanically covers every entry the finder says is "not counted."** The clause immediately preceding the "8 live entries" arithmetic — "entries already carrying a `(user label: X)` suffix are renamed in place" — is a blanket rule, not an enumeration, and it self-evidently extends to any current or future suffix-bearing entry without needing restatement. Verified directly against the live file: FU.5 (`FEEDBACK-LOG.md:101`, "user label: FU.0.1"), FU.6 (`:113`), FU.7 (`:125`), FU.8 (`:137`), FU.9 (`:148`), FU.10 (`:165`), and FU.11 (`:176`) **all** carry `(user label: X)` suffixes, so all seven are already covered by the general rule cited in the same sentence the finder quotes. The finder's own finding text concedes this ("The general fallback rule... does mechanically cover them"), which directly undercuts the Critical severity claim that install "without an operator independently re-reading" would leave FU.5–FU.11 "with no explicit alias-normalization treatment" — the treatment is explicit, it is just expressed as a rule rather than an enumeration.

3. **The live `FEEDBACK-LOG.md` is explicitly out-of-scope as a deliverable, by the finder's own Execution Notes.** The report's own scope statement says the live log files were read "for cross-verification only, not deliverables under review" (s-004-findings.md Execution Notes, and `restore-notes.md` frames it the same way — a permitted disposition record, not a reviewed artifact). Elevating a stale banner line in a live, actively-edited bootstrap working file (`FEEDBACK-LOG.md:4`) to a Critical finding against the *design document's* quality is a materiality overreach: the banner is a status note in a WIP file that gets touched on essentially every edit pass, not a shipped template or rule-file artifact (the staged templates under `design/staging-feedback-logs/` do not contain this banner text or its stale count).

4. **No feedback is actually lost, no ids collide, and no entry is unhandled.** Cross-checked directly against the live file: all 12 entries (FU.0–FU.11 + DEC-LLM-001-003) are present, uniquely numbered, and each falls cleanly into one of the two migration buckets (no-suffix historical set, or suffix-bearing set governed by the blanket rule). The convention's stated purpose — no lost feedback, honest per-entry metadata — is not threatened by this wording; at worst, the illustrative arithmetic is a documentation-precision nit and the live banner is a one-line staleness in a non-deliverable working file, both fixable by a trivial edit with zero mechanism change (consistent with the finder's own P0 mitigation recommending only a wording fix, not new machinery).

**Verdict:** REFUTED. The finding rests on a misreading of the scoped "8 live entries" clause (a fixed no-suffix subset, not a total-entry claim) combined with elevating a stale banner line in an explicitly out-of-scope, non-deliverable working file to Critical severity. The actual migration mechanism (general suffix-rename rule) already and correctly covers every entry the finder flags as uncovered, by the finder's own concession. This does not genuinely block "no lost feedback," "burden-free capture," "navigable growth," or "honest metadata" at the design/template level — it is a style/precision point in illustrative text, refuted per this round's default-refuted-if-uncertain and improbable-edge-case/style-point exclusion instructions.

## Summary

| Finding | Severity (as claimed) | Verdict |
|---------|------------------------|---------|
| PM-001 | Critical | **REFUTED** |

**Verified Criticals:** 0
**Refuted Criticals:** 1 (PM-001)

No other Criticals appear in the target report (PM-002, PM-003 are Major and out of scope for this Critical-only pass).
