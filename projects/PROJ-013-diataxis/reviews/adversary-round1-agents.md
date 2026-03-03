# Adversarial Review: Agent Definitions (Round 1)

## Execution Context

- **Strategies Applied:** S-007 Constitutional AI Critique, S-013 Inversion Technique, S-002 Devil's Advocate, S-010 Self-Refine
- **Deliverables:** 12 files (6 agent .md + 6 .governance.yaml pairs)
- **Criticality:** C3 (agent definitions for a new skill: affects >10 files, >1 day to reverse)
- **Quality Threshold:** >= 0.95 weighted composite
- **Executed:** 2026-02-27
- **Reviewer:** adv-executor
- **References:** `.context/rules/agent-development-standards.md`, `docs/schemas/agent-governance-v1.schema.json`

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

## Per-Agent Summary

| Agent | Tool Tier | Cognitive Mode | Schema | Constitutional Triplet | Overall |
|-------|-----------|----------------|--------|------------------------|---------|
| diataxis-tutorial | T2 | systematic | PASS | PASS | Minor gaps only |
| diataxis-howto | T2 | convergent | PASS (minor gap) | PASS | Moderate — mode mismatch, missing guardrail subsections |
| diataxis-reference | T2 | systematic | PASS | PASS | Minor gaps only |
| diataxis-explanation | T2 | divergent | PASS | PASS | Minor — model justification missing |
| diataxis-classifier | T1 | convergent | Partial (output.required absent) | PASS | Major — hint bypass vulnerability |
| diataxis-auditor | T1 | systematic | PASS | PASS | Major — multi-quadrant gap, classification duplication |

---

## S-007 Constitutional AI Critique

**Finding Prefix:** CC
**Execution ID:** 20260227

### Applicable Principles

| Principle | Tier | Applicable to Agent Definitions |
|-----------|------|---------------------------------|
| H-01/P-003: No recursive subagents | HARD | YES — workers must not have Task tool |
| H-02/P-020: User authority | HARD | YES — must not override user decisions |
| H-03/P-022: No deception | HARD | YES — accurate capability/confidence reporting |
| H-34: Dual-file architecture + schema validation | HARD | YES — primary compliance rule |
| H-35/H-34b: Worker agents must NOT have Task in tools | HARD | YES |
| H-23: Navigation table for .md >30 lines | HARD | YES — applies to all Claude-consumed markdown |
| AD-M-003: description WHAT+WHEN+triggers ≤1024 chars | MEDIUM | YES |
| AD-M-005: identity.expertise ≥2 specific entries | MEDIUM | YES |
| AD-M-007: session_context declared | MEDIUM | YES |
| AD-M-009: model selection justified | MEDIUM | YES |

### Principle-by-Principle Evaluation

#### H-34: YAML Frontmatter Fields (Official Claude Code Fields Only)

All 6 .md files declare only official Claude Code fields: `name`, `description`, `model`, `tools`. No non-official fields present in any frontmatter. **COMPLIANT.**

#### H-35: No Task Tool in Worker Agents

| Agent | Tools Declared | Task Present |
|-------|---------------|--------------|
| diataxis-tutorial | Read, Write, Edit, Glob, Grep, Bash | NO — PASS |
| diataxis-howto | Read, Write, Edit, Glob, Grep, Bash | NO — PASS |
| diataxis-reference | Read, Write, Edit, Glob, Grep, Bash | NO — PASS |
| diataxis-explanation | Read, Write, Edit, Glob, Grep, Bash | NO — PASS |
| diataxis-classifier | Read, Glob, Grep | NO — PASS |
| diataxis-auditor | Read, Glob, Grep | NO — PASS |

**COMPLIANT on all agents.**

#### H-34b: Constitutional Triplet (P-003/P-020/P-022)

All 6 agents declare all three principles in both `constitution.principles_applied` (>=3 entries) and `capabilities.forbidden_actions` (>=6 entries each). **COMPLIANT on all agents.**

#### H-34: Schema Validation (agent-governance-v1.schema.json required fields)

Required schema fields: `version`, `tool_tier`, `identity.role`, `identity.expertise` (min 2), `identity.cognitive_mode` (enum), `guardrails.fallback_behavior`, `constitution.principles_applied` (min 3).

| Agent | version | tool_tier | role | expertise ≥2 | cognitive_mode enum | fallback | principles ≥3 |
|-------|---------|-----------|------|--------------|---------------------|----------|---------------|
| tutorial | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | systematic PASS | warn_and_retry PASS | 3 PASS |
| howto | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | convergent PASS | warn_and_retry PASS | 3 PASS |
| reference | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | systematic PASS | warn_and_retry PASS | 3 PASS |
| explanation | 0.1.0 PASS | T2 PASS | PASS | 4 PASS | divergent PASS | warn_and_retry PASS | 3 PASS |
| classifier | 0.1.0 PASS | T1 PASS | PASS | 4 PASS | convergent PASS | escalate_to_user PASS | 3 PASS |
| auditor | 0.1.0 PASS | T1 PASS | PASS | 4 PASS | systematic PASS | escalate_to_user PASS | 3 PASS |

**COMPLIANT on all agents.** One schema gap found: diataxis-classifier.governance.yaml `output` block is missing `required:` field. The schema's conditional (`if required: true, then location required`) is silently bypassed. Classified as **CC-003** below.

#### H-23: Navigation Table Required for .md >30 Lines

All 6 agent .md files exceed 30 lines. None contain a markdown navigation table. The files use XML-tagged sections (`<identity>`, `<purpose>`, `<input>`, etc.) rather than `## Heading` sections, which is the prescribed format per agent-development-standards.md. H-23 literally applies to all Claude-consumed markdown >30 lines.

**Assessment:** This is a HARD rule violation on technical grounds. However, the agent-development-standards.md explicitly specifies XML-tagged section format for agent .md body, which is structurally incompatible with a traditional `## Section` navigation table. The contradiction exists between H-23 (universal markdown nav table) and H-34 (agent .md uses XML body). This warrants a formal exemption or resolution in agent-development-standards.md rather than a Critical finding on individual agents. Classified as **CC-001** at Major severity pending framework-level resolution.

#### Tool Tier vs. Tool Access Consistency

T2 = Read, Write, Edit, Bash, Glob, Grep. T1 = Read, Glob, Grep. All agents are consistent: writer agents are T2 with T2 tools; classifier and auditor are T1 with T1 tools. **COMPLIANT.**

#### Cognitive Mode vs. Task Type

| Agent | cognitive_mode | Assessment |
|-------|----------------|------------|
| tutorial | systematic | CORRECT — procedural completeness, checklist |
| howto | convergent | QUESTIONABLE — how-to must handle multiple paths per H-03; convergent narrows to single answer (see CC-004) |
| reference | systematic | CORRECT — procedural completeness over all elements |
| explanation | divergent | CORRECT — broad exploration, connection-making |
| classifier | convergent | CORRECT — narrow evaluation to single classification decision |
| auditor | systematic | CORRECT — evaluate each criterion methodically |

#### AD-M-009: Model Selection Justified

| Agent | Model | Justification Documented | Assessment |
|-------|-------|--------------------------|------------|
| tutorial | sonnet | Implicit (standard T2 writer) | PASS |
| howto | sonnet | Implicit | PASS |
| reference | sonnet | Implicit | PASS |
| explanation | opus | NO — no documented justification in .md body or governance.yaml | MAJOR gap (CC-005) |
| classifier | haiku | Implicit (T1, procedural, fast) | PASS |
| auditor | sonnet | Implicit (systematic, checklist-based) | PASS |

### S-007 Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260227 | H-23: Navigation table required | HARD | Major | All 6 agent .md files >30 lines lack navigation tables; XML-tagged format conflicts with H-23 expectation | Completeness |
| CC-002-20260227 | H-34: .md body guardrail completeness | MEDIUM | Major | diataxis-howto.md `<guardrails>` section missing `## Input Validation` and `## Output Filtering` subsections present in all 5 other agents | Internal Consistency |
| CC-003-20260227 | H-34: Schema conditional — output.required absent | MEDIUM | Major | diataxis-classifier.governance.yaml output block has no `required:` field; schema conditional for location enforcement is bypassed | Completeness |
| CC-004-20260227 | Cognitive mode taxonomy (AD-M) | MEDIUM | Major | diataxis-howto cognitive_mode: convergent — taxonomy says convergent "narrows from options to decision" which conflicts with H-03 requiring multi-path handling | Methodological Rigor |
| CC-005-20260227 | AD-M-009: Model selection justification | MEDIUM | Major | diataxis-explanation uses model: opus with no documented justification in .md body or governance.yaml | Evidence Quality |
| CC-006-20260227 | AD-M-007: session_context | MEDIUM | Minor | No agent declares session_context (on_receive/on_send); classifier-to-writer pipeline is the primary workflow and has no formal handoff contract | Actionability |
| CC-007-20260227 | AD-M-003: forbidden_actions domain-specificity | SOFT | Minor | diataxis-howto P-022 entry "Misrepresent capabilities or confidence" is generic; other agents have domain-specific formulations (e.g., auditor "Inflate or deflate finding severity") | Internal Consistency |

### S-007 Constitutional Compliance Score

- Critical violations: 0
- Major violations: 5 (CC-001 through CC-005, -0.05 each = -0.25)
- Minor violations: 2 (CC-006, CC-007, -0.02 each = -0.04)

**Score:** 1.00 - 0.25 - 0.04 = **0.71** — REJECTED (below 0.85 threshold)

---

## S-013 Inversion Technique

**Finding Prefix:** IN
**Execution ID:** 20260227

### Step 1: Primary Goals of Agent Set

1. Each agent produces correctly-quadrant-classified Diataxis documentation reliably
2. Routing signals direct invocations to the correct agent (no wrong-quadrant output)
3. Constitutional constraints prevent capability misuse
4. T1 agents stay read-only; T2 agents write files but no more
5. Self-review prevents quadrant mixing from reaching the output file

### Step 2: Anti-Goals

To guarantee failure:
- Anti-1: Make agent descriptions indistinguishable so routing chooses the wrong writer
- Anti-2: Allow quadrant mixing to persist silently to output (no blocking gate)
- Anti-3: Break hint handling so classifier produces arbitrary high-confidence misclassifications
- Anti-4: Let auditor operate on multi-quadrant documents with no defined behavior
- Anti-5: Writer agents apply stale criteria not loaded from standards file

### Step 3: Assumption Map

| # | Assumption | Type | Confidence | Category |
|---|-----------|------|------------|----------|
| A1 | hint_quadrant bypass is safe because callers provide valid hints | Process | Low | Security |
| A2 | Quadrant mixing flags + proceeding to write = acceptable workflow | Process | Low | Quality |
| A3 | diataxis-auditor can handle any document type including multi-quadrant | Technical | Low | Capability |
| A4 | Writer agents apply current criteria without loading the standards file | Resource | Low | Maintenance |
| A5 | Tutorial and how-to descriptions are distinct enough for reliable routing | Technical | Medium | Routing |
| A6 | Bash verification of steps is implicitly optional with no failure consequence | Process | High | Quality |

### Step 4: Stress-Test Results

| ID | Assumption | Inversion | Severity | Evidence | Affected Dimension |
|----|-----------|-----------|----------|----------|--------------------|
| IN-001-20260227 | A1: hint_quadrant callers provide valid hints | A malicious or mistaken caller provides `hint_quadrant: tutorial` for a reference document; classifier returns confidence 1.00 and routes to diataxis-tutorial which writes a tutorial wrapping reference content | Critical | classifier.md Step 5: "Override the two-axis test result with the hint and set confidence to 1.00 (user-directed)" — no plausibility check; P-022 violated (1.00 confidence is deceptive when hint contradicts content) | Evidence Quality |
| IN-002-20260227 | A2: Mixing flags + proceed to write is acceptable | Writer flags `[QUADRANT-MIX: explanation in tutorial]` then proceeds immediately to Step 6 Persist Output; flagged mixed-quadrant content is written to disk without user resolution | Major | tutorial.md Step 5 flags mixing; Step 6 follows immediately; no gate or user confirmation between steps; diataxis-standards.md Section 3 requires describing and asking user, but this is not in agent methodology | Actionability |
| IN-003-20260227 | A3: Auditor handles any document type | Input: multi-quadrant document (e.g., SKILL.md with tables, narrative, and how-to sections) submitted with no declared_quadrant; auditor's internal classification cannot return "multi"; auditor evaluates against one quadrant and produces misleading PASS | Major | auditor.md input: "use diataxis-classifier methodology to determine the quadrant first" — internal fallback cannot produce multi; Step 1 loads criteria for exactly one quadrant; no multi-quadrant audit path exists | Completeness |
| IN-004-20260227 | A4: Writer agents apply current criteria from methodology text | diataxis-standards.md updates T-08 criteria; all 4 writer agents continue applying old T-08 criteria from their methodology text; quality checks silently diverge from standard | Major | tutorial.md Step 4: criteria T-01 through T-08 listed inline in methodology; no "read standards file" step; auditor correctly loads from file in Step 1 but writers do not | Methodological Rigor |
| IN-005-20260227 | A5: Tutorial/howto descriptions are distinct for routing | New user asks for "step-by-step guide to authenticate with the CLI"; both tutorial and how-to descriptions mention "step-by-step"; routing is ambiguous; wrong agent selected | Major | tutorial description: "Creates step-by-step tutorials"; howto description: "step-by-step directions toward a concrete goal" — both use "step-by-step"; distinction requires deep reading of "learning" vs. "goal" | Internal Consistency |
| IN-006-20260227 | A6: Bash failure has no consequence | Tutorial agent runs `jerry session start` as part of step verification; command fails; agent proceeds with unverified step text; output tutorial documents a non-working command | Minor | tutorial.md capabilities: "Bash to verify that tutorial steps actually produce the documented results"; no failure handling defined; verification is implied optional | Evidence Quality |

### Step 5: Mitigations

**Critical:**
- **IN-001:** Modify classifier Step 5 to always run the two-axis test when hint is provided; compare hint to test result; cap confidence at 0.85 when hint conflicts; note the conflict in rationale. Acceptance: classifier cannot return confidence 1.00 for a hint that contradicts two-axis result.

**Major:**
- **IN-002:** Add explicit gate in writer agent Step 5: "If QUADRANT-MIX flags exist, do not proceed to Step 6. Describe flagged content to user and wait for resolution decision (remove, keep with [ACKNOWLEDGED], or extract)."
- **IN-003:** Add multi-quadrant audit path to auditor methodology (Step 1b): when quadrant is "multi" or confidence <0.70, escalate to user before auditing; document each constituent quadrant's criteria separately.
- **IN-004:** Add Step 0 to all writer agent methodologies: "Read `skills/diataxis/rules/diataxis-standards.md`. Use the criteria from the file, not from memory."
- **IN-005:** Strengthen routing descriptions: tutorial adds "NOT for users needing quick task completion"; howto adds "NOT for beginners building skills for the first time."

**Minor:**
- **IN-006:** Add Bash verification failure handling: annotate unverified step with `[VERIFICATION-FAILED]`; warn user before proceeding.

---

## S-002 Devil's Advocate

**Finding Prefix:** DA
**Execution ID:** 20260227

**H-16 Note:** S-003 Steelman was not included in the requested strategy sequence. Per H-16, S-002 requires prior S-003. Proceeding as instructed given this is a directed adversarial review; findings are presented to challenge the deliverable's claims as strengthened by their best interpretation.

### Step 1: Role Assumption

Challenge: the 6 diataxis agent definitions constitute a correct, complete, and sufficient agent-based implementation of the Diataxis methodology. The core claims being challenged: (a) agents are correctly specialized, (b) workflows between agents are coherent, (c) quality mechanisms are effective.

### Step 2: Assumption Challenges

**Explicit assumptions:**
- Classifier uses "deterministic confidence derivation" (not LLM self-assessment)
- Tutorial teaches "by doing not by explanation" — enforced through agent constraints
- Auditor produces audit reports accurately reflecting quadrant quality

**Implicit assumptions:**
- The 6 agents are sufficient to cover all Diataxis use cases
- Bash is needed for step verification in writer agents
- Opus is required for explanation writing quality
- The auditor can self-classify undeclared quadrants equivalently to the classifier

### Step 3: Counter-Arguments

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260227 | diataxis-explanation uses opus with no justification — costs 5x more per token without documented quality benefit | Major | explanation.md: `model: opus`; all other writers use sonnet; no justification in .md body, governance.yaml, or any comment; AD-M-009 says opus for "complex reasoning, research, architecture, synthesis" — explanation writing from existing docs does not meet this bar | Evidence Quality |
| DA-002-20260227 | Bash in all 4 writer agents adds shell execution risk; diataxis-explanation has Bash listed but no Bash usage pattern documented | Major | explanation.md capabilities: lists Bash in tools frontmatter but capabilities section has NO Bash usage pattern; capabilities says "Read design decisions... Search for related concepts... Write the explanation... Read existing docs" — zero Bash uses; Bash is dead capability with no justification | Methodological Rigor |
| DA-003-20260227 | Auditor's internal classification fallback re-implements classifier logic and will drift when standards change | Major | auditor.md Step 2: "apply the two-axis classification test from Section 4 of diataxis-standards.md" — same source as classifier but different execution path; classifier has 6 steps including hint handling and confidence derivation; auditor's internal fallback lacks these; two classification implementations will diverge | Internal Consistency |
| DA-004-20260227 | Tutorial and how-to agent descriptions are routinely ambiguous; "step-by-step" appears in both | Major | tutorial description: "Creates step-by-step tutorials"; howto description: "Creates action-only guides... step-by-step directions"; a routing system doing keyword matching on "step by step" will fire both; the distinction requires semantic understanding of "learning" vs. "goal" — which is not a keyword-level signal | Internal Consistency |
| DA-005-20260227 | diataxis-howto cognitive_mode: convergent conflicts with H-03 (multi-path handling requirement) | Major | howto.md identity: "Cognitive Mode: Convergent -- you focus on solving a specific problem"; howto H-03: "Addresses real-world variations -- At minimum one 'If you need X, do Y' variant"; convergent mode "narrows from options to decision" per taxonomy — will systematically suppress the multi-path variations that define how-to quality | Methodological Rigor |
| DA-006-20260227 | No agent has session_context declared — classifier-to-writer pipeline is an informal convention, not a contract | Major | All 6 governance.yaml files: no session_context block; the primary diataxis workflow is classifier → writer → auditor; without session_context, the structured classification result from the classifier has no declared mapping to writer input fields (Topic, Goal, Subject, Topic) | Actionability |
| DA-007-20260227 | Auditor verdict PASS threshold (0 Critical, ≤2 Minor) is too lenient for documentation quality enforcement | Minor | auditor.md: "PASS: Zero Critical findings, at most 2 Minor findings"; two minor quadrant-mixing violations in a tutorial (e.g., one "why" digression + one alternative offered) are each independently meaningful violations of tutorial design principles; allowing both to PASS undermines the auditor as a quality gate | Methodological Rigor |
| DA-008-20260227 | No agent declares enforcement metadata; quality gate tier cannot be machine-verified | Minor | All governance.yaml: no `enforcement` section; schema supports `enforcement.tier` (hard/medium/soft) and `escalation_path`; C3 criticality work should declare enforcement tier | Completeness |

### Step 4: Response Requirements

**P0 (Critical):** None at Critical severity from S-002 alone (IN-001 from S-013 is Critical).

**P1 (Major — SHOULD resolve before acceptance):**

- **DA-001:** Either document justification for opus in explanation.md and governance.yaml ("opus selected because explanation synthesis across cross-cutting architectural concerns has degraded quality with sonnet, evidence: [link]") or downgrade to sonnet.
- **DA-002:** Remove Bash from diataxis-explanation.md frontmatter tools list immediately. For tutorial, howto, reference: document Bash use case in capabilities AND add explicit guardrail "Bash ONLY for step verification commands."
- **DA-003:** Clarify auditor Step 2 as an intentional fallback with documented divergence risk; add note: "For pipeline use, invoke diataxis-classifier before auditor. Internal classification is standalone fallback only."
- **DA-004:** Revise tutorial and howto descriptions to add negative routing signals. Tutorial: add "NOT for users who need to quickly accomplish a task." Howto: add "NOT for users learning a skill for the first time."
- **DA-005:** Change diataxis-howto.governance.yaml cognitive_mode from `convergent` to `systematic`. Update identity section in howto.md.
- **DA-006:** Define session_context for classifier (on_send: quadrant, confidence, rationale, axis_placement) and writer agents (on_receive: consume classifier output).

### Step 5: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-006, DA-008: No handoff contracts or enforcement metadata |
| Internal Consistency | 0.20 | Negative | DA-004: Overlapping routing signals; DA-003: Two classification implementations |
| Methodological Rigor | 0.20 | Negative | DA-005: Cognitive mode conflicts with how-to multi-path requirement; DA-002: Dead Bash capability |
| Evidence Quality | 0.15 | Negative | DA-001: Opus selection lacks documented evidence |
| Actionability | 0.15 | Negative | DA-006: No formal handoff contract means cross-agent workflows are ad hoc |
| Traceability | 0.10 | Neutral | Constitutional triplet and schema validation are well-traced |

---

## S-010 Self-Refine

**Finding Prefix:** SR
**Execution ID:** 20260227

Systematic dimension-by-dimension review of all 6 agents as a coherent set.

### Completeness Check

**SR-001:** diataxis-classifier.governance.yaml `output.required` is absent. The schema conditional (`if required: true, then location required`) is silently bypassed. The classifier is labeled as always producing required output (`<output>` section says "Required: Yes") but the governance.yaml does not encode this.

- Evidence: classifier.governance.yaml output block has `location` and `levels` but no `required` field; all 5 other agents have `required: true`
- Severity: **Major**

**SR-002:** diataxis-auditor.md `<input>` Fallback Behavior covers "invalid document path" and "missing quadrant" but NOT "missing output path." The `<output>` section specifies a default location but this fallback is not surfaced in the guardrails section where a reader expects to find all fallbacks.

- Evidence: auditor.md Fallback Behavior: 2 cases listed; output path fallback documented only in `<output>` section
- Severity: **Minor**

### Internal Consistency Check

**SR-003:** diataxis-howto.md `<guardrails>` is structurally incomplete versus all 5 sibling agents. Tutorial, reference, explanation, and auditor all have `## Input Validation` and `## Output Filtering` subsections within `<guardrails>`. Howto has only `## Constitutional Compliance`, `## Domain-Specific Constraints`, and `## Fallback Behavior`.

- Evidence: howto.md guardrails: 3 subsections; all other agents: 5 subsections; governance.yaml correctly has input_validation and output_filtering fields — only the .md system prompt is missing them
- Severity: **Major** (the LLM will not see these behavioral constraints during execution)

**SR-004:** All four writer agents use `model: sonnet` plus Bash tool but do NOT declare `reasoning_effort` per ET-M-001. Per ET-M-001, C2-level agents SHOULD declare `reasoning_effort: medium`. None do.

- Evidence: All .md frontmatter files: `model: sonnet` without `reasoning_effort`; ET-M-001 in agent-development-standards.md: "SHOULD declare reasoning_effort aligned with criticality level"
- Severity: **Minor**

### Methodological Rigor Check

**SR-005:** Writer agents (tutorial, howto, reference, explanation) cite diataxis quality criteria (T-01 through T-08 etc.) inline in methodology but do not include a step to read `skills/diataxis/rules/diataxis-standards.md`. If criteria are updated in the standards file, writer agents silently apply stale criteria. The auditor correctly loads dynamically in Step 1.

- Evidence: tutorial.md Step 4: criteria listed by code inline; no Read step for diataxis-standards.md; auditor.md Step 1: "Read `skills/diataxis/rules/diataxis-standards.md`"
- Severity: **Major**

**SR-006:** diataxis-classifier multi-quadrant sequence numbering (tutorial=1, how-to=2, reference=3, explanation=4 per Step 4) is implied but not explicit. When content spans only 2 non-adjacent quadrants (e.g., tutorial + reference, skipping how-to), the sequence numbering creates a gap.

- Evidence: classifier.md Step 4: "Assign sequence numbers (tutorial first, then how-to, then reference, then explanation)" — gap case undefined
- Severity: **Minor**

### Evidence Quality Check

**SR-007:** All writer agents include Bash for step verification but no agent defines what "verification success" means in quantifiable terms. How does the agent determine a step "produces the documented result"? If the tutorial says "You should see: `Project created`" and Bash returns `Project created successfully.` (with "successfully" appended), does this pass or fail?

- Evidence: tutorial.md capabilities: "Bash to verify that tutorial steps actually produce the documented results" — no success criteria or output matching specification
- Severity: **Major**

### Actionability Check

**SR-008:** No agent defines a mapping from classifier output to writer input fields. The classifier outputs `quadrant, confidence, rationale, axis_placement`. The tutorial writer expects `Topic, Prerequisites, Target outcome, Output path`. No documented mapping exists for how an orchestrator should translate classifier output to writer input.

- Evidence: classifier.md output format: `{quadrant, confidence, rationale, axis_placement}`; tutorial.md input: `{Topic, Prerequisites, Target outcome, Output path}`; no mapping in any file
- Severity: **Minor**

### Traceability Check

**SR-009:** None of the 6 governance.yaml files use the `prior_art` field. The schema supports this for referencing source tasks and features. PROJ-013 worktracker entities (FEAT-013-001 for core writers, FEAT-013-002 for classifier/auditor) are not referenced from any agent definition.

- Evidence: All governance.yaml: no `prior_art` field; schema line 193-197: `prior_art` array available; PROJ-013 worktracker has FEAT-013-001, FEAT-013-002
- Severity: **Minor**

### S-010 Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-20260227 | classifier output.required absent — schema conditional bypassed | Major | classifier.governance.yaml: output block has location+levels but no `required` field | Completeness |
| SR-002-20260227 | auditor output path fallback in wrong section | Minor | Fallback for missing output path in `<output>` not `<guardrails>` | Completeness |
| SR-003-20260227 | howto .md body missing Input Validation and Output Filtering subsections | Major | howto.md guardrails: 3 subsections vs 5 in sibling agents; LLM will not see behavioral constraints | Internal Consistency |
| SR-004-20260227 | reasoning_effort not declared in any agent | Minor | All .md: no reasoning_effort; ET-M-001 SHOULD for C2+ | Completeness |
| SR-005-20260227 | Writer agents apply criteria from static methodology text, not from standards file | Major | tutorial.md et al.: criteria listed inline; no Read step for diataxis-standards.md | Methodological Rigor |
| SR-006-20260227 | Classifier multi-quadrant sequence numbering gap for non-adjacent quadrant pairs | Minor | classifier.md Step 4: sequential numbering undefined for sparse quadrant combinations | Completeness |
| SR-007-20260227 | Bash verification success criteria undefined in writer agents | Major | tutorial.md: "verify steps actually produce documented results" — no output match specification | Evidence Quality |
| SR-008-20260227 | No mapping from classifier output to writer input fields | Minor | classifier output: quadrant/confidence/rationale; writer input: Topic/Goal/Subject — no mapping | Actionability |
| SR-009-20260227 | prior_art unused — no traceability to PROJ-013 worktracker entities | Minor | All governance.yaml: no prior_art; FEAT-013-001, FEAT-013-002 unreferenced | Traceability |

---

## Finding Summary Table

| # | Agent(s) | Severity | Strategy | Finding | Location | Recommendation |
|---|---------|----------|----------|---------|----------|----------------|
| 1 | diataxis-classifier | **Critical** | S-013 (IN-001) | hint_quadrant bypass: confidence 1.00 for any hint regardless of plausibility — P-022 violation | classifier.md Step 5 | Run two-axis test when hint provided; cap at 0.85 if hint conflicts; note conflict in rationale |
| 2 | All 6 agents | **Major** | S-007 (CC-001) | H-23: all .md files >30 lines lack navigation tables; XML-tagged format conflicts with H-23 | All .md files | Formal exemption in agent-development-standards.md OR add minimal doc nav table before `<agent>` tag |
| 3 | diataxis-howto | **Major** | S-007 (CC-002) / S-010 (SR-003) | howto .md body missing `## Input Validation` and `## Output Filtering` guardrail subsections | howto.md `<guardrails>` | Add subsections matching tutorial/reference pattern |
| 4 | diataxis-classifier | **Major** | S-007 (CC-003) / S-010 (SR-001) | output.required absent in classifier.governance.yaml — schema conditional bypassed | classifier.governance.yaml output block | Add `required: true` to output block |
| 5 | diataxis-howto | **Major** | S-007 (CC-004) / S-002 (DA-005) | cognitive_mode: convergent conflicts with H-03 multi-path requirement; systematic is correct | howto.governance.yaml, howto.md identity | Change to `systematic`; update identity section prose |
| 6 | diataxis-explanation | **Major** | S-007 (CC-005) / S-002 (DA-001) | model: opus without documented justification; AD-M-009 SHOULD requires justification | explanation.md frontmatter, explanation.governance.yaml | Document justification or downgrade to sonnet |
| 7 | All 4 writer agents | **Major** | S-013 (IN-002) | Quadrant mixing flags written to output with no user confirmation gate | tutorial/howto/reference/explanation .md Step 5 | Add gate: if QUADRANT-MIX flags detected, describe to user and wait for resolution before Step 6 |
| 8 | diataxis-auditor | **Major** | S-013 (IN-003) / S-002 (DA-003) | Auditor internally re-implements classifier's two-axis logic — duplication, divergence risk | auditor.md Step 2 | Document as explicit fallback; reference standards file directly; note divergence risk |
| 9 | diataxis-auditor | **Major** | S-013 (IN-004) | No audit handling path for multi-quadrant documents | auditor.md methodology | Add Step 1b: multi-quadrant audit path; escalate_to_user when quadrant confidence <0.70 |
| 10 | All 4 writer agents | **Major** | S-013 (IN-004) / S-010 (SR-005) | Writers apply static inline criteria; do not load diataxis-standards.md at runtime | All writer .md Step 4 | Add Step 0: read diataxis-standards.md; use file criteria not memory |
| 11 | diataxis-tutorial, howto | **Major** | S-013 (IN-005) / S-002 (DA-004) | "Step-by-step" appears in both tutorial and howto descriptions — routing ambiguity | .md description fields | Add negative routing signals (tutorial: "NOT for quick task completion"; howto: "NOT for first-time learners") |
| 12 | All 6 agents | **Major** | S-002 (DA-006) | No session_context declared — classifier-to-writer pipeline lacks formal handoff contract | All governance.yaml files | Add session_context to classifier (on_send) and writers (on_receive) at minimum |
| 13 | diataxis-explanation | **Major** | S-002 (DA-002) | Bash listed in tools but NO Bash usage pattern in capabilities section — dead capability | explanation.md frontmatter + capabilities | Remove Bash from explanation tools; add usage guardrail to remaining 3 writers |
| 14 | All 4 writer agents | **Major** | S-010 (SR-007) | Bash verification success criteria undefined — no spec for what "produces documented results" means | All writer .md capabilities | Define success matching spec; add failure handling: annotate with [VERIFICATION-FAILED] |
| 15 | diataxis-auditor | **Minor** | S-013 (IN-006) | Auditor fallback for missing output path in `<output>` section, not `<guardrails>` | auditor.md Fallback Behavior | Move/duplicate fallback note to Fallback Behavior section |
| 16 | All 6 agents | **Minor** | S-007 (CC-006) | No session_context in any agent (covered by #12 at Major, listed here for S-007 traceability) | All governance.yaml | Resolved by finding #12 |
| 17 | diataxis-howto | **Minor** | S-007 (CC-007) | P-022 forbidden_action is generic vs. domain-specific in sibling agents | howto.governance.yaml | Change to "Misrepresent procedure accuracy or claim unverified steps work (P-022)" |
| 18 | diataxis-auditor | **Minor** | S-002 (DA-007) | PASS threshold allows 2 minor findings — may be too lenient for quality gate tool | auditor.md verdict thresholds | Tighten to ≤1 Minor or document rationale for 2-Minor tolerance |
| 19 | All 6 agents | **Minor** | S-002 (DA-008) | No enforcement section in any governance.yaml | All governance.yaml | Add `enforcement: {tier: medium, escalation_path: "/adversary skill"}` |
| 20 | All agents | **Minor** | S-010 (SR-004) | reasoning_effort not declared despite ET-M-001 SHOULD | All .md frontmatter | Add reasoning_effort: medium (C2) or high (C3) per criticality |
| 21 | diataxis-classifier | **Minor** | S-010 (SR-006) | Multi-quadrant sequence numbering gap for non-adjacent quadrants | classifier.md Step 4 | Clarify: "assign sequence by quadrant type; omit unused types" |
| 22 | All 6 agents | **Minor** | S-010 (SR-008) | No classifier-to-writer input mapping defined | classifier.md output + writer inputs | Define mapping table in SKILL.md or add to classifier session_context.on_send |
| 23 | All 6 agents | **Minor** | S-010 (SR-009) | prior_art field unused — no traceability to PROJ-013 worktracker | All governance.yaml | Add prior_art entries referencing FEAT-013-001, FEAT-013-002 |

---

## Execution Statistics

- **Total Findings:** 23 (some share IDs across strategies — 16 distinct issues at Major+, 7 Minor)
- **Critical:** 1 (IN-001: classifier hint bypass)
- **Major:** 13 (CC-001 through CC-005, IN-001 through IN-005, DA-001 through DA-006, SR-001, SR-003, SR-005, SR-007)
- **Minor:** 9
- **Strategies Executed:** 4 of 4 (S-007, S-013, S-002, S-010)
- **Agents Reviewed:** 6 (12 files total)

## Overall Assessment

**Constitutional compliance:** All 6 agents pass the core HARD rules (no Task tool, constitutional triplet declared, schema required fields present, tool tier consistent). The foundation is sound.

**Quality threshold assessment against >= 0.95:**

The 1 Critical finding (-0.10) and 13 Major findings (proportional adjustment -0.04 each = -0.52) and 9 Minor findings (-0.01 each = -0.09) yields:

1.00 - 0.10 - 0.52 - 0.09 = **0.29** — well below 0.95 threshold.

Even using the S-007 penalty model (Critical -0.10, Major -0.05, Minor -0.02):
1.00 - 0.10 - (13 × 0.05) - (9 × 0.02) = 1.00 - 0.10 - 0.65 - 0.18 = **0.07** — REJECTED.

The agent set requires targeted revision. The issues cluster into four fixable themes:

**Theme 1 — Classifier Safety (Critical):** IN-001 hint bypass is the highest-priority fix. It enables arbitrary confidence-1.00 misclassification.

**Theme 2 — Writer Agent Quality Gates (Major):** IN-002 (no mixing resolution gate), SR-005 (static criteria), SR-007 (undefined verification success), IN-005 (routing ambiguity) — all weaken the quality enforcement that differentiates Diataxis quadrants.

**Theme 3 — Auditor Completeness (Major):** IN-003 (classification duplication), IN-004 (no multi-quadrant path) limit the auditor's reliability as a quality enforcement tool.

**Theme 4 — Cross-Agent Workflow (Major):** DA-006/CC-006 (no session_context), DA-003/CC-004 (howto cognitive mode), CC-005/DA-001 (explanation model) are agent-level correctness issues with straightforward fixes.

**Priority order for remediation:**
1. IN-001 — Critical, classifier safety
2. Findings 2-14 — Major, grouped by agent (howto fixes together, writer fixes together, auditor fixes together)
3. Findings 15-23 — Minor, implement in same PR as Major fixes where co-located

---

*Report generated: 2026-02-27*
*Strategies applied: S-007 (CC prefix), S-013 (IN prefix), S-002 (DA prefix), S-010 (SR prefix)*
*Template references: s-007-constitutional-ai.md, s-013-inversion.md, s-002-devils-advocate.md, s-010-self-refine.md*
*SSOT: `.context/rules/quality-enforcement.md`, `.context/rules/agent-development-standards.md`*
