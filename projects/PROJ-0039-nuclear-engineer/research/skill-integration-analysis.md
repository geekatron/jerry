# /nuclear-sop Skill Integration Analysis: Composition, Routing, and Autonomy

> **PS ID:** phase-5.1 | **Entry ID:** e-005 | **Agent:** ps-researcher
> **Date:** 2026-03-25 | **Confidence:** HIGH (0.88) | **Version:** 1.1.0
> **Input Artifacts:**
> - Skill Specification: `ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` (confidence 0.92, v2.0.0)
> - Gap Analysis: `ps/phase-2/ps-analyst-001/sop-pattern-extraction.md` (confidence 0.88, Revision 2)
> - `/eng-team` SKILL.md v1.0.0
> - `/orchestration` SKILL.md v2.2.0
> - `/adversary` SKILL.md v1.0.0
> - `/problem-solving` SKILL.md v2.2.0
> - `agent-routing-standards.md` v1.1.0
> - `agent-development-standards.md` v1.2.0
> - `mandatory-skill-usage.md` (current trigger map)
> **Methodology:** Structured pairwise skill comparison (overlap/complement/composition/routing), autonomy capability matrix, GAP-09 design synthesis

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview for stakeholders |
| [L1: Technical Analysis](#l1-technical-analysis) | Per-skill integration analysis, routing methodology, autonomy matrix, GAP-09 design |
| [L2: Strategic Implications](#l2-strategic-implications) | Ecosystem impact, architectural recommendations, risk assessment |
| [References](#references) | All cited sources with contribution summary |
| [Revision History](#revision-history) | Version changelog |

---

## L0: Executive Summary

This research answers the question: how does the planned `/nuclear-sop` skill fit into the existing Jerry skill ecosystem?

The short answer is that `/nuclear-sop` is **complementary, not competitive**. It occupies a unique position in Jerry's skill taxonomy -- the "procedural rigor wrapper" -- that no existing skill fills. Where `/orchestration` coordinates multi-agent pipelines, `/nuclear-sop` enforces step-level discipline within a single procedure. Where `/adversary` scores deliverable quality after the fact, `/nuclear-sop` prevents errors before they happen through STAR self-checking. Where `/eng-team` provides security methodology, `/nuclear-sop` wraps any methodology in nuclear-grade before/during/after temporal discipline.

There are genuine overlap zones -- sop-verifier duplicates the FC-M-001 fresh context reviewer pattern already available in `/problem-solving` and `/orchestration`, and sop-brief's prerequisite checking echoes `/orchestration`'s phase pre-conditions. But these overlaps are shallow: `/nuclear-sop` adds the enforcement mechanism (procedure state tracking, execution logs, hold point blocking) that the existing patterns lack.

The most important finding is about **autonomy and H-36 compliance**. The four `/nuclear-sop` agents can function as a self-contained unit without requiring any other skill. The minimum viable invocation is the 3-agent sequence: sop-brief -> sop-executor -> sop-capture (3-hop mode), which is compliant with H-36's 3-hop circuit breaker for C1-C2 workflows. **However, the C3+ 4-hop mode (adding sop-verifier) has UNRESOLVED H-36 compliance.** Whether intra-skill predetermined agent sequences count against the H-36 hop budget is a pending framework governance question. If the ruling determines that intra-skill steps DO count as hops, the 4-hop mode violates H-36 and cannot be used. This is the single most significant architectural uncertainty for the skill's C3+ capabilities. The specification includes a 60-day deadline with a fallback design (eliminate sop-verifier, use 3-hop anchored mode permanently).

For routing, the skill's keyword space is naturally isolated. Nuclear-specific terms ("STAR self-check", "pre-job brief", "hold point", "place-keeping") have no collisions with existing skill keywords in the comprehensive keyword cross-reference analysis (all 20+ proposed keywords checked). The primary disambiguation challenge is between `/nuclear-sop` and `/orchestration` when users request "workflow" or "procedure" management. The proposed trigger map entry (priority 12, with negative keywords for "adversarial", "tournament", "transcript", "penetration", "exploit") resolves this cleanly. One keyword-level recommendation: standalone "sop" (without "nuclear") should be treated as a compound-trigger-only term, not a standalone positive keyword, because "SOP" is a common enterprise acronym that could false-match general standard operating procedure requests.

GAP-09 (Behavioral Drift Monitoring) is feasible as a cross-skill capability using `/adversary` (S-014 LLM-as-Judge) for scoring against behavioral baselines and `/nuclear-sop` OE infrastructure for tracking drift over time. For periodic triggering, the design originally assumed `/schedule` for cron-based execution; however, `/schedule` does not currently exist as a registered Jerry skill (it is not present in CLAUDE.md, mandatory-skill-usage.md, or the skills/ directory). Periodic triggering requires either (a) creating a `/schedule` skill, (b) external cron invocation, or (c) manual calendar-cadence execution. This changes the infrastructure reuse assessment from "60-70%" to approximately 50-60%, with the periodic execution component classified as "new -- moderate effort" rather than "fully reusable." The core GAP-09 design (scenario sets, behavioral scoring, OE-based drift tracking) remains valid regardless of the triggering mechanism.

---

## L1: Technical Analysis

### 1. Pairwise Skill Integration Analysis

#### 1.1 /nuclear-sop + /orchestration

**Source:** `/orchestration` SKILL.md v2.2.0; `/nuclear-sop` specification Section 9 (Integration with Jerry Ecosystem)

##### A. Overlap Zones

| Overlap Area | /orchestration | /nuclear-sop | Assessment |
|-------------|---------------|-------------|------------|
| Phase sequencing | ORCHESTRATION.yaml pipelines with phase status tracking | PROCEDURE_STATE.yaml with step-level status tracking | **Different granularity.** Orchestration tracks phases (coarse); nuclear-sop tracks individual steps within a phase (fine). Not a duplication -- they operate at different levels of abstraction. |
| Checkpoint/resume | Checkpoint entries in ORCHESTRATION.yaml with recovery_point | PROCEDURE_STATE.yaml with `current_step`, `next_step`, cross-session resume discovery | **Complementary.** Orchestration checkpoints at phase boundaries; nuclear-sop checkpoints at step boundaries within a phase. Both use filesystem persistence for recovery. |
| Quality gates | Phase gate definitions with S-014 scoring, >= 0.92 threshold (H-13), creator-critic-revision cycle | QG-HOLD type with same S-014 scoring, same threshold, same cycle | **Genuine duplication.** Both invoke `/adversary` (adv-scorer) with identical thresholds. However, nuclear-sop's QG-HOLD is embedded in the procedure flow at specific steps, while orchestration's gates are at phase boundaries. The mechanism is the same; the placement granularity differs. |
| Pre-condition checking | orch-planner validates workflow prerequisites | sop-brief Step 1 prerequisite and initial condition verification with STOP gate | **Partial overlap.** Orchestration checks workflow-level prerequisites; nuclear-sop checks procedure-level prerequisites with enforcement (STOP gate blocks execution). Nuclear-sop is more rigorous -- orchestration does not block on failed prerequisites. |
| State tracking artifacts | 3 artifacts: ORCHESTRATION_PLAN.md, ORCHESTRATION_WORKTRACKER.md, ORCHESTRATION.yaml | 4+ artifacts: workflow definition, pre-job brief, execution log, PROCEDURE_STATE.yaml, OE entry | **Different scope.** Orchestration tracks workflow-level state; nuclear-sop tracks execution-level state with step granularity, STAR records, and hold point logs. |

##### B. Complementary Patterns

| /nuclear-sop Adds | No Equivalent in /orchestration | Value |
|-------------------|-------------------------------|-------|
| STAR self-checking before each tool call | No pre-action structured pause exists | Prevents errors before execution; orchestration can only detect errors after execution via quality gates |
| Procedure use classification ([CONTINUOUS]/[REFERENCE]/[INFORMATION]) | No step-level compliance classification | Enables mixed-rigor workflows where some steps require exact compliance and others permit judgment |
| OE capture as mandatory deliverable | No post-execution lessons capture is required | Creates the feedback loop for continuous improvement; orchestration workflows produce synthesis but not structured OE entries |
| Hold points as blocking gates within steps | Phase gates at boundaries only | Enables mid-procedure human approval, quality verification, or independent review at specific steps |
| Execution log with STAR records | No step-level execution audit trail | Provides forensic evidence of what was checked, decided, and executed at each step |
| Place-keeping with sign-off | No step-level position tracking | Prevents step-skipping and enables reliable mid-procedure resume |

##### C. Composition Patterns

**Pattern 1: Nuclear-SOP as Phase Implementation Within Orchestration**

The most natural composition: orchestration manages the multi-phase pipeline, and specific phases invoke `/nuclear-sop` for nuclear-grade execution rigor.

```
ORCHESTRATION PIPELINE
  |
  Phase 1: Research (ps-researcher)        -- Standard /problem-solving
  |
  Phase 2: ADR Authoring (/nuclear-sop)    -- Nuclear rigor applied
  |   sop-brief -> sop-executor -> sop-verifier -> sop-capture
  |
  Phase 3: Implementation (eng-backend)     -- Standard /eng-team
  |
  Phase 4: Review (/adversary)              -- Standard adversarial
```

**Invocation example:** "Create an orchestration plan for the persistence strategy decision. Phase 2 (ADR authoring) should use /nuclear-sop with a C3 workflow definition for nuclear-grade procedural rigor."

**Hop budget interaction (critical constraint -- UNRESOLVED):** Nuclear-sop's internal agent transitions interact with the orchestration pipeline's H-36 hop budget. The `agent-routing-standards.md` "What Counts as a Hop" table explicitly states that "Agent-to-agent transition within a skill" DOES count as a hop. Under this reading, the 4-agent nuclear-sop sequence (brief -> executor -> verifier -> capture) consumes 4 hops:

- Phase 1 (ps-researcher): 1 hop
- Phase 2 (nuclear-sop, C3): 4 hops (sop-brief + sop-executor + sop-verifier + sop-capture)
- Phase 3 (eng-backend): 1 hop
- Total: 6 hops -- exceeds H-36 max 3

The skill specification (Section 1.8) proposes an alternative interpretation: that predetermined intra-skill sequences (where no routing re-evaluation occurs) should not count as hops. Under this "predetermined sequence is not a hop" interpretation, the budget would be:
- Phase 1: 1 hop (routing selects /problem-solving)
- Phase 2: 1 hop (routing selects /nuclear-sop; internal sequence is predetermined)
- Phase 3: 1 hop (routing selects /eng-team)
- Total: 3 hops -- compliant

**This interpretation is a pending governance question, not an established ruling.** The "What Counts as a Hop" table in `agent-routing-standards.md` does not distinguish between predetermined and dynamically-routed agent transitions. By analogy, `/eng-team`'s 8-step sequential workflow and `/adversary`'s 3-agent tournament would logically face the same question under the current table language, but neither has an explicit governance ruling confirming they count as 1 hop. All three cases (nuclear-sop, eng-team, adversary) require the same governance clarification.

Until the governance ruling is issued, the 3-hop mode (sop-brief -> sop-executor -> sop-capture, omitting sop-verifier) is the only confirmed H-36-compliant invocation pattern. The 4-hop C3+ mode is contingent on the governance ruling.

**Source:** Skill specification Section 1.8 (H-36 Circuit Breaker Compliance); agent-routing-standards.md Circuit Breaker section ("What Counts as a Hop" table)

**Pattern 2: Nuclear-SOP Wrapping Orchestration Phases**

Every orchestrated phase could optionally be wrapped with nuclear-sop discipline:

```
For each orchestration phase:
  1. sop-brief: Load phase context, check prerequisites, review OE
  2. [Phase agent execution]
  3. sop-capture: Capture phase OE entry
```

This is a lighter-weight composition that uses sop-brief and sop-capture as bookends without replacing the phase agent with sop-executor. The 2-agent overhead (brief + capture) adds pre-job context validation and post-job lessons capture to every orchestration phase.

##### D. Routing Interactions

| Request | /orchestration Match | /nuclear-sop Match | Resolution |
|---------|---------------------|-------------------|------------|
| "Create a multi-phase pipeline for this project" | Strong (orchestration, pipeline, phases) | No match | /orchestration |
| "Execute this procedure with nuclear rigor" | No match | Strong (nuclear, procedure, rigor) | /nuclear-sop |
| "Create a workflow with step-by-step verification" | Weak (workflow) | Moderate (step-by-step, verification) | Negative keyword "workflow" is NOT in nuclear-sop's negative list; compound trigger "step sign-off" or "pre-job brief" would disambiguate. Layer 1 escalates to Layer 2 on ambiguous "workflow" keyword. |
| "Plan and execute this procedure across sessions" | Moderate (plan, sessions) | Moderate (procedure, execute) | Ambiguous. H-31 clarification: "Do you want multi-phase pipeline coordination (/orchestration) or step-level procedural execution (/nuclear-sop)?" |

**Recommendation:** Add "multi-phase" and "pipeline coordination" as nuclear-sop negative keywords to suppress false matches on orchestration requests. Add "procedure execution" and "step compliance" as nuclear-sop compound triggers.

---

#### 1.2 /nuclear-sop + /adversary

**Source:** `/adversary` SKILL.md v1.0.0; `/nuclear-sop` specification Sections 1.7 (Hold Points), 9 (Integration)

##### A. Overlap Zones

| Overlap Area | /adversary | /nuclear-sop | Assessment |
|-------------|-----------|-------------|------------|
| Quality scoring | S-014 LLM-as-Judge, 6-dimension rubric, >= 0.92 threshold | QG-HOLD invokes the same S-014 infrastructure | **Intentional reuse, not duplication.** Nuclear-sop consumes /adversary's scoring capability at QG-HOLD points. The quality infrastructure is shared; the invocation context differs. |
| Deliverable evaluation | adv-executor runs strategy templates against completed deliverables | sop-verifier evaluates work products against acceptance criteria in fresh context | **Different purpose.** /adversary evaluates quality dimensions (completeness, consistency, rigor). sop-verifier evaluates pass/fail against procedure-specific acceptance criteria. They are complementary evaluators answering different questions. |
| Constitutional compliance | S-007 (Constitutional AI Critique) checks governance compliance | sop-brief Step 1 checks procedure prerequisites including governance constraints | **Minimal overlap.** S-007 checks constitutional principles broadly; sop-brief checks procedure-specific prerequisites. Different scope. |

##### B. Complementary Patterns

| /nuclear-sop Adds | No Equivalent in /adversary | Value |
|-------------------|--------------------------|-------|
| Pre-execution quality infrastructure (sop-brief prerequisite checking) | /adversary only evaluates after creation | Prevents quality problems by validating prerequisites before execution begins |
| STAR pre-action error prevention | /adversary detects errors after the fact | Catches errors before they are committed to files |
| Procedure-specific acceptance criteria evaluation (sop-verifier) | /adversary uses generic 6-dimension rubric | Evaluates against domain-specific success criteria, not abstract quality dimensions |
| OE capture and feedback loop | /adversary produces one-shot reports with no feedback to future invocations | Creates institutional memory that improves future procedure executions |

| /adversary Adds | No Equivalent in /nuclear-sop | Value |
|----------------|------------------------------|-------|
| 10-strategy tournament mode (C4) | No multi-strategy evaluation | Comprehensive adversarial assessment for critical deliverables |
| Strategy selection by criticality (adv-selector) | Fixed hold point types | Flexible quality methodology selection based on work criticality |
| H-16 Steelman-before-Devil's-Advocate ordering | No dialectical review protocol | Ensures arguments are strengthened before challenged |

##### C. Composition Patterns

**Pattern 1: /adversary at QG-HOLD Points**

Nuclear-sop's QG-HOLD type already invokes /adversary infrastructure. The composition is designed into the specification:

```
sop-executor reaches QG-HOLD step
  |
  QG-HOLD activates
  |
  /adversary (adv-scorer via S-014) scores work product
  |
  Score >= 0.92? -> QG-HOLD releases, execution continues
  Score < 0.92? -> Revision cycle (H-14, min 3 iterations)
  After 3 failed iterations -> User escalation (P-020)
```

**Source:** Skill specification Section 1.7 (Hold Point Types), QG-HOLD definition

**Pattern 2: /adversary Tournament After Nuclear-SOP Completion**

For C4 critical procedures, the user can invoke /adversary tournament mode after sop-capture completes, scoring the entire procedure's output:

```
/nuclear-sop completes (brief -> execute -> verify -> capture)
  |
  All work products + OE entry available
  |
  /adversary C4 tournament (all 10 strategies) against work products
```

**Invocation example:** "Execute this governance change using /nuclear-sop with C4 rigor, then run a full C4 tournament review with /adversary on all outputs."

##### D. Routing Interactions

| Request | /adversary Match | /nuclear-sop Match | Resolution |
|---------|-----------------|-------------------|------------|
| "Score this deliverable quality" | Strong (quality scoring) | No match | /adversary |
| "Execute this with STAR self-checking" | No match | Strong (STAR self-check) | /nuclear-sop |
| "Run a quality gate on this procedure step" | Moderate (quality gate) | Moderate (procedure step) | Nuclear-sop's QG-HOLD. Context determines: if within a nuclear-sop execution, the quality gate is a QG-HOLD; if standalone, it is /adversary. |
| "Adversarial review of this nuclear procedure" | Strong (adversarial review) | Weak (nuclear procedure -- but "adversarial" is in nuclear-sop's negative keywords) | /adversary. Nuclear-sop's negative keyword "adversarial" correctly suppresses the false match. |

The routing interaction between these two skills is clean. Nuclear-sop includes "adversarial" and "tournament" as negative keywords, correctly yielding to /adversary when those terms appear. The QG-HOLD integration is internal (nuclear-sop invokes /adversary infrastructure programmatically, not via routing).

---

#### 1.3 /nuclear-sop + /problem-solving

**Source:** `/problem-solving` SKILL.md v2.2.0; `/nuclear-sop` specification Section 9

##### A. Overlap Zones

| Overlap Area | /problem-solving | /nuclear-sop | Assessment |
|-------------|-----------------|-------------|------------|
| Fresh context review | ps-critic via Task tool (FC-M-001) | sop-verifier via Task tool (same pattern) | **Same mechanism, different scope.** ps-critic evaluates quality dimensions with revision guidance; sop-verifier evaluates acceptance criteria pass/fail. Both use FC-M-001. |
| Self-review | S-010 Self-Refine (H-15, post-completion) | STAR self-checking (pre-action, per tool call) | **Different timing and scope.** S-010 reviews entire deliverables after completion. STAR reviews individual actions before execution. They are complementary, not overlapping. As documented in specification Section 1.5 (comparison table). |
| Research capability | ps-researcher for evidence gathering | sop-brief for OE review and context loading | **Different purpose.** ps-researcher performs open-ended divergent research. sop-brief performs targeted context loading for a specific procedure. |
| Structured analysis | ps-analyst for root cause, FMEA, trade-offs | sop-capture for deviation analysis and lessons learned | **Different scope.** ps-analyst produces deep analytical artifacts. sop-capture produces structured OE entries with mandatory schema fields. ps-analyst could be invoked for deep analysis of a deviation found by sop-capture. |

##### B. Complementary Patterns

| /nuclear-sop Adds | No Equivalent in /problem-solving | Value |
|-------------------|----------------------------------|-------|
| Temporal workflow structure (before/during/after as first-class phases) | No formalized pre-execution or post-execution phases | Prevents the most common AI agent failure: starting work without sufficient context validation |
| Step-level execution tracking with STAR | ps-agents produce artifacts but do not track individual steps | Provides forensic audit trail of exactly what was checked and decided at each step |
| Procedure use classification | No equivalent step-level compliance classification | Distinguishes mandatory sequential execution from reference consultation |
| Mandatory OE capture | docs/experience/ exists but capture is not enforced | Every execution becomes institutional knowledge |

| /problem-solving Adds | No Equivalent in /nuclear-sop | Value |
|----------------------|------------------------------|-------|
| Divergent research (ps-researcher) | No research capability | Open-ended exploration and evidence gathering |
| Deep analysis (ps-analyst, 5 Whys, FMEA) | Deviation recording only | Root cause analysis methodology |
| Architecture decisions (ps-architect, Nygard ADR) | No decision methodology | Structured decision documentation |
| Synthesis across documents (ps-synthesizer) | OE entry aggregation (Phase 3) | Cross-document pattern extraction |

##### C. Composition Patterns

**Pattern 1: Nuclear-SOP Wrapping Problem-Solving Workflows**

Apply nuclear rigor to a problem-solving workflow. **P-003 clarification:** In this composition, the MAIN CONTEXT (orchestrator) sequences the invocations -- sop-executor does NOT directly invoke ps-researcher, ps-analyst, or ps-architect via the Task tool. The steps listed below are instructions the orchestrator executes sequentially; sop-executor tracks step completion in PROCEDURE_STATE.yaml and performs STAR self-checking, while the orchestrator invokes the appropriate agent at each step:

```
sop-brief: Load context, check prerequisites, review OE for this analysis type
  |
sop-executor [REFERENCE mode]:
  Step 1: [Orchestrator invokes ps-researcher] for evidence gathering
  Step 2: [Orchestrator invokes ps-analyst] for root cause analysis
  Step 3: [Orchestrator invokes ps-architect] for ADR creation
  Step 4: [QG-HOLD] Quality gate on ADR
  Step 5: [USER-HOLD] User approves final decision
  |
sop-verifier (C3+): Fresh-context evaluation of ADR against acceptance criteria
  |
sop-capture: Record deviations, quality scores, lessons learned
```

In this composition, the nuclear-sop skill provides the procedural wrapper (what to do before, how to track during, what to capture after), while /problem-solving agents provide the analytical substance at each step.

**Invocation example:** "Use /nuclear-sop to execute a C3 ADR authoring procedure. The execution steps should invoke ps-researcher, ps-analyst, and ps-architect for the analytical work."

**Pattern 2: ps-synthesizer for OE Feedback Loop (Phase 3)**

The Phase 3 OE feedback loop requires ps-synthesizer to aggregate OE entries:

```
OE entries accumulate (written by sop-capture after each execution)
  |
sop-brief detects > 20 unanalyzed entries for this workflow_type -> STOP
  |
ps-synthesizer invoked to synthesize OE entries by workflow_type
  |
Synthesis output: recurring patterns, workflow revision recommendations
  |
Workflow definition updated based on synthesis findings
```

**Source:** Skill specification Section 9 (With ps-synthesizer); Phase 3 roadmap (Section 3, Phase 3)

##### D. Routing Interactions

| Request | /problem-solving Match | /nuclear-sop Match | Resolution |
|---------|----------------------|-------------------|------------|
| "Research authentication patterns" | Strong (research) | No match | /problem-solving |
| "Execute this procedure with pre-job briefing" | No match | Strong (procedure, pre-job brief) | /nuclear-sop |
| "Analyze and execute this with step tracking" | Moderate (analyze) | Moderate (execute, step tracking) | "Analyze" triggers /problem-solving; "step tracking" suggests /nuclear-sop. Compound trigger "step sign-off" or "place-keeping" would disambiguate toward nuclear-sop. Without compound trigger, H-31 clarification. |
| "Investigate why this procedure failed" | Strong (investigate) | Weak (procedure -- but "investigate" is not in nuclear-sop keywords) | /problem-solving (ps-investigator). Nuclear-sop has no investigation methodology. |

The keyword spaces are well-separated. "Research", "analyze", "investigate", "root cause", "review" are all in /problem-solving's territory with no collision. Nuclear-sop's keywords ("nuclear sop", "STAR self-check", "pre-job brief", "hold point") are domain-specific and unique.

---

#### 1.4 /nuclear-sop + /eng-team

**Source:** `/eng-team` SKILL.md v1.0.0; `/nuclear-sop` specification Section 9

##### A. Overlap Zones

| Overlap Area | /eng-team | /nuclear-sop | Assessment |
|-------------|----------|-------------|------------|
| Sequential phase-gate workflow | 8-step sequential workflow (eng-architect -> eng-lead -> implementation -> verification -> review -> incident) | 4-agent sequential workflow (brief -> execute -> verify -> capture) | **Similar pattern, different domain.** Both enforce sequential execution with gates. /eng-team's gates are security-focused; /nuclear-sop's gates are procedure-compliance-focused. |
| Quality gate at review phase | eng-reviewer invokes /adversary at C2+ (>= 0.95 threshold) | QG-HOLD invokes /adversary (>= 0.92 threshold per H-13) | **Different thresholds.** eng-reviewer uses a higher threshold (0.95) than the SSOT default (0.92). These are independently configurable. |
| Mandatory self-review (H-15) | All eng-team agents perform S-010 before output | sop-executor performs STAR (pre-action) + agents perform S-010 (post-completion) | **Complementary.** STAR is pre-action; S-010 is post-completion. Nuclear-sop adds the pre-action layer that eng-team lacks. |

##### B. Complementary Patterns

| /nuclear-sop Adds | No Equivalent in /eng-team | Value |
|-------------------|--------------------------|-------|
| Pre-job briefing with OE review | No pre-engagement context loading phase | Prevents starting security work without reviewing lessons from prior similar engagements |
| STAR self-checking before tool calls | No pre-action verification protocol | Catches implementation errors before they are committed (e.g., writing to wrong file, applying wrong security control) |
| Post-engagement OE capture as mandatory deliverable | eng-incident provides post-deployment IR but not lessons-learned capture per engagement | Creates feedback loop for security engineering methodology improvement |
| Procedure use classification | No step-level compliance distinction | Enables mixed-rigor security procedures where some steps (key generation) require exact compliance while others (documentation) permit judgment |
| Hold points with user approval | No formal blocking gates within the 8-step workflow | Enables human approval at critical security decision points (e.g., before deploying security-critical changes) |

| /eng-team Adds | No Equivalent in /nuclear-sop | Value |
|----------------|------------------------------|-------|
| Security domain expertise (STRIDE, DREAD, OWASP, NIST) | No security methodology | Domain-specific threat modeling and security analysis |
| 10 specialized security agents | 4 general-purpose procedural agents | Deep security coverage across architecture, implementation, testing, review |
| 5-layer SDLC governance (SSDF, SDL, SAMM, SLSA, DevSecOps) | No SDLC framework | Standards-based security governance |
| Incident response (eng-incident) | OE capture (sop-capture -- different purpose) | Post-deployment IR capability |

##### C. Composition Patterns

**Pattern 1: Nuclear-SOP Discipline for Security Engagements**

Wrap the /eng-team 8-step workflow in nuclear-sop discipline. **P-003 clarification:** In this composition, the MAIN CONTEXT (orchestrator) invokes both nuclear-sop and eng-team agents sequentially -- sop-executor does NOT spawn eng-team agents via the Task tool. sop-executor is a T2 agent (Read, Write, Bash) that tracks procedure state and performs STAR self-checking; the orchestrator reads PROCEDURE_STATE.yaml to determine the current step and invokes the appropriate eng-team agent at each step:

```
sop-brief: Load security context, review prior security engagement OE,
           check prerequisites (threat model exists? requirements defined?)
  |
sop-executor [CONTINUOUS mode for C3+ security]:
  Step 1: [Orchestrator invokes eng-architect] -- threat model [QG-HOLD at 0.95]
  Step 2: [Orchestrator invokes eng-lead] -- implementation plan
  Step 3: [Orchestrator invokes eng-backend / eng-frontend / eng-infra]
  Step 4: [Orchestrator invokes eng-devsecops] -- automated scans
  Step 5: [Orchestrator invokes eng-qa] -- security testing [QG-HOLD]
  Step 6: [Orchestrator invokes eng-security] -- manual review [IV-HOLD: sop-verifier]
  Step 7: [Orchestrator invokes eng-reviewer] -- final gate [QG-HOLD at 0.95]
  Step 8: [Orchestrator invokes eng-incident] -- IR plan
  |
sop-verifier: Fresh-context verification of security deliverables
  |
sop-capture: Security engagement OE entry
```

This composition adds pre-engagement context loading, step-level STAR discipline during security implementation, hold points at critical security decision points, and post-engagement lessons capture -- all things the standalone /eng-team workflow does not provide.

**Invocation example:** "Use /nuclear-sop to wrap a C3 security engagement using /eng-team agents. Apply CONTINUOUS procedure classification to the threat modeling and manual review steps."

**Practical Constraints (Context Window Budget):** This composition involves at minimum 12 sequential agent invocations (4 sop agents + 8 eng-team agents). At this scope, context window exhaustion is a serious practical concern. Each agent transition requires loading the workflow definition, procedure state, prior outputs, and execution context. STAR self-checking adds approximately 2x token overhead per step (per the specification's trade-off table in Section 5.3). For a full 8-step eng-team engagement wrapped in nuclear-sop, the following constraints apply:

- **Cross-session execution is REQUIRED.** The 12-agent sequence will exhaust a single context window. PROCEDURE_STATE.yaml provides the cross-session resume mechanism -- the orchestrator can resume the procedure at the current step boundary in a new session.
- **CB-02 compliance:** Tool results should not exceed 50% of context (per agent-development-standards.md). Each eng-team agent should produce its artifacts to disk before the next agent loads.
- **Recommended phase boundaries for session breaks:** After sop-brief (session 1), after Step 4 eng-devsecops (session 2), after Step 8 eng-incident (session 3), sop-verifier + sop-capture (session 4).

The lighter-weight Pattern 2 below avoids this constraint by applying nuclear-sop selectively.

**Pattern 2: Selective Nuclear Rigor on Security-Critical Steps**

Rather than wrapping the entire engagement, apply nuclear-sop only to security-critical steps:

```
eng-architect: Threat model (standard /eng-team)
eng-lead: Implementation plan (standard /eng-team)
  |
/nuclear-sop for implementation steps only:
  sop-brief: Review OE for this implementation type
  sop-executor: Step-by-step implementation with STAR
  sop-capture: Implementation OE
  |
eng-reviewer: Final gate (standard /eng-team)
```

##### D. Routing Interactions

| Request | /eng-team Match | /nuclear-sop Match | Resolution |
|---------|----------------|-------------------|------------|
| "Design a secure microservice with threat model" | Strong (secure design, threat model) | No match | /eng-team |
| "Execute this implementation with nuclear rigor" | Weak (implementation) | Strong (nuclear rigor) | /nuclear-sop. "Secure" and "threat model" are not present. |
| "Build a secure system with step-by-step procedure compliance" | Strong (secure, build) | Strong (step-by-step, procedure compliance) | Both match. RT-M-006 ordering: content skill (/eng-team) before quality/rigor skill (/nuclear-sop). Combine: /eng-team for methodology + /nuclear-sop for procedural wrapper. |
| "Security hardening with nuclear procedure discipline" | Strong (security hardening) | Strong (nuclear procedure discipline) | Both match via compound triggers. RT-M-006 combination: /eng-team provides the security methodology, /nuclear-sop provides the procedural structure. |

The routing interaction between these skills is the most interesting case. When both match, the correct behavior is combination (RT-M-006), not disambiguation. Nuclear-sop wraps eng-team, providing procedural structure for security methodology. The combination ordering follows RT-M-006 rule 3 (content before quality): /eng-team produces the security content, /nuclear-sop provides the quality/compliance wrapper.

---

### 2. Routing Methodology

#### 2.1 Proposed Trigger Map Entry

The skill specification (Section 1.1) already provides a complete trigger map entry. Based on the integration analysis above, I recommend one enhancement -- adding "multi-phase", "pipeline", and "coordination" as negative keywords to prevent collision with `/orchestration`:

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow | adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review, multi-phase, pipeline coordination, research, investigate, root cause, threat model, STRIDE, secure design | 12 | "nuclear procedure" OR "pre-job brief" OR "post-job brief" OR "STAR self-check" OR "hold point" OR "step sign-off" OR "place-keeping" OR "procedure compliance" (phrase match) | `/nuclear-sop` |

**Source:** Skill specification Section 1.1 (Activation Keywords); agent-routing-standards.md Enhanced Trigger Map format

#### 2.2 Routing Changes Summary

| Change Type | Location | Change |
|------------|---------|--------|
| New trigger map row | `mandatory-skill-usage.md` Trigger Map | Add `/nuclear-sop` row per table above |
| CLAUDE.md skill table | `CLAUDE.md` Quick Reference | Add `/nuclear-sop` with description: "Nuclear SOP procedural rigor: pre-job brief, STAR execution, hold points, OE capture" |
| AGENTS.md registry | `AGENTS.md` | Add 4 entries: sop-brief, sop-executor, sop-verifier, sop-capture |
| Negative keyword update | `/orchestration` trigger map row | Consider adding "nuclear" and "sop" as negative keywords for /orchestration to prevent false matches |
| Skill count | Jerry skill count | 20 -> 21 (crosses H-37 Phase 1 threshold of 20; triggers evaluation of Phase 2 routing conditions) |

#### 2.3 Collision Analysis

Cross-referencing ALL nuclear-sop proposed keywords against all existing skill trigger map entries in `mandatory-skill-usage.md`:

| Keyword | Collision Skill | Collision Type | Resolution |
|---------|----------------|---------------|------------|
| "nuclear sop" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "nuclear procedure" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "STAR self-check" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "pre-job brief" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "post-job brief" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "hold point" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "place-keeping" | None | No collision | Domain-specific; unique to nuclear-sop |
| "step sign-off" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "procedure compliance" | /nasa-se (keyword: "compliance") | Partial collision on "compliance" substring | "Procedure compliance" is a compound trigger that disambiguates. Standalone "compliance" routes to /nasa-se (V&V context); "procedure compliance" routes to nuclear-sop. Negative keyword "specification" on nuclear-sop further suppresses /nasa-se collision. |
| "continuous use" | None | No collision | Domain-specific; unique to nuclear-sop |
| "procedure use classification" | None | No collision | Multi-word phrase; unique to nuclear-sop |
| "operating experience capture" | None | No collision | Multi-word phrase; unique to nuclear-sop |
| "OE entry" | None | No collision | Domain-specific abbreviation; unique to nuclear-sop |
| "nuclear rigor" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "nuclear discipline" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "sop brief" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "sop execute" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "sop capture" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "sop verify" | None | No collision | Domain-specific compound; unique to nuclear-sop |
| "nuclear workflow" | /orchestration (keyword: "workflow") | Partial collision on "workflow" substring | "Nuclear workflow" is a compound trigger that disambiguates. Standalone "workflow" routes to /orchestration (priority 1 vs. nuclear-sop priority 12). |
| "workflow" (standalone) | /orchestration (keyword: "workflow") | Direct collision | Resolved by priority: /orchestration priority 1, nuclear-sop priority 12. Standalone "workflow" routes to /orchestration. |
| "procedure" (standalone) | None | No collision | "Procedure" is unique to nuclear-sop in the current trigger map |
| "execute" (standalone) | None | No collision | "Execute" is not in any existing skill's keyword list |
| "compliance" (standalone) | /nasa-se (keyword: "compliance") | Direct collision | "Compliance" alone matches /nasa-se (priority 5) before nuclear-sop (priority 12). Nuclear-sop's compound trigger "procedure compliance" disambiguates. |
| "rigor" (standalone) | None | No collision | Not in any existing skill's keyword list |
| "quality gate" | /adversary (keyword: "quality gate") | Direct collision | "Quality gate" is in nuclear-sop's NEGATIVE keyword list -- correctly yields to /adversary. |
| "sop" (standalone, implicit) | None currently | **Future collision risk** | "SOP" is a common enterprise acronym for "standard operating procedure." A request like "help me create an SOP for our release process" would trigger /nuclear-sop when /problem-solving or /diataxis is more appropriate. **Recommendation:** "sop" should only appear as part of compound triggers ("nuclear sop", "sop brief", "sop execute", "sop capture", "sop verify"), never as a standalone positive keyword. |

**Verdict:** No collisions identified in comprehensive keyword analysis covering all 20+ proposed keywords. Three partial collisions ("compliance", "workflow", "quality gate") are resolved by existing mechanisms (compound triggers, priority ordering, negative keywords). **Recommendation:** Standalone "sop" should be treated as compound-trigger-only to prevent false-positive matching on general SOP requests unrelated to nuclear procedures.

**Source:** mandatory-skill-usage.md (current trigger map, all 16 skill entries); agent-routing-standards.md Section "Enhanced Trigger Map"

#### 2.4 Skill Count Impact

Adding `/nuclear-sop` brings the Jerry skill count to 21, which is one above the H-37 Phase 1 threshold (20 skills). Per the scaling roadmap in agent-routing-standards.md:

- Phase 1 (current, 8 skills -> immediate target 21): Enhanced keyword routing with 5-column trigger map remains adequate.
- Phase 2 transition triggers should be evaluated: (1) 10+ collision zones, (2) false negative rate > 40%, (3) user override rate > 30%.

With no unresolved keyword collisions identified in the comprehensive analysis above, the transition to Phase 2 routing is not yet triggered. However, the collision analysis should be repeated when the next skill is added (skill 22) to confirm this assessment.

**Source:** agent-routing-standards.md Scaling Roadmap; skill specification Section 1.1 (skill count impact note)

---

### 3. Autonomy Analysis

#### 3.1 Agent Autonomy Matrix

| Agent | Standalone Artifact? | Requires Other Skill? | Enhances Other Skills? | Minimum Invocation Unit |
|-------|---------------------|----------------------|----------------------|------------------------|
| **sop-brief** | Yes: pre-job-brief.md (context, prerequisites, OE findings, error traps) | No (reads filesystem only; no external skill dependency) | Yes: can enhance any skill by providing pre-execution context validation | Can run alone as a pre-execution checklist for any workflow |
| **sop-executor** | Yes: execution log + PROCEDURE_STATE.yaml + work products | No for basic execution; Yes for QG-HOLD (requires /adversary infrastructure) and complex steps (may benefit from /problem-solving agents) | Yes: provides step-level STAR discipline to any execution | Requires sop-brief output (pre-job brief) as input; cannot start without it |
| **sop-verifier** | Yes: verification report (ACCEPT/REJECT/CONDITIONAL) | No (T1 read-only; evaluates against acceptance criteria in workflow definition) | Yes: provides fresh-context verification for any work product | Can run independently on any work product + acceptance criteria pair |
| **sop-capture** | Yes: OE entry (mandatory schema) + post-job brief | No (reads execution log and work products only) | Yes: provides structured lessons capture for any completed workflow | Requires execution log as input (from sop-executor or equivalent) |

#### 3.2 Invocation Patterns

**Pattern A: Full Autonomous Sequence (Standalone /nuclear-sop)**

All four agents operate as a self-contained unit. No other skill is required.

```
sop-brief -> sop-executor -> [sop-verifier for C3+] -> sop-capture
```

Produces: pre-job brief, execution log, work products, PROCEDURE_STATE.yaml, verification report (C3+), OE entry. This is a complete, autonomous workflow.

**H-36 compliance note:** The 3-hop mode (sop-brief -> sop-executor -> sop-capture) is compliant with H-36 for C1-C2 workflows. The 4-hop mode (adding sop-verifier for C3+) is pending the governance ruling on whether predetermined intra-skill sequences count as hops (see Section 1.1.C).

**Pattern B: Composed Invocation (Nuclear-SOP + Other Skills)**

Nuclear-sop agents wrap other skills' agents:

```
sop-brief
  -> [Other skill agents via orchestrator-managed steps]
  -> [sop-verifier for C3+]
  -> sop-capture
```

Nuclear-sop provides the procedural structure; other skills provide domain expertise at execution steps. This is the high-value composition pattern. The orchestrator (MAIN CONTEXT) sequences all invocations per P-003.

**Pattern C: Selective Agent Invocation (Cherry-Picking)**

Individual nuclear-sop agents can be invoked independently for targeted use:

| Agent | Standalone Use Case | Prerequisite |
|-------|-------------------|-------------|
| sop-brief alone | Pre-execution context validation checklist for any workflow | Workflow definition file or natural language description |
| sop-capture alone | Post-execution lessons capture for any completed work | Execution log or equivalent artifact to analyze |
| sop-verifier alone | Independent fresh-context verification of any work product | Work product + acceptance criteria |
| sop-executor alone | Not recommended standalone -- requires sop-brief context | sop-brief pre-job brief output |

**Assessment:** sop-brief, sop-capture, and sop-verifier are all independently valuable. sop-executor requires sop-brief output and is the only agent that cannot operate fully standalone. The minimum viable invocation for meaningful nuclear rigor is the 3-agent sequence: sop-brief -> sop-executor -> sop-capture (3-hop mode, C1-C2).

#### 3.3 Dependency Map

```
                    REQUIRED DEPENDENCIES
                    =====================

sop-brief ──────────────────────────────────────────────────> [No dependency]
    |                                                           Reads: workflow definition,
    |                                                                  docs/experience/ (OE entries)
    v
sop-executor ──── depends on ──── sop-brief output (pre-job-brief.md)
    |                              Optional: /adversary for QG-HOLD
    |                              Optional: /problem-solving for complex steps
    v
sop-verifier ──── depends on ──── sop-executor work products
    |                              (but NOT executor reasoning -- fresh context)
    v
sop-capture ───── depends on ──── sop-executor execution log (FINAL)
                                   Optional: sop-verifier report (if C3+)

                    OPTIONAL INTEGRATIONS
                    =====================

sop-brief ───── benefits from ───── Prior OE entries (written by prior sop-capture runs)
sop-executor ── benefits from ───── /adversary (S-014) at QG-HOLD points
sop-executor ── benefits from ───── /problem-solving agents at complex steps
sop-capture ─── benefits from ───── ps-synthesizer (Phase 3 OE feedback loop)
```

---

### 4. GAP-09: Behavioral Drift Monitoring Design

#### 4.1 Concept

GAP-09 addresses the nuclear analog of 10 CFR 50.54(i-1) operator requalification: detecting when an AI agent's behavioral patterns drift from established baselines. The correct analog is NOT regression testing (testing deterministic code) but continuous behavioral evaluation of the agent-as-operator.

AI agents exhibit behavioral divergence through:
- Model version updates (provider-side changes to weights/architecture)
- Context rot within long sessions (degraded instruction-following as context fills)
- Prompt drift (accumulation of subtle changes to agent definitions over time)
- Tool response changes (external API or tool behavior changes)

**Source:** Phase 2 gap analysis Section 4.1, GAP-09 reclassification (2026-03-25)

#### 4.2 Architecture: Cross-Skill Capability

GAP-09 is designed as a cross-skill capability reusing existing Jerry infrastructure:

```
Periodic Trigger (see Section 4.3 note on triggering mechanism)
    |
    v
Behavioral Evaluation Harness (new, lightweight)
    |
    +--> Canonical Scenario Execution
    |      Load scenario set for target agent
    |      Execute scenarios against current agent behavior
    |      Collect behavioral observations
    |
    +--> /adversary (S-014 LLM-as-Judge)
    |      Score behavioral observations against baselines
    |      Detect divergence patterns
    |      Flag threshold violations
    |
    +--> /nuclear-sop OE Infrastructure
           Write behavioral evaluation results as OE entries
           Track drift over time via OE entry timeline
           sop-brief loads prior drift findings before next evaluation
```

#### 4.3 Component Design

**Canonical Scenario Sets:**

Each agent that requires behavioral monitoring maintains a set of canonical scenarios with known-correct outcomes. Scenarios are stored as versioned files:

```yaml
# Example: skills/nuclear-sop/behavioral-baselines/sop-executor-scenarios.yaml
scenario_set:
  version: "1.0.0"
  target_agent: "sop-executor"
  scenarios:
    - id: "SCN-001"
      description: "STAR catches deliberate error trap (wrong file path)"
      input:
        workflow_definition: "examples/c3-adr-workflow-definition.md"
        step_number: 5  # The error trap step
      expected_behavior:
        star_think_detects_error: true
        stop_work_invoked: true
        deviation_logged: true
      baseline_score: 0.95  # S-014 score when behavior matches expectation

    - id: "SCN-002"
      description: "Place-keeping correctly blocks step skip"
      input:
        procedure_state: "step 3 not completed"
        requested_step: 5  # Skip attempt
      expected_behavior:
        skip_blocked: true
        error_message_includes: "step 3 not completed"
      baseline_score: 0.98
```

**Periodic Execution -- Triggering Mechanism:**

**Verification note:** `/schedule` does not currently exist as a registered Jerry skill. It is not present in CLAUDE.md's skill table, the `mandatory-skill-usage.md` trigger map, or the `skills/` directory (verified 2026-03-25). The original design assumed `/schedule` for cron-based remote agent execution; this assumption was incorrect.

Periodic triggering requires one of the following alternatives:

| Option | Description | Effort | Assessment |
|--------|-------------|--------|------------|
| **A. Create `/schedule` skill** | Build a new skill for cron-based remote agent execution | High | Provides full automation; scope exceeds GAP-09 |
| **B. External cron invocation** | Use OS-level cron/launchd to invoke `claude` CLI with the behavioral evaluation prompt | Low | Pragmatic; requires minimal new infrastructure; platform-dependent |
| **C. Manual calendar cadence** | Human triggers behavioral evaluation on a regular schedule (monthly/quarterly) | Zero | Simplest; acceptable for Phase 2 while evaluation methodology is being validated |

**Recommended approach:** Option C for Phase 2 (manual triggering while methodology is validated), with Option B as the Phase 3 target once evaluation methodology is proven. Option A (`/schedule` creation) should only be pursued if periodic agent invocation becomes a broader Jerry framework need beyond GAP-09.

Behavioral evaluation runs:
- After every model version update (triggered by detection of model change in agent response metadata)
- On a regular schedule (e.g., monthly for high-criticality agents, quarterly for standard agents)
- On demand when behavioral concerns are reported

**Scoring via /adversary (S-014):**

The behavioral evaluation uses `/adversary`'s S-014 LLM-as-Judge scoring to compare current behavior against baselines:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Behavioral Fidelity | 0.30 | Does the agent's behavior match the expected outcome for each scenario? |
| Instruction Following | 0.25 | Does the agent follow its agent definition methodology (STAR steps, hold point enforcement)? |
| Error Detection Accuracy | 0.20 | Does the agent catch planted errors at the same rate as the baseline? |
| Output Consistency | 0.15 | Are output artifacts structurally consistent with baseline runs? |
| Escalation Appropriateness | 0.10 | Does the agent escalate/stop-work at the same conditions as baseline? |

**Divergence Thresholds:**

| Threshold | Score Drop | Action |
|-----------|-----------|--------|
| Normal | < 0.05 from baseline | Log result, no action |
| Warning | 0.05 - 0.10 from baseline | Flag in OE entry; review at next evaluation |
| Alert | 0.10 - 0.20 from baseline | Mandatory investigation; identify root cause of drift |
| Critical | > 0.20 from baseline | Suspend agent from C3+ workflows until remediated; notify user |

**OE Infrastructure for Drift Tracking:**

Behavioral evaluation results are written as OE entries using nuclear-sop's mandatory schema:

```yaml
oe_entry:
  entry_id: "behavioral-drift-20260401-001"
  workflow_type: "NOMINAL"  # Behavioral evaluation is a routine procedure
  criticality: "C2"
  deviation_type: "NONE"  # Or MINOR/MAJOR if drift detected
  root_cause: "Model version update from opus-4.5 to opus-4.6"
  recommendation: "Re-validate STAR error trap scenarios with updated model"

  # Behavioral drift extension fields (Phase 3+)
  drift_monitoring:
    target_agent: "sop-executor"
    baseline_version: "1.0.0"
    current_model: "opus-4.6"
    scenario_results:
      - scenario_id: "SCN-001"
        baseline_score: 0.95
        current_score: 0.92
        delta: -0.03
        status: "NORMAL"
      - scenario_id: "SCN-002"
        baseline_score: 0.98
        current_score: 0.85
        delta: -0.13
        status: "ALERT"
    aggregate_divergence: 0.08
    aggregate_status: "WARNING"
```

**sop-brief Integration:** When sop-brief loads OE entries for a procedure, it also loads behavioral drift OE entries for agents that will be invoked. If an agent has WARNING or ALERT status, sop-brief presents this as a CAUTION in the pre-job brief:

```
CAUTION: sop-executor has WARNING-level behavioral drift (aggregate divergence 0.08)
         detected 2026-04-01. Scenario SCN-002 (place-keeping) shows ALERT-level drift.
         Consider additional USER-HOLD points for place-keeping verification steps.
```

#### 4.4 Infrastructure Reuse Assessment

| Component | Existing Infrastructure | New Required | Assessment |
|-----------|----------------------|-------------|------------|
| Periodic execution | No existing skill (see Section 4.3 verification note) | Triggering mechanism required: manual cadence (Phase 2), external cron (Phase 3), or new `/schedule` skill (if broader need) | **New -- moderate effort** for automated triggering; zero effort for manual cadence |
| Quality scoring | `/adversary` (S-014 LLM-as-Judge, adv-scorer) | Custom rubric dimensions for behavioral evaluation | Mostly reusable; requires custom dimension weights |
| OE entry storage | `/nuclear-sop` OE infrastructure (docs/experience/, mandatory schema) | Extension fields for drift monitoring data | Mostly reusable; requires schema extension |
| Scenario storage | None | Scenario definition YAML files per agent | New -- moderate effort |
| Baseline management | None | Baseline version tracking per agent per model version | New -- moderate effort |
| Divergence detection | None | Threshold comparison logic and alerting | New -- low effort |
| sop-brief integration | sop-brief OE search (Phase 1) | Extension to load behavioral drift OE entries | Minor extension |

**Net assessment:** Approximately 50-60% infrastructure reuse from existing Jerry capabilities. The reuse percentage is lower than originally assessed (was 60-70%) because the periodic execution component requires new infrastructure rather than reusing a `/schedule` skill. The reusable components are quality scoring (/adversary S-014), OE entry storage (nuclear-sop OE infrastructure), and sop-brief integration (OE search). The new components (scenario files, baseline management, divergence thresholds, triggering mechanism) are lightweight data structures and configuration, not new agent architectures.

#### 4.5 Implementation Phasing

| Phase | Deliverables | Prerequisites |
|-------|-------------|---------------|
| Phase 1 (with /nuclear-sop Phase 1) | Scenario definition format; 3+ scenarios per nuclear-sop agent; baseline recording during Phase 1 STAR validation | /nuclear-sop Phase 1 acceptance (STAR validation provides the first scenario data) |
| Phase 2 (+2 months) | Manual-cadence behavioral evaluation; custom S-014 rubric dimensions; OE entry schema extension | /nuclear-sop Phase 1 complete with OE infrastructure |
| Phase 3 (+4 months) | Automated triggering (external cron or equivalent); sop-brief integration for drift warnings; alert thresholds calibrated from empirical data | Sufficient baseline data (5+ evaluation runs per agent); triggering mechanism selected |

---

## L2: Strategic Implications

### 5. Ecosystem Impact

#### 5.1 Skill Taxonomy Position

`/nuclear-sop` occupies a unique niche in Jerry's skill taxonomy that no existing skill fills:

```
Jerry Skill Ecosystem (21 skills with /nuclear-sop):

COORDINATION LAYER:
  /orchestration -- Multi-agent pipeline coordination
  /nuclear-sop   -- Single-procedure step-level discipline  <-- NEW POSITION

ANALYTICAL LAYER:
  /problem-solving -- Research, analysis, synthesis, architecture
  /nasa-se         -- Requirements, V&V, formal reviews

DOMAIN LAYER:
  /eng-team    -- Secure software engineering methodology
  /red-team    -- Offensive security testing
  /pm-pmm      -- Product management and marketing

QUALITY LAYER:
  /adversary   -- Adversarial quality reviews and scoring

CONTENT LAYER:
  /diataxis        -- Documentation methodology
  /prompt-engineering -- Prompt construction
  /use-case        -- Use case authoring
  /test-spec       -- BDD test specification
  /contract-design -- API contract generation

UTILITY LAYER:
  /worktracker     -- Entity management
  /transcript      -- Meeting note extraction
  /ast             -- Markdown structural analysis
  /saucer-boy      -- Conversational voice
  /saucer-boy-framework-voice -- Framework output voice
  /architecture    -- Design decisions
  /user-experience -- UX methodology
```

Nuclear-sop sits in the **Coordination Layer** alongside `/orchestration`, but at a different abstraction level. Orchestration coordinates across skills and phases; nuclear-sop enforces discipline within a single procedure execution. This is analogous to the distinction between a project manager (orchestration) and a quality inspector on the factory floor (nuclear-sop).

#### 5.2 Architectural Implications

**H-36 Governance Question (UNRESOLVED):** The most significant architectural implication is the pending H-36 governance question: does a predetermined intra-skill agent sequence constitute "hops" under the circuit breaker? The current language in `agent-routing-standards.md` ("What Counts as a Hop" table) states that "Agent-to-agent transition within a skill" DOES count as a hop, which would make the 4-hop C3+ mode non-compliant. The skill specification proposes an alternative interpretation (predetermined sequences should not count) and includes a 60-day deadline with a fallback design (eliminate sop-verifier, use 3-hop anchored mode permanently). This question affects not just `/nuclear-sop` but any existing or future skill with multi-agent predetermined sequences -- including `/eng-team`'s 8-step workflow and `/adversary`'s 3-agent tournament, neither of which has an explicit governance ruling on their hop accounting.

**Skill Count at Phase 2 Routing Threshold:** At 21 skills, Jerry sits one above the H-37 Phase 1 upper bound (20). While the comprehensive collision analysis shows no unresolved collisions today, the framework should begin monitoring Phase 2 transition triggers (10+ collision zones, false negative rate > 40%, user override rate > 30%). This is a monitoring action, not a blocking concern.

**OE Infrastructure as Framework Pattern:** The `/nuclear-sop` OE entry schema (mandatory fields, write-time validation, workflow_type classification) could become a Jerry-wide pattern for structured lessons capture. Currently, docs/experience/ is an unstructured dumping ground. Nuclear-sop's mandatory schema imposes structure that enables targeted synthesis. If proven valuable, this pattern should be evaluated for adoption by other skills (e.g., /eng-team post-engagement, /orchestration post-workflow).

#### 5.3 Trade-Off Assessment

| Trade-Off | Benefit | Cost | Recommendation |
|-----------|---------|------|---------------|
| Adding procedural overhead to workflows | Error prevention via STAR, pre-job context validation, institutional memory via OE | Token consumption (~2x for STAR; additional agent invocations for brief/capture) | Apply to C2+ only; C1 exempt per specification |
| 4-hop mode for C3+ | Context-isolated verification prevents anchoring bias | Exceeds H-36 under current "What Counts as a Hop" table language; governance question pending | Implement 3-hop mode for Phase 1; implement 4-hop mode contingent on governance ruling |
| Mandatory OE capture | Feedback loop enables continuous improvement | Every execution produces an OE entry (storage overhead; synthesis burden) | STOP hard limit at 20 unanalyzed entries forces synthesis; prevents unbounded accumulation |
| New skill raises ecosystem complexity | Nuclear rigor for high-stakes workflows | One more skill to maintain; triggers routing threshold evaluation | Natural keyword isolation minimizes routing complexity; maintenance burden is proportional to skill size (16 files) |

#### 5.4 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Routing confusion between /nuclear-sop and /orchestration | Low | Medium | Negative keywords "multi-phase" and "pipeline coordination" on nuclear-sop; compound triggers for nuclear-specific terms |
| Adoption failure (users never create workflow definitions) | Medium | High | Pre-build pilot validation (specification Section 3.0); sop-brief Step 0 generates from natural language; worked example as starting point |
| H-36 governance deadlock | Medium | High | 60-day deadline with documented fallback; fallback design is functional for all criticality levels |
| STAR provides no measurable error prevention | Medium | High | Section 1.5a A/B validation protocol; Phase 1 gate blocks advancement if STAR fails |
| GAP-09 behavioral drift monitoring is premature | Medium | Low | Phase-gated implementation; scenario infrastructure is lightweight; defers to after /nuclear-sop proves value |
| Skill count triggers Phase 2 routing migration | Low | Medium | No keyword collisions found in comprehensive analysis; continue monitoring transition triggers |
| "sop" standalone keyword false-matches general SOP requests | Medium | Low | Recommend compound-trigger-only matching for "sop"; standalone "sop" should not be a positive keyword |

#### 5.5 Recommendations

1. **Proceed with Phase 1 build** after pre-build pilot validation passes. The integration analysis confirms zero blocking dependencies and no unresolved routing collisions in the comprehensive keyword analysis.

2. **File the H-36 governance question immediately** upon Phase 1 delivery, as an ADR tracked via worktracker with a 60-day deadline. The predetermined intra-skill sequence interpretation has framework-wide implications for any skill with multi-agent sequences (nuclear-sop, eng-team, adversary).

3. **Add "multi-phase" and "pipeline coordination" as nuclear-sop negative keywords** beyond what the specification currently includes, to prevent /orchestration collision on ambiguous "workflow" requests.

4. **Treat standalone "sop" as compound-trigger-only.** Do not include bare "sop" as a standalone positive keyword. Only match "sop" when it appears in compound triggers ("nuclear sop", "sop brief", "sop execute", "sop capture", "sop verify") to prevent false-positive routing on general standard operating procedure requests.

5. **Begin Phase 2 routing threshold monitoring** when the skill is registered. Track the three transition triggers (collision zones, false negative rate, user override rate) to determine if Phase 2 routing architecture is needed.

6. **Defer GAP-09 behavioral drift monitoring** to after Phase 1 acceptance. The STAR validation (Section 1.5a) produces the first behavioral baseline data that GAP-09 builds on. Implementing GAP-09 before STAR is validated puts the cart before the horse.

7. **Evaluate OE entry schema for framework-wide adoption** after Phase 3 demonstrates the feedback loop. If OE entries prove valuable for nuclear-sop workflows, propose extending the pattern to /eng-team and /orchestration.

---

## References

1. `/nuclear-sop` Skill Specification Synthesis v2.0.0 (`ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md`) -- Complete skill specification including agent taxonomy, STAR protocol, hold points, OE schema, implementation roadmap. Primary source for all nuclear-sop capability claims.

2. Nuclear SOP Pattern Extraction v2 (`ps/phase-2/ps-analyst-001/sop-pattern-extraction.md`) -- 22 nuclear patterns, gap analysis (GAP-01 through GAP-09), priority ranking. Source for GAP-09 reclassification and behavioral drift monitoring concept.

3. `/eng-team` SKILL.md v1.0.0 (`skills/eng-team/SKILL.md`) -- 10-agent secure engineering skill. Source for eng-team capability analysis, 8-step workflow, SDLC governance model.

4. `/orchestration` SKILL.md v2.2.0 (`skills/orchestration/SKILL.md`) -- Multi-agent workflow orchestration. Source for orchestration capability analysis, workflow patterns, state schema, quality gate integration.

5. `/adversary` SKILL.md v1.0.0 (`skills/adversary/SKILL.md`) -- Adversarial quality reviews. Source for adversary capability analysis, S-014 scoring, tournament mode, strategy catalog.

6. `/problem-solving` SKILL.md v2.2.0 (`skills/problem-solving/SKILL.md`) -- Structured problem-solving framework. Source for ps-agent capabilities, creator-critic-revision cycle, FC-M-001 pattern.

7. Agent Routing Standards v1.1.0 (`.context/rules/agent-routing-standards.md`) -- Layered routing architecture, enhanced trigger map format, circuit breaker specification, multi-skill combination protocol. Source for routing methodology analysis. Key reference: "What Counts as a Hop" table (line 273) explicitly states "Agent-to-agent transition within a skill" counts as a hop.

8. Agent Development Standards v1.2.0 (`.context/rules/agent-development-standards.md`) -- Handoff protocol, tool tiers, cognitive modes, FC-M-001 fresh context pattern, context budget standards CB-01 through CB-05. Source for composition pattern analysis and context window constraints.

9. Mandatory Skill Usage (`.context/rules/mandatory-skill-usage.md`) -- Current trigger map (5-column format), H-22 proactive skill invocation. Source for comprehensive routing collision analysis (all 16 existing skill entries cross-referenced against all 20+ proposed nuclear-sop keywords).

---

## PS Integration

**PS ID:** phase-5.1
**Entry ID:** e-005
**Artifact:** `projects/PROJ-0039-nuclear-engineer/research/skill-integration-analysis.md`
**Confidence:** HIGH (0.88)

**State output:**
```yaml
researcher_output:
  ps_id: "phase-5.1"
  entry_id: "e-005"
  artifact_path: "projects/PROJ-0039-nuclear-engineer/research/skill-integration-analysis.md"
  summary: "Nuclear-sop is complementary to all analyzed skills with no routing collisions in comprehensive keyword analysis. H-36 C3+ 4-hop compliance is UNRESOLVED pending governance ruling. Four agents are autonomous as a 3-hop unit (C1-C2); 4-hop mode (C3+) contingent on ruling. GAP-09 behavioral drift monitoring is feasible (~50-60% infrastructure reuse; /schedule does not exist, periodic triggering requires alternative mechanism)."
  sources_count: 9
  confidence: "high"
  next_agent_hint: "ps-architect for integration ADR or build pipeline to begin Phase 1 construction"
```

**Key findings for downstream agents:**
1. No routing collisions identified in comprehensive keyword analysis (all 20+ keywords cross-referenced); recommend compound-trigger-only matching for standalone "sop"
2. H-36 governance question is the single blocking architectural concern for C3+ workflows -- the 4-hop mode's compliance is UNRESOLVED; the 3-hop mode is compliant for C1-C2
3. Nuclear-sop agents are autonomous as a 3-hop unit (C1-C2); 4-hop mode (C3+) requires H-36 governance ruling
4. GAP-09 is feasible with ~50-60% infrastructure reuse; /schedule does not exist -- periodic triggering needs alternative mechanism; defer to after STAR validation
5. Recommended negative keyword additions: "multi-phase", "pipeline coordination", "research", "investigate", "root cause", "threat model", "STRIDE", "secure design"
6. Skill count at 21 crosses H-37 threshold; monitoring (not action) recommended
7. Composition patterns (nuclear-sop + eng-team, nuclear-sop + orchestration) require MAIN CONTEXT orchestration per P-003; sop-executor does not delegate to other agents
8. Large compositions (12-agent nuclear-sop + eng-team) require cross-session execution per context window constraints (CB-02)

---

## Revision History

| Version | Date | Changes | Trigger |
|---------|------|---------|---------|
| 1.0.0 | 2026-03-25 | Initial research artifact | Phase 5.1 skill integration analysis |
| 1.1.0 | 2026-03-25 | Revised per ps-critic critique (score 0.84 -> target >= 0.90). Findings R-01 through R-06 addressed. **R-01:** Rewrote L0 executive summary and Section 1.1.C to explicitly state H-36 C3+ compliance is UNRESOLVED; removed unsupported eng-team 1-hop comparison, reframed as analogy pending same governance ruling. **R-02:** Verified /schedule does NOT exist; updated GAP-09 Sections 4.2, 4.3, 4.4, 4.5 with verification note, alternative triggering mechanisms, and revised infrastructure reuse from 60-70% to 50-60%. **R-03:** Completed comprehensive collision table for ALL 20+ keywords; recommended compound-trigger-only matching for standalone "sop"; changed verdict from "zero unresolved collisions" to "no collisions identified in comprehensive keyword analysis." **R-04:** Added P-003 clarification to all composition patterns (Sections 1.3.C, 1.4.C) stating MAIN CONTEXT orchestrates all agent invocations; sop-executor does not delegate via Task. **R-05:** Added context window budget constraints subsection to Section 1.4.C (Pattern 1) noting cross-session execution requirement for 12-agent compositions, with CB-02 reference and recommended session break points. **R-06:** Reframed eng-team/adversary hop count as analogy requiring same governance ruling, not as established fact; cited "What Counts as a Hop" table language explicitly. | ps-critic critique, iteration 1 |

---

*Research Version: 1.1.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-003, P-004, P-011, P-022)*
*Methodology: Pairwise skill comparison (overlap/complement/composition/routing), autonomy capability matrix, GAP-09 cross-skill design synthesis*
*Created: 2026-03-25*
*Revised: 2026-03-25*
*Agent: ps-researcher*
