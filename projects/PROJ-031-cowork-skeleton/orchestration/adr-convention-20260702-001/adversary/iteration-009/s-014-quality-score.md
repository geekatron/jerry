# Quality Score Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Iteration 9

## L0 Executive Summary
**Score:** 0.86/1.00 (VERIFIED-CRITICALS protocol) | **Old-protocol score (all claimed Criticals counted):** 0.68/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.82)
**One-line assessment:** A genuinely mature, 9-round C4 governance package with an unusually honest residual-disclosure discipline, but 5 newly-VERIFIED Critical findings (all text-only, no-new-machinery fixes) block acceptance at the 0.95 gate — fix the lint scan-path/topology-fallback claims, the self-promotion migration-plan gaps, and the grandfather-baseline temporal anchor, then re-score.

## Scoring Context
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.10)
- **Deliverable Type:** ADR (C4 governance decision) + companion MEDIUM-tier rule draft
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol (2-of-3 majority refutation panel per claimed Critical)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Gate:** 0.95 (elevated C4 tournament gate for this iteration, per invoking task; SSOT baseline H-13 gate is 0.92 for C2+)
- **Iteration:** 9 of a 9-round (to date) adversarial tournament
- **Scored:** 2026-07-06

## Panel-Outcome Reconciliation (Protocol Input)

Ten Critical findings were claimed across the iteration-9 strategy reports (S-001, S-002, S-004, S-011, S-012). Each was independently re-examined by three refutation lenses (factual-accuracy, materiality, remediation-value); a 2-of-3 majority determined the final verdict. Reconciliation below is computed directly from the panel files in `adversary/iteration-009/verify/` (independently re-derived, matches the invoking task's stated outcome exactly):

| Claimed Critical | Strategy | Factual | Materiality | Remediation-Value | Majority | Disposition |
|---|---|---|---|---|---|---|
| RT-001-iter009 | S-001 Red Team | VERIFIED | VERIFIED | VERIFIED | **VERIFIED (3/3)** | Counted |
| RT-002-iter009 | S-001 Red Team | REFUTED | VERIFIED | VERIFIED | **VERIFIED (2/3)** | Counted |
| DA-001-20260706-i9 | S-002 Devil's Advocate | VERIFIED | REFUTED | REFUTED | REFUTED (2/3) | Not counted |
| DA-002-20260706-i9 | S-002 Devil's Advocate | VERIFIED | REFUTED | VERIFIED | **VERIFIED (2/3)** | Counted |
| 004-001 | S-004 Pre-Mortem | VERIFIED | REFUTED | REFUTED | REFUTED (2/3) | Not counted |
| 004-002 | S-004 Pre-Mortem | VERIFIED | REFUTED | REFUTED | REFUTED (2/3) | Not counted |
| 011-001 / CV-001 | S-011 Chain-of-Verification | REFUTED | REFUTED | REFUTED | REFUTED (3/3) | Not counted |
| 012-001 | S-012 FMEA | VERIFIED | REFUTED | VERIFIED | **VERIFIED (2/3)** | Counted |
| 012-002 | S-012 FMEA | VERIFIED | REFUTED | REFUTED | REFUTED (2/3) | Not counted |
| 012-003 | S-012 FMEA | VERIFIED | VERIFIED | REFUTED | **VERIFIED (2/3)** | Counted |

**Verified Criticals: 5** (RT-001-iter009, RT-002-iter009, DA-002-20260706-i9, 012-001, 012-003)
**Refuted Criticals: 5** (DA-001-20260706-i9, 004-001, 004-002, 011-001/CV-001, 012-002)

This matches the invoking task's stated panel outcome exactly. Per protocol rule 1, automatic-REVISE is triggered by the presence of any VERIFIED Critical — independent of the numeric composite.

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (VERIFIED-CRITICALS protocol)** | 0.86 |
| **Weighted Composite (old protocol — all 10 claimed Criticals counted)** | 0.68 |
| **Threshold** | 0.95 (this iteration's elevated C4 gate) |
| **Verdict** | **REVISE** |
| **Verified Criticals** | 5 |
| **Refuted Criticals** | 5 |
| **Strategy Findings Incorporated** | Yes — 9 strategy reports (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013) + 15 refutation-panel files |

## Dimension Scores (VERIFIED-CRITICALS protocol)

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.84 | 0.168 | Exhaustive ID/location/promotion/lint/migration coverage; but 3 verified gaps land squarely on PROJ-031's *stated primary audience* (downstream CoWork/plugin distribution): guidance absent from skeleton builds until untracked M-2 lands (012-001), repo-based-topology fallback non-functional (RT-002), self-promotion migration plan under-scoped by 5 links (DA-002). |
| Internal Consistency | 0.20 | 0.82 | 0.164 | RT-001: repeated "18 files reachable by the scan path" claim is contradicted by the one command the document itself specifies (`find ... -path '*/decisions/*'` cannot match flat `docs/design/*.md`). 012-003: grandfather-baseline anchored to "when the lint ships" contradicts D-4's own "existing/pre-ratification" framing. Two unrefuted advisory Majors compound this (RT-003: "mandatory" tier-overclaim + wrong ADR-M-003/M-013 citation; 013-001: L-2 lint rule lacks the scope qualifier all 4 sibling rules carry, contradicting the twice-stated PROJ-014 grandfather promise). |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | The tournament *process* itself is exceptional (9 rounds, blind-protocol de-duplication against a 17-item residual register, RPN-scored FMEA, 22-claim Chain-of-Verification, 2-of-3 majority refutation panels) — genuinely showcase-quality methodology. Docked for DA-002 (the flagship self-promotion "worked example" is itself under-scoped — the demonstration doesn't fully practice what it teaches) and advisory Majors 003-001 (L-4's matching algorithm is prose-only, unlike its 4 sibling rules) and 013-001. |
| Evidence Quality | 0.15 | 0.87 | 0.1305 | Extraordinarily strong evidentiary discipline elsewhere (S-007 independently re-verified 13 load-bearing claims, all accurate; S-011 independently verified 20/22 extracted claims exactly). Docked because RT-001's "18 files reachable" — a claim repeated 3+ times as authoritative — was never verified against the one command the document itself cites, for 8 prior rounds. |
| Actionability | 0.15 | 0.90 | 0.135 | Every verified finding (and every advisory Major) has a concrete, narrowly-scoped, text-only remediation already specified by the reviewing strategy — fully consistent with the package's own "subtract, don't compensate" doctrine. No new machinery required for any of the 5 verified fixes. |
| Traceability | 0.10 | 0.90 | 0.090 | Extensive R-1...R-17 (+R-A/R-B/R-C) residual register, exact file+line citations throughout both deliverables and all 9 strategy reports, and a changelog reconciling every prior iteration's fixes. |
| **TOTAL** | **1.00** | | **0.8615 ≈ 0.86** | |

## Detailed Dimension Analysis

### Completeness (0.84/1.00)

**Evidence:** The package specifies ID grammar (canonical + closed-set dialect), a two-topology location model, a 13-field frontmatter schema, a 3-path promotion process, a 5-rule lint spec, a 14-row Migration Plan, and a 17-item + 3-lettered residual register — genuinely exhaustive for a MEDIUM-tier naming convention. `docs/design/README.md`/`docs/adrs/README.md` gaps and enforcement-timeline gaps (M-2/M-6/M-9/M-12 all `TBD-Task`, no worktracker entity) are honestly disclosed, not hidden.

**Gaps (verified):** 012-001 — the "guidance carries value on day one, needs no tooling" claim is false for PROJ-031's own named downstream CoWork/plugin audience, because both deliverables live under `projects/`, which is unconditionally stripped from every skeleton build (`phase3-skeleton-generation-design.md:159-160`), and the guidance's real destination (`.context/rules/adr-standards.md`, via M-2) is untracked. RT-002 — the repository-based-topology "consolation" pre-flight one-liner is hardcoded to roots (`projects`, `docs/design`) that topology's own Canonical Location Model table says do not exist/apply, so that named audience's collision-safety fallback is non-functional, not merely "no lint coverage." DA-002 — the ADR's own self-promotion (M-9) migration-plan repair scope names only 1 of at least 6 relative links that will break on execution.

**Improvement Path:** Add the disclosure sentences already drafted by the reviewing strategies (all text-only): qualify line ~675's "day one" claim; either parameterize the pre-flight command for the repository-based topology or honestly narrow the D-5 claim; extend M-2/M-9's repair-scope enumeration to the 5 additional links DA-002 identifies.

### Internal Consistency (0.82/1.00)

**Evidence:** S-007's independent 13-point verification log found zero discrepancies; S-011's Chain-of-Verification independently confirmed 20 of 22 extracted claims exactly (including the complex D-4 grandfather-count reconciliation). The package's overall self-consistency, after 8 prior rounds, is very high.

**Gaps (verified):** RT-001 — the document repeats "18 files reachable by the scan path" (D-4, the L-3 row, the M-6 regression-test acceptance criterion) as a single authoritative figure, but the one command it specifies as implementing that scan structurally excludes the 3 canonical `docs/design/*.md` files (no `decisions/` path segment exists there) — the true reachable count under the cited command is 15, not 18. 012-003 — the grandfather-baseline is anchored to "when the lint first ships" (an undated future event), which is inconsistent with D-4's own framing of grandfathering as a courtesy for *pre-existing, pre-ratification* legacy ADRs; because the dialect remains SOFT-`MAY`-permitted indefinitely, this creates a growing, unstated amnesty window for ADRs minted after ratification but before M-6 ships.

**Improvement Path:** Correct the "18 files reachable" claim to match the actual command (two-clause `find`, or an honest count correction) at all 3 citing locations; anchor the grandfather baseline to the ratification date (2026-07-05/06) or explicitly disclose the amnesty-window growth risk as a named residual.

### Methodological Rigor (0.87/1.00)

**Evidence:** The adversarial-review methodology applied to produce and validate this package is itself exemplary: 9 tournament rounds, a documented "subtract, don't compensate" doctrine that closed 8 of 10 iteration-5 Criticals by deletion rather than compensating machinery, RPN-scored FMEA, 22-claim Chain-of-Verification, and — this iteration — a 2-of-3-majority, 3-lens (factual/materiality/remediation-value) refutation panel applied to every claimed Critical, which is a meaningfully more rigorous verification discipline than typical single-pass adversarial review.

**Gaps:** DA-002 shows the flagship "worked example of self-compliance" (this ADR's own scheduled Path-2 self-promotion, M-9) is itself under-scoped — a rigor lapse in the one place the document is most explicitly modeling correct behavior for future authors. Two unrefuted advisory Majors compound this: 003-001 (L-4's "ID↔location" matching algorithm is prose-only and non-executable as written for a real subset of the grandfathered corpus, unlike L-1/L-2/L-3/L-7's literal regexes) and 013-001 (L-2 is the one lint rule of five lacking the scope qualifier every sibling rule carries, an asymmetry that survived 8 prior rounds).

**Improvement Path:** Extend M-2/M-9's link-repair enumeration (DA-002); add an explicit match procedure + scope-narrowing disclosure to L-4 (003-001); scope L-2 to the same roots as its siblings or add the 4 PROJ-014 files to the grandfather baseline (013-001).

### Evidence Quality (0.87/1.00)

**Evidence:** Both the deliverables and the reviewing strategy reports demonstrate unusually strong evidentiary discipline — Glob/Grep/Read verification is used pervasively rather than assumed, inference is explicitly labeled per P-022, and independent spot-checks (S-007: 13/13 accurate; S-011: 20/22 accurate) corroborate the bulk of the package's factual claims.

**Gaps:** RT-001 is fundamentally an evidence-quality failure: a load-bearing quantitative claim ("18 files reachable by the scan path"), repeated as authoritative across 3 locations, was never verified against the one artifact — the specified `find` command — that would have falsified it, for 8 prior review rounds. 012-001 is a related pattern: an affirmative, present-tense value claim ("carries value... on day one") was made without checking it against the skeleton-generation strip-set design that directly contradicts it for the stated audience.

**Improvement Path:** No new practice is needed — the package already has the verification habit (Glob/Grep-before-claim) that would have caught both gaps; apply it retroactively to the two corrected claims and re-verify after the text edits land.

### Actionability (0.90/1.00)

**Evidence:** Every one of the 5 verified findings, and every unrefuted advisory Major, carries a concrete, narrowly-scoped, text-only remediation (e.g., "add one sentence," "correct one citation," "parameterize one command") that requires no new lint rule, ledger, gate, or schema field — fully consistent with the package's own ratified subtraction doctrine. The Migration Plan (M-1..M-14) already provides an execution scaffold with owners and gating status for the larger structural items.

**Gaps:** None of the 5 verified fixes have been applied as of this scoring pass (expected mid-tournament); Migration Plan rows M-2/M-6/M-9/M-12 remain `TBD-Task` with no worktracker entity or GitHub Issue, which is itself honestly disclosed rather than hidden.

**Improvement Path:** Apply the 5 verified text-only fixes; open worktracker Task entities for M-2/M-6/M-9/M-12 per this package's own H-32 GitHub-issue-parity discipline once this repository's rule applies.

### Traceability (0.90/1.00)

**Evidence:** The 17-item + 3-lettered (R-A/R-B/R-C) residual register, the changelog spanning v1.0 through v1.10, and exact file+line citations throughout both deliverables and all 9 iteration-9 strategy reports together constitute an unusually complete traceability chain — every finding in this scoring pass could be independently re-derived from primary sources.

**Gaps:** Minor only — 012-002 (refuted; not weighted) noted the ADR↔companion-rule-file relationship pattern lacks a dedicated schema field, and 007-002 (Minor, Constitutional) noted the PS Integration "Pending" items are not cross-linked to Migration-Plan rows. Neither is load-bearing.

**Improvement Path:** Optional: add a one-line cross-reference from PS Integration to the relevant Migration Plan rows (007-002).

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency / Evidence Quality | 0.82 / 0.87 | 0.92+ | **RT-001-iter009:** Correct the "18 files reachable by the scan path" claim (D-4, L-3 row, M-6 acceptance criterion) to match the actual `find` command's behavior — either fix the command (two-clause `find` covering flat `docs/design/*.md` and nested `projects/*/decisions/*.md`) or correct the count to 15 and disclose the `docs/design/` scan gap. |
| 2 | Completeness | 0.84 | 0.92+ | **RT-002-iter009:** Ship a topology-parameterized pre-flight command for the repository-based topology, or narrow the D-5 "receives... for collision-safety" claim to admit the manual fallback does not currently cover that topology either. |
| 3 | Completeness / Methodological Rigor | 0.84 / 0.87 | 0.92+ | **DA-002-20260706-i9:** Extend M-2/M-9's cross-link repair scope to name and repair all 5 additional relative links (3× `../FEEDBACK-LOG.md`, 1× `subtraction-pass-notes.md`, 1× rule-draft's `ADR-PROJ031-003` link) before M-9 is treated as executable. |
| 4 | Completeness | 0.84 | 0.92+ | **012-001:** Add one disclosure sentence at the "Downstream/plugin disclosure" paragraph stating plainly that until M-2 executes and a subsequent skeleton build is cut, a distributed plugin install carries no trace of this convention at all. |
| 5 | Internal Consistency | 0.82 | 0.92+ | **012-003:** Anchor the grandfather-baseline's temporal reference to the ratification date (2026-07-05/06) rather than "when the lint ships," or explicitly disclose the post-ratification amnesty-window growth risk as a named residual. |
| 6 (advisory) | Internal Consistency | 0.82 | — | **RT-003-iter009 (unrefuted Major):** Fix the ADR-M-003→ADR-M-013 citation and downgrade "mandatory" to SHOULD-consistent language in the Rationale section. |
| 7 (advisory) | Methodological Rigor | 0.87 | — | **013-001 (unrefuted Major):** Scope L-2 to the same roots as its 4 sibling lint rules, or add the 4 PROJ-014 files to the grandfather baseline. |
| 8 (advisory) | Methodological Rigor | 0.87 | — | **003-001 (unrefuted Major):** Add an explicit match procedure to L-4 (hyphen-normalization + scope-narrowing disclosure for the EPIC/FEAT/STORY-in-project-`decisions/`-dir case). |

## Composite-Protocol Comparison (Transparency)

| Protocol | Composite | Verdict | Basis |
|----------|-----------|---------|-------|
| **VERIFIED-CRITICALS (this report)** | **0.86** | REVISE | Only the 5 findings that survived 2-of-3 majority refutation are weighted as Critical-severity evidence; refuted findings and re-derivations of disclosed R-1..R-17 residuals carry no dimension weight. |
| **Old protocol (all 10 claimed Criticals counted at face value)** | **~0.68** | REVISE (deeper band) | Counting DA-001 (out-of-mandate precedent-document defect, already covered by disclosed R-B), 004-001 (eng-architect's default output never enters the ADR namespace), 004-002 (an unrelated project-isolation pytest module, not an ADR-lifecycle rule), and CV-001/011-001 (a defensible "near-zero" aggregate-hedge reading, disclosed 5x elsewhere in the same document) as if each were a genuine, load-bearing defect would double the Critical-severity hits landing on Completeness (5), Internal Consistency (4), and Evidence Quality (4), dropping those dimensions to roughly 0.55-0.65 each and pulling the composite down to the "significant gaps" band. |

**Why the gap matters:** The ~0.18-point difference between the two protocols is the quantified value of the VERIFIED-CRITICALS refutation panel for this package — it demonstrates that a majority of this iteration's claimed Critical findings (5 of 10) were either restatements of already-disclosed residuals (CV-001 restates a fact disclosed 5x in the document; RT-002 substantially restates R-10), out-of-mandate (DA-001 targets a different document, already bucketed under the non-gating M-10/R-B pattern), or a materiality overreach (004-001, 004-002 — real facts that do not bear on ADR identity/collision-safety). Without the panel, a naive scorer would have both over-penalized the package and directed remediation effort at findings that do not actually need to change anything about the ratified convention.

## Residual Register Status (Context, Not Findings)

The package's own disclosed residual register (R-1 through R-17, plus R-A/R-B/R-C, PM-009) was independently re-examined across all 9 strategy reports and consistently judged a valid, honest MEDIUM-tier posture — not overclaimed coverage. No strategy this iteration re-opened any of R-1..R-17 as a fresh finding; several (R-9, R-10, R-11, R-12, R-13, R-14, R-15, R-16, R-17) were explicitly checked and confirmed still accurate against the live filesystem. This register is a genuine asset of the package and was correctly excluded from dimension scoring per the invoking task's instruction (rule 2).

## Leniency Bias Check
- [x] Each dimension scored independently before computing the composite
- [x] Evidence documented for each score (file+line citations traced through the panel reconciliation table)
- [x] Uncertain scores resolved downward (Completeness and Internal Consistency held at 0.82-0.84 despite the package's overall maturity, because 5 VERIFIED Criticals is a genuine, non-trivial signal at a 0.95 gate)
- [x] First-draft calibration considered and rejected as inapplicable — this is a 9th-iteration, heavily mature artifact, scored accordingly above the 0.65-0.80 first-draft band
- [x] No dimension scored above 0.95; only Actionability and Traceability approach 0.90, each with a specific, disclosed limiting factor
