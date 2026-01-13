# Knowledge Extraction: PROJ-001 Insights for Agents Cleanup

> **PS ID:** proj-003
> **Entry ID:** e-004
> **Date:** 2026-01-12
> **Author:** ps-analyst agent (v2.0.0)
> **Analysis Type:** knowledge-extraction
> **Topic:** PROJ-001 Knowledge Base Extraction for Agents/Skills Cleanup

---

## L0: Executive Summary (ELI5)

PROJ-001-plugin-cleanup established comprehensive standards for organizing agents and skills in the Jerry framework. Think of it as creating a "rulebook" for how AI assistants should be organized and behave.

**Key Findings:**

1. **Agents live in TWO places** - general-purpose agents in `.claude/agents/` and skill-specific agents in `skills/{skill}/agents/`. The `problem-solving` skill is the reference implementation with 8 specialized agents.

2. **Less is more for instructions** - Anthropic recommends keeping CLAUDE.md to 100-200 lines maximum. Claude can only reliably follow ~150-200 instructions. Jerry's current setup (4 rules files totaling ~800 lines) may be too verbose.

3. **One file per concept** - The Design Canon mandates "clean, verbose, atomic structure" where each class/concept gets its own file for discoverability.

4. **Skills need agent backing** - The worktracker skills are "incomplete" compared to problem-solving because they lack agents, playbooks, and orchestration docs. This is a known gap.

5. **Constitutional compliance is mandatory** - All agents must follow the Jerry Constitution with specific enforcement levels (P-001 through P-022).

**Cleanup Implications:**
- The `.claude/agents/` directory should contain ONLY general-purpose agents (orchestrator, qa-engineer, security-auditor)
- Skill-specific agents (ps-*, wt-*) belong in `skills/{skill}/agents/`
- Any duplicated agent definitions should be consolidated
- Missing worktracker agents may be out of scope for "cleanup" (they were never created)

---

## L1: Technical Analysis (Software Engineer)

### 1. Current Agent Organization

Based on PROJ-001 research, Jerry has two distinct agent locations:

#### Location 1: `.claude/agents/` (General Purpose)

| Agent | File | Purpose | Status |
|-------|------|---------|--------|
| orchestrator | `orchestrator.md` | Task decomposition, delegation, synthesis | Active |
| qa-engineer | `qa-engineer.md` | Test design, quality assurance | Active |
| security-auditor | `security-auditor.md` | Security review, vulnerability assessment | Active |
| TEMPLATE | `TEMPLATE.md` | Agent creation template | Reference |

**Source:** `AGENTS.md` (root), `.claude/agents/` directory

#### Location 2: `skills/problem-solving/agents/` (Skill-Specific)

| Agent | File | Lines | Purpose |
|-------|------|-------|---------|
| ps-researcher | `ps-researcher.md` | 459 | Information gathering, 5W1H framework |
| ps-analyst | `ps-analyst.md` | 442 | Root cause analysis, 5 Whys, FMEA |
| ps-synthesizer | `ps-synthesizer.md` | 477 | Pattern extraction, thematic analysis |
| ps-validator | `ps-validator.md` | 429 | Constraint verification, RTM |
| ps-reporter | `ps-reporter.md` | 468 | Status reporting, health indicators |
| ps-architect | `ps-architect.md` | 426 | ADR creation, architecture decisions |
| ps-reviewer | `ps-reviewer.md` | 446 | Code/design/security reviews |
| ps-investigator | `ps-investigator.md` | 489 | Failure analysis, incident response |
| PS_AGENT_TEMPLATE | `PS_AGENT_TEMPLATE.md` | 335 | Template for ps-* agents |

**Source:** `init-wt-skills-e-001-ps-agent-portfolio.md`

### 2. Canonical Agent Structure (from PS_AGENT_TEMPLATE)

PROJ-001 established the canonical agent definition format:

```yaml
# Agent Definition Structure
- YAML Frontmatter (name, version, capabilities, etc.)
- <agent> XML block containing:
  - <identity>: role, expertise, cognitive mode
  - <persona>: tone, communication style
  - <capabilities>: allowed tools, forbidden actions
  - <guardrails>: input validation, output filtering
  - <constitutional_compliance>: principle mapping, self-critique
  - <invocation_protocol>: PS context, mandatory persistence
  - <output_levels>: L0/L1/L2 definitions
  - <state_management>: output key, upstream/downstream
```

**Pattern ID:** PAT-001 (Agent Definition Template Pattern)
**Source:** `init-wt-skills-e-001-ps-agent-portfolio.md` L209-219

### 3. Constitutional Compliance Requirements

All agents must apply these principles:

| Principle | Enforcement | Universal Behavior |
|-----------|-------------|-------------------|
| P-001 (Truth/Accuracy) | Soft | All claims cite sources/evidence |
| P-002 (File Persistence) | **Medium** | ALL output MUST be persisted to files |
| P-003 (No Recursion) | **Hard** | Task tool spawns single-level only |
| P-004 (Provenance) | Soft | Methodology and sources documented |
| P-011 (Evidence-Based) | Soft | Recommendations tied to evidence |
| P-020 (User Authority) | **Hard** | ADRs marked PROPOSED until user approves |
| P-022 (No Deception) | **Hard** | Transparent about limitations/gaps |

**Source:** `init-wt-skills-e-001-ps-agent-portfolio.md` L102-115

### 4. File Organization Standards (ADR-003)

PROJ-001 established "one file per concept" as mandatory:

| Type | Pattern | Example |
|------|---------|---------|
| Value Object | One file per VO | `project_id.py`, `task_id.py` |
| Entity | One file per entity | `project_info.py` |
| Aggregate Root | One file per AR | `task.py`, `phase.py` |
| Domain Event | One file per event | `task_completed.py` |
| Query/Command | One file per handler | `scan_projects.py` |
| Agent | One file per agent | `ps-researcher.md` |

**Source:** `ADR-003-code-structure.md` L132-146

### 5. CLAUDE.md Verbosity Guidelines

PROJ-001 research identified that Jerry's configuration may be too verbose:

| Component | Current State | Recommended | Gap |
|-----------|---------------|-------------|-----|
| Root CLAUDE.md | ~400+ lines | 100-200 lines | HIGH |
| .claude/rules/ total | ~800 lines | <200 lines total | CRITICAL |
| Pattern Catalog | Progressive disclosure | Already aligned | OK |

**Key Quote:** "Frontier thinking LLMs can follow ~150-200 instructions with reasonable consistency."

**Recommendations from PROJ-001:**
1. **R1:** Restructure CLAUDE.md as index (use `@path` imports)
2. **R2:** Add path scoping to rules files
3. **R3:** Move session-specific content to project CLAUDE.md
4. **R4:** Convert Pattern Catalog to SKILL.md format (low priority)

**Source:** `td-017-e-006-claude-code-best-practices.md` L182-371

### 6. Skills Gap Analysis

PROJ-001 documented that worktracker skills lack agent backing:

| Metric | problem-solving | worktracker-decomposition | worktracker |
|--------|-----------------|--------------------------|-------------|
| Total files | 11 | 1 | 1 |
| Total lines | 5,129 | 440 | 336 |
| Agent count | 8 | 0 | 0 |
| PLAYBOOK.md | Yes | No | No |
| ORCHESTRATION.md | Yes | No | No |
| Template extracted | Yes | No (inline) | No |

**Missing worktracker agents (planned):**
- `wt-analyzer` - Analyze WORKTRACKER files
- `wt-decomposer` - Execute decomposition
- `wt-validator` - Validate decomposed structure
- `wt-creator` - Create work items
- `wt-tracker` - Track status transitions
- `wt-summarizer` - Generate session summaries

**Source:** `init-wt-skills-e-004-worktracker-skill-gaps.md`

---

## L2: Architectural Implications (Principal Architect)

### 1. Canonical Directory Structure Decision

PROJ-001 established the definitive agent organization:

```
jerry/
├── .claude/
│   ├── agents/                    # GENERAL PURPOSE agents only
│   │   ├── orchestrator.md        # Conductor pattern
│   │   ├── qa-engineer.md         # Testing specialist
│   │   ├── security-auditor.md    # Security specialist
│   │   └── TEMPLATE.md            # General agent template
│   ├── rules/                     # Configuration rules
│   └── patterns/                  # Pattern catalog
│
├── skills/
│   ├── problem-solving/
│   │   ├── SKILL.md               # Skill definition
│   │   ├── PLAYBOOK.md            # User guide
│   │   ├── agents/                # SKILL-SPECIFIC agents
│   │   │   ├── PS_AGENT_TEMPLATE.md
│   │   │   ├── ps-researcher.md
│   │   │   ├── ps-analyst.md
│   │   │   └── ... (8 total)
│   │   └── docs/
│   │       └── ORCHESTRATION.md
│   │
│   ├── worktracker/
│   │   └── SKILL.md               # Missing: agents/, PLAYBOOK.md
│   │
│   └── worktracker-decomposition/
│       └── SKILL.md               # Missing: agents/, PLAYBOOK.md
│
└── AGENTS.md                      # Agent registry
```

**Design Decision:** Skill-specific agents belong with their skill, not in `.claude/agents/`.

### 2. Relevant Decisions from PROJ-001

| Decision | Context | Applies to Cleanup? |
|----------|---------|---------------------|
| ADR-003: One file per concept | Code organization | YES - agents should follow |
| PAT-001: Agent template pattern | Agent consistency | YES - use PS_AGENT_TEMPLATE as reference |
| PAT-002: L0/L1/L2 output levels | Multi-audience output | YES - all agents need this |
| R1: Restructure CLAUDE.md | Reduce verbosity | MAYBE - out of scope? |
| R2: Path-scoped rules | Targeted rules | MAYBE - out of scope? |

### 3. Cleanup Scope Clarification

Based on PROJ-001 knowledge, the cleanup task should:

**IN SCOPE:**
1. Verify `.claude/agents/` contains only general-purpose agents
2. Verify `skills/problem-solving/agents/` contains ps-* agents
3. Check for duplicate agent definitions between locations
4. Ensure agent files follow canonical template structure
5. Validate AGENTS.md registry is accurate and complete

**POTENTIALLY OUT OF SCOPE:**
1. Creating missing worktracker agents (they were never created - this is greenfield work, not cleanup)
2. Restructuring CLAUDE.md (separate initiative)
3. Adding path scoping to rules (separate initiative)
4. Creating PLAYBOOK.md for worktracker skills (enhancement, not cleanup)

**KEY INSIGHT:** The "cleanup" distinction is important. Cleanup implies removing/organizing existing content, while creating new worktracker agents is new development.

### 4. Patterns to Apply During Cleanup

| Pattern | ID | Application |
|---------|-----|-------------|
| Agent Definition Template | PAT-001 | Ensure all agents follow structure |
| Layered Output Levels | PAT-002 | Verify L0/L1/L2 in all agents |
| Constitutional Compliance | PAT-003 | Check principle mapping exists |
| Persistence-First Output | PAT-004 | Verify output.location defined |
| Single-Level Delegation | PAT-005 | Verify Task tool restrictions |

**Source:** `init-wt-skills-e-001-ps-agent-portfolio.md` L208-275

### 5. Agent Composition Relationships

The ps-* agents form a pipeline:

```
INFORMATION GATHERING          ANALYSIS & SYNTHESIS            OUTPUT

┌─────────────────┐
│  ps-researcher  │──────┐
│   (divergent)   │      │
└─────────────────┘      │
                         │     ┌─────────────────┐
                         ├────►│   ps-analyst    │──────┐
                         │     └─────────────────┘      │
                         │                              │
                         │     ┌─────────────────┐      │
                         └────►│  ps-synthesizer │──────┼────► ps-reporter
                               └─────────────────┘      │
                                                        │
                               ┌─────────────────┐      │
                               │   ps-architect  │◄─────┤
                               └─────────────────┘      │
                                      │                 │
                                      ▼                 │
                               ┌─────────────────┐      │
                               │  ps-validator   │◄─────┘
                               └─────────────────┘
                                      │
                                      ▼
                               ┌─────────────────┐
                               │   ps-reviewer   │
                               └─────────────────┘
                                      │
                                      ▼
                               ┌─────────────────┐
                               │ ps-investigator │
                               └─────────────────┘
```

**Implication:** Cleanup should preserve these relationships. Any changes to agent locations must maintain the composition capability.

---

## Evidence Table

| Document | Path | Key Quotes/Findings |
|----------|------|---------------------|
| Agent Skills Standards | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-002-agent-skills-standards.md` | "A Skill is a modular knowledge package: a folder containing a SKILL.md file" (L30-39) |
| PS Agent Portfolio | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-001-ps-agent-portfolio.md` | 8 agents, PAT-001 through PAT-006 patterns (L208-396) |
| Claude Code Best Practices | `projects/PROJ-001-plugin-cleanup/research/td-017-e-006-claude-code-best-practices.md` | "Sweet spot is 100-200 lines maximum for CLAUDE.md" (L420-421), R1-R4 recommendations (L309-371) |
| Jerry Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` | Hexagonal Architecture, CQRS, Event Sourcing canonical patterns |
| Unified Architecture Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md` | Layer dependency rules (L818-827), directory structure (L829-852) |
| ADR-003 Code Structure | `projects/PROJ-001-plugin-cleanup/design/ADR-003-code-structure.md` | "One file per concept" mandate (L132-146) |
| Worktracker Skill Gaps | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-004-worktracker-skill-gaps.md` | Missing: 8 agents, PLAYBOOK.md, ORCHESTRATION.md for worktracker skills (L296-306) |
| AGENTS.md | `AGENTS.md` (root) | General agent registry, handoff protocol (L78-96) |

---

## Relevant Decisions Summary

### Decisions That Apply to Cleanup

1. **Agent Location Decision**
   - General agents: `.claude/agents/`
   - Skill agents: `skills/{skill}/agents/`
   - Source: Directory structure conventions in Design Canon

2. **One File Per Concept (ADR-003)**
   - Each agent gets its own file
   - No bundling multiple agents in one file
   - Source: ADR-003-code-structure.md

3. **Agent Template Requirement (PAT-001)**
   - All agents follow PS_AGENT_TEMPLATE structure
   - YAML frontmatter + XML blocks mandatory
   - Source: init-wt-skills-e-001-ps-agent-portfolio.md

4. **Constitutional Compliance (PAT-003)**
   - P-002 (Medium): Output persistence mandatory
   - P-003 (Hard): Single-level delegation only
   - P-022 (Hard): No deception about capabilities
   - Source: init-wt-skills-e-001-ps-agent-portfolio.md

### Gaps Identified in PROJ-001

1. **Worktracker agents not created** - Known gap, but this is greenfield work, not cleanup
2. **CLAUDE.md verbosity** - May be out of scope for "cleanup"
3. **Rules file verbosity** - May be out of scope for "cleanup"
4. **Template extraction from SKILL.md** - Known gap for worktracker skills

---

## Canonical Patterns Summary

| Pattern ID | Name | Enforcement | Cleanup Relevance |
|------------|------|-------------|-------------------|
| PAT-001 | Agent Definition Template | MANDATORY | Verify all agents follow |
| PAT-002 | L0/L1/L2 Output Levels | MANDATORY | Check all agents have |
| PAT-003 | Constitutional Compliance | MANDATORY | Verify principle mapping |
| PAT-004 | Persistence-First Output | MEDIUM | Check output.location |
| PAT-005 | Single-Level Delegation | HARD | Verify Task tool usage |
| PAT-006 | Cognitive Mode Alignment | HIGH | Check divergent/convergent |

---

## Migration Guidance

### If Moving Agents Between Locations

1. **Identify agent purpose** - Is it general or skill-specific?
2. **Check dependencies** - What does this agent compose with?
3. **Update AGENTS.md** - Registry must reflect actual locations
4. **Update skill SKILL.md** - If moving to skill, update agent catalog
5. **Test invocation** - Ensure Claude can still find and invoke agent

### If Consolidating Duplicates

1. **Identify canonical version** - Which is more complete?
2. **Merge unique content** - Combine any unique sections
3. **Remove duplicate** - Delete the redundant file
4. **Update references** - Find all files that reference the duplicate

### If Standardizing Agent Format

1. **Use PS_AGENT_TEMPLATE as reference**
2. **Add missing sections** - YAML frontmatter, XML blocks
3. **Add constitutional compliance** - Principle mapping table
4. **Add state management** - Output key, upstream/downstream

---

## References

### PROJ-001 Source Documents

| ID | Title | Path |
|----|-------|------|
| e-001 | PS Agent Portfolio | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-001-ps-agent-portfolio.md` |
| e-002 | Agent Skills Standards | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-002-agent-skills-standards.md` |
| e-004 | Worktracker Skill Gaps | `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-004-worktracker-skill-gaps.md` |
| td-017-e-006 | Claude Code Best Practices | `projects/PROJ-001-plugin-cleanup/research/td-017-e-006-claude-code-best-practices.md` |
| e-006 | Unified Architecture Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md` |
| e-011-v1 | Jerry Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| ADR-003 | Code Structure | `projects/PROJ-001-plugin-cleanup/design/ADR-003-code-structure.md` |

### Current Repository Structure

| Location | Contents |
|----------|----------|
| `.claude/agents/` | orchestrator.md, qa-engineer.md, security-auditor.md, TEMPLATE.md |
| `skills/problem-solving/agents/` | 8 ps-* agents + PS_AGENT_TEMPLATE.md |
| `skills/worktracker/` | SKILL.md only (no agents) |
| `skills/worktracker-decomposition/` | SKILL.md only (no agents) |
| `skills/architecture/` | SKILL.md only |
| `AGENTS.md` | Agent registry |

---

*Document generated by ps-analyst agent v2.0.0*
*Constitutional Compliance: P-001, P-002, P-004, P-011*
*Analysis completed: 2026-01-12*
