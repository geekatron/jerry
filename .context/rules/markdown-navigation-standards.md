# Markdown Navigation Standards

> Navigation table requirements for all markdown files that Claude reads.
> This standard improves Claude's document comprehension and enables targeted reading.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Intention](#intention) | Why this standard exists - LLM comprehension benefits |
| [Strategy](#strategy) | How to implement - Table formats, anchor links, placement |
| [Requirements](#requirements) | What must be included - Mandatory elements |
| [Examples](#examples) | Reference implementations - Jerry skill examples |
| [Validation](#validation) | How to verify compliance - Checklist |
| [References](#references) | Sources and citations |

**Related Standards**:
- [File Organization](file-organization.md) - Directory structure
- [Coding Standards](coding-standards.md) - Code style rules

**Decision Reference**: [FEAT-002:DEC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DEC-001-navigation-table-standard.md)

**Research**: [Navigation Table Research](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/EN-202-claude-md-rewrite/research-navigation-table-optimization.md)

---

## Intention

### Why Navigation Tables with Anchor Links Matter

Claude reads markdown files linearly, but understanding document structure upfront significantly improves comprehension. A navigation table with **anchor links** immediately after frontmatter serves as an active "document map" that:

1. **Enables Direct Navigation** - Claude can jump to specific sections via anchor links
2. **Provides Section Visibility** - Claude sees all sections at a glance
3. **Creates Knowledge Graph** - Table format reveals how concepts relate
4. **Supports Audience Targeting** - Triple-Lens tables guide detail level
5. **Improves Extractability** - LLMs can pinpoint specific information more efficiently

### Anthropic Official Guidance

> "For reference files that exceed 100 lines, it's important to include a table of contents at the top. This structure helps Claude understand the full scope of information available... **A table of contents allows Claude to efficiently navigate and jump to specific sections as required**, ensuring it can access the necessary details without reading the entire lengthy document."
>
> — [Claude Platform Documentation - Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### Industry Evidence

> "Anchor links enhance extractability, making it easier for LLMs to pinpoint and utilize specific information when generating responses. A table of contents provides LLMs with a clear overview of the document's structure and organization, helping them understand the semantic relationships between different sections."
>
> — [Geeky Tech: Anchor Links and ToC for LLM Skimming](https://www.geekytech.co.uk/anchor-links-and-table-of-contents-for-llm-skimming/)

> "Markdown is extremely close to plain text... Mainstream LLMs natively '_speak_' Markdown, and often incorporate Markdown into their responses unprompted."
>
> — [Microsoft MarkItDown](https://github.com/microsoft/markitdown)

---

## Strategy

### Placement

The navigation table MUST appear:
1. **After** the YAML frontmatter (if present)
2. **After** the title and metadata blockquote
3. **Before** the first content section

This satisfies the **"First-100-Words Rule"** - include key navigation in the first 100 words to aid extraction.

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
| [Summary](#summary) | What this document covers |
| [Details](#details) | Implementation specifics |

---

## Summary                  <-- Content starts AFTER
```

### Anchor Link Syntax

Section names MUST be anchor links following GitHub-flavored markdown rules:

| Rule | Description | Example |
|------|-------------|---------|
| Lowercase | Convert heading to lowercase | `Summary` → `summary` |
| Hyphens | Replace spaces with hyphens | `Problem Statement` → `problem-statement` |
| Remove special chars | Remove parentheses, colons, etc. | `Children (Tasks)` → `children-tasks` |

**Anchor Examples:**

| Heading | Anchor Link |
|---------|-------------|
| `## Summary` | `[Summary](#summary)` |
| `## Problem Statement` | `[Problem Statement](#problem-statement)` |
| `## Children (Tasks)` | `[Children (Tasks)](#children-tasks)` |
| `## Acceptance Criteria` | `[Acceptance Criteria](#acceptance-criteria)` |
| `## Related Items` | `[Related Items](#related-items)` |

### Table Formats

Choose the format appropriate for your document type:

#### Format 1: Section Index with Anchors (General Documents)

Use for rule files, enablers, features, and general markdown:

```markdown
## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this document covers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Cross-references and dependencies |
```

#### Format 2: Triple-Lens Audience with Anchors (Skills, Playbooks)

Use for documents serving multiple audience levels:

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections |
|-------|----------|----------|
| **L0 (ELI5)** | Stakeholders | [Purpose](#purpose), [When to Use](#when-to-use) |
| **L1 (Engineer)** | Developers | [Quick Start](#quick-start), [Examples](#examples) |
| **L2 (Architect)** | Designers | [Patterns](#patterns), [Trade-offs](#trade-offs) |
```

#### Format 3: Hybrid (Complex Documents)

Combine both for large, complex documents:

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections |
|-------|----------|----------|
| **L0** | ... | [Section](#section), ... |
| **L1** | ... | [Section](#section), ... |
| **L2** | ... | [Section](#section), ... |

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section Name](#section-name) | What it covers |
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
| **NAV-004** | Each major section (## heading) listed | MEDIUM |
| **NAV-005** | Purpose/description for each section | MEDIUM |
| **NAV-006** | Section names use anchor links `[Name](#anchor)` | **HARD** |

### File Types Covered

| File Type | Location | Table Format |
|-----------|----------|--------------|
| Skill files | `skills/*/SKILL.md` | Triple-Lens with anchors |
| Playbooks | `skills/*/PLAYBOOK.md` | Triple-Lens with anchors |
| Rule files | `.claude/rules/*.md` | Section Index with anchors |
| Agent files | `skills/*/agents/*.md` | Section Index with anchors |
| Worktracker entities | `projects/**/EN-*.md`, `FEAT-*.md` | Section Index with anchors |
| Worktracker templates | `.context/templates/worktracker/*.md` | Section Index with anchors |
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

| Section | Purpose |
|---------|---------|
| [Intention](#intention) | Why this standard exists |
| [Strategy](#strategy) | How to implement |
| [Requirements](#requirements) | What must be included |
| [Examples](#examples) | Reference implementations |
| [Validation](#validation) | How to verify compliance |
```

### Example 2: Enabler File

```markdown
## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [Children (Tasks)](#children-tasks) | Task breakdown with dependencies |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done checklist |
| [Related Items](#related-items) | Bugs, discoveries, decisions |
```

### Example 3: Skill File (orchestration/SKILL.md)

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections |
|-------|----------|----------|
| **L0 (ELI5)** | Stakeholders | [Purpose](#purpose), [When to Use](#when-to-use) |
| **L1 (Engineer)** | Developers | [Quick Start](#quick-start), [State Schema](#state-schema) |
| **L2 (Architect)** | Designers | [Workflow Patterns](#workflow-patterns), [Compliance](#constitutional-compliance) |
```

### Example 4: Worktracker Template

```markdown
## Template Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of work item |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Proof of completion |
| [Related Items](#related-items) | Links to parent/children |
| [History](#history) | Change log |
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
- [ ] **NAV-006**: Section names are anchor links (`[Name](#anchor)`)

### Anchor Link Verification

Test that anchors resolve correctly:
1. Click each anchor link in preview mode
2. Verify it jumps to the correct section
3. Check anchor follows naming rules (lowercase, hyphens, no special chars)

### Automated Validation (Future)

Consider implementing:
- Pre-commit hook to check for navigation table presence
- CI validation for anchor link format
- Linting rule for table placement and structure

---

## References

### Primary Sources (Authoritative)

| Source | URL | Key Finding |
|--------|-----|-------------|
| Claude Platform Docs | [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | ToC allows Claude to "jump to specific sections" |
| Claude Platform Docs | [Long Context Tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips) | Structure with tags, quote-first pattern |
| Anthropic Courses | [GitHub](https://github.com/anthropics/courses) | XML tags for structure |
| Microsoft MarkItDown | [GitHub](https://github.com/microsoft/markitdown) | LLMs natively "speak" Markdown |

### Secondary Sources (Industry)

| Source | URL | Key Finding |
|--------|-----|-------------|
| Geeky Tech | [LLM Skimming](https://www.geekytech.co.uk/anchor-links-and-table-of-contents-for-llm-skimming/) | Anchor links enhance extractability |
| ZC Marketing | [LLM Internal Linking 2025](https://zcmarketing.au/seo-tips/llm-internal-linking-2025/) | First-100-words rule, heading hierarchy |
| Wetrocloud | [Medium Article](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7) | Hierarchical structure helps LLMs |
| llmstxt.org | [Standard](https://llmstxt.org/) | /llms.txt proposal |

### Jerry Internal Sources

| Type | Path | Description |
|------|------|-------------|
| Research | [Navigation Table Research](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/EN-202-claude-md-rewrite/research-navigation-table-optimization.md) | Full research document |
| Discovery | [FEAT-002:DISC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DISC-001-navigation-tables-for-llm-comprehension.md) | Initial findings |
| Decision | [FEAT-002:DEC-001](../../projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002--DEC-001-navigation-table-standard.md) | Standard adoption |

---

*Rule Version: 2.0.0*
*Created: 2026-02-01*
*Updated: 2026-02-01 (v2.0 - Added anchor link requirement NAV-006)*
*Decision: FEAT-002:DEC-001*
