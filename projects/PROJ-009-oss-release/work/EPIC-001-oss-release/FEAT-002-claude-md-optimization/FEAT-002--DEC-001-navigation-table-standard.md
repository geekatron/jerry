# FEAT-002:DEC-001: Navigation Tables Required in Claude-Consumed Markdown

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-01 (FEAT-002 optimization work)
PURPOSE: Establish standard for navigation tables in markdown files
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** high
> **Created:** 2026-02-01T17:00:00Z
> **Parent:** FEAT-002
> **Owner:** User + Claude
> **Related:** DISC-001, EN-202

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of 2 decisions |
| [Decision Context](#decision-context) | Background, constraints, stakeholders |
| [Decisions](#decisions) | D-001 and D-002 detailed decisions |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Affected Files](#affected-files) | What needs updating |
| [Related Artifacts](#related-artifacts) | Cross-references and industry sources |
| [Document History](#document-history) | Change log |

---

## Summary

All markdown files that Claude reads MUST include a navigation table immediately after the frontmatter. This improves Claude's comprehension of document structure and enables targeted reading.

**Decisions Captured:** 2

**Key Outcomes:**
- New rule file created: `.claude/rules/markdown-navigation-standards.md`
- Worktracker templates updated with navigation table requirement
- All existing Claude-consumed files will be updated

---

## Decision Context

### Background

During EN-201 Worktracker Skill Extraction, it was discovered that the extracted rule files lacked navigation tables, even though Jerry skill files consistently include "Document Audience (Triple-Lens)" tables. Industry research confirms that hierarchical structure and navigation aids significantly improve LLM document comprehension.

### Constraints

- Must not significantly increase file size
- Must be easy to maintain
- Must provide genuine value to Claude
- Must be consistent across all file types

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Decision Maker | Consistent, high-quality documentation |
| Claude | Consumer | Better document comprehension |
| Contributors | Authors | Clear standard to follow |

---

## Decisions

### D-001: Navigation Tables Are Mandatory for Claude-Consumed Markdown

**Date:** 2026-02-01T17:00:00Z
**Participants:** User, Claude

#### Question/Context

Should all markdown files that Claude reads include navigation tables, and if so, what should they contain?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | No standard - optional | Flexibility | Inconsistent comprehension |
| **B** | Navigation tables required | Better comprehension, consistent | More boilerplate |
| **C** | Only for large files (>100 lines) | Targeted improvement | Arbitrary threshold |

#### Decision

**We decided:** Option B - Navigation tables are REQUIRED for all markdown files that Claude reads.

#### Rationale

1. **Industry Evidence:** Multiple sources confirm hierarchical structure helps LLMs
2. **Existing Pattern:** Jerry skills already implement this successfully
3. **Consistency:** Same pattern everywhere reduces cognitive load
4. **Marginal Cost:** ~10-15 lines per file is minimal overhead

#### Implications

- **Positive:** Improved Claude comprehension, consistent documentation
- **Negative:** Slightly more boilerplate per file
- **Follow-up required:** Update existing files, create rule, update templates

---

### D-002: Navigation Table Structure and Placement

**Date:** 2026-02-01T17:00:00Z
**Participants:** User, Claude

#### Question/Context

Where should the navigation table appear and what should it contain?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | After frontmatter, before content | Early visibility | None identified |
| **B** | At end of document | Doesn't interrupt flow | Claude may not see it |
| **C** | In HTML comment | Hidden from humans | Defeats purpose |

#### Decision

**We decided:** Option A - Navigation table appears immediately after frontmatter/header, before main content.

**Table Structure:**

```markdown
## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Section Name** | What it covers | Summary of content |
```

OR for audience-aware documents (Triple-Lens):

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Description | Sections |
| **L1 (Engineer)** | Description | Sections |
| **L2 (Architect)** | Description | Sections |
```

#### Rationale

1. **Early Position:** Claude reads documents top-to-bottom; early placement ensures visibility
2. **Table Format:** Tables are highly parseable by LLMs (per industry research)
3. **Flexibility:** Both simple section index and Triple-Lens formats are acceptable

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Navigation tables required for all Claude-consumed markdown | 2026-02-01 | ACCEPTED |
| D-002 | Tables placed after frontmatter, use section or Triple-Lens format | 2026-02-01 | ACCEPTED |

---

## Affected Files

### Must Be Updated

| Category | Location | Count |
|----------|----------|-------|
| Rule files | `.claude/rules/*.md` | ~8 |
| Worktracker rules | `skills/worktracker/rules/*.md` | 5 |
| Worktracker templates | `.context/templates/worktracker/*.md` | 10 |

### Already Compliant

| Category | Location | Count |
|----------|----------|-------|
| Skill files | `skills/*/SKILL.md` | ~5 |
| Playbooks | `skills/*/PLAYBOOK.md` | ~4 |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-claude-md-optimization.md) | Parent feature |
| Discovery | [DISC-001](./FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) | Research findings |
| Rule | `.claude/rules/markdown-navigation-standards.md` | Enforcement rule |
| Task | EN-202/TASK-000 | Update worktracker files |

### Industry Sources

| Source | URL | Key Finding |
|--------|-----|-------------|
| Wetrocloud | [Medium Article](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7) | "Hierarchical structure is gold for LLMs" |
| Anthropic | [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | Break up information, reference files |
| Anthropic | [CLAUDE.md Guide](https://claude.com/blog/using-claude-md-files) | Document structure aids comprehension |
| Claude Plugins | [Markdown Standards](https://claude-plugins.dev/skills/@ai-digital-architect/awesome-claude-code/markdown-standards) | Include TOC for navigation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-01T17:00:00Z | Claude | Created decision document |

---

## Metadata

```yaml
id: "FEAT-002:DEC-001"
parent_id: "FEAT-002"
work_type: DECISION
title: "Navigation Tables Required in Claude-Consumed Markdown"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-01T17:00:00Z"
updated_at: "2026-02-01T17:00:00Z"
decided_at: "2026-02-01T17:00:00Z"
participants: [User, Claude]
tags: [markdown, navigation, standard, llm]
decision_count: 2
superseded_by: null
supersedes: null
```
