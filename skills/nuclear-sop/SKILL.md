---
name: nuclear-sop
description: "Nuclear-inspired standard operating procedure (SOP) skill for high-rigor, procedural execution of C2+ workflows. Provides pre-job briefing, step-by-step STAR self-checked execution with place-keeping and hold points, context-isolated independent verification, and mandatory post-job operating experience (OE) capture. WHEN: use for any workflow requiring mandatory pre-execution context loading, step-level compliance verification, named blocking hold points, and structured lessons-capture as required infrastructure. Triggers: nuclear sop, pre-job brief, STAR self-check, hold point, place-keeping, OE capture, nuclear procedure, nuclear workflow, nuclear rigor, nuclear discipline."
version: "1.1.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "nuclear sop"
  - "nuclear procedure"
  - "STAR self-check"
  - "pre-job brief"
  - "post-job brief"
  - "hold point"
  - "place-keeping"
  - "step sign-off"
  - "procedure compliance"
  - "continuous use"
  - "procedure use classification"
  - "operating experience capture"
  - "OE entry"
  - "nuclear rigor"
  - "nuclear discipline"
  - "sop brief"
  - "sop execute"
  - "sop capture"
  - "sop verify"
  - "nuclear workflow"
---

# /nuclear-sop Skill

> **Version:** 1.1.0
> **Framework:** Jerry Nuclear SOP (NSOP)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Source Spec:** `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` v2.0.0

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | New users, workflow designers | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Routing Disambiguation](#routing-disambiguation), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Workflow Execution Sequence](#workflow-execution-sequence), [Security Considerations](#security-considerations), [File Structure](#file-structure) |
| **L2 (Architect)** | Framework maintainers, governance leads | [H-36 Circuit Breaker Compliance](#h-36-circuit-breaker-compliance), [P-003 Compliance](#p-003-compliance), [Constitutional Compliance](#constitutional-compliance), [References](#references), [Registration Content](#registration-content) |

---

## Purpose

The `/nuclear-sop` skill imports 50+ years of nuclear power plant SOP methodology into Jerry agent workflows. Nuclear engineering has spent half a century solving the same problem that AI agent frameworks face today: how do you ensure a capable agent executes a high-stakes procedure reliably, catches its own errors, learns from failures, and escalates when conditions do not match expectations?

The nuclear answer is a multi-layered framework of temporal discipline (before/during/after as first-class phases), step-level compliance verification, named blocking hold points, and a mandatory feedback loop that converts every execution into institutional knowledge. This skill imports that framework.

### What the Skill Closes

The highest-value gap this skill addresses is the absence of formalized pre/post-execution phases in Jerry workflows. Treating context loading and lessons capture as infrastructure rather than first-class procedural steps is the most significant weakness the nuclear framework reveals in AI agent practice.

### Key Capabilities

- **Pre-Job Briefing** -- mandatory context loading, prerequisite check, OE history review, error trap identification before any execution begins
- **STAR Self-Checking** -- Stop-Think-Act-Review applied before every state-modifying tool call (Write, Edit, Bash)
- **Place-Keeping** -- step-level sign-off with persistent `PROCEDURE_STATE.yaml` enabling pause/resume across sessions
- **Hold Points** -- three blocking gate types: USER-HOLD (human approval), QG-HOLD (quality gate), IV-HOLD (independent verification)
- **Procedure Use Classification** -- `[CONTINUOUS]` (execute exactly), `[REFERENCE]` (judgment permitted), `[INFORMATION]` (context only)
- **Context-Isolated Verification** -- sop-verifier operates with fresh context (no executor reasoning) for C3+ workflows
- **OE Capture** -- mandatory post-job schema-validated operating experience entry written to `docs/experience/`

---

## When to Use This Skill

Activate when:

- Workflow requires mandatory pre-execution context loading before any tool calls begin
- Workflow has a defined procedure with numbered steps that must be executed in sequence
- Step-level place-keeping and sign-off are required (audit trail, pause/resume across sessions)
- Independent verification of work products is needed with fresh context
- Post-job operating experience capture is a required output (not optional)
- Criticality is C2+ and procedural rigor must be documented
- Workflow definition does not yet exist and must be generated from a natural language description (Step 0)

NEVER invoke this skill when:

- Task is C1 routine work without a defined procedure -- Consequence: sop-brief, sop-executor, sop-verifier, sop-capture overhead is disproportionate to a single-session reversible task; use standard quality patterns (S-010 self-review only)
- Task is pure research or exploratory analysis with no procedure to follow -- Consequence: nuclear SOP phases (brief, execute, verify, capture) impose sequential structure on divergent work that requires free exploration; use `/problem-solving` instead
- Task is multi-phase pipeline coordination with no defined workflow definition -- Consequence: /nuclear-sop requires a procedure file as entry point; ad-hoc pipeline coordination without enumerated steps belongs in `/orchestration`
- Task requires coordination of multiple Jerry skills -- Consequence: /nuclear-sop is a single-skill execution framework; cross-skill sequencing and barrier synchronization belong in `/orchestration`
- No workflow definition exists AND user declines Step 0 workflow generation -- Consequence: sop-brief Step 1 cannot proceed without a procedure file; halt and route to `/orchestration` or user-defined plan
- **Workflow is C3+ AND the STAR A/B validation gate (QG-E4, ENG Phase 4 PM-01/PM-02) has NOT PASSED** -- Consequence: the STAR self-checking protocol is a behavioral claim, not a verified deterministic constraint; using this skill at C3+ before QG-E4 passes exposes irreversible work to an unvalidated error-trap catch-rate; restrict to C1-C2 only until QG-E4 produces a documented PASS result. See [STAR Validation Pre-Ship Gate](#star-validation-pre-ship-gate) in Security Considerations.

---

## Available Agents

| Agent | Role | Tool Tier | Model | Cognitive Mode | Primary Nuclear Patterns |
|-------|------|-----------|-------|---------------|--------------------------|
| `sop-brief` | Pre-job briefing: context load, prerequisite check, OE history review, error trap identification; optionally generates workflow definition from natural language (Step 0) | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | systematic | F-2a, D-1, H-2, A-3 sections 1-6 |
| `sop-executor` | Step-by-step execution: STAR self-checking before each tool call, place-keeping, hold point activation, persistent PROCEDURE_STATE.yaml; max steps per invocation enforced by criticality | T2 (Read, Write, Edit, Glob, Grep, Bash) | opus | systematic | B-1, A-5, A-2, A-4, D-2, C-3, E-2 |
| `sop-verifier` | Context-isolated verification: evaluates work products against acceptance criteria with fresh context, no exposure to executor reasoning chain; required for C3+ (4-hop mode) | T1 (Read, Glob, Grep -- read-only by design) | sonnet | convergent | C-2 (approximated), C-3 (IV-HOLD) |
| `sop-capture` | Post-job OE capture: deviations, quality gate results, lessons learned, improvement recommendations; integrated IV verification in 3-hop mode (C1-C2 only) | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | systematic | F-2b, H-1, H-2 infrastructure |

**Agent paths:** `skills/nuclear-sop/agents/{agent-name}.md` and `skills/nuclear-sop/agents/{agent-name}.governance.yaml`

---

## Workflow Execution Sequence

**Step 0 is OPTIONAL (workflow generation from natural language). Steps 1-4 are MANDATORY once a workflow definition exists.**

```
USER REQUEST + WORKFLOW DEFINITION (or natural language description)
        |
        v
+---------------------------+
| 0. sop-brief [OPTIONAL]   |  Workflow Definition Generation from natural language
|   IF no workflow file:    |  Generates draft, presents to user for confirmation (P-020)
|   generate + confirm      |  Output: brief/draft-workflow-definition.md
+--------+------------------+
         |
         | [MANDATORY from here for any /nuclear-sop invocation]
         v
+---------------------------+
| 1. sop-brief [MANDATORY]  |  Pre-Job Briefing Phase
|   - Locate procedure file |  STOP: if no procedure definition found, offer Step 0 or HALT
|   - Load context          |  Patterns: F-2a, D-1, H-2, A-3 sections 1-6
|   - Check prerequisites   |  STOP if prereqs fail (P-020 -- user decides)
|   - Validate acceptance   |  STOP if acceptance criteria missing/unverifiable
|     criteria quality      |  WARNING if >10 OE entries without synthesis
|   - Search OE history     |    STOP if >20 OE entries without synthesis (hard limit)
|   - Present OE entries    |  OE findings are MANDATORY CONTEXT, not optional reading
|   - Identify error traps  |
+--------+------------------+
         |
         | Output: brief/pre-job-brief.md
         v
+---------------------------+
| 2. sop-executor           |  Execution Phase
|   - STAR per tool call    |  Patterns: B-1, A-5, A-2, A-4, D-2, C-3, E-2
|   - Place-keeping         |  State: PROCEDURE_STATE.yaml (updated per step)
|   - [CONTINUOUS] strict   |  C3 workflows: max 15 steps per invocation
|   - [REFERENCE] judgment  |  >15 steps: split into sub-procedures with handoff
|   - Hold points block     |
|   - Stop-work on deviation|
+--------+------------------+
         |
         | Output: work products + execution-log.md (FINAL) + PROCEDURE_STATE.yaml
         v
+---------------------------------------+
| 3. Verification (mode depends on C-level)  |
|                                            |
| C1-C2: sop-capture [3-hop, integrated IV]  |
|   - Step 0: verify work products before OE |
|   - Anchoring-bias disclaimer applies      |
|   - Acceptable for C1-C2 (reversible work) |
|                                            |
| C3+: sop-verifier [4-hop, REQUIRED]        |
|   - Fresh context via Task tool            |
|   - NO executor reasoning in input         |
|   - Acceptance criteria evaluation only    |
|   - Disposition: ACCEPT / REJECT / CONDITIONAL |
|   - 4-hop mode REQUIRED, not optional      |
+-------------------+--------------------+
         |
         v
+---------------------------+
| 4. sop-capture [MANDATORY]|  Post-Job Capture Phase
|   - Read FINAL exec log   |  Patterns: F-2b, H-1, H-2 infrastructure
|   - Compare to plan       |  OE entry schema: mandatory fields enforced
|   - Document deviations   |  workflow_type, deviation_type, root_cause,
|   - Lessons learned       |  recommendation, criticality (all REQUIRED)
|   - Improvement recs      |
+--------+------------------+
         |
         v
    OE ENTRY (written to both local capture dir and docs/experience/)
    Schema-validated: missing required fields block write (not warn)
```

---

## Routing Disambiguation

| Request Type | Use This Skill | Use Instead | Reason |
|--------------|---------------|-------------|--------|
| Execute a defined step-by-step procedure with sign-off | `/nuclear-sop` | -- | Core use case |
| Multi-phase research/analysis pipeline without defined steps | -- | `/orchestration` | No procedure to execute; pipeline coordination is orchestration's domain |
| Iterative improvement with creator-critic-revision loops | -- | `/problem-solving` | H-14 quality cycles are a /problem-solving pattern; STAR is for pre-action checking, not iterative refinement |
| Standalone adversarial quality review of a completed deliverable | -- | `/adversary` | /adversary applies S-001 through S-014 strategy templates; /nuclear-sop applies QG-HOLD gates as part of procedure execution |
| Threat model, security architecture, SAST review | -- | `/eng-team` | Domain-specific secure engineering methodology; nuclear-sop provides execution rigor, not security analysis |
| Independent verification (IV) within a nuclear-sop execution | `sop-verifier` (invoked by main context) | -- | sop-verifier IS the IV mechanism; invoke it directly as part of the 4-hop sequence for C3+ |

### Decision Table: `/nuclear-sop` vs. `/orchestration`

| Condition | Use `/nuclear-sop` | Use `/orchestration` |
|-----------|--------------------|--------------------|
| Task has a defined procedure with numbered steps | Yes | No |
| Task requires step-level place-keeping and sign-off | Yes | No |
| Task requires independent verification of work products | Yes (sop-verifier) | Partial (FC-M-001, no context isolation guarantee) |
| Task requires post-job OE capture as a required artifact | Yes (sop-capture) | No |
| Task is multi-phase research/analysis pipeline | No | Yes |
| Task requires coordination of multiple skills | No | Yes |
| Task is C1 routine work | No -- overhead disproportionate | Optional |
| No defined procedure exists yet | Use sop-brief Step 0 to generate one | Yes, if ad-hoc coordination only |

---

## Security Considerations

> **SR-06 Requirement:** This section is a mandatory security disclosure. Read before executing any workflow definition.

### Workflow Definitions Are Executable Content

A workflow definition is not a passive document. Every `[CONTINUOUS]` step directs the sop-executor to make specific tool calls (Write, Edit, Bash) against specific targets. A crafted workflow definition can instruct the executor to overwrite files, delete artifacts, or execute shell commands.

**Treat workflow definition code review with the same rigor as a shell script review.**

Before using any workflow definition you did not author yourself, verify:
- [ ] The author and version metadata are accurate and trustworthy
- [ ] No step targets paths outside the intended project scope
- [ ] No Bash commands execute external processes without explicit rationale
- [ ] All `[USER-HOLD]` annotations are present on state-modifying steps for C3+ workflows

### Prompt Injection Surface (TB-1 Trust Boundary)

The workflow definition file is the primary trust boundary (TB-1) in the nuclear-sop architecture. Content read by sop-brief and sop-executor during a workflow execution is injected into the agent's context. A malicious or corrupted workflow definition can attempt to override agent behavior through embedded instructions.

**Compensating control for shared repositories:** All workflow definitions in shared repositories MUST be code-reviewed before first use. Treat the `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` schema as the canonical structure; deviations warrant scrutiny.

### STAR Validation Pre-Ship Gate

**C3+ status: WITHDRAWN pending re-validation** (QG-E4 evidence invalidated in PROJ-032 review; see remediation register REM-04). **Approved use: C1-C2 only.** The 2026-04-20 "3/3 catch rate" result was a simulation walkthrough (desk-check) of a fixture containing its own expected answers; it is not independent execution evidence and does not support lifting the C3+ restriction. The STAR self-checking protocol remains a behavioral claim, not a verified deterministic constraint.

**QG-E4 Pre-Ship Gate:**

| Field | Value |
|-------|-------|
| Owner | eng-qa-001 |
| Pass criteria | STAR-ON catch rate >= 60% on 3+ deliberate error traps; STAR-OFF catch rate 0% (confirming traps are functional) |
| Test protocol | A/B comparison defined in `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-4/eng-qa-001/test-strategy.md` Section 1.4 |
| Test fixture | `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` (TRAP-01, TRAP-02, TRAP-03) |
| Result | **INVALIDATED.** The 2026-04-20 result (`projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/validation/qg-e4/star-validation-results.md`) was a simulation walkthrough (desk-check), not independent execution evidence. Re-validation with blind fixtures and live executed runs is required before C3+ approval (PROJ-032 remediation register REM-04). |

**SEC-008 status:** REMEDIATED in the PROJ-032 maintainer patch (remediation register REM-12) — sop-verifier's hold-point consistency check is now fail-closed: a missing or unreadable PROCEDURE_STATE.yaml records a `STATE-FILE-UNAVAILABLE` anomaly and the disposition cannot be unconditional ACCEPT.

---

## H-36 Circuit Breaker Compliance

The 4-agent sequence (sop-brief -> sop-executor -> sop-verifier -> sop-capture) creates an ambiguous case under H-36 (max 3 routing hops). Two operating modes are defined, with mode selection bound to workflow criticality.

### 3-Hop Mode (C1-C2, Unambiguously Compliant)

| Hop | From | To | Notes |
|-----|------|-----|-------|
| 1 | Main context | sop-brief | Skill entry via routing |
| 2 | Main context | sop-executor | Predetermined sequence |
| 3 | Main context | sop-capture (with integrated IV) | Integrated IV in Step 0 before OE capture |

Trade-off: sop-capture has access to execution log before verifying work products (anchoring bias). Accepted for C1-C2 because work is reversible.

### 4-Hop Mode (C3+, REQUIRED)

| Hop | From | To | Classification |
|-----|------|-----|---------------|
| 1 | Main context | sop-brief | HOP (skill entry) |
| 2 | Main context | sop-executor | Ambiguous (predetermined sequence) |
| 3 | Main context | sop-verifier | Claimed: NOT a hop (quality gate analog); Strict: HOP |
| 4 | Main context | sop-capture | Exceeds limit if hop 3 is a hop |

For C3+ work, the anchoring bias of 3-hop mode is a material quality compromise. The 3-hop mode MUST NOT be used for C3+ workflows.

### Governance Ruling Pending

A governance request has been filed: whether a predetermined intra-skill verification step (no routing re-evaluation) constitutes a "hop" under H-36. This ruling has framework-wide implications for any skill with 4+ agents.

**Governance ruling deadline:** If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is 3-hop mode for all criticality levels. sop-verifier is eliminated as a separate agent; sop-capture's integrated IV (Step 0) becomes the permanent verification mechanism for all criticality levels, with anchoring bias limitation explicitly documented.

---

## File Structure

```
skills/nuclear-sop/
  SKILL.md                            # This file -- skill definition, routing, activation keywords
  agents/
    sop-brief.md                      # Pre-job briefing agent (Step 0 + Step 1)
    sop-brief.governance.yaml
    sop-executor.md                   # Execution agent: STAR + hold points + place-keeping
    sop-executor.governance.yaml
    sop-verifier.md                   # Context-isolated verification agent (T1 read-only)
    sop-verifier.governance.yaml
    sop-capture.md                    # Post-job OE capture agent (+ integrated IV for C1-C2)
    sop-capture.governance.yaml
  templates/
    WORKFLOW_DEFINITION.template.md   # 11-section nuclear procedure template
    PRE_JOB_BRIEF.template.md         # Pre-job briefing output template
    POST_JOB_BRIEF.template.md        # OE capture output template
    HOLD_POINT_LOG.template.md        # Hold point sign-off record
    PROCEDURE_STATE.template.yaml     # Execution state schema for pause/resume
  examples/
    c3-adr-workflow-definition.md     # Worked example: C3 ADR with nuclear rigor (STAR validation fixture)
  rules/
    nuclear-sop-behavior-rules.md     # Skill-scoped behavioral rules (this skill only)
  behavioral-baselines/
    bb-001-star-clean-execution.md    # Expected STAR behavior baseline
    bb-002-user-hold-activation.md    # Expected hold point behavior baseline
    bb-003-oe-feedback-loop-integrity.md  # Expected OE feedback behavior baseline
  composition/                        # DERIVED ARTIFACTS -- see note below
    {agent}.agent.yaml                # Derived canonical-format agent definitions (4 files)
    {agent}.prompt.md                 # Derived system prompts (4 files)
  docs/
    tutorial-getting-started.md       # Tutorial
    howto-guides.md                   # How-to guides
    reference.md                      # Reference documentation
```

> **Composition files are derived artifacts.** The normative source for each agent is `agents/{name}.md` + `agents/{name}.governance.yaml` — these are what `plugin.json` and Claude Code load. The `composition/` copies are derived; on conflict, the `agents/` pair wins.

### Execution Directory (`{execution_dir}`)

`{execution_dir}` is the base directory for all per-execution artifacts (PROCEDURE_STATE.yaml, HOLD_POINT_LOG.md, execution-log.md, `brief/`, `capture/`). Per the Unified Output Path Resolution Protocol (AD-M-011), it is the **caller-provided base path (Priority 2)**, defaulting to:

```
projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/
```

when the caller provides no explicit path. Agent `output.location` declarations in the governance files reference `{execution_dir}` against this definition.

---

## P-003 Compliance

All nuclear-sop agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates the workflow.

```
P-003 AGENT HIERARCHY:
======================

  +---------------------------+
  | MAIN CONTEXT              |  <-- Orchestrator (Claude session)
  | (orchestrator)            |
  +---------------------------+
     |        |        |        |
     v        v        v        v
  +-------+ +-------+ +-------+ +-------+
  | sop-  | | sop-  | | sop-  | | sop-  |  <-- Workers (max 1 level)
  | brief | | exec  | |verify | |capture|
  +-------+ +-------+ +-------+ +-------+

  Agents CANNOT invoke other agents.
  Agents CANNOT spawn subagents.
  Only MAIN CONTEXT orchestrates the sequence.
  sop-verifier invoked via Task tool (fresh context isolation).
```

---

## Invoking an Agent

Three invocation patterns (choose based on your context):

**Option 1: Natural language (recommended)**
Tell Claude what you need and it routes to the correct agent:
```
"Run a pre-job brief for this workflow definition"     → sop-brief
"Execute this procedure with STAR self-checking"       → sop-executor
"Verify the work products from this execution"         → sop-verifier
"Capture operating experience from this execution"     → sop-capture
```

**Option 2: Explicit agent name**
```
"Use /nuclear-sop sop-executor to execute workflow.md"
```

**Option 3: Full workflow sequence**
The main context orchestrates the full 3-hop or 4-hop sequence:
```
1. sop-brief   → pre-job brief (mandatory)
2. sop-executor → step execution with STAR (mandatory)
3. sop-verifier → independent verification (C3+ only, via Task tool)
4. sop-capture  → OE capture (mandatory)
```

---

## Constitutional Compliance

| Principle | Requirement | Nuclear-SOP Application |
|-----------|-------------|------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | All four agents are T1/T2 workers; Task tool absent from all agent tool lists |
| P-020 | NEVER override user intent -- ask before destructive ops | All USER-HOLD points require explicit APPROVE/REJECT/WAIVE; OE STOP threshold requires user override; prerequisite failures present options, not auto-resolutions |
| P-022 | NEVER deceive about actions, capabilities, or confidence | STAR behavioral limitations (not deterministic), approximated nuclear patterns, and 3-hop vs. 4-hop ambiguity are documented explicitly in every sop-executor invocation |
| P-002 | NEVER leave outputs in transient context only -- persist to files | PROCEDURE_STATE.yaml, execution-log.md, pre-job-brief.md, and OE entries are all mandatory file artifacts; no nuclear-sop output lives only in context |
| STAR Transparency | STAR is a structural behavioral prompt constraint, not a physical interruption | sop-executor.md documents: "Both STAR reasoning and the tool call are generated in the same inference pass. The temporal separation is a structural constraint in the prompt, not a physical interruption as in nuclear plant operations." |
| OE Schema Enforcement | OE entry missing required fields blocks the write | sop-capture must not write a partial OE entry with optional fields missing; a write-block is not a warning |

---

## Quick Reference

### Common Invocations

| Need | Agent | Example |
|------|-------|---------|
| Run full nuclear-rigor workflow from NL description | sop-brief (Step 0 then 1) | "Use nuclear-sop to generate and execute a procedure for ADR authoring at C3" |
| Execute an existing workflow definition | sop-brief then sop-executor | "Run pre-job brief for skills/nuclear-sop/examples/c3-adr-workflow-definition.md then execute" |
| Verify completed work products (C3+) | sop-verifier | "Use sop-verifier to evaluate work products against acceptance criteria in PROCEDURE_STATE.yaml" |
| Capture post-job OE | sop-capture | "Use sop-capture to write the OE entry for workflow run WF-ADR-001" |
| Check active paused workflows | main context scan | "Scan for any PROCEDURE_STATE.yaml files with non-terminal status in PROJ-0039" |

### Hold Point Quick Reference

| Type | Annotation | Release Condition |
|------|-----------|-------------------|
| `[USER-HOLD]` | Step requires human approval | User responds APPROVE, REJECT, or WAIVE |
| `[QG-HOLD]` | Phase quality gate | Quality score >= 0.92 (H-13) via ps-critic |
| `[IV-HOLD]` | Independent verification required | sop-verifier produces ACCEPT disposition |

### Procedure Classification Quick Reference

| Classification | Annotation | Executor Behavior |
|---------------|------------|-------------------|
| Continuous | `[CONTINUOUS]` | Execute exactly as written. Full STAR. Step sign-off required. |
| Reference | `[REFERENCE]` | Consult for guidance. Agent may exercise judgment. |
| Information | `[INFORMATION]` | Background context. Not executed. |

---

## References

| Resource | Path | Purpose |
|----------|------|---------|
| Behavioral rules | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` | HARD/MEDIUM rules (NS-H-01 through NS-H-10) |
| Agent: sop-brief | `skills/nuclear-sop/agents/sop-brief.md` | Pre-job briefing agent definition |
| Agent: sop-executor | `skills/nuclear-sop/agents/sop-executor.md` | Step execution agent definition |
| Agent: sop-verifier | `skills/nuclear-sop/agents/sop-verifier.md` | Independent verification agent definition |
| Agent: sop-capture | `skills/nuclear-sop/agents/sop-capture.md` | OE capture agent definition |
| Template: Workflow definition | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` | 11-section procedure structure |
| Template: Procedure state | `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` | Execution state schema |
| Template: Pre-job brief | `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` | Briefing output structure |
| Template: Post-job brief | `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` | OE capture output structure |
| Template: Hold point log | `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` | Hold point sign-off record |
| Example: C3 ADR workflow | `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` | Worked example with STAR traps |
| Baseline: STAR clean | `skills/nuclear-sop/behavioral-baselines/bb-001-star-clean-execution.md` | Expected STAR behavior |
| Baseline: USER-HOLD | `skills/nuclear-sop/behavioral-baselines/bb-002-user-hold-activation.md` | Expected hold point behavior |
| Baseline: OE loop | `skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md` | Expected OE feedback behavior |
| Spec synthesis | `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` | Requirements SSOT (0.922) |
| ADR-001 | `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` | Architecture decisions (0.933) |
| QG-E4 results | `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/validation/qg-e4/star-validation-results.md` | STAR A/B simulation walkthrough (desk-check; invalidated per PROJ-032 remediation register REM-04 — not independent execution evidence) |

### Nuclear Industry Source References

| Source | Citation | Patterns Derived |
|--------|----------|-----------------|
| INPO AP-907 Rev.3 | INPO, "Procedure Use and Adherence," AP-907 Rev.3, 2016 | Procedure use classification, place-keeping, STAR self-checking |
| INPO 09-003 | INPO, "Guidelines for Performance Improvement at Nuclear Power Plants," 09-003 Rev.1, 2012 | Pre-job briefing, post-job review, OE capture |
| INPO 06-003 | INPO, "Human Performance Reference Manual," 06-003, 2006 | STAR protocol (Stop-Think-Act-Review), questioning attitude, conservative decision-making |
| 10 CFR 50 App B | NRC, "Quality Assurance Criteria for Nuclear Power Plants," 10 CFR 50 Appendix B | Hold points, independent verification, QC hold points |
| NUREG-1792 | NRC, "Good Practices for Implementing HRA," NUREG-1792, 2005 | Human reliability analysis context for procedural compliance |

---

## Registration Content

> H-26 requirement: Registration artifacts must appear in SKILL.md so QG-E3 can verify their presence before registration is executed.
>
> **REGISTRATION STATUS: APPLIED.** The skill is registered in `CLAUDE.md` (Skills quick-reference table), `AGENTS.md` (Nuclear SOP Skill Agents section), `.context/rules/mandatory-skill-usage.md` (trigger map, priority 16), and `plugin.json` as part of PR #269. QG-E6 final review gate scored **0.934 PASS on 2026-04-14** — evidence: `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-6/eng-reviewer-001/qg-e6-score.md`.

### CLAUDE.md Quick Reference Table Row

As registered in the Skills table in `CLAUDE.md`:

```
| `/nuclear-sop` | Nuclear-inspired SOP execution: pre-job brief, STAR self-check, hold points, OE capture |
```

### AGENTS.md Entries

As registered in `AGENTS.md` under the "Nuclear SOP Skill Agents" section:

```markdown
### /nuclear-sop

| Agent | File | Role |
|-------|------|------|
| `sop-brief` | `skills/nuclear-sop/agents/sop-brief.md` | Pre-job briefing: context load, prerequisite check, OE history review, error trap identification |
| `sop-executor` | `skills/nuclear-sop/agents/sop-executor.md` | Step-by-step execution with STAR self-checking, place-keeping, hold point activation |
| `sop-verifier` | `skills/nuclear-sop/agents/sop-verifier.md` | Context-isolated independent verification (T1 read-only, fresh context) |
| `sop-capture` | `skills/nuclear-sop/agents/sop-capture.md` | Post-job OE capture with schema-enforced mandatory fields |
```

### mandatory-skill-usage.md Trigger Map Row

The live trigger map row is maintained in `.context/rules/mandatory-skill-usage.md` (Trigger Map table, priority 16) — that file is the SSOT for the `/nuclear-sop` routing row. No copy is duplicated here: a second copy would drift from the live row (it already had, before the PROJ-032 remediation removed it).
