# Steelman Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 4)

## Navigation

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Metadata |
| [Summary](#summary) | Assessment overview |
| [Charitable Interpretation](#charitable-interpretation) | Step 1 output: core thesis + strengthening opportunities |
| [Best Case Scenario](#best-case-scenario) | Step 4 output: conditions under which the design is strongest |
| [Steelman Reconstruction (excerpts)](#steelman-reconstruction-excerpts) | Strongest-form restatement of the two load-bearing findings |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings with severity |
| [Improvement Details](#improvement-details) | Expanded Critical/Major findings |
| [Scoring Impact](#scoring-impact) | Dimension impact table |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + all files in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`) — 6 files total.
- **Deliverable Type:** Design + staged convention artifacts (MEDIUM-tier rule + templates)
- **Criticality Level:** C4 (engagement gate 0.95, user-set)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 4, blind protocol — no prior adversary iteration outputs read)
- **Date:** 2026-07-06
- **Original Author:** ps-architect (per design doc header)

---

## Summary

**Steelman Assessment:** The package is a mature, heavily-hedged MEDIUM-tier convention that has already absorbed three rounds of adversarial remediation (v3–v5 in the design doc's own changelog); it correctly adopts a descoped-with-disclosure posture (single-writer discipline, collision-resistant not collision-proof, capture is SHOULD not MUST) and explicitly rejects machinery the anti-bloat doctrine would forbid (F-004/005/010/019/021/022/023/027/028 rebuttals). Applying the strongest charitable reading, most candidate objections are already pre-empted in the text. Two genuine gaps survive charity: (1) a specific, well-evidenced instance of the exact "overclaim recurring in an un-swept location" failure class the design's own changelog says it already fixed package-wide, found in the one artifact most likely to be read standalone post-install; (2) a numeric claim (rule-file token count) used as evidence for a live P-020 ratification decision that is stale relative to text additions the design's own changelog documents having made to that same file in a later iteration.
**Improvement Count:** 1 Critical, 1 Major, 2 Minor
**Original Strength:** High — the design is internally self-aware, cites its own evidence (measured token counts, PM-001 truncation, real bootstrap entries), and has a documented, falsifiable remediation trail. The remaining gaps are narrow and fixable by wording changes alone (zero new machinery), consistent with the anti-bloat doctrine already governing the rest of the package.
**Recommendation:** Incorporate the 1 Critical + 1 Major finding (both are one-clause/one-number fixes, not redesigns); the 2 Minor findings are optional polish. Ready for S-002/S-004/S-001 critique after these are addressed; the Critical finding in particular should be closed before further critique rounds spend cycles re-discovering it (it is exactly the class of finding that has driven auto-REVISE in prior iterations per the design doc's own changelog).

---

## Charitable Interpretation

**Core thesis:** Turn an emergent, un-codified feedback/decision-capture habit into two lightweight, append-only, segment-rotating markdown ledgers, deliberately kept MEDIUM-tier (the HARD rule ceiling is full) so that once an entry is captured *and committed*, it survives compaction, session boundaries, and model swaps — without re-creating the context-rot problem Jerry exists to solve.

**Key claims:**
1. Logger-assigned canonical ids + verbatim operator aliases remove the [internal-kb] id-collision failure mode (FU.6) without requiring the operator to track a counter.
2. Capped-collection segment rotation (FU.5) keeps every single Read within the tool's read-window and well under the empirically observed truncation point (PM-001), at the cost of a small, in-file Segment Index.
3. The convention is deliberately minimal (≤3 lint checks, one new MEDIUM rule for rotation, zero new subsystems) — a corrective to the sibling ADR-convention's over-engineering spiral, cited as direct evidence (`design/adr-standards-rule-draft.md` ~30k-token L1 auto-load).
4. Every residual risk the design cannot close with proportionate machinery (concurrent-writer races, transcript-retention dependency, discovery-cost beyond canonical-id lookup, no L2 re-injection) is named explicitly rather than hidden — this is the design's strongest and most consistently applied virtue across all six files.

**Strengthening opportunities (expression/evidence, not substance):** the design's disclosure discipline is excellent in the design doc itself but has not been fully mirrored into the artifact that will actually be consulted after install (the staged rule file has no L2 re-injection and is the practical substitute for it); and one supporting metric (token count) has fallen behind the file it measures. Both are presentation/evidence gaps, not flaws in the underlying scheme.

**Decision Point:** Fundamentally coherent; no thesis-level incoherence. Proceeding through all six steps.

---

## Best Case Scenario

**Ideal conditions:** A single operator, single continuously-mediating assistant session, project-scoped work, feedback volume well under the ~50-entry/~800-line segment cap, and an install step that is actually completed (wiring the ≤3 lint checks into CI and adding the session-start read instruction to `project-workflow.md`). Under these conditions the scheme is genuinely low-ceremony and durable.

**Supporting assumptions that must hold:** (a) the operator does not run concurrent top-level sessions or unsynchronized hand-edits against the same log; (b) commits happen at the existing commit-cadence checkpoint so appended-but-uncommitted entries do not sit exposed for long; (c) the JSONL transcript backing `LLM-DECISION-LOG`'s excerpt+pointer default is retained and portable to wherever it is later read.

**Confidence assessment:** A rational evaluator should have **high** confidence in the underlying scheme (id/alias split, segment rotation, MEDIUM-tier scoping) — it is well-reasoned and evidenced. Confidence in the **as-currently-worded artifact set** is **moderate-high**, gated on the one Critical finding below: the specific "survive…" claim as worded in the artifact that ships stand-alone to `.context/rules/` (no design-doc cross-reference, no L2 re-injection) does not yet carry the qualifier the design doc itself decided was necessary.

---

## Steelman Reconstruction (excerpts)

Full-document rewrite is unnecessary — the six files are already well-hedged; only two passages need strengthening. Strongest-form restatements below (changes in **bold**; `[SM-NNN]` markers reference the Findings Table).

**`design/staging-feedback-logs/feedback-decision-logs-standards.md`, line 3 (current):**
> Two append-only, segment-rotating ledgers so that, once captured, user feedback and human/LLM decisions survive compaction, sessions, and model swaps.

**Strengthened `[SM-001]`:**
> Two append-only, segment-rotating ledgers so that, once captured **and committed**, user feedback and human/LLM decisions survive compaction, sessions, and model swaps. **An appended-but-uncommitted entry carries the same exposure as any other uncommitted change in this repo and is not covered by this guarantee** — commit at the existing commit-cadence checkpoint.

**`feedback-decision-log-convention-design.md`, line 202 (current):**
> ...the iteration-2 draft measures ~1,120 words ≈ ~2,150 tokens (`tiktoken cl100k`-estimate). The overage is re-ratified as the working budget...

**Strengthened `[SM-002]`:**
> ...the iteration-2 draft measured ~1,120 words ≈ ~2,150 tokens (`tiktoken cl100k`-estimate); **the current (iteration-3-revised) draft has since grown further (RT-003 CI-wiring caveat, the LOG-M-005 concurrent-session/hand-edit hedge, and the LOG-M-006 self-count discipline were all added directly into the shipped rule file after this count was taken — see changelog v5) and has not been re-measured. Treat ~2,150 as a floor, not the current figure, until re-counted.** The overage is re-ratified as the working budget on that basis...

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-i4-20260706 | Rule-file banner omits the "AND committed" durability qualifier that the design doc itself added (IN-001, iteration-3/v5) to close this exact overclaim class — the omission survives in the one artifact with no L2 re-injection that is meant to stand alone post-install | Critical | `feedback-decision-logs-standards.md:3` — "once captured...survive compaction, sessions, and model swaps" (no commit caveat) | Adds "and committed" + one-clause exposure note, mirroring `feedback-decision-log-convention-design.md:30`'s scope note (ii) | Internal Consistency |
| SM-002-i4-20260706 | Rule-file token-count measurement (~2,150 tokens) cited as evidence for a live P-020 ratification decision (SR-003) is attributed to "the iteration-2 draft" and is not re-measured, despite the design doc's own iteration-3 (v5) changelog documenting further additions made directly into that same staged file after the count was taken | Major | `feedback-decision-log-convention-design.md:202` and `:320` (SR-003) cite ~2,150 tokens as current; `feedback-decision-logs-standards.md:27-28,64` contain text the v5 changelog attributes to RT-003/RT-001/FM-005, added after that count | Re-measure the current staged file and re-state the figure (or explicitly flag it as a floor) before the P-020 ratification proceeds | Evidence Quality |
| SM-003-i4-20260706 | LOG-M-005's "operators SHOULD NOT do this" (referring to "concurrent top-level sessions/windows or direct human hand-edits") is ambiguous on first read against `examples-appendix.md`'s "Common cases" entry, which gives an explicit, endorsed procedure for solo hand-editing; the two are compatible under a charitable reading (the SHOULD-NOT targets concurrent/multi-writer scenarios, not solo hand-edits) but the wording does not make that scope explicit | Minor | `feedback-decision-logs-standards.md:27` vs `examples-appendix.md:172` | Reword LOG-M-005 to name the condition explicitly, e.g. "SHOULD NOT allow a concurrent writer (another session, or a hand-edit happening alongside an active assistant append) — a solo hand-edit with no other writer active is safe (see appendix, Common cases)" | Internal Consistency |
| SM-004-i4-20260706 | LOG-M-004 / design doc L1.2's graduation-trigger criterion (b) — "is ratified/durable (has survived at least one review)" — has no operational definition of "review" for a low-ceremony log entry, unlike criterion (a) which is directly checkable (attaches to a worktracker parent) | Minor | `feedback-decision-log-convention-design.md:139` | Add a one-clause example of what counts as "survived a review" (e.g., "referenced again in a later turn/session without being overturned, or explicitly re-affirmed by the user") — no new tracking field required | Methodological Rigor |

**Finding ID Format:** `SM-{NNN}-i4-{YYYYMMDD}` (iteration 4, 2026-07-06) to prevent collisions across tournament executions.

---

## Improvement Details

### SM-001-i4-20260706 (Critical) — Missing commit-durability qualifier in the shipped rule file

**Affected Dimension:** Internal Consistency (primary), Evidence Quality (secondary)

**Original Content:** `feedback-decision-logs-standards.md` line 3: *"...so that, once captured, user feedback and human/LLM decisions survive compaction, sessions, and model swaps."*

**Strengthened Content:** See [Steelman Reconstruction](#steelman-reconstruction-excerpts) `[SM-001]` above — add "and committed" plus the one-clause exposure note.

**Rationale:** The design doc's own L0 scope note (ii), added specifically to close an overclaim ("`Survive' means once appended **AND committed**. An uncommitted append carries the same exposure as any other uncommitted change in the repo — a `git checkout`/`clean`/`reset` before the next commit erases it, with no backstop", line 30), was written precisely because an unqualified "survive" claim had already been flagged as a defect once (the design doc's own v4/v5 changelog documents a "package-wide overclaim sweep across all 6 files" in iteration-2, and IN-001 adding this exact caveat to L0 in iteration-3). The staged rule file — the one artifact of the six that (a) is the actual install target for `.context/rules/`, (b) receives **no L2 per-prompt re-injection** (the design doc itself states this at line 221: "it receives no L2 per-prompt re-injection...it is therefore more context-rot-vulnerable than a HARD rule"), and (c) does not cross-reference the design doc for the fuller nuance — restates the same "survive...compaction, sessions, and model swaps" claim **without** the qualifier that was added to fix exactly this problem elsewhere. A future session or operator that only ever reads the installed rule file (the expected steady-state post-install) would receive the overclaimed version, not the corrected one. This is not a design flaw — the underlying scheme (commit-cadence-gated durability) is sound and already correctly stated in the design doc — but the fix from a prior remediation round did not fully propagate to the operationally primary artifact, which is precisely the "recurrence in an un-swept location" failure mode this project's own adversary history (per the design doc's iteration-2 auto-REVISE) treats as Critical. Per this iteration's explicit instruction, overclaimed coverage is Critical.

**Best Case Conditions:** Fixed by adding four words and one clause to a single line; zero new machinery, fully consistent with the anti-bloat doctrine already governing every other fix in this package.

---

### SM-002-i4-20260706 (Major) — Stale token-count evidence for a live P-020 decision

**Affected Dimension:** Evidence Quality (primary), Traceability (secondary)

**Original Content:** `feedback-decision-log-convention-design.md` line 202: *"...the iteration-2 draft measures ~1,120 words ≈ ~2,150 tokens (`tiktoken cl100k`-estimate). The overage is re-ratified as the working budget..."* — reiterated verbatim at line 320 (v5 changelog, `[USER-DECISION]: SR-003`) as if it describes the current file.

**Strengthened Content:** See [Steelman Reconstruction](#steelman-reconstruction-excerpts) `[SM-002]` above.

**Rationale:** The design doc's own v5 (iteration-3) changelog entry documents specific text additions made *directly into the staged rule file* during that same iteration — "RT-003 added the CI-wiring-required caveat **into the staged rule file's L5 Lint section**", "RT-001/FM-002/PM-003 added a Scope boundary naming concurrent top-level sessions/windows and direct human hand-edits... (design L1.1 + rule LOG-M-005)", "FM-005 added an interim in-session self-count discipline (LOG-M-006 + L1.4)". Cross-checking against the current staged file confirms all three are present (`feedback-decision-logs-standards.md` lines 27-28 and 64). None of this text existed when the "~1,120 words ≈ ~2,150 tokens" figure was measured (that figure is explicitly attributed to "the iteration-2 draft"). The design doc never re-measures or re-states the count for the iteration-3-revised file; it instead reuses the iteration-2 figure as if current, including at the exact point (SR-003, line 320) where the user is asked to make a P-020 ratification call between "ratify-target-at-~2,150 vs trim-toward-1,500." An understated overage figure could bias that live decision. This does not undermine the underlying design (the convention works regardless of whether the true count is 2,150 or, say, 2,300 tokens) but it is a genuine, checkable evidence gap feeding an active user decision.

**Best Case Conditions:** Fixed by re-running the token count against the current staged file and updating the two citations (or, more cheaply, softening both to "~2,150 tokens as of iteration-2; grown further since — re-count before ratifying" — zero new machinery either way).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Both open questions (SM-003, SM-004) are pre-existing disclosed trades, not gaps in coverage; the package already covers segment rotation, id scheme, scoping, boundaries, and lint. |
| Internal Consistency | 0.20 | Negative (pre-fix) / Positive (post-fix) | SM-001 is a direct recurrence of the overclaim class this project's own adversary history treats as the primary Internal Consistency failure mode; fixing it removes the last confirmed instance found under charitable reading. SM-003 is resolved by charitable reading but benefits from the reworded clarification. |
| Methodological Rigor | 0.20 | Neutral/Positive | The six-file package demonstrates disciplined charitable-reading-compatible design (single-writer framing, collision-resistant framing); SM-004 is a minor rigor polish (operationalizing "survived a review"). |
| Evidence Quality | 0.15 | Negative (pre-fix) / Positive (post-fix) | SM-002 is a direct Evidence Quality gap: a specific, precise-looking number is stale relative to the very changelog that documents the edits which invalidated it. |
| Actionability | 0.15 | Positive | All four findings are single-clause or single-recount fixes; no new subsystem, lint, or field is required for any of them — directly incorporable by the original author. |
| Traceability | 0.10 | Positive | Both major findings were verified by direct cross-reference between the design doc's own changelog claims and the current staged file content (line-cited above), making each finding independently checkable. |

---

*Steelman execution complete. Ready for downstream critique strategies (S-002, S-004, S-001) per H-16 — SM-001 in particular should be resolved first so downstream critique targets the corrected artifact rather than re-discovering the same recurrence.*
