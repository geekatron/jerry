# Materiality Refutation Panel — S-011 Chain-of-Verification Findings (iteration 2)

> Lens: **Materiality** — does the finding genuinely undermine the ADR (wrong decision, unimplementable
> spec, false evidence)? Style/edge-case defects are REFUTED even if factually true. DEFAULT REFUTED
> IF UNCERTAIN. Blind pass — no other panel lens's output consulted.

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Which findings this panel adjudicates |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Roll-up table |

---

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-011-findings.md`

The refutation-panel protocol (per the ADR under review itself, e.g.
`projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md:146` —
"no refutation panel runs against non-Critical findings under this protocol") scopes panels to
**Critical**-severity findings only. The S-011 report contains two Criticals (CV-001-20260707,
CV-002-20260707) and one Major (CV-003-20260707). Per the commissioned instruction ("Attempt to
REFUTE each Critical"), this panel adjudicates only the two Criticals. CV-003-20260707 (Major) is
out of scope for this panel and is not scored here.

---

## Verdicts

### CV-001-20260707 — "Flagship fabricated-verification anecdote misattributes the catching mechanism" [CRITICAL]

**VERIFIED.**

Independently re-read the primary source the ADR itself cites. The score report
(`projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md:45-58`,
"Verified-Criticals Disposition" table) lists exactly six claimed Criticals that were run through the
3-lens refutation panel: 002-001, 002-002, 004-001, 012-004, 013-001, CV-001-i010. The fabricated
PR-template claim is a **different** finding, tracked as `RT-001-iter010`, and appears only in the
same report's "Unrefuted Majors/Minors (Advisory)" table
(`s-014-quality-score.md:144-161`), explicitly labeled **Major**, sourced from **S-001 Red Team**, with
the report's own stated rule that "no refutation panel runs against non-Critical findings under this
protocol." The cited support file, `.../iteration-010/post-ceiling-fix-notes.md:55-65` (Cluster 3),
documents the factual correction but attributes it to this post-ceiling owner-remediation pass itself,
not to any panel/lens mechanism. This is genuinely material, not stylistic: the ADR's Decision Rationale
and L1 sections use this exact anecdote, three separate times, as the flagship causal evidence that the
**new** independent Refutation-Panel Verify stage (D-1/D-6) is what is needed — when the primary
record shows an **ordinary pre-existing finder rotation (S-001 Red Team)**, not the new mechanism,
made the catch. This weakens the evidentiary basis for the ADR's central proposed innovation. False
attribution of supporting evidence for a core Decision-section causal claim meets the "false evidence"
materiality bar.

### CV-002-20260707 — "Figure 3 permits a VERIFIED Critical to bypass remediation, contradicting D-2 and Figure 2" [CRITICAL]

**VERIFIED.**

Re-traced Figure 3's edges directly in the ADR
(`projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:533-557`):
`Q1{"Any VERIFIED Criticals this round?"} -- "Yes" --> Q2{"...RECUR across independent rounds?"}`;
`Q2 -- "No: fresh stream..." --> Q3{"Running verified protocol already?"}`; `Q3 -- "Yes" --> Q4{"RT-M-010
ceiling reached?"}` — with no edge from this path into `FIX`. This is confirmed against Figure 2
(`:488-529`, `Verified --> AutoReviseGate: blocks PASS regardless of composite` unconditionally) and
D-2's own decision-table text (`:290-312`, `:404`, "Only panel-VERIFIED Criticals trigger
automatic-REVISE" — stated with no recurrence qualifier). The contradiction is structurally severe,
not an edge case: because "recurrence across independent rounds" by definition cannot be satisfied on
a Critical's *first* appearance, the diagram as literally drawn would route every freshly-panel-VERIFIED
Critical (once already on the verified protocol) around the `FIX` node on its first occurrence —
directly reintroducing "unresolved Critical claims counted as non-issues," the exact failure mode this
ADR exists to close. The ADR explicitly frames all four figures as "mmdc-validated" and central to the
Decision section (implementation work item WI-5 references this exact diagram for the stop-condition
spec an implementer would build from). An implementable-specification defect that silently defeats the
ADR's own core gating rule (D-2) is material, not stylistic.

---

## Summary

| ID | Verdict |
|----|---------|
| CV-001-20260707 | VERIFIED |
| CV-002-20260707 | VERIFIED |
| CV-003-20260707 | Out of scope (Major; not panel-adjudicated per protocol) |

---

*Materiality-lens panel. Blind to factual-accuracy and remediation-value lens outputs. No subagents
spawned (P-003). No files edited outside this output path (P-020). All evidence cited by repo-relative
file path; severity/materiality judgments are this panel's own interpretation, labeled as such, not
independently-verified fact beyond the cited primary-source quotes (P-022).*
