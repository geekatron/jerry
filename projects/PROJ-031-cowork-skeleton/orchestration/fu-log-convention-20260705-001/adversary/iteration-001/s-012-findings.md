# FMEA Report: Feedback & Decision Log Convention (FEEDBACK-LOG / LLM-DECISION-LOG)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}` (project `PROJ-031-cowork-skeleton`)
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012 FMEA, blind protocol, iteration 1)
**H-16 Compliance:** Not independently verifiable within this execution's blind scope (this agent is barred from reading prior/sibling `adversary/` outputs, including any S-003 Steelman artifact). Orchestrator-asserted per package framing ("Revision (2026-07-05, user review + UX heuristic evaluation)").
**Elements Analyzed:** 14 | **Failure Modes Identified:** 27 | **Total RPN:** 4,435

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Posture Note](#posture-note) | How the minimal/descoped-with-disclosure convention was treated |
| [Element Inventory](#element-inventory) | 14 decomposed elements with source refs |
| [Findings Table](#findings-table) | All 27 findings with S/O/D/RPN/severity |
| [Finding Details — Critical](#finding-details--critical) | Expanded detail for 7 Critical findings |
| [Finding Details — Major](#finding-details--major) | Expanded detail for 12 Major findings |
| [Minor Findings — Evidence](#minor-findings--evidence) | Compact evidence/action for 8 Minor findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

14 elements decomposed across the log lifecycle (creation, aliasing, rotation, linking, cross-navigation, backfill, concurrency, verbatim policy, graduation, scoping, lint, hooks, governance); 27 failure modes identified, 7 Critical (RPN >= 200 or S >= 9), 12 Major, 8 Minor. Highest-RPN finding: **FM-016** (concurrent background-agent writes can silently overwrite/lose an appended entry, RPN 405) — a direct hit against the deliverable's own stated purpose ("so that we don't loose feedback or follow up items," `FEEDBACK-LOG.md:63`). The element with the highest cumulative RPN is **E-13 Hook design** (602), driven by a falsifiable gap: the hook's own keyword-trigger list would have missed FU.9, an entry that is *already captured, verbatim, in the live log being reviewed* (`FEEDBACK-LOG.md:150-153`). **Recommendation: REVISE.** The Critical findings are concentrated in a recurring pattern — **claims of resilience/coverage that are not backed by an enforcement mechanism** (id-collision-proof, rotation-guaranteed, transcript-recoverable, hook-catches-feedback) — rather than in the core schema or MEDIUM-tier posture, which is sound and appropriately minimal. All 7 Critical corrective actions are documentation/disclosure changes or one additional cheap lint check, consistent with the package's own anti-bloat doctrine; none require new subsystems.

## Posture Note

Per instruction, this review does **not** penalize the package for being minimal, for using MEDIUM-tier (SHOULD) rules instead of HARD, for the 3-check lint budget, or for deferring the hook (Q3). Several candidate findings were explicitly discarded as "demands for heavyweight machinery" (e.g., a real-time inline-marker scanning service, NLP-based feedback classification, a distributed lock manager, a status dashboard) because the package's own UX-disposition rebuttals (`orchestration/fu-log-convention-20260705-001/revision-notes.md:89-116`) already correctly reject that class of fix. What *is* flagged below is the narrower, C4-relevant class: places where the deliverable's own prose **asserts a guarantee** ("cannot collide," "full fidelity is preserved," "MUST harvest") that the surrounding mechanism does not actually make true — overclaimed coverage, per the C4 gate instruction, is treated as Critical regardless of package size.

---

## Element Inventory

| ID | Element | Primary Source |
|----|---------|-----------------|
| E-01 | Entry creation — chat capture (LOG-M-001, capture triggers) | design.md:74-81; standards.md:23 |
| E-02 | Entry creation — inline-doc harvesting (`FU:`/`DEC:` marker) | design.md:79; standards.md:36; FEEDBACK-LOG.template.md:23 |
| E-03 | Alias/canonical-id mapping (logger-assigned monotonic ids) | design.md:62-70; standards.md:27 |
| E-04 | Segment rotation trigger (cap ~50 entries/~800 lines) | design.md:157-172; standards.md:46-53 |
| E-05 | Segment linking (prev/next, immutable sealed segments, index) | design.md:163-171; examples-appendix.md:116-142 |
| E-06 | Cross-log navigation (canonical id as join key) | design.md:170; standards.md:53; examples-appendix.md:140 |
| E-07 | Backfill Queue (candidate rows, promotion) | design.md:243 (Q4); FEEDBACK-LOG.template.md:53-59; FEEDBACK-LOG.md:161-170 |
| E-08 | Multi-session / multi-agent concurrency (concurrent writes) | FEEDBACK-LOG.md:63 (FU.2 "background agents"); design.md:70 |
| E-09 | LLM-DECISION-LOG verbatim policy (Q1 excerpt+pointer) | design.md:103-112; LLM-DECISION-LOG.template.md:22-27 |
| E-10 | Boundary/graduation to worktracker `DEC-NNN` / ADR | design.md:114-126; standards.md:26,66-69 |
| E-11 | Scoping rule (`JERRY_PROJECT` set/unset; Q2 `scope:framework`) | design.md:83-87,241; standards.md:57 |
| E-12 | L5 lint enforcement (3 declared checks) | standards.md:59-64; design.md:191-197 |
| E-13 | Hook design (Seams 1-3, Q3 deferred) | hook-design-note.md (whole file); design.md:132-155 |
| E-14 | Governance / install / token-budget posture | design.md:176-211; revision-notes.md:122-124 |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|
| FM-001 | E-01 | No reconciliation/self-check confirming all feedback-signal turns were captured; interim (pre-hook) period is unbounded | 6 | 5 | 7 | 210 | Critical | Completeness |
| FM-002 | E-01 | Capture-trigger keyword list is exact-phrase based; ambiguous casual-vs-loggable boundary | 4 | 5 | 5 | 100 | Major | Completeness |
| FM-003 | E-02 | Inline-doc harvest fires only "when the assistant reads a doc" — no scheduled sweep; coverage gap is undisclosed | 7 | 6 | 8 | 336 | Critical | Completeness |
| FM-004 | E-02 | No de-duplication for a marker re-read/re-harvested across sessions (doc mutation explicitly rejected, revision-notes.md:111) | 5 | 6 | 6 | 180 | Major | Internal Consistency |
| FM-005 | E-02 | Self-referential false-positive risk: template's own syntax example (`FU: this section needs a diagram`, FEEDBACK-LOG.template.md:23) is itself a marker-shaped line | 3 | 3 | 5 | 45 | Minor | Evidence Quality |
| FM-006 | E-03 | Overclaim: "parallel/background agents cannot collide" (design.md:70) asserted with no locking/coordination mechanism for concurrent id-minting | 8 | 6 | 8 | 384 | Critical | Internal Consistency |
| FM-007 | E-03 | No repair procedure when the id-integrity lint detects a collision/gap — conflicts with "immutable once sealed" (design.md:167) | 5 | 4 | 6 | 120 | Major | Methodological Rigor |
| FM-008 | E-04 | Rotation is "documented, not new enforcement" (design.md:172) and Seam 3 explicitly "MUST NOT rotate autonomously" (hook-design-note.md:49); no lint checks the cap itself — the FU.5 truncation failure this subsystem exists to prevent has no detection path | 8 | 5 | 9 | 360 | Critical | Methodological Rigor |
| FM-009 | E-04 | "~800 lines" cap ambiguous — entries-only vs. whole file (header/index/backfill overhead uncounted) | 3 | 4 | 5 | 60 | Minor | Internal Consistency |
| FM-010 | E-05 | "Rebuildable by ls" (design.md:169) understates recovery cost — id-range column needs a grep of every segment, not `ls` | 3 | 4 | 4 | 48 | Minor | Evidence Quality |
| FM-011 | E-05 | "Immutable once sealed" (design.md:167) asserted with no checksum/permission/lint enforcement | 4 | 3 | 6 | 72 | Minor | Methodological Rigor |
| FM-012 | E-06 | Cross-log id resolution asserted "no extra machinery" (design.md:170) but never worked through end-to-end in the appendix (only same-log rotation is, examples-appendix.md:116-142) | 3 | 5 | 5 | 75 | Minor | Traceability |
| FM-013 | E-07 | No spec for the canonical id a promoted backfill row receives relative to its content date (tail-id vs. retroactive-insert) | 5 | 6 | 6 | 180 | Major | Traceability |
| FM-014 | E-07 | Backfill rows carry no Disposition/expiry; Q4 "pending user authorization" has no trigger for when authorization is sought | 4 | 6 | 5 | 120 | Major | Actionability |
| FM-015 | E-07 | Live evidence: a Backfill Queue row already effectively resolved sits undispositioned (`FEEDBACK-LOG.md:167`) | 3 | 7 | 3 | 63 | Minor | Internal Consistency |
| FM-016 | E-08 | No write-serialization/locking for concurrent background-agent appends to the same file — a race can silently overwrite (lose) an entire entry | 9 | 5 | 9 | 405 | Critical | Completeness |
| FM-017 | E-09 | Overclaim: "full fidelity is preserved… byte-exact source of record" (design.md:110) with no cited transcript-retention guarantee or `{session_id}#{uuid}` resolution tooling | 7 | 5 | 9 | 315 | Critical | Methodological Rigor |
| FM-018 | E-09 | "Decision-relevant excerpt" selection has no rubric; compounded by acknowledged per-turn model swaps (design.md:59) | 4 | 5 | 5 | 100 | Major | Internal Consistency |
| FM-019 | E-10 | Graduation trigger ("hardens and attaches to a work item," design.md:126) is undefined judgment, absent from lint; live log already shows a promised-not-executed graduation with no deadline (`LLM-DECISION-LOG.md:66`) | 5 | 6 | 6 | 180 | Major | Actionability |
| FM-020 | E-10 | LOG-M-004 "cross-link, never duplicate" over-states the mechanism — schema itself restates Decision/Summary content (design.md:98) | 2 | 5 | 3 | 30 | Minor | Traceability |
| FM-021 | E-11 | Q2's `scope: framework` tag has no field defined in the fixed 5-field schema; self-referentially, this very feedback is framework-level feedback sitting in a project-scoped log right now | 5 | 7 | 4 | 140 | Major | Completeness |
| FM-022 | E-11 | No defined behavior for `JERRY_PROJECT` changing mid-session (active-project switch) | 4 | 4 | 5 | 80 | Major | Internal Consistency |
| FM-023 | E-12 | Adoption/migration plan (design.md:203-211) has no implementation step for the lint script itself (no CI wiring referenced) — as written, the 3 checks have no path to becoming operative | 5 | 7 | 3 | 105 | Major | Actionability |
| FM-024 | E-13 | Overclaim falsified by the package's own evidence: Seam 2's keyword list (hook-design-note.md:33) would have missed FU.9, an entry already captured verbatim in this log (`FEEDBACK-LOG.md:150-153`) | 7 | 7 | 8 | 392 | Critical | Methodological Rigor |
| FM-025 | E-13 | No fallback for `model_of_last_assistant_turn` resolution on a session's first user turn (no prior assistant record) | 3 | 4 | 5 | 60 | Minor | Evidence Quality |
| FM-026 | E-13 | Q3 defers the hook (and its Seam-2 reconciliation function) with no target date/re-check — interim manual-only period is unbounded | 5 | 6 | 5 | 150 | Major | Actionability |
| FM-027 | E-14 | Token budget "~1,584 tokens" (revision-notes.md:124) measures only the rule file, not the appendix it now depends on or the templates — understates real first-use load, echoing the sibling ADR-convention's own "measure what's convenient" failure (design.md:40) | 5 | 5 | 5 | 125 | Major | Evidence Quality |

**Totals:** Critical = 7 (FM-001, FM-003, FM-006, FM-008, FM-016, FM-017, FM-024) · Major = 12 (FM-002, FM-004, FM-007, FM-013, FM-014, FM-018, FM-019, FM-021, FM-022, FM-023, FM-026, FM-027) · Minor = 8 (FM-005, FM-009, FM-010, FM-011, FM-012, FM-015, FM-020, FM-025)

---

## Finding Details — Critical

### FM-001: No capture reconciliation / unbounded interim period

| Attribute | Value |
|---|---|
| Element | E-01 Entry creation — chat |
| S/O/D | 6 / 5 / 7 = RPN 210 |

**Effect:** LOG-M-001 is SHOULD-tier by construction (HARD ceiling 25/25, `standards.md:23`; design.md:81). The only proposed backstop is the Seam-2 Stop-hook reminder (hook-design-note.md:31-34), which is itself deferred under Q3 ("shipped as a separate gated change," design.md:242) with **no target date or re-check checkpoint**. Until it ships, there is zero mechanism — not even a periodic self-audit — to confirm that every feedback-signal turn in a session was actually logged. A missed item is silent: nothing in the deliverable produces a signal that a turn *should have* been captured and wasn't.

**S/O/D rationale:** S=6 (loses individual feedback items — the stated core purpose — without invalidating the whole log); O=5 (plausible over a long session/project, not certain); D=7 (a silent miss produces no artifact to notice).

**Corrective Action:** Add one sentence to LOG-M-001 (or the templates) explicitly disclosing that until the Q3 hook lands, capture is best-effort only, and recommend an end-of-session self-check ("did I log everything flagged this session?") as a zero-machinery MEDIUM habit — not a new tool.

**Acceptance Criteria:** Standards doc or template states the interim limitation explicitly; a one-line self-check habit is documented.

**Post-Correction RPN estimate:** ~90 (D drops to ~3 once the gap is disclosed and a check habit exists; S/O unchanged since underlying detection remains manual).

---

### FM-003: Inline-doc harvest has no scheduled sweep; gap undisclosed

| Attribute | Value |
|---|---|
| Element | E-02 Entry creation — inline-doc |
| S/O/D | 7 / 6 / 8 = RPN 336 |

**Effect:** "When the assistant *reads* a doc containing such annotations, it MUST harvest them" (design.md:79) is the **only** trigger. If a document carrying an `FU:`/`DEC:` marker (standards.md:36) is never re-opened by an assistant in a future turn, the annotation sits unharvested indefinitely — with no periodic scan, no repo-wide check, and (critically) no disclosure anywhere in the package that coverage is opportunistic rather than guaranteed. This directly targets the deliverable's own stated purpose: inline-doc capture was one of the two channels the user explicitly asked for (FEEDBACK-LOG.md:63, "either in the turn by turn chat or in-line in documentation").

**S/O/D rationale:** S=7 (silently defeats an explicitly-requested capture channel); O=6 (annotated docs not immediately reread are a normal occurrence in multi-file, multi-session project work); D=8 (nothing surfaces the gap — nothing counts unharvested markers).

**Corrective Action:** This does **not** need a scanning service (that would be the machinery the package correctly avoids elsewhere). Add one disclosure sentence to `standards.md` (§FEEDBACK-LOG) stating that inline-doc harvest is opportunistic, bounded to documents the assistant actually reads — and optionally recommend, as a MEDIUM habit (not tooling), a `grep -rn '^FU:\|^DEC:'` sweep at project-open time.

**Acceptance Criteria:** Standards doc explicitly states the opportunistic-coverage limitation; optional grep habit documented as SHOULD, not a required subsystem.

**Post-Correction RPN estimate:** ~144 (D drops to ~4 with the disclosed limitation + habit; underlying O unchanged since the fix is disclosure, not elimination).

---

### FM-006: "Cannot collide" claim has no minting-coordination mechanism

| Attribute | Value |
|---|---|
| Element | E-03 Alias/canonical-id mapping |
| S/O/D | 8 / 6 / 8 = RPN 384 |

**Effect:** design.md:70 states plainly: *"canonical ids are logger-owned, so parallel/background agents cannot collide."* This is the design's headline improvement over `[internal-kb]`'s `DJ-025` collision (Improvement Ledger row 2, design.md:222). But the mechanism for **how** two concurrent background agents — a pattern the user explicitly requested (FEEDBACK-LOG.md:63, "leverage background agents") and the project itself uses (e.g., `wf_dcb52638-593`, "59 agents") — coordinate on the *next* monotonic integer is never specified. A flat append-only markdown file has no lock; two agents reading "last id = FU.9" concurrently can both mint `FU.10` for different feedback, reproducing exactly the collision class the design claims to have eliminated. The only stated detection is the L5 id-integrity lint (standards.md:63) — post-hoc, not preventive, and its own repair path is undefined (see FM-007).

**S/O/D rationale:** S=8 (the specific guarantee the design uses to justify itself over the legacy pattern is broken); O=6 (background-agent concurrency is an explicit, active usage pattern in this very project); D=8 (only caught if/when the lint actually runs, after the fact).

**Corrective Action:** No locking subsystem needed. Soften the claim to accuracy: state that minting is expected to be **serialized through the invoking/orchestrating context** (consistent with the framework's own P-003/H-01 orchestrator-worker topology, where workers return results to a single coordinating context rather than writing files in parallel) and that the id-integrity lint is a **backstop**, not a guarantee. This is a wording fix plus one clarifying sentence, not new machinery.

**Acceptance Criteria:** design.md/standards.md no longer states collision is structurally impossible; documents the serialization assumption and the lint's backstop role.

**Post-Correction RPN estimate:** ~144 (S drops to ~4 once the claim matches the actual, weaker but honest, guarantee).

---

### FM-008: Rotation cap has no enforcement path

| Attribute | Value |
|---|---|
| Element | E-04 Segment rotation trigger |
| S/O/D | 8 / 5 / 9 = RPN 360 |

**Effect:** Rotation is explicitly "documented, not new enforcement" (design.md:172), and the one hook seam that could auto-remind is scoped to never act autonomously ("It MUST NOT rotate autonomously... reminder only, not a rotation engine," hook-design-note.md:49) and is itself Q3-deferred. The 3 declared L5 lint checks (standards.md:61-64: nav table, id integrity, terminal evidence) **do not include a check for "ACTIVE file has exceeded the cap."** Nothing in the shipped package — not lint, not hook, not a periodic check — actually detects or forces the rotation that FU.5 exists to guarantee. An ACTIVE log can silently grow past ~800 lines and reproduce the exact truncation failure (`~25k-token file truncation was observed in this very project — PM-001,` design.md:159) that motivated the entire segment-rotation subsystem.

**S/O/D rationale:** S=8 (recreates the confirmed context-rot defect the mechanism exists to prevent); O=5 (requires sustained heavy usage, plausible for the "long running sessions and/or projects" case FU.5 itself names, FEEDBACK-LOG.md:104); D=9 (no lint, no hook, no reminder — fully silent until someone experiences a truncated read).

**Corrective Action:** Add a 4th lint check of the **same cheap, pure-text class** as the existing 3: "ACTIVE `*-LOG.md` line count / entry count is under the stated cap." This is not scope creep — it completes the mechanism using the exact minimalism doctrine the package already applies to its other 3 checks.

**Acceptance Criteria:** `standards.md` §L5 Lint lists a 4th check for cap-exceeded detection on the ACTIVE file.

**Post-Correction RPN estimate:** ~90 (D drops to ~2 with a lint check; O unchanged since the check is still post-hoc, not preventive, but at least the silent-forever failure mode is closed).

---

### FM-016: No write-serialization for concurrent appends

| Attribute | Value |
|---|---|
| Element | E-08 Multi-session / multi-agent concurrency |
| S/O/D | 9 / 5 / 9 = RPN 405 |

**Effect:** This is the highest-RPN finding in the analysis. FU.2 explicitly asks to "leverage background agents so that we don't burn through the main context window" (FEEDBACK-LOG.md:63); FU.9 explicitly challenges whether background agents were used "to their maximum potential" (FEEDBACK-LOG.md:153). Neither the design doc nor the standards doc describes any write-safety mechanism for the shared flat file: a classic read-modify-write race (agent A reads the file, appends its entry in memory, writes back; agent B does the same concurrently against the pre-A state) can cause B's write to **silently overwrite and permanently lose A's entire entry** — not a duplicate id (FM-006's effect), but total data loss with zero trace. This directly and completely inverts the deliverable's stated reason to exist (`FEEDBACK-LOG.md:63`, "so that we don't loose feedback or follow up items").

**S/O/D rationale:** S=9 (silent total loss of a captured entry — deliverable-invalidating for that entry, and this is the framework's own core purpose); O=5 (requires genuinely concurrent writers touching the same log window, plausible given the project's demonstrated multi-agent orchestration patterns); D=9 (nothing detects a vanished append — the id-integrity lint has nothing to compare a lost entry against).

**Corrective Action:** No distributed-locking system needed. Document the actual safety assumption explicitly: appends to a given log MUST be serialized through a single writing context (the orchestrating/main-thread agent), never issued as parallel raw file writes by multiple concurrently-running background agents. If Jerry's actual runtime already enforces this via its P-003 orchestrator-worker topology (workers return results to the orchestrator rather than writing files themselves), state that explicitly as the mechanism — currently the package is silent on it entirely.

**Acceptance Criteria:** Standards doc states the write-serialization assumption/mechanism in one sentence; the "background agents" framing in the design doc is reconciled with it (background agents *analyze/draft*, the orchestrator *appends*).

**Post-Correction RPN estimate:** ~135 (S drops to ~5 — loss becomes an implementation-discipline risk rather than an architecturally-unaddressed one; O/D roughly unchanged pending actual enforcement).

---

### FM-017: Transcript-recoverability claim has no retention guarantee

| Attribute | Value |
|---|---|
| Element | E-09 LLM-DECISION-LOG verbatim policy |
| S/O/D | 7 / 5 / 9 = RPN 315 |

**Effect:** The entire justification for Option B (excerpt + pointer) over Option A (full paste) rests on one claim: *"full fidelity is preserved (the transcript is the byte-exact source of record)... the full turn always recoverable from the immutable JSONL transcript"* (design.md:110). Nothing in the package cites a transcript-retention policy, an archival guarantee, or a resolution procedure/tool for `{session_id}#{uuid}` (design.md:99). If session transcripts are ever pruned, rotated, or simply not retained indefinitely — a realistic operational possibility for any long-lived framework — the compensating claim silently fails, and the log becomes precisely the lossy record Option B was chosen specifically to avoid. This is the load-bearing assumption behind the whole Q1 ratification (design.md:112) and is not verified anywhere in the reviewed package.

**S/O/D rationale:** S=7 (undermines the entire stated rationale for rejecting full-paste); O=5 (transcript rotation/pruning is a plausible eventual operational reality, not certain); D=9 (silent — only discovered when someone tries to resolve an old pointer and finds the transcript gone).

**Corrective Action:** Add one sentence citing the actual transcript retention behavior (or, if unknown, explicitly flag it as an open assumption/risk in the Q1 proposed-default rather than presenting "full fidelity is preserved" as settled fact). This is a wording/disclosure fix, not new tooling.

**Acceptance Criteria:** Q1 section (design.md) either cites a retention guarantee or is reworded to flag transcript retention as an unverified dependency of Option B.

**Post-Correction RPN estimate:** ~135 (S drops to ~3 once the claim is honestly scoped as conditional; O/D unchanged since retention itself isn't fixed by wording).

---

### FM-024: Hook keyword list is falsified by the package's own captured entry

| Attribute | Value |
|---|---|
| Element | E-13 Hook design |
| S/O/D | 7 / 7 / 8 = RPN 392 |

**Effect:** Seam 2's Stop-hook heuristic fires on "correction/preference/directive keywords: 'no', 'actually', 'instead', 'I want', 'I'd like', 'from now on', 'don't', 'stop'" (hook-design-note.md:33). FU.9 — a real entry already captured verbatim in `FEEDBACK-LOG.md:150-153` — reads: *"Did you leverage any jerry (jerry:*) skills and agents...? Did you ensure that you ran the outputs using the /adversary C4 >=0.95...? How are we ensuring that we're doing a quality job...?"* This is unambiguously feedback (a process-accountability challenge that changed downstream behavior, per its own Summary/Disposition), and it contains **none** of the listed trigger terms. This is not a hypothetical edge case — it is a demonstrated miss against the deliverable's own evidence base, meaning the hook, once shipped, would silently fail to flag exactly the class of feedback the package uses as its own worked example elsewhere.

**S/O/D rationale:** S=7 (a stated detection mechanism fails against the package's own proof case); O=7 (demonstrated, not projected — it already happened); D=8 (silent miss, no fallback stated for non-keyword-matching feedback).

**Corrective Action:** No NLP/classifier needed (that would be the heavyweight fix this package correctly avoids elsewhere). Add question-pattern cues ("did you," "how are we," "?" combined with process/quality nouns) to the existing keyword list, **and** add one sentence acknowledging residual false-negative risk for indirect/interrogative feedback — consistent with the fail-open, judgment-preserved design already stated (hook-design-note.md:36-41).

**Acceptance Criteria:** hook-design-note.md keyword list is expanded with at least one interrogative-pattern cue; residual-risk sentence added.

**Post-Correction RPN estimate:** ~168 (O drops to ~3 for this specific demonstrated pattern once added; general keyword-list fragility remains, appropriately, a disclosed residual risk rather than a hidden one).

---

## Finding Details — Major

### FM-002: Capture-trigger keyword ambiguity (E-01)
**Evidence:** design.md:76-79 lists 4 trigger classes ("corrects/redirects," "states a preference," "follow-up item," "inline annotation") with example phrases only, no boundary rule against ordinary conversational disagreement. **Corrective Action:** Add one clarifying sentence distinguishing standing/substantive feedback from in-context conversational back-and-forth; no new mechanism required.

### FM-004: No de-duplication for repeated inline-marker harvest (E-02)
**Evidence:** Doc mutation to mark a harvested marker was explicitly declined ("writing a `<!-- HARVESTED -->` comment back... declined as intrusive," revision-notes.md:111), removing the only proposed tracking signal; nothing else prevents the same marker being re-harvested by a later read. **Corrective Action:** Recommend the harvesting agent check the target log for an existing entry with matching verbatim/slug before minting a new id — a judgment-based check, not new infrastructure.

### FM-007: No collision-repair procedure; conflicts with immutability (E-03)
**Evidence:** design.md:167 "immutable once sealed" vs. standards.md:63 id-integrity lint that can flag a broken/duplicate sequence spanning sealed segments — no reconciliation procedure bridges the two. **Corrective Action:** State that a lint-detected collision is resolved by adding a corrective/superseding entry (consistent with the append-only correction pattern already used for verbatim fixes, standards.md §FEEDBACK-LOG "Corrections are append-only"), never by editing a sealed file.

### FM-013: Backfill id-vs-chronology ambiguity (E-07)
**Evidence:** design.md:243 (Q4) and templates (FEEDBACK-LOG.template.md:53-59) never state whether a promoted backfill row receives a tail id (mint-time order) or a chronologically-placed one. **Corrective Action:** One sentence: backfilled entries receive the next tail canonical id at promotion time (mint-time monotonicity, not content chronology); their approximate original date stays in the entry body.

### FM-014: Ungoverned Backfill Queue accumulation (E-07)
**Evidence:** Template's Backfill Queue table (FEEDBACK-LOG.template.md:57-59) has no Disposition column; Q4 "execution pending user authorization" (design.md:243) has no review cadence. **Corrective Action:** Note that Backfill Queue rows are reviewed opportunistically alongside Segment Index rebuilds or major milestones — a scheduling pointer, not new tooling.

### FM-018: No excerpt-selection rubric for assistant verbatim (E-09)
**Evidence:** design.md:110 "decision-relevant excerpt" has no selection criteria; design.md:59 acknowledges models vary per turn within a session. **Corrective Action:** Add a one-line rubric (excerpt = the recommendation/options/rationale/pushback sentence(s), per LLM-DECISION-LOG.template.md:23's own gloss) — already implicit; make it explicit as a MUST-follow gloss rather than an example.

### FM-019: Undefined, untracked graduation trigger (E-10)
**Evidence:** design.md:126 "when a decision hardens and attaches to a work item" has no owner/checklist; `LLM-DECISION-LOG.md:66` already shows a named-but-unexecuted future ADR with no deadline. **Corrective Action:** Add graduation as a Backfill-Queue-style lightweight tracked note (which decisions are graduation candidates), reviewed at the same cadence as FM-014's fix — one shared mechanism, not two new ones.

### FM-021: Q2 `scope: framework` tag has no schema field (E-11)
**Evidence:** design.md:83-87,241 propose the tag; the fixed 5-field schema (design.md:52-60) has no 6th field or placement rule for it. **Corrective Action:** Specify the tag as a Context-line suffix (e.g., append `· scope: framework` to the existing Context field) — reuses the existing field, adds no new column.

### FM-022: Undefined behavior on `JERRY_PROJECT` mid-session change (E-11)
**Evidence:** design.md:83-87 states the set/unset rule but not a transition rule. **Corrective Action:** One sentence: the log resolved at session/turn start remains the append target for that turn; a project switch takes effect on the next turn.

### FM-023: Lint checks have no implementation step in the adoption plan (E-12)
**Evidence:** design.md's 7-step adoption/migration plan (lines 203-211) lists rule-file/template installation but never assigns implementing or CI-wiring the lint script itself. **Corrective Action:** Add one line to the adoption plan: "implement and wire the 3 (or 4, per FM-008) lint checks into the existing L5 CI gate" as an explicit step.

### FM-026: Unbounded interim period before hook ships (E-13)
**Evidence:** Q3 (design.md:242) defers the hook with no target date; the manual-only interim (also underlying FM-001) has no re-check trigger. **Corrective Action:** Add a re-check note in the adoption plan (design.md §Adoption) tying hook-shipment reconsideration to a concrete checkpoint (e.g., "revisit at the next FEEDBACK-LOG segment rotation" — reuses FM-008's existing trigger rather than inventing a new one).

### FM-027: Token-budget measurement scope understates real load (E-14)
**Evidence:** revision-notes.md:124 measures only `feedback-decision-logs-standards.md` (1,584 tokens); `examples-appendix.md` (166 lines) and both templates are excluded despite the rule file now depending on the appendix by design (design.md:42). **Corrective Action:** Report a second, honest figure: combined rule-file + appendix token count, alongside the existing rule-file-only figure, so the "lean" claim is scoped accurately (this mirrors the self-critique the package already applies to the sibling ADR-convention failure, design.md:40).

---

## Minor Findings — Evidence

| ID | Evidence | Corrective Action |
|----|----------|--------------------|
| FM-005 | `FU: this section needs a diagram` appears as a literal syntax example inside FEEDBACK-LOG.template.md:23 | Wrap syntax examples in a form visibly distinct from a live marker (e.g., prefix "Example:" before the code span) |
| FM-009 | design.md:165 cap math ("800 lines ≈ 2.5× headroom") does not state whether header/Segment-Index/Backfill-Queue lines count toward the 800 | One clause: "~800 lines of *entry content*, excluding header/index/backfill overhead" |
| FM-010 | design.md:169/standards.md:52 "rebuildable by `ls`" — `ls` yields filenames only, not id ranges | Reword to "segment list rebuildable by `ls`; id ranges rebuildable by opening each sealed segment's first/last entry" |
| FM-011 | design.md:167 "immutable once sealed" has no checksum/lock/lint backing it | State that immutability is a git-history convention (no file-system enforcement), consistent with the package's own low-ceremony posture |
| FM-012 | examples-appendix.md:140 states the cross-log lookup in one sentence but never walks it through with a worked example (unlike the same-log rotation walkthrough at lines 116-142) | Add one short worked example: "FU.7 cites `DEC-LLM-004` → open LLM-DECISION-LOG's Segment Index → resolve to file" |
| FM-015 | FEEDBACK-LOG.md:167 Backfill Queue row already marked "already captured as memory `feedback_*`" sits undispositioned | Strike or annotate resolved Backfill Queue rows at next review pass |
| FM-020 | standards.md:26 "cross-link, never duplicate" vs. design.md:98 schema that restates Decision/Summary content by design | Reword LOG-M-004 to "cross-link the verbatim source, never duplicate it" (scope the absolute claim to the verbatim field only) |
| FM-025 | hook-design-note.md:28 model resolution reads "the last assistant record" with no stated fallback for a session's first turn | Add: "if no prior assistant record exists, stamp `model: (session start)` and defer to the next turn's resolution" |

---

## Recommendations

Prioritized by RPN (highest first); all corrective actions above are documentation/wording/one-lint-rule fixes — none require new subsystems, consistent with the package's own anti-bloat doctrine and the instruction not to demand heavyweight machinery for a deliberately minimal MEDIUM-tier convention.

1. **FM-016** (RPN 405) — Document write-serialization assumption for concurrent background-agent appends.
2. **FM-024** (RPN 392) — Expand Seam-2 keyword list with interrogative-pattern cues; disclose residual risk.
3. **FM-006** (RPN 384) — Soften "cannot collide" to an accurate serialized-minting + lint-backstop claim.
4. **FM-008** (RPN 360) — Add a 4th cheap lint check for ACTIVE-file cap-exceeded detection.
5. **FM-003** (RPN 336) — Disclose inline-doc harvest is opportunistic, not swept; optional grep habit.
6. **FM-017** (RPN 315) — Cite or flag-as-assumption the transcript-retention guarantee behind Option B.
7. **FM-001** (RPN 210) — Disclose the interim manual-only capture gap; add an end-of-session self-check habit.
8. **FM-013 / FM-004 / FM-019** (RPN 180 each) — One-sentence fixes: backfill-id policy, marker-dedup check, graduation tracking note.
9. Remaining Majors (FM-002, FM-007, FM-014, FM-018, FM-021, FM-022, FM-023, FM-026, FM-027) — one sentence or one adoption-plan line each; batchable into a single revision pass.
10. Minors — batchable wording/precision fixes; none block acceptance on their own.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001, FM-003 (capture-channel coverage gaps), FM-008 (rotation-enforcement gap), FM-021 (undefined schema field for a proposed default) |
| Internal Consistency | 0.20 | Negative | FM-006/FM-016 (stated guarantee vs. actual mechanism contradiction), FM-007 (lint vs. immutability contradiction), FM-020 (rule wording vs. schema behavior) |
| Methodological Rigor | 0.20 | Negative | FM-017 (unverified compensating claim), FM-024 (mechanism falsified by the package's own evidence), FM-008 (enforcement step missing from an otherwise-systematic design) |
| Evidence Quality | 0.15 | Mixed | The package is unusually well-evidenced overall (genericized real entries, cited PM-001 truncation, honest 1,584-token disclosure) — but FM-017 and FM-027 show two places where a supporting claim is asserted rather than verified/fully scoped |
| Actionability | 0.15 | Negative | FM-014, FM-019, FM-023, FM-026 show specified mechanisms (backfill governance, graduation, lint, hook) with no assigned owner, trigger, or implementation step |
| Traceability | 0.10 | Negative | FM-013 (id-vs-chronology ambiguity for backfill), FM-012 (cross-log resolution unworked in the examples) |

---

<!-- Executed per S-012 template (.context/templates/adversarial/s-012-fmea.md v1.0.0). Blind protocol: only the target deliverable package + explicitly-permitted context files were read; no prior/sibling adversary iteration output was consulted. -->

*Strategy: S-012 FMEA*
*Finding ID format: `FM-NNN` (execution: iteration-001, 2026-07-06)*
*SSOT: `.context/rules/quality-enforcement.md`*
