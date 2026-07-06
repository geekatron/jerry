# Remediation Notes — Iteration 1 → 2 (FU-Log / DEC-LLM Convention)

> ps-architect · owner-first remediation after S-014 score 0.64 (gate 0.95).
> Doctrine: **anti-bloat** — close findings by simplifying/clarifying/deleting, never by adding machinery. Any addition must delete something bigger (state the trade). Rebut invalid findings with evidence.
> Constitutional: P-003 (no subagents), P-020 (draft-only; nothing under `.context/`, `docs/`, `hooks/`), P-022 (cite evidence, label inference).
> Public-repo hygiene: repo-relative paths + placeholders only.

## Root-cause of the 0.64

The score is driven by **Internal Consistency (0.46)**: the package ships several
**overclaims** ("cannot collide", "guarantee … survive compaction", "immutable once
sealed", "full fidelity is preserved") that the document's own later disclosures
contradict. Every adversary strategy judged these **fixable by wording** — no new
machinery required. That is exactly the anti-bloat sweet spot: the fix is to *soften/qualify
claims to match the mechanism actually shipped*, and in several cases to **delete** the
overclaiming adjective outright.

The dominant remediation verb is therefore **delete/soften**, not **add**. Where a finding
asks for machinery, it is rebutted (already covered, or violates anti-bloat) with evidence.

## Change ledger (this iteration)

Legend: **D** = deletion/softening/simplification (anti-bloat win); **A** = addition (disclosure/protocol — offset per doctrine); **REBUT** = declined with evidence.

| # | Finding(s) | Type | Deliverable(s) touched | Change |
|---|-----------|------|------------------------|--------|
| 1 | RT-001/DA-001/PM-001/FM-006 (Critical ×4) — "cannot collide" | D | design L1.1; rule LOG-M-005 | Softened to **collision-resistant under single-writer-per-log append discipline**; concurrent-writer race disclosed as residual, backstopped by the id-integrity lint (detect, not prevent). |
| 2 | RT-003/CC-001/IN-001 (Critical ×3) — L0 "guarantee … survive compaction" | D | design L0 | Scoped the guarantee to **persistence of *captured* entries**; capture stays MEDIUM/SHOULD until the Q3 hook ships. |
| 3 | RT-002/PM-002/FM-008 (Critical ×3) — "immutable once sealed" + no cap detection | D | design L1.4; rule Segment rotation + L5 | "immutable" → **immutable-by-convention (git-backstopped)**; cap-crossing detection **folded into lint check 1** (no 4th check). |
| 4 | CC-002 (Major) — present-tense hook outliers | D | design L1.1 line 81, Improvement Ledger rows 3–4 | Applied the **Q3-deferred hedge** uniformly ("designed, not yet shipped"). |
| 5 | CC-003 (Major) — HARD "never" in MEDIUM rows | D | design + rule LOG-M-004/005 | "never" → "SHOULD NOT" / "does not". |
| 6 | SR-001 (Major, self-ID) — `Source` represented 3 ways | D | design schema, rule, both templates | **Folded `source` into the Context line** (deleted the separate field) — one representation across all four artifacts. |
| 7 | SM-001 (Major, Steelman) — FU.0 vs FU.3 same entry | A | examples-appendix | One clarifying note: same directive, different log position; alias stable, canonical id advances. |
| 8 | SR-004 (Minor) — DEC example missing alias suffix | A | DEC template (+ nav anchor, H-24 verified) | Added `(alias: —)` to the worked example heading. |
| 9 | SR-005 (Minor) — `Reflected in` missing from L1.2 schema | A | design L1.2 | Added the `Reflected in` graduation cross-link component. |
| 10 | SR-006 (Minor) — HARD "MUST" in MEDIUM convention | D | design schema rows + capture-trigger heading + harvest | MUST → SHOULD / definitional phrasing (kept legitimate P-020 and H-23-citing MUSTs). |
| 11 | PM-003/FM-017 (Critical) — "full fidelity is preserved / byte-exact" | D | design Q1 table + PROPOSED-DEFAULT | Reworded to **disclose the transcript-retention/cross-machine-portability dependency** (`[INFERENCE]`); foregrounded the C3+ full-paste escape hatch as the mitigation. |
| 12 | CC-004 (Major) — residual internal ids vs "zero internal tokens" | D | design + hook note | Genericized `DJ-025`→`[legacy-fu-id]`, `OI-019`→`[legacy-oi-id]`, "eng-arch reconciliation"→"architecture reconciliation" (**public-repo hygiene**). |
| 13 | CV-001/003/004 (Minor, CoVe) — citation precision | A | design | Disclosed PM-001 is from the sibling adr-convention orchestration; fixed the DECISION.md quote attribution; disambiguated "~19k" → "~19 KB on disk (file size)". |
| 14 | DA-002 (Critical) — bare-alias back-reference ambiguity | A | design id-scheme + appendix Common cases | Added the **H-31 disambiguation protocol** (enumerate candidates + ask; don't infer from recency). |
| 15 | DA-004 (Major) — no `alias: —` fallback for FEEDBACK-LOG | A | design schema + rule + template | Added the `—` fallback, symmetric with LLM-DECISION-LOG. |
| 16 | PM-006 (Major, live-evidenced) — no staleness mechanism | A | design Disposition row + rule | **Staleness-review nudge at the existing commit-cadence checkpoint** — reuses an existing event, no new machinery. |
| 17 | FM-003 (Critical) + IN-002/PM-008 — opportunistic inline-doc harvest | A | design capture triggers + rule | Disclosed harvest is opportunistic (bounded to docs re-read); optional `grep` sweep backstop. |
| 18 | FM-008 (Critical) — cap-crossing has no detection | D | design + rule L5 | **Folded into lint 1** (line-count pass flags cap-exceeded) — still ≤3 checks. |
| 19 | IN-004 (Major) — lint misses dropped mid-sequence entry | D | design + rule L5 | **Folded contiguity into lint 2** (unique + monotonic + contiguous). |
| 20 | IN-005 (Major) — no post-rotation parity check | A | design rotation procedure + rule | One-line `grep -c` parity step. |
| 21 | DA-003 (Major, partial rebut) — Segment Index unbounded | A | design L1.4 | Disclosed index grows **≈1 row / 50 entries** (10k entries → ~200 rows) — bounded, self-compactable at implausible extreme; the "shard-not-solve" framing overstates. |
| 22 | IN-006 (Major) — no cross-scope discovery signal | A | design Scoping + rule | Multi-scope discovery caveat ("check both project-scoped and repo-root logs"). |
| 23 | FM-024 (Critical) — hook keyword list misses FU.9 interrogative | A | hook-design-note Seam 2 | Added interrogative/challenge cues + **disclosed the heuristic is best-effort; capture does not depend on the hook** (LOG-M-001 governs). |
| 24 | PM-005/FM-023 (Major) — lint checks have no delivery path | A | design adoption plan Step 3 | Added the **lint CI-wiring action item** with owner + acceptance. |
| 25 | PM-004 (Major) — hook deferral open-ended | A | design adoption plan Step 6 + Q3 | Added an **event-based re-assessment trigger** (first rotation or first missed-capture). |
| 26 | FM-019 (Major) — graduation trigger undefined | A | design boundary rule | Added a **concrete low-ceremony graduation trigger** (attached-to-parent AND ratified; user authorizes). |
| 27 | SR-007 (Minor) — token overage | D | design governance + staged-artifacts + changelog | Re-measured rule file (**~1,690 cl100k tokens**) after edits; **ratified as the working budget** with the +106 trade stated. Trimmed elaborations into the appendix to hold it there. |

**Totals:** 27 findings closed by edit — **12 D (delete/soften/simplify) + 15 A (disclosure/protocol)** — plus **1 REBUT**. Every A is a wording/documentation addition, no new subsystem/hook/lint-beyond-a-clause; the only measurable growth is the rule file's ratified +106 tokens (SR-007), justified as buying the consistency fixes that closed the Criticals.

## Rebuttal (declined with evidence)

**DA-005 (Major) — "add an optional author/participant Context field."** Declined.
- **Evidence:** the score's own text notes "the worktracker DECISION entity this log graduates into *requires* `participants[]`." That is precisely the boundary this convention already draws: identity is a **graduation-time, formal-artifact concern**, owned by the AST-validated DECISION entity (H-33), *not* a per-entry field on a low-ceremony ledger.
- **Anti-bloat:** adding an author field to every entry is the schema-creep the doctrine forbids (a field carried by thousands of single-operator entries at zero information gain). The single-operator default is already implicit.
- **Resolution (no new field):** made the boundary explicit in the design's **Graduation trigger** — "Author/participant identity is captured at graduation (the DECISION entity's `participants[]`), not per log entry." This closes the *gap* DA-005 identified (where does identity live?) without adding the field it proposed.

## INHERENT items — affirmed as disclosed, no action (per S-014 tags)

- **IN-007 / RT-008** — transcript-pointer resolvability unenforced: accepted anti-bloat trade (design F-028), already disclosed.
- **DA-007** — manual rotation relies on post-hoc lint, not a real-time validator: accepted MEDIUM-tier trade.
- **PM-007 / PM-009** — Backfill Queue / Q1–Q4 ratification lack a hard deadline: correctly gated to explicit user authorization (P-020), not a defect.

## Verification performed

- Grep sweep: no residual `cannot collide` / `immutable once sealed` / `full fidelity is preserved` as standalone claims (only quoted in the v3 changelog for traceability); no `DJ-025` / `OI-019` / absolute `[home]/` paths in the 6 deliverable files.
- Rule file re-measured with `tiktoken cl100k`: 1,584 → 1,690 tokens (disclosed).
- DEC template nav anchor recomputed against github-slugger algorithm: `#dec-llm-001-example-entry-alias-` matches (H-24).
