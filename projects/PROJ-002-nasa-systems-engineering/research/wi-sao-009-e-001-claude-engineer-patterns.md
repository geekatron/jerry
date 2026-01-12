# Research Artifact: Claude Engineer Agent Template Patterns

**PS ID:** wi-sao-009
**Entry ID:** e-research-001
**Topic:** Boris Cherny and Claude Engineers Agent Template Patterns
**Date:** 2026-01-11
**Researcher:** ps-researcher (Claude Opus 4.5)

---

## L0: Executive Summary

Boris Cherny (Creator of Claude Code at Anthropic) advocates for multi-session parallel agent workflows with verification loops, using Opus 4.5 exclusively and maintaining shared CLAUDE.md files as "do not repeat" ledgers. Anthropic's official agent template format uses YAML frontmatter with two required fields (`name`, `description`) for Skills and four key fields (`name`, `description`, `tools`, `model`) for subagents, following a progressive disclosure pattern that loads only relevant context on-demand. The industry is shifting from "prompt engineering" to "context engineering" - curating the optimal token configuration rather than finding magic words.

---

## L1: Technical Findings

### 1. Subagent Template Format (Official Specification)

Claude Code subagents use Markdown files with YAML frontmatter:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices. Use PROACTIVELY for auto-invocation.
tools: Read, Glob, Grep
model: sonnet
---

# Role
You are a code reviewer. When invoked, analyze the code and provide specific, actionable feedback.

# HITL Rule
Request human approval before suggesting architectural changes.
```

**Required Fields:**
| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Unique identifier (kebab-case) | `security-auditor` |
| `description` | Action-oriented purpose with trigger keywords | `Reviews security. Use after implementation complete.` |

**Optional Fields:**
| Field | Purpose | Default |
|-------|---------|---------|
| `tools` | Comma-separated tool whitelist | Inherits thread tools |
| `model` | Model override | `inherit` |
| `priority` | Delegation preference | None |
| `environment` | Environment-specific | None |
| `team` | Team-specific usage | None |

**Storage Locations:**
- Project: `.claude/agents/` (version-controlled, team-shared)
- User: `~/.claude/agents/` (personal, all projects)

### 2. Skills Format (Official Specification)

Skills are folders containing a `SKILL.md` file with simpler frontmatter:

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Instructions that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

**Progressive Disclosure Levels:**
1. **L1 (Startup):** Metadata (name/description) loaded into system prompt
2. **L2 (Activation):** SKILL.md body loaded when Claude determines relevance
3. **L3+ (Execution):** Linked supporting files loaded as needed

**Key Difference from Subagents:**
- Skills = Reusable context/instructions (no isolated context window)
- Subagents = Isolated agents with own context window

### 3. Boris Cherny's Multi-Agent Workflow

**Session Management:**
- 10-15 concurrent Claude Code sessions (5 terminal, 5-10 browser, mobile)
- Exclusively uses Opus 4.5 with thinking for all work
- Sessions numbered with OS notifications for tracking

**Key Patterns:**

```
Parallel Execution Pattern:
- Agent 1: Planning/Architecture
- Agent 2: Implementation
- Agent 3: Testing/Verification
- Agent 4: Documentation
- Agent 5: Code simplification
```

**Verification Loops (2-3x quality improvement):**
```
Claude writes code -> Claude opens browser -> Claude tests UI ->
Claude self-corrects -> Repeat until working
```

**CLAUDE.md as "Do Not Repeat" Ledger:**
- Short, focused file in git repository
- Updated when Claude makes mistakes
- NOT a comprehensive specification
- Acts as collective memory for anti-patterns

**Slash Commands:**
- `/commit-push-pr` - Full git workflow automation
- Stored in `.claude/commands/`
- Used dozens of times daily

### 4. Long-Running Agent Architecture

**Two-Agent Pattern:**

```
Session 0: Initializer Agent
├── Creates init.sh (dev server startup)
├── Creates claude-progress.txt (session log)
├── Creates feature-list.json (testable requirements)
└── Initial git commit

Session 1+: Coding Agent
├── Reads git log + progress file
├── Runs init.sh
├── Picks ONE feature
├── Implements + tests
├── Commits with descriptive message
└── Updates progress file
```

**claude-progress.txt Format:**
```
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

**feature-list.json Structure:**
```json
{
  "category": "functional",
  "description": "Clear end-to-end requirement",
  "steps": ["numbered", "verification", "steps"],
  "passes": false
}
```

### 5. Context Engineering Principles

**Core Philosophy:**
> "Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

**The "Right Altitude" Framework:**
- Too Prescriptive: Hardcoded if-else logic creates brittle agents
- Too Vague: "Be helpful" provides no concrete signals
- Goldilocks Zone: Clear behavioral signals with flexibility

**System Prompt Structure:**
```xml
<background_information>
Project context, constraints, domain knowledge
</background_information>

<instructions>
Specific behavioral guidance
</instructions>

## Tool guidance
When to use which tools

## Output description
Expected format and structure
```

**Anti-Patterns to Avoid:**
| Area | Anti-Pattern | Solution |
|------|--------------|----------|
| System Prompts | Excessive rules | 3-5 examples instead |
| Tools | Overlapping functionality | Single-purpose tools |
| Context | Pre-loading all data | Dynamic retrieval |
| Compaction | Stripping critical context | Preserve decisions |

**Improvement Metrics:**
- Context engineering can yield 54% improvement in agent tasks
- Multi-agent systems use 15x more tokens than chat
- LLM-as-judge can boost performance (lower robustness)

### 6. Multi-Agent Orchestration Pattern

**Orchestrator-Worker Architecture:**
```
User Query
    │
    v
Lead Agent (Orchestrator)
├── Analyzes request
├── Develops strategy
├── Spawns 3-5 subagents in parallel
│   ├── Subagent A: Aspect 1
│   ├── Subagent B: Aspect 2
│   └── Subagent C: Aspect 3
├── Collects condensed results
└── Synthesizes final answer
```

**Subagent Spawning:**
Each subagent receives:
- Objective
- Output format
- Tools/sources guidance
- Clear task boundaries

**Context Isolation Benefits:**
- Each subagent has own context window
- Only relevant excerpts returned to orchestrator
- Prevents token bloat from full context sharing

### 7. Tool Permissions by Role

| Role | Tools | Rationale |
|------|-------|-----------|
| Read-only (reviewers) | Read, Grep, Glob | Analyze without modifying |
| Research (analysts) | Read, Grep, Glob, WebFetch, WebSearch | Gather information |
| Write (developers) | Read, Write, Edit, Bash, Glob, Grep | Create and execute |
| Documentation | Read, Write, Edit, Glob, Grep, WebFetch, WebSearch | Document with research |
| PM/Architect | Read, Write, Grep, Glob, WebSearch | Search and docs |
| Implementer | Read, Edit, Write, Bash, Grep, Glob | Full write/execute |

### 8. Pipeline Pattern (Three-Stage)

```
Stage 1: pm-spec
├── Input: Enhancement request
├── Output: Spec, acceptance criteria, open questions
├── Status: READY_FOR_ARCH
└── Tools: Read, Write, Grep, Glob, WebSearch

Stage 2: architect-review
├── Input: Spec from PM
├── Output: ADR, guardrails
├── Status: READY_FOR_BUILD
└── Tools: Read, Write, Grep, Glob, WebSearch

Stage 3: implementer-tester
├── Input: ADR + spec
├── Output: Code, tests (passing), docs
├── Status: DONE
└── Tools: Read, Edit, Write, Bash, Grep, Glob
```

**Hooks for Chaining:**
- Register `SubagentStop` and `Stop` events
- Hook reads queue file, prints next command
- Human approval gate before proceeding
- Queue tracks: `BACKLOG -> READY_FOR_ARCH -> READY_FOR_BUILD -> DONE`

---

## L2: Strategic Implications for Unified Template Design

### 1. Template Unification Recommendations

**Converge on YAML Frontmatter Standard:**
Both Skills and Subagents use YAML frontmatter. The unified template should support:
```yaml
---
# Required (both Skills and Subagents)
name: agent-name
description: Clear, action-oriented description

# Subagent-specific (optional)
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit | sonnet | opus

# Extended (optional)
priority: high | normal | low
environment: development | production
team: backend | frontend | infrastructure
---
```

### 2. Progressive Disclosure Architecture

Adopt Anthropic's three-level loading:
1. **Index Level:** Name + description in system prompt (minimal tokens)
2. **Activation Level:** Full SKILL.md/agent prompt loaded on-demand
3. **Execution Level:** Supporting files loaded during task execution

This aligns with Jerry's anti-context-rot philosophy.

### 3. Verification Loop Integration

Every agent template should define:
- How it verifies its own work
- Exit criteria for success
- Handoff protocol for failure

Boris Cherny's insight: "The best agents are the ones that can check and self-correct."

### 4. CLAUDE.md as Living Anti-Pattern Registry

Maintain project-level CLAUDE.md as:
- NOT exhaustive documentation
- YES "do not repeat" ledger
- Updated reactively when mistakes occur
- Short and focused (<500 lines recommended)

### 5. Long-Running Agent Support

Templates should support:
- `claude-progress.txt` or equivalent state file
- Git commit checkpointing
- Feature list with testable criteria
- Session handoff protocols

### 6. Tool Whitelist Enforcement

Security-first approach:
- Default: Deny all
- Explicitly whitelist by role
- Separate read-only from write-capable agents
- Use hooks for sensitive operation gates

---

## Sources

### Primary Sources (Anthropic Official)

1. [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Official SKILL.md specification
2. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - System prompt best practices
3. [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) - claude-progress.txt pattern
4. [Building Agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) - SDK architecture patterns
5. [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) - Orchestrator-worker pattern
6. [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents) - Official subagent format
7. [Anthropic Skills GitHub Repository](https://github.com/anthropics/skills) - Official template repository

### Secondary Sources (Analysis & Interviews)

8. [The Creator of Claude Code Revealed His Workflow (VentureBeat)](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are) - Boris Cherny workflow
9. [Claude Code for Financial Services Webinar](https://www.anthropic.com/webinars/claude-code-for-financial-services-a-session-with-the-creator-boris-cherny) - Official Anthropic webinar
10. [Best Practices for Claude Code Subagents (PubNub)](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) - Pipeline patterns
11. [Agent Skills: Anthropic's Next Bid to Define AI Standards](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/) - Industry analysis
12. [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - Technical deep dive
13. [How Boris Cherny Uses Claude Code (Karo Zieminski)](https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow) - Workflow analysis
14. [VoltAgent Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 100+ template examples

### Related Resources

15. [Agent Skills Official Site](https://agentskills.io/home) - Open standard documentation
16. [Using Skills with Deep Agents (LangChain)](https://blog.langchain.com/using-skills-with-deep-agents/) - Cross-platform adoption
17. [Claude Prompting Best Practices](https://console.anthropic.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices) - Official prompting guide

---

## Appendix A: Unified Template Proposal

Based on research findings, here is a proposed unified agent template:

```yaml
---
# === Required Fields ===
name: nse-architect
description: >
  NASA Systems Engineering architect agent. Creates architecture decision records
  and system decomposition. Use after requirements are defined.

# === Subagent Configuration (Optional) ===
tools: Read, Write, Edit, Grep, Glob, WebSearch
model: inherit

# === Extended Metadata (Optional) ===
priority: high
team: systems-engineering
environment: development

# === Jerry Extensions (Optional) ===
worktracker_integration: true
verification_loop: self-test
---

# Role

You are a NASA Systems Engineering Architect. Your responsibility is to create
architecture decision records (ADRs) and system decomposition artifacts.

## Constraints

- Follow NASA-STD-8729.1 guidance
- All decisions must be traceable to requirements
- Document rationale for all architectural choices

## Input/Output Contract

**Input:** Requirements specification from pm-analyst
**Output:** ADR document + component diagram + interface definitions

## Verification

Before marking complete:
1. Verify all requirements are addressed
2. Confirm traceability matrix is complete
3. Validate interface definitions are consistent

## HITL Rules

Request human approval for:
- Safety-critical architectural decisions
- Interface changes affecting multiple subsystems
- Technology selection decisions
```

---

*Research completed: 2026-01-11*
*Token efficiency: Progressive disclosure recommended*
*Next action: Use findings to create unified template specification*
