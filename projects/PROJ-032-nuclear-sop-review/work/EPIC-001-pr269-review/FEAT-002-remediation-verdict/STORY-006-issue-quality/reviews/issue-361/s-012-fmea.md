# FMEA Report: GitHub Issue #361 (BUG-012 / REM-12 state machine + completion contract)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-361.md` (live text of GitHub issue #361, geekatron/jerry)
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this blind lane — deliverable reviewed as a standalone communication artifact.
**Elements Analyzed:** 8 (title; what-this-is; 3 what-was-wrong sub-points; what-the-fix-changed; how-to-verify; tracking footer) | **Findings:** 6 | **Total RPN (informational):** 1,146

## Summary

Fact-checked every claim in the issue text against the remediation register (REM-12), the remediation log, the verdict, and the full `c07033ce` diff: **all substantive claims verify** (three-way state-machine divergence, COMPLETED-before-capture contradiction, literal-`true` vs. path type break, verifier's fail-open "if accessible" gap and its SEC-008 fail-closed fix, CI link, worktracker path). No factually wrong or misleading statements found — recommendation is **ACCEPT with corrections**. The findings below are all Major/Minor actionability and polish gaps, concentrated in the "How to verify" section, which is the only part of the text that would send a reader down extra, avoidable work.

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action |
|----|---------|-------------|---|---|---|-----|----------|-------------------|
| S-012-01 | How to verify | Insufficient: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` shows all 7 FIX-NOW clusters (REM-08..14, ~25 files), not just this issue's 3 defects | 5 | 9 | 6 | 270 | Major | Scope the diff to the 4 files this fix touches |
| S-012-02 | How to verify | Missing: no direct link to view the commit diff on GitHub; verification requires a local clone of the branch | 5 | 7 | 6 | 210 | Major | Add `https://github.com/geekatron/jerry/commit/c07033ce` alongside the CI link |
| S-012-03 | Title | Ambiguous ordering: leads with unexplained internal IDs (`PROJ-032/BUG-012`) before any human-readable context | 3 | 8 | 5 | 120 | Minor | Move IDs to the end of the title or drop from title (Tracking footer already carries them) |
| S-012-04 | What was wrong (2) | Insufficient: one run-on sentence packs 3 facts (forbidden transition, path-vs-boolean type break, blast radius) with no punctuation break | 3 | 6 | 5 | 90 | Minor | Split into two sentences |
| S-012-05 | What was wrong (3) | Inconsistent: text otherwise avoids bare internal codes (no "QG-E6", "NS-H-06", "IV-REJECTED") but drops in "(its SEC-008 item)" unexpanded | 3 | 5 | 5 | 75 | Minor | Expand inline: "(tracked as SEC-008 in your own QG-E6 report)" |
| S-012-06 | What the fix changed | Missing: fix sentences aren't numbered to mirror the (1)/(2)/(3) problem list, so the fix-to-problem mapping is implicit | 3 | 5 | 5 | 75 | Minor | Number the three fix clauses (1)/(2)/(3) to match |

**Finding ID format:** `S-012-NN` per orchestrator instruction (supersedes template default `FM-NNN`).

## Finding Details (Major)

**S-012-01** — Effect: a reviewer running the literal command sees ~25 changed files spanning registration text, schema fixes, OE contract, composition drift, and nav tables, and must manually isolate the 4 files relevant to this issue. Not wrong, but forces extra work contrary to the "act from this text alone" bar. Post-correction RPN estimate: ~60 (D drops once scoped).

**S-012-02** — Effect: an external contributor triaging via the GitHub UI (no local clone) has no click-through path to the diff; only the CI Actions run is a live link. Post-correction RPN estimate: ~70.

## Recommendations (priority order)

1. **S-012-01** — Replace the verify command with: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/agents/sop-verifier.md`.
2. **S-012-02** — Add the commit permalink next to the CI run link.
3. **S-012-03..06** — Polish pass: reorder title, split the dense sentence, expand the SEC-008 mention, number the fix list.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All 3 defects and their fixes are present and correct |
| Internal Consistency | 0.20 | Neutral | No contradictions found between claims and ground truth |
| Methodological Rigor | 0.20 | Negative (minor) | S-012-06: fix list doesn't trace 1:1 to problem list |
| Evidence Quality | 0.15 | Negative | S-012-01/02: verification path is imprecise and clone-only |
| Actionability | 0.15 | Negative | S-012-01/02 directly reduce ease of independent verification |
| Traceability | 0.10 | Negative (minor) | S-012-03: title ID placement; S-012-05: bare code |
