# Steelman Report: Feedback & Decision Log Convention (FU.2 Design Package)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Scope, deliverable, criticality |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Charitable Interpretation](#charitable-interpretation) | Core thesis, key claims, strengths (Step 1) |
| [Weakness Classification](#weakness-classification) | Presentation/structural/evidence weaknesses (Step 2) |
| [Steelman Reconstruction (Targeted)](#steelman-reconstruction-targeted) | Before/after excerpts for each finding (Step 3) |
| [Best Case Scenario](#best-case-scenario) | Conditions under which the design is strongest (Step 4) |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings (Step 5) |
| [Improvement Details](#improvement-details) | Expanded rationale per finding |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of improvements |
| [Readiness for Downstream Critique](#readiness-for-downstream-critique) | Step 6 sign-off |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + all files in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
- **Deliverable Type:** Design (multi-file convention package: design doc + MEDIUM-tier rule draft + 2 templates + examples appendix + hook design note)
- **Criticality Level:** C4 (Critical) — touches `.context/rules/` on install (AE-002/AE-003), engagement gate 0.95
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-07-05 | **Original Author:** ps-architect (this project)
- **Blind protocol:** no adversary-sibling outputs read; only permitted context (ux/heuristic-evaluation.md, revision-notes.md, research doc, live bootstrap logs) plus the deliverable package itself.

---

## Summary

**Steelman Assessment:** The package is a directionally sound, well-researched, and already-once-revised MEDIUM-tier convention that honestly discloses its own scope limits (token budget overage, pending-ratification defaults, deferred hook). Under strongest charitable reading, its core argument — logger-assigned monotonic ids + verbatim aliases, capped-collection segment rotation, and a lean rule file that points at (rather than embeds) examples — survives intact. The findings below are narrow presentation/traceability gaps, not substantive flaws, and none require new machinery to fix.

**Improvement Count:** 0 Critical, 1 Major, 2 Minor

**Original Strength:** High. The package was already revised once against real user feedback (FU.5/FU.6/FU.8) and a 31-finding UX heuristic evaluation (22 folded / 9 rebutted with anti-bloat rationale). Cross-file consistency is strong overall (scoping rule, id/alias scheme, verbatim policy, and lint-check counts all match across the design doc, rule file, and both templates). Descoping choices (MEDIUM-tier only, ≤3 lint checks, hook designed-but-deferred, backfill execution-gated) are explicitly and honestly labelled `PROPOSED-DEFAULT` — this is legitimate descoped-with-disclosure, not a gap.

**Recommendation:** Incorporate improvements. All three findings are low-cost text fixes (id correction, one forward-reference sentence, one citation anchor) fully within the existing anti-bloat posture — none add new sections, lint checks, or hooks. Ready for downstream critique strategies (S-002/S-004/S-007/S-012/S-013) once these are folded, or in parallel since none is load-bearing for the core design decision.

---

## Charitable Interpretation

**Core thesis:** Turn the [internal-kb] pattern's genuinely good raw material (directional separation, verbatim-wins fidelity, a graduation chain to formal decisions) — which was never codified and had observably drifted (`DJ-025` id collision, hand-typed model/session labels) — into a real, enforced-but-lightweight Jerry convention: two append-only markdown ledgers where every harness-stampable field (session, timestamp, model-per-turn) is designed to be stamped by a fail-open hook, and every ledger is a **capped collection** (not unbounded append-only) so it never outgrows the LLM's own read limits.

**Key claims examined for the strongest interpretation:**
1. Logger-assigned monotonic ids + operator verbatim aliases remove the "operator must track a global counter" burden (FU.6) — verified sound; the mechanism is explained consistently in the design doc, rule file, and both templates, and is already applied in the live bootstrap `FEEDBACK-LOG.md` (FU.5–FU.9 use the alias notation correctly).
2. Segment rotation at ~50 entries/~800 lines keeps every log within the Read tool's ~2,000-line window and under the ~25k-token truncation point — the arithmetic checks out (800/2000 = 40% = "2.5× headroom"; 25k/8–12k ≈ 2.1–3.1× = "2–3× under truncation").
3. The rule file stays MEDIUM-tier (HARD ceiling 25/25, zero headroom) and is honestly reported at ~1,584 tokens against a ~1,500-token target — this is a *strength*, not a finding: the design doc discloses the modest overage and its cause (FU.5 + FU.6 subsystems) rather than silently exceeding or rounding down.
4. The four open questions (Q1–Q4) all carry `PROPOSED-DEFAULT` labels and are explicitly not treated as ratified — correctly honors P-020.
5. The 31-item UX heuristic evaluation is honestly reconciled: 22 folded + 9 rebutted = 31 (verified by direct count against `revision-notes.md`'s per-finding disposition list); rebuttals cite the anti-bloat doctrine with a specific alternative (e.g., `grep 'Disposition: OPEN'` in place of a dashboard) rather than simply declining without justification.

**Strengthening opportunities identified (presentation/evidence, not substance) — see [Weakness Classification](#weakness-classification) below.**

---

## Weakness Classification

| Weakness | Type | Magnitude | Strongest interpretation of author's intent |
|----------|------|-----------|----------------------------------------------|
| `FEEDBACK-LOG.template.md` worked example is numbered `FU.0`; `examples-appendix.md`'s presentation of the *same* real entry (identical verbatim text, identical disposition/evidence) is numbered `FU.3` | Evidence / Internal Consistency | Major | The author intended two complementary illustrations — a "what a brand-new log's first entry looks like" example in the template, and a "what really happened in this project" example in the appendix — but did not add the one clarifying sentence that reconciles the two numbers, so a reader who cross-references both artifacts (as this Steelman did) sees an apparent contradiction in a claim ("real entries... lightly genericized") that is exactly the FU.8 improvement being showcased. |
| Design doc states "Two fail-open seams" (L1.3) while `hook-design-note.md` — the very file it points to — defines three seams (Seam 3 is the segment-cap reminder), and the design doc's own L1.4 section separately cites "Seam 3" by name | Presentation | Minor | The author scoped "two seams" to L1.3's own topic (capture automation) and treated the segment-cap reminder (introduced in L1.4, a different section) as an add-on rather than a miscount. A forward-reference in L1.3 would remove the momentary "wait, weren't there two?" beat for a reader proceeding section-by-section. |
| The segment-cap line-count claim ("measured ~12–18 lines/entry") and the truncation claim ("PM-001") are asserted without a locatable citation, unlike the doc's other quantitative claims (which cite file paths, e.g. `orchestration/adr-convention-20260702-001/.../s-014-quality-score.md`) | Evidence | Minor | The author had real measurements in hand (the numbers are plausible against the actual bootstrap entries) but the doc's own stated method ("Quotes carry paths; inference is labelled `[INFERENCE]`") was not applied to this one figure and to the bare "PM-001" identifier. A one-clause citation would bring this row up to the evidentiary standard the rest of the document already meets. |

No substantive (idea-level) weaknesses were found under charitable reading — see [Best Case Scenario](#best-case-scenario).

---

## Steelman Reconstruction (Targeted)

Per the blind protocol, the deliverable files are **not edited** by this review — only the owner edits. The excerpts below are strengthening suggestions for the owner to apply, shown as before/after text, each tagged `[SM-NNN]`.

### [SM-001] `FEEDBACK-LOG.template.md` — reconcile the worked-example canonical id

**Original** (`FEEDBACK-LOG.template.md:36`):
```markdown
## FU.0 commit-push-cadence (alias: FU.0)

> Worked example (genericized from a real standing directive). Note the `(alias: FU.0)` suffix — you typed `FU.0`, and here it happens to match the canonical id; on a later turn your `FU.0` would map to canonical `FU.1`, `FU.2`, and so on. Delete this block when real entries land.
```

**Strengthened (either option closes the gap):**
```markdown
## FU.0 commit-push-cadence (alias: FU.0)

> Worked example (genericized from a real standing directive — this project's actual log records it as FU.3, since FU.0–FU.2 already existed when it was captured; this template shows the FU.0 case because a brand-new log's first entry is exactly this scenario). Note the `(alias: FU.0)` suffix — you typed `FU.0`, and here it happens to match the canonical id; on a later turn your `FU.0` would map to canonical `FU.1`, `FU.2`, and so on. Delete this block when real entries land.
```
*(Alternative: renumber the template example to `FU.3` to match `examples-appendix.md` verbatim, if a "fresh log" framing is not needed.)*

### [SM-002] Design doc L1.3 — forward-reference Seam 3

**Original** (`feedback-decision-log-convention-design.md:150`):
```markdown
Principle: harness-executed capture is the durable path. Two fail-open seams, both reusing existing precedent (`hooks_prompt_submit_handler.py` already reads `transcript_path` and returns `additionalContext`):
```

**Strengthened:**
```markdown
Principle: harness-executed capture is the durable path. Two fail-open seams for capture (a third, optional segment-cap reminder is covered in [L1.4](#l14-segment-rotation-fu5)), both reusing existing precedent (`hooks_prompt_submit_handler.py` already reads `transcript_path` and returns `additionalContext`):
```

### [SM-003] Design doc L1.4 — cite the measurement source

**Original** (`feedback-decision-log-convention-design.md:159,165`):
```markdown
**Problem (FU.5, confirmed).** Append-only logs eventually exceed the LLM's read limit. Evidence: the default Read tool window is ~2,000 lines; ~25k-token file truncation was observed **in this very project** (PM-001). ...
...50 entries is the human-eyeballable trip-wire; measured ~12–18 lines/entry lands the two thresholds together. Wide margin is deliberate.
```

**Strengthened:**
```markdown
**Problem (FU.5, confirmed).** Append-only logs eventually exceed the LLM's read limit. Evidence: the default Read tool window is ~2,000 lines; ~25k-token file truncation was observed **in this very project** (PM-001 — {add worktracker path or session/transcript pointer}). ...
...50 entries is the human-eyeballable trip-wire; measured ~12–18 lines/entry (against `FEEDBACK-LOG.md` FU.0–FU.9) lands the two thresholds together. Wide margin is deliberate.
```

---

## Best Case Scenario

**Ideal conditions:** The design is strongest when read as what it explicitly claims to be — a MEDIUM-tier, deliberately minimal convention shipped under a hard 25/25 rule-ceiling constraint, for an operator population (the project's own author/user) whose actual usage pattern (turn-by-turn restart-at-FU.0 labeling, real 25k-token truncation already observed) is the evidence base, not a hypothetical persona.

**Supporting assumptions that must hold:** (1) the HARD ceiling truly has zero headroom (confirmed: `quality-enforcement.md` "Current count: 25 HARD rules... Zero headroom"); (2) the hook-deferral risk (manual metadata until Seam 1/2 ship) is acceptable because the MEDIUM rule still governs manual capture in the interim (explicitly stated in both the design doc and `hook-design-note.md`); (3) the operator will read the templates in the same session as the rule file/appendix rather than only one in isolation (this is where SM-001's cross-file id mismatch would otherwise surface as confusion).

**Strongest evidence chain:** internal-kb critique (drift, non-codification, no turn model) → Jerry mechanism inventory (what hooks can/cannot stamp) → design (sidecar-stamped provenance + capped-collection rotation + logger-assigned ids) → real user re-review (FU.5/6/8) → UX heuristic evaluation (31 findings, systematically triaged) → this revision. Each step is evidenced with file citations; the chain is unusually well-documented for a MEDIUM-tier convention.

**Confidence:** HIGH that the core design (two ledgers, capped rotation, logger-assigned ids, MEDIUM-tier enforcement, graduation boundary to worktracker DECISION) is sound and ready for critique strategies to attack on substance. The three findings above are refinements to the *fidelity* of the supporting illustrations and citations, not to the mechanism itself.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260705T-iter1 | Worked example for "commit-push-cadence" carries canonical id `FU.0` in the template but `FU.3` in the appendix for the same real entry | Major | `FEEDBACK-LOG.template.md:36` `## FU.0 commit-push-cadence (alias: FU.0)` | Reconciling note or matching id (see [SM-001](#sm-001-feedback-logtemplatemd--reconcile-the-worked-example-canonical-id)) | Internal Consistency |
| SM-002-20260705T-iter1 | Design doc says "Two fail-open seams" while its own referenced file defines three (Seam 3 in L1.4) | Minor | `feedback-decision-log-convention-design.md:150` | Forward-reference to L1.4 (see [SM-002](#sm-002-design-doc-l13--forward-reference-seam-3)) | Internal Consistency |
| SM-003-20260705T-iter1 | Segment-cap line-count measurement and "PM-001" truncation citation lack a locatable pointer, unlike the doc's other quantitative claims | Minor | `feedback-decision-log-convention-design.md:159,165` | Add path/pointer (see [SM-003](#sm-003-design-doc-l14--cite-the-measurement-source)) | Evidence Quality |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where `execution_id` = `20260705T-iter1` (this S-003 execution, iteration 1).

---

## Improvement Details

### SM-001 (Major)

- **Affected Dimension:** Internal Consistency
- **Original Content:** `FEEDBACK-LOG.template.md:36-38` labels the worked "commit-push-cadence" example as canonical `FU.0`; `examples-appendix.md:43-59` labels the *same verbatim text and disposition* as canonical `FU.3`.
- **Strengthened Content:** See [Steelman Reconstruction SM-001](#sm-001-feedback-logtemplatemd--reconcile-the-worked-example-canonical-id) — either a one-clause note explaining the template shows the "fresh log" case (id 0) while the appendix shows this project's real history (id 3), or renumber one to match the other.
- **Rationale:** FU.8 (worked examples) exists specifically so the id/alias scheme is "rationalizable" (design doc L0, Improvement Ledger row 10). An unexplained id mismatch between the two documents that both claim to show "a real entry... lightly genericized" works against exactly that goal for a reader who reads both. This is narrow (one example, one heading label) and does not touch the id/alias *mechanism*, which is explained correctly and consistently everywhere else (design doc L1.1, rule file LOG-M-005, both templates' "Ids & aliases" prose, and the live `FEEDBACK-LOG.md` bootstrap entries FU.5–FU.9, which apply the scheme correctly).
- **Best Case Conditions:** Fully closes if the owner adds the one-sentence reconciling note (no new machinery, no schema change).

### SM-002 (Minor)

- **Affected Dimension:** Internal Consistency
- **Original Content:** `feedback-decision-log-convention-design.md:150` — "Two fail-open seams..."; `hook-design-note.md:11-15` (nav table) and `:47-49` define a third, "Seam 3 (optional): segment-cap reminder," which the design doc itself names explicitly at `:172` in a later section (L1.4).
- **Strengthened Content:** See [Steelman Reconstruction SM-002](#sm-002-design-doc-l13--forward-reference-seam-3).
- **Rationale:** Not a contradiction on close reading (L1.3 scopes "two" to capture automation; Seam 3 is optional and belongs to segment rotation, introduced in L1.4) — but the un-forward-referenced "two" creates a momentary count mismatch for a reader proceeding top-to-bottom, exactly the kind of presentation friction Steelman exists to remove before critique strategies test the substance.

### SM-003 (Minor)

- **Affected Dimension:** Evidence Quality
- **Original Content:** `feedback-decision-log-convention-design.md:159` ("PM-001" cited with no path) and `:165` ("measured ~12–18 lines/entry" with no source cited).
- **Strengthened Content:** See [Steelman Reconstruction SM-003](#sm-003-design-doc-l14--cite-the-measurement-source).
- **Rationale:** The design doc's own stated method (front-matter: "Quotes carry paths; inference is labelled `[INFERENCE]`") is met almost everywhere else in the document (e.g., specific `orchestration/.../s-014-quality-score.md` citations). This one figure and one bare identifier are the exception; a short pointer would bring the whole document to a uniform evidentiary standard.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Package already covers schema, ids, rotation, automation, boundaries, governance, and open questions; no missing section identified under charitable reading. |
| Internal Consistency | 0.20 | Positive | SM-001 and SM-002 close cross-file id/count mismatches that a downstream critique strategy (e.g., S-011 Chain-of-Verification) would otherwise need to spend a full pass discovering. |
| Methodological Rigor | 0.20 | Neutral | Charitable-interpretation and presentation-vs-substance distinction fully maintained; no substantive weakness surfaced. |
| Evidence Quality | 0.15 | Positive | SM-003 brings one under-cited figure up to the document's own already-high citation standard. |
| Actionability | 0.15 | Positive | All three findings are directly incorporable as single-sentence or single-word edits; no new machinery, lint, or hook required (honors the package's own anti-bloat doctrine). |
| Traceability | 0.10 | Positive | SM-001/SM-002 specifically restore traceability between companion artifacts (template ↔ appendix; L1.3 ↔ L1.4) that a reader relies on to build the mental model FU.6/FU.8 exist to teach. |

---

## Readiness for Downstream Critique

Self-review applied (H-15). All three findings carry specific file+line evidence and before/after text; none require re-scoping the design or adding enforcement machinery, consistent with the MEDIUM-tier/anti-bloat posture explicitly declared by the deliverable itself. Reconstruction preserves the original thesis in full. Ready for S-002 (Devil's Advocate), S-004 (Pre-Mortem), S-007 (Constitutional AI), S-012 (FMEA), and S-013 (Inversion) per H-16 — those strategies should target the substance (e.g., the Q1–Q4 proposed defaults, the graduation boundary to worktracker DECISION, the hook-deferral risk) rather than the three presentation items closed here.

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` | Constitutional: P-003 no subagents, P-020 draft-only (no framework paths touched by this report), P-022 evidence cited with file+line, inference unlabelled claims treated as author intent under charitable reading.*
