# ADR-001: Nuclear SOP Skill Architecture for Jerry Framework

> **PS ID:** phase-3.1 | **Entry ID:** e-003 | **Agent:** ps-architect-001
> **Date:** 2026-03-22 | **Revised:** 2026-03-23 (Iteration 3 -- QG3 FINAL revision)
> **Confidence:** HIGH (0.90)
> **Input Artifacts:** Phase 1 (nuclear-sop-survey.md, 0.88), Phase 2 (sop-pattern-extraction.md, 0.88), QG3 Review (architecture-review.md, adv-executor-003)
> **Criticality:** C3 (Significant) -- new skill architecture, >10 files, API surface change

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state |
| [Revision History](#revision-history) | QG3 findings addressed in this iteration |
| [L0: Executive Summary](#l0-executive-summary) | Non-technical decision overview |
| [L1: Technical Implementation](#l1-technical-implementation) | Engineer-facing design specification |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term strategic consequences |
| [Context](#context) | Problem motivating this decision |
| [Constraints](#constraints) | Jerry constitutional and architectural limits |
| [Forces](#forces) | Design tensions |
| [Options Considered](#options-considered) | Four architectures evaluated |
| [Decision](#decision) | Chosen option with rationale |
| [Architecture Specification](#architecture-specification) | Detailed skill and agent design |
| [H-36 Circuit Breaker Compliance](#h-36-circuit-breaker-compliance) | Formal hop analysis with rule-text citations |
| [Hold Point Implementation Specification](#hold-point-implementation-specification) | Detailed mechanics for USER-HOLD, QG-HOLD, IV-HOLD |
| [Procedure State Persistence](#procedure-state-persistence) | PROCEDURE_STATE.yaml for pause/resume and cross-session resume discovery |
| [Nuclear Pattern Mapping](#nuclear-pattern-mapping) | Pattern-to-agent assignment |
| [Fidelity Transparency](#fidelity-transparency) | What is preserved vs. approximated vs. impossible (P-022) |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Risks](#risks) | What could go wrong |
| [Implementation Roadmap](#implementation-roadmap) | Phased delivery plan |
| [Related Decisions](#related-decisions) | Links to other ADRs |
| [PS Integration](#ps-integration) | Orchestration context |
| [Self-Review Record](#self-review-record) | S-010 compliance |

---

## Status

**PROPOSED**

---

## Revision History

| Version | Date | Trigger | Changes |
|---------|------|---------|---------|
| 1.0.0 | 2026-03-22 | Initial creation | Full ADR produced by ps-architect-001 |
| 1.1.0 | 2026-03-23 | QG3 REVISE (0.850 < 0.920) | 6 required revisions applied (R1-R6). See below. |
| 1.2.0 | 2026-03-23 | QG3 REVISE (0.914 < 0.920) | 2 minor revisions applied (R7-R8). See below. |

### QG3 Iteration 3 Findings Addressed (adv-executor-003, 2026-03-23)

| Finding | Severity | Revision | Summary of Change |
|---------|----------|----------|-------------------|
| NC-001 | Minor | **R7: sop-capture Integrated Verification for 3-Hop Mode** | Added conditional Step 0 to sop-capture methodology: when operating in 3-hop mode (no IV report available), sop-capture performs integrated verification of executor work products before proceeding to OE capture. Includes anchoring-bias disclaimer. |
| NC-002 | Minor | **R8: Cross-Session Resume Discovery** | Added resume discovery subsection to Procedure State Persistence: orchestrator checks for PROCEDURE_STATE.yaml files with non-terminal status at session start. References ORCHESTRATION.yaml resumption context pattern. |

### QG3 Findings Addressed (adv-executor-003, 2026-03-22)

| Finding | Severity | Revision | Summary of Change |
|---------|----------|----------|-------------------|
| PM-001 / CC-002 | Critical / Major | **R1/R3: H-36 Compliance Proof** | Replaced informal "quality gate" claim with formal rule-text analysis. Redesigned workflow as star topology (orchestrator fan-out). Documented that 3 of 4 transitions are hops; verifier is the ambiguous case. Provided both compliant-by-design (3-hop) and enhanced (4-hop with governance request) modes. |
| PM-002 | Critical | **R2: Hold State Persistence** | Added PROCEDURE_STATE.yaml specification with full schema for mid-execution pause and cross-session resume. Defined resume protocol with place-keeper reconstruction from filesystem state. |
| CC-002 | Major | **R3: Formal H-36 Proof** | Cited H-36 rule text verbatim. Analyzed each transition against the "routing logic re-evaluates the destination" criterion. Documented that predetermined skill-internal sequences are an ambiguous case not explicitly covered by current H-36 text. |
| DA-004 | Major | **R4: Hold Point Implementation** | Added full implementation specification for all three hold point types: USER-HOLD (AskUserQuestion + PROCEDURE_STATE.yaml), QG-HOLD (ps-critic via /adversary S-014, threshold per H-13), IV-HOLD (main context invokes sop-verifier via Task, passes only artifact paths). |
| DA-005 | Major | **R5: sop-brief Workflow Generation** | Added Step 0 to sop-brief methodology: generate draft workflow definition from natural language when no file is provided. Added `sop-author` as a future consideration but scoped generation into sop-brief for Phase 1. |
| DA-001 | Major | **R6: Verifier Independence Transparency** | Moved Independent Verification (C-2) from "Preserved" to "Approximated" in the fidelity table. Explicitly documented what FC-M-001 provides (context isolation, anchoring bias prevention) vs. what nuclear Criterion X requires (different qualified person). |

### Additional QG3 Items Addressed (P1/P2)

| Finding | Severity | Change |
|---------|----------|--------|
| PM-003 | Major | Added canonical execution log version rule to sop-capture methodology. |
| PM-004 | Major | Scoped sop-executor Bash usage to specific use cases with CAUTION annotation. |
| PM-006 | Major | Committed to providing 1 worked example workflow definition in Phase 1 deliverables. |
| CC-001 | Minor | Added governance YAML skeleton for sop-verifier as reference. |
| CC-003 | Minor | Acknowledged 21-skill count; confirmed keyword-first routing remains adequate. |
| CC-004 | Minor | Added mandatory-skill-usage.md to Implementation Roadmap registration targets. |
| DA-002 | Minor | Added explicit relationship between CONTINUOUS/REFERENCE/INFORMATION and C1-C4. |
| DA-003 | Minor | Added STAR vs. S-010 comparison table. |
| DA-006 | Minor | Added decision table: when to use /nuclear-sop vs. /orchestration. |
| PM-005 | Minor | Added workflow_type field to OE entry schema. |

---

## L0: Executive Summary

We need to decide how to bring nuclear power plant procedural discipline into Jerry's AI agent workflows. Nuclear engineering has spent 50+ years developing the most rigorous procedure-compliance framework in any industry -- practices like mandatory pre-job briefings, step-by-step place-keeping with sign-offs, independent verification by someone other than the performer, and post-job lessons-learned capture. Phase 1 research identified 22 such patterns. Phase 2 analysis found that Jerry already partially implements 11 of them, but 3 high-value patterns are entirely missing: formalized pre-execution briefings, post-execution experience capture, and step-level compliance classification.

We evaluated three options: a three-agent skill (brief/execute/capture), a five-agent skill (adding independent verifier and procedure reviewer), and embedding nuclear patterns into existing Jerry skills without creating a new one. We recommend **Option D: a four-agent `/nuclear-sop` skill** -- a refinement of the Phase 2 three-agent proposal that adds a dedicated `sop-verifier` agent inspired by the nuclear principle that the person who verifies must not be the person who performed the work. The verifier provides context isolation and anchoring-bias prevention (via FC-M-001 fresh context), which approximates but does not fully replicate nuclear independent verification (see Fidelity Transparency section for the honest distinction).

The skill introduces three workflow phases -- brief, execute, capture -- that wrap any Jerry agent workflow with nuclear-inspired procedural rigor. It does not replace existing Jerry quality gates; it supplements them with a structured workflow definition format, STAR self-checking at tool-call boundaries, named hold points with persistent execution state for pause/resume, and a mandatory operating experience feedback loop.

---

## L1: Technical Implementation

### Skill Structure

```
skills/nuclear-sop/
  SKILL.md                          # Skill definition (activation keywords, routing)
  agents/
    sop-brief.md                    # Pre-job briefing agent (+ workflow def generation)
    sop-brief.governance.yaml
    sop-executor.md                 # Procedure execution with STAR + hold points
    sop-executor.governance.yaml
    sop-verifier.md                 # Independent verification agent
    sop-verifier.governance.yaml
    sop-capture.md                  # Post-job OE capture agent
    sop-capture.governance.yaml
  templates/
    WORKFLOW_DEFINITION.template.md  # 11-section nuclear procedure template
    PRE_JOB_BRIEF.template.md       # Briefing output template
    POST_JOB_BRIEF.template.md      # OE capture output template
    HOLD_POINT_LOG.template.md       # Hold point sign-off record
    PROCEDURE_STATE.template.yaml    # Execution state for pause/resume
  examples/
    c3-adr-workflow-definition.md    # Worked example: C3 ADR with nuclear rigor
  rules/
    nuclear-sop-behavior-rules.md   # Skill-scoped behavioral rules
```

### Agent Taxonomy

| Agent | Role | Cognitive Mode | Tool Tier | Model | Input | Output |
|-------|------|---------------|-----------|-------|-------|--------|
| `sop-brief` | Pre-job briefing: load context, check prerequisites, review OE, identify error traps; optionally generate workflow definition from natural language | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | Workflow definition file (or natural language description), project context, OE history | `brief/pre-job-brief.md` (and optionally `brief/draft-workflow-definition.md`) |
| `sop-executor` | Step-by-step procedure execution with STAR self-checking, place-keeping, hold points, persistent execution state | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash) | opus | Pre-job brief, workflow definition, target artifacts | Step-annotated execution log, primary work products, PROCEDURE_STATE.yaml |
| `sop-verifier` | Context-isolated verification of executor output; separate context, no access to executor reasoning | convergent | T1 (Read, Glob, Grep) | sonnet | Work product file paths only (no executor reasoning) | `verification/iv-report.md` |
| `sop-capture` | Post-job OE capture: deviations, quality gate results, lessons learned, improvement recommendations | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | Execution log (FINAL version), IV report, quality scores, pre-job brief | `capture/post-job-brief.md`, `capture/oe-entry.md` |

**Bash tool scope for sop-executor (PM-004 response):** Bash is included in sop-executor's T2 tool set for specific use cases: running test suites (`uv run pytest`), executing linting/formatting tools (`uv run ruff`), and running project-specific build commands specified in workflow definition steps. General-purpose Bash commands that modify system state outside the workflow scope are prohibited. The sop-executor methodology includes a CAUTION annotation: "Bash tool use requires STAR with WARNING-level scrutiny. Bash commands that modify state outside the target artifact scope require `[USER-HOLD]` annotation in the workflow definition."

### Workflow Execution Sequence

```
USER REQUEST + WORKFLOW DEFINITION (or natural language description)
        |
        v
+-------------------+
| 0. sop-brief      |  (Optional) Workflow Definition Generation
|   IF no workflow   |  Generate draft from natural language
|   definition file  |  Ask user to confirm before proceeding
+--------+----------+
         |
         v
+-------------------+
| 1. sop-brief      |  Pre-Job Briefing Phase
|   - Load context   |  (Patterns: F-2a, D-1, H-2, A-3 sections 1-6)
|   - Check prereqs  |
|   - Review OE      |
|   - Identify traps  |
+--------+----------+
         |
         | Pre-Job Brief artifact
         v
+-------------------+
| 2. sop-executor   |  Execution Phase
|   - STAR per step  |  (Patterns: B-1, A-5, A-2, A-4, D-2, C-3)
|   - Place-keeping  |  State persisted to PROCEDURE_STATE.yaml
|   - Hold points    |
|   - Step sign-off  |
+--------+----------+
         |
         | Work products + execution log + PROCEDURE_STATE.yaml
         v
+-------------------+
| 3. sop-verifier   |  Context-Isolated Verification Phase
|   - Fresh context  |  (Patterns: C-2 approximation, C-3)
|   - IV checklist   |  (Implements FC-M-001: context isolation)
|   - No executor    |  (Does NOT implement nuclear Criterion X personnel
|     reasoning      |   independence -- see Fidelity Transparency)
+--------+----------+
         |
         | IV report (pass/fail + findings)
         v
+-------------------+
| 4. sop-capture    |  Post-Job Capture Phase
|   - What worked    |  (Patterns: F-2b, H-1, H-2)
|   - Deviations     |  Uses FINAL execution log version only
|   - Lessons learned |
|   - OE entry       |
+-------------------+
         |
         v
    OE ENTRY (persisted to docs/experience/)
```

### STAR Self-Checking Implementation

The STAR protocol is applied by `sop-executor` before each tool call that modifies state (Write, Edit, Bash). This is distinct from S-010 (Self-Refine), which is a post-completion review. STAR is a pre-action checkpoint.

```
Before each state-modifying tool call:

  S - STOP:  Log current step number and target action.
             Verify: Am I on the correct step per the workflow definition?
             Verify: Is this the correct file/target per the step specification?

  T - THINK: What is the expected outcome of this action?
             What are the preconditions for this step?
             What could go wrong? (Check WARNING/CAUTION from workflow definition)
             Is the step classified [CONTINUOUS] (must execute exactly) or
             [REFERENCE] (judgment permitted)?

  A - ACT:   Execute the tool call.
             Maintain focus on the specified target.

  R - REVIEW: Did the outcome match expectation?
              If not: STOP WORK (D-2). Log deviation. Escalate per hold point type.
              If yes: Sign off step in execution log. Advance place-keeper.
              Update PROCEDURE_STATE.yaml with completed step.
```

**Implementation note:** STAR is encoded in the `sop-executor` agent's methodology section as a mandatory pre-action protocol. It is NOT a separate agent. The executor applies STAR inline before each tool call, producing a structured log entry per step. For `[REFERENCE]`-classified steps, the Think phase permits agent judgment about execution approach; for `[CONTINUOUS]`-classified steps, the Think phase verifies exact conformance to the written step.

#### STAR vs. S-010 Comparison (DA-003 response)

| Dimension | STAR Self-Checking (B-1) | S-010 Self-Refine |
|-----------|--------------------------|-------------------|
| **Timing** | Pre-action: before each tool call | Post-completion: after entire deliverable |
| **Scope** | Single step / single tool call | Entire output artifact |
| **Trigger** | Every state-modifying tool call (Write, Edit, Bash) | End of agent execution |
| **Action on failure** | Stop-Work (D-2): halt execution immediately | Revision: re-enter reasoning loop |
| **State tracking** | Updates PROCEDURE_STATE.yaml per step | No state file |
| **Nuclear analog** | Operator self-checking before each valve operation | Supervisor walk-down after shift |
| **Value for CONTINUOUS steps** | High: enforces stop-check-act-review sequencing, prevents "running ahead" | Low: post-hoc review cannot undo steps already executed |
| **Value for REFERENCE steps** | Moderate: STAR Think phase permits adaptation but still requires deliberate pause | Same as CONTINUOUS: post-hoc review |
| **LLM implementation reality** | Both STAR reasoning and tool call are generated in the same inference pass; the temporal separation is a structural constraint in the prompt, not a physical interruption as in nuclear plant operations | Same cognitive process applied after completion |

### Procedure Use Classification

Steps in the workflow definition are annotated with use levels:

| Classification | Annotation | Executor Behavior | Nuclear Analog | Relationship to C1-C4 |
|---------------|------------|-------------------|----------------|----------------------|
| **Continuous** | `[CONTINUOUS]` | Must execute exactly as written, in sequence. No deviation. Full STAR. Place-keeping with step sign-off. | EOPs, STPs -- "read and follow each step in sequence" | Typically used in C3+ workflows. DEFAULT for steps without annotation in C3+ workflows. |
| **Reference** | `[REFERENCE]` | Consult step for guidance. Agent may exercise judgment on execution approach. STAR Think phase permits adaptation. | AOPs, ARPs -- "consult as needed" | Typically used in C1-C2 workflows. DEFAULT for steps without annotation in C1-C2 workflows. |
| **Information** | `[INFORMATION]` | Background context loaded into brief. Not executed as a step. | Reference materials -- "available for consultation" | Used at any criticality for context-only content. |

**Relationship to C1-C4 criticality (DA-002 response):** The CONTINUOUS/REFERENCE/INFORMATION taxonomy operates at the *step level* within a workflow, while C1-C4 criticality operates at the *deliverable level* across the framework. They are complementary, not redundant. C1-C4 determines *whether* to use nuclear rigor and *how much* quality gate enforcement to apply. CONTINUOUS/REFERENCE/INFORMATION determines *how each step within a nuclear-rigor workflow is executed*. A C3 workflow might contain both CONTINUOUS steps (critical path) and REFERENCE steps (supporting tasks). The default classification rules bridge the two systems: C3+ workflows default to CONTINUOUS; C1-C2 default to REFERENCE.

### Structured Workflow Definition Format

The 11-section nuclear procedure structure maps to a workflow definition template. **User authoring scope:** Users write sections 1-9. Sections 10-11 are populated at runtime by the skill.

| # | Nuclear Section | Workflow Definition Section | Content | Author |
|---|----------------|---------------------------|---------|--------|
| 1 | Cover/Title Page | `## Metadata` | Workflow ID, version, classification, author, date | User |
| 2 | Purpose and Scope | `## Purpose and Scope` | What this workflow accomplishes, boundaries | User |
| 3 | References | `## References` | Related ADRs, standards, prior workflows | User |
| 4 | Prerequisites | `## Prerequisites` | Required project state, files that must exist, env vars | User |
| 5 | Initial Conditions | `## Initial Conditions` | System/project state assertions checked by sop-brief | User |
| 6 | Limitations and Precautions | `## Limitations and Precautions` | Boundaries that must not be exceeded; scope limits | User |
| 7 | WARNING/CAUTION/NOTE | Inline in steps | `WARNING:` before steps with irreversible consequences; `CAUTION:` before steps with quality risk; `NOTE:` for guidance | User |
| 8 | Performance Steps | `## Steps` | Numbered steps with `[CONTINUOUS]`/`[REFERENCE]`/`[INFORMATION]` and hold point annotations | User |
| 9 | Acceptance Criteria | `## Acceptance Criteria` | Quantitative/qualitative success measures per step and overall | User |
| 10 | Sign-off/Verification | Hold point log | Captured in `HOLD_POINT_LOG.md` | Runtime |
| 11 | Attachments/Data Sheets | `## Attachments` | Supporting data, templates, reference files | Runtime |

### Trigger Keywords

For `mandatory-skill-usage.md` integration:

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow | adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review | 12 | "nuclear procedure" OR "pre-job brief" OR "post-job brief" OR "STAR self-check" OR "hold point" (phrase match) | `/nuclear-sop` |

### When to Use: `/nuclear-sop` vs. `/orchestration` (DA-006 response)

| Condition | Use `/nuclear-sop` | Use `/orchestration` + `/adversary` |
|-----------|--------------------|------------------------------------|
| Task has a defined procedure with numbered steps | Yes | No -- orchestration manages phases, not steps |
| Task requires step-level place-keeping and sign-off | Yes | No -- no step-level tracking |
| Task requires pre-job context loading as a formal phase | Yes | No -- context loading is infrastructure |
| Task requires independent verification of work products | Yes (sop-verifier) | Partial -- FC-M-001 via Task tool, but not structured |
| Task requires post-job OE capture | Yes (sop-capture) | No -- no mandatory OE mechanism |
| Task is multi-phase research/analysis pipeline | No -- nuclear-sop is for procedures | Yes |
| Task requires multiple skills coordinated in sequence | No -- nuclear-sop is a single skill | Yes |
| Task is C1 routine work | No -- disproportionate overhead | Optional |
| Task has no defined procedure | Use sop-brief to generate one, then decide | Yes -- orchestration handles ad-hoc coordination |

---

## L2: Architectural Implications

### Long-Term Evolution Path

**Phase 1 (Immediate):** The `/nuclear-sop` skill establishes the three-phase workflow pattern (brief/execute-verify/capture) as a reusable architectural primitive. Other Jerry skills can adopt this pattern selectively -- any skill could add a pre-job brief phase or post-job capture phase without adopting the full nuclear rigor.

**Phase 2 (6 months):** The structured workflow definition format becomes a candidate for adoption beyond `/nuclear-sop`. If the 11-section template proves valuable, it could become Jerry's standard workflow specification format, analogous to how ORCHESTRATION_PLAN.md standardized orchestration workflows.

**Phase 3 (12 months):** The OE feedback loop matures. Post-job OE entries accumulate. Periodic synthesis (via ps-synthesizer) identifies recurring failure patterns and proposes workflow definition revisions. This closes the nuclear feedback loop: every execution teaches, every lesson improves the next execution.

**Phase 4 (18+ months):** Symptom-based emergency routing (GAP-06) could be formalized as ABNORMAL/EMERGENCY workflow types that activate on observable symptoms (quality score collapse, repeated hold point failures, context fill emergency) rather than requiring diagnosis of the root cause first.

### Systemic Consequences

**Positive systemic effects:**
1. **Temporal discipline becomes explicit.** The brief/execute/capture pattern makes pre-execution and post-execution first-class workflow phases, not afterthoughts. This addresses the systemic weakness identified in Phase 2: current AI agent frameworks treat context loading as infrastructure rather than a procedural step.
2. **Step-level granularity.** The procedure use classification system introduces per-step compliance rigor. This is a granularity increase from Jerry's current phase-level enforcement to step-level enforcement -- a significant architectural evolution.
3. **Feedback loop closes.** The mandatory OE entry after every workflow execution creates a data source for continuous improvement that currently does not exist in Jerry.
4. **Context-isolated verification formalized.** While FC-M-001 already recommends fresh-context review for C3+ deliverables, `sop-verifier` makes this a named, structured, non-optional phase with its own agent, checklist, and sign-off. This provides context isolation and anchoring bias prevention -- genuine quality improvements over in-context self-review, even though it does not replicate nuclear-grade personnel independence (see Fidelity Transparency).

**Negative systemic effects:**
1. **Context budget pressure.** Four agent invocations per workflow (brief + executor + verifier + capture) consume significant context window. Each Task invocation costs approximately 2,000-8,000 tokens for agent definition loading (CB-02 concern). A full nuclear-rigor workflow could consume 20-30% of the context window on agent overhead alone.
2. **Execution latency.** Four sequential agent phases increase wall-clock time. The `sop-verifier` phase is especially impactful because it requires a fresh-context invocation (Task tool) that cannot parallelize with the executor.
3. **Governance surface area.** Four new agent definitions, a new SKILL.md, behavioral rules, and templates add maintenance burden. Each agent requires H-34/H-35 compliance, governance YAML, and ongoing version management.
4. **Adoption friction.** Users must create workflow definition files before invoking the skill. This is partially mitigated by sop-brief's Step 0 (generate from natural language), but structured workflow definitions remain the primary operating mode for C3+ work.
5. **Circuit breaker tension.** The 4-agent sequence creates an ambiguous case under H-36 that requires either a governance ruling or a fallback 3-hop design. See H-36 Circuit Breaker Compliance section.

### Integration with Existing Architecture

**Composability with `/orchestration`:** The `/nuclear-sop` skill is designed to work *within* orchestration workflows. An orchestrated pipeline could invoke `/nuclear-sop` for individual phases that require nuclear-grade rigor, while using standard `/problem-solving` agents for research phases. The orchestrator sequences the `/nuclear-sop` skill as a workflow unit. **Hop budget consideration:** When composed within orchestration, the nuclear-sop skill's internal hops count against the orchestration pipeline's hop budget. This means orchestration pipelines that include nuclear-sop must reserve 3 hops (or 2 in 3-hop fallback mode) for the skill.

**Composability with `/adversary`:** The QG-HOLD points in `/nuclear-sop` invoke the same quality gate infrastructure (H-13, H-14, S-014) that `/adversary` uses. The `sop-verifier` agent provides nuclear-inspired context-isolated verification that supplements (not replaces) adversarial quality review.

**Composability with `/problem-solving`:** The `sop-executor` can delegate individual execution steps to ps-agents via the main context (orchestrator pattern). The nuclear skill provides the procedural wrapper; problem-solving agents provide the analytical capability.

**Skill count impact (CC-003 response):** Adding `/nuclear-sop` brings the skill count from 20 to 21, which is one skill above the H-37 Phase 1 threshold of 20 skills. H-37 requires keyword-first routing below 20 skills; above 20, the Phase 2 transition analysis from agent-routing-standards.md Scaling Roadmap applies. At 21 skills, keyword-first routing remains adequate -- the threshold is for when to *require* keyword-first routing, not when to *stop* using it. The Phase 2 transition trigger conditions (10+ collision zones, false negative rate > 40%, user override rate > 30%) should be evaluated when this skill is registered.

---

## Context

The Jerry Framework provides structured agent workflows for software engineering, systems engineering, and quality assurance. Phase 1 research (nuclear-sop-survey.md, confidence 0.88) surveyed nuclear power plant standard operating procedure practices across NRC regulations, INPO standards, DOE handbooks, and IAEA guidance. Phase 2 analysis (sop-pattern-extraction.md, confidence 0.88) extracted 22 patterns across 9 families, mapped them to Jerry equivalents, identified 8 gaps, and recommended a 3-agent skill architecture.

The motivation for this ADR is to determine the optimal skill architecture for bringing nuclear SOP discipline into Jerry's AI agent workflows, preserving the highest-value patterns while respecting Jerry's constitutional constraints and practical implementation limits.

**Key inputs from Phase 2:**
1. 22 nuclear SOP patterns extracted across 9 families (A-1 through I-1)
2. 8 gaps identified; 3 are high-value and high-feasibility (GAP-01 Pre-Job Brief, GAP-02 Post-Job Brief, GAP-03 Procedure Use Classification)
3. 3-agent architecture recommended: nse-brief + nse-executor + nse-capture
4. Nuclear framework extends Jerry at the workflow definition layer and feedback layer
5. Concurrent peer checking (GAP-05) is architecturally impossible
6. Operations Turnover (I-1) maps to Strong fit with existing handoff schema

---

## Constraints

| ID | Constraint | Source | Impact on Design |
|----|-----------|--------|-----------------|
| P-003 | Max 1 nesting level (orchestrator to workers) | H-01 | No agent spawns sub-agents. Verifier must be invoked by main context, not by executor. |
| P-020 | User authority preserved | H-02 | USER-HOLD points require explicit user approval. User can waive hold points. |
| P-022 | Transparent about preserved vs. approximated patterns | H-03 | ADR and SKILL.md must document which patterns are approximated. |
| H-34 | Dual-file agent architecture (.md + .governance.yaml) | agent-development-standards | Each agent requires both files. |
| H-35 | Constitutional triplet in every agent | agent-development-standards | P-003, P-020, P-022 in every forbidden_actions. |
| H-36 | Circuit breaker max 3 hops | agent-routing-standards | 4-agent sequence must be analyzed against hop definition. See H-36 Compliance section. |
| H-13 | Quality threshold >= 0.92 for C2+ | quality-enforcement | QG-HOLD gates enforce this threshold. |
| H-14 | Creator-critic-revision min 3 iterations | quality-enforcement | QG-HOLD failure triggers revision cycle. |
| H-22 | Proactive skill invocation | mandatory-skill-usage | Trigger keywords must be registered. |
| H-25/H-26 | Skill naming and registration standards | skill-standards | SKILL.md, kebab-case folder, CLAUDE.md + AGENTS.md + mandatory-skill-usage.md registration. |

---

## Forces

| Force | Tension |
|-------|---------|
| Nuclear fidelity vs. implementation complexity | More agents = higher fidelity but higher token cost and maintenance burden |
| Verification independence vs. P-003 nesting limit | Independent verifier must run in fresh context but cannot be spawned by executor |
| Step-level rigor vs. C1 task overhead | Full STAR on every tool call is excessive for routine tasks |
| OE feedback value vs. OE entry accumulation | Mandatory post-job capture produces data that must be periodically synthesized |
| Composability vs. self-containment | Skill must work standalone AND within orchestration pipelines |
| Adoption simplicity vs. workflow definition upfront cost | Users must create workflow definitions before using the skill |
| H-36 compliance vs. verification independence | A strict 3-hop reading may require merging verifier into another phase |

---

## Options Considered

### Evaluation Dimensions

| Dimension | Weight | Definition |
|-----------|--------|------------|
| Nuclear Fidelity | 0.25 | How accurately the option preserves nuclear SOP principles |
| Jerry Compliance | 0.20 | P-003, P-020, P-022, H-34, H-35, H-36 compliance |
| Implementation Complexity | 0.15 | Number of new files, agents, rules needed |
| Composability | 0.15 | Integration with existing Jerry skills |
| Value per Agent | 0.15 | Whether each agent carries sufficient distinct responsibility |
| Maintenance Burden | 0.10 | Ongoing governance cost |

### Option A: Three-Agent Architecture (Phase 2 Recommendation)

`sop-brief` (pre-job) + `sop-executor` (STAR + hold points) + `sop-capture` (post-job OE)

**Steelman (S-003):** This is the most efficient architecture. Three agents provide a clean mapping to the nuclear temporal discipline (before/during/after). Each agent has a clearly distinct responsibility. The token budget is minimized with only 3 Task invocations. Implementation is the simplest of the dedicated-skill options. The executor handles both execution and verification internally via STAR self-checking. H-36 compliance is unambiguous at 3 hops.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Nuclear Fidelity | 6 | Missing dedicated IV agent violates Appendix B Criterion X: "Inspection shall be performed by individuals other than those who performed the activity." Self-checking (STAR) is not independent verification. |
| Jerry Compliance | 9 | Clean P-003 compliance; 3 hops fits within circuit breaker budget. |
| Implementation Complexity | 9 | 3 agents + SKILL.md + templates = ~12 files. Manageable. |
| Composability | 8 | Fits within orchestration as a 3-phase unit. |
| Value per Agent | 9 | Each agent has a clearly distinct concern. |
| Maintenance Burden | 9 | 3 agent definitions to maintain. Lowest governance cost. |

**Weighted Score:** 0.25(6) + 0.20(9) + 0.15(9) + 0.15(8) + 0.15(9) + 0.10(9) = 1.50 + 1.80 + 1.35 + 1.20 + 1.35 + 0.90 = **8.10**

### Option B: Five-Agent Architecture (Full Nuclear Fidelity)

`sop-brief` + `sop-executor` + `sop-verifier` + `sop-capture` + `sop-reviewer`

**Steelman (S-003):** This is the highest-fidelity option. The dedicated `sop-verifier` implements Appendix B Criterion X with architectural separation between performer and inspector. The `sop-reviewer` provides procedure maintenance capability -- reviewing workflow definitions for currency, incorporating OE, and proposing revisions. This mirrors the nuclear industry's distinction between performing work, verifying work, and maintaining procedures. Every nuclear workflow role has a dedicated agent.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Nuclear Fidelity | 9 | Full role separation: performer, verifier, reviewer. Matches nuclear org chart. |
| Jerry Compliance | 7 | 5 hops in sequence would exceed H-36 circuit breaker (max 3). Requires careful composition to avoid routing loop detection. P-003 compliant if main context orchestrates all 5. |
| Implementation Complexity | 4 | 5 agents + SKILL.md + templates = ~18 files. Substantial initial investment. |
| Composability | 5 | 5-agent sequence is difficult to compose within orchestration without exceeding hop budget. |
| Value per Agent | 5 | `sop-reviewer` duplicates functionality of existing `/adversary` (procedure review) and worktracker (procedure maintenance). Insufficient distinct value. |
| Maintenance Burden | 4 | 5 agent definitions, 5 governance YAMLs. Highest ongoing cost. |

**Weighted Score:** 0.25(9) + 0.20(7) + 0.15(4) + 0.15(5) + 0.15(5) + 0.10(4) = 2.25 + 1.40 + 0.60 + 0.75 + 0.75 + 0.40 = **6.15**

### Option C: Embedded Enhancement (No New Skill)

Add nuclear patterns to existing `/orchestration`, `/problem-solving`, and `/adversary` skills.

**Steelman (S-003):** This avoids the governance overhead of a new skill entirely. Nuclear patterns like STAR self-checking could be added to all agent definitions as a behavioral primitive. Pre-job briefing could become a standard orchestration phase. Post-job capture could extend the worktracker. No new routing keywords needed. Zero learning curve because users invoke existing skills. The nuclear concepts permeate the framework rather than living in an isolated skill.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Nuclear Fidelity | 3 | Patterns scattered across skills lose coherence. No dedicated workflow definition format. No structured pre/post-job phases. The nuclear temporal discipline (before/during/after as first-class concepts) is lost when patterns are distributed. |
| Jerry Compliance | 10 | No new agents, no new routing, no new nesting. Fully compliant by definition. |
| Implementation Complexity | 7 | Modifying existing agents is less work than creating new ones, but cross-cutting changes across many files are error-prone. |
| Composability | 10 | No composition needed -- patterns are already in existing skills. |
| Value per Agent | N/A | No new agents. Existing agents gain marginal enhancement. |
| Maintenance Burden | 6 | Changes distributed across many files. No single owner for nuclear pattern coherence. Maintenance diffusion risk. |

**Weighted Score:** 0.25(3) + 0.20(10) + 0.15(7) + 0.15(10) + 0.15(5*) + 0.10(6) = 0.75 + 2.00 + 1.05 + 1.50 + 0.75 + 0.60 = **6.65**

*Value per Agent scored as 5 (neutral) since dimension is not directly applicable.*

### Option D: Four-Agent Architecture (Recommended)

`sop-brief` + `sop-executor` + `sop-verifier` + `sop-capture`

This is a refinement of Options A and B. It adds the context-isolated verifier from Option B to Option A's three-agent base, but omits the procedure reviewer (which duplicates existing capabilities).

**Steelman for rejected alternatives before deciding:**

- **Option A's strongest argument:** "STAR self-checking within the executor is sufficient for verification; a separate verifier adds token cost without proportional quality improvement." **Counter:** STAR is self-checking by the performer. While nuclear Appendix B Criterion X ("inspection shall be performed by individuals other than those who performed the activity") cannot be fully replicated by AI agents sharing the same model (see Fidelity Transparency), the context isolation provided by FC-M-001 via a separate agent prevents anchoring bias -- the verifier evaluates the work product without being anchored to the executor's reasoning chain. This is a genuine quality improvement over self-review, even if it does not achieve full nuclear-grade independence.

- **Option B's strongest argument:** "The procedure reviewer agent completes the nuclear lifecycle: create procedures, execute them, verify them, capture OE, and maintain them." **Counter:** Procedure review/maintenance in Jerry is already covered by `/adversary` (S-002, S-003 applied to any artifact) and the worktracker (issue tracking for procedure updates). A dedicated `sop-reviewer` agent would need to differ meaningfully from adv-executor + worktracker, and the Phase 2 analysis does not identify a gap that these existing tools cannot fill. The fifth agent's value is insufficient to justify the circuit breaker pressure and governance cost.

- **Option C's strongest argument:** "Nuclear discipline should permeate the framework, not be an optional add-on skill." **Counter:** Embedding nuclear patterns in existing skills destroys the coherence of the nuclear temporal discipline (before/during/after). The pre-job brief is not merely "better context loading" -- it is a structured procedural phase with its own agent, output template, and quality gate. Distributing this across `/orchestration` (brief), `/problem-solving` (execution), and `/adversary` (verification) loses the workflow-as-a-unit architectural property that makes nuclear procedures effective.

| Dimension | Score (1-10) | Rationale |
|-----------|-------------|-----------|
| Nuclear Fidelity | 8 | Context-isolated verification preserved via FC-M-001 pattern. Missing only procedure review/maintenance agent (acceptable -- covered by existing skills). Honest that this approximates, not replicates, nuclear IV. |
| Jerry Compliance | 8 | P-003 compliant. H-36 compliance depends on hop interpretation -- 3 hops under primary design, 4 under strict reading. See H-36 Compliance section for full analysis and fallback design. |
| Implementation Complexity | 7 | 4 agents + SKILL.md + templates + examples = ~16 files. Moderate. |
| Composability | 7 | Fits within orchestration as a 4-phase unit. Verifier adds 1 phase vs. Option A. |
| Value per Agent | 8 | Each agent has distinct responsibility. Verifier justified by context isolation value for C3+ work. |
| Maintenance Burden | 7 | 4 agent definitions. Moderate governance cost. |

**Weighted Score:** 0.25(8) + 0.20(8) + 0.15(7) + 0.15(7) + 0.15(8) + 0.10(7) = 2.00 + 1.60 + 1.05 + 1.05 + 1.20 + 0.70 = **7.60**

### Comparison Summary

| Option | Weighted Score | Nuclear Fidelity | Jerry Compliance | Complexity | Key Trade-off |
|--------|---------------|------------------|-----------------|------------|---------------|
| A: Three-Agent | **8.10** | 6 | 9 | 9 | Highest efficiency but sacrifices IV independence |
| B: Five-Agent | 6.15 | 9 | 7 | 4 | Highest fidelity but exceeds hop budget, duplicates existing capabilities |
| C: Embedded | 6.65 | 3 | 10 | 7 | Zero overhead but destroys nuclear coherence |
| **D: Four-Agent** | **7.60** | **8** | **8** | **7** | **Best balance of fidelity and practicality** |

---

## Decision

**We choose Option D: Four-Agent `/nuclear-sop` Skill Architecture** (`sop-brief`, `sop-executor`, `sop-verifier`, `sop-capture`).

### Rationale

1. **Context-isolated verification provides genuine quality value.** The sop-verifier agent, invoked with fresh context and no access to executor reasoning, prevents anchoring bias that in-context self-review cannot avoid. While this approximates rather than replicates nuclear Appendix B Criterion X (see Fidelity Transparency), the context isolation is a real architectural improvement for C3+ deliverables -- consistent with FC-M-001's recommendation.

2. **Four agents is the minimum for nuclear temporal discipline.** The before/during/after pattern requires at least 3 agents (brief/execute/capture). Adding the verifier between execution and capture preserves the nuclear inspection sequence without the overhead of Option B's fifth agent.

3. **Option B's fifth agent lacks sufficient distinct value.** Procedure review and maintenance are already served by `/adversary` (adversarial review of any artifact) and the worktracker (tracking procedure update needs). The `sop-reviewer` would duplicate these capabilities without adding nuclear-specific value that justifies the circuit breaker pressure and governance cost.

4. **Option C sacrifices the core architectural insight.** The Phase 2 analysis identified "temporal discipline (before/during/after as first-class concepts)" as the most important systemic pattern. Distributing nuclear patterns across existing skills destroys this temporal coherence.

5. **Option A scores highest numerically but omits a valuable verification pattern.** The weighted score favors Option A (8.10 vs. 7.60), but omitting context-isolated verification from a skill named "nuclear SOP" would underdeliver on the skill's value proposition. The 0.50-point score difference is outweighed by the quality improvement that context isolation provides for C3+ work.

### Why Not the Highest Score?

Option A scores 8.10 vs. Option D's 7.60. The 0.50 gap comes from Option D's higher complexity (7 vs. 9) and lower compliance score (8 vs. 9). However:

- The complexity difference (2 points, weighted at 0.15 = 0.30) reflects the additional agent, which is justified by the verification quality improvement.
- The compliance difference (1 point, weighted at 0.20 = 0.20) reflects circuit breaker ambiguity, which is addressed by the dual-mode design in the H-36 Compliance section.

The analyst override selects Option D because context-isolated verification provides genuine quality improvement for the C3+ work that this skill targets, and the H-36 ambiguity is manageable through the dual-mode design.

---

## Architecture Specification

### Skill Definition (SKILL.md)

**Skill name:** `nuclear-sop`
**Folder:** `skills/nuclear-sop/`
**Version:** 1.0.0
**Activation keywords:** nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow

**When to use:** Invoke when a workflow requires nuclear-inspired procedural rigor: mandatory pre-job context loading, step-by-step place-keeping with STAR self-checking, named hold points requiring explicit release, context-isolated verification of work products, and post-job operating experience capture.

**When NOT to use:** C1 routine tasks (disproportionate overhead), pure research tasks (no procedure to follow), tasks without a defined procedure or workflow definition file (unless you want sop-brief to generate one from natural language).

### Agent Specifications

#### sop-brief (Pre-Job Briefing Agent)

| Property | Value |
|----------|-------|
| **Name** | `sop-brief` |
| **Role** | Pre-job briefing: context loading, prerequisite verification, OE review, error trap identification; workflow definition generation from natural language |
| **Cognitive Mode** | systematic |
| **Tool Tier** | T2 (Read, Write, Edit, Glob, Grep, Bash) |
| **Model** | sonnet |
| **Patterns Implemented** | F-2a (Pre-Job Brief), D-1 (Prerequisite Check), H-2 (OE Review), A-3 sections 1-6 |

**Input:** Workflow definition file OR natural language description of the task, project context (PLAN.md, WORKTRACKER.md), OE history (docs/experience/)
**Output:** `brief/pre-job-brief.md` containing: scope confirmation, prerequisite checklist (pass/fail), OE findings relevant to this workflow type, identified error traps, authority levels for each hold point, selected human performance tools. Optionally: `brief/draft-workflow-definition.md` if generating from natural language.

**Methodology:**
0. **(R5: Workflow Definition Generation)** If no workflow definition file is provided: generate a draft workflow definition from the user's natural language description of the task. Use the 11-section template (sections 1-9). Populate sections 1-6 from the description. Generate step outlines for section 8 with default annotations (`[CONTINUOUS]` for C3+, `[REFERENCE]` for C1-C2). Generate acceptance criteria for section 9 from the user's stated goals. Write draft to `brief/draft-workflow-definition.md`. Present draft to user via AskUserQuestion and request confirmation, revision, or rejection before proceeding. If user confirms: use the draft as the workflow definition for subsequent steps. If user rejects: halt (P-020).
1. Read and parse the workflow definition (sections 1-6: Metadata, Purpose, References, Prerequisites, Initial Conditions, Limitations).
2. Verify all prerequisites are met. If any prerequisite fails: STOP. Report failure to user (P-020).
3. Validate acceptance criteria quality (section 9). Each criterion must be verifiable -- either quantitative (numeric threshold) or qualitative (defined pass conditions). If criteria are vague or missing: issue a WARNING in the pre-job brief. If no acceptance criteria exist for any step: STOP. Report failure to user (P-020). Workflow definitions without acceptance criteria cannot support meaningful verification.
4. Search docs/experience/ for OE entries related to this workflow type. Filter by `workflow_type` field first (exact match), then by keyword search for broader relevance. If >10 OE entries exist for this workflow type without a synthesis entry, include a WARNING: "OE synthesis overdue for this workflow type."
5. If OE entries found: extract relevant error traps and lessons learned. If none: note "no prior OE for this workflow type."
6. Produce pre-job brief artifact with all findings.

#### sop-executor (Procedure Execution Agent)

| Property | Value |
|----------|-------|
| **Name** | `sop-executor` |
| **Role** | Step-by-step procedure execution with STAR self-checking, place-keeping, hold points, persistent execution state |
| **Cognitive Mode** | systematic |
| **Tool Tier** | T2 (Read, Write, Edit, Glob, Grep, Bash -- Bash scoped to test/build commands per methodology CAUTION) |
| **Model** | opus |
| **Patterns Implemented** | B-1 (STAR), A-5 (Place-Keeping), A-2 (Use Classification), A-4 (WARNING/CAUTION/NOTE), D-2 (Stop-Work), C-3 (Hold Points) |

**Input:** Pre-job brief, workflow definition (section 8: Steps), target artifacts, PROCEDURE_STATE.yaml (if resuming from hold)
**Output:** Primary work products, execution log with step-level STAR records, hold point activations, PROCEDURE_STATE.yaml (updated after each step)

**Methodology:**
1. Check for existing PROCEDURE_STATE.yaml. **If resuming from hold:** read PROCEDURE_STATE.yaml to identify last completed step. Verify consistency between PROCEDURE_STATE.yaml and execution log file. Resume from the next uncompleted step. **If starting fresh:** initialize PROCEDURE_STATE.yaml with workflow metadata and step count.
2. Load pre-job brief. Load workflow definition Steps section.
3. For each step in sequence (starting from resume point if applicable):
   a. Read step annotation: `[CONTINUOUS]`, `[REFERENCE]`, or `[INFORMATION]`.
   b. Read any WARNING/CAUTION/NOTE before the step.
   c. If step has hold point annotation (`[USER-HOLD]`, `[QG-HOLD]`, `[IV-HOLD]`): prepare for hold.
   d. Apply STAR protocol (Stop-Think-Act-Review) before each state-modifying tool call.
   e. For `[CONTINUOUS]` steps: execute exactly as written. No deviation.
   f. For `[REFERENCE]` steps: consult step guidance, exercise judgment on execution approach.
   g. CAUTION: Bash tool use requires STAR with WARNING-level scrutiny. Bash commands that modify state outside the target artifact scope require `[USER-HOLD]` annotation in the workflow definition. Only use Bash for: running test suites (`uv run pytest`), linting/formatting (`uv run ruff`), and project-specific build commands specified in workflow steps.
   h. After action: review outcome against acceptance criteria.
   i. If outcome does not match: invoke Stop-Work (D-2). Log deviation. Escalate.
   j. Sign off step in execution log. Advance place-keeper.
   k. Update PROCEDURE_STATE.yaml: mark step as completed, record timestamp, record outcome.
4. At hold points: activate appropriate hold behavior (see Hold Point Implementation Specification).
5. After all steps complete: mark PROCEDURE_STATE.yaml as `status: COMPLETED`. Produce execution log with full STAR records. Mark execution log as `FINAL`.

**Critical constraint:** The executor MUST NOT invoke `sop-verifier`. The main context (orchestrator) invokes the verifier. This preserves P-003 compliance and verification independence.

#### sop-verifier (Context-Isolated Verification Agent)

| Property | Value |
|----------|-------|
| **Name** | `sop-verifier` |
| **Role** | Context-isolated verification of executor output; fresh context, no executor reasoning |
| **Cognitive Mode** | convergent |
| **Tool Tier** | T1 (Read, Glob, Grep) -- read-only by design |
| **Model** | sonnet |
| **Patterns Implemented** | C-2 (Independent Verification -- approximated via context isolation; see Fidelity Transparency), C-3 (QC Hold Point -- IV-HOLD) |

**Input:** Work product file paths ONLY (no executor reasoning, no execution log, no STAR records). Workflow definition (acceptance criteria section). This implements FC-M-001 deliberately: the verifier receives only the artifact and the criteria, not the creator's reasoning process.
**Output:** `verification/iv-report.md` containing: pass/fail per acceptance criterion, findings, disposition (ACCEPT / REJECT / ACCEPT-WITH-CONDITIONS).

**Methodology:**
1. Read acceptance criteria from workflow definition (section 9).
2. Read each work product artifact.
3. Evaluate each acceptance criterion independently.
4. For each criterion: document evidence for pass or fail.
5. Produce IV report with overall disposition.
6. If REJECT: list specific findings requiring revision with enough detail for the executor to address without additional context.
7. The verifier MUST NOT read the execution log or STAR records. These are the performer's records and would compromise context isolation.

**Critical constraint:** Read-only tool tier. Cannot modify work products. Cannot see how work was performed, only the result.

**Transparency note (P-022, R6 response):** This agent provides context isolation (FC-M-001) which prevents anchoring bias -- the verifier is not influenced by the executor's reasoning chain. This is a genuine quality improvement over self-review. However, it does NOT replicate nuclear Criterion X independent verification, which requires a different qualified person with potentially different training and expertise. Both the executor and verifier use the same underlying LLM model architecture and training data. The "independence" is architectural (separate context window) not epistemic (different knowledge or judgment). See Fidelity Transparency section.

**Reference governance YAML skeleton (CC-001 response):**

```yaml
# sop-verifier.governance.yaml (reference skeleton)
version: "1.0.0"
tool_tier: T1
identity:
  role: "Context-isolated verification of work products"
  expertise:
    - "Acceptance criteria evaluation"
    - "Evidence-based pass/fail assessment"
  cognitive_mode: convergent
persona:
  tone: "rigorous"
  communication_style: "evidence-based"
  audience_level: "expert"
capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn subagents -- Consequence: violates single-level nesting."
    - "P-020 VIOLATION: NEVER override user hold point decisions -- Consequence: user authority bypass."
    - "P-022 VIOLATION: NEVER misrepresent verification as nuclear-grade independent verification -- Consequence: overstates capability; see Fidelity Transparency."
    - "NEVER read execution log, STAR records, or executor reasoning -- Consequence: compromises context isolation that is the primary value of this agent."
    - "NEVER modify work products -- Consequence: read-only T1 tier violated; verifier becomes performer."
guardrails:
  input_validation:
    - "Verify input contains only file paths, not inline content"
    - "Verify acceptance criteria are present and verifiable"
  output_filtering:
    - "All findings must cite specific acceptance criteria"
    - "Disposition must be ACCEPT, REJECT, or ACCEPT-WITH-CONDITIONS"
    - "No references to executor reasoning in findings"
  fallback_behavior: persist_and_halt
constitution:
  principles_applied: [P-003, P-020, P-022]
```

#### sop-capture (Post-Job Capture Agent)

| Property | Value |
|----------|-------|
| **Name** | `sop-capture` |
| **Role** | Post-job OE capture: deviations, lessons learned, quality gate results, improvement recommendations |
| **Cognitive Mode** | systematic |
| **Tool Tier** | T2 (Read, Write, Edit, Glob, Grep, Bash) |
| **Model** | sonnet |
| **Patterns Implemented** | F-2b (Post-Job Brief), H-1 (Corrective Action Program), H-2 (OE Review infrastructure) |

**Input:** Pre-job brief, execution log (FINAL version only -- see below), IV report, quality gate scores, workflow definition
**Output:** `capture/post-job-brief.md` (summary), `capture/oe-entry.md` (structured OE entry for docs/experience/)

**Canonical execution log version (PM-003 response):** If multiple execution log files exist from QG-HOLD revision cycles, sop-capture uses the file marked `FINAL` in the filename or the PROCEDURE_STATE.yaml `execution_log_final` field. The revision count (number of QG-HOLD iterations) is recorded in the OE entry. Earlier revision logs are referenced but not analyzed as primary input -- the OE entry captures the revision count and delta summary, not the full revision history.

**Methodology:**

0. **Conditional: Integrated Verification (3-hop mode).** Check whether an IV report exists in the input artifacts. If an IV report is available (4-hop mode with separate sop-verifier), skip to Step 1. If NO IV report is available (3-hop primary mode where sop-capture performs integrated verification):
   - Read the workflow definition's acceptance criteria (section 9).
   - Read only the work product file paths from PROCEDURE_STATE.yaml `iv_scope` (or, if iv_scope is empty, all work products listed in the execution log).
   - Evaluate each work product against the acceptance criteria. Produce a disposition: ACCEPT, REJECT, or ACCEPT-WITH-CONDITIONS.
   - If REJECT: halt and return findings to the main context for sop-executor revision (same protocol as IV-HOLD rejection).
   - If ACCEPT or ACCEPT-WITH-CONDITIONS: record the verification result and proceed to Step 1. Record conditions (if any) for inclusion in the OE entry.
   - **Anchoring bias disclaimer (P-022):** In 3-hop mode, sop-capture has access to the execution log before performing verification. This means the verification is NOT context-isolated -- the agent has seen the executor's reasoning and may be anchored to it. This trade-off is documented in the H-36 Compliance section. The 3-hop mode sacrifices verification independence for unambiguous H-36 compliance. For C3+ deliverables where verification independence is critical, the enhanced 4-hop mode with separate sop-verifier is preferred (pending governance ruling).

1. Read PROCEDURE_STATE.yaml to identify the FINAL execution log path.
2. Read all input artifacts (pre-job brief, FINAL execution log, IV report (if available from 4-hop mode or Step 0 integrated verification result), quality gate scores).
3. Compare execution to plan: identify deviations, stop-work events, hold point failures.
4. Document what worked well, what did not, and why.
5. Extract quality gate scores from IV report and any QG-HOLD iterations.
6. Formulate improvement recommendations for the workflow definition.
7. Produce structured OE entry following the standard schema:

```yaml
# OE Entry Schema
oe_entry:
  date: "YYYY-MM-DD"
  workflow_type: "{workflow type from metadata section}"  # PM-005: enables exact-match filtering
  workflow_id: "{workflow ID from metadata section}"
  outcome: "COMPLETED | COMPLETED-WITH-DEVIATIONS | ABORTED"
  criticality: "C1 | C2 | C3 | C4"
  qg_hold_iterations: 0          # Number of QG-HOLD revision cycles
  iv_hold_iterations: 0          # Number of IV-HOLD revision cycles
  user_hold_count: 0             # Number of USER-HOLD activations
  deviations: []                 # List of deviations from procedure
  stop_work_events: []           # List of D-2 stop-work events
  lessons_learned: []            # Key insights
  recommendations: []            # Proposed workflow definition changes
  synthesis_status: "pending"    # Set to "synthesized" after ps-synthesizer review
```

8. Write OE entry to both the workflow-local capture directory and `docs/experience/` for cross-workflow searchability.

### Quality Gate Mapping

| Nuclear Verification Concept | Jerry Quality Mechanism | `/nuclear-sop` Implementation |
|------------------------------|------------------------|-------------------------------|
| QC Hold Point (Appendix B Criterion X) | H-13 quality threshold + H-14 creator-critic cycle | QG-HOLD: automated quality gate at phase boundaries |
| Independent Verification (Appendix B Criterion X) | FC-M-001 (fresh context review) | IV-HOLD: sop-verifier invoked via Task with fresh context; read-only; no executor reasoning. **Approximation -- not equivalent to nuclear IV.** |
| Mandatory Witness (regulatory hold point) | P-020 (user authority) | USER-HOLD: work stops until user explicitly approves |
| Self-Checking (STAR) | S-010 (Self-Refine) -- different mechanism | STAR protocol: pre-action checkpoint at every state-modifying tool call; distinct from S-010 post-action review |
| Acceptance Criteria (Appendix B Criterion V) | Scoring dimensions (S-014) | Acceptance criteria in workflow definition section 9; evaluated by sop-verifier |
| Post-Maintenance Testing | Regression testing, integration verification | Verification steps in workflow definition after main execution |

---

## H-36 Circuit Breaker Compliance

### Rule Text Analysis (R1/R3 response)

The H-36 rule text (from `agent-routing-standards.md`) states:

> "No request SHALL be routed more than 3 hops without reaching a terminal agent that produces output. **A hop is one transition between skills or agents where routing logic re-evaluates the destination.**"

The "What Counts as a Hop" table specifies:

| Counts as a hop | Does NOT count as a hop |
|-----------------|------------------------|
| Skill-to-skill transition | Creator-critic-revision iterations (H-14 loops) |
| **Agent-to-agent transition within a skill** | Explicit user-initiated redirections |
| Re-routing due to agent inability | **Quality gate retry within same agent** |

### Transition-by-Transition Analysis

The `/nuclear-sop` workflow involves 4 transitions from the main context to agents. All are orchestrated by the main context (star topology per P-003), not chained agent-to-agent.

| # | From | To | Routing Logic Re-evaluates? | H-36 Classification | Rationale |
|---|------|-----|----------------------------|---------------------|-----------|
| 1 | Main context | sop-brief | Yes -- routing selects /nuclear-sop skill | **HOP** | This is the skill-to-agent entry point. Routing logic matched keywords and selected the skill. |
| 2 | Main context | sop-executor | No -- predetermined sequence | **Ambiguous** | The main context does not re-evaluate which agent to invoke next. The sequence brief->executor is fixed by the skill definition. However, the "Agent-to-agent transition within a skill" row in the hop table says this counts. |
| 3 | Main context | sop-verifier | No -- predetermined quality gate | **Ambiguous** | The verifier is invoked as a verification step, not a routing decision. The closest analog in the hop table is "Quality gate retry within same agent" (does NOT count), but sop-verifier is a *different* agent. The quality gate precedent suggests this should not count, but the letter of the rule ("agent-to-agent transition within a skill") suggests it does. |
| 4 | Main context | sop-capture | No -- predetermined sequence | **Ambiguous** | Same analysis as transition 2. |

### The Ambiguity

H-36's hop definition contains an internal tension:

- The *definition* says "where routing logic re-evaluates the destination" -- suggesting predetermined sequences where the destination is fixed should NOT count.
- The *table* says "Agent-to-agent transition within a skill" counts -- suggesting all intra-skill agent transitions DO count regardless of routing re-evaluation.

The creator-critic-revision exemption provides a relevant precedent: the main context invokes the creator, then the critic, then the creator again -- this is an "agent-to-agent transition within a skill" but is explicitly exempted. The exemption logic is that the sequence is a predetermined quality pattern, not a routing decision.

The nuclear-sop 4-agent sequence is analogously a predetermined quality pattern (brief->execute->verify->capture), not a routing decision tree. However, unlike creator-critic-revision (which iterates within a bounded loop on the same deliverable), nuclear-sop transitions between distinct phases with different inputs and outputs.

### Dual-Mode Design (Resolution)

Rather than rely on an ambiguous interpretation, this ADR provides two compliant operating modes:

**Primary Mode: 3-Hop Design (Unambiguously Compliant)**

In the primary mode, sop-verifier's verification logic is integrated into the sop-capture phase. sop-capture receives the work products, acceptance criteria, AND the execution log, and performs both verification and OE capture in a single agent invocation.

| # | From | To | Hop? |
|---|------|-----|------|
| 1 | Main context | sop-brief | Yes |
| 2 | Main context | sop-executor | Yes |
| 3 | Main context | sop-capture (with integrated IV) | Yes |

**Trade-off:** This sacrifices FC-M-001 context isolation for verification. sop-capture would see the execution log before evaluating work products, introducing anchoring bias. The verification portion of sop-capture is not truly independent. However, this mode is unambiguously H-36 compliant.

**Enhanced Mode: 4-Hop Design (Requires Governance Clarification)**

In the enhanced mode, sop-verifier runs as a separate agent with full FC-M-001 context isolation:

| # | From | To | Hop? |
|---|------|-----|------|
| 1 | Main context | sop-brief | Yes |
| 2 | Main context | sop-executor | Yes |
| 3 | Main context | sop-verifier | Claimed: No (quality gate). Strict: Yes. |
| 4 | Main context | sop-capture | Yes (if transition 3 is No) or exceeds limit (if transition 3 is Yes) |

**Governance request:** Before implementing the enhanced mode, a governance ruling should be sought on whether a predetermined intra-skill verification step (not involving routing re-evaluation) constitutes a "hop" under H-36. This ruling would have framework-wide implications for any future skill with 4+ agents.

**Implementation recommendation:** Implement sop-capture with BOTH capabilities: (a) standalone OE capture (3-hop mode -- default), and (b) standalone OE capture receiving IV report from separate sop-verifier (4-hop mode -- activated when governance ruling permits). The agent definition for sop-capture should accept IV report as an optional input. If absent, sop-capture performs integrated verification before capture.

---

## Hold Point Implementation Specification

### R4 Response: Full Implementation Detail

#### USER-HOLD Implementation

**Trigger:** Step annotated with `[USER-HOLD]` in workflow definition.

**Pause sequence:**
1. sop-executor completes all steps before the `[USER-HOLD]` step.
2. sop-executor writes current state to PROCEDURE_STATE.yaml:
   - `status: HELD`
   - `hold_type: USER-HOLD`
   - `held_at_step: {step number}`
   - `held_at_timestamp: {ISO-8601}`
   - `hold_prompt: "{description of what the user is being asked to approve}"`
3. sop-executor writes a hold point entry to HOLD_POINT_LOG.md.
4. sop-executor presents the hold to the user: displays the step description, the hold prompt, and asks for explicit approval. This uses the standard Claude Code conversational interface -- the executor's output text includes the hold point information and the main context presents it to the user.

**Resume sequence:**
1. User responds with approval, rejection, or guidance.
2. If **approved:** Main context re-invokes sop-executor with PROCEDURE_STATE.yaml. Executor reads state, confirms `status: HELD` at the expected step, changes status to `RESUMING`, and continues from the held step.
3. If **rejected:** Executor logs rejection in HOLD_POINT_LOG.md. Executor captures user guidance. Executor re-enters STAR for the affected step with user's guidance as additional context. Updates PROCEDURE_STATE.yaml.
4. If **session boundary crossed** (user responds in a different session): See Procedure State Persistence section.

**What the user sees:** The sop-executor's output includes a clearly formatted hold point notification:

```
=== USER-HOLD POINT ===
Step: {number} - {title}
Description: {step description from workflow definition}
Hold Reason: {hold prompt from workflow definition}
Preceding Step Result: {summary of last completed step}

Please respond with:
- APPROVE to proceed with this step
- REJECT to stop and provide alternative guidance
- WAIVE to skip this hold point (P-020: your authority)
========================
```

#### QG-HOLD Implementation

**Trigger:** Automated quality gate at phase boundaries (typically between sop-executor completion and sop-verifier/sop-capture invocation).

**Critic identity:** QG-HOLD invokes the standard Jerry quality gate: `ps-critic` from `/problem-solving` (or `/adversary` adv-scorer for S-014 scoring). The threshold is H-13 (>= 0.92 for C2+ deliverables). The scoring rubric is the 6-dimension S-014 rubric from quality-enforcement.md (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability).

**Execution protocol:**
1. sop-executor completes all steps and produces work products.
2. Main context invokes quality gate evaluation: ps-critic (or adv-scorer) evaluates work products against acceptance criteria using S-014 rubric.
3. If score >= threshold: QG-HOLD auto-releases. Proceed to next phase.
4. If score < threshold: Revision cycle per H-14 (min 3 iterations, max per RT-M-010 ceilings). Main context re-invokes sop-executor with critic findings. Executor resumes from the failed step(s) identified by critic.
5. After each revision: re-evaluate with critic. Repeat until threshold met or iteration ceiling reached.
6. If iteration ceiling reached without passing: mandatory user escalation (P-020). Present best result and critic findings.

**State management:** Each QG-HOLD iteration produces a new execution log revision. PROCEDURE_STATE.yaml tracks the revision count. The FINAL execution log is the one that passes the quality gate (or the best result presented to the user at escalation). All prior revisions are preserved with revision numbers but only the FINAL is used by sop-capture.

#### IV-HOLD Implementation

**Trigger:** Steps annotated with `[IV-HOLD]` in workflow definition, or the phase boundary between execution and capture (when enhanced 4-hop mode is active).

**Coordination protocol:**
1. sop-executor completes the work covered by the IV-HOLD scope.
2. sop-executor writes state to PROCEDURE_STATE.yaml:
   - `status: IV-PENDING`
   - `iv_scope: [list of work product file paths]`
   - `iv_criteria_path: "{path to acceptance criteria section}"`
3. sop-executor's output signals to the main context that IV is required. The main context reads PROCEDURE_STATE.yaml.
4. Main context invokes sop-verifier via Task tool with ONLY:
   - Work product file paths from `iv_scope`
   - Workflow definition path (for acceptance criteria, section 9)
   - **Deliberately excluded:** execution log, STAR records, pre-job brief, PROCEDURE_STATE.yaml (except for file paths listed in iv_scope)
5. sop-verifier produces `verification/iv-report.md` with disposition.
6. Main context reads IV report.
7. If **ACCEPT:** Main context updates PROCEDURE_STATE.yaml (`status: IV-PASSED`). Proceeds to next phase.
8. If **REJECT:** Main context passes verifier findings (specific revision requirements) back to sop-executor. Executor receives findings as input, revises affected work products, and re-submits. Fresh sop-verifier invocation (new Task, new context). After 3 rejections: mandatory user escalation (P-020).
9. If **ACCEPT-WITH-CONDITIONS:** Main context records conditions in HOLD_POINT_LOG.md. Proceeds with conditions noted. sop-capture includes conditions in OE entry.

---

## Procedure State Persistence

### R2 Response: PROCEDURE_STATE.yaml Specification

The PROCEDURE_STATE.yaml file provides execution state persistence for pause/resume across hold points and session boundaries.

**Location:** Written to the workflow execution directory alongside the execution log.

**Schema:**

```yaml
# PROCEDURE_STATE.yaml
procedure_state:
  # --- Workflow Identity ---
  workflow_id: "{from workflow definition metadata}"
  workflow_version: "{from workflow definition metadata}"
  workflow_definition_path: "{path to workflow definition file}"

  # --- Execution Status ---
  status: "IN-PROGRESS"
  # Valid values: INITIALIZING | IN-PROGRESS | HELD | RESUMING |
  #               IV-PENDING | IV-PASSED | IV-REJECTED |
  #               COMPLETED | ABORTED

  # --- Place-Keeping ---
  total_steps: 0
  current_step: 0                 # Last completed step number (0 = not started)
  next_step: 1                    # Next step to execute
  steps_completed: []             # List of completed step numbers with timestamps
    # - step: 1
    #   completed_at: "2026-03-23T14:30:00Z"
    #   outcome: "PASS"           # PASS | DEVIATION | STOP-WORK
    #   star_record_path: "execution-log.md#step-1"

  # --- Hold Point State ---
  hold_type: null                 # USER-HOLD | QG-HOLD | IV-HOLD | null
  held_at_step: null
  held_at_timestamp: null
  hold_prompt: null               # Description of what is being held for
  hold_resolution: null           # APPROVED | REJECTED | WAIVED | null

  # --- IV State ---
  iv_scope: []                    # File paths of work products under IV
  iv_criteria_path: null          # Path to acceptance criteria
  iv_iteration: 0                 # Current IV attempt (max 3)
  iv_report_path: null            # Path to most recent IV report

  # --- QG State ---
  qg_iteration: 0                # Current QG-HOLD revision count
  qg_scores: []                  # Score per iteration
    # - iteration: 1
    #   score: 0.85
    #   critic_findings_path: "qg-findings-001.md"

  # --- Execution Log ---
  execution_log_path: "execution-log.md"
  execution_log_revision: 1       # Incremented on QG-HOLD revision
  execution_log_final: null       # Set to path when FINAL version produced

  # --- Timestamps ---
  started_at: "2026-03-23T14:00:00Z"
  last_updated: "2026-03-23T14:30:00Z"
  completed_at: null
```

### Resume Protocol

When sop-executor is invoked with an existing PROCEDURE_STATE.yaml (indicating a resume):

1. **Read PROCEDURE_STATE.yaml.** Verify `status` is `HELD` or `RESUMING` or `IV-REJECTED`.
2. **Read execution log** at `execution_log_path`. Verify step count in execution log matches `current_step` in PROCEDURE_STATE.yaml. If mismatch: STOP WORK. Report inconsistency to user.
3. **Reconstruct position.** Set place-keeper to `next_step`. Load any hold resolution context (user guidance for USER-HOLD, verifier findings for IV-REJECTED, critic findings for QG-HOLD).
4. **Update status** to `IN-PROGRESS` (or `RESUMING` for the first step after hold).
5. **Continue execution** from `next_step` using standard STAR protocol.

### Cross-Session Resume

If a hold point spans a session boundary (context compaction or new session):

1. PROCEDURE_STATE.yaml persists on the filesystem independent of session state.
2. The new session's main context reads PROCEDURE_STATE.yaml and understands the workflow state.
3. The main context re-invokes sop-executor with the PROCEDURE_STATE.yaml path. The executor reconstructs its position entirely from filesystem state -- it does not depend on any in-context memory from the prior session.
4. **AE-006 compaction resilience:** PROCEDURE_STATE.yaml is the authoritative state record. Even if the entire context window is compacted, the filesystem state is sufficient to resume. The execution log provides the detailed record; PROCEDURE_STATE.yaml provides the index.

### Resume Discovery (R8 -- NC-002 response)

When a user returns to a project in a fresh session after a hold point fired (e.g., USER-HOLD requiring approval, or IV-HOLD awaiting verifier results), the orchestrator must discover the paused workflow. The discovery mechanism operates as follows:

1. **At session start:** The orchestrator (main context) checks the active project's workflow execution directories for PROCEDURE_STATE.yaml files with non-terminal status. Terminal statuses are `COMPLETED` and `ABORTED`; all others (`HELD`, `IV-PENDING`, `IV-REJECTED`, `IN-PROGRESS`, `RESUMING`, `INITIALIZING`) indicate an in-progress workflow that may need resumption.
2. **Discovery path:** The orchestrator scans `projects/{JERRY_PROJECT}/**/PROCEDURE_STATE.yaml` using Glob. For each file found, it reads the `status` field. If any file has a non-terminal status, the orchestrator presents the paused workflow to the user with: workflow ID, held-at step, hold type, and hold prompt.
3. **User decision (P-020):** The user chooses to resume, abandon, or defer the paused workflow. This preserves user authority -- the orchestrator never auto-resumes without explicit user intent.
4. **Relationship to ORCHESTRATION.yaml:** For nuclear-sop workflows running within an `/orchestration` pipeline, the ORCHESTRATION.yaml `resumption_context` field references the PROCEDURE_STATE.yaml path. The orchestration resume protocol (orch-tracker) discovers the orchestration state; the nuclear-sop resume protocol discovers the procedure state within it. Both mechanisms are filesystem-based and session-independent.
5. **Explicit invocation alternative:** Users may also explicitly resume by providing the PROCEDURE_STATE.yaml path: "Resume the nuclear workflow at `{path-to-PROCEDURE_STATE.yaml}`". This bypasses the scan and directly loads the workflow state.

---

## Nuclear Pattern Mapping

### Pattern-to-Agent Assignment

| Pattern ID | Pattern Name | Implementing Agent | Implementation Mechanism |
|-----------|-------------|-------------------|-------------------------|
| A-2 | Procedure Use Classification | sop-executor | Step annotations: `[CONTINUOUS]`, `[REFERENCE]`, `[INFORMATION]` |
| A-3 | Standard Procedure Structure | Workflow definition template | 11-section template mapped from nuclear structure |
| A-4 | WARNING/CAUTION/NOTE Pre-Placement | sop-executor | Inline annotations in workflow definition before steps |
| A-5 | Place-Keeping / Step Sign-Off | sop-executor | Execution log with step-level tracking and sign-off, PROCEDURE_STATE.yaml |
| B-1 | STAR Self-Checking | sop-executor | Pre-action protocol before each state-modifying tool call |
| C-2 | Independent Verification | sop-verifier | Context-isolated verification via FC-M-001 (**approximation** -- see Fidelity Transparency) |
| C-3 | QC Hold Point | sop-executor + sop-verifier | Three hold point types: USER-HOLD, QG-HOLD, IV-HOLD |
| D-1 | Prerequisite / Initial Condition Check | sop-brief | Prerequisite checklist in pre-job brief |
| D-2 | Stop-Work Authority | sop-executor | STAR Review step: if outcome deviates, invoke stop-work |
| E-2 | Conservative Decision-Making | sop-executor + sop-brief | STAR Think phase: when uncertain, take conservative action |
| F-2a | Pre-Job Briefing | sop-brief | Full pre-job brief artifact |
| F-2b | Post-Job Briefing / OE Capture | sop-capture | Post-job brief + structured OE entry |
| H-1 | Corrective Action Program | sop-capture | OE entries written to docs/experience/ with workflow_type field |
| H-2 | Operating Experience Review | sop-brief | Search docs/experience/ by workflow_type then keywords during briefing |
| I-1 | Operations Turnover | Existing handoff schema | Validated as Strong fit; no new implementation |

### Patterns NOT Implemented (with Rationale)

| Pattern ID | Pattern Name | Reason Not Implemented |
|-----------|-------------|----------------------|
| A-1 | Procedure Type Hierarchy | Deferred. Workflow types (NOMINAL/ABNORMAL/EMERGENCY) add value but are lower priority than core brief/execute/verify/capture. Phase 2 implementation. |
| B-2 | Questioning Attitude | Embedded conceptually in STAR Think phase. Not a discrete agent or step. Behavioral transfer uncertain. |
| C-1 | Peer Checking (Concurrent) | Architecturally impossible (GAP-05). Accept as inherent limitation. |
| E-1 | Decision Authority Hierarchy | Deferred. AE rules + criticality levels (C1-C4) partially cover this. Extension after Tier 2 patterns. |
| F-1 | Three-Part Communication | Deferred. Handoff schema already implements concept. Echo-confirmation extension is a handoff schema enhancement, not a new pattern. |
| G-1 | Symptom-Based Emergency Framework | Deferred to Phase 4 (see Implementation Roadmap). High implementation complexity. |

---

## Fidelity Transparency

This section documents what the `/nuclear-sop` skill preserves, approximates, and cannot implement from nuclear SOP practices, per P-022 (no deception about capabilities).

### Preserved with High Fidelity

These patterns are directly implemented with mechanisms that closely parallel their nuclear analogs:

- Pre-job briefing structure and content (F-2a) -- directly implemented as sop-brief agent
- Post-job OE capture (F-2b) -- directly implemented as sop-capture agent
- Place-keeping and step sign-off (A-5) -- execution log + PROCEDURE_STATE.yaml with step-level tracking
- Standard procedure structure (A-3) -- 11-section workflow definition template
- Hold points as blocking gates (C-3, D-1) -- three hold point types with full implementation spec
- Stop-work authority (D-2) -- STAR Review step triggers stop-work on deviation
- WARNING/CAUTION/NOTE pre-placement (A-4) -- inline in workflow definition before steps
- Conservative decision-making (E-2) -- embedded in STAR Think phase and hold point escalation

### Approximated (Not Equivalent)

These patterns are inspired by nuclear practices but adapted for the AI agent context. The adaptation introduces limitations that differ from the nuclear original. **Per P-022, these limitations are documented honestly.**

- **Independent verification by non-performer (C-2)** -- sop-verifier provides **context isolation** via FC-M-001 (fresh context window, no access to executor reasoning). This prevents **anchoring bias**: the verifier evaluates work products without being influenced by the executor's reasoning chain. This is a genuine quality improvement over self-review (S-010). **However, this is NOT equivalent to nuclear Criterion X independent verification.** Nuclear IV requires a different qualified person -- someone with potentially different training, different knowledge, and different cognitive biases. sop-verifier and sop-executor use the same underlying LLM model architecture and training data. The "independence" is **architectural** (separate context window) not **epistemic** (different knowledge or judgment). The verifier may reach the same conclusions the executor would reach on a second pass, because both share the same model. What is preserved: bias reduction through context isolation. What is NOT preserved: genuine diversity of perspective that comes from a different human inspector. **(R6 revision: moved from "Preserved" to "Approximated" per DA-001.)**

- STAR self-checking (B-1) -- implemented as a structured pre-action protocol in prompt text, but cannot replicate the physical "touch the component while reading the label" verification of nuclear plant operations. The AI analog (verify file path, verify step number, verify expected outcome) is a reasonable approximation. Both STAR reasoning and the tool call are generated in the same LLM inference pass; the temporal separation is a structural constraint in the prompt, not a physical interruption.

- Procedure use classification (A-2) -- annotation system preserves the taxonomy, but the behavioral distinction between CONTINUOUS and REFERENCE relies on prompt compliance rather than physical procedure-in-hand enforcement.

- Operating experience review (H-2) -- sop-brief searches docs/experience/ for prior OE entries using workflow_type matching and keyword search, but lacks the industry-wide OE sharing network (INPO, IAEA, NRC generic communications) that nuclear plants access. OE is local to the repository, not shared across teams or organizations.

### Not Implemented (Acknowledged Limitations)

These patterns cannot be implemented in an AI agent framework. This is an inherent limitation of the medium, not a design choice:

- Concurrent peer checking (C-1/GAP-05) -- architecturally impossible in sequential AI execution
- Real-time task observation/coaching -- no equivalent to supervisory presence during work
- Regulatory audit program (GAP-08) -- no external scheduling infrastructure
- Operator requalification -- no equivalent for AI model version changes
- Questioning Attitude as dispositional trait (B-2) -- embedded conceptually in STAR Think phase but cannot be verified as a behavioral property of an LLM

---

## Consequences

### Positive

1. **Nuclear-inspired temporal discipline.** Pre/post-job phases become first-class workflow elements with their own agents, outputs, and quality gates. This is the most significant structural improvement: Jerry workflows gain the before/during/after rigor that nuclear plants have proven effective over 50 years.

2. **Context-isolated verification with architectural separation.** The sop-verifier agent, invoked with fresh context and read-only access, provides genuine anchoring-bias prevention that self-review (S-010) and in-context critic review cannot achieve. While this approximates rather than replicates nuclear IV (see Fidelity Transparency), the context isolation is a real quality improvement for C3+ deliverables.

3. **Mandatory OE feedback loop.** Every workflow execution produces a structured OE entry with workflow_type classification. Over time, these entries create a searchable knowledge base of what works, what fails, and what to watch for. This is currently absent from Jerry.

4. **Step-level compliance granularity.** The CONTINUOUS/REFERENCE/INFORMATION classification system enables appropriate rigor per step rather than uniform rigor per phase. This complements (not duplicates) the C1-C4 criticality levels which apply to entire deliverables.

5. **Reusable workflow definition format.** The 11-section template is skill-agnostic. Other Jerry skills could adopt it for any procedure-based work, extending nuclear discipline beyond `/nuclear-sop`.

6. **Persistent execution state.** PROCEDURE_STATE.yaml enables pause/resume across hold points and session boundaries, a capability that does not exist in other Jerry skills.

### Negative

1. **Context budget pressure.** Four Task invocations consume approximately 12,000-32,000 tokens in agent definition loading alone (3,000-8,000 per agent). For a 200K context window, this is 6-16% of the budget on overhead before any work begins. Workflows with many steps will face context pressure.

2. **Execution latency.** Four sequential agent phases increase wall-clock time. The verifier phase adds 30-120 seconds depending on work product size. For workflows where speed matters more than rigor, this is a significant cost.

3. **Workflow definition upfront cost.** Users must create a structured workflow definition file before using the skill. This is partially mitigated by sop-brief's Step 0 (generate from natural language), but the generated draft still requires user review and confirmation.

4. **OE entry accumulation without synthesis.** If OE entries are not periodically reviewed and synthesized, they accumulate without producing value. The skill creates entries and warns when synthesis is overdue (>10 entries per workflow type), but does not schedule synthesis. This requires external discipline (periodic ps-synthesizer invocation) to close the feedback loop.

5. **Circuit breaker tension.** The 4-agent sequence creates an ambiguous case under H-36. The primary 3-hop mode sacrifices verification context isolation. The enhanced 4-hop mode requires a governance ruling. Either path involves a trade-off.

### Neutral

1. **No impact on existing skills.** The `/nuclear-sop` skill is additive. No existing agent definitions, rules, or templates are modified.

2. **Skill count increases to 21.** This is one above the H-37 Phase 1 threshold. Keyword-first routing remains adequate at this count, but the Phase 2 transition triggers should be evaluated.

3. **Agent count increases by 4.** Jerry's total agent population grows, but all 4 agents are within a single skill. The AGENTS.md registry gains 4 entries.

---

## Risks

| Risk ID | Risk | Severity | Occurrence | Detection | RPN | Mitigation |
|---------|------|----------|------------|-----------|-----|------------|
| R-001 | Over-engineering: nuclear rigor applied to C1 tasks creates friction without safety benefit | 7 | 6 | 5 | 210 | Default classification rules: `[CONTINUOUS]` default for C3+, `[REFERENCE]` default for C1-C2. SKILL.md explicitly states "do not use for C1 routine tasks." |
| R-002 | Context exhaustion during long workflows: multi-step procedures with full STAR consume excessive tokens | 8 | 5 | 4 | 160 | STAR logging uses compact structured format (not prose). Place-keeping state stored in PROCEDURE_STATE.yaml, not in-context memory. AE-006 graduated escalation handles context fill. |
| R-003 | OE entry accumulation without review creates false confidence that a feedback loop exists | 5 | 7 | 7 | 245 | Document in SKILL.md that OE entries require periodic synthesis. sop-brief warns when >10 OE entries exist without synthesis. workflow_type field enables targeted synthesis. |
| R-004 | Hold point fatigue: too many USER-HOLD points cause users to approve without reading | 8 | 5 | 4 | 160 | Limit USER-HOLD to C3+ steps. Default to QG-HOLD (automated) and IV-HOLD (sop-verifier) for C2 verification. |
| R-005 | sop-verifier becomes a rubber stamp due to insufficient acceptance criteria in workflow definition | 6 | 5 | 6 | 180 | sop-brief validates acceptance criteria quality in Step 3. Missing criteria for any step triggers STOP (not just WARNING). Vague criteria trigger WARNING. |
| R-006 | Naming confusion: `sop-*` prefix may conflict with future skill naming conventions | 3 | 3 | 8 | 72 | Prefix is specific to this skill. Register in AGENTS.md to prevent collision. Jerry's naming convention (H-25) uses skill-name prefix, so `sop-*` is correct for `nuclear-sop` skill. |
| R-007 | H-36 circuit breaker ambiguity: 4-agent sequence may be interpreted as 4 hops | 7 | 5 | 3 | 105 | Dual-mode design: primary 3-hop mode is unambiguously compliant; enhanced 4-hop mode requires governance ruling. Fallback always available. |
| R-008 | State loss during hold point: PROCEDURE_STATE.yaml corruption or inconsistency with execution log | 6 | 3 | 5 | 90 | Resume protocol includes consistency check (step count match). Mismatch triggers STOP WORK and user notification. |

### Pre-Mortem Analysis (S-004)

*"It is 6 months after implementing this skill and it has failed. Why?"*

**Scenario 1: Nobody uses it.** The workflow definition upfront cost is too high. Users prefer invoking `/problem-solving` or `/orchestration` directly because those skills accept natural language prompts without structured input files. **Mitigation:** sop-brief Step 0 generates draft workflow definitions from natural language. Phase 1 deliverables include one worked example workflow definition (C3 ADR procedure) to lower the barrier. Starter workflow definitions for common patterns (code review, architecture decision, deployment) reduce the cold-start problem.

**Scenario 2: STAR logging overwhelms the context.** A 50-step workflow with full STAR records on each step produces 50 x ~200 tokens = 10,000 tokens of execution log, plus the agent overhead. The context fills before capture phase runs. **Mitigation:** STAR records are written to filesystem incrementally (not accumulated in context). sop-executor writes each step's STAR record to the execution log file via Write tool, keeping only the current step's STAR in context. PROCEDURE_STATE.yaml tracks position without requiring context retention.

**Scenario 3: OE entries are never synthesized.** 6 months of post-job briefs accumulate in docs/experience/ but nobody runs the synthesis. The feedback loop is open-loop only. **Mitigation:** sop-brief checks OE entry count per workflow_type. When >10 entries exist without a synthesis entry, the pre-job brief includes a WARNING that OE synthesis is overdue. The workflow_type field enables targeted synthesis.

**Scenario 4: The sop-verifier is always pass.** Acceptance criteria in workflow definitions are too vague ("the output should be good"), so the verifier always passes. IV becomes performative. **Mitigation:** sop-brief validates acceptance criteria quality in Step 3. Criteria must be verifiable. Missing criteria trigger STOP. Vague criteria trigger WARNING. The verifier's governance YAML includes a forbidden action against accepting work products when acceptance criteria are not evaluable.

---

## Implementation Roadmap

### Phase 1: Core Skill (Target: Immediate)

**Deliverables:**
- `skills/nuclear-sop/SKILL.md`
- `sop-brief` agent definition (.md + .governance.yaml)
- `sop-executor` agent definition (.md + .governance.yaml)
- `sop-verifier` agent definition (.md + .governance.yaml)
- `sop-capture` agent definition (.md + .governance.yaml)
- `templates/WORKFLOW_DEFINITION.template.md`
- `templates/PRE_JOB_BRIEF.template.md`
- `templates/POST_JOB_BRIEF.template.md`
- `templates/HOLD_POINT_LOG.template.md`
- `templates/PROCEDURE_STATE.template.yaml`
- `examples/c3-adr-workflow-definition.md` (worked example: C3 ADR with nuclear rigor)
- `rules/nuclear-sop-behavior-rules.md`

**Registration:**
- Add `/nuclear-sop` to CLAUDE.md skill table
- Add `/nuclear-sop` to AGENTS.md
- Add trigger keywords to `mandatory-skill-usage.md` (CC-004 response)

**Governance action:**
- Seek H-36 ruling on whether predetermined intra-skill agent transitions constitute "hops" (enables enhanced 4-hop mode)

**Patterns implemented:** F-2a, F-2b, B-1, A-2, A-3, A-4, A-5, C-2 (approximated), C-3, D-1, D-2, E-2, H-1, H-2

### Phase 2: Workflow Type Classification (Target: +2 months)

**Deliverables:**
- NOMINAL/ABNORMAL/EMERGENCY workflow type definitions (A-1)
- Decision authority annotations per workflow type (E-1)
- Three-part communication echo-confirmation extension to handoff schema (F-1)

### Phase 3: OE Feedback Loop (Target: +4 months)

**Deliverables:**
- Periodic OE synthesis trigger (threshold-based)
- OE-to-workflow-revision pipeline (ps-synthesizer integration)
- OE entry schema formalization (H-1 CAP maturation)

### Phase 4: Emergency Routing (Target: +6 months)

**Deliverables:**
- Symptom-based emergency workflow activation (G-1)
- Integration with AE-006 graduated escalation
- ABNORMAL/EMERGENCY workflow definitions with distinct agent behaviors

---

## Related Decisions

| Related ADR | Relationship |
|-------------|-------------|
| ADR-PROJ007-001 (Agent Definition Standards) | This ADR's agent designs conform to the dual-file architecture and governance schema defined there. |
| ADR-PROJ007-002 (Agent Routing Standards) | Trigger keywords and circuit breaker analysis follow routing standards defined there. H-36 ambiguity documented. |
| ADR-EPIC002-001 (Quality Enforcement Strategy) | QG-HOLD gates use the quality enforcement threshold and scoring dimensions defined there. |
| Phase 2 Pattern Extraction (sop-pattern-extraction.md) | Direct input to this ADR. 22 patterns, 8 gaps, 3-agent recommendation. |
| Phase 1 Research Survey (nuclear-sop-survey.md) | Foundation evidence for all nuclear patterns referenced in this ADR. |
| QG3 Architecture Review (architecture-review.md) | Adversarial review that identified 16 findings driving this revision. |

---

## PS Integration

**PS ID:** phase-3.1
**Entry ID:** e-003
**Decision type:** architecture
**Artifact:** `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md`
**Confidence:** HIGH (0.90) -- increased from 0.87 after addressing QG3 findings

**Key findings for downstream agents:**
1. Option D (four-agent) selected: sop-brief + sop-executor + sop-verifier + sop-capture
2. Context-isolated verification (FC-M-001) approximates but does not replicate nuclear Criterion X IV -- honest about limitations per P-022
3. Skill adds 4 agents, ~16 files, 1 SKILL.md, and 1 trigger map entry
4. Dual-mode H-36 compliance: primary 3-hop mode (unambiguous), enhanced 4-hop mode (requires governance ruling)
5. PROCEDURE_STATE.yaml enables pause/resume across hold points and sessions
6. Hold point implementation fully specified: USER-HOLD (user approval), QG-HOLD (ps-critic S-014), IV-HOLD (Task-invoked sop-verifier)
7. sop-brief can generate workflow definitions from natural language (Step 0)
8. Highest risk: OE entry accumulation without synthesis (RPN 245) and over-engineering C1 tasks (RPN 210)
9. Phase 1 delivers all 14 core patterns; Phases 2-4 extend with workflow types, OE loop, and emergency routing

**Next agent hint:** Phase 3 QG3 re-evaluation at >= 0.92 threshold.

---

## Self-Review Record

### S-010 Self-Refine Applied Before Submission (Iteration 3 -- FINAL)

**Completeness check:**
- [x] All three options from task description evaluated
- [x] Option D (recommended refinement) added as analyst-designed fourth option
- [x] All 6 evaluation dimensions scored for each option
- [x] Nuclear pattern mapping complete (22 patterns addressed)
- [x] Hold point implementation fully specified (3 types with pause/resume mechanics) -- R4
- [x] STAR implementation specified with S-010 comparison table -- DA-003
- [x] Procedure use classification specified (3 levels) with C1-C4 relationship -- DA-002
- [x] Circuit breaker analysis with formal rule-text citation and dual-mode design -- R1/R3
- [x] Trigger keywords defined
- [x] PROCEDURE_STATE.yaml schema defined with resume protocol -- R2
- [x] sop-brief workflow generation capability specified (Step 0) -- R5
- [x] Governance YAML skeleton provided for sop-verifier -- CC-001
- [x] Worked example committed to Phase 1 deliverables -- PM-006
- [x] mandatory-skill-usage.md in registration targets -- CC-004
- [x] 21-skill count acknowledged with Phase 2 transition note -- CC-003
- [x] Decision table: /nuclear-sop vs. /orchestration -- DA-006
- [x] OE entry schema with workflow_type field -- PM-005
- [x] Canonical execution log version rule for sop-capture -- PM-003
- [x] sop-executor Bash scope constrained with CAUTION -- PM-004
- [x] sop-capture conditional Step 0 for 3-hop integrated verification with anchoring-bias disclaimer -- R7/NC-001
- [x] Cross-session resume discovery mechanism specified (Glob scan for non-terminal PROCEDURE_STATE.yaml) -- R8/NC-002

**Internal consistency check (NC-001 resolution):**
- [x] sop-capture methodology Step 0 now aligns with H-36 Compliance section's dual-mode design recommendation (line 754 area)
- [x] IV report is treated as optional input in sop-capture Step 2: "if available from 4-hop mode or Step 0 integrated verification result"
- [x] 3-hop mode is operationally specified: sop-capture can perform integrated verification without separate sop-verifier

**Actionability check (NC-002 resolution):**
- [x] Resume discovery mechanism specified: orchestrator scans for PROCEDURE_STATE.yaml with non-terminal status at session start
- [x] User decision preserved (P-020): orchestrator presents paused workflow but never auto-resumes
- [x] Relationship to ORCHESTRATION.yaml resumption context documented
- [x] Explicit invocation alternative provided for users who know the path

**Consequence check (P-022):**
- [x] Negative consequences documented (5 items including context budget, latency, adoption friction, circuit breaker tension)
- [x] Patterns NOT implemented explicitly listed with rationale
- [x] Approximated patterns distinguished from preserved patterns -- with C-2 moved to Approximated per R6
- [x] Impossible patterns acknowledged (C-1 peer checking, operator requalification, regulatory oversight)
- [x] sop-verifier independence claim explicitly bounded: context isolation (preserved) vs. personnel independence (not preserved) -- R6
- [x] 3-hop mode anchoring-bias trade-off honestly documented in sop-capture Step 0 -- R7

**Rationale check (P-011):**
- [x] Each option has steelman applied (S-003)
- [x] Decision rationale addresses why highest-score option was not selected
- [x] Evidence traces to Phase 1 and Phase 2 artifacts
- [x] QG3 adversarial review findings addressed (iterations 1, 2, and 3)

**Constitutional compliance (P-003, P-020, P-022):**
- [x] P-003: No agent spawns sub-agents. Main context orchestrates all 4.
- [x] P-020: USER-HOLD preserves user authority. Status is PROPOSED (not ACCEPTED). Resume discovery preserves user decision authority.
- [x] P-022: Transparent about preserved vs. approximated vs. impossible patterns. sop-verifier independence explicitly bounded. 3-hop mode anchoring bias honestly disclosed.

**Pre-Mortem applied (S-004):**
- [x] 4 failure scenarios analyzed with strengthened mitigations (Step 0, acceptance criteria STOP, workflow_type field)

---

*ADR Version: 1.2.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-003, P-004, P-011, P-020, P-022)*
*Criticality: C3 (Significant) per AE-003 (new ADR)*
*Created: 2026-03-22*
*Revised: 2026-03-23 (QG3 Iteration 3 FINAL -- R7 sop-capture integrated verification + R8 resume discovery)*
*Agent: ps-architect-001*
