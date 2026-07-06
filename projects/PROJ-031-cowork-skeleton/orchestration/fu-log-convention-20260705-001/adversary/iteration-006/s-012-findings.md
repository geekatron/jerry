# FMEA Report: Feedback & Decision Log Convention (design + 5 staged artifacts)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory-step-1) | Lifecycle decomposition (8 elements) |
| [Findings Table](#findings-table-rpn-sorted) | All FM-NNN findings, RPN-sorted |
| [Finding Details](#finding-details) | Expanded Critical + Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Header

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012, iteration 6, blind protocol — no other adversary iteration files read)
**H-16 Compliance:** S-003 Steelman is not directly required before S-012 (not named in H-16); this deliverable's own changelog shows an S-003-equivalent strengthening pass occurred across iterations 1–5 (design revision rounds v1–v7) prior to this execution — treated as satisfied for the C3+ sequence per template Prerequisites.
**Elements Analyzed:** 8 | **Failure Modes Identified:** 12 | **Total RPN:** 1,509

---

## Summary

Decomposing the FU/DEC log convention across 8 lifecycle elements (chat capture, inline-doc capture, alias/canonical mapping, rotation trigger, segment linking, cross-log navigation, backfill, multi-session concurrency) surfaced 12 failure modes, 3 Critical (RPN 210–336), 5 Major (RPN 80–126), 4 Minor/monitor (RPN 36–75, mostly amplifying disclosures the package already makes). All three Criticals are **wording/scope-clarification gaps in existing mechanisms**, not missing subsystems — consistent with the anti-bloat posture the package has maintained across 5 prior revision rounds; none of the recommended fixes below add a new file, lint check, or subsystem. **Recommendation: REVISE** (targeted corrections), not REJECT — the design's decomposition is sound and its disclosure discipline is unusually strong (most disclosed residuals in this package are genuinely accepted trade-offs, not silent gaps); the 3 Criticals are concentrated in the same recurring failure class this deliverable's own changelog names across iterations 1–5 (SM-003: "a disclosure that exists somewhere in the package but not at the point of the claim," or here, a claim whose own cited evidence contains an unacknowledged counter-example).

---

## Element Inventory (Step 1)

| Element | Description |
|---------|-------------|
| E1 | Entry creation — chat channel (LOG-M-001/002, design L1.1 entry schema) |
| E2 | Entry creation — inline-doc channel (`FU:`/`DEC:` marker harvest) |
| E3 | Alias/canonical ID mapping (LOG-M-005, FU.6 scheme) |
| E4 | Rotation trigger (LOG-M-006, ~50 entries/~800 lines cap, self-count discipline) |
| E5 | Segment linking (prev/next, Segment Index) |
| E6 | Cross-log navigation (`Related: <id>`) |
| E7 | Backfill (Backfill Queue, promotion, `(backfilled)` tag, chronology) |
| E8 | Multi-session concurrency (single-writer-per-log discipline) |

Decomposition is MECE against the 7 lifecycle areas named for this execution (chat and inline-doc are split from "entry creation" into E1/E2 for analytical granularity).

---

## Findings Table (RPN-sorted)

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-i6 | E2 | No dedup for repeated harvest of the same `FU:`/`DEC:` inline-doc marker across multiple reads of the same file | 7 | 6 | 8 | 336 | Critical | See [Details](#fm-001-i6-duplicate-inline-doc-marker-harvest) | Completeness |
| FM-002-i6 | E4 | ~800-line rotation cap assumes uniform ~12–18 lines/entry; assistant-authored Disposition/Summary fields can be dense single-line paragraphs that defeat the line-count proxy for the ~25k-token truncation guard | 7 | 5 | 8 | 280 | Critical | See [Details](#fm-002-i6-linecount-cap-is-not-a-reliable-token-proxy) | Internal Consistency |
| FM-003-i6 | E1 | LOG-M-002 defines chat capture as "a chat message in full," but the package's own real usage splits one multi-topic message into several per-topic entries, each capturing only its slice | 6 | 7 | 5 | 210 | Critical | See [Details](#fm-003-i6-full-capture-rule-contradicts-observed-split-entry-practice) | Internal Consistency |
| FM-004-i6 | E1 | Machine anchor `{session_id}#{promptId}` identifies a turn, not an entry; one turn can (and demonstrably does) yield multiple FU.N entries sharing one anchor with no sub-turn disambiguator | 3 | 6 | 7 | 126 | Major | See [Details](#fm-004-i6-turn-anchor-is-not-unique-per-entry) | Traceability |
| FM-005-i6 | E7 | The `(backfilled)` anti-fabrication tag's presence/removal is not checked by any of the 3 lints; premature removal (falsely implying independent verification) is undetectable | 5 | 3 | 7 | 105 | Major | See [Details](#fm-005-i6-backfilled-tag-integrity-is-unenforced) | Evidence Quality |
| FM-006-i6 | E5 | Segment Index/Backfill-Queue overflow mitigation ("*-INDEX.md sidecar") is deferred/not built; its only trigger is the same commit-cadence checkpoint already named elsewhere as a correlated SPOF for 4 other safety functions — this makes it a 5th | 4 | 4 | 6 | 96 | Major | Name this as a 5th dependent in the existing "One shared dependency" disclosure | Methodological Rigor |
| FM-007-i6 | E3 | No format guidance for operator-supplied alias text; a heading-breaking alias (unbalanced `)`, backtick, embedded newline) could corrupt `## FU.N <slug> (alias: X)`, silently defeating all 3 exact-pattern lints at once | 5 | 3 | 6 | 90 | Major | See [Details](#fm-007-i6-unsanitized-alias-text-can-corrupt-the-heading-pattern) | Methodological Rigor |
| FM-008-i6 | E3 | H-31 bare-alias enumeration is not required to show each candidate's source document/turn; with per-document alias restart, multiple unrelated docs can share the same alias label with no source-disambiguated listing mandated | 4 | 4 | 5 | 80 | Major | Require source (path/turn) alongside each enumerated candidate | Completeness |
| FM-009-i6 | E4 | The interim self-count rotation discipline says "propose rotation on approaching the cap" with no numeric trigger point (e.g., 80% of 50/800), unlike every other threshold in the design | 3 | 5 | 5 | 75 | Minor | Add a numeric early-trigger (e.g., ~40 entries / ~640 lines) | Actionability |
| FM-010-i6 | E6 | `Related: <id>` cross-log referential integrity is not checked by any lint (already disclosed in rule file scope-limits) | 3 | 3 | 6 | 54 | Minor (monitor) | No new action; already disclosed, not overclaimed | Traceability |
| FM-011-i6 | E7 | Backfill chronology-by-datetime requires reading every segment to reconstruct a true timeline once backfilled entries exist (already disclosed generically as a discovery-cost trade) | 3 | 3 | 5 | 45 | Minor (monitor) | No new action; consistent with disclosed discovery-cost trade | Traceability |
| FM-012-i6 | E8 | Single-writer-per-log discipline is procedural only, not lint- or permission-enforced (exhaustively disclosed across 5 revision rounds — RT-001/DA-001/PM-001/FM-001/IN-001 per the design's own changelog) | 4 | 3 | 3 | 36 | Minor (monitor) | No new action; this is the most thoroughly disclosed residual in the package | Internal Consistency |

**RPN >= 200 count:** 3 of 12 (25%) — flags Critical per protocol.
**RPN > 80 count:** 7 of 12 (58%) — exceeds the 30% systemic-quality-issues threshold per protocol Step 3 Decision Point. Read in context: 4 of those 7 are wording-level fixes to *existing* mechanisms (FM-004, FM-006, FM-007, FM-008), not missing subsystems, and the package's own remediation history (5 prior rounds, all "wording/deletion/propagation, zero new machinery") shows this class of finding is normal and cheaply closeable for this deliverable — it is not evidence of an under-designed convention.

---

## Finding Details

### FM-001-i6: Duplicate inline-doc marker harvest

| Attribute | Value |
|-----------|-------|
| **Element** | E2 — Entry creation, inline-doc channel |
| **Severity** | Critical (RPN 336 = S7 × O6 × D8) |

**Evidence:** `feedback-decision-logs-standards.md:36` — "On reading a doc, harvest each marker with `source: inline-doc` + path/anchor and announce in-turn (**no doc mutated**)." The design doc's own UX disposition table explicitly declined the one mechanism that would prevent re-harvest: `feedback-decision-log-convention-design.md:305` — "F-026 (standardized syntax + in-turn announce fold; writing a `<!-- HARVESTED -->` comment back into the operator's source doc **declined as intrusive**)." `FEEDBACK-LOG.template.md:25` repeats the same no-mutation harvest instruction. Nowhere in the design doc, rule file, templates, or `examples-appendix.md` "Common cases" section is there a substitute mechanism (e.g., "check the log for an existing entry with the same path+anchor before minting a new one").

**Analysis:** Because the source document is never mutated to mark a marker as captured, every subsequent read of that document by the assistant (a different session, a later turn in the same session, or simply re-opening the file for an unrelated task) is a candidate to harvest the *same* `FU:`/`DEC:` line again, per the letter of the harvest instruction ("when the assistant reads a doc containing such a marker, it SHOULD harvest it"). The one disclosed dedup discussion in this package (`FM-004` in the iteration-4 changelog, `feedback-decision-log-convention-design.md:330`) addresses a *different* problem — the same feedback appearing in both chat and an inline-doc — and explicitly declines a scan-before-mint as "machinery." That rebuttal does not cover the narrower, higher-occurrence case here: the identical marker, in the identical file, read twice. Occurrence is rated 6 (not 8) because it requires the assistant to actually re-read the *full* (not offset-limited) span containing the marker on a later occasion, which is common in a project this size but not universal. Detection is rated 8: the id-integrity lint (rule file `feedback-decision-logs-standards.md:66`) only checks uniqueness/monotonicity/contiguity of `FU.N`, which duplicate-harvested entries still satisfy (each gets a fresh, valid, non-colliding id) — nothing flags that two ids reference materially identical verbatim content from the same source anchor.

**Corrective Action:** No new file, lint, or doc-mutation is required (preserves the F-026 rebuttal's anti-bloat rationale). Add one behavioral clause to LOG-M-001/the inline-marker bullet: "before minting a new inline-doc entry, check whether an existing entry already carries `source: inline-doc` with the same `path:line/anchor` — if so, do not mint a duplicate; note the re-encounter against the existing entry instead (e.g., a one-line `Re-observed: {date}` addendum, or simply skip)." This reuses the existing Context `source` sub-field as the dedup key — no new field, no new lint.

**Acceptance Criteria:** The rule file's inline-marker bullet and both templates' inline-doc bullets state the check-before-mint step; `examples-appendix.md` "Common cases" gains one bullet illustrating it.

**Post-Correction RPN estimate:** Occurrence drops to 2 (dedup check now instructed) → RPN ≈ 7 × 2 × 8 = 112 (Major, residual because the check itself remains a SHOULD-tier behavioral step, not a lint).

---

### FM-002-i6: Line-count cap is not a reliable token proxy

| Attribute | Value |
|-----------|-------|
| **Element** | E4 — Rotation trigger |
| **Severity** | Critical (RPN 280 = S7 × O5 × D8) |

**Evidence:** The cap's entire justification rests on a uniform-density assumption: `feedback-decision-logs-standards.md:28` — "The cap assumes ~12–18 lines/entry, so a **few unusually verbose verbatim entries** SHOULD trigger earlier rotation regardless of the numeric count (IN-002)." The design doc repeats the same scope: `feedback-decision-log-convention-design.md:180` cites "measured ~12–18 lines/entry on the real bootstrap entries" as the evidence the two thresholds (50 entries / 800 lines) "land together." But the cited evidence file itself contains a direct counter-example the design does not name: `FEEDBACK-LOG.md:49` — the **Disposition** field of `FU.1` is a single unwrapped markdown line running to several hundred words (a multi-round remediation narrative: "CONCLUDED AT ITERATION CEILING… Verified-criticals endgame… Diagnosis: non-convergent finding stream…"), which by itself is comparable in token weight to what the design assumes an *entire multi-line entry* costs.

**Analysis:** IN-002's mitigation names only **"verbatim"** entries as the source of length variance — i.e., long user input. But the actual evidence shows the risk is at least as strong (here, entirely) in **assistant-authored** fields: Disposition and Summary have no length constraint in the schema (design doc `feedback-decision-log-convention-design.md:54-59`, entry schema table), and FU.1's Disposition is exactly the kind of running-status narrative that recurs naturally for any entry that gets updated across a long remediation arc (which this project has already done at least once). Because raw line-count does not track token count once a field is a dense unwrapped paragraph, a segment could show well under the ~800-line / ~50-heading cap (and pass lint check 1 cleanly) while already holding materially more tokens than the ~8–12k the cap is designed to bound — silently defeating the stated purpose of the cap ("2–3× under the ~25k-token truncation observed in this very project"). Severity is rated 7 (the failure undermines the specific safety property FU.5/L1.4 exists to guarantee, even though the log itself is not otherwise invalidated). Detection is rated 8: no L5 lint counts tokens or words, only lines and headings (`feedback-decision-logs-standards.md:65`).

**Corrective Action:** Widen IN-002's language from "verbose verbatim entries" to "verbose entries in **any** field (verbatim, summary, or disposition)" — a one-clause edit, no new machinery. Optionally note that a Disposition field accreting a running narrative across multiple review rounds (as `FU.1` demonstrates) is exactly the pattern to watch for, and that terminal-disposition text SHOULD be periodically compacted with detail moved to a linked artifact rather than left to grow in place — consistent with the log's own append-only/status-pointer conventions.

**Acceptance Criteria:** `feedback-decision-logs-standards.md` LOG-M-006 wording updated; `design/feedback-decision-log-convention-design.md` L1.4 cap-justification paragraph acknowledges the Disposition-field counter-example already present in its own cited evidence file.

**Post-Correction RPN estimate:** Occurrence unchanged (the phenomenon still occurs), but Detection drops to 5 once the assistant is explicitly instructed to weigh field density, not just line count, when self-counting near the cap → RPN ≈ 7 × 5 × 5 = 175 (Major, residual because there is still no automated token check).

---

### FM-003-i6: "Full" capture rule contradicts observed split-entry practice

| Attribute | Value |
|-----------|-------|
| **Element** | E1 — Entry creation, chat channel |
| **Severity** | Critical (RPN 210 = S6 × O7 × D5) |

**Evidence:** LOG-M-002 (`feedback-decision-logs-standards.md:24`): "Capture user feedback **verbatim and full** … the operator's complete text *as given in that channel* (a chat message **in full**…)." The design doc's entry-schema row states the identical rule (`feedback-decision-log-convention-design.md:56`). Compare this against the package's own real usage: `FEEDBACK-LOG.md:97` — "User reviewed `design/staging-feedback-logs/feedback-decision-logs-standards.md` and provided **5 items**" (singular review turn, 5 items) — yet the result is **5 separate entries** (`FU.5` at line 101, `FU.6` at line 113, `FU.7` at line 125, `FU.8` at line 137, plus `FU.9` under a different heading at line 148), each with a **distinct, non-overlapping** Verbatim block containing only that entry's own topic (e.g., `FU.6`'s Verbatim at line 115-120 is only the id-scheme question; it does not repeat `FU.5`'s log-growth question or `FU.7`'s ceiling question).

**Analysis:** If "a chat message in full" is read literally, each of the 5 resulting entries should carry the *entire* combined message as its Verbatim (since all 5 items were "provided" in what the header implies was one review submission) — but none do; each carries only its own slice. This is a genuine, demonstrable gap between the stated fidelity rule and the actual, sensible practice of splitting a multi-topic message into per-topic entries. The ambiguity matters because LOG-M-002 is the package's single most load-bearing claim ("verbatim wins on conflict," repeated at `feedback-decision-logs-standards.md:24` and `examples-appendix.md` throughout) — an unclarified "full" that in practice becomes "the entry's own excerpt" without ever saying so is exactly the overclaim class this tournament has repeatedly had to correct (the design's own changelog names this pattern as its dominant recurring defect across iterations 1–5: a claim whose scope silently narrows in practice). Occurrence is rated 7 because it has **already happened** in this project's only multi-item feedback turn to date — it is not a hypothetical. Severity 6 (a fidelity-rule ambiguity, not a lost-data failure — the union of the 5 entries does reconstruct the original content). Detection 5 (visible on direct comparison, as done here, but nothing in the self-review or lint checks the "full" claim against message-splitting).

**Corrective Action:** Clarify LOG-M-002 (wording-only, no new machinery): "When a single message bundles multiple distinct feedback items, each MAY be logged as a separate entry; each entry's Verbatim is that item's own text (not required to repeat the full combined message in every split entry). Splitting is itself a judgment call and SHOULD be noted in the Summary (e.g., '1 of 5 items from this turn')." Propagate the same clause to the design-doc entry-schema row and, if space allows, one line in `examples-appendix.md`.

**Acceptance Criteria:** LOG-M-002 no longer reads as requiring whole-message duplication across split entries; the FU.5–FU.9 pattern in the live bootstrap log becomes an example of *compliant* practice rather than an unacknowledged departure from the written rule.

**Post-Correction RPN estimate:** Ambiguity resolved → Detection drops to 2 (the rule now matches practice, so there is nothing latent to miss) → RPN ≈ 6 × 7 × 2 = 84 (Major → trends toward Minor once observed once more without incident).

---

## Recommendations

Grouped by severity, highest RPN first. All corrective actions are wording/clarification edits to existing artifacts — none add a new file, lint check, or subsystem, consistent with the package's established anti-bloat remediation pattern.

**Critical (fix before ratification):**
1. **FM-001-i6** — Add a check-existing-entry-before-mint step to the inline-doc harvest instruction (rule file + both templates). Est. RPN reduction: 336 → ~112.
2. **FM-002-i6** — Widen IN-002 to cover Disposition/Summary field density, not only verbatim length; name the FU.1 counter-example explicitly in L1.4. Est. RPN reduction: 280 → ~175.
3. **FM-003-i6** — Clarify LOG-M-002's "full" to permit per-topic split entries without requiring whole-message duplication; note the split in the Summary field. Est. RPN reduction: 210 → ~84.

**Major (recommended before ratification, not blocking):**
4. **FM-004-i6** — Note in L1.1/LOG-M-005 that one turn anchor may cover multiple entries; this is expected, not an error.
5. **FM-005-i6** — Extend lint 3 (terminal-evidence presence) description to also note `(backfilled)` tag presence is unchecked, OR add one clause to Backfill mechanics that the tag's removal SHOULD cite the specific reference inline (self-documenting, no lint needed).
6. **FM-006-i6** — Name the Segment-Index-overflow trigger as a 5th dependent of the existing "One shared dependency" commit-cadence SPOF disclosure.
7. **FM-007-i6** — Add one line: aliases SHOULD avoid unbalanced parentheses/backticks/newlines; if present, the logger normalizes or drops the offending characters before recording.
8. **FM-008-i6** — Require the H-31 enumeration to list each candidate's source (path/turn), not just its alias text.

**Minor (monitor only, no action required):**
9–12. FM-009 through FM-012-i6 are consistent with trade-offs the package already discloses explicitly; no additional wording is needed. They are listed here only for lifecycle-coverage completeness (MECE decomposition), not as new gaps.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001 (no dedup path for repeated inline-doc harvest) and FM-008 (source-disambiguation gap in H-31 enumeration) are real gaps in mechanisms the package otherwise designed thoroughly. |
| Internal Consistency | 0.20 | Negative | FM-002 and FM-003 are both cases where a stated rule/justification is contradicted by the package's own cited evidence (the bootstrap log) — the same defect class (propagation/scope-mismatch) this deliverable's changelog names as its dominant recurring issue across iterations 1–5. |
| Methodological Rigor | 0.20 | Negative | FM-006 and FM-007 show two more places where an existing disclosed limitation (commit-cadence SPOF; heading-format drift) has a specific, previously-unnamed instance that should be folded in, rather than a rigor failure in the FMEA-relevant sense of missing methodology. |
| Evidence Quality | 0.15 | Mixed | The package's evidence discipline is genuinely strong (real bootstrap entries cited throughout, file+line traceable) — FM-005's gap is narrow (one tag's enforcement) and FM-002/FM-003 findings were only findable *because* the package cites verifiable, checkable evidence in the first place. |
| Actionability | 0.15 | Positive | Every Critical and Major finding above has a one-clause, anti-bloat-compliant corrective action with an estimated post-correction RPN; none require new machinery. |
| Traceability | 0.10 | Positive | All 12 findings cite specific file+line evidence and map cleanly to one of the 8 decomposed lifecycle elements. |

---

*Template: `s-012-fmea.md` v1.0.0 | Execution: iteration-006, blind protocol (S-012 only; no other adversary-iteration files read) | P-003: no subagents invoked | P-020: draft-only, no framework-path writes | P-022: all findings cite file+line evidence; inferences about turn-splitting from the "provided 5 items" header phrasing are labeled `[INFERENCE]` where the underlying combined-message text itself was not directly observed (only its 5 resulting split entries).*
