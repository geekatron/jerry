# Refutation Panel — Remediation-Value Lens — S-004 Pre-Mortem Analysis (iteration-007)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Target report, lens, method |
| [PM-001 Disposition](#pm-001-disposition-refuted) | The sole Critical, evaluated |
| [Summary](#summary) | Final verdict |

## Scope

**Lens:** remediation-value — would fixing the finding materially change adoption outcomes, or is it churn? Fixes that add machinery against the anti-bloat doctrine are refuted. Default refuted if uncertain.
**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-004-findings.md`
**Criticals in target:** 1 (PM-001). PM-002/PM-003 are Major — out of scope per the task's "every Critical" instruction.
**Deliverables cross-checked:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/*`, `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md`, `projects/PROJ-031-cowork-skeleton/LLM-DECISION-LOG.md`, `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md`.

## PM-001 Disposition: REFUTED

**Claim:** design doc's Adoption Plan Step 4 (`design/feedback-decision-log-convention-design.md:255`) states an "8 live entries" worked count that is stale, and the live `FEEDBACK-LOG.md` banner (`FEEDBACK-LOG.md:4`, "Entries FU.0–FU.9 are real and preserved") is stale relative to its own body (FU.10/FU.11 exist at `FEEDBACK-LOG.md:165,176`).

**Design-doc arithmetic is not actually false.** `design/feedback-decision-log-convention-design.md:255` states two independent, jointly-exhaustive branches in the same sentence: (a) "entries already carrying a `(user label: X)` suffix are renamed in place" — a generic, self-executing rule, and (b) "of the **8 live entries** that currently all carry **no suffix** (FU.0–FU.4, DEC-LLM-001..003), 5 receive `(alias: —)` ... while FU.0, FU.1, and FU.2 receive their embedded self-label re-derived." Verified against the live log: `FEEDBACK-LOG.md:26,41,55,71,84` (FU.0–FU.4 headings) carry no `(user label: X)` suffix — still exactly 8 no-suffix entries today, matching the design's count exactly. FU.5–FU.11 (`FEEDBACK-LOG.md:101,113,125,137,148,165,176`) all carry `(user label: X)` suffixes and are therefore already covered, completely and correctly, by branch (a) — no re-derivation or re-count is needed for them under the stated rule. The design text is a complete description of the current 12-entry state, not a stale enumeration masquerading as a total; PM-001's own quoted evidence supports this reading once the full sentence (not the isolated clause) is considered.

**The one genuinely-true fact (banner staleness) is out of scope of the deliverable and is churn to fix.** `FEEDBACK-LOG.md:4`'s "FU.0–FU.9" banner text is real and is one review-round behind its own body — but this bootstrap banner is explicitly disclosed as "ACTIVE bootstrap" (temporary) in the same line, and `design/feedback-decision-log-convention-design.md:255` already states the correct remediation is wholesale replacement at install ("On ratification, swap it for the ratified-convention banner"), independent of whatever number the interim banner currently carries. The finding's own Execution Notes concede the live files were "read for cross-verification only, not deliverables under review." Editing the banner's number today produces no change to the shipping artifact or the install outcome — it would be overwritten at install regardless — so this is exactly the "churn, not adoption-relevant" case the remediation-value lens is designed to filter out. The proposed mitigation (reword the banner "to be self-relative") is a defensible taste improvement but not necessary for correct installation, since the design's rename-in-place rule already produces the correct outcome without it.

**Conclusion:** the Critical conflates (1) a design-doc claim that is, on full-sentence reading, still accurate and complete, with (2) a bootstrap-file cosmetic staleness that the design's own adoption plan already schedules for full replacement regardless of its current wording. Neither branch would materially change the adoption outcome if "fixed" today — verified per H-16-adjacent close reading; per this lens's default-refute-if-uncertain instruction and the anti-bloat/churn test, PM-001 is REFUTED.

## Summary

| ID | Severity (as filed) | Disposition | Rationale (one line) |
|----|---------------------|-------------|------------------------|
| PM-001 | Critical | REFUTED | Design-doc arithmetic remains accurate on full-sentence reading (8 no-suffix entries unchanged, suffix-rule already covers FU.5–FU.11); live-banner staleness is real but is an out-of-scope bootstrap cosmetic slated for wholesale replacement at install — fixing it now is churn, not adoption-relevant. |

**No Criticals verified this round.**
