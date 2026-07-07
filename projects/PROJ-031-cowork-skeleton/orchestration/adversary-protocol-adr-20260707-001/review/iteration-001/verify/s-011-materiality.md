Materiality Refutation Panel — S-011 Chain-of-Verification findings, iteration 1

Lens: materiality. Question per Critical: does the finding genuinely undermine the ADR (wrong
decision, unimplementable spec, false evidence) — as opposed to a style/edge-case nit? DEFAULT
REFUTED IF UNCERTAIN.

Target: projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-011-findings.md
Deliverable under review: projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md

Scope note: only the two Critical-severity findings (CV-001-20260707-i1, CV-002-20260707-i1) are
adjudicated per the panel task scope ("Attempt to REFUTE each Critical"). CV-003-20260707-i1 is
Major severity and out of scope for this panel.

---

## CV-001-20260707-i1 — "18 verification-panel files" false citation (FU-log iteration 8)

**Verdict: VERIFIED**

Confirmed by direct filesystem listing: `orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/` contains exactly 12 files (3 lenses x 4 Critical-bearing reports: S-001, S-002, S-004, S-012), not 18. The cited source, `orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:36`, itself states "18 verification-panel files ... (factual / materiality / remediation-value lenses x 4 Critical-bearing reports: S-001, S-002, S-004, S-012)" — 3 x 4 = 12, an internal arithmetic contradiction in the cited source, and the filesystem confirms 12 over 18. The ADR propagates the false "18" figure in three separate locations: `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:206` (Constraint c-004), `:364` (D-6 rationale), and `:625-626` (Cost model, "~15-18 verifier files per C4 round"). This is material: it is false evidence, repeated three times, directly supporting the ADR's cost-proportionality justification (c-004, Consequences Negative #1) and its own "honest costs" / evidentiary-rigor claims — not a stylistic or edge-case nit.

## CV-002-20260707-i1 — Invocation-contract granularity contradiction (per-report vs. per-Critical)

**Verdict: VERIFIED**

Confirmed by direct evidence: iteration-9 (ADR-convention) had 10 claimed Criticals from 5 reports (S-001, S-002, S-004, S-011, S-012) per `orchestration/adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md:21,36-37`, and the `verify/` directory contains exactly 15 files (5 reports x 3 lenses), not 30 (10 claims x 3) — a direct Glob listing confirms 15 files. The FU-log iteration-8 factual-lens file for S-004 (`orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/s-004 pre-mortem analysis (iteration 8, verified-criticals protocol)-refutation-factual.md:9-12`) contains verdicts for both PM-001-iter8 and PM-002-iter8 in one document, confirming panels are organized per-report, bundling multiple claimed Criticals per file. Yet the ADR's own text is self-contradictory across three locations: the L1 invocation contract (`decisions/ADR-...-001-verified-criticals-methodology.md:585-587`) says calls happen "per lens per Critical-bearing report" but describes Input as "the single claimed Critical" (singular); the Cost model (`:624-625`) states "cost ~ 3 x (number of claimed Criticals)" (claim-level, which would be 30 for iteration-9, not the cited 15-18); and Fig. 4's PANELS label (`:555`) says "3 lenses per Critical." This is material — it is an unimplementable-as-written spec that directly affects WI-1's acceptance criteria and contradicts the very cost figures used to justify the D-1 option-C choice, not a wording nit.

---

## Summary

| ID | Verdict |
|----|---------|
| CV-001-20260707-i1 | VERIFIED |
| CV-002-20260707-i1 | VERIFIED |
