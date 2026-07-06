# Refutation Panel — Factual-Accuracy Lens (S-002, iteration-007)

> Panel: factual-accuracy. Target: `adversary/iteration-007/s-002-findings.md`. Scope: the single Critical (`DA-001-iter7`) only, per assignment. Verdict is VERIFIED or REFUTED based strictly on whether the defect exists at the cited lines in the CURRENT deliverable files, not on severity or novelty judgment.

## Method

Read the target report's Critical finding and its three cited locations verbatim against the current file content:
- `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:195` (L1.4 Cap row) and `:203-208` (rotation procedure, cited only for context)
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006)
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/examples-appendix.md:173` (hand-edit bullet)

Also searched the three deliverable files (plus the design doc's full Revision Changelog, `feedback-decision-log-convention-design.md:337-352`) for any stated offset/baseline-addition formula (`baseline`, `starting id`, `starting canonical`, `offset`) that might save the shortcut, and checked `restore-notes.md`'s "Residuals Disclosed" table for whether this specific arithmetic gap was already named as a closed/disclosed iteration-006 Critical.

## Finding: DA-001-iter7 — Near-cap `grep -c` id-minting shortcut miscounts after the first segment [CRITICAL]

**VERDICT: VERIFIED**

**Citations checked, confirmed current:**
- `feedback-decision-log-convention-design.md:195` (Cap row, id-minting clause) reads, verbatim in the current file: *"At or near cap (within ~5 entries, PM-005), id-minting SHOULD derive the next id from a deterministic `grep -c '^## FU\.'` (or `'^## DEC-LLM-'`) count — reusing the parity-check tool, no new lint — rather than an LLM Read of a file that may already be truncated past its tail (PM-002)."* This is the literal current text; no offset/baseline term appears in this sentence or anywhere else in the Cap row.
- `staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006) carries the same instruction verbatim: *"…derive the next id from a `grep -c '^## FU\.'` / `'^## DEC-LLM-'` count, not an LLM Read of a possibly-truncated file (PM-002)."*
- `staging-feedback-logs/examples-appendix.md:173` carries the same instruction in the hand-edit bullet: *"If the file is at or near the segment cap, count with `grep -c '^## FU\.'` rather than a Read that may truncate before the tail (PM-002)."*

**Arithmetic verification:** `grep -c '^## FU\.' FEEDBACK-LOG.md` run against the stable ACTIVE file returns the count of matching headings physically present in *that one file*. Per the design's own Segment Index example (`examples-appendix.md:141`, `2 | FEEDBACK-LOG.md (ACTIVE) | FU.50 – …`), the ACTIVE file's first heading after Segment-1 rotation is `FU.50`, not `FU.0`. A Segment-2 ACTIVE file holding `FU.50`…`FU.94` (45 headings) yields `grep -c` = 45. None of the three cited locations states an addition of the segment's starting canonical id (e.g., "+ 50") to that count. Applying the instruction exactly as written — "derive the next id from" the count — would mint `FU.45`, which already exists in sealed Segment 1. This reproduces the failure LOG-M-005 is designed to prevent (`feedback-decision-logs-standards.md:27`: ids "unique and monotonic per log across segments").

**Confirmed not a false positive / misreading:**
1. A repo-wide search of the three deliverable files plus the design doc's full Revision Changelog (`:337-352`, all 9 rounds) for `baseline`, `starting id`, `starting canonical`, `offset` returns zero hits that supply the missing segment-baseline term for this specific shortcut. The only other `grep -c` use in the package is the **parity check** (`feedback-decision-log-convention-design.md:207`, `feedback-decision-logs-standards.md:67`), which is a distinct mechanism (sums two file-local counts against a *pre-recorded* pre-seal total) and does not compute an absolute id either — so it supplies no save.
2. `restore-notes.md`'s Step 1 table (the authoritative "6 iteration-006 Criticals closed" record) lists RT-001, DA-001/FM-006 ("Four"→"Five"), PM-001/IN-001 (AE-006e disclosure), PM-002 (install-stall bound), FM-001 (inline-doc dedup), FM-003 (split-entry) as the closed set. None of these six addresses the near-cap id-count arithmetic; this is a distinct claim from all of them. It is therefore not a restatement of an already-disclosed/closed residual.
3. The design doc's own Revision Changelog v7 entry (`:349`) shows the `grep -c` near-cap shortcut was *introduced* in iteration-5 ("a deterministic `grep -c` id-count near cap," RT-004/FM-001/PM-002) as a Major-tier propagation fix for a different concern (avoiding model-dependent counting); no subsequent round's changelog entry (v8 `:350`, v9 `:351`) revisits or corrects this shortcut's per-segment arithmetic. The defect is therefore original to the current text, not a stale reference to a prior, since-fixed state.

**Assessment:** The cited defect exists verbatim at all three cited locations in the current files, the arithmetic argument is sound (segment-2-onward ACTIVE-file heading counts diverge from global canonical id values by exactly the prior segments' entry totals), and no disclosed-residual or restore-notes entry already covers this specific gap. This is not a misreading, a stale reference, or a restatement of a disclosed residual.

## Summary Table

| ID | Verdict | Basis |
|----|---------|-------|
| DA-001-iter7 | VERIFIED | Defect confirmed verbatim at `feedback-decision-log-convention-design.md:195`, `feedback-decision-logs-standards.md:28`, `examples-appendix.md:173`; no offset/baseline formula found anywhere in the 3 deliverable files or the design doc's 9-round changelog; not listed among restore-notes.md's 6 already-closed iteration-006 Criticals. |
