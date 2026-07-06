# Devil's Advocate Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (FU-Log)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-05
**Reviewer:** adv-executor (S-002, iteration 1)
**H-16 Compliance:** ASSUMED via orchestration group-sequencing (self-refine -> steelman -> challenge -> verify -> decompose -> score); this executor operates under BLIND PROTOCOL and did not read `.../adversary/` outputs, including any S-003 (Steelman) output, and therefore cannot directly confirm S-003 ran. This is a documented assumption, not a verified fact -- flagged for the orchestrator to confirm before this report is used to gate acceptance.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All DA-NNN findings with severity and evidence |
| [Finding Details](#finding-details) | Expanded detail for Critical and Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

7 counter-arguments identified (2 Critical, 3 Major, 2 Minor), targeting the three assigned attack vectors: segment-rotation growth economics, alias/canonical-id reference ambiguity, and multi-user adoptability. The package's MEDIUM-tier, anti-bloat posture is respected throughout this critique -- none of the findings ask for new machinery; most ask for either a documented boundary/disclosure or a one-line schema addition. Two findings are Critical because they are **overclaims of fact contradicted by the design's own evidence**: (1) the claim that "parallel/background agents cannot collide" (DA-001) is asserted with no concurrency mechanism, in a project whose own decision log documents 50-agent parallel tournaments; and (2) the alias scheme's own worked example (DA-002) proves that a single alias label maps to multiple canonical entries, yet no resolution procedure exists for a later bare-alias reference -- directly the scenario the attack prompt named ("FU.1 from three turns ago"). Recommend REVISE (targeted, mostly disclosure/one-line-schema fixes, not structural rework) before this deliverable proceeds to S-014 scoring.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-S002i1 | "Cannot collide" id-minting claim has no concurrency mechanism | Critical | `design/feedback-decision-log-convention-design.md:70`; `LLM-DECISION-LOG.md:36-38` (DEC-LLM-001 Context cites "5 blind 10-strategy tournaments") | Internal Consistency |
| DA-002-S002i1 | No resolution procedure for a later bare-alias back-reference (e.g. "FU.1" from 3 turns ago) | Critical | `staging-feedback-logs/examples-appendix.md:24-34`; `FEEDBACK-LOG.md` FU.6 (line 121) | Completeness |
| DA-003-S002i1 | Segment Index is itself unbounded and lives inside the very cap it is meant to protect | Major | `design/feedback-decision-log-convention-design.md:163-169`; `staging-feedback-logs/feedback-decision-logs-standards.md:52` | Completeness |
| DA-004-S002i1 | FEEDBACK-LOG schema has no defined "no operator label" fallback; alias scheme is modeled on one user's documented personal habit | Major | `staging-feedback-logs/FEEDBACK-LOG.template.md:20,24-25`; `FEEDBACK-LOG.md:118` (FU.6 verbatim) vs. `staging-feedback-logs/LLM-DECISION-LOG.template.md:19` (which does define `<label or —>`) | Traceability |
| DA-005-S002i1 | No author/participant identity field -- schema assumes a single operator, unlike the worktracker DECISION entity it is meant to feed | Major | `design/feedback-decision-log-convention-design.md:59`; `research/feedback-decision-log-research.md:201,265` (DECISION `participants[]` required) | Completeness |
| DA-006-S002i1 | Cross-segment content (non-id) search has no specified mechanism beyond ad hoc `grep`; not explicit that Bash grep (not Read) is required | Minor | `staging-feedback-logs/examples-appendix.md:162-166` | Actionability |
| DA-007-S002i1 | Manual, LLM-performed segment rotation has no correctness check other than post-hoc L5 lint | Minor | `design/feedback-decision-log-convention-design.md:172`; `staging-feedback-logs/hook-design-note.md:47-49` (Seam 3: rotation "MUST NOT" be automated) | Methodological Rigor |

**Finding ID Format:** `DA-{NNN}-S002i1` (S-002, iteration 1, this execution).

---

## Finding Details

### DA-001: "Cannot collide" id-minting claim has no concurrency mechanism [CRITICAL]

**Claim Challenged:** "canonical ids are logger-owned, so parallel/background agents cannot collide, and the operator is never asked to remember a number." (`design/feedback-decision-log-convention-design.md:70`). The same unqualified guarantee is restated for the segment-aware id scheme (LOG-M-005, `staging-feedback-logs/feedback-decision-logs-standards.md:27`) and claimed as an explicit improvement over [internal-kb]'s observed `DJ-025` collision.

**Counter-Argument:** The claim is a factual overclaim. "Logger-assigned" only describes *who* mints the id (the LLM, not the operator) -- it says nothing about *how* a unique, monotonic id is safely produced when more than one writer (agent/session) targets the same file concurrently. Minting a new canonical id necessarily requires reading the current maximum id and writing the next one; with no documented locking, atomic-append, or single-writer-serialization mechanism, two concurrent writers that both read the same "current max" before either writes will independently mint the *same* next id -- reproducing the exact `DJ-025`-class collision the design claims to have eliminated, just moved from manual human numbering to concurrent machine numbering. Nothing in the rule file, the hook design note, or the templates specifies a locking/atomicity/serialization discipline. The only backstop offered anywhere is the L5 lint's *post-hoc* "ids unique and strictly increasing" check (`design/feedback-decision-log-convention-design.md:196`), which detects a collision only at commit/CI time -- after it has already been written, potentially by two different (background) agents in two different turns.

**Evidence:** This is not a hypothetical scenario for this project: `LLM-DECISION-LOG.md:36-38` (DEC-LLM-001 Context) documents that this very deliverable's own decision-history was produced by "workflow `wf_dcb52638-593` (... 5 blind 10-strategy tournaments" -- i.e., up to 50 parallel background agents were already fanned out in this project's operational history. The user's own FU.2 requirement (`FEEDBACK-LOG.md:63`) explicitly asks to "leverage background agents so that we don't burn through the main context window" -- the exact concurrency profile that breaks the "cannot collide" guarantee if any of those agents independently append log entries.

**Impact:** If the guarantee is relied upon as stated, concurrent background-agent writes to FEEDBACK-LOG or LLM-DECISION-LOG can silently collide (two entries claiming the same canonical id), corrupting the very cross-log, cross-segment id-based navigation the design depends on (id-based cross-references, per L1.4, become ambiguous the moment two entries share an id). This directly undermines the "so that we don't lose feedback" purpose (FU.2 verbatim) the whole convention exists to serve.

**Dimension:** Internal Consistency (the claim is inconsistent with the absence of any supporting mechanism) and, secondarily, Evidence Quality (an unqualified "cannot" claim with no cited mechanism).

**Response Required:** Either (a) specify a concrete concurrency-safe minting mechanism (e.g., single-writer discipline -- only the orchestrating/main-context agent appends to the log; background/worker agents return findings via handoff for serial append, consistent with Jerry's own P-003 orchestrator-worker topology), or (b) explicitly narrow the claim to state its actual scope (e.g., "collision-safe under single-writer append discipline; NOT engineered for concurrent direct writes by multiple agents/sessions") per P-022 (no overclaiming).

**Acceptance Criteria:** The revised design either names the serialization mechanism that makes "cannot collide" true, or replaces the unqualified claim with an honestly scoped one and states the operational discipline required (e.g., "log-append is main-context-only; background agents report findings upstream").

---

### DA-002: No resolution procedure for a later bare-alias back-reference [CRITICAL]

**Claim Challenged:** The alias scheme is presented as fully solving the operator-burden problem: "The operator must NEVER need to remember a global counter... this was an operator-UX defect in the draft design" (`FEEDBACK-LOG.md:121`, FU.6 disposition) and "[the alias] carr[ies] zero maintenance burden" (`design/feedback-decision-log-convention-design.md:67`).

**Counter-Argument:** The fix only addresses the *write-time* direction (operator mints a local label; logger silently maps it to a canonical id). It does not address -- and does not even mention -- the *read-time* direction: what happens when the operator later refers back to their own alias (e.g., "let's revisit FU.1") without additional context? The design's own worked example proves the ambiguity is real and structural, not edge-case: `staging-feedback-logs/examples-appendix.md:24-31` shows the SAME alias label recurring across turns and mapping to *different* canonical ids each time ("Turn 1 ... FU.0 (alias: FU.0) ... Turn 2 ... FU.3 (alias: FU.0) ... inline doc ... FU.5 (alias: FU.0)"). Given the user's own stated habit is to "re-start at FU.0 everytime a turn happens" AND "in every document I am reviewing" (`FEEDBACK-LOG.md:118`, FU.6 verbatim), alias collisions across the corpus are the *norm*, not a rare occurrence. If, three turns after minting canonical FU.3 (alias FU.0), the user says "what's the status of FU.0?", there is no documented procedure for the assistant (or a human co-collaborator scanning the raw file) to determine which of the (potentially many) FU.0-aliased entries is meant. The "Common cases" section (`staging-feedback-logs/examples-appendix.md:162-166`) only covers "I forgot to capture," "how do I find that feedback about X" (assumes a topical slug, not a bare alias), and "the verbatim was wrong" -- it does not cover "the user re-used an ambiguous alias to reference a prior entry," which is exactly the scenario named in this review's attack brief.

**Evidence:** `staging-feedback-logs/examples-appendix.md:19-34` ("Ids & aliases (before/after)" section, the design's own canonical illustration of the scheme) and `FEEDBACK-LOG.md:113-124` (FU.6, the requirement this scheme was built to satisfy).

**Impact:** An ambiguous or mis-resolved back-reference is a silent feedback-loss/misattribution failure -- precisely the failure mode the entire convention was commissioned to prevent (FU.2: "so that we don't loose feedback or follow up items"). Unlike DA-001 (a structural/engineering gap), this is a gap in the *operating procedure* around a schema the design otherwise gets right; it is a Critical because of how directly it contradicts the design's own stated no-loss purpose and because the design's own worked example is the proof of the ambiguity.

**Dimension:** Completeness (the operating procedure for the read-time direction of the alias scheme is entirely unaddressed) and Actionability (no defined operator/assistant action when an alias reference is ambiguous).

**Response Required:** Add an explicit disambiguation protocol to the rule file/appendix, e.g.: "If a user references a bare alias (e.g., 'FU.1') without further context, and more than one canonical entry shares that alias, the assistant MUST enumerate the candidates (canonical id, slug, turn/date) and ask the user to select (per H-31) rather than infer from conversational recency." Add one worked example showing this resolution to `examples-appendix.md`.

**Acceptance Criteria:** `examples-appendix.md` "Common cases" gains an explicit "ambiguous alias reference" case with the disambiguation procedure above (or an equivalent), and the rule file references it.

---

### DA-003: Segment Index is itself unbounded and lives inside the very cap it protects [MAJOR]

**Claim Challenged:** "Keeps every log loadable in one Read; cross-log navigation is free via canonical ids (FU.5)" (Improvement Ledger row 9, `design/feedback-decision-log-convention-design.md:229`); segment rotation is presented as resolving FU.5's "what are the consequences ... when this file grows too large" concern in full.

**Counter-Argument:** This is a "shard, not solve" critique, precisely per the assigned attack vector. The per-entry growth problem is genuinely addressed (the ~50-entry/~800-line cap on ACTIVE content is well-justified against the ~2,000-line Read window and ~25k-token truncation, `design/feedback-decision-log-convention-design.md:165`). However, the **Segment Index** -- "a small `segment · file · canonical-id-range` table [that] lives *only in the ACTIVE file* (one row per rotation; rebuildable by `ls`)" (`design/feedback-decision-log-convention-design.md:169`; identical wording in `staging-feedback-logs/feedback-decision-logs-standards.md:52`) -- is itself an append-only, never-rotated, never-truncated structure, and it lives *inside* the file whose size is capped at ~800 lines. Every rotation permanently adds one row to this index and the row is never removed. As the number of segments grows (a genuinely plausible outcome for a long-running project/session per the exact scenario FU.5 asked about -- "long running sessions and or projects," `FEEDBACK-LOG.md:104`), the index consumes an ever-larger share of the 800-line ACTIVE-file budget before a single new entry is written, forcing progressively *more frequent* rotations with *fewer* real entries per segment -- a shrinking-capacity spiral nested inside the very mechanism designed to prevent unbounded growth. The design never addresses this second-order growth; it recurses the original problem at roughly 1/50th the rate (one line per ~50 entries) rather than eliminating it.

**Evidence:** `design/feedback-decision-log-convention-design.md:163-169` (cap table + Segment Index row); `staging-feedback-logs/feedback-decision-logs-standards.md:52` ("a small `segment, file, id-range` index lives in the ACTIVE file"); `staging-feedback-logs/examples-appendix.md:131-138` (worked example shows the index growing by exactly one row per rotation with no compaction step shown or mentioned).

**Impact:** For the current single-project, MEDIUM-tier scope this is very unlikely to bite (it requires hundreds of segments / tens of thousands of entries before the index meaningfully competes with entry budget). But the design's claim ("keeps every log loadable in one Read") is stated unconditionally, not scoped to an expected entry-count ceiling, which is an evidence-quality gap given the anti-bloat doctrine's own stated principle: "start minimal ... grow only on evidence" (`design/feedback-decision-log-convention-design.md:40`) -- the evidence for *this* particular unbounded dimension is not evaluated at all.

**Dimension:** Completeness (an identified growth dimension left unaddressed) and, secondarily, Evidence Quality (unconditional claim of a bound that is not actually unconditionally true).

**Response Required:** Either (a) document an explicit index-compaction step (e.g., "if the index exceeds M rows, collapse older rows into a single `segments 1-N: FU.0-FU.{k} (see segment-index-archive.md)` summary line"), or (b) explicitly disclose the boundary condition and its expected practical irrelevance at anticipated project scale (e.g., "not addressed; acceptable given expected lifetime of < X segments for a MEDIUM-tier per-project log; revisit if a project exceeds X segments"), consistent with the anti-bloat doctrine's own "grow only on evidence" standard -- but stated as a disclosed limitation, not an unconditional guarantee.

**Acceptance Criteria:** The design doc's Improvement Ledger row 9 and/or L1.4 gains either a compaction mechanism or an explicit disclosed-limitation note bounding the "keeps every log loadable" claim.

---

### DA-004: FEEDBACK-LOG schema has no defined "no operator label" fallback [MAJOR]

**Claim Challenged:** The design is explicitly intended to be a general, framework-wide, multi-user convention: "I want this to be a Jerry convention" (`FEEDBACK-LOG.md:63`, FU.2 verbatim).

**Counter-Argument:** The FEEDBACK-LOG entry schema and its only template/example are built entirely around one specific, documented personal habit: the user's own statement, "Typically I re-start at FU.0. everytime a turn happens ... I also start from FU.0. in every document that I am reviewing" (`FEEDBACK-LOG.md:118`, FU.6 verbatim). The template instructs all future adopters using near-identical language: "you will typically restart at `FU.0` every turn and every document you review. That is expected." (`staging-feedback-logs/FEEDBACK-LOG.template.md:20`). Nowhere in the FEEDBACK-LOG schema, template, or appendix is a "no operator label given" case defined -- contrast this with the LLM-DECISION-LOG schema, which explicitly provides for the no-alias case: `## DEC-LLM-NNN <slug> (alias: <label or —>)` (`staging-feedback-logs/LLM-DECISION-LOG.template.md:19`, emphasis on the `— ` fallback). A different Jerry user or team who never assigns any `FU.N`-style label to their own feedback (arguably the more common default mode for a plain-language user) has no documented fallback for the FEEDBACK-LOG heading format `## FU.N <slug> (alias: <operator-label>)` (`design/feedback-decision-log-convention-design.md:52`). This is an asymmetric completeness gap directly relevant to general adoptability: the convention's worked example, its teaching text, and its schema are all built from -- and only demonstrated for -- a single individual's idiosyncratic labeling tic inherited from a prior, unrelated internal-kb pattern, rather than from a generalized "any Jerry user" baseline.

**Evidence:** `staging-feedback-logs/FEEDBACK-LOG.template.md:20,24-25`; `FEEDBACK-LOG.md:113-124` (FU.6); contrast `staging-feedback-logs/LLM-DECISION-LOG.template.md:19,42` (`<label or —>`, `alias: —`).

**Impact:** For the current single-user deployment this is cosmetic. For the stated goal of shipping this "into the Jerry Framework" as a general convention (`FEEDBACK-LOG.md:63`), an unaddressed schema gap for the (likely majority) no-alias case is a real adoption barrier -- new adopters copying the template have no example to follow when they simply write feedback in plain language with no self-assigned numbering.

**Dimension:** Traceability (schema documentation does not trace to a generalized user population) and Completeness.

**Response Required:** Add the same `(alias: <label or —>)` fallback pattern to the FEEDBACK-LOG schema (`design/feedback-decision-log-convention-design.md:52`, `staging-feedback-logs/feedback-decision-logs-standards.md:32`) and one worked example in `examples-appendix.md` showing a plain-language entry with `alias: —`.

**Acceptance Criteria:** `FEEDBACK-LOG.template.md` and `examples-appendix.md` each contain at least one example with no operator-assigned alias.

---

### DA-005: No author/participant identity field [MAJOR]

**Claim Challenged:** The Context field is fixed as "`datetime · session · model(s) · turn · agents/workflow · source`" (`design/feedback-decision-log-convention-design.md:59`) and is presented as sufficient provenance for the log, explicitly modeled to feed and cross-link the worktracker DECISION entity via graduation (`design/feedback-decision-log-convention-design.md:114-126`).

**Counter-Argument:** The worktracker DECISION entity this log is designed to graduate into **requires** `participants[]` (`research/feedback-decision-log-research.md:201`, "`participants[]` **required**"; restated at `research/feedback-decision-log-research.md:265`, "Ceremony | ... `participants[]` required, co-located ..."). The new log's own Context schema has no equivalent field identifying *which human* gave the feedback or made the decision -- it captures session/model/turn but not author. This is invisible in the current bootstrap because PROJ-031 is evidently a single-operator project, but it is a real adoptability gap for any team (multiple humans) adopting the convention: two different people's feedback in the same or different sessions is indistinguishable by author in the log itself, and the graduation path to a DECISION entity (which *does* require participants) would need to reconstruct that information from outside the log (e.g., from transcripts) at graduation time -- exactly the kind of "what depends on the model remembering will eventually be forgotten" failure (the design's own stated governing principle, `design/feedback-decision-log-convention-design.md:38`) that this convention exists to prevent.

**Evidence:** `design/feedback-decision-log-convention-design.md:59` (Context field list, no author/participant); `research/feedback-decision-log-research.md:201,265` (DECISION entity `participants[]` requirement).

**Impact:** Blocks clean, lossless graduation from log entry to DECISION entity for any multi-operator/team adoption, and undermines the "Jerry convention" (multi-user, general) framing the requirement explicitly asked for.

**Dimension:** Completeness.

**Response Required:** Add an optional `author`/`participant` component to the Context line (default: the session's sole known operator, so the current single-user case incurs zero added burden), documented as required for team/multi-operator adoption.

**Acceptance Criteria:** The Context schema in the design doc and both templates lists an `author`/`participant` field (may default to a single implicit value), with a one-line note on multi-operator usage.

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- DA-001: Specify the concurrency-safe id-minting mechanism (or narrow the "cannot collide" claim to its true scope: single-writer append discipline). Acceptance: see [DA-001](#da-001-cannot-collide-id-minting-claim-has-no-concurrency-mechanism-critical).
- DA-002: Add the ambiguous-alias-reference disambiguation protocol + worked example. Acceptance: see [DA-002](#da-002-no-resolution-procedure-for-a-later-bare-alias-back-reference-critical).

**P1 (Major -- SHOULD resolve; require justification if not):**
- DA-003: Document Segment Index compaction or explicitly disclose the boundary condition as an accepted, evidence-based limitation. Acceptance: see [DA-003](#da-003-segment-index-is-itself-unbounded-and-lives-inside-the-very-cap-it-protects-major).
- DA-004: Add the FEEDBACK-LOG `alias: —` fallback + worked example. Acceptance: see [DA-004](#da-004-feedback-log-schema-has-no-defined-no-operator-label-fallback-major).
- DA-005: Add an optional author/participant Context field. Acceptance: see [DA-005](#da-005-no-authorparticipant-identity-field-major).

**P2 (Minor -- MAY resolve; acknowledgment sufficient):**
- DA-006: Add one line clarifying that cross-segment content search is expected via Bash `grep` (not the Read tool), to make the existing implicit mitigation explicit. Acknowledgment sufficient.
- DA-007: Note that the L5 id-integrity lint is the sole correctness backstop for manual rotation, and that this is an accepted MEDIUM-tier tradeoff. Acknowledgment sufficient.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002 (no back-reference protocol), DA-003 (index growth unaddressed), DA-004 (no-alias fallback missing), DA-005 (no author field) all identify unaddressed scope gaps |
| Internal Consistency | 0.20 | Negative | DA-001: the "cannot collide" claim is inconsistent with the complete absence of a supporting concurrency mechanism, in a project whose own history demonstrates the triggering concurrency pattern |
| Methodological Rigor | 0.20 | Negative | DA-007: rotation correctness relies solely on post-hoc lint with no in-process check; otherwise the 5-step method (cap derivation, id scheme, examples) is well-executed |
| Evidence Quality | 0.15 | Negative | DA-001 and DA-003 both involve unconditional claims ("cannot collide", "keeps every log loadable") that are not qualified against the scenarios that break them, despite the deliverable otherwise being strong on cited evidence (PM-001 truncation numbers, tiktoken counts) |
| Actionability | 0.15 | Negative | DA-002, DA-006: no defined operator/assistant procedure for ambiguous back-references or cross-segment search |
| Traceability | 0.10 | Negative | DA-004: schema and worked examples trace to one individual's documented habit rather than to a generalized adopter population, undercutting the "Jerry convention" (framework-wide) framing |

**Overall assessment:** Major/targeted revision required. Both Critical findings (DA-001, DA-002) are addressable without new machinery -- a documented discipline/scope statement (DA-001) and a disambiguation protocol plus one worked example (DA-002) -- consistent with the deliverable's own anti-bloat doctrine. Major findings (DA-003 to DA-005) are one-line schema additions or explicit disclosures, not structural rework. This deliverable should NOT proceed to S-014 scoring until P0 items are addressed per H-13/H-14.
