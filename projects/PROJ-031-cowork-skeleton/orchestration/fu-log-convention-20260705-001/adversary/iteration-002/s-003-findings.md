# Steelman Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, execution metadata |
| [Summary](#summary) | Overall assessment and improvement count |
| [Step 1-2: Charitable Reading + Weakness Classification](#step-1-2-charitable-reading--weakness-classification) | Core thesis, claim inventory, presentation-vs-substance triage |
| [Steelman Reconstruction (targeted)](#steelman-reconstruction-targeted) | Strongest-form patches, inline SM-NNN tags |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded before/after for Major findings |
| [Best Case Scenario](#best-case-scenario) | Conditions under which this design is strongest |
| [Scoring Impact](#scoring-impact) | Dimension-level impact of the findings |
| [Recommendation to Downstream Strategies](#recommendation-to-downstream-strategies) | Guidance for S-002/S-004/S-007/S-014 |

---

## Steelman Context
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` (v3, 2026-07-06) + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Deliverable Type:** Design (Jerry convention proposal: MEDIUM-tier rule file + 2 templates + examples appendix + hook design note)
- **Criticality Level:** C4 (Critical) — engagement gate 0.95
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 2, blind protocol) | **Date:** 2026-07-06 | **Original Author:** ps-architect

---

## Summary

**Steelman Assessment:** This is the v3 (iteration-1-remediated) revision of an already-substantial design; the package has already absorbed a prior 0.64→REVISE cycle (per its own changelog) and closed the Internal-Consistency-driving overclaims that cycle found (collision "cannot" → "collision-resistant," "guarantee...survive compaction" scoped to persistence-of-captured-entries, "immutable once sealed" → "immutable-by-convention"). Under the strongest charitable reading, the surviving gaps found in this pass are refinements of presentation and cross-file completeness, not substance — no gap here invalidates the core argument or reintroduces the overclaimed-coverage failure mode this project was warned against.
**Improvement Count:** 0 Critical, 4 Major, 3 Minor
**Original Strength:** High. The core thesis (two lightweight, git-native, append-only ledgers, MEDIUM-tier because the HARD ceiling is full, with disclosed residual risks rather than invented enforcement machinery) is sound, evidenced, and consistently anti-bloat. Disclosure discipline (PROPOSED-DEFAULT tags, `[INFERENCE]` labels, residual-risk call-outs) is applied more rigorously here than in most C4 packages reviewed at this tier.
**Recommendation:** Incorporate the 4 Major findings before the C4 gate — all are additive-clarification fixes (a sentence or a schema line each), consistent with the anti-bloat doctrine (no new machinery, no new lint, no new rule). None require a design change.

---

## Step 1-2: Charitable Reading + Weakness Classification

**Core thesis:** Two append-only Jerry conventions — FEEDBACK-LOG and LLM-DECISION-LOG — persist user feedback and LLM-decision provenance across compaction/session/model-swap boundaries, at MEDIUM tier (the HARD ceiling is full at 25/25), built from a genuinely useful but never-codified prior-art pattern, deliberately minimal per the ADR-convention over-engineering lesson (iteration-005 composite 0.66) already learned in this same project.

**What the charitable reading resolves without further findings** (already fixed by the v3 remediation, verified present in the current text, not re-litigated here): the "cannot collide" → collision-resistant-under-single-writer-discipline softening (L1.1); the L0 scope note distinguishing persistence-of-captured-entries from capture-completeness; "immutable once sealed" → "immutable-by-convention (git-backstopped)" (L1.4, standards.md, examples-appendix.md all consistent); the `source`-as-Context-subfield fold across all four staged artifacts; the alias fallback `—` symmetry between logs; the H-31 back-reference disambiguation guidance; the post-rotation parity check; the segment-index growth-bound disclosure; the multi-scope discovery caveat; the ≤3-lint-check ceiling honored by folding cap-crossing and contiguity detection into existing checks rather than adding a 4th.

**Surviving weaknesses (all presentation/structure/evidence, none substantive):**

| Weakness | Type | Location | Magnitude |
|---|---|---|---|
| L0 headline items (3)/(4) present "harness-stamped provenance" and "hook-maintained ordinal" as accomplished replacements without the adjacent "designed, not yet shipped (Q3)" hedge that the Improvement Ledger row 3 and L1.3 carry | Presentation (internal-consistency risk recurrence) | design doc L0, line 36 | Major |
| Rule file (`feedback-decision-logs-standards.md`, the artifact that actually ships to `.context/rules/`) omits the "collision-resistant, not collision-proof" residual-risk framing for LOG-M-005/lint check 2 that the design doc carries in L1.1 | Structural/Evidence | standards.md LOG-M-005 + L5 Lint §2 | Major |
| F-027 rebuttal's load-bearing claim — "the assistant's capture-time self-check is the preventive layer" — cites a mechanism that is not defined anywhere else in the four staged artifacts or the design doc | Evidence | design doc UX Findings Disposition, F-027 row | Major |
| Q2's `scope: framework` tag (PROPOSED-DEFAULT) has no schema anchor: neither template's Context-field definition, nor the standards.md Context gloss, lists a `scope` sub-field | Structural | design doc Q2 row + standards.md Scoping section | Major |
| Adoption plan step 4 claims bootstrap "operator labels are recorded as aliases" but the live bootstrap heading syntax reads `(user label: FU.0.1)`, not the ratified `(alias: FU.0.1)` — no explicit rename action is listed | Structural | design doc L2 Adoption/migration plan, step 4 | Minor |
| F-010 rebuttal's stated reasoning ("A state machine is precisely the worktracker DECISION entity's job... graduation covers it") is a non-sequitur for an ordinary (non-graduated) FEEDBACK-LOG entry, weakening an otherwise sufficient rebuttal (lint check 3 alone already suffices) | Presentation (logical connection) | design doc UX Findings Disposition, F-010 row | Minor |
| L5 Lint check 1 describes cap-crossing detection as "the same line-counting pass," which does not literally cover the `~50-entry` half of the OR-cap without an entry/heading count — converges in practice per the design's own line/entry math, but is imprecisely worded | Methodological (precision) | standards.md L5 Lint §1; design doc L2 lint §1 | Minor |

---

## Steelman Reconstruction (targeted)

Per H-02/P-020, the deliverable is not edited directly; strengthened wording is proposed here for the owner to incorporate. Each patch is additive (a clause or a schema line), preserving the original thesis, consistent with the anti-bloat doctrine.

**[SM-001] design doc, L0, line 36** — add the same hedge already used elsewhere:
> *Before:* "(3) **harness-stamped provenance** replaces hand-typed model/session labels that drifted ...; (4) a **turn model** (composite anchor + hook-maintained ordinal) replaces manually-declared "rounds" ..."
> *After:* "(3) a **harness-stampable provenance schema** (hook designed, Q3 — shipped as a fast-follow) replaces hand-typed model/session labels that drifted ...; (4) a **turn model** (composite anchor + hook-maintained ordinal, Q3-deferred) replaces manually-declared "rounds" ..."

**[SM-003] standards.md, LOG-M-005** — append the residual-risk clause already present in the design doc:
> *Before:* "...under a **single-writer-per-log** append discipline. The operator's turn/document-local label is kept **verbatim as an alias**..."
> *After:* "...under a **single-writer-per-log** append discipline (collision-resistant, not collision-proof under concurrent/background-agent writers — lint check 2 is the backstop, not a guarantee). The operator's turn/document-local label is kept **verbatim as an alias**..."

**[SM-005] design doc, F-027 row** — either cite the mechanism or drop the claim:
> *Before:* "...the assistant's capture-time self-check is the preventive layer."
> *After (Option A — add the mechanism):* "...the assistant SHOULD sanity-check evidence-link presence/format before finalizing a terminal-disposition entry (a judgment step, not tooling)." *(and add one line to LOG-M-006/evidence guidance so this is not F-027-only.)*
> *After (Option B — drop the unsupported clause, anti-bloat-preferred):* "Post-hoc commit-time lint is the right cheap enforcement for a MEDIUM convention; a real-time validator is machinery the MEDIUM tier does not warrant. Presence-only checking at commit time is an accepted trade for a low-ceremony log."

**[SM-006] standards.md, Scoping section** — anchor the Q2 tag in the schema it will occupy:
> *Before:* "Framework-level feedback during an active project stays in the active-project log with a `scope: framework` tag (PROPOSED-DEFAULT, pending ratification)."
> *After:* "Framework-level feedback during an active project stays in the active-project log with a `scope: framework` tag **appended to the Context line as a trailing sub-field** (PROPOSED-DEFAULT, pending ratification; default `scope: project` need not be written — absence implies project-scope)."

**[SM-002] design doc, L2 Adoption plan, step 4** — add the missing migration action:
> *Before:* "...entries and ids are preserved (FU.0–FU.9, DEC-LLM-001..003 keep their numbers; their operator labels are recorded as aliases)."
> *After:* "...entries and ids are preserved (FU.0–FU.9, DEC-LLM-001..003 keep their numbers); **heading suffixes are renamed from `(user label: X)` to `(alias: X)` at install time** to match the ratified template syntax."

**[SM-004] design doc, F-010 row** — drop the non-sequitur, keep the sufficient reasoning:
> *Before:* "A state machine is precisely the worktracker DECISION entity's job (H-33); graduation covers it. Lint check 3 already asserts terminal evidence. MEDIUM-tier is forced by the 25/25 ceiling."
> *After:* "Lint check 3 already asserts terminal evidence is present (the concrete safeguard F-010 asks for); a full disposition state machine is out of scope for a MEDIUM-tier, low-ceremony log (that ceremony belongs to the worktracker DECISION entity when — and only when — an item graduates there, H-33)."

**[SM-007] standards.md, L5 Lint §1** — precision fix:
> *Before:* "...the same line-counting pass also flags the ACTIVE file when it exceeds the ~800-line/~50-entry cap."
> *After:* "...the same pass also flags the ACTIVE file when it exceeds the ~800-line cap **or its `## FU.N`/`## DEC-LLM-NNN` heading count exceeds ~50** (the two thresholds converge in practice per the ~12–18 lines/entry measurement, L1.4)."

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|--------------|----------|----------|---------------|-----------|
| SM-001-ITER002 | L0 headline overclaims hook-dependent improvements as delivered, without the hedge carried elsewhere | Major | "harness-stamped provenance replaces..." (unhedged in L0) | Adds "(hook designed, Q3 — shipped as fast-follow)" inline | Internal Consistency |
| SM-002-ITER002 | Adoption plan step 4 omits the heading-syntax rename action needed to make the "recorded as aliases" claim literally true | Minor | "...their operator labels are recorded as aliases" | Adds explicit rename action `(user label: X)` → `(alias: X)` | Completeness |
| SM-003-ITER002 | Rule file (operational SSOT) omits the collision-resistant-not-collision-proof disclosure the design doc carries for the same mechanism | Major | LOG-M-005: "...single-writer-per-log append discipline." | Adds "(collision-resistant, not collision-proof...lint check 2 is the backstop)" | Completeness / Traceability |
| SM-004-ITER002 | F-010 rebuttal's stated justification is a non-sequitur (worktracker DECISION state machine does not apply to ordinary FEEDBACK-LOG entries) | Minor | "A state machine is precisely the worktracker DECISION entity's job...graduation covers it." | Drops the DECISION-entity clause; keeps the sufficient "lint check 3" reasoning | Methodological Rigor |
| SM-005-ITER002 | F-027 rebuttal's load-bearing claim references an undocumented "capture-time self-check" mechanism | Major | "...the assistant's capture-time self-check is the preventive layer." | Either defines the mechanism once (LOG-M-006/evidence guidance) or drops the unsupported clause | Evidence Quality |
| SM-006-ITER002 | Q2's `scope: framework` tag has no schema anchor in any Context-field definition | Major | Scoping section states the tag exists; Context schema (both templates + standards.md) never lists it | Adds "appended to the Context line as a trailing sub-field" + default-omission rule | Completeness / Actionability |
| SM-007-ITER002 | Lint check 1's "line-counting pass" wording does not literally cover the entry-count half of the OR-cap | Minor | "...the same line-counting pass also flags...the ~800-line/~50-entry cap." | Clarifies the pass also counts `## FU.N` headings; notes the two thresholds converge by design | Methodological Rigor |

**Finding ID Format:** `SM-{NNN}-ITER002` — execution id `ITER002` denotes this is the iteration-2 blind Steelman pass (folder `adversary/iteration-002/`).

---

## Improvement Details

### SM-001-ITER002 (Major, Internal Consistency)
**Affected Dimension:** Internal Consistency.
**Original Content:** design doc L0, line 36: "(3) **harness-stamped provenance** replaces hand-typed model/session labels that drifted...; (4) a **turn model** (composite anchor + hook-maintained ordinal) replaces manually-declared "rounds"..."
**Strengthened Content:** See [Steelman Reconstruction SM-001](#steelman-reconstruction-targeted).
**Rationale:** The Improvement Ledger (row 3: "hook, Q3 — designed, not yet shipped") and L1.3 ("Whether the hook ships in v1 or as a follow-up is Q3") both correctly hedge this claim. The L0 executive summary — the section most likely to be read in isolation, and the exact layer whose overclaims drove the prior 0.46 Internal-Consistency score (per the v3 changelog's own diagnosis) — restates the same claim as an accomplished fact. A reader who stops at L0 would reasonably conclude the hook already exists. This is a recurrence of the identified failure class in a location the prior remediation pass did not touch.
**Best Case Conditions:** If the L0 hedge is added, the claim becomes fully self-consistent across all three locations (L0, Improvement Ledger, L1.3) with zero new machinery — a one-clause fix.

### SM-003-ITER002 (Major, Completeness / Traceability)
**Affected Dimension:** Completeness, Traceability.
**Original Content:** standards.md LOG-M-005 states the single-writer-per-log discipline as a bare requirement; L5 Lint §2 states id-integrity contiguity checking with no rationale.
**Strengthened Content:** See [Steelman Reconstruction SM-003](#steelman-reconstruction-targeted).
**Rationale:** The rule file is the artifact that actually installs to `.context/rules/` — it is the operational SSOT a future reader (or L5 CI implementer) will consult, not the design doc's narrative history. The design doc's own L5-lint rationale explicitly says lint check 2 exists to "catch[] the id-collision class disclosed at L1.1" (design doc line 201) — but that disclosure never made it into the artifact the lint is actually attached to. Without it, a rule-file-only reader would not know why contiguity matters or that it is a deliberate backstop for an accepted risk rather than decorative validation.
**Best Case Conditions:** A one-clause addition to LOG-M-005 closes the gap without adding a new rule or lint check, fully consistent with the anti-bloat doctrine already governing this package.

### SM-005-ITER002 (Major, Evidence Quality)
**Affected Dimension:** Evidence Quality, Methodological Rigor.
**Original Content:** design doc F-027 row: "...the assistant's capture-time self-check is the preventive layer."
**Strengthened Content:** See [Steelman Reconstruction SM-005](#steelman-reconstruction-targeted), Option A or B.
**Rationale:** Grep across the full deliverable package confirms the phrase "capture-time self-check" (or "self-check") appears exactly once — in this rebuttal cell — and is not defined as a rule, template instruction, or hook behavior anywhere else. The rebuttal's decision to decline a preventive validator is itself sound and anti-bloat-consistent (post-hoc lint is the right cheap enforcement for a MEDIUM convention), but citing an uncited counterbalancing mechanism as load-bearing justification is an evidence gap: either the mechanism should be named once as real guidance, or the rebuttal should stand on the sufficient reasoning it already has (post-hoc lint is appropriate for MEDIUM tier) without invoking a phantom safeguard.
**Best Case Conditions:** Option B (drop the clause) is the more anti-bloat-consistent fix — it requires zero new guidance and the rebuttal remains fully sound on the lint-sufficiency argument alone.

### SM-006-ITER002 (Major, Completeness / Actionability)
**Affected Dimension:** Completeness, Actionability.
**Original Content:** design doc Q2 row and standards.md Scoping section both state the `scope: framework` tag mechanism; grep confirms zero other occurrences of `scope` in the FEEDBACK-LOG/LLM-DECISION-LOG Context-field schema (design doc L1.1, standards.md Context gloss, both templates).
**Strengthened Content:** See [Steelman Reconstruction SM-006](#steelman-reconstruction-targeted).
**Rationale:** Q1 (assistant-verbatim excerpt+pointer) is a comparable PROPOSED-DEFAULT and it IS reflected in the schema (LOG-M-003, both templates' verbatim-policy notes). Q2's tag mechanism receives no equivalent schema anchor, so an implementer ratifying Q2 as-is would not know where the tag is written (a new Context sub-field? a heading suffix? a separate line?). This is an asymmetric completeness gap between two PROPOSED-DEFAULTs of similar design weight, and it is squarely an Actionability concern — the convention would not be directly incorporable on this point without an interpretive choice the design doc does not make.
**Best Case Conditions:** A one-clause addition to the Scoping section (Context-line trailing sub-field, default-omission rule) resolves this without expanding the Context schema's mandatory field count for the common (non-framework) case.

---

## Best Case Scenario

**Ideal conditions:** A single primary operator per project (or a small team honoring the single-writer-per-log discipline as a working norm), moderate feedback volume (well under the ~50-entry/~800-line segment cap before rotation becomes routine), a git-tracked repository (so "immutable-by-convention" sealed segments have a real audit backstop), and eventual delivery of the Q3 hook (so provenance stamping stops depending on manual fill-in).

**Supporting assumptions that must hold:**
1. Concurrent/background-agent writes to the same log file are rare enough that the lint's post-hoc detection (not prevention) is an acceptable risk posture — explicitly disclosed and accepted, not hidden.
2. The ≤3 L5 lint checks are actually wired into CI/pre-commit at install time (the design doc's step 3 already assigns this as an owned, accepted acceptance criterion — a concrete, checkable commitment rather than an unowned "someday").
3. The 4 PROPOSED-DEFAULTs (Q1-Q4) are ratified or amended by the user before install, per the explicit P-020 gate already built into the plan.

**Confidence:** HIGH that the core design (segment rotation, logger-assigned ids + verbatim aliases, MEDIUM-tier rule + ≤3 lint, graduation boundary to worktracker DECISION) is sound and appropriately scoped for a MEDIUM-tier convention at the HARD-ceiling constraint. The 7 findings above are refinements that close the gap between "sound design" and "fully self-consistent artifact set," not signals of a flawed thesis.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-002, SM-003, SM-006 close three schema/migration/disclosure gaps; each is a small addition, not a structural rework |
| Internal Consistency | 0.20 | Positive | SM-001 closes a recurrence of the specific failure class (unhedged claims in an executive-summary layer) that drove the pre-iteration-1 score to 0.46 IC |
| Methodological Rigor | 0.20 | Positive | SM-004 and SM-007 tighten two rebuttal/lint descriptions without changing the underlying method |
| Evidence Quality | 0.15 | Positive | SM-005 removes (or grounds) an uncited mechanism used as load-bearing justification in a rebuttal |
| Actionability | 0.15 | Positive | SM-006 makes Q2 directly incorporable if ratified as-is; the other findings are already directly incorporable one-liners |
| Traceability | 0.10 | Positive | SM-003 carries a design-doc-level risk disclosure through to the rule file that actually ships, closing a traceability break between the two artifacts |

**Net assessment:** All 6 scoring dimensions are positively but modestly affected. No dimension is flagged Negative — no finding here introduces a new weakness; each strengthens an existing, sound position. Consistent with S-003's constructive orientation, none of these findings should be read as grounds for a REVISE/REJECTED verdict on their own; they are the kind of polish appropriate to close before, not because of, the C4 gate.

---

## Recommendation to Downstream Strategies

For S-002 (Devil's Advocate) / S-004 (Pre-Mortem) / S-007 (Constitutional AI) / S-014 (LLM-as-Judge) consuming this Steelman output: the 4 Major findings (SM-001, SM-003, SM-005, SM-006) are legitimate attack surface if left unaddressed — a strict reading of SM-001 could be pressed as a P-022 (no-deception) concern given this project's explicit prior history of L0-level overclaims scoring 0.46 IC; a strict reading of SM-006 could be pressed as an incompleteness finding against the ratification-readiness of Q2. Neither, however, rises to Critical: both are single-clause fixes fully within the anti-bloat doctrine already governing the package, and neither reflects a change of substance to the design. The 3 Minor findings (SM-002, SM-004, SM-007) are presentation polish only. **No finding in this report should be read as license to demand new machinery, new lint checks, or new rules** — every proposed fix is a wording or schema-line addition, consistent with the deliverable's own, well-evidenced anti-bloat posture.

---

*Strategy Version: S-003 Steelman Technique v1.0.0*
*Executed by: adv-executor (blind protocol, iteration 2)*
*Date: 2026-07-06*
