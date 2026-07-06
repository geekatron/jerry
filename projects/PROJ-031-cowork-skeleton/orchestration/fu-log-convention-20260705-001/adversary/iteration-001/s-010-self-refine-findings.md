# S-010 Self-Refine — Findings (iteration 1)

> **Strategy:** S-010 Self-Refine (Group A, first in the adversary order)
> **Reviewer/Owner:** ps-architect (creator self-review, H-15)
> **Deliverable package:** `feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/` (rule file, 2 templates, examples-appendix, hook-design-note)
> **Criticality:** C3 (AE-002 rules/ + AE-003 ADR install; convention ships MEDIUM-tier)
> **Date:** 2026-07-05 · **Iteration:** 1

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Metadata |
| [Summary](#summary) | Overall assessment |
| [Verification Log](#verification-log) | The 7 targeted checks + results |
| [Findings Table](#findings-table) | All findings, severity-sorted |
| [Finding Details](#finding-details) | Expanded Major/Minor detail + fixes |
| [Scoring Impact](#scoring-impact) | Dimension mapping |
| [Decision](#decision) | Verdict + next action |

---

## Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | FEEDBACK-LOG + LLM-DECISION-LOG Jerry convention (FU.2 design + staged artifacts) |
| Criticality | C3 |
| Reviewer | ps-architect (creator) |
| Iteration | 1 of N |

## Summary

The package is coherent, well-evidenced, and largely internally consistent; the FU.5 rotation math, the FU.6 operator-burden model, and the anti-bloat doctrine hold up under self-critique. One **Major** consistency defect undercuts the FU.8 goal directly: the **`Source` field** is represented three different ways across the schema, the rule file, the templates, and the appendix — a logger following the schema and a logger copying the examples would produce different-shaped entries. Five **Minor** findings are small textual/precision fixes (a stale sealed-segment index, one overclaim to qualify, a missing alias suffix in the DEC example, a missing `Reflected in` component in the L1.2 schema row, and a design-doc tier-vocabulary note). The rule file measures **1584 cl100k tokens** — exactly the figure the design self-reports — an accurate, honestly-disclosed **+5.6% over the "≤ ~1,500" target**. No fundamental flaws. Verdict: **REVISE** (targeted fixes, no re-architecture).

## Verification Log

The seven checks the owner was asked to verify specifically:

| # | Check | Result | Note |
|---|-------|--------|------|
| V1 | FU.5 rotation internally consistent (cap, links, index, cross-log nav) | **PASS with 1 minor** | Cap/naming/prev-next/forward-nav/id-join-key all consistent and the headroom math checks (800 = 40% of 2000-line window = 2.5×; 8–12k tok = 2–3× under 25k). Exception: sealed-segment stale index (SR-002). |
| V2 | FU.6 id scheme burden-free (operator) + collision-free (logger) | **PASS with 1 minor** | Operator side is genuinely burden-free (aliases restart freely; canonical id logger-minted, monotonic-across-segments, never reset) and eliminates the DJ-025 operator-collision class. "cannot collide" for concurrent loggers is an overclaim (SR-003). |
| V3 | FU.8 examples present, correct, consistent with schema | **FAIL (Major) + 1 minor** | Examples are present and mostly correct, but the `Source` field is schema-inconsistent (SR-001, Major) and the DEC example heading drops the `(alias: …)` suffix (SR-004). |
| V4 | Rule file ≤ ~1,500 tokens (measure, state) | **MEASURED: 1584 (cl100k) / 1571 (o200k)** | Matches the design's self-reported "~1,584 cl100k" exactly (P-001/P-022 accurate). +84 tok / +5.6% over target; self-disclosed and justified (SR-007). |
| V5 | PROPOSED-DEFAULT markers intact on the 4 open questions | **PASS** | Q1–Q4 all present in the Proposed Defaults table under the "PROPOSED-DEFAULT (pending ratification)" column; Q1 (rule/LLM-template/appendix), Q2 (rule scoping), Q3 (hook-note) also carry inline markers. Q4 relies on the table cell only — acceptable; optional inline token would tighten it. |
| V6 | Tier vocabulary clean | **PASS (shipped artifacts) / 1 minor (design doc)** | Rule file + both templates + appendix contain zero HARD keywords (MUST/SHALL/NEVER/REQUIRED/FORBIDDEN). Design doc uses MUST for entry-content fidelity inside a MEDIUM convention without stating the conditional-MUST framing (SR-006). |
| V7 | No internal-refs / absolute-path hygiene violations | **PASS (clean)** | Zero `[home]/` paths and zero employer-internal literals across the design doc and all staged artifacts. `[internal-kb]` placeholder used correctly throughout. |

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-20260705 | `Source` field represented 3 inconsistent ways (standalone schema field vs. folded into Context line vs. relabeled "Source detail" in template; omitted as a field in appendix) | **Major** | design `L1.1` rows 59–60 (Source field + "· source" in Context format); rule file lines 32/35; FEEDBACK template lines 18/22/47/49; appendix lines 56/78 (no standalone field) | Internal Consistency |
| SR-002-20260705 | Sealed-segment stale Segment Index contradicts "index lives **only** in ACTIVE / sealed segments **just** carry prev-next" | Minor | design `L1.4` rows 169 + 172 (rotation "copies the filled ACTIVE content" which includes the index section) | Internal Consistency |
| SR-003-20260705 | Overclaim: "canonical ids are logger-owned, so parallel/background agents **cannot collide**" — true for the operator, not for concurrent loggers absent serialization | Minor | design `L1.1` line 70 | Evidence Quality / Internal Consistency (P-022) |
| SR-004-20260705 | LLM-DECISION-LOG template worked-example heading omits the `(alias: …)` suffix its own schema + the appendix require | Minor | template line 39 `## DEC-LLM-001 example-entry` vs schema line 19 + appendix line 88 `(alias: —)` | Internal Consistency / Example correctness |
| SR-005-20260705 | Design doc `L1.2` Context schema row omits the `Reflected in` cross-link component present in rule/template/appendix | Minor | design line 101 vs rule line 42, template line 55, appendix line 108 | Completeness / Traceability |
| SR-006-20260705 | Tier-vocabulary: design doc uses MUST for entry-content rules inside a MEDIUM (SHOULD) convention without stating the conditional-MUST framing | Minor | design lines 56, 58, 79 ("MUST be word-for-word", terminal "MUST carry", "MUST harvest") | Internal Consistency |
| SR-007-20260705 | Rule file 1584 cl100k tokens vs "≤ ~1,500" target (+5.6%); accurate + disclosed but nominally over | Minor | measured cl100k 1584 / o200k 1571; design lines 40/180/271 | Actionability |

## Finding Details

### SR-001-20260705 — `Source` field is not schema-consistent (Major) — FU.8 core

- **Severity:** Major
- **Affected Dimension:** Internal Consistency (0.20)
- **Evidence:**
  - Design `L1.1`: `Source` is declared a standalone 5th field (row 60) **and** "· source" is the last component of the Context format string (row 59) — doubly represented.
  - Rule file: lists `**Source**` as the 5th field (line 32) with an enum (line 35); its Context is an opaque "provenance line" that does **not** show source.
  - FEEDBACK template: declares `**Source**` as the 5th field (line 18), **also** puts "source" in the Context format (line 22), and in the worked example renders the standalone field as **"Source detail (inline-doc only): `{path}:{line-or-anchor}`"** (line 49) while the channel value lives in the Context line ("· source `chat`", line 47).
  - Appendix: worked entries have **no** standalone Source field at all — only "· source `chat`" inside Context (lines 56, 78).
- **Impact:** This is precisely the FU.8 promise ("examples consistent with the schema"). A logger following the schema writes a distinct `Source:` field; a logger copying the examples folds the channel into Context and uses "Source detail" only for an inline-doc path. Lint/readers cannot rely on a stable shape. It is the single load-bearing consistency fix in the package.
- **Recommendation (pick ONE representation, then align all four artifacts + the FEEDBACK-LOG schema/lint):**
  - **Option A (recommended — matches every worked example):** the channel lives **in the Context line** (`… · source chat`). Drop `Source` as a standalone field from the design `L1.1` table and the rule file; rename the template's standalone line to **"Inline-doc anchor (inline-doc source only): `{path}:{anchor}`"** so it clearly carries only the path, not the channel. Net: fewer fields, examples already conform.
  - **Option B:** keep `Source` a standalone field; then **remove "source" from every Context format string** and render the examples as a real `**Source:** chat` field. More edits; contradicts the current examples.
  - Either way, state the decision once and make the design table, rule file, both templates, and the appendix agree.

### SR-002-20260705 — Sealed-segment stale index (Minor) — FU.5

- **Severity:** Minor
- **Affected Dimension:** Internal Consistency (0.20)
- **Evidence:** Design `L1.4` asserts the Segment Index "lives **only** in the ACTIVE file" (row 169) and "sealed segments stay immutable and **just** carry prev/next" — but the rotation procedure (row 172) "copy the filled ACTIVE content to the next `.{NNN}.md`" carries the whole ACTIVE body, **including its Segment Index section**, into the immutable sealed file. Post-rotation, `FEEDBACK-LOG.001.md` therefore contains a frozen index that still lists itself as "(ACTIVE)".
- **Impact:** A reader who opens a sealed segment sees a stale index labeling that sealed file ACTIVE. Navigation still works via the ACTIVE index + `ls`-rebuild + id join key, so it is non-functional-breaking — but it contradicts the stated invariant.
- **Recommendation:** Either (a) add a one-line rotation step "on seal, strip/neutralize the Segment Index section (or mark it FROZEN — see ACTIVE file for the authoritative index)", or (b) soften the claim to "the **authoritative** index lives in the ACTIVE file; sealed copies are frozen snapshots, not to be trusted for navigation." (a) is cleaner; (b) is zero-mechanism.

### SR-003-20260705 — "cannot collide" overclaim (Minor, P-022) — FU.6

- **Severity:** Minor
- **Affected Dimension:** Evidence Quality (0.15) / Internal Consistency
- **Evidence:** Design `L1.1` line 70: "canonical ids are logger-owned, so parallel/background agents **cannot collide**." The reasoning is a non-sequitur for concurrent writers: logger-ownership removes the **operator**-side counter (the real DJ-025 fix), but two concurrent loggers that each "read max-id then append" can still mint the same `FU.N` without serialization. Jerry does run blind background agents (the adversary pipeline itself), so concurrency is a real regime, not hypothetical.
- **Impact:** Honesty/accuracy of a headline FU.6 claim. The mechanism is sound in the serialized-append reality and lint check 2 (uniqueness+monotonicity) is a post-hoc backstop — but the absolute "cannot collide" overstates the guarantee.
- **Recommendation:** Qualify: "eliminates the **operator-side** collision class (DJ-025); concurrent appends are serialized by the harness and lint check 2 backstops any residual race." Keep the (true) operator-burden claim as-is.

### SR-004-20260705 — DEC example heading missing alias suffix (Minor) — FU.8

- **Severity:** Minor
- **Affected Dimension:** Internal Consistency / Example correctness
- **Evidence:** `LLM-DECISION-LOG.template.md` line 39 heading `## DEC-LLM-001 example-entry` lacks the `(alias: …)` suffix mandated by its own schema (line 19: `## DEC-LLM-NNN <slug> (alias: <label or —>)`) and shown correctly in the appendix (line 88: `## DEC-LLM-001 ratify-approach-b (alias: —)`).
- **Impact:** The one DEC worked example does not model the required heading shape — teaches the wrong pattern.
- **Recommendation:** Change to `## DEC-LLM-001 example-entry (alias: —)` **and** update the nav-table anchor (H-24) to the regenerated slug; verify the anchor after editing (the `(alias: —)` suffix changes the GitHub slug — do not hand-guess it).

### SR-005-20260705 — L1.2 Context schema omits `Reflected in` (Minor)

- **Severity:** Minor
- **Affected Dimension:** Completeness (0.20) / Traceability (0.10)
- **Evidence:** Design `L1.2` Context row (line 101) = `datetime · session · model · agents/workflow · artifacts` — no `Reflected in`. The rule file (line 42), template (line 55), and appendix (line 108) all include `· Reflected in`.
- **Impact:** `Reflected in` is the cross-link that makes LOG-M-004 graduation traceable; its absence from the primary schema table is a real gap (downstream artifacts are correct and agree among themselves).
- **Recommendation:** Add `· Reflected in` to the design `L1.2` Context format string.

### SR-006-20260705 — Design-doc MUST inside a MEDIUM convention (Minor)

- **Severity:** Minor
- **Affected Dimension:** Internal Consistency (0.20)
- **Evidence:** Design `L1.1` uses HARD verbs — "MUST be word-for-word" (line 56), terminal states "MUST carry an evidence link" (line 58), "MUST harvest" (line 79) — while the shipped convention is uniformly MEDIUM/SHOULD (rule file, verified clean). Defensible as a two-level model (SHOULD *whether* you log; MUST *how* an entry is shaped once logged) but that framing is never stated.
- **Impact:** A reader may perceive a HARD/MEDIUM tension. The shipped artifacts are clean, so impact is confined to the design doc's own readability.
- **Recommendation:** Either add one sentence ("these MUSTs are conditional entry-content rules that apply *once* an entry is written; whether to write one is the MEDIUM LOG-M-001 SHOULD"), or downgrade the design-doc verbs to SHOULD for uniformity.

### SR-007-20260705 — Token target nominally exceeded (Minor)

- **Severity:** Minor
- **Affected Dimension:** Actionability (0.15)
- **Evidence:** Measured cl100k 1584 / o200k 1571 tokens; design self-reports "~1,584 tokens by tiktoken cl100k" (line 180) against a "≤ ~1,500" target (lines 40, 271). Measurement is exact and honestly disclosed (P-001/P-022 pass).
- **Impact:** Trivial; the "~" tilde and explicit justification ("the modest overage buys the FU.5 rotation subsystem + FU.6 alias scheme") make it acceptable.
- **Recommendation:** Either (a) explicitly ratify 1584 as the budget and restate the target as "≤ ~1,600", or (b) trim ~84 tokens (fold two of the 7 nav rows; tighten the Segment-rotation prose which duplicates the appendix). Low priority.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral→Negative | SR-005 (missing `Reflected in` in L1.2 schema); otherwise thorough (all sections, worked examples, FU.5/6/8 all addressed). |
| Internal Consistency | 0.20 | Negative | SR-001 (Major, Source field); SR-002, SR-004, SR-006 minors. Primary weakness. |
| Methodological Rigor | 0.20 | Positive | Anti-bloat doctrine applied consistently; UX triage disciplined; rotation math derived, not asserted. |
| Evidence Quality | 0.15 | Negative | SR-003 overclaim; otherwise claims are cited (research §, DJ-025, PM-001 truncation) and the token figure is exact. |
| Actionability | 0.15 | Positive | Staged artifacts installable; adoption plan is step-wise; SR-007 minor. |
| Traceability | 0.10 | Positive | References section + Improvement Ledger + PROPOSED-DEFAULT table give strong provenance; SR-005 is the one gap. |

**Estimated composite:** ~0.88–0.90 (REVISE band). Driver: Internal Consistency (SR-001).

## Decision

**Outcome:** REVISE. One Major consistency fix (SR-001 Source field) plus five Minor alignments; no fundamental flaws, no re-architecture. The design's core theses (survive-compaction ledgers, logger-assigned ids, capped-collection rotation, cross-link-not-duplicate boundary) are sound.

**Revision handling (Step 5 — deferred, with rationale):** As Group A (first) in a six-strategy blind adversary order, I am **not** mutating the shared deliverables in this iteration. Rationale: (1) SR-001 requires an owner **design choice** (Option A vs B) that is P-020 user-ratifiable, not a mechanical fix; (2) SR-004's fix changes a nav anchor (H-24) that must be regenerated, not hand-guessed under time pressure; (3) keeping the baseline stable lets the downstream strategies (steelman, challenge, verify, decompose, score) review one artifact. All fixes are specified precisely above for the consolidated revision phase.

**Next Action:** Proceed to S-003 Steelman (Group B) on this baseline; apply SR-001–SR-007 in the consolidated revision after the full strategy set reports. Re-run token measurement after any rule-file edit.
