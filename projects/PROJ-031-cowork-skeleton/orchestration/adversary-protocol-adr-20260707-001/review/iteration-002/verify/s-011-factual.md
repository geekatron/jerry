# Refutation Panel — Factual Lens (S-011 Chain-of-Verification, iteration 2)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What was checked and how |
| [Verdicts](#verdicts) | Per-Critical VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Roll-up |

---

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-011-findings.md` (S-011 Chain-of-Verification).

Lens: **Factual accuracy only** — does the cited defect exist verbatim at the cited file+line locations in the deliverable and its cited primary sources? Restatements of disclosed limits, stale references, or misreads of the source text are REFUTED. Default REFUTED if uncertain. Only Critical-severity findings (CV-001-20260707, CV-002-20260707) are in scope; CV-003-20260707 is Major and out of scope for this panel per the VERIFIED-CRITICALS protocol (panels adjudicate Criticals only).

Deliverable checked: `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`.

---

## Verdicts

### CV-001-20260707 — Flagship "fabricated-verification" anecdote misattributes the catching mechanism

**Verdict: VERIFIED**

The ADR's Context section states verbatim (deliverable lines ~181–187): "...was reaffirmed across iterations 6, 7, 8, and 9, and was caught only by the iteration-10 refutation panel's factual lens (`.../adversary/iteration-010/post-ceiling-fix-notes.md:55-65`)." Independent read of the primary source, `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md`, shows the Verified-Criticals Disposition table (lines 43–58) lists exactly six claimed Criticals adjudicated by the 3-lens panel — 002-001, 002-002, 004-001, 012-004, 013-001, CV-001-i010 — none of which is the PR-template claim. The PR-template finding is tracked separately as **RT-001-iter010**, attributed explicitly to **S-001 Red Team** and listed in the same report's "Unrefuted Majors/Minors (Advisory)" table (lines 144–159) with the note "no refutation panel runs against non-Critical findings under this protocol." `iteration-010/post-ceiling-fix-notes.md` Cluster 3 (lines 55–66) corroborates the same finding without crediting any panel mechanism. The misattribution recurs in the ADR's L1 section (line ~622, "This is the lens that would have caught the fabricated PR-template claim") and Decision Rationale (lines ~414–417, "...correctly discarded restatements and one false claim" attributed to "the single intervention" of the 3-lens gate). The defect exists exactly as the finder describes: a Major-severity, panel-untouched finder-strategy catch is credited to the panel mechanism the ADR proposes to institutionalize.

### CV-002-20260707 — Figure 3 permits a VERIFIED Critical to bypass remediation, contradicting D-2 and Figure 2

**Verdict: VERIFIED**

Deliverable Figure 3 (mermaid flowchart, deliverable lines ~534–553) reads exactly as quoted by the finder: `Q1{"Any VERIFIED Criticals this round?"} -- "Yes" --> Q2{"Do findings RECUR across independent rounds?"}`; `Q2 -- "No: fresh stream every round (protocol artifact)" --> Q3{"Running verified protocol already?"}`; `Q3 -- "Yes" --> Q4{"RT-M-010 ceiling reached?"}`. There is no edge from this `Q3="Yes"` branch (nor from anywhere on the Q2=No path) into the `FIX["Owner subtraction-first remediation pass"]` node; only `Q2="Yes"` routes to `FIX`. This is confirmed by direct inspection of the mermaid source — the only inbound edges to `FIX` are `Q2 -- "Yes: convergent (real defect)" --> FIX`, and the only outbound edge from `FIX` is `FIX --> Q4`. Figure 2 (deliverable lines ~488–525), by contrast, states unconditionally `Verified --> AutoReviseGate: blocks PASS regardless of composite` then `AutoReviseGate --> Remediated: owner subtraction-first pass`, with no recurrence-conditional branch. The Decision table's D-2 row (deliverable lines ~404) states "Only panel-VERIFIED Criticals trigger automatic-REVISE" with no recurrence qualifier. Cross-checking the ADR's own Changelog (final table entry, deliverable lines ~858) confirms the iteration-1 remediation pass explicitly left "decision (D-1..D-6), or diagram source" unchanged, so this contradiction is not something already fixed elsewhere in the document. The literal wiring the finder describes is present verbatim in the cited figure, and it does contradict Figure 2 and D-2 as claimed.

---

## Summary

| ID | Verdict |
|----|---------|
| CV-001-20260707 | VERIFIED |
| CV-002-20260707 | VERIFIED |

Both Critical findings from the S-011 report describe defects that exist verbatim at the cited locations in the deliverable and are corroborated by independent reads of the cited primary source files. Neither is a misread, a stale reference, or a restatement of an already-disclosed limitation.

---

*No subagents spawned (P-003). All evidence cited by repo-relative file path. Interpretive judgments are this panel's own assessment, not asserted as independently-authoritative beyond what the cited text states (P-022). Report persisted incrementally per P-002.*
