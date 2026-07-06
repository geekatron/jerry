# Research: Feedback/Follow-up Log + LLM Decision Log Convention

> **PS Context:** PROJ-031-cowork-skeleton · Research feeding the FU.* + LLM-Decision-Log Jerry convention design (user requirement FU.2, 2026-07-05).
> **Agent:** ps-researcher (divergent, opus) · **Status:** draft (P-020: nothing here writes into framework paths; all output under `projects/PROJ-031-cowork-skeleton/`).
> **Method:** Direct source extraction (Read/Grep/Glob) of the [internal-kb] reference repo + the Jerry codebase. Verbatim quotes carry file paths; inference is labelled `[INFERENCE]`.

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What [internal-kb] defines, one-paragraph critique, what is automatable in Jerry |
| [L1: Technical Findings](#l1-technical-findings) | Verbatim [internal-kb] rules/schema appendix + Jerry mechanism inventory with citations |
| [L1.A [internal-kb] prior art (verbatim)](#l1a-internal-kb-prior-art-verbatim) | The three-log system, ID scheme, lifecycle, verbatim capture, decision journal |
| [L1.B Jerry mechanism inventory](#l1b-jerry-mechanism-inventory) | Hooks + stdin fields, DECISION entity, transcript reality, bootstrap files, adjacent conventions |
| [L2: Design Implications](#l2-design-implications) | Automatable-metadata table, boundary with DEC-NNN, turn-reference options |
| [References](#references) | Source files with paths |

---

## L0: Executive Summary

**What [internal-kb] defines.** The user's reference repo ([internal-kb]) has an *emergent, un-codified* three-artifact pattern that lives per-PDD (never as a global rule or template). (1) A **`feedback-log.md`** ("Feedback & Follow-up Log") tracks maintainer review feedback to closure, organised into **rounds**, with each item keyed **`R{round}-FU.{n}`** and a status legend (Addressed / In progress / Planned / Deferred / Gating). (2) A sibling **`feedback/round-{N}-verbatim.md`** captures the maintainer's words **verbatim** with YAML frontmatter (`artifact_type, round, captured, source, status`) — the "verbatim file wins" fidelity guarantee. (3) An **`llm-decision-journal.md`** records the LLM<->maintainer decision dialogue as **`DJ-NNN`** entries whose template *already* carries `Provenance: <user> · <model-id> · session <session-id>`, plus Status / Type / Confidence / Reversibility / "Reflected in". Decision-bearing items **graduate** verbatim -> feedback-log -> DJ-NNN -> ratified **`DEC-NNN`** in `decisions.md`. Precedence: formal artifact wins over journal; **verbatim wins over everything.**

**One-paragraph critique.** The pattern is genuinely good raw material — directional separation (maintainer->LLM vs LLM<->maintainer vs ratified), a verbatim fidelity guarantee, a graduation chain, decision-quality signals (Confidence + one-way/two-way-door Reversibility), and provenance fields that already name the model and session. But it is **entirely manual and un-enforced**: a repo-wide grep finds **zero** references to it in `rules.md`, skills, standards, or templates; it was only ever "templatize this" wish-listed as `OI-019`. The manual numbering has already drifted in the wild — `DJ-025` carries a note that a reconcile brief mis-numbered it "DJ-021" because `DJ-021..024` already existed. Model/session provenance is hand-typed and inconsistent (real `claude-opus-4-8` in one entry, a prose label `session (2026-06-10 eng-arch reconciliation)` in another), which is exactly the metadata a human forgets. There is **no turn concept**, rounds must be manually declared (awkward for continuous turn-by-turn feedback), and the whole thing is bound to the PDD artifact type — there is no project-scoped-or-root instance the user's requirement calls for.

**What is automatable in Jerry.** The forgettable, drift-prone metadata is exactly what a Jerry **hook** can stamp deterministically. Jerry's `UserPromptSubmit`, `Stop`, `SessionStart`, and `PreCompact` hooks each receive JSON on stdin containing **`session_id`**, **`transcript_path`**, **`cwd`**, and **`hook_event_name`** (verified in `hooks/session_start.py` and the settings wiring). The `transcript_path` points at the session JSONL whose messages carry stable **`uuid`** / **`parentUuid`** fields and per-line offsets — the only stable "turn" references that exist (there is no native turn number). So: session id, transcript path, timestamp, project id, and a resolvable message-uuid anchor are **harness-automatable**; the model id is available at message granularity inside the transcript JSONL (label `[INFERENCE]` where the hook stdin does not directly carry it). Verbatim text, the human summary, and disposition remain model/human-authored. The new convention should keep DJ-NNN's decision journal **distinct** from the worktracker `{ParentId}--DEC-NNN` entity (design decisions with lifecycle), positioning the LLM-Decision-Log as the *dialogue capture* that can graduate into a formal worktracker DECISION.

---

## L1: Technical Findings

### L1.A [internal-kb] prior art (verbatim)

> **Root:** `[internal-kb]`. **Codification status: NONE.** `grep -rn -iE "feedback.?log" .context .claude` returns **zero** hits; the pattern exists only as instantiated artifacts inside two PDDs ([internal-doc-A], [internal-doc-B]) and is wish-listed for templatizing as `OI-019` (see below). It is NOT in `rules.md`, NOT a skill, NOT a template.

#### The "known example" paths are a red herring

The two files named as known examples in the task —
`/.../codename-a/infrastructure/rate-limiting/[ado-id-1]-follow-up-cloudops-rate-limiting.md` and
`.../native-grpc/[ado-id-2]-follow-up-cloudops-grpc.md` — are **NOT feedback-log entries**. They are Azure DevOps work-item mirror files (a PBI titled "Follow up on investigations CloudOps is doing"), e.g. verbatim:

```
# Follow up on investigations CloudOps is doing
**ADO ID:** [[ado-id-1]]  **Type:** Product Backlog Item  **State:** New
**Parent Feature:** [681340] - Rate Limiting for APIs in Platform
**Last Synced:** 2025-12-19
## Description
Track and follow up on CloudOps investigations related to API rate limiting.
```
Path: `.context/current/planning/development/codename-a/infrastructure/rate-limiting/[ado-id-1]-follow-up-cloudops-rate-limiting.md`. These are ADO-sync artifacts using "follow up" in the ordinary sense, unrelated to the FU.* feedback convention.

#### The REAL reference implementation (two PDD instances)

- `docs/tag/pdds/[internal-doc-A]/feedback-log.md` (+ `feedback/round-{1..5}-verbatim.md`, `llm-decision-journal.md`, `decisions.md`)
- `docs/tag/pdds/[internal-doc-B]/feedback-log.md` (+ same siblings)

**Artifact 1 — `feedback-log.md` header + strategy (verbatim, [internal-doc-B]):**
```
# Feedback & Follow-up Log
| **Project** | ... | **Last Updated** | 2026-06-11 |
| **Purpose** | Running, durable log of maintainer/stakeholder review feedback so every point is tracked to closure and nothing is lost. |

## How this works (the strategy)
- Feedback arrives in **rounds** (one per review pass). Each item gets a stable ID **`R{round}-FU.{n}`**
  (the maintainer's `FU.n` numbering resets each round, so the round prefix disambiguates).
- **The maintainer's raw feedback is captured VERBATIM** (word-for-word, never paraphrased) in
  `feedback/round-{N}-verbatim.md` — that is the fidelity guarantee. **This log** then tracks each item's
  **status** + **resolution** (commit hash, file, or "folds into X"). If the verbatim file and a summary
  here ever disagree, **the verbatim file wins.**
- **Decision-bearing** items also graduate into the LLM Decision Journal as a `DJ-NNN` entry; a decision that
  is ratified there graduates further into a `DEC-NNN` in decisions.md. The chain is:
  *verbatim -> feedback-log (this file) -> decision-journal (if decision-bearing) -> decisions.md (if ratified)*.
  The formal artifact (decisions.md) wins over the journal on conflict; the verbatim wins over everything.
- A round is **not closed** until every item is `Addressed` or explicitly `Deferred` (with a reason).

**Status legend:** Addressed · In progress · Planned (scheduled, not started) · Deferred · Gating (blocks a downstream step)
```
(Emoji glyphs in the source: ✅ Addressed · ⏳ In progress · 📋 Planned · ⏸ Deferred · 🔒 Gating.)

**Round structure (verbatim excerpt, [internal-doc-B] Round 5):** each round is a `## Round {N} — {date} ({STATE})` heading, a `> Verbatim:` pointer line naming the source + which DJ it graduated to, then a table `| Item | Maintainer ruling (see verbatim) | Status | Resolution |`, then a bold `**Round {N} gate:**` closure line. Example rows:
```
| **R5-FU.1** (DEC-002) | "Document direction; stays OPEN" | ✅ | DEC-002 ... stays OPEN. → DJ-007 |
| **R5-FU.5** (process — scripts) | "update the vendored one in internal-kb..." | ✅ | corrections-render added to the vendored jerry_transcript_anchors.py ... |
```
[internal-doc-A] uses the identical schema; its Round 2 records the origin turn `R2-FU.13 | Need a running feedback log so points aren't lost | ✅ | **This file.**` and `R2-FU.14 | Address all R2 items before the C4 adversarial review | 🔒 | Adversary deferred until every R2 item is ✅.`

**Artifact 2 — `feedback/round-{N}-verbatim.md` (verbatim, [internal-doc-A] round-1 header):**
```
---
artifact_type: feedback-verbatim
round: 1
captured: 2026-06-04
source: "Maintainer (Adam Nowak) inline >AN: FU.0-12 annotations on the first design draft
         (preserved in git commit 01a19edc; recovered for the audit trail)"
status: CLOSED
---
# Round 1 — verbatim maintainer feedback
> Verbatim capture (recovered from git `01a19edc`). Resolution recorded in feedback-log.md (Round 1)...
## FU.0 — obligation vs advice
> Regarding obligations vs advice: in XACML, obligations are **mandatory** ...
## FU.1 — resource DRN shape
> Regarding: `drn:dws:inventory::computer:...` DRNs are tenanted, you are missing the fragments ...
```
Each `FU.n` is a `## FU.{n} — {slug}` heading followed by the maintainer's words as a blockquote, unedited. The inline annotation convention in the source doc is `>AN: FU.{n}. {text}` (maintainer initials `AN:`), later harvested into these files.

**Artifact 3 — `llm-decision-journal.md` (verbatim, [internal-doc-A] header + entry template):**
```
# LLM Decision Journal
| **Purpose** | Durable record of the **decision dialogue** between the LLM (Claude) and the maintainer —
  the questions/recommendations the LLM raised and the maintainer's rulings + rationale — so decisions
  made in working chat survive context compaction. |

## What this is (and how it differs from the other logs)
| Log | Direction | Captures |
| llm-decision-journal.md (this file) | LLM ⇄ maintainer | LLM questions/recommendations/options/pushback + maintainer rulings+rationale |
| feedback-log.md (+ feedback/)       | maintainer → LLM | maintainer review feedback, captured verbatim |
| decisions.md                        | —                | Formal, ratified DEC-NNN. Journal entries that harden graduate into a DEC. |
| outstanding-items.md                | —                | Open questions/concerns. A journal entry that surfaces one spawns an OI-NNN. |

**Scope — decision-bearing turns only.** ... **Not** every turn ...
**Conflict rule:** where a journal entry and a later formal artifact (DEC/OI) disagree, the formal artifact wins.

## Entry template (copy this for new entries)
### DJ-NNN — {short title}
| **Date** | YYYY-MM-DD |
| **Provenance** | <user> · `<model-id>` · session `<session-id>` |
| **Status** | Decided / Open / Revisit (<trigger>) / Superseded by DJ-NNN |
| **Type** | Recommendation / Question / Options / Correction |
| **Confidence** | LOW / MED / HIGH |
| **Reversibility** | Reversible (two-way door) / Hard-to-reverse (one-way door) |
| **Reflected in** | <commit(s) / DEC-NNN / OI-NNN / file / task> |
**Context.** ...  **What I raised.** ...  **Your decision.** ...  **Rationale.** ...  **Follow-ups.** ...
```
Real provenance values seen in-repo: `Adam Nowak · claude-opus-4-8 · session (2026-06-10 eng-arch reconciliation)` (DJ-025) vs. `... session <session-id>` template intent — i.e. the session field is sometimes a real-ish id, sometimes a prose label.

**Artifact 4 — `decisions.md` (verbatim, [internal-doc-A]): DEC-NNN with `Status: Proposed/Active/Superseded`, `Date`, `Decision Owner`, `Source Session`, then Decision / Rationale / Alternatives Considered / Cross-references.** This is the graduation target; it predates the FU/DJ pattern and has its own copy-template.

**`OI-019` (the templatize-this wish, verbatim from [internal-doc-A] R3-FU.0 / feedback-log):**
> "Restructured: raw feedback now captured word-for-word in `feedback/round-{1,2,3}-verbatim.md` ...; this log tracks resolution + defers to the verbatim on conflict. OI-019 filed to templatize this."
And [internal-doc-B] R1-FU.4 verbatim: *"Use **both** the Feedback/Follow-up Log **and** the LLM Decision Log for accountability, traceability, visibility."* — this is the user's own instruction that seeded the pattern.

#### Critique of the [internal-kb] pattern (steelman first, then gaps)

**Strongest form (what works):**
- **Directional separation** is genuinely clarifying: maintainer->LLM (feedback), LLM<->maintainer (journal), ratified (decisions). Each answers a different audit question.
- **Verbatim fidelity guarantee** with an explicit precedence rule ("verbatim wins") is exactly the anti-drift anchor the user asked for.
- **Graduation chain** (verbatim -> FU -> DJ -> DEC) prevents both loss (nothing dropped) and premature formalization (only ratified items reach DEC).
- **Decision-quality metadata** — Confidence + Reversibility (one/two-way door) — flags the "LOW-confidence + hard-to-reverse" entries that most need revisiting. That is more sophisticated than a bare decision log.
- **Provenance fields already name model + session**, proving the author wanted exactly the metadata the Jerry requirement lists.
- **Round-closure discipline** ("not closed until every item Addressed or Deferred-with-reason") makes "nothing is lost" enforceable at the round boundary.

**Gaps / weaknesses (what to make better):**
1. **Not codified, not enforced.** Zero references in `rules.md`/skills/templates; purely emergent in two PDDs. `OI-019` ("templatize into the PDD template") was filed but never shipped. -> Jerry should ship it as a real convention (rule + template) not a wish.
2. **Entirely manual -> real drift observed.** `DJ-025` documents an ID collision ("the brief named this DJ-021, but DJ-021..024 already exist"). Manual `NNN` numbering does not survive parallel/background agents. -> IDs and ordering need tooling.
3. **Model/session provenance is hand-typed and inconsistent.** `claude-opus-4-8` (good) vs `session (2026-06-10 eng-arch reconciliation)` (a prose label, not a UUID). This is the forgettable metadata that hooks should stamp.
4. **No turn concept.** "Round" is a coarse, manually declared review-pass grouping. The user's requirement explicitly includes **turn-by-turn chat** feedback, which rounds model poorly (a round assumes a review pass, not a live turn stream).
5. **Free-text prose drift between instances.** The two PDDs' "strategy" preambles, status legends, and gate lines are convergent but not identical (e.g., "C4 adversarial review" vs "C1 ([internal-kb]-strongest = Jerry-C4)"). Without a schema/template they will keep diverging.
6. **PDD-scoped only.** Bound to the PDD artifact type; there is no project-root or global instance. The user wants project-scoped when `JERRY_PROJECT` is set, else repo root.
7. **Capture trigger is human memory.** Someone must remember to open a verbatim file and mint the FU/DJ entry. No `UserPromptSubmit`/`Stop` automation appends anything — so the "don't lose feedback" goal depends on the very attention that gets lost under context pressure.

---

### L1.B Jerry mechanism inventory

> **Root:** `.`. All line citations verified against the files on this branch.

#### B.1 Hooks — lifecycle events and what actually arrives on stdin

`hooks/hooks.json` wires **six** Claude Code lifecycle events, each to a thin Python wrapper that pipes stdin into `uv run ... jerry --json hooks <event>` (the wrappers in `hooks/*.py` do `input=sys.stdin.buffer.read()`; they do not parse fields themselves — the real parsing is in `src/interface/cli/hooks/*`):

| Event | hooks.json matcher | Wrapper | Delegates to |
|-------|-------------------|---------|--------------|
| `SessionStart` | `*` | `hooks/session-start.py` | `jerry hooks session-start` |
| `UserPromptSubmit` | (all) | `hooks/user-prompt-submit.py` | `jerry hooks prompt-submit` |
| `PreCompact` | (all) | `hooks/pre-compact.py` | `jerry hooks pre-compact` |
| `PreToolUse` | `Write\|Edit\|MultiEdit\|NotebookEdit\|Bash` | `hooks/pre-tool-use.py` | `jerry hooks pre-tool-use` |
| `SubagentStop` | (all) | `hooks/subagent-stop.py` | `jerry hooks subagent-stop` |
| `Stop` | `*` | `hooks/context-stop-gate.py` | `jerry hooks stop` |

**Fields each handler actually reads from the JSON on stdin (proven in code):**

| Handler (`src/interface/cli/hooks/`) | Fields consumed | Cite |
|---|---|---|
| `hooks_session_start_handler.py` | `session_id` | line 136 (`hook_data.get("session_id", "")`) |
| `hooks_prompt_submit_handler.py` | `transcript_path` only | line 150 (`hook_data.get("transcript_path", "")`) — it estimates context fill from the transcript and returns `additionalContext`; it does **not** read the prompt text or `session_id` |
| `hooks_pre_compact_handler.py` | `transcript_path`, `session_id` | lines 130-131 |
| `hooks_subagent_stop_handler.py` | `session_id`, `agent_id`\|`agent_name`, `agent_type`, `agent_transcript_path`\|`transcript_path` | lines 101, 103, 104, 105-107 |
| `hooks_pre_tool_use_handler.py` | `tool_name`, `tool_input` | lines 128-129 |
| `hooks_stop_gate_handler.py` | **none** — reads only the Jerry context-state-file tier, ignores stdin entirely | lines 95, 111-123 |

**Load-bearing findings for automation:**
1. **`session_id` and `transcript_path` are reliably present** on hook stdin (SessionStart / PreCompact / SubagentStop carry `session_id`; UserPromptSubmit / PreCompact / SubagentStop carry a transcript path). These are the automatable anchors.
2. **No hook handler reads a `model` field.** `grep -rn '"model"' src/interface/cli/hooks` returns nothing; the only `model` reference in the hook/context path is `context_estimate_handler.py:281` `"model": agent.model` — that is the **Jerry agent-registry** model, not the live conversation model. **[INFERENCE]** Claude Code does not put the acting model on hook stdin for these events; the model is only discoverable by reading the transcript JSONL (see B.3). This is exactly why a hand-typed model field drifts.
3. **The UserPromptSubmit handler is a working precedent for the automation seam we need:** it already (a) receives `transcript_path`, (b) parses the transcript, and (c) returns injected text (`{"additionalContext": ...}`, line 194). A feedback/decision hook can piggyback on the same shape to *stamp* provenance without model cooperation.
4. **Fail-open discipline is the house style** — every handler swallows parse errors and continues (`except ... print(..., file=sys.stderr)`; Stop/SubagentStop wrappers even `print('{"decision":"approve"}')` on exception). Any capture hook must be fail-open too (never block a turn because logging failed).

#### B.2 Worktracker DECISION entity — the boundary to protect

- **Template:** `.context/templates/worktracker/DECISION.md`. **Entity id:** `{ParentId}:DEC-NNN` (frontmatter line 54, e.g. `EPIC-001:DEC-001`). **File name:** `{ParentId}--{DecisionId}-{slug}.md` (e.g. `EPIC-001--DEC-001-worktracker-planning.md`, `FEAT-001--DEC-001-id-scheme.md`) per `skills/worktracker/rules/worktracker-directory-structure.md:65,73`.
- **State machine:** `PENDING -> DOCUMENTED -> {ACCEPTED | SUPERSEDED}` with ACCEPTED/SUPERSEDED **terminal** (template lines 95-136).
- **Containment (strict):** allowed parents = Epic/Feature/Story/Enabler; **must** be co-located in the parent's folder; leaf node; `participants[]` **required**; validated at **L3 by AST (H-33)** (template lines 139-151, 366-372).
- **Internal structure:** `D-NNN` entries — Question/Context, Options Considered, Decision, Rationale, Date+Participants, Implications (lines 197-262).
- **Overlap alarm (verbatim from the template + directory rule):** DECISION.md exists "*For capturing decisions made during work, including user-agent discussions*" (line 9) and each Decision File "*documenting decisions between the User and Claude ... Captures decisions when Claude asks for clarification*" (`worktracker-directory-structure.md:65`). **This is the same problem space as the requested LLM Decision Log** — so the new convention MUST NOT re-implement or shadow it; it must define a crisp boundary and a graduation path (see L2/B-boundary).

#### B.3 Session/transcript reality — no native turn number

- **Location:** `[claude-home]/projects/<repo-slug>/<session-uuid>.jsonl`. Verified for this session: `.../<repo-slug>/fd8559c2-abdd-4da7-b29a-ef4895fa5248.jsonl` (11 MB). The `<repo-slug>` is the absolute cwd with `/` -> `-`. (Note: this install uses `.claude-geek`, not `.claude`.)
- **Format:** newline-delimited JSON, one record per line, **mixed record types** (histogram over the whole file): `assistant` 1110 · `user` 536 · `attachment` 410 · `system` 318 · `queue-operation` 274 · `last-prompt` 221 · `mode` 219 · `permission-mode` 219 · `ai-title` 218 · `file-history-snapshot` 49.
- **Substantive records** (`user`, `assistant`, `attachment`) carry: `uuid`, `parentUuid` (forms a parent-linked chain/DAG), `sessionId`, `timestamp` (ISO-8601 ms `Z`), `gitBranch`, `version` (Claude Code version, e.g. `2.1.193`), `cwd`, `isSidechain`, `userType`.
- **`user` records:** `message = {role:"user", content}` — **no model** (model is null on user turns); and crucially carry **`promptId`** (a UUID stable per user-prompt submission, e.g. `39f4a2fc-...`). Verified.
- **`assistant` records:** `message.model` **is populated** (e.g. `claude-opus-4-8`), plus `message.id` (`msg_...`), top-level `requestId` (`req_...`), and `message.usage` (token counts). **No `promptId` on assistant records** (it was null) — linking an assistant turn to its user prompt requires walking `parentUuid`.
- **There is NO native turn number anywhere.** The stable references that DO exist: `uuid` (per record), `parentUuid` (chain), `promptId` (per user prompt), `requestId`/`message.id` (per assistant response), `timestamp`, `sessionId`, and raw line offset (brittle). See L2 turn-reference options.
- **Subagents:** `isSidechain` is a real field (False on the main thread); no `isSidechain:true` record was found in this main transcript, consistent with subagent conversations living in **separate** agent transcripts — the `SubagentStop` handler reads `agent_transcript_path` precisely to reach them (B.1). So "which agent said what" is recoverable per-subagent-transcript, not from the main file alone.

#### B.4 Existing bootstrap instances (must be adoptable)

`projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` and `.../LLM-DECISION-LOG.md` already exist (created 2026-07-05, both flagged **"BOOTSTRAP format ... migrates to the ratified Jerry convention once designed"**). They already improve on [internal-kb] and encode design intent the convention should preserve:
- **FEEDBACK-LOG bootstrap schema:** per entry — **Verbatim** (typos preserved), **Summary**, **Disposition** (`OPEN / IN-PROGRESS / DONE / WONTFIX` + evidence links), **Context** (date, session id, model(s), turn ref, related agent/workflow ids); plus a shared session-metadata block and a **Backfill Queue** for pre-log feedback. It keeps the user's own `FU.N. <slug>` labeling and explicitly notes "*Turn references are approximate (no native turn counter — a robust scheme is part of the convention design).*"
- **LLM-DECISION-LOG bootstrap schema:** per entry — **Decision** (one line), **User verbatim** (full), **Assistant verbatim** (decision-relevant excerpt + transcript pointer; it flags "full multi-page turns would bloat the log; final policy is an open design question"), **Summary/consequences**, **Context** (datetime, session id, model, agent/workflow ids, artifacts). It states the **scoping rule** (project-scoped when a Jerry Project is active, else repo root) and an explicit boundary banner: "*Distinct from worktracker `DEC-NNN` entities ... this log is the interaction-level record ... Entries cross-link to DEC/ADR artifacts.*" It uses ids `DEC-LLM-NNN` to avoid colliding with `{ParentId}:DEC-NNN`.
- **Honest gaps they already flag** (adopt as design inputs): (a) no native turn counter; (b) assistant-verbatim length policy unresolved; (c) **model varies within a session** — the shared block records "receiving model `claude-fable-5` (session default since 2026-07-02; turns before that were `claude-opus-4-8`)", which a single human-typed header cannot represent but the transcript captures per assistant record.

#### B.5 Adjacent Jerry conventions to align with

| Convention | What it establishes | Implication for the FU/decision-log design |
|---|---|---|
| **H-32 GitHub parity** (`project-workflow.md`) | Jerry-repo work items need a matching GH issue; worktracker = internal SSOT, GH = external surface, kept in sync | Precedent for "one SSOT + a sync duty." Reuse the *pattern* (verbatim file = SSOT), but do **not** mandate a GH issue per feedback item (too heavy for turn-by-turn capture). |
| **H-23 nav tables** (`markdown-navigation-standards.md`) | Every Claude-consumed markdown > 30 lines needs a nav table with anchor links | The log templates MUST ship with a nav table (the bootstrap files already comply). |
| **MEDIUM vocabulary + HARD ceiling 25/25** (`quality-enforcement.md`) | HARD rule budget is **full (25/25, zero headroom)**; new MUST-rules need a C4 ADR ceiling exception | A "MUST log feedback" rule **cannot be HARD** without a ceiling exception. Make it **MEDIUM (SHOULD)** enforced by a fail-open hook, or fold guidance into an existing rule. This is a firm constraint on the design. |
| **AE-002 / AE-003** (`quality-enforcement.md`) | Touching `.context/rules/` = auto-C3 minimum; new/modified ADR = auto-C3 | Installing the convention is **C3+**, so it goes through an adversary gate before any framework-path change (the bootstrap `LLM-DECISION-LOG` DEC-LLM-003 already anticipates this). |
| **Auto-memory `MEMORY.md`** (`[claude-home]/projects/.../memory/`) | User-scoped memory already stores `feedback_*.md` entries (several are loaded this session) | **Tension:** Jerry uses auto-memory, but [internal-kb]'s `R-CONTEXT-002` explicitly **rejects** auto-memory for persistent guidance (not git-tracked, invisible to collaborators, split-state). The new convention should make the **git-tracked log the SSOT** and treat memory as a convenience pointer, resolving the exact split-state [internal-kb] warns about. Real duplication already exists — the FEEDBACK-LOG backfill row notes 2026-06-30 feedback "*already captured as memory `feedback_*`*". |

---

## L2: Design Implications

### B-metadata: Automatable-metadata table (harness-stampable vs model/human-dependent)

The single biggest improvement over [internal-kb] is to stop hand-typing the forgettable metadata. Classify every requested field by whether the harness can stamp it deterministically:

| Field (from FU.2 requirement) | Best source | Automatable? | Mechanism / note |
|---|---|---|---|
| **session id** | hook stdin `session_id` (SessionStart/PreCompact/SubagentStop) + transcript `sessionId` | **YES (harness)** | Deterministic; already consumed by handlers. |
| **transcript path** | hook stdin `transcript_path` (UserPromptSubmit/PreCompact/SubagentStop) | **YES (harness)** | The durable pointer to full turns. |
| **date / datetime** | transcript record `timestamp` (ISO-8601 ms Z) or system clock | **YES (harness)** | Per-record, precise. |
| **project id** | `JERRY_PROJECT` env / session state | **YES (harness)** | Also selects project-scoped vs repo-root log file (the FU.2 scoping rule). |
| **cwd / gitBranch / CC version** | transcript `cwd`/`gitBranch`/`version` | **YES (harness)** | Useful context, free. |
| **model(s) involved** | transcript **assistant** `message.model` | **YES, but only via transcript** | NOT on hook stdin (B.1). Per-assistant-turn granularity; **can vary within a session** — resolve per turn, never a single header value. |
| **turn reference** | transcript `promptId` / `uuid`+`parentUuid` / `requestId` / line offset | **YES (resolvable), NO native number** | See B-turnref; recommend a hook-maintained ordinal anchored to `promptId`. |
| **agent id** | `SubagentStop` `agent_id`/`agent_type` + `agent_transcript_path`; Jerry workflow/agent ids | **PARTIAL** | Main-thread turns have no agent id; subagent turns are in sidechain transcripts. |
| **user verbatim feedback** | transcript `user` record `content` (or the live prompt) | **CAPTURABLE, not classifiable** | The bytes are automatable; deciding *which* user text is "feedback" needs model/human judgment. |
| **assistant verbatim** | transcript `assistant` record `content` | **CAPTURABLE** | Length policy unresolved (bootstrap flags it) — recommend excerpt + `uuid`/`requestId` pointer, not full paste. |
| **your summary** | model-authored | **NO** | Inherent model output. |
| **disposition / status** | human/model-maintained lifecycle | **NO** | The closure discipline ([internal-kb] "round not closed until every item Addressed/Deferred") stays human-owned. |

**Design conclusion:** split the record into a **machine-stamped provenance sidecar** (session id, transcript path, timestamp, project id, model-per-turn, promptId/uuid anchor, agent id) written fail-open by a hook, and a **human/model-authored body** (verbatim, summary, disposition). The human-readable log *references* the sidecar key, so the metadata that [internal-kb] lost to hand-typing (see the `DJ-025` id-collision and the prose `session (2026-06-10 ...)` label) becomes harness-guaranteed. This directly answers the FU.2 goal "so that we don't lose feedback."

### B-boundary: relationship to the worktracker `{ParentId}:DEC-NNN` entity

The overlap is real (B.2: DECISION.md is explicitly for "decisions between the User and Claude"). Keep them distinct by **scope, ceremony, and lifecycle**, and connect them by **graduation** (mirroring [internal-kb]'s verbatim -> FU -> DJ -> DEC chain):

| Dimension | LLM Decision Log (new) | Worktracker DECISION `{ParentId}:DEC-NNN` (exists) |
|---|---|---|
| Scope | Session/interaction-level; project-root **or** project-scoped | Work-item-scoped; **requires** an Epic/Feature/Story/Enabler parent |
| Granularity | Every decision-bearing exchange, chronological | One formal decision cluster (`D-NNN` entries) per file |
| Ceremony | Low; append-only ledger; provenance-first | High; `participants[]` required, co-located, **AST-validated (H-33)** |
| Lifecycle | Running capture (survives compaction) | State machine PENDING->DOCUMENTED->ACCEPTED/SUPERSEDED (terminal) |
| Authority on conflict | Loses to the formal artifact | **Wins** (ratified state) |
| Id | `DEC-LLM-NNN` (bootstrap precedent) — deliberately distinct | `{ParentId}:DEC-NNN` |

**Boundary rule to encode:** the LLM Decision Log is the **working provenance ledger**; when a decision hardens *and* attaches to a work item, it **graduates** into a worktracker DECISION and/or a Scheme-B ADR (`ADR-{domain-slug}-NNN`, per DEC-LLM-001), with a bidirectional cross-link and a `Reflected in:` pointer. The log entry is **never** itself a DECISION entity (no parent, no state machine, no AST schema). Standardize the `DEC-LLM-NNN` id prefix so the two id spaces can never collide. This preserves H-33/worktracker integrity while giving the user the low-friction, always-on capture they asked for.

### B-turnref: turn-reference options (no native turn number exists)

Ranked options for the "turn" field, given B.3:

| # | Option | Durable? | Human-friendly? | Verdict |
|---|--------|----------|-----------------|---------|
| 1 | **`promptId`** (user record) | Yes (UUID, stable per prompt) | No | **Best machine anchor** for "a turn" (one user prompt). Assistant turns link via `parentUuid`. |
| 2 | `uuid` + `parentUuid` chain | Yes | No | Most precise (addresses any record); verbose. Use for the assistant-excerpt pointer. |
| 3 | `requestId` (`req_...`) / `message.id` (`msg_...`) | Yes | No | Good anchor for a specific assistant response. |
| 4 | `timestamp` (ISO-8601) | Yes | Yes | Sortable and readable, but not unique under rapid/parallel turns. Good as a secondary display key. |
| 5 | Raw JSONL line offset | **No** | Slightly | **Reject** — compaction/rewrites shift offsets. |
| 6 | **Hook-maintained monotonic turn ordinal** in Jerry session state (increment on `UserPromptSubmit`) | Yes (harness-owned) | **Yes** ("turn 42") | **Recommended human-facing ref**, because it is stamped by the harness (immune to model forgetting) and reads naturally. |

**Recommendation:** use a **composite anchor** — durable machine key `{session_id}#{promptId}` (fall back to `{session_id}@{timestamp}` when a promptId is absent, e.g. an inline-doc annotation), plus the **hook-maintained turn ordinal** (Option 6) as the human-facing "turn N". This is the piece [internal-kb] never had (it only had a manually declared "round"), and it fits the user's turn-by-turn requirement that rounds model poorly. Never persist a bare line offset.

### B-install: enforcement-tier and workflow constraints

- **Tier:** the HARD ceiling is **25/25 with zero headroom**, so the convention's "capture feedback/decisions" obligation must be **MEDIUM (SHOULD)** backed by a **fail-open hook** (matching B.1 house style) — not a new HARD rule (which would need a C4 ceiling-exception ADR).
- **Criticality:** installing it touches `.context/rules/` (and adds an ADR) -> **AE-002/AE-003 auto-C3 minimum** -> adversary gate before any framework-path write. (P-020: this research writes nothing into framework paths; the bootstrap `DEC-LLM-003` already routes install through that gate.)
- **Automation seam:** `UserPromptSubmit` (and optionally `Stop`) already read `transcript_path` and can emit injected/side-channel output fail-open — the natural home for stamping the provenance sidecar (B-metadata) without model cooperation.
- **Migration:** the design must adopt the two existing `PROJ-031` bootstrap files in place (they already carry the improved Disposition enum, scoping rule, DEC boundary, and Backfill Queue) rather than replacing them.

---

## References

> All paths absolute. `[M]` = [internal-kb] reference repo (`[internal-kb]`); `[J]` = Jerry branch (`.`).

**[internal-kb] (PART A):**
1. `[M]/.context/current/rules.md` — platform rules; `R-CONTEXT-002` rejects auto-memory (lines 83-105); feedback captured inline as rule annotations ("(User feedback 2026-05-11 ...)", lines 67, 97). Grep confirms **no** `feedback-log` rule exists.
2. `[M]/CLAUDE.md` — repo memory hierarchy; work-item conventions.
3. `[M]/docs/tag/pdds/[internal-doc-B]/feedback-log.md` — reference `feedback-log.md` (strategy, `R{round}-FU.{n}` id scheme, status legend, round gates, verbatim-wins rule, graduation chain).
4. `[M]/docs/tag/pdds/[internal-doc-A]/feedback-log.md` — second instance; Round 2 records the log's own origin (`R2-FU.13`) and the C4-gate (`R2-FU.14`).
5. `[M]/docs/tag/pdds/[internal-doc-A]-.../feedback/round-1-verbatim.md` — verbatim-capture format (YAML frontmatter `artifact_type/round/captured/source/status`; `## FU.n` blockquotes).
6. `[M]/docs/tag/pdds/[internal-doc-A]-.../llm-decision-journal.md` — `DJ-NNN` journal; entry template with `Provenance: <user> · <model-id> · session <session-id>`, Status/Type/Confidence/Reversibility/"Reflected in"; directional-separation table; `DJ-025` documents a manual id-collision.
7. `[M]/docs/tag/pdds/[internal-doc-A]-.../decisions.md` — ratified `DEC-NNN` (Proposed/Active/Superseded) graduation target.
8. `[M]/docs/tag/pdds/[internal-doc-A]-.../HOWTO.md` — "AI-assisted PM" philosophy behind the template.
9. `[M]/.context/current/planning/development/codename-a/infrastructure/{rate-limiting/[ado-id-1],native-grpc/[ado-id-2]}-follow-up-*.md` — the "known example" paths; confirmed to be **ADO work-item mirrors, not FU-log entries**.

**Jerry (PART B):**
10. `[J]/hooks/hooks.json` — six lifecycle events + matchers.
11. `[J]/hooks/{session-start,user-prompt-submit,pre-compact,pre-tool-use,subagent-stop,context-stop-gate}.py` — thin fail-open wrappers.
12. `[J]/src/interface/cli/hooks/hooks_session_start_handler.py:136` — reads `session_id`.
13. `[J]/src/interface/cli/hooks/hooks_prompt_submit_handler.py:150,194` — reads `transcript_path`; returns `additionalContext` (automation seam).
14. `[J]/src/interface/cli/hooks/hooks_pre_compact_handler.py:130-131` — reads `transcript_path`, `session_id`.
15. `[J]/src/interface/cli/hooks/hooks_subagent_stop_handler.py:101-107` — reads `session_id`, `agent_id`/`agent_name`, `agent_type`, `agent_transcript_path`.
16. `[J]/src/interface/cli/hooks/hooks_pre_tool_use_handler.py:128-129` / `hooks_stop_gate_handler.py:95` — `tool_name`/`tool_input`; Stop reads no stdin. **No handler reads `model`.**
17. `[J]/.context/templates/worktracker/DECISION.md` — DECISION entity: id `{ParentId}:DEC-NNN`, state machine, containment, `D-NNN` structure, "user-agent discussions" purpose (line 9).
18. `[J]/skills/worktracker/rules/worktracker-directory-structure.md:65,73` — DEC file name `{ParentId}--{DecisionId}-{slug}.md`; "decisions between the User and Claude".
19. Transcript: `[transcripts]/fd8559c2-abdd-4da7-b29a-ef4895fa5248.jsonl` (11 MB) — NDJSON structure inspected: `user` records carry `promptId` (no model); `assistant` records carry `message.model=claude-opus-4-8`, `requestId`, `message.id`, `usage`; universal `uuid`/`parentUuid`/`sessionId`/`timestamp`/`isSidechain`; **no native turn number**.
20. `[J]/projects/PROJ-031-cowork-skeleton/{FEEDBACK-LOG.md,LLM-DECISION-LOG.md}` — bootstrap instances to adopt.
21. `[J]/.context/rules/{quality-enforcement.md,project-workflow.md,markdown-navigation-standards.md}` — HARD ceiling 25/25, AE-002/003, H-32, H-23; auto-memory `MEMORY.md` (loaded `feedback_*` entries).

*[INFERENCE] markers in-text denote claims not directly provable from a single source line (notably: Claude Code omitting `model` from hook stdin — inferred from the absence of any `model` read across all handlers).*
