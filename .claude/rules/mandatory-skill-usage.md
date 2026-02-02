# Mandatory Skill Usage (PROACTIVE)

> **CRITICAL:** You MUST use the following skills PROACTIVELY without waiting for the user to prompt you.
> These skills are designed to ensure quality, rigor, and traceability in all work.

---

## /problem-solving (MANDATORY for Research/Analysis)

**USE AUTOMATICALLY WHEN:**
- Starting ANY research or analysis task
- Investigating bugs, issues, or problems
- Performing root cause analysis
- Synthesizing findings from multiple sources
- Creating architecture decisions (ADRs)

**Provides:**
- 8 specialized agents: researcher, analyst, synthesizer, architect, reviewer, investigator, validator, reporter
- Structured frameworks: 5W2H, Ishikawa, Pareto, FMEA, 8D
- Evidence-based decision making with citations
- Persistent artifact generation

**Trigger Phrases (use skill automatically):**
- "research", "analyze", "investigate", "explore"
- "root cause", "why", "understand"
- "synthesize", "consolidate", "summarize findings"
- "review", "validate", "critique"

---

## /nasa-se (MANDATORY for Requirements/Design)

**USE AUTOMATICALLY WHEN:**
- Defining or analyzing requirements
- Creating design specifications
- Performing verification & validation
- Conducting technical reviews
- Managing system integration
- Risk management activities

**Provides:**
- NPR 7123.1D process implementation
- 10 specialized agents for systems engineering
- Requirements engineering rigor
- Verification/validation frameworks
- Technical review protocols
- Mission-grade quality practices

**Trigger Phrases (use skill automatically):**
- "requirements", "specification", "shall statements"
- "verification", "validation", "V&V"
- "technical review", "design review"
- "risk management", "FMEA"
- "system integration", "interface"

---

## /orchestration (MANDATORY for Multi-Step Workflows)

**USE AUTOMATICALLY WHEN:**
- Work involves multiple phases or stages
- Multiple agents need coordination
- Tasks have dependencies requiring sync barriers
- State must be checkpointed for recovery
- Cross-pollinated pipelines are needed

**Provides:**
- ORCHESTRATION_PLAN.md - Strategic workflow context
- ORCHESTRATION_WORKTRACKER.md - Tactical execution tracking
- ORCHESTRATION.yaml - Machine-readable state (SSOT)
- Sync barriers for parallel work coordination
- State checkpointing for resilience

**Trigger Phrases (use skill automatically):**
- "orchestration", "pipeline", "workflow"
- "multi-agent", "parallel", "coordinate"
- "sync barrier", "checkpoint"
- "phases", "stages", "gates"

See `skills/orchestration/PLAYBOOK.md` for step-by-step workflow guidance.

---

## Skill Usage Behavior Rules

1. **DO NOT WAIT** for user to invoke skills - use them proactively when triggers apply
2. **COMBINE SKILLS** when appropriate (e.g., /orchestration + /problem-solving + /nasa-se for complex analysis)
3. **INVOKE EARLY** - Use skills at the start of work, not after struggling without them
4. **PERSIST ARTIFACTS** - All skill outputs must be persisted to the repository
5. **REFERENCE IN TODO** - Track skill invocations and outputs in your TODO list

---

## Example: Starting a New Feature

```
User: "Let's work on EN-004 Architecture Decisions"

Claude's Internal Process:
1. ✅ Invoke /orchestration - This has multiple ADRs requiring coordination
2. ✅ Invoke /problem-solving - Research and analysis needed for each ADR
3. ✅ Invoke /nasa-se - Architecture decisions require SE rigor
4. ✅ Create/update TODO with skill tracking
5. ✅ Proceed with coordinated execution
```

---

## Quick Reference: Trigger → Skill Mapping

| Detected Keywords | Skill to Invoke |
|-------------------|-----------------|
| research, analyze, investigate, explore, root cause, why | `/problem-solving` |
| requirements, specification, V&V, technical review, risk | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases | `/orchestration` |

---

## Agents Available

See `AGENTS.md` for the full registry. Agents are scoped to skills:

| Skill | Agents | Location |
|-------|--------|----------|
| problem-solving | 8 specialists (researcher, analyst, synthesizer, etc.) | `skills/problem-solving/agents/` |
| nasa-se | 10 SE specialists (requirements, verification, risk, etc.) | `skills/nasa-se/agents/` |
| orchestration | 3 workflow specialists (planner, tracker, synthesizer) | `skills/orchestration/agents/` |

Invoke agents via the respective skill.
