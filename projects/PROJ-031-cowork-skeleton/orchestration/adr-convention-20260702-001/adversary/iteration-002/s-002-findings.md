# Devil's Advocate Report: ADR-PROJ031-004 (ADR Identifier, Location, Promotion Convention) + adr-standards-rule-draft.md

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95, user-raised above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-002 Devil's Advocate, iteration 2, blind independent reviewer)
**H-16 Compliance:** Verified via `Glob` file-existence check only (no content read, per blind protocol) — `s-003-findings.md` and `s-010-self-refine-findings.md` both present in `.../adversary/iteration-002/` prior to this execution, confirming Steelman + Self-Refine ran before this Devil's Advocate pass.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Role Assumption](#role-assumption) | Scope of critique, H-16 confirmation |
| [Assumption Inventory](#assumption-inventory) | Explicit/implicit assumptions challenged |
| [Findings Table](#findings-table) | All counter-arguments, severity, evidence |
| [Finding Details](#finding-details) | Full analysis of Critical/Major findings |
| [Response Requirements](#response-requirements) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Summary](#summary) | Overall assessment |

---

## Role Assumption

**Deliverable challenged:** ADR-PROJ031-004 (canonical `ADR-adr-convention-001`), decision to adopt Scheme B (subject-encoded, domain-slug ADR identity) as Jerry's canonical ADR convention, plus its companion rule draft.

**Scope of critique:** Per invoking task, priority targets are (1) the promotion-frequency assumption, (2) whether the promotion mechanic actually preserves citation continuity, (3) whether the scheme survives 50+ projects, (4) slug-governance failure modes.

**Criticality:** C4. **H-16 confirmed** (see header). Mandate: construct the strongest possible case that this ADR is wrong, incomplete, or overconfident — targeting the load-bearing promotion-frequency belief and the citation-continuity mechanic specifically, as instructed.

**Method note:** All factual claims below are independently re-verified against the live repository via `Glob`/`Grep`/`Read` (evidence excludes any file under `.../adversary/` other than this output, per blind protocol). Where I could not independently verify a claim (e.g., specific git commit hashes not accessible without Bash/git tooling), I label it explicitly as **unverifiable-by-this-reviewer**, per P-022.

---

## Assumption Inventory

| # | Assumption (explicit/implicit) | Challenge |
|---|---|---|
| A-1 | (Explicit) "3/3 framework ADRs arrived by promotion" is clean, decisive evidence that promotion is the normal path and the citation-break risk is real and recurring. | Is the underlying promotion *event* actually as clean as portrayed? See DA-001. |
| A-2 | (Explicit) "The author usually knows the intent at birth" (bimodal refinement) — framework-relevance is knowable and declarable at ADR-authoring time. | Does the ADR's own authorship behavior contradict this? See DA-003. |
| A-3 | (Implicit) A per-domain-slug sequence + `sort \| uniq -d` CI lint is sufficient governance for slug-uniqueness at scale. | Is the named enforcement mechanism (M-5b arbiter) real, or aspirational? Does it address the *actual* named risk (synonymy) vs. exact-string collision? See DA-002, DA-006. |
| A-4 | (Implicit) The scheme "survives 50+ projects" (per invoking task framing, tracking BUG-006's own 50+-ADR collision-risk threshold). | Is this quantitatively demonstrated anywhere, or merely asserted by analogy to the *old* scheme's proven failure at scale? See DA-004. |
| A-5 | (Explicit) The sensitivity analysis identifies a rigorous tipping point "C2 ≳ 22" deciding B vs. C. | Is this a real univariate threshold, or an interpolation between two bundled multi-weight scenarios dressed as a clean sensitivity result? See DA-005. |
| A-6 | (Implicit) Grandfathering + lint scope (`decisions/` + `docs/design/` + bounded `work/.../{ENTITY}/` paths) is fully specified and deterministic ("zero-token... no central registry"). | Is the L-4 dialect↔location check for EPIC/STORY dialects actually bounded, or open-ended across an unconstrained `work/` tree? See DA-007. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260702iter2 | Flagship citation-continuity evidence is contradicted by an omitted, independently-verifiable historical record showing the actual promotion event left dangling SSOT references and unresolved traceability debt | **Critical** | `projects/PROJ-030-bugs/reviews/BUG-006-c4-rescore-iter2.md:6,52,152,200,202,229` | Evidence Quality, Traceability |
| DA-002-20260702iter2 | The named slug-governance mitigation (M-5b "ps-architect... automated fuzzy-match" arbiter) does not exist in the current ps-architect agent, and ps-architect's own configured ADR output-naming template matches neither proposed grammar | Major | `skills/problem-solving/agents/ps-architect.governance.yaml:31` vs. ADR-PROJ031-004 M-5b row | Actionability, Completeness |
| DA-003-20260702iter2 | The "author usually knows framework-relevance at birth" premise is directly contradicted by this ADR's own authorship: it is unambiguously framework-scope yet was NOT authored under the recommended domain-slug identity | Major | ADR-PROJ031-004 Meta-Note (lines ~561-569); D-3 text | Internal Consistency, Methodological Rigor |
| DA-004-20260702iter2 | "Survives 50+ projects" is asserted but never quantitatively stress-tested; the only comparable quantitative collision analysis in the corpus (BUG-006) was performed for the *old* scheme, not the new one | Major | `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md:19,104`; ADR-PROJ031-004 R-6 | Completeness, Evidence Quality |
| DA-005-20260702iter2 | The sensitivity "tipping point... C2 ≳ 22" overstates rigor: it is a linear interpolation between two bundled, three-variable reweighting scenarios, not a derived univariate threshold | Major | `.../explore/trade-study.md:246-292` | Methodological Rigor |
| DA-006-20260702iter2 | The one control that addresses the explicitly-named taxonomy risk (slug *synonymy*, e.g. `agent-design` vs `agent-definition`) is marked non-gating, while the gating lint (M-6/L-3) only catches exact-string duplicates, not synonymy | Major | ADR-PROJ031-004 Migration Plan M-5b row; Negative Consequences #3; R-3 | Actionability, Completeness |
| DA-007-20260702iter2 | L-4 "Dialect↔location" lint for EPIC/STORY dialects is specified to scan an unbounded `work/.../{ENTITY}/` path tree, undermining the "deterministic, zero-token, no central registry" enforcement claim | Minor | `adr-standards-rule-draft.md:193` (L-4 row) | Methodological Rigor |

---

## Finding Details

### DA-001: The core "promotion is free / citation continuity preserved" claim is contradicted by an omitted historical record of the exact same promotion event [CRITICAL]

**Claim Challenged:** ADR-PROJ031-004 §Rationale, argument 3: "100% of framework ADRs (3/3) arrived by promotion, and each one incurred an ID change and a citation break — one of which (`ADR-PROJ007-001/002`) is *still* unrepaired..." and §Options B: "This is a paid promotion tax with a git receipt... B would have prevented every dollar of that tax." The whole tipping-point argument (§Promotion-Frequency Sensitivity) rests on this promotion history being clean, decisive evidence that "the corpus has already voted" for B.

**Counter-Argument:** The ADR names only 2 of the 3 framework-ADR promotion events as evidence (the PROJ-007 pair via BUG-006's remediation commit) and never engages with the third — the EPIC-002 promotion of what is now `docs/design/ADR-output-path-resolution-001.md`. I independently located a directly on-point, pre-existing, non-adversarial-package document scoring that exact promotion event: `projects/PROJ-030-bugs/reviews/BUG-006-c4-rescore-iter2.md`. It states, verbatim:

- Line 6: "...the ADR ID collision remains unresolved (ADR is named `ADR-output-path-resolution-001` in a namespace that breaks the SSOT's `ADR-EPIC002-001` chain)..."
- Line 152: "ADR renamed to `ADR-output-path-resolution-001.md` removes the direct `ADR-EPIC002-001` collision. The `quality-enforcement.md` SSOT references `ADR-EPIC002-001` for the strategy-selection ADR... this is a DIFFERENT document, and no file with that name exists in `docs/design/`."
- Line 200: "The naming convention inconsistency between this ADR (domain-first) and its three peers... creates a discoverability traceability gap... The numbering is now ambiguous."
- Line 202: "`quality-enforcement.md` References section... reads `ADR-EPIC002-001 | Strategy selection...` This entry needs updating... The current state is that a SSOT reference points to a file that cannot be found."
- Line 229 (verification table): "CC-003/CV-001/FM-014: ADR ID collision with SSOT — **PARTIALLY RESOLVED**. Direct ID collision eliminated by rename. New issue: naming convention inconsistency... SSOT `ADR-EPIC002-001` reference now dangling."

This document is a C4 re-score (iteration 2) of the identical promotion this ADR cites as its flagship "paid tax" evidence, and it shows the rename did **not** cleanly restore citation continuity — it eliminated one collision and produced a new, explicitly-flagged, at-the-time-unresolved dangling-SSOT-reference problem plus an ongoing "numbering is now ambiguous" traceability gap. (Note, per P-022: I confirmed the *currently live* `quality-enforcement.md` References entry for `ADR-EPIC002-001` — visible in my own system context — does now correctly point to `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md`, a path I verified exists via `Glob`. So the specific dangling-reference instance has since been fixed. That does not rescue the argument: it demonstrates the "zero-churn" claim is empirically false for this exemplar — real remediation work, across at least two iterations, was required to fully repair it.) ADR-PROJ031-004's References table cites only `BUG-006-adr-naming-evaluation.md` (ref #6); it never cites or reconciles with `BUG-006-c4-rescore-iter2.md`, despite iteration-1 adversarial review having specifically performed a "count reconciliation" on this exact EPIC-002 promotion (closing SM-004) — and still missing this document.

**Impact:** The central empirical premise of the tipping-point argument — "the corpus has already voted, promotion is free once you do it right" — is weaker than presented. The evidence shows real promotions, even executed by careful agents, produce **residual, multi-iteration traceability debt**, not the clean one-time `git mv` the L0 Executive Summary promises. If this is representative, the "3/3 promotions, zero re-pointing" framing overstates the case for Scheme B specifically on the promotion-continuity axis — which is the ADR's own stated tie-breaker.

**Dimension:** Evidence Quality, Traceability

**Response Required:** Either (a) locate and cite `BUG-006-c4-rescore-iter2.md` explicitly in the Rationale/References and reconcile its "PARTIALLY RESOLVED"/"dangling"/"ambiguous" findings with the "paid tax... prevented every dollar" framing, revising the confidence language accordingly, or (b) provide affirmative evidence that this rescore's flagged residual issues were fully closed and are not representative of expected Path-1/Path-2 promotion friction going forward.

**Acceptance Criteria:** A revised Rationale/Sensitivity section that either downgrades the "zero re-pointing"/"paid tax" claim to acknowledge measured multi-iteration remediation cost, or demonstrates (with citation) that the residual gaps identified in the rescore are fully closed and non-recurring.

---

### DA-002: The named slug-governance safeguard (M-5b) does not exist, and the responsible agent's own naming template already diverges from both proposed grammars [MAJOR]

**Claim Challenged:** ADR-PROJ031-004 Migration Plan M-5b: "Name the taxonomy arbiter (TBR-2)... the `ps-architect` agent SHOULD run an automated fuzzy-match (Levenshtein/token-overlap) of any new slug against the `docs/design/README.md` registry at ADR-creation time, and flag near-duplicates... for human adjudication."

**Counter-Argument:** I read the live `ps-architect.governance.yaml` (`skills/problem-solving/agents/ps-architect.governance.yaml`). It contains no fuzzy-match capability, no reference to a `docs/design/README.md` registry, no slug-taxonomy guardrail in `input_validation`/`output_filtering`, and no `capabilities.allowed_tools` entry that would support this behavior. More materially: its `output.location` field (line 31) is hardcoded to `projects/${JERRY_PROJECT}/decisions/{ps-id}-{entry-id}-adr-{decision-slug}.md` — a **fourth, previously uncatalogued ID pattern** that matches neither the canonical `ADR-{domain-slug}-NNN` grammar (D-1/ADR-M-001) nor the permitted dialect `ADR-{PROJECT-ID}-NNN` grammar (D-3/ADR-M-003). This pattern does not appear anywhere in the ADR's own 9-family corpus catalog, meaning the corpus-survey (which the ADR treats as exhaustive, having already added a "missed 9th family" correction in iteration 1) is still incomplete: it never inspected the agent configuration that actually authors these files. M-5b is listed in the Migration Plan as "No (soft process, but owned)" for gating — i.e., ratification does not require this mechanism to exist, be implemented, or even be assigned a real owner beyond a description in a table row.

**Impact:** The one governance mechanism intended to prevent exactly the taxonomy-sprawl risk the ADR itself names (Negative Consequence #3, Risk R-3, MED probability) is currently vaporware, is not required before ratification, and the agent it names is not configured to comply with the scheme at all. Ratifying this ADR does not, by itself, cause any agent to behave differently.

**Dimension:** Actionability, Completeness

**Response Required:** Either mark M-5b as a ratification-gating item (consistent with the treatment already given to M-2b and M-6), or explicitly disclose that slug governance is 100% manual/advisory until M-5b is separately implemented and scheduled with an owner and deadline. Separately, add a Migration Plan item to update `ps-architect.governance.yaml`'s `output.location` to match the ratified grammar — the corpus catalog and gating regression test should account for this configuration, not just the two files fixed in Deliverable 2 (Fix 1/Fix 2).

**Acceptance Criteria:** A Migration Plan row for updating `ps-architect.governance.yaml` `output.location`, and an explicit gating/non-gating decision for M-5b with rationale, rather than the current silent "No" with no fallback description of interim manual process.

---

### DA-003: The load-bearing "authors know framework-relevance at birth" premise is falsified by this ADR's own creation [MAJOR]

**Claim Challenged:** §Promotion-Frequency Sensitivity, "Which regime is real? The bimodal refinement": "the author usually knows the intent at birth — the 2-for-2 / 1-of-3 evidence shows framework-relevance is a knowable, declarable property at authoring time, not a retroactive guess (`advocate-domain-slug.md:133`)." This premise directly supports D-3's design ("An ADR whose scope is **known at birth to be framework-wide**... SHOULD NOT use the dialect").

**Counter-Argument:** ADR-PROJ031-004 is, by its own repeated self-description, unambiguously framework-scope at birth — it is a governance convention "affecting the whole ontology" (Criticality header), explicitly targeted at `.context/rules/` (AE-002), and its own Meta-Note states it "is itself framework-scope (it governs the whole framework)." There is no plausible reading under which its author did not know, at the moment of creation, that this decision was framework-wide. Per ADR-M-003 (the rule draft's own text): "An ADR whose scope is known at birth to be framework-wide... SHOULD NOT use the dialect — it SHOULD take a domain slug from the start to avoid the Path-2 rename." Yet the ADR was filed as `ADR-PROJ031-004` (the discouraged dialect), not `ADR-adr-convention-001` (the canonical form) — a decision the Meta-Note frames as compelled by "the invoking task mandated this exact path," not by any uncertainty about scope. This is a live, present-tense instance of exactly the D-3-abuse risk the ADR itself names (R-4/FM-3: "Authors abuse the dialect, re-introducing rename churn... MED probability, LOW impact") — except this is not a hypothetical future author, it is the ADR's own author, on the ADR that defines the rule, choosing the discouraged path for a case where framework-scope was maximally obvious.

**Impact:** If the single cleanest, least-ambiguous case of "framework-relevance known at birth" in the entire corpus (this ADR itself) did not result in domain-slug-at-birth behavior, the bimodal-refinement claim that "framework-relevance is a knowable, declarable property at authoring time" is weaker than the confidence language ("not a retroactive guess") suggests. Authors facing real deadline/task-mandate pressure (as this one explicitly did) will defer to dialect even when they know better — meaning the promotion-frequency argument's supporting mechanism (authors self-select correctly) has a demonstrated failure rate of at least 1-for-1 in the available sample of "obviously framework-scope" cases.

**Dimension:** Internal Consistency, Methodological Rigor

**Response Required:** Acknowledge this ADR as a *disconfirming* data point for the "authors know at birth" claim (not merely a "worked example of Path-2," as the Meta-Note currently frames it), and either revise R-4's probability estimate upward or add an explicit mitigating mechanism beyond "SHOULD-guidance" (e.g., a pre-commit prompt/checklist item requiring authors to affirmatively declare scope before choosing dialect vs. canonical).

**Acceptance Criteria:** R-4/FM-3 revised to reflect an observed (not merely hypothetical) instance of dialect-despite-known-scope, with either an upgraded probability rating or a concrete non-"SHOULD"-only mitigation.

---

### DA-004: "Survives 50+ projects" is asserted, not demonstrated [MAJOR]

**Claim Challenged:** Invoking-task framing and ADR-PROJ031-004's implicit claim that the domain-slug scheme resolves the scale problem BUG-006 identified. BUG-006 (`projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md:19`): "fails usability tests for discoverability, reference clarity, and **collision resistance at scale (50+ ADRs)**." Line 104: "Impact: Low at current scale (6 ADRs), but becomes critical at 50+ ADRs where collisions become statistically inevitable."

**Counter-Argument:** BUG-006's 50+-ADR collision-risk statement was made about the **old** entity-ID scheme (where collision arises from reused worktracker entity IDs like `EPIC002` across projects). The new domain-slug scheme trades that risk for a **different** collision surface: independently-authored, free-text, kebab-case subject slugs with no central registry (rejected by c-006) and no birthday-paradox-style probability model computed anywhere in the ADR, the rule draft, or the explore/ trade study. The corpus currently contains exactly 3 live domain-slug ADRs (`agent-design`, `routing-triggers`, `output-path-resolution`) — far too small a sample to extrapolate collision behavior at 50+ projects, each potentially minting several ADRs across concurrent branches. The ADR's own R-6 explicitly concedes: "No registry-free scheme fully eliminates this... reduced and detected, not structurally prevented" — but gives no quantified residual collision probability at 50+ scale, unlike BUG-006's explicit scale-based severity claim for the scheme it replaces.

**Impact:** The claim that the new scheme "survives" 50+ projects is a qualitative hope backed by a reactive CI lint (post-hoc detection, not prevention), not a quantitative demonstration. Given that BUG-006 — the ADR's own foundational source — treats 50+-scale collision risk as the decisive severity multiplier for the *old* scheme, the absence of an equivalent analysis for the *new* scheme is a significant evidentiary gap precisely where the invoking task asked for scrutiny.

**Dimension:** Completeness, Evidence Quality

**Response Required:** Provide (or explicitly commission as a gating migration item) a quantitative collision-probability estimate for domain-slug minting at projected project/ADR counts (e.g., a simple birthday-paradox calculation given an estimated vocabulary size of distinguishable domain slugs), or explicitly downgrade the "survives 50+ projects" framing to "reduces, does not eliminate, collision risk; residual risk at scale is unquantified."

**Acceptance Criteria:** Either a numeric estimate with stated assumptions, or explicit acknowledgment in the L0/Consequences section that the 50+-project collision-resistance claim is qualitative, not quantitative, mirroring the honesty already applied to R-6.

---

### DA-005: The "C2 ≳ 22" tipping point overstates the rigor of a two-point, multi-variable interpolation [MAJOR]

**Claim Challenged:** §Promotion-Frequency Sensitivity: "The approximate crossover is **C2 ≳ 22**." Sourced to `trade-study.md:246-292`.

**Counter-Argument:** I read `trade-study.md:240-294` directly. The "High-promotion weight vector" is not a single-variable sweep of C2 — it simultaneously changes three weights: C2 (16→28), C5 (12→6), and C7 (8→4), "Σ=100" constrained (line 250). The document itself states the crossover is between exactly two discrete, fully-computed scenario vectors (baseline vs. high-promotion), then reports "approximate crossover: C2 ≳ 22" as if a clean univariate threshold in C2 alone had been derived. Since three weights move together in a fixed bundle (not independently), stating a standalone "C2 ≳ 22" implies a precision (a specific breakpoint for one variable, holding others fixed) that was never actually computed — only two bundled endpoints (16/12/8 and 28/6/4) were scored, and a linear interpolation between exactly two points was verbally rounded to "≳22."

**Impact:** For a C4 governance decision explicitly built around "the single assumption that decides A/C-vs-B" (the ADR's own words), presenting an interpolated guess between two bundled scenarios as a derived sensitivity threshold overstates methodological rigor. A reader could reasonably conclude a rigorous single-variable sensitivity sweep was performed when it was not.

**Dimension:** Methodological Rigor

**Response Required:** Either compute an actual single-variable sweep (varying C2 alone while holding C5/C7 fixed at baseline, or clearly presenting the compound nature of the scenario) and report the true breakeven point, or rephrase "approximate crossover: C2 ≳ 22" to explicitly state it is an interpolation between two bundled multi-weight scenarios, not an isolated-variable threshold.

**Acceptance Criteria:** Revised sensitivity language that does not imply single-variable precision from a two-point bundled-scenario interpolation.

---

### DA-006: The gating lint catches exact-string duplicates only; the named taxonomy risk is synonymy, which nothing gating actually checks [MAJOR]

**Claim Challenged:** Migration Plan M-5b marked "No (soft process, but owned)" for gating, while M-6 (the lint) is the sole ratification-blocking control for slug governance. Negative Consequences #3: "Domain-slug taxonomy can sprawl (`agent-design` vs `agent-definition`). The lint catches exact collisions, not synonymy."

**Counter-Argument:** The ADR itself admits, in the same breath, that (a) the taxonomy-sprawl/synonymy risk is real (Con #3, R-3 rated MED probability), and (b) the only mechanism that would catch it (M-5b fuzzy-match arbitration) is explicitly non-gating, while (c) the mechanism that *is* gating (L-3, `sort | uniq -d`) is explicitly acknowledged to not catch that exact risk. This is a direct mismatch between what is required for ratification and what the ADR's own risk register says needs mitigating. The gating bar is set at the wrong control.

**Impact:** Ratification per this ADR's own Migration Plan can proceed while the specific, named, MED-probability risk (taxonomy sprawl/synonymy) remains fully unmitigated by anything gating. This is not hypothetical: the corpus already shows organic precedent for exactly this failure mode elsewhere (`adr-cli-integration` → `adr-cli-integration-v2`, cited by the ADR itself at `adr-convention-standards-research.md:68` as an example of ungoverned disambiguation).

**Dimension:** Actionability, Completeness

**Response Required:** Either promote M-5b (or some interim manual equivalent, e.g. a mandatory `docs/design/README.md` review step before minting a new slug) to gating status, or explicitly document in the Risk table why a MED-probability, named risk is acceptable to leave without any gating control at ratification.

**Acceptance Criteria:** M-5b (or an equivalent interim control) added to the gating column, or an explicit risk-acceptance rationale in R-3.

---

### DA-007: L-4 lint scope for EPIC/STORY dialects is not path-bounded, undermining the "deterministic, zero-token" claim [MINOR]

**Claim Challenged:** `adr-standards-rule-draft.md` L-4 row: "For `ADR-EPIC{NNN}-NNN` / `ADR-STORY{NNN}-NNN`: the entity prefix equals `origin_entity` frontmatter AND appears in the containing `work/.../{ENTITY}/` path." Enforcement Design intro: "Deterministic, zero-token, no central registry."

**Counter-Argument:** Unlike L-1/L-2/L-3 (scoped explicitly to `projects/*/decisions/` and `docs/design/`), L-4's EPIC/STORY branch must search an unbounded `work/` subtree per project (arbitrary depth, e.g. the actual STORY-015 example lives at `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-.../STORY-015-.../ADR-STORY015-001-....md` — four directory levels deep). No glob pattern, depth limit, or file-type filter is specified for this scan, unlike the other rules which give exact regex/glob scopes.

**Impact:** Minor — this is a specification-completeness gap, not a logic error; the check is still computable, just under-specified for an implementer to write deterministically without guessing the traversal bound.

**Dimension:** Methodological Rigor

**Response Required:** Add an explicit glob bound for the L-4 EPIC/STORY case (e.g., `projects/*/work/**/{ENTITY}/ADR-*.md`).

**Acceptance Criteria:** L-4 row specifies a concrete glob/traversal pattern, matching the specificity given to L-1/L-2/L-3.

---

## Response Requirements

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Reconcile the promotion-continuity narrative with `BUG-006-c4-rescore-iter2.md`. Either cite and account for the documented multi-iteration remediation cost of the EPIC-002 promotion event, or provide evidence the residual gaps it flagged are fully closed and non-representative.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-002:** Add a Migration Plan item for `ps-architect.governance.yaml` `output.location` alignment; resolve M-5b's gating status.
- **DA-003:** Revise R-4/FM-3 to reflect the observed (not hypothetical) self-referential dialect-despite-known-scope instance; strengthen mitigation beyond "SHOULD."
- **DA-004:** Provide a quantitative (or explicitly-labeled-qualitative) 50+-project collision-risk statement, mirroring BUG-006's own scale-based severity framing.
- **DA-005:** Correct the "C2 ≳ 22" tipping-point framing to disclose its two-point bundled-scenario derivation.
- **DA-006:** Promote a synonymy-catching control to gating status, or explicitly justify leaving a MED-probability named risk ungated.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-007:** Add explicit glob bound to L-4's EPIC/STORY branch.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002, DA-004, DA-006: corpus catalog still incomplete (ps-architect's own naming template uncatalogued); 50+-scale collision analysis absent; synonymy risk uncovered by any gating control |
| Internal Consistency | 0.20 | Negative | DA-003: the ADR's own authorship directly contradicts its "authors know framework-relevance at birth" premise |
| Methodological Rigor | 0.20 | Negative | DA-005, DA-007: sensitivity-analysis rigor overstated (bundled two-point interpolation presented as univariate threshold); L-4 lint under-specified |
| Evidence Quality | 0.15 | Negative | DA-001, DA-004: the flagship promotion-continuity exemplar is contradicted by an omitted, directly on-point historical record; scale-survival claim unquantified |
| Actionability | 0.15 | Negative | DA-002, DA-006: named mitigations (M-5b) are non-gating and effectively unimplemented; gating lint (M-6) does not address the named taxonomy risk |
| Traceability | 0.10 | Negative | DA-001: the ADR's own References section omits the single most relevant piece of evidence for its central claim |

**Estimated composite impact:** 1 Critical (~-0.10 to -0.15 on Evidence Quality/Traceability) + 5 Major (~-0.05 to -0.10 each, concentrated on Completeness/Methodological Rigor/Actionability) + 1 Minor (~-0.01 to -0.03 on Methodological Rigor). Given the 0.95 engagement gate (above the 0.92 SSOT floor), these findings are individually and collectively material to whether this C4 deliverable clears that elevated bar in its current form.

---

## Summary

7 counter-arguments identified (1 Critical, 5 Major, 1 Minor), concentrated exactly on the four priority targets specified for this review. The most serious finding (DA-001) is that the ADR's own flagship evidence for "promotion preserves citation continuity" — the EPIC-002 → `ADR-output-path-resolution-001` promotion — is independently documented elsewhere in this repository (`BUG-006-c4-rescore-iter2.md`) as having left dangling SSOT references and unresolved traceability ambiguity across at least two review iterations, and this document is neither cited nor reconciled by the ADR despite a prior adversarial pass specifically reconciling adjacent EPIC-002 counting details. The remaining Major findings show that the scheme's slug-governance safeguards (M-5b) are aspirational and non-gating against a named, conceded risk (synonymy); that the "authors know framework-relevance at birth" premise is falsified by the ADR's own authorship choice; that "survives 50+ projects" is asserted without the quantitative rigor applied to the scheme it replaces; and that the sensitivity analysis's headline tipping-point number overstates what was actually computed. None of these findings invalidate the underlying architectural argument for subject-encoded identity (the two promotion-independent rationale arguments — ontology-fit and discoverability — are not directly attacked here), but they materially weaken the promotion-frequency evidentiary chain that the ADR itself calls "the single assumption that decides" the winner, and several are concrete, fixable gaps in the enforcement/migration design. Recommend **REVISE** before this package can be expected to clear the 0.95 engagement gate.
