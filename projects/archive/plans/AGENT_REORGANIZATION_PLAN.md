# Agent Reorganization Plan - ps-*.md Agents and Enforcement

> **Status:** DRAFT - AWAITING APPROVAL
> **Created:** 2026-01-08
> **Author:** Claude (Distinguished Systems Engineer persona)
> **Related Research:** `docs/research/AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md`

---

## Executive Summary

This plan reorganizes Jerry's `ps-*.md` agents to implement a **4-tier progressive enforcement model** focusing on **Advisory, Soft, and Medium enforcement** (deferring Hard enforcement). Based on comprehensive research from Anthropic, OpenAI, Google DeepMind, and academic sources.

### Key Design Decisions

| Decision | Choice | Evidence |
|----------|--------|----------|
| **Enforcement Model** | 4-Tier Progressive (Advisory → Soft → Medium → Hard) | Industry consensus; AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md |
| **Primary Emphasis** | Advisory + Soft (75%) | Constitutional AI research; OpenAI Model Spec |
| **Agent Location** | `.claude/agents/` + `skills/*/agents/` | Claude Code conventions |
| **Self-Monitoring** | Enable skill-level metrics | DeepMind amplified oversight patterns |
| **Constitutional Principles** | Create Jerry Constitution | Anthropic Constitutional AI |

---

## 1. Problem Statement (5W1H Analysis)

### WHO is affected?
- Jerry framework users deploying ps-*.md agents
- Agent orchestration workflows
- Future skill developers

### WHAT problem are we solving?
- Current agents have Hard enforcement references that aren't fully implemented
- Need working agents with Advisory + Soft + Medium enforcement
- Architecture skill needs cleanup
- ps-*.md agents reference non-existent infrastructure

### WHERE does the problem manifest?
- `skills/problem-solving/agents/ps-*.md` - 8 agent definitions
- `skills/architecture/SKILL.md` - Hard enforcement references
- `.claude/agents/` - orchestration layer

### WHEN does it occur?
- When attempting to invoke ps-* agents via Task tool
- When agents reference c-009 persistence enforcement that isn't implemented
- When trying to use Context7 MCP tools that may not be configured

### WHY does it matter?
- Non-functional agents reduce trust and productivity
- Missing enforcement creates inconsistent behavior
- Hard enforcement adds complexity without established soft foundations

### HOW will we solve it?
1. Implement Jerry Constitution for Advisory principles
2. Add self-monitoring and reflection to agents
3. Simplify agents to work without Hard enforcement
4. Create Medium enforcement via tool restrictions
5. Defer Hard enforcement until Advisory/Soft/Medium are proven

---

## 2. Current State Analysis

### 2.1 Existing ps-*.md Agents (8 total)

| Agent | Purpose | Current Issues |
|-------|---------|----------------|
| `ps-researcher` | Deep research with Context7 | References c-009 hard enforcement, link-artifact CLI |
| `ps-analyst` | Root cause, trade-offs, FMEA | References non-existent templates |
| `ps-architect` | ADR creation (Nygard format) | CLI paths hardcoded to ECW |
| `ps-validator` | Constraint validation | References problem-statement skill |
| `ps-synthesizer` | ? | Need to analyze |
| `ps-reviewer` | ? | Need to analyze |
| `ps-investigator` | ? | Need to analyze |
| `ps-reporter` | ? | Need to analyze |

### 2.2 Enforcement Tier Analysis

Current state references 4 tiers but only Advisory is partially implemented:

| Tier | Current State | Target State |
|------|---------------|--------------|
| **Advisory** | Partial (CLAUDE.md, SKILL.md) | Full constitutional principles |
| **Soft** | Not implemented | Self-monitoring, warnings, reflection |
| **Medium** | Not implemented | Tool restrictions, escalation triggers |
| **Hard** | Referenced but not built | Deferred (not focus of this plan) |

---

## 3. Target Architecture

### 3.1 4-Tier Progressive Enforcement Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     JERRY 4-TIER ENFORCEMENT MODEL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TIER 1: ADVISORY (60% of enforcement)                                  │ │
│  │  ─────────────────────────────────────────────────────────────────────  │ │
│  │  • Jerry Constitution (principles)                                      │ │
│  │  • CLAUDE.md / SKILL.md instructions                                    │ │
│  │  • Agent persona definitions                                            │ │
│  │  • Best practice reminders                                              │ │
│  │  Mechanism: System prompts, skill frontmatter                           │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TIER 2: SOFT (30% of enforcement)                                      │ │
│  │  ─────────────────────────────────────────────────────────────────────  │ │
│  │  • Self-monitoring metrics                                              │ │
│  │  • Reflection prompts before destructive actions                        │ │
│  │  • Warning messages (non-blocking)                                      │ │
│  │  • Consent prompts for consequential operations                         │ │
│  │  Mechanism: Agent self-checks, SKILL.md consent patterns                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TIER 3: MEDIUM (8% of enforcement)                                     │ │
│  │  ─────────────────────────────────────────────────────────────────────  │ │
│  │  • Tool restrictions (allowed-tools in frontmatter)                     │ │
│  │  • Escalation triggers                                                  │ │
│  │  • Action logging                                                       │ │
│  │  • Agent trust levels                                                   │ │
│  │  Mechanism: Frontmatter tool lists, escalation protocols                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │  TIER 4: HARD (2% of enforcement) - DEFERRED                            │ │
│  │  ─────────────────────────────────────────────────────────────────────  │ │
│  │  • PreToolUse hooks that block                                          │ │
│  │  • PostToolUse validation                                               │ │
│  │  • Forced escalation                                                    │ │
│  │  • Session termination                                                  │ │
│  │  Mechanism: Python hooks (NOT IMPLEMENTED YET)                          │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Jerry Constitution v1.0

Create `/docs/governance/JERRY_CONSTITUTION.md` with principles:

**General Principles:**
1. Maximize user productivity and learning
2. Respect user autonomy - guide don't control
3. Persist state to survive context compaction
4. Ask when uncertain, escalate when consequential
5. Provide evidence for claims and decisions

**Operational Principles:**
1. Use filesystem as infinite memory (not context)
2. Track work in WORKTRACKER.md
3. Create artifacts, not transient responses
4. Follow BDD Red/Green/Refactor cycle
5. Cite authoritative sources

**Agent Principles:**
1. Agents complete their designated task
2. Agents persist outputs to filesystem
3. Agents self-monitor for quality
4. Agents escalate failures, don't hide them
5. Agents respect tool restrictions

### 3.3 Simplified Agent Structure

New agent template without hard enforcement dependencies:

```yaml
---
name: ps-{function}
description: {purpose}
version: "2.0.0"
enforcement-tier: advisory  # or soft, medium
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  # ... tool list
output:
  required: true
  location: "docs/{category}/{topic-slug}.md"
self-monitoring:
  enabled: true
  metrics: [completion, quality, persistence]
---
```

---

## 4. Implementation Phases

### Phase 1: Foundation (AGT-001 to AGT-005)

| ID | Task | Description | BDD |
|----|------|-------------|-----|
| AGT-001 | Create Jerry Constitution | `/docs/governance/JERRY_CONSTITUTION.md` | RED: Test principles exist, GREEN: Create file |
| AGT-002 | Update CLAUDE.md with constitution reference | Add Advisory principles | RED: Check reference, GREEN: Add reference |
| AGT-003 | Create simplified agent template | Remove hard enforcement references | RED: Template test, GREEN: Create template |
| AGT-004 | Audit all ps-*.md agents | Document current state vs target | Analysis task |
| AGT-005 | Define tool restriction matrix | Which agents get which tools | Analysis task |

### Phase 2: Agent Refactoring (AGT-010 to AGT-018)

| ID | Task | Description | BDD |
|----|------|-------------|-----|
| AGT-010 | Refactor ps-researcher | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-011 | Refactor ps-analyst | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-012 | Refactor ps-architect | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-013 | Refactor ps-validator | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-014 | Refactor ps-synthesizer | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-015 | Refactor ps-reviewer | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-016 | Refactor ps-investigator | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-017 | Refactor ps-reporter | Simplify to Advisory + Soft + Medium | RED: Invocation test, GREEN: Implement |
| AGT-018 | Clean up architecture SKILL.md | Remove hard enforcement references | Edit task |

### Phase 3: Soft Enforcement (AGT-020 to AGT-025)

| ID | Task | Description | BDD |
|----|------|-------------|-----|
| AGT-020 | Implement self-monitoring interface | Metrics collection for agents | RED: Interface test, GREEN: Implement |
| AGT-021 | Add reflection prompts | Pre-action self-assessment | RED: Prompt test, GREEN: Implement |
| AGT-022 | Create warning message patterns | Non-blocking alerts | Design task |
| AGT-023 | Implement consent request pattern | For consequential operations | RED: Consent test, GREEN: Implement |
| AGT-024 | Add quality self-assessment | Agents grade their outputs | Design task |
| AGT-025 | Document soft enforcement patterns | Best practices guide | Documentation |

### Phase 4: Medium Enforcement (AGT-030 to AGT-035)

| ID | Task | Description | BDD |
|----|------|-------------|-----|
| AGT-030 | Define trust levels | Agent privilege matrix | Analysis task |
| AGT-031 | Implement tool restriction enforcement | Validate allowed-tools | RED: Restriction test, GREEN: Implement |
| AGT-032 | Create escalation trigger patterns | When to escalate to user | Design task |
| AGT-033 | Add action logging | Audit trail for agent actions | RED: Logging test, GREEN: Implement |
| AGT-034 | Test trust-based restrictions | Verify enforcement works | Integration test |
| AGT-035 | Document medium enforcement patterns | Best practices guide | Documentation |

---

## 5. File Structure

### Target Directory Structure

```
jerry/
├── docs/
│   ├── governance/
│   │   └── JERRY_CONSTITUTION.md           # NEW: Constitutional principles
│   ├── plans/
│   │   └── AGENT_REORGANIZATION_PLAN.md    # THIS FILE
│   └── research/
│       └── AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md  # EXISTS
├── .claude/
│   ├── agents/
│   │   ├── orchestrator.md                 # EXISTS
│   │   ├── qa-engineer.md                  # EXISTS
│   │   └── security-auditor.md             # EXISTS
│   └── templates/
│       └── agent-template.md               # NEW: Simplified template
└── skills/
    ├── problem-solving/
    │   ├── SKILL.md                        # UPDATE: Simplify
    │   └── agents/
    │       ├── ps-researcher.md            # REFACTOR
    │       ├── ps-analyst.md               # REFACTOR
    │       ├── ps-architect.md             # REFACTOR
    │       ├── ps-validator.md             # REFACTOR
    │       ├── ps-synthesizer.md           # REFACTOR
    │       ├── ps-reviewer.md              # REFACTOR
    │       ├── ps-investigator.md          # REFACTOR
    │       └── ps-reporter.md              # REFACTOR
    └── architecture/
        └── SKILL.md                        # UPDATE: Remove hard enforcement
```

---

## 6. Success Criteria

### Phase 1 Exit Criteria
- [ ] Jerry Constitution v1.0 exists and is referenced in CLAUDE.md
- [ ] Simplified agent template created
- [ ] All ps-*.md agents audited

### Phase 2 Exit Criteria
- [ ] All 8 ps-*.md agents refactored to new template
- [ ] Agents invoke successfully via Task tool
- [ ] Hard enforcement references removed

### Phase 3 Exit Criteria
- [ ] Self-monitoring interface implemented
- [ ] Reflection prompts documented
- [ ] Soft enforcement patterns guide published

### Phase 4 Exit Criteria
- [ ] Trust levels defined and documented
- [ ] Tool restrictions enforced via frontmatter
- [ ] Escalation patterns documented

---

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Agents break during refactor | Medium | High | Incremental changes, test each agent |
| Over-simplification | Low | Medium | Keep core functionality, remove complexity |
| Missing enforcement gaps | Medium | Medium | Document exceptions, plan for iteration |
| Context7 MCP unavailable | High | Low | Make Context7 optional, not required |

---

## 8. References

- [AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md](../research/AGENT_BEHAVIOR_ENFORCEMENT_ANALYSIS.md)
- [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [OpenAI Model Spec (2025)](https://model-spec.openai.com/2025-12-18.html)
- [Google DeepMind Frontier Safety Framework](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/)

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-08 | Claude | Initial creation |
