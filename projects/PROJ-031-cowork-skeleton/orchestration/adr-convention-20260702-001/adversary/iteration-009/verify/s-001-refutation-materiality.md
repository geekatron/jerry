# Refutation Panel — Materiality Lens (Iteration 9, S-001 Red Team Findings)

> Panel mandate: attempt to REFUTE every Critical finding in `adversary/iteration-009/s-001-findings.md`. Default to REFUTED if uncertain. Materiality test: does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention), or is it a negligible-probability×impact edge case / cosmetic wording / style preference (REFUTE even if factually true)?
>
> Scope: only Critical-severity findings are in scope for this panel. RT-003-iter009 (Major) and RT-004-iter009 (Minor) are out of scope and receive no verdict here.
>
> Blind pass: this panel did not read any sibling refuter output or other lens panels for iteration 9.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Method](#method) | What was independently checked |
| [RT-001-iter009 Verdict](#rt-001-iter009-the-lints-specified-scan-command-cannot-see-the-3-canonical-docsdesign-adrs-it-claims-to-cover) | Verdict + reasoning |
| [RT-002-iter009 Verdict](#rt-002-iter009-the-repository-based-topology-consolation-fallback-pre-flight-one-liner-does-not-reach-that-topologys-own-adr-home) | Verdict + reasoning |
| [Summary](#summary) | Tally |

---

## Method

Independently re-read (a) the full S-001 iteration-9 findings report, (b) the current ADR (`ADR-PROJ031-004-adr-identifier-convention.md`) sections cited by the findings (D-4 grandfather-count reconciliation ~L225-231, D-5 topology-scope note ~L233-235, Risks R-10 ~L469, L-3/L-4 rule rows ~L683-684, Migration M-6 ~L536), (c) the companion rule draft (`adr-standards-rule-draft.md`, L-3 row ~L177, Frozen-and-Grandfathered ~L94, pre-flight command ~L188-199), and (d) `subtraction-pass-notes.md` (the residual register, specifically R-10, R-13, and the prior Critical-disposition tables) to check whether either Critical is already fully disclosed elsewhere (which would make it non-material/duplicate) or is genuinely novel and load-bearing. Re-ran the filesystem checks the report claims independently (`Glob docs/design/ADR-*.md`, `Glob projects/*/decisions/ADR-*.md`) rather than trusting the report's numbers at face value.

---

## RT-001-iter009: The lint's specified scan command cannot see the 3 canonical `docs/design/` ADRs it claims to cover

**Verdict: VERIFIED**

**Independent filesystem check.** `Glob docs/design/ADR-*.md` returns exactly 3 files (`ADR-agent-design-001.md`, `ADR-output-path-resolution-001.md`, `ADR-routing-triggers-001.md`), none under any `decisions/` path segment. `Glob projects/*/decisions/ADR-*.md` returns exactly 15 files. Both counts match the report's claims exactly, confirming the report's premise is not fabricated.

**Command-behavior check.** The specified command (`ADR-PROJ031-004-adr-identifier-convention.md:407`; identical at `adr-standards-rule-draft.md:188`) is `find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' ...`. GNU/BSD `find -path` matches the full traversed path against the pattern without treating `/` specially, so `-path '*/decisions/*'` requires the literal substring `/decisions/` to appear anywhere in the path. `docs/design/ADR-agent-design-001.md` does not contain that substring, so the predicate evaluates false for all 3 canonical files regardless of `docs/design` being passed as a search root. This is deterministic `find` semantics, not a hypothetical.

**Is this material, or a documentation nicety about a not-yet-built tool?** It is material for two independent reasons, both inside the current document's own evidentiary claims (not merely the future lint's eventual correctness): (1) The document repeats, verbatim, "18 files reachable by the scan path" as an authoritative, single-sourced figure across three locations (D-4 reconciliation `:227,229`; L-3 row `:683`/`adr-standards-rule-draft.md:177`; M-6 grandfather regression test `:536`/`adr-standards-rule-draft.md:181,201`) and explicitly attributes the underlying mechanism ("exactly what L-3 runs in CI") to the one command shown. That figure is demonstrably false against the one command it cites — the true reachable count under the shown command is 15, not 18. This is a self-inflicted Evidence Quality/Internal Consistency defect inside a document whose entire iteration-9-worthy credibility rests on having systematically hunted down and disclosed this exact class of defect eight times already (R-9, R-10, R-13, R-14, R-15, R-16, R-17 are all "the specified mechanism doesn't reach X" disclosures). A ninth, undisclosed instance of the identical defect class is not cosmetic wording — it is the review's own stated failure mode recurring. (2) Substantively, it means the 3 highest-stakes framework-governance ADRs — the exact population the ADR's own Criticality section says this convention exists to protect — would silently fall outside grammar (L-1), duplicate-ID (L-3), and relationship-target (L-7) checking once M-6 ships as specified, with the document's own regression-test gate (`the 18 files reachable by the scan path... pass L-1`) failing to catch this because the regression corpus as specified only ever contained 15, not 18, of the files it claims. Confirming this required only running the one command the document itself gives, against the one filesystem it itself describes — precisely the "the verification the document did not perform for this specific claim" argument in the report's own Scoring Impact table, and it is correct.

**Distinguishing from an already-disclosed residual (checked against R-10 and R-13).** R-10 (`ADR-PROJ031-004-adr-identifier-convention.md:469`) discloses that the hard-coded scan misses (a) entity-embedded ADRs and (b) the repository-based topology's `decisions/` home — i.e., location *classes the scan structurally cannot reach at all*. R-13 discloses a title-slug-tail extraction false negative in the `sed`/`grep` post-processing, unrelated to root traversal. Neither residual discloses that the `docs/design/` root itself — a root the document explicitly claims IS reached ("Across the scanned roots (`projects/*/decisions/` + `docs/design/`)", `:683`) — is in fact not reached for its 3 flat-layout files due to the `-path '*/decisions/*'` filter. This is a distinct, previously-undisclosed defect, not a restatement of R-10 or R-13.

**Conclusion:** Not a negligible-probability edge case and not cosmetic wording. It is a factually verified, deterministic command-behavior defect that directly contradicts a repeated, load-bearing quantitative claim ("18 files reachable") used to gate M-6's acceptance criteria, and it silently drops lint coverage for exactly the tier ("framework-wide governance") the ADR's own Criticality statement says is the highest-stakes population this convention protects. This genuinely undermines "collision-free identity" and "honest promotion" for that population. **VERIFIED.**

---

## RT-002-iter009: The repository-based-topology "consolation" fallback (pre-flight one-liner) does not reach that topology's own ADR home

**Verdict: VERIFIED**

**Textual check.** D-5's topology-scope note (`ADR-PROJ031-004-adr-identifier-convention.md:235`) reads: "L-1/L-3/L-7 do not reach that home ([R-10]), so that audience receives the guidance plus the zero-tooling pre-flight one-liner only — not lint coverage — for collision-safety." The pre-flight one-liner given anywhere in either document (`:407`; `adr-standards-rule-draft.md:188`) is hardcoded to `find projects docs/design ...`. The Canonical Location Model (`adr-standards-rule-draft.md:81`) and the worktracker-topology note (`ADR-PROJ031-004-adr-identifier-convention.md:395`) both state the repository-based topology's ADR home is `{RepositoryRoot}/decisions/` with **no `projects/` directory at all**. Running the hardcoded command in that topology searches a nonexistent `projects/` root and a `docs/design/` root that (per RT-001-iter009, and regardless of that finding, per the topology's own definition) does not contain that repo's ADRs — so it returns nothing for that topology's actual corpus.

**Checked against R-10 for redundancy (is this already fully disclosed, making it immaterial/duplicate?).** R-10 (`:469`) discloses, in the context of the automated lint (L-1/L-3/L-7), that "the hard-coded scan... misses... the repository-based topology's `{RepositoryRoot}/decisions/` home... PROJ-031's own named downstream audience." Since the pre-flight one-liner is textually the identical command to the one R-10 describes as failing to reach that home, a fully rigorous reader could in principle infer the manual command shares the same blind spot. However, D-5's own sentence structure asserts an affirmative claim beyond R-10's negative framing: it says the audience "receives... the pre-flight one-liner... for collision-safety" — i.e., that running the manual command yields some collision-safety value for that audience — in the very same sentence that cites R-10 for the point that the underlying scan mechanism does not reach that audience's ADR home at all. If the scan (per R-10) provides zero coverage of that location, then the sentence's claim that the audience "receives... for collision-safety" the identical mechanism is not merely under-qualified, it is affirmatively wrong for the one artifact (their own `decisions/` corpus) collision-safety is supposed to protect: running the command yields empty output that is indistinguishable from "no collisions found," when the true state is "nothing was searched." This creates exactly the false-assurance failure mode the threat-actor profile targets, for the project's own explicitly named downstream audience — not a hypothetical or generic audience.

**Materiality.** PROJ-031's stated purpose is to produce a distributable Jerry CoWork/plugin skeleton, and the repository-based topology is explicitly named as an audience its own downstream adopters run. Being told "you get a working manual fallback" when the fallback (as literally specified) silently returns nothing for that topology is a materially worse and undisclosed position than "no lint coverage, but you're on your own honestly" — it actively misinforms the one population the ADR's Decision section chose to call out by name. This is not a style preference or a low-probability edge case: it is a concrete, deterministic, easily-triggered failure (any repository-based adopter who copies and runs the one command given) affecting the "adoptable MEDIUM-tier convention" and "honest promotion" purposes for the standard's stated target users.

**Conclusion:** The overlap with R-10 narrows the finding (the underlying mechanism gap is already named), but D-5's specific "receives... for collision-safety" framing makes an additional, uncorrected claim of manual-fallback efficacy that R-10's own text does not make and does not neutralize. This is a genuine, material overclaim, not a cosmetic wording nit. **VERIFIED.**

---

## Summary

| ID | Severity (per report) | Verdict | Basis |
|----|------------------------|---------|-------|
| RT-001-iter009 | Critical | **VERIFIED** | Filesystem-confirmed `find -path '*/decisions/*'` cannot match `docs/design/*.md` (no `decisions/` segment); contradicts a repeated, load-bearing "18 files reachable" claim; drops the highest-stakes ADR population from claimed lint coverage; distinct from all disclosed residuals (R-9, R-10, R-13). |
| RT-002-iter009 | Critical | **VERIFIED** | D-5's "receives... the pre-flight one-liner... for collision-safety" claim is affirmatively false for the repository-based topology (no `projects/` root exists there); goes beyond R-10's disclosed mechanism gap by asserting manual-fallback value that does not exist for PROJ-031's own named downstream audience; creates a genuine false-assurance risk for real adopters. |

Both Criticals survive this materiality-lens refutation attempt.

*No subagents invoked (P-003). Scope limited to the assigned target file and cited context files (P-020). All verdicts cite file+line; inference explicitly labeled where used (P-022). No employer-internal references or absolute filesystem paths introduced into this artifact's substantive content (file-path citations use repo-relative paths per the source documents' own convention).*
