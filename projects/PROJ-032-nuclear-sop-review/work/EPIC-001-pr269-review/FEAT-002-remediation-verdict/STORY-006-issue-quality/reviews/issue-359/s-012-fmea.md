# FMEA Report: GitHub Issue #359 (BUG-010 — agent schema/standards conformance)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-359.md` (live text of GitHub issue #359, geekatron/jerry)
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this compact adaptation — blind single-strategy execution per orchestrator instruction
**Elements Analyzed:** 6 | **Failure Modes Identified:** 5 | **Total RPN:** ~1210

## Summary

Six elements analyzed (header, "what this is," "what was wrong," "what the fix changed," "how to verify," tracking footer). One Critical finding: the fix-summary paragraph asserts a project-anchored output location was declared "for all four agents," but the evidence pack shows sop-verifier's governance file explicitly declares **no** output location (`required: false`, no `location:` key — T1 read-only agent returns its report as Task response content). This is a factual overstatement of what the commit actually did. One Major finding: the "8 of 8 files valid" figure is asserted with no enumeration of which 8 files, forcing a reader to reconstruct the count from the diff (4 governance.yaml + 4 composition agent.yaml across the 4 agents) rather than the issue text. Two Minor polish items. Recommendation: **ACCEPT with one correction** (the output-location overstatement should be fixed before/alongside any further edits; the rest of the issue is accurate and well-evidenced against the remediation register and diff).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|-----------|
| S-012-01 | "What the fix changed" | Overstates scope: claims project-anchored output locations declared "for all four agents"; sop-verifier's governance file declares `output.required: false` with **no** `location:` key at all (T1, returns report as Task response content) | 8 | 10 | 7 | 560 | Critical | Reword to "for the three agents that produce file output (sop-brief, sop-capture, sop-executor); sop-verifier declares no file output, by design (T1 read-only)" | Completeness / Evidence Quality |
| S-012-02 | "What the fix changed" | "8 of 8 files valid" cites a count with no stated basis; only 3 files are named earlier in the issue (sop-verifier.agent.yaml, sop-brief.governance.yaml, sop-verifier.governance.yaml) — reader must infer the other 5 (sop-executor/sop-capture governance.yaml + sop-brief/sop-executor/sop-capture composition agent.yaml) from the diff | 4 | 10 | 7 | 280 | Major | Append a one-clause gloss: "(the 4 governance.yaml + 4 composition agent.yaml files across all four agents)" | Traceability |
| S-012-03 | "What was wrong" | sop-capture is never named; "four agents" is asserted but only three (sop-brief, sop-verifier, sop-executor) are identified by file name anywhere in the issue | 3 | 8 | 6 | 144 | Minor | Name sop-capture once, e.g. in the output-location sentence, so all four agents are identifiable from the text alone | Completeness |
| S-012-04 | "What the fix changed" | "reasoning_effort: high added to the executor" is true but incomplete — the same commit also added `reasoning_effort: high` to sop-capture's governance file; the issue implies executor was the only agent affected | 2 | 7 | 7 | 98 | Minor | Add ", and to sop-capture (aligned to the same C3 tier)" or drop the exclusivity implication | Internal Consistency |
| S-012-05 | "How to verify" | Verify command gives no fallback if the reader's local tooling lacks a schema-validator CLI; "re-validate ... — zero errors" names no concrete command (contrast with the git diff command given one clause earlier) | 2 | 6 | 8 | 96 | Minor | Name the actual validator invocation used by the register (`uv run jsonschema` or repo validator script path) instead of leaving it generic | Actionability |

## Finding Details (Critical + Major)

### S-012-01 (Critical): Output-location claim overstates the fix

**Element:** "What the fix changed" paragraph, clause "project-anchored output locations declared for all four agents."

**Effect:** A reader (human or agent) checking sop-verifier's `agents/sop-verifier.governance.yaml` after reading this sentence will find no `output.location` field at all and may conclude the fix is incomplete or the issue text is unreliable — undermining trust in the rest of the (otherwise accurate) issue. This also misrepresents the remediation register's own fix specification, which explicitly directs "sop-verifier: no file output (required:false), so declare none."

**S/O/D rationale:** S=8 — directly contradicts verifiable evidence and could cause a reviewer to distrust or re-litigate an already-closed fix. O=10 — the sentence is present exactly as written; the overstatement is certain, not probabilistic. D=7 — undetectable without cross-referencing the governance-yaml diff; a reader without repo access cannot self-catch this.

**Corrective Action:** Replace "project-anchored output locations declared for all four agents" with wording that distinguishes the three agents that gained a `location:` field (sop-brief, sop-capture, sop-executor) from sop-verifier, which intentionally declares none.

**Acceptance Criteria:** Revised sentence names or implies exactly 3 agents received a location declaration, and states sop-verifier's no-output-location status as a deliberate T1 design choice, not an omission.

**Post-Correction RPN estimate:** ~40 (S=2, O=5, D=4 — residual risk only if wording is still terse).

### S-012-02 (Major): Unexplained "8 of 8" figure

**Element:** "What the fix changed" paragraph, closing parenthetical.

**Effect:** The number 8 does not match any count established earlier in the issue text (which names 3 specific files). A careful reader has to go find the diff/register to learn "8" = 4 governance.yaml + 4 composition agent.yaml. This forces an avoidable lookup for a claim the issue could state plainly.

**S/O/D rationale:** S=4 — does not mislead, only under-explains. O=10 — present as written. D=7 — only resolvable by reading the evidence pack, which the target audience (external contributor) does not have linked from the issue.

**Corrective Action:** Add a short gloss identifying what the 8 files are (4 governance.yaml + 4 composition agent.yaml, one pair per agent).

**Acceptance Criteria:** The "8 of 8" figure is self-explanatory from the issue text alone, without requiring the register or diff.

**Post-Correction RPN estimate:** ~40.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-012-01 omits/misstates sop-verifier's actual (no-output) status; S-012-03 leaves one of four agents unnamed |
| Internal Consistency | 0.20 | Negative | S-012-01 contradicts the register's own fix spec for sop-verifier; S-012-04 implies executor-only scope for a change also made to sop-capture |
| Methodological Rigor | 0.20 | Neutral | The "What was wrong" enumeration otherwise tracks the register's G1–G8 groups precisely (error counts, file names, and consequences all verified accurate) |
| Evidence Quality | 0.15 | Negative | S-012-01's claim is not just unevidenced but contradicted by the cited evidence pack |
| Actionability | 0.15 | Negative | S-012-05: verify step 2 lacks a concrete command, unlike verify step 1 |
| Traceability | 0.10 | Negative | S-012-02's uncited "8 of 8" figure breaks the otherwise strong traceability (worktracker path, register section, branch name, CI run link all verified correct) |

**Overall assessment:** Targeted corrections required. The issue's factual claims are overwhelmingly accurate and well-evidenced (error counts, file names, worktracker path, CI link, branch name all check out against the remediation register, remediation log, and commit evidence pack) — but the single Critical overstatement (S-012-01) about sop-verifier's output-location status must be corrected before this issue can be considered a fully honest closure record.
