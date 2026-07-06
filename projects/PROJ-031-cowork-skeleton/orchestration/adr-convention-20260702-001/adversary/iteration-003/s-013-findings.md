# Inversion Report: ADR-PROJ031-004 (ADR Identifier Convention) + adr-standards-rule-draft.md

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (693 lines) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (300 lines)
**Criticality:** C4 (engagement quality gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, independent — iteration 3)
**H-16 Compliance:** S-003 Steelman is embedded throughout the deliverable itself (each of six schemes A-F is explicitly steelmanned per H-16 before critique — see `ADR-PROJ031-004.md:119-166`); this reviewer additionally confirms the deliverable's own extensive self-critique record (iterations 1-2, `Changelog` section) before proceeding.
**Goals Analyzed:** 3 (stated) + 2 (inferred) | **Assumptions Mapped:** 5 | **Vulnerable Assumptions:** 5 (1 Critical, 2 Major, 2 Minor)

> **Blind-protocol note:** This review does not read any other reviewer's output (this iteration or prior). All findings below are derived solely from the two deliverable files, the S-013 template, and other repo files cited as evidence (research corpus, rule files, `explore/trade-study.md`, `Glob` verification of on-disk ADR files).

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1-2: Goals and Anti-Goals](#step-1-2-goals-and-anti-goals) | What would guarantee failure |
| [Step 3-4: Assumption Map and Stress Tests](#step-3-4-assumption-map-and-stress-tests) | 5 assumptions inverted |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence and analysis per finding |
| [Zero-Governance Null Alternative — Independent Re-Test](#zero-governance-null-alternative--independent-re-test) | Second goal-inversion requested by the task |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

This package has already absorbed two prior remediation rounds (scores 0.67, 0.54 per the Changelog) and is dense with self-correction. Inverting the goal ("what would guarantee this fails or makes the repo worse?") surfaces one **Critical** finding that survived both prior rounds untouched: the package builds an elaborate, gated Migration Plan (14 items, several marked "ratification blocker") but supplies **zero technical mechanism** preventing the `status:` field from being flipped `PROPOSED` -> `ACCEPTED` before any gating item — including the lint itself (M-6) — actually lands. This is the exact "prose promise, no deterministic gate" failure mode the package elsewhere insists on eliminating (its own words: "a prose table row is a plan, not evidence of completion," `ADR-PROJ031-004.md:444`), applied reflexively to itself and left unresolved. Two **Major** findings follow: an unresolved internal contradiction between the Canonical Location Model's general `ADR-{ENTITY-ID}-NNN` claim and the actually-codified closed 4-prefix dialect grammar (which silently excludes legitimate worktracker entity types `BUG-`, `TASK-`, `DISC-`, `IMP-`); and an overstated rebuttal of the requested zero-governance null alternative that claims the domain-slug scheme's "index is free and always current" while the same document elsewhere (twice) treats that same index as a real, gating, rot-prone governance artifact. Two **Minor** findings round out the assumption stress-test. **Recommendation: REVISE** — the Critical finding is a structural gap in the ratification mechanism itself, not the naming scheme it governs; the scheme (Scheme B / subject-encoded identity) remains sound and is not invalidated by these findings.

---

## Step 1-2: Goals and Anti-Goals

**Stated goals** (from `ADR-PROJ031-004.md:50-56`, D-1 through D-5, `L0: Executive Summary`):
1. G1 — Make ADR identity survive project-to-framework promotion with zero citation breakage (the "decisive property," `:188`).
2. G2 — Preserve provenance without encoding it in the mutable identifier (`:186-187`, `ADR-M-002`).
3. G3 — Enforce the convention deterministically (L5 CI lint) without consuming a scarce HARD-rule slot (`:194`, c-001/c-002).

**Inferred goals** (implicit but necessary for the deliverable to succeed):
4. G4 — The convention must actually take effect (be ratified and enforced), not merely exist as a well-argued but inert document.
5. G5 — The convention must cover the corpus's actual entity-type surface, not just the subset the authors happened to enumerate.

**Anti-goals ("what would guarantee failure at each goal?")**

| Goal | Anti-goal condition (guaranteed-failure recipe) | Does the package currently avoid this? |
|---|---|---|
| G1 | Ratify the scheme, then never build the lint; citations keep breaking exactly as before. | **Partially avoided** — disclosed via Claim-Status blocks (`:554`, rule-draft `:187`) and M-6 is marked a "ratification blocker." See Finding IN-001: the blocker has no technical teeth. |
| G3 | Let "MEDIUM tier, lint-enforced" become "MEDIUM tier, no lint, no enforcement" by shipping the rule file before the lint. | **Not fully avoided** — see IN-001: nothing stops M-2/M-2b (rule + symlink, which *activate* the SHOULD-guidance at L1) from landing before M-6 (the lint) is even started. |
| G4 | Produce a 693-line ADR + 300-line companion so dense that no future agent invocation actually completes the Migration Plan; the convention sits `PROPOSED` forever, or worse, gets rubber-stamped `ACCEPTED` without the work being done. | **Not avoided** — see IN-001. The document's own honesty ("zero worktracker Tasks or GH Issues exist for any row," `:446`) is evidence the anti-goal condition is *already occurring* as of this review. |
| G5 | Design the dialect grammar around the two or three entity types the authors had on-disk examples for, silently excluding the rest of the worktracker ontology. | **Not avoided** — see IN-002: the closed set `{PROJ\|EPIC\|FEAT\|STORY}` omits `BUG-`, `TASK-`, `DISC-`, `IMP-`, all of which are documented, live worktracker entity-ID prefixes (`.../explore/trade-study.md:56`; `skills/worktracker/rules/worktracker-entity-hierarchy.md:43,57`). |

---

## Step 3-4: Assumption Map and Stress Tests

| # | Assumption (explicit/implicit) | Type | Confidence | Inversion ("what if this is wrong?") | Severity | Finding |
|---|---|---|---|---|---|---|
| A1 | Marking Migration-Plan rows "Yes — gating"/"ratification blocker" is sufficient to prevent `status: ACCEPTED` before the gated work (esp. the L5 lint, M-6) is done. | Implicit | Low | Nothing but prose and future-agent diligence enforces the gate; a rushed or context-limited session (or a well-meaning user asking "just ratify it") can flip `status:` with zero technical resistance. | **Critical** | IN-001 |
| A2 | The Canonical Location Model's "Entity-embedded (permitted): `ADR-{ENTITY-ID}-NNN`" claim is scoped identically to the closed 4-prefix dialect grammar used everywhere else in the package. | Implicit | Medium | The Location Model row is unqualified ("any `{ENTITY}`"); the grammar/lint is a closed enumeration. A `BUG-`/`TASK-`/`DISC-`/`IMP-` scoped ADR is "permitted" by one table and rejected by the lint the other table relies on. | **Major** | IN-002 |
| A3 | Scheme B's domain-slug taxonomy needs no dedicated governance index — "the filename grammar itself" is "free and always current" (`:234`). | Explicit (stated as fact) | Low | The same document elsewhere calls the domain-slug taxonomy "the new long-term liability" needing "a lightweight index... a soft process that can rot" (`:363`) and makes building that index a **gating** Migration-Plan item with a named arbiter (M-5/M-5b, `:455-456`). The "free" framing directly contradicts the "liability/gating" framing. | **Major** | IN-003 |
| A4 | A purely-L1 rule file (auto-loaded prose, no L2 re-injection marker, no Tier-B-style skill-embedded compensating control) is sufficient for the *judgment-based* SHOULD rules (ADR-M-003 "positive certainty of locality," ADR-M-013 declared `scope:`) to survive context rot across long agent sessions. | Implicit | Medium | The framework's own SSOT (`quality-enforcement.md` Enforcement Architecture table) classifies L1-only content as "Vulnerable" to context rot; the deterministic string-pattern rules (L-1..L-10) get an L5 CI backstop, but the two rules requiring actual judgment get none. | **Minor** | IN-004 |
| A5 | The waiver mechanism (>=40-char justification + API-verified second reviewer) is sufficient to prevent low-substance, rubber-stamped waivers of FAIL-class lint rules. | Implicit | Medium | API verification confirms *who* approved, not whether the justification is substantively sound; a 40-character filler string technically satisfies the length gate. | **Minor** | IN-005 |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260702iter3 | Ratification gate for `status: ACCEPTED` has no technical enforcement | Anti-Goal | Low | **Critical** | `ADR-PROJ031-004.md:444,446-465` (Migration Plan); `quality-enforcement.md` Enforcement Architecture (L1-L5) | Methodological Rigor, Actionability |
| IN-002-20260702iter3 | Closed dialect-prefix set contradicts the general "Entity-embedded (permitted)" claim | Assumption | Medium | **Major** | `ADR-PROJ031-004.md:291,332`; `adr-standards-rule-draft.md:67,87`; `explore/trade-study.md:56`; `worktracker-entity-hierarchy.md:43,57` | Internal Consistency, Completeness |
| IN-003-20260702iter3 | "Free, always-current index" claim contradicts "long-term liability / gating M-5b arbiter" claim | Assumption | Low | **Major** | `ADR-PROJ031-004.md:234` vs. `:363-364,455-456` | Internal Consistency |
| IN-004-20260702iter3 | Judgment-based SHOULD rules (ADR-M-003, ADR-M-013) have no enforcement layer beyond vulnerable L1 prose | Assumption | Medium | **Minor** | `adr-standards-rule-draft.md:48,58`; `.context/rules/quality-enforcement.md` Enforcement Architecture table; `agent-development-standards.md` Two-Tier Enforcement Model | Methodological Rigor |
| IN-005-20260702iter3 | Waiver justification length gate (>=40 chars) does not verify substance | Assumption | Medium | **Minor** | `adr-standards-rule-draft.md:191,193` | Actionability |

---

## Finding Details

### IN-001-20260702iter3: Ratification Gate Is Prose-Only, Not Technically Enforced [CRITICAL]

**Type:** Anti-Goal (inversion of G3/G4: "how would we guarantee this convention is ratified without ever being enforced?")

**Original claim:** "**Ratification (`PROPOSED` → `ACCEPTED`) is conditional on independently-verified completion of every gating item, M-6 in particular — not on the presence of these rows**" (`ADR-PROJ031-004.md:444`). Fourteen Migration-Plan rows are marked "Yes" or "Yes — [gating description]" in the `Gating?` column (`:448-465`), including M-6 ("Implement + wire the L5 CI lint... **with the mandatory 16-file grandfather regression test green**... **Yes — ratification blocker**", `:457`) and M-12 (fix the ADR-producing agent, "**Yes — the producing agent must emit compliant IDs or the convention is defeated at the source**", `:463`).

**Inversion:** Invert the goal directly: *what would guarantee this convention is ratified while remaining functionally unenforced?* Answer: flip `status: PROPOSED` -> `status: ACCEPTED` in this file (a single-line edit) without having completed M-6/M-12/M-2b. Nothing in the deliverable prevents this. There is no CI check on the ADR's own frontmatter `status` transition; none of the ten specified lint rules (L-1 through L-10, `:586-598`) validate the *ratification precondition* itself — they all validate ADR *naming/location/tombstone* properties, which are only meaningful once the convention is already live. The document is explicit that, as of this review, **zero** worktracker Tasks and **zero** GitHub Issues exist for any Migration-Plan row (`:446`, its own Claim-Status disclosure) — i.e., the anti-goal condition (declared work with no tracked, verifiable progress) is not hypothetical; it is the document's own current state.

**Plausibility:** High. This is not a contrived edge case — it is the ordinary path by which any `PROPOSED` document becomes `ACCEPTED` in this repo: a human or agent edits the `Status:` line. The document supplies extensive reasoning for *why* the gate should hold (P-020 ratification honesty, M-6 "not an optional follow-up") but supplies no *mechanism* that makes violating it costly or even detectable at the moment it happens.

**Consequence:** If ratification occurs before M-6 (lint) and M-12 (agent fix) land, two compounding failures occur simultaneously: (a) the rule file becomes active governance (per M-2b, symlinked into `.claude/rules/`, auto-loaded at every session start) while carrying zero deterministic backing — a pure Tier-B-without-compensating-controls state, weaker than the framework's own documented Tier B pattern (`agent-development-standards.md` / `quality-enforcement.md` Two-Tier Enforcement Model, which requires *some* compensating skill/CI control, not zero); and (b) `ps-architect` (the ADR-producing agent, per M-12/Fix 3) keeps emitting the exact non-compliant `{ps_id}-{entry_id}-adr-{slug}.md` grammar the convention exists to eliminate, so every ADR authored between ratification and M-12's completion is born already violating the just-ratified rule — precisely the "convention defeated at the source" scenario the document itself names as the reason M-12 is gating (`:463-464`).

**Self-referential irony (P-022):** The document repeatedly, correctly, criticizes exactly this failure mode when directed at *others* — "a prose table row is a plan, not evidence of completion" (`:444`); it built a whole L5 lint apparatus specifically because "MEDIUM tier... SHOULD... overridable with documented justification" was judged insufficient for ADR *naming* discipline. It did not apply the same skepticism to its own ratification event, which is the single highest-leverage transition in the entire document (it is what turns 693 lines of argument into live, auto-loaded governance).

**Evidence:** `ADR-PROJ031-004.md:444` (gating language), `:446` (zero-tracking admission), `:448-465` (Migration Plan table, no dependency/ordering column), `:552-554` (Claim-Status: lint DESIGNED-NOT-BUILT — itself evidence that a prior iteration already surfaced the *lint* gap but not the *ratification-gate* gap this finding raises), `.context/rules/quality-enforcement.md` Enforcement Architecture table (L1 = "Vulnerable" to context rot, L5 = "Immune"; a status flip is exactly an L1-only event with no L5 backstop here).

**Dimension:** Methodological Rigor (the package's own methodology — deterministic gates over prose — is not applied to its own most consequential step); Actionability (the "gating" label is not actionable/enforceable as specified).

**Mitigation:** Add a fifteenth, structural Migration-Plan item — call it M-0 or fold into M-6 — that makes the ratification transition itself lint-checked: e.g., a pre-commit/CI check that fails if a `docs/design/*.md` or `projects/*/decisions/*.md` file's diff sets `status: ACCEPTED` while (a) `scripts/lint_adr_convention.py` does not exist in the same commit tree, or (b) any Migration-Plan row explicitly tagged `Gating: Yes` lacks a linked, closed worktracker Task ID in the ADR's own frontmatter/PS-Integration block. Absent CI tooling, at minimum add a single explicit sentence: "No agent or human SHOULD edit this file's `status:` field to `ACCEPTED` without first pasting the M-6 CI run URL into this ADR's Changelog" — converting the existing prose into a specific, falsifiable, one-step checklist rather than a distributed 14-row promise.

**Acceptance Criteria:** Either (a) a CI/lint mechanism exists that blocks a `status: ACCEPTED` commit lacking verified gating-item completion, or (b) the document adds an explicit, single-sentence, unambiguous pre-ratification checklist gate directly beneath the `Status:` field itself (not buried in the Migration Plan 400 lines later) naming the exact evidence (e.g., "green CI run URL for M-6") required before the field may be changed.

---

### IN-002-20260702iter3: Closed Dialect-Prefix Set Contradicts the General "Entity-Embedded" Location-Model Claim [MAJOR]

**Type:** Assumption (A2)

**Original claim (general form, stated twice):**
- ADR: "| Entity-embedded (permitted) | `projects/.../work/.../{ENTITY}/` | `ADR-{ENTITY-ID}-NNN` | Active (legacy dialect) |" (`ADR-PROJ031-004.md:332`)
- Rule draft ID Scheme table: "| **Dialect** (PERMITTED, discouraged) | `ADR-{PROJECT-ID\|ENTITY-ID}-NNN-{title-slug}.md` | `ADR-PROJ031-005-foo.md` | Project-local only |" (`adr-standards-rule-draft.md:67`) and its own Canonical Location Model mirror at `:87`.

**Codified form (closed, narrower):** "`PROJECT-ID`: one of a CLOSED entity-prefix set `{PROJ\|EPIC\|FEAT\|STORY}\d{3}` — legacy/tactical (PM-005: this is a fixed enumeration, NOT open-ended 'any finer entity ID'...)" (`ADR-PROJ031-004.md:291`), matching the L-1b lint regex `^ADR-(PROJ|EPIC|FEAT|STORY)\d{3}-\d{3}...` in both files (`ADR-PROJ031-004.md:589`, `adr-standards-rule-draft.md:200,203`).

**Inversion:** Invert the "Entity-embedded (permitted)" claim: what if `{ENTITY-ID}` is read literally, as the table states it, rather than as shorthand for the closed 4-item set defined 40+ lines earlier? Then an entity-embedded dialect ADR under any other live worktracker entity type is "permitted" by the Location Model but will fail the actual lint. The worktracker ontology's own scope-prefixed entity set is documented as `PROJ-`, `EPIC-`, `FEAT-`, `STORY-`, `TASK-`, `BUG-`, `DISC-`, `IMP-`, `DEC-` (cited by this very deliverable's own trade study: `explore/trade-study.md:56`, itself quoting `worktracker-directory-structure.md:56-88`), and `Bug`/`Task`/`Spike` are live, documented entity types with their own containment rules (`skills/worktracker/rules/worktracker-entity-hierarchy.md:43,49,57`). A `BUG-`-embedded dialect ADR (e.g., `ADR-BUG006-001-*.md` under a `work/.../BUG-006-*/` folder) is structurally identical in kind to the already-existing, already-grandfathered `ADR-STORY015-001` (entity-embedded under `work/.../STORY-015-*/`, filesystem-verified via `Glob`) — yet it fails **both** L-1a (uppercase, not lowercase-slug) **and** L-1b (`BUG` is not in the `PROJ|EPIC|FEAT|STORY` alternation).

**Plausibility:** Medium-high. No `ADR-BUG*`/`ADR-TASK*` dialect file exists on disk today (confirmed via `Glob` of `**/ADR-*.md` across `projects/` and `docs/` — none found), so this is a *forward-looking* gap, not a currently-broken file. But `BUG-006` (the very entity this ADR's motivating evidence, `BUG-006-adr-naming-evaluation.md`, is named after) is exactly the kind of quality-review/decision-heavy entity type where an author might plausibly want to embed an architecture decision — the gap is realistic, not contrived.

**Consequence:** A future author or agent, reading only the Canonical Location Model table (the natural first stop when deciding where an ADR goes), reasonably concludes any entity-scoped dialect is fine, authors `ADR-BUG006-001-*.md`, and the L5 lint (once built, per M-6) then rejects a filename the ADR's own documentation told them was "permitted." This recreates, in miniature, exactly the kind of "the rule and the enforcement disagree" defect that 5-of-7 adversarial strategies in iteration 1 already caught once for the L-1 lowercase-only regex (`ADR-PROJ031-004.md:577`) — the same *class* of defect (documentation and codified grammar silently diverging) has resurfaced in a different location.

**Dimension:** Internal Consistency (the two same-document tables disagree on scope); Completeness (the entity-type enumeration is incomplete relative to the worktracker ontology this deliverable itself cites as authoritative).

**Mitigation:** Either (a) narrow the Location Model row's example column to explicitly read `ADR-{PROJ\|EPIC\|FEAT\|STORY}-NNN` (matching PM-005's closed-set framing) in both files, or (b) widen the closed set (and the L-1b regex, and the regression-test corpus) to the full worktracker entity-prefix vocabulary (`PROJ|EPIC|FEAT|STORY|TASK|BUG|DISC|IMP`) so the general phrasing in the Location Model table becomes true rather than aspirational. Option (a) is lower-risk (matches the PM-005 rationale already given for keeping the set closed and small) and is the recommended fix.

**Acceptance Criteria:** Both the ADR (`:332`) and the rule draft (`:67,87`) Location-Model / ID-Scheme tables use the identical, explicitly-closed prefix set as the grammar section and the L-1b lint regex — verified by a single grep for `ENTITY-ID` returning zero remaining unscoped instances.

---

### IN-003-20260702iter3: "Free, Always-Current Index" Claim Contradicts the Document's Own "Long-Term Liability / Gating Arbiter" Claim [MAJOR]

**Type:** Assumption (A3), directly bearing on the task-mandated null-alternative benchmark (IN-004 in the source document's own numbering)

**Claim as used to beat the null alternative:** "An index is itself governance — someone must build, run, and keep it fresh (a server-ish process the constraints reject, c-006), **whereas B's 'index' is the filename grammar itself, free and always current**." (`ADR-PROJ031-004.md:234`, inside "The zero-governance null alternative (requested benchmark, IN-004)" section). This is offered as one of four reasons B beats the "do-nothing + search" null.

**Contradicting claims elsewhere in the same document:**
1. "**Taxonomy governance is the new long-term liability.** B trades the *scope portion's* structural collision-*resistance*... for a domain-slug taxonomy that must stay coherent... This needs **a lightweight index** (`docs/design/README.md`) **and an arbiter** (TBR-2). **This is a *soft* process that can rot** ... Named here so it is owned, not discovered." (`:363`)
2. Migration Plan M-5: "Add `docs/design/README.md` domain index (**also the canonical taxonomy registry — see M-5b**) + `docs/adrs/README.md` frozen banner... **Yes** (elevated from optional iter-1: it is the manual collision check until the lint ships...)" (`:455`)
3. M-5b: "**Name the taxonomy arbiter (TBR-2).** Assign domain-slug approval to a concrete owner/process: the `ps-architect` agent SHOULD run an automated fuzzy-match... and flag near-duplicates... for human adjudication." (`:456`)

**Inversion:** Invert the "free and always current" claim directly: what if it is *not* free, and requires exactly the ongoing build/run/maintain effort the null-rebuttal denies? The document's own Migration Plan answers this for us — M-5/M-5b are not hypothetical, they are gating action items with a named owner ("docs owner"/"ps-architect / governance"), a tracked-but-currently-empty worktracker Task, and a description ("soft process that can rot") that is the textbook definition of "a server-ish process... someone must build, run, and keep... fresh" — the very thing line 234 says B does *not* need. The two passages cannot both be fully true: either the index is free (line 234's claim, used to win the null-alternative argument) or it is a liability requiring an owned arbiter process (lines 363/455/456's claim, used honestly elsewhere in the same document). It is, in fact, the latter — line 234 is the overstated one.

**Plausibility:** High — this is not a speculative inversion, it is a direct textual contradiction within the same 693-line document, verified by three separate line citations.

**Consequence:** This weakens, specifically, the one piece of analysis this review round was explicitly asked to re-test (the "maximum decision-findability with zero governance" null-alternative benchmark). The null-alternative section's strongest anti-null argument ("free and always current") is not true of Scheme B either — Scheme B, honestly read via `:363-364` and M-5/M-5b, *also* requires an index, an arbiter, and ongoing synonymy monitoring (`L-10`, WARN-only). This does not overturn the decision (Scheme B still wins on the citation-continuity argument, which is orthogonal and does not depend on the index being free), but it means the null-alternative rebuttal as written overclaims one of its four supporting legs. See [Zero-Governance Null Alternative — Independent Re-Test](#zero-governance-null-alternative--independent-re-test) below for the full re-run of that comparison.

**Dimension:** Internal Consistency (two irreconcilable claims about the same artifact's cost, ~130 lines apart).

**Mitigation:** Reword `:234` to something like: "B's identity substrate needs no *runtime* index to function as citations (the filename grammar itself is the queryable substrate); it does, like any taxonomy, need a lightweight discoverability/synonymy index (M-5/M-5b) to stay *coherent* over time — a cost this ADR discloses and owns at [L2: Architectural Implications](#l2-architectural-implications), not a cost B avoids." This keeps the genuinely-true part of the claim (no lint/registry is needed for citations to *resolve*, unlike a hash-based or pure-search null) while retracting the overstated "free" framing.

**Acceptance Criteria:** Line 234's claim and lines 363/455-456 are reconciled to a single, consistent cost model for the domain-slug index, cross-referenced in both places.

---

### IN-004-20260702iter3: Judgment-Based SHOULD Rules Have No Enforcement Layer Beyond Vulnerable L1 Prose [MINOR]

**Type:** Assumption (A4)

**Claim:** ADR-M-003 requires authors to judge, at authoring time, whether an ADR has "positive certainty of locality" before choosing the discouraged dialect (`adr-standards-rule-draft.md:48`); ADR-M-013 requires declaring `scope: framework|project` at authoring time and defaulting to canonical-under-uncertainty (`:58`). Both are genuine judgment calls, not string-pattern checks.

**Inversion:** What if a future ADR-authoring agent session simply forgets or misapplies this judgment because the governing rule is L1-only? The framework's own SSOT (`quality-enforcement.md` Enforcement Architecture table) explicitly classifies L1 ("Session start... Behavioral foundation via rules") as "Vulnerable" to context rot, and reserves "Immune" status for L2 (per-prompt re-injection) and L5 (CI). The ten *deterministic* lint rules (L-1 through L-10) all get an L5 backstop (once M-6 ships). The two *judgment* rules do not: nothing re-injects "default to canonical under uncertainty" per-prompt (no L2-REINJECT marker is proposed for `adr-standards.md`), and no skill-embedded compensating control (the Tier-B pattern used elsewhere for H-16/H-17/H-18) is proposed either.

**Plausibility:** Medium. This is exactly the class of failure the framework's own governance literature (`agent-development-standards.md` Two-Tier Enforcement Model, `quality-enforcement.md` Tier Vocabulary) is designed to anticipate for *other* rules; it was simply not applied reflexively to this rule file's two judgment-based standards.

**Consequence:** Minor and self-limiting — a wrongly-judged dialect choice is exactly the discouraged-but-permitted, low-regret Path 2 case the ADR already designs for (rename + tombstone on eventual promotion); it does not corrupt the corpus, only re-introduces the citation-churn tax the whole convention exists to reduce, in the specific cases where judgment fails.

**Dimension:** Methodological Rigor.

**Mitigation:** Either accept the residual risk explicitly (name it alongside R-4/PM-009 in the existing Risks table) or add one lightweight compensating control: a `uv run jerry lint adr --advise` pre-flight hint (already proposed for M-13's CLI form) that prints "no `scope:` declared — defaulting is ambiguous; see ADR-M-013" whenever a new ADR file is saved without a `scope:` field, giving the judgment rule an L3/L4-equivalent nudge without spending an L2 token budget.

**Acceptance Criteria:** Either an explicit disclosed-residual-risk note is added, or the M-13 CLI lint form includes an advisory (non-blocking) check for the presence of `scope:`/dialect-choice reasoning at authoring time.

---

### IN-005-20260702iter3: Waiver Justification Length Gate Does Not Verify Substance [MINOR]

**Type:** Assumption (A5)

**Claim:** A waiver requires "`justification` (>= 40 chars)" plus an API-verified distinct approving reviewer (`adr-standards-rule-draft.md:191,193`).

**Inversion:** What if the justification is 40+ characters of low-content filler (e.g., "This is fine, please approve this waiver now, thanks a lot.") and the approving reviewer rubber-stamps without truly evaluating it? The API-verification fix (RT-004, closing the *identity*-spoofing gap) is real and effective for its stated purpose — confirming a *distinct* reviewer approved — but does not, and cannot by itself, verify *justification quality*. The document's own reconciliation argument for why L-2/L-3 stay "practically strict" without being HARD (`ADR-PROJ031-004.md:584`) rests on "no constructable justification exists" for a genuine ID collision — a claim about the *rule*, not a guarantee about what a rushed reviewer will actually read before clicking approve.

**Plausibility:** Medium — process-fatigue rubber-stamping is a well-documented failure mode in any review gate, not specific to this package, but the package's own tier-reconciliation argument leans on justification-writing being genuinely hard, which a content-blind length check does not enforce.

**Consequence:** Low — this is a defense-in-depth gap, not a primary control failure; branch protection + CODEOWNERS + an audited append-only ledger already provide meaningful friction.

**Dimension:** Actionability.

**Mitigation:** Note (does not require new tooling) that the append-only waiver ledger is itself auditable — add one sentence recommending periodic (e.g., quarterly) human review of `adr-lint-waivers.yaml` entries for justification quality, analogous to the "periodic audit" already recommended for the domain-slug taxonomy (M-5b).

**Acceptance Criteria:** A one-line periodic-audit recommendation is added alongside the waiver mechanism spec.

---

## Zero-Governance Null Alternative — Independent Re-Test

The task asks: *"if we wanted maximum decision-findability with zero governance, what would we do — and does the package beat that null alternative?"* The deliverable already runs this exact benchmark once, labeled "IN-004" in its own numbering (`ADR-PROJ031-004.md:229-234`), against a "no ID convention + rely on a generated index/search" null. This reviewer re-runs it independently, including a stronger null the document did not construct.

**The document's own null ("no convention + search/index"):** correctly loses to Scheme B, for the reasons the document gives — a search index does nothing for a broken hyperlink/path, it has no collision story, and (per IN-003 above) *both* the null and Scheme B actually require an ongoing index-maintenance cost, so that specific axis is a wash rather than a clean win for B — but B still wins decisively on the citation-continuity axis, which the null cannot address at all. **The document's conclusion (a convention is warranted) holds; only its "index is free" framing is overstated (IN-003).**

**A stronger null this reviewer constructs, that the document did not consider: content-addressed/hash-based identity** (e.g., `ADR-{8-hex-hash}.md`, generated at authoring time from content+timestamp, with the human-readable subject purely a cosmetic filename suffix, never authoritative). This null:
- **Beats B on collision-avoidance:** structurally collision-free (no shared taxonomy, no `sort | uniq -d` needed), versus B's disclosed "resistant, not immune" status (the `ADR-EPIC002-001` collision, `:86`).
- **Beats B on governance-zero-ness:** requires no domain-slug taxonomy discipline, no arbiter (M-5b), no synonymy fuzzy-match (L-10) — eliminating exactly the liability the document names at `:363`.
- **Loses badly on the document's *other* first-order goal, discoverability:** a hash is exactly as opaque as the bare `ADR-NNN` Scheme E this document already "decisively dominated... deprecate" (`:158`) — `grep -r "ADR-agent-" docs/design/` (a stated B win, `:374`) has no hash analogue. BUG-006's core discoverability findings (F-001/F-003, cited throughout) are *not* solved by a hash; they are actively reproduced by one.

**Conclusion of the independent re-test:** the task's own framing ("maximum decision-findability" *and* "zero governance," conjunctively) may itself be close to a category error for a subject-organized identifier scheme — maximizing findability-by-subject intrinsically requires *some* shared vocabulary discipline (which is itself a form of governance, however lightweight), and a null alternative that achieves true zero governance (the hash null) necessarily sacrifices findability, landing back in Scheme-E territory. This is offered as **inference** (P-022 label), not verified fact: no external literature citation supports this "these two goals are in tension" claim beyond the internal consistency of the argument itself. Under that reading, the package's core claim survives the stronger null too, but the document's own presentation (`:229-234`) does not surface this reasoning — it constructs and beats a weaker null than the one the task's framing actually implies, and (per IN-003) overstates one of the arguments it does use. **Net assessment: the decision (Scheme B) still beats every null alternative considered, including the stronger hash-based one this reviewer added; the deliverable's null-alternative section itself is the part that needs the strengthening (IN-003 + the above), not the underlying decision.**

---

## Recommendations

| Priority | Finding | Action | Acceptance Criteria |
|---|---|---|---|
| MUST mitigate | IN-001 (Critical) | Add a concrete, single-point technical or checklist gate on the `status:` field transition itself, not just on the 14 downstream Migration-Plan rows. | Green CI evidence or an explicit named checklist directly beneath the `Status:` header is required before any future edit sets `status: ACCEPTED`. |
| SHOULD mitigate | IN-002 (Major) | Reconcile the Canonical Location Model's "Entity-embedded (permitted)" claim with the closed 4-prefix dialect grammar in both files. | Zero unscoped `ENTITY-ID` references remain; L-1b regex, ADR-M-003, and both Location Model tables enumerate an identical set. |
| SHOULD mitigate | IN-003 (Major) | Reword the null-alternative rebuttal's "free and always current" claim to match the document's own "long-term liability / gating arbiter" framing elsewhere. | The two passages describe one consistent cost model, cross-referenced. |
| MAY mitigate | IN-004 (Minor) | Disclose the L1-only enforcement gap for judgment-based SHOULD rules, or add a lightweight CLI advisory. | Either a disclosed-residual-risk note or an M-13 CLI advisory check exists. |
| MAY mitigate | IN-005 (Minor) | Add a periodic-audit recommendation for waiver justification quality. | One sentence added near the waiver mechanism spec. |

---

## Scoring Impact

Mapping to the S-014 scoring dimensions (`.context/rules/quality-enforcement.md`):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002: dialect grammar does not cover the full worktracker entity-prefix surface it implicitly claims to (per the Location Model table). |
| Internal Consistency | 0.20 | Negative | IN-002 and IN-003 are both same-document, verifiable, unresolved textual contradictions — the second (IN-003) directly undercuts the specific null-alternative analysis this review round was asked to re-test. |
| Methodological Rigor | 0.20 | Negative | IN-001: the document's own core methodological principle (deterministic gates over prose promises) is not applied to its own ratification transition — the single highest-leverage step in the whole package. IN-004: judgment-based rules lack the enforcement-tier treatment given to string-pattern rules. |
| Evidence Quality | 0.15 | Neutral | Findings are corroborated by direct citation and, where relevant, `Glob`/`Grep` verification against the live repo (no fabricated evidence). |
| Actionability | 0.15 | Negative | IN-001 and IN-005: both name a real gap in an otherwise highly actionable, mitigation-rich document (which generally scores well here). |
| Traceability | 0.10 | Neutral | All prior review tags (CV-/FM-/PM-/RT-/SM-/IN-/DA-/CC-) remain internally consistent with the glossary at `:46`; this review's own IDs (`IN-NNN-20260702iter3`) are namespaced to avoid collision with the deliverable's in-line iteration-1/2 tags. |

**Overall assessment:** REVISE. One Critical finding (IN-001) targets the package's own governance-of-itself, not the ADR-naming scheme it proposes; the scheme (Scheme B, subject-encoded identity with a permitted dialect and grandfather clause) remains sound under this inversion pass and beats every null alternative tested, including a stronger one this review constructed. The two Major findings (IN-002, IN-003) are same-document internal contradictions that are cheap to fix (a handful of sentences) but should not survive to ratification given how much weight this deliverable places on its own P-022 "no overclaiming" discipline elsewhere.

---

*Template Conformance: S-013 Inversion Technique v1.0.0*
*Reviewer: adv-executor (blind, iteration 3) — no other reviewer's output read, per blind protocol*
*Constitutional Compliance: P-001 (evidence cited for every claim), P-003 (no subagents spawned), P-004 (provenance: all citations are file+line), P-011 (evidence-based), P-020 (no deliverable files edited), P-022 (inferences explicitly labeled, e.g. the null-alternative tension claim and the hash-null construction)*
