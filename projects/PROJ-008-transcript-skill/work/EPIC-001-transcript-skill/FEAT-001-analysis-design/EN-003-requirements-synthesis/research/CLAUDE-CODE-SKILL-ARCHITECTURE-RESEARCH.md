# Claude Code Skill Architecture Research

> **Research ID:** EN-003-RESEARCH-001
> **Date:** 2026-01-25
> **Author:** ps-researcher (Claude Opus 4.5)
> **Status:** COMPLETE
> **Traceability:** EN-003 Requirements Synthesis → FEAT-001 Analysis & Design → EPIC-001

---

## Document Audience (Triple-Lens)

| Level | Audience | Focus Areas |
|-------|----------|-------------|
| **L0 (ELI5)** | Stakeholders, New Users | Executive Summary, Key Takeaways |
| **L1 (Engineer)** | Developers implementing skills | Technical Patterns, Code Examples |
| **L2 (Architect)** | System designers, Decision makers | Strategic Implications, Trade-offs |

---

## Executive Summary (L0)

### What Are Claude Code Skills?

**Simple Analogy:** Think of skills as "recipe cards" for an AI chef. Each card contains specific instructions for making a particular dish. The chef (Claude) reads the card when needed and follows the steps. Without recipe cards, the chef must figure out everything from scratch each time.

**Key Insight:** Skills are **modular playbooks** that teach Claude how to perform specific tasks in a repeatable, standardized manner. They solve the "context rot" problem by offloading specialized knowledge to files.

### Key Takeaways

1. **Skills are simple to create** - Just a folder with a SKILL.md file containing YAML frontmatter and instructions
2. **Progressive disclosure** - Claude loads information in stages as needed, not all at once
3. **Model-agnostic potential** - Skills follow the [Agent Skills open standard](https://agentskills.io) working across multiple AI tools
4. **Three eras of evolution** - Prompt Engineering → Context Engineering → Agent Engineering

---

## Technical Deep Dive (L1)

### 1. SKILL.md Structure and Format

#### Basic Structure

```markdown
---
name: skill-name
description: What this skill does and when to use it
version: 1.0.0
---

# Skill Instructions

Your detailed instructions, guidelines, and examples go here...
```

#### YAML Frontmatter Fields

| Field | Required | Max Length | Description |
|-------|----------|------------|-------------|
| `name` | No* | 64 chars | Lowercase letters, numbers, hyphens only |
| `description` | Recommended | 1024 chars | What skill does AND when to use it |
| `version` | No | - | Semantic version |
| `disable-model-invocation` | No | - | Set `true` to prevent auto-invocation |
| `user-invocable` | No | - | Set `false` to hide from `/` menu |
| `allowed-tools` | No | - | Restrict tools (e.g., `Read, Grep, Glob`) |
| `model` | No | - | Model to use (`sonnet`, `opus`, `haiku`) |
| `context` | No | - | Set `fork` to run in isolated subagent |
| `agent` | No | - | Subagent type when `context: fork` |
| `hooks` | No | - | Lifecycle hooks for the skill |

*If omitted, uses directory name

**Source:** [Anthropic Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

#### Critical Rules

1. **Write descriptions in third person** - "Processes Excel files" NOT "I can help you process Excel files"
2. **Include trigger phrases** - "Use when the user asks to 'create a hook', 'add a PreToolUse hook'"
3. **Keep SKILL.md under 500 lines** - Split larger content into reference files
4. **All "when to use" info in description** - The body only loads AFTER triggering

### 2. Directory Structure Patterns

#### Simple Skill

```
skill-name/
└── SKILL.md              # Main instructions (required)
```

#### Complex Skill with Resources

```
skill-name/
├── SKILL.md              # Overview and navigation (required)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── commands/             # Slash commands (optional)
├── agents/               # Specialized agents (optional)
├── skills/               # Agent Skills (optional)
├── hooks/                # Event handlers (optional)
├── .mcp.json             # MCP tool configuration (optional)
└── README.md             # Plugin documentation
```

**Source:** [Claude Code Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)

### 3. Skill Storage Locations and Priority

| Location | Path | Applies To | Priority |
|----------|------|------------|----------|
| Enterprise | Managed settings | All org users | Highest |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects | High |
| Project | `.claude/skills/<name>/SKILL.md` | This project only | Medium |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled | Namespaced |

**Priority Resolution:** enterprise > personal > project (same name)

**Source:** [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

### 4. Agent Definition Structure

```markdown
---
name: agent-name
description: Agent role and expertise
capabilities:
  - Specific task 1
  - Specific task 2
tools: Read, Grep, Glob, Bash
model: sonnet
---

Detailed agent instructions and knowledge...
```

#### Invocation Patterns

```markdown
# Standard Response Patterns
assistant: "I'll use the [agent-name] agent to [what it will do]."

# Examples:
assistant: "I'll use the code-reviewer agent to analyze the changes."
assistant: "Let me use the test-generator agent to create comprehensive tests."
```

**Source:** [Context7 - Anthropic Claude Code](https://github.com/anthropics/claude-code)

### 5. Progressive Disclosure Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL LOADING STAGES                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Stage 1: DISCOVERY                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Only name + description from YAML frontmatter loaded │   │
│  │ Claude judges relevance to current task              │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                  │
│  Stage 2: INVOCATION                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Full SKILL.md body loaded into context               │   │
│  │ Instructions become active                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                  │
│  Stage 3: PROGRESSIVE DISCLOSURE                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Referenced files loaded only when needed             │   │
│  │ Scripts executed without loading into context        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight:** "The context window is a public good" - be concise because tokens compete.

**Source:** [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### 6. Command vs Skill vs Subagent

| Concept | Location | Invocation | Purpose |
|---------|----------|------------|---------|
| **Skill** | `.claude/skills/<name>/SKILL.md` | `/skill-name` or auto | Modular capabilities |
| **Command** | `.claude/commands/<name>.md` | `/command-name` | Legacy (merged into skills) |
| **Subagent** | `.claude/agents/<name>.md` | Task delegation | Isolated execution context |

**Note:** Commands have been merged into skills. Both work the same way.

**Source:** [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

### 7. Invocation Control Matrix

| Frontmatter | User Can Invoke | Claude Can Invoke | Context Loading |
|-------------|-----------------|-------------------|-----------------|
| (default) | Yes | Yes | Description always, full on invoke |
| `disable-model-invocation: true` | Yes | No | Not in context until user invokes |
| `user-invocable: false` | No | Yes | Description always, full on invoke |

**Use Cases:**
- `disable-model-invocation: true` → `/deploy`, `/commit` (side effects)
- `user-invocable: false` → Background knowledge (not actionable as command)

### 8. Tool Restriction Pattern

```yaml
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### 9. Dynamic Context Injection

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh:*)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
```

The `!`command`` syntax runs shell commands BEFORE Claude sees the content.

---

## Strategic Analysis (L2)

### 1. Evolution of AI Development Paradigms

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THREE ERAS OF AI DEVELOPMENT                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Era 1: PROMPT ENGINEERING (2022-2024)                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Focus: Finding the right words and phrases for prompts      │    │
│  │ Challenge: Manual orchestration, brittle instructions       │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              ↓                                       │
│  Era 2: CONTEXT ENGINEERING (2024-2025)                             │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Focus: Curating optimal context during inference            │    │
│  │ Tools: CLAUDE.md files, memory management, RAG              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              ↓                                       │
│  Era 3: AGENT ENGINEERING (2025+)                                   │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Focus: Designing specialized, reusable, efficient agents    │    │
│  │ Pattern: From manual orchestration to automatic delegation  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Source:** [ClaudeLog - Agent Engineering](https://claudelog.com/mechanics/agent-engineering/)

### 2. Model-Agnostic Design Principles

#### Industry Trend: Portable Skills

| Framework | Model Support | Key Feature |
|-----------|---------------|-------------|
| **Agent Skills Standard** | Claude, Codex, Gemini CLI, custom | Open standard via agentskills.io |
| **Strands Agents SDK** | Bedrock, Anthropic, LlamaAPI, Ollama, OpenAI | Pluggable provider interface |
| **Promptfoo** | Claude, Gemini, Llama, Ollama | Cross-provider evaluation |
| **OpenCode** | Any OpenAI-compatible | Provider-agnostic assistant |

**Source:** [AWS Strands Agents SDK](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/)

#### Portable Skill Design Patterns

1. **Prompt Intermediate Representation** - Structured, language-agnostic format as intermediary
2. **Pluggable Provider Interface** - Switch models by changing configuration, not code
3. **Avoid Provider-Specific Features** - XML preferred for Claude, YAML/JSON for others
4. **Test Across Models** - What works for Opus may need more detail for Haiku

**Source:** [Promptware Engineering Research](https://arxiv.org/html/2503.02400v1)

### 3. Multi-Agent Orchestration Patterns

#### Google ADK Architecture Principles

1. **Separate storage from presentation** - Distinguish durable state from per-call views
2. **Explicit transformations** - Context built through named, ordered processors
3. **Scope by default** - Every model call sees minimum context required

**Source:** [Google Developers Blog - Multi-Agent Framework](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)

#### Context Management for Multi-Agent Systems

- **Partial isolated context** - Each agent avoids confusion and context clash
- **Inter-agent communication protocols** - Share summarized context efficiently
- **Context checkpoints** - Manage token consumption and reuse

**Source:** [Vellum - Multi Agent AI Systems](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering)

### 4. Skill Authoring Best Practices Summary

| Principle | Description | Source |
|-----------|-------------|--------|
| **Concise is key** | Only add context Claude doesn't already have | Anthropic |
| **Set appropriate freedom** | High freedom for flexible tasks, low for fragile operations | Anthropic |
| **Test with all models** | Haiku needs more guidance, Opus may over-engineer | Anthropic |
| **Build evaluations first** | Create tests BEFORE documentation | Anthropic |
| **Progressive disclosure** | Split content >500 lines into separate files | Anthropic |
| **One level deep references** | All reference files link directly from SKILL.md | Anthropic |
| **Third-person descriptions** | "Processes files" not "I can help you" | Anthropic |

**Source:** [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

### 5. Freedom Spectrum for Instructions

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEGREES OF FREEDOM SPECTRUM                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  HIGH FREEDOM ←──────────────────────────────────────→ LOW FREEDOM  │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │ Text-based      │  │ Pseudocode/     │  │ Specific        │     │
│  │ instructions    │  │ parameterized   │  │ scripts         │     │
│  │                 │  │ scripts         │  │                 │     │
│  │ Use when:       │  │ Use when:       │  │ Use when:       │     │
│  │ - Multiple      │  │ - Preferred     │  │ - Operations    │     │
│  │   approaches    │  │   pattern       │  │   are fragile   │     │
│  │   valid         │  │   exists        │  │ - Consistency   │     │
│  │ - Decisions     │  │ - Some          │  │   critical      │     │
│  │   depend on     │  │   variation OK  │  │ - Specific      │     │
│  │   context       │  │                 │  │   sequence      │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
│                                                                      │
│  Example: Code     Example: Report     Example: Database           │
│  review            generation          migration                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Analogy:** Think of Claude as a robot on a path:
- **Narrow bridge with cliffs** → Provide exact instructions (low freedom)
- **Open field** → Give general direction (high freedom)

### 6. Trade-offs Analysis

| Design Choice | Pros | Cons | Recommendation |
|---------------|------|------|----------------|
| **Monolithic SKILL.md** | Simple, single file | Context bloat, slow loading | Use for <200 lines |
| **Progressive disclosure** | Efficient, focused | More files to maintain | Use for complex skills |
| **Auto-invocation** | Seamless UX | May trigger unexpectedly | Default for knowledge skills |
| **Manual-only** | Full control | User must remember command | Use for side-effect operations |
| **Subagent execution** | Isolated context | No conversation history | Use for focused tasks |

### 7. Claude 4.x Specific Considerations

> "Earlier versions of Claude would infer intent and expand on vague requests. Claude 4.x takes you literally and does exactly what you ask for, nothing more."

> "Claude Opus 4.5 has a tendency to overengineer... add explicit prompting to keep solutions minimal."

**Source:** [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## Exemplar Analysis

### Jerry Framework Skill Patterns (Internal)

| Skill | Version | Agents | Key Pattern |
|-------|---------|--------|-------------|
| `nasa-se` | 1.1.0 | 10 agents | NPR 7123.1D compliance, L0/L1/L2 outputs |
| `problem-solving` | 2.1.0 | 9 agents | Research/analysis/synthesis workflow |
| `orchestration` | 2.1.0 | 3 agents | Cross-pollinated pipelines, state tracking |

### Common Patterns Observed

1. **YAML frontmatter** - name, description, version, allowed-tools, activation-keywords
2. **Document audience table** - L0/L1/L2 triple-lens structure
3. **Agent tables** - Role, output location, state key
4. **Tool invocation examples** - Concrete bash/python examples
5. **Constitutional compliance** - P-002 (persistence), P-003 (no recursive subagents)
6. **Quick reference tables** - Common workflows, agent selection hints

---

## Actionable Recommendations for Transcript Skill

### 1. Skill Structure

```
transcript/
├── SKILL.md                    # Main skill (< 500 lines)
├── agents/
│   ├── ts-analyzer.md          # Analyzes transcript structure
│   ├── ts-extractor.md         # Extracts key information
│   └── ts-summarizer.md        # Generates summaries
├── templates/
│   ├── summary-template.md     # Output template for summaries
│   └── extraction-template.md  # Output template for extractions
├── reference/
│   ├── transcript-formats.md   # Supported format documentation
│   └── nlp-patterns.md         # NLP pattern reference
└── scripts/
    ├── parse_transcript.py     # Transcript parser utility
    └── validate_output.py      # Output validation
```

### 2. SKILL.md Template

```yaml
---
name: transcript
description: Analyzes meeting transcripts and conversations to extract insights, summarize content, and identify action items. Use when working with transcript files, meeting notes, conversation logs, or when the user asks about "what was discussed" or "summarize the meeting".
version: 1.0.0
allowed-tools: Read, Grep, Glob, Write
---

# Transcript Analysis Skill

## Document Audience (Triple-Lens)

| Level | Audience | Focus Areas |
|-------|----------|-------------|
| **L0** | Meeting participants | Key decisions, action items |
| **L1** | Project managers | Detailed analysis, timelines |
| **L2** | Leadership | Strategic implications |

## Available Agents

| Agent | Role | Output Location |
|-------|------|-----------------|
| `ts-analyzer` | Structure analysis | `docs/analysis/` |
| `ts-extractor` | Information extraction | `docs/extractions/` |
| `ts-summarizer` | Summary generation | `docs/summaries/` |

## Quick Start

[Instructions here...]

## Reference Files

- For transcript format details, see [reference/transcript-formats.md](reference/transcript-formats.md)
- For NLP patterns, see [reference/nlp-patterns.md](reference/nlp-patterns.md)
```

### 3. Model-Agnostic Design

1. **Use standard markdown** - Avoid provider-specific syntax
2. **Parameterize model selection** - Allow configuration override
3. **Document provider differences** - Note where behavior may vary
4. **Test with multiple models** - Verify with Haiku, Sonnet, Opus

### 4. Quality Gates

- [ ] SKILL.md under 500 lines
- [ ] Description under 1024 characters with trigger phrases
- [ ] Third-person descriptions throughout
- [ ] All references one level deep
- [ ] Evaluations created before documentation
- [ ] Tested with Haiku, Sonnet, and Opus

---

## Sources and Citations

### Primary Sources

1. **Anthropic Official Documentation**
   - [Claude Code Skills](https://code.claude.com/docs/en/skills)
   - [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
   - [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
   - [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

2. **GitHub Repositories**
   - [anthropics/claude-code](https://github.com/anthropics/claude-code)
   - [anthropics/skills](https://github.com/anthropics/skills)
   - [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)
   - [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

### Secondary Sources

3. **Industry Research**
   - [Promptware Engineering](https://arxiv.org/html/2503.02400v1) - Language-agnostic prompt design
   - [AWS Strands Agents SDK](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/)
   - [Google ADK Architecture](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)
   - [Vellum Multi-Agent Systems](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering)

4. **Community Resources**
   - [ClaudeLog - Agent Engineering](https://claudelog.com/mechanics/agent-engineering/)
   - [Mikhail Shilkov - Claude Code Skills](https://mikhail.io/2025/10/claude-code-skills/)
   - [Tyler Folkman - Claude Skills Guide](https://tylerfolkman.substack.com/p/the-complete-guide-to-claude-skills)

---

## Appendix: Research Methodology

### Sources Queried

1. **Context7** - /anthropics/claude-code, /davila7/claude-code-templates, /affaan-m/everything-claude-code
2. **WebSearch** - Claude Code skills, prompt engineering, multi-agent orchestration, model-agnostic design
3. **WebFetch** - Anthropic official documentation pages
4. **Internal Exemplars** - skills/nasa-se/, skills/problem-solving/, skills/orchestration/

### Frameworks Applied

- 5W2H (What, Why, Where, When, Who, How, How Much)
- Technology Assessment Matrix
- Trade-off Analysis
- Pattern Recognition across exemplars

---

*Research Document Version: 1.0.0*
*Last Updated: 2026-01-25*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-004, P-011)*
