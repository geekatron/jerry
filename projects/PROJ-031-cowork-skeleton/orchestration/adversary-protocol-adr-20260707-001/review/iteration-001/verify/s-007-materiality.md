# Refutation Panel — Materiality Lens — S-007 Findings (iteration 1)

> **Lens:** Materiality (does the claimed defect genuinely undermine the ADR — wrong decision,
> unimplementable spec, or false evidence — or is it a style/edge-case issue?)
> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-007-findings.md`
> **Target deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
> **Scope:** Critical findings only (CC-001, CC-002) per refutation-panel mandate. Major/Minor
> findings (CC-003, CC-004, CC-005) are out of scope for this panel.
> **Default:** REFUTED on uncertainty (anti-inflation default).

---

## CC-001-20260707-iter1: RSK-1 Mitigation Is the Logical Inverse of DEFAULT-REFUTED

**Verdict: REFUTED**

The underlying textual inconsistency is real — line 707's Risks-table cell states "DEFAULT-REFUTED
biases toward *keeping* claims," while the ADR defines DEFAULT-REFUTED identically and consistently
elsewhere (line 74: "default is: does not count"; line 381: "DEFAULT-REFUTED, blind to each other";
line 590: "REFUTED on uncertainty (the anti-inflation default)") as biasing toward *discarding*
claims under uncertainty. That much of the finder's factual observation is not in dispute. However,
materiality requires more than a true internal inconsistency: it requires that the defect change the
decision, make a spec unimplementable, or constitute false evidence about the world. This does none
of the three. The error is confined to one clause in one Risks-table cell (line 707) describing *why*
RSK-1 is mitigated; it does not appear in, and does not alter, the Decision section (D-1, line 381)
or the L1 Technical Implementation default rule (line 590), both of which state DEFAULT-REFUTED
correctly and are the operative specification an implementer would build from. RSK-1's mitigation
also lists three other independent controls in the same cell ("factual lens is evidence-anchored...
anti-leniency mandate... convergence discriminator") that remain valid and unaffected by the
erroneous clause, so the risk is not left substantively unmitigated even though one supporting
sentence is worded backwards. This is a real but narrow style/internal-consistency defect confined to
risk-register prose, not a defect that changes the ADR's decision, renders any work item
unimplementable, or misstates a verifiable fact about the tournament record — REFUTED per the
"style/edge-cases REFUTED even if true" instruction.

---

## CC-002-20260707-iter1: Verification Invocation Granularity Is Self-Contradictory and Empirically Falsified

**Verdict: VERIFIED**

Independent verification performed in this panel (Glob, this session) confirms the finder's
filesystem claims exactly: `orchestration/adr-convention-20260702-001/adversary/iteration-009/verify/`
contains precisely 15 files organized as 5 report-prefixed groups (`s-001`, `s-002`, `s-004`, `s-011`,
`s-012`) × 3 lens suffixes. Reading `s-012-refutation-factual.md` in that directory confirms one file
adjudicates all three of that report's Critical findings (012-001, 012-002, 012-003) together in a
single verdict document — this directly contradicts the ADR's own WI-1 invocation-contract clause at
`decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:588`, "Input = the
single claimed Critical (id, severity, evidence, affected dimension)" (singular), while the same
sentence's opening clause at line 586 states the call cadence is "one call per lens per
Critical-bearing report." These two clauses of one sentence cannot both be literally true for any
report with more than one Critical, as `s-012`'s three Criticals in iteration-009 concretely
demonstrate. This is a genuine, self-contained textual contradiction verifiable from the ADR text
alone (no external citation needed to see clauses 586 and 588 conflict), and it is compounded by the
Cost Model formula at line 624-626 ("3 × (number of claimed Criticals)"), which — cross-checked
against the ADR's own Context section (line 144: "Of 10 claimed Criticals...") — implies 30 files
would be needed for iteration-009, not the 15 that this panel independently confirmed exist. The
defect is material: it leaves WI-1's acceptance criteria (the central new-agent contract this ADR
proposes, Work-Item Decomposition line 727, "one-invocation-per-lens contract") genuinely ambiguous
about the input schema an implementer must build — one Critical per call, or a report's full set
batched into one call — which is exactly the "unimplementable spec" condition the materiality lens
targets, and it also undermines the Cost Model argument used to justify the criticality-proportional
design choice (D-1 Option C) and the RSK-4 mitigation, both of which cite a formula not supported by
the ADR's own referenced evidence.

---

## Summary

| ID | Verdict |
|----|---------|
| CC-001-20260707-iter1 | REFUTED |
| CC-002-20260707-iter1 | VERIFIED |
