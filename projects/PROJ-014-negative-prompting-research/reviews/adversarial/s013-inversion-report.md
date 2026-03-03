# Strategy Execution Report: Inversion Technique (S-013)

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverable 1:** `projects/PROJ-014-negative-prompting-research/prompts/orchestration-mega-prompt-template.md`
- **Deliverable 2:** `projects/PROJ-014-negative-prompting-research/prompts/orchestration-behavioral-constraints.md`
- **Executed:** 2026-03-02T00:00:00Z
- **Finding Prefix:** IN (per template Identity section)
- **Goals Analyzed:** 5 explicit + 4 implicit = 9 total
- **Assumptions Mapped:** 14
- **Vulnerable Assumptions:** 11 (6 Critical, 4 Major, 1 Minor)
- **H-16 Note:** S-003 Steelman not listed in prior outputs. S-013 is not directly blocked by H-16 (H-16 names S-002/S-004/S-001); proceeding per template Integration section which clarifies S-013 is not H-16-gated. Findings noted where the absence of steelman strengthening creates additional exposure.

---

## Summary

Inversion analysis of 22 NPT-013 constraints across 7 domains reveals that the deliverables carry significant assumption debt concentrated in three failure clusters: (1) the constraints assume a C4-scale operational environment that does not match simpler workflows, causing overhead-induced productivity destruction when applied at C1/C2 criticality; (2) several constraints contain internal loops that, when followed literally, produce unbounded escalation chains (AQ-1 feeding AQ-5 feeding AQ-3 feeding AQ-1); and (3) the 0.95 quality threshold is assumed achievable by current tooling but has no validated baseline, making the gate a potential permanent blocker. 11 of 14 mapped assumptions fail stress-testing at Major or Critical severity. Recommendation: **REVISE before broad adoption** -- the constraint set is architecturally sound for C4 workflows but requires explicit scope guards, loop-termination conditions, and a validated threshold baseline before deployment as a `.claude/rules/` file applied unconditionally.

---

## Step 1: Goal Inventory

| # | Goal | Type | Specific, Measurable Form |
|---|------|------|--------------------------|
| G1 | Achieve high behavioral compliance for multi-agent orchestration | Explicit | NPT-013 compliance rate >= 100% (claimed in deliverable header: "100% vs 92.2%") |
| G2 | Prevent quality degradation from uncontrolled orchestration | Explicit | No phase output below 0.95 threshold reaches downstream agents (AQ-1) |
| G3 | Be adopted without modification for new C4 projects | Explicit | Template placeholder swap is the only required change |
| G4 | Outperform positive-only framing | Explicit | Statistical claim: p=0.016, measured compliance delta of 7.8 percentage points |
| G5 | Scale across diverse orchestration scenarios | Implicit | Constraints apply correctly to any /orchestration + skill-agent combination |
| G6 | Avoid creating worse outcomes than having no constraints | Implicit | Net effect of constraint adoption is positive across all usage contexts |
| G7 | Maintain C1/C2 productivity for simpler tasks | Implicit | Overhead introduced by constraints does not destroy value for non-C4 work |
| G8 | Terminate gracefully when quality thresholds are not met | Implicit | Circuit breakers fire; no infinite loops; user is notified |
| G9 | Constraints interact coherently without producing contradictions | Implicit | 22 constraints form a consistent behavioral system with no internal conflicts |

---

## Step 2: Anti-Goals (Goal Inversions)

To **guarantee failure** at these goals, we would:

- **Against G1 (compliance):** Apply constraints so rigidly that agents spend all cycles on compliance theater rather than productive work. Or apply them to contexts (C1, quick fixes) where compliance is unmeasurable.
- **Against G2 (quality gate):** Set the threshold to a level (0.95) that no real deliverable achieves, causing permanent pipeline stall at the first phase gate.
- **Against G3 (adoption without modification):** Embed assumptions (C4 always, /adversary always, /red-team always) that do not match the majority of Jerry project workflows, forcing every adopter to modify constraints before use.
- **Against G4 (outperform positive framing):** Apply NPT-013 constraints in a context where the 7.8pp compliance delta does not hold (e.g., experienced teams where the LLM already follows positive instructions reliably), eroding the statistical rationale.
- **Against G5 (scale):** Constraints reference specific Jerry skills (/eng-team, /red-team, /adversary) that are not universally available, causing constraint violations to trigger on otherwise valid workflows that simply do not use those skills.
- **Against G6 (net positive):** Generate so much overhead (worktracker entity per sub-task, WebSearch before every decision, adversarial gate at every phase boundary) that adoption actually degrades throughput without commensurate quality gain.
- **Against G7 (C1/C2 productivity):** The rule file has no scope guard -- it applies to ALL sessions including trivial C1 bug fixes, demanding full adversarial review (9 strategies, AQ-1 through AQ-5) before a 3-line patch can be handed off.
- **Against G8 (graceful termination):** AQ-1 requires returning output to creator if below threshold; AQ-3 requires re-running adversarial gate after revision; AQ-5 halts pipeline at first failing gate. These three constraints, followed literally on the same output, create a triangular loop: fail gate -> return to creator -> revise -> re-run gate -> fail gate -> return to creator...
- **Against G9 (coherence):** EC-2 requires WebSearch before every decision; SI-1 requires worktracker entity before work; DA-1 forbids main-context work. A literal reading requires creating a worktracker entity (main context work?) before delegating to an agent (which requires WebSearch before the decision to delegate?).

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| IN-001 | Critical | Missing criticality scope guard -- constraints apply to C1/C2 workflows without modification | Usage / Scope |
| IN-002 | Critical | AQ-1 + AQ-3 + AQ-5 form a potential infinite escalation loop | Adversarial Quality Gates |
| IN-003 | Critical | 0.95 threshold unvalidated -- may be permanently unachievable for typical deliverables | AQ-1, Quality Gate element |
| IN-004 | Critical | DA-1 prohibits main-context work but SI-1 requires main-context worktracker creation -- direct conflict | Agent Delegation / State |
| IN-005 | Critical | EC-2 (WebSearch before every decision) makes atomic operations impossible and destroys C2 throughput | Evidence and Claims |
| IN-006 | Critical | AQ-4 (separate agent per strategy) requires 9+ parallel Task invocations -- exceeds realistic resource bounds and H-01 single-level nesting architecture | Adversarial Quality Gates |
| IN-007 | Major | IT-1 + IT-2 hard-require /eng-team and /red-team -- projects without these skills installed will never satisfy constraints | Implementation and Testing |
| IN-008 | Major | PC-2 ("no human review needed") sets an unachievable bar that blocks all delivery when automated pipeline gaps exist | Prompt Craft |
| IN-009 | Major | EC-1 (cite every fact) applied literally to internal orchestration handoffs produces unmaintainable annotation overhead | Evidence and Claims |
| IN-010 | Major | OP-2 (full Mermaid diagram) + OP-1 (all paths in plan) applied before scope is known forces premature specification that must be reworked | Plan Fidelity |
| IN-011 | Minor | SI-2 (real-time worktracker updates) conflicts with DA-1 (no main-context work) for parallel agent execution | State and Documentation Integrity |

---

## Detailed Findings

### IN-001: Missing Criticality Scope Guard [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Usage section of orchestration-behavioral-constraints.md; implicit in mega-prompt template |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
The Usage section states: "These constraints apply to multi-agent orchestration workflows -- any task that uses `/orchestration`, `/problem-solving`, `/eng-team`, `/red-team`, or `/adversary` in combination." The mega-prompt template header says: "Quality gate: C4 adversarial review at every phase boundary." The `.claude/rules/` placement mechanism (via L2-REINJECT) injects these constraints into EVERY session, not only C4 sessions.

**Analysis:**
The Inversion: "A user applies these constraints to a C1 bug fix that uses /problem-solving." Result: AQ-1 requires /adversary at C4 before handoff. AQ-4 requires 9 separate agent invocations. AQ-5 requires per-phase gates. IT-4 requires a failing test before the bug fix. EC-2 requires WebSearch before the fix decision. A single-file bug fix that should take 5 minutes becomes a multi-hour ceremonial compliance exercise. The L2-REINJECT marker at rank=3 fires on every prompt, making there no escape for users who legitimately use /problem-solving for simple tasks.

The quality-enforcement.md SSOT explicitly defines C1 as "HARD rules only; S-010 optional." These constraints far exceed C1 enforcement. There is no mechanism in either deliverable to detect task criticality and apply proportional constraint enforcement. The constraint set is therefore almost guaranteed to produce worse outcomes than no constraints for C1/C2 work.

**Plausibility:** Very high. The Jerry framework is regularly used for C1/C2 tasks. The L2-REINJECT fires unconditionally.

**Recommendation:**
Add a criticality-detection guard at the top of the rule file and the constraint block:
```
## Scope Guard
These constraints apply ONLY to C3 and C4 criticality workflows. For C1/C2 tasks
(reversible in 1 session/day, < 10 files), do not apply AQ-1 through AQ-5, IT-1
through IT-5, or EC-2. C1/C2 minimum: DA-1, SI-1, EC-1 only.
```
Remove the L2-REINJECT or scope it explicitly to sessions with JERRY_PROJECT set to a C3+ work item.

**Acceptance Criteria:** The rule file and template both explicitly state criticality applicability. A C1 bug fix session does NOT trigger AQ-1, AQ-4, or IT-4.

---

### IN-002: AQ-1 + AQ-3 + AQ-5 Form an Infinite Escalation Loop [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Adversarial Quality Gates (AQ-1, AQ-3, AQ-5) |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
- AQ-1: "NEVER allow a creator agent to hand off output downstream without first launching /adversary... and confirming the adversarial quality score is >= 0.95... if below threshold, return output to the creator with critic findings."
- AQ-3: "NEVER leave critic feedback unaddressed... route all critic feedback back to the originating creator agent... then re-run the adversarial gate on the revised output."
- AQ-5: "NEVER allow a phase output below the quality threshold to flow as input to the next phase... halt the pipeline at the first failing gate."

**Analysis:**
Trace the execution path when a creator agent's output scores 0.88 (below 0.95):
1. AQ-1 fires: "Do not hand off. Return to creator with findings."
2. Creator revises. Re-runs adversarial gate. Scores 0.91. Still below 0.95.
3. AQ-3 fires: "Feedback unaddressed. Return to creator. Re-run gate."
4. Creator revises again. Scores 0.93. Still below 0.95.
5. AQ-5 fires: "Pipeline halted. Gate failed."

The circuit-breaker in AQ-2 declares a CEILING (default 10 for C4). But AQ-2's ceiling is declared in the Orchestration Plan -- it is not embedded in the constraints themselves. An agent reading only the constraint file sees three constraints that interact without a stated exit condition beyond AQ-2's ceiling. If the LLM does not correlate AQ-2's ceiling with AQ-1 and AQ-3's "return and retry" instructions, it enters an infinite revision loop.

Worse: AQ-5 says "halt the pipeline at the first failing gate." AQ-1 says "return to creator (not halt)." These are contradictory termination behaviors for the same triggering condition (below-threshold score). An LLM following both constraints literally cannot resolve which action to take.

**Plausibility:** High. These are separate, independently-worded constraints. There is no explicit cross-reference between them. An LLM reading them in the context of a failing phase will attempt to satisfy all three simultaneously.

**Recommendation:**
(a) Add explicit cross-references: "AQ-1 revision cycles are bounded by AQ-2's declared ceiling. When the ceiling is reached, AQ-5 governs: halt and escalate to user." (b) Resolve the AQ-1 vs AQ-5 contradiction: below-threshold output either returns to creator (AQ-1) OR halts (AQ-5), not both. Specify: AQ-1 applies within a phase; AQ-5 applies at phase boundary. (c) Add a numeric loop guard directly in AQ-3: "after N returns (default: 3), escalate to user rather than continuing."

**Acceptance Criteria:** An agent receiving below-threshold output can unambiguously determine whether to (a) return to creator, (b) halt and escalate, or (c) accept with findings -- with a finite termination condition for each path.

---

### IN-003: 0.95 Threshold Is Unvalidated and May Be Permanently Unachievable [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | AQ-1, Quality Gate element of mega-prompt template |
| **Strategy Step** | Step 3 (Assumption Mapping) and Step 4 (Stress-Test) |

**Evidence:**
AQ-1: "confirming the adversarial quality score is >= 0.95." The mega-prompt template: "Quality gate: C4 adversarial review at every phase boundary. Threshold: >= {{QUALITY_THRESHOLD}} (recommend 0.95 for C4 deliverables)." The quality-enforcement.md SSOT threshold is >= 0.92. The deliverables recommend 0.95, which is above the SSOT baseline.

**Analysis:**
The Inversion: "What if 0.95 is never achievable for a given deliverable type?" The deliverables provide no empirical evidence that 0.95 is routinely achievable for the deliverable types they target (orchestration plans, ADRs, research outputs). The S-014 LLM-as-Judge rubric uses 6 dimensions weighted at 0.20/0.20/0.20/0.15/0.15/0.10. For a composite of 0.95, every dimension must score approximately 0.95 on average -- a very high bar. If any dimension consistently scores 0.85 (e.g., Traceability for early-phase research), the composite will fall below 0.95 even with perfect performance on other dimensions.

Result: A team adopting these constraints at face value for an orchestration plan may find their pipeline permanently stalled at Phase 1 because the research output cannot clear 0.95 on Evidence Quality (WebSearch results are inherently uncertain). The circuit breaker fires at 10 iterations with no improvement. The user is notified of a "failure" -- but the failure is a miscalibrated threshold, not a genuinely inadequate deliverable.

The statistical claim (100% compliance, p=0.016) is about LLM behavioral compliance with the constraint format, not about deliverable quality scores. These are different measurements. The threshold recommendation is not grounded in the cited research.

**Plausibility:** High for research-heavy phases. Medium for implementation phases.

**Recommendation:**
(a) Provide calibration guidance: reference the SSOT threshold (0.92) as the baseline, and require explicit justification with measurement data before recommending 0.95 for a given workflow. (b) Add a note in the mega-prompt template: "If your workflow has not previously measured S-014 scores for this deliverable type, use 0.92 until a baseline is established." (c) Add to AQ-1: "If the threshold is consistently not met after 3 iterations with substantive revision, consider whether the threshold is miscalibrated rather than the deliverable inadequate."

**Acceptance Criteria:** The threshold recommendation is backed by a reference to measured S-014 baselines for orchestration workflows, or is reduced to 0.92 (SSOT) with explicit justification required for higher values.

---

### IN-004: DA-1 Prohibits Main-Context Work But SI-1 Requires It [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Agent Delegation (DA-1), State and Documentation Integrity (SI-1) |
| **Strategy Step** | Step 3 (Assumption Mapping) and Step 4 (Stress-Test) |

**Evidence:**
- DA-1: "NEVER execute research, analysis, design, implementation, testing, or quality-review work directly in the main context."
- SI-1: "NEVER begin execution on a work item without first creating the corresponding /worktracker entity."

Creating a /worktracker entity requires: (a) invoking the /worktracker skill, (b) executing `jerry items create` or equivalent tool calls, (c) writing WORKTRACKER.md. All of these are work executed in the main context. The /worktracker creation IS work. DA-1 bans it. SI-1 mandates it.

**Analysis:**
The Inversion: "An agent reads DA-1 and SI-1 simultaneously. To comply with DA-1, it must not execute any work in main context. To comply with SI-1, it must create a worktracker entity before starting. Creating the entity is work in the main context. The agent is blocked."

This is not a theoretical edge case. It is the first action in every workflow: you must create tracking entities before delegating work, and creating tracking entities is work performed in the main context. A sufficiently literal LLM following both constraints will loop: "I cannot do work in main context (DA-1) but I must create a worktracker entity (SI-1) which is work in the main context. I am blocked."

**Plausibility:** High in strict interpretation scenarios. The constraint wording does not carve out "orchestration housekeeping" from DA-1's prohibition.

**Recommendation:**
Refine DA-1 to explicitly exclude coordination and state-management actions from the main-context prohibition: "NEVER execute research, analysis, design, implementation, testing, or quality-review work directly in the main context. Orchestration-only actions (worktracker entity creation, handoff routing, status updates, circuit-breaker decisions) are explicitly permitted in the main context."

**Acceptance Criteria:** DA-1 and SI-1 can both be satisfied without contradiction in the first minute of a new workflow.

---

### IN-005: EC-2 Requires WebSearch Before Every Decision -- Destroys Throughput [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Evidence and Claims (EC-2) |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
EC-2: "NEVER make an architectural, design, or implementation decision without first querying WebSearch and WebFetch -- Consequence: decisions based solely on training-data knowledge may reflect outdated practices or incompatible library versions. Instead: invoke WebSearch to retrieve current consensus and WebFetch for authoritative documentation, then cite both in the decision rationale."

The constraint applies to: architectural decisions, design decisions, AND implementation decisions. In a multi-phase orchestration pipeline with 6+ phases, there may be hundreds of implementation decisions: which error handling pattern to use, how to name a variable, which test assertion style to use, whether to use a list comprehension or a for loop.

**Analysis:**
The Inversion: "A team adopts EC-2 and applies it literally." Every micro-decision in implementation triggers a WebSearch + WebFetch call. A 200-line module might require 40 decisions. 40 WebSearch calls plus 40 WebFetch calls = 80 external lookups for one module. Pipeline throughput collapses. Context window fills rapidly with search results. The "instead" clause says "cite both in the decision rationale" -- a 200-line module would require a 200-entry citation appendix.

Even at the architectural level: an agent deciding whether to use dependency injection vs. service locator makes one architectural decision. EC-2 requires WebSearch + WebFetch before this decision. Fine. But EC-2's language ("NEVER make an... implementation decision") does not distinguish between strategic decisions (which pattern to use) and tactical decisions (how to name a function). Literally followed, it creates an unworkable overhead loop.

The consequence stated in EC-2 ("decisions may reflect outdated practices") applies specifically to library version choices and current best practices -- not to internal design choices governed by established patterns. The constraint is calibrated for the wrong granularity.

**Plausibility:** Very high for any implementation-heavy workflow.

**Recommendation:**
Scope EC-2 to the decision types where outdated training knowledge is a real risk: "NEVER make a library selection, external dependency version choice, or technology adoption decision without first querying WebSearch and WebFetch. Internal design decisions (naming, pattern application within an established architecture) do not require external validation."

**Acceptance Criteria:** EC-2 triggers for library selection and technology adoption decisions. EC-2 does NOT trigger for internal implementation choices within an established architecture.

---

### IN-006: AQ-4 Requires 9+ Separate Agent Invocations -- Exceeds Architecture Limits [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Adversarial Quality Gates (AQ-4) |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
AQ-4: "NEVER assign all adversarial strategies to a single agent -- Consequence: a single agent's blind spots apply uniformly across all strategies, defeating the independence that makes multi-strategy review effective. Instead: assign each adversarial strategy (S-001 through S-014) to a separate agent invocation so that each strategy executes with an independent context window free of prior strategy bias."

The mega-prompt template lists 9 strategies: S-001, S-002, S-003, S-004, S-007, S-010, S-012, S-013, S-014. AQ-4 requires each to run in a separate agent invocation. AQ-5 requires this at "every major phase boundary." A 6-phase pipeline would require 6 x 9 = 54 separate adversarial agent invocations.

**Analysis:**
The Inversion: "What happens when an agent follows AQ-4 literally?" Each invocation is a Task tool call. The H-01/P-003 constraint limits the architecture to one nesting level: orchestrator -> worker. The orchestrator must spawn and manage 9 simultaneous (or sequential) Task calls per phase gate. With 6 phases, the orchestrator manages 54 Task calls total, each requiring a handoff in and a result out. The orchestrator's context fills with handoff state.

The /adversary skill's own agent (adv-executor) can run multiple strategies against a single deliverable in one invocation -- this is the designed workflow. AQ-4's prohibition on "single agent" means the adv-executor cannot be used as designed; instead, each strategy becomes its own invocation. This contradicts the /adversary skill architecture. The constraint as written is incompatible with the Jerry agent hierarchy at scale.

Furthermore, a 6-phase pipeline with 9 adversarial agents per phase = 54 Task invocations + 6 phases of creator work = 60+ agent invocations. At realistic turn limits, this is not executable within a single Jerry session.

**Plausibility:** High for any non-trivial orchestration pipeline.

**Recommendation:**
(a) Clarify that "separate agent invocation" means separate adv-executor Task calls per strategy -- not separate top-level orchestrator spawns. (b) Add a practical bound: "For C4 workflows, strategies S-001 through S-014 SHOULD be executed in separate adv-executor invocations; for C3 workflows, grouping 2-3 strategies per invocation is acceptable provided each group maintains independent context." (c) Consider that adv-executor already handles one strategy at a time -- AQ-4 is satisfied by using adv-executor correctly, not by requiring 9 top-level Task calls.

**Acceptance Criteria:** AQ-4 compliance is achievable within the H-01 agent hierarchy without requiring more than the framework's designed invocation patterns.

---

### IN-007: IT-1 and IT-2 Hard-Require Skills That May Not Be Installed [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Implementation and Testing (IT-1, IT-2) |
| **Strategy Step** | Step 3 (Assumption Mapping) and Step 4 (Stress-Test) |

**Evidence:**
- IT-1: "NEVER implement application code without delegating to /eng-team agents."
- IT-2: "NEVER perform security testing or vulnerability assessment without delegating to /red-team agents."

Both constraints use NEVER, making them HARD prohibitions. Both reference specific Jerry skills (/eng-team, /red-team) that are registered skills in the framework but may not be installed or available in all deployments.

**Analysis:**
The Inversion: "A team adopts these constraints but operates in a Jerry deployment without /red-team installed (e.g., they use Jerry only for documentation and research workflows, not security testing)." IT-2 prohibits security testing without /red-team. If /red-team is not installed, IT-2 cannot be satisfied and security testing cannot proceed at all -- not even a basic security review using /problem-solving. The constraint does not provide a fallback for absent skills.

Similarly, a project team using Jerry for a non-software deliverable (research report, policy document) has no use for /eng-team. IT-1's prohibition on main-context implementation is nonsensical in that context. Yet the rule file applied via `.claude/rules/` fires on all sessions.

**Plausibility:** High for non-software teams. Medium for software teams without all Jerry skills installed.

**Recommendation:**
Add conditional applicability: "IT-1 applies when the deliverable includes application code. IT-2 applies when the deliverable includes security-relevant systems or components. If /eng-team or /red-team are not installed in the current Jerry deployment, escalate to the user rather than blocking all implementation."

**Acceptance Criteria:** IT-1 and IT-2 do not block non-software workflows. Absent skills produce escalation, not constraint violation.

---

### IN-008: PC-2 Sets an Unachievable Bar That Blocks All Delivery [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Prompt Craft (PC-2) |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
PC-2: "NEVER produce code that requires human manual review to reach production quality -- Consequence: mandatory human review indicates an incomplete automated quality pipeline. Instead: ensure all code passes automated linting, type checking, >= 90% test coverage, and adversarial quality scoring >= 0.95, so that human review is an optional audit."

**Analysis:**
The Inversion: "What if the automated pipeline has a gap that cannot be closed without human judgment?" Legal compliance validation, ethical review of AI system outputs, architectural decisions involving business-domain tradeoffs, security threat modeling for novel attack surfaces -- these are categories where human review is not merely a quality gap but a governance requirement. PC-2 as written prohibits producing code if any of these human review requirements exist.

Worse: "requires human manual review" is defined by the consequence ("indicates an incomplete automated pipeline") rather than the condition. An agent that produces code passing all automated checks but where a human reviewer would nonetheless recommend changes is technically in compliance. But an agent that produces code where governance requires a human sign-off (e.g., SOC2 compliance review) cannot comply with both PC-2 (NEVER require human review) and the governance requirement (human review required). The constraint creates a compliance trap.

The "optional audit" framing in the Instead clause acknowledges that human review exists but re-labels it as "optional." This is semantically deceptive -- governance-required human review is not optional by definition.

**Plausibility:** High for any regulated-domain software project.

**Recommendation:**
Revise PC-2 to: "NEVER produce code where human review is required ONLY because automated quality checks have not been applied. Automated linting, type checking, and >= 90% test coverage are prerequisites, not substitutes for governance-required human review." Remove the 0.95 adversarial scoring requirement from PC-2 (this is already covered by AQ-1); the duplication creates a second unvalidated threshold reference.

**Acceptance Criteria:** PC-2 does not prohibit code delivery in contexts with legitimate governance-required human review.

---

### IN-009: EC-1 Applied to Internal Handoffs Creates Unmaintainable Annotation Overhead [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Evidence and Claims (EC-1) |
| **Strategy Step** | Step 3 (Assumption Mapping) and Step 4 (Stress-Test) |

**Evidence:**
EC-1: "NEVER state a fact without a traceable citation and NEVER proceed on an assumption without documenting it as unverified -- Consequence: uncited facts and undocumented assumptions appear as verified findings to downstream agents... Instead: cite every factual claim with its source (URL, file path, or document reference), and mark every assumption as '[ASSUMPTION: unverified]' with a verification plan."

**Analysis:**
The Inversion: "An agent applies EC-1 to an internal orchestration handoff." The handoff contains statements like: "Research phase is complete. The optimal architecture for this use case is hexagonal architecture." These are facts (to the agent making the handoff). Under EC-1, every such statement requires a traceable citation. The citation for "hexagonal architecture is appropriate" would require pointing to: (a) the research output file, (b) the specific section, (c) the WebSearch results, (d) the ADR. A 500-token handoff becomes a 3,000-token citation appendix.

Multiply across a 6-phase pipeline with 10+ handoffs and the citation overhead becomes a material driver of context window exhaustion, triggering the very compaction problem that DA-1 is designed to prevent. EC-1 and DA-1 are working against each other: EC-1 inflates handoff size; DA-1 requires main-context parsimony.

The constraint was evidently designed for research claims (where citation is critical) but is scoped to "any fact" with no distinction between research-phase claims and implementation-phase decisions.

**Plausibility:** High. The constraint is worded absolutely: "NEVER state a fact without a citation." Internal state transitions are facts.

**Recommendation:**
Scope EC-1 to external claims: "NEVER state a fact derived from external sources (literature, web search, documentation) without a traceable citation. Internal state transitions, workflow decisions, and in-session observations do not require external citations but SHOULD reference the artifact or phase that produced them."

**Acceptance Criteria:** EC-1 does not inflate internal handoff size. Research claims continue to require full citations. Handoff size remains proportional to handoff content.

---

### IN-010: OP-1 + OP-2 Force Premature Specification Before Scope Is Known [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Orchestration Plan Fidelity (OP-1, OP-2) |
| **Strategy Step** | Step 2 (Anti-Goals) and Step 4 (Stress-Test) |

**Evidence:**
- OP-1: "NEVER omit phases, agent assignments, barrier conditions, or artifact paths from the Orchestration Plan... include every phase, named agent, sync barrier, quality gate threshold, and output artifact path in the Orchestration Plan before delegating any work."
- OP-2: "NEVER substitute the Mermaid diagram with an ASCII diagram or produce a Mermaid diagram that omits nodes, edges, decision points, or labels."

Both constraints require COMPLETE specification before ANY work begins.

**Analysis:**
The Inversion: "What if the full scope cannot be known at plan-creation time?" In research-first workflows, Phase 1 research may reveal that Phase 3 design is unnecessary (technology doesn't support the approach) or that Phase 4 requires a skill not initially anticipated. OP-1 requires all paths to be in the Orchestration Plan before Phase 1 begins. This means the Orchestration Plan must specify Phase 4 in detail before Phase 1 has produced the findings that will shape Phase 4.

The result: either the Orchestration Plan is filled with placeholder-heavy detail ("Phase 4: TBD based on Phase 1 findings") that violates OP-1's "no omissions" rule, or the team specifies Phase 4 upfront and must rework the plan when research contradicts the spec. OP-2's full Mermaid requirement means this plan rework includes diagram updates -- significant overhead for a diagram that was necessarily speculative.

Agile workflows, emergent research findings, and iterative architecture approaches all require plans that evolve. OP-1 and OP-2 encode a waterfall assumption: all scope is known at plan creation.

**Plausibility:** High for research-driven and greenfield projects.

**Recommendation:**
Add an adaptive planning allowance: "OP-1 requires complete specification for all known phases. For phases that are contingent on prior-phase findings, include a placeholder with the triggering condition: 'Phase N will be specified after Phase N-1 output confirms [condition].' OP-2 Mermaid diagrams SHOULD include contingent nodes with dashed borders for unconfirmed phases."

**Acceptance Criteria:** OP-1 and OP-2 compliance does not require specifying phases whose content is unknown at plan creation.

---

### IN-011: SI-2 Real-Time Updates Conflict with DA-1 in Parallel Execution [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | State and Documentation Integrity (SI-2), Agent Delegation (DA-1) |
| **Strategy Step** | Step 4 (Stress-Test) |

**Evidence:**
- SI-2: "NEVER leave a worktracker entity in a state that does not accurately reflect the current status... update entity status and artifact paths immediately after each state change, before other work proceeds."
- DA-1: "NEVER execute... work directly in the main context... delegate all execution work to the appropriate skill agent... keeping the main context for orchestration state only."

**Analysis:**
When two parallel agents (e.g., eng-backend and eng-qa running simultaneously) both produce state changes, SI-2 requires immediate entity updates. These updates are main-context work. DA-1 says this is fine (orchestration state is main-context work). However, the "immediately after each state change" requirement, combined with parallel execution, means the main context must context-switch rapidly between processing agent outputs and updating worktracker state. In practice, the orchestrator often batches updates. SI-2's "immediately... before other work proceeds" prohibits this batching.

This is Minor rather than Critical because the contradiction is manageable in practice -- most LLMs will batch updates and the consequence (slightly stale worktracker state) is low severity for parallel phases. However, a strict interpretation creates compliance failures in every parallel workflow.

**Plausibility:** Medium. Parallel execution is common in multi-agent workflows.

**Recommendation:**
Clarify SI-2: "Update entity status immediately upon each agent's output being received by the main context. Parallel agent execution may produce simultaneous state changes; process updates in receipt order, not in strict execution order."

**Acceptance Criteria:** SI-2 compliance is achievable in parallel-agent workflows without requiring sequential agent execution.

---

## Execution Statistics

- **Total Findings:** 11
- **Critical:** 6 (IN-001 through IN-006)
- **Major:** 4 (IN-007 through IN-010)
- **Minor:** 1 (IN-011)
- **Protocol Steps Completed:** 6 of 6

---

## Step 4 Stress-Test Summary Table

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|------------|-----------|--------------|----------|--------------------|
| IN-001 | Constraints apply proportionally to task criticality | L2-REINJECT fires on ALL sessions; no scope guard exists | Very High | Critical | Completeness, Actionability |
| IN-002 | AQ-1/AQ-3/AQ-5 form a coherent system with finite termination | Three constraints create a triangular loop with no shared exit condition | High | Critical | Internal Consistency, Methodological Rigor |
| IN-003 | 0.95 threshold is achievable for all deliverable types | No baseline data shows 0.95 is routinely achievable; SSOT threshold is 0.92 | High | Critical | Evidence Quality, Methodological Rigor |
| IN-004 | Main-context work prohibition excludes orchestration housekeeping | DA-1 bans main-context work; SI-1 requires it for worktracker creation | High | Critical | Internal Consistency |
| IN-005 | "Implementation decision" means strategic decisions, not micro-decisions | EC-2 literally covers all decisions including naming, producing 80+ WebSearch calls per module | Very High | Critical | Actionability, Methodological Rigor |
| IN-006 | Separate agent per strategy is achievable within H-01 architecture | 9 strategies x N phases = potentially 54+ top-level Task invocations, exceeding session limits | High | Critical | Methodological Rigor, Completeness |
| IN-007 | /eng-team and /red-team are always available | Neither skill is universally installed; non-software workflows have no use for them | High | Major | Completeness, Actionability |
| IN-008 | Human review can always be made optional with sufficient automation | Governance-required human review is not optional; PC-2 creates a compliance trap | High | Major | Internal Consistency |
| IN-009 | EC-1 applies to external research claims, not internal workflow state | "NEVER state a fact" covers internal handoff statements, inflating handoffs 3-6x | High | Major | Evidence Quality, Actionability |
| IN-010 | Full scope is known at plan creation time | Research-first workflows discover scope during Phase 1; OP-1/OP-2 force waterfall specification | High | Major | Completeness, Methodological Rigor |
| IN-011 | Parallel agents produce sequential state changes | Parallel execution produces simultaneous state changes; SI-2 "immediately" creates batching violations | Medium | Minor | Internal Consistency |

---

## Recommendations (Prioritized)

### Critical -- MUST Address Before Broad Adoption

| ID | Mitigation Action | Acceptance Criteria |
|----|-------------------|---------------------|
| IN-001 | Add criticality scope guard at top of rule file and constraint block; remove unconditional L2-REINJECT or scope to C3+ sessions | C1 bug fix session does not trigger AQ-1, AQ-4, IT-4 |
| IN-002 | Add explicit cross-references between AQ-1, AQ-3, AQ-5 with shared termination semantics; resolve AQ-1 vs AQ-5 contradiction | Agent can unambiguously determine termination action for below-threshold output |
| IN-003 | Calibrate threshold to SSOT 0.92 as default; require measured baseline before recommending 0.95 | Threshold recommendation is backed by empirical baseline data |
| IN-004 | Carve out orchestration housekeeping from DA-1's main-context prohibition | DA-1 and SI-1 can both be satisfied without contradiction |
| IN-005 | Scope EC-2 to library selection and technology adoption decisions only | EC-2 does not trigger for internal implementation micro-decisions |
| IN-006 | Clarify AQ-4 "separate invocation" means adv-executor Task calls, not top-level orchestrator spawns; add practical bounds for C3 workflows | AQ-4 compliance achievable within H-01 architecture |

### Major -- SHOULD Address

| ID | Mitigation Action | Acceptance Criteria |
|----|-------------------|---------------------|
| IN-007 | Add conditional applicability and absent-skill escalation to IT-1 and IT-2 | IT-1/IT-2 do not block non-software or partial-skill-install workflows |
| IN-008 | Revise PC-2 to exclude governance-required human review from its prohibition | PC-2 does not block regulated-domain code delivery |
| IN-009 | Scope EC-1 to external-source claims; exclude internal handoff state | EC-1 does not inflate internal handoff size |
| IN-010 | Add adaptive planning allowance to OP-1/OP-2 for contingent phases | OP-1/OP-2 compliance does not require waterfall-complete upfront specification |

### Minor -- MAY Address

| ID | Mitigation Action | Acceptance Criteria |
|----|-------------------|---------------------|
| IN-011 | Clarify SI-2 to handle parallel-agent update ordering | SI-2 compliance achievable in parallel-agent workflows |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-001 (no scope guard), IN-006 (AQ-4 unachievable at scale), IN-010 (OP-1/OP-2 incomplete for adaptive workflows). Three findings indicate the constraint set is incomplete for its claimed scope. |
| Internal Consistency | 0.20 | Negative | IN-002 (AQ-1/AQ-3/AQ-5 loop), IN-004 (DA-1 vs SI-1 contradiction), IN-011 (SI-2 vs parallel execution). Three findings reveal internal contradictions that make the constraint system internally incoherent in specific execution paths. |
| Methodological Rigor | 0.20 | Negative | IN-003 (threshold not grounded in evidence), IN-005 (EC-2 granularity miscalibrated), IN-006 (AQ-4 architecture incompatibility). Three findings indicate the methodology is calibrated for an idealized C4 context that does not reflect actual deployment conditions. |
| Evidence Quality | 0.15 | Negative | IN-003 (0.95 threshold recommendation lacks empirical grounding beyond the 92.2% compliance claim, which measures behavioral compliance not deliverable quality scores), IN-009 (EC-1 scope creates overhead that paradoxically undermines evidence quality by inflating non-evidential content). |
| Actionability | 0.15 | Negative | IN-001 (non-C4 teams blocked), IN-005 (EC-2 over-broad), IN-007 (IT-1/IT-2 block absent-skill workflows). Three actionability failures: constraints produce blocking conditions with no actionable resolution path. |
| Traceability | 0.10 | Positive | All 22 constraints have IDs, the constraint file has a navigation table, and the mega-prompt template includes a full constraint inventory. Traceability within the deliverables themselves is strong. The IN-NNN findings here trace to specific constraint IDs in the deliverable. |

**Overall Assessment:** The constraint set has strong traceability and a solid structural foundation, but carries six Critical assumption vulnerabilities that would likely produce worse outcomes than no constraints in non-C4 contexts, and would produce infinite escalation loops or permanent pipeline stalls in C4 contexts without the specified mitigations. **REVISE before adoption as unconditional `.claude/rules/` content.**

---

## What Is the WORST Realistic Outcome?

Per the S-013 Inversion task specification, the worst realistic outcome of adopting these constraints without modification:

**Scenario:** A development team installs `orchestration-behavioral-constraints.md` into `.claude/rules/` as documented. They use Jerry daily for a mix of C1 bug fixes (60%), C2 feature work (30%), and C4 architectural decisions (10%).

**Outcome:**
1. The L2-REINJECT fires on every session (100% of workflows).
2. For C1 bug fixes (60% of work), AQ-1 mandates /adversary at C4 before handoff. The team cannot hand off a 3-line bug fix without 9 adversarial strategy invocations. They spend 2+ hours on adversarial review for a 5-minute fix.
3. AQ-1 + AQ-3 + AQ-5 interact on the first failing gate. The LLM enters a revision loop. AQ-2 provides a ceiling (10 iterations) but the agent does not correlate AQ-2 with AQ-1/AQ-3. The loop runs until context compaction, the very failure mode DA-1 was designed to prevent.
4. EC-2 fires for every implementation decision. WebSearch calls saturate the context window. The context compacts mid-workflow, losing all in-context state. SI-1 state was not fully persisted because the compaction was unexpected.
5. After one week, the team removes the rule file entirely -- not because adversarial review is bad, but because the constraint set as written made Jerry unusable for their actual work mix.

**Net result:** Adoption of these constraints produces worse outcomes than no constraints for a team with a realistic C1/C2/C4 work mix, because the overhead and contradiction severity in the C1/C2 cases (60-90% of usage) dominates the genuine quality improvement in C4 cases (10%).

The constraints are well-designed for a dedicated C4 project session (e.g., a specific PROJ-014 research effort where ALL work is C4). They are counterproductive as a permanent `.claude/rules/` file applied unconditionally.
