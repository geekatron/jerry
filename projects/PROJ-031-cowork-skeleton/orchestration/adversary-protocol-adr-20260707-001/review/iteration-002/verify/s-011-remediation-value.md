# Refutation Panel — Remediation-Value Lens (S-011 Chain-of-Verification, iteration 2)

> Lens question: would fixing this finding materially improve the ADR's decision quality, or is
> the fix churn/machinery-adding? Default REFUTED if uncertain. Blind to other lens panels.

## Scope

- **Target findings file:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-011-findings.md`
- **Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Criticals adjudicated:** CV-001-20260707, CV-002-20260707 (per protocol, only Critical-severity findings are panelled; CV-003-20260707 is Major and out of scope for this panel)

---

## CV-001-20260707 — Flagship "fabricated-verification" anecdote misattributes the catching mechanism

**Verdict: VERIFIED**

Cross-checked against the two primary sources the finder cites. `.../adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md` lines 43-58 (Verified-Criticals Disposition table) lists exactly six panel-adjudicated Criticals (002-001, 002-002, 004-001, 012-004, 013-001, CV-001-i010) — none concerns the PR-template claim. The same report's "Unrefuted Majors/Minors (Advisory)" table (lines 144-163, row `RT-001-iter010`) explicitly classifies the PR-template catch as an **S-001 Red Team, Major** finding, with the report's own protocol note that "no refutation panel runs against non-Critical findings under this protocol" — i.e., RT-001-iter010 never entered any 3-lens panel. `post-ceiling-fix-notes.md` lines 55-67 (Cluster 3) independently re-verifies the same fact and credits no panel mechanism either.

This is not churn: the misattributed anecdote is the ADR's single most load-bearing evidentiary citation for D-1 (add a new Verify stage) and D-6 (add a new `adv-verifier` agent) — it appears three times (Context, L1 Item 2, Decision Rationale) and directly underwrites the "Why C is chosen" / Decision Rationale paragraphs' causal claim that *independence via the new panel mechanism* is what closed this gap. The actual record shows the existing blind finder rotation (S-001 Red Team, zero new machinery) already caught it. Correcting the attribution is a targeted, subtraction-consistent text fix (reattribute or drop the anecdote) that directly changes whether the ADR's strongest argument for its central proposed change (a new T1 agent + new template) still holds — this is a substantive decision-quality fix, not gold-plating.

---

## CV-002-20260707 — Figure 3 permits a VERIFIED Critical to bypass remediation, contradicting D-2 and Figure 2

**Verdict: VERIFIED**

Independently re-traced the Figure 3 mermaid source in the deliverable itself (ADR lines 533-557): `Q1{"Any VERIFIED Criticals this round?"} -- "Yes" --> Q2{"...RECUR..."}`; `Q2 -- "No: fresh stream..." --> Q3{"Running verified protocol already?"}`; `Q3 -- "Yes" --> Q4{"RT-M-010 ceiling reached?"}` — with `FIX` reachable only via the `Q2="Yes"` edge, and no edge from the `Q3="Yes"` branch into `FIX`. This confirms a literal path (Q1=Yes, Q2=No, Q3=Yes) that reaches the ceiling-check node without passing through remediation. D-2 (line ~404, "Only panel-VERIFIED Criticals trigger automatic-REVISE") and Figure 2 (lines 510-513, `Verified --> AutoReviseGate: blocks PASS regardless of composite` then `AutoReviseGate --> Remediated`) both state the gating is unconditional once a Critical is VERIFIED, with no recurrence qualifier. The three artifacts are mutually inconsistent as drawn.

This is not over-literal nitpicking of a diagram nobody will read as code: Figure 3 is explicitly one of the "four mmdc-validated figures central to the Decision section" and the ADR names "implementable specification" as a fitness criterion (WI-4/WI-5 downstream implementers are expected to build from these figures). A silently-adopted implementation of Figure 3 as drawn would let a genuinely panel-VERIFIED Critical (already cleared 2-of-3 independent review) skip remediation under a specific but reachable condition — reintroducing exactly the "unresolved Critical claims counted as non-issues" failure mode this entire ADR exists to close. The suggested fix (remove the post-Q1 recurrence branch, or add an edge from that branch into `FIX`) is a small, cheap, clarifying correction to an already-drawn diagram — it does not add new machinery, and its absence carries real downstream risk. High remediation value.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| CV-001-20260707 | VERIFIED | Fix corrects the ADR's flagship evidentiary anecdote supporting its central proposed change (D-1/D-6); confirmed misattribution via primary source cross-check; fix is subtraction-consistent, not machinery-adding. |
| CV-002-20260707 | VERIFIED | Fix corrects a genuine diagram-logic defect in an "implementable specification" figure that could let a VERIFIED Critical bypass remediation; confirmed by independently retracing the mermaid source; fix is a small clarifying edit, not new machinery. |

---

*Panel: remediation-value lens. Blind to factual-accuracy and materiality lens panels. No subagents spawned (P-003). Evidence cited by repo-relative file path and line number (P-022); severity/materiality judgments beyond the remediation-value question are out of this panel's scope and are not re-litigated here. No employer-internal references or absolute filesystem paths introduced (hygiene).*
