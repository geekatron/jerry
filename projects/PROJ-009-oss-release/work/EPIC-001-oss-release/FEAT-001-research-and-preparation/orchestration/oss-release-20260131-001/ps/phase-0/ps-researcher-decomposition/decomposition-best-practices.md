# Decomposition with Imports: Best Practices Research

> **PS ID:** PROJ-009-oss-release
> **Entry ID:** EN-006
> **Agent:** ps-researcher (Research Specialist)
> **Topic:** Decomposition with Imports Research
> **Workflow:** oss-release-20260131-001
> **Phase:** 0 (Divergent Exploration)
> **Created:** 2026-01-31
> **Status:** Complete

---

## L0: Executive Summary (ELI5)

### The Problem: Information Overload for AI

Imagine you have a brilliant assistant who can read thousands of pages of documentation. The problem? The more you give them to read at once, the worse they perform. It's like trying to find your keys in a room full of boxes - more boxes means more confusion.

This is called **"context rot"** - when too much information actually makes the AI less effective, even when it technically has room to hold it all.

### The Solution: Smart Organization

Instead of one giant instruction manual:

1. **Break it into chapters** - Decompose large files into logical sections
2. **Create a table of contents** - Use index/manifest files for navigation
3. **Load only what's needed** - Like checking out library books instead of buying the whole library
4. **Use references** - Point to information instead of copying it everywhere

### Key Insight

> "Claude is already smart enough - intelligence is not the bottleneck, context is."
> -- Anthropic AWS re:Invent 2025

The goal is to give the AI the **smallest set of high-signal information** that enables it to solve the task at hand.

---

## L1: Technical Implementation Details (Engineer)

### 1. Decomposition Patterns

#### 1.1 Directory-Based Decomposition

**Pattern: `.claude/rules/` Automatic Loading**

All markdown files in `.claude/rules/` are automatically loaded with the same priority as the main CLAUDE.md. This enables:

- **Team ownership**: Frontend team maintains `code-style.md`, security team maintains `security.md`
- **No merge conflicts**: Separate files instead of one giant document
- **Domain separation**: Testing rules in `testing.md`, architecture in `architecture.md`

```
project/
├── CLAUDE.md                    # Core instructions (~60 lines ideal)
└── .claude/
    └── rules/
        ├── code-style.md        # Auto-loaded
        ├── testing.md           # Auto-loaded
        ├── security.md          # Auto-loaded
        └── api-conventions.md   # Auto-loaded
```

**Source:** [The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)

#### 1.2 Conditional/Scoped Rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field:

```yaml
---
description: Backend API conventions
paths:
  - "src/api/**/*.py"
  - "src/services/**/*.py"
---

When working with API files:
- Use async/await patterns
- Return proper HTTP status codes
```

**Source:** [Claude Code Memory Management](https://code.claude.com/docs/en/memory)

#### 1.3 Hierarchical Decomposition Pattern

Based on analysis of current Jerry structure and industry best practices:

```
Level 0: Root Context (CLAUDE.md)
├── Project overview, core philosophy
├── Essential commands, critical constraints
└── Pointers to detailed documentation

Level 1: Domain-Specific Rules (.claude/rules/)
├── Architecture standards
├── Coding standards
├── Testing standards
└── Error handling patterns

Level 2: Skill-Specific Context (skills/*/SKILL.md)
├── Loaded on-demand when skill invoked
├── Contains domain-specific instructions
└── May include embedded examples

Level 3: Reference Documentation (docs/)
├── ADRs, design decisions
├── Patterns, exemplars
└── Loaded only when explicitly referenced
```

### 2. Import/Include Mechanisms

#### 2.1 Claude Code `@` Syntax

```markdown
# In CLAUDE.md
@.claude/rules/architecture.md
@.claude/rules/testing.md

# Import from home directory (personal preferences)
@~/.claude/my-project-instructions.md

# Dynamic plugin resources
@${CLAUDE_PLUGIN_ROOT}/templates/report.md
```

**Constraints:**
- Maximum import depth: 5 hops (recursive imports)
- Imports NOT evaluated inside code blocks or spans
- Imports are resolved at file load time

**Source:** [Claude Code Documentation](https://code.claude.com/docs/en/memory)

#### 2.2 Shell Command Injection (`!` syntax)

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
---

## Dynamic Context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

Commands execute before Claude processes the prompt, enabling dynamic data injection.

**Source:** [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

#### 2.3 Cross-Platform Comparison

| Tool | Include Syntax | Auto-Discovery | Max Depth |
|------|----------------|----------------|-----------|
| Claude Code | `@path/to/file.md` | `.claude/rules/` | 5 hops |
| Cursor | `.cursor/rules/*.mdc` | Yes, by directory | Not specified |
| Python-Markdown | `{!filename!}` | No | Unlimited |
| MkDocs | `{% include %}` | Glob patterns | Configurable |
| DocFX | `[!INCLUDE [...]]` | No | Not specified |

### 3. Always-Loaded vs. Contextual Loading

#### 3.1 What Should ALWAYS Be Loaded

Based on Anthropic guidance and industry consensus:

| Category | Examples | Rationale |
|----------|----------|-----------|
| **Identity** | Project name, core purpose | Every response needs this |
| **Hard Constraints** | Security rules, forbidden actions | Safety critical |
| **Essential Commands** | Build, test, deploy commands | Frequently needed |
| **File Structure** | Key directory layout | Navigation essential |
| **Style Fundamentals** | Language version, line length | Consistency |

**Recommendation: < 300 lines total, ideally < 60 lines**

**Source:** [Writing a Good CLAUDE.md - HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

#### 3.2 What Should Be Loaded ON-DEMAND

| Category | Trigger | Loading Mechanism |
|----------|---------|-------------------|
| **Skill Content** | Skill invocation | `disable-model-invocation: true` |
| **Pattern Details** | Architecture questions | `@` import or explicit read |
| **API Docs** | API-related tasks | Retrieval or file read |
| **Test Examples** | Writing tests | Skill or file read |
| **ADRs** | Design decisions needed | Explicit file reference |

**Key Pattern: Progressive Disclosure**

> "Don't tell Claude all the information you could possibly want it to know. Rather, tell it how to find important information so that it can find and use it, but only when it needs to."

**Source:** [The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)

#### 3.3 Skills Lazy Loading Pattern

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions      # Preloaded into subagent
  - error-handling-patterns
---
```

Skills are aware of descriptions at session start, but full content loaded only when actively used.

**Source:** [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)

### 4. Cross-Reference Systems

#### 4.1 Path Resolution Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Relative from File** | Import from same module | `@./related-doc.md` |
| **Relative from Parent** | Import from sibling | `@../shared/common.md` |
| **Absolute from Root** | Project-wide reference | `@/docs/design/ADR-001.md` |
| **Home Directory** | User preferences | `@~/.claude/preferences.md` |
| **Environment Variable** | Plugin resources | `@${CLAUDE_PLUGIN_ROOT}/...` |

#### 4.2 Link Validation Strategies

1. **Build-Time Validation**: Check all `@` references resolve during CI
2. **Runtime Graceful Degradation**: Log warning for missing files, continue
3. **Dead Link Detection**: Periodic scan for broken references

#### 4.3 Reference Conventions for Jerry

Based on existing patterns in the codebase:

```markdown
# Reference to another file (for navigation/understanding)
**See Also**: `docs/design/ADR-002-project-enforcement.md`

# Reference to pattern catalog
**Related Pattern**: [Hexagonal Architecture](../patterns/architecture/hexagonal-architecture.md) (PAT-ARCH-001)

# Reference to template (for creation)
**Template**: `.context/templates/worktracker/TASK.md`
```

### 5. Context Optimization Techniques

#### 5.1 Token Budget Management

**The Attention Budget Concept:**

Like humans with limited working memory, LLMs have an "attention budget" that depletes as tokens are added. Research shows:

- Performance degrades non-uniformly as context grows
- "Lost in the middle" effect: best recall at start/end of context
- Semantic similarity affects retrieval accuracy

**Source:** [Chroma Research - Context Rot](https://research.trychroma.com/context-rot)

**Quantified Impact:**
- Accuracy for information at positions 1 or 20: 70-75%
- Accuracy for middle positions: 55-60%
- **15-20 percentage point drop** based purely on position

#### 5.2 Compaction Strategies

```bash
# Manual compaction with focus
/compact Focus on the API changes

# Configure in CLAUDE.md
"When compacting, always preserve the full list of modified files and any test commands"
```

**Source:** [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)

#### 5.3 Hierarchical Summarization Pattern

```
┌─────────────────────────────────────────────┐
│ Level 0: Index/Manifest (always loaded)     │
│ - File inventory, brief descriptions        │
│ - Relationships, dependencies               │
│ - Navigation hints                          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Level 1: Section Summaries (on-demand)      │
│ - Key decisions, critical constraints       │
│ - Interface specifications                  │
│ - Example snippets                          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Level 2: Full Details (explicit request)    │
│ - Complete implementations                  │
│ - Exhaustive examples                       │
│ - Historical context                        │
└─────────────────────────────────────────────┘
```

#### 5.4 Chunking for Large Documents

```python
# From Anthropic Cookbook
def chunk_text(text, chunk_size=2000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

**Contextual Embeddings** solve the "chunk lacks context" problem by adding relevant context to each chunk before embedding.

**Source:** [Anthropic Cookbook - RAG Guide](https://github.com/anthropics/anthropic-cookbook)

### 6. Index/Manifest Patterns

#### 6.1 Registry Pattern (Jerry Example)

```markdown
# projects/README.md - Project Registry

| ID | Name | Status | Description |
|----|------|--------|-------------|
| PROJ-001 | plugin-cleanup | COMPLETE | Plugin system refactoring |
| PROJ-008 | transcript-skill | IN_PROGRESS | Transcript processing |
| PROJ-009 | oss-release | PLANNING | Open source preparation |
```

#### 6.2 Navigation Index Pattern

```markdown
# .claude/patterns/PATTERN-CATALOG.md

## Architecture Patterns
| ID | Pattern | Location | Status |
|----|---------|----------|--------|
| PAT-ARCH-001 | Hexagonal Architecture | architecture/hexagonal-architecture.md | Stable |
| PAT-ARCH-002 | Ports and Adapters | architecture/ports-adapters.md | Stable |
```

#### 6.3 Skills Discovery Pattern

```yaml
# Skills are discovered by description, loaded when invoked
---
name: transcript
description: Parse VTT files and generate structured transcripts
disable-model-invocation: false  # Claude can invoke when relevant
---
```

---

## L2: Strategic Implications & Design Rationale (Architect)

### 1. Trade-off Analysis

#### 1.1 Monolithic vs. Decomposed Context

| Aspect | Monolithic (One File) | Decomposed (Many Files) |
|--------|----------------------|------------------------|
| **Simplicity** | Single source of truth | More files to manage |
| **Merge Conflicts** | High (everyone edits same file) | Low (separated concerns) |
| **Token Efficiency** | Everything loaded always | Load only what's needed |
| **Discovery** | Easy (one place to look) | Requires navigation |
| **Team Scale** | Poor (bottleneck) | Good (parallel work) |
| **Context Rot Risk** | High (bloated context) | Lower (targeted loading) |

**Recommendation:** Decomposed for projects > 100 lines of context, with clear navigation.

#### 1.2 Eager vs. Lazy Loading

| Strategy | Pros | Cons | Use When |
|----------|------|------|----------|
| **Eager (Always Load)** | No latency, guaranteed available | Consumes token budget | Critical constraints, identity |
| **Lazy (On-Demand)** | Token efficient, fresh data | Requires discovery mechanism | Reference docs, examples |
| **Hybrid** | Best of both | Complexity | Most real-world scenarios |

#### 1.3 Import Depth Trade-offs

| Depth | Maintainability | Cognitive Load | Debug Difficulty |
|-------|-----------------|----------------|------------------|
| 1 (flat) | Low (duplication) | Low | Low |
| 2-3 | Balanced | Moderate | Moderate |
| 4-5 | High (DRY) | High | High |
| 5+ | Fragile | Very High | Very High |

**Jerry Decision:** Maximum 3 levels recommended, with clear hierarchy.

### 2. Failure Mode Analysis (FMEA)

| Failure Mode | Cause | Effect | Severity | Mitigation |
|--------------|-------|--------|----------|------------|
| **Broken Import** | File moved/deleted | Context incomplete | High | CI validation of `@` paths |
| **Circular Import** | A imports B imports A | Infinite loop / crash | Critical | Max depth limit (5) |
| **Token Overflow** | Too many imports | Performance degradation | Medium | Budget monitoring, compaction |
| **Stale Reference** | Doc updated, ref outdated | Incorrect guidance | Medium | Link validation in CI |
| **Lost in Middle** | Important info in large file | Missed information | High | Hierarchical organization |
| **Semantic Drift** | Section doesn't match summary | Incorrect retrieval | Medium | Periodic audit, versioning |

### 3. Design Rationale

#### 3.1 Why Filesystem as Memory?

**Anthropic's Guidance:**
> "Claude Code already uses context engineering techniques - it doesn't load entire codebases into context. Instead, it explores files on-demand using tools, just like a human developer would."

**Benefits:**
1. **Infinite capacity**: Filesystem has no token limit
2. **Persistence**: Survives session restarts
3. **Versioning**: Git tracks changes
4. **Sharing**: Team members access same knowledge
5. **Tooling**: Existing search, grep, IDE support

#### 3.2 Why Skills System?

The skills architecture provides:

1. **Encapsulation**: Domain knowledge bundled with invocation
2. **Lazy Loading**: Full content loaded only when invoked
3. **Subagent Isolation**: Skills can run in separate context
4. **Composability**: Skills can reference other skills

#### 3.3 Why Index/Manifest Pattern?

**The Information Retrieval Problem:**

Without an index, Claude must:
1. Guess file names
2. Search directories
3. Read multiple files to find relevant info

With an index:
1. Consult single location
2. Navigate directly to relevant file
3. Read only what's needed

**Token Savings:** An index of 100 files might be 2KB vs. reading all 100 files (potentially 500KB+)

### 4. Pareto Analysis (80/20 Rule)

**80% of value comes from:**
1. **Core CLAUDE.md** (< 60 lines) - Identity, commands, critical constraints
2. **Top 5 rules files** - Most frequently needed guidance
3. **Active skill content** - Currently invoked domain knowledge

**20% long-tail (load on-demand):**
- Historical ADRs
- Edge case handling
- Exhaustive examples
- Reference documentation

### 5. Industry Comparison Matrix

| Feature | Claude Code | Cursor | Windsurf | GitHub Copilot |
|---------|-------------|--------|----------|----------------|
| **Auto-load rules dir** | Yes (.claude/rules/) | Yes (.cursor/rules/) | Yes | Limited |
| **Import syntax** | `@path` | N/A (MDC format) | N/A | N/A |
| **Max import depth** | 5 | Not specified | N/A | N/A |
| **Scoped rules** | YAML frontmatter | globs in MDC | .codeiumignore | N/A |
| **Skill/Command system** | Yes (skills/) | MCP | Cascade | Extensions |
| **Codebase indexing** | On-demand (tools) | Yes (full index) | Yes (RAG) | Yes |
| **Memory/Notes** | NOTES.md pattern | Memories | Memories | N/A |

### 6. Recommendations for Jerry OSS Release

#### 6.1 Immediate Actions

1. **Audit CLAUDE.md size** - Target < 300 lines, ideally < 100 for core
2. **Validate import chains** - Check for circular or deep imports
3. **Create navigation index** - Consolidate pattern catalog, skill registry
4. **Document loading strategy** - Which files are always-loaded vs. on-demand

#### 6.2 Decomposition Strategy

```
CLAUDE.md (Core - Always Loaded)
├── Project identity (10 lines)
├── Core commands (15 lines)
├── Critical constraints (15 lines)
├── Navigation pointers (10 lines)
└── Total: ~50 lines

.claude/rules/ (Auto-Loaded)
├── coding-standards.md (~100 lines)
├── architecture-standards.md (~150 lines)
├── testing-standards.md (~100 lines)
└── Total: ~350 lines (but loaded separately)

skills/ (On-Demand via Invocation)
├── worktracker/SKILL.md
├── problem-solving/SKILL.md
├── orchestration/SKILL.md
└── transcript/SKILL.md

docs/ (Explicit Reference Only)
├── design/ADR-*.md
├── patterns/*.md
└── governance/*.md
```

#### 6.3 OSS Considerations

For open-source release:
1. **Clear entry point**: CLAUDE.md should orient new contributors
2. **Self-documenting structure**: Directory names indicate purpose
3. **Minimal barrier**: Core instructions should be scannable in < 2 minutes
4. **Progressive complexity**: Advanced patterns discovered as needed

---

## Research Sources & Citations

### Primary Sources (Authoritative)

1. **Anthropic Engineering** - [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (September 2025)
2. **Claude Code Documentation** - [Memory Management](https://code.claude.com/docs/en/memory)
3. **Claude Code Documentation** - [Best Practices](https://code.claude.com/docs/en/best-practices)
4. **Claude Code Documentation** - [Skills](https://code.claude.com/docs/en/skills)
5. **Chroma Research** - [Context Rot](https://research.trychroma.com/context-rot) (July 2025)
6. **Anthropic Cookbook** - [RAG Guide](https://github.com/anthropics/anthropic-cookbook)

### Secondary Sources (Community/Analysis)

7. **Builder.io** - [The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
8. **HumanLayer** - [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
9. **Cursor Documentation** - [Rules](https://docs.cursor.com/context/rules)
10. **Windsurf Documentation** - [Context Awareness Overview](https://codeium.mintlify.app/context-awareness/overview)
11. **RAGFlow** - [From RAG to Context - 2025 Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)
12. **Augment Code** - [AI Coding Assistants for Large Codebases](https://www.augmentcode.com/tools/ai-coding-assistants-for-large-codebases-a-complete-guide)

### Research Papers

13. **Adobe Research** - Multi-hop Needle-in-Haystack Tests (February 2025)
14. **Stanford** - "Lost in the Middle" Phenomenon
15. **arXiv** - [Agentic RAG Survey](https://arxiv.org/abs/2501.09136) (January 2025)

### Context7 Documentation Queries

16. **Claude Code Repository** - Plugin resource access patterns
17. **Anthropic Cookbook** - Token counting, context management

---

## Appendix A: Pattern Quick Reference

### Import Syntax Cheat Sheet

```markdown
# File import (relative)
@./sibling-file.md
@../parent-dir/file.md

# File import (absolute from project root)
@/docs/design/ADR-001.md

# Home directory import
@~/.claude/preferences.md

# Plugin resource
@${CLAUDE_PLUGIN_ROOT}/templates/template.md

# Shell command injection (for dynamic context)
!`gh pr diff`
!`git log -5 --oneline`
```

### Directory Structure Template

```
project/
├── CLAUDE.md                    # Entry point, < 100 lines
├── .claude/
│   ├── rules/                   # Auto-loaded markdown files
│   │   ├── coding-standards.md
│   │   ├── architecture.md
│   │   └── testing.md
│   └── patterns/                # Referenced when needed
│       └── PATTERN-CATALOG.md
├── skills/                      # Loaded on invocation
│   └── {skill-name}/
│       ├── SKILL.md
│       └── docs/
└── docs/                        # Explicit reference only
    ├── design/
    └── knowledge/
```

### Loading Priority Matrix

| Priority | Source | When Loaded | Token Impact |
|----------|--------|-------------|--------------|
| 1 (Highest) | CLAUDE.md core | Always | ~500-1000 |
| 2 | .claude/rules/*.md | Always | ~2000-5000 |
| 3 | Active skill SKILL.md | On invocation | ~1000-3000 |
| 4 | Referenced docs | On explicit @ | Variable |
| 5 (Lowest) | Full file reads | On tool use | Variable |

---

*Research completed by ps-researcher on 2026-01-31*
*Frameworks applied: 5W2H, Pareto (80/20), FMEA*
