# TD-017-E-006: Claude Code Rules and Patterns Best Practices

> **Research Entry:** td-017-e-006
> **Topic:** Claude Code Configuration Best Practices
> **Date:** 2026-01-11
> **Researcher:** ps-researcher agent

---

## L0: Executive Summary (ELI5)

This research investigates how to best organize Claude Code configuration files - the `.claude/` folder, rules, patterns, and CLAUDE.md files. Think of these as "instruction manuals" that Claude reads before helping with your code.

**Key Findings:**

1. **Less is More:** Anthropic recommends keeping instructions concise - around 100-200 lines maximum in CLAUDE.md. Claude can only reliably follow ~150-200 instructions consistently. Jerry's current setup (4 rules files totaling ~600+ lines) may be too verbose.

2. **Progressive Disclosure is Critical:** Don't front-load all information. Instead, use pointers to files that Claude can read when needed. Jerry already does this well with the Pattern Catalog approach.

3. **Industry Standard Structures Exist:** The `.claude/rules/` directory with path-scoped rules, subagent definitions in `.claude/agents/`, and skills in `skills/` are now industry standards (Claude Code v2.0.64+).

4. **Jerry is Ahead of the Curve:** Jerry's structure (rules, agents, skills, pattern catalog) aligns well with Anthropic's latest recommendations. Minor refinements could improve instruction following.

**Impact on Jerry:** The current structure is sound. The main optimization opportunity is reducing verbosity in rules files and ensuring CLAUDE.md serves as a "table of contents" rather than a comprehensive manual.

---

## L1: Technical Analysis (Software Engineer)

### 1. Industry Examples of .claude/ Structures

Based on web research of open-source projects and Anthropic documentation:

#### Standard Directory Layout (Anthropic Recommended)

```
project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions (or ../CLAUDE.md)
│   ├── settings.json       # User/project settings
│   ├── settings.local.json # Local overrides (gitignored)
│   ├── rules/              # Modular rule files (v2.0.64+)
│   │   ├── code-style.md
│   │   ├── testing.md
│   │   ├── security.md
│   │   └── frontend/       # Subdirectories allowed
│   │       └── react.md
│   ├── agents/             # Subagent definitions
│   │   └── code-reviewer.md
│   ├── commands/           # Custom slash commands
│   │   └── todo.md
│   └── skills/             # OR skills at project root
│       └── my-skill/
│           └── SKILL.md
├── skills/                 # Alternative: skills at root
│   └── worktracker/
│       └── SKILL.md
└── CLAUDE.md               # Root-level instructions
```

**Source:** [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)

#### Memory Type Hierarchy

| Memory Type | Location | Priority | Shared With |
|-------------|----------|----------|-------------|
| Enterprise policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Highest | Org |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | High | Team |
| Project rules | `./.claude/rules/*.md` | High | Team |
| User memory | `~/.claude/CLAUDE.md` | Medium | Just you |
| Local project | `./CLAUDE.local.md` | Medium | Just you |

**Source:** [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)

### 2. Rules Organization Patterns

#### Pattern A: Path-Scoped Rules (Recommended)

Rules can be scoped to specific files using YAML frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

**When to use:** When rules apply only to specific file types or directories.

**Source:** [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)

#### Pattern B: Topic-Based Organization

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

**When to use:** Large monorepos with distinct codebases.

#### Pattern C: Symlinked Shared Rules

```bash
# Share rules across multiple projects
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

**When to use:** Enterprise environments with standardized rules.

**Source:** [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)

### 3. Pattern Documentation Formats

#### Anthropic Skill Format (SKILL.md)

The official pattern for documenting reusable knowledge:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files. Use when working with PDFs.
---

# PDF Processing

## Quick start

[Minimal working example]

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
```

**Key principles:**
- Frontmatter with `name` (64 chars max, lowercase with hyphens) and `description` (1024 chars max)
- Body under 500 lines for optimal performance
- Use progressive disclosure - reference files loaded on-demand
- One level deep references only (no nested reference chains)

**Source:** [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

#### Table of Contents Pattern for Large Reference Files

For files over 100 lines:

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features
- Error handling patterns
- Code examples

## Authentication and setup
...
```

**Rationale:** Claude may use partial reads (e.g., `head -100`) on nested references. A ToC ensures Claude sees the full scope.

**Source:** [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### 4. CLAUDE.md Best Practices

#### Instruction Limit Research

> "Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency."
> - Multiple industry sources

**Source:** [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices), [HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

#### What to Include

**DO Include:**
- Project structure map (what's where)
- Build/test/run commands
- Stack/technology context
- Verification commands
- Repository etiquette (branch naming, merge vs rebase)
- Unexpected behaviors or warnings

**DO NOT Include:**
- Detailed code style rules (use linters instead)
- Full code snippets (become outdated - use file:line references)
- Every possible command
- Explanations Claude already knows

**Source:** [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

#### Progressive Disclosure Pattern

```markdown
# Project Context

## About This Project
FastAPI REST API for user authentication.

## Key Directories
- `app/models/` - database models
- `app/api/` - route handlers
- `app/core/` - configuration and utilities

## Standards
See @.claude/rules/coding-standards.md for details.

## Testing
See @docs/testing/README.md for test conventions.
```

**The `@path` Import Syntax:**
CLAUDE.md supports `@path/to/file` to import content. Recursive imports supported (max depth 5).

**Source:** [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)

### 5. Subagent Definition Format

Subagents use Markdown with YAML frontmatter:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

**Available Fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Identifier for the subagent |
| `description` | Yes | When to invoke (Claude uses this to decide) |
| `tools` | No | Whitelist tools (inherits all if omitted) |
| `model` | No | Which model to use (sonnet, haiku, opus) |
| `hooks` | No | Subagent-specific hooks |

**Source:** [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents), [Shipyard Blog](https://shipyard.build/blog/claude-code-subagents-guide/)

---

## L2: Architectural Implications (Principal Architect)

### Jerry-Specific Analysis

#### Current State Assessment

| Component | Jerry Has | Industry Standard | Gap |
|-----------|-----------|-------------------|-----|
| Root CLAUDE.md | Yes (detailed) | Concise pointer | Medium gap |
| .claude/rules/ | 4 files (~600+ lines) | <200 lines total | Large gap |
| Pattern Catalog | Yes (progressive) | Skill-like format | Aligned |
| Agent Definitions | Yes (template) | YAML frontmatter | Aligned |
| Skills | Yes (worktracker) | SKILL.md format | Aligned |

#### Strengths of Jerry's Approach

1. **Progressive Disclosure Already Implemented**
   - Pattern Catalog serves as reference, not loaded upfront
   - Rules are modular in separate files
   - Skills have proper SKILL.md structure

2. **Strong Governance Framework**
   - Jerry Constitution provides principle-based guidance
   - Agent templates ensure consistency
   - Behavior tests validate compliance

3. **Project Isolation**
   - Per-project PLAN.md and WORKTRACKER.md
   - Environment variable enforcement
   - Clear project boundaries

#### Identified Gaps

1. **CLAUDE.md Verbosity**
   - Current root CLAUDE.md is extensive (~400+ lines)
   - Contains implementation details that could be referenced
   - WIF implementation status block is project-specific

2. **Rules File Density**
   - coding-standards.md: ~200 lines
   - architecture-standards.md: ~200 lines
   - file-organization.md: ~200 lines
   - testing-standards.md: ~200 lines
   - Total: ~800 lines (4x recommended limit)

3. **Missing Path Scoping**
   - Rules apply globally when some could be path-scoped
   - Example: testing-standards could scope to `tests/**/*.py`

### Recommendations

#### R1: Restructure CLAUDE.md as Index (HIGH PRIORITY)

```markdown
# CLAUDE.md - Jerry Framework Root Context

> Procedural memory - loaded at session start.

## What is Jerry?
[2-3 sentences only]

## Quick Reference
- **Current Project:** Set `JERRY_PROJECT` env var
- **Build:** `pytest tests/`
- **Verify:** `python scripts/session_start.py`

## Where to Find Information
- Architecture: @.claude/rules/architecture-standards.md
- Coding: @.claude/rules/coding-standards.md
- Patterns: @.claude/patterns/PATTERN-CATALOG.md
- Governance: @docs/governance/JERRY_CONSTITUTION.md

## Project Context
[Short description, not WIF implementation details]
```

**Rationale:** Use `@path` imports to load details on-demand.

#### R2: Add Path Scoping to Rules (MEDIUM PRIORITY)

```markdown
---
paths:
  - "tests/**/*.py"
  - "tests/**/*.feature"
---

# Testing Standards
...
```

**Impact:** Rules only apply when Claude works on matching files.

#### R3: Convert Pattern Catalog to Skill Format (LOW PRIORITY)

The Pattern Catalog already follows progressive disclosure principles. Converting to SKILL.md format would:
- Add discoverable frontmatter
- Enable activation via `/skill` command
- Align with Anthropic's skill ecosystem

#### R4: Leverage CLAUDE.local.md for Session State (MEDIUM PRIORITY)

Move session-specific content (like WIF implementation status) to:
- Project-specific CLAUDE.md: `projects/PROJ-001-plugin-cleanup/CLAUDE.md`
- Or gitignored: `CLAUDE.local.md`

### Trade-Off Analysis

| Recommendation | Effort | Risk | Benefit |
|----------------|--------|------|---------|
| R1: Restructure CLAUDE.md | Low | Low | High (better instruction following) |
| R2: Path scoping | Medium | Low | Medium (targeted rules) |
| R3: Skill format | High | Low | Low (already functional) |
| R4: Session state | Low | None | Medium (cleaner context) |

### Alignment with Existing Architecture

The recommendations align with Jerry's core principles:
- **P-002 (File Persistence):** Using `@path` imports maintains filesystem as memory
- **P-004 (Explicit Provenance):** Pattern Catalog references Design Canon
- **P-011 (Evidence-Based):** Research-backed recommendations

---

## Research Methodology

### Sources Consulted

1. **Official Anthropic Documentation**
   - [Claude Code Memory Documentation](https://code.claude.com/docs/en/memory)
   - [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
   - [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
   - [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)

2. **Community Resources**
   - [Using CLAUDE.MD Files](https://claude.com/blog/using-claude-md-files)
   - [HumanLayer - Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
   - [Shipyard - Claude Code Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)
   - [Shipyard - Subagents Guide](https://shipyard.build/blog/claude-code-subagents-guide/)

3. **GitHub Projects**
   - [anthropics/skills](https://github.com/anthropics/skills) - Official skill examples
   - [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Community patterns
   - [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ subagent examples

4. **LLM Instruction Research**
   - [Markdown for LLMs](https://medium.com/@wetrocloud/why-markdown-is-the-best-format-for-llms-aa0514a409a7)
   - [llms.txt Standard](https://llmstxt.org/)

### Search Queries Executed
- "Claude Code CLI .claude rules folder structure best practices 2025"
- "Claude Code CLAUDE.md project context file examples best practices"
- "Anthropic Claude Code configuration rules patterns documentation"
- "GitHub .claude folder examples open source projects 2025"
- "Claude Code skills directory structure examples templates"
- "LLM instruction following documentation format patterns markdown"
- "claude code agent subagent markdown definition specification"

---

## Appendix: Key Quotes

> "The sweet spot is 100-200 lines maximum [for CLAUDE.md]."
> - [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

> "Context window is a public good. Your Skill shares the context window with everything else Claude needs to know."
> - [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

> "Default assumption: Claude is already very smart. Only add context Claude doesn't already have."
> - [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

> "Avoid deeply nested references. Keep references one level deep from SKILL.md."
> - [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

---

*Document Version: 1.0*
*Research Date: 2026-01-11*
*Constitutional Compliance: P-001, P-002, P-004, P-011*
