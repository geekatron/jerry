# PLAN: CLAUDE.md Optimization and Decomposition

> **Document ID**: PLAN-CLAUDE-MD-OPTIMIZATION
> **Version**: 1.0
> **Date**: 2026-02-01
> **Status**: APPROVED
> **Author**: ps-synthesizer (orchestrated)

---

## Executive Summary

This plan addresses the critical need to optimize Jerry's CLAUDE.md file from its current **914 lines (~10,000 tokens)** to a target of **60-80 lines (~3,300-3,500 tokens)** - a **91-93% reduction**. The optimization is essential for OSS release readiness, developer onboarding experience, and preventing context rot that degrades LLM performance.

### Key Outcomes

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| CLAUDE.md Lines | 914 | 60-80 | 91-93% reduction |
| Token Footprint | ~10,000 | ~3,300-3,500 | 65-67% reduction |
| Session Start Load | All content | Tier 1 only | Progressive disclosure |
| Worktracker Lines | 371 (inline) | 0 (skill) | 100% extraction |

### Strategic Approach

The plan implements a **Tiered Hybrid Loading Strategy** with four tiers:
- **Tier 1**: CLAUDE.md root (~60-80 lines) - Always loaded
- **Tier 2**: `.claude/rules/` (~500 lines) - Auto-loaded by Claude Code
- **Tier 3**: Skills (~1,500+ lines) - On-demand via `/skill` invocation
- **Tier 4**: Reference docs (unlimited) - Explicit file access when needed

---

## Current State Analysis

### CLAUDE.md Structure (914 lines)

```
Current CLAUDE.md Breakdown:
├── Project Overview                    ~50 lines
├── Worktracker Section                ~371 lines (40.6%)  [EXTRACT]
│   ├── Entity Hierarchy               ~80 lines
│   ├── Entity Classification          ~60 lines
│   ├── System Mappings                ~120 lines
│   └── Directory Structure            ~111 lines
├── TODO Section                        ~80 lines
├── Architecture                        ~50 lines
├── Working with Jerry                  ~100 lines
├── Project Enforcement                 ~80 lines
├── Skills/Agents Tables               ~50 lines
├── Mandatory Skill Usage              ~80 lines
├── Code Standards (inline)            ~30 lines
└── References                         ~23 lines
```

### Problems Identified

1. **Context Rot Risk**: At 914 lines, CLAUDE.md consumes ~10,000 tokens at every session start
2. **OSS Onboarding Barrier**: New contributors face a wall of text before writing code
3. **Redundancy**: `.claude/rules/` already exists but content is duplicated in CLAUDE.md
4. **Worktracker Dominance**: 40% of CLAUDE.md is worktracker content that belongs in a skill
5. **No Progressive Disclosure**: All information loaded regardless of task relevance

### Context Rot Science

Research from [Chroma](https://research.trychroma.com/context-rot) demonstrates:
- LLM performance degrades as context window fills
- **75% utilization is the sweet spot** for quality
- At 90%+ utilization, performance significantly degrades
- Selective context > maximum context

---

## Research Findings

### Claude Code Native Mechanisms

| Mechanism | Loading | Best For |
|-----------|---------|----------|
| `CLAUDE.md` | Always | Critical identity, navigation pointers |
| `.claude/rules/*.md` | Auto-loaded | Coding standards, architecture rules |
| `@file.md` syntax | Eager on reference | Critical dependencies needed immediately |
| Plain file reference | Lazy on access | Supporting documentation |
| Skills | On-demand | Specialized workflows |

### Industry Best Practices

From [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [Builder.io](https://www.builder.io/blog/claude-md-guide), and [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices):

1. **Keep it Lean and Focused**: "Less (instructions) is more"
2. **Progressive Disclosure**: "Tell Claude how to find information, not all the information"
3. **Pointers Over Copies**: "Include file:line references to point Claude to authoritative context"
4. **Modular Rules**: "Each file in `.claude/rules/` should cover one topic"
5. **Directory-Level Rules**: Use directory-specific CLAUDE.md for context-relevant loading

### @ Import Syntax

Claude Code supports file inclusion via `@path/to/file.md`:
- Content is included when Claude processes the reference
- Supports up to 5 hops of nested includes
- Best for critical context that must be available immediately

**Usage Pattern**:
```markdown
See @docs/architecture.md for system design
Review @.claude/rules/coding-standards.md for style guide
```

---

## Architecture Decisions

### ADR-OSS-001: Decomposition Strategy

**Decision**: Use "Option C: Hybrid with Lazy Loading"

**Rationale**:
- Maximizes context efficiency (91-93% reduction)
- Leverages Claude Code native mechanisms
- Maintains full functionality via progressive disclosure
- Reduces OSS onboarding cognitive load

### ADR-OSS-003: Worktracker Extraction

**Decision**: Complete extraction to `/worktracker` skill

**Rationale**:
- Worktracker is 371 lines (40% of CLAUDE.md)
- Skill invocation provides on-demand loading
- Maintains full functionality without always-loaded overhead
- Existing skill infrastructure already in place

### ADR-OSS-004: Multi-Persona Documentation

**Decision**: Implement L0/L1/L2 documentation pattern

| Level | Audience | Length | Purpose |
|-------|----------|--------|---------|
| L0 | ELI5 | 200-400 words | Quick understanding |
| L1 | Engineer | 800-2000 words | Implementation details |
| L2 | Architect | 500-1500 words | Trade-offs, rationale |

---

## Decomposition Strategy

### Tier 1: CLAUDE.md Root (~75 lines)

The new CLAUDE.md will contain ONLY:

```markdown
# CLAUDE.md - Jerry Framework

## Identity (10 lines)
- Framework purpose statement
- Core principle: "Filesystem as infinite memory"
- Context rot reference

## Navigation Pointers (20 lines)
- How to find coding standards → .claude/rules/
- How to find skills → skills/
- How to find project context → projects/
- How to find knowledge → docs/

## Active Project (15 lines)
- Project context enforcement
- JERRY_PROJECT variable
- Hook output interpretation

## Critical Constraints (15 lines)
- P-003: No recursive subagents (HARD)
- P-020: User authority (HARD)
- P-022: No deception (HARD)
- Python 3.11+ / UV only

## Quick Reference (15 lines)
- CLI command summary (jerry session/items/projects)
- Skill invocation summary
- Key file locations
```

### Tier 2: .claude/rules/ (Auto-Loaded)

Existing rules already in place:
- `architecture-standards.md` - Hexagonal, CQRS, ES
- `coding-standards.md` - Python style, type hints
- `error-handling-standards.md` - Exception hierarchy
- `file-organization.md` - Directory structure
- `python-environment.md` - UV requirements
- `testing-standards.md` - Test pyramid, BDD
- `tool-configuration.md` - pytest, mypy, ruff

**No changes needed** - these are already properly structured.

### Tier 3: Skills (On-Demand)

| Skill | Content Moved | Lines |
|-------|---------------|-------|
| `/worktracker` | Entity hierarchy, mappings, templates, behavior | 371+ |
| `/problem-solving` | PS framework, agents | (existing) |
| `/nasa-se` | SE processes | (existing) |
| `/orchestration` | Workflow coordination | (existing) |
| `/architecture` | ADR guidance | (existing) |

### Tier 4: Reference Documentation

- `docs/governance/JERRY_CONSTITUTION.md` - Full constitution
- `docs/design/ADR-*.md` - Architecture decisions
- `docs/knowledge/` - Pattern catalog, exemplars
- `.context/templates/worktracker/` - Work item templates

---

## Implementation Phases

### Phase 1: Worktracker Skill Extraction (2-3 hours)

**Objective**: Extract 371 lines of worktracker content to skill

**Tasks**:
1. Fix SKILL.md description (currently has transcript skill copy-paste bug)
2. Create `skills/worktracker/rules/worktracker-entity-hierarchy.md`
3. Create `skills/worktracker/rules/worktracker-system-mappings.md`
4. Create `skills/worktracker/rules/worktracker-behavior-rules.md`
5. Create `skills/worktracker/rules/worktracker-directory-structure.md`
6. Update `skills/worktracker/SKILL.md` with navigation pointers
7. Validate skill loads correctly on invocation

**Acceptance Criteria**:
- [ ] `/worktracker` skill loads all entity and mapping information
- [ ] No worktracker content remains in CLAUDE.md
- [ ] All template references work correctly

### Phase 2: CLAUDE.md Rewrite (2-3 hours)

**Objective**: Create new 60-80 line CLAUDE.md

**Tasks**:
1. Create new CLAUDE.md following Tier 1 structure
2. Add identity section (~10 lines)
3. Add navigation pointers section (~20 lines)
4. Add active project section (~15 lines)
5. Add critical constraints section (~15 lines)
6. Add quick reference section (~15 lines)
7. Validate all pointers resolve correctly

**Acceptance Criteria**:
- [ ] CLAUDE.md is 60-80 lines
- [ ] Token count is ~3,300-3,500
- [ ] All navigation pointers work
- [ ] No duplicated content from rules/

### Phase 3: TODO Section Migration (1 hour)

**Objective**: Move TODO behavior rules to worktracker skill

**Tasks**:
1. Create `skills/worktracker/rules/todo-integration.md`
2. Move META TODO requirements to worktracker skill
3. Add brief TODO mention in CLAUDE.md quick reference
4. Update skill to load TODO rules on invocation

**Acceptance Criteria**:
- [ ] TODO section removed from CLAUDE.md
- [ ] Worktracker skill includes TODO behavior
- [ ] Brief TODO pointer remains in CLAUDE.md

### Phase 4: Validation & Testing (1-2 hours)

**Objective**: Verify optimization success

**Tasks**:
1. Start fresh Claude Code session
2. Verify context token count at session start
3. Test `/worktracker` skill invocation
4. Test navigation pointers resolve
5. Test typical workflows (project creation, work tracking)
6. Document any issues found

**Acceptance Criteria**:
- [ ] Session start tokens < 5,000 (vs ~10,000 before)
- [ ] All skills load correctly
- [ ] No broken references
- [ ] Typical workflows unchanged

### Phase 5: Documentation Update (1 hour)

**Objective**: Update supporting documentation

**Tasks**:
1. Update INSTALLATION.md with new structure explanation
2. Create CLAUDE-MD-GUIDE.md for contributors
3. Update relevant ADRs with implementation status
4. Add context optimization rationale to docs/design/

---

## Validation Criteria

### Quantitative Metrics

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| CLAUDE.md lines | 60-80 | `wc -l CLAUDE.md` |
| CLAUDE.md tokens | 3,300-3,500 | Claude Code `/context` command |
| Total rules lines | ~500 | `wc -l .claude/rules/*.md` |
| Worktracker skill lines | 400+ | `wc -l skills/worktracker/rules/*.md` |

### Qualitative Criteria

| Criterion | Validation |
|-----------|------------|
| OSS onboarding improved | New contributor can start contributing within 10 minutes |
| Skill invocation works | `/worktracker` loads all entity information |
| Navigation pointers work | All file references resolve |
| No functionality regression | All existing workflows still function |
| Context rot addressed | Session start under 50% context utilization |

### Test Scenarios

1. **Fresh Session Test**: Start new Claude Code session, verify token count
2. **Skill Invocation Test**: Invoke `/worktracker`, verify content loads
3. **Navigation Test**: Follow each pointer in CLAUDE.md, verify target exists
4. **Workflow Test**: Create project, create work items, complete typical tasks
5. **OSS Contributor Test**: Simulate new contributor experience

---

## Risk Mitigation

### Risk 1: Loss of Critical Information

**Risk**: Important instructions might be lost during extraction

**Mitigation**:
- Create comprehensive mapping of all CLAUDE.md sections to destinations
- Verify each section has a home in new structure
- Test all workflows after migration
- Keep backup of original CLAUDE.md

### Risk 2: Skill Invocation Overhead

**Risk**: Users forget to invoke skills, missing important context

**Mitigation**:
- CLAUDE.md explicitly states when to use each skill
- Skills auto-suggest based on context (e.g., work item discussion triggers worktracker)
- Brief inline reminders in CLAUDE.md

### Risk 3: Rules Loading Inconsistency

**Risk**: `.claude/rules/` might not load consistently

**Mitigation**:
- Test on multiple platforms (macOS, Linux, Windows)
- Document any platform-specific behavior
- Fallback: include critical rules inline with @ imports

### Risk 4: Contributor Confusion

**Risk**: Contributors unfamiliar with tiered structure

**Mitigation**:
- Create clear CLAUDE-MD-GUIDE.md explaining structure
- Include "How to Find Information" section in CLAUDE.md
- Update CONTRIBUTING.md with context management guidance

### Risk 5: Backward Compatibility

**Risk**: Breaking changes for existing users

**Mitigation**:
- Version CLAUDE.md changes clearly
- Provide migration notes in release
- Maintain semantic versioning for structure changes

---

## Timeline and Effort

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Worktracker Extraction | 2-3 hours | None |
| Phase 2: CLAUDE.md Rewrite | 2-3 hours | Phase 1 |
| Phase 3: TODO Migration | 1 hour | Phase 1 |
| Phase 4: Validation | 1-2 hours | Phases 1-3 |
| Phase 5: Documentation | 1 hour | Phase 4 |

**Total Estimated Effort**: 7-10 hours

**Critical Path**: Phase 1 -> Phase 2 -> Phase 4

---

## Success Criteria

### Must Have (P0)

- [ ] CLAUDE.md reduced to 60-80 lines
- [ ] Session start tokens reduced by 65%+
- [ ] Worktracker fully functional via skill
- [ ] All existing workflows unchanged
- [ ] No broken references

### Should Have (P1)

- [ ] Documentation updated for contributors
- [ ] Migration guide for existing users
- [ ] Validation test suite created

### Nice to Have (P2)

- [ ] Automated token count monitoring
- [ ] Context utilization dashboard
- [ ] Progressive disclosure analytics

---

## References

### Internal Sources

- ADR-OSS-001: CLAUDE.md Decomposition Strategy
- ADR-OSS-003: Work Tracker Extraction Strategy
- ADR-OSS-004: Multi-Persona Documentation
- ps-researcher: claude-md-best-practices.md
- ps-researcher: decomposition-best-practices.md
- ps-analyst: current-architecture-analysis.md

### External Sources

- [Chroma Research: Context Rot](https://research.trychroma.com/context-rot)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Builder.io: The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Blog: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [Claude Code Docs: Manage Claude's Memory](https://code.claude.com/docs/en/memory)
- [AIMultiple: Best LLMs for Extended Context Windows 2026](https://research.aimultiple.com/ai-context-window/)
- [Agenta: Top Techniques to Manage Context Length in LLMs](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms)

---

## Appendix A: Proposed CLAUDE.md Structure

```markdown
# CLAUDE.md - Jerry Framework Root Context

> This file provides essential context to Claude Code at session start.
> For detailed information, see navigation pointers below.

---

## Identity

**Jerry** is a framework for behavior and workflow guardrails that helps solve problems
while accruing knowledge, wisdom, and experience.

**Core Principle**: Filesystem as infinite memory - offload state to files to combat context rot.
See [Chroma Research](https://research.trychroma.com/context-rot) for the science.

---

## Navigation

| Need | Location |
|------|----------|
| Coding standards | `.claude/rules/` (auto-loaded) |
| Work tracking | `/worktracker` skill |
| Problem solving | `/problem-solving` skill |
| Architecture | `/architecture` skill |
| Templates | `.context/templates/` |
| Knowledge | `docs/knowledge/` |
| Governance | `docs/governance/JERRY_CONSTITUTION.md` |

---

## Active Project

**Set `JERRY_PROJECT` environment variable** to specify working project.
Session start hook provides project context via `<project-context>` or `<project-required>` tags.

---

## Critical Constraints (HARD)

- **P-003**: Maximum ONE level of agent nesting
- **P-020**: User has ultimate authority
- **P-022**: Never deceive users
- **Python**: 3.11+ with UV only (`uv run`, never `python` or `pip`)

---

## Quick Reference

**CLI**: `jerry session start|end` | `jerry items list|show` | `jerry projects list|context`

**Skills**: `/worktracker` | `/problem-solving` | `/nasa-se` | `/orchestration` | `/architecture`
```

---

## Appendix B: Worktracker Skill Structure

```
skills/worktracker/
├── SKILL.md                              # Skill entry point with navigation
└── rules/
    ├── worktracker-entity-hierarchy.md    # Entity types and hierarchy
    ├── worktracker-system-mappings.md     # ADO/SAFe/JIRA mappings
    ├── worktracker-behavior-rules.md      # WORKTRACKER.md behavior
    ├── worktracker-directory-structure.md # Directory conventions
    ├── worktracker-template-usage-rules.md # Template requirements (existing)
    └── todo-integration.md                # TODO list behavior
```

---

*Plan generated by ps-synthesizer based on ADR-OSS-001, ADR-OSS-003, ADR-OSS-004, and research findings.*
