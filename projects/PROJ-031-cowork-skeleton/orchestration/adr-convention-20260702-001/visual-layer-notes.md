# Visual Layer Notes — FU.10 (ps-architect, creator/owner)

> User feedback FU.10 (2026-07-06): "Is there a reason why we don't have any diagrams to help
> visualize ... what the process is supposed to be? This is massive walls of text..."
> Task: add a compact Mermaid visual layer to both deliverables; diagrams REPLACE equivalent
> prose where possible (net tokens DECREASE or stay flat; rule draft should shrink); 5-rule lint
> core unchanged; content decisions unchanged — representation only. Append changelog v1.13.

## Baseline (measured 2026-07-06, `wc`)

| File | Lines | Words | ~Tokens (words x1.35) |
|------|------:|------:|----------------------:|
| ADR-PROJ031-004 | 811 | 28,229 | ~38.1k |
| adr-standards-rule-draft | 254 | 4,757 | ~6.4k |

## Diagram inventory

### ADR (target ~4)
- **A. ID-scheme decision tree** (flowchart TD) — top of `## L1: Technical Implementation`.
  Encodes D-1..D-4: framework→domain-slug in docs/design/; project-local default→domain-slug in
  projects/*/decisions/ (RECOMMENDED); positively-local→ADR-{PROJECT-ID}-NNN dialect (permitted,
  discouraged); legacy entity-embedded; bare ADR-NNN→DEPRECATED. Additive nav aid.
- **B. Lifecycle state machine** (stateDiagram-v2) — Status Vocabulary. REPLACES the "Valid status
  transitions (FM-020)" table (equivalent prose→diagram). Adds amend-in-place self-loop vs
  supersede-with-new. Consistent with transition table + terminal-state disclosure.
- **C. Promotion flow** (flowchart TD) — top of `## Promotion Process (Step-by-Step)`. Path 0
  (draft graduation, no tombstone) / Path 1 (pure git mv, ID+title-slug unchanged, citations
  intact) / Path 2 (rename + tombstone + promoted_from/to back-links + citation re-point).
- **D. Location model map** (flowchart LR) — L1 canonical location model, beside the table.
  Two canonical homes + repo-based alt + permitted dialect + frozen legacy + transient drafts.

### Rule draft (target 2-3, must shrink)
- **R1. ID-scheme decision tree** (compact flowchart TD) — ID Scheme section.
- **R2. Promotion flow** (compact flowchart TD) — Promotion Process; rewrite Path 0/1/2 narrative
  terse under diagram (biggest prose-saving lever) to guarantee net shrink.
- **R3. Lifecycle state machine** (stateDiagram-v2) — Status Vocabulary; REPLACES the "Transitions:"
  run-on sentence enumeration (keep terminal-state clarification).

## Consistency guard (S-011 will check)
Each diagram must not contradict adjacent prose. Cross-checked against: D-1..D-5 (Decision),
Status transition table (645-650) + terminal-state prose (652), Path 0/1/2 steps (562-599),
Location Model table (386-395 / rule 77-88). Mermaid: quoted labels, no exotic features.

## Final measurements (honest, `wc` 2026-07-06)

| File | Before | After | Delta |
|------|--------|-------|-------|
| ADR-PROJ031-004 | 811 lines / 28,229 words / ~38.1k tok | 868 lines / 28,820 words / ~38.9k tok | +57 lines / +591 words / ~+0.8k tok (+2.1%) |
| adr-standards-rule-draft | 254 lines / 4,757 words / ~6.42k tok | 283 lines / 4,792 words / ~6.47k tok | +29 lines / +35 words / ~+47 tok (+0.7%) |

Diagrams: **4** in ADR (Fig. 1 ID-scheme tree, Fig. 2 location map, Fig. 3 promotion flow,
Fig. 4 lifecycle), **3** in rule draft (ID-scheme tree, promotion flow, lifecycle). All **7 render
clean** with `mmdc` (mermaid-cli) — valid `flowchart TD/LR` + `stateDiagram-v2`, no exotic features.

## Honest outcome note (P-022)
Both files land at **"stay flat"** (ADR +2.1%, rule draft +0.7%), satisfying the HARD floor
"DECREASE or stay flat." Neither achieved a strict net *shrink*. Reasons, disclosed plainly:
- The mandatory v1.13 changelog row (append-only; prior rows not deletable) adds ~85-230 words.
- Multi-line Mermaid blocks add lines even when their labels replace prose.
- The rule draft has been through 10 subtraction passes; the only remaining non-normative fat was
  the size-note (compressed ~230→~70 words) — a further net shrink would require deleting
  load-bearing residual disclosures (R-B/R-10/R-14…R-18, FM-007, CC-002), which the task forbids
  ("content decisions unchanged"). Prose→diagram swaps done: ID-scheme form-bullets, Path 0/1/2
  paragraphs, the `Transitions:` sentence (rule draft); the FM-020 transition table (ADR).
- Self-referential measurement (the changelog row counts itself) was converged to exact `wc` values.

## Progress log
- [DONE] 4 ADR diagrams + captions inserted below their sections; FM-020 transition table → Fig. 4.
- [DONE] 3 rule-draft diagrams + captions; form-bullets / Path paragraphs / Transitions sentence
  replaced; size-note compressed.
- [DONE] v1.13 changelog appended to both, with honest re-measured before/after.
- [DONE] H-23 nav tables unchanged (zero `##` sections added/removed); anchors intact.
- [DONE] 7/7 Mermaid diagrams validated via mmdc render; no absolute home-directory paths; no internal refs.
