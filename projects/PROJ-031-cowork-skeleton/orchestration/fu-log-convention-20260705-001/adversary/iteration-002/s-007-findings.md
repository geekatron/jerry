# Constitutional Compliance Report: Feedback & Decision Log Convention (iteration 2)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-007, blind, iteration 2)
**Constitutional Context:** JERRY_CONSTITUTION principles P-001 (Truth), P-020 (User Authority), P-022 (No Deception); HARD rules H-03 (=P-022), H-23/H-24 (nav tables), H-19 (AE escalation), H-31 (clarify when ambiguous), H-32 (GH parity); `quality-enforcement.md` Tier Vocabulary (HARD ceiling 25/25) and MEDIUM-tier standards conventions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional verdict |
| [Findings Table](#findings-table) | All findings, severity, evidence pointer |
| [Compliant / No-Finding Checks](#compliant--no-finding-checks) | Explicitly-tasked checks that PASS |
| [Finding Details](#finding-details) | Full evidence + analysis per finding |
| [Recommendations](#recommendations) | P0/P1/P2 remediation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping + compliance score |

---

## Summary

**PARTIAL compliance.** The four explicitly-tasked checkpoints (H-23 nav tables, P-022 hook-disclosure honesty, P-020 open-question labelling, public-repo hygiene) all **PASS** with clean evidence across all five reviewed files. However, an independent principle-by-principle sweep surfaced **1 Critical, 1 Major, 2 Minor** findings, the load-bearing one being an **overclaimed transcript-fidelity guarantee**: the main design document properly hedges "full fidelity is recoverable *provided the JSONL transcript is retained*" (an admitted, unenforced assumption), but three of the four staged artifacts that operators will actually read day-to-day restate the same claim as an unqualified fact ("the JSONL is the byte-exact record," "not a loss of fidelity"). This is the pattern the task brief calls out as Critical-by-definition ("overclaimed coverage IS Critical") — it is a P-022/H-03 (no deception) issue localized to a few sentences, not a structural defect, and is fixable by wording propagation alone (consistent with the package's own anti-bloat, fix-by-simplifying doctrine). Constitutional compliance score: **0.81** (REJECTED per S-007 band; driven entirely by the single Critical). Recommend a targeted P0 wording fix (no new machinery) plus three smaller clarifications.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-i2 | P-022/H-03: No deception about capability/guarantees | HARD | **Critical** | `staging-feedback-logs/feedback-decision-logs-standards.md:44`, `staging-feedback-logs/LLM-DECISION-LOG.template.md:23`, `staging-feedback-logs/examples-appendix.md:114` state the transcript pointer is unconditionally "byte-exact"/"not a loss of fidelity," while `design/feedback-decision-log-convention-design.md:113` discloses this is contingent on unenforced transcript retention | Internal Consistency / Evidence Quality |
| CC-002-i2 | Internal consistency of MEDIUM-tier rule doc (L5 lint spec) | MEDIUM | Major | `design/feedback-decision-log-convention-design.md:201,214,248` — "a gap is never legitimate" contiguity claim is not reconciled with the Q4 Backfill mechanism's id-assignment method | Completeness / Methodological Rigor |
| CC-003-i2 | MEDIUM-tier vocabulary discipline (HARD-ceiling purity doctrine) | SOFT | Minor | `staging-feedback-logs/hook-design-note.md:39-42,46,50` use MUST/MUST NOT language inside a package that otherwise deliberately avoids HARD-tier vocabulary | Internal Consistency |
| CC-004-i2 | Traceability of stated user requirement (background agents) | SOFT | Minor | FU.2 verbatim ("leverage background agents…") vs. `design/…-design.md:70,193` "single-writer-per-log" discipline — no explicit reconciliation | Traceability |

**Finding ID format:** `CC-{NNN}-i2` (iteration 2, this execution).

**Severity definitions:** Critical = HARD-tier violation, blocks acceptance (H-13). Major = MEDIUM-tier violation, requires revision or documented justification. Minor = SOFT-tier, improvement opportunity.

---

## Compliant / No-Finding Checks

Documented per Step 3 ("COMPLIANT: document supporting evidence") for the four checkpoints the orchestrator explicitly named, plus one structural sweep, so this report does not read as one-sided (P-022 applies to this report too):

| Checkpoint | Verdict | Evidence |
|---|---|---|
| **H-23 nav tables + anchor links (H-24 sub-item)** across all 5 files | **COMPLIANT** | Every file has a `## Document Sections` (or equivalent) table immediately after the frontmatter blockquote; every anchor was hand-traced against its target heading's GitHub-slug and resolves correctly (e.g. `design/…-design.md:18` `#l13-automation-hook-assisted-capture` → `design/…-design.md:137` `### L1.3 Automation (hook-assisted capture)`; `staging-feedback-logs/LLM-DECISION-LOG.template.md:14` `#dec-llm-001-example-entry-alias-` → `:39` `## DEC-LLM-001 example-entry (alias: —)`). No broken anchors found. |
| **P-022 hook-disclosure honesty** ("hook is DESIGNED not shipped"; "must-log is model-dependent until hook ships") | **COMPLIANT** | `design/…-design.md:30` scopes the L0 claim explicitly: "Capture stays a MEDIUM (SHOULD) discipline until the fail-open hook of Q3 ships." `staging-feedback-logs/hook-design-note.md:1-3` opens with "**Design-only.** No framework path is touched by this note. Installing any hook is a separate, gated step." `staging-feedback-logs/hook-design-note.md:56` labels shipping timing "PROPOSED-DEFAULT (Q3, pending ratification)." Consistent across all three surfaces. |
| **P-020** — 4 open questions still PROPOSED-DEFAULT, not decided | **COMPLIANT** | `design/…-design.md:241` header: "These are **proposals, not decisions** — the design proceeds on them provisionally, and each still requires explicit user ratification (P-020)." Every downstream artifact that restates a default labels it: `feedback-decision-logs-standards.md:25,44,57` ("PROPOSED-DEFAULT"), `LLM-DECISION-LOG.template.md:27` ("PROPOSED-DEFAULT... pending user ratification"), `hook-design-note.md:56`. The live bootstrap `FEEDBACK-LOG.md:4` banner also states "pending final user ratification" (not itself in review scope, but consistent). No artifact silently treats a PROPOSED-DEFAULT as ratified. |
| **Public-repo hygiene** (no internal refs / absolute paths) | **COMPLIANT** | Grep across the entire `design/` tree for `[home]/`, `[employer]`, `[employer]` returned zero matches inside the reviewed deliverable (one unrelated match exists in `design/qg3-review/s-014-quality-score.md`, which is **not** part of this review's deliverable scope). Grep for the operator's actual home path (`jerry-wt`, `adam.nowak`, `saucer.boy`, `proj-030-skeleton-branch`) also returned zero matches. All internal identifiers already carry the FU.4 redaction pattern (`[internal-kb]`, `[legacy-fu-id]`, `[legacy-oi-id]`). |
| **MEDIUM-tier purity of the operative rule file** (no MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) | **COMPLIANT** (rule file itself) — see CC-003 for a narrower exception in a non-rule artifact | Grep of `staging-feedback-logs/feedback-decision-logs-standards.md` for `MUST\|SHALL\|NEVER\|FORBIDDEN\|REQUIRED\|CRITICAL` returned zero matches; all 6 LOG-M-* rows use SHOULD-tier diction. Same zero-match result for the design doc body, both templates, and the examples appendix. |

---

## Finding Details

### CC-001-i2: Overclaimed transcript-fidelity guarantee across staged artifacts [CRITICAL]

**Principle:** P-022 / H-03 — no deception about actions, capabilities, or confidence.

**Locations:**
- `design/feedback-decision-log-convention-design.md:113` (properly hedged baseline): *"full fidelity is recoverable **provided the JSONL transcript is retained and its pointer resolves on the reading machine** (the transcript is the byte-exact source of record). That retention/cross-machine-portability dependency is **an assumption this convention does not itself enforce** (`[INFERENCE]`: no transcript-retention policy is cited)."*
- `staging-feedback-logs/feedback-decision-logs-standards.md:44`: *"excerpt + pointer — full paste re-creates context-rot; **the JSONL is the byte-exact record**. Full paste optional for C3+/ADR-graduating decisions. Size math + rationale: design doc Q1."* — the pointer to "design doc Q1" is scoped to "size math + rationale," not to the retention caveat; the claim itself is unqualified.
- `staging-feedback-logs/LLM-DECISION-LOG.template.md:23`: *"the full turn is **recoverable from the immutable JSONL**; the excerpt keeps the log loadable... **this is intentional, not a loss of fidelity**."* — the strongest instance: this is the exact sentence every future operator reads while filling out a real entry, and it flatly denies any fidelity loss with zero hedge and zero pointer.
- `staging-feedback-logs/examples-appendix.md:114`: *"...the **byte-exact** full turn stays recoverable from the **immutable JSONL**."* — restates the unqualified claim a third time, in the artifact explicitly designed (FU.8) to be the rationalizable reference operators consult instead of the design memo.

**Impact:** The entire rationale for choosing "Option B — excerpt + pointer" over "Option A — full paste" (`design/…-design.md:106-115`) rests on the premise that the excerpted assistant text is not actually lossy because the full turn remains recoverable from the transcript. The design document itself admits this recoverability is **not enforced by this convention** and cites no retention policy. Three of the four artifacts operators will actually use post-install (the rule file that installs into `.context/rules/`, the decision-log template every entry is copied from, and the examples appendix the rule file points readers to) drop that caveat and assert the guarantee as settled fact. An operator who only ever reads the installed rule + template — the expected, intended reading path once this graduates — would reasonably believe recoverability is assured, when the source design document discloses it is not. This is precisely the "governing principle" the whole convention is built to defend against (`design/…-design.md:38`: *"what depends on the model remembering will eventually be forgotten"*) — applied here to a *transcript* dependency instead of a model-memory dependency, and left undisclosed at the point of use.

**Why Critical, not Major:** The task brief is explicit that overclaimed coverage/guarantees are Critical-by-definition in this review. This also maps directly to a HARD rule (H-03/P-022): a confidence/capability claim ("byte-exact," "not a loss of fidelity") stated as fact in the operative artifacts while the same package discloses it as an unenforced assumption elsewhere. It is downgraded from "structural" concern because remediation is a wording-propagation fix only (no new machinery required) — consistent with the package's established anti-bloat, fix-by-simplifying doctrine already used for the v3 remediation round.

**Recommendation:** Propagate the existing hedge (already correctly written once, at `design/…-design.md:113`) into all three downstream call-outs. Minimal-diff suggestion: append "(while the transcript is retained — see design doc Q1)" to each of the three quoted claims, and soften `LLM-DECISION-LOG.template.md:23`'s "not a loss of fidelity" to "keeps the log loadable; full fidelity depends on transcript retention (design doc Q1)." No schema, lint, or mechanism change required.

---

### CC-002-i2: Backfill id-assignment vs. asserted id contiguity [MAJOR]

**Principle:** Internal consistency of the MEDIUM-tier rule specification (LOG-M-005/LOG-M-006 and the L5 lint description within the same reviewed package).

**Locations:**
- `design/feedback-decision-log-convention-design.md:201` (L5 lint check 2): *"`FU.N` / `DEC-LLM-NNN` ids are unique, strictly increasing, **and contiguous (no gaps)** across all segments of each log... since the log is append-only, **a gap is never legitimate**."*
- `design/feedback-decision-log-convention-design.md:214` (Adoption plan step 5): *"**Backfill** (optional, Q4) — the two Backfill Queues list pre-log items; adopt retroactively or leave forward-only."*
- `design/feedback-decision-log-convention-design.md:248` (Q4 row): *"**Supported by the design** (BACKFILL-marked candidate rows in both Backfill Queues); execution pending user authorization — not auto-adopted."*

**Impact:** The design categorically asserts contiguity is an invariant the log can never legitimately violate, then separately proposes a backfill mechanism to retroactively adopt pre-log items "authorized" by the user — without specifying what canonical id a backfilled entry receives, or how that assignment interacts with the append-order monotonicity the contiguity lint depends on. If a backfilled item is inserted at a historically-accurate position (as its "retroactive" framing implies), it would either require renumbering already-assigned ids (breaking the "ids never reset/move" guarantee elsewhere in the design) or be appended at the current tail with a present-day id carrying a historical date (which the design never states). Either resolution is workable, but neither is chosen, leaving the "a gap is never legitimate" claim and the backfill feature in an unreconciled state.

**Recommendation:** Add one sentence to either the Q4 row or the L5 lint check 2 description clarifying that backfilled entries are appended at the current tail with the next available canonical id (historical date recorded in the entry body, not encoded in the id), and are therefore exempt from — not a counterexample to — the contiguity invariant. This is a documentation addition, not new machinery.

---

### CC-003-i2: HARD-tier vocabulary inside a MEDIUM-tier-disciplined package [MINOR]

**Principle:** Tier-vocabulary discipline (`quality-enforcement.md` Tier Vocabulary: HARD keywords MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL are reserved for the 25/25-ceiling HARD rule set).

**Locations:** `staging-feedback-logs/hook-design-note.md:39-42` (four "MUST NOT" bullets), `:46` ("A capture hook **MUST be fail-open**"), `:50` ("It **MUST NOT** rotate autonomously").

**Impact:** Every other artifact in this package (the rule draft, both templates, the design doc, the examples appendix) deliberately avoids HARD-tier vocabulary specifically because the HARD ceiling is full (25/25) and this convention must remain MEDIUM-tier (`design/…-design.md:183-185`). `hook-design-note.md` is explicitly out-of-scope for `.context/rules/` (it targets `hooks/`, a separate gated change, per its own header at `:1-3`), and its MUST-language describes code-implementation contracts for a not-yet-built script rather than a Jerry governance rule — so this is not an actual ceiling violation. It is, however, a stylistic inconsistency in a package that otherwise treats tier-vocabulary purity as a first-class constraint, and it creates a small risk of confusing a future automated ceiling-compliance sweep or a reviewer who greps for HARD keywords across the whole staged directory rather than scoping to `.context/rules/`.

**Recommendation:** Either (a) reword the four bullets to SHOULD-tier for full-package consistency, or (b) add one clarifying sentence at the top of `hook-design-note.md` noting that its MUST/MUST NOT language specifies code-implementation contracts for the (separately gated) hook script, not Jerry HARD-rule-tier governance, and is therefore exempt from the 25/25 ceiling accounting.

---

### CC-004-i2: Background-agent requirement not explicitly reconciled with single-writer discipline [MINOR]

**Principle:** Traceability — a load-bearing user requirement should be explicitly reconciled with a design constraint that touches it.

**Locations:** FU.2 verbatim requirement (context file, `FEEDBACK-LOG.md` FU.2): *"I would like you to use the most appropriate jerry (jerry:*) skills and agents to build this into the Jerry Framework and **leverage background agents so that we don't burn through the main context window**."* vs. `design/feedback-decision-log-convention-design.md:70,193`: *"under a **single-writer-per-log** append discipline"* / *"Concurrent writers appending to the *same* log file (e.g. **parallel/background agents**) are a **disclosed residual risk**."*

**Impact:** This is honestly disclosed (satisfies P-022 — it is not hidden), so it is not elevated beyond Minor. But the design never explicitly closes the loop back to the user's own stated rationale for wanting background agents (avoiding main-context burn), i.e., it does not state whether/why background-agent parallelism for the *broader* design/build work is unaffected by the single-writer constraint that applies specifically to *appending to these two ledger files*. A reader tracing FU.2 → design decisions could reasonably wonder whether the chosen id scheme quietly narrows the very capability the user asked for.

**Recommendation:** Add one sentence to L1.1 (or the FU.2 disposition) clarifying that background agents perform the substantive work in parallel, but only the orchestrating/main context appends to `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md`, preserving single-writer discipline without constraining background-agent use elsewhere.

---

## Recommendations

**P0 (Critical):** CC-001-i2 — propagate the retention/portability caveat from `design/…-design.md:113` into `feedback-decision-logs-standards.md:44`, `LLM-DECISION-LOG.template.md:23`, and `examples-appendix.md:114`. Wording-only fix; no new machinery.

**P1 (Major):** CC-002-i2 — add one sentence reconciling backfill id-assignment with the "no gaps ever legitimate" contiguity claim (L5 lint check 2 or the Q4 row).

**P2 (Minor):** CC-003-i2 — reword or disclaim the MUST/MUST NOT language in `hook-design-note.md`. CC-004-i2 — add one sentence reconciling single-writer discipline with the FU.2 background-agent requirement.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor-Major) | CC-002 (Major): backfill/contiguity interaction unresolved. |
| Internal Consistency | 0.20 | Negative (Critical) | CC-001 (Critical): three artifacts contradict the design doc's own hedged fidelity claim. CC-002/CC-003 compound this at Major/Minor. |
| Methodological Rigor | 0.20 | Negative (Major) | CC-002: lint specification not reconciled against the backfill feature it must also govern. |
| Evidence Quality | 0.15 | Negative (Critical) | CC-001: the unqualified "byte-exact"/"not a loss of fidelity" claims are assertions unsupported by (indeed contradicted by) the package's own disclosed evidence. |
| Actionability | 0.15 | Neutral | All findings carry a specific, wording-level fix; no finding blocks on an unresolved design question. |
| Traceability | 0.10 | Negative (Minor) | CC-004: FU.2's background-agent rationale not explicitly traced through to the single-writer constraint. |

**Constitutional Compliance Score:** `1.00 - (1 × 0.10 + 1 × 0.05 + 2 × 0.02) = 1.00 - 0.19 = 0.81`

**Threshold Determination:** REJECTED (< 0.85 band per S-007 SSOT bands) — driven entirely by the single Critical (CC-001). Contextual note: the underlying defect is a 3-sentence wording-propagation fix, not a structural or machinery gap; all four explicitly-tasked checkpoints (H-23, P-022 hook disclosure, P-020 labelling, public-repo hygiene) are fully compliant, and the package's overall constitutional discipline (nav-table hygiene, MEDIUM-tier purity of the operative rule file, honest process disclosure at FU.9) is strong.

---

*Execution: S-007 Constitutional AI Critique, iteration 2 (blind). Template: `.context/templates/adversarial/s-007-constitutional-ai.md`. P-003: no subagents invoked. P-020: draft-only, no writes outside `projects/PROJ-031-cowork-skeleton/`.*
