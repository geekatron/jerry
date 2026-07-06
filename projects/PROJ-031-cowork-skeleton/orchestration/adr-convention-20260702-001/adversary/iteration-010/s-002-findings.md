# Devil's Advocate Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 10)

> **Strategy:** S-002 Devil's Advocate
> **Deliverables:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11)
> **Criticality:** C4 · **Gate:** 0.95
> **H-16 Compliance:** S-003 Steelman has been applied to this package across prior iterations (e.g. `adversary/iteration-008/s-003-findings.md`, `adversary/iteration-005/s-003-findings.md` — readable, non-blind per protocol). Confirmed satisfied; proceeding to S-002.
> **Blind protocol:** No files under `adversary/iteration-009/` or `adversary/iteration-010/` were read except this output file. `subtraction-pass-notes.md` and iterations 001–008 were read per the explicit exception.
> **Reviewer:** adv-executor (S-002 Devil's Advocate)
> **Date:** 2026-07-06

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All counter-arguments, severity, evidence |
| [Finding Details](#finding-details) | Full analysis per finding |
| [Recommendations](#recommendations) | Prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Summary

After 9 prior tournament iterations and an exhaustive, well-disciplined subtraction pass, the package has already dispositioned 17 Criticals plus 17 named residuals (R-1..R-17, R-A/R-B/R-C). Nearly every angle a Devil's Advocate would normally raise — collision safety, promotion honesty, enforcement Claim-Status, citation staleness — is already disclosed with specific, cited evidence. Playing the assigned role against this hardened package, **3 counter-arguments survive scrutiny as genuinely new** (not restatements of any disclosed R-N/FM/RT/PM/DA/CC/IN/CV/SM finding I could locate in the readable corpus): two Critical, one Major. Both Criticals attack the same two things this iteration's mandate names explicitly — **5-rule lint adequacy** (002-001: L-4 is undefined/broken for a real, heavily-cited pair of grandfathered ADRs, and the stated verification methodology would never have caught it) and **the adoptable-MEDIUM-tier-convention purpose for the named downstream audience** (002-002: the shipped rule file is not self-contained — its own residual-disclosure apparatus is permanently unreachable in every CoWork/plugin build). Recommend REVISE: both Criticals are text/spec-level fixes consistent with the subtraction doctrine (clarify or extend the Location Model; inline or disclose the cross-file dependency) — no new lint rule or machinery is required to close either one.

---

## Findings Table

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| 002-001 | Critical | L-4 (ID↔location) is undefined/broken for real, corpus-resident entity-dialect ADRs; the grandfather regression test never tests L-4 (or L-3/L-7) against the real corpus | ADR: Canonical Location Model, Enforcement Design; Rule draft: Canonical Location Model, L5 CI Lint Specification |
| 002-002 | Critical | The rule draft (the artifact that actually ships to the named CoWork/plugin audience) is not self-contained: 14 bare `R-N` residual-ID citations resolve only in the parent ADR, which is permanently and unconditionally absent from every distributed build | Rule draft: References, ID Scheme, L5 CI Lint Specification; ADR: Meta-Note, Enforcement Scope |
| 002-003 | Major | The "18-file grandfather regression test" gates only L-1; L-3/L-4/L-7 ship with zero dry-run verification against the real corpus, so lint-adequacy claims for 4 of 5 rules rest entirely on manual reasoning, not demonstrated test coverage | ADR: Enforcement Design; Rule draft: L5 CI Lint Specification |

---

## Finding Details

### 002-001: L-4 ID↔location has no defined (or correct) behavior for the corpus's own entity-dialect ADRs, and the stated verification never checks it [CRITICAL]

**Claim Challenged:** The ADR's Canonical Location Model (`ADR-PROJ031-004-adr-identifier-convention.md:384-393`) and the identical table in the rule draft (`adr-standards-rule-draft.md:77-86`) enumerate exactly two dialect-location patterns and only two:

- "Project (permitted dialect)" — `ADR-PROJ{NNN}-NNN` — home `projects/PROJ-NNN-*/decisions/` (ADR:389 / rule-draft:82)
- "Entity-embedded (permitted) — closed prefix set only" — `ADR-{PROJ|EPIC|FEAT|STORY}NNN-NNN` — home `projects/.../work/.../{ENTITY}/` (ADR:390 / rule-draft:83)

L-4 is specified identically in both files: *"A `PROJ{NNN}`/`EPIC{NNN}`/`FEAT{NNN}`/`STORY{NNN}` dialect prefix (the full closed set) matches its containing project/entity dir"* (ADR:689, rule-draft:178).

**Counter-Argument:** The document's own worked example directly contradicts its own Location Model. The ADR itself repeatedly discusses `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` (ADR:113: *"`ADR-EPIC002-002-enforcement-architecture.md` is a separate, legitimately-issued ADR that still lives in `projects/PROJ-001-oss-release/decisions/`"*), and schedules them for a YAML-frontmatter retrofit at Migration-Plan row M-11 (ADR:546: *"onto the framework-cited entity-dialect ADRs `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture` (cited repeatedly from `.context/rules/quality-enforcement.md`)"*). I independently verified via `Glob` (2026-07-06) that both files exist exactly at `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md` and `.../ADR-EPIC002-002-enforcement-architecture.md`.

This is an **EPIC{NNN}-prefixed dialect ID sitting in a plain project `decisions/` folder** — a third pattern the Location Model does not enumerate at all. It is neither the "Project (permitted dialect)" row (which is `PROJ{NNN}`-only) nor the "Entity-embedded" row (which requires `work/.../{ENTITY}/`, not `decisions/`). Two readings of L-4 are possible, and both are bad:

1. **Strict reading** (L-4 verifies prefix-to-directory correspondence, as its name and stated purpose imply): these two files would **FAIL L-4** the next time they are git-modified — which the ADR's own Migration Plan schedules at M-11. The convention's own migration step would trigger a lint failure on the SSOT's two most-cited entity-dialect ADRs.
2. **Loose reading** (L-4 only checks "some project dir," ignoring prefix type for non-PROJ prefixes): then L-4 provides **no actual location-integrity guarantee** for EPIC/FEAT/STORY-prefixed dialects at all — exactly the kind of misplacement L-4's stated purpose ("ID↔location") claims to prevent — silently defeating the rule's documented function for that entire prefix class.

Either reading is a genuine gap. Critically, **neither reading is disclosed anywhere in the 17 registered residuals (R-1..R-17) or the pre-mortem table**, and it is distinct from R-10 (which covers *out-of-scan* locations — repository-based topology and entity-embedded paths *without* a `decisions/` segment). The EPIC002 files are fully *in-scan* (`projects/*/decisions/`); the gap is that their location doesn't match any *defined* pattern for their ID form, not that they're unreached by the scan.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:103` (Context corpus table listing "Entity-ID scoped" family), `:113` (explicit discussion of both files' real location), `:384-393` (Location Model, no matching row), `:546` (M-11 schedules editing these exact files), `:689` (L-4 spec); `adr-standards-rule-draft.md:77-86` (identical Location Model), `:178` (identical L-4 spec). Independently verified via `Glob('**/decisions/ADR-*.md')` on 2026-07-06: `projects/PROJ-001-oss-release/decisions/ADR-EPIC002-001-strategy-selection.md`, `.../ADR-EPIC002-002-enforcement-architecture.md` both confirmed present at that path.

**Impact:** Directly undermines the "collision-free ADR identity" and "5-rule lint adequacy" purposes named in this iteration's mandate. If L-4 is strict, the convention's own migration plan (M-11) breaks CI on its own SSOT-cited ADRs the moment it is executed — a self-inflicted defeat of the "no big-bang, low-regret" design goal (c-003). If L-4 is loose, the rule silently does not do what its name and row purpose claim for two of the closed-set's four prefixes, which is a materially false adequacy claim for "5-rule lint adequacy," not a cosmetic wording issue.

**Dimension:** Methodological Rigor, Internal Consistency

**Response Required:** Either (a) add a third Location Model row explicitly covering "entity-ID-scoped dialect ADR in a plain project `decisions/` dir" as a recognized, grandfathered pattern, and narrow L-4's check to apply directory-prefix matching only to the `PROJ{NNN}` case (explicitly stating EPIC/FEAT/STORY-prefixed files inside a project `decisions/` dir are exempt from directory-correspondence checking), or (b) if L-4 is intended to be strict for all four prefixes, disclose this as a new residual (parallel to R-14/R-15/R-16/R-17) naming the two EPIC002 files as pre-existing non-conforming instances that will need remediation before M-11 can safely touch them.

**Acceptance Criteria:** The Location Model and L-4 spec state a single, unambiguous, testable rule that the two real EPIC002 files either satisfy or are explicitly grandfathered against; the grandfather regression test (or a documented reason it cannot) includes L-4, not only L-1.

---

### 002-002: The rule draft — the only artifact the named downstream audience actually receives — is not self-contained; its residual-disclosure apparatus is permanently unreachable in every CoWork/plugin distribution [CRITICAL]

**Claim Challenged:** The rule draft's References table states plainly: *"`ADR-PROJ031-004` ... the full residual register (R-1…R-17, R-A/R-B/R-C) — the `R-N` shorthand used above resolves there"* (`adr-standards-rule-draft.md:234`). I counted **14 bare `R-N` residual-ID references** in the rule draft body itself (grep, 2026-07-06) — e.g. ADR-M-001's `R-15` cross-reference (`:46`), the Frozen-and-Grandfathered section's `R-14` (`:94`), the L5 spec's `R-9`/`R-10`/`R-13`/`R-16`/`R-17` (`:175,177,179,181,206`), the Supersede-and-Amend section's `R-17` (`:151`) — plus multiple bare internal review-tag citations (e.g. `RT-002-iter8`, `FM-001-iter8`, `012-003-iter9`) that are only glossed in the *parent ADR's* tag glossary (ADR:65), not in the rule draft at all.

**Counter-Argument:** The ADR's own Enforcement Scope table (ADR:663-680) establishes that the **CoWork/plugin distribution is PROJ-031's own named downstream audience**, and that the Phase-3 skeleton generator **unconditionally strips `projects/`** from every build (VALIDATED strip set, not merely recommended — `phase3-skeleton-generation-design.md:159`: `git rm -r projects/ tests/ skills/.graveyard .github`, "retains everything else BY CONSTRUCTION"). The parent ADR lives at `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-...md` — **inside the always-stripped `projects/` tree, unconditionally, regardless of whether M-9's self-promotion to `docs/design/` ever executes** (and even post-M-9, `docs/` is itself a *recommended* — if not yet mandatory — additional strip target per the same design file, `:168-170`, which would keep it absent either way). Meanwhile `.context/rules/adr-standards.md` (the artifact M-2 creates from this very rule draft) is **not** in any strip list and therefore **does** ship to that audience.

The consequence: the one artifact a downstream CoWork/plugin adopter actually receives cites 14 residual IDs and multiple review-tag IDs by bare shorthand, with **its only definition living in a document that is structurally guaranteed never to reach that reader** — not "not yet, until M-2 lands" (which the existing 012-001-iter9 disclosure already covers for the *pre-M-2* state), but **permanently, even in the fully-executed, post-M-2, post-M-9 target state this ADR itself points to as the resolution**. This is a different and unaddressed gap from 012-001's disclosure: 012-001 is about the convention being *entirely absent* before M-2 executes; this finding is about the convention being *present but not self-contained* after M-2 executes — the intended end-state itself ships an artifact with structurally dead internal references.

This is material precisely because the document already demonstrates it cares about exactly this audience's fidelity (the Enforcement Scope table, the 012-001 caveat, the CLI-fallback disclosure) — yet this specific, permanent self-containedness gap was never named among the 17 registered residuals.

**Evidence:** `adr-standards-rule-draft.md:234` (References row naming the dependency), 14 occurrences of `R-9`/`R-10`/`R-11`/`R-13`/`R-14`/`R-15`/`R-16`/`R-17`/`R-A`/`R-B`/`R-C` in the same file (grep count, 2026-07-06); `ADR-PROJ031-004-adr-identifier-convention.md:663-680` (Enforcement Scope table naming the downstream audience); `phase3-skeleton-generation-design.md:159` (`projects/` unconditionally stripped — VALIDATED set) and `:168-170` (`docs/` a *recommended*, not-yet-mandatory, additional strip).

**Impact:** Directly undermines "adoptable MEDIUM-tier convention" — the very purpose this iteration's mandate names. A downstream author trying to understand why, say, L-7 or L-4 behaves the way the rule file says it does hits a dead reference by design, forever, for the framework's own most bandwidth-constrained audience (the one PROJ-031 exists to serve).

**Dimension:** Traceability, Completeness

**Response Required:** Either (a) inline a condensed, self-contained residual summary directly into the rule draft (a short table restating each `R-N`'s one-line substance, not just its ID) so the shipped artifact needs no external file, or (b) add an explicit disclosure at the top of the rule draft (parallel to the existing Claim-Status pattern) stating that the `R-N`/review-tag citations are internal tracking references whose full detail is not available outside the `geekatron/jerry` source repository, and that this is a permanent (not M-2-timing-dependent) property of the CoWork/plugin distribution.

**Acceptance Criteria:** The rule draft either requires zero external file to be fully understood, or explicitly and permanently (not only pre-M-2) discloses that it does.

---

### 002-003: The "18-file grandfather regression test" verifies only L-1; L-3/L-4/L-7 ship with no demonstrated dry-run against the real corpus [MAJOR]

**Claim Challenged:** *"A grandfather regression test gates the lint before it ships: the 18 files reachable by the two-clause scan path ... pass L-1"* (ADR:691; identical wording rule-draft:181, 183).

**Counter-Argument:** The stated verification methodology for "5-rule lint adequacy" tests **exactly one of the five rules** (L-1 grammar) against the real corpus. L-3 (duplicate detection), L-4 (ID↔location), and L-7 (relationship-target resolution) have **no corresponding regression fixture drawn from the actual 18-file corpus** — their correctness rests entirely on manual author reasoning and post-hoc disclosure, not on a demonstrated pass/fail run. This is not hypothetical: 002-001 above is a concrete instance of exactly this gap — L-4 has an undefined/broken outcome for two real corpus files, and the "18 files pass L-1" claim would not have surfaced it because L-4 was never in scope for the regression test to begin with. Separately, the document's own R-16 admits L-7 "has zero real validation targets in this project's own live supersession chain" (ADR:480) — i.e., L-7's real-corpus surface is empty by the author's own account, so "L-7 works" is also an untested claim, not a demonstrated one.

**Evidence:** ADR:691 ("pass L-1" — no L-3/L-4/L-7 mention), rule-draft:181/183 (same); ADR:480 (R-16, L-7 zero real targets); 002-001 above (L-4 concrete failure instance, independently `Glob`-verified).

**Impact:** Weakens "5-rule lint adequacy" as a documented claim: the verification methodology that is supposed to give confidence the lint is safe to ship (per the explicit purpose of the grandfather test, ADR:691: "the dry-run-against-the-real-corpus step whose absence caused an earlier lowercase-only defect") only covers 20% of the rule surface. The lowercase-only defect the test was *introduced to prevent* (iter-6 RT-101) was itself an L-3 bug, not an L-1 bug — meaning the regression test as currently scoped would not have caught the very class of defect that motivated its creation.

**Dimension:** Methodological Rigor

**Response Required:** Extend the grandfather regression test's stated scope to cover L-3, L-4, and L-7 against the real 18-file corpus (even if the expected result for L-3/L-7 is simply "zero collisions / zero relationship targets to check" for L-7), or explicitly narrow the "dry-run-against-the-real-corpus" claim to state it applies to L-1 only and disclose the untested status of the other four rules as a residual.

**Acceptance Criteria:** The regression-test scope statement in both files accurately describes which rules it exercises; if it remains L-1-only, that scope limitation is stated as plainly as the "designed, not built" Claim-Status already is.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- 002-001: Reconcile the Location Model / L-4 spec against the corpus's own EPIC002-prefixed dialect ADRs (add a Location Model row, or narrow L-4's directory-matching scope, or disclose as a new residual). Do this before M-11 executes.
- 002-002: Make the rule draft self-contained (inline residual summaries) or add a permanent (not M-2-timing-scoped) disclosure that its `R-N` cross-references are unresolvable in every distributed build.

**P1 (Major — SHOULD resolve; require justification if not):**
- 002-003: State the grandfather regression test's true scope (L-1 only) explicitly, or extend it to cover L-3/L-4/L-7.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | 002-001: Location Model omits a real, cited, in-scan placement pattern; 002-002: rule draft omits self-contained residual detail |
| Internal Consistency | 0.20 | Negative | 002-001: Location Model contradicts the document's own worked EPIC002 example |
| Methodological Rigor | 0.20 | Negative | 002-001, 002-003: stated verification (grandfather regression test) does not cover the rule where a real defect was found |
| Evidence Quality | 0.15 | Neutral | All three findings are independently file+line verified against the live corpus |
| Actionability | 0.15 | Positive | All three findings have concrete, subtraction-doctrine-consistent remediation paths (spec clarification or disclosure, no new machinery) |
| Traceability | 0.10 | Negative | 002-002: shipped artifact's own cross-references are untraceable for its named audience |

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 2
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (Role assumption, Assumption challenge, Counter-argument construction, Substantive-response specification, Synthesis)
