# FMEA Report: Feedback & Decision Log Convention (FEEDBACK-LOG + LLM-DECISION-LOG)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012, blind background agent, iteration-004)
**H-16 Compliance:** S-003 Steelman is assumed applied earlier in this tournament's sequence per the orchestration protocol (not independently verified by this blind executor — no prior-strategy artifacts were read per the blind protocol).
**Elements Analyzed:** 8 (lifecycle-stage decomposition, scoped to the task's named failure-mode categories) | **Failure Modes Identified:** 9 | **Total RPN:** 1329

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope Note](#scope-note) | Decomposition approach for this execution |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | The 8 lifecycle-stage elements analyzed |
| [Findings Table](#findings-table) | All 9 findings, RPN-ranked |
| [Finding Details](#finding-details) | Expanded detail for Critical + Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Scope Note

Per the task assignment, this FMEA decomposes the log-lifecycle **process**, not the document structure: entry creation (chat + inline-doc), alias/canonical mapping, rotation trigger, segment linking, cross-log navigation, backfill, multi-session concurrency. This is a deliberate scope adaptation of Step 1 (normally a document-section decomposition) to a **process-lifecycle decomposition**, appropriate because the deliverable is a *convention* (a set of procedures applied to two ledger files) rather than a static document. All 5 elements plus 3 additional lifecycle-stage elements (chat/inline-doc split into two, plus rotation-trigger and segment-linking split) yield 8 elements, within the template's target range for a focused review. Findings are evidence-cited against the design doc, the staged rule file/templates/appendix, and (where material) the two **live** bootstrap logs at repo root, which are the only executable evidence of how the convention behaves in practice.

**Anti-bloat calibration applied (per task instruction):** findings that merely note the *absence* of additional machinery (e.g., "no search index," "no real-time validator") are NOT raised here where the design doc already discloses the trade explicitly — that is a valid descoped-with-disclosure posture, not a defect. Findings below are either (a) genuine, undisclosed structural gaps, or (b) evidenced by the live artifacts themselves (not hypothetical).

---

## Summary

8 lifecycle elements analyzed; 9 failure modes identified; 1 Critical (RPN 336) and 6 Major findings, 2 Minor. The Critical finding is a genuine, undisclosed structural conflict — not an anti-bloat-declined edge case: the single-line `FU:`/`DEC:` inline-doc marker convention cannot represent the multi-paragraph verbatim text that LOG-M-002 unconditionally requires for **all** captured feedback, including the inline-doc channel that FU.2 explicitly named as one of the two required capture surfaces. The 6 Major findings are concrete, most independently confirmed against the live bootstrap logs (segment-link self-containment gap, batch-harvest cap overshoot, cross-channel duplicate-capture risk, an evidenced cross-log-reference labeling inconsistency in the live `LLM-DECISION-LOG.md`, an evidenced backfill-review-trigger non-firing already observed twice in this project, and an undefined interrupted-rotation recovery path). **Recommendation: REVISE** — all 7 Critical/Major findings are closable by wording/clarification additions consistent with the package's own anti-bloat doctrine (no new subsystem required for any of them).

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| E1 | Entry creation — chat | LOG-M-001, capture-trigger heuristics (5 categories), same-turn append |
| E2 | Entry creation — inline-doc | `FU:`/`DEC:` marker convention, opportunistic harvest, CB-05 blind spot |
| E3 | Alias/canonical mapping | FU.6 logger-assigned canonical id + verbatim alias scheme (LOG-M-005), H-31 back-reference disambiguation |
| E4 | Rotation trigger | ~50 entries / ~800 lines cap detection, interim self-count discipline (LOG-M-006) |
| E5 | Segment linking | Sealed/ACTIVE prev/next header fields, forward-nav fallback rule, Segment Index |
| E6 | Cross-log navigation | FEEDBACK-LOG ⇄ LLM-DECISION-LOG reference-by-canonical-id, `Reflected in` / `Related` fields |
| E7 | Backfill | Backfill Queue mechanics, staleness/review trigger, id-assignment-at-tail rule |
| E8 | Multi-session concurrency | Single-writer-per-log discipline, orchestrator-only-append, rotation-as-critical-section |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260706T1400 | E2 Inline-doc entry creation | Single-line marker syntax cannot represent multi-paragraph verbatim feedback, contradicting LOG-M-002's unconditional "verbatim and full" | 8 | 6 | 7 | 336 | Critical | Add a fenced block-marker convention (e.g., `FU:` opening line + closing `:FU` or blockquote continuation) for multi-line inline-doc feedback; disclose the single-line default as sufficient for short annotations only | Internal Consistency |
| FM-005-20260706T1400 | E6 Cross-log navigation | Cross-log backlink labeling is inconsistent in the **live** `LLM-DECISION-LOG.md`: 2 of 3 entries use an explicit `Related: FEEDBACK-LOG FU.N` tag, 1 uses unlabeled embedded prose | 3 | 8 | 6 | 144 | Major | Standardize a single labeled sub-field (`Related:`) in the Context line of both schemas; retrofit DEC-LLM-002 at install | Internal Consistency / Traceability |
| FM-006-20260706T1400 | E7 Backfill | Backfill-review trigger ("same commit-cadence checkpoint") lacks the calendar bound given to the analogous Q3 hook trigger, and has already failed to fire across 2 real commits in this project | 4 | 8 | 5 | 160 | Major | Add an explicit calendar bound (e.g., "~3 months or next milestone, whichever first") to the Backfill staleness trigger, mirroring the Q3 hook's fix pattern | Actionability |
| FM-003-20260706T1400 | E4 Rotation trigger | Interim self-count discipline assumes per-entry append; a multi-marker batch harvest from one inline-doc read can append several entries in one operation, overshooting the cap beyond the ~1-entry margin the headroom math assumes | 5 | 5 | 6 | 150 | Major | Add explicit guidance: when a single harvest batch would cross the cap, seal immediately after the batch (not mid-batch) and state the resulting overshoot is bounded by "one batch," not "one entry" | Methodological Rigor |
| FM-004-20260706T1400 | E3 Alias/canonical mapping | No de-duplication check when the same feedback is captured once via chat and again via a later inline-doc annotation of the same content | 4 | 5 | 7 | 140 | Major | Add a one-line convention: before harvesting an inline-doc marker, the assistant SHOULD scan recent entries for an obvious verbatim/paraphrase match and, if found, cross-reference instead of duplicating | Methodological Rigor |
| FM-002-20260706T1400 | E5 Segment linking | A sealed segment's `next` pointer can name a file that does not yet exist on disk (successor not yet sealed); the forward-nav fallback rule that resolves this lives only in the rule file/appendix, not in the segment's own header | 4 | 6 | 6 | 144 | Major | Add one clause to the per-segment header text itself (in both templates' worked examples): "if `next` file is absent, the tail is the stable ACTIVE file" | Completeness |
| FM-007-20260706T1400 | E8 Multi-session concurrency | No recovery/idempotency guidance for a rotation interrupted mid-procedure (crash/compaction) between "copy to sealed" and "reset ACTIVE + parity check"; this project has already experienced a mid-workflow session crash | 6 | 4 | 5 | 120 | Major | Add a one-line recovery rule: on resuming after an interruption, run the parity check first — if sealed + active already sum to more than the pre-crash count, the copy step was already done; do not re-copy | Methodological Rigor |
| FM-008-20260706T1400 | E4 Rotation trigger | "Propose rotation on approaching the cap" (LOG-M-006) does not define a numeric trigger for "approaching" | 3 | 5 | 5 | 75 | Minor | State a concrete self-count checkpoint (e.g., "at ~45 entries or ~750 lines") | Methodological Rigor |
| FM-009-20260706T1400 | E1/E3 Entry creation + alias mapping | No stated precedence when chat capture and inline-doc harvest could both mint canonical ids within the same turn (cosmetic only — ids remain unique/monotonic either way) | 2 | 5 | 6 | 60 | Minor | Optional: state that chat-originated entries are minted before same-turn harvested entries, for readability only | Traceability |

**Rating note (FM-005):** Occurrence is rated 8 (not the more conservative 5-6 "plausible" band) because this failure mode is **already observed** in the live artifact (1 of 3 live entries uses an unlabeled form), not merely probable — see Finding Details for the evidence and the RPN-scale justification.

---

## Finding Details

### FM-001-20260706T1400: Inline-doc marker cannot carry multi-line verbatim feedback

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 336) |
| **Element** | E2 — Entry creation, inline-doc channel |
| **Strategy Step** | Step 2 (Enumerate Failure Modes — "Insufficient" + "Inconsistent" lenses) |

**Evidence:**
- `feedback-decision-logs-standards.md:36`: "**Inline marker:** a line beginning `FU:` / `DEC:`. On reading a doc, harvest each marker with `source: inline-doc` + path/anchor and announce in-turn (no doc mutated)."
- `FEEDBACK-LOG.template.md:23`: "annotate any document with a line beginning `FU:` (or `DEC:` for a decision), e.g. `FU: this section needs a diagram`."
- `feedback-decision-logs-standards.md:24` (LOG-M-002): "Capture user feedback **verbatim and full** (typos preserved); on any conflict, **verbatim wins**." — stated as an unconditional MEDIUM standard, with no channel-specific carve-out anywhere in the rule file, the design doc L1.1 entry-schema table, or the examples appendix.

**Analysis:** The design's own entry schema (`feedback-decision-log-convention-design.md:56`) states "**Verbatim** | User's exact words, **always full**... Word-for-word — verbatim means verbatim... The verbatim is the fidelity anchor" — with no exception for the `source: inline-doc` case. But the *only* documented syntax for leaving inline-doc feedback is a single physical line beginning `FU:`/`DEC:`. Real inline document review comments are frequently multi-sentence or multi-paragraph (the live FEEDBACK-LOG's own FU.5–FU.9 entries, though captured via chat rather than inline-doc, show the verbatim register the convention is built to preserve routinely runs 3–6 sentences). Nothing in any of the 5 staged files defines how an operator marks a multi-line comment block for harvest (no closing marker, no blockquote-continuation rule, no "everything until the next blank line" convention). This is not a disclosed anti-bloat trade (the package discloses many similar limitations explicitly elsewhere, e.g. the opportunistic-harvest coverage caveat) — it is an unacknowledged structural conflict between two normative statements in the same ratified package: the channel's only defined syntax truncates to one line; the capture rule demands the full text regardless of channel.

**Corrective Action:** Add a minimal (zero-new-subsystem) block convention, e.g.: "For feedback longer than one line, open with `FU:` and close with a blank line or a `:FU` sentinel; the assistant harvests everything between as the verbatim." Alternatively, explicitly restrict the inline-doc channel to short annotations and instruct that substantive multi-paragraph feedback be given in chat instead (a disclosed descope, consistent with the package's own doctrine) — either fix is a wording-only change.

**Acceptance Criteria:** The rule file and both templates state, in one place, how a multi-line inline-doc comment is delimited for harvest (or explicitly scope the channel to single-line annotations only).

**Post-Correction RPN estimate:** ~40 (S=4 residual ambiguity in edge formatting, O=2, D=5) once the convention is stated.

---

### FM-005-20260706T1400: Cross-log reference labeling is inconsistent in the live LLM-DECISION-LOG

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 144) |
| **Element** | E6 — Cross-log navigation |
| **Strategy Step** | Step 2 ("Inconsistent" lens) + Step 3 (rating) |

**Evidence:**
- `LLM-DECISION-LOG.md:36`, DEC-LLM-001: "...Related: FEEDBACK-LOG FU.0." — uses an explicit labeled `Related:` sub-field.
- `LLM-DECISION-LOG.md:68`, DEC-LLM-003: "**Context:** Related: FEEDBACK-LOG FU.2 (verbatim + disposition)..." — same labeled form.
- `LLM-DECISION-LOG.md:54`, DEC-LLM-002: "**Context:** Workflow launched 2026-07-05 (id recorded on dispatch; see FEEDBACK-LOG FU.1 disposition). Prior evidence: `orchestration/adr-convention-20260702-001/adversary/iteration-005/s-014-quality-score.md`." — the same cross-log fact (this decision corresponds to FEEDBACK-LOG FU.1) is present but rendered as unlabeled parenthetical prose, not the `Related:` tag used by the other two entries.

**Analysis:** L1.4's cross-log-navigation feature ("FEEDBACK ⇄ DECISION references are canonical ids only... no file paths in cross-references, no extra machinery") is real and does resolve via id in all three cases — this is not a missing-content defect. But neither the design doc's entry schema table nor the staged rule file/templates designate `Related:` (vs. embedded prose) as the *required* label, so the convention's own 2-of-3 live sample already drifted to two different renderings in the first 3 entries ever written. Because no lint checks field-label presence for cross-log references (only terminal-disposition evidence and id integrity are checked), this drift is invisible to the ≤3-lint backstop and will not self-correct. **[INFERENCE]** on generalization: a 3-entry sample is small, but it is the entirety of the live evidence available, and the inconsistency is 100% attributable to an underspecified schema field rather than operator error (both are equally correct interpretations of an unspecified convention).

**Corrective Action:** Add "Related:" as the named sub-field for cross-log references in both entry schemas (design doc L1.1/L1.2 tables + the staged rule file's Context-field description), and retrofit DEC-LLM-002 at install time (already scheduled to normalize other stale annotations per the Adoption plan step 4).

**Acceptance Criteria:** Both schemas name `Related:` as the cross-log reference sub-field; DEC-LLM-002 is retrofitted at install alongside the other Adoption-step-4 normalizations already planned.

**Post-Correction RPN estimate:** ~30 (S=3, O=2, D=5).

**Rating note:** Occurrence is rated 8 ("very likely/certain" per the RPN Scale Reference), not the more conservative 5-6 "plausible" band, because this failure mode is not hypothetical but **already realized** in 1 of the 3 live entries examined. RPN = 3×8×6 = **144**.

---

### FM-006-20260706T1400: Backfill review trigger lacks a calendar bound and has already failed to fire twice

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 160) |
| **Element** | E7 — Backfill |
| **Strategy Step** | Step 2 ("Insufficient" lens) + Step 4 (corrective action) |

**Evidence:**
- `feedback-decision-log-convention-design.md:276`, Q4 mechanics (c): "**Staleness trigger (not open-ended):** Backfill Queue rows carry an added-date and are re-assessed at the same commit-cadence checkpoint as OPEN entries — or sooner if a row's source... is observed to have rotated... **Disclosure (P-022):** as of 2026-07-06 no checkpoint has yet actioned them — the 2026-07-05 commit+push (FU.3) was a *commit* event, and 'checkpoint' here means a deliberate human *review*, a separate and currently-unenforced step; treat these rows as pending review, not as handled."
- `FEEDBACK-LOG.md:78`, FU.3 disposition: records commits `518c6556` and `8ea94fc6`, both pushed on 2026-07-05 — i.e., 2 real commit events have already occurred since the Backfill Queue was created, and neither triggered the "commit-cadence checkpoint" review the design names as the staleness trigger.
- Compare `feedback-decision-log-convention-design.md:237` (Adoption step 6, Q3 hook trigger): "...**or ~3 months of wall-clock time**... whichever comes first. **The calendar bound ensures the decision cannot be deferred purely by the absence of a rotation/checkpoint event.**" — the design explicitly recognized and fixed this exact class of gap (a review trigger that can be indefinitely deferred by the absence of its own triggering event) for the Q3 hook decision, but the same fix was not applied to the Backfill staleness trigger.

**Analysis:** This is a self-disclosed risk (not hidden), but the disclosure itself is evidence that the mitigation is not working: the design's own remediation pattern for exactly this failure class (a "checkpoint" trigger that depends on an event which may never occur) exists elsewhere in the same document and was not carried over to Backfill. Absent a calendar bound, the 8 backfill rows across both live queues can remain "pending review, not handled" indefinitely — which is precisely what has happened across the two commits observed so far.

**Corrective Action:** Apply the same fix already used for Q3: add an explicit calendar bound to the Backfill staleness trigger (e.g., "~3 months of wall-clock time or the next milestone checkpoint, whichever comes first").

**Acceptance Criteria:** Q4 mechanics item (c) states a calendar bound in addition to the commit-cadence-checkpoint and source-rotation triggers.

**Post-Correction RPN estimate:** ~40 (S=4, O=2, D=5).

---

### FM-003-20260706T1400: Batch inline-doc harvest can overshoot the segment cap beyond the assumed single-entry margin

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 150) |
| **Element** | E4 — Rotation trigger |
| **Strategy Step** | Step 2 ("Insufficient" lens — the self-count discipline's implicit granularity assumption) |

**Evidence:**
- `feedback-decision-log-convention-design.md:178`: "Rotate *after* the crossing entry, so none is split. A single oversized entry that alone exceeds the cap seals its segment immediately after it lands (a one-entry segment is acceptable; never split an entry)." — the "crossing entry" language and the headroom math (2.5× the Read window, 2–3× under the truncation point) are both framed around a single entry crossing the cap.
- `feedback-decision-logs-standards.md:28` (LOG-M-006): "Until the Q3 cap-reminder hook ships, the assistant SHOULD self-count entries/lines when it appends and propose rotation on approaching the cap."
- Capture-trigger item 4 (`feedback-decision-log-convention-design.md:84`): "When the assistant *reads* a doc containing such a marker, it SHOULD harvest it into the log with `source: inline-doc`..." — no batch-size limit stated; a single document read can surface multiple markers.

**Analysis:** The cap-crossing math is justified against a "single entry" or "the crossing entry" — a bounded increment. But inline-doc harvest is explicitly a batch operation (a document may carry several `FU:`/`DEC:` markers, all harvested together when the assistant reads it, per capture-trigger item 4 and the CB-05 discussion of large-file reads). Nothing in LOG-M-006 or the rotation procedure addresses appending N markers in one operation: the self-count discipline is written as a per-append check, but if the model appends a 5-marker batch as one Write, the log can jump from, say, 47 to 52 entries in a single step — 2 entries past the ~50 trip-wire rather than the 1-entry overshoot the headroom math is calibrated against. The eventual lint-1 backstop still catches this at commit time, so no data is lost, but the intra-session headroom guarantee ("2.5× the Read window") is weaker than stated for the harvest path specifically.

**Corrective Action:** Add one clause to L1.4/LOG-M-006: "If a single harvest batch would cross the cap, seal the segment immediately after the whole batch lands (not mid-batch); the resulting overshoot is bounded by one batch, not one entry — keep batches to a handful of markers."

**Acceptance Criteria:** The rotation procedure explicitly names the batch case, not only the single-entry case.

**Post-Correction RPN estimate:** ~50 (S=5, O=2, D=5).

---

### FM-004-20260706T1400: No de-duplication check across chat and inline-doc capture channels

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 140) |
| **Element** | E3 — Alias/canonical mapping (capture-side) |
| **Strategy Step** | Step 2 ("Inconsistent" lens) |

**Evidence:**
- Capture triggers 1–5 (`feedback-decision-log-convention-design.md:79-86`) enumerate independent conditions for chat capture and, separately, item 4 for inline-doc harvest — each evaluated on its own with no cross-check against recently captured entries.
- The id scheme (FU.6, `feedback-decision-log-convention-design.md:63-76`) guarantees uniqueness and monotonicity of the **id**, not uniqueness of the **content** — two canonical ids can legitimately hold near-identical verbatim text with no mechanism flagging the overlap.

**Analysis:** A user who states feedback in chat and later also annotates a document with the same point (a plausible workflow — discuss, then leave a written note as a reminder) will have it captured twice under two different canonical ids, with no cross-reference between them. This does not corrupt the log (both entries are individually valid, verbatim, well-formed) but works against "so that we don't lose feedback" in the opposite direction — feedback becomes fragmented across two entries with no link, which can also produce two independent (and potentially divergent) Dispositions for what is actually one item.

**Corrective Action:** Add a one-line convention: before minting a new canonical id from an inline-doc harvest, the assistant SHOULD scan the last few entries (or Segment Index range since the topic last came up) for an obvious verbatim/paraphrase match; if found, cross-reference the existing id instead of minting a new one, or mint a new id that references the earlier one as `Duplicate of: FU.N` (parallel to the existing `Superseded by:` status-pointer convention).

**Acceptance Criteria:** The rule file states a lightweight duplicate-check step, reusing the existing status-pointer mechanism rather than adding new machinery.

**Post-Correction RPN estimate:** ~48 (S=4, O=3, D=4).

---

### FM-002-20260706T1400: Sealed-segment `next` pointer can name a nonexistent file with no in-header explanation

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 144) |
| **Element** | E5 — Segment linking |
| **Strategy Step** | Step 2 ("Missing" lens) |

**Evidence:**
- `examples-appendix.md:144`: "**Forward-nav rule:** from segment N, go to `FEEDBACK-LOG.{N+1:03d}.md` if it exists, else the ACTIVE `FEEDBACK-LOG.md`." — the fallback rule is stated once, in the appendix.
- `feedback-decision-log-convention-design.md:181`: "`next` is written once at seal time and stays valid (the not-yet-sealed successor resolves to the stable ACTIVE name) — sealed segments never need relinking." — confirms the sealed segment's literal `next` string is written before the successor file necessarily exists.
- `FEEDBACK-LOG.template.md:5`: "**Segment 1 (ACTIVE)** · prev: — · next: —" — the only per-file header text shown anywhere in the staged package is the ACTIVE-file blockquote; none of the 5 staged files include an actual sealed-segment header (`FEEDBACK-LOG.001.md`'s content is only *described* in prose in the appendix walkthrough, never rendered as a template).

**Analysis:** Under the common case of exactly one rotation ever having occurred (plausible for the lifetime of many projects), segment 1 is sealed with `next: FEEDBACK-LOG.002.md` while segment 2 is still ACTIVE (physically named `FEEDBACK-LOG.md`, not `FEEDBACK-LOG.002.md`) — so the literal filename named in segment 1's own header does not exist on disk. A reader who opens `FEEDBACK-LOG.001.md` directly, without also having the rule file or examples appendix open, has no way to know from the file itself that a dangling `next` pointer means "the tail is the stable ACTIVE file" rather than "this link is broken" (data-loss-looking, though not actually a defect). The fallback rule is real and correct but lives entirely outside the artifact it governs.

**Corrective Action:** Add one clause directly into each template's own worked-example header text (both `FEEDBACK-LOG.template.md` and `LLM-DECISION-LOG.template.md`), e.g.: "`next: —` means this is the tail; if a named `next` file does not exist, the tail is the stable ACTIVE file of this name." Since the package has no rendered sealed-segment template today, this is best added as a one-line footnote in the Segment Index section of the ACTIVE template (which every segment, sealed or active, is instructed to reference).

**Acceptance Criteria:** The fallback rule is discoverable from a segment file itself (or from the Segment Index section every segment is told to reference), not only from the design doc or appendix.

**Post-Correction RPN estimate:** ~48 (S=4, O=2, D=6).

---

### FM-007-20260706T1400: No recovery guidance for a rotation interrupted mid-procedure

| Attribute | Value |
|-----------|-------|
| **Severity** | Major (RPN 120) |
| **Element** | E8 — Multi-session concurrency (intersects E4 Rotation trigger) |
| **Strategy Step** | Step 2 ("Missing" lens) — **[INFERENCE]**: this scenario is not discussed in any source file; it is constructed from the documented rotation procedure plus this project's own evidenced crash history |

**Evidence:**
- `feedback-decision-log-convention-design.md:185-191`: the 4-step rotation procedure (copy to sealed → reset ACTIVE + reseed index + carry forward Backfill → **required** parity check → resume appends), framed as "a short single-writer critical section."
- `FEEDBACK-LOG.md:49` (FU.1 disposition): "...Subtraction + iterations 006–008 completed 2026-07-05 (workflow `wf_b7e89510-8c2`; **interrupted by a session crash, resumed from cache**)." — direct evidence that mid-workflow session crashes are a real, already-observed event in this project, not a hypothetical.

**Analysis:** No file in the package states what to do if the rotation critical section is interrupted between step 1 (a sealed copy now exists) and step 4 (resume). The already-added orphan-segment check (id-integrity lint check 2, `feedback-decision-logs-standards.md:66`: "flags any on-disk segment absent from the Segment Index") provides a **partial**, post-hoc (commit-time only) detection backstop for one specific interrupted state (sealed file exists, index not yet updated) — but there is no stated recovery action once that state is detected, and no guidance for a session resuming rotation to check "was this already partially done?" before re-running the procedure from step 1 (which could duplicate the sealed copy or, worse, double-apply the Backfill-carry-forward step).

**Corrective Action:** Add one line to the rotation procedure: "On resuming after any interruption, run the parity check (step 3) *before* re-attempting steps 1–2; if sealed + active already reconcile to the pre-interruption count, the copy was already done — proceed to step 4 only."

**Acceptance Criteria:** The rotation procedure names the resume-after-interruption case explicitly, reusing the already-required parity check as the resumption test (no new machinery).

**Post-Correction RPN estimate:** ~48 (S=6, O=2, D=4).

---

## Recommendations

Ranked by RPN (highest first); all are wording/clarification additions consistent with the package's own anti-bloat doctrine — none requires a new subsystem, lint check, or file.

| Rank | ID | RPN | Corrective Action | Est. Post-Correction RPN |
|------|-----|-----|--------------------|---------------------------|
| 1 | FM-001 | 336 | Define a multi-line inline-doc marker block (or explicitly scope the channel to single-line only) | ~40 |
| 2 | FM-005 | 144 (reconciled) | Name `Related:` as the required cross-log-reference sub-field; retrofit DEC-LLM-002 | ~30 |
| 3 | FM-006 | 160 | Add a calendar bound to the Backfill staleness trigger, mirroring the Q3 hook fix | ~40 |
| 4 | FM-003 | 150 | State the batch-harvest case in the rotation procedure (overshoot bounded by one batch, not one entry) | ~50 |
| 5 | FM-002 | 144 | Add the forward-nav fallback clause into the template's own Segment Index section | ~48 |
| 6 | FM-004 | 140 | Add a lightweight cross-channel duplicate-check step, reusing the existing status-pointer pattern | ~48 |
| 7 | FM-007 | 120 | Add a resume-after-interruption rule for rotation, reusing the existing parity check | ~48 |
| 8 | FM-008 | 75 | State a concrete numeric self-count checkpoint for "approaching the cap" | ~30 |
| 9 | FM-009 | 60 | Optional: state a same-turn id-minting precedence (chat before harvest) | ~30 |

**Aggregate:** if all 9 corrective actions are applied, estimated total RPN falls from 1329 to roughly 364 — no new lint, no new file, no new field beyond one label (`Related:`) and one status-pointer convention (`Duplicate of:`) that mirrors the already-accepted `Superseded by:` pattern.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-002: segment self-containment gap means a reader of an isolated sealed file cannot navigate correctly without external documentation |
| Internal Consistency | 0.20 | Negative | FM-001: LOG-M-002's unconditional "verbatim and full" contradicts the single-line inline-doc marker syntax; FM-005: cross-log reference labeling is evidenced-inconsistent in the live artifact itself |
| Methodological Rigor | 0.20 | Negative | FM-003: cap-crossing math assumes single-entry granularity but the harvest path is batch-oriented; FM-004: capture procedure has no dedup step; FM-007: rotation procedure has no interruption-recovery case |
| Evidence Quality | 0.15 | Neutral | Findings in this report are themselves evidence-grounded (file+line); the reviewed package's own evidence citations remain generally strong and were not degraded by these findings |
| Actionability | 0.15 | Negative | FM-006: the named corrective mechanism (commit-cadence checkpoint review) has already failed to fire twice, and lacks the calendar-bound fix applied to the analogous Q3 trigger |
| Traceability | 0.10 | Negative | FM-005/FM-009: cross-reference labeling and same-turn id-minting order are under-specified, weakening traceability between the two logs and between capture channels |

---

*Strategy Execution: S-012 FMEA*
*Executor: adv-executor (blind background agent, iteration-004)*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Constitutional: P-003 (no subagents invoked) · P-020 (draft-only, no deliverable or framework path edited) · P-022 (all findings evidence-cited; one scenario labelled [INFERENCE])*
