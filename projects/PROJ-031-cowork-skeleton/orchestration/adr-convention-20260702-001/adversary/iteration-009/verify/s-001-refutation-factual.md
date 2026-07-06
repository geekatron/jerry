# Factual-Accuracy Refutation Panel — S-001 Findings, Iteration 9

## Scope

Lens: FACTUAL-ACCURACY. Target: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-001-findings.md`. Only the two Critical findings (RT-001-iter009, RT-002-iter009) are in scope per the panel mandate. Verdict is VERIFIED or REFUTED; default to REFUTED when the cited defect does not exist at the cited lines in the CURRENT deliverables, or when the finding restates an already-disclosed residual (R-1..R-17 / disposition tables).

## RT-001-iter009 — VERIFIED

**Claim:** The single pre-flight/L-3 scan command `find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' ...` cannot see the 3 canonical `docs/design/` ADRs, because `-path '*/decisions/*'` requires a literal `decisions` path segment and none of the three files sit under one — contradicting the repeated "18 files reachable by the scan path" / "scanned roots (`projects/*/decisions/` + `docs/design/`)" claims.

**Verification:**
- Command reproduced verbatim at `ADR-PROJ031-004-adr-identifier-convention.md:407` and `adr-standards-rule-draft.md:188` — identical `-path '*/decisions/*'` predicate applied uniformly across both hard-coded roots (`projects`, `docs/design`).
- Filesystem-verified: `Glob docs/design/ADR-*.md` and `Glob docs/design/**/ADR-*.md` both return exactly `docs/design/ADR-agent-design-001.md`, `docs/design/ADR-output-path-resolution-001.md`, `docs/design/ADR-routing-triggers-001.md` — none contain a `decisions/` path segment; there is no `docs/design/decisions/` directory anywhere in the repo.
- POSIX `find -path` semantics: the predicate matches the full constructed pathname as a shell glob; `*/decisions/*` requires the literal substring `/decisions/`. None of the 3 canonical paths contain that substring, so the predicate is false for all 3 regardless of the fact that `docs/design` is a specified starting root.
- The document's own D-4 reconciliation (`ADR-PROJ031-004...:227`) and the L-3/M-6 rows (`:683,686`; rule draft `:177,181`) repeatedly assert these 3 files are part of the "18 files reachable by the scan path," and the enforcement table's own phrasing distinguishes "15 dialect files **in `decisions/` dirs**" from "3 canonical `docs/design/` ADRs" (no `decisions/` qualifier) — the asymmetry the finding names is present verbatim in the prose.
- This is a distinct defect from R-10 (out-of-scan location *classes*: entity-embedded ADRs and the repository-based topology's `{RepositoryRoot}/decisions/` home) — R-10 concerns roots the command never visits at all; RT-001 concerns files inside an already-specified root (`docs/design`) that the `-path` filter itself silently excludes. No R-1..R-17 residual, and no disposition-table entry (subtraction-pass-notes.md Critical/Major tables, iter-6/7/8 dispositions), addresses this specific `-path` vs. flat-`docs/design/`-layout mismatch. Confirmed as a genuinely new, factually accurate finding.

## RT-002-iter009 — REFUTED

**Claim:** The pre-flight one-liner offered to repository-based-topology adopters as a "consolation" (D-5, `ADR-PROJ031-004...:235`) does not actually reach that topology's ADR home (`{RepositoryRoot}/decisions/`) because the command hardcodes `projects`/`docs/design` as roots, so the "guidance plus the zero-tooling pre-flight one-liner" framing overstates what that audience actually gets.

**Verification:**
- The underlying defect is already disclosed verbatim in the ADR's own Risk register: **R-10** (`ADR-PROJ031-004-adr-identifier-convention.md:469`) states: "the hard-coded scan `find projects docs/design -path '*/decisions/*'` misses **two whole location classes**... (b) the **repository-based topology's** `{RepositoryRoot}/decisions/` home (no `projects/` prefix), **PROJ-031's own named downstream audience**." This is the identical fact pattern RT-002-iter009 presents as a new discovery.
- The document itself equates the pre-flight one-liner with the L-3 scan mechanism ("which is also exactly what lint L-3 runs in CI," `:403`; "exactly what L-3 runs in CI," rule draft `:185`), so R-10's disclosure that the hard-coded scan misses the repository-based topology's home necessarily covers the pre-flight one-liner too — they are the same command.
- `subtraction-pass-notes.md` confirms R-10 was generalized across iterations 6–7 ("RT-001/RT-002-iter7 generalized," `subtraction-pass-notes.md:174`) specifically to cover this repository-based-topology gap, and iteration-8's DA-001 disposition (`subtraction-pass-notes.md:190`) states the D-5 topology-scope disclosure itself was added *because of* this pre-existing R-10 gap ("underlying gap = the already-registered R-10").
- The target report's own stated scope excludes exactly this class of finding: "The 17 prior Criticals (R-1..R-17...) documented in `subtraction-pass-notes.md` are honestly disclosed residuals, not findings, and are excluded from this report" (`s-001-findings.md:30`). RT-002-iter009 restates R-10 under new packaging (naming the pre-flight one-liner specifically rather than the lint generally) but the cited defect — the hard-coded scan/one-liner not reaching the repository-based topology's `decisions/` home — is the same fact already disclosed at ADR line 469 and cross-referenced at D-5 (`:235`) itself. Per the factual-accuracy lens instruction to refute findings restating an already-disclosed residual, this is REFUTED.

## Summary

| ID | Verdict | Basis |
|---|---|---|
| RT-001-iter009 | VERIFIED | Novel defect: `-path '*/decisions/*'` filter excludes flat `docs/design/*.md` files (no `decisions/` segment exists there); filesystem- and text-confirmed; not covered by any existing R-1..R-17 residual or prior disposition. |
| RT-002-iter009 | REFUTED | Restates R-10 (`ADR-PROJ031-004-adr-identifier-convention.md:469`), an already-disclosed residual the target report's own scope statement excludes; the pre-flight one-liner and the L-3 scan are the document's own stated identical mechanism. |
