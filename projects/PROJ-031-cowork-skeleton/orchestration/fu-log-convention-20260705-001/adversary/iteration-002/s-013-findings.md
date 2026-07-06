# Inversion Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (design + staged artifacts)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md,FEEDBACK-LOG.template.md,LLM-DECISION-LOG.template.md,examples-appendix.md,hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (iteration 2, blind)
**H-16 Compliance:** Not directly verifiable under the blind protocol (adversary iteration-001 outputs excluded from this executor's reads). `[INFERENCE]` from the deliverable's own v3 changelog (`design/feedback-decision-log-convention-design.md:290`), which cites an `SM-001` finding among the remediated items, indicating S-003 Steelman ran in iteration 1 ahead of this C3+ sequence, consistent with H-16.
**Goals Analyzed:** 5 (G1-G5, see below) | **Assumptions/Anti-Goals Stress-Tested:** 7 | **Vulnerable Assumptions:** 7 (1 Critical, 3 Major, 3 Minor)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Goals and Anti-Goals](#goals-and-anti-goals) | Step 1-2: stated goals, inverted failure conditions |
| [Findings Table](#findings-table) | All IN-NNN findings, severity-classified |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Dimension-level impact mapping |
| [Null-Alternative Comparison](#null-alternative-comparison) | Does the package beat memory files + transcripts alone? |

---

## Summary

Applying inversion ("what would guarantee feedback/decisions get lost despite this convention?") to the design + 5 staged artifacts surfaces **1 Critical, 3 Major, 3 Minor** findings. The package **does** commit one genuine overclaim (IN-001: a claimed lint backstop that does not actually detect the dominant concurrent-write failure mode) and **does** carry several honestly-disclosed residual risks that nonetheless leave real loss vectors open (capture-itself still depends on model memory pending a deferred hook; a live, evidenced Backfill Queue of non-verbatim placeholder items has no expiration/urgency mechanism; segment file existence is never verified). None of these findings ask for new heavyweight machinery beyond what the design already gestures at (tightening wording, verifying an existing claim, adding a deadline) — consistent with the anti-bloat posture. **Recommendation: REVISE** (not REJECT) — the Critical finding is a wording/claim-accuracy fix, not a redesign, and the Majors are largely disclosure/deadline tightening. On the explicit null-alternative question: the package **does beat** memory-files-only and transcripts-only for the primary goal (durable, structured, disposition-tracked persistence of *captured* items), but it does **not** clearly beat the null alternative on the harder half of the user's original ask — guaranteeing that capture happens at all — and on one narrow axis (shared-file concurrent-write safety) it is arguably *less* robust than the null alternative's independent-per-topic-file model.

**Strengths noted (robust against inversion):** the git-tracked, structured, disposition-lifecycle design is a real and substantial improvement over both raw JSONL transcripts (unstructured, same truncation ceiling this design was built to dodge) and `MEMORY.md` bullets (no verbatim, no disposition, no formal provenance) — see [Null-Alternative Comparison](#null-alternative-comparison).

---

## Goals and Anti-Goals

**Step 1 — Goals (from L0, `design/feedback-decision-log-convention-design.md:30-38`):**

- **G1:** User feedback/follow-up items, *once captured*, survive context compaction, session boundaries, and model swaps (persistence of captured entries — note the deliberate scope narrowing to "once logged").
- **G2:** Human<->LLM decisions, once captured, likewise survive, with a clean, non-duplicating boundary to worktracker `DEC-NNN`/ADRs.
- **G3:** The convention is codified and shipped (rule + templates), not an emergent, un-enforced wish.
- **G4:** The convention stays MEDIUM-tier and minimal (forced by the HARD ceiling at 25/25).
- **G5 (the user's literal, broader ask, `FEEDBACK-LOG.md:59`, FU.2 verbatim):** *"I want this to be a Jerry convention so that we don't loose feedback or follow up items."* — note this is broader than G1: it is not scoped to "once captured."

**Step 2 — Anti-goals (what would guarantee failure of G1/G2/G5):**

| Anti-goal | Present in the package? |
|---|---|
| AG1: Depend entirely on model memory to trigger the *first* write, and defer the one automation (hook) that would harness-guarantee it, with no ship date. | **Yes** — Q3 default, `design/...design.md:247`. Disclosed as a G1-vs-G5 scope narrowing, not an overclaim. (IN-003, Major) |
| AG2: Let multiple writers mutate the single shared ACTIVE log file concurrently, and claim a lint backstop that does not actually catch the dominant race pattern. | **Yes** — `design/...design.md:70`. This is an overclaim, not a disclosed limitation. (IN-001, Critical) |
| AG3: Let historical items sit indefinitely as non-verbatim placeholders with no deadline, while their sources (memory files, transcripts) can independently rot. | **Yes, already live** — `FEEDBACK-LOG.md:161-170`, `LLM-DECISION-LOG.md:72-81`. (IN-002, Major) |
| AG4: Never verify that segment files referenced by the Segment Index still exist on disk. | **Yes** — no such check exists in the 3 L5 lint checks. (IN-005, Major) |
| AG5: Make the durability advantage over memory files conditional on an unenforced side-practice (commit/push cadence) without disclosing the dependency. | **Partially** — mitigated by evidenced compliance (FU.3 shows 2 real commits). (IN-004, Minor) |
| AG6: Split capture across two undiscoverable scopes with no unified index. | **Yes, disclosed as an accepted trade.** (IN-006, Minor) |
| AG7: Make full-fidelity decision recovery depend on an external, ungoverned transcript-retention policy. | **Yes, disclosed with a C3+ escape hatch.** (IN-007, Minor) |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-i2-20260706 | "Collision-resistant" claim: lint (L5 #2) detects the dominant concurrent-write failure mode | Anti-Goal (AG2) | High (the race is straightforward read-modify-write) | **Critical** | `design/feedback-decision-log-convention-design.md:70,201` | Internal Consistency |
| IN-002-i2-20260706 | Backfill Queue items will eventually convert to full verbatim entries before their sources rot | Assumption | Medium | **Major** | `FEEDBACK-LOG.md:161-170`, `LLM-DECISION-LOG.md:72-81`, `design/...design.md:248` (Q4) | Completeness |
| IN-003-i2-20260706 | The "don't lose feedback" goal (G5) is satisfied by a design that only guarantees persistence *after* capture (G1), while capture itself stays model-memory-dependent pending a hook with no ship date | Anti-Goal (AG1) | High | **Major** | `design/...design.md:30,215,247`; `research/feedback-decision-log-research.md:159`; `FEEDBACK-LOG.md:59` | Completeness |
| IN-004-i2-20260706 | Git commit/push cadence (a MEDIUM, unenforced side-practice) is reliably followed, so the log's durability edge over memory files holds in practice | Assumption | Medium (evidenced compliance so far) | Minor | `FEEDBACK-LOG.md:71-81` (FU.3); `staging-feedback-logs/hook-design-note.md:35` | Evidence Quality |
| IN-005-i2-20260706 | Sealed segment files referenced by the Segment Index continue to exist on disk (no verification) | Assumption | Medium | **Major** | `design/...design.md:168-177,196-202`; `staging-feedback-logs/feedback-decision-logs-standards.md:59-64` | Methodological Rigor |
| IN-006-i2-20260706 | Feedback given under an ambiguous/switching `JERRY_PROJECT` scope remains findable via manual dual-grep | Assumption | Medium | Minor | `design/...design.md:90` | Completeness |
| IN-007-i2-20260706 | The JSONL transcript backing an excerpt+pointer decision entry remains retained and resolvable indefinitely | Assumption | Low | Minor | `design/...design.md:112-115` (Q1) | Evidence Quality |

**Finding ID format:** `IN-{NNN}-i2-20260706` (iteration 2, this session, 2026-07-06) to avoid collision with iteration-1 `IN-NNN` identifiers referenced in the deliverable's own changelog.

---

## Finding Details

### IN-001-i2-20260706: Lint backstop does not detect the dominant concurrent-write failure mode [CRITICAL]

**Type:** Anti-Goal (AG2)
**Original Assumption:** "it is backstopped by the id-integrity lint (L5 #2), which *detects* a duplicate/gap rather than *preventing* the race" (`design/feedback-decision-log-convention-design.md:70`; lint definition at line 201 and `staging-feedback-logs/feedback-decision-logs-standards.md:63`: "ids unique, strictly increasing, and contiguous... Contiguity catches a *dropped mid-sequence entry*").
**Inversion:** Model the realistic race the design itself names ("parallel/background agents" appending to the *same* log file, `:70`): Agent A reads the file (last id `FU.11`), computes next id `FU.12`, writes back the *entire file* (read-modify-write, the only pattern a markdown-append tool has). Agent B reads the file at nearly the same time (also sees `FU.11`, stale), also computes `FU.12`, and writes back the entire file with its own content. If B's write lands after A's, the final file contains `FU.0`-`FU.11` (unchanged) + B's `FU.12` only. There is **no duplicate id** (only one `FU.12` survives) and **no gap** (ids run 0..12 contiguously) — A's entire entry is gone with zero trace. This is the single most direct, literal answer to "what would guarantee feedback gets lost despite this convention," and the design's own explicit invitation to use "background agents" for this system (`FEEDBACK-LOG.md:63`, FU.2 verbatim: *"leverage background agents so that we don't burn through the main context window"*) makes concurrent writers a designed-for scenario, not a remote edge case.
**Plausibility:** High — this is the default behavior of any "read whole file, append in memory, write whole file" implementation (the only pattern markdown logs support without a database or lock file); no code, hook, or protocol in the reviewed package performs atomic append or file locking.
**Confidence:** High
**Consequence:** A background agent's captured feedback or decision is silently and permanently lost, with the lint (the claimed safety net) reporting a clean pass. This directly contradicts the deliverable's central thesis ("what depends on the model remembering will eventually be forgotten" now also applies to "what depends on a write ordering race will eventually be dropped").
**Evidence:** `design/feedback-decision-log-convention-design.md:70` (the overclaim), `:201` (lint definition claiming "contiguity catches a dropped mid-sequence entry" — this is true for a *gap-leaving* drop, not a *clobbering* drop); `staging-feedback-logs/feedback-decision-logs-standards.md:27,63` (LOG-M-005 "single-writer-per-log" + lint check 2, same gap); `FEEDBACK-LOG.md:63` (user's explicit background-agent intent).
**Dimension:** Internal Consistency (the disclosed-residual-risk framing is more reassuring than the mechanism actually warrants — this is the "overclaimed coverage" class the review brief calls Critical).
**Mitigation:** No new machinery required — this is a wording/scope fix, not a redesign. Either (a) narrow the claim: state plainly that the lint detects *some* collision patterns (e.g., a true simultaneous duplicate-id write that both survive, which requires a non-clobbering storage layer) but does **not** detect a lost-update overwrite, and treat concurrent same-log writes as fully out-of-scope for background-agent use until a serialization mechanism exists; or (b) add one line of *process* guidance (not new lint machinery): route all writes to a given log through a single coordinating agent/turn when multiple background agents are active in the same session, preserving the already-stated "single-writer-per-log" discipline as a MUST-follow operational rule rather than an aspiration.
**Acceptance Criteria:** The design doc and standards file no longer imply the lint "detects" a lost-update overwrite; either the residual-risk wording is corrected to name the actual gap, or a single-writer coordination rule is stated as binding guidance for multi-agent sessions.

### IN-002-i2-20260706: Backfill Queue already holds non-verbatim placeholders for real items with no deadline to convert them [MAJOR]

**Type:** Assumption
**Original Assumption:** Backfill Queue rows are temporary "candidates... pending user authorization" (design intent, confirmed as intentionally lightweight per the deliverable's own rebuttal of UX finding F-022: "the queue is intentionally a lightweight candidate list, not full entries").
**Inversion:** What if authorization for backfill (Q4) is never given, or is deferred long enough that the underlying sources rot? This is not hypothetical — the Backfill Queue **already contains real, currently-existing items** captured only as one-line paraphrases, not verbatim: e.g. `FEEDBACK-LOG.md:167` *"YAGNI is not a good answer (repo naming; deferred-change cost) | chat, prior session — already captured as memory `feedback_*`"* — this is a title, not the user's verbatim words, sitting inside a convention whose core promise (LOG-M-002) is "verbatim and full." The row's own source pointer ("memory `feedback_*`") is itself a local, prunable file, not a durable record. `LLM-DECISION-LOG.md:78-81` shows the same pattern for 4 pre-log decisions.
**Plausibility:** High — Q4 (`design/...design.md:248`) is explicitly open-ended ("execution pending user authorization — not auto-adopted"), with no deadline or trigger comparable to Q3's re-assessment trigger.
**Consequence:** If the referenced memory file or transcript for a queued item is ever pruned/rotated (neither is governed by this convention), the underlying feedback is permanently reduced to the one-line paraphrase already in the table — a quiet, partial realization of exactly the failure this convention exists to prevent, and it is already partially in effect today for 8 real items across the two live logs.
**Evidence:** `FEEDBACK-LOG.md:161-170`; `LLM-DECISION-LOG.md:72-81`; `design/feedback-decision-log-convention-design.md:248` (Q4 has no deadline, unlike Q3's explicit re-assessment trigger).
**Dimension:** Completeness (the backfill mechanism is incomplete without an expiration/urgency handling policy).
**Mitigation:** No new subsystem — add one line to LOG-M-004/Q4 giving the Backfill Queue an explicit staleness trigger symmetric to Q3's (e.g., "re-assess backfill authorization at the same checkpoint as the Q3 hook re-assessment, or when a queued item's source (memory file/transcript) is observed to have rotated, whichever comes first").
**Acceptance Criteria:** Q4 carries an explicit re-assessment trigger (not open-ended); the two live Backfill Queues are flagged for a one-time authorization decision at the next commit-cadence checkpoint rather than indefinitely.

### IN-003-i2-20260706: Capture-itself remains model-memory-dependent; only a reactive (post-incident) re-assessment trigger exists [MAJOR]

**Type:** Anti-Goal (AG1)
**Original Assumption:** The convention meaningfully answers the user's ask "so that we don't loose feedback or follow up items" (`FEEDBACK-LOG.md:59`, FU.2 verbatim — G5).
**Inversion:** The design honestly narrows its actual guarantee to "once captured, entries survive" (`design/...design.md:30`, the L0 scope note), explicitly stating "capture stays a MEDIUM (SHOULD) discipline until the fail-open hook... ships." Q3 (`:247`) defaults to shipping the hook "as a separate gated change" with no committed date. The design's own research explicitly diagnosed this exact failure mode in [internal-kb]: *"Capture trigger is human memory... the 'don't lose feedback' goal depends on the very attention that gets lost under context pressure"* (`research/feedback-decision-log-research.md:159`) — and the v1 package reproduces this same dependency for the common (chat, non-inline-doc) case. The chosen re-assessment trigger for shipping the hook (`:215`) is *"the first segment rotation OR the first observed missed-capture incident, whichever comes first"* — by construction, the missed-capture branch of that trigger fires only **after** a loss has already occurred.
**Plausibility:** High — this is not a hypothetical inversion; it is the explicitly disclosed, current state of the design.
**Consequence:** The harder, arguably more central half of the user's literal request (G5: capture never happens without the model remembering) is not solved by v1; it is deferred. This is honestly disclosed (not an overclaim — the L0 scope note is careful), so it does not invalidate the deliverable's narrower, stated core approach (G1), but it does mean the deliverable's persuasive framing ("so that we don't lose feedback") risks being read by a stakeholder as solving more than it does.
**Evidence:** `design/feedback-decision-log-convention-design.md:30,215,247`; `research/feedback-decision-log-research.md:159`; `FEEDBACK-LOG.md:59`.
**Dimension:** Completeness (the stated user goal is only partially met by the shipped scope).
**Mitigation:** No new machinery — reframe the re-assessment trigger to include a proactive component alongside the reactive one (e.g., "or after N sessions of manual-compliance spot-check showing a miss," or simply a calendar checkpoint), so the decision to ship the hook does not structurally require a loss event first. Also consider surfacing the G1-vs-G5 scope gap more prominently (e.g., in the L0 headline, not only a parenthetical scope note) so a reader ratifying the design is not misled about what is actually guaranteed today.
**Acceptance Criteria:** The re-assessment trigger includes at least one proactive (non-incident-contingent) condition; the L0 headline states the G1-vs-G5 scope distinction as plainly as the "Design posture: start minimal" callout already does for token budget.

### IN-005-i2-20260706: Segment-file existence is never verified — the rotation subsystem can silently lose its own history [MAJOR]

**Type:** Assumption
**Original Assumption:** "immutable once sealed... git history is the backstop... an accidental edit surfaces as a reviewable git diff, not silent corruption" (`design/...design.md:172`).
**Inversion:** What if a sealed segment (`FEEDBACK-LOG.001.md`) is *deleted* rather than edited — via an aggressive cleanup script, a bad rebase/squash that drops history, or simply an accidental `rm` before a commit lands? The stated mitigation ("surfaces as a reviewable git diff") only helps if the deletion is itself committed and someone reviews that specific diff; it does not help for uncommitted deletions, and none of the 3 L5 lint checks (`:198-202`; `staging-feedback-logs/feedback-decision-logs-standards.md:59-64`) verify that every file listed in the ACTIVE file's Segment Index actually still exists on disk. The Segment Index would continue to claim `Segment 1 | FEEDBACK-LOG.001.md | FU.0-FU.49` even after the file is gone, with no automated signal.
**Plausibility:** Medium — requires an unusual operational mistake, but segment rotation exists specifically to prevent loss-at-scale (FU.5), so silently permitting physical loss of exactly the artifact rotation was meant to preserve undercuts that subsystem's stated purpose.
**Consequence:** Total, silent loss of an entire sealed segment (up to ~50 entries / ~800 lines) with no detection until a human happens to try to read it.
**Evidence:** `design/feedback-decision-log-convention-design.md:168-177` (L1.4 table, "Sealed segments" row); `:196-202` (the 3 lint checks, none of which cover file-existence); `staging-feedback-logs/feedback-decision-logs-standards.md:59-64`.
**Dimension:** Methodological Rigor (the segment-rotation mechanism's own verification story has a gap in exactly the area it was designed to protect).
**Mitigation:** No new subsystem — fold a file-existence check into the *existing* lint 1 pass (which already walks the log files for the nav-table/cap check): assert every segment path listed in the ACTIVE file's Segment Index resolves to an existing file. This is a same-shape addition to a check that already exists, not a new mechanism.
**Acceptance Criteria:** Lint check 1 (or a documented one-line addition to it) fails if any Segment Index row's file path does not exist on disk.

---

## Recommendations

**MUST mitigate (Critical):**
- **IN-001-i2-20260706** — Correct the "collision-resistant... backstopped by the id-integrity lint" claim so it does not imply detection of a lost-update overwrite it cannot detect; state a binding single-writer-coordination rule for multi-agent sessions instead of an aspirational one.

**SHOULD mitigate (Major):**
- **IN-002-i2-20260706** — Give the Backfill Queue an explicit re-assessment/expiration trigger; flag the two live queues (8 items total) for a near-term authorization decision.
- **IN-003-i2-20260706** — Add a proactive component to the Q3 hook re-assessment trigger; state the G1-vs-G5 scope narrowing more prominently.
- **IN-005-i2-20260706** — Fold a segment-file-existence check into the existing lint 1 pass.

**MAY mitigate (Minor):**
- **IN-004-i2-20260706** — Note the commit/push-cadence dependency explicitly as a precondition for the log's durability claim (already evidenced as followed in practice — low urgency).
- **IN-006-i2-20260706** — No action required beyond the existing disclosed grep-both-logs guidance; acceptable anti-bloat trade.
- **IN-007-i2-20260706** — No action required beyond the existing C3+ full-paste escape hatch; acceptable anti-bloat trade, already disclosed with size math.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002 (Backfill Queue has no expiration), IN-003 (capture-itself goal only partially met), IN-006 (multi-scope discovery gap, minor) |
| Internal Consistency | 0.20 | Negative | IN-001: the disclosed-residual-risk claim ("lint detects a duplicate/gap") does not match the actual dominant race outcome (silent clobbering with neither duplicate nor gap) |
| Methodological Rigor | 0.20 | Negative | IN-005: the segment-rotation subsystem's own lint coverage does not verify the one thing it exists to protect (segment file continuity) |
| Evidence Quality | 0.15 | Negative (minor) | IN-004 (durability claim conditioned on unenforced practice, though evidenced as followed), IN-007 (transcript-retention dependency undisclosed-by-policy, though disclosed-by-design) |
| Actionability | 0.15 | Neutral-to-Positive | All 7 findings have concrete, low-machinery mitigations consistent with the deliverable's own anti-bloat doctrine; none require new subsystems |
| Traceability | 0.10 | Neutral | Findings trace cleanly to specific lines in the design doc, standards file, and the two live log instances; no traceability gap identified |

---

## Null-Alternative Comparison

**Does the package beat the null alternative (memory files + transcripts only)?**

**Yes, clearly, for the primary goal (durable, structured, disposition-tracked persistence of *captured* items):**
- Git-tracked files survive collaboration, machine changes, and are versioned/auditable; `MEMORY.md`-only persistence is local-machine-scoped, not git-tracked, and is exactly what the research's own [internal-kb] citation (`R-CONTEXT-002`) rejects for persistent guidance ("not git-tracked, invisible to collaborators, split-state" — `research/feedback-decision-log-research.md:230`).
- The verbatim + summary + disposition + context schema is structured and greppable; raw JSONL transcripts are large, unstructured, and subject to the *same* ~25k-token truncation ceiling this design exists to route around (`design/...design.md:164`); `MEMORY.md` bullets (see this session's own auto-loaded memory) carry no verbatim, no disposition, and no formal provenance beyond a filename.
- Disposition lifecycle (`OPEN/IN-PROGRESS/DONE/WONTFIX` + evidence-on-terminal) exists in neither the transcript nor the memory-file null alternative at all.

**No / not clearly, on two specific axes:**
- **Guaranteeing capture happens at all (IN-003).** Both the log convention (v1, pre-hook) and the null alternative depend equally on the model choosing to notice and act; the convention adds a norm (LOG-M-001, "SHOULD append same-turn") but not yet a harness guarantee. This is the harder half of the user's literal ask and is not solved by either approach today.
- **Concurrent-writer safety (IN-001).** The null alternative's memory-file model stores each independent piece of feedback as its own separately-named file (e.g. `feedback_never_print_credentials.md`, `feedback_skills_during_planning.md` — see this session's auto-loaded `MEMORY.md`), which structurally avoids the shared-mutable-resource race entirely: there is no id to collide over. The proposed single-shared-ACTIVE-file design *introduces* a race condition the null alternative does not have, in exchange for the (real) benefits of a single chronological, disposition-tracked timeline. This is a genuine, if narrow, trade-off that the design does not explicitly weigh against the null.

**Net assessment:** the package is a legitimate, well-evidenced improvement over the null alternative for everything downstream of "an entry got written" — which is most of the value proposition and should not be understated. It does not yet close the gap on whether an entry gets written in the first place, and it introduces one new failure mode (shared-file concurrent writes) that the null alternative's independent-file model did not have. Both points are appropriately sized as Major/Critical findings above rather than reasons to reject the overall design direction.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 1
- **Major:** 3
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations developed, synthesized)
