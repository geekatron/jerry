# Markdown Navigation Standards

> Navigation table requirements for all markdown files that Claude reads.
> This standard improves Claude's document comprehension and enables targeted reading.

## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Intention** | Why this standard exists | LLM comprehension benefits |
| **Strategy** | How to implement | Table formats and placement |
| **Requirements** | What must be included | Mandatory elements |
| **Examples** | Reference implementations | Jerry skill examples |
| **Validation** | How to verify compliance | Checklist |

**Related Standards**:
- [File Organization](file-organization.md) - Directory structure
- [Coding Standards](coding-standards.md) - Code style rules

**Decision Reference**: [FEAT-002:DEC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DEC-001-navigation-table-standard.md)

---

## Intention

### Why Navigation Tables Matter

Claude reads markdown files linearly, but understanding document structure upfront significantly improves comprehension. A navigation table immediately after frontmatter serves as a "document map" that:

1. **Provides Section Visibility** - Claude sees all sections at a glance
2. **Enables Targeted Reading** - Claude can focus on relevant sections
3. **Shows Relationships** - Table format reveals how concepts relate
4. **Supports Audience Targeting** - Triple-Lens tables guide detail level

### Industry Evidence

> "Markdown lets you structure content with nested lists, tables, and subheadings. This kind of **hierarchical structure is gold for LLMs** — it tells them how concepts relate to one another, what's a main idea, what's a subpoint, and what's a list of items to extract or reason over."
>
> — [Wetrocloud: Why Markdown is the Best Format for LLMs](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7)

> "Best practices include starting with a clear introduction about what the document covers, using consistent heading hierarchy to maintain logical structure, and **including a table of contents for long docs to enable easy navigation**."
>
> — [Markdown Documentation Standards - Claude Skills](https://claude-plugins.dev/skills/@ai-digital-architect/awesome-claude-code/markdown-standards)

---

## Strategy

### Placement

The navigation table MUST appear:
1. **After** the YAML frontmatter (if present)
2. **After** the title and metadata blockquote
3. **Before** the first content section

```markdown
---
name: example
description: ...
---

# Document Title

> **Version:** 1.0.0
> **Framework:** ...

---

## Document Sections        <-- Navigation table goes HERE

| Section | Purpose |
|---------|---------|
| ... | ... |

---

## First Content Section    <-- Content starts AFTER
```

### Table Formats

Choose the format appropriate for your document type:

#### Format 1: Section Index (General Documents)

Use for rule files, knowledge documents, and general markdown:

```markdown
## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Section Name** | What it covers | Summary of key content |
| **Another Section** | What it covers | Summary of key content |
```

#### Format 2: Triple-Lens Audience (Skills, Playbooks)

Use for documents serving multiple audience levels:

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | Purpose, When to Use, Quick Reference |
| **L1 (Engineer)** | Developers, implementers | Quick Start, Details, Examples |
| **L2 (Architect)** | Designers, reviewers | Patterns, Trade-offs, Compliance |
```

#### Format 3: Hybrid (Complex Documents)

Combine both for large, complex documents:

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0** | ... | ... |
| **L1** | ... | ... |
| **L2** | ... | ... |

## Document Sections

| Section | Purpose |
|---------|---------|
| ... | ... |
```

---

## Requirements

### Mandatory Elements

All Claude-consumed markdown files MUST include:

| Requirement | Description | Enforcement |
|-------------|-------------|-------------|
| **NAV-001** | Navigation table present | HARD |
| **NAV-002** | Table appears after frontmatter, before content | HARD |
| **NAV-003** | Table uses markdown table format | HARD |
| **NAV-004** | Each major section listed | MEDIUM |
| **NAV-005** | Purpose/description for each section | MEDIUM |

### File Types Covered

| File Type | Location | Table Format |
|-----------|----------|--------------|
| Skill files | `skills/*/SKILL.md` | Triple-Lens |
| Playbooks | `skills/*/PLAYBOOK.md` | Triple-Lens |
| Rule files | `.claude/rules/*.md` | Section Index |
| Agent files | `skills/*/agents/*.md` | Section Index |
| Worktracker templates | `.context/templates/worktracker/*.md` | Section Index |
| Knowledge docs | `docs/**/*.md` | Section Index or Triple-Lens |

### Exceptions

Navigation tables are NOT required for:
- Files under 30 lines
- Pure data files (YAML, JSON)
- Generated files (reports, logs)
- Temporary/scratch files

---

## Examples

### Example 1: Rule File (This Document)

```markdown
## Document Sections

| Section | Purpose | Key Information |
|---------|---------|-----------------|
| **Intention** | Why this standard exists | LLM comprehension benefits |
| **Strategy** | How to implement | Table formats and placement |
| **Requirements** | What must be included | Mandatory elements |
| **Examples** | Reference implementations | Jerry skill examples |
| **Validation** | How to verify compliance | Checklist |
```

### Example 2: Skill File (orchestration/SKILL.md)

```markdown
## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Project stakeholders, new users | Purpose, When to Use, Core Artifacts |
| **L1 (Engineer)** | Developers executing workflows | Quick Start, State Schema |
| **L2 (Architect)** | Workflow designers | Workflow Patterns, Constitutional Compliance |
```

### Example 3: Worktracker Template

```markdown
## Template Sections

| Section | Purpose | Required |
|---------|---------|----------|
| **Summary** | Brief description of work item | Yes |
| **Acceptance Criteria** | Definition of done | Yes |
| **Evidence** | Proof of completion | Yes |
| **Related Items** | Links to parent/children | Yes |
| **History** | Change log | Recommended |
```

---

## Validation

### Compliance Checklist

Before finalizing any Claude-consumed markdown file, verify:

- [ ] **NAV-001**: Navigation table is present
- [ ] **NAV-002**: Table appears after frontmatter, before first content section
- [ ] **NAV-003**: Table uses proper markdown table syntax
- [ ] **NAV-004**: All major sections (## headings) are listed
- [ ] **NAV-005**: Each entry has a purpose/description

### Automated Validation (Future)

Consider implementing:
- Pre-commit hook to check for navigation table presence
- CI validation for markdown structure
- Linting rule for table placement

---

## References

### Industry Sources

| Source | URL | Key Finding |
|--------|-----|-------------|
| Wetrocloud | [Medium Article](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7) | Hierarchical structure helps LLMs |
| Anthropic | [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | Break up information, reference files |
| Anthropic | [CLAUDE.md Guide](https://claude.com/blog/using-claude-md-files) | Structure aids comprehension |
| Claude Plugins | [Markdown Standards](https://claude-plugins.dev/skills/@ai-digital-architect/awesome-claude-code/markdown-standards) | Include TOC for navigation |

### Jerry Internal Sources

- [FEAT-002:DISC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) - Discovery
- [FEAT-002:DEC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DEC-001-navigation-table-standard.md) - Decision
- `skills/orchestration/SKILL.md` - Reference implementation
- `skills/problem-solving/SKILL.md` - Reference implementation

---

*Rule Version: 1.0.0*
*Created: 2026-02-01*
*Decision: FEAT-002:DEC-001*
