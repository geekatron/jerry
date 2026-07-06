# Inversion Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + adr-standards-rule-draft.md)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration 5, independent of other reviewers)
**H-16 Compliance:** S-003 Steelman applied within this package's own iteration history (embedded steelmans for each option, `ADR-PROJ031-004` Options A-F); confirmed per this document's own disclosure at line 67.
**Goals Analyzed:** 6 | **Assumptions Mapped:** 8 | **Vulnerable Assumptions:** 6

> Status note (P-002): this file is being written incrementally. Sections below are populated in order; if truncated mid-run, everything above this line is complete and load-bearing.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Step 1: Goals](#step-1-goals-stated-precisely) | The deliverable's goals, restated measurably |
| [Step 2: Anti-Goals](#step-2-anti-goals-what-would-guarantee-failure) | Inverted failure conditions and whether the package falls into them |
| [Step 3: Assumption Map](#step-3-assumption-map) | Explicit/implicit assumptions with confidence and validation status |
| [Step 4: Stress-Test Findings](#step-4-stress-test-findings-table) | Findings table |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Zero-Governance Null Alternative Re-Examination](#zero-governance-null-alternative-re-examination) | Requested benchmark, independently re-derived |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Finding counts |

---

## Summary

The package has already absorbed four prior full adversarial iterations plus a self-refine pass, and it shows: most "obvious" inversions (rename-on-promotion churn, taxonomy synonymy, waiver self-approval, lint non-existence) are already disclosed with named residual risk IDs. This iteration therefore focused on inversions the package's own extensive self-critique has not yet reached: (1) the enforcement mechanism (M-6) has grown monotonically larger across every remediation pass with no corresponding complexity budget, which is itself an inversion of "how do we guarantee the lint ships" — Critical; (2) the requested zero-governance null-alternative benchmark compares Scheme B against a weaker null than its strongest form, so the benchmark the task explicitly asked for is not fully discharged — Major; (3) the one promotion path that still renames (Path 2) is never itself inverted ("must it rename?") — Major; (4) the package's own authorship is live evidence that the "author defaults correctly" assumption already failed once, with no mechanical fix to the producing agent's decision heuristic (only to its filename grammar) — Major; (5) a downstream-degraded-mode disclosure gap; (6) a structural provenance-verification downgrade (FAIL-checkable in Scheme A/C vs. WARN/best-effort in Scheme B) that is real but never named as a trade-off. Recommendation: **REVISE** — none of these are fatal to the decision itself (Scheme B is not overturned by any of them), but several are fixable-now document gaps consistent with this package's own remediation discipline, and one (M-6 scope growth) is a genuine viability threat to the whole two-tier enforcement design that the document does not yet manage.

---

## Step 1: Goals Stated Precisely

| # | Goal (as stated or inferred) | Measurable form |
|---|---|---|
| G1 | Eliminate promotion-induced citation breakage (the demonstrated BUG-006 / stale `ADR-PROJ007-001/002` wound) | Zero citation re-pointing required for **any** ADR that is promoted from a project into `docs/design/`, regardless of how it was originally named |
| G2 | Preserve provenance (origin) without polluting identity | `origin_project`/`origin_entity` recoverable for 100% of ADRs, verifiably correct, without requiring the identifier to encode it |
| G3 | Deterministic, registry-free collision detection | `sort \| uniq -d` (or equivalent) catches 100% of exact-identity collisions with no central counter/server process |
| G4 | Stay within MEDIUM tier (no new HARD rule) | Zero uppercase HARD-tier keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) in the rule draft; zero consumption of the 25/25 HARD-rule ceiling |
| G5 | Low-regret under promotion-frequency uncertainty (n=3 evidentiary base) | Decision remains net-positive even in the disclosed adverse regime (near-zero forward promotion) |
| G6 | Best-in-class discoverability/sortability, matching or beating a do-nothing null | `grep`/directory-listing clusters ADRs by subject at zero marginal tooling cost; beats the explicitly-requested zero-governance benchmark |

---

## Step 2: Anti-Goals — What Would Guarantee Failure?

| # | Anti-goal ("to guarantee failure, we would...") | Does the package fall into this? |
|---|---|---|
| AG1 | ...let the lint's implementation scope grow without bound across every review cycle, so a single maintainer can never finish it | **Yes, partially** — see [IN-013-005](#in-013-005-m-6-enforcement-scope-has-grown-monotonically-across-every-remediation-pass-with-no-complexity-budget-critical). The rule count and required subsystems (YAML parser, waiver ledger + GitHub-API cross-check, taxonomy arbiter, 12+ named test fixtures) have only increased, iteration over iteration. |
| AG2 | ...keep at least one promotion path that still renames the ID, reproducing the exact citation-break bug for a real subset of ADRs | **Yes, by design (Path 2)** — disclosed as "the discouraged case," but never itself inverted (is a rename actually required?). See [IN-013-006](#in-013-006-path-2-rename-on-promotion-is-never-itself-inverted-major). |
| AG3 | ...benchmark the winning scheme against a weaker null than the one actually requested, so the benchmark looks won when it might not be against the toughest configuration | **Yes** — see [IN-013-007](#in-013-007-the-zero-governance-null-benchmark-does-not-test-its-strongest-configuration-major). |
| AG4 | ...leave the "author picks correctly under uncertainty" assumption enforced only by prose, with no mechanical default in the one agent that actually authors ADRs | **Yes, largely** — Fix 3 (`ps-architect.md`) corrects filename *grammar* only, not the scope-selection *heuristic*. See [IN-013-008](#in-013-008-the-producing-agent-fix-corrects-grammar-not-the-scope-selection-heuristic-major). |
| AG5 | ...disclose a downstream degraded-mode for one stripped directory (`projects/`) but not for a second, independently-recommended stripped directory (`docs/`) that the same convention depends on for its own worked examples | **Yes, partially** — see [IN-013-009](#in-013-009-the-downstream-degraded-mode-disclosure-omits-the-recommended-docs-strip-minormajor). |
| AG6 | ...silently downgrade a structurally-checkable invariant (location matches encoded origin) to an advisory-only, best-effort one (frontmatter correctness), without naming this as a cost of the decision | **Yes** — see [IN-013-010](#in-013-010-provenance-verification-is-structurally-weaker-under-scheme-b-than-under-a-c-minor). |
| AG7 | ...let the convention apply to a repo whose plugin-distribution audience never actually authors ADRs against a populated corpus, so "discoverability" is untestable in practice | **No** — already disclosed exhaustively (PM-002 degraded-mode section); not re-litigated here beyond AG5's narrower gap. |
| AG8 | ...conflate the worktracker `DEC-NNN` entity with ADRs so the two governance surfaces collide | **No** — explicitly and correctly non-conflated (verified: co-location counter-example at `PROJ-002-roadmap-next/decisions/DEC-001-project-creation.md` is disclosed, and the lint keys on filename prefix, not folder, which correctly handles it). |

---

## Step 3: Assumption Map

| # | Assumption | Type | Confidence | Validation Status | Consequence If Wrong |
|---|---|---|---|---|---|
| A1 | The L5 lint (M-6), once specified, will actually be built by the sole maintainer | Implicit / Process | Low | Hoped (Glob-verified absent: `scripts/lint_adr_convention.py` does not exist) | Tier-2 enforcement never activates; convention is permanently advisory (FM-1, already disclosed) — but see IN-013-005 for the **undisclosed driver** of this risk |
| A2 | Path-2 rename-on-promotion is the only way to keep `docs/design/` under one grammar | Implicit / Design | Medium | Asserted, not tested against the alternative of a mixed-grammar `docs/design/` | If wrong, the convention forfeits a fully rename-free promotion story it could have had |
| A3 | The requested zero-governance null alternative has been benchmarked in its strongest form | Explicit (IN-004 section) | Medium | Partially validated — the benchmark's own rebuttal argument (citations, not discovery) does not address a never-move + tag-only null | See IN-013-007 |
| A4 | The producing agent (`ps-architect.md`), once its filename grammar is fixed (Fix 3), will choose the canonical slug under uncertainty as ADR-M-003 recommends | Implicit / Behavioral | Low-Medium | **Empirically falsified once already** — this very ADR's own authorship chose the dialect for a document that turned out to be maximal framework scope | Recurrence of exactly the Path-2 rename churn the convention exists to minimize (R-4) |
| A5 | Downstream plugin-install authors reading `.context/rules/adr-standards.md` have access to the framework-ADR exemplars and canonical home it references | Implicit | Medium | Partially false under the RECOMMENDED (not required) `docs/` strip (`phase3-skeleton-generation-design.md:170-172`) | Rule references a location/examples that do not exist in a subset of installs; no disclosure of this specific compounding gap |
| A6 | Moving provenance from identity to frontmatter preserves an equivalent level of verifiability | Implicit | Medium | Only WARN-tier, best-effort (L-6b), versus Scheme A/C's FAIL-tier structural dialect-location match (L-4) | A wrong `origin_project` value is invisible without opening the file; a wrong scope-prefixed directory is visibly wrong and machine-checked |
| A7 | Forward promotion rate for framework-mandate projects will continue at a rate materially above ~0% | Explicit (Sensitivity section) | Low-Medium (n=3, self-disclosed) | Explicitly disclosed as unvalidated, capped confidence 0.70-0.75 | Already exhaustively handled by the document itself (PM-009, adverse-regime test); not re-litigated here |
| A8 | A single named human arbiter (M-5b) will actually adjudicate L-10 taxonomy-synonymy WARNs on a per-creation cadence | Implicit / Process | Low | Disclosed as capacity-constrained (DA-005), same solo-maintainer bottleneck as A1 | Compounds with A1: two separate governance subsystems (lint-build and per-ADR arbitration) both depend on the same single person's bandwidth, and neither disclosure connects the two as a **combined** load |

---

## Step 4: Stress-Test Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-013-005 | A1 / AG1 — M-6 scope growth | Assumption | Low | **Critical** | `adr-standards-rule-draft.md:213-232` (18 distinct rule IDs); ADR Changelog rows 1.1-1.6 (`ADR-PROJ031-004…:808-813`) | Methodological Rigor / Actionability |
| IN-013-006 | A2 / AG2 — Path-2 rename never inverted | Assumption | Medium | **Major** | `ADR-PROJ031-004…:568-570`, M-9 (`:534`) | Methodological Rigor |
| IN-013-007 | A3 / AG3 — null-alternative benchmark incomplete | Assumption | Medium | **Major** | `ADR-PROJ031-004…:283-288`; `:463` | Evidence Quality / Methodological Rigor |
| IN-013-008 | A4 / AG4 — producing-agent fix is grammar-only | Assumption | Low-Medium | **Major** | `adr-standards-rule-draft.md:277-286` (Fix 3); `ADR-PROJ031-004…:747-756` (Meta-Note, self-authorship) | Actionability / Completeness |
| IN-013-009 | A5 / AG5 — downstream degraded-mode gap | Assumption | Medium | **Minor-Major** | `phase3-skeleton-generation-design.md:159,170-172`; `ADR-PROJ031-004…:644,659` | Completeness |
| IN-013-010 | A6 / AG6 — provenance verification downgrade | Assumption | Medium | **Minor** | `adr-standards-rule-draft.md:223` (L-6b, WARN, best-effort) vs. `:219` (L-4, FAIL) | Internal Consistency |

**Finding ID Format:** `IN-013-{NNN}` (execution_id = `013`, i.e., iteration 5 of S-013 for this deliverable, per the strategy's `IN-NNN-{execution_id}` convention — collision-avoided against prior iterations' `IN-001`..`IN-008` tags already embedded in the deliverable text, which belong to iterations 1-4).

---

## Finding Details

### IN-013-005: M-6 Enforcement Scope Has Grown Monotonically Across Every Remediation Pass, With No Complexity Budget [CRITICAL]

**Type:** Assumption (A1) — "the lint will actually get built"
**Original Assumption:** The document treats M-6 (the L5 CI lint) as a fully-specified, buildable deliverable, gated only by "independently-verified completion (tracked Task + GH Issue)" (`ADR-PROJ031-004…:473`, R-5 mitigation).
**Inversion:** What would guarantee M-6 never ships? Keep adding FAIL/WARN rules and required subsystems at every review cycle, with no corresponding subtraction or phasing, against a single-maintainer repo.
**Plausibility:** High — this is not hypothetical, it is the observed history of this exact document. Tracing the rule-draft's own Changelog and lint table:
- Iteration 1 (v1.1): L-1 split into L-1a/L-1b, L-2, L-3 — roughly 4 rule-forms.
- Iteration 2 (v1.2): + L-9 (frozen-dir block), L-10 (taxonomy synonymy) — 6.
- Iteration 3 (v1.3): + L-6b (provenance correctness), L-11 (waiver-ledger integrity), L-12 (grandfather-allowlist freeze) — 9.
- Iteration 4 (v1.5): + L-4b (repository-topology dialect-reject), L-6c (scope-presence), L-13 (supersession legitimacy), L-14 (producer-side drift) — 13-14 distinct rule identifiers, per the live table at `adr-standards-rule-draft.md:213-232` (L-1a, L-1b, L-2, L-3, L-4, L-4b, L-5, L-6, L-6b, L-6c, L-7, L-8, L-9, L-10, L-11, L-12, L-13, L-14 = **18** distinct rule IDs).
- On top of the 18 rules: a from-scratch YAML frontmatter parser (`jerry ast` only parses blockquote frontmatter, per the CC-003 disclosure at `ADR-PROJ031-004…:387-391`), a waiver ledger requiring live GitHub-API cross-checking of approving reviewers, a closed `legitimacy_category` enum, a grandfather-allowlist-freeze mechanism with an exact-match seed assertion, and — per `adr-standards-rule-draft.md:709` — a minimum of 12 individually-named red-then-green regression fixtures (`test_L2_rejects_new_bare_id` through `test_L13_rejects_single_author_illegitimate_supersession`).
**Consequence:** R-5 (`ADR-PROJ031-004…:473`) already rates "lint never gets built" as MED probability / HIGH impact and treats the mitigation as "M-6 is now a ratification blocker requiring independently-verified completion" — but that mitigation only controls **whether Tier-2 ratifies**, not **whether M-6 ever gets built at all**. Nothing in either document caps M-6's growth, requires the next revision to net-simplify, or phases M-6 into an MVP subset. The trend line (4 -> 6 -> 9 -> 18 rule-forms across four iterations, each iteration adding rules to close a newly-found gap and removing none) is monotonically increasing under a fixed single-maintainer capacity (`@geekatron`, the sole `CODEOWNERS` entry for `.context/rules/`, `.github/workflows/`, `docs/governance/` — verified `.github/CODEOWNERS:8,14`). If the review process itself keeps this document alive for a sixth, seventh iteration, M-6's required scope will very likely grow further before it ships, which is the opposite of what "ratification blocker" pressure is supposed to produce.
**Evidence:** `adr-standards-rule-draft.md:213-232` (the 18-rule table); `ADR-PROJ031-004-adr-identifier-convention.md:808-813` (Changelog rows showing rule additions at every version); `.github/CODEOWNERS:8,14` (single-maintainer verification); `scripts/lint_adr_convention.py` (Glob-verified: does not exist).
**Dimension:** Methodological Rigor (the enforcement design has no phasing/MVP discipline); Actionability (M-6 as currently scoped is not a schedulable unit of work for a solo maintainer).
**Mitigation:** Split M-6 into an explicit MVP sub-tier ("Tier-2a": L-1a/L-1b/L-2/L-3/L-9 — the collision/bare-ID/frozen-dir core, buildable as a simple filename-regex script with no YAML parsing, no waiver-ledger API integration) that alone restores the core collision-prevention guarantee, versus "Tier-2b" (L-4/L-4b/L-6/L-6b/L-6c/L-7/L-8/L-10/L-11/L-12/L-13/L-14 — the richer integrity/taxonomy/waiver machinery), tracked and gated separately, mirroring the Tier-1/Tier-2 guidance-vs-enforcement split the document already applies one level up. Add an explicit statement that future remediation passes MUST NOT add a new FAIL/WARN rule to Tier-2a without removing or downgrading an existing one (a complexity budget), to stop the observed monotonic growth.
**Acceptance Criteria:** The Migration Plan (M-6) is re-split into two independently-schedulable sub-milestones with distinct GH Issues, and the ADR states an explicit rule-count ceiling or growth policy for future amendments.

---

### IN-013-006: Path-2 Rename-on-Promotion Is Never Itself Inverted [MAJOR]

**Type:** Assumption (A2)
**Original Assumption:** "Promotion of a canonical (domain-slug) ADR from a project to the framework SHOULD be a pure `git mv` with no identifier change (Path 1). Only a project-scoped *dialect* ADR SHOULD incur a rename + tombstone on promotion (Path 2)." (`adr-standards-rule-draft.md:53`, ADR-M-008)
**Inversion:** What would guarantee the convention still exhibits its own motivating failure (citation breakage on promotion) for at least some ADRs? Keep a rename step reachable from any live promotion path. Path 2 is exactly that path, and it is not hypothetical: this ADR's own scheduled Path-2 self-promotion (M-9, `ADR-PROJ031-004…:534`) is the concrete, named instance.
**Plausibility:** High — Path 2 is not an edge case the document is unaware of; it is explicitly retained ("the one case with a rename, and its cost is exactly why D-1 recommends domain slugs from birth," `ADR-PROJ031-004…:568-570`). What is missing is the inversion step itself: the document's own S-013 self-check at line 497 inverts the *whole-scheme* choice ("If we deliberately chose the opposite... Scheme A everywhere... what breaks?") but never inverts this *narrower* design choice — whether Path 2 must rename at all, versus `git mv`-ing the dialect-named file into `docs/design/` unchanged and simply accepting a permanently origin-looking ID for that one promoted ADR (forfeiting only that ADR's grep-by-domain clustering, not its citation stability).
**Consequence:** The headline claim "Promotion is a pure file move... zero ID-string churn" (`ADR-PROJ031-004…:444`) is true only for the subset of ADRs born under the canonical slug — exactly the same qualification Path 1's "designed default, not yet demonstrated" honesty note already applies (`:580`). Path 2 leaves the ADR's own most cited failure mode (BUG-006's still-stale PROJ-007 citations) structurally reachable again, for every dialect ADR that is promoted, forever — bounded only by SHOULD-guidance (ADR-M-003's "default to canonical under uncertainty") that this very document's own authorship failed to follow (see IN-013-008).
**Dimension:** Methodological Rigor (the document's own inversion methodology was applied one level too coarse).
**Mitigation:** Add an explicit sub-analysis to the Promotion Process section inverting "must Path 2 rename?" and either (a) justify the rename as necessary (the taxonomy-clustering argument at L2 Architectural Implications, `:463`, "Location still signals scope," is available but not connected to this specific question), or (b) offer an alternative "Path 2b" that preserves the dialect ID on promotion, trading clustering for citation-stability, for authors/reviewers who judge the latter more valuable for a specific ADR.
**Acceptance Criteria:** The Promotion Process section states, explicitly, why a rename is required on Path 2 rather than optional, with the trade-off named (not merely asserted).

---

### IN-013-007: The Zero-Governance Null Benchmark Does Not Test Its Strongest Configuration [MAJOR]

**Type:** Anti-Goal (AG3) — the invoking task explicitly required this benchmark ("if we wanted maximum decision-findability with zero governance, what would we do... does the package beat that null alternative?")
**Original Assumption:** "The zero-governance null alternative" section (`ADR-PROJ031-004…:283-288`, tagged IN-004 from a prior iteration) already benchmarks Scheme B against "no ID convention at all... rely on a generated index or repo-wide grep/semantic search," and concludes B wins because "Citations, not discovery, are the load-bearing failure... a search index does nothing for a hyperlink or path that already points at a moved file."
**Inversion:** Invert the null alternative itself — construct the *strongest* zero-governance, maximum-findability configuration, not merely "search instead of naming." The strongest null is: **apply zero naming/taxonomy governance, AND never physically relocate a decision file on promotion — tag `scope`/`domain` in frontmatter only, and generate a queryable index (e.g., a `jerry adr index --scope framework` command or nightly-generated `INDEX.md`) that resolves current scope from tags regardless of physical location.**
**Plausibility:** High as a configuration (it costs nothing more than the "index" the document's null already concedes needs building), and it directly defeats the document's own stated rebuttal: if nothing ever moves, there is no "hyperlink that already points at a moved file" for the search index to fail to fix — the null alternative's citation-stability property becomes **equal to** Scheme B's on the exact axis (G1) the document cites as decisive, and it does so at **zero** of Scheme B's residual taxonomy-collision risk (R-3/R-7, slug synonymy and slug-squatting — both explicitly named as *unmitigated* residuals in the very same document, `ADR-PROJ031-004…:455,475`).
**Consequence:** The document's own [L2 Architectural Implications] section concedes the actual reason physical relocation has residual value: "Location still signals scope... the ontology's scope-awareness moves from the identifier to the path, not away entirely" (`:463`) — i.e., `docs/design/` as a browsable, physically-consolidated canonical home has a real discoverability benefit a location-agnostic tag-only index would sacrifice (a downstream author or new agent browsing `docs/design/` sees the entire framework-ADR corpus at a glance; a tag-only null requires running the index tool first). **This is a valid, available rebuttal — but the document never connects it to the null-alternative section.** As written, the requested benchmark is answered against a weaker null (search-instead-of-naming, same move practices as today) than the one the task's own phrasing invites (maximum decision-findability with *zero* governance), so the document's affirmative conclusion ("The benchmark confirms a convention is warranted") is not yet fully earned on the page, even though a correct rebuttal exists elsewhere in the same document.
**Dimension:** Evidence Quality (the benchmark, as constructed, is not the strongest available counter-case) / Methodological Rigor.
**Mitigation:** Add an explicit sub-case to the null-alternative section: "tag-only, never-move" — and rebut it using the already-present location-browsability argument from L2 Architectural Implications, plus the point (already made for the weaker null, item (3) at `:288`) that a tag-only index is "itself governance" (someone must build, run, and keep it fresh — symmetric to the point already made, just not cross-referenced here).
**Acceptance Criteria:** The null-alternative section explicitly names and rebuts the never-move + tag-only configuration, not only the search-instead-of-naming configuration.

---

### IN-013-008: The Producing-Agent Fix Corrects Grammar, Not the Scope-Selection Heuristic — And the Package's Own Authorship Already Falsified the Assumption It Corrects For [MAJOR]

**Type:** Assumption (A4) — "authors (including the producing agent) will default to the canonical slug under uncertainty"
**Original Assumption:** ADR-M-003 / the Rationale section states the corrected position that "the correct default under uncertainty is the canonical slug, not the dialect" (`ADR-PROJ031-004…:313`), and Fix 3 (`adr-standards-rule-draft.md:275-286`) specifies edits to the ADR-*producing* agent, `skills/problem-solving/agents/ps-architect.md` — but every one of F3-a through F3-e is a **filename-grammar or path** fix (bare title, non-canonical filename pattern, phantom template path, phantom/H-05-violating CLI reference, output-location alignment). None of the five specifies a **decision heuristic**: what the agent should do when the human/task has not explicitly declared the decision's intended locality.
**Inversion:** What would guarantee recurrence of exactly the Path-2 rename churn (IN-013-006) the convention exists to minimize? Leave the scope-selection choice to unenforced, prose-only SHOULD guidance in the one agent that actually authors most future ADRs, with no default-heuristic wired into its behavior.
**Plausibility:** This is not merely plausible — it is **already observed**, in the most on-point instance available: this very ADR's own authorship. Per the Meta-Note (`ADR-PROJ031-004…:747-756`), the filename as written uses "the legacy project-scoped dialect (`ADR-PROJ031-004`)... which the decision permits (D-3) but does not recommend for an ADR of framework scope," explained as "written here because the invoking task mandated this exact path." The document treats this honestly and even reframes it as pedagogically useful (a "worked example of its own Path-2 promotion"). But from a strict inversion standpoint, the mandated-path explanation does not remove the underlying signal: **the same agent (`ps-architect`) that is simultaneously authoring the rule recommending "default to canonical under uncertainty" produced, in the same breath, an artifact that does not follow that rule** — under conditions of maximal context-awareness of the very recommendation being violated. Ordinary future invocations, operating with less exhaustive context (a routine task, a rushed session, a less deliberate agent state), have no stronger reason to choose correctly than this flagship instance did, and Fix 3 does not add one: it fixes what the output *looks like*, not what triggers the *choice* between dialect and canonical form.
**Consequence:** Without an explicit default-heuristic wired into the producing agent (e.g., "if the user/task has not explicitly stated persistent, single-project-only locality, propose the canonical domain-slug form, not the dialect, regardless of the agent's own uncertainty"), the SHOULD-only guidance in ADR-M-003 depends entirely on either (a) a human catching the wrong choice at review time, or (b) the agent independently reasoning its way to the recommended default every time — the same failure mode this document's own creation just demonstrated.
**Dimension:** Actionability (the fix, as specified, does not close the gap it is meant to close) / Completeness.
**Mitigation:** Add F3-f to Fix 3: an explicit default-to-canonical decision rule in `ps-architect.md`'s ADR-authoring logic, triggered whenever `origin`/`scope` intent has not been explicitly and persistently declared by the invoking task, mirroring ADR-M-013's frontmatter-level default.
**Acceptance Criteria:** `ps-architect.md` contains a stated default rule (not merely output-format grammar) that resolves to the canonical slug whenever locality is undeclared or ambiguous.

---

### IN-013-009: The Downstream Degraded-Mode Disclosure Omits the RECOMMENDED `docs/` Strip [MINOR-MAJOR]

**Type:** Assumption (A5)
**Original Assumption:** The "Degraded-mode disclosure for the downstream CLI" (PM-002, `ADR-PROJ031-004…:659`) discloses that a fresh plugin install carries "zero seeded `decisions/` ADRs on day one" because `projects/` is stripped, and frames the CLI-lint's usefulness as bounded by that empty corpus.
**Inversion:** What would guarantee a downstream author is confused rather than helped by this convention? Ship them the rule file (Tier-1 guidance) while silently removing the very directory, exemplars, and index the rule file tells them to use.
**Plausibility:** Confirmed by direct evidence. `phase3-skeleton-generation-design.md:159` shows the VALIDATED strip set is `projects/ tests/ skills/.graveyard .github` — **`.context/` is not in this list**, so `.context/rules/adr-standards.md` (the guidance layer) does ship, confirming Tier-1 guidance reaches the downstream audience (a check this reviewer performed independently; it is a **positive** finding, not itself a defect). However, `phase3-skeleton-generation-design.md:170-172` lists a **RECOMMENDED (SHOULD, not required)** additional strip that includes `docs/` (247 files) — and the parent ADR itself already discloses this fact in passing ("and, as a recommended addition, `docs/`," `ADR-PROJ031-004…:644`). What is **not** disclosed anywhere is the specific consequence for *this* convention: under that recommended strip, `docs/design/` — the canonical framework-ADR home this very rule file prescribes — along with all three framework-ADR exemplars this document cites as "EXEMPLAR"/"PRECEDENT" (`ADR-agent-design-001`, `ADR-output-path-resolution-001`; `ADR-PROJ031-004…:766-767`) and the recommended `docs/design/README.md` domain-taxonomy index (M-5) — would **all** be absent from that install.
**Consequence:** A downstream author following the RECOMMENDED strip receives a rule file that says "framework ADRs live in `docs/design/`, see the exemplars there for the pattern" while `docs/design/` does not exist in their tree at all — a stronger and more specific version of the already-disclosed "empty `projects/` corpus" gap (PM-002), compounding it rather than duplicating it (PM-002 covers the *project* corpus being empty; this covers the *framework* corpus and its worked examples also being absent, under a documented-but-not-fully-traced second strip).
**Dimension:** Completeness (the degraded-mode disclosure is incomplete for a second, independently-recommended strip configuration).
**Mitigation:** Extend PM-002's degraded-mode disclosure to explicitly name the `docs/` strip's consequence for this convention specifically (loss of `docs/design/` as a location, loss of the 3 exemplar ADRs, loss of the recommended domain index) alongside the existing `projects/`-corpus disclosure.
**Acceptance Criteria:** The Enforcement Scope / Degraded-Mode section names both stripped directories' consequences for this convention in one place.

---

### IN-013-010: Provenance Verification Is Structurally Weaker Under Scheme B Than Under A/C [MINOR]

**Type:** Assumption (A6)
**Original Assumption:** "Provenance preserved by convention... origin lives in frontmatter... satisfying P-004/c-005 without polluting identity" (`ADR-PROJ031-004…:446`, already correctly softened from "losslessly" to "by convention" per the FM-104 fix, with a WARN-tier L-6b provenance-correctness check added).
**Inversion:** What would guarantee provenance silently becomes wrong and stays wrong? Move it from a location that is structurally, mechanically checked (FAIL-tier) to one that is only advisory-checked (WARN-tier, "best-effort... skipped where origin is not derivable," `adr-standards-rule-draft.md:223`).
**Plausibility:** Medium-High. Under Scheme A/C, a directory/prefix mismatch (an `ADR-PROJ010-*` file sitting outside `projects/PROJ-010-*/decisions/`) is a **FAIL-class, mechanically detectable** anomaly (L-4, `adr-standards-rule-draft.md:219`) — visibly wrong at a glance and blocked by CI once M-6 ships. Under Scheme B, the equivalent fact (a wrong `origin_project` value in frontmatter) is checked only by L-6 (presence) and L-6b (correctness, explicitly "best-effort... skipped where origin is not derivable," WARN-class, never blocking).
**Consequence:** This is a real, disclosed-but-not-explicitly-compared cost of the identity/provenance split: Scheme B trades a *structurally self-checking* provenance signal (visible mismatch, FAIL-class) for a *frontmatter-only, best-effort* one (invisible-until-audited, WARN-class). The document names the mechanism (L-6b exists) but never states the comparative trade-off this plainly — that moving provenance out of the identifier is not a free lunch; it is a real (if modest) verifiability downgrade, paid to gain a real (and larger) citation-stability upside.
**Dimension:** Internal Consistency (the Negative Consequences list at `ADR-PROJ031-004…:451-458` enumerates several real costs of Scheme B but does not include this one alongside them).
**Mitigation:** Add this trade-off as an explicit Negative Consequence entry, paired with L-6b, so the full cost/benefit ledger for choosing frontmatter-based provenance over identity-based provenance is stated in one place.
**Acceptance Criteria:** Negative Consequences list gains an entry naming the FAIL-vs-WARN verifiability asymmetry.

---

## Zero-Governance Null Alternative Re-Examination

Per the explicit task instruction to invert the goal ("if we wanted maximum decision-findability with zero governance, what would we do — and does the package beat that null alternative?"), this reviewer independently re-derived the strongest null and compared it against Scheme B, without reading the deliverable's own IN-004 section content into this comparison a priori (it was read afterward, per the blind protocol, only for cross-reference at write-up time):

**Strongest null: "tag, never move."** Leave every ADR's filename and location exactly where it was born, forever — no promotion `git mv`, no rename, ever. Add a `scope` (`framework`|`project`) and `domain` frontmatter tag to every ADR (zero taxonomy governance: freeform text, no slug uniqueness required). Build one script (`jerry adr index`) that scans all `decisions/` directories repo-wide for these tags and renders a queryable, always-current virtual index grouped by `scope`/`domain`, independent of physical location.

**How it compares to Scheme B on the document's own three cited axes (G1/G2/G6):**
- **Citation stability (G1):** Equal to Scheme B for canonical-slug-born ADRs, and **better** than Scheme B for dialect-born ADRs that are later promoted (the null never renames anything, so it has no Path-2-equivalent citation-break residual at all — see IN-013-006).
- **Collision safety (G3) / taxonomy risk:** **Better** than Scheme B — no domain-slug uniqueness governance is required at all (no L-3, no L-10 taxonomy arbiter, no synonymy/slug-squatting residual R-3/R-7), because the null does not encode subject into a governed, collision-prone namespace.
- **Discoverability (G6):** **Worse** than Scheme B in one specific, real way the document itself names but does not connect back to the null comparison: `docs/design/` as a *browsable, physically-consolidated* canonical home (`ADR-PROJ031-004…:463`) has a zero-tooling discoverability property (a person or agent can `ls`/`grep` the directory with no script) that a virtual, tag-only index cannot match without first running the index tool. This is the null's one genuine weakness, and it is a real one.

**Verdict on the benchmark:** The package's affirmative claim that "a convention is warranted" survives against this stronger null, but only via the physical-consolidation/zero-tooling-browsability argument — **not** via the argument the document's own IN-004 section actually uses ("citations, not discovery, are the load-bearing failure"), which this stronger null defeats on its own terms. The conclusion (B > null) still holds; the stated reasoning for it, as written, does not fully hold against the toughest null. This is exactly the gap named at IN-013-007.

---

## Recommendations

**MUST mitigate (Critical):**
- **IN-013-005:** Split M-6 into a phased Tier-2a (MVP: L-1a/L-1b/L-2/L-3/L-9, no YAML parser, no waiver-ledger API integration) and Tier-2b (the remaining 13 rules + waiver/arbiter/fixture machinery), tracked as separate, independently-schedulable milestones. State an explicit no-net-growth policy for future amendments to Tier-2a.

**SHOULD mitigate (Major):**
- **IN-013-006:** Add an explicit inversion of "must Path 2 rename?" to the Promotion Process section; either justify the rename via the location-signals-scope argument or offer a non-renaming Path-2 variant.
- **IN-013-007:** Extend the zero-governance null-alternative section to explicitly name and rebut the "tag-only, never-move" configuration, using the already-available location-browsability argument from L2 Architectural Implications.
- **IN-013-008:** Add F3-f to Fix 3 — an explicit default-to-canonical-slug decision heuristic wired into `ps-architect.md`'s authoring logic, not just filename-grammar correction.

**MAY mitigate (Minor):**
- **IN-013-009:** Extend the PM-002 degraded-mode disclosure to name the `docs/` strip's specific consequence for this convention's own referenced exemplars/index.
- **IN-013-010:** Add an explicit Negative-Consequences entry naming the FAIL-vs-WARN provenance-verifiability asymmetry between Scheme A/C and Scheme B.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-013-009: downstream degraded-mode disclosure incomplete for the second (docs/) strip configuration; IN-013-008: producing-agent fix addresses output format, not the decision heuristic |
| Internal Consistency | 0.20 | Negative | IN-013-010: a real cost (provenance-verifiability downgrade) of the chosen scheme is not named alongside the document's own otherwise-thorough Negative Consequences list |
| Methodological Rigor | 0.20 | Negative | IN-013-005: the document's own inversion methodology (applied exhaustively elsewhere) was not applied to the buildability of its central enforcement mechanism, nor to whether Path-2's rename step (IN-013-006) is itself necessary |
| Evidence Quality | 0.15 | Negative | IN-013-007: the requested null-alternative benchmark is answered against a weaker configuration than the one specifically requested, even though the correct rebuttal exists elsewhere in the document |
| Actionability | 0.15 | Negative | IN-013-005 and IN-013-008 both identify fixes that are gap-closing but not yet specified as concrete edits (unlike the rest of this package's exhaustively concrete Fix 1/2/3 specifications) |
| Traceability | 0.10 | Neutral | All findings in this report cite specific file+line evidence; no traceability gap identified in the reviewed deliverable itself on this axis |

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1
- **Major:** 3
- **Minor (incl. Minor-Major):** 2
- **Protocol Steps Completed:** 6 of 6 (Goals, Anti-Goals, Assumption Map, Stress-Test, Mitigations/Recommendations, Synthesis/Scoring)

**Overall assessment:** REVISE. None of the six findings overturn the core decision (Scheme B / subject-encoded ADR identity remains the correct call under inversion). One finding (IN-013-005, M-6 scope growth) is a genuine, previously-undisclosed viability risk to the entire Tier-2 enforcement design and should be treated as gating before further tournament iterations are spent polishing prose that depends on an ever-growing, likely-unbuildable lint. The remaining five findings are consistent with, and extend, this package's own demonstrated remediation discipline (specific, evidence-cited, file+line-anchored, non-fabricated) and are readily closable in a single further revision pass.

---

**Constitutional Compliance:** P-003 (no subagents spawned), P-020 (no files outside this mandate edited — deliverables were read-only inspected), P-022 (every factual claim above is cited to a specific file+line or is explicitly labeled as this reviewer's inference/construction, e.g. the "tag, never move" null configuration and the M-6 growth-trend characterization).
