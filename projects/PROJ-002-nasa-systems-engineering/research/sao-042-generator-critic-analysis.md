---
id: sao-042-analysis
title: "Generator-Critic Pattern Analysis"
type: analysis
parent: "../work/initiatives/sao-init-007-triple-lens-playbooks/wi-sao-042.md"
initiative: sao-init-007
created: "2026-01-12"
last_updated: "2026-01-12"
status: COMPLETE
analyst: "ps-analyst (via main context)"
token_estimate: 1200
---

# WI-SAO-042 Analysis: Generator-Critic Pattern Decision Guide

> **Status:** COMPLETE
> **Work Item:** WI-SAO-042
> **Date:** 2026-01-12
> **Input:** `research/sao-042-generator-critic-research.md`

---

## Executive Summary (L0)

This analysis provides decision guidance for when to use ps-critic (Generator-Critic pattern) versus ps-validator or ps-reviewer. The key insight is that these three agents serve distinct purposes despite superficial similarity: ps-critic improves quality iteratively, ps-validator verifies constraints, and ps-reviewer finds defects.

---

## Decision Matrix: Critic vs Validator vs Reviewer

### Quick Reference

| Dimension | ps-critic | ps-validator | ps-reviewer |
|-----------|-----------|--------------|-------------|
| **Purpose** | Improve quality | Verify constraints | Find defects |
| **Output** | Score + recommendations | Pass/Fail | Findings + severity |
| **Iteration** | Yes (loop) | No (one-shot) | No (one-shot) |
| **When to use** | Quality matters | Compliance matters | Safety matters |
| **Pairs with** | Generator agents | Any output | Code/design |

### Detailed Comparison

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT SELECTION DECISION TREE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  What is your primary goal?                                             │
│       │                                                                 │
│       ├─► "Is it CORRECT?" ──────────────► ps-validator (Pass/Fail)    │
│       │   (constraints, schema, rules)                                  │
│       │                                                                 │
│       ├─► "Does it have DEFECTS?" ───────► ps-reviewer (Severity)      │
│       │   (bugs, security, performance)                                 │
│       │                                                                 │
│       └─► "Is it GOOD ENOUGH?" ──────────► ps-critic (Score 0.0-1.0)   │
│           (quality, completeness, clarity)                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Scenario Guide

| Scenario | Best Agent | Rationale |
|----------|------------|-----------|
| ADR needs polish | **ps-critic** | Quality improves with iteration |
| API schema validation | ps-validator | Binary compliance check |
| PR code review | ps-reviewer | Find bugs and issues |
| Research synthesis | **ps-critic** | Completeness matters |
| Configuration file check | ps-validator | Syntax must be correct |
| Security audit | ps-reviewer | Find vulnerabilities |
| Documentation draft | **ps-critic** | Clarity improves with feedback |
| Contract verification | ps-validator | Legal compliance binary |
| Design review | **ps-reviewer** + **ps-critic** | Find issues + improve quality |

---

## Optimal Workflow Compositions

### For Each PS-* Agent: When to Pair with ps-critic

| Generator Agent | Critic Pairing | Example Workflow |
|-----------------|----------------|------------------|
| **ps-researcher** | YES - Recommended | Research → Critique → Refine → Accept |
| **ps-analyst** | YES - Optional | Analysis → Critique (if deep dive needed) |
| **ps-architect** | YES - Strongly Recommended | Design → Critique → Iterate → Accept |
| **ps-investigator** | NO - Typically | Root cause analysis is one-shot |
| **ps-reporter** | NO - Typically | Status reports don't iterate |
| **ps-synthesizer** | YES - Optional | Synthesis → Critique (for key summaries) |
| **ps-validator** | NO - Never | Validator output is binary |
| **ps-reviewer** | NO - Never | Review findings don't iterate |
| **ps-critic** | NO - Never | Cannot self-critique (P-003) |

### Workflow Patterns

#### Pattern A: Simple Generator-Critic

```
MAIN CONTEXT
    │
    ├──► Generator (ps-architect)
    │         │
    │         ▼ output
    │    ┌─────────┐
    │    │ design  │
    │    │ draft   │
    │    └─────────┘
    │         │
    ├──► ps-critic ◄──┘
    │         │
    │         ▼ score=0.72, feedback
    │
    │    [score < 0.85, iteration < 3]
    │
    ├──► Generator + feedback
    │         │
    │         ▼ output v2
    │
    ├──► ps-critic
    │         │
    │         ▼ score=0.89
    │
    │    [score >= 0.85] → ACCEPT
    │
    └──► Done
```

#### Pattern B: Research-Critic-Synthesis

```
MAIN CONTEXT
    │
    ├──► ps-researcher ──► research_output
    │
    ├──► ps-critic (evaluate research)
    │         │
    │         ▼ score=0.65, "missing X, Y"
    │
    ├──► ps-researcher + feedback ──► research_v2
    │
    ├──► ps-critic
    │         │
    │         ▼ score=0.88 → ACCEPT
    │
    └──► ps-synthesizer ──► final synthesis
```

#### Pattern C: Design-Review-Critique Hybrid

```
MAIN CONTEXT
    │
    ├──► ps-architect ──► design draft
    │
    ├──► ps-reviewer ──► review findings (3 HIGH, 5 MEDIUM)
    │
    │    [Has HIGH severity findings]
    │
    ├──► ps-architect + findings ──► design v2
    │
    ├──► ps-reviewer ──► review findings (0 HIGH, 2 MEDIUM)
    │
    │    [No HIGH severity]
    │
    ├──► ps-critic ──► quality polish
    │         │
    │         ▼ score=0.82
    │
    ├──► ps-architect + polish feedback ──► design v3
    │
    ├──► ps-critic ──► score=0.91 → ACCEPT
    │
    └──► Done (design ready for implementation)
```

---

## Circuit Breaker Decision Logic

### Parameters (from ps-critic.md)

```yaml
max_iterations: 3
improvement_threshold: 0.10  # 10%
acceptance_threshold: 0.85
consecutive_no_improvement_limit: 2
```

### Decision Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│                   CIRCUIT BREAKER LOGIC                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  score = ps-critic.quality_score                            │
│  iteration = current iteration number                       │
│  improvement = score - previous_score                       │
│                                                             │
│  IF score >= 0.85:                                          │
│      ──► ACCEPT (threshold met)                             │
│                                                             │
│  ELIF iteration >= 3:                                       │
│      ──► ACCEPT_WITH_CAVEATS or ESCALATE                   │
│          (max iterations reached)                           │
│                                                             │
│  ELIF improvement < 0.10 AND no_improvement_count >= 2:     │
│      ──► ACCEPT_WITH_CAVEATS                               │
│          (no further improvement likely)                    │
│                                                             │
│  ELSE:                                                      │
│      ──► REVISE (send feedback to generator)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns to Document

### 1. Critic-Everything Anti-Pattern

**Description:** Using ps-critic for every agent output regardless of need.

**Problem:** Unnecessary latency and cost.

**Solution:** Only use critic when quality improvement justifies iteration time.

### 2. Infinite Loop Anti-Pattern

**Description:** Not implementing circuit breaker, leading to endless iterations.

**Problem:** Never converges; wastes resources.

**Solution:** Always enforce max_iterations and improvement_threshold.

### 3. Self-Orchestration Anti-Pattern

**Description:** Letting ps-critic invoke the next iteration or manage the loop.

**Problem:** Violates P-003 (No Recursive Subagents).

**Solution:** MAIN CONTEXT always orchestrates; ps-critic only evaluates.

### 4. Wrong-Agent Anti-Pattern

**Description:** Using ps-critic when ps-validator or ps-reviewer is appropriate.

**Problem:** Score-based feedback when pass/fail or severity needed.

**Solution:** Use decision matrix above to select correct agent.

### 5. Missing-Criteria Anti-Pattern

**Description:** Invoking ps-critic without defining evaluation criteria.

**Problem:** Vague, inconsistent feedback.

**Solution:** Always provide criteria (custom or accept defaults).

---

## Recommendations for Playbook Documentation

### Structure for Generator-Critic Section

```markdown
## L0: Generator-Critic Pattern (ELI5)

**Metaphor:** Like a writing workshop where you draft, get feedback,
revise, and repeat until your work meets quality standards.

**When to use:** When output quality matters and iteration time is acceptable.

## L1: Generator-Critic Implementation (Engineer)

### Invocation Pattern
{Task tool syntax with generator + critic}

### Circuit Breaker Parameters
{max_iterations, threshold, exit conditions}

### State Management
{output_key flow between agents}

## L2: Generator-Critic Constraints (Architect)

### P-003 Compliance
{MAIN CONTEXT orchestrates, agents don't self-loop}

### Anti-Patterns
{5 anti-patterns with examples}

### Decision Matrix
{When to use critic vs validator vs reviewer}
```

### Required Examples (for WI-SAO-043)

Each ps-* agent needs examples showing:

| Agent | Example 1 | Example 2 | Example 3 | Example 4 | Example 5 |
|-------|-----------|-----------|-----------|-----------|-----------|
| ps-researcher | SE: Tech spike | PM: Competitor analysis | UX: User research | SE: Library eval | PM: Market sizing |
| ps-analyst | SE: Root cause | PM: Feature trade-offs | UX: Friction analysis | SE: Perf bottleneck | PM: Risk assessment |
| ps-architect | SE: ADR creation | PM: System design | UX: IA design | SE: API design | PM: Integration arch |
| ps-validator | SE: Schema check | PM: Req validation | UX: A11y compliance | SE: Config verify | PM: SLA check |
| ps-critic | SE: Code quality | PM: Doc polish | UX: Design critique | SE: ADR refinement | PM: Proposal quality |
| ps-investigator | SE: Bug RCA | PM: Failure post-mortem | UX: Drop-off analysis | SE: Outage analysis | PM: Churn investigation |
| ps-reporter | SE: Sprint status | PM: OKR progress | UX: Research summary | SE: Release notes | PM: Stakeholder update |
| ps-reviewer | SE: PR review | PM: Spec review | UX: Design review | SE: Security review | PM: Contract review |
| ps-synthesizer | SE: Retro synthesis | PM: Research synthesis | UX: Insight synthesis | SE: Doc synthesis | PM: Decision synthesis |

---

## Analysis Conclusion

1. **ps-critic is for iterative quality improvement** - not validation or defect detection
2. **Always use circuit breakers** - max 3 iterations, 0.85 threshold
3. **MAIN CONTEXT orchestrates** - P-003 compliance is non-negotiable
4. **Generator pairing** - ps-architect, ps-researcher, ps-analyst benefit most
5. **Document anti-patterns** - prevent common misuse

---

*Analysis artifact for WI-SAO-042*
*Created: 2026-01-12*
