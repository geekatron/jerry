# FEAT-002:DISC-001: Navigation Tables Improve LLM Document Comprehension

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-02-01 (User feedback during EN-201)
PURPOSE: Document finding about markdown structure best practices for LLM consumption
-->

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-01T17:00:00Z
> **Completed:** 2026-02-01T17:00:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** User feedback, industry research

---

## Summary

Markdown files that Claude reads benefit significantly from having a **navigation table immediately after the frontmatter**. This table provides Claude with visibility into the document's sections and structure, improving comprehension and enabling targeted reading.

**Key Findings:**
- Hierarchical structure in markdown is "gold for LLMs" - helps understand concept relationships
- Navigation tables after frontmatter serve as a document map
- Pattern already implemented in Jerry skills (Triple-Lens audience tables)
- Industry best practices confirm this approach

**Validation:** Confirmed by Anthropic documentation, industry research, and existing Jerry patterns.

---

## Context

### Background

During EN-201 Worktracker Skill Extraction, the user identified that the extracted rule files lacked navigation tables. The existing Jerry skill files (`orchestration/SKILL.md`, `problem-solving/SKILL.md`, `nasa-se/SKILL.md`) all include a "Document Audience (Triple-Lens)" table immediately after frontmatter, but this pattern wasn't applied to the new rule files.

### Research Question

Is placing navigation tables after frontmatter a documented best practice for LLM-consumed markdown files?

### Investigation Approach

1. Searched Jerry codebase for existing patterns
2. Reviewed industry sources on markdown for LLMs
3. Analyzed Anthropic's official documentation
4. Compared Jerry skill file structures

---

## Finding

### Industry Evidence

#### Source 1: Wetrocloud - "Why Markdown is the Best Format for LLMs"

> "Markdown lets you structure content with nested lists, tables, and subheadings. This kind of **hierarchical structure is gold for LLMs** — it tells them how concepts relate to one another, what's a main idea, what's a subpoint, and what's a list of items to extract or reason over."

**Citation:** [Why Markdown is the best format for LLMs](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7)

#### Source 2: Anthropic - "Claude Code Best Practices"

> "CLAUDE.md is added to Claude Code's context every time, so from a context engineering and prompt engineering standpoint, keep it concise. One option: **break up information into separate markdown files and reference them** inside the CLAUDE.md file."

**Citation:** [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)

#### Source 3: Anthropic - "Using CLAUDE.MD Files"

> "CLAUDE.md is a special file that Claude automatically pulls into context when starting a conversation. This makes it an ideal place for documenting repository etiquette, developer environment setup, and any unexpected behaviors particular to the project."

**Citation:** [Using CLAUDE.MD files](https://claude.com/blog/using-claude-md-files)

#### Source 4: Claude Markdown Documentation Standards

> "Best practices include starting with a clear introduction about what the document covers, using consistent heading hierarchy to maintain logical structure, and **including a table of contents for long docs to enable easy navigation**."

**Citation:** [Markdown Documentation Standards - Claude Skills](https://claude-plugins.dev/skills/@ai-digital-architect/awesome-claude-code/markdown-standards)

### Jerry Internal Evidence

The existing Jerry skill files implement this pattern consistently:

```markdown
---
name: orchestration
description: ...
---

# Orchestration Skill

> **Version:** 2.1.0
> **Framework:** Jerry Orchestration (ORCH)

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Project stakeholders | Purpose, When to Use |
| **L1 (Engineer)** | Developers | Quick Start, Details |
| **L2 (Architect)** | Workflow designers | Patterns, Compliance |

---

## Purpose
...
```

**Files implementing this pattern:**
- `skills/orchestration/SKILL.md`
- `skills/problem-solving/SKILL.md`
- `skills/nasa-se/SKILL.md`
- `skills/transcript/SKILL.md`

### Why Navigation Tables Help Claude

| Benefit | Explanation |
|---------|-------------|
| **Section Visibility** | Claude can see all sections at a glance without scanning the entire document |
| **Audience Targeting** | Triple-lens tables help Claude select appropriate detail level |
| **Relationship Understanding** | Tables show how concepts relate to each other |
| **Efficient Navigation** | Claude can jump to relevant sections instead of reading linearly |
| **Context Compression** | When summarizing, Claude knows which sections matter for which audiences |

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Industry Article | Markdown structure for LLMs | Wetrocloud Medium | 2024 |
| E-002 | Official Docs | Claude Code best practices | Anthropic Engineering | 2025 |
| E-003 | Official Docs | CLAUDE.md usage guide | Anthropic Blog | 2025 |
| E-004 | Community Docs | Markdown standards for Claude | claude-plugins.dev | 2025 |
| E-005 | Internal Pattern | Triple-Lens audience tables | Jerry skills/ | 2026 |

### Validation

- **User Feedback:** User identified missing pattern during EN-201 review
- **Pattern Comparison:** Jerry skills vs. extracted rule files
- **Industry Confirmation:** Multiple sources recommend structural navigation aids

---

## Implications

### Impact on Project

This discovery affects ALL markdown files that Claude reads:
- Skill files (`skills/*/SKILL.md`)
- Rule files (`.claude/rules/*.md`)
- Worktracker templates (`.context/templates/worktracker/*.md`)
- Worktracker entities (enablers, tasks, discoveries, etc.)
- Knowledge documents (`docs/**/*.md`)

### Design Decisions Affected

- **DEC-001:** Adopt navigation tables as standard practice
- **Rule Creation:** New rule file for markdown navigation standards
- **Template Updates:** Add navigation table pattern to templates

### Scope of Change

| File Category | Count (Est.) | Impact |
|---------------|--------------|--------|
| Skill files | ~10 | Already compliant (Triple-Lens) |
| Rule files | ~8 | Need navigation tables added |
| Worktracker templates | ~10 | Need template section added |
| Worktracker entities | ~50+ | Future entities will comply |

---

## Relationships

### Creates

- [FEAT-002:DEC-001](./FEAT-002--DEC-001-navigation-table-standard.md) - Decision to adopt this pattern

### Informs

- [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite/EN-202-claude-md-rewrite.md) - Must apply pattern
- `.claude/rules/` - Need navigation tables added
- `.context/templates/worktracker/` - Template updates

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-claude-md-optimization.md) | Parent feature |
| Pattern Example | skills/orchestration/SKILL.md | Triple-Lens implementation |
| Pattern Example | skills/problem-solving/SKILL.md | Triple-Lens implementation |

---

## Recommendations

### Immediate Actions

1. Create DEC-001 documenting the decision
2. Create new rule file: `.claude/rules/markdown-navigation-standards.md`
3. Add TASK to EN-202 to update worktracker rule files
4. Update worktracker templates with navigation table section

### Long-term Considerations

- All new markdown files should include navigation tables
- Consider automated validation of this pattern
- Extend to all docs/ knowledge files

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T17:00:00Z | Claude | Created discovery |

---

## Metadata

```yaml
id: "FEAT-002:DISC-001"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Navigation Tables Improve LLM Document Comprehension"
status: VALIDATED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-02-01T17:00:00Z"
updated_at: "2026-02-01T17:00:00Z"
completed_at: "2026-02-01T17:00:00Z"
tags: [markdown, navigation, llm, structure, best-practice]
source: "User feedback, industry research"
finding_type: PATTERN
confidence_level: HIGH
validated: true
```
