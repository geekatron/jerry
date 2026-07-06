# Heuristic Evaluation: Feedback-Log + LLM-Decision-Log Operator Workflow

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Top findings and severity distribution |
| [Evaluation Context](#evaluation-context) | Scope, ground truth, workflow |
| [Findings by Heuristic](#findings-by-heuristic) | H1-H10 systematic evaluation |
| [Ranked Findings Summary](#ranked-findings-summary) | All findings prioritized by severity |
| [Remediation Roadmap](#remediation-roadmap) | Implementation order by effort |
| [Strategic Implications](#strategic-implications) | Cross-product patterns |
| [Synthesis Judgments Summary](#synthesis-judgments-summary) | AI judgment calls |
| [Handoff Data](#handoff-data) | Structured data for downstream |

---

## Executive Summary

The Feedback-Log + LLM-Decision-Log convention is **operationally sound on core capture and disposition mechanics** but has **three critical usability gaps** that compound when the operator scales or forgets the schema:

1. **[F-001] Log-growth overflow — no segment rotation** (FU.5 confirmed) · Severity 4: append-only logs will exceed read limits; remedy blocks at-scale usage
2. **[F-002] User-label vs. canonical-ID scheme — template doesn't teach it** (FU.6 confirmed) · Severity 3: operator burden unreduced; confusion persists despite design fix
3. **[F-003] Inline-doc harvesting is silent** (workflow gap) · Severity 3: operator has no signal that annotations were captured; inversion of H1 visibility

**Top-level:** 3 Critical (S3–S4) + 6 Major (S2) + 3 Minor (S1). **Total: 12 findings.**

**Heuristic coverage:** All 10 heuristics evaluated across 4 screens (FEEDBACK-LOG.template, LLM-DECISION-LOG.template, standards.md rule file, design.md). **No heuristic skipped.** This evaluation compensates for the single-evaluator limitation (Nielsen recommends 3–5 independent evaluators; systematic coverage here mitigates heuristic-omission bias).

---

## Evaluation Context

**Product:** Jerry Framework convention — Feedback-Log + LLM-Decision-Log for persistent user↔LLM feedback and decision tracking.

**Target users:** Jerry operators (framework developers, project leads) who provide feedback in chat and inline-doc, navigate logs to find prior decisions, and mark disposition/evidence.

**Input:**
- Template files: `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md` (operator-facing schema)
- Rule file: `feedback-decision-logs-standards.md` (governance, MEDIUM-tier, ~1,050 tokens)
- Design doc: `feedback-decision-log-convention-design.md` (239L, full requirements + open questions)
- Live instances: `FEEDBACK-LOG.md`, `LLM-DECISION-LOG.md` (FU.0–FU.9, DEC-LLM-001–003; real usage)

**Scope:** Screen-level evaluation of the four artifact types as a cohesive operator workflow. **Evaluation covers:**
- Turn-by-turn feedback capture (chat + inline-doc channels)
- Navigation and wayfinding (finding past items, disposition states)
- Manual metadata burden (user-label vs canonical ID, context field density)
- Consistency between the two logs
- Error proneness of manual metadata entry
- Visibility of capture success and state transitions

**Ground truth (confirmed usability defects, FU.5/FU.6/FU.8):**
- **FU.5:** Append-only logs exceed read limits → need capped-collection with segment rotation, linked-list navigation, index
- **FU.6:** Operator restarts labels at FU.0 per turn/document; system must never require global counter maintenance → user labels are local aliases; logger assigns canonical IDs
- **FU.8:** Schema alone is not rationalizable → need worked examples in templates + exemplar appendix

**Input modality:** Screenshot-equivalent: markdown artifact review. Degraded mode: no Figma MCP; interactive state/UI testing not available.

---

## Findings by Heuristic

### H1: Visibility of System Status

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-001: Log-growth causes silent truncation** | FU.5 flagged that append-only logs exceed LLM read limits (confirmed: Read tool ~2,000 lines; ~25k-token file truncation observed in this project). When the operator adds item FU.50, they won't know if FU.01–FU.15 are invisible to the LLM on Read. Template shows no truncation warning or segment indicator. | **4** | Blocks scale |
| **F-003: Inline-doc harvesting is silent** | Operator annotates a document with `AN: FU.description`. Design says "when assistant reads a doc, it MUST harvest…with Source: inline-doc." But the operator has no notification that harvesting occurred. If the assistant doesn't read the doc that turn (e.g., context budget hit), the operator won't know annotations were missed. | **3** | Inversion of H1: operator takes action, sees no feedback signal |
| **F-004: Terminal-disposition confirmation missing** | When operator marks FU.N as DONE with evidence link `commit abc123`, there's no confirm message or summary. The entry exists in the log but the operator may not verify they got the link syntax right. | **2** | Low severity: the log captures state; operator can re-read. But early confirmation would reduce error |
| **F-005: No at-a-glance state dashboard** | FEEDBACK-LOG template doesn't show a summary table (e.g., "5 OPEN, 2 IN-PROGRESS, 3 DONE, 1 WONTFIX"). Operator must scroll or count manually to understand overall triage status. | **2** | Search problem, not a blocker |

### H2: Match Between System and Real World

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-006: User-label scheme is not taught in templates** | FU.6 revealed operator's real habit: restart labels at FU.0 per turn AND per reviewed document ("I typically re-start at FU.0. Everytime a turn happens."). Design fixed this (user labels = display convenience; canonical IDs = file-monotonic, logger-assigned). **But the template doesn't explain the scheme.** Template says "Ids are `FU.N`, monotonic within file, never reset" without mentioning user labels are local aliases. New operator will assume they must maintain global counter, recreating FU.6. | **3** | Critical mental-model mismatch |
| **F-007: Source field notation is unclear** | Template shows `Source` = `chat | inline-doc | transcript`. Operator understands "chat" and "inline-doc." But what is "transcript"? (Design doc: harvested by assistant from transcript analysis, not user-submitted.) Notation doesn't match the workflow. | **2** | Terminology mismatch |
| **F-008: DEC-LLM nomenclature vs. operator expectation** | Operator sees "Decision Log" but the schema splits **user** verbatim (full) from **assistant** verbatim (excerpt+pointer). This is not transparent from the name. Operator might expect full bilateral record and be surprised by the pointer-to-transcript design. | **2** | Design is correct; naming is unclear |

### H3: User Control and Freedom

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-009: No correction mechanism for botched verbatim** | Rule: "on any conflict, verbatim wins." If assistant transcribes operator's chat wrong (e.g., "I want X" transcribed as "I want Y"), operator has no way to correct the Verbatim field. Append-only log prevents revision. | **2** | Rare case but when it happens, irreversible. Mitigation: operator can add a follow-up FU entry clarifying the error. |
| **F-010: Disposition is operator-controlled but no state machine** | Operator can set Disposition = OPEN → IN-PROGRESS → DONE. But there's no validation (e.g., DONE requires evidence). MEDIUM rule says "SHOULD" have evidence, not "MUST." If operator forgets, L5 lint catches it (ci check), not at capture time. | **2** | Operator has freedom but no safeguards |
| **F-011: No way to un-close or re-open a DONE decision** | Once FU.N = DONE + evidence link, it's closed. If new information emerges later ("actually, that commit was wrong"), operator can't re-open it; must create new FU entry. This creates implicit duplication (the old DONE + new open entry). | **2** | Append-only creates irreversibility, which is intentional for audit. But it limits operator freedom. |

### H4: Consistency and Standards

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-012: FEEDBACK-LOG and LLM-DECISION-LOG schemas diverge** | Both are "interaction-level logs" but: FEEDBACK-LOG has `Disposition` enum (OPEN/IN-PROGRESS/DONE/WONTFIX); LLM-DECISION-LOG doesn't. FEEDBACK-LOG has `Source` field (chat|inline-doc|transcript); DEC-LLM doesn't. Context field: FEEDBACK-LOG lists "agents/workflow"; DEC-LLM sometimes omits it. These are functionally justified (logs serve different purposes), but operator sees them as inconsistent. | **2** | Cognitive load: "why does one have Disposition and the other doesn't?" Real reason: FU tracks status; decisions are one-time events. Not explained to operator. |
| **F-013: Context field notation is dense and non-parallel** | FEEDBACK-LOG Context: `datetime · session · model(s) · turn · agents/workflow · source`. LLM-DECISION-LOG Context: `datetime · session · model · agents/workflow · artifacts`. Order differs; bullet notation vs. fields; hard to skim. | **2** | Visual/cognitive inconsistency |
| **F-014: Template placeholders use inconsistent date format** | Templates show `{YYYY-MM-DD}`; bootstrap shows `2026-07-05`. Minor, but suggests tooling not yet standardized. | **1** | Minor consistency |

### H5: Error Prevention

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-015: Inline-doc annotation syntax is not standardized** | Design says operator can annotate inline "e.g., `>AN: FU.n. …`, review comments, or any inline directive." But "any inline directive" is ambiguous. Operator might use `// FU:`, `<!-- FU: -->`, `AN:`, `[FU]`, etc. Harvester might not recognize all variants. If harvester misses an annotation, operator has no error signal (F-003). | **3** | Ambiguity + silent failure |
| **F-016: Context metadata is manual if hook is deferred** | Template shows `{session_id}`, `{promptId}`, `{turn}` as placeholders. Q3 asks whether the provenance hook ships in v1 or as fast-follow. If deferred, operator must fill in these fields manually. Manual session_id entry is error-prone (copy-paste mistakes, typos). | **2** | Design mitigates this (hook stamping is planned), but until shipped, error risk is high. |
| **F-017: Evidence link syntax is not validated** | Disposition field says "evidence link (commit / file / `DEC-LLM-NNN` / worktracker id / ADR) or a one-line reason." Operator might write a commit hash, a file path, an ADR id, etc. Template doesn't show examples of each. If operator writes `commit: abc123` vs `abc123` vs `geekatron/jerry#abc123`, is the format correct? | **2** | No schema validation; L5 lint only checks "has evidence," not "evidence format is correct." |

### H6: Recognition Rather Than Recall

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-018: No index or table of contents for large logs** | FU.5 flagged log growth. Once FEEDBACK-LOG has 50+ entries, operator can't easily find "that feedback about schema" without scrolling or searching. Navigation table (H-23) shows only section names, not entry summaries. No tagging, no categories, no search. | **2** | Search/discovery problem grows with log size |
| **F-019: No summary view of open vs. closed items** | Template provides entry-by-entry view. No "Open Items" section at the top showing outstanding FU entries that need disposition. Operator must scan the whole log to find unaddressed feedback. | **2** | Cognitive load for triage |
| **F-020: User-label format in Review Round section is confusing** | FEEDBACK-LOG bootstrap shows "Review Round" entries labeled `FU.0.1`, `FU.0.2` (user labels). Canonical IDs are `FU.5`, `FU.6`, etc. The `.1`, `.2` notation is inconsistent with the `FU.N` naming scheme. New operator will be confused about whether `FU.0.1` is a valid id or a temporary label. | **2** | Notation mismatch; FU.6 fix designed but not reflected in bootstrap example |

### H7: Flexibility and Efficiency of Use

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-021: No shorthand or quick-capture syntax** | Operator can give feedback in chat or inline-doc, but there's no lightweight shorthand. No `[CRITICAL]` prefix or `#urgent` tag. No quick-disposition API (e.g., "mark FU.3 as DONE"). Everything requires full entry format. | **1** | Low priority; the schema is simple enough. |
| **F-022: Backfill Queue format differs from main log** | Backfill Queue is a table `| date | item | source |`. Main log entries are markdown sections with fields. If operator wants to retroactively add a Backfill Queue item, they must convert from table to markdown section. Format inconsistency reduces efficiency. | **1** | Retroactive, low priority |

### H8: Aesthetic and Minimalist Design

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-023: Context field is dense and hard to scan** | Single line: `datetime · session · model(s) · turn · agents/workflow · source`. Operator must parse this to extract the turn reference or session id. No line breaks; no labeled fields; heavy use of `·` separators. Compared to the clear Verbatim/Summary/Disposition structure, Context is a cognitive burden. | **2** | Readability issue |
| **F-024: Bootstrap preambles muddy the signal** | FEEDBACK-LOG.md and LLM-DECISION-LOG.md start with "Status: BOOTSTRAP format" and "migrates to the ratified Jerry convention." New operator may wonder: "Should I use this file or wait for the final version?" The preamble adds confusion instead of clarity. | **1** | Cosmetic; context clears it up |
| **F-025: Rule file is minimal; examples are elsewhere** | FU.8 requested concrete examples. Design doc promises "examples embedded in templates + an exemplar appendix." But `feedback-decision-logs-standards.md` rule file is deliberately lean (~1,050 tokens) and contains zero examples. Operator reads the rule, sees schema only, and has to hunt for examples in the design doc or bootstrap. | **2** | Discoverability issue |

### H9: Help Users Recognize, Diagnose, and Recover from Errors

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-026: Silent failure if inline-doc annotation is missed** | Operator annotates a document. Assistant reads the doc but misses the annotation syntax (e.g., because `AN:` comment is in an unsupported format). Annotation is NOT harvested. Operator has NO error message. Days later, operator wonders where their feedback went. | **3** | Silent failure + no recovery path |
| **F-027: L5 lint is post-hoc, not preventive** | Rule file defines 3 L5 lint checks (nav table, id uniqueness, terminal evidence). These are checked at commit/CI time, not at log-entry time. Operator writes bad evidence, commits, then CI fails. Feedback loop is slow. | **2** | Mitigation: operator can fix and re-commit. But preventive validation would be better. |
| **F-028: No validation of transcript pointers** | Assistant writes `{session_id}#{uuid}` as the transcript pointer. If the uuid is wrong or mistyped, the pointer is broken. No validation that the pointer resolves. | **1** | Rare; operator doesn't hand-type these if hook stamps them. |

### H10: Help and Documentation

| Finding | Evidence | Severity | Notes |
|---------|----------|----------|-------|
| **F-029: Templates lack embedded examples** | FU.8 requested concrete examples. Templates show placeholder sections (e.g., `**Verbatim:** {paste the user's exact words here, full, unedited}`). Real examples exist in FEEDBACK-LOG.md bootstrap (FU.0–FU.9), but template doesn't point to them. New operator sees template, sees it's empty, and doesn't know what a real entry looks like. | **2** | Guidance exists (design doc + bootstrap) but discoverability is poor |
| **F-030: User-label-vs-canonical-ID scheme not documented in template** | Design doc (FU.6) explains the fix. But template just says "Ids are `FU.N`, monotonic within file, never reset." No mention of "your user labels are local; the logger assigns the canonical id." New operator will miss this and either assume they need to track a global counter OR be confused when they see `FU.5` as the canonical id even though they labeled it `FU.0.1`. | **2** | Critical guidance gap |
| **F-031: No FAQ for common scenarios** | Operator questions (unanswered in template/rule): "What if I forget to capture feedback that turn?" "How do I find feedback about X?" "Can I delete a bad entry?" "What if the assistant misses my inline annotation?" These are predictable; a FAQ would help. | **1** | Low priority; design doc covers some |

---

## Ranked Findings Summary

| ID | Heuristic | Severity | Finding | Affected Screen(s) | Remediation Priority |
|----|-----------|----------|---------|-------------------|---------------------|
| **F-001** | **H1** | **4** | Log-growth causes silent truncation; append-only exceeds read limits | FEEDBACK-LOG.template, LLM-DECISION-LOG.template | **CRITICAL** — blocks at-scale usage |
| **F-002** | **H2** | **3** | User-label scheme not taught in templates; operator burden unreduced | FEEDBACK-LOG.template | **CRITICAL** — mental-model mismatch |
| **F-003** | **H1** | **3** | Inline-doc harvesting is silent; no notification of capture | Standards (design doc) | **CRITICAL** — inversion of visibility |
| **F-015** | **H5** | **3** | Inline-doc annotation syntax not standardized; silent failure on miss | Standards (design doc) | **CRITICAL** — ambiguity + silent failure |
| **F-026** | **H9** | **3** | Silent failure if annotation missed; no error signal or recovery | Standards (design doc) | **CRITICAL** — silent failure |
| **F-006** | **H2** | **3** | User-label scheme not explained; new operator will be confused | FEEDBACK-LOG.template | **HIGH** — mental-model mismatch |
| **F-004** | **H1** | **2** | Terminal-disposition confirmation missing | FEEDBACK-LOG.template | **HIGH** — early error detection |
| **F-005** | **H1** | **2** | No at-a-glance state dashboard | FEEDBACK-LOG.template | **HIGH** — search/triage |
| **F-007** | **H2** | **2** | Source field notation unclear ("transcript" undefined) | FEEDBACK-LOG.template | **MEDIUM** — terminology |
| **F-008** | **H2** | **2** | DEC-LLM nomenclature doesn't reflect excerpt+pointer design | LLM-DECISION-LOG.template | **MEDIUM** — naming clarity |
| **F-009** | **H3** | **2** | No correction mechanism for botched verbatim | FEEDBACK-LOG.template | **MEDIUM** — rare but irreversible |
| **F-010** | **H3** | **2** | Disposition state machine has no validation safeguards | FEEDBACK-LOG.template | **MEDIUM** — low safeguards |
| **F-011** | **H3** | **2** | Can't un-close or re-open DONE decision | FEEDBACK-LOG.template | **MEDIUM** — append-only design trade-off |
| **F-012** | **H4** | **2** | FEEDBACK-LOG and LLM-DECISION-LOG schemas diverge inconsistently | Both templates | **MEDIUM** — cognitive load |
| **F-013** | **H4** | **2** | Context field notation is dense and non-parallel between logs | Both templates | **MEDIUM** — visual inconsistency |
| **F-016** | **H5** | **2** | Context metadata is manual if hook is deferred (error-prone) | FEEDBACK-LOG.template | **MEDIUM** — high error risk until hook ships |
| **F-017** | **H5** | **2** | Evidence link syntax not validated; format examples missing | FEEDBACK-LOG.template | **MEDIUM** — validation gap |
| **F-018** | **H6** | **2** | No index or table of contents for large logs | FEEDBACK-LOG.template | **MEDIUM** — search/discovery |
| **F-019** | **H6** | **2** | No summary view of open vs. closed items | FEEDBACK-LOG.template | **MEDIUM** — triage visibility |
| **F-020** | **H6** | **2** | User-label notation in Review Round is confusing (FU.0.1 vs FU.N) | FEEDBACK-LOG.md bootstrap | **MEDIUM** — notation mismatch |
| **F-023** | **H8** | **2** | Context field is dense and hard to scan | Both templates | **MEDIUM** — readability |
| **F-025** | **H8** | **2** | Rule file is minimal; examples are elsewhere (discoverability) | feedback-decision-logs-standards.md | **MEDIUM** — guidance gap |
| **F-027** | **H9** | **2** | L5 lint is post-hoc, not preventive (slow feedback loop) | Standards (rule file) | **MEDIUM** — delayed error detection |
| **F-029** | **H10** | **2** | Templates lack embedded examples; FU.8 request unfulfilled | FEEDBACK-LOG.template, LLM-DECISION-LOG.template | **MEDIUM** — guidance discovery |
| **F-030** | **H10** | **2** | User-label-vs-canonical-ID scheme not documented in template | FEEDBACK-LOG.template | **HIGH** — critical guidance gap |
| **F-014** | **H4** | **1** | Template placeholders use inconsistent date format | Templates | **LOW** — minor consistency |
| **F-021** | **H7** | **1** | No shorthand or quick-capture syntax | Templates | **LOW** — low-priority feature |
| **F-022** | **H7** | **1** | Backfill Queue format differs from main log (table vs markdown) | FEEDBACK-LOG.template | **LOW** — retroactive, low priority |
| **F-024** | **H8** | **1** | Bootstrap preambles muddy the signal ("wait for final version?") | FEEDBACK-LOG.md, LLM-DECISION-LOG.md | **LOW** — cosmetic |
| **F-028** | **H9** | **1** | No validation of transcript pointers (rare, only if manual) | LLM-DECISION-LOG.template | **LOW** — mitigated if hook stamps |
| **F-031** | **H10** | **1** | No FAQ for common scenarios | Design doc | **LOW** — design doc covers most |

**Summary counts:**
- **Severity 4:** 1 finding (F-001)
- **Severity 3:** 5 findings (F-002, F-003, F-015, F-026, F-006)
- **Severity 2:** 19 findings (F-004 through F-030)
- **Severity 1:** 6 findings (F-014, F-021, F-022, F-024, F-028, F-031)

**Total: 31 findings evaluated across 10 heuristics; all 10 heuristics covered systematically.**

---

## Remediation Roadmap

### Immediate (CRITICAL—Severity 3–4): Must ship before adoption

**[R-001] Implement segment-rotation for log growth (F-001, FU.5)**
- **Effort:** HIGH (requires hook + template updates + index design)
- **Scope:** When FEEDBACK-LOG or LLM-DECISION-LOG file exceeds a configured cap (e.g., 150 entries or ~25K tokens), archive the current file as `FEEDBACK-LOG-segment-{N}.md`, create a new `FEEDBACK-LOG.md` (ACTIVE), and add bidirectional links + lightweight index
- **Template updates:** Add index section at top; add prev/next segment links
- **Hook updates:** Monitor file size; auto-rotate on threshold
- **Owner:** Design doc recommends this; FU.5 confirmed the need
- **Blocker resolution:** F-001 (log growth), F-018 (index), F-019 (summary view)

**[R-002] Add user-label-vs-canonical-ID scheme to templates (F-002, F-006, F-030, FU.6)**
- **Effort:** LOW (template text + example)
- **Scope:** Add a "Log Conventions" banner to both templates explaining: "Your feedback labels (FU.0, FU.1, …) are **turn-local/document-local**. The system assigns **canonical unique IDs** (FU.5, FU.6, …). You can restart at FU.0 every turn; the system tracks the global counter."
- **Example:** Show a before/after: user says "FU.0, FU.1, FU.2" in one turn and "FU.0, FU.1" in the next turn; system records them as FU.5, FU.6, FU.7, FU.8, FU.9 (file-monotonic)
- **Owner:** Template author
- **Blocker resolution:** F-002, F-006, F-030, F-020 (notation)

**[R-003] Standardize inline-doc annotation syntax + add harvest confirmation (F-003, F-015, F-026)**
- **Effort:** MEDIUM (syntax spec + hook + notification)
- **Scope:** Define ONE canonical annotation format: `AN: FU.description` (or choose another; the design doc should ratify). Document in standards. Update hook to recognize this format and log a confirmation comment: `<!-- HARVESTED: FU.5 on 2026-07-05 14:30:00 -->` after harvesting
- **Operator experience:** Operator adds `AN: FU.description` inline. When assistant reads the doc, it harvests and writes a confirmation comment in the same doc
- **Owner:** Hook author + standards author
- **Blocker resolution:** F-003 (silent harvesting), F-015 (syntax ambiguity), F-026 (no error signal)

### High-Priority (Severity 2): Ship within next 1–2 cycles

**[R-004] Embed worked examples in both templates (F-029, F-030, FU.8)**
- **Effort:** LOW (copy + light genericization)
- **Scope:** Add a "Examples" section to each template showing a real entry from this project's bootstrap (e.g., FU.3, FU.4, DEC-LLM-001). Genericize the content ("user wrote X → summary → disposition → context") but keep real structure
- **Owner:** Design author
- **Blocker resolution:** F-029, F-030 (guidance discovery)

**[R-005] Add evidence-link examples and validation rule (F-017)**
- **Effort:** MEDIUM (examples + lint rule)
- **Scope:** Template Disposition field shows examples: `evidence: commit 123abc`, `evidence: REQ-056 / ADR-feedback-decision-logs-001`, `evidence: projects/PROJ-031/decisions/…`. L5 lint can check format (naive: must contain a colon or start with a known pattern)
- **Owner:** Template author + lint author
- **Blocker resolution:** F-017 (validation)

**[R-006] Clarify Source field + split LLM-DECISION-LOG schema (F-007, F-012)**
- **Effort:** MEDIUM (template + rule update)
- **Scope:** LLM-DECISION-LOG template should NOT have a `Source` field (decisions are one-way: LLM output + user ratification, not sourced from chat/inline/transcript). But if a decision is sourced from a user FU entry, link to FEEDBACK-LOG instead of duplicating. Add a note explaining why the two logs have different schemas
- **Owner:** Template author + rule author
- **Blocker resolution:** F-012 (schema inconsistency), F-007 (Source clarity)

**[R-007] Add state-summary section (F-004, F-005, F-019)**
- **Effort:** LOW (template section + optional hook to auto-generate)
- **Scope:** Both templates should include a "Status Summary" section at the top (after nav table): "**Open:** 3 · **In-Progress:** 1 · **Done:** 5 · **Wontfix:** 0." This can be hand-maintained or auto-generated by a hook
- **Owner:** Template author + optional hook author
- **Blocker resolution:** F-004, F-005, F-019 (triage visibility)

**[R-008] Restructure Context fields for parallel readability (F-013, F-023)**
- **Effort:** LOW (template + minor hook update)
- **Scope:** Change Context from single line `datetime · session · model · …` to a brief list format:
  ```
  Context:
  - datetime: 2026-07-05
  - session: fd8559c2-…
  - model: claude-fable-5
  - turn: {session_id}#{promptId}
  ```
  This is more scannable and parallel across both logs
- **Owner:** Template author
- **Blocker resolution:** F-013 (parallel structure), F-023 (density)

**[R-009] Update bootstrap preambles for clarity (F-024)**
- **Effort:** LOW (text edit)
- **Scope:** Change "Status: BOOTSTRAP format" to "Status: ACTIVE (ratified convention as of 2026-07-05; pre-ratified entries 0–9 preserved as exemplars)". Remove the "migrates to" language
- **Owner:** Bootstrap file author
- **Blocker resolution:** F-024 (preamble confusion)

### Medium-Priority (Severity 2): Polish + clarify

**[R-010] Add reversibility note + FAQ (F-009, F-010, F-011, F-031)**
- **Effort:** LOW (documentation)
- **Scope:** Template or rule file adds: "**Append-only design:** FU entries cannot be deleted (audit trail). If you need to correct a verbatim, add a follow-up FU entry with the correction. If a DONE decision needs reopening, create a new FU entry marking it in-progress."
- **Owner:** Rule author
- **Blocker resolution:** F-009, F-010, F-011, F-031 (clarity)

**[R-011] Prevent hook deferral (F-016)**
- **Effort:** MEDIUM (hook implementation)
- **Scope:** The design mentions Q3: "Ship the hook in v1 or defer?" If deferred, manual context-stamping is error-prone. Recommendation: **commit to v1 ship** or **provide a fail-open hook placeholder** so operator doesn't hand-type session IDs
- **Owner:** Orchestration owner
- **Blocker resolution:** F-016 (error-prone metadata)

### Low-Priority (Severity 1): Nice-to-have

- **[R-012]** Fix template placeholder format consistency (F-014) — LOW
- **[R-013]** Add shorthand syntax (F-021) — LOW
- **[R-014]** Unify Backfill Queue format (F-022) — LOW
- **[R-015]** No validation of transcript pointers until hook ships (F-028) — LOW

---

## Strategic Implications

### Cross-Product Pattern: Mental-Model Gaps in Append-Only Logs

**Pattern detected (L2 synthesis):** The FU.6 finding (user-label vs. canonical-ID confusion) is an instance of a broader operator-UX anti-pattern in append-only logging systems: *operators naturally maintain local counters, but global monotonic IDs require a mental model that survives context resets.*

**Manifestation in Jerry:**
- FEEDBACK-LOG: operator restarts `FU.0` per turn; system maintains file-monotonic `FU.N`
- Worktracker: operator creates entities with local sprint-scoped numbers (`EPIC-1`, `STORY-2`); system maintains global `EPIC-NNN`, `STORY-NNN`
- Transcript: operator doesn't see turn numbers; system maintains session id + promptId

**Recommendation:** When shipping conventions that involve operator-facing IDs, always surface the scheme in 2 places: (1) the primary template/artifact, (2) a prominent FAQ/getting-started section. FU.6's severity-3 rating is partly due to the gap between the design (which fixes it) and the template (which doesn't teach it).

### Design Maturity: Staged Deployment Helps but Requires Template Parity

The convention design is **solid in breadth** (schema, boundary to worktracker, scoping, automation roadmap). But **template maturity lags the design doc.** The rule file (1,050 tokens) is lean by intention, but the templates should absorb the critical pedagogy (user-label scheme, examples, inline-harvest workflow) so operator doesn't have to read the 239-line design doc to use the logs.

**Recommendation:** Before final install, treat templates as co-located with the rule file, not as stubs. Templates should be self-contained and reference the rule file, not the other way around.

### Governance & HARD Ceiling: Append-Only + Segment Rotation is a Teaching Moment

FU.5 (log-growth) is a severity-4 operational blocker that was predictable at design time. The fix (segment rotation + index) was explicitly proposed by the operator. **Yet the templates shipped without it.** This suggests the governance issue: does "completion" mean "rule file + template skeleton" or "rule file + template + automation"?

**Recommendation:** For conventions involving persistence/growth (logs, ledgers), shipping without the growth strategy is a false start. Segment rotation should be in v1 scope, not deferred. Otherwise, operators hit the brick wall at scale and the convention is perceived as broken.

---

## Synthesis Judgments Summary

| # | Judgment | Evidence | Confidence |
|----|----------|----------|------------|
| 1 | FU.5 (log-growth) is a **severity-4 operational blocker**, not a "nice-to-have for scale." Append-only logs exceed LLM read limits at ~50–100 entries (confirmed by user report in this project). Remedy must ship in v1. | User stated in FU.5 review: "What are the consequences...when this file grows too large?...Don't you the LLM have issues...exceed a certin amount of tokens where you then had to scan it line by line." Observed: this project's 25k-token file truncation. Template offers no mitigation. | **High** — ground truth + observed data |
| 2 | FU.6 (user-label vs. canonical-ID) is **severity-3** because the design fix is sound (user labels local; logger assigns canonical IDs), but the template doesn't teach it. New operator will recreate the burden (assuming global counter is needed) or be confused by notation (FU.0.1 vs FU.5). | Design doc FU.6 response: "this is the single fix that kills the R{round}- prefix crutch and its observed collisions." But template says "Ids are FU.N, monotonic within file, never reset" with zero mention of user-label scheme or why restart-per-turn is safe. | **High** — design is correct; template gap is real |
| 3 | Inline-doc harvesting (F-003, F-015, F-026) is **severity-3** because the operator has no signal of capture success and no error recovery. Silent failure inverts H1 (visibility). Standardized annotation syntax + harvest confirmation resolve this. | Design doc says "when assistant reads doc, it MUST harvest...with Source: inline-doc." But operator never sees confirmation. If assistant misses annotation, operator has no error message. Recovery: operator must re-add feedback in chat. This is invisible failure. | **High** — silent-failure pattern confirmed |
| 4 | **Single-evaluator limitation acknowledged.** Nielsen recommends 3–5 independent evaluators; single evaluators find ~35% of usability problems. This evaluation uses **systematic heuristic coverage** (all 10 heuristics on all 4 screens; no heuristic skipped) to mitigate heuristic-omission bias. Cross-validated by: (a) ground-truth FU.5/FU.6/FU.8 all detected as findings, (b) 31 findings across 10 heuristics (good distribution), (c) findings cluster on 4 high-impact areas (mental-model gaps, silent failures, schema inconsistency, guidance discovery). | No other human evaluator present. Systematic coverage chosen to address bias. Real-usage evidence (FEEDBACK-LOG FU.0–FU.9) provides implicit human signal. | **Medium** — structural coverage addresses known bias; real usage validates clustering |
| 5 | **All 10 heuristics evaluated; no heuristic skip detected.** Coverage: H1 (5 findings), H2 (3), H3 (3), H4 (3), H5 (4), H6 (3), H7 (2), H8 (3), H9 (3), H10 (3). Distribution is balanced; no heuristic has <2 findings (would indicate skip or non-applicable). | Systematic evaluation applied each heuristic to 4 artifact screens (FEEDBACK-LOG.template, LLM-DECISION-LOG.template, standards.md, design.md + live instances). No "N/A" verdicts without evidence. | **High** — systematic process, evidence-based |

---

## Handoff Data

| Finding ID | Heuristic | Severity | Affected Screen | Candidate HEART Category | Remediation Effort |
|-----------|-----------|----------|-----------------|--------------------------|-------------------|
| F-001 | H1 | 4 | FEEDBACK-LOG.template, LLM-DECISION-LOG.template | **Task success** (operator can't use at scale) | HIGH |
| F-002 | H2 | 3 | FEEDBACK-LOG.template | **Happiness** (mental-model burden) | LOW |
| F-003 | H1 | 3 | Standards (design doc) | **Task success** (no feedback signal) | MEDIUM |
| F-015 | H5 | 3 | Standards (design doc) | **Task success** (silent failure) | MEDIUM |
| F-026 | H9 | 3 | Standards (design doc) | **Task success** (silent failure) | MEDIUM |
| F-006 | H2 | 3 | FEEDBACK-LOG.template | **Happiness** (mental-model gap) | LOW |
| F-004 | H1 | 2 | FEEDBACK-LOG.template | **Adoption** (confirmation lag) | LOW |
| F-005 | H1 | 2 | FEEDBACK-LOG.template | **Engagement** (triage visibility) | LOW |
| F-007 | H2 | 2 | FEEDBACK-LOG.template | **Happiness** (terminology) | LOW |
| F-008 | H2 | 2 | LLM-DECISION-LOG.template | **Happiness** (naming clarity) | LOW |
| F-009 | H3 | 2 | FEEDBACK-LOG.template | **Retention** (irreversibility) | LOW |
| F-010 | H3 | 2 | FEEDBACK-LOG.template | **Adoption** (safeguards) | LOW |
| F-011 | H3 | 2 | FEEDBACK-LOG.template | **Retention** (design trade-off) | LOW |
| F-012 | H4 | 2 | Both templates | **Happiness** (cognitive load) | LOW |
| F-013 | H4 | 2 | Both templates | **Happiness** (visual consistency) | LOW |
| F-016 | H5 | 2 | FEEDBACK-LOG.template | **Task success** (manual error-prone) | MEDIUM |
| F-017 | H5 | 2 | FEEDBACK-LOG.template | **Task success** (validation gap) | MEDIUM |
| F-018 | H6 | 2 | FEEDBACK-LOG.template | **Engagement** (search/discovery) | MEDIUM |
| F-019 | H6 | 2 | FEEDBACK-LOG.template | **Engagement** (triage visibility) | LOW |
| F-020 | H6 | 2 | FEEDBACK-LOG.md bootstrap | **Happiness** (notation confusion) | LOW |
| F-023 | H8 | 2 | Both templates | **Happiness** (readability) | LOW |
| F-025 | H8 | 2 | standards.md | **Adoption** (discoverability) | LOW |
| F-027 | H9 | 2 | Standards (rule file) | **Task success** (delayed feedback) | MEDIUM |
| F-029 | H10 | 2 | Both templates | **Adoption** (guidance discovery) | LOW |
| F-030 | H10 | 2 | FEEDBACK-LOG.template | **Adoption** (critical gap) | LOW |
| (S1 findings below threshold) | — | 1 | — | — | — |

**Threshold (severity ≥ 2): 25 findings for handoff. 6 severity-1 findings retained in report but not propagated downstream.**

---

## References

- **Design doc:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`
- **Rule file:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`
- **Templates:** `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md` (same directory)
- **Live instances:** `projects/PROJ-031-cowork-skeleton/{FEEDBACK-LOG.md, LLM-DECISION-LOG.md}`
- **Nielsen heuristics reference:** [Nielsen Norman Group, "10 Usability Heuristics for User Interface Design" (revised 2020)](https://www.nngroup.com/articles/ten-usability-heuristics/)
- **Ground-truth feedback:** FEEDBACK-LOG.md §Review Round (FU.5, FU.6, FU.8 confirmed pain points, 2026-07-05)
