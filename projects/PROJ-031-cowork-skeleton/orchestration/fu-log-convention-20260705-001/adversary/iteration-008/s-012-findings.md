# FMEA Report: Feedback & Decision Log Convention (design + 5 staged artifacts)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory-step-1) | Lifecycle decomposition (10 elements) |
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
**Reviewer:** adv-executor (S-012, iteration-008, VERIFIED-CRITICALS protocol, blind — no iteration-007/008 adversary files read except `iteration-007/restore-notes.md`, explicitly disclosed as readable)
**H-16 Compliance:** S-003 Steelman is not directly required before S-012 (not named in H-16). This deliverable's own Revision Changelog documents 8 rounds of S-003-equivalent strengthening (v1–v9) and the iteration-007 RESTORE pass prior to this execution; treated as satisfied for the C4 sequence per template Prerequisites. Not independently re-verified under blind protocol (S-003 iteration-008 output not read).
**Elements Analyzed:** 10 | **Failure Modes Identified:** 4 | **Total RPN:** 840

---

## Summary

This is iteration 8 of an already heavily-remediated (8 revision rounds) design package. Rather than re-deriving the 6 iteration-006 Criticals the owner's `iteration-007/restore-notes.md` documents as closed (verified against current text — all 6 confirmed closed, no regression found), this execution decomposed the **current** post-restore text — specifically the newest additions (the "Five safety functions" fix, the inline-doc dedup instruction, the redaction category+size carve-out, and the two brand-new FU.10 Mermaid diagrams) — for genuinely new failure modes. **Two Critical findings surfaced, both instances of the package's own named recurring defect class ("a claim contradicts an adjacent/cross-referenced disclosure," per the iteration-007 hunt brief) appearing in text that is *newer than the class's own remediation*.** FM-001-i008fmea is a direct, provable contradiction between the design doc's L2 governance section (claims lint 2 "detects" segment-index overflow) and the rule file's own Scope-limits disclosure (which explicitly lists Segment Index accuracy as something the lints do **not** check) — the exact fix that raised "Four safety functions" to "Five" (DA-001, this restore round) introduced a fresh instance of the class it was fixing elsewhere. FM-002-i008fmea finds that the mechanism which closed the tournament's single highest-RPN historical Critical (FM-001-i6, duplicate inline-doc harvest, RPN 336) has no defined canonical key format and — checked across all 6 files — **zero worked examples anywhere in the package**, despite the package's own FU.8 doctrine of embedding a worked example for every mechanism. Two Major findings (FM-003, FM-004) round out the decomposition: the brand-new FU.10 lifecycle diagram omits the dedup gate it sits directly above, and the redaction mechanism (this round's other Critical fix, RT-001) likewise has no worked example. All four corrective actions are wording/example-only — consistent with the package's established anti-bloat remediation pattern; none require new machinery. **Recommendation: REVISE** (targeted, wording/example-level fixes) — the two Criticals are concentrated in the newest text (post-restore), not in previously-verified-stable sections, and both are one-paragraph-scale fixes.

---

## Element Inventory (Step 1)

| Element | Description |
|---------|--------------|
| E1 | Entry creation — chat channel |
| E2 | Entry creation — inline-doc channel (marker harvest + dedup gate) |
| E3 | Alias/canonical id mapping (H-31 back-reference enumeration) |
| E4 | Segment rotation mechanics (cap, parity check, crash recovery) |
| E5 | Segment Index (display + overflow re-assessment trigger) |
| E6 | Entry-lifecycle visual layer (FU.10, new this round: 2 Mermaid diagrams) |
| E7 | Redaction / public-repo hygiene carve-out (RT-001, new this round) |
| E8 | Governance / Adoption plan (shared commit-cadence checkpoint dependency) |
| E9 | L5 lint scope (3 checks + disclosed scope-limits block) |
| E10 | Worked-examples appendix (FU.8 completeness doctrine) |

Decomposition targets the artifacts and mechanisms materially changed or added in the iteration-007 RESTORE pass (per `restore-notes.md`), since the remaining, previously-stable text was already re-verified there against regression.

---

## Findings Table (RPN-sorted)

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|---------------------|
| FM-001-i008fmea | E5/E8 | The design doc's "Five safety functions" fix (this round's own DA-001 closure) claims lint 2 "detects" Segment-Index overflow, directly contradicted by the rule file's own Scope-limits disclosure, which lists Segment Index accuracy as unchecked | 7 | 6 | 7 | 294 | Critical | See [Details](#fm-001-i008fmea-segment-index-overflow-exemption-contradicts-the-rule-files-own-scope-limits-disclosure) | Internal Consistency |
| FM-002-i008fmea | E2/E10 | The inline-doc dedup key (`path:line/anchor`) that closed the tournament's highest-RPN historical Critical (FM-001-i6) has no defined canonical format and zero worked examples anywhere in the 6-file package | 7 | 6 | 7 | 294 | Critical | See [Details](#fm-002-i008fmea-inline-doc-dedup-key-is-unspecified-and-has-zero-worked-examples-in-the-package) | Evidence Quality |
| FM-004-i008fmea | E7/E10 | The redaction mechanism (this round's own RT-001 closure — category + approximate-size disclosure) has no worked example anywhere in the package, despite FU.8's embedded-example doctrine covering every other mechanism | 4 | 6 | 6 | 144 | Major | See [Details](#fm-004-i008fmea-redaction-mechanism-has-no-worked-example) | Actionability |
| FM-003-i008fmea | E6 | The new FU.10 entry-lifecycle `stateDiagram-v2` (rule file) omits the check-before-mint dedup gate it sits directly above, and shows `DONE`/`WONTFIX` transitioning straight to `[*]` with no visual reopen path, understating the process it is meant to teach "for yourself" (per `restore-notes.md` Step 2) | 6 | 3 | 6 | 108 | Major | See [Details](#fm-003-i008fmea-new-fu10-diagram-omits-the-dedup-gate-and-the-reopen-path) | Completeness |

**RPN >= 200 count:** 2 of 4 (50%) — flags Critical per protocol. Both Criticals are concentrated in text added or rewritten in the iteration-007 RESTORE pass, not in previously-verified-stable sections.
**RPN > 80 count:** 4 of 4 (100%) — exceeds the 30% systemic-quality-issues threshold per protocol Step 3 Decision Point. Read in context: this reflects the narrow, targeted scope of this execution (decomposing only the 4 newest mechanisms, per the Summary), not a re-scan of the whole package; the 6 previously-closed Criticals were not re-litigated.

---

## Finding Details

### FM-001-i008fmea: Segment-Index-overflow exemption contradicts the rule file's own Scope-limits disclosure

| Attribute | Value |
|-----------|-------|
| **Element** | E5 Segment Index / E8 Governance |
| **Severity** | Critical (RPN 294 = S7 × O6 × D7) |

**Evidence:** Design doc, `feedback-decision-log-convention-design.md:264` ("One shared dependency" paragraph, this round's DA-001 fix): "**Five** safety functions — staleness review, graduation proposal, Backfill-Queue review, this install-stall re-assessment, **and the Segment-Index-overflow re-assessment (L1.4)** — all fire at the **same** commit-cadence checkpoint... The Segment-Index-overflow trigger is **explicitly exempt** from the Q3-style dated-worktracker forcing function (DA-001): unlike capture, **its failure is detected by lint 2's contiguity/orphan check** and is fully recoverable by re-reading segment headings, so it needs no owned review date."

Compare the rule file's own Scope-limits disclosure, `feedback-decision-logs-standards.md:85`, item (e): "**Segment Index display accuracy** — the displayed `id-range` per row is **not checked** against the segment's true first/last heading (lint 2 derives contiguity from headings directly), so a stale index row can sit undetected (PM-003-i6)."

The specific trigger the design doc claims lint 2 "detects" is defined at `feedback-decision-log-convention-design.md:199` (L1.4, Segment index row): "**Re-assessment trigger:** if one ACTIVE segment's index+queue overhead ever exceeds ~100 lines, revisit at the same commit-cadence checkpoint... fallback is to move the Segment Index to its own `*-INDEX.md` sidecar." Lint 2's actual scope (`feedback-decision-logs-standards.md:82`) is "ids unique, strictly increasing, and contiguous... flags any on-disk segment absent from the Segment Index (orphan)" — a check on **id sequence integrity**, not on the **line-count of the index table itself**.

**Analysis:** These are two unrelated failure modes conflated by one sentence. Lint 2 verifies id contiguity and orphaned segment files; it contains no logic that measures or bounds the Segment Index table's own size. The rule file's own Scope-limits block (item e) says exactly this — the index's displayed content (which includes its own line-count/size implicitly) is **not** checked by any of the three lints. So the design doc's justification for exempting the Segment-Index-overflow trigger from a dated-tracking-item forcing function (the same treatment Q3 got) rests on a detection mechanism that the package's own rule file explicitly disclaims two files away. This is the identical failure class this exact restore round fixed elsewhere in the same paragraph's sibling finding (PM-001/IN-001: deleting the false "AE-006e is a cap-crossing backstop" claim) — a false claim that an existing automated check covers a residual risk, undermining the "honest metadata" pillar the whole package's 8 rounds of remediation have been converging toward. Unlike the overflow scenario itself (bounded — the design's own text says "no entry is lost, only the per-segment count drifts down"), this is not a data-loss risk; it is a live, present, and provable internal-consistency defect in text that shipped **this round**, so it has not yet been through a dedicated tournament pass.

**Corrective Action:** Wording-only, no new machinery. Either (a) delete the "its failure is detected by lint 2's contiguity/orphan check" clause and replace with the accurate rationale ("a missed re-assessment causes no data loss — segments merely seal earlier as the index nets against entry capacity, L1.4 — so no dated forcing function is needed, unlike Q3"), or (b) if a real backstop is intended, name the correct one (there is none currently — this would require disclosing the gap honestly, per the pattern already used for PM-001/IN-001 two paragraphs earlier in the same file).

**Acceptance Criteria:** The design doc's "One shared dependency" paragraph and the rule file's Scope-limits item (e) state the same fact about lint 2's actual coverage; no sentence in the package claims lint 2 detects Segment-Index-overflow.

**Post-Correction RPN estimate:** Detection drops to 3 once the claim is corrected to match the rule file's own disclosure → RPN ≈ 7 × 6 × 3 = 126 (Major residual — the underlying "no forcing function for this trigger" gap remains, but honestly disclosed rather than falsely backstopped).

---

### FM-002-i008fmea: Inline-doc dedup key is unspecified and has zero worked examples in the package

| Attribute | Value |
|-----------|-------|
| **Element** | E2 Entry creation (inline-doc) / E10 Appendix |
| **Severity** | Critical (RPN 294 = S7 × O6 × D7) |

**Evidence:** The dedup key is specified identically (and identically vaguely) in three places: design doc `feedback-decision-log-convention-design.md:61` — "for `inline-doc`, append the annotation's `path:line/anchor`"; rule file `feedback-decision-logs-standards.md:51` — "Before minting, check for an existing entry carrying the same `source: inline-doc` `path:line/anchor` — if one exists, do not re-mint"; template `FEEDBACK-LOG.template.md:25` — "it checks for an existing entry with the same `source: inline-doc` path/anchor." None of the three defines whether the recorded key is a raw line number, a markdown heading anchor, or a concatenation of both — nor whether the key is stable if the document is edited between two harvests of the same marker (a line-number-based key shifts if lines are inserted above the marker; a heading-anchor-based key would not, but nothing states which is used).

Checked `examples-appendix.md` end to end (the package's designated home for every worked example per FU.8): both FEEDBACK-LOG worked examples (Example 1 "commit-push-cadence", Example 2 "log-growth-capped-collection") use `source: chat`, not `inline-doc`. The "Common cases" section (`examples-appendix.md:169`) restates the rule in prose ("The assistant checks for an existing entry carrying the same `source: inline-doc` path/anchor before minting") but shows **no concrete key value** — no line like `source: inline-doc research/foo.md:42` or `source: inline-doc research/foo.md#pricing-section` appears anywhere in the 6 reviewed files.

**Analysis:** FM-001-i6 (the tournament's single highest-RPN historical Critical, RPN 336, iteration-006) was "no dedup path for repeated inline-doc marker harvest." Its closure (this restore round) added the check-before-mint instruction quoted above — but the instruction names a compound key (`path:line/anchor`) that is never disambiguated and never demonstrated. A dedup check whose own key format is undefined cannot be verified for correctness by a reader, and is likely to be computed inconsistently across sessions or models (one session recording a raw line number, another a heading anchor, another both) — in which case two harvests of the *same, unedited* marker could still fail to match and silently re-mint a duplicate, reproducing the exact failure FM-001-i6 was raised to close. This is compounded by the package's own explicit doctrine (FU.8, "schema alone is not rationalizable → embedded worked examples in each template + an `examples-appendix.md`") — a doctrine applied to every other mechanism in the package (ids/aliases, both log types, segment rotation, evidence-link formats) but, checked directly, not to this one, despite it being the highest-stakes mechanism added this round.

**Corrective Action:** Wording + one example, no new field/lint/machinery. (a) Pick one canonical key form (recommend: `path` + the nearest preceding stable heading anchor, not a raw line number, since headings survive line-number drift from unrelated edits) and state it once, consistently, in the rule file (`feedback-decision-logs-standards.md:51`) and propagate to the design doc and template. (b) Add one worked example to `examples-appendix.md`'s "Common cases" section showing an actual inline-doc-sourced Context line with the chosen key form, e.g. `Context: ... source inline-doc research/foo.md#pricing-section`.

**Acceptance Criteria:** All three specification sites (design doc, rule file, template) state the identical key form; `examples-appendix.md` contains at least one concrete inline-doc Context-line example.

**Post-Correction RPN estimate:** Occurrence drops to 3 once the key form is fixed and demonstrated (removing the cross-session/cross-model computation drift) → RPN ≈ 7 × 3 × 5 = 105 (Major residual — line-number-based keys, if chosen, would still be edit-sensitive; anchor-based keys close this fully).

---

### FM-004-i008fmea: Redaction mechanism has no worked example

| Attribute | Value |
|-----------|-------|
| **Element** | E7 Redaction / E10 Appendix |
| **Severity** | Major (RPN 144 = S4 × O6 × D6) |

**Evidence:** The redaction carve-out is this restore round's other Critical closure (RT-001) and is described at length in prose: design doc `feedback-decision-log-convention-design.md:65` (a single paragraph running to several hundred words covering the category+size note, the "presence not veracity" scrutiny discipline, irreversibility, and the git-history caveat) and rule file `feedback-decision-logs-standards.md:24` (LOG-M-002 exception clause, similarly dense). `examples-appendix.md` was checked end to end (see [FM-002](#fm-002-i008fmea-inline-doc-dedup-key-is-unspecified-and-has-zero-worked-examples-in-the-package) for the section list) — no section shows a redacted entry, a `‹redacted: {what}›` marker, or a category+size note in context.

**Analysis:** This is the same evidence-quality gap as FM-002, applied to a different mechanism. The redaction carve-out is arguably the single most safety-critical SHOULD-tier rule in the package (it is the public-repo-hygiene backstop for secrets/PII, explicitly a "presence, not veracity" discipline the design compares to lint 3 and the `(backfilled)` tag) — yet, unlike lint 3's terminal-evidence check (which has worked examples at `examples-appendix.md:150`) and the `(backfilled)` tag (demonstrated via the Backfill Queue mechanics), the redaction marker itself is never shown in a worked context. Without a concrete example of what a compliant `‹redacted: credential, ~40 chars›`-style entry actually looks like inline in a Verbatim block, an implementer has to reconstruct the format purely from prose, increasing the chance of inconsistent application (e.g., omitting the category, omitting the size, or malforming the marker such that it is not visually distinguishable from an unredacted verbatim).

**Corrective Action:** Wording + one example, no new machinery. Add one short worked example to `examples-appendix.md` (e.g., a genericized Verbatim block showing `‹redacted: credential, ~40 chars›` inline, with the accompanying category+size note as it would actually render).

**Acceptance Criteria:** `examples-appendix.md` contains at least one worked redaction example, consistent with the FU.8 doctrine already applied to every other mechanism in the package.

**Post-Correction RPN estimate:** Occurrence drops to 3 once a concrete example exists → RPN ≈ 4 × 3 × 5 = 60 (Minor residual).

---

### FM-003-i008fmea: New FU.10 diagram omits the dedup gate and the reopen path

| Attribute | Value |
|-----------|-------|
| **Element** | E6 Entry-lifecycle visual layer |
| **Severity** | Major (RPN 108 = S6 × O3 × D6) |

**Evidence:** `feedback-decision-logs-standards.md:36-48` (the new FU.10 `stateDiagram-v2`, added this restore round per `restore-notes.md` Step 2b, explicitly for "the shipped rule the runtime LLM consults — 'for yourself'"): the diagram transitions `Captured --> Logged: mint canonical FU.N + record (alias)` directly, and shows `DONE --> [*]` / `WONTFIX --> [*]` as unconditional terminal transitions. Three lines below the diagram (`:51`), the very same section states the check-before-mint dedup gate ("Before minting, check for an existing entry carrying the same `source: inline-doc` `path:line/anchor` — if one exists, do not re-mint"), and two lines further (`:53`) states the reopen mechanic ("to fix a verbatim or reopen a `DONE`, add a follow-up entry referencing the old id; mark the old entry `Superseded by: FU.N`").

**Analysis:** `restore-notes.md` Step 2 states the two new diagrams are "presentations of existing rules — zero new lint/file/field/subsystem" and specifically that the rule-file diagram is placed there because it is "the shipped rule the runtime LLM consults." A diagram positioned as the compact, at-a-glance take-away for exactly the audience (the model itself) most likely to rely on it under context pressure omits the one gate (dedup-before-mint) that closed the tournament's highest-RPN historical Critical, and depicts terminal states with no visual branch back into the lifecycle for the reopen path the adjacent prose describes. Read charitably, `DONE --> [*]` is defensible as "this entry's own lifecycle ends here; a reopen mints a new entry" (consistent with the append-only design) — but the diagram does not say so, and nothing marks it as a deliberately simplified per-entry view rather than a complete process map. Severity is moderate (not Critical) because the diagram sits directly above, not instead of, the prose that covers both gaps — a reader who continues past the diagram will see the missing steps within three lines.

**Corrective Action:** Wording/diagram-only, no new machinery. Either (a) add one dashed/annotated branch or a one-line caption under the diagram noting "dedup check precedes Logged for inline-doc entries; see below" and "DONE/WONTFIX end this entry's lifecycle — reopening mints a new entry (see Corrections, below)", or (b) leave the diagram as-is but add an explicit one-line caption stating it is a simplified per-entry view, not the full process.

**Acceptance Criteria:** The diagram or its caption discloses that it is a simplified per-entry view and does not depict the dedup gate or the cross-entry reopen mechanic, so a reader (including the model consulting it "for yourself") is not misled into thinking the diagram is exhaustive.

**Post-Correction RPN estimate:** RPN ≈ 6 × 4 × 2 = 48 (Minor residual, once captioned).

---

## Recommendations

Grouped by severity, highest RPN first. All corrective actions are wording/example-level edits to existing artifacts — none add a new file, lint check, field, or subsystem, consistent with the package's established anti-bloat remediation pattern.

**Critical (fix before ratification):**
1. **FM-001-i008fmea** — Correct or delete the "lint 2 detects Segment-Index-overflow" claim in the design doc's "One shared dependency" paragraph so it matches the rule file's own Scope-limits item (e). Est. RPN reduction: 294 → ~126.
2. **FM-002-i008fmea** — Fix the inline-doc dedup key to one canonical, edit-stable form (anchor-based, not raw line number) and add one worked example to `examples-appendix.md`. Est. RPN reduction: 294 → ~105.

**Major (recommended before ratification, not blocking):**
3. **FM-004-i008fmea** — Add one worked redaction example to `examples-appendix.md`. Est. RPN reduction: 144 → ~60.
4. **FM-003-i008fmea** — Add a one-line caption to the new FU.10 rule-file diagram disclosing it is a simplified per-entry view. Est. RPN reduction: 108 → ~48.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-003: the new visual layer, positioned as the compact take-away for the runtime model, omits the dedup gate and the reopen mechanic it sits directly beside. |
| Internal Consistency | 0.20 | Negative | FM-001: a direct, provable contradiction between the design doc's governance section and the rule file's own Scope-limits disclosure — the same defect class this exact restore round fixed elsewhere (PM-001/IN-001), recurring in the fix that closed a different Critical (DA-001) in the same paragraph. |
| Methodological Rigor | 0.20 | Neutral | No new methodology gaps found; the package's 5-lint-scope-limits disclosure discipline and rotation/parity procedures remain intact and were not the target of this pass. |
| Evidence Quality | 0.15 | Negative | FM-002 and FM-004 both show a mechanism described only in dense prose, never demonstrated — for FM-002, specifically the mechanism that closed the tournament's single highest-RPN historical Critical. |
| Actionability | 0.15 | Positive | All four findings have concrete, anti-bloat-compliant, wording/example-only corrective actions with estimated post-correction RPNs; none require new machinery. |
| Traceability | 0.10 | Positive | All four findings cite specific file+line evidence across at least two of the six files and map to a MECE-decomposed lifecycle element. |

---

*Template: `s-012-fmea.md` v1.0.0 | Execution: iteration-008, VERIFIED-CRITICALS blind protocol (S-012 only; no other iteration-007/008 adversary files read except `iteration-007/restore-notes.md`, explicitly disclosed as the owner's public disposition record) | P-003: no subagents invoked | P-020: draft-only, no framework-path writes, no edits to the deliverable | P-022: all findings cite file+line evidence from the current (post-restore) deliverable text; no finding re-derives a residual the deliverable itself discloses as accepted.*
