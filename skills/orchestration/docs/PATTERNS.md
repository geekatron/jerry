# Orchestration Patterns

> **Version:** 1.0.0
> **Skill:** orchestration
> **References:** [Microsoft AI Agent Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), [LangGraph](https://langchain-ai.github.io/langgraph/), [CrewAI Flows](https://docs.crewai.com/concepts/flows)

---

## Overview

This document describes orchestration patterns supported by the Jerry orchestration skill, based on industry best practices from Microsoft, LangGraph, CrewAI, and NASA SE.

---

## Pattern 1: Cross-Pollinated Pipeline

**Description:** Two or more pipelines running in parallel with synchronization barriers for bidirectional information exchange.

**Use When:**
- Multiple perspectives needed on same problem
- Pipelines have complementary expertise
- Cross-domain validation required

**Example:** ps-* (Problem-Solving) ↔ nse-* (NASA SE) pipelines

```
PIPELINE A                              PIPELINE B
    │                                       │
    ▼                                       ▼
┌─────────┐                           ┌─────────┐
│ Phase 1 │                           │ Phase 1 │
└────┬────┘                           └────┬────┘
     │                                     │
     └──────────────┬──────────────────────┘
                    ▼
            ╔═══════════════╗
            ║   BARRIER 1   ║  ← Bidirectional exchange
            ║  a→b artifact ║
            ║  b→a artifact ║
            ╚═══════════════╝
                    │
     ┌──────────────┴──────────────────────┐
     │                                     │
     ▼                                     ▼
┌─────────┐                           ┌─────────┐
│ Phase 2 │                           │ Phase 2 │
└─────────┘                           └─────────┘
```

**Barrier Artifacts:**
- Extract key findings from completed phase
- Transform into cross-pollination document
- Target pipeline consumes before next phase

---

## Pattern 2: Sequential with Checkpoints

**Description:** Single pipeline with checkpoint creation after each phase for recovery.

**Use When:**
- Linear workflow with clear dependencies
- Long-running process needs recovery points
- Debugging capability required

**Example:** Research → Analysis → Design → Implementation

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Phase 1 │────►│ Phase 2 │────►│ Phase 3 │────►│ Phase 4 │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
   CP-001          CP-002          CP-003          CP-004
   (recovery)      (recovery)      (recovery)      (recovery)
```

**Checkpoint Contents:**
- State snapshot at completion
- List of artifacts created
- Recovery instructions

---

## Pattern 3: Fan-Out / Fan-In

**Description:** Parallel execution of independent agents with synthesis at the end.

**Use When:**
- Multiple independent research streams
- Diverse perspectives on same topic
- Time-critical parallel work

**Example:** Parallel research on caching, queuing, storage

```
                  ┌─────────┐
                  │  Start  │
                  └────┬────┘
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     ┌────────┐   ┌────────┐   ┌────────┐
     │Agent A │   │Agent B │   │Agent C │
     │(cache) │   │(queue) │   │(store) │
     └────┬───┘   └────┬───┘   └────┬───┘
          └────────────┼────────────┘
                       ▼
                ┌────────────┐
                │ Synthesize │
                └────────────┘
```

**Execution:**
- All fan-out agents run in parallel (same group)
- Synthesis agent waits for all to complete
- Synthesis consumes all artifacts

---

## Pattern 4: Hierarchical Delegation

**Description:** Manager agent coordinates specialist agents.

**Use When:**
- Complex task requiring specialist knowledge
- Dynamic routing based on task type
- Quality control needed

**Example:** Triage → Specialist routing

```
┌─────────────────┐
│  Manager Agent  │
└────────┬────────┘
         │ Delegates based on task type
    ┌────┼────┬────────┐
    ▼    ▼    ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│Spec A│ │Spec B│ │Spec C│
└──────┘ └──────┘ └──────┘
```

**Note:** In Jerry, the MAIN CONTEXT acts as manager, not a spawned agent (P-003 compliant).

---

## Pattern 5: Iterative Refinement (Generator-Critic)

**Description:** Generator creates output, critic evaluates, loop until quality threshold.

**Use When:**
- Output quality is critical
- Iterative improvement possible
- Clear evaluation criteria exist

**Example:** Draft → Review → Revise → Review → Accept

```
┌────────────┐     ┌────────────┐
│ Generator  │────►│   Critic   │
└────────────┘     └─────┬──────┘
      ▲                  │
      │                  │ Feedback
      │                  ▼
      │            ┌──────────┐
      └────────────┤ Threshold│
                   │  Met?    │
                   └──────────┘
                        │
                        ▼ Yes
                   ┌──────────┐
                   │  Accept  │
                   └──────────┘
```

**Circuit Breaker:**
- max_iterations: 3
- improvement_threshold: 10%
- Stop if no improvement after 2 consecutive iterations

---

## Pattern Selection Guide

| Scenario | Recommended Pattern |
|----------|---------------------|
| Two domain perspectives needed | Cross-Pollinated Pipeline |
| Long-running single track | Sequential with Checkpoints |
| Independent parallel research | Fan-Out / Fan-In |
| Complex task routing | Hierarchical Delegation |
| Quality-critical output | Iterative Refinement |

---

## Constitutional Constraints

All patterns must comply with:

| Constraint | ID | Implication |
|------------|----|----|
| Single nesting | P-003 | Main context is orchestrator, agents are workers |
| File persistence | P-002 | All state to ORCHESTRATION.yaml |
| User authority | P-020 | User can override any decision |
| No deception | P-022 | Honest status reporting |

---

## Industry References

1. Microsoft. (2025). *AI Agent Orchestration Patterns*. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
2. LangChain. (2025). *LangGraph State Management*. https://langchain-ai.github.io/langgraph/
3. CrewAI. (2025). *Flows and Routing*. https://docs.crewai.com/concepts/flows
4. NASA. (2024). *NPR 7123.1D SE Engine*. https://nodis3.gsfc.nasa.gov/

---

*Document Version: 1.0.0*
*Skill: orchestration*
