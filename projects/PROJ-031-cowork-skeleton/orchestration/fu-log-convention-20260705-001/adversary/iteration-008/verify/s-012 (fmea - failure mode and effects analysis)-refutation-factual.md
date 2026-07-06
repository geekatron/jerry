# Factual-Accuracy Refutation Panel — S-012 (FMEA) — Iteration 8

> Lens: **factual accuracy only** — does each cited Critical defect exist at the cited lines in the CURRENT deliverable files? Misreadings, stale references, and restatements of already-disclosed residuals or `iteration-007/restore-notes.md` dispositions are REFUTED. No other iteration-007/008 adversary panel files were read.

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-012-findings.md`
**Deliverables checked:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`, `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Cross-reference:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md`

---

## Criticals under review

The findings table lists 2 Criticals (FM-001-i008fmea, FM-002-i008fmea) and 2 Majors (FM-003-i008fmea, FM-004-i008fmea, out of scope for this Criticals-only panel).

---

### FM-001-i008fmea: Segment-Index-overflow exemption contradicts the rule file's own Scope-limits disclosure

**Verdict: VERIFIED**

Design doc `feedback-decision-log-convention-design.md:264` reads exactly as quoted: "...its failure is detected by lint 2's contiguity/orphan check and is fully recoverable by re-reading segment headings, so it needs no owned review date," referring to the "Five safety functions" paragraph's segment-index-overflow exemption. The rule file's Scope-limits item (e), `feedback-decision-logs-standards.md:85`, independently and correctly states: "Segment Index display accuracy — the displayed `id-range` per row is not checked against the segment's true first/last heading... so a stale index row can sit undetected." Both L5-lint-2 definitions (design doc `:236`, rule file `:82`) describe id uniqueness/contiguity/orphan detection only — neither describes any check on the Segment Index's own line-count/overhead (the actual subject of the L1.4 "index+queue overhead exceeds ~100 lines" trigger, design doc `:199`). The design doc's claim that lint 2 "detects" this trigger's failure is unsupported by lint 2's own documented scope in both files, and `restore-notes.md`'s Step 1 row 2 / Residuals Disclosed table confirms the owner closed this as a clean wording fix with **no disclosed residual** — so this is not a restatement of an already-accepted residual; it is a genuine, newly-introduced internal-consistency defect in text added this round, accurately cited.

---

### FM-002-i008fmea: Inline-doc dedup key is unspecified and has zero worked examples in the package

**Verdict: VERIFIED**

All three cited specification sites match verbatim: design doc `:61` ("for `inline-doc`, append the annotation's `path:line/anchor`"), rule file `:51` ("check for an existing entry carrying the same `source: inline-doc` `path:line/anchor`"), and `FEEDBACK-LOG.template.md:25` ("checks for an existing entry with the same `source: inline-doc` path/anchor") — none disambiguates raw line number vs. heading anchor vs. a concatenation. Direct inspection of `examples-appendix.md` confirms both FEEDBACK-LOG worked examples (`:57`, `:81`) use `source \`chat\``, and the "Common cases" bullet at `:169` restates the rule in prose with no concrete key value. The only near-miss is `FEEDBACK-LOG.template.md:53`, a comment showing the pattern `source inline-doc {path}:{line-or-anchor}` — but this uses unfilled placeholder tokens (and the literal token "line-or-anchor" itself embodies, rather than resolves, the ambiguity the finding names), not a concrete worked value, so it does not contradict the "zero worked examples" claim as the finding specifically defines it (a filled-in Context line with a real path/line or anchor). This is a genuine, accurately-cited evidence-quality gap, not a misreading.

---

## Summary

| ID | Verdict |
|----|---------|
| FM-001-i008fmea | VERIFIED |
| FM-002-i008fmea | VERIFIED |

Both Criticals cite file+line evidence that checks out exactly against the current post-restore deliverable text; neither is a stale reference, a misreading, nor a restatement of a residual `restore-notes.md` already discloses as accepted (that table lists only PM-001/IN-001 as carrying a disclosed residual — DA-001, the fix underlying FM-001, is recorded as closed with no residual). No Criticals in this report were refuted under the factual-accuracy lens.

---

*Panel: adv-executor, iteration-008, S-012 factual-accuracy refutation pass. P-003: no subagents invoked. P-020: draft-only, no writes to `.context/`, `docs/`, or `hooks/`. P-022: all verdicts cite file+line from the current deliverable text; no other iteration-007/008 adversary panel files were read except `iteration-007/restore-notes.md`.*
