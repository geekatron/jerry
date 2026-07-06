# Quality Score Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Iteration 10

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Score, verdict, one-line assessment |
| [Scoring Context](#scoring-context) | Deliverables, protocol, thresholds |
| [Verified-Criticals Disposition](#verified-criticals-disposition) | The 6 claimed Criticals and their 2-of-3 panel outcomes |
| [Score Summary](#score-summary) | Composite vs. old-protocol composite |
| [Dimension Scores](#dimension-scores) | Weighted table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence per dimension |
| [Unrefuted Majors/Minors (Advisory)](#unrefuted-majorsminors-advisory) | Findings outside the Critical refutation mandate |
| [Old-Protocol Composite Derivation](#old-protocol-composite-derivation) | Transparency counterfactual |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered actions |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |

---

## L0: Executive Summary

**Score:** 0.88/1.00 (VERIFIED-CRITICALS protocol) | **Old-protocol score:** 0.68/1.00 (if all 6 claimed Criticals were counted as real) | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.85)

**One-line assessment:** After 10 tournament rounds this is a mature, honestly-disclosed C4 governance convention with zero VERIFIED Criticals this iteration, but a recurring table-vs-prose reconciliation seam (independently found by 4 strategies) and one demonstrated evidentiary lapse (a twice-reaffirmed "Glob-verified absent" claim that is false) keep the composite below the 0.95 gate.

---

## Scoring Context

- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11, 797 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11, 253 lines)
- **Deliverable Type:** ADR (ratified decision, `status: ACCEPTED`) + companion MEDIUM-tier rule draft
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol, iteration 10
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Gate (as invoked for this iteration):** 0.95
- **Scored:** 2026-07-06
- **Inputs read:** both deliverables (full); `subtraction-pass-notes.md` (full disposition history, iterations 1–9); all 9 iteration-10 finder reports (`s-001`, `s-002`, `s-003`, `s-004`, `s-007`, `s-010`, `s-011`, `s-012`, `s-013`); all 15 refutation-panel files in `adversary/iteration-010/verify/` (factual, materiality, remediation-value lenses for every claimed Critical).

---

## Verified-Criticals Disposition

Six Criticals were claimed across five strategies in iteration 10. Each was adjudicated by a 3-lens (factual / materiality / remediation-value) refutation panel with a 2-of-3 majority rule (default REFUTE on uncertainty). **Result: 0 VERIFIED, 6 REFUTED** (matches the deterministic panel outcome stated in the invoking task).

| # | ID | Strategy | Claim | Factual | Materiality | Remediation-Value | Majority |
|---|----|----------|-------|---------|--------------|--------------------|---------|
| 1 | 002-001 | S-002 Devil's Advocate | L-4 (ID↔location) undefined/broken for `ADR-EPIC002-001/002` (EPIC-dialect ADRs in a plain project `decisions/` dir) | VERIFIED | REFUTED | REFUTED | **REFUTED** |
| 2 | 002-002 | S-002 Devil's Advocate | Rule draft's 14 bare `R-N` residual citations are unreachable in every CoWork/plugin build | VERIFIED | REFUTED | REFUTED | **REFUTED** |
| 3 | 004-001 | S-004 Pre-Mortem | Deleting an ADR file silently frees its `NNN` for reuse, misdirecting old citations | VERIFIED | REFUTED | REFUTED | **REFUTED** |
| 4 | 012-004 | S-012 FMEA | Grandfather-baseline enumeration (19 items) excludes PROJ-014's 4 bare drafts, which L-2's unscoped wording would otherwise catch | VERIFIED | REFUTED | REFUTED | **REFUTED** |
| 5 | 013-001 | S-013 Inversion | L-1's row definition ("canonical OR dialect") and the "18 files pass L-1" claim contradict each other for `ADR-150-001` | REFUTED | REFUTED | REFUTED | **REFUTED** (unanimous) |
| 6 | CV-001-i010 | S-011 Chain-of-Verification | Canonical Location Model table omits the actual (location, ID-form) pattern of the `EPIC002` dialect pair; L-4 would misfire on them | VERIFIED | REFUTED | REFUTED | **REFUTED** |

**Pattern observed (not itself a scoring override, but informs Internal Consistency below):** four of the six claimed Criticals (002-001, 012-004, 013-001, CV-001-i010) independently converge on the same underlying textual class — a specific rule's *row-level* wording (L-1, L-2, or L-4), read narrowly, appears to contradict a broader grandfather/exemption principle stated in an adjacent paragraph or in D-4's blanket "grandfathered … in place" framing. Every refutation panel confirmed the **factual core is real** (the textual tension exists) but found it does not clear the **materiality** bar (the lint is designed-not-built; the practical disposition is stated unambiguously elsewhere; the worst case is a trivially-overridable MEDIUM-tier advisory on 2–4 already-named legacy files) or the **remediation-value** bar (fixing it changes no observable adoption behavior today). Per the task's Rule 2, this refuted convergence carries **no dimension weight** as a Critical — but the recurring pattern itself (independent strategies repeatedly re-deriving the same seam) is weighed below as a genuine, bounded Internal Consistency signal, distinct from re-litigating the refuted claims themselves.

**Verified Criticals: 0. Refuted Criticals: 6.** Per the task's Rule 1, no automatic-REVISE trigger fires from Criticals this iteration.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (VERIFIED-CRITICALS protocol)** | **0.88** |
| **Composite under old protocol (all 6 claimed Criticals counted as real/unaddressed)** | **0.68** |
| **Gate (as invoked)** | 0.95 |
| **Verdict** | **REVISE** |
| **Verified Criticals** | 0 |
| **Refuted Criticals** | 6 |
| **Strategy Findings Incorporated** | Yes — 9 finder reports + 15 refutation-panel files (iteration 10) |

**Verdict basis:** No VERIFIED Critical exists, so the automatic-REVISE-on-Critical trigger does not fire. The verdict is nonetheless **REVISE** because the weighted composite (0.88) falls in the 0.85–0.91 operational band ("close to threshold, targeted improvements") relative to the invoked 0.95 gate — a score-band determination, not a Critical-triggered one.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.90 | 0.180 | Comprehensive ID/location/frontmatter/promotion/amend/status/lint/residual coverage; genuine gap: cross-installation collision detection for the stated downstream-plugin audience (012-006, unrefuted Major, novel — not R-6/R-10) |
| Internal Consistency | 0.20 | 0.85 | 0.170 | 4 of 6 refuted Criticals independently converged on the same table-row-vs-grandfather-prose reconciliation seam; every panel confirmed the textual tension is real, only its materiality was refuted |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | Trade study + sensitivity analysis + VERIFIED-CRITICALS 3-lens protocol is rigorous; but the "ratification-time baseline" fix is policy-without-procedure (004-002/012-005/013-002, 3 independent unrefuted Majors converging), and RT-001-iter010 shows the verification methodology itself missed a case-sensitivity variant twice |
| Evidence Quality | 0.15 | 0.85 | 0.1275 | Extensive file+line citation and Glob/Grep verification discipline throughout; direct counter-evidence: RT-001-iter010 shows a specific "Glob-verified absent" claim (M-9's PR-template justification) is factually false, reaffirmed across iterations 6, 7, 8, 9 before being caught this iteration |
| Actionability | 0.15 | 0.90 | 0.135 | Guidance is adoptable today with zero tooling; concrete Migration Plan; unrefuted Major 003-001 (SM-001) shows M-2 does not specify stripping ~15 inline tournament tags before the file becomes the auto-loaded rule |
| Traceability | 0.10 | 0.90 | 0.090 | R-1…R-17 + R-A/R-B/R-C residual register with owners and homes; minor cosmetic asymmetry (SR-003) and the refuted-but-real R-N cross-file dependency (002-002) |
| **TOTAL** | **1.00** | | **0.8765 → 0.88** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:** The package covers ID grammar (canonical + dialect), location model (framework/project/repository-based/entity-embedded/frozen/transient), frontmatter schema, promotion (Path 0/1/2), supersede-vs-amend, status vocabulary, a 5-rule lint spec, a Migration Plan (M-1 through M-14), and a 17-item + 3-lettered residual register (R-1…R-17, R-A/R-B/R-C). This is an unusually complete artifact set for a MEDIUM-tier naming convention.

**Gaps (unrefuted, advisory weight):** 012-006 (S-012 FMEA, Major, unrefuted — no refutation panel runs against Majors per this protocol) identifies that the entire collision-detection model (pre-flight one-liner, L-3, `uv run jerry lint adr`) is single-filesystem-tree-scoped, leaving zero cross-installation collision check for PROJ-031's own stated upstream/downstream-plugin distribution model. This is genuinely novel — distinct from R-6 (single-repo branch race) and R-10 (single-repo out-of-scan directories) — and touches the project's actual charter (`adr-standards-rule-draft.md` L5 spec; `phase3-skeleton-generation-design.md:159`). Also unrefuted: 004-001's deletion-then-reuse scenario (refuted at Critical severity, but the underlying observation — no residual names post-deletion `NNN` reuse — was independently confirmed factually accurate by all three refutation panels; only its severity/materiality was refuted, not its existence as a genuine, if narrow, gap).

**Improvement Path:** Add a named residual (parallel to R-6/R-10) for cross-installation collision, per 012-006's proposed wording. Add a SHOULD-NOT-delete guidance line + R-18 residual per 004-001's proposed (declined-as-Critical-but-cheap) mitigation.

### Internal Consistency (0.85/1.00)

**Evidence:** No contradiction was found that survives materiality/remediation-value scrutiny. However, four independent strategies (S-002 Devil's Advocate, S-011 Chain-of-Verification, S-012 FMEA, S-013 Inversion) — using different methodologies — each separately identified essentially the same class of tension: a specific enforcement-rule row (L-1, L-2, or L-4), read narrowly and literally, appears to contradict a broader "grandfathered … in place" principle stated elsewhere (D-4's blanket framing, or the adjacent L-1 grandfather-baseline paragraph at ADR:693/rule-draft:183). Every refutation panel's own **factual lens explicitly confirmed the textual tension is real** ("the cited table rows, file paths, line numbers... all check out"; "the factual core is confirmed") — only the **materiality** (does it block the standard's purpose?) and **remediation-value** (would fixing it change real behavior?) lenses found the tension non-blocking, because the lint is designed-not-built, the practical disposition is stated unambiguously elsewhere (Migration Plan M-11's "Grandfather in place… Zero [cost]" row), and every override is MEDIUM-tier and zero-friction.

**Gaps:** The recurring nature of this seam — this is at minimum the third time (iteration 8's IN-001, iteration 9's implicit closure, iteration 10's 013-001/CV-001-i010/002-001/012-004) that a rule-row-vs-grandfather-prose reconciliation gap has been independently rediscovered — indicates the document's specification tables (L-1, L-2, L-4) are not yet fully self-contained; a reader must cross-reference an adjacent paragraph or D-4 to resolve an apparent contradiction rather than the row itself stating the exemption.

**Improvement Path:** Fold the grandfather-baseline exemption directly into L-1's row definition (as 013-001 itself proposes: "canonical OR dialect OR present on the ratification-time baseline"); add a third Location Model row (or an explicit L-4 scope note) for the EPIC002-class dialect-in-project-`decisions/` pattern, closing the recurring seam at its source rather than relying on adjacent-paragraph reconciliation.

### Methodological Rigor (0.87/1.00)

**Evidence:** The decision methodology is exceptional: a 6-scheme trade study with weighted-sum scoring, an explicit promotion-frequency sensitivity analysis with a stated tipping point and bimodal-refinement discussion, a confidence figure capped against the trade study's own stated ceiling (0.75), and — specific to this review cycle — a disciplined VERIFIED-CRITICALS 3-lens refutation protocol that itself represents methodological maturity (defaulting to REFUTE under uncertainty, requiring 2-of-3 majority).

**Gaps:** Three independent, unrefuted Major findings (004-002 Pre-Mortem, 012-005 FMEA, 013-002 Inversion) converge on the same rigor gap: the "ratification-time, not lint-ship-time" grandfather-baseline fix (012-003, iteration 9) is a *policy* correction stated in prose, with no named *procedure* (no pinned commit SHA, no checked-in filename manifest) for a future M-6 implementer to actually reconstruct "the corpus as of ratification." Separately, RT-001-iter010 (S-001 Red Team, unrefuted Major) demonstrates a verification-methodology blind spot: the claim "no `.github/PULL_REQUEST_TEMPLATE.md` exists — Glob-verified" was reaffirmed as true across iterations 6, 7, 8, and 9, but a case-insensitive check reveals `.github/pull_request_template.md` (lowercase, the GitHub-recognized form) does exist — the verification pattern used (exact-case search) recurred as a blind spot across 4 iterations before being caught.

**Improvement Path:** Add a concrete artifact-generation instruction to M-6 (a checked-in baseline filename list or a pinned git tag/commit reference), per 012-005/013-002's proposed fix. Correct M-9's justification and add the atomicity checklist bullet to the already-existing `.github/pull_request_template.md`, per RT-001-iter010.

### Evidence Quality (0.85/1.00)

**Evidence:** The package's evidentiary discipline is generally excellent — every claim in the 10-iteration corpus is tied to a file+line citation, and iteration 10's own S-011 Chain-of-Verification independently re-checked 19 load-bearing factual claims and found 18/19 clean (94.7%) against the live filesystem.

**Gaps:** The one clean miss (the 19th claim, CV-001-i010) plus RT-001-iter010's direct demonstration that a specific "Glob-verified absent" claim was factually wrong — and wrong in a way that survived three prior review iterations' independent re-verification passes (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019) before this iteration caught it — is a concrete, non-hypothetical evidence-quality defect, not merely a hypothetical risk.

**Improvement Path:** Correct the M-9 row's justification (RT-001-iter010's proposed fix); as a process improvement, verification passes asserting a file's absence should include a case-insensitive / alternate-casing check for conventionally-cased artifacts (e.g., `.github/` templates).

### Actionability (0.90/1.00)

**Evidence:** The convention is explicitly designed to deliver value with zero tooling today (MEDIUM-tier, SHOULD-level guidance), backed by a concrete Migration Plan (M-1 through M-14) and a pre-flight collision one-liner runnable today. Every disposed finding across 10 iterations closed via a specific, concrete, subtraction-doctrine-consistent action (delete the overclaim, correct the command, add one disclosure line) — a strong actionability track record.

**Gaps:** 003-001 (S-003 Steelman, Major, unrefuted) identifies that the rule draft — the one artifact the named downstream audience actually receives once M-2 executes — carries ~15 inline tournament-provenance tags (`RT-002-iter8`, `FM-003-iter8`, etc.) with no glossary of its own (unlike the ADR, which has one), and M-2's Migration Plan row does not specify whether these tags are stripped before the file ships as `.context/rules/adr-standards.md`.

**Improvement Path:** Add a tag-stripping (or footnote-relocation) clause to M-2's close-condition, mirroring the existing M-2/M-9 reciprocal-link atomicity discipline, per SM-001's proposed fix.

### Traceability (0.90/1.00)

**Evidence:** An exceptionally traceable residual register (R-1…R-17, R-A/R-B/R-C) with named homes, owners, and detection signals; every one of the 10 iterations' disposition history is preserved in `subtraction-pass-notes.md` with per-finding IDs; the ADR's own tag glossary (`ST-*`, `RT-*`, `FM-*`, etc.) provides traceability to the originating adversarial strategy.

**Gaps:** 002-002 (refuted at Critical severity, but its factual core — 14 bare `R-N` citations in the rule draft resolve only in the parent ADR, which is unconditionally stripped from every CoWork/plugin build today — was independently VERIFIED by the factual-accuracy panel) remains a real, if non-blocking, cross-file traceability gap for the artifact's actual downstream audience. SR-003 (S-010 Self-Refine, Minor) notes a cosmetic asymmetry: R-16/R-17 carry in-ADR-body `(#risks)` pointers while R-14/R-15 do not.

**Improvement Path:** Either inline a condensed residual summary into the rule draft, or add a permanent (not M-2-timing-scoped) disclosure that `R-N` cross-references are source-repo-only, per 002-002's proposed remediation (declined as Critical, but cheap and consistent with the subtraction doctrine).

---

## Unrefuted Majors/Minors (Advisory)

Per the task's Rule 3, unrefuted Majors carry advisory weight at scorer judgment (no refutation panel runs against non-Critical findings under this protocol). The following were incorporated into the dimension analysis above and did **not** individually block PASS, but collectively support the composite landing in the mid-0.80s rather than at/above the 0.92–0.95 gate:

| ID | Strategy | Severity | One-line | Dimension(s) Affected |
|----|----------|----------|----------|------------------------|
| 002-003 | S-002 | Major | Grandfather regression test verifies only L-1; L-3/L-4/L-7 have no demonstrated dry-run against the real corpus | Methodological Rigor |
| 004-002 | S-004 | Major | Ratification-anchored baseline has no captured artifact (file/tag/SHA) — policy without procedure | Methodological Rigor, Actionability |
| 012-005 | S-012 | Major | Same ratification-baseline procedure gap, independently derived | Methodological Rigor |
| 012-006 | S-012 | Major | Collision-detection model is single-tree-scoped; no cross-installation check for the stated distribution model | Completeness |
| 013-002 | S-013 | Major | Same ratification-baseline procedure gap, independently derived (3rd instance) | Methodological Rigor, Actionability |
| RT-001-iter010 | S-001 | Major | "No PR template exists — Glob-verified" is false; a lowercase-cased template already exists and has for at least 4 iterations | Evidence Quality, Actionability |
| 003-001 (SM-001) | S-003 | Major | Shipped rule draft has ~15 unglossed inline tournament tags; M-2 doesn't specify stripping | Actionability, Completeness |
| 004-003 | S-004 | Minor | `docs/design/` scan clause does not reach nested subdirectories | Traceability |
| CC-101 | S-007 | Minor | AE-002 cited as an independent C4-floor basis slightly before it factually applies (pre-M-2) | Internal Consistency |
| SR-001/SR-002/SR-003 | S-010 | Minor | Register-file (not deliverable) staleness + cosmetic cross-ref asymmetry | Internal Consistency, Traceability |
| 003-002 (SM-002) | S-003 | Minor | No quick-reference entry point for a first-time author | Actionability |

**Note on convergence:** 004-002, 012-005, and 013-002 are three independent strategies re-deriving the same underlying gap (ratification-baseline procedure). This is treated as **one** substantive weakness (weighted once in Methodological Rigor above, not triple-counted), but the fact that three separate methodologies converged on it independently is itself evidence the gap is real and not an artifact of any one strategy's framing.

---

## Old-Protocol Composite Derivation

For transparency, the composite that would result if all 6 claimed Criticals were counted as real, unaddressed findings (i.e., without the VERIFIED-CRITICALS refutation step):

| Dimension | Weight | Old-protocol score | Rationale |
|-----------|--------|---------------------|-----------|
| Completeness | 0.20 | 0.72 | 2 of 6 Criticals (002-002, 004-001) + Major 012-006 unaddressed |
| Internal Consistency | 0.20 | 0.55 | 5 of 6 Criticals hit this dimension (002-001, 004-001, 012-004, 013-001, CV-001-i010) — multiple unresolved contradictions per rubric's 0.5–0.69 band |
| Methodological Rigor | 0.20 | 0.58 | 3 Criticals (002-001, 013-001, CV-001-i010) + 3 converging Majors unaddressed |
| Evidence Quality | 0.15 | 0.85 | Findings' own evidence is strong; deliverable's evidentiary practice is not the primary attack surface of the 6 Criticals |
| Actionability | 0.15 | 0.78 | Remediation paths are known/concrete even under the naive count, but urgency is higher with 6 open Criticals |
| Traceability | 0.10 | 0.75 | 002-002 Critical directly hits this dimension |

Old-protocol composite = (0.72×0.20)+(0.55×0.20)+(0.58×0.20)+(0.85×0.15)+(0.78×0.15)+(0.75×0.10) = 0.144+0.110+0.116+0.1275+0.117+0.075 = **0.6895 → 0.68**

This is consistent with this package's own historical trajectory under comparable naive counting (iteration 6: 0.59 with 7 distinct Criticals; iteration 8: 0.62 with 7 Criticals) — a 6-claimed-Critical iteration lands slightly above that band, as expected.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Internal Consistency | 0.85 | 0.92+ | Fold the grandfather-baseline exemption directly into L-1's own row text (three-way disjunction: canonical / dialect / ratification-baseline-listed) rather than an adjacent paragraph; add a Location Model row or explicit L-4 scope note for the EPIC002-class (dialect prefix in a project `decisions/` dir) pattern. Closes the recurring 4-strategy seam at its source. |
| 2 | Methodological Rigor | 0.87 | 0.92+ | Add a concrete, checked-in artifact (filename manifest or pinned commit/tag) for the ratification-time grandfather baseline in the Migration Plan's M-6 row, per the 3 independently-converging findings (004-002/012-005/013-002). |
| 3 | Evidence Quality | 0.85 | 0.90+ | Correct M-9's "no PR template exists" justification (RT-001-iter010) — the checklist bullet can be added to the existing `.github/pull_request_template.md` at zero cost. |
| 4 | Actionability | 0.90 | 0.93+ | Add a tag-stripping/relocation clause to Migration Plan M-2's close-condition for the ~15 inline tournament-provenance tags in the shipped rule draft (SM-001/003-001). |
| 5 | Completeness | 0.90 | 0.93+ | Register a new residual (R-18 or equivalent) for cross-installation domain-slug collision, naming the manual contribution-time mitigation (012-006). |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score (file+line citations traced through finder reports and refutation panels)
- [x] Uncertain scores resolved downward — composite kept at 0.88, not pushed toward 0.92+ despite zero VERIFIED Criticals, because of the convergent Internal Consistency seam and the demonstrated Evidence Quality lapse (RT-001-iter010)
- [x] Iteration maturity considered, but not used to inflate scores beyond what unrefuted findings support — refuted Criticals carry zero weight per protocol, but their factually-confirmed textual observations (distinct from their refuted severity claims) inform Internal Consistency and Methodological Rigor as bounded, real signals
- [x] No dimension scored above 0.95 without exceptional documented evidence; no dimension scored above 0.90 in this iteration

---

*Scored by adv-scorer (S-014 LLM-as-Judge, VERIFIED-CRITICALS protocol). No subagents spawned (P-003). No files edited outside this output (P-020). All evidence cited by repo-relative file path and line number where available; interpretive judgments (dimension score placement, convergence weighting) are labeled as this scorer's judgment, not independently-verified fact (P-022). No employer-internal references or absolute filesystem paths introduced into this artifact.*
