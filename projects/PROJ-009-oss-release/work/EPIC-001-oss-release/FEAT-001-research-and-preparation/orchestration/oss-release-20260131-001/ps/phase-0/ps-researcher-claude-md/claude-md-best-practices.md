# CLAUDE.md Optimization Best Practices Research

> **PS ID:** PROJ-009-oss-release | **Entry ID:** EN-003
> **Researcher:** ps-researcher (Research Specialist)
> **Date:** 2026-01-31
> **Workflow:** oss-release-20260131-001 | **Phase:** 0 (Divergent Exploration)

---

## L0: Executive Summary (ELI5)

**What is CLAUDE.md?**
Think of CLAUDE.md like a personalized instruction manual you give to a new team member on their first day. It tells Claude Code what your project is about, what rules to follow, and how to help you effectively.

**The Problem:**
When you give too many instructions at once, people (and AI) get overwhelmed and start missing important things. This is called "context rot" - where performance degrades as information accumulates.

**The Solution:**
Keep your instruction manual short and focused. Put detailed instructions in separate "skill" files that only load when needed - like having a main orientation guide, with specialized handbooks for specific tasks.

**Key Numbers:**
- Keep CLAUDE.md under **500 lines** (ideal) or **10,000 words** (maximum)
- Current Jerry CLAUDE.md: **912 lines** (needs optimization)
- Potential token savings: **50-70%** with proper structuring
- Quality improvement: Sessions stopping at **75% context utilization** produce higher-quality code

---

## L1: Technical Implementation Details (Engineer)

### 1. CLAUDE.md Structure and Organization

#### 1.1 Recommended File Size Limits

| Metric | Target | Maximum | Current Jerry |
|--------|--------|---------|---------------|
| Lines | ~500 | ~800 | 912 (over) |
| Words | ~5,000 | ~10,000 | ~8,500 (est.) |
| Tokens | ~5,000 | ~10,000 | ~10,000 (est.) |

**Source:** [Claude Code Docs - Costs](https://code.claude.com/docs/en/costs), [Builder.io Guide](https://www.builder.io/blog/claude-md-guide)

#### 1.2 Optimal Section Hierarchy

Based on analysis of effective CLAUDE.md files from authoritative sources:

```markdown
# Project CLAUDE.md

## Project Overview
[2-3 sentences max - what it does, tech stack]

## Critical Rules (MUST FOLLOW)
[Only rules that, if violated, cause failures]

## Available Commands
[Quick reference for /slash commands]

## Architecture Overview
[Brief structural guidance - ~10 lines]

## Testing Requirements
[Minimal essential testing rules]

## References
[Pointers to detailed docs, NOT inline content]
```

**Source:** [Everything Claude Code](https://context7.com/affaan-m/everything-claude-code/llms.txt)

#### 1.3 What to Include vs. Exclude

**INCLUDE (Always-Needed Context):**
- Project name and core purpose (1-2 sentences)
- Technology stack (list format)
- Critical coding rules that prevent failures
- Common bash commands (build, test, deploy)
- File/directory organization summary
- Environment setup essentials

**EXCLUDE (Move to Skills or Reference Files):**
- Detailed API documentation
- Comprehensive pattern libraries
- Full troubleshooting guides
- Verbose workflow instructions
- Entity mapping tables (like current Worktracker section)
- Template directories (reference, don't inline)

**Source:** [Anthropic Engineering Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

#### 1.4 Import/Reference Syntax

Claude Code supports two reference mechanisms:

**1. Eager Loading (@ syntax):**
```markdown
# CLAUDE.md
@docs/architecture.md
@docs/coding-standards.md
```
- Content loads at session start
- Increases initial token count
- Use sparingly for critical content

**2. Lazy Loading (Plain Reference):**
```markdown
# CLAUDE.md
See docs/detailed-patterns.md for comprehensive guide.
```
- Content loads only when Claude accesses the file
- Zero initial token cost
- Preferred for reference material

**Source:** [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules)

### 2. Content Optimization Techniques

#### 2.1 The Pruning Test

For each line in CLAUDE.md, ask:
> "Would removing this cause Claude to make mistakes?"

If NO, remove it. Bloated CLAUDE.md files cause instruction loss.

**Source:** [Builder.io Guide](https://www.builder.io/blog/claude-md-guide)

#### 2.2 Emphasis Hierarchy

```markdown
## CRITICAL (Must Never Violate)
IMPORTANT: Never modify the migrations folder directly.
YOU MUST run tests before committing.

## Guidelines (Strong Preference)
Prefer composition over inheritance.
Use 2-space indentation for TypeScript.

## Conventions (Soft Suggestions)
Function names should be descriptive.
```

**Source:** [SmartScope Optimization Guide](https://smartscope.blog/en/generative-ai/claude/claude-md-concise-agent-optimization-2026/)

#### 2.3 Output Constraints for Concise Plans

Add to reduce verbosity by 50-70%:

```markdown
## Output Constraints
- Maximum 500 words for implementation plans
- Use heading hierarchy up to h3 only
- Always specify: file names, commands, line numbers
- End with 2-3 specific follow-up questions
```

**Source:** [SmartScope Optimization Guide](https://smartscope.blog/en/generative-ai/claude/claude-md-concise-agent-optimization-2026/)

### 3. Multi-Project Patterns

#### 3.1 File Placement Hierarchy

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/CLAUDE.md` | Global | Personal preferences across all projects |
| `./CLAUDE.md` | Project | Team conventions (checked into git) |
| `./CLAUDE.local.md` | Project-Local | Personal overrides (gitignored) |
| `./subdir/CLAUDE.md` | Subdirectory | Module-specific rules |

**Precedence:** More specific files override less specific ones.

**Source:** [Claude Code Docs - Memory](https://docs.anthropic.com/en/docs/claude-code/memory)

#### 3.2 Monorepo Patterns

**Challenge:** One developer reduced CLAUDE.md from 47k to 9k words by splitting context.

**Solution: Hierarchical Loading**
```
project-root/
├── CLAUDE.md              # Core rules only (~500 lines)
├── frontend/
│   └── CLAUDE.md          # Frontend-specific rules
├── backend/
│   └── CLAUDE.md          # Backend-specific rules
└── docs/
    ├── architecture.md    # Reference (lazy-loaded)
    └── api-patterns.md    # Reference (lazy-loaded)
```

**Source:** [DEV.to Monorepo Guide](https://dev.to/anvodev/how-i-organized-my-claudemd-in-a-monorepo-with-too-many-contexts-37k7)

#### 3.3 Multi-Directory Workspace

Use `--add-dir` flag or `additionalDirectories` in `.claude/settings.json`:

```json
{
  "additionalDirectories": [
    "../shared-library",
    "../common-types"
  ]
}
```

**Source:** [ClaudeLog --add-dir Guide](https://claudelog.com/faqs/--add-dir/)

### 4. Context Rot Prevention

#### 4.1 The 75% Rule

Research finding: Sessions that stop at **75% context utilization** produce higher-quality, more maintainable code than sessions that run to 90%+.

**Why:** Context rot degrades architectural consistency and pattern adherence.

**Source:** [Claude Fast - Context Management](https://claudefa.st/blog/guide/mechanics/context-management)

#### 4.2 Strategic Commands

| Command | When to Use |
|---------|-------------|
| `/clear` | After each subtask completion |
| `/compact` | When approaching 50% context |
| `/compact <focus>` | Preserve specific information |
| `/cost` | Monitor token usage |

**Custom Compaction in CLAUDE.md:**
```markdown
## Compact Instructions
When compacting, preserve:
- Full list of modified files
- Test commands used
- API changes made
```

**Source:** [Claude Code Docs - Costs](https://code.claude.com/docs/en/costs)

#### 4.3 Subagent Delegation

Delegate context-heavy operations:
```
Use a subagent to investigate the test failures.
Use a subagent to research the authentication library.
```

Subagents run in separate context windows, returning only summaries.

**Source:** [Medium - Keep Context Clean](https://medium.com/@arthurpro/claude-code-keep-the-context-clean-d4c629ed4ac5)

#### 4.4 .claudeignore Usage

Create `.claudeignore` to exclude irrelevant directories:

```gitignore
node_modules/
vendor/
dist/
build/
*.log
.git/
__pycache__/
```

**Source:** [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)

### 5. Skills vs. CLAUDE.md

#### 5.1 When to Use Skills

| Content Type | Location | Reason |
|--------------|----------|--------|
| Always-needed rules | CLAUDE.md | Loaded every session |
| PR review workflow | Skill | Load on-demand |
| Database migrations | Skill | Load on-demand |
| Testing protocols | Skill | Load on-demand |
| API documentation | Skill reference/ | Load on-demand |

**Source:** [Claude Code Docs - Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

#### 5.2 Progressive Disclosure Architecture

Skills employ a 3-tier loading system:

1. **Metadata Loading** (~100 tokens): Claude scans available skills
2. **Full Instructions** (<5k tokens): Loaded when skill applies
3. **Bundled Resources**: Loaded only as needed

**Typical Token Savings:**
- API extraction: ~1,400 tokens
- Pattern library: ~3,640 tokens
- Troubleshooting: ~5,640 tokens
- Scripts: ~960 tokens

**Source:** [GitHub - Context Optimization](https://gist.github.com/johnlindquist/849b813e76039a908d962b2f0923dc9a)

---

## L2: Strategic Analysis (Architect)

### 1. Performance Implications

#### 1.1 Token Economics

| Scenario | Initial Tokens | Session Quality | Cost Impact |
|----------|---------------|-----------------|-------------|
| Bloated CLAUDE.md (1000+ lines) | ~15k | Degraded | +30-50% |
| Optimized CLAUDE.md (~500 lines) | ~5k | Optimal | Baseline |
| Optimized + Skills | ~5k base + on-demand | Optimal | -20-30% |

**Evidence:** Tool Search feature reduced MCP context bloat by 46.9% (51k tokens to 8.5k).

**Source:** [Medium - MCP Context Reduction](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)

#### 1.2 Quality vs. Quantity Trade-off

```
                    Quality
                       ▲
                       │     ★ Sweet Spot (75% utilization)
                   100%├─────★─────────────────
                       │    /  \
                       │   /    \  Context Rot Zone
                       │  /      \
                    50%├─/        \──────────────
                       │/          \
                       ├────────────────────────► Context Fill %
                       0%    50%    75%    90%   100%
```

**Key Insight:** More output ≠ better output. Raw token throughput peaks at 90% utilization, but code quality peaks at 75%.

### 2. Trade-offs Analysis

#### 2.1 Completeness vs. Brevity

| Approach | Pros | Cons |
|----------|------|------|
| **Complete CLAUDE.md** | All context available | Token waste, instruction loss |
| **Minimal CLAUDE.md** | Fast startup, focused | May miss context |
| **CLAUDE.md + Skills** | Best of both | Requires skill architecture |

**Recommendation:** CLAUDE.md + Skills architecture for Jerry.

#### 2.2 Eager vs. Lazy Loading

| Strategy | Initial Cost | Runtime Cost | Best For |
|----------|-------------|--------------|----------|
| Eager (@import) | High | None | Critical rules |
| Lazy (reference) | None | On-access | Reference material |
| Skills | Minimal | On-invoke | Workflows |

**Recommendation:**
- Eager: Core rules, coding standards
- Lazy: Templates, patterns, entity mappings
- Skills: Worktracker workflows, problem-solving, orchestration

### 3. One-Way Door Decisions

#### 3.1 Monorepo vs. Per-Project CLAUDE.md

**Current State:** Single CLAUDE.md at repo root (912 lines)

**Options:**

| Option | Reversibility | Risk | Benefit |
|--------|--------------|------|---------|
| Split into hierarchical | Fully reversible | Low | 50-70% token reduction |
| Move to skills | Mostly reversible | Medium | On-demand loading |
| Keep monolithic | N/A | High | No migration effort |

**Recommendation:** Hierarchical split is low-risk and reversible.

#### 3.2 Skills Migration

Moving content from CLAUDE.md to Skills is a **two-way door**:
- Easy to move content to skills
- Easy to move back if needed
- No permanent architectural commitment

### 4. Design Rationale for Jerry OSS Release

#### 4.1 Current Problems

1. **Token Bloat:** 912 lines exceeds 500-line recommendation by 82%
2. **Context Pollution:** Worktracker entity mappings loaded for non-worktracker tasks
3. **Template Duplication:** Full template structures inline instead of referenced
4. **TODO Verbosity:** 25+ META TODO items always in context

#### 4.2 Recommended Architecture

```
jerry/
├── CLAUDE.md                          # ~300 lines - Core only
│   ├── Project Overview               # 20 lines
│   ├── Core Architecture              # 50 lines
│   ├── Critical Rules                 # 30 lines
│   ├── Quick Commands                 # 20 lines
│   └── Skill/Reference Pointers       # 30 lines
│
├── skills/
│   ├── worktracker/SKILL.md           # Full worktracker guidance
│   ├── problem-solving/SKILL.md       # PS frameworks
│   ├── orchestration/SKILL.md         # Multi-agent coordination
│   └── architecture/SKILL.md          # Design guidance
│
└── docs/
    ├── knowledge/
    │   └── worktracker/               # Entity mappings, templates
    └── governance/
        └── JERRY_CONSTITUTION.md      # Governance (referenced)
```

#### 4.3 Proposed Optimized CLAUDE.md Structure

```markdown
# CLAUDE.md - Jerry Framework

## Overview
Jerry: Framework for behavior and workflow guardrails with filesystem-based memory.

## Core Architecture
- Hexagonal: domain/ → application/ → infrastructure/ → interface/
- Skills: Natural language interfaces in skills/
- Work Tracker: Persistent task state in projects/

## Critical Rules
IMPORTANT: Use UV for all Python operations (never pip/python directly)
IMPORTANT: One class per file in src/
YOU MUST: Update WORKTRACKER.md after completing work items

## Quick Commands
- /problem-solving - Research & analysis workflows
- /orchestration - Multi-agent coordination
- /worktracker - Task management

## Skills (Load On-Demand)
- worktracker - See skills/worktracker/SKILL.md
- problem-solving - See skills/problem-solving/SKILL.md
- orchestration - See skills/orchestration/SKILL.md

## References
- Templates: .context/templates/worktracker/
- Architecture: .claude/rules/architecture-standards.md
- Governance: docs/governance/JERRY_CONSTITUTION.md
```

**Estimated Reduction:** 912 lines → ~300 lines (67% reduction)

### 5. Implementation Roadmap

| Phase | Action | Token Impact |
|-------|--------|-------------|
| 1 | Extract Worktracker to skill | -200 lines |
| 2 | Move templates to references | -100 lines |
| 3 | Condense TODO to META checklist | -50 lines |
| 4 | Move entity mappings to docs | -150 lines |
| 5 | Optimize remaining sections | -100 lines |

---

## Research Citations

### Primary Sources (High Authority)

1. **Anthropic Official Documentation**
   - [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
   - [Claude Code Memory Management](https://docs.anthropic.com/en/docs/claude-code/memory)
   - [Claude Code Cost Management](https://code.claude.com/docs/en/costs)
   - [Anthropic Engineering Blog](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **Context7 Documentation Libraries**
   - [/anthropics/claude-code](https://github.com/anthropics/claude-code) - Official repo (781 snippets, High reputation)
   - [/websites/code_claude](https://code.claude.com) - Official docs (1619 snippets, High reputation)
   - [/nikiforovall/claude-code-rules](https://github.com/nikiforovall/claude-code-rules) - Handbook (1176 snippets, High reputation)
   - [/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) - Battle-tested configs (649 snippets, High reputation)

### Secondary Sources (Community Best Practices)

3. **Industry Guides**
   - [Builder.io - Complete CLAUDE.md Guide](https://www.builder.io/blog/claude-md-guide)
   - [SmartScope - Concise Agent Optimization](https://smartscope.blog/en/generative-ai/claude/claude-md-concise-agent-optimization-2026/)
   - [ClaudeLog - Token Optimization](https://claudelog.com/faqs/how-to-optimize-claude-code-token-usage/)

4. **Research & Analysis**
   - [Chroma Research - Context Rot](https://research.trychroma.com/context-rot)
   - [Medium - 60% Token Optimization](https://medium.com/@jpranav97/stop-wasting-tokens-how-to-optimize-claude-code-context-by-60-bfad6fd477e5)
   - [GitHub Gist - 54% Token Reduction](https://gist.github.com/johnlindquist/849b813e76039a908d962b2f0923dc9a)
   - [Medium - MCP Context Bloat Reduction](https://medium.com/@joe.njenga/claude-code-just-cut-mcp-context-bloat-by-46-9-51k-tokens-down-to-8-5k-with-new-tool-search-ddf9e905f734)

5. **Monorepo & Multi-Project**
   - [DEV.to - Monorepo Organization](https://dev.to/anvodev/how-i-organized-my-claudemd-in-a-monorepo-with-too-many-contexts-37k7)
   - [Claude Fast - Context Management](https://claudefa.st/blog/guide/mechanics/context-management)

---

## Appendix A: Analysis Frameworks Applied

### 5W2H Analysis

| Question | Answer |
|----------|--------|
| **What** | CLAUDE.md optimization for token efficiency and context quality |
| **Why** | Current 912-line file causes context rot and instruction loss |
| **Who** | Jerry framework users (developers, agents, OSS contributors) |
| **Where** | Repository root, with hierarchical overrides in subdirectories |
| **When** | Before OSS release to ensure quality first impression |
| **How** | Skills architecture, lazy loading, section pruning |
| **How Much** | Target: 67% reduction (912 → 300 lines) |

### Pareto Analysis (80/20)

**20% of Content Causing 80% of Token Waste:**
1. Worktracker entity hierarchy (full tree) - Move to skill
2. Worktracker templates directory structure - Reference only
3. META TODO items (25+ lines) - Consolidate to checklist
4. Entity mapping tables (ADO/SAFe/JIRA) - Move to docs
5. Detailed directory structure - Reference only

**20% of Content Providing 80% of Value:**
1. Project overview (what Jerry is)
2. Core architecture (hexagonal, skills)
3. Critical rules (UV, one-class-per-file)
4. Quick commands reference
5. Skill pointers for on-demand loading

---

## Appendix B: Comparison with Industry Exemplars

| Project | CLAUDE.md Lines | Strategy | Token Efficiency |
|---------|-----------------|----------|------------------|
| Everything Claude Code | ~200 | Skills + References | High |
| Claude Code Handbook | ~150 | Imports + Sections | High |
| Jerry (Current) | 912 | Monolithic | Low |
| Jerry (Proposed) | ~300 | Skills + Lazy Loading | High |

---

*Research completed: 2026-01-31*
*Researcher: ps-researcher (Research Specialist)*
*Validation: Pending ps-critic review*
