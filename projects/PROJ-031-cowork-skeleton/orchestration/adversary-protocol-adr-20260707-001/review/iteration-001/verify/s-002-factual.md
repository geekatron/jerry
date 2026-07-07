# Factual Refutation Panel: S-002 Devil's Advocate Criticals (Iteration 1)

**Lens:** Factual accuracy (does the defect exist at the cited lines?)
**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-002-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Reviewer:** blind refutation panel, lens = factual, iteration 1
**Rule:** default REFUTED if uncertain; misreads/stale refs/restatements of disclosed limits are REFUTED.

---

## DA-001-20260707-i1 — VERIFIED

**Claim:** ADR cites "18 verifier files" for fu-log iteration-8 vs. 12 actual.

Independently re-globbed `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/*`: exactly 12 files exist (S-001, S-002, S-004, S-012 x 3 lenses each). The ADR text at line 206 (c-004 row: "iter-8 FU: 18 files") and line 364 ("`.../fu-log .../iteration-008/`: '18 verification-panel files'") both state 18, confirmed false against the independently-counted 12; the underlying source score report itself (`fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:36`) even says "18 verification-panel files ... x 4 Critical-bearing reports," which is internally inconsistent with its own math (4 x 3 = 12, not 18), corroborating that this is a real, propagated arithmetic error. Note: the finder's own citation of "Context, line 133" for the second occurrence is a stale/incorrect line pointer (line 133 discusses iteration-6 score decline, not file counts; the actual second occurrence is at line 364, in the D-6 Options-Considered section, not "Context") — a citation defect within the finding itself — but the finder's other citation ("Constraints c-004, line 206") is accurate, and the core quantitative defect is independently confirmed true, so the finding is VERIFIED despite the imprecise secondary line reference.

## DA-002-20260707-i1 — VERIFIED

**Claim:** Cost-model formula ("3 x number of claimed Criticals") contradicts c-004 ("3 agent runs per Critical-bearing report") and the cited evidence.

Confirmed at cited lines: c-004 (ADR line 206) states the unit is "per Critical-bearing report"; the Cost model paragraph (ADR lines 624-626) states "cost ~= 3 x (number of claimed Criticals)," a different, per-finding unit — a genuine textual contradiction, not a misread. Applying the arithmetic: iteration-9's own Panel-Outcome Reconciliation table (`adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md:21`) lists exactly 10 claimed Criticals across 5 reports, and the actual file count is 15 (independently reglobbed), matching 5 reports x 3 = 15, not 10 x 3 = 30; iteration-8 FU-log's Verification Roll-Up table lists exactly 7 claimed Criticals, and actual files are 12 (4 reports x 3), not 7 x 3 = 21 — both rounds falsify the "3 x Criticals" reading and confirm the "3 x reports" reading. The cited invocation-contract ambiguity ("one call per lens per Critical-bearing report" vs. "Input = the single claimed Critical," ADR lines 585-587) is also confirmed present verbatim. VERIFIED.

## DA-003-20260707-i1 — VERIFIED

**Claim:** D-1's C1/C2/C3-vs-C4 gating boundary is evidenced by zero C1, C2, or C3 tournament rounds; 100% of cited rounds are C4.

Grepped `Criticality Level` across every `s-003-findings.md` and `s-014-quality-score.md` file in both `adr-convention-20260702-001/**` and `fu-log-convention-20260705-001/**`: every match reads "C4" (with a small number of files noting, as an aside, that S-010/self-refine mislabels its own round C3 internally — explicitly dismissed in those same files as "a minor internal labeling inconsistency... not scored against the deliverable," so it does not constitute an actual C1/C2/C3 round). Zero rounds are genuinely scored/declared at C1, C2, or C3. The cited ADR text at line 264 ("the spiral is an observed C4/C3-governance phenomenon over many rounds; C1-C2 work... neither exhibited it") is confirmed present verbatim, and the counter-argument that this is an unevidenced extrapolation (no C1/C2/C3 round exists to check) is factually accurate. VERIFIED.

## DA-004-20260707-i1 — VERIFIED

**Claim:** RSK-1's mitigation ("DEFAULT-REFUTED... biases toward keeping claims") misdescribes DEFAULT-REFUTED's own direction of effect relative to D-1/D-2's own definitions.

Confirmed at cited lines: RSK-1 (ADR line 707) states verbatim "2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims"; D-1 (ADR line 381) defines the same mechanism as "2-of-3 majority, DEFAULT-REFUTED, blind to each other," and D-2 (ADR line 382) states "Refuted claims carry zero dimension weight." By construction, a default of REFUTED-under-uncertainty biases the system toward discarding/not-counting claims, not toward keeping them — the opposite of what RSK-1 asserts as its primary mitigation for a false-negative (real-Critical-discarded) risk. This is a genuine, textually-confirmed self-contradiction (the ADR's own two other definitions of DEFAULT-REFUTED directly contradict RSK-1's characterization of the same term), not a misread. VERIFIED.

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-20260707-i1 | VERIFIED |
| DA-002-20260707-i1 | VERIFIED |
| DA-003-20260707-i1 | VERIFIED |
| DA-004-20260707-i1 | VERIFIED |

**Result:** {lens: 'factual', verified_ids: ['DA-001-20260707-i1', 'DA-002-20260707-i1', 'DA-003-20260707-i1', 'DA-004-20260707-i1'], refuted_ids: [], file: 'projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/verify/s-002-factual.md'}

---

*Constitutional compliance: P-003 (no subagents invoked); P-020 (writes confined to
`projects/PROJ-031-cowork-skeleton/`); P-022 (all verdicts cite file+line evidence independently
re-derived via Glob/Grep against the ADR and the cited score-report/panel-file corpus; the one
citation defect found (DA-001's stale "line 133" pointer) is disclosed rather than silently
accepted or used to inflate the refutation count). All paths in this report are repo-relative; no
absolute filesystem paths or employer-internal tokens are present.*
