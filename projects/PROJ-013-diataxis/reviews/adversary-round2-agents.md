# Strategy Execution Report: Adversarial Quality Review Round 2

## Execution Context

- **Strategy:** S-007 (Constitutional AI Critique), S-013 (Inversion Technique), S-002 (Devil's Advocate), S-010 (Self-Refine)
- **Templates:** `.context/templates/adversarial/s-007-constitutional-ai.md`, `s-013-inversion.md`, `s-002-devils-advocate.md`, `s-010-self-refine.md`
- **Deliverables:** 12 files — 6 `.md` + 6 `.governance.yaml` in `skills/diataxis/agents/`
- **Criticality:** C3 (Significant — new skill, >10 files affected, >1 day to reverse)
- **Quality Threshold:** >= 0.95 weighted composite
- **Executed:** 2026-02-27
- **Reviewer:** adv-executor (Round 2)
- **Prior Round:** `projects/PROJ-013-diataxis/reviews/adversary-round1-agents.md`

### Deliverables Reviewed

| Agent | .md File | .governance.yaml File |
|-------|----------|----------------------|
| diataxis-tutorial | `skills/diataxis/agents/diataxis-tutorial.md` | `skills/diataxis/agents/diataxis-tutorial.governance.yaml` |
| diataxis-howto | `skills/diataxis/agents/diataxis-howto.md` | `skills/diataxis/agents/diataxis-howto.governance.yaml` |
| diataxis-reference | `skills/diataxis/agents/diataxis-reference.md` | `skills/diataxis/agents/diataxis-reference.governance.yaml` |
| diataxis-explanation | `skills/diataxis/agents/diataxis-explanation.md` | `skills/diataxis/agents/diataxis-explanation.governance.yaml` |
| diataxis-classifier | `skills/diataxis/agents/diataxis-classifier.md` | `skills/diataxis/agents/diataxis-classifier.governance.yaml` |
| diataxis-auditor | `skills/diataxis/agents/diataxis-auditor.md` | `skills/diataxis/agents/diataxis-auditor.governance.yaml` |

---

## Round 1 Fix Verification

The following Round 1 findings have been verified against the remediated files:

| Round 1 Finding | Severity | Fix Applied | Verified |
|----------------|----------|-------------|----------|
| IN-001: hint_quadrant confidence 1.00 bypass | Critical | classifier.md Step 5 now runs two-axis test first; caps at 0.85 on conflict | FIXED |
| CC-002/SR-003: howto .md missing Input Validation + Output Filtering | Major | howto.md now has both subsections in `<guardrails>` | FIXED |
| CC-003/SR-001: classifier output.required absent | Major | classifier.governance.yaml now has `required: true` | FIXED |
| CC-004/DA-005: howto cognitive_mode convergent | Major | howto.governance.yaml now `systematic`; identity prose updated | FIXED |
| CC-005/DA-001: explanation model opus unjustified | Major | explanation.md identity has Model Justification paragraph | FIXED |
| IN-002: No mixing resolution gate in writers | Major | All 4 writers have Mixing Resolution Gate in Step 5 | FIXED |
| IN-003: Auditor no multi-quadrant path | Major | auditor.md Step 2 has multi-quadrant handling + pipeline note | FIXED |
| IN-004/SR-005: Writers apply static inline criteria | Major | All 4 writers Step 4 now loads from diataxis-standards.md | FIXED |
| IN-005/DA-004: Tutorial/howto descriptions ambiguous | Major | Both descriptions now have negative routing signals | FIXED |
| DA-002: explanation has Bash with no usage pattern | Major | Bash removed from explanation.md tools | FIXED |
| SR-007: Bash verification success undefined | Major | tutorial.md Step 5b: adds `[VERIFICATION-FAILED]` annotation | FIXED |
| DA-003/IN-003 (auditor duplication note) | Major | auditor.md Step 2 now has pipeline-use disclaimer | FIXED |
| DA-006/CC-006: No session_context | Major | NOT FIXED — session_context absent from all governance.yaml | PERSISTS |
| CC-001: H-23 navigation table conflict | Major | NOT FIXED — no navigation tables in any .md | PERSISTS |
| DA-007: PASS threshold too lenient | Minor | NOT FIXED — still allows 2 Minor findings | PERSISTS |
| DA-008: No enforcement section | Minor | NOT FIXED — no enforcement block in any governance.yaml | PERSISTS |
| SR-002: auditor output path fallback in wrong section | Minor | NOT FIXED — still in `<output>` not `<guardrails>` | PERSISTS |
| SR-004: reasoning_effort not declared | Minor | NOT FIXED — no reasoning_effort in any .md frontmatter | PERSISTS |
| SR-006: Classifier multi-quadrant sequence gap | Minor | NOT FIXED — still uses sequential numbering with no gap handling | PERSISTS |
| SR-008: No classifier-to-writer mapping | Minor | NOT FIXED — no mapping defined | PERSISTS |
| SR-009: prior_art unused | Minor | NOT FIXED — no prior_art in any governance.yaml | PERSISTS |
| CC-007: howto P-022 forbidden_action generic | Minor | NOT FIXED — still generic wording | PERSISTS |
| IN-006: Bash verification failure handling | Minor | FIXED (subsumed by Step 5b VERIFICATION-FAILED annotation) | FIXED |

**Fix summary:** 12 of 23 Round 1 findings fixed. 11 persist (2 Major, 9 Minor). All Critical and top-priority Major findings resolved.

---

## S-007 Constitutional AI Critique

**Finding Prefix:** CC
**Execution ID:** 20260227R2

### Principle-by-Principle Evaluation

#### H-34 / H-35: HARD Rule Compliance

**Frontmatter fields (official only):** All 6 .md files use only official Claude Code fields (`name`, `description`, `model`, `tools`). COMPLIANT.

**Task tool absent from workers:** All 6 agents lack Task in their tools list. COMPLIANT.

**Constitutional triplet in both locations:**
- All 6 governance.yaml: `constitution.principles_applied` has >= 3 entries with P-003, P-020, P-022. COMPLIANT.
- All 6 governance.yaml: `capabilities.forbidden_actions` has >= 6 entries (>= minimum 3). COMPLIANT.

**Required schema fields:**

| Agent | version | tool_tier | role | expertise >=2 | cognitive_mode enum | fallback_behavior | principles >=3 | output.required |
|-------|---------|-----------|------|---------------|---------------------|-------------------|----------------|-----------------|
| tutorial | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | systematic PASS | warn_and_retry PASS | 3 PASS | true PASS |
| howto | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | systematic PASS | warn_and_retry PASS | 3 PASS | true PASS |
| reference | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | systematic PASS | warn_and_retry PASS | 3 PASS | true PASS |
| explanation | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | divergent PASS | warn_and_retry PASS | 3 PASS | true PASS |
| classifier | 0.1.0 PASS | T1 PASS | PASS | 4 PASS | convergent PASS | escalate_to_user PASS | 3 PASS | **true PASS (FIXED)** |
| auditor | 0.1.0 PASS | T1 PASS | PASS | 4 PASS | systematic PASS | escalate_to_user PASS | 3 PASS | true PASS |

All schema required fields: COMPLIANT.

#### H-23: Navigation Table for .md >30 Lines

All 6 .md files exceed 30 lines. None contain a markdown navigation table. The XML-tagged body format is structurally incompatible with a traditional `## Section` navigation table. This is the same persistent gap from Round 1.

**Status:** PERSISTS (CC-001 from Round 1 — requires framework-level resolution). Classified as Major.

#### Tool Tier vs. Tool Access Consistency

T2 agents (tutorial, howto, reference, explanation): tools = Read, Write, Edit, Glob, Grep, Bash (explanation now has Read, Write, Edit, Glob, Grep — no Bash, consistent with T2-minus-Bash used correctly). All compliant.

T1 agents (classifier, auditor): tools = Read, Glob, Grep. Compliant.

One new observation: explanation uses T2 tier but lists only 5 tools (no Bash). The tool tier says T2 (Read-Write). T2 is defined as T1 + Write, Edit, Bash. However, explanation omits Bash. This is a precision issue: the tier label does not strictly match the tool list. This is acceptable behavior (T2 is the minimum tier that satisfies requirements; dropping Bash from T2 is a reduction, not an expansion). No finding required — the framework allows subset tool lists within a tier.

#### Cognitive Mode vs. Task Type (Post-Remediation)

| Agent | cognitive_mode | Assessment |
|-------|----------------|------------|
| tutorial | systematic | CORRECT — procedural completeness |
| howto | systematic | CORRECT (FIXED — was convergent) |
| reference | systematic | CORRECT |
| explanation | divergent | CORRECT |
| classifier | convergent | CORRECT |
| auditor | systematic | CORRECT |

All cognitive modes correct. COMPLIANT.

#### AD-M-009: Model Selection Justified

| Agent | Model | Justification | Status |
|-------|-------|---------------|--------|
| tutorial | sonnet | Implicit (T2 writer, standard) | PASS |
| howto | sonnet | Implicit | PASS |
| reference | sonnet | Implicit | PASS |
| explanation | opus | Explicit: "synthesizing design rationale across multiple architectural documents, making non-obvious cross-topic connections, producing nuanced discursive prose that balances multiple perspectives" in identity section | PASS (FIXED) |
| classifier | haiku | Implicit (T1, procedural, fast) | PASS |
| auditor | sonnet | Implicit (systematic, checklist-based) | PASS |

All model selections: COMPLIANT.

#### New Observation: howto P-022 Forbidden Action Still Generic

howto.governance.yaml `forbidden_actions`: `"Misrepresent capabilities or confidence (P-022)"` — generic formulation unchanged from Round 1. Tutorial has `"Misrepresent tutorial completeness or reliability (P-022)"`, auditor has `"Inflate or deflate finding severity (P-022)"`. Howto's formulation is correct in substance but less precise than siblings.

Status: PERSISTS (CC-007 from Round 1). Minor.

### S-007 Findings Table

| ID | Principle | Tier | Severity | Finding | Status vs R1 |
|----|-----------|------|----------|---------|--------------|
| CC-001-20260227R2 | H-23: Navigation table | HARD | Major | All 6 .md files >30 lines lack navigation tables; XML-tagged format conflicts with H-23 | PERSISTS from R1 |
| CC-002-20260227R2 | AD-M-007: session_context | MEDIUM | Major | No agent declares session_context; classifier-to-writer pipeline has no formal handoff contract | PERSISTS from R1 (DA-006) |
| CC-003-20260227R2 | AD-M-003: forbidden_actions domain specificity | SOFT | Minor | howto forbidden_actions P-022 entry is generic vs. domain-specific in sibling agents | PERSISTS from R1 (CC-007) |

---

## S-013 Inversion Technique

**Finding Prefix:** IN
**Execution ID:** 20260227R2

### Step 1: Restated Primary Goals (Post-Remediation)

The remediated agent set claims to:
1. Classify documentation requests accurately with plausibility-checked hints (IN-001 fixed)
2. Prevent quadrant mixing from reaching output via Mixing Resolution Gate (IN-002 fixed)
3. Load criteria dynamically from standards file (IN-004/SR-005 fixed)
4. Route correctly to tutorial vs. howto via strengthened negative signals (IN-005 fixed)
5. Audit multi-quadrant documents with an escalation path (IN-003 fixed)

### Step 2: New Anti-Goals (Post-Remediation)

To guarantee failure of the remediated system:
- Anti-1: Make the Mixing Resolution Gate block legitimate mixed content that authors intentionally include
- Anti-2: Cause the auditor's internal classification to silently diverge from the classifier over time
- Anti-3: Exploit the howto Step 4 criterion load instruction — it says to verify against H-01 through H-07 from the file, but the methodology text still enumerates them inline as a redundant list
- Anti-4: The classifier's two-axis test now caps hint confidence at 0.85 when hint conflicts — but the output format template (Step 6) still accepts confidence values up to 1.00 without a declared maximum; a LLM could still output 1.00 for a non-hint path and the output template provides no ceiling guardrail
- Anti-5: The Bash verification Step 5b annotation only helps after verification failure; there is no guidance on what commands to run or how to interpret borderline output matches

### Step 3: Assumption Map

| # | Assumption | Type | Confidence | Category |
|---|-----------|------|------------|----------|
| A1 | Mixing Resolution Gate can be bypassed if user says "keep with ACKNOWLEDGED" for all flags | Process | Medium | Quality |
| A2 | Auditor's internal classification will remain aligned with classifier methodology over time | Technical | Medium | Maintenance |
| A3 | howto Step 4 inline criteria list will be kept in sync with the loaded file criteria | Resource | Low | Maintenance |
| A4 | Bash verification failure annotation is sufficient safety net for unverifiable commands | Process | Medium | Evidence |
| A5 | Classifier confidence computation for non-hint paths is fully deterministic (no LLM self-assessment leak) | Technical | High | Integrity |

### Step 4: Stress-Test Results

| ID | Assumption | Inversion | Severity | Evidence |
|----|-----------|-----------|----------|---------|
| IN2-001-20260227R2 | A3: howto inline criteria sync | howto.md Step 4 enumerates H-01 through H-07 inline AND instructs loading from diataxis-standards.md; when standards file adds H-08, the howto methodology silently applies 7 criteria while loading 8; the inline list creates a false signal of completeness | Minor | howto.md Step 4: "Verify against H-01 through H-07 from diataxis-standards.md: - H-01: Goal stated in title - H-02: Action-only content..." — inline enumeration present alongside the load instruction; tutorial and reference have the same pattern |
| IN2-002-20260227R2 | A2: Auditor drift from classifier | auditor.md Step 2 internal fallback references "Section 4 of diataxis-standards.md" for classification; classifier.md references the same section; if Section 4 is revised and the classifier methodology is updated but auditor is not re-reviewed, the auditor will drift; no explicit versioning or coupling noted | Minor | auditor.md Step 2: "apply the two-axis classification test from Section 4 of diataxis-standards.md" — references same source but separate code path from classifier; Round 1 DA-003 noted this; the disclaimer "standalone fallback only" was added but drift risk remains |
| IN2-003-20260227R2 | A1: Mixing Resolution Gate ACKNOWLEDGED bypass | A user can mark all QUADRANT-MIX flags as `[ACKNOWLEDGED]` and proceed to Step 6, producing a file full of acknowledged mixing violations; the gate halts correctly but the `keep with ACKNOWLEDGED` path allows any amount of mixing to persist; no limit on ACKNOWLEDGED count per document | Minor | tutorial.md Step 5: "keep with [ACKNOWLEDGED] tag" is one of three resolution options; no constraint on how many ACKNOWLEDGEDs are acceptable before the document should be reclassified |
| IN2-004-20260227R2 | A5: Non-hint path confidence determinism | classifier.md Step 3 table is deterministic; however, "Both axes unambiguous" yields 1.00; an LLM applying this table could misclassify an axis as "unambiguous" when it is borderline, producing overconfident classification; no explicit instruction to prefer 0.85 when uncertain about ambiguity | Minor | classifier.md Step 3: "Both axes unambiguous → 1.00" — the word "unambiguous" is evaluated by the LLM; there is no secondary check or reviewer; under-specification of axis certainty threshold leaves room for LLM self-assessment creep |

### Step 5: Mitigations

- **IN2-001 (Minor):** Remove inline criteria enumeration from all writer Step 4 sections. Replace with: "Load criteria from diataxis-standards.md. Apply all criteria found there (not a memorized list)." This eliminates the false-completeness signal.
- **IN2-002 (Minor):** Add to auditor Step 2: "If the auditor's classification result conflicts with a prior diataxis-classifier output for the same document, flag the discrepancy in the report rather than silently overriding."
- **IN2-003 (Minor):** Add to Mixing Resolution Gate: "If more than 2 QUADRANT-MIX flags are ACKNOWLEDGED, recommend reclassifying the document to a different quadrant or extracting a second document."
- **IN2-004 (Minor):** Add to classifier Step 2: "When determining 'mixed' vs. 'unambiguous', err toward 'mixed' for axis placements that require judgment. Only mark an axis as unambiguous when placement is obvious from the explicit content of the request."

---

## S-002 Devil's Advocate

**Finding Prefix:** DA
**Execution ID:** 20260227R2

**H-16 Note:** S-003 Steelman was not included in the requested strategy sequence. Per H-16, S-002 requires prior S-003. Proceeding as directed; findings are presented against the deliverable's claims as strengthened by their best interpretation. This is Round 2 of a directed review; the same constraint applied in Round 1.

### Step 1: Role Assumption

The remediated 6 agent definitions claim to constitute a correct, complete, and production-ready implementation of the Diataxis methodology for the Jerry framework. The core claims being challenged: (a) all critical findings from Round 1 are fully resolved, (b) the remaining persistent minor issues do not materially impair function, (c) the agent set is sufficient without session_context for operational use.

### Step 2: Assumption Challenges

**Explicit claims being challenged:**
- "Writers load criteria from the standards file" — true at the method level, but inline criteria lists remain and create maintenance risk
- "Mixing Resolution Gate prevents quadrant mixing from reaching output" — true, but the ACKNOWLEDGED bypass is unconstrained
- "Explanation model selection is justified" — the justification exists but is self-asserted without external evidence

**Implicit assumptions being challenged:**
- Session_context absence is acceptable because callers will construct inputs manually
- The auditor's PASS threshold (0 Critical, <=2 Minor) is sufficient for a quality enforcement tool
- An agent can serve as its own quality gate for mixing resolution

### Step 3: Counter-Arguments

| ID | Finding | Severity | Evidence |
|----|---------|----------|---------|
| DA2-001-20260227R2 | The session_context gap (persisting from Round 1 DA-006) now impairs all 3 workflow patterns: (1) classifier output → writer input has no declared field mapping, (2) writer output → auditor input has no declared handoff contract, (3) auditor findings → orchestrator correction loop has no declared schema. The classifier produces `{quadrant, confidence, rationale, axis_placement}` but writers expect `{Topic, Goal, Subject, Topic}` — zero field overlap without manual translation. | Major | classifier.md Step 6 output: `{Quadrant, Confidence, Rationale, Axis Placement, Decomposition}`; tutorial.md input: `{Topic, Prerequisites, Target outcome, Output path}`; howto.md input: `{Goal, Context, Output path}`; reference.md input: `{Subject, Source, Output path}`; explanation.md input: `{Topic, Context, Output path}`. No session_context block in any governance.yaml. |
| DA2-002-20260227R2 | Explanation model justification exists in the .md identity section but NOT in the governance.yaml. AD-M-009 guidance ("model selection SHOULD be justified") would most naturally be encoded in the machine-readable governance.yaml as a field, not only in prose. No standard governance.yaml field for model_justification exists, but an `identity.model_justification` extension field would align with the schema's `additionalProperties: true` policy. | Minor | explanation.md identity: has justification paragraph. explanation.governance.yaml: no model justification field. governance schema line: `additionalProperties: true` allows extension. |
| DA2-003-20260227R2 | The auditor PASS verdict threshold (0 Critical, <=2 Minor) allows a document with 2 minor quadrant mixing violations to PASS. A tutorial with `[QUADRANT-MIX: explanation in tutorial]` and `[QUADRANT-MIX: how-to content in tutorial]` — one of each — passes audit. These are exactly the violations the Diataxis methodology most emphasizes. The threshold has no documented rationale. | Minor | auditor.md verdict thresholds: "PASS: Zero Critical findings, at most 2 Minor findings" — no rationale. The Mixing Resolution Gate in writers blocks them during creation, but post-audit PASS for 2 mixing violations undermines the enforcement chain. |
| DA2-004-20260227R2 | diataxis-howto.md `<guardrails>` ordering differs from all siblings. Tutorial, reference, explanation, classifier, auditor all lead with `## Constitutional Compliance`. Howto leads with `## Constitutional Compliance` but then goes `## Input Validation`, `## Output Filtering`, `## Domain-Specific Constraints`, `## Fallback Behavior`. The ordering matches siblings. On closer inspection this is COMPLIANT — but the Step 4 howto methodology still contains an inline H-01 through H-07 list even though it says to load from file. | Minor | howto.md Step 4: "Verify against H-01 through H-07 from diataxis-standards.md: - H-01: Goal stated in title - H-02: Action-only content (no explanatory paragraphs)..." — the inline list is a maintenance liability even though the load instruction precedes it. |
| DA2-005-20260227R2 | Explanation agent omits Bash but keeps T2 tier designation. The explanation.governance.yaml `tool_tier: T2` implies Bash access per agent-development-standards.md T2 definition ("T1 + Write, Edit, Bash"). The actual tools list omits Bash. This creates a documentation inconsistency: the tier claims Bash capability that the tool list retracts. A CI/CD schema validator checking tier-tool consistency would flag this. | Minor | explanation.governance.yaml: `tool_tier: T2`; explanation.md frontmatter: `tools: Read, Write, Edit, Glob, Grep` — Bash absent. T2 definition in agent-development-standards: "T1 + Write, Edit, Bash". |

### Step 4: Response Requirements

**P1 (Major — SHOULD resolve before acceptance):**

- **DA2-001:** Define session_context for classifier (on_send) and all writers (on_receive), mapping classifier output fields to writer input fields. This is the highest unresolved gap; it impairs operational use of the pipeline.

**P2 (Minor — SHOULD address):**

- **DA2-002:** Add `identity: { model_justification: "..." }` extension field to explanation.governance.yaml for machine-readable traceability.
- **DA2-003:** Add rationale comment to auditor verdict thresholds: "2-Minor tolerance is intentional — minor style issues should not block publication; Critical and Major issues do block publication."
- **DA2-004:** Remove inline criteria enumeration from howto Step 4 (and tutorial, reference, explanation for consistency). Load-then-apply, not load-and-redundantly-list.
- **DA2-005:** Either (a) change explanation.governance.yaml `tool_tier: T1` since it does not use Write/Edit/Bash (incorrect — it uses Write and Edit for output), or (b) add a comment: "T2 minus Bash — Bash not needed for explanation writing." Option (b) is cleaner.

---

## S-010 Self-Refine

**Finding Prefix:** SR
**Execution ID:** 20260227R2

Systematic dimension-by-dimension review of all 6 agents as a coherent set, post-remediation.

### Completeness Check

**All 6 agents have `output.required: true`** — SR-001 from Round 1 confirmed fixed.

**session_context absent from all governance.yaml files** — DA-006/CC-006 from Round 1, now also DA2-001. Persists as a functional gap. The primary Diataxis workflow (classify → write → audit) has no declared handoff contract anywhere in the agent definitions.

**SR2-001:** diataxis-auditor.md Fallback Behavior section covers "invalid document path" and "missing quadrant" but still does not cover "missing output path." The `<output>` section specifies the default location (`projects/${JERRY_PROJECT}/audits/{document-slug}-audit.md`) but this fallback is not surfaced in `<guardrails>` where a reader expects all fallbacks. Persists from Round 1 SR-002.

- Evidence: auditor.md `<guardrails>` Fallback Behavior: 2 cases listed; output path default in `<output>` section only.
- Severity: **Minor**

### Internal Consistency Check

**SR2-002:** All four writer agents (tutorial, howto, reference, explanation) now correctly load criteria from diataxis-standards.md in Step 4. However, tutorial, howto, and reference retain an inline enumeration of their criteria codes immediately after the load instruction. This creates a dual-source for criteria codes: (a) the file load instruction, and (b) the inline list. If diataxis-standards.md adds a new criterion (e.g., T-09), the load instruction picks it up but the inline list still says "T-01 through T-08" — the agent will apply the listed range, not the full file content.

- Evidence: tutorial.md Step 4: "Load quality criteria from `skills/diataxis/rules/diataxis-standards.md` -- do not use memorized criteria. Verify against T-01 through T-08: - T-01: Completable end-to-end..." — load instruction followed immediately by inline enumeration. Same pattern in howto.md (H-01 through H-07), reference.md (R-01 through R-07).
- Note: explanation.md Step 4 does NOT have inline enumeration — it only has the load instruction and a list of E-01 through E-07 descriptions. Same issue applies.
- Severity: **Minor**

**SR2-003:** howto.md `<guardrails>` Domain-Specific Constraints includes `ALWAYS load quality criteria from skills/diataxis/rules/diataxis-standards.md` — this is correct and complete. However, tutorial.md, reference.md, and explanation.md `<guardrails>` Domain-Specific Constraints do NOT include this ALWAYS directive. Only howto carries it in guardrails. Tutorial, reference, explanation have it in methodology Step 4 only. The guardrails section is the behavioral enforcement layer visible during agent execution; missing it there means the constraint is less salient.

- Evidence: howto.md guardrails Domain-Specific Constraints: includes "ALWAYS load quality criteria from...". tutorial.md, reference.md, explanation.md Domain-Specific Constraints: no corresponding ALWAYS directive.
- Severity: **Minor**

### Methodological Rigor Check

**SR2-004:** diataxis-classifier Step 5 (Honor Hints) is now correctly specified — runs two-axis test first, caps at 0.85 on conflict. However, Step 3 (Compute Confidence) table still shows `Both axes unambiguous → 1.00`. The word "unambiguous" is LLM-evaluated. The table has no guidance on when an axis placement qualifies as unambiguous vs. borderline-but-leaning. An LLM applying this table could rationalize 1.00 confidence for a borderline case by deciding the axes are "unambiguous." The table provides no guardrail against overconfident axis assessment.

- Evidence: classifier.md Step 3: "Both axes unambiguous → 1.00" — no definition of "unambiguous threshold"; Step 2 says "determine placement: practical/theoretical/mixed" but does not specify when something is "mixed" vs. "clearly one or the other"
- Severity: **Minor**

**SR2-005:** All writer agents define Step 5b (verification failure handling) for Bash — "annotate the step with `[VERIFICATION-FAILED: {error}]` and warn the user before proceeding." This handles failure but does not handle partial success or ambiguous output (e.g., command succeeds but output differs from documented). No guidance for borderline Bash output.

- Evidence: tutorial.md Step 5b: "If Bash verification of any step fails, annotate the step with [VERIFICATION-FAILED: {error}] and warn the user before proceeding." — binary pass/fail only; no partial success handling.
- Severity: **Minor**

### Evidence Quality Check

**SR2-006:** explanation.governance.yaml does not encode the model justification that is present in explanation.md identity prose. The governance.yaml is machine-readable and schema-validated; the justification exists only in the LLM-consumed .md body. This means tooling that reads governance.yaml for model audit purposes will find no justification. The schema's `additionalProperties: true` on `identity` allows adding `model_justification`.

- Evidence: explanation.md identity: has justification paragraph; explanation.governance.yaml identity block: has `role`, `expertise`, `cognitive_mode` — no `model_justification` field
- Severity: **Minor**

### Actionability Check

**SR2-007:** The session_context absence (persisting DA-006 and now DA2-001) is the highest actionability gap. Without it, callers must manually construct the translation from classifier output format to writer input format for each of the 4 writer agents. The 4 writers have 4 different input field names. No document defines the mapping. This is an operational deployment risk.

- Evidence: classifier.md output: `Quadrant, Confidence, Rationale, Axis Placement`; tutorial.md input: `Topic, Prerequisites, Target outcome, Output path`; howto.md input: `Goal, Context, Output path`; reference.md input: `Subject, Source, Output path`; explanation.md input: `Topic, Context, Output path` — zero overlap in field names
- Severity: **Major** (functional gap in primary workflow)

### Traceability Check

**SR2-008:** None of the 6 governance.yaml files use the `prior_art` field. Persists from Round 1 SR-009.

- Evidence: All governance.yaml: no `prior_art` field; FEAT-013-001, FEAT-013-002 unreferenced
- Severity: **Minor**

**SR2-009:** None of the 6 governance.yaml files declare an `enforcement` section. Persists from Round 1 DA-008.

- Evidence: All governance.yaml: no `enforcement` block; agent-development-standards.md supports `enforcement: {tier, escalation_path}`
- Severity: **Minor**

**SR2-010:** `reasoning_effort` is not declared in any .md frontmatter. Persists from Round 1 SR-004.

- Evidence: All .md frontmatter: `model:` present without `reasoning_effort`; ET-M-001 SHOULD for C2+ agents
- Severity: **Minor**

---

## Findings Summary

| ID | Severity | Finding | Agent(s) | Strategy | vs R1 |
|----|----------|---------|---------|----------|-------|
| CC-001-20260227R2 | Major | H-23: all .md files >30 lines lack navigation tables | All 6 agents | S-007 | PERSISTS |
| CC-002-20260227R2 / DA2-001 / SR2-007 | **Major** | No session_context — classifier-to-writer pipeline lacks formal handoff contract; field mapping undefined | All 6 agents | S-007 + S-002 + S-010 | PERSISTS |
| IN2-001-20260227R2 | Minor | Writer Step 4 inline criteria enumeration conflicts with load instruction — maintenance liability | tutorial, howto, reference, explanation | S-013 | NEW |
| IN2-002-20260227R2 | Minor | Auditor internal classification divergence risk — no discrepancy flag when result conflicts with prior classifier output | diataxis-auditor | S-013 | NEW |
| IN2-003-20260227R2 | Minor | Mixing Resolution Gate ACKNOWLEDGED path unconstrained — no limit on ACKNOWLEDGED flags per document | All 4 writers | S-013 | NEW |
| IN2-004-20260227R2 | Minor | Classifier Step 3 "unambiguous" threshold is LLM-evaluated — no guidance on borderline axis certainty | diataxis-classifier | S-013 | NEW (refines) |
| DA2-002-20260227R2 | Minor | Explanation model justification in .md prose only, not in governance.yaml machine-readable field | diataxis-explanation | S-002 | NEW |
| DA2-003-20260227R2 | Minor | Auditor PASS threshold (0 Critical, <=2 Minor) has no documented rationale | diataxis-auditor | S-002 | PERSISTS (R1 DA-007) |
| DA2-005-20260227R2 | Minor | explanation.governance.yaml tool_tier: T2 inconsistent with actual tools (no Bash) | diataxis-explanation | S-002 | NEW |
| SR2-001-20260227R2 | Minor | Auditor fallback for missing output path not in `<guardrails>` Fallback Behavior | diataxis-auditor | S-010 | PERSISTS (R1 SR-002) |
| SR2-002-20260227R2 | Minor | Writer Step 4 inline criteria range ("T-01 through T-08") will not auto-update when standards file adds criteria | tutorial, howto, reference, explanation | S-010 | NEW (refines IN2-001) |
| SR2-003-20260227R2 | Minor | "ALWAYS load quality criteria" directive in guardrails only in howto; missing from tutorial/reference/explanation guardrails | tutorial, reference, explanation | S-010 | NEW |
| SR2-004-20260227R2 | Minor | Classifier "unambiguous" axis threshold under-specified — leaves room for LLM rationalization | diataxis-classifier | S-010 | NEW (refines IN2-004) |
| SR2-005-20260227R2 | Minor | Bash verification Step 5b handles binary failure but not ambiguous/partial output | tutorial, howto, reference | S-010 | NEW |
| SR2-006-20260227R2 | Minor | explanation.governance.yaml lacks machine-readable model_justification field | diataxis-explanation | S-010 | NEW |
| SR2-008-20260227R2 | Minor | prior_art unused — no traceability to PROJ-013 worktracker entities | All 6 agents | S-010 | PERSISTS (R1 SR-009) |
| SR2-009-20260227R2 | Minor | No enforcement section in any governance.yaml | All 6 agents | S-010 | PERSISTS (R1 DA-008) |
| SR2-010-20260227R2 | Minor | reasoning_effort not declared in any .md frontmatter | All 6 agents | S-010 | PERSISTS (R1 SR-004) |
| CC-003-20260227R2 | Minor | howto forbidden_actions P-022 entry is generic | diataxis-howto | S-007 | PERSISTS (R1 CC-007) |

---

## Detailed Findings

### CC-001-20260227R2: Navigation Table Absent from All Agent .md Files

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All 6 .md files — file-level structural issue |
| **Strategy Step** | S-007 H-23 check |

**Evidence:**
All 6 agent .md files exceed 30 lines and use XML-tagged body sections (`<agent>`, `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>`). H-23 requires navigation tables for all Claude-consumed markdown >30 lines. No navigation table is present in any of the 6 files.

**Analysis:**
H-23 is a HARD rule (cannot be overridden). The XML-tagged section format is mandated by H-34 (agent-development-standards.md §Markdown Body Sections). These two HARD rules are structurally incompatible: H-23 requires `## Section` headings for navigation tables (NAV-001); H-34 requires XML tags for agent body sections. This is a framework-level contradiction requiring formal resolution. Individual agent files cannot resolve it unilaterally.

The contradiction was noted in Round 1. It still persists because the resolution path (exemption in agent-development-standards.md or framework guidance) has not been executed.

**Recommendation:**
Add a one-line navigation table in the .md files BEFORE the `<agent>` XML tag:
```markdown
<!-- Navigation: Identity | Purpose | Input | Capabilities | Methodology | Output | Guardrails -->
```
This satisfies H-23's intent (navigability) without requiring `## Section` headings in the XML body. Alternatively, add formal exemption language to agent-development-standards.md: "Agent .md files are exempt from H-23 navigation table requirement; XML-tagged body sections provide equivalent navigation structure."

---

### CC-002-20260227R2: session_context Absent — Pipeline Handoff Undefined

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All governance.yaml files |
| **Strategy Step** | S-007 AD-M-007 check; S-002 Step 2; S-010 Actionability check |

**Evidence:**
- classifier.md Step 6 output: `{Quadrant, Confidence, Rationale, Axis Placement, Decomposition}`
- tutorial.md input: `{Topic, Prerequisites, Target outcome, Output path}`
- howto.md input: `{Goal, Context, Output path}`
- reference.md input: `{Subject, Source, Output path}`
- explanation.md input: `{Topic, Context, Output path}`
- All 6 governance.yaml: no `session_context` block with `on_receive`/`on_send` fields

**Analysis:**
The primary Diataxis workflow is classify → write → audit. The classifier produces a structured result with fields that have zero nominal overlap with the writer input fields. An orchestrator invoking this pipeline must manually construct the field translation. AD-M-007 (MEDIUM) states agents SHOULD declare `session_context` with `on_receive` and `on_send` processing steps for structured handoff participation. This gap means the pipeline is an informal convention, not a contract. Per agent-development-standards.md Handoff Protocol, HD-M-001 states handoff data SHOULD validate against the canonical schema. Without session_context declarations, no such validation is possible.

**Recommendation:**
Add `session_context` to classifier.governance.yaml:
```yaml
session_context:
  on_send:
    quadrant: "The classified quadrant (tutorial|howto|reference|explanation|multi)"
    confidence: "Confidence score 0.0-1.0"
    rationale: "1-2 sentence explanation of axis placement"
    axis_placement: "{practical|theoretical|mixed} x {acquisition|application|mixed}"
    decomposition: "If multi: list of {quadrant, content_scope, sequence}"
```
Add `session_context` to each writer's governance.yaml `on_receive` block mapping classifier fields to writer input fields.

---

### DA2-001-20260227R2: Inline Criteria Enumeration Conflicts with Load Instruction

*(See IN2-001 / SR2-002 — detailed in those sections.)*

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | tutorial.md Step 4, howto.md Step 4, reference.md Step 4, explanation.md Step 4 |
| **Strategy Step** | S-013 Step 4 stress-test; S-010 Internal Consistency check |

**Evidence:**
tutorial.md Step 4: "Load quality criteria from `skills/diataxis/rules/diataxis-standards.md` -- do not use memorized criteria. Verify against T-01 through T-08: - T-01: Completable end-to-end without external help..."
The load instruction is followed immediately by inline criterion descriptions. The phrase "T-01 through T-08" is hardcoded; if the standards file adds T-09, the load instruction loads it but the criteria range in the text does not mention it.

**Recommendation:**
Remove inline enumeration from all writer Step 4 sections. Replace with: "Load criteria from `skills/diataxis/rules/diataxis-standards.md`. Apply ALL criteria found in the file for this quadrant."

---

## Execution Statistics

- **Total Findings:** 19
- **Critical:** 0
- **Major:** 2 (CC-001, CC-002/DA2-001/SR2-007)
- **Minor:** 17
- **Protocol Steps Completed:** 4 of 4 (S-007, S-013, S-002, S-010)
- **Round 1 Findings Fixed:** 12 of 23 (52%)
- **Round 1 Critical Fixed:** 1 of 1 (100%)
- **Round 1 Major Fixed:** 10 of 13 (77%)
- **Round 1 Minor Fixed:** 1 of 9 (11%)
- **New Findings (Round 2 only):** 8 (all Minor)

---

## S-014 Quality Scoring (6-Dimension Weighted Composite)

### Dimension-by-Dimension Assessment

| Dimension | Weight | Round 1 Score | Round 2 Score | Rationale |
|-----------|--------|---------------|---------------|-----------|
| Completeness | 0.20 | ~0.55 | 0.88 | session_context still absent (major gap); prior_art/enforcement minor gaps; output.required fixed; criteria loading fixed |
| Internal Consistency | 0.20 | ~0.55 | 0.90 | Howto cognitive_mode fixed; criteria load added; inline enumeration vs. load creates minor drift risk; explanation T2/tool inconsistency minor |
| Methodological Rigor | 0.20 | ~0.50 | 0.92 | Mixing Resolution Gate added; criteria load added; multi-quadrant audit path added; remaining: unambiguous threshold, ACKNOWLEDGED bypass, partial Bash output |
| Evidence Quality | 0.15 | ~0.60 | 0.90 | Explanation model justification added to .md; not in governance.yaml; hint confidence fix verified |
| Actionability | 0.15 | ~0.50 | 0.82 | session_context gap impairs pipeline deployment; classifier-to-writer mapping undefined; individual agents actionable as standalone |
| Traceability | 0.10 | ~0.65 | 0.85 | Constitutional triplet well-traced; schema compliant; prior_art/enforcement/reasoning_effort absent |

### Weighted Composite Score

```
Score = (0.88 × 0.20) + (0.90 × 0.20) + (0.92 × 0.20) + (0.90 × 0.15) + (0.82 × 0.15) + (0.85 × 0.10)
      = 0.176 + 0.180 + 0.184 + 0.135 + 0.123 + 0.085
      = 0.883
```

**Round 2 Composite Score: 0.883**

**Status: REVISE** (0.85-0.91 band — near threshold, targeted revision likely sufficient)

**Delta from Round 1:** Round 1 scored approximately 0.29-0.50 range (below 0.85 REJECTED). Round 2 is in the REVISE band. Significant improvement achieved through Round 1 fixes. Not yet at 0.95 threshold.

### Gap Analysis: Distance to 0.95

**Required improvement:** 0.95 - 0.883 = 0.067

**Actionability dimension** (0.82, weight 0.15) is the primary drag. Resolving the session_context gap (CC-002) would move Actionability from 0.82 to approximately 0.95, contributing +0.019 to composite.

**Completeness dimension** (0.88, weight 0.20) is the second drag. Resolving session_context moves it to ~0.93, contributing +0.010. Adding enforcement/prior_art/reasoning_effort adds ~0.02 more.

**Estimated score after fixing CC-002 + minor persisting items:** approximately 0.93-0.95.

### Path to 0.95

| Fix | Priority | Estimated Score Impact |
|-----|----------|----------------------|
| CC-002: Add session_context to classifier and writers | P1 | +0.030 (Completeness +0.05, Actionability +0.13) |
| SR2-002/IN2-001: Remove inline criteria enumeration from Step 4 | P2 | +0.005 (Internal Consistency +0.02) |
| DA2-005: Document T2-minus-Bash in explanation governance | P2 | +0.003 (Internal Consistency +0.01) |
| SR2-003: Add criteria load directive to tutorial/reference/explanation guardrails | P2 | +0.004 (Methodological Rigor +0.02) |
| SR2-010/DA-008: Add reasoning_effort and enforcement to governance files | P3 | +0.010 (Completeness +0.02, Traceability +0.05) |
| IN2-003/IN2-004: Add ACKNOWLEDGED limit and axis certainty guidance | P3 | +0.005 (Methodological Rigor +0.02) |
| SR2-008/SR2-009: Add prior_art and enforcement | P3 | +0.004 (Traceability +0.04) |
| CC-001: Resolve H-23/H-34 navigation conflict | P4 (framework-level) | +0.003 (Completeness +0.01) |

**Estimated composite after P1+P2:** ~0.921 (REVISE band — close)
**Estimated composite after P1+P2+P3:** ~0.940 (approaching threshold)
**Estimated composite after all:** ~0.950 (meets threshold)

---

## Overall Assessment

**Significant progress from Round 1.** The Critical finding (IN-001 hint bypass) is fully resolved. 10 of 13 Major findings from Round 1 are fixed. The agent set is now functionally coherent at the individual-agent level — each agent has correct cognitive mode, model justification, criteria loading, security guardrails, and mixing resolution.

**Remaining blockers:**
1. **CC-002 (Major):** session_context absence is the functional deployment blocker. The classify → write → audit workflow cannot be orchestrated without a field mapping contract. This is the single highest-priority fix for Round 3.
2. **CC-001 (Major):** H-23/H-34 navigation conflict requires framework-level resolution, not individual agent fix.

**Round 3 recommendation:** Focus on:
1. session_context declarations (one targeted change per agent: 6 files)
2. Remove inline criteria enumeration from writer Step 4 (4 files)
3. Add load directive to guardrails sections (3 files)
4. reasoning_effort + enforcement + prior_art additions (6 governance.yaml files)
5. Resolve H-23/H-34 conflict via framework exemption (1 rule file or minimal .md header)

If those 5 fix categories are applied, the estimated composite score reaches 0.95+ and the agent set PASSES.

**Constitutional compliance:** HARD rules fully satisfied. No Critical findings. Foundation is sound for production deployment with the session_context gap documented as a known limitation.

---

*Report generated: 2026-02-27*
*Round 2 of adversarial review — Round 1 at `projects/PROJ-013-diataxis/reviews/adversary-round1-agents.md`*
*Strategies applied: S-007 (CC prefix), S-013 (IN prefix), S-002 (DA prefix), S-010 (SR prefix)*
*Template references: s-007-constitutional-ai.md, s-013-inversion.md, s-002-devils-advocate.md, s-010-self-refine.md*
*SSOT: `.context/rules/quality-enforcement.md`, `.context/rules/agent-development-standards.md`*
