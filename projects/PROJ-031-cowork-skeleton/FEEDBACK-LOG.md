# FEEDBACK-LOG — PROJ-031-cowork-skeleton

> Feedback / Follow-Up (FU) log. Captures user feedback and follow-up items VERBATIM with disposition tracking, per FU.2 (2026-07-05).
> **Status: BOOTSTRAP format.** The canonical Jerry convention (schema, id scheme, hook-assisted capture) is being designed — see [FU.2](#fu2-feedback-decision-logs) — and this file migrates to it once ratified. Until then: entries follow the user's own `FU.N. <slug>` labeling.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Log Conventions (bootstrap)](#log-conventions-bootstrap) | Entry schema until the framework convention lands |
| [FU.0 ratify-scheme-b](#fu0-ratify-scheme-b) | Scheme B ratification |
| [FU.1 subtraction-authorization](#fu1-subtraction-authorization) | Subtraction pass + ≥0.95 gate authorization |
| [FU.2 feedback-decision-logs](#fu2-feedback-decision-logs) | FU log + LLM Decision Log as Jerry conventions |
| [Backfill Queue](#backfill-queue) | Prior-session feedback not yet retro-logged |

## Log Conventions (bootstrap)

Each entry records: **Verbatim** (user's exact words, typos preserved — verbatim means verbatim), **Summary** (assistant's normalization), **Disposition** (OPEN / IN-PROGRESS / DONE / WONTFIX + evidence links), and **Context** (date, session id, model(s), turn reference, related agent/workflow ids). Turn references are approximate (no native turn counter — a robust scheme is part of the convention design).

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

**Disposition:** **IN-PROGRESS** — subtraction + blind tournament iterations 006–008 workflow launched 2026-07-05 (id recorded in LLM-DECISION-LOG DEC-LLM-002 when assigned). Path-to-0.95 explanation delivered in-turn (levers: zero unresolved Criticals [automatic-REVISE rule], IC ≥0.9 via machinery deletion, PM-001 token budget, IN-013-005 lint scope, claim/reality alignment, preserve EvidQual/Trace strengths).

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

## Backfill Queue

Feedback given before this log existed (candidates for retroactive entries, pending user authorization — see open question in the 2026-07-05 response):

| Approx date | Item | Source |
|---|---|---|
| 2026-06-30 | "YAGNI is not a good answer" (repo naming; deferred-change cost) | chat, prior session — already captured as memory `feedback_*` |
| 2026-07-02 | "We should rename the ADRs for now with a slug that makes sense" | chat, this session |
| 2026-07-02 | "we're only 27% into this session so I don't know what you're complaining about" (context-stop-gate false alarm; hook bug candidate) | chat, this session |
| 2026-07-05 | "Do you think the Project is really the right slug… I want us to be job sure" (re-opened scheme decision) | chat, this session |
