# Devil's Advocate Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (post-subtraction, iteration 7)

> **Strategy:** S-002 Devil's Advocate
> **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
> **Criticality:** C4 (engagement gate 0.95)
> **Date:** 2026-07-06
> **Reviewer:** adv-executor (S-002, blind reviewer, iteration 7)
> **H-16 Compliance:** Structural evidence only (filename-listing, not content read) confirms `adversary/iteration-007/s-003-findings.md` already exists alongside this file, consistent with the disclosed 6-group sequential order (self-refine -> steelman -> challenge -> ...). Content of that file was not read (blind protocol). **[Inference, not content-verified]**

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverables, H-16 check, role assumed |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | DA-NNN findings with severity |
| [Finding Details](#finding-details) | Expanded findings, all severities |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-002 (Devil's Advocate)
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md`
- **Deliverables reviewed:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (763 lines, read in full)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (238 lines, read in full)
  - Owner disclosure record read as permitted context: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`
- **Criticality:** C4; engagement gate 0.95
- **Attack angle mandated by orchestrator:** (1) does the slimmed 5-rule lint still deliver the collision-safety the ADR claims; (2) is anything load-bearing among the deletions; (3) is the descoped list honest or a hidden commitment.
- **Independent verification performed:** `Glob` over `**/decisions/ADR-*.md`, `docs/design/ADR-*.md`, and `**/ADR-STORY015-001*.md` to independently confirm corpus counts cited in the deliverables (see DA-003).

**Role assumed:** Argue against the post-subtraction package's central claim — that the slimmed 5-rule L5 lint plus grandfathered dialect delivers adequate collision-safety and citation-continuity, and that the "descoped, honestly" list is a closed, honest disclosure rather than a hidden commitment. The subtraction pass's own doctrine ("close findings by deleting the claim/mechanism that created the exposure") is itself treated as fair game: a deletion that removes a *false* claim is legitimate; a deletion that removes the *only* mechanism addressing a still-real problem is not.

---

## Summary

8 counter-arguments identified (1 Critical, 4 Major, 3 Minor). The post-subtraction package is honest about most of its own limits and its self-correction discipline (count reconciliations, Claim-Status labeling) is real and mostly working. But the single strongest finding is that the document's own headline motivating evidence — the still-unrepaired PROJ-007 citation wound, cited three times as the reason this ADR exists — has **no remediation task anywhere in the 14-row Migration Plan** and is not disclosed as a residual; M-10 repairs a different (ci.yml) citation and explicitly excludes markdown files, so the two markdown files bearing the cited wound (`WORKTRACKER.md`, `EN-001.md`) are untouched. A second Major finding (DA-003) is a live, independently-verified arithmetic inconsistency in the lint's own gating acceptance criterion (M-6 says 19 files must pass the grandfather test; the Enforcement Design section, the rule draft, and direct repo verification all say 18). Recommend REVISE: address DA-001 and DA-002 before the package can credibly claim it "eliminates the demonstrated failure mode," and correct DA-003 before M-6 is treated as a well-specified gate.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260706 | Migration Plan has no remediation task for the ADR's own headline motivating evidence (still-stale PROJ-007 citations); M-10 covers a different citation and explicitly excludes markdown files | Critical | ADR `:73`, `:113`, `:521` (M-10 row) | Completeness, Actionability |
| DA-002-20260706 | "Eliminates the demonstrated failure mode" claim rests on a citation-ratio measured in a corpus the document itself later discloses excludes the corpus where the actual failure lives | Major | ADR `:423` (Positive-1) vs. ADR `:549` (DA-002 iter-4 scope-limitation note) | Internal Consistency, Evidence Quality |
| DA-003-20260706 | M-6's grandfather-test target ("19 files") contradicts the Enforcement Design section's and rule draft's corrected figure ("18 files"); independently verified via repo Glob that 18, not 19, is reachable by the stated scan path | Major | ADR `:517` (M-6 row) vs. ADR `:664` and rule draft `:94`; independent Glob verification | Internal Consistency, Methodological Rigor |
| DA-004-20260706 | L-4 (ID<->location) is explicitly scoped to project-based topology only; in repository-based topology there is zero (not degraded) lint coverage for dialect/location consistency, in what the ADR itself names as a likely primary downstream-adopter topology | Major | ADR `:383`, rule draft `:176` (L-4 row), subtraction-pass-notes.md Major table (RT-007 row) | Completeness, Actionability |
| DA-005-20260706 | "Not phased, not committed" framing for descoped items conflicts with named, threshold-triggered escalation commitments (R-6, R-7, PM-009) that have no monitoring/measurement mechanism and no Migration Plan task to build one | Major | ADR `:454` (R-7), `:453` (R-6/DA-009), `:461-462` (PM-009), `:666` (Descoped note) | Actionability, Traceability |
| DA-006-20260706 | "Gating?" column's reconciled meaning ("sequencing flag, not an enforcement gate") does not match the substantive weight of language used in specific rows, e.g. M-12's "or the convention is defeated at the source" | Minor | ADR `:502` (reconciliation note) vs. `:523` (M-12 row) | Internal Consistency |
| DA-007-20260706 | R-9 (case-folded slug lookalike) severity rating (LOW) may understate real-world confusion risk given it demonstrates the anti-collision mechanism can be defeated by an identity a human reader would treat as identical, using an example drawn from the corpus under review itself | Minor | ADR `:456` (R-9 row) | Methodological Rigor |
| DA-008-20260706 | Waiver-ledger deletion removes the only structured record of where/how often the MEDIUM-tier lint override is invoked; no replacement telemetry proposed, reducing convention-erosion observability | Minor | subtraction-pass-notes.md `:54,:61` (waiver ledger deletion + override model) | Traceability |

---

## Finding Details

### DA-001: Migration Plan omits remediation for the ADR's own headline motivating evidence [CRITICAL]

**Claim Challenged:** L0 Executive Summary: "This has already happened — all three framework ADRs... were born inside projects and renamed on promotion; the resulting broken citations remain *unrepaired* months later (verified for the PROJ-007 pair — see References)" (ADR `:73`). Restated in Context: "stale citations to the extinct `ADR-PROJ007-001/002` IDs still sit in PROJ-007's own `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107`, and `EN-001.md:48-49,72-73` as of 2026-07-02" (ADR `:113`).

**Counter-Argument:** This is the document's own primary justification for existing — cited three separate times (L0, Context, and again implicitly wherever "the demonstrated failure mode" is invoked) as live, present-tense, unrepaired damage. Yet scanning the full 14-row Migration Plan (ADR `:489-525`), the only remediation task touching a stale citation is **M-10**: "Repair the dangling full-path citation `ADR-CI-001` in `.github/workflows/ci.yml:2`... **and audit non-markdown files** for further live `ADR-*` citations" (ADR `:521`). `ORCHESTRATION.yaml` is non-markdown and might fall inside that audit scope; `WORKTRACKER.md` and `EN-001.md` are **markdown** files, explicitly outside the stated "non-markdown files" audit boundary. There is no other Migration Plan row, Risk row, or Residual entry (checked against `subtraction-pass-notes.md` "Residuals Disclosed" table, which lists R-A through R-C, R-1, R-6, R-7, PM-009 — none of them is "repair the still-stale PROJ-007 citations") that assigns an owner, a task, or even an honest disclosure of this specific, named, cited-as-evidence gap.

**Evidence:** ADR `:73` (L0), `:113` (Context, explicit line-cited stale references), `:521` (M-10, the only citation-repair task, scoped to a different file and to non-markdown files only). Cross-checked against the full Migration Plan table `:489-525` and `subtraction-pass-notes.md` Residuals table `:120-133` — no matching row found.

**Impact:** The convention fixes the *mechanism* going forward (future Path-1 promotions of canonical-slug ADRs will not rename, so future citations of that class survive) but performs and tasks **zero remediation** of the exact damage it repeatedly cites as its reason to exist. A reader who takes the L0 "This has already happened" framing at face value would reasonably expect a Migration Plan line item to fix it; none exists, and its absence is not even disclosed as a residual (contrast with the document's otherwise thorough residual-disclosure discipline for R-A through R-C, R-1, R-6 through R-11).

**Dimension:** Completeness (0.20), Actionability (0.15).

**Response Required:** Either (a) add a Migration Plan row repairing the specific cited stale references in `WORKTRACKER.md:106-107` and `EN-001.md:48-49,72-73` (with owner and tracked Task/GH-Issue per H-32), or (b) if repair is deliberately out of scope (e.g., per the same P-020 "not silently edited" rationale already used for `ci.yml`), add an explicit disclosed residual naming the gap, an owner, and a cadence — matching the rigor already applied to R-A/R-B/R-C.

**Acceptance Criteria:** A Migration Plan row or a named Residual entry exists, citing the exact file:line references already established in Context (`:113`), with an owner and a tracked item (or an explicit, reasoned "will not fix" disclosure per P-022 — not silence).

---

### DA-002: "Eliminates the demonstrated failure mode" claim rests on evidence scoped to the wrong corpus [MAJOR]

**Claim Challenged:** Consequences > Positive, item 1: "Promotion is a pure file move — zero ID-string churn for canonical (domain-slug) ADRs, and therefore zero breakage for the bare-ID citation majority (grep-measured, DA-001 iter-3: ~72% of ADR citations in `.context/rules/` are bare-ID — 28 of 39...). ... Eliminates the demonstrated failure mode (BUG-006's ~150-reference remediation; the still-stale `ADR-PROJ007-001/002` citations)." (ADR `:423`)

**Counter-Argument:** The 72%/28% ratio this claim leans on is measured **only within `.context/rules/`** (ADR `:423`, `:549`). The document's own later section explicitly concedes this scope limitation: "This ratio was measured **only within `.context/rules/`** — a narrow corpus that excludes worktracker entity files (`projects/*/WORKTRACKER.md`), orchestration YAMLs..." and "The 72%/28% split therefore cannot be safely generalized repo-wide" (ADR `:549`). But `WORKTRACKER.md` and `ORCHESTRATION.yaml` are **precisely** the files the "still-stale `ADR-PROJ007-001/002`" wound lives in (ADR `:113`). The document therefore uses a citation-ratio measured in a corpus it later admits excludes the exact corpus where its own founding evidence resides, to support a claim ("eliminates the demonstrated failure mode") about that same founding evidence. This is a self-referential evidentiary gap: the support and the claim it supports are drawn from disjoint populations.

**Evidence:** ADR `:423` (the claim), ADR `:549` (the scope-limitation disclosure, itself dated/labeled "DA-002, iter-4"), ADR `:113` (identifying `WORKTRACKER.md`/`ORCHESTRATION.yaml` as the location of the actual wound).

**Impact:** Reduces confidence that Path-1 (pure file move) actually would have prevented, or will prevent, citation staleness for the citation *type and corpus* that produced the demonstrated failure. The claim may still be directionally correct (Path-1 does remove ID-churn, which was the proximate cause of the PROJ-007 rename-driven staleness), but "eliminates" is an overstatement not supported by the cited ratio, and the document's own later self-correction (`:549`) already establishes the mechanism by which this overstatement can be shown.

**Dimension:** Internal Consistency (0.20), Evidence Quality (0.15).

**Response Required:** Either narrow the "eliminates the demonstrated failure mode" claim to "removes the ID-rename cause of the PROJ-007-style staleness for future Path-1 promotions" (without asserting elimination is measured), or extend the citation-ratio measurement to `WORKTRACKER.md`/orchestration YAMLs before making the "eliminates" claim (the document already commits to exactly this extension at `:549` — "extend the citation-ratio measurement beyond `.context/rules/` to at least `WORKTRACKER.md`, orchestration YAMLs... before M-6 ships" — but Positive-1's headline claim at `:423` was not softened to match that already-disclosed limitation).

**Acceptance Criteria:** Positive-1's claim and the `:549` scope-limitation disclosure say the same thing about what has and has not been demonstrated.

---

### DA-003: M-6's grandfather-test count (19) contradicts the corrected figure (18) used elsewhere, verified independently [MAJOR]

**Claim Challenged:** Migration Plan, M-6: "Implement + wire the 5-rule L5 CI lint... into CI, **with the grandfather regression test green (16 dialect + 3 canonical = 19 files pass L-1)** plus one named red-then-green fixture per rule." (ADR `:517`)

**Counter-Argument:** This directly contradicts the Enforcement Design section of the *same document*: "A **grandfather regression test** gates the lint before it ships: the **18 files reachable by the scan path** (15 dialect files in `decisions/` dirs + 3 canonical `docs/design/` ADRs) pass L-1... The entity-embedded `ADR-STORY015-001`... is **out-of-scan** (R-10, FM-002), grandfathered in place but not lint-covered." (ADR `:664`), and it contradicts the companion rule draft: "Of the 16-file dialect corpus + 3 canonical ADRs, the **18 reachable** by the `projects/*/decisions/` + `docs/design/` scan path pass the grandfather regression test; the entity-embedded `ADR-STORY015-001` is out-of-scan (R-10)." (rule draft `:94`). The subtraction-pass-notes.md changelog itself records this exact correction as *already done*: "grandfather test narrowed 19→**18** reachable, STORY015 disclosed out-of-scan R-10 (FM-002)" (subtraction-pass-notes.md `:166`). **Independent verification (this review):** `Glob` over `**/decisions/ADR-*.md` (excluding `docs/archive/`) returns 15 files (`ADR-EPIC002-001`, `ADR-EPIC002-002`, `ADR-PROJ010-001..006`, `ADR-PROJ022-001..002`, `ADR-150-001`, `ADR-PROJ031-001..004`), and `Glob` over `docs/design/ADR-*.md` returns 3 (`ADR-agent-design-001`, `ADR-output-path-resolution-001`, `ADR-routing-triggers-001`) — 15 + 3 = **18**, matching the corrected figure, not the M-6 row's stale 19. `ADR-STORY015-001` is confirmed to live outside any `decisions/` directory (at `.../STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md`), confirming it is out-of-scan as R-10 states.

**Evidence:** ADR `:517` (M-6, stale "19"), ADR `:664` (Enforcement Design, correct "18"), rule draft `:94` (correct "18"), subtraction-pass-notes.md `:166` (claims the 19->18 correction was already made repo-wide); independent `Glob` results listed above (15 dialect + 3 canonical = 18).

**Impact:** M-6 is marked "Yes" (gating) in the Migration Plan. As written, an implementer following M-6 literally would target a regression-test invariant ("19 files pass L-1 via the scan path") that is arithmetically unsatisfiable given the same document's own disclosed out-of-scan exclusion of `ADR-STORY015-001` — the 19th file is, by the ADR's own R-10 disclosure, never reached by the scan path, so it cannot "pass" a test it is never subjected to. This is precisely the class of count-reconciliation defect the document otherwise prides itself on catching (DA-003, CC-002, CC-003, SM-102, FM-002-iter6 are all prior instances of the *same* self-correction discipline); one live instance of the same class of error survived the iteration-6 remediation pass unedited.

**Dimension:** Internal Consistency (0.20), Methodological Rigor (0.20).

**Response Required:** Correct the M-6 row's parenthetical to "(15 dialect + 3 canonical = 18 files pass L-1; `ADR-STORY015-001` out-of-scan per R-10)" to match `:664` and the rule draft.

**Acceptance Criteria:** All three locations (M-6 row, Enforcement Design section, rule draft) state the same reachable-file count, and the count matches a fresh repo-wide Glob at merge time.

---

### DA-004: L-4 provides zero (not degraded) enforcement in repository-based topology, the ADR's own named likely downstream-adopter topology [MAJOR]

**Claim Challenged:** L-4 rule definition: "A `PROJ{NNN}`/`EPIC{NNN}`/`STORY{NNN}` dialect prefix matches its containing project/entity dir (**project-based topology**)." (ADR `:662`; rule draft `:176` uses identical wording). Canonical Location Model note: "the dialect presumes the project-based tree and SHOULD NOT be used in repository-based repos." (ADR `:383`).

**Counter-Argument:** L-4 is not merely *weaker* in repository-based topology — it is **inapplicable**, i.e. it performs zero checks there, because its entire logic depends on a `projects/PROJ-{NNN}-*/` path segment that a repository-based repo structurally does not have. The document's own subtraction-pass-notes.md confirms the supporting control for repository-based dialect misuse (former **L-4b**) was one of the 13 rules deleted outright, and re-dispositions the gap as "plain **SHOULD-NOT guidance**" (subtraction-pass-notes.md, Major Findings table, RT-007 row). But PROJ-031 — the project producing this very ADR — exists specifically to build a distribution/skeleton for **downstream CoWork/plugin adopters** (ADR `:638-651`, Enforcement Scope table), and the ADR itself names repository-based topology as a live possibility for exactly that audience ("**downstream plugin adopters (PROJ-031's stated audience) may run the repository-based topology**", ADR `:383`). This means the one lint rule most relevant to "does a dialect ID actually match where it lives" — the rule most directly responsive to the user's "collision-safety" attack question — has **no operative form at all** for what may be the primary real-world deployment target of this entire distribution effort, and this is disclosed as a downgrade-to-guidance rather than as a "zero coverage for a named likely-majority audience" gap.

**Evidence:** ADR `:662` and rule draft `:176` (L-4's project-based-topology scoping), ADR `:383` (repository-based topology named as a likely downstream pattern), subtraction-pass-notes.md Major Findings table RT-007 row (L-4b deleted, re-dispositioned as SHOULD-NOT guidance), ADR `:638-651` (PROJ-031's downstream/plugin audience framing).

**Impact:** Understates the practical enforcement gap for the deployment context PROJ-031 says it is building for. "SHOULD-NOT guidance" and "zero mechanism, structurally, for this topology" are materially different claims; the document uses language ("re-dispositioned...not rebuilt behind a lint rule") that reads as a graceful downgrade rather than naming that the affected population could be the numeric majority of actual adopters.

**Dimension:** Completeness (0.20), Actionability (0.15).

**Response Required:** Either state explicitly, next to L-4's definition, that it has zero operative effect in repository-based topology (not merely "not applicable" as a scoping footnote), or add a repository-based-topology-aware variant of L-4 keyed on `{RepositoryRoot}/decisions/` (a location the ADR already names at `:376` as the canonical repository-based home), which would not re-add the deleted machinery so much as generalize the one retained location-consistency rule to the second of the two topologies this ADR explicitly supports.

**Acceptance Criteria:** The Canonical Location Model and Enforcement Design sections state, in one place, exactly which lint rules (of L-1/L-2/L-3/L-4/L-7) do and do not operate under repository-based topology, and name the resulting coverage gap's likely audience size candidly.

---

### DA-005: "Not phased, not committed" conflicts with named, threshold-triggered escalation commitments that have no measurement mechanism [MAJOR]

**Claim Challenged:** "**Descoped, honestly (not phased, not committed).**... None of the above is promised for a later release; if a specific gap causes real pain, a future amendment MAY add a single targeted rule." (ADR `:666`; near-identical wording in rule draft `:194`).

**Counter-Argument:** Several of the very residuals this note describes as "not committed" carry named, specific, threshold-triggered escalation plans elsewhere in the same document: R-6 defines a **concrete numeric threshold** — "`≥ 2 distinct L-3 collision failures on `main` within any rolling 90-day window`" — that "triggers a review of whether to tighten to a per-domain `NNN` reservation convention... via amendment" (ADR `:462`, DA-009). R-7 states: "if slug-squatting is observed in practice, add a per-slug-family topical-coherence review at a defined cadence... or a lightweight... gate" (ADR `:454`). PM-009 states a **commitment**, verbatim: "Commitment: re-examine the promotion rate after the next 2–3 framework-relevant projects produce ADRs; if forward promotion stays ≈0%... Scheme C should be reconsidered via a superseding ADR" (ADR `:461`). These are, functionally, a phased commitment roadmap (if condition X, then action Y) — the opposite of "not phased." More importantly, **none of the trigger conditions has a named measurement mechanism**: R-6's own text concedes "the threshold... is revisable once real L-3 telemetry exists" (ADR `:462`) — but no L-3 telemetry mechanism appears anywhere in the 14-row Migration Plan, meaning there is currently no way to detect whether the R-6 threshold has even been crossed. The same applies to R-7 ("if slug-squatting is observed in practice" — observed by whom, tracked how?) and to PM-009 ("re-examine... after the next 2-3 framework-relevant projects" — no owner or trigger-check cadence named beyond the text itself).

**Evidence:** ADR `:666` (the "not committed" framing) and rule draft `:194` (identical framing), against ADR `:462` (R-6/DA-009 threshold), `:454` (R-7 escalation), `:461` (PM-009 commitment, literal word "Commitment").

**Impact:** This is not a fabrication concern (P-022 is otherwise well-served throughout the document) — it is a **tone/substance mismatch**: readers evaluating "is the descoped list honest or a hidden commitment" will find the document simultaneously asserts "nothing is committed" while also stating literal commitments with numeric thresholds, and none of those thresholds is actually measurable today. A commitment that cannot be detected as triggered is not meaningfully different from no commitment at all, except that it reads as more reassuring.

**Dimension:** Actionability (0.15), Traceability (0.10).

**Response Required:** Either soften "not committed" to acknowledge the named escalation triggers exist as conditional commitments (distinct from "new lint rules," which genuinely are not promised), or add a Migration Plan task to build the minimal telemetry (e.g., a scheduled CI job logging L-3 failure counts) that would make the R-6 threshold and PM-009's review cadence actually checkable rather than aspirational.

**Acceptance Criteria:** The "not committed" language and the R-6/R-7/PM-009 threshold language are reconciled to say the same thing, and at least R-6's threshold has a named, even if manual, detection mechanism.

---

### DA-006: "Gating?" column's reconciled meaning does not match the tone of specific rows [MINOR]

**Claim Challenged:** "**'Gating?' column, post-ratification (PM-002/FM-006, iter-6).** With the two-tier ratification gate deleted (v1.7), a 'Yes' no longer gates *ratification*... It now means the row **gates the two remaining bundled milestones**: this ADR's own Path-2 self-promotion (M-9) and the lint's ship-readiness (M-6)... It is a **sequencing flag, not an enforcement gate**." (ADR `:502`)

**Counter-Argument:** M-12's own "Gating?" cell reads: "**Yes — the producing agent must emit compliant IDs or the convention is defeated at the source**" (ADR `:523`). This is stronger, more consequential language than "sequencing flag" — it reads as an existential claim about the convention's viability, not a note about sequencing relative to M-9 or M-6 specifically. M-12 (fixing the ADR-producing agent's hardcoded non-compliant grammar) has no stated causal dependency on M-9 (this ADR's own self-promotion) or M-6 (the lint shipping); it is about the correctness of *future agent-authored ADRs* generally, a distinct concern from either named milestone.

**Evidence:** ADR `:502` (the reconciliation note) vs. `:523` (M-12's row).

**Impact:** Minor internal-consistency wrinkle; does not change the underlying decision, but readers relying on the reconciliation note's uniform "sequencing flag" framing may under-weight M-12's practical urgency, or conversely wonder why M-12 doesn't literally block M-9/M-6 if it is truly "gating."

**Dimension:** Internal Consistency (0.20).

**Response Required:** Either soften M-12's "Gating?" cell language to match the "sequencing flag" framing, or carve out an explicit exception in the `:502` reconciliation note for rows (like M-12) whose gating relationship is to the convention's overall integrity rather than to M-9/M-6 specifically.

**Acceptance Criteria:** The reconciliation note explains, or the row language matches, without requiring the reader to reconcile the two independently.

---

### DA-007: R-9 (case-fold slug lookalike) may be under-rated given its direct relevance to the ADR's central promise [MINOR]

**Claim Challenged:** "R-9: **Case-folded slug look-alike** (RT-102, iter-6) — a lowercase slug that case-folds to a dialect prefix (`ADR-proj031-001` shadowing `ADR-PROJ031-001`) passes L-1 and is tracked as a distinct identity | **LOW** | LOW–MED |" (ADR `:456`)

**Counter-Argument:** The example chosen to illustrate this residual is drawn from `PROJ031` — the very project producing this ADR — which makes it a concrete, not merely hypothetical, near-miss. A case-folded lookalike defeats exactly the mechanism (L-1 grammar + L-3 exact-string dedup) that the user's attack question asks about ("does the slimmed lint still deliver the collision-safety the ADR claims?"): two visually-identical identities are treated as distinct by the lint, which is the discoverability/clustering failure mode this entire ADR exists to eliminate (BUG-006). Rating this LOW probability may be reasonable (authors are unlikely to *deliberately* case-fold), but LOW–MED *impact* seems conservative given that a successful instance would silently defeat the ADR's headline discoverability promise for that specific identity pair, with no lint signal at all (by design: L-1 accepts it, L-3 does not flag it because the strings differ case-sensitively).

**Evidence:** ADR `:456` (R-9 row and its LOW/LOW-MED rating).

**Impact:** Modest — the residual is already disclosed and reasoned (restoring the deleted L-1a/L-1b split was correctly declined per subtraction doctrine), so this is a severity-calibration quibble, not a missing disclosure.

**Dimension:** Methodological Rigor (0.20).

**Response Required:** Consider whether LOW-MED impact should read MED, given the residual maps directly onto the ADR's central discoverability claim rather than a peripheral concern; acknowledgment sufficient if the author judges LOW-MED already reflects this.

**Acceptance Criteria:** Acknowledgment; no revision required (P2).

---

### DA-008: Waiver-ledger deletion removes override-pattern observability with no replacement [MINOR]

**Claim Challenged:** "**Waiver ledger** (`adr-lint-waivers.yaml`... append-only audit)... [deleted]... Override model after subtraction: the **standard MEDIUM mechanism** — SHOULD + a small lint + override-with-documented-justification-in-the-PR... No ledger, no CODEOWNERS gate, no enum." (subtraction-pass-notes.md `:54`, `:61`)

**Counter-Argument:** The waiver ledger's *form* (self-approvable, unbounded `expires`, solo-CODEOWNERS) was correctly identified as broken and its deletion is well-justified. But the ledger also served a second, distinct function the subtraction pass does not address: a single, queryable place to see the **aggregate pattern** of overrides over time (which rule is overridden most often, by whom, how frequently) — a convention-erosion early-warning signal. Under "documented justification in the PR," this information still exists, but only diffusely, scattered across individual PR descriptions with no aggregation mechanism. If, say, L-1's grammar proves too strict in practice and is overridden in 40% of new ADRs, nothing in the retained mechanism would surface that pattern except a manual `git log`/PR-description trawl.

**Evidence:** subtraction-pass-notes.md `:54` (deletion rationale, correctly scoped to the ledger's *broken* properties) and `:61` (the replacement mechanism, which has no aggregation capability).

**Impact:** Low — this is a genuine but modest observability loss, consistent with how MEDIUM-tier overrides are handled elsewhere in Jerry (no ledger requirement exists in the SSOT for other MEDIUM rules either), so it is not a deviation from Jerry norms, just a residual worth naming.

**Dimension:** Traceability (0.10).

**Response Required:** Acknowledgment sufficient; optionally note in a future amendment that override frequency could be sampled at the M-5b review cadence rather than via a standing ledger.

**Acceptance Criteria:** Acknowledgment (P2).

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- **DA-001:** Add a Migration Plan row (or an explicit, owned Residual disclosure) repairing or formally deferring repair of the specific stale citations named at ADR `:113` (`WORKTRACKER.md:106-107`, `EN-001.md:48-49,72-73`). Acceptance criteria: the document's own headline motivating evidence has a disposition — fixed, tasked, or honestly disclosed as will-not-fix — matching the rigor already applied to every other named residual.

**P1 (Major -- SHOULD resolve; require justification if not):**
- **DA-002:** Reconcile Positive-1's "eliminates the demonstrated failure mode" claim with the document's own `:549` disclosure that the supporting citation-ratio excludes the corpus bearing the actual wound. Acceptance criteria: the claim's scope matches its evidence.
- **DA-003:** Correct M-6's "19 files" to "18 files" (matching `:664` and the rule draft, and matching independent Glob verification). Acceptance criteria: all three locations state the same count.
- **DA-004:** Disclose explicitly that L-4 has zero operative effect in repository-based topology (PROJ-031's own named likely downstream audience), not merely "not applicable." Acceptance criteria: coverage gap and its likely-audience size are stated candidly in one place.
- **DA-005:** Reconcile "not phased, not committed" with the R-6/R-7/PM-009 threshold-triggered commitments; name at least a manual detection mechanism for the R-6 threshold. Acceptance criteria: no reader-visible contradiction between the descoped note and the escalation-path language.

**P2 (Minor -- MAY resolve; acknowledgment sufficient):**
- **DA-006:** Acknowledge or soften the M-12 "Gating?" cell's tone mismatch with the reconciliation note.
- **DA-007:** Acknowledge whether R-9's LOW-MED impact rating already accounts for its direct relevance to the ADR's discoverability promise.
- **DA-008:** Acknowledge the override-pattern observability loss from the waiver-ledger deletion; optional future-amendment note.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001 (unaddressed headline motivating evidence), DA-004 (zero enforcement in repository-based topology for a named likely audience) |
| Internal Consistency | 0.20 | Negative | DA-002 (claim/evidence scope mismatch), DA-003 (19-vs-18 count contradiction, independently verified), DA-006 (Gating-column tone mismatch) |
| Methodological Rigor | 0.20 | Negative | DA-003 (a count-reconciliation defect of exactly the class this document otherwise catches, surviving the iteration-6 pass), DA-007 (severity-calibration quibble) |
| Evidence Quality | 0.15 | Negative | DA-002 (citation-ratio evidence does not support the claim it is cited for) |
| Actionability | 0.15 | Negative | DA-001, DA-004, DA-005 (no named owner/task/detection mechanism for the respective gaps) |
| Traceability | 0.10 | Negative | DA-005 (no measurement mechanism for named thresholds), DA-008 (override-pattern observability loss) |

**Overall assessment:** The post-subtraction package is largely honest and its self-correction discipline is real (verified: the iter-6 L-3 regex fix genuinely broadens dialect-ID collision detection; the 72%/28% figure is disclosed as narrow-scoped rather than hidden). But on the three specific attack angles mandated for this review: (1) the slimmed lint's collision-safety claim is *directionally* sound for exact-duplicate IDs but has a live, verified internal contradiction in its own gating acceptance test (DA-003) and a structural, likely-majority-audience gap (DA-004); (2) among the deletions, **L-8 (free-text citation scan) was load-bearing for exactly the citation type (full-path/markdown) that produced the still-unrepaired founding wound**, and that wound now has no remediation task at all (DA-001, DA-002); (3) the descoped list is mostly honest, but its "not phased, not committed" framing sits uneasily next to several named, threshold-triggered commitments that cannot currently be detected as triggered (DA-005). Recommend **REVISE**, prioritizing DA-001 (Critical) and DA-002/DA-003/DA-004/DA-005 (Major) before this package is treated as closing the collision-safety and citation-continuity questions it was designed to answer.

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 1
- **Major:** 4
- **Minor:** 3
- **Protocol Steps Completed:** 5 of 5 (Assume Advocate Role; Document and Challenge Assumptions; Construct Counter-Arguments; Require Substantive Responses; Synthesize and Score Impact)
