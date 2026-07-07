# Constitutional Compliance Report: ADR-adversary-tournament-protocol-001 (iteration 3)

> **Strategy:** S-007 Constitutional AI Critique
> **Template:** `.context/templates/adversarial/s-007-constitutional-ai.md`
> **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
> **Criticality:** C3 (tournament-declared; the ADR self-declares Auto-C3 via c-007/AE-003)
> **Executed:** 2026-07-07
> **Execution ID:** iter3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverable identifiers |
| [Constitutional Context Loaded](#constitutional-context-loaded) | Sources and principle scope for this pass |
| [Summary](#summary) | Overall compliance verdict |
| [Findings Summary](#findings-summary) | Table of all findings |
| [Detailed Findings](#detailed-findings) | Full evidence, analysis, remediation per finding |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping and constitutional compliance score |
| [Execution Statistics](#execution-statistics) | Counts and protocol-step completion |

---

## Execution Context

- **Strategy:** S-007 (Constitutional AI Critique)
- **Template:** `.context/templates/adversarial/s-007-constitutional-ai.md`
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Executed:** 2026-07-07

## Constitutional Context Loaded

Per Step 1 of the S-007 protocol, this pass loaded: `.context/rules/quality-enforcement.md` (HARD Rule Index, Criticality Levels, Auto-Escalation Rules, HARD Rule Ceiling Derivation), the ADR-standards convention the deliverable claims to dogfood (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`), and the three cited implementation-target files in `skills/adversary/` (`SKILL.md`, `agents/adv-scorer.md`, `agents/adv-selector.md`) to spot-check every file+line citation the ADR makes against them. Scope for this pass, per the assignment brief: Scheme-B id compliance, MEDIUM-tier purity, HARD-ceiling integrity, H-13/H-14/RT-M-010 consistency, H-23 navigation compliance, and P-022 honesty on costs and on proposal-vs-decided framing.

**Positive verification results (not findings, recorded for completeness):**
- H-23: the Navigation table's 17 entries match the document's 17 `##` headings exactly, in order, with correct GitHub-anchor derivation (spot-checked all 17).
- HARD-ceiling claim: quality-enforcement.md's HARD Rule Index currently enumerates 25 rules; the ADR's "25/25 ceiling untouched" claim is accurate, and WI-7's own acceptance criterion ("verified by diff") is a legitimate self-check.
- Citation accuracy: `adv-scorer.md:166-167`, `adv-selector.md:112-128`, `adv-selector.md:89-107`, and `SKILL.md:111-133` were each read and match the ADR's quotes/paraphrases exactly (no misquotation found).
- H-16 ordering and Group-F-last are correctly described as unchanged and match `adv-selector.md`'s actual recommended order.
- No MUST/SHALL/NEVER/REQUIRED language anywhere in the ADR attempts to add a new row to the quality-enforcement.md HARD Rule Index; all such language is either (a) internal ADR "Constraints" framing (c-001..c-007, standard Nygard practice) or (b) proposed agent-guardrail language for the new `adv-verifier` agent, which is the same idiom already used by every existing agent's `forbidden_actions` (not itself a HARD-rule-ceiling addition). MEDIUM-tier purity holds.
- H-13/H-14/RT-M-010 numeric values (0.92 / min-3-iterations / C1=3,C2=5,C3=7,C4=10) are quoted correctly and are not altered by any of the six decisions.

---

## Summary

**PARTIAL compliance.** No HARD-rule violations found — the ADR's central claim ("no HARD rule is touched, 25/25 ceiling untouched") holds up under verification. Three Major findings were identified, all in the register this strategy is built to catch: places where the ADR's own summary/meta framing does not fully reconcile with its own detailed body, which is exactly the kind of self-consistency gap that undermines a document whose subject matter is rigor-about-verification. One Minor completeness gap was also found. **Recommendation: REVISE** (targeted, non-structural — no decision, diagram, or HARD/MEDIUM boundary needs to change).

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CC-001-iter3 | Major | Alignment table's "Implementation Effort: M" enumerates only 6 of 8 proposed work items, silently omitting the new guidance doc (WI-6) and the mandatory validation pass (WI-8) from its own cost characterization | Decision > Alignment |
| CC-002-iter3 | Major | Draft GitHub Issues A-F cover only 7 of the 8 proposed work items; WI-8 — the validation pass that is an explicit precondition of WI-7's SSOT pointer — has no drafted issue | Work-Item Decomposition (PROPOSED) |
| CC-003-iter3 | Major | Frontmatter declares `scope: framework` while the file still resides at the project-scoped `decisions/` location; the Meta-Note's three "deliberately exercised" Scheme-B properties never address this scope-declaration-timing question, which the cited convention itself states as a location-driven, promotion-time transition | Frontmatter; Meta-Note: Scheme B Dogfooding |
| CC-004-iter3 | Minor | The proposed `s-016-refutation-panel.md` template is not referenced anywhere in quality-enforcement.md's Strategy Catalog section, leaving an 11th template undocumented against the SSOT that currently frames the template directory as "all 10 selected strategies" | L1 Technical Implementation (item 2, 7) |

---

## Detailed Findings

### CC-001-iter3: Alignment table's cost summary omits 2 of 8 backlog items [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `## Decision` > `### Alignment` table |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — evaluated against P-022 honest-cost framing and Internal Consistency |

**Evidence:**

The Alignment table states (row "Implementation Effort"): *"One new agent, one new template, three edited artifacts, one SSOT pointer; no code, no HARD-rule work."* That enumeration is exactly 6 items: `adv-verifier.md` (new agent), `s-016-refutation-panel.md` (new template), `adv-scorer.md`/`adv-selector.md`/`SKILL.md` (three edits), and the `quality-enforcement.md` pointer (one SSOT pointer).

The `## L1 Technical Implementation` change-surface list, immediately below, actually has **7** items — item 6 is *"New guidance doc `skills/adversary/references/tournament-runner-guide.md` — the runner's playbook: subtraction-first doctrine, disposition-table format, convergence discriminator, dual-protocol reporting, and the worked 18-round case study distilled from this ADR's evidence."* This is a new, non-trivial document (sized "M" in the backlog, same tier as the new agent and the new template) and it is absent from the Alignment table's own enumeration.

The `## Work-Item Decomposition (PROPOSED)` table then adds an **8th** item, WI-8 ("Validation pass — dogfood the new protocol on a sample deliverable, including one non-ADR-genre case," also sized "M" — requiring an actual C3 tournament run with a non-ADR-genre deliverable), which likewise does not appear anywhere in the Alignment table's cost characterization.

**Analysis:**

Per S-007 Step 3/4, this is evaluated against the honest-cost-framing intent that P-022 (No Deception) protects and against Internal Consistency (S-014 dimension). Nothing is actively hidden — WI-6 and WI-8 are both fully specified later in the same document — but the one authoritative "how much work is this" sentence in the Decision section (the row a ratifying reader is most likely to anchor on) undercounts the backlog by 2 of 8 items (25% of the total items, and 2 of the 4 "M"-sized items — half of the medium-effort work). Both omitted items are substantive: WI-6 is a new reference document requiring synthesis of the entire 18-round case study, and WI-8 is not a documentation task but an operational validation requiring an actual tournament execution. A reader who ratifies based on the Alignment table's summary alone would materially underestimate the total effort. This is not a HARD-rule violation (ADR conventions and Alignment-table content are not HARD-tier), so it does not block acceptance, but it is a genuine Internal-Consistency/Evidence-Quality gap in a document whose own thesis is that summary claims must reconcile with the full record.

**Recommendation:** Expand the Alignment table's "Implementation Effort" cell to enumerate all 8 backlog items (or explicitly state "6 change-surface artifacts + 1 guidance doc + 1 validation pass = 8 work items, M-to-L aggregate effort"), so the one-line cost summary matches the full backlog it summarizes.

---

### CC-002-iter3: WI-8 has no drafted GitHub Issue despite gating WI-7's SSOT pointer [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `## Work-Item Decomposition (PROPOSED)` > "Draft GitHub issues" |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — evaluated against H-32 (GitHub Issue parity) and Actionability |

**Evidence:**

The Work-Item Decomposition table lists WI-8 as a "Task," size M, with an explicit dependency note baked into WI-7's own acceptance criteria: *"Precondition (RSK-7/DA-003-i2): the SSOT pointer — the concrete act of treating the protocol as framework-general — MUST NOT land until WI-8's non-ADR-genre validation has run and its results are attached."* WI-7's `Depends on` column lists `WI-2, WI-3, **WI-8**` (WI-8 bolded for emphasis).

The "Draft GitHub issues (titles + bodies, PROPOSED)" section that follows drafts exactly six issues, Issue A through Issue F, mapped as: A→WI-1, B→WI-2, C→WI-3, D→WI-4, E→WI-5+WI-6, F→WI-7. There is no Issue G (or any issue) mapped to WI-8.

**Analysis:**

`.context/rules/project-workflow.md` (H-32) requires GitHub Issue parity for all worktracker bugs, stories, enablers, and tasks in the jerry repo; the ADR's own preamble to this section states each work item "becomes a worktracker entity and a GitHub Issue per H-32 parity" on approval. The ADR is not itself in violation of H-32 today (none of these are live worktracker entities yet — they are PROPOSED), but it has done the courtesy of pre-drafting issue bodies for 7 of 8 items to smooth the "user review → GH-issue pass" that Author Notes describe as the next step. The one item silently missing a draft is precisely the item load-bearing for the ADR's own disclosed risk mitigation (RSK-7's external-validity concern, and the DA-003-i2 precondition that exists specifically to stop the SSOT pointer from landing prematurely). If the eventual issue-creation pass mechanically works from "the 6 drafted issues" without independently re-deriving WI-8 from the backlog table, the precondition this ADR treats as required has a live path to being silently dropped.

**Recommendation:** Add a seventh draft issue (Issue G) for WI-8, e.g. `test(adversary): validate verified-criticals protocol via C3 tournament incl. non-ADR-genre deliverable`, cross-referencing the WI-7 precondition explicitly in its body so the dependency survives the transcription from ADR to tracked issues.

---

### CC-003-iter3: `scope: framework` declared pre-promotion; unaddressed by the Meta-Note's dogfooding claims [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Frontmatter (lines 1-15); `## Meta-Note: Scheme B Dogfooding` |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — evaluated against Internal Consistency and the ADR-standards convention this ADR claims to dogfood |

**Evidence:**

Frontmatter: `scope: framework # governs the /adversary skill + tournament process framework-wide`, `promoted_from: null`, `promoted_to: null # -> docs/design/ on approval (pure git mv; id UNCHANGED; zero citation churn)`. The file currently resides at `projects/PROJ-031-cowork-skeleton/decisions/`.

`design/adr-standards-rule-draft.md`'s Canonical Location Model table maps `scope: framework` to canonical home `docs/design/`, and `scope: project` to `projects/PROJ-NNN-*/decisions/` — the file's current home matches the **project** row, not the **framework** row it declares. The same file's Promotion Process section describes Path 1 (the exact path this ADR says it will take) as: *"git mv to docs/design/; id + title-slug UNCHANGED; **scope: framework**; bare-ID citations intact"* — i.e., the convention's own Promotion Process names `scope: framework` as an outcome/side-effect of the git-mv, which has not yet happened for this file.

The ADR's own `## Meta-Note: Scheme B Dogfooding` enumerates exactly three properties it claims to "exercise deliberately": (1) subject-encoded canonical-from-birth id, (2) born-in-project / promotes-by-git-mv, (3) frontmatter completeness. None of the three addresses whether `scope: framework` is correctly declared *before* the git-mv the ADR says will set it.

**Analysis:**

This is a genuine tension inside the cited convention itself: ADR-M-007 says "scope is expressed by location (may change)" (descriptive — scope should track where the file currently lives), while ADR-M-013 says scope "SHOULD" be declared "at authoring time" based on the author's intent (prospective — independent of current location, because canonical-slug identity "promotes for free"). The Promotion Process table sides with the descriptive reading, listing `scope: framework` as something the *git mv itself sets*. This ADR — as the acknowledged first test case of the whole convention — has silently resolved that tension in favor of the prospective reading without ever naming the tension or its resolution, in a Meta-Note whose entire purpose is to enumerate exactly how this document deliberately conforms to the convention. This does not touch a HARD rule (ADR conventions are MEDIUM-tier), and it does not change any of the six substantive decisions D-1..D-6, so it is not gate-blocking; but it is a real, checkable Internal-Consistency gap in the one section of the document whose specific job is convention-compliance narration.

**Recommendation:** Either (a) set `scope: project` now (matching current location per ADR-M-007's descriptive reading, promoted to `framework` at the actual git-mv per the Promotion Process table), or (b) keep `scope: framework` but add a fourth bullet to the Meta-Note explicitly naming the M-007/M-013 tension and stating that this ADR resolves it via the prospective (author-intent) reading, so the convention's first dogfood case sets a citable precedent rather than an unstated one.

---

### CC-004-iter3: `s-016-refutation-panel.md` absent from the Strategy Catalog SSOT [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `## L1 Technical Implementation` (items 2 and 7) |
| **Strategy Step** | Step 3 (Principle-by-Principle Evaluation) — evaluated against Completeness |

**Evidence:**

`.context/rules/quality-enforcement.md`'s Implementation section states: *"Strategy Templates: All 10 selected strategies have execution templates in `.context/templates/adversarial/`."* L1 item 2 proposes a new `.context/templates/adversarial/s-016-refutation-panel.md`, and L1 item 7 scopes the `quality-enforcement.md` edit to *"(Implementation section only) — add a pointer to the verified-criticals protocol and this ADR. No HARD rule, weight, threshold, or criticality set is changed."* Neither item touches the Strategy Catalog table (the list of S-001..S-014 selected/excluded strategies) to note that an 11th, differently-purposed template (an adjudication panel, not a scored finder strategy) now exists in the same directory.

**Analysis:**

This does not make the SSOT's "All 10 selected strategies have execution templates" sentence false — it remains true on its own terms — but it leaves the template directory one template ahead of what its own governing catalog documents, with no cross-reference explaining the numbering jump (S-015 excluded, S-016 new-and-different-kind). The ADR's own "naming note (avoid collision)" already anticipates conceptual confusion between Group-D "verify-strategies" (S-007/S-011, finders) and the new Refutation-Panel Verify stage — the same care could easily extend to the catalog-registration gap this finding identifies.

**Recommendation:** Add one sentence to the L1 item 7 scope (or to WI-7's acceptance criteria) noting that the Strategy Catalog table is deliberately left unmodified because S-016 is an adjudication-stage template, not a 11th scored/selected finder strategy — closing the gap with a one-line disclosure rather than a table edit.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor) | CC-004: new template undocumented in the governing catalog |
| Internal Consistency | 0.20 | Negative (Major x2) | CC-001: Alignment-table summary vs. full backlog; CC-003: scope field vs. cited convention's own promotion-process semantics |
| Methodological Rigor | 0.20 | Neutral | No HARD/MEDIUM procedural violations found; six-decision analysis is systematic and internally sound |
| Evidence Quality | 0.15 | Neutral | All four spot-checked file+line citations (`adv-scorer.md:166-167`, `adv-selector.md:112-128`, `adv-selector.md:89-107`, `SKILL.md:111-133`) verified accurate |
| Actionability | 0.15 | Negative (Major) | CC-002: missing draft issue for the one work item (WI-8) gating the SSOT-pointer precondition |
| Traceability | 0.10 | Negative (Major, Minor) | CC-001/CC-002 (backlog-to-summary and backlog-to-issues traceability); CC-004 (template-to-catalog traceability) |

**Constitutional Compliance Score (S-007 operational formula, NOT the SSOT gate):** `1.00 - (0.05 * 3 + 0.02 * 1) = 1.00 - 0.17 = 0.83`

**Threshold note:** This 0.83 figure is S-007's own internal strategy-execution scoring convention (quality-enforcement.md's authoritative >=0.92 threshold and 6-dimension weights are unchanged and are what the tournament's S-014 composite actually gates on). Zero Critical findings means nothing here triggers automatic-REVISE under either the current unconditional rule or this ADR's own proposed verified-only gating — these are three Major + one Minor advisory findings that would, under the ADR's own D-3 subtraction-first doctrine, be closed by a small amount of *additional disclosure text*, not by adding machinery.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 0
- **Major:** 3
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Load Constitutional Context; Enumerate Applicable Principles; Principle-by-Principle Evaluation; Generate Remediation Guidance; Score Constitutional Compliance)
