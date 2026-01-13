---
id: sao-042-research
title: "Generator-Critic Patterns Research"
type: research
parent: "../work/initiatives/sao-init-007-triple-lens-playbooks/wi-sao-042.md"
initiative: sao-init-007
created: "2026-01-12"
last_updated: "2026-01-12"
status: COMPLETE
researcher: "ps-researcher (via main context)"
token_estimate: 1500
---

# WI-SAO-042 Research: Generator-Critic Patterns

> **Status:** COMPLETE
> **Work Item:** WI-SAO-042
> **Date:** 2026-01-12

---

## Executive Summary (L0)

The Generator-Critic pattern is an iterative refinement technique where one agent produces output and another evaluates it against criteria, creating a feedback loop until quality thresholds are met. In Jerry, this is implemented via ps-critic paired with generator agents (ps-architect, ps-researcher, ps-analyst), orchestrated by the MAIN CONTEXT (Claude session) per P-003 compliance.

Key insight: Jerry's implementation aligns with industry best practices from Google ADK, AWS, and academic research (Self-Refine).

---

## Research Sources

### Primary Sources (HIGH Authority)

| Source | Authority | URL |
|--------|-----------|-----|
| Google ADK Multi-Agent Patterns | HIGH | [developers.googleblog.com](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) |
| AWS Evaluator Reflect-Refine Loops | HIGH | [docs.aws.amazon.com](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/evaluator-reflect-refine-loop-patterns.html) |
| Self-Refine Paper (Madaan et al.) | HIGH | [arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651) |
| MongoDB Agentic Design Patterns | MEDIUM | [medium.com/mongodb](https://medium.com/mongodb/here-are-7-design-patterns-for-agentic-systems-you-need-to-know-d74a4b5835a5) |

### Internal Sources

| Source | Location |
|--------|----------|
| ps-critic agent definition | `skills/problem-solving/agents/ps-critic.md` |
| ORCHESTRATION_PATTERNS.md | `skills/shared/ORCHESTRATION_PATTERNS.md` |
| Jerry Constitution P-003 | `docs/governance/JERRY_CONSTITUTION.md` |

---

## PS-* Agent Inventory

### All 9 Problem-Solving Agents

| Agent | Role | Cognitive Mode | Typical Use |
|-------|------|----------------|-------------|
| **ps-researcher** | Deep research | DIVERGENT | Information gathering, literature review |
| **ps-analyst** | Analysis | CONVERGENT | Root cause, trade-offs, gaps, risks |
| **ps-architect** | Decisions | CONVERGENT | ADRs, design decisions |
| **ps-validator** | Verification | CONVERGENT | Constraint checking (pass/fail) |
| **ps-critic** | Quality eval | CONVERGENT | Iterative refinement (score-based) |
| **ps-investigator** | Debugging | CONVERGENT | Failure analysis (5 Whys, FMEA) |
| **ps-reporter** | Reporting | CONVERGENT | Status and progress reports |
| **ps-reviewer** | Code review | CONVERGENT | Defect detection (severity-based) |
| **ps-synthesizer** | Meta-analysis | CONVERGENT | Pattern synthesis across outputs |

### Agent Distinctions (Critical for Documentation)

| Agent | Focus | Output Type | Loop Participation |
|-------|-------|-------------|-------------------|
| ps-critic | Quality improvement | Score + recommendations | CRITIC in feedback loop |
| ps-validator | Constraint verification | Pass/Fail | One-shot verification |
| ps-reviewer | Defect detection | Severity ratings | One-shot review |

---

## Industry Patterns Comparison

### Google ADK: 8 Multi-Agent Patterns

| Pattern | Jerry Equivalent | Notes |
|---------|------------------|-------|
| Sequential Pipeline | Pattern 2: Sequential Chain | output_key for state transfer |
| Coordinator/Dispatcher | MAIN CONTEXT orchestration | LLM-driven routing |
| Parallel Fan-Out/Gather | Pattern 3/4: Fan-Out/Fan-In | Unique keys prevent race conditions |
| Hierarchical Decomposition | Not implemented | AgentTool wrapping |
| **Generator-Critic** | **Pattern 8: Generator-Critic Loop** | Pass/Fail correctness |
| Iterative Refinement | Extension of Pattern 8 | Score-based polish |
| Human-in-the-Loop | User escalation | Via circuit breaker |
| Composite | Multi-pattern workflows | Real-world systems |

### AWS: Evaluator Reflect-Refine Loop

| Component | Jerry Implementation |
|-----------|---------------------|
| Generator agent | ps-architect, ps-researcher, ps-analyst |
| Evaluator agent | ps-critic |
| Refiner | Generator with feedback |
| Circuit breaker | max_iterations=3, threshold=0.85 |
| Orchestration | MAIN CONTEXT (Step Functions equivalent) |

---

## Generator-Critic Pattern in Jerry

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN CONTEXT (Orchestrator)              │
│                         P-003 Compliant                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐     Iteration 1     ┌─────────────┐      │
│   │  Generator  │ ──────────────────► │  ps-critic  │      │
│   │ (ps-architect)│                    │             │      │
│   └─────────────┘                      └─────────────┘      │
│         ▲                                    │              │
│         │         score < 0.85               │              │
│         │         feedback                   │              │
│         └────────────────────────────────────┘              │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              Circuit Breaker Logic                   │  │
│   │  IF score >= 0.85: ACCEPT                           │  │
│   │  ELIF iteration >= 3: ACCEPT_WITH_CAVEATS           │  │
│   │  ELIF no_improvement × 2: ACCEPT_WITH_CAVEATS       │  │
│   │  ELSE: REVISE (send feedback to generator)          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### ps-critic Configuration

From `skills/problem-solving/agents/ps-critic.md`:

```yaml
orchestration_guidance:
  pattern: "iterative_refinement"
  circuit_breaker:
    max_iterations: 3
    improvement_threshold: 0.10
    stop_conditions:
      - "quality_score >= 0.85"
      - "iteration >= max_iterations"
      - "no_improvement_for_2_consecutive_iterations"
  pairing_agents:
    - "ps-architect"
    - "ps-researcher"
    - "ps-analyst"
```

### Quality Evaluation Criteria

Default dimensions (if not custom):

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.25 | Addresses all requirements? |
| Accuracy | 0.25 | Information correct and verifiable? |
| Clarity | 0.20 | Clear and understandable? |
| Actionability | 0.15 | Can be acted upon? |
| Alignment | 0.15 | Aligns with goals/constraints? |

### Quality Score Thresholds

| Score Range | Assessment | Action |
|-------------|------------|--------|
| 0.85 - 1.00 | EXCELLENT | ACCEPT |
| 0.70 - 0.84 | GOOD | Accept or minor revision |
| 0.50 - 0.69 | ACCEPTABLE | Revision recommended |
| 0.30 - 0.49 | NEEDS_WORK | Revision required |
| 0.00 - 0.29 | POOR | Major revision required |

---

## When to Use Generator-Critic Pattern

### Good Use Cases

| Scenario | Why Generator-Critic |
|----------|---------------------|
| ADR creation | Design quality improves with feedback |
| Research synthesis | Completeness and accuracy matter |
| Documentation | Clarity benefits from iteration |
| Complex analysis | Multiple perspectives improve output |

### Bad Use Cases

| Scenario | Why NOT Generator-Critic |
|----------|-------------------------|
| Simple queries | Overhead not justified |
| Time-critical tasks | Latency from iterations |
| Binary validation | Use ps-validator instead |
| Defect detection | Use ps-reviewer instead |

---

## P-003 Compliance: Critical Architecture

**P-003 (Hard Principle):** Agents cannot spawn other agents. Maximum ONE level of nesting.

**Implication for Generator-Critic:**
- ps-critic does NOT manage the iteration loop
- ps-critic does NOT invoke the generator
- MAIN CONTEXT (Claude session) orchestrates the loop
- ps-critic only evaluates and returns recommendations

**From ps-critic.md:**
> "You DO NOT manage the loop yourself - that would violate P-003 (agents cannot orchestrate other agents)."

---

## Best Practices from Industry Research

### 1. Define Clear Evaluation Criteria
> "Since LLMs are used as evaluators, the evaluation criteria should be clearly defined so that the LLM can effectively reason through them." — Industry consensus

**Jerry Implementation:** ps-critic has default criteria + custom criteria support

### 2. Set Iteration Limits (Circuit Breakers)
> "The loop should continue until either the evaluator determines the output is satisfactory or a maximum number of iterations is reached." — AWS

**Jerry Implementation:** max_iterations=3, improvement_threshold=0.10

### 3. Start Simple
> "Do not build a nested loop system on day one. Start with a sequential chain, debug it, and then add complexity." — Google ADK

**Jerry Recommendation:** Use sequential chain first, add critic when quality matters

### 4. Build in Guardrails
> "Set iteration limits, plan for human bottlenecks, and define success metrics before adding complexity." — Industry consensus

**Jerry Implementation:** Circuit breaker logic, escalation path to user

### 5. Use Specialized Agents
> "A single agent tasked with too many responsibilities becomes a Jack of all trades, master of none." — MongoDB

**Jerry Implementation:** 9 specialized ps-* agents with distinct roles

---

## Known Challenges

### 1. Degeneration-of-Thought
> "Reflexion-style patterns are vulnerable to 'degeneration-of-thought,' where the agent repeats the same flawed reasoning across iterations."

**Mitigation:** consecutive_no_improvement_limit=2 in circuit breaker

### 2. Safety and Governance
> "Self-refining agents that generate and act on their own critiques introduce safety challenges."

**Mitigation:** P-003 prevents self-orchestration; human escalation path

### 3. Latency
Multiple iterations add latency. Use generator-critic only when quality justifies time cost.

---

## Recommendations for Documentation

### For Problem-Solving PLAYBOOK.md

1. **Add Generator-Critic Section** with:
   - L0: What it is and why use it (metaphor)
   - L1: How to invoke (Task tool syntax)
   - L2: Anti-patterns and constraints

2. **Add Agent Comparison Table** showing:
   - ps-critic vs ps-validator vs ps-reviewer distinctions

3. **Add Workflow Examples**:
   - ADR refinement workflow
   - Research quality improvement workflow
   - Design document polish workflow

4. **Document Circuit Breaker** parameters prominently

### For L0/L1/L2 Examples (WI-SAO-043)

Each ps-* agent needs 5+ concrete examples showing:
- Real-world scenario (SE, PM, UX domains)
- L0 perspective (what/why)
- L1 perspective (how)
- L2 perspective (constraints)

---

## References

- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [AWS Evaluator Reflect-Refine Loops](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/evaluator-reflect-refine-loop-patterns.html)
- [Self-Refine: Iterative Refinement (Madaan et al., 2023)](https://arxiv.org/abs/2303.17651)
- [MongoDB Agentic Design Patterns](https://medium.com/mongodb/here-are-7-design-patterns-for-agentic-systems-you-need-to-know-d74a4b5835a5)

---

*Research artifact for WI-SAO-042*
*Created: 2026-01-12*
