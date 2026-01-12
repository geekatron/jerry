# Research: Worktracker Skill Gap Inventory

> **PS ID:** init-wt-skills
> **Entry ID:** e-004
> **Topic:** Worktracker Skill Gap Inventory
> **Author:** ps-researcher (Claude Opus 4.5)
> **Created:** 2026-01-11
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

The `problem-solving` skill is the mature reference implementation in Jerry - it has a complete infrastructure with 8 specialized agents, detailed playbooks, and orchestration documentation. Think of it as a well-organized toolbox where each tool has its own manual and clear purpose.

In contrast, the `worktracker` and `worktracker-decomposition` skills are like having the right screwdriver but no manual, no carrying case, and no organization system. They have the core functionality documented in SKILL.md files, but lack the supporting infrastructure that makes agents reliable and maintainable.

**The Gap in Numbers:**
- `problem-solving`: 5,129 total lines across 11 files (SKILL.md + PLAYBOOK.md + ORCHESTRATION.md + 8 agents + 1 template)
- `worktracker-decomposition`: 440 lines in 1 file (SKILL.md only)
- `worktracker`: 336 lines in 1 file (SKILL.md only)

**What This Means:** To bring worktracker skills to parity, we need to create approximately 4,400 lines of new content across agents, playbooks, orchestration docs, and extracted templates. This will enable composable agent workflows, context-rot-resistant operations, and consistent quality standards.

---

## L1: Technical Analysis (Software Engineer)

### 1. File Inventory and Line Counts

#### problem-solving Skill (Reference Implementation)

| File | Lines | Purpose |
|------|-------|---------|
| `skills/problem-solving/SKILL.md` | 265 | Main skill definition, agent catalog, invocation methods |
| `skills/problem-solving/PLAYBOOK.md` | 407 | User guide with examples, patterns, troubleshooting |
| `skills/problem-solving/docs/ORCHESTRATION.md` | 486 | Technical orchestration architecture, state management |
| `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` | 335 | Canonical agent template for consistency |
| `skills/problem-solving/agents/ps-researcher.md` | 459 | Research specialist agent definition |
| `skills/problem-solving/agents/ps-analyst.md` | 442 | Analysis specialist (5 Whys, FMEA, trade-offs) |
| `skills/problem-solving/agents/ps-architect.md` | 426 | Architecture decisions (ADRs) |
| `skills/problem-solving/agents/ps-validator.md` | 429 | Constraint verification |
| `skills/problem-solving/agents/ps-synthesizer.md` | 477 | Pattern extraction across documents |
| `skills/problem-solving/agents/ps-reviewer.md` | 446 | Code/design/security reviews |
| `skills/problem-solving/agents/ps-investigator.md` | 489 | Failure analysis and investigations |
| `skills/problem-solving/agents/ps-reporter.md` | 468 | Status and progress reports |
| **TOTAL** | **5,129** | |

#### worktracker-decomposition Skill

| File | Lines | Purpose |
|------|-------|---------|
| `skills/worktracker-decomposition/SKILL.md` | 440 | Complete skill with inline templates |
| **TOTAL** | **440** | |

**Missing Components:**
- PLAYBOOK.md - Not present
- docs/ORCHESTRATION.md - Not present
- agents/ directory - Not present
- templates/ directory - Not present (templates inline in SKILL.md)

#### worktracker Skill

| File | Lines | Purpose |
|------|-------|---------|
| `skills/worktracker/SKILL.md` | 336 | Work item CRUD operations |
| **TOTAL** | **336** | |

**Missing Components:**
- PLAYBOOK.md - Not present
- docs/ directory - Not present
- agents/ directory - Not present
- templates/ directory - Not present

### 2. Component Comparison Matrix

| Component | problem-solving | worktracker-decomposition | worktracker | Gap Description |
|-----------|-----------------|--------------------------|-------------|-----------------|
| SKILL.md | 265 lines | 440 lines | 336 lines | worktracker skills have content but no agent references |
| PLAYBOOK.md | 407 lines | Missing | Missing | No user guide for either worktracker skill |
| docs/ORCHESTRATION.md | 486 lines | Missing | Missing | No orchestration documentation |
| agents/ directory | 9 files (8 agents + template) | Missing | Missing | No specialized agents |
| Agent template | 335 lines | Missing | Missing | No canonical agent structure |
| Total agent definitions | 3,636 lines | 0 | 0 | No agent backing for operations |
| templates/ directory | Implied | Inline in SKILL.md | Implied | Templates not extracted |
| L0/L1/L2 output levels | Yes (all agents) | Not defined | Not defined | Missing multi-audience output |
| Constitutional compliance | Full (P-001 to P-022) | Partial | Partial | Missing agent-level enforcement |
| State management | Google ADK pattern | Missing | Missing | No state passing between agents |

### 3. Template Extraction Opportunities

#### From worktracker-decomposition/SKILL.md

| Template | Current Location | Lines | Target Location |
|----------|-----------------|-------|-----------------|
| Phase File Template | SKILL.md:297-348 | ~51 | `templates/phase.md` |
| Hub Template | SKILL.md:350-390 | ~40 | `templates/hub.md` |

#### New Templates Needed

| Template | Purpose | Estimated Lines |
|----------|---------|-----------------|
| `templates/analysis-report.md` | Decomposition analysis output | ~80 |
| `templates/validation-report.md` | Post-decomposition validation | ~60 |
| `templates/category.md` | Cross-cutting category file | ~50 |
| `templates/work-item.md` | Individual work item format | ~40 |

### 4. Agent Requirements List

Based on INITIATIVE-WORKTRACKER-SKILLS.md and pattern analysis:

#### For worktracker-decomposition Skill

| Agent | Purpose | Composes With | Output |
|-------|---------|---------------|--------|
| `wt-analyzer` | Analyze WORKTRACKER files for decomposition triggers | ps-analyst, ps-researcher | Analysis report |
| `wt-decomposer` | Execute decomposition transformation | ps-architect, ps-synthesizer | Hub + spoke files |
| `wt-validator` | Validate decomposed structure | ps-validator, ps-reporter | Validation report |

**Estimated Lines per Agent:** ~450 (based on ps-* average of 456 lines)
**Total New Agent Content:** ~1,350 lines

#### For worktracker Skill

| Agent | Purpose | Composes With | Output |
|-------|---------|---------------|--------|
| `wt-creator` | Create work items with proper structure | ps-researcher (for context) | Work item file |
| `wt-tracker` | Track status transitions | ps-reporter | Status update |
| `wt-summarizer` | Generate summaries for session resume | ps-synthesizer | Summary document |

**Estimated Lines per Agent:** ~450
**Total New Agent Content:** ~1,350 lines

### 5. Inline Template Analysis

#### worktracker-decomposition/SKILL.md Inline Templates

**Phase File Template (Lines 297-348):**
```markdown
# Phase N: {Title}
> **Status**: {STATUS_EMOJI} {STATUS} ({PERCENT}%)
> **Goal**: {One-line goal description}
---
## Navigation
| Link | Description |
...
## Task Summary
| Task ID | Title | Status | Subtasks | Output |
...
## Session Context
...
## Document History
```

**Hub Template (Lines 350-390):**
```markdown
# Work Tracker - {PROJECT_ID}
**Last Updated**: {TIMESTAMP}
...
## Navigation Graph
{ASCII diagram}
## Quick Status Dashboard
| Phase | File | Status | Progress |
...
## Session Resume Protocol
```

**Extraction Priority:** HIGH - These templates are duplicated in RUNBOOK-002 and PURPOSE-CATALOG, indicating they should be centralized.

---

## L2: Architectural Implications (Principal Architect)

### 1. Structural Patterns to Replicate

The `problem-solving` skill establishes clear patterns that worktracker skills should follow:

#### Pattern 1: Three-Document Structure
```
skills/{skill-name}/
├── SKILL.md          # What the skill does (contract)
├── PLAYBOOK.md       # How to use it (user guide)
└── docs/
    └── ORCHESTRATION.md  # How it works internally (technical)
```

**Implication:** Both worktracker skills need PLAYBOOK.md and docs/ORCHESTRATION.md.

#### Pattern 2: Agent-Backed Operations
Every command in problem-solving routes to a specialized agent:
- "Research X" -> ps-researcher
- "Analyze X" -> ps-analyst
- "Review X" -> ps-reviewer

**Implication:** worktracker-decomposition commands should route to wt-* agents:
- "@worktracker-decompose analyze" -> wt-analyzer
- "@worktracker-decompose execute" -> wt-decomposer
- "@worktracker-decompose validate" -> wt-validator

#### Pattern 3: Agent Template Consistency
All ps-* agents follow PS_AGENT_TEMPLATE.md with:
- YAML frontmatter (identity, persona, capabilities, guardrails)
- `<agent>` XML block with structured sections
- Constitutional compliance table
- State management schema
- Post-completion verification

**Implication:** Create WT_AGENT_TEMPLATE.md following same structure.

### 2. Dependency Analysis

```
worktracker-decomposition
    ├── depends on: worktracker (for work item operations)
    ├── composes with: problem-solving agents
    │   ├── ps-analyst (gap analysis)
    │   ├── ps-architect (structure decisions)
    │   ├── ps-validator (constraint verification)
    │   └── ps-synthesizer (pattern extraction)
    └── consumed by: any project needing decomposition

worktracker
    ├── depends on: Jerry core (filesystem, git)
    ├── standalone capability
    └── consumed by: all Jerry projects
```

**Risk:** worktracker-decomposition's composition pattern requires problem-solving to be available. If ps-* agents change, wt-* agents may break.

**Mitigation:** Define explicit interface contracts for composed agents.

### 3. Implementation Priority Recommendations

| Priority | Work Item | Rationale | Effort |
|----------|-----------|-----------|--------|
| P0 | Extract templates from SKILL.md | Removes duplication, enables reuse | 2h |
| P1 | Create PLAYBOOK.md for both skills | Improves discoverability and usability | 4h |
| P2 | Create wt-analyzer agent | Enables automated decomposition analysis | 6h |
| P2 | Create wt-decomposer agent | Enables automated decomposition execution | 6h |
| P3 | Create wt-validator agent | Enables post-decomposition validation | 4h |
| P3 | Create docs/ORCHESTRATION.md | Documents composition patterns | 3h |
| P4 | Create worktracker agents | Enables agent-backed work item operations | 8h |

**Total Estimated Effort:** ~33 hours

### 4. Risk Assessment for Gaps

| Gap | Risk Level | Impact if Not Addressed | Mitigation |
|-----|------------|------------------------|------------|
| No agents | HIGH | Operations lack constitutional compliance, L0/L1/L2 output, state management | Implement wt-* agents |
| No PLAYBOOK.md | MEDIUM | Users struggle to understand invocation patterns | Create playbooks |
| Inline templates | MEDIUM | Template changes require SKILL.md edits, duplication risk | Extract to templates/ |
| No ORCHESTRATION.md | LOW | Developers can't understand composition | Create orchestration docs |
| No WT_AGENT_TEMPLATE.md | MEDIUM | Agent inconsistency as more are created | Create template first |

### 5. Strategic Alignment

The gap analysis aligns with:

1. **Jerry Constitution P-002 (File Persistence):** Agent backing ensures all operations produce persistent artifacts, not transient output.

2. **Context Rot Mitigation:** Playbooks and orchestration docs provide compressed knowledge that survives context compaction.

3. **Anthropic Agent Skills Standard:** Skills should be procedural knowledge interfaces with agent backing, not just documentation.

4. **Hexagonal Architecture:** Agents act as primary adapters (interface layer) invoking domain use cases.

---

## References

### Internal Sources

| Source | Path | Key Insight |
|--------|------|-------------|
| problem-solving SKILL.md | `skills/problem-solving/SKILL.md` | Reference skill structure with 8 agents |
| problem-solving PLAYBOOK.md | `skills/problem-solving/PLAYBOOK.md` | User guide pattern with examples |
| problem-solving ORCHESTRATION.md | `skills/problem-solving/docs/ORCHESTRATION.md` | State management and composition patterns |
| ps-researcher.md | `skills/problem-solving/agents/ps-researcher.md` | Agent template reference (459 lines) |
| worktracker-decomposition SKILL.md | `skills/worktracker-decomposition/SKILL.md` | Current state with inline templates |
| worktracker SKILL.md | `skills/worktracker/SKILL.md` | Current state, 336 lines |
| INITIATIVE-WORKTRACKER-SKILLS.md | `projects/PROJ-001-plugin-cleanup/work/INITIATIVE-WORKTRACKER-SKILLS.md` | Work breakdown and agent portfolio |
| RUNBOOK-002 | `projects/PROJ-001-plugin-cleanup/runbooks/RUNBOOK-002-worktracker-decomposition.md` | Procedural decomposition steps |
| PURPOSE-CATALOG | `projects/PROJ-001-plugin-cleanup/work/PURPOSE-CATALOG.md` | File type taxonomy and templates |

### External Sources

| Source | URL | Key Insight |
|--------|-----|-------------|
| Anthropic Agent Skills | [VentureBeat Article](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard) | Skills are procedural knowledge interfaces |
| Context Rot Research | [Chroma Research](https://research.trychroma.com/context-rot) | Context construction matters more than quantity |
| Anthropic Context Engineering | [Anthropic Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Context engineering is the new prompt engineering |

---

## Summary Statistics

| Metric | problem-solving | worktracker-decomposition | worktracker | Gap |
|--------|-----------------|--------------------------|-------------|-----|
| Total files | 11 | 1 | 1 | -10 files |
| Total lines | 5,129 | 440 | 336 | -4,353 lines |
| Agent count | 8 | 0 | 0 | -8 agents |
| L0/L1/L2 support | Yes | No | No | Missing |
| State management | Yes | No | No | Missing |
| Templates extracted | Implied | No | No | Missing |
| Constitutional compliance | Full | Partial | Partial | Incomplete |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-11 | ps-researcher (Claude Opus 4.5) | Initial gap inventory from comparative analysis |
