# INITIATIVE: WORKTRACKER-SKILLS - Shore Up Work Tracking Skills

> **Initiative ID**: INIT-WT-SKILLS
> **Status**: ✅ RESEARCH COMPLETE | 🔄 IMPLEMENTATION PENDING
> **Objective**: Transform thin worktracker skills into robust, agent-backed capabilities

---

## Executive Summary

The `worktracker` and `worktracker-decomposition` skills are currently thin documentation-only interfaces lacking the infrastructure present in mature skills like `problem-solving`. This initiative addresses that gap by implementing agent backing, extracting templates, and aligning with the Anthropic Agent Skills Standard.

### Research Phase Completion (2026-01-11)

The research phase was executed via ps-* agent orchestration, producing 11 artifacts:

| Entry | Type | Document | Status |
|-------|------|----------|--------|
| e-001 | Research | PS Agent Portfolio Analysis | ✅ |
| e-002 | Research | AI Agent Skills Standards | ✅ |
| e-003 | Research | Context Rot Patterns | ✅ |
| e-004 | Research | Worktracker Skill Gaps | ✅ |
| e-005 | Analysis | Gap Analysis | ✅ |
| e-006 | Analysis | Trade-off Analysis | ✅ |
| e-007 | Synthesis | Unified Recommendations | ✅ |
| e-008 | Decision | ADR: Composed Architecture | ✅ |
| e-009 | Analysis | Constitution Validation | ✅ |
| e-010 | Review | Synthesis Review (5/5) | ✅ |
| e-011 | Report | Final Status Report | ✅ |

**Key Decision:** Option C (Composed Architecture) selected with 8.60/10 score.
See: `decisions/ADR-INIT-WT-SKILLS-composed-architecture.md`

**Implementation Roadmap:** 43 hours across 3 phases (see synthesis e-007).

### The Problem

| Skill | Current State | Gap |
|-------|--------------|-----|
| `problem-solving` | SKILL.md + PLAYBOOK.md + 8 agents + orchestration docs | ✅ Reference |
| `worktracker-decomposition` | SKILL.md only (440 lines, inline templates) | ❌ No agents, no extracted templates |
| `worktracker` | Similar state | ❌ Needs same treatment |

### The Solution

Transform worktracker skills using proven patterns from `problem-solving`:
- **Option C**: Specialized agents that compose with ps-* agents (e.g., `wt-decomposer` delegates to `ps-researcher`)
- **Extracted templates**: Move inline templates to `templates/` directory
- **Playbook**: Create orchestration documentation
- **Constitutional compliance**: Full Jerry Constitution adherence

---

## Research Foundation

### ps-* Agent Analysis (8 Agents)

| Agent | Role | Cognitive Mode | Output Location |
|-------|------|----------------|-----------------|
| ps-researcher | Research Specialist | Divergent | `research/` |
| ps-analyst | Analysis Specialist | Convergent | `analysis/` |
| ps-synthesizer | Synthesis Specialist | Convergent | `synthesis/` |
| ps-validator | Validation Specialist | Convergent | `analysis/` |
| ps-reporter | Reporting Specialist | Convergent | `reports/` |
| ps-architect | Architecture Specialist | Convergent | `decisions/` |
| ps-reviewer | Review Specialist | Convergent | `reviews/` |
| ps-investigator | Investigation Specialist | Convergent | `investigations/` |

**Common Features Across All ps-* Agents**:
- Version 2.0.0 schema
- L0/L1/L2 Output Levels (Executive, Engineer, Architect)
- Jerry Constitution v1.0 compliance
- Mandatory file persistence (P-002)
- PS Context integration (ps_id, entry_id)
- State management (Google ADK pattern)
- Prior art citations (P-011)
- Post-completion verification

### Industry Best Practices

#### 1. Anthropic Agent Skills Standard (Dec 2025)

> "MCP provides secure connectivity to external software and data, while skills provide the procedural knowledge for using those tools effectively."
> — [Anthropic Agent Skills](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard)

**Key Insight**: Skills are procedural knowledge interfaces, not just documentation.

#### 2. Context Rot Research (Chroma, July 2025)

> "Not only do LLMs perform worse as more tokens are added to their context, they exhibit more severe performance degradation on more complex tasks."
> — [Chroma Context Rot Research](https://research.trychroma.com/context-rot)

**Key Insight**: How context is constructed matters more than quantity. WORKTRACKER decomposition directly addresses this.

#### 3. Anthropic Context Engineering (2025)

> "The primary takeaway from context rot research is stark: the quantity of input tokens is not the sole determinant of quality. How the context is constructed, filtered, and presented is equally, if not more, vital."
> — [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Key Insight**: Context engineering is the new prompt engineering - skills should embody this knowledge.

#### 4. Composable Agent Patterns (Anthropic)

> "Effective agents come from design choices with three guiding principles: Keep the architecture simple, Make the reasoning process visible, Ensure reliable tool interactions."
> — [Building AI Agents with Anthropic's 6 Composable Patterns](https://research.aimultiple.com/building-ai-agents/)

**Key Insight**: Agents should compose, not monolithically solve.

---

## Architecture Decision

### Option Analysis

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Duplicate ps-* agents for worktracker | Self-contained | Maintenance burden, DRY violation |
| B | Extend ps-* agents with worktracker methods | Single codebase | Coupling, bloat |
| **C** | Specialized agents that compose with ps-* | Clean separation, reuse | Need orchestration |

### Selected: Option C - Composition Pattern

**Rationale**:
1. Follows Anthropic's "composable patterns" guidance
2. Leverages existing, tested ps-* agents
3. Aligns with hexagonal architecture (ports & adapters)
4. Enables worktracker-specific logic without ps-* contamination

**Example Flow**:
```
wt-analyzer (worktracker-specific)
    └── delegates to ps-analyst (generic analysis)
              └── produces analysis/ artifact
    └── adds worktracker-specific interpretation
```

---

## Work Breakdown Structure

### Phase 0: Research (COMPLETE)

| ID | Task | Status | Deliverables |
|----|------|--------|--------------|
| RESEARCH-001 | PS Agent Portfolio Analysis | ✅ DONE | `research/init-wt-skills-e-001-ps-agent-portfolio.md` |
| RESEARCH-002 | Industry Standards Research | ✅ DONE | `research/init-wt-skills-e-002-agent-skills-standards.md` |
| RESEARCH-003 | Context Rot Patterns | ✅ DONE | `research/init-wt-skills-e-003-context-rot-patterns.md` |
| RESEARCH-004 | Skill Gap Inventory | ✅ DONE | `research/init-wt-skills-e-004-worktracker-skill-gaps.md` |
| ANALYSIS-001 | Gap Analysis | ✅ DONE | `analysis/init-wt-skills-e-005-gap-analysis.md` |
| ANALYSIS-002 | Trade-off Analysis | ✅ DONE | `analysis/init-wt-skills-e-006-tradeoff-analysis.md` |
| SYNTHESIS-001 | Unified Recommendations | ✅ DONE | `synthesis/init-wt-skills-e-007-unified-synthesis.md` |
| DECISION-001 | ADR: Composed Architecture | ✅ DONE | `decisions/ADR-INIT-WT-SKILLS-composed-architecture.md` |
| VALIDATION-001 | Constitution Compliance | ✅ DONE | `analysis/init-wt-skills-e-009-constitution-validation.md` |
| REVIEW-001 | Synthesis Quality Review | ✅ DONE | `reviews/init-wt-skills-e-010-synthesis-review.md` |
| REPORT-001 | Final Status Report | ✅ DONE | `reports/init-wt-skills-e-011-status-report.md` |

**Research Phase Metrics:**
- Total artifacts: 11 documents
- Total lines: ~4,000 lines
- Patterns cataloged: 8 (PAT-001 through PAT-008)
- Commit: `cd91d0b`

### Phase 1: Foundation (13 hours estimated)

| ID | Task | Status | Dependencies | Deliverables |
|----|------|--------|--------------|--------------|
| WT-001 | Extract templates from SKILL.md | ⏳ TODO | None | `templates/phase.md`, `templates/hub.md` |
| WT-002 | Create WT_AGENT_TEMPLATE.md | ⏳ TODO | None | `agents/WT_AGENT_TEMPLATE.md` |
| WT-003 | Create PLAYBOOK.md (worktracker) | ⏳ TODO | None | `skills/worktracker/PLAYBOOK.md` |
| WT-004 | Create PLAYBOOK.md (decomposition) | ⏳ TODO | None | `skills/worktracker-decomposition/PLAYBOOK.md` |

### Phase 2: Core Agents (14 hours estimated)

| ID | Task | Status | Dependencies | Deliverables |
|----|------|--------|--------------|--------------|
| WT-005 | wt-coordinator agent | ⏳ TODO | WT-002 | `agents/wt-coordinator.md` |
| WT-006 | ps-analyst adapter | ⏳ TODO | WT-005 | `agents/wt-adapters/ps-analyst.yaml` |
| WT-007 | ps-reporter adapter | ⏳ TODO | WT-005 | `agents/wt-adapters/ps-reporter.yaml` |
| WT-008 | ps-validator adapter | ⏳ TODO | WT-005 | `agents/wt-adapters/ps-validator.yaml` |
| WT-009 | ps-synthesizer adapter | ⏳ TODO | WT-005 | `agents/wt-adapters/ps-synthesizer.yaml` |

### Phase 3: Integration (16 hours estimated)

| ID | Task | Status | Dependencies | Deliverables |
|----|------|--------|--------------|--------------|
| WT-010 | Create ORCHESTRATION.md | ⏳ TODO | WT-009 | `docs/ORCHESTRATION.md` |
| WT-011 | Update @worktracker commands | ⏳ TODO | WT-010 | Updated command handlers |
| WT-012 | Behavioral tests (P-003) | ⏳ TODO | WT-011 | `tests/behavioral/test_p003.py` |
| WT-013 | Compaction triggers | ⏳ TODO | WT-011 | Context compaction hooks |

**Total Implementation Effort:** 43 hours (~5.5 person-days)

---

## Proposed Agent Portfolio

### wt-analyzer

**Purpose**: Analyze WORKTRACKER files to determine if decomposition is needed.

**Composes With**:
- `ps-analyst` for gap analysis (current vs desired state)
- `ps-researcher` for best practices lookup

**Output**: Analysis report with trigger assessment, phase breakdown, recommendation.

### wt-decomposer

**Purpose**: Execute the decomposition transformation.

**Composes With**:
- `ps-architect` for structure decisions
- `ps-synthesizer` for pattern extraction

**Output**: Hub file + spoke files + navigation links.

### wt-validator

**Purpose**: Validate decomposed structure for completeness and correctness.

**Composes With**:
- `ps-validator` for constraint verification
- `ps-reporter` for validation report

**Output**: Validation report with pass/fail status.

---

## Templates to Extract

### From worktracker-decomposition/SKILL.md (lines 296-390):

| Template | Current Location | Target Location |
|----------|-----------------|-----------------|
| Phase File Template | SKILL.md:296-348 | `templates/phase.md` |
| Hub Template | SKILL.md:350-390 | `templates/hub.md` |

### New Templates Needed:

| Template | Purpose |
|----------|---------|
| `templates/analysis-report.md` | Decomposition analysis output |
| `templates/validation-report.md` | Post-decomposition validation |
| `templates/category.md` | Cross-cutting category template |

---

## Success Criteria

1. **Agent Coverage**: 3+ agents in `worktracker-decomposition/agents/`
2. **Template Extraction**: All templates in `templates/` directory
3. **Playbook**: PLAYBOOK.md with orchestration patterns
4. **Docs**: docs/ORCHESTRATION.md explaining composition
5. **Tests**: Fresh context execution validates full workflow
6. **Parity**: Same structural pattern as `problem-solving` skill

---

## References

### Industry Sources

1. [Anthropic Agent Skills Standard](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard) - Dec 2025
2. [Chroma Context Rot Research](https://research.trychroma.com/context-rot) - July 2025
3. [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - 2025
4. [Building AI Agents - Anthropic Patterns](https://research.aimultiple.com/building-ai-agents/) - 2025
5. [Martin Fowler - Agile Practices](https://martinfowler.com/agile.html) - 2025

### Internal Sources

1. `skills/problem-solving/agents/*.md` - 8 ps-* agent definitions
2. `projects/PROJ-001-plugin-cleanup/runbooks/RUNBOOK-002-worktracker-decomposition.md`
3. `projects/PROJ-001-plugin-cleanup/work/PURPOSE-CATALOG.md`
4. `docs/governance/JERRY_CONSTITUTION.md`

---

---

## Navigation

| Link | Description |
|------|-------------|
| [← WORKTRACKER](../WORKTRACKER.md) | Back to main tracker |
| [PHASE-DISCOVERY](PHASE-DISCOVERY.md) | Related discoveries (DISC-003, DISC-004) |
| [PHASE-TECHDEBT](PHASE-TECHDEBT.md) | Related tech debt (TD-010) |
| [ADR](../decisions/ADR-INIT-WT-SKILLS-composed-architecture.md) | Architecture decision |
| [Synthesis](../synthesis/init-wt-skills-e-007-unified-synthesis.md) | Unified recommendations |

---

## Related Items

### Discoveries
- **DISC-003**: link-artifact CLI command missing → TD-010
- **DISC-004**: ps-* agent orchestration validated Composed Architecture

### Technical Debt
- **TD-010**: Implement link-artifact CLI command (blocks full ps-* protocol)

### Bugs
- None identified during research phase

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-11 | Claude | Initial creation from DOC-001 expansion |
| 2026-01-11 | Claude | Research phase complete: 11 artifacts, ADR accepted |
