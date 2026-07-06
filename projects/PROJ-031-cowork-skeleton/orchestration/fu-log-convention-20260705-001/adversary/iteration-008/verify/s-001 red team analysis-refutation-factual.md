# Refutation Panel — Factual Lens (Iteration 8, S-001 Red Team Analysis)

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-001-findings.md`
**Lens:** Factual accuracy — does the defect exist at the cited lines in the CURRENT files? Misreadings, stale refs, and restatements of already-disclosed residuals or restore-notes dispositions are REFUTED. Default REFUTED if uncertain.
**Reviewer:** adv-executor (verification panel, iteration-008, factual lens)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What was checked |
| [Critical Verdicts](#critical-verdicts) | Per-Critical VERIFIED/REFUTED |
| [Supporting Evidence](#supporting-evidence) | Cross-checks performed |
| [Summary](#summary) | Final counts |

## Scope

The target report contains exactly **one** Critical finding in its Findings Table: `RT-001-20260706-iter8`. The report's "Verification Notes" section documents a second candidate (Adoption-plan step-4 entry-count staleness) that the report itself already ruled out as *not a finding* — it is not in the Findings Table and is not evaluated here as a Critical.

Checked against current file state:
- `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md`
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/examples-appendix.md`
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/hook-design-note.md`
- `.context/rules/agent-development-standards.md` (CB-04 cross-reference)
- `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/restore-notes.md` (prior-round disposition record)

## Critical Verdicts

### RT-001-20260706-iter8 — Background-agent "candidate" handoff carries no verbatim-fidelity requirement

**VERIFIED.**

All four primary citations check out at the current line numbers: `feedback-decision-log-convention-design.md:58` is the Verbatim-field schema row ("User's exact words, full... Word-for-word — verbatim means verbatim... verbatim wins", Author column "user (copied)"); `feedback-decision-log-convention-design.md:78` is the concurrent-writer/candidate-handoff paragraph containing "the orchestrator appends it verbatim" and defining a candidate as "a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary"; `feedback-decision-logs-standards.md:27` is LOG-M-005, which describes worker/background candidates returned "inline via the P-003 handoff" with the same silence on payload-content fidelity; `FEEDBACK-LOG.template.md:22` is the single-writer-safety callout, likewise silent on whether the candidate text equals the operator's own words. The `agent-development-standards.md` CB-04 cross-reference is accurate: that rule genuinely characterizes `key_findings` as a "3-5 bullets... 10:1 compression ratio" orientation field, not a verbatim-quote field.

A targeted search across all five candidate/background-agent files for any clause requiring the candidate payload to preserve the operator's unaltered wording (searched for "unaltered", "paraphrase", "quote the operator", "worker's own words", and all "candidate"/"background agent" occurrences) returned no hits beyond the passages already cited by the report — confirming the report's "Existing Defense: Missing" claim is accurate as of the current text. The Verbatim-field's generic "Author: user (copied)" rule (line 58) states the *intended* end-state for the field but, contrary to a possible rebuttal, does not itself instruct how a worker/background agent should construct the candidate text to satisfy that intent — the candidate-handoff clause (line 78) that governs that specific pathway addresses only serialization/race-condition mechanics, not content provenance. This is a load-bearing, genuinely new gap, not a restatement: the report's own Summary correctly distinguishes it from the four residuals this round declined to re-litigate (concurrent-writer race, `--no-verify` bypass, transcript-retention dependency, silent-non-capture/Q5), and a full read of the Revision Changelog (`feedback-decision-log-convention-design.md` v3–v9 entries, lines 345–351) confirms the candidate-handoff bullet has been revised repeatedly for *race-condition* and *CP-01-exception* framing (PM-004/FM-002/FM-006/FM-008) but never for *content-fidelity* — so this is not a restatement of any already-disclosed residual or any iteration-007 restore-notes disposition (the six Criticals restore-notes.md closes are RT-001 redaction-hygiene, DA-001/FM-006 "Five safety functions," PM-001/IN-001 AE-006e-cap-backstop, PM-002 install-stall placeholder, FM-001 inline-doc dedup, and FM-003 split-entry — none address candidate verbatim fidelity).

## Supporting Evidence

- `feedback-decision-log-convention-design.md:78` (Read, offset 1-120): confirms exact quoted text "(A candidate is a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary — a stated exception to CP-01's file-paths-only preference... the orchestrator appends it verbatim.)"
- `feedback-decision-log-convention-design.md:58`: confirms exact quoted text "Word-for-word — verbatim means verbatim. The verbatim is the fidelity anchor: on any conflict, **verbatim wins**."
- `feedback-decision-logs-standards.md:27` (LOG-M-005): confirms "workers (incl. background handoffs) return short candidates inline via the P-003 handoff, appended the same turn (a stated exception to CP-01)" — silent on candidate content fidelity.
- `FEEDBACK-LOG.template.md:22`: confirms "Background agents return short *candidates* the orchestrator appends; they do not write here directly" — silent on candidate content fidelity.
- Grep for `unaltered|paraphrase|worker's own words|quote the operator|verbatim.*candidate|candidate.*verbatim` across the design directory: no matches in the design doc or templates (only tangential hits in the rule file and hook-design-note that do not address this gap).
- `examples-appendix.md` and `hook-design-note.md`: reviewed in full; neither discusses background/worker-agent candidate content fidelity.
- `iteration-007/restore-notes.md`: the 6 Criticals it closes are unrelated to candidate-content verbatim fidelity (redaction hygiene, safety-function count, AE-006e disclosure, install-stall bound, inline-doc dedup, split-entry) — this finding is not a restatement of any restore-notes disposition.
- Revision Changelog (`feedback-decision-log-convention-design.md` lines 345-351, v3-v9): confirms the candidate-handoff bullet's prior revisions addressed race-condition/CP-01-exception framing only, never content-fidelity — supporting the report's claim that this is a genuinely new gap.

## Summary

| Metric | Count |
|--------|-------|
| Criticals in target report | 1 |
| Verified | 1 |
| Refuted | 0 |
