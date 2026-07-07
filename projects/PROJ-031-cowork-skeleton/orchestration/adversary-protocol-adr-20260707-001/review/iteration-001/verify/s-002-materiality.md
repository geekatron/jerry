# Refutation Panel: Materiality Lens — S-002 Devil's Advocate Findings (Iteration 1)

**Lens:** Materiality — does the finding genuinely undermine the ADR (wrong decision, unimplementable
spec, false evidence)? Style/edge-case findings are refuted even if factually true.
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-002-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Scope:** All four Critical findings in the target report (DA-001, DA-002, DA-003, DA-004).
**Blind:** No sibling panel/lens outputs consulted.

---

## DA-001-20260707-i1 — "18 files" citation is factually false (12 actual)

**Verdict: VERIFIED**

Independent enumeration of `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/` (Glob, twice, including a broad `**/*refutation*` pattern) returns exactly 12 files (4 Critical-bearing reports x 3 lenses: S-001, S-002, S-004, S-012). The ADR cites "18 files" at `c-004` (decisions ADR line 206) and "18 verification-panel files" at line 364. Notably, the false "18" figure is not an ADR fabrication in isolation — it is inherited verbatim from the ADR's own cited primary source, `fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:53` ("8 complete iteration-008 reports + 18 verification-panel files"), whose own Verification Roll-Up table (lines 63-71) lists only 7 findings across 4 reports = 12 files, not 18. This is genuine false evidence cited (twice) by the ADR to support constraint c-004's cost-proportionality claim — not a style nitpick — and it is the exact failure mode (an uncaught false quantitative claim) the ADR's own thesis exists to catch.

## DA-002-20260707-i1 — Cost-model formula contradicts c-004 and its own invocation contract

**Verdict: VERIFIED**

Independently confirmed against `iteration-009/s-014-quality-score.md` lines 19-38: 10 claimed Criticals across 5 reports (S-001 x2, S-002 x2, S-004 x2, S-011 x1, S-012 x3), corroborated by 15 actual verify files (Glob-confirmed). Constraint c-004 (ADR line 206) defines the unit as "per Critical-bearing report" (5 reports x 3 = 15, matching evidence); the Cost model paragraph (ADR lines 624-626) instead states "3 x (number of claimed Criticals)" (10 x 3 = 30, contradicting the cited 15-file evidence). This is a genuine, load-bearing internal contradiction, not stylistic: the ADR's own L1 invocation-contract sentence (line ~585-587) compounds it by saying "one call per lens per Critical-bearing report" in the same breath as "Input = the single claimed Critical," leaving WI-1's implementer with no unambiguous unit of work — a real Actionability/Internal-Consistency defect that would produce a ~2x cost discrepancy depending on interpretation.

## DA-003-20260707-i1 — D-1's criticality-gating boundary is unevidenced at C1/C2/C3

**Verdict: VERIFIED**

Independent grep of `Criticality Level` across every `s-003`/`s-014` file in both `adr-convention-20260702-001` and `fu-log-convention-20260705-001` confirms 100% self-declared C4 (dozens of matching lines, zero C1/C2/C3 hits for either package's actual tournament rounds). D-1's rationale (ADR line 264) asserts "C1-C2 work... neither exhibited it [the spiral]," framed as an evidence-led finding per c-005 ("the decision must be evidence-led and cite the tournament record"), and the Alignment table (line 405) scores Constraint Satisfaction HIGH partly on this basis. Since no C1, C2, or C3 round exists in the cited 18-round record, this specific claim is an unlabeled extrapolation presented as an observation — this is false-evidence framing on one of the six core decisions (D-1), not an edge case, and it also collapses the Option-B-vs-Option-C distinction the review was asked to probe (both are identical at 100%-C4 evidence).

## DA-004-20260707-i1 — RSK-1's mitigation misdescribes DEFAULT-REFUTED's own direction of effect

**Verdict: VERIFIED**

Confirmed at ADR line 707: RSK-1's mitigation reads "2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims." This directly contradicts the ADR's own repeated definitions of the same term: D-1 (line 381, "DEFAULT-REFUTED") and D-2 (line 382, "Refuted claims carry zero dimension weight") both establish that uncertainty defaults to discarding a claim, not keeping it — i.e., DEFAULT-REFUTED biases toward *discarding* claims (the false-positive counterweight), which is the structural opposite of what RSK-1's mitigation text claims. This is a direct, self-contradictory textual defect in the risk register's description of the exact mechanism the invoking review was asked to sanity-check (false-negative suppression), materially misleading a reader assessing whether RSK-1 is honestly bounded — not a stylistic or edge-case issue.

---

## Summary

| Finding | Verdict |
|---------|---------|
| DA-001-20260707-i1 | VERIFIED |
| DA-002-20260707-i1 | VERIFIED |
| DA-003-20260707-i1 | VERIFIED |
| DA-004-20260707-i1 | VERIFIED |

**Refuted:** none.

---

*Constitutional compliance: P-003 (no subagents invoked); P-020 (writes confined to
`projects/PROJ-031-cowork-skeleton/`; the deliverable and target report were not edited); P-022
(each verdict cites file+line or independently-reproduced Glob/grep counts). All paths in this
report are repo-relative; no absolute filesystem paths or employer-internal tokens are present.*
