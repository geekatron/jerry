# PAT-SKILL-001: Jerry Skill Structure

> Canonical structure for Jerry framework skills. Combines Anthropic's universal skill requirements with Jerry-specific conventions.
> **SSOT:** Rules H-25 through H-30 are defined in `.context/rules/skill-standards.md` v1.1.0. This pattern MUST be updated when skill-standards.md changes.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pattern Summary](#pattern-summary) | ID, status, source |
| [Structure](#structure) | Directory layout |
| [SKILL.md Template](#skillmd-template-jerry) | Frontmatter + body template |
| [Key Rules](#key-rules) | HARD rule summary |
| [Workflow Patterns](#workflow-patterns) | Five proven patterns |
| [Anti-Patterns](#anti-patterns) | What to avoid |
| [References](#references) | Source documents |

## Pattern Summary

| Attribute | Value |
|-----------|-------|
| **ID** | PAT-SKILL-001 |
| **Name** | Jerry Skill Structure |
| **Status** | MANDATORY |
| **Category** | Skill Development |
| **Source** | Anthropic Skill Guide + Jerry Framework Conventions |
| **SSOT Version** | skill-standards.md v1.1.0 |

## Structure

```
skills/your-skill-name/
├── SKILL.md              # Required — main skill file
├── agents/               # Required (if multi-agent)
│   ├── agent-one.md     # Agent definition
│   └── agent-two.md     # Agent definition
├── references/           # Optional — loaded on demand
│   ├── ref-one.md       # Reference document
│   └── ref-two.md       # Reference document
├── scripts/              # Optional — executable code
└── assets/               # Optional — templates, etc.
```

## SKILL.md Template (Jerry)

```yaml
---
name: skill-name
description: >-
  What it does. When to use it — specific trigger phrases.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep
activation-keywords:
  - "keyword one"
  - "keyword two"
---
```

```markdown
# Skill Name

> **Version:** X.Y.Z
> **Framework:** Jerry [Domain] ([Abbreviation])
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What the skill does |
| [When to Use This Skill](#when-to-use-this-skill) | Activation and anti-patterns |
| [Available Agents](#available-agents) | Agent registry |
| [Quick Reference](#quick-reference) | Common workflows |
| [References](#references) | Source documents |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0** | Stakeholders | Purpose, When to Use, Quick Reference |
| **L1** | Engineers | Available Agents, Invoking an Agent |
| **L2** | Architects | P-003 Compliance, Integration Points |

## Purpose
[What + Key Capabilities]

## When to Use This Skill
Activate when: [triggers]
Do NOT use when: [anti-patterns]

## Available Agents
| Agent | Role | Model | Output Location |

## P-003 Compliance
[Hierarchy diagram: MAIN CONTEXT → workers]

## Invoking an Agent
### Option 1: Natural Language Request
### Option 2: Explicit Agent Request
### Option 3: Task Tool Invocation

## [Domain-Specific Sections]

## Integration Points

## Constitutional Compliance
| Principle | Requirement |

## Quick Reference
### Common Workflows
### Agent Selection Hints

## References
| Source | Content |
(Full repo-relative paths)

*Skill Version: X.Y.Z*
*Constitutional Compliance: Jerry Constitution v1.0*
```

## Key Rules
- Folder: kebab-case, matches `name` field
- SKILL.md: exact case-sensitive naming
- No README.md inside skill folder
- Document Sections navigation table REQUIRED (H-23/NAV-001) with anchor links (H-24)
- All file references: full repo-relative paths
- SKILL.md under 5,000 words (~6,500 tokens — SHOULD per MEDIUM tier)
- References loaded on demand (Level 3 progressive disclosure)
- Agents are workers (P-003), max 1 level deep
- `.context/` is Claude-agnostic; `.claude/rules/` symlinks to `.context/rules/` for auto-loading

## Workflow Patterns

Five proven patterns from Anthropic's guide:

| ID | Pattern | When to Use | Key Techniques |
|----|---------|-------------|----------------|
| PAT-SKILL-WF-001 | Sequential Orchestration | Multi-step processes in specific order | Explicit ordering, dependencies, validation per stage, rollback |
| PAT-SKILL-WF-002 | Multi-Source Coordination | Workflows spanning multiple services | Phase separation, data passing, cross-phase validation |
| PAT-SKILL-WF-003 | Iterative Refinement | Output quality improves with iteration | Quality criteria, validation scripts, refinement loops, stop conditions |
| PAT-SKILL-WF-004 | Context-Aware Selection | Same outcome, different tools by context | Decision trees, fallbacks, transparency |
| PAT-SKILL-WF-005 | Domain-Specific Intelligence | Specialized knowledge beyond tool access | Embedded expertise, compliance-before-action, audit trails |

## Anti-Patterns
- Monolithic SKILL.md with everything inline (violates progressive disclosure)
- Relative file paths in SKILL.md (ambiguous when loaded from different CWDs)
- README.md inside skill folder (conflicts with SKILL.md)
- Generic description without trigger phrases (skill won't activate)
- Assuming skill is the only capability loaded (violates composability)

## Related Patterns
- PAT-ARCH-001: Hexagonal Architecture (skills are a form of ports/adapters)
- Testing patterns (PAT-TEST-001 to PAT-TEST-003) apply to skill testing

## References
| Source | Content |
|--------|---------|
| `.context/rules/skill-standards.md` | HARD rules for skill development |
| `.context/guides/skill-development.md` | Educational guide with examples |
| `docs/knowledge/anthropic-skill-development-guide.pdf` | Anthropic's official guide |
| `skills/adversary/SKILL.md` | Reference implementation |
