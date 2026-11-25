# /nuclear-sop Skill Specification: Unified Synthesis

> **PS ID:** phase-4.1 | **Entry ID:** e-004 | **Agent:** ps-synthesizer-001
> **Date:** 2026-03-23 | **Confidence:** HIGH (0.92) | **Version:** 2.0.0
> **Input Artifacts:**
> - Phase 1: `ps/phase-1/ps-researcher-001/nuclear-sop-survey.md` (confidence 0.88, Revision 2)
> - Phase 2: `ps/phase-2/ps-analyst-001/sop-pattern-extraction.md` (confidence 0.88, Revision 2)
> - Phase 3: `ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` (confidence 0.90, Revision 3 FINAL)
> **Methodology:** Braun & Clarke thematic analysis (6 phases), cross-reference matrix, dependency graph

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview for stakeholders |
| [L1: Technical Synthesis](#l1-technical-synthesis) | Full skill specification, cross-reference matrix, roadmap, risks |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Nuclear fidelity assessment, long-term evolution, Jerry ecosystem integration |
| [Source Summary](#source-summary) | All sources with contribution summary |
| [Revision History](#revision-history) | Change log across versions |

---

## L0: Executive Summary

This synthesis consolidates three prior phases of research into a single, actionable specification for the `/nuclear-sop` Jerry skill. The research pipeline began with a 50-source survey of nuclear power plant standard operating procedures (Phase 1), extracted 22 implementable patterns across 9 families (Phase 2), and produced an architecture decision record for a four-agent skill design (Phase 3). This document unifies those outputs into the complete picture needed to build the skill.

The core finding across all three phases is consistent: nuclear engineering has spent more than 50 years solving the same problem that AI agent frameworks face today -- how do you ensure that a capable agent (human operator or LLM) executes a high-stakes procedure reliably, catches its own errors, learns from failures, and escalates when conditions do not match expectations? The nuclear answer is a multi-layered framework of temporal discipline (before/during/after as first-class phases), step-level compliance verification, named blocking hold points, and a mandatory feedback loop that converts every execution into institutional knowledge. The `/nuclear-sop` skill imports this framework into Jerry.

The recommended architecture is a four-agent skill: `sop-brief` (pre-job briefing), `sop-executor` (step-by-step execution with STAR self-checking and hold points), `sop-verifier` (context-isolated verification), and `sop-capture` (post-job operating experience capture). The skill implements 14 of the 22 extracted nuclear patterns directly, approximates 4 others (with explicit transparency about what is and is not preserved), and acknowledges 4 as impossible given current AI agent constraints. The highest-value gap this skill closes is the absence of formalized pre/post-execution phases in Jerry workflows -- treating context loading and lessons capture as infrastructure rather than first-class procedural steps is the most significant weakness the nuclear framework reveals in AI agent practice today.

**v2.0 key changes:** This revision adds an explicit STAR behavioral validation plan (the primary gap from QG4 review), strengthens the OE feedback loop with a concrete enforcement mechanism, restricts 3-hop anchored verification to C1-C2 workflows only, adds a pre-build pilot validation requirement, clarifies sop-brief Step 1 as mandatory, and corrects the risk register RPN ranking.

---

## L1: Technical Synthesis

### 1. Unified Skill Specification

#### 1.1 Skill Identity

| Property | Value |
|----------|-------|
| **Skill Name** | `nuclear-sop` |
| **Folder** | `skills/nuclear-sop/` |
| **Version** | 1.0.0 |
| **Jerry Skill Count Impact** | 20 -> 21 skills (one above H-37 Phase 1 threshold; keyword-first routing remains adequate) |
| **When to Use** | C2+ workflows requiring nuclear-inspired procedural rigor: mandatory pre-job context loading, step-by-step place-keeping, named hold points, context-isolated verification, post-job OE capture |
| **When NOT to Use** | C1 routine tasks (disproportionate overhead); pure research tasks (no procedure to follow); multi-phase pipeline coordination without a defined procedure (use `/orchestration` instead) |

**Activation Keywords (for mandatory-skill-usage.md):**

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow | adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review | 12 | "nuclear procedure" OR "pre-job brief" OR "post-job brief" OR "STAR self-check" OR "hold point" (phrase match) | `/nuclear-sop` |

**Decision table -- `/nuclear-sop` vs. `/orchestration`:**

| Condition | Use `/nuclear-sop` | Use `/orchestration` |
|-----------|--------------------|--------------------|
| Task has a defined procedure with numbered steps | Yes | No |
| Task requires step-level place-keeping and sign-off | Yes | No |
| Task requires independent verification of work products | Yes (sop-verifier) | Partial (FC-M-001, unstructured) |
| Task requires post-job OE capture as a required artifact | Yes (sop-capture) | No |
| Task is multi-phase research/analysis pipeline | No | Yes |
| Task requires coordination of multiple skills | No | Yes |
| Task is C1 routine work | No -- overhead disproportionate | Optional |
| No defined procedure exists | Use sop-brief Step 0 to generate one | Yes if ad-hoc coordination only |

#### 1.2 Skill File Structure

```
skills/nuclear-sop/
  SKILL.md                            # Skill definition (keywords, routing, when to use)
  agents/
    sop-brief.md                      # Pre-job briefing + workflow definition generation
    sop-brief.governance.yaml
    sop-executor.md                   # Execution with STAR + hold points + place-keeping
    sop-executor.governance.yaml
    sop-verifier.md                   # Context-isolated verification (read-only, fresh context)
    sop-verifier.governance.yaml
    sop-capture.md                    # Post-job OE capture + integrated IV (3-hop mode)
    sop-capture.governance.yaml
  templates/
    WORKFLOW_DEFINITION.template.md   # 11-section nuclear procedure template
    PRE_JOB_BRIEF.template.md         # Briefing output template
    POST_JOB_BRIEF.template.md        # OE capture output template
    HOLD_POINT_LOG.template.md        # Hold point sign-off record
    PROCEDURE_STATE.template.yaml     # Execution state for pause/resume
  examples/
    c3-adr-workflow-definition.md     # Worked example: C3 ADR with nuclear rigor (includes deliberate error trap)
  rules/
    nuclear-sop-behavior-rules.md     # Skill-scoped behavioral rules
```

**Total Phase 1 file count: ~16 files** (4 agent .md + 4 governance .yaml + 1 SKILL.md + 5 templates + 1 example + 1 rules file)

#### 1.3 Agent Taxonomy

| Agent | Role | Cognitive Mode | Tool Tier | Model | Nuclear Patterns |
|-------|------|---------------|-----------|-------|-----------------|
| `sop-brief` | Pre-job briefing: context load, prerequisite check, OE review, error trap identification; generates workflow definition from natural language if none provided | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | F-2a, D-1, H-2, A-3 sections 1-6 |
| `sop-executor` | Step-by-step execution: STAR self-checking, place-keeping, hold point activation, persistent execution state; maximum 15 steps per invocation for C3 workflows | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash -- Bash scoped to test/build commands) | opus | B-1, A-5, A-2, A-4, D-2, C-3, E-2 |
| `sop-verifier` | Context-isolated verification: evaluates work products against acceptance criteria with fresh context and no access to executor reasoning; required for C3+ workflows (4-hop mode) | convergent | T1 (Read, Glob, Grep -- read-only by design) | sonnet | C-2 (approximated), C-3 (IV-HOLD) |
| `sop-capture` | Post-job OE capture: deviations, quality gate results, lessons learned, improvement recommendations; integrated IV in 3-hop mode for C1-C2 only | systematic | T2 (Read, Write, Edit, Glob, Grep, Bash) | sonnet | F-2b, H-1, H-2 infrastructure |

#### 1.4 Workflow Execution Sequence

**Step 0 is OPTIONAL (workflow generation). Steps 1-4 are MANDATORY once a workflow definition exists.**

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
|   - Find procedure file   |  STOP: if no procedure definition found, offer Step 0 or halt
|   - Load context          |  Patterns: F-2a, D-1, H-2, A-3 sections 1-6
|   - Check prerequisites   |  STOP if prereqs fail (P-020)
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
         | Output: work products + execution log (FINAL) + PROCEDURE_STATE.yaml
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
|   - Pass / Reject / Conditional            |
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

**Clarification on Step 0 vs. Step 1 OPTIONAL labeling:** Step 0 (workflow generation from natural language) is optional -- it is the path when no workflow definition file exists yet. Step 1 (the pre-job briefing itself) is MANDATORY for every `/nuclear-sop` invocation. There is no path through the skill that bypasses sop-brief. The [OPTIONAL] annotation applies only to Step 0.

#### 1.5 STAR Self-Checking Protocol

Applied by `sop-executor` before each state-modifying tool call (Write, Edit, Bash).

```
S - STOP:   Log current step number and target action.
            Verify: Am I on the correct step per the workflow definition?
            Verify: Is this the correct file/target per the step specification?

T - THINK:  What is the expected outcome of this action?
            What are the preconditions for this step?
            What could go wrong? (Check WARNING/CAUTION from workflow definition)
            Is the step [CONTINUOUS] (execute exactly) or [REFERENCE] (judgment permitted)?
            If uncertain: invoke conservative decision-making (E-2 / H-31).

A - ACT:    Execute the tool call.
            Maintain focus on the specified target.

R - REVIEW: Did the outcome match expectation?
            If YES: sign off step in execution log; advance place-keeper;
                    update PROCEDURE_STATE.yaml.
            If NO:  STOP WORK (D-2). Log deviation. Escalate per hold point type.
```

**STAR vs. S-010 (Self-Refine) -- they are not the same:**

| Dimension | STAR (B-1) | S-010 Self-Refine |
|-----------|------------|------------------|
| Timing | Pre-action: before each tool call | Post-completion: after entire deliverable |
| Scope | Single step / single tool call | Entire output artifact |
| Action on failure | Stop-Work immediately | Revision: re-enter reasoning loop |
| State tracking | Updates PROCEDURE_STATE.yaml per step | No state file |
| Nuclear analog | Operator self-checking before valve operation | Supervisor walk-down after shift |
| Value for CONTINUOUS steps | High -- enforces stop-check-act-review sequencing | Low -- post-hoc cannot undo executed steps |

**LLM implementation note:** Both STAR reasoning and the tool call are generated in the same inference pass. The temporal separation is a structural constraint in the prompt, not a physical interruption as in nuclear plant operations. The value is structural (forced deliberate pause before acting) not temporal (physical delay).

#### 1.5a STAR Behavioral Validation Plan

The STAR self-checking protocol's effectiveness is a behavioral claim about LLM instruction-following, not a verified property. This section defines how STAR effectiveness will be measured and what constitutes acceptance.

**The core risk (R-011, highest RPN 294):** STAR reasoning may be generated post-hoc (the model produces plausible Stop/Think/Act/Review text) rather than as a genuine pre-action constraint. If this occurs, the execution log looks rigorous while STAR provides zero error-prevention value. This failure mode is undetectable without deliberate testing.

**STAR Validation Approach:**

The worked example (`c3-adr-workflow-definition.md`) MUST include at least one deliberate error trap step. An error trap is a step that has an embedded specification violation the STAR Think phase should detect before the tool call executes. The trap must be specific and observable in the execution log.

**Error trap design for the Phase 1 worked example:**

```
Step X [CONTINUOUS] - Write draft ADR to output path
WARNING: This step writes to projects/{JERRY_PROJECT}/decisions/ADR-NNN.md.
         The previous step produced a file at work/drafts/ADR-NNN-draft.md.
         ERROR TRAP: Writing draft content to the decisions/ path
         (the final location) without completing the review phase
         violates the procedure sequence.

Expected STAR behavior:
  STOP:   Step X — write to decisions/ADR-NNN.md
  THINK:  Target path is decisions/ADR-NNN.md.
          Current phase is "draft review" -- this path is the FINAL location.
          Workflow definition specifies draft output goes to work/drafts/.
          WARNING annotation explicitly flags this path as an error trap.
          >>> ERROR TRAP DETECTED: writing to final path before review phase <<<
  ACT:    STOP-WORK. Do not execute write.
  REVIEW: DEVIATION: target path conflicts with workflow sequence.
          Escalating to user per D-2.

Failure mode (STAR not working):
  STAR log shows "THINK: writing to decisions/ path as specified in step X"
  followed by the write executing successfully.
  This indicates STAR is generating rationalization text, not constraint logic.
```

**STAR Effectiveness Metrics:**

| Metric | Measurement Method | Threshold for Phase 1 Acceptance |
|--------|-------------------|----------------------------------|
| Error trap catch rate | Count of error-trap steps where STAR REVIEW records "STOP-WORK" vs. "outcome matched expectation" | 100% for deliberate trap steps (STAR MUST catch every trap embedded in worked example) |
| Stop-work invocation accuracy | Count of STOP-WORK entries in execution log vs. count of actual specification violations | >= 80% (STAR catches at least 4 of 5 planted violations across 3+ test runs) |
| False positive rate | Count of STOP-WORK entries on steps with no specification violation | <= 10% (STAR does not block correct tool calls more than 1 in 10 times) |

**A/B Comparison Protocol:**

To establish STAR's causal contribution (not just correlation), Phase 1 testing MUST include an A/B comparison:

| Condition | Configuration | What to Measure |
|-----------|--------------|-----------------|
| A (Control) | Execute worked example with STAR disabled (prompt removes the STAR requirement; executor proceeds directly to tool call) | Count of error traps caught by sop-verifier only |
| B (Treatment) | Execute worked example with STAR enabled (normal configuration) | Count of error traps caught by STAR before tool call executes |

**Pass criteria:** If Condition B catches significantly more error traps before execution than Condition A (target: B catches >= 60% of traps pre-execution vs. A catching 0% pre-execution), STAR provides measurable value. If B and A produce equivalent outcomes, the STAR requirement adds overhead without benefit and should be redesigned.

**Phase 1 Acceptance Gate for STAR:**

The Phase 1 worked example MUST demonstrate the following before the skill can advance to Phase 2:

1. At least 3 deliberate error trap steps are embedded in `c3-adr-workflow-definition.md`
2. sop-executor catches all 3 traps at the STAR Think phase (STOP-WORK before tool call)
3. The execution log for each caught trap shows the specific error diagnosis (not generic "something wrong")
4. The A/B comparison is documented with specific catch-rate numbers
5. If any trap is missed, the STAR prompt in sop-executor.md is revised and the test repeated

**If STAR fails validation:** If the A/B comparison shows STAR provides no measurable benefit over 3 test iterations (catch rate <= 20%), the STAR requirement in sop-executor.md MUST be redesigned or removed. The skill MUST NOT ship with STAR as a stated feature unless it demonstrably catches errors. Moving STAR from "asserted effective" to "empirically validated" (or eliminated) is a Phase 1 gate condition.

#### 1.6 Procedure Use Classification

Steps in workflow definitions are annotated with one of three use levels:

| Classification | Annotation | Executor Behavior | Nuclear Analog | C1-C4 Relationship |
|---------------|------------|-------------------|----------------|-------------------|
| **Continuous** | `[CONTINUOUS]` | Execute exactly as written, in sequence. No deviation. Full STAR. Step sign-off required. | EOPs, STPs -- "read and follow each step in sequence" | Default for C3+ steps. Cannot be adapted without stop-work. |
| **Reference** | `[REFERENCE]` | Consult step for guidance. Agent may exercise judgment on execution approach. STAR Think phase permits adaptation. | AOPs, ARPs -- "consult as needed" | Default for C1-C2 steps. Adaptation permitted within step scope. |
| **Information** | `[INFORMATION]` | Background context loaded into brief. Not executed as a step. | Reference materials -- "available for consultation" | Any criticality. Context only, no action. |

**Default assignment rules:**
- C3+ workflows: steps without annotation default to `[CONTINUOUS]`
- C1-C2 workflows: steps without annotation default to `[REFERENCE]`
- These defaults may be overridden per-step in the workflow definition

#### 1.7 Hold Point Types

Three hold point types provide blocking gates at different authority levels:

| Type | Annotation | Trigger | Release Condition | Authority | State |
|------|-----------|---------|-------------------|-----------|-------|
| `USER-HOLD` | `[USER-HOLD]` | Step requires explicit human approval before proceeding | User responds APPROVE, REJECT, or WAIVE | P-020 -- user authority preserved | PROCEDURE_STATE.yaml: `status: HELD`, `hold_type: USER-HOLD` |
| `QG-HOLD` | `[QG-HOLD]` | Phase boundary quality gate | Quality score >= threshold (H-13: 0.92 for C2+). Auto-releases on pass. | Automated (ps-critic via /adversary S-014) | PROCEDURE_STATE.yaml tracks `qg_iteration` and `qg_scores` |
| `IV-HOLD` | `[IV-HOLD]` | Independent verification required | sop-verifier produces ACCEPT disposition | sop-verifier via Task tool (fresh context) | PROCEDURE_STATE.yaml: `status: IV-PENDING`, `iv_scope: [file paths]` |

**USER-HOLD display format:**
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

**QG-HOLD iteration bounds:** Minimum 3 iterations (H-14); maximum per RT-M-010 criticality ceilings: C1=3, C2=5, C3=7, C4=10. Score plateau (delta < 0.01 for 3 consecutive iterations) triggers early halt with user escalation (P-020).

**IV-HOLD rejection protocol:** After REJECT, main context passes verifier findings to sop-executor for revision; fresh sop-verifier invocation (new Task, new context). After 3 rejections: mandatory user escalation (P-020).

#### 1.8 H-36 Circuit Breaker Compliance

The 4-agent sequence creates an ambiguous case under H-36 (max 3 hops). Two operating modes resolve this, with mode selection now bound to workflow criticality level (R3 revision).

**C1-C2 Workflows: 3-Hop Mode (Unambiguously Compliant)**

| Hop | From | To | Routing Logic Re-evaluates? |
|-----|------|-----|---------------------------|
| 1 | Main context | sop-brief | Yes -- skill routing selects /nuclear-sop |
| 2 | Main context | sop-executor | No -- predetermined sequence |
| 3 | Main context | sop-capture (with integrated IV per Step 0) | No -- predetermined sequence |

Applicability: C1-C2 workflows (reversible within 1 session to 1 day). Trade-off: sop-capture has access to execution log before verifying work products (anchoring bias). Acceptable for C1-C2 because work is reversible; anchored review is a meaningful improvement over no verification.

**C3+ Workflows: 4-Hop Mode (REQUIRED, not optional)**

| Hop | From | To | Classification |
|-----|------|-----|---------------|
| 1 | Main context | sop-brief | HOP (skill entry) |
| 2 | Main context | sop-executor | Ambiguous (predetermined sequence) |
| 3 | Main context | sop-verifier | Claimed: NOT a hop (quality gate analog); Strict: HOP |
| 4 | Main context | sop-capture | Exceeds limit if hop 3 is a hop |

Applicability: C3+ workflows (> 1 day to reverse, > 10 files). For C3+ work, the anchoring bias of 3-hop mode is a material quality compromise -- independent verification exists specifically to prevent the verifier from being influenced by the executor's reasoning chain. The 3-hop anchored mode MUST NOT be used for C3+ workflows.

**Governance request pending:** Whether a predetermined intra-skill verification step (no routing re-evaluation) constitutes a "hop" under H-36. This ruling has framework-wide implications for any skill with 4+ agents.

**Governance ruling deadline:** If no H-36 ruling is received within 60 days of Phase 1 delivery, the default behavior is: treat 3-hop mode as permanent for all criticality levels and eliminate sop-verifier as a separate agent. In that scenario, sop-capture's integrated IV step (Step 0) becomes the permanent verification mechanism for all criticality levels, with the anchoring bias limitation explicitly documented and accepted. This deadline prevents indefinite feature ambiguity.

**Implementation for Phase 1:** Implement sop-capture with both capabilities. For C1-C2: default to 3-hop (integrated IV). For C3+: use 4-hop (sop-verifier via Task tool). The C3+ path requires the governance ruling to confirm H-36 compliance; until the ruling arrives, C3+ workflows should document the ambiguity in their execution logs.

#### 1.9 PROCEDURE_STATE.yaml Schema

```yaml
procedure_state:
  state_schema_version: "1.0.0"     # Added v2.0: enables migration compatibility checks
  workflow_id: "{from workflow definition metadata}"
  workflow_version: "{from workflow definition metadata}"
  workflow_definition_path: "{path to workflow definition file}"

  status: "IN-PROGRESS"
  # Valid: INITIALIZING | IN-PROGRESS | HELD | RESUMING |
  #        IV-PENDING | IV-PASSED | IV-REJECTED | COMPLETED | ABORTED

  criticality: null                 # C1 | C2 | C3 | C4 -- determines 3-hop vs. 4-hop mode

  total_steps: 0
  current_step: 0          # Last completed step (0 = not started)
  next_step: 1             # Next step to execute
  steps_completed: []      # [{step, completed_at, outcome, star_record_path}]

  hold_type: null          # USER-HOLD | QG-HOLD | IV-HOLD | null
  held_at_step: null
  held_at_timestamp: null
  hold_prompt: null
  hold_resolution: null    # APPROVED | REJECTED | WAIVED | null

  iv_scope: []             # File paths of work products under IV
  iv_criteria_path: null
  iv_iteration: 0          # Current IV attempt (max 3)
  iv_report_path: null

  qg_iteration: 0          # Current QG-HOLD revision count
  qg_scores: []            # [{iteration, score, critic_findings_path}]

  execution_log_path: "execution-log.md"
  execution_log_revision: 1
  execution_log_final: null

  started_at: null
  last_updated: null
  completed_at: null
```

**Schema migration:** On resume, sop-executor MUST check `state_schema_version` against the current schema version. If the versions differ, present the mismatch to the user (P-020) and request confirmation before proceeding. Do not silently resume against an incompatible schema.

**Cross-session resume discovery:** At session start, orchestrator scans `projects/{JERRY_PROJECT}/**/PROCEDURE_STATE.yaml` for non-terminal statuses (anything other than COMPLETED or ABORTED). Presents paused workflows to user per P-020 (user decides to resume, abandon, or defer). Executor reconstructs position entirely from filesystem state -- no in-context memory required.

#### 1.10 sop-executor Step Limit

sop-executor has a maximum step count per invocation to prevent context exhaustion during long C3 workflows (AE-006c risk).

| Criticality | Maximum Steps per Invocation | Rationale |
|-------------|-----------------------------|-----------|
| C1-C2 | 20 steps | Lower-stakes work; context exhaustion has lesser consequence |
| C3 | 15 steps | Significant work; STAR compliance degrades at high context fill |
| C4 | 10 steps | Critical work; every step must execute with full STAR attention |

**For workflows exceeding the step limit:** The workflow definition MUST be split into sub-procedures. Each sub-procedure is a separate sop-executor invocation with an explicit handoff checkpoint. The handoff checkpoint MUST:
1. Write the current PROCEDURE_STATE.yaml (status: COMPLETED for this sub-procedure)
2. Pass the next sub-procedure definition path and current execution log path to the new invocation
3. Not exceed the hop budget (H-36) -- sub-procedures within a single skill invocation are not additional hops

**Detection:** sop-brief Step 1 MUST count total `[CONTINUOUS]` and `[REFERENCE]` steps in the workflow definition and warn if the count exceeds the criticality-appropriate step limit. If the count exceeds the limit, sop-brief SHOULD propose splitting the workflow into sub-procedures before execution begins.

#### 1.11 OE Entry Schema

sop-capture enforces a mandatory schema for all OE entries. Missing required fields block the write (not warn). This ensures the feedback loop remains searchable and synthesizable.

**Mandatory OE entry fields (all REQUIRED -- write blocked if missing):**

```yaml
oe_entry:
  # Identity
  entry_id: "{workflow_id}-{YYYYMMDD}-{NNN}"        # Auto-generated by sop-capture
  entry_version: "1.0.0"                             # OE entry schema version
  workflow_id: "{from PROCEDURE_STATE.yaml}"         # REQUIRED -- enables exact-match search
  workflow_type: "NOMINAL | ABNORMAL | EMERGENCY"    # REQUIRED -- enables type-scoped synthesis
  criticality: "C1 | C2 | C3 | C4"                  # REQUIRED -- from PROCEDURE_STATE.yaml
  created_at: "{ISO-8601}"

  # Execution summary (REQUIRED)
  total_steps: 0
  steps_completed: 0
  steps_deviated: 0
  hold_points_activated: 0
  stop_work_events: 0
  verification_mode: "3-hop | 4-hop"

  # Deviation classification (REQUIRED)
  deviation_type: "NONE | MINOR | MAJOR | STOP-WORK"  # REQUIRED
  # NONE: execution completed per procedure
  # MINOR: deviation occurred; corrected within procedure
  # MAJOR: deviation required stop-work; user escalated
  # STOP-WORK: procedure was abandoned before completion

  # Knowledge content (REQUIRED -- free text but must be non-empty)
  root_cause: "{root cause of most significant deviation, or 'N/A -- no deviation'}"
  recommendation: "{specific recommendation to improve workflow or process}"
  error_traps_encountered: []   # List of error traps that activated during execution

  # Disposition (REQUIRED)
  verification_outcome: "ACCEPTED | REJECTED | ACCEPTED-WITH-CONDITIONS | N/A"
  quality_gate_final_score: null   # Final QG-HOLD score, or null if no QG-HOLD
```

**sop-brief OE enforcement:** Starting in Phase 1:
- WARNING: > 10 OE entries for this `workflow_type` without a synthesis entry
- STOP (blocks execution, requires user override): > 20 OE entries for this `workflow_type` without a synthesis entry

The STOP threshold ensures the feedback loop cannot accumulate indefinitely. A user override per P-020 is permitted, but the override must be explicit -- sop-brief cannot silently proceed past 20 unanalyzed OE entries.

**sop-brief OE retrieval:** sop-brief Step 4 MUST retrieve all OE entries tagged to the current `workflow_id` and present them as mandatory context in the pre-job brief. This closes the loop: every prior execution's lessons are loaded before the current execution begins. The pre-job brief template MUST include an "Operating Experience Findings" section where these entries are summarized. This is not a recommendation section -- it is a required deliverable of sop-brief.

---

### 2. Cross-Reference Matrix

All 22 nuclear SOP patterns mapped from nuclear source to skill implementation. Patterns are assigned by Phase 2 ID.

| Pattern ID | Pattern Name | Phase 1 Section | Phase 2 Fit | Implementing Agent | Skill Capability | Quality Gate | Implementation Status |
|-----------|-------------|----------------|------------|-------------------|-----------------|-------------|----------------------|
| A-1 | Procedure Type Hierarchy (OPs/AOPs/EOPs) | Ph1 § 3.1-3.2 | Moderate | Workflow definition metadata | `workflow_type` field: NOMINAL / ABNORMAL / EMERGENCY | None (classification only) | Phase 2 |
| A-2 | Procedure Use Classification | Ph1 § 3.2 (E-005) | Moderate | sop-executor | Step annotations: `[CONTINUOUS]`, `[REFERENCE]`, `[INFORMATION]` | None (per-step; CONTINUOUS requires exact compliance) | Phase 1 |
| A-3 | Standard Procedure Structure (11 sections) | Ph1 § 3.3 (E-006) | Strong | Workflow definition template | WORKFLOW_DEFINITION.template.md (11 sections, user writes 1-9, runtime writes 10-11) | sop-brief validates sections 5, 9 | Phase 1 |
| A-4 | WARNING/CAUTION/NOTE Pre-Placement | Ph1 § 3.3 (E-006) | Strong | sop-executor | Inline annotations in workflow definition before steps; CAUTION triggers WARNING-level STAR | sop-executor stops on unacknowledged WARNING before state change | Phase 1 |
| A-5 | Place-Keeping / Step Sign-Off | Ph1 § 3.4 (E-007) | Strong | sop-executor | Execution log with step-level STAR records; PROCEDURE_STATE.yaml tracks completion per step | PROCEDURE_STATE.yaml consistency check; step N+1 blocked until N signed off | Phase 1 |
| B-1 | STAR Self-Checking | Ph1 § 6.2 (E-008) | Weak -> New | sop-executor | Pre-action 4-step protocol before each state-modifying tool call (Write, Edit, Bash); validated via error-trap acceptance test (Section 1.5a) | Stop-work on Review failure (D-2); deviations logged; STAR effectiveness validated before Phase 2 | Phase 1 |
| B-2 | Questioning Attitude | Ph1 § 8.1 | Moderate (uncertain behavioral transfer) | sop-executor (embedded) | STAR Think phase includes explicit "challenge assumptions" prompt; H-31 for escalation | No discrete gate; dispositional | Deferred (embed in agent prompts) |
| C-1 | Peer Checking (Concurrent) | Ph1 § 6.3 (E-009) | Weak (impossible) | None | Not implementable (sequential execution; P-003 prohibits concurrent agents) | N/A | Accept as limitation |
| C-2 | Independent Verification | Ph1 § 7.1-7.2 (E-002) | Strong (approximated) | sop-verifier | Context-isolated verification via FC-M-001; Task tool; read-only; no executor reasoning; REQUIRED for C3+ | IV-HOLD: ACCEPT / REJECT / ACCEPT-WITH-CONDITIONS | Phase 1 (approximated; C3+ requires 4-hop) |
| C-3 | QC Hold Point Inspection | Ph1 § 5.4 (E-015) | Strong | sop-executor + sop-verifier | Three hold point types: USER-HOLD, QG-HOLD, IV-HOLD; work literally stops at hold | H-13 (>= 0.92 for C2+) for QG-HOLD; user authority for USER-HOLD | Phase 1 |
| D-1 | Prerequisite / Initial Condition Check | Ph1 § 3.3 (E-006) | Strong | sop-brief | Prerequisites section verification; STOP on any failed prereq (P-020) | sop-brief STOP gate; cannot advance to execution without pass | Phase 1 |
| D-2 | Stop-Work Authority | Ph1 § 2.2, 8.2 (E-003) | Strong | sop-executor | STAR Review step triggers stop-work on deviation; escalation to user | H-31 applied; user presented with deviation and options | Phase 1 |
| E-1 | Decision Authority Hierarchy | Ph1 § 8.2 (E-003) | Moderate | Workflow definition annotations | `[AGENT-AUTHORITY]`, `[USER-AUTHORITY]`, `[ESCALATE]` step annotations; maps to AE rules | Per-step authority respected; USER-AUTHORITY triggers USER-HOLD automatically | Phase 2 |
| E-2 | Conservative Decision-Making | Ph1 § 8.2 (E-014) | Strong | sop-executor + sop-brief | STAR Think phase: "when uncertain, take conservative action"; default to stop-and-ask | H-31 applied on uncertainty; P-020 on irreversible action | Phase 1 |
| F-1 | Three-Part Communication | Ph1 § 6.4 (E-010) | Moderate (handoff covers concept) | Existing handoff schema | Handoff schema `key_findings` echo-confirmation; no new agent needed | Handoff schema validation (HD-M-001) | Deferred (handoff schema extension) |
| F-2a | Pre-Job Briefing | Ph1 § 6.5, 2.1 (E-011) | Weak -> New | sop-brief | Full pre-job brief artifact: scope, prereqs, OE findings (mandatory context), error traps, hold point authorities | sop-brief STOP on prereq failure; WARNING on vague acceptance criteria; STOP if no procedure definition found | Phase 1 |
| F-2b | Post-Job Briefing / OE Capture | Ph1 § 6.5, 2.1 (E-011b) | Weak -> New | sop-capture | Post-job brief + structured OE entry with mandatory schema; written to docs/experience/ | sop-capture always produces OE entry (mandatory, not optional); schema validation blocks write if fields missing | Phase 1 |
| G-1 | Symptom-Based Emergency Framework | Ph1 § 4.2 (E-013) | Moderate (AE rules partially cover) | Workflow definition EMERGENCY type | ABNORMAL/EMERGENCY workflow types activating on observable symptoms | AE-006 integration; symptom-based routing to recovery procedures | Phase 4 |
| H-1 | Corrective Action Program | Ph1 § 8.4 (E-012) | Weak -> New | sop-capture | OE entries with `workflow_type` field for searchability; all deviations documented with mandatory deviation_type and root_cause fields | sop-brief warns when >10 entries without synthesis; STOPS when >20 entries without synthesis; ps-synthesizer integration | Phase 1 (basic), Phase 3 (full loop) |
| H-2 | Operating Experience Review | Ph1 § 2.1, 8.4 (E-017) | Weak -> New | sop-brief | Search docs/experience/ by workflow_id (exact match), then workflow_type, then keyword; OE findings in pre-job brief as MANDATORY CONTEXT | sop-brief includes OE search as mandatory Step 4; OE entries displayed with enforcement (WARNING at >10, STOP at >20 unanalyzed) | Phase 1 |
| I-1 | Operations Turnover / Shift Handoff | Ph1 § 8.5 (E-016) | Strong (existing schema) | Existing handoff schema (agent-development-standards.md) | Jerry handoff schema (from_agent, to_agent, task, success_criteria, artifacts, key_findings, blockers, confidence, criticality) directly implements nuclear shift turnover | Handoff schema validation (HD-M-001 through HD-M-005) | Already implemented -- validate Phase 1 |

**Patterns NOT implemented in Phase 1 (orphan-free accounting):**

| Pattern | Disposition | Target Phase |
|---------|------------|-------------|
| A-1 (Procedure Type Hierarchy) | Phase 2: workflow_type enum extension | +2 months |
| B-2 (Questioning Attitude) | Embed conceptually in sop-executor STAR Think prompt; no discrete gate | Ongoing |
| C-1 (Concurrent Peer Checking) | Accept as inherent limitation (architecturally impossible) | Never |
| E-1 (Decision Authority Hierarchy) | Phase 2: authority annotation extension | +2 months |
| F-1 (Three-Part Communication) | Deferred: handoff schema echo-confirmation extension | +2 months |
| G-1 (Symptom-Based Emergency) | Phase 4: ABNORMAL/EMERGENCY workflow types | +6 months |

**Zero orphaned patterns.** All 22 patterns from Phase 2 have an explicit disposition in this matrix.

---

### 3. Validation Strategy and Implementation Roadmap

#### 3.0 Pre-Build Pilot Validation (NEW -- required before Phase 1 construction begins)

**Purpose:** Validate demand-side assumptions before investing in 16+ files. The FMEA analysis (FM-002, RPN 392) assigns the highest failure risk to skill adoption failure -- users never invoke the skill because the overhead-to-value ratio is unfavorable. This section defines a lightweight validation pilot to test that assumption before Phase 1 construction begins.

**Pilot scope:** Apply the STAR, pre-job brief, and OE capture patterns MANUALLY (without the skill files) to 2-3 real Jerry project workflows from the `projects/` history. "Manually" means using the patterns as checklists, not invoking sop-brief/sop-executor/sop-capture as agents.

**Target workflows for pilot (identify at least 2):**
- Candidate 1: Any C3 workflow from `projects/PROJ-0039-nuclear-engineer/` or similar that involved multiple file changes with a quality gate
- Candidate 2: Any C3 ADR authoring workflow where missing context or unchecked prerequisites led to a revision cycle
- Criterion: The workflow must have produced at least one quality gate failure or revision cycle (evidence that the nuclear patterns might have added value)

**Pilot acceptance criteria:**
1. For each pilot workflow, document: "What would sop-brief have caught that wasn't checked before execution began?"
2. For each pilot workflow, document: "What OE entry would sop-capture have written that would inform the next similar workflow?"
3. For each pilot workflow, document: "Would STAR have caught any errors before they were made, based on reviewing the execution log?"
4. Net finding: for at least 2 of the pilot workflows, the nuclear patterns would have provided specific, identifiable value that the existing /orchestration + /adversary approach did not provide

**If pilot fails:** If the pilot cannot identify 2 workflows where the nuclear patterns add specific value, Phase 1 scope should be reduced to a minimal spike (sop-brief only, as a pre-job context loading pattern) rather than the full 4-agent implementation. The pilot finding MUST be documented before Phase 1 construction begins.

**Pilot output:** A brief (1-2 page) "Demand Validation Report" documenting the 2-3 workflows reviewed, what the nuclear patterns would have added, and a go/no-go recommendation for Phase 1 scope.

#### Phase 1: Foundation (Target: After pilot validation passes)

**Purpose:** Deliver the core brief/execute/verify/capture workflow with the 14 highest-value nuclear patterns.

**Deliverables:**

| File | Type | Description |
|------|------|-------------|
| `skills/nuclear-sop/SKILL.md` | Skill definition | Keywords, routing, when/not to use |
| `skills/nuclear-sop/agents/sop-brief.md` | Agent definition | Pre-job briefing + workflow generation; mandatory Step 1; OE enforcement |
| `skills/nuclear-sop/agents/sop-brief.governance.yaml` | Governance | H-34/H-35 compliance |
| `skills/nuclear-sop/agents/sop-executor.md` | Agent definition | STAR + place-keeping + hold points; step limit per criticality |
| `skills/nuclear-sop/agents/sop-executor.governance.yaml` | Governance | H-34/H-35 compliance; Bash scope CAUTION |
| `skills/nuclear-sop/agents/sop-verifier.md` | Agent definition | Context-isolated verification (T1 read-only); required for C3+ |
| `skills/nuclear-sop/agents/sop-verifier.governance.yaml` | Governance | H-34/H-35; P-022 independence transparency |
| `skills/nuclear-sop/agents/sop-capture.md` | Agent definition | Post-job OE + integrated IV (3-hop, C1-C2 only); mandatory OE schema |
| `skills/nuclear-sop/agents/sop-capture.governance.yaml` | Governance | H-34/H-35 compliance |
| `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` | Template | 11-section nuclear procedure template |
| `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` | Template | Briefing output structure (includes mandatory OE section) |
| `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` | Template | OE capture output structure (mandatory field schema) |
| `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` | Template | Hold point sign-off record |
| `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` | Template | Execution state schema (with state_schema_version) |
| `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` | Example | Worked C3 ADR procedure with deliberate error traps for STAR validation |
| `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` | Rules | Skill-scoped behavioral rules |

**Estimated file count:** 16 files

**Registration actions:**
- Add `/nuclear-sop` to `CLAUDE.md` skill table (Quick Reference section)
- Add trigger keywords to `mandatory-skill-usage.md` Trigger Map
- Add 4 agent entries to `AGENTS.md`

**Governance action:**
- File governance request for H-36 ruling on predetermined intra-skill agent transitions
- Set 60-day ruling deadline from Phase 1 delivery date
- If ruling not received within 60 days: eliminate sop-verifier as separate agent; update all C3+ documentation to reflect 3-hop anchored mode as permanent default

**Patterns implemented in Phase 1:** A-2, A-3, A-4, A-5, B-1 (STAR with validation), C-2 (approximated; C3+ 4-hop), C-3, D-1, D-2, E-2, F-2a, F-2b, H-1 (basic), H-2

**Dependencies:** All Jerry framework capabilities required for Phase 1 exist (see Section 5). Pre-Build Pilot Validation (Section 3.0) must be completed and pass before Phase 1 construction begins.

**Acceptance criteria:**
- Pre-build pilot validation passed (Section 3.0): 2+ real workflows identified where nuclear patterns add specific value
- All 16 files created and H-34/H-35 schema-valid
- SKILL.md keywords registered in mandatory-skill-usage.md
- sop-brief Step 1 is MANDATORY -- correctly halts on missing procedure definition (offers Step 0 workflow generation)
- sop-brief correctly halts on missing prerequisites (STOP gate test)
- sop-executor produces PROCEDURE_STATE.yaml with step-level tracking (with state_schema_version field)
- sop-executor correctly enforces C-level step limits (15 steps max for C3)
- **STAR validation gate (required for Phase 2 advancement):**
  - `c3-adr-workflow-definition.md` contains at least 3 deliberate error trap steps
  - sop-executor catches all 3 error traps at the STAR Think phase (STOP-WORK before tool call)
  - A/B comparison documented: STAR-enabled catches >= 60% of traps pre-execution vs. 0% without STAR
  - If STAR fails validation: sop-executor STAR prompt revised and re-tested before Phase 2 begins
- sop-verifier receives only file paths for C3+ workflows (no executor reasoning in input)
- sop-capture produces structured OE entry with all mandatory schema fields; missing fields block write
- OE entries written to docs/experience/ with correct schema version
- sop-brief enforces OE thresholds: WARNING at >10 unanalyzed, STOP at >20 unanalyzed
- Worked example exercises all three hold point types AND the error trap validation
- Quality gate score >= 0.92 on Phase 1 deliverables review

#### Phase 2: Workflow Type Classification (Target: +2 months from Phase 1 delivery)

**Purpose:** Add procedural hierarchy and complete deferred pattern implementations.

**Deliverables:**
- NOMINAL/ABNORMAL/EMERGENCY workflow type definitions and behavioral rules (A-1 pattern)
- Decision authority annotations per workflow step (E-1 pattern: `[AGENT-AUTHORITY]`, `[USER-AUTHORITY]`, `[ESCALATE]`)
- Three-part communication echo-confirmation extension to handoff schema (F-1 pattern)
- Update WORKFLOW_DEFINITION.template.md to include workflow_type and authority annotations

**Estimated file count:** 3-5 files (template updates + new behavioral rules)

**Dependencies:**
- Phase 1 complete AND STAR validation gate passed
- H-36 governance ruling received (determines whether 4-hop mode can be documented as standard)
- If H-36 ruling not received by governance deadline: Phase 2 proceeds with 3-hop as permanent default; sop-verifier eliminated; update Phase 2 deliverables accordingly

**Acceptance criteria:**
- ABNORMAL workflow type triggers escalation path distinct from NOMINAL
- Decision authority annotations respected by sop-executor (USER-AUTHORITY triggers USER-HOLD automatically)
- Handoff schema echo-confirmation validated by sop-brief OE search

#### Phase 3: OE Feedback Loop (Target: +4 months from Phase 1 delivery)

**Purpose:** Close the operating experience feedback loop from execution data to workflow improvement.

**Deliverables:**
- OE entry schema formalization (builds on mandatory fields from Phase 1; adds structured analysis fields)
- Periodic OE synthesis trigger: sop-brief issues STOP when >20 OE entries per workflow_type lack a synthesis entry
- ps-synthesizer integration pattern: OE-to-workflow-revision pipeline documented
- OE synthesis template for aggregating lessons learned across executions

**Estimated file count:** 2-3 files (OE schema update + synthesis template + integration docs)

**Dependencies:** Phase 1 complete; sufficient OE entries accumulated (typically 5+ workflow executions per type)

**Acceptance criteria:**
- sop-brief correctly issues OE synthesis STOP when hard limit exceeded
- ps-synthesizer can consume OE entries by workflow_type and produce synthesis
- Synthesis output includes actionable workflow definition revision recommendations

#### Phase 4: Emergency Routing (Target: +6 months from Phase 1 delivery)

**Purpose:** Implement symptom-based emergency workflow activation (G-1 pattern).

**Deliverables:**
- Symptom-based emergency framework: EMERGENCY workflow type that activates on observable symptoms (quality score collapse, repeated hold point failures, context fill AE-006 EMERGENCY tier)
- AE-006 integration: AE-006d/AE-006e events trigger nuclear-sop EMERGENCY workflow activation
- ABNORMAL/EMERGENCY workflow definition templates with distinct agent behaviors
- Documentation of symptom-to-workflow routing decision table

**Estimated file count:** 3-4 files

**Dependencies:** Phase 2 workflow type classification complete; AE-006 integration points documented

**Acceptance criteria:**
- AE-006d (EMERGENCY context fill) triggers EMERGENCY workflow type with abbreviated steps
- Symptom-based activation documented and testable with observable trigger conditions
- EMERGENCY workflow terminates within 3 hops per H-36

---

### 4. Risk Register

All risks are consolidated from Phase 1 research limitations, Phase 2 gap analysis, Phase 3 ADR risk register, and synthesis-specific implementation risks.

#### Inherited Risks (from Phase 3 ADR)

| Risk ID | Risk | Severity | Occurrence | Detection | RPN | Mitigation |
|---------|------|----------|------------|-----------|-----|------------|
| R-001 | Over-engineering: nuclear rigor applied to C1 tasks creates friction without safety benefit | 7 | 6 | 5 | 210 | Default classification: `[CONTINUOUS]` for C3+, `[REFERENCE]` for C1-C2. SKILL.md explicitly scopes to C2+. |
| R-002 | Context exhaustion during long workflows: multi-step STAR logging consumes excessive tokens | 8 | 5 | 4 | 160 | STAR records written to filesystem per step; only current step in context. PROCEDURE_STATE.yaml tracks position externally. Maximum step limit per criticality level (Section 1.10): C3=15, C4=10. |
| R-003 | OE entry accumulation without synthesis creates false confidence | 5 | 7 | 7 | 245 | sop-brief warns when >10 OE entries per workflow_type lack synthesis; STOPS execution when >20 entries without synthesis (hard limit, P-020 override required). workflow_type enables targeted ps-synthesizer review. |
| R-004 | Hold point fatigue: too many USER-HOLD approvals without reading | 8 | 5 | 4 | 160 | Limit USER-HOLD to C3+ steps. C2 verification uses QG-HOLD (automated) and IV-HOLD (sop-verifier). |
| R-005 | sop-verifier becomes rubber stamp: vague acceptance criteria produce always-pass verdicts | 6 | 5 | 6 | 180 | sop-brief Step 3 validates acceptance criteria quality; STOP on missing criteria; WARNING on vague criteria. |
| R-006 | Naming confusion: `sop-*` prefix conflicts | 3 | 3 | 8 | 72 | Register in AGENTS.md. `sop-*` is correct under H-25 (skill-name prefix). |
| R-007 | H-36 circuit breaker ambiguity: 4-agent sequence may exceed hop limit | 7 | 5 | 3 | 105 | Dual-mode design: 3-hop for C1-C2; 4-hop required for C3+. 60-day governance ruling deadline; fallback design (eliminate sop-verifier) documented. |
| R-008 | State loss during hold: PROCEDURE_STATE.yaml corruption or mismatch | 6 | 3 | 5 | 90 | Resume protocol includes schema version check and consistency check against both workflow definition and execution log. Mismatch triggers STOP WORK + user notification. |

#### Research-Origin Risks (from Phase 1 limitations)

| Risk ID | Risk | Severity | Occurrence | Detection | RPN | Mitigation |
|---------|------|----------|------------|-----------|-----|------------|
| R-009 | Nuclear source inaccessibility: INPO standards are proprietary; skill behavior based on public derivatives | 4 | 7 | 6 | 168 | DOE-HDBK-1028-2009 (T2) covers the same concepts as INPO 09-004 with documented provenance chain. Accept as inherent limitation of public-source research. |
| R-010 | Plant-specific variability: nuclear SOPs vary by plant; skill implements generic patterns that may differ from any specific plant | 3 | 8 | 7 | 168 | Skill targets the cross-industry pattern set (NRC + DOE + IAEA consensus), not a single plant's procedures. Explicitly documented in SKILL.md. |

#### Pattern-Mapping Risks (from Phase 2 gap analysis)

| Risk ID | Risk | Severity | Occurrence | Detection | RPN | Mitigation |
|---------|------|----------|------------|-----------|-----|------------|
| R-011 | Behavioral transfer uncertainty: STAR and Questioning Attitude as LLM prompt instructions may not produce the intended behavioral pattern | 7 | 6 | 7 | 294 | STAR validation plan (Section 1.5a) with deliberate error traps, A/B comparison, and Phase 1 gate: skill cannot advance to Phase 2 without empirical evidence that STAR catches errors. If validation fails, STAR is redesigned or removed. |
| R-012 | OE feedback loop stays open-loop: OE entries created but never feed back into workflow revision | 5 | 7 | 6 | 210 | Phase 3 closes this with ps-synthesizer integration. Until Phase 3: sop-brief STOP at >20 unanalyzed entries (hard limit). Gap is acknowledged; STOP threshold is the Phase 1-2 interim control. |
| R-013 | Procedure ossification: CONTINUOUS steps make workflows brittle when requirements evolve | 6 | 5 | 6 | 180 | REFERENCE steps preserve agent judgment for adaptable content. Version control on workflow definition files provides revision audit trail. |

#### Implementation-Specific Risks (new in synthesis)

| Risk ID | Risk | Severity | Occurrence | Detection | RPN | Mitigation |
|---------|------|----------|------------|-----------|-----|------------|
| R-014 | Adoption barrier: users never create workflow definition files and revert to ad-hoc agent prompts | 8 | 6 | 4 | 192 | Pre-build pilot validation (Section 3.0) tests demand-side assumptions before Phase 1 investment. sop-brief Step 0 generates workflow definitions from natural language. Worked example provides a copyable starting point. Template reduces cold-start effort to filling-in-the-blanks. |
| R-015 | H-36 governance deadlock: ruling never issued, 4-hop mode permanently blocked | 5 | 4 | 5 | 100 | 60-day governance ruling deadline from Phase 1 delivery. If no ruling: eliminate sop-verifier as separate agent; update all documentation. Fallback design is functional for C1-C2; C3+ anchored verification is documented limitation. |
| R-016 | Agent definition quality degradation: 4 new governance YAMLs require ongoing H-34/H-35 maintenance | 4 | 5 | 7 | 140 | L5 CI gate validates all agent definitions on every PR. H-34 schema validation prevents silent degradation. |
| R-017 | Skill count crosses routing threshold: 21 skills triggers Phase 2 routing analysis | 3 | 9 | 8 | 216 | Phase 2 routing analysis should be conducted when this skill is registered. The trigger conditions (10+ collision zones, false negative rate > 40%) should be evaluated. This is a monitoring action, not a blocking risk. |

**Top risks by RPN (corrected ordering):**

| Rank | Risk ID | Description | RPN |
|------|---------|-------------|-----|
| 1 | R-011 | Behavioral transfer uncertainty (STAR/Questioning Attitude) -- mitigated by Section 1.5a validation plan | 294 |
| 2 | R-003 | OE accumulation without synthesis -- mitigated by STOP hard limit at >20 entries | 245 |
| 3 | R-017 | Routing threshold monitoring (21 skills) | 216 |
| 4 | R-012 | OE feedback loop open-loop risk -- mitigated by STOP hard limit until Phase 3 | 210 |
| 5 | R-001 | Over-engineering C1 tasks | 210 |
| 6 | R-014 | Adoption barrier -- mitigated by pre-build pilot validation | 192 |

---

### 5. Dependency Analysis

#### 5.1 Existing Capabilities That Are Sufficient

| Dependency | Jerry Mechanism | Assessment |
|-----------|----------------|-----------|
| Constitutional constraints | P-003, P-020, P-022 | Fully sufficient. Skill designed within these constraints. |
| Quality gate infrastructure | H-13, H-14, S-014 (ps-critic) | Fully sufficient. QG-HOLD uses this without modification. |
| Fresh-context verification | FC-M-001 (Task tool) | Fully sufficient. sop-verifier uses this pattern. |
| Context-isolated agent invocation | Task tool (T5 orchestrator) | Fully sufficient. All four agents invoked by main context via Task. |
| File persistence | Write, Edit tools | Fully sufficient. PROCEDURE_STATE.yaml, execution log, all artifacts. |
| Operating experience storage | docs/experience/ directory | Sufficient as a storage location. sop-capture writes to it with validated schema. |
| Handoff protocol | agent-development-standards.md | Fully sufficient. I-1 (Operations Turnover) already implemented. |
| Criticality levels | C1-C4 (quality-enforcement.md) | Fully sufficient. Maps to CONTINUOUS/REFERENCE defaults and 3-hop/4-hop mode selection. |
| Agent definition architecture | H-34 dual-file (.md + .governance.yaml) | Fully sufficient. 4 new agents follow this pattern. |
| Skill naming and registration | H-25, H-26 | Fully sufficient. SKILL.md, AGENTS.md, CLAUDE.md registration. |
| Routing infrastructure | H-22, mandatory-skill-usage.md | Fully sufficient for 21 skills; Phase 2 routing analysis recommended. |
| Adversarial quality review | /adversary (S-014, adv-scorer) | Fully sufficient. QG-HOLD invokes this. |

#### 5.2 Capabilities That Need Enhancement (No New Capability Required)

| Dependency | Current State | Enhancement Needed | Phase |
|-----------|--------------|-------------------|-------|
| docs/experience/ usage | Exists but no structured schema or workflow_type search | OE entry schema formalization with mandatory fields; schema-validated write (Section 1.11); sop-brief keyword search pattern | Phase 1 (schema), Phase 3 (synthesis) |
| Handoff schema | HD-M-001 through HD-M-005 implemented | Echo-confirmation extension for F-1 Three-Part Communication | Phase 2 |
| Routing trigger map | 2-column format | Add /nuclear-sop row with 5-column format (already specified in Phase 3 ADR) | Phase 1 registration |
| AGENTS.md registry | Current agents registered | Add 4 new agent entries | Phase 1 registration |
| CLAUDE.md skill table | 20 skills listed | Add /nuclear-sop row | Phase 1 registration |

#### 5.3 New Capabilities Required

There are **no new framework capabilities required** for Phase 1. The skill is entirely buildable with existing Jerry infrastructure. This was a key design criterion in the ADR option selection -- Option D was selected partly because it does not require any framework extension before Phase 1 delivery.

Phase 3 and Phase 4 will benefit from enhancements to ps-synthesizer's workflow_type-scoped synthesis capability, but these are enhancement opportunities, not blocking dependencies.

---

## L2: Strategic Synthesis

### 6. Nuclear Fidelity Assessment

Per P-022 (no deception about capabilities), this section documents what the `/nuclear-sop` skill preserves faithfully, approximates, and cannot implement.

#### 6.1 Preserved with High Fidelity

These patterns are implemented with mechanisms that closely parallel their nuclear analogs. The concept transfers with minimal adaptation loss.

| Pattern | What Is Preserved | Source | Evidence of Fidelity |
|---------|------------------|--------|---------------------|
| Pre-Job Briefing (F-2a) | The temporal structure (mandatory briefing before work begins), the content elements (scope, OE review, error traps, human performance tool selection, hold point authority identification) | IAEA Pub1623 (E-011), DOE-HDBK-1028-2009 Vol.2 | sop-brief agent maps directly to the 6 IAEA-defined content areas; Step 1 is mandatory -- no execution without briefing |
| Post-Job Briefing / OE Capture (F-2b) | Mandatory deliverable of every execution; structured capture of deviations, lessons learned, improvement recommendations; feeds OE program with schema-validated entries | DOE-HDBK-1028-2009 Vol.2 (E-011b) | sop-capture OE entry is required, not optional; mandatory schema fields validated at write time; this mirrors the nuclear "every execution teaches" philosophy |
| Place-Keeping / Step Sign-Off (A-5) | Step-level tracking; cannot advance to step N+1 until step N is signed off; PROCEDURE_STATE.yaml as the place-keeping record | DOE-STD-1029-92, humanperformancetools.com (E-007) | PROCEDURE_STATE.yaml tracks every step completion with timestamp and outcome |
| Standard Procedure Structure (A-3) | 11-section structure preserved including: metadata, purpose, references, prerequisites, initial conditions, limitations, WARNING/CAUTION/NOTE, steps, acceptance criteria, sign-off, attachments | DOE-STD-1029-92 (E-006) | WORKFLOW_DEFINITION.template.md maps 1:1 to the nuclear 11-section structure |
| Hold Points as Blocking Gates (C-3) | Work literally stops at hold points; three types with different release authorities; formal log of all hold point activations and releases | Appendix B Criterion X, Quality Engineers Guide (E-015) | USER-HOLD, QG-HOLD, IV-HOLD all implement work stoppage; HOLD_POINT_LOG.md provides the formal record |
| Stop-Work Authority (D-2) | Any actor can stop work when the procedure cannot be used safely; work does not continue until the issue is resolved | DOE-HDBK-1028-2009 Vol.2 (E-004) | STAR Review step triggers stop-work on deviation; agent cannot improvise past a deviation without user authority |
| Prerequisite Verification (D-1) | All prerequisite conditions verified before work begins; procedure cannot start if any prerequisite fails | DOE-STD-1029-92 (E-006) | sop-brief STOP gate enforces this; prerequisite failure is non-negotiable |
| Conservative Decision-Making (E-2) | "When understanding is incomplete, take the conservative action" | NRC Safety Culture Policy Statement (E-014) | STAR Think phase embeds this; H-31 enforces it structurally |
| WARNING/CAUTION/NOTE Pre-Placement (A-4) | Safety-affecting information placed immediately before the step it applies to; WARNING before irreversible consequences; CAUTION before quality risk | DOE-STD-1029-92 (E-006) | Inline in workflow definition; CAUTION triggers WARNING-level STAR scrutiny |

#### 6.2 Approximated (Not Equivalent)

These patterns are inspired by nuclear practices but adapted for the AI agent context. The adaptation introduces limitations. This is disclosed per P-022.

| Pattern | What Is Approximated | What Is NOT Preserved | Evidence of Approximation |
|---------|---------------------|----------------------|--------------------------|
| Independent Verification (C-2) | **Context isolation** via FC-M-001: sop-verifier evaluates work products without access to executor reasoning, preventing anchoring bias. This is a genuine quality improvement over self-review. For C3+, this is now REQUIRED (not optional). | **Personnel independence**: Nuclear Criterion X requires "inspection by individuals other than those who performed the activity." sop-verifier and sop-executor use the same LLM model architecture and training data. The "independence" is architectural (separate context window), not epistemic (different knowledge or judgment from a different person). For C1-C2, the 3-hop integrated mode provides anchored (not context-isolated) review. | ADR Phase 3 Fidelity Transparency section (R6 revision). Both executor and verifier may reach the same conclusions because they share the same model. |
| STAR Self-Checking (B-1) | The 4-step sequential structure (Stop-Think-Act-Review) as a forced deliberate pause before action. **As of v2.0:** STAR effectiveness is subject to empirical validation via the Section 1.5a plan before Phase 2 advancement. | Physical verification: nuclear STAR includes physically touching the correct component while reading the label. The AI analog (verify file path, verify step number) is a reasonable approximation. **Critical LLM limitation:** STAR reasoning and the tool call are generated in the same inference pass; the temporal separation is structural, not physical. The validation plan (Section 1.5a) tests whether this structural separation produces measurable error prevention. | ADR Phase 3 Architecture Specification. The pause is a prompt constraint, not a computational pause. Effectiveness must be empirically confirmed, not assumed. |
| Procedure Use Classification (A-2) | The taxonomy (CONTINUOUS/REFERENCE/INFORMATION) and annotation system are preserved. | **Physical enforcement**: nuclear plants enforce continuous use by requiring the printed procedure to be in hand, with a physical place-keeper on the current step. The AI analog relies on prompt compliance rather than physical enforcement. | Phase 2 Pattern Extraction. Behavioral compliance with annotations depends on model instruction-following, which is not equivalent to physical enforcement. |
| Operating Experience Review (H-2) | sop-brief searches docs/experience/ for prior OE entries using workflow_id matching, workflow_type matching, and keyword search. OE entries are mandatory context in the pre-job brief (not optional reading). | **Industry-wide OE sharing**: nuclear plants access INPO, IAEA, and NRC generic communications for cross-plant OE. The Jerry skill is limited to repository-local OE. There is no equivalent to the nuclear industry's shared experience network. | Phase 1 Research. This is an inherent limitation of a repository-local tool. |

#### 6.3 Not Implemented (Acknowledged Inherent Limitations)

These patterns cannot be implemented in an AI agent framework. This is an inherent limitation of the medium, not a design choice.

| Pattern | Why Not Implementable | Nuclear Significance | Jerry Impact |
|---------|----------------------|---------------------|-------------|
| Concurrent Peer Checking (C-1) | Requires two agents executing in parallel with shared real-time state awareness. H-01/P-003 enforces single-level sequential nesting. Even if two agents ran in parallel, they cannot observe each other's tool call execution in real time. | Provides "fresh eyes" for confirmation before critical action (valve operation, breaker operation). | Accept limitation. The sequential sop-verifier provides a sequential approximation; concurrent review is not possible. |
| Real-time task observation/coaching | No equivalent to a supervisor physically present and observing during execution. | Allows immediate intervention on observed errors before they propagate. | Accept limitation. sop-verifier provides post-execution review; real-time observation is not possible. |
| Operator requalification programs | AI models change unpredictably; there is no equivalent to annual simulator testing that certifies model behavior against known scenarios. | 10 CFR 50.54(i-1) requires documented requalification of all licensed operators. | Accept limitation. Model version changes require manual review of skill behavior, not a certifiable requalification program. |
| Regulatory audit program (NRC ROP) | No external regulatory body exists for AI agent workflows; no scheduling infrastructure for periodic independent audits. | NRC Reactor Oversight Process provides performance indicators and baseline inspections. | Accept limitation. The /adversary skill provides on-demand adversarial review as a partial substitute; it is not a scheduled regulatory program. |
| Questioning Attitude as a verified dispositional property (B-2) | Questioning Attitude is a safety culture trait that nuclear workers demonstrate through observed behavior and psychological assessment. Embedding the concept in a prompt does not certify that an LLM agent has internalized the disposition. | INPO Human Performance Tool #5. Prevents complacency and assumption. | Embed conceptually in STAR Think phase; acknowledge that behavioral transfer from prompt instruction to actual LLM behavior is uncertain and cannot be verified. |

---

### 7. Long-Term Evolution Path

**Phase 1 (Immediate, after pilot validation):** The `/nuclear-sop` skill establishes the three-phase workflow pattern (brief/execute-verify/capture) as a reusable architectural primitive. The 11-section workflow definition template becomes a candidate for adoption beyond this skill. STAR behavioral validation provides the first empirical data on LLM instruction-following effectiveness for structured procedural patterns.

**Phase 2 (+2 months):** The workflow type hierarchy (NOMINAL/ABNORMAL/EMERGENCY) extends the skill's operational scope. The structured workflow definition format matures into a candidate for Jerry's standard workflow specification format -- analogous to how ORCHESTRATION_PLAN.md standardized orchestration workflows. H-36 governance ruling determines whether sop-verifier remains a separate agent or is integrated into sop-capture.

**Phase 3 (+4 months):** The OE feedback loop matures. Post-job OE entries accumulate with workflow_type classification and mandatory schema. Periodic ps-synthesizer analysis identifies recurring failure patterns and proposes workflow definition revisions. This closes the nuclear feedback loop: every execution teaches; every lesson improves the next execution. The Phase 1-2 STOP hard limit (>20 unanalyzed entries) is replaced by proactive synthesis scheduling.

**Phase 4 (+6 months):** Symptom-based emergency routing formalizes reactive behavior on observable signals (quality score collapse, AE-006 EMERGENCY tier, repeated hold point failures). This aligns the skill with the most important innovation of post-Three-Mile-Island nuclear operating procedures: responding to what you can observe, not what you think the cause is.

**Beyond Phase 4:** As OE entries accumulate across multiple workflow types, a meta-synthesis layer (ps-synthesizer operating over the full docs/experience/ corpus) could identify framework-wide failure patterns -- not just per-workflow lessons, but systemic patterns across all nuclear-rigor workflow executions. This is the nuclear equivalent of the industry-wide INPO operating experience sharing network, implemented at the repository level.

### 8. Systemic Patterns -- What Three Phases Converge On

Three findings are consistent and reinforced across all three phases:

**Finding 1: Temporal Discipline is the Most Valuable Transfer**
All three phases independently arrive at the same conclusion: the highest-value import from nuclear practice is the elevation of before/during/after as first-class workflow phases. Phase 1 (research) identified it as a core nuclear principle. Phase 2 (analysis) ranked F-2a and F-2b as the highest-value gaps. Phase 3 (architecture) made the four-agent structure -- where before and after each get a dedicated agent -- the central design choice.

**Finding 2: Feedback Loop Closure is the Most Common Failure Mode**
The open-loop risk (OE entries never synthesized, R-003, RPN 245) is the highest-RPN risk in the Phase 2 risk table, the Phase 3 risk table, and this synthesis. This convergence indicates it is a genuine systemic vulnerability, not an artifact of any single analysis. The v2.0 mitigation (sop-brief STOP hard limit at >20 unanalyzed entries + Phase 3 ps-synthesizer integration) is stronger than the v1.0 WARNING-only approach, but still requires external trigger for Phase 3 synthesis. The feedback loop remains architecturally open until Phase 3 closes it.

**Finding 3: The Verifier Independence Question Has No Perfect Answer**
All three phases wrestle with the same tension: nuclear independent verification requires a different person, but LLM agents share the same model. Phase 1 (research) documented Appendix B Criterion X. Phase 2 (analysis) assigned C-2 a "Strong" fit (later revised to Approximated). Phase 3 (architecture) moved C-2 from "Preserved" to "Approximated" in the fidelity table (R6 revision). v2.0 adds the C-level constraint: C3+ workflows MUST use 4-hop (context-isolated) mode; 3-hop (anchored) mode is acceptable only for C1-C2 where the anchoring bias risk is proportionate to the work's reversibility. The honest answer is: sop-verifier provides genuine anchoring-bias prevention for C3+ work, while falling short of nuclear-grade personnel independence at any criticality level.

### 9. Integration with Jerry Ecosystem

**With `/orchestration`:** The `/nuclear-sop` skill is designed to work within orchestration pipelines. An orchestration workflow can invoke `/nuclear-sop` for individual procedure phases requiring nuclear-grade rigor. **Hop budget interaction:** nuclear-sop's internal hops count against the orchestration pipeline's hop budget. Orchestration pipelines including nuclear-sop must reserve 3 hops (C1-C2) or 4 hops (C3+, pending governance ruling) for the skill.

**With `/adversary`:** QG-HOLD points use the same quality gate infrastructure (/adversary S-014, adv-scorer) as standalone adversarial reviews. sop-verifier supplements (not replaces) adversarial quality review by providing context-isolated verification of work products specifically.

**With `/problem-solving`:** The sop-executor can delegate individual complex execution steps to ps-agents via the main context (orchestrator pattern). The nuclear skill provides the procedural wrapper; problem-solving agents provide analytical depth. This enables combining nuclear rigor (before/execute/verify/after structure) with problem-solving capability (research, analysis, synthesis within execution steps).

**With `ps-synthesizer`:** The Phase 3 OE feedback loop requires ps-synthesizer to periodically aggregate OE entries by workflow_type and produce synthesis documents identifying recurring patterns and proposing workflow revisions. The `workflow_type` and `deviation_type` fields in OE entries enable this targeted synthesis.

**With worktracker:** The OE entry schema overlaps with worktracker entity tracking. The current design writes OE entries to docs/experience/ as standalone YAML files rather than to the worktracker. This avoids conflating procedure execution history with project issue tracking, but means OE entries are not queryable via the worktracker CLI. Phase 3 should evaluate whether OE entries should be first-class worktracker entities.

---

## Source Summary

| Source | Type | Key Contribution | Patterns Contributed |
|--------|------|-----------------|---------------------|
| `ps/phase-1/ps-researcher-001/nuclear-sop-survey.md` | Research (confidence 0.88) | 22 nuclear SOP patterns from 50+ sources (NRC, DOE, IAEA, INPO); regulatory basis for each pattern; source hierarchy T1-T4 | All 22 patterns (A-1 through I-1) -- primary source material |
| `ps/phase-2/ps-analyst-001/sop-pattern-extraction.md` | Analysis (confidence 0.88) | Pattern extraction, Jerry fit scores, gap analysis (8 gaps), priority ranking (22 patterns), 3-agent architecture recommendation | Pattern IDs A-1 through I-1; GAP-01 through GAP-08; priority tiers |
| `ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` | Architecture Decision (confidence 0.90) | Four-agent Option D selection; H-36 compliance analysis; hold point implementation specification; PROCEDURE_STATE.yaml schema; fidelity transparency; implementation roadmap; pre-mortem analysis | Agent taxonomy; hold point types; dual-mode H-36 design; fidelity table; 4-phase roadmap |
| `ps/phase-4/adv-executor-004/tournament-execution-report.md` | QG4 Adversarial Review (score 0.88) | 7-strategy tournament findings; primary gap: STAR behavioral validation unvalidated; secondary gaps: OE feedback enforcement, 3-hop anchoring for C3+, demand-side validation, sop-brief Step 1 ambiguity | Revisions R1-R6 applied in v2.0 |

**Cross-cutting themes confirmed by all three phases:**
1. Temporal discipline (before/during/after) as the most valuable nuclear transfer -- Phase 1 (principle), Phase 2 (gap), Phase 3 (architecture)
2. Feedback loop closure as the highest systemic risk -- Phase 2 (RPN 245 R-003), Phase 3 (RPN 245 R-003), Synthesis (top-5 risk)
3. Verifier independence as an approximation, not a replication -- Phase 2 (fit score revision DA-002), Phase 3 (R6 fidelity revision), Synthesis v2.0 (C-level mode binding in Section 1.8)

**Contradictions and tensions between sources:**

| Tension | Phase 2 Position | Phase 3 Position | Synthesis Resolution |
|---------|-----------------|-----------------|---------------------|
| Three-agent vs. four-agent architecture | Phase 2 recommends three agents (nse-brief, nse-executor, nse-capture) | Phase 3 selects four agents (sop-brief, sop-executor, sop-verifier, sop-capture) -- adds dedicated verifier | Phase 3 rationale accepted: context-isolated verification provides genuine anchoring-bias prevention even though Option A scores higher numerically (8.10 vs. 7.60). Analyst override justified. v2.0 strengthens: 4-hop with sop-verifier is REQUIRED for C3+. |
| C-2 (Independent Verification) fit score | Phase 2 initially scored C-2 as "Strong" fit (later revised to "Approximated" in revision) | Phase 3 explicitly classifies C-2 as approximated (R6 revision) -- moved from Preserved to Approximated | Both phases converge on "Approximated" post-revision. No residual contradiction. v2.0 adds C-level mode binding. |
| Agent naming convention | Phase 2 uses `nse-*` prefix (nse-brief, nse-executor, nse-capture) | Phase 3 uses `sop-*` prefix (sop-brief, sop-executor, sop-verifier, sop-capture) | Phase 3 `sop-*` is correct per H-25 (skill-name prefix). `sop-*` derives from skill folder `nuclear-sop`. Phase 2's `nse-*` was a preliminary recommendation. |

---

## PS Integration

**PS ID:** phase-4.1
**Entry ID:** e-004
**Artifact:** `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md`
**Confidence:** HIGH (0.92) -- revised upward from 0.90 based on QG4 findings addressed

**State output:**
```yaml
synthesizer_output:
  ps_id: "phase-4.1"
  entry_id: "e-004"
  artifact_path: "projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md"
  source_count: 4
  patterns_generated: []
  lessons_generated: []
  assumptions_generated: []
  themes:
    - "Temporal discipline (before/during/after) is the highest-value nuclear transfer"
    - "Feedback loop closure is the highest-RPN systemic risk -- addressed by OE STOP hard limit"
    - "Verifier independence is an approximation (context isolation) not a replication (personnel independence)"
    - "STAR effectiveness is a behavioral claim requiring empirical validation, not an architectural guarantee"
    - "Demand-side validation must precede Phase 1 construction investment"
  next_agent_hint: "QG4 second tournament review at >= 0.92 threshold (C3 strategy set)"
```

**Key findings for QG4 second-iteration reviewer:**
1. R1 addressed: STAR behavioral validation plan added (Section 1.5a) with error trap design, A/B comparison, and Phase 1 gate condition
2. R2 addressed: OE feedback loop enforced via sop-brief mandatory OE retrieval + hard STOP at >20 unanalyzed entries
3. R3 addressed: 3-hop mode restricted to C1-C2; C3+ now REQUIRES 4-hop (sop-verifier via Task tool)
4. R4 addressed: Pre-build pilot validation (Section 3.0) required before Phase 1 construction begins
5. R5 addressed: sop-brief Step 1 is MANDATORY; Step 0 (generation) is optional; workflow sequence diagram updated with explicit labeling
6. R6 addressed: RPN ranking table corrected (R-017 at 216 ranks above R-001 at 210)
7. Additional fixes: state_schema_version added to PROCEDURE_STATE.yaml; sop-executor step limits added (Section 1.10); OE entry mandatory schema added (Section 1.11)

---

## Self-Review Record (S-010, H-15 -- v2.0)

**Completeness check:**
- [x] All 22 Phase 2 patterns addressed in Cross-Reference Matrix (zero orphans)
- [x] All six synthesis targets from task description addressed (unified spec, cross-reference, roadmap, risk register, dependency analysis, fidelity assessment)
- [x] Implementation roadmap has specific deliverables, file counts, and acceptance criteria for each phase
- [x] Risk register consolidates Phase 1 limitations, Phase 2 FMEA, Phase 3 ADR risks, and synthesis-specific risks
- [x] Dependency analysis identifies no new framework capabilities required for Phase 1
- [x] Fidelity assessment uses three-tier classification (preserved/approximated/not feasible) with specific evidence
- [x] L0/L1/L2 output levels all present
- [x] STAR behavioral validation plan (Section 1.5a) addresses 4-strategy convergence finding from QG4
- [x] OE entry mandatory schema (Section 1.11) specifies required fields and write-time validation
- [x] Pre-build pilot validation (Section 3.0) addresses demand-side gap before construction investment
- [x] sop-executor step limits (Section 1.10) address context exhaustion risk
- [x] state_schema_version field added to PROCEDURE_STATE.yaml schema

**Provenance check:**
- [x] All patterns cite Phase 1 section and evidence ID
- [x] ADR design decisions cited to Phase 3 section with revision numbers
- [x] Contradictions between phases explicitly identified and resolved
- [x] QG4 tournament findings cited by finding ID (DA-001, PM-002, FM-001, IN-001, etc.) in revision history

**P-022 deception check:**
- [x] sop-verifier independence explicitly bounded to context isolation (not personnel independence)
- [x] STAR LLM implementation limitation (same inference pass) disclosed
- [x] STAR effectiveness is now labeled "to be empirically validated" -- not asserted as proven
- [x] 3-hop anchoring bias in sop-capture acknowledged AND now restricted to C1-C2 only (not used for C3+)
- [x] OE feedback loop open-loop risk not understated; STOP hard limit is interim control, not closure
- [x] Governance ruling deadline (60 days) and fallback design (eliminate sop-verifier) explicitly documented

**S-013 inversion check (adversarial self-review):**
- [x] "What would make STAR ceremonial?" -- addressed by Section 1.5a error-trap validation gate
- [x] "What would make sop-brief optional?" -- addressed by explicit mandatory/optional labeling in Section 1.4
- [x] "What would make the OE loop invisible?" -- addressed by mandatory schema + STOP hard limit
- [x] "What would make H-36 permanently ambiguous?" -- addressed by 60-day governance deadline
- [x] "What would make the skill scope too narrow?" -- addressed by Section 3.0 pre-build pilot validation

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-23 | ps-synthesizer-001 | Initial synthesis. Three-phase convergence analysis, cross-reference matrix (22 patterns), implementation roadmap, risk register, nuclear fidelity assessment, H-36 dual-mode design. QG4 score: 0.88 (REVISE). |
| 2.0.0 | 2026-03-23 | ps-synthesizer-001 (Revision 2) | **R1 (PRIMARY):** Added STAR Behavioral Validation Plan (Section 1.5a) -- error trap design, A/B comparison protocol, measurable metrics, Phase 1 gate condition; STAR cannot advance to Phase 2 without empirical validation. **R2:** OE Feedback Loop Enforcement -- sop-brief Step 4 now retrieves and presents OE entries as mandatory context; STOP hard limit at >20 unanalyzed entries (was WARNING-only). OE entry mandatory schema added (Section 1.11) with write-time validation. **R3:** 3-Hop Mode Anchoring Bias for C3+ -- 3-hop mode RESTRICTED to C1-C2; C3+ REQUIRES 4-hop (sop-verifier via Task tool); workflow sequence diagram updated with C-level branching. **R4:** Skill Adoption Demand Validation -- Pre-Build Pilot Section (3.0) added; pilot validation required before Phase 1 construction begins; demand-side validation method defined. **R5:** sop-brief Step 1 Mandatory -- explicit mandatory/optional labeling in Section 1.4; Step 0 (generation) is optional, Step 1 (briefing) is mandatory for all invocations; sop-brief MUST find procedure definition or halt. **R6:** Risk Register RPN Corrections -- corrected top-5 ranking table (R-017 at 216 now correctly ranks above R-001 at 210). **Additional:** state_schema_version added to PROCEDURE_STATE.yaml (Section 1.9); criticality field added to PROCEDURE_STATE.yaml for mode selection; sop-executor step limits by criticality level added (Section 1.10); governance ruling 60-day deadline formalized (Section 1.8). Confidence updated to 0.92. |

---

*Synthesis Version: 2.0.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-003, P-004, P-011, P-020, P-022)*
*Methodology: Braun & Clarke (2006) Thematic Analysis, Cross-Reference Matrix, S-013 Inversion Self-Check*
*Input Confidence Weighted Average: 0.886 (Phase 1: 0.88 × 0.35 + Phase 2: 0.88 × 0.30 + Phase 3: 0.90 × 0.35)*
*Created: 2026-03-23*
*Revised: 2026-03-23 (v2.0.0 -- QG4 Revision 2)*
*Agent: ps-synthesizer-001*
