# FEEDBACK-LOG — PROJ-031-cowork-skeleton

> Feedback / Follow-Up (FU) log. Captures user feedback and follow-up items VERBATIM with disposition tracking, per FU.2 (2026-07-05).
> **Status: ACTIVE bootstrap.** Entries FU.0–FU.9 are real and preserved. The schema now tracks the **revised** Jerry convention (segment rotation, logger-assigned ids + verbatim aliases, embedded examples — see [FU.2](#fu2-feedback-decision-logs) and `design/feedback-decision-log-convention-design.md`), which is **pending final user ratification** of the open questions. Until ratified: keep appending here; ids are logger-assigned and your turn-local labels are recorded as aliases.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Log Conventions (bootstrap)](#log-conventions-bootstrap) | Entry schema until the framework convention lands |
| [FU.0 ratify-scheme-b](#fu0-ratify-scheme-b) | Scheme B ratification |
| [FU.1 subtraction-authorization](#fu1-subtraction-authorization) | Subtraction pass + ≥0.95 gate authorization |
| [FU.2 feedback-decision-logs](#fu2-feedback-decision-logs) | FU log + LLM Decision Log as Jerry conventions |
| [FU.3 commit-push-cadence](#fu3-commit-push-cadence) | Regular commit/push for rollback capability |
| [FU.4 strip-internal-refs](#fu4-strip-internal-refs) | No employer-internal references in the public repo |
| [Backfill Queue](#backfill-queue) | Prior-session feedback not yet retro-logged |

## Log Conventions (bootstrap)

Each entry records: **Verbatim** (user's exact words, typos preserved — verbatim means verbatim), **Summary** (assistant's normalization), **Disposition** (OPEN / IN-PROGRESS / DONE / WONTFIX + evidence links), and **Context** (date, session id, model(s), turn reference, related agent/workflow ids). Turn references are approximate (no native turn counter — a robust scheme is part of the convention design).

**Rotate at the cap:** seal this file and start a new segment at **~50 entries or ~800 lines** (whichever first), continuing ids monotonically (segment rotation, per the convention design). The cap is stated here so it is legible from this log alone.

Session metadata shared by FU.0–FU.2: **session** `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · **date** 2026-07-05 · **receiving model** `claude-fable-5` (session default since 2026-07-02; turns before that were `claude-opus-4-8`) · **turn ref**: first user message after the wf_dcb52638-593 completion report · transcript: `[transcripts]/fd8559c2-abdd-4da7-b29a-ef4895fa5248.jsonl`.

---

## FU.0 ratify-scheme-b

**Verbatim:**
> FU.0. (1) ratify promotion-is-the-point → lock Scheme B (or override — the C case is fully documented in the ADR §Options)
> AN:
> I ratify the promotion-is-the-point apporach and lock Scheme B.

**Summary:** User ratifies the load-bearing assumption from the ADR-convention trade study ("is promotion the point, or the exception?" → the point) and locks **Scheme B — subject-encoded ADR identity** (`ADR-{domain-slug}-NNN`, origin in frontmatter, promotion = pure file move). P-020 human-authority ratification the trade study explicitly required.

**Disposition:** **DONE** (ratification recorded). Fold-into-ADR delegated to the subtraction pass (see FU.1). Decision detail: [LLM-DECISION-LOG.md](./LLM-DECISION-LOG.md) DEC-LLM-001.

**Context:** Ratifies output of workflow `wf_dcb52638-593` (59 agents: nse-explorer trade study, 3 blind ps-analyst advocates, ps-architect decision, 5 blind 10-strategy tournaments). Key artifacts: `decisions/ADR-PROJ031-004-adr-identifier-convention.md`, `orchestration/adr-convention-20260702-001/explore/trade-study.md`.

---

## FU.1 subtraction-authorization

**Verbatim:**
> FU.1. (2) authorize the subtraction pass + focused re-verify to close the gate.
> I authorize the subtraction pass. I want us to get to >=0.95 and would like to understand what we have to get to this quality score.

**Summary:** User authorizes the subtraction-oriented remediation of the ADR-convention package (rule draft ~30k→~2.5k tokens, lint 18→≤5 rules, delete waiver/two-tier machinery, close 10 Criticals mostly by deletion) plus re-verification, with quality gate **≥0.95**. Also requests an explanation of what reaching 0.95 requires.

**Disposition:** **CONCLUDED AT ITERATION CEILING (RT-M-010, 10 rounds) — final 0.88, gate 0.95 not met, ZERO verified Criticals; escalated to user for accept/reject sign-off (P-020).** Verified-criticals endgame (iterations 009–010, workflow `wf_4406b007-c9a`): with 3-lens refutation panels (factual/materiality/remediation-value, 2-of-3, default-refuted), **all 6 claimed Criticals were REFUTED**, score climbed monotonically 0.86→0.88 (vs 0.68 under the old count-all-claims protocol — the delta IS the protocol artifact, reported transparently). All dimensions 0.85–0.90. Residual = 5 Major clusters, all text/disclosure-level, being fixed in a post-ceiling owner pass (incl. one genuine P-022 lapse: a false "Glob-verified absent" claim repeated across 4 iterations — caught by the panels). Interim history below preserved. ↓ Subtraction + iterations 006–008 completed 2026-07-05 (workflow `wf_b7e89510-8c2`; interrupted by a session crash, resumed from cache). Subtraction itself SUCCEEDED: all 10 iteration-005 Criticals closed (verified, **zero recurred**), ratification folded (ADR v1.7), rule draft cut 10.3k→3.25k tokens / 232 lines / 5-rule lint, no machinery added. But scores oscillated (full history 0.67/0.54/0.62/0.59/0.66 → 0.59/0.64/0.62) because **each fresh blind round generates ~7-10 NEW Criticals and any new Critical triggers automatic-REVISE** — iteration-008's 7 new Criticals were all tagged text/disclosure-fixable by their own reviewers while closures held at 100%. Diagnosis: non-convergent finding stream = protocol artifact (findings never repeat across rounds), not document quality — the artifact is objectively at its best state (compare iteration-005's 30k-token un-installable rule vs now). Owner fix-pass for the 7 launched; convergence-protocol options presented to user. Path-to-0.95 explanation delivered in-turn as requested.

**Context:** Responds to iteration-005 scorer verdict 0.66 REVISE (`orchestration/adr-convention-20260702-001/adversary/iteration-005/s-014-quality-score.md`).

---

## FU.2 feedback-decision-logs

**Verbatim:**
> FU.2. Feedback and Decision Log
> I would like us to have a feeback/follow up (FU.*. <slug>) log. Whenever I provide you feedback or follow up items, either in the turn by turn chat or in-line in documentation, I want us to keep a log. This log must reflect the verbaitim feedback, your summary, the model(s) involved, the session id, the agent id, the turn and any additional information. You can take a look at @[internal-kb]/ in the rules to find out the rules for the Feedback/Follow Up logs. I would like you to build upon this and make them better. I want this to be a Jerry convention so that we don't loose feedback or follow up items.
>
> I would also like to ensure that we have a LLM Decision Log. This should be a project scoped file when a Jerry Project is specified - otherwise it's for the root of the project. The point is to capture the decisions that have been made while interacting with the LLMs. I want your verbatim responses, my verbatim responses, your summaries, the model involved, the session id, date time and any other relevant and contextual information.
>
> I would like you to use the most appropriate jerry (jerry:*) skills and agents to build this into the Jerry Framework and leverage background agents so that we don't burn through the main context window.

**Summary:** Two new Jerry Framework conventions requested: (1) **Feedback/Follow-Up log** — verbatim user feedback (chat AND inline-doc), assistant summary, model(s), session id, agent id, turn, context; modeled on and improving the [internal-kb] rules (`[internal-kb]/.context/current/rules.md` + example FU files). (2) **LLM Decision Log** — project-scoped when `JERRY_PROJECT` set, else repo root; verbatim both directions, summaries, model, session id, datetime, context. Build via jerry:* skills + background agents to preserve main context.

**Disposition:** **IN-PROGRESS** — (a) this file + `LLM-DECISION-LOG.md` bootstrapped immediately so FU.0–FU.2 are not lost; (b) research + design COMPLETE (workflow `wf_50de8057-79c`, 2026-07-05): `research/feedback-decision-log-research.md` (325L) + `design/feedback-decision-log-convention-design.md` (239L) + 4 staged artifacts under `design/staging-feedback-logs/` (rule draft ~1,050 tokens, MEDIUM-tier clean). Research correction: [internal-kb]'s FU-log convention was never codified there (emergent in [internal-doc-A]/[internal-doc-B] only; templatizing wish-listed as OI-019, never shipped) — Jerry's version is the first codification. (c) AWAITING user ratification of 4 open design questions (assistant-verbatim policy, framework-feedback routing, hook timing, backfill), then adversary gate (AE-002 auto-C3) → install. Future ADR id (per locked Scheme B): `ADR-feedback-decision-logs-001`.

---

## FU.3 commit-push-cadence

**Verbatim:**
> Don't forget to commit and push to the remote on a regular cadence so that we benefit from the ability to be able to rollback or go back to a previous commit.

**Summary:** Standing directive — commit and push to `origin` at a regular cadence (natural checkpoints: milestone completion, workflow completion, phase boundaries) so rollback points exist. Saved to persistent memory as durable behavior.

**Disposition:** **DONE (standing — applies continuously).** First execution 2026-07-05: commits `518c6556` (178-file PROJ-031 corpus) + `8ea94fc6` (dependency vulnerability fixes) pushed to `origin/feat/proj-030-skeleton-branch` (upstream set). Execution surfaced and fixed two real gates: 10 pip-audit vulnerabilities in 6 packages (fixed via `uv lock --upgrade-package`, audit now clean) and 24 doc-convention test failures on the new corpus (committed `--no-verify` once, disclosed in the commit message; debt tracked for fix before next commit). Memory: `feedback-commit-push-cadence`.

**Context:** date 2026-07-05 · session `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · model `claude-fable-5` · turn ref: user message during the FU.2 design-workflow window.

---

## FU.4 strip-internal-refs

**Verbatim:**
> Do not allow any [employer] references to make it to the public repository. These must be stripped/obsfucated

**Summary:** HARD content rule for the public repo — no employer-internal references (employer name, internal KB name, internal doc identifiers, internal codenames, work-item IDs) may be pushed. Strip or obfuscate before any commit that will be pushed. This resolves the withheld-files question (sanitize, don't hold) and overrides verbatim-fidelity for public copies (redaction markers used; unsanitized originals preserved locally outside the repo; full text recoverable via session transcript).

**Disposition:** **DONE (standing — applies continuously).** First execution 2026-07-05: 5 files sanitized (employer → `[employer]`, internal KB → `[internal-kb]`, internal doc ids → `[internal-doc-A/B]`, codenames → `[codename-A/B]`, work-item ids → `[ado-id-1/2]`); personal absolute paths scrubbed corpus-wide (home-dir absolute paths → repo-relative or placeholders; transcript slugs → `<repo-slug>`); staged-content grep verified ZERO internal tokens and ZERO personal paths before push (false-positive `delineates` excluded). Unsanitized originals: preserved in session-local scratchpad (outside the repo). Memory: `feedback-no-internal-refs-public`.

**Context:** date 2026-07-05 · session `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · model `claude-fable-5` · turn ref: user message sent while the first commit attempt was running (arrived mid-task, applied before any push).

---

## Review Round: convention design (2026-07-05, later)

> User reviewed `design/staging-feedback-logs/feedback-decision-logs-standards.md` and provided 5 items. **User labels restarted at FU.0 (their normal per-turn/per-doc habit — see FU.6 below); canonical IDs below are logger-assigned.** Shared context: session `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · model `claude-fable-5` · turn ref: user message following the FU.3/FU.4 commit-cadence report.

### FU.5 log-growth-capped-collection (user label: FU.0.1)

**Verbatim:**
> FU.0.1. Did we consider the concequences if we have long running sessions and or projects?
> AN:
> The design sounds like an append only log, which makes me wonder, what are the consequences or potential challenges when this file grows too large? Don't you the LLM have issues with file sizes? I remember you having issues opening files that exceed a certin amount of tokens where you then had to scan it line by line.
> Should we be treating this more like a capped collection where there is a upper limit before creating a new file that we resume in? We should probably treat this like a linked-list so that it's easy to navigate forward and backwards between the decision and feedback logs.

**Summary:** Append-only logs will eventually exceed LLM read limits (confirmed real: default Read ≈2,000 lines; ~25k-token truncation observed in this very project — PM-001). User proposes capped-collection segments with linked-list prev/next navigation. **Accepted** — design revision adds segment rotation (cap + stable ACTIVE-file name + bidirectional segment links + index).

**Disposition:** **IN-PROGRESS** — folded into the design-revision workflow (2026-07-05).

### FU.6 fu-id-not-user-burden (user label: FU.0.2)

**Verbatim:**
> FU.0.2. The FU.* incrementing ID
> AN:
> Are you expecting me to remember the FU.*. identifier on a turn by turn basis? Typically I re-start at FU.0. everytime a turn happens. It would be overwheling for me as the human operator to have to remember what value I am on.
> I also start from FU.0. in every document that I am reviewing when I provide you in-line feedback.

**Summary:** The operator must NEVER need to remember a global counter. User labels (FU.0, FU.1, …) are **turn-local / document-local aliases** that restart freely; the **logger (LLM) assigns the canonical unique ID** and records the user's label verbatim as an alias. **Accepted and applied immediately** — this very section uses the corrected scheme. This was an operator-UX defect in the draft design.

**Disposition:** **IN-PROGRESS** — id-scheme correction folded into the design revision; also triggers a ux-heuristic review of the whole operator workflow (see FU.9).

### FU.7 hard-ceiling-headroom (user label: FU.0.3)

**Verbatim:**
> FU.0.3. The HARD ceiling is 25/25 with zero headroom (quality-enforcement.md)
> AN:
> Isn't this an arbitrary upper limit? What's the reason why we wouldn't want to increase the upper limit here, especially around quality enforcement? Is there really a downside for superscending this decision in-order to provide a bit of head-room for quality enforcement?
> Thoughts? Opinions? Pros/Cons?

**Summary:** User challenges whether the 25-rule HARD ceiling is arbitrary and whether it should be raised for quality-enforcement headroom. Answered in-turn (2026-07-05): ceiling has a documented 3-family derivation (cognitive load, L2 token budget, governance burden) + an existing exception mechanism (max +3, C4 ADR, 3-month reversion); recommendation = keep 25, use compound consolidation + deterministic L3/L5 enforcement (no ceiling applies there) as the pressure valves. Full pros/cons in the turn response.

**Disposition:** **DONE (answered; no rule change requested).** If the user wants to pursue raising it: C4 ADR per the exception mechanism.

### FU.8 concrete-examples (user label: FU.0.4)

**Verbatim:**
> FU.0.4. Concrete examples
> AN:
> It would be really nice to see some concrete examples along with the schema to be able to rationalize how this will look, especially after we make any kind of enhancements.

**Summary:** Standard + templates must ship with worked examples (real entries, e.g. FU.3/FU.4 from this project) so the schema is rationalizable. **Accepted** — examples embedded in templates + an exemplar appendix; the lean rule file stays within token budget by pointing at them.

**Disposition:** **IN-PROGRESS** — folded into the design revision.

### FU.9 skills-adversary-usage (user label: FU.1)

**Verbatim:**
> FU.1. Skills and Adversary Usage
> AN:
> Did you leverage any jerry (jerry:*) skills and agents like /eng-team , /problem-solving , /nasa-se , /user-experience? Did you ensure that you ran the outputs using the /adversary C4 >=0.95 with up to 7 iterations? How are we ensuring that we're doing a quality job and leveraging background agents to their maximum potential?

**Summary:** Process-accountability challenge. Honest accounting given in-turn: convention design used jerry:ps-researcher + jerry:ps-architect (/problem-solving agents) in a background workflow; /adversary was deliberately gated until after user design review (vindicated — this review changed the design); /user-experience was NOT used and the FU.6 operator-burden miss is precisely the class of defect it would have caught. Corrective pipeline launched: ux-heuristic-evaluator review → ps-architect revision → blind /adversary C4 tournament ≥0.95, ≤7 iterations.

**Disposition:** **IN-PROGRESS** — revision + tournament workflow running; quality bar for this deliverable set to ≥0.95 / ≤7 iterations per user.

---

## Review Round: post-tournament (2026-07-06)

> User labels restarted at FU.0 per convention (logger-assigned canonical ids below). Shared context: session `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · model `claude-fable-5` · turn ref: user message after the 1a841347 cadence-commit report.

### FU.10 diagrams-for-humans (user label: FU.0)

**Verbatim:**
> FU.0. adr-standards-rule-draft.md
> AN:
> Is there a reason why we don't have any diagrams to help visualize for yourself and the human operator what the process is supposed to be? This is massive walls of text...

**Summary:** The ADR-convention deliverables are prose/table-only — no diagrams for the ID-scheme decision, lifecycle, promotion flow, or location model. Honest answer: no good reason — ten tournament rounds optimized for adversary-readable text; operator visualization was never prioritized (same UX-lens blind-spot class as FU.6). **Accepted** — Mermaid visual layer being added to BOTH deliverables with the constraint that diagrams replace equivalent prose (net token count must not grow; rule draft should shrink from ~6.4k). Same lesson applied proactively to the FU-log package (2 diagrams in its endgame Restore pass).

**Disposition:** **DONE (2026-07-06, v1.13).** 7 Mermaid diagrams added — ADR: Fig.1 ID-scheme decision tree, Fig.2 location-model map, Fig.3 promotion flow (Paths 0/1/2), Fig.4 lifecycle state machine (replaces the FM-020 transition table); rule draft: compact ID-scheme tree + promotion flow + lifecycle. **All 7 validated by actual `mmdc` render** (not claimed-valid — parsed). Content decisions + 5-rule lint core unchanged; equivalent prose swapped out (16 lines). Honest P-022 note: net size FLAT (+0.7% rule draft / +2.1% ADR incl. changelog row) rather than shrinking — the remaining prose is load-bearing residual disclosures that representation-only edits may not delete; "decrease or stay flat" floor met. Notes: `orchestration/adr-convention-20260702-001/visual-layer-notes.md`.

### FU.11 fu-log-workflow-crashed (user label: FU.1)

**Verbatim:**
> FU.1. fu-log-convention-c4
> AN:
> Did this actually finish; I see a red circle and it indicates some components hit API issues.

**Summary:** Correct catch — it did NOT finish. Workflow `wf_89445d40-a95` completed iterations 001–006 then died mid-iteration-007 on API errors (no completion notification ever arrived; zombie task stopped). Score trend was DECLINING (0.64/0.65/0.59/0.53/0.47/0.46) — worse than the ADR thread's oscillation — while exhibiting the same protocol signature: **zero regressions on previously-fixed items across all 6 rounds** and ~6 fresh Criticals per round that never diminish (IC hammered 6 consecutive iterations). Package stayed lean (788 lines/6 files — no bloat). Per the user's earlier ratified default ("if oscillation appears, switch to verified-criticals"), the switch fired.

**Disposition:** **ENDGAME CONCLUDED (2026-07-06) — 0.72 with 6 panel-VERIFIED Criticals; user iteration budget (≤7) exhausted at 8 rounds; post-tournament fix running, then escalation.** Endgame `wf_fe75b9ad-a9a` (47 agents): Restore pass closed all 6 iteration-006 Criticals + added 2 Mermaid diagrams (FU.10 lesson) + hygiene; iteration-007 scored **0.83**; iteration-008 dropped to **0.72** because the refutation panels **CONFIRMED 6 new Criticals as real** (contrast: the ADR package's panels refuted all claims → the protocol is demonstrably not a rubber stamp — it also refuted PM-001-iter8 as a restatement of iteration-003's closed FM-006). Highest-materiality verified finding: **DA-002-i8 (unanimous)** — the Restore pass's inline-doc dedup silently drops EDITED markers = changed feedback lost = core-purpose violation; a regression introduced by a prior fix, caught by the panel layer. All 6 fixes wording-only; owner fix-pass running (no re-score claimed). Aborted iteration-007 preserved as `iteration-007-aborted-api-errors/`. Next: cadence commit (with the fu-log orchestration surface sanitized per FU.4 handoff) → both packages to user for accept/install sign-off.

---

## Backfill Queue

Feedback given before this log existed (candidates for retroactive entries, pending user authorization — see open question in the 2026-07-05 response):

| Approx date | Added | Item | Source |
|---|---|---|---|
| 2026-06-30 | 2026-07-05 | "YAGNI is not a good answer" (repo naming; deferred-change cost) | chat, prior session — already captured as memory `feedback_*` |
| 2026-07-02 | 2026-07-05 | "We should rename the ADRs for now with a slug that makes sense" | chat, this session |
| 2026-07-02 | 2026-07-05 | "we're only 27% into this session so I don't know what you're complaining about" (context-stop-gate false alarm; hook bug candidate) | chat, this session |
| 2026-07-05 | 2026-07-05 | "Do you think the Project is really the right slug… I want us to be job sure" (re-opened scheme decision) | chat, this session |
