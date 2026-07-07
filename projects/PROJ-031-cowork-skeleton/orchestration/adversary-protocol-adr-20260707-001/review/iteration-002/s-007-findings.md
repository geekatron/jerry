# Constitutional Compliance Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology) — Iteration 2

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional assessment |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Full evidence and analysis per finding |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Constitutional Compliance Score](#constitutional-compliance-score) | S-007 operational score (distinct from S-014 composite) |
| [Methodology Note](#methodology-note) | What was and was not verified |

---

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3 (per invoking task; consistent with the ADR's own c-007 self-classification, AE-002/AE-003)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-007, blind, iteration 2)
**Constitutional Context:** `.context/rules/quality-enforcement.md` (HARD Rule Index, Criticality Levels, Strategy Catalog), `.context/rules/agent-development-standards.md` (H-34, Tool Security Tiers, Handoff Protocol), `.context/rules/agent-routing-standards.md` (H-36), CLAUDE.md (H-01–H-05, H-31)

---

## Summary

**PARTIAL compliance.** The deliverable is evidence-disciplined — every citation spot-checked against the tournament corpus (file counts, quoted scores, quoted rationale) resolved exactly as stated, including the ADR's own disclosed corrections. The genuine constitutional problem is narrower and sharper: **the specification for the new `adv-verifier` agent (D-6) is internally self-contradictory on tool tier vs. required behavior**, which is a Critical-severity defect because it makes the work-item as written non-implementable without a silent tier change, and it touches P-002 (File Persistence) and the H-34 Tool Security Tier system directly. One further Major finding concerns an unaddressed "blindness" enforcement gap, and one Major concerns an SSOT single-source-of-truth completeness risk. One Minor concerns a `scope:` vs. location ambiguity inherited from the still-draft ADR-M convention.

- **Findings:** 1 Critical, 2 Major, 1 Minor
- **Recommendation:** REVISE (Critical finding blocks acceptance per H-13; the fix is text-only and narrowly scoped — no new machinery required, consistent with the ADR's own subtraction-first doctrine)

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-iter2 | H-34 / P-002 (agent tool-tier vs. required file persistence) | HARD | Critical | ADR lines 604, 614–616, 762, 777–782 vs. `agent-development-standards.md` Tool Security Tiers (T1 row) | Methodological Rigor / Actionability |
| CC-002-iter2 | H-34 (agent independence design completeness) | MEDIUM | Major | ADR lines 612–613, 742 | Methodological Rigor |
| CC-003-iter2 | quality-enforcement.md SSOT completeness (c-002) | MEDIUM | Major | ADR lines 215, 403, 646–648, 765 vs. quality-enforcement.md Criticality Levels table | Internal Consistency / Traceability |
| CC-004-iter2 | ADR-M-007 (`scope:` vs. location) | MEDIUM (draft convention) | Minor | ADR frontmatter lines 5–6, 93–96 vs. `adr-standards-rule-draft.md:52` | Internal Consistency |

**Finding ID Format:** `CC-{NNN}-iter2` (execution_id = `iter2`, this being the second S-007 execution against this deliverable).

---

## Finding Details

### CC-001-iter2: `adv-verifier` Tool-Tier Self-Contradiction (T1 Read-Only vs. Mandatory File Persistence) [CRITICAL]

**Principle:** H-34 (agent definition standards; `tool_tier` MUST be schema-valid and, per the Tool Security Tier selection guidelines, MUST match what the agent's documented function actually requires) and P-002 (File Persistence — every worker agent's output MUST be persisted to a file, not left in transient context).

**Location:** ADR `## L1 Technical Implementation`, item 1 (lines 602–618); repeated at `## Work-Item Decomposition`, WI-1 (line 762); repeated again at Draft GitHub Issue A (lines 776–782).

**Evidence (verbatim, deliverable):**

> "Tool tier **T1 (read-only: Read, Glob, Grep)** — a verifier must not edit or spawn; guarantees P-003 safety and blindness." (line 604)
>
> "Output = a per-lens verdict `VERIFIED | REFUTED` with a one-paragraph justification and a file+line citation, **persisted** to `.../adversary/iteration-NNN/verify/{finding-id}-{lens}.md`." (lines 614–616)
>
> WI-1 acceptance criteria: "`skills/adversary/agents/adv-verifier.md` + `.governance.yaml` created; **T1 tools only**; H-34 (incl. sub-item b, ex-H-35) schema-valid; one-invocation-per-lens-per-claimed-Critical contract; DEFAULT-REFUTED; **per-lens verdict files persisted**; P-003 self-check present." (line 762)
>
> Draft Issue A body: "AC: agent + governance.yaml schema-valid (H-34, incl. sub-item b, ex-H-35); **T1 tools only**; **per-lens verdict files persisted**; P-003 self-check." (lines 777–782)

**Evidence (verbatim, SSOT for the T1 tier definition — `.context/rules/agent-development-standards.md`, Tool Security Tiers section):**

> "| **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring, validation | pe-scorer, diataxis-classifier, sb-voice |"
> "| **T2** | Read-Write | T1 + Write, Edit, Bash | Analysis, document production, code generation | ps-critic, adv-scorer, uc-author |"
>
> Selection Guidelines: "2. **T2 when the agent produces artifacts.** Writing files (reports, analysis, code) requires T2 minimum."

**Impact:** T1 is defined framework-wide as `Read, Glob, Grep` — it structurally excludes `Write`. Persisting a new file (the per-lens verdict `.md`) requires `Write`. The ADR's own three restatements of the `adv-verifier` contract (L1 item 1, WI-1, Issue A) each assert **both** "T1 tools only" **and** "per-lens verdict files persisted" as simultaneous, non-negotiable requirements — but per the framework's own Tool Security Tier system (which H-34 requires every agent's `tool_tier` field to conform to), these two requirements cannot both be satisfied by a single agent. This is not a hypothetical edge case: it is the literal, load-bearing output contract of the entire D-6 decision — the per-lens verdict files are the artifact the whole verification architecture depends on (Fig. 1, Fig. 2, Fig. 4; cited "12–15 verifier files per round" cost model). As written, a builder implementing WI-1 exactly as specified cannot produce a schema-valid, functioning agent: either the agent silently gets `Write` added (contradicting the ADR's stated tier and its stated rationale, which invokes T1 read-only specifically to argue P-003 safety) or the agent genuinely has only `Read, Glob, Grep` and cannot execute its own Output Format contract (violating P-002, the same constitutional principle every existing adversary agent — adv-selector, adv-executor, adv-scorer — explicitly declares compliance with in their own `<constitutional_compliance>` blocks: `tools: Read, Write, Glob` for adv-selector; `tools: Read, Write, Edit, Glob, Grep` for adv-scorer).

The ADR's own stated rationale for T1 ("a verifier must not edit or spawn") is actually an argument against `Edit` and `Task`/`Agent`, not against `Write` — creating a *new* file at a fresh path (`verify/{finding-id}-{lens}.md`) does not require modifying the deliverable or any existing file. The correct tier for "must persist new files but must not edit existing ones or spawn subagents" is closer to T2 with an explicit added guardrail forbidding edits to the deliverable/prior verdict files, not T1. As written, the spec conflates "read-only" (no Write) with "non-destructive" (no Edit) — these are different tool grants in the framework's own taxonomy, and the ADR uses the wrong one three times.

**Dimension:** Methodological Rigor (the agent-design decision, D-6, is not executable as specified) and Actionability (WI-1's acceptance criteria are self-contradictory; a builder cannot satisfy both bullets simultaneously).

**Remediation:** Change "Tool tier T1 (read-only: Read, Glob, Grep)" to a tier that includes `Write` (e.g., state the tier explicitly as "T1 + Write only — no Edit, no Bash, no Agent/Task" or adopt T2 with an added `forbidden_actions` entry: "NEVER edit the deliverable or any prior verdict file"), and propagate the correction to all three restatements (L1 item 1, WI-1, Issue A). This is a text-only fix; no new machinery is required, consistent with the ADR's own subtraction-first doctrine (D-3).

---

### CC-002-iter2: "Architectural" Blindness Claim Not Enforced Against Cross-Lens Filesystem Reads [MAJOR]

**Principle:** H-34 (agent guardrail completeness — an agent's independence claims should be backed by an actual technical barrier, not only a prompt-level instruction, when the ADR itself explicitly labels the claim "architectural").

**Location:** ADR `## L1 Technical Implementation`, item 1 (lines 612–613); `## Risks`, RSK-2 (line 742).

**Evidence (verbatim):**

> "The agent **MUST NOT receive** the other lenses' verdicts or the scorer's context (blindness)." (lines 612–613, invocation-contract language — an instruction to the orchestrator about what to *include in the prompt*, not a technical restriction on what the agent *can read*)
>
> RSK-2 mitigation: "Blindness is enforced **architecturally** (separate T1 invocations, no shared context, no scorer context) and distinct rubrics per lens; verdicts persisted as separate files for audit." (line 742)

**Analysis:** `adv-verifier` is granted `Glob` and `Read` (per its own T1 declaration) and its invocation contract gives it "the deliverable path" — the same directory tree that also contains `.../adversary/iteration-NNN/verify/`, where sibling lenses' verdict files are persisted (per CC-001-iter2's own cited output contract). If the three lens invocations for the same claimed Critical are not run strictly in parallel (the ADR specifies no ordering guarantee — Fig. 4 shows "3 lenses per Critical" without stating simultaneity), a later-invoked lens has both the tool access (`Glob`/`Read`) and, plausibly, the directory-naming knowledge (`{finding-id}-{lens}.md` is documented in the ADR itself) to locate and read an earlier lens's already-persisted verdict — even though its prompt "MUST NOT receive" that verdict. The only barrier against this is a behavioral instruction ("MUST NOT receive"), not the "architectural" enforcement RSK-2 claims. This is exactly the class of gap the ADR is otherwise unusually careful to distinguish (RSK-2's own next sentence: "context isolation delivers *context* independence, **not** *reasoning* independence" — but that caveat addresses model-correlation, not this separate, addressable filesystem-access vector, which goes unaddressed). Given that independence is stated to be "the load-bearing property" for the entire D-1 decision (Force 6, D-1 rationale), an unaddressed technical vector by which blindness can be structurally defeated is a genuine gap, not a nitpick.

**Dimension:** Methodological Rigor (the independence mechanism the whole ADR is built around is asserted as stronger — "architectural" — than what is actually specified) / Internal Consistency (RSK-2's own honesty-caveat pattern is not applied to this adjacent, addressable gap).

**Remediation:** Either (a) specify that the three lens invocations for a given claimed Critical MUST run before any of their outputs are read by a subsequent invocation (i.e., true parallelism, or a documented ordering guarantee), or (b) scope the agent's `Glob`/`Read` grant to exclude the `verify/` directory for lens invocations still in flight, or (c) downgrade RSK-2's "enforced architecturally" to "enforced by invocation-contract instruction, with a residual filesystem-access vector disclosed" — consistent with the ADR's own disclosure discipline elsewhere (e.g., RSK-1, RSK-2's own model-correlation caveat).

---

### CC-003-iter2: New Mandatory Verify Stage Not Reflected in the SSOT's Own Criticality Levels Table [MAJOR]

**Principle:** c-002 (this ADR's own constraint: "SSOT constants (weights, threshold, criticality sets) are referenced, never redefined") and the general SSOT single-source-of-truth discipline underlying `quality-enforcement.md`.

**Location:** ADR constraint c-002 (line 215); D-1 decision (line 403: "C4 all Criticals; C3 Criticals only; C1–C2 none"); WI-4 acceptance criteria (line 765); L1 item 7 (lines 646–648) — vs. `.context/rules/quality-enforcement.md` Criticality Levels table (`Required Strategies` column for C3/C4).

**Evidence (verbatim, deliverable):**

> D-1 decision row: "**C — criticality-proportional 3-lens refutation panels** (C4 all Criticals; C3 Criticals only; C1–C2 none)." (line 403)
>
> WI-4 AC: "Verify stage added between Groups E and F; **C4 = all Criticals, C3 = Criticals only, C1–C2 = none**; H-16 and Group-F-last preserved; AE re-check documents gating." (line 765)
>
> L1 item 7: "Edit `.context/rules/quality-enforcement.md` (Implementation section only) — add a pointer to the verified-criticals protocol and this ADR. **No HARD rule, weight, threshold, or criticality set is changed** (c-001)." (lines 646–648)

**Evidence (verbatim, SSOT — `quality-enforcement.md` Criticality Levels table, current text, this repository):**

> "| C3 | Significant | ... | All tiers | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |"
> "| C4 | Critical | ... | All tiers + tournament | All 10 selected | None |"

**Analysis:** The Verify stage is described as *mandatory, not optional*, at C3 (for Criticals) and C4 (for all Criticals) — it gates the automatic-REVISE outcome (D-2), which is exactly the kind of "what must happen at this criticality level" fact the Criticality Levels table exists to answer for a reader. Yet the ADR deliberately scopes its only SSOT edit to "the Implementation section" (a pointer/reference), explicitly declining to touch the Criticality Levels table itself (c-001/c-002). The result: a reader consulting the authoritative SSOT table for "what is required at C3/C4" will see the unchanged 10-strategy list and have no indication that a mandatory adjudication stage now also applies. This may be a defensible, intentional design choice (there is a real precedent — `adv-scorer.md`'s own gating rule, "Any Critical finding → automatic REVISE," already lives outside the SSOT table today), but the ADR does not name or defend this precedent, and does not explain why a *new*, criticality-differentiated mandatory gate is different in kind from a decision worth stating that this is a deliberate, precedent-following omission versus an accidental one. Left as-is, this is a genuine two-sources-of-truth risk: `quality-enforcement.md` and `skills/adversary/agents/adv-selector.md`/`SKILL.md` can drift on what C3/C4 actually requires, with no single table a reader can trust for the full picture.

**Dimension:** Internal Consistency (SSOT vs. skill-level requirements can diverge) / Traceability (a reader cannot derive "is the Verify stage required at C3?" from the SSOT alone).

**Remediation:** Either (a) add one row/footnote to the Criticality Levels table itself (e.g., "C3/C4: Verify stage (refutation panel) additionally REQUIRED on claimed Criticals — see Implementation pointer"), which is a small, MEDIUM-tier-consistent edit, not a redefinition of weights/thresholds/strategy sets; or (b) explicitly name the `adv-scorer.md`-gating precedent in L1 item 7 and state why the Verify stage is intentionally kept out of the SSOT table by the same precedent. Either resolves the traceability gap without adding machinery.

---

### CC-004-iter2: `scope: framework` Declared While Physically Located in a Project `decisions/` Directory, Pre-Promotion [MINOR]

**Principle:** ADR-M-007 (draft convention this ADR dogfoods): "Scope is expressed by **location** (may change); identity SHOULD NOT change when location changes."

**Location:** ADR frontmatter, lines 5–6 (`scope: framework`, `origin_project: PROJ-031`); Status section, lines 93–96.

**Evidence (verbatim, deliverable frontmatter):**

> `scope: framework                             # governs the /adversary skill + tournament process framework-wide` (line 5)

**Evidence (verbatim, `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:52`):**

> "**ADR-M-007** | A framework-governing ADR SHOULD live in `docs/design/`; a project ADR in `projects/PROJ-NNN-*/decisions/`. Scope is expressed by **location** (may change); identity SHOULD NOT change when location changes."

**Analysis:** The reviewed ADR declares `scope: framework` in frontmatter while its file physically resides at `projects/PROJ-031-cowork-skeleton/decisions/` — a project location per the very table ADR-M-007 belongs to — and its status is `PROPOSED`, not yet promoted. ADR-M-007's own phrasing ("scope is expressed by location") reads most naturally as *scope tracks where the file currently lives*, which would imply `scope: project` until the Path-1 `git mv` in the Status section actually happens. The reviewed ADR instead declares the *aspirational, post-promotion* scope at authoring time. This is plausibly intentional and even desirable (ADR-M-013 only mandates defaulting to `project` "when uncertain," and this ADR's author is not uncertain that it governs a framework skill) — but the draft convention does not explicitly reconcile a PROPOSED-and-not-yet-relocated framework-scoped ADR with ADR-M-007's location-expresses-scope framing, so this is a genuine, if soft, ambiguity rather than a clear violation. It does not undermine the ADR's technical content and the convention itself is still in draft (per `adr-standards-rule-draft.md`'s own wrapper note), so severity is capped at Minor.

**Dimension:** Internal Consistency.

**Remediation:** Optional one-line clarification in the Meta-Note or Status section: state explicitly that `scope: framework` is declared prospectively at authoring time (permitted under ADR-M-013's "not uncertain" carve-out) rather than reflecting current location, so a future reader of the still-draft `adr-standards.md` does not read this ADR as evidence that ADR-M-007's location-expresses-scope framing is optional.

---

## Remediation Plan

**P0 (Critical):** CC-001-iter2 — Correct the `adv-verifier` tool-tier declaration (all three restatements: L1 item 1, WI-1, Issue A) so it is consistent with a P-002-compliant, file-persisting agent; the current "T1 read-only" + "persisted verdict files" pairing is self-contradictory and non-implementable as specified.

**P1 (Major):** CC-002-iter2 — Specify an actual technical barrier (ordering guarantee or directory-scope restriction) for cross-lens blindness, or downgrade the "architectural" claim in RSK-2 to match what is actually specified. CC-003-iter2 — Add a Criticality Levels table footnote/row for the new mandatory Verify stage, or explicitly name and justify the `adv-scorer.md`-precedent for keeping it SSOT-external.

**P2 (Minor):** CC-004-iter2 — Add one clarifying sentence reconciling prospective `scope: framework` declaration with ADR-M-007's location-expresses-scope framing.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No finding affects requirements coverage; the ADR's scope (six coordinated decisions) is fully addressed. |
| Internal Consistency | 0.20 | Negative | CC-002 (Major): "architectural" blindness claim overstated relative to the specified mechanism. CC-003 (Major): SSOT table vs. skill-level requirement can diverge. CC-004 (Minor): scope/location tension. |
| Methodological Rigor | 0.20 | Negative | CC-001 (Critical): the D-6 agent-design decision is not executable as specified — a HARD-adjacent defect in the one place this ADR is proposing new agent machinery. CC-002 (Major) also lands here (independence design completeness). |
| Evidence Quality | 0.15 | Positive | Every citation spot-checked this iteration (file counts in `verify/` directories, quoted scorer language, quoted risk mitigations) resolved exactly as the ADR states, including its own disclosed corrections (the "12 files" fix, the 0.460/0.468 delta, the fabricated-PR-template incident). No unsupported claims found. |
| Actionability | 0.15 | Negative | CC-001 (Critical): WI-1's acceptance criteria cannot both be satisfied as written; a builder would have to silently resolve the contradiction, undermining "implementable specification." |
| Traceability | 0.10 | Negative | CC-003 (Major): a reader cannot derive the full C3/C4 requirement set from the SSOT table alone once this ADR ships. |

---

## Constitutional Compliance Score

Per the S-007 template's own operational penalty model (Step 5; distinct from and not a substitute for the S-014 tournament composite computed by adv-scorer):

- 1 Critical × -0.10 = -0.10
- 2 Major × -0.05 = -0.10
- 1 Minor × -0.02 = -0.02
- Base 1.00 − 0.22 = **0.78**

**Threshold Determination:** REJECTED band (< 0.85) on this strategy's own operational rubric — driven entirely by CC-001-iter2 (Critical). Note this operational score is a constitutional-critique-specific instrument (S-007 Scoring Rubric), not the authoritative H-13 gate; the authoritative composite and PASS/REVISE/ESCALATE verdict for this deliverable is computed by adv-scorer per SSOT, which under this very ADR's own proposed VERIFIED-CRITICALS protocol would first route CC-001-iter2 through a 3-lens refutation panel before it counts.

---

## Methodology Note

This execution followed the S-007 protocol (`.context/templates/adversarial/s-007-constitutional-ai.md`, Steps 1–5): constitutional context loaded from `quality-enforcement.md`, `agent-development-standards.md`, and `agent-routing-standards.md`; applicable principles enumerated (H-13, H-14, H-16, H-23, H-31, H-34, H-36, P-002, P-003, P-020, P-022, RT-M-010, AE-001–AE-006); each candidate finding evaluated against the deliverable's own text and, where verifiable, against the cited evidence corpus (`orchestration/adr-convention-20260702-001/`, `orchestration/fu-log-convention-20260705-001/`) and the live agent/skill files it proposes to edit (`skills/adversary/agents/adv-scorer.md`, `adv-selector.md`, `skills/adversary/SKILL.md`).

Citations independently verified this iteration (all confirmed accurate, no discrepancies found):
- `fu-log-convention-20260705-001/adversary/iteration-008/verify/` — confirmed exactly 12 files (matches the ADR's disclosed correction from "18" to "12").
- `adr-convention-20260702-001/adversary/iteration-009/verify/` — confirmed exactly 15 files (3 lenses × 5 Criticals).
- `adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md:36-37` — confirmed "Verified Criticals: 5" / "Refuted Criticals: 5" quoted exactly.
- `adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md:128-135` — confirmed the "~0.18-point difference" quote exactly.
- `fu-log-convention-20260705-001/adversary/iteration-006/s-014-quality-score.md:19-20,56` — confirmed the 0.460/0.468 declining-score figures and the "closes the specific instance ... but has not yet closed the class of problem" quote exactly.
- `adr-convention-20260702-001/adversary/iteration-010/post-ceiling-fix-notes.md:55-65` — confirmed the fabricated `PULL_REQUEST_TEMPLATE.md` claim and its correction exactly.
- `skills/adversary/agents/adv-scorer.md:166-167`, `skills/adversary/agents/adv-scorer.md:68-91`, `skills/adversary/agents/adv-selector.md:89-107,112-128`, `skills/adversary/SKILL.md:111-133` — all confirmed to match the ADR's paraphrases/quotes.

Not independently re-derived this iteration (out of scope for a constitutional-critique pass; noted, not treated as a gap): the full 18-round evidence chain's causal narrative (declining-score root-cause attribution), and the `adr-standards-rule-draft.md` lint specification's own internal residual register (R-1…R-18), which the reviewed ADR references but does not itself assert new claims about beyond what was independently checked above.

No findings were omitted or minimized. All four findings above are believed genuine and load-bearing against the stated review criteria (evidence-decision traceability, implementable specification, honest costs/limits); CC-001-iter2 in particular is offered with file+line citations sufficient for independent refutation-panel adjudication under this ADR's own proposed protocol.
