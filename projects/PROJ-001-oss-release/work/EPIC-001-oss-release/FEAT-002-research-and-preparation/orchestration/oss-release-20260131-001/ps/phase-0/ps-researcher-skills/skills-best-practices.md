# Claude Code Skills Best Practices Research

<!--
PS ID: PROJ-001-oss-release
Entry ID: EN-105
Topic: Claude Code Skills Research
Agent: ps-researcher
Workflow: oss-release-20260131-001
Phase: 0 (Divergent Exploration)
Created: 2026-01-31
-->

---

## L0: Executive Summary (ELI5)

**What are Claude Code Skills?**

Think of skills like recipe cards for Claude. When you tell Claude to do something specific (like "process this meeting transcript" or "review my code"), Claude looks through its recipe cards to find the right one. Each skill contains step-by-step instructions, helper tools, and examples that make Claude really good at that specific task.

**Key Findings in Plain Language:**

1. **Skills are simple to create** - Just a folder with a SKILL.md file containing a name, description, and instructions. You can add scripts, templates, and reference files as needed.

2. **The description is crucial** - It tells Claude WHEN to use the skill. Write it like "This skill should be used when the user asks to..." followed by specific phrases users might say.

3. **One skill = one job** - Don't try to make a skill do everything. A "PDF text extraction" skill is better than a generic "document helper" skill.

4. **Multi-agent patterns matter** - For complex tasks, skills can orchestrate multiple agents, but there's a hard rule: only ONE level of nesting (orchestrator → workers, never orchestrator → worker → sub-worker).

5. **Skills are portable** - Anthropic designed skills as an open standard that can work across different AI tools, not just Claude.

**Business Impact:**

Properly designed skills transform Claude from a general-purpose assistant into a specialized expert for your specific workflows. The Jerry framework's skills (problem-solving, orchestration, transcript) demonstrate this pattern - each provides domain expertise that would otherwise require lengthy prompts every session.

---

## L1: Technical Analysis (Engineer)

### 1. SKILL.md Structure and Organization

#### 1.1 Required Frontmatter (YAML)

Based on [Anthropic's Claude Code documentation](https://code.claude.com/docs/en/skills), every SKILL.md requires YAML frontmatter:

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2". Be concrete and specific about trigger conditions.
version: "1.0.0"
---
```

**Extended Frontmatter (Jerry Pattern):**

```yaml
---
name: problem-solving
description: Structured problem-solving framework with specialized agents...
version: "2.1.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "research"
  - "analyze"
  - "investigate"
  - "architecture decision"
---
```

**Source:** Jerry `skills/problem-solving/SKILL.md` (analyzed from repository)

#### 1.2 Document Structure Patterns

| Section | Purpose | Jerry Implementation |
|---------|---------|---------------------|
| **Document Audience** | Triple-lens (L0/L1/L2) guide | Table mapping audiences to sections |
| **Purpose** | What the skill does | Key capabilities list |
| **When to Use** | Activation triggers | Bullet list of scenarios |
| **Available Agents** | Agent registry | Table with Role, Output Location |
| **Invoking an Agent** | Usage patterns | 3 options: Natural language, Explicit, Task Tool |
| **Orchestration Flow** | Multi-agent patterns | Sequential chain + state diagram |
| **State Management** | Agent handoff | Output keys and schema |
| **Constitutional Compliance** | Governance | Principle mapping table |
| **Quick Reference** | Fast lookup | Command examples + keyword hints |

#### 1.3 Skill Directory Structure

**Minimal Structure (Anthropic Standard):**

```
my-skill/
├── SKILL.md                 # Required: Instructions and metadata
└── (optional files)
```

**Full Structure (Best Practice):**

```
my-skill/
├── SKILL.md                 # Required: Main instructions
├── scripts/                 # Executable code for reliability
│   └── process.py
├── references/              # Documentation loaded as needed
│   └── api-schema.md
├── assets/                  # Files used in output
│   └── template.html
└── examples/                # Example outputs
    └── sample.md
```

**Source:** [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules)

**Jerry Enhanced Structure:**

```
skills/
└── skill-name/
    ├── SKILL.md             # Main skill definition
    ├── agents/              # Agent definition files
    │   ├── agent-type-1.md
    │   ├── agent-type-2.md
    │   └── AGENT_TEMPLATE.md
    ├── docs/                # Supporting documentation
    │   ├── PLAYBOOK.md      # Step-by-step execution guide
    │   └── RUNBOOK.md       # Operational procedures
    ├── templates/           # Output templates
    │   └── output.md
    ├── contexts/            # Domain-specific context (transcript skill)
    │   └── domain.yaml
    └── test_data/           # Validation data
        └── validation/
```

### 2. Skill Design Patterns

#### 2.1 Single-Agent vs. Multi-Agent Skills

**Single-Agent Pattern:**

Use when the skill has a focused, well-defined task:

```yaml
---
name: code-review
description: Reviews code for best practices...
---

# Instructions for code review
1. Check organization
2. Check error handling
3. Report findings
```

**Multi-Agent Pattern (Jerry):**

Use when the skill needs specialized perspectives:

```
MAIN CONTEXT (Claude) ← Orchestrator
    │
    ├──► ps-researcher   (gather info)
    ├──► ps-analyst      (analyze findings)
    ├──► ps-architect    (make decisions)
    └──► ps-reporter     (generate output)
```

**Source:** Jerry Constitution P-003, `skills/orchestration/SKILL.md`

#### 2.2 Agent Definition Structure

**Agent File Pattern (ps-researcher.md):**

```yaml
---
name: ps-researcher
version: "2.2.0"
description: "Deep research agent with MANDATORY artifact persistence..."
model: opus  # Complex research requires deeper reasoning

identity:
  role: "Research Specialist"
  expertise:
    - "Literature review and synthesis"
    - "Web research and source validation"
  cognitive_mode: "divergent"

persona:
  tone: "professional"
  communication_style: "consultative"
  audience_level: "adaptive"

capabilities:
  allowed_tools:
    - Read, Write, Edit, Glob, Grep
    - WebSearch, WebFetch, Task, Bash
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"

guardrails:
  input_validation:
    - ps_id_format: "^[a-z]+-\\d+(\\.\\d+)?$"
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations

output:
  required: true
  location: "projects/${JERRY_PROJECT}/research/{ps-id}-{entry-id}-{topic-slug}.md"
  levels: [L0, L1, L2]

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
---

<agent>
<identity>You are **ps-researcher**...</identity>
<persona>...</persona>
<capabilities>...</capabilities>
<guardrails>...</guardrails>
<constitutional_compliance>...</constitutional_compliance>
<invocation_protocol>...</invocation_protocol>
<output_levels>...</output_levels>
<state_management>...</state_management>
</agent>
```

**Key Design Elements:**

| Element | Purpose | Best Practice |
|---------|---------|---------------|
| `identity` | Define agent's role | Include expertise and cognitive mode |
| `persona` | Communication style | Specify tone and audience adaptation |
| `capabilities` | Tool access | Whitelist allowed tools, blacklist forbidden actions |
| `guardrails` | Input/output validation | Validate IDs, filter secrets |
| `output` | Persistence rules | Require file creation, specify location |
| `constitution` | Governance compliance | Reference principles and enforcement tiers |

#### 2.3 P-003 Compliance (No Recursive Subagents)

**Hard Constraint:**

```
ALLOWED:
Orchestrator → Worker (ONE level)

FORBIDDEN:
Orchestrator → Worker → Sub-worker (TWO+ levels)
```

**Enforcement Pattern:**

```yaml
forbidden_actions:
  - "Spawn recursive subagents (P-003)"
  - "Use Task tool that spawns further Tasks"
```

**Source:** Jerry Constitution, `docs/governance/JERRY_CONSTITUTION.md`

#### 2.4 State Passing Between Agents

**State Schema Pattern (Google ADK):**

```yaml
researcher_output:
  ps_id: "{ps_id}"
  entry_id: "{entry_id}"
  artifact_path: "projects/${JERRY_PROJECT}/research/{filename}.md"
  summary: "{key-findings-summary}"
  sources_count: {number}
  confidence: "{high|medium|low}"
  next_agent_hint: "ps-analyst for root cause analysis"
```

**Session Context Schema (Agent Handoff):**

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "{uuid}"
  source_agent:
    id: "ps-researcher"
    family: "ps"
  target_agent: "{next-agent}"
  payload:
    key_findings: [...]
    confidence: 0.85
    artifacts:
      - path: "{artifact-path}"
        type: "research"
```

### 3. Skill Integration Patterns

#### 3.1 Discovery and Loading

**How Claude Discovers Skills:**

1. **Slash Commands:** `/skill-name` directly invokes skill
2. **Description Matching:** Claude matches user intent to skill descriptions
3. **Keyword Activation:** Specific keywords trigger skill loading

**Best Practice (Specific Trigger Phrases):**

```yaml
# GOOD - Specific phrases
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", "validate tool use", or mentions hook events.

# BAD - Vague description
description: Helps with development tasks.
```

**Source:** [Claude Code Plugin Documentation](https://code.claude.com/docs/en/plugins)

#### 3.2 Invocation Patterns

**Option 1: Natural Language (Implicit):**
```
User: "Research best practices for event sourcing in Python"
Claude: (Detects "research" keyword → loads ps-researcher)
```

**Option 2: Explicit Agent Request:**
```
User: "Use ps-researcher to explore graph database options"
```

**Option 3: Slash Command:**
```
User: /transcript meeting.vtt --output-dir ./output/
```

**Option 4: Task Tool (Programmatic):**
```python
Task(
    description="ps-researcher: Graph databases",
    subagent_type="general-purpose",
    prompt="..."
)
```

#### 3.3 Context Injection Pattern

**Domain-Specific Context Loading (Transcript Skill):**

```yaml
context_injection:
  default_domain: "general"

  domains:
    - name: "software-engineering"
      description: "Standups, sprint planning..."
      file: "contexts/software-engineering.yaml"
      spec: "docs/domains/SPEC-software-engineering.md"

    - name: "security-engineering"
      description: "Security audits, threat modeling..."
      file: "contexts/security-engineering.yaml"
      special_requirements: ["stride_support"]

  context_path: "./contexts/"
```

**Template Variables:**
```yaml
template_variables:
  - name: domain
    source: invocation.domain
    default: "general"
  - name: entity_definitions
    source: context.entity_definitions
    format: yaml
```

### 4. Documentation Structure (L0/L1/L2)

#### 4.1 Triple-Lens Pattern

**Anthropic Recommendation:** Serve multiple audiences with layered content.

| Level | Audience | Focus |
|-------|----------|-------|
| **L0 (ELI5)** | Stakeholders, new users | What/Why in plain language |
| **L1 (Engineer)** | Developers | How with code examples |
| **L2 (Architect)** | Workflow designers | Trade-offs, strategic implications |

**Implementation Pattern:**

```markdown
## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0** | New users | Purpose, When to Use |
| **L1** | Developers | Agent Pipeline, State Schema |
| **L2** | Architects | Orchestration Flow, Constitutional Compliance |
```

#### 4.2 Playbook vs. Runbook

| Document | Purpose | Content |
|----------|---------|---------|
| **PLAYBOOK.md** | Step-by-step execution guide | Phases, decision points, rollback |
| **RUNBOOK.md** | Operational procedures | Troubleshooting, recovery, monitoring |

**Playbook Structure (Jerry Pattern):**

```markdown
## Table of Contents
1. Quick Start (L0 - ELI5)
2. Overview
3. Prerequisites
4. Phase 1: Foundation
5. Phase 2: Core Extraction
6. Phase 3: Integration
7. Phase 4: Validation
8. Rollback Procedures
9. Decision Points Summary
10. L2: Architecture & Performance
11. Anti-Patterns
12. Pattern References
13. Constraints and Limitations
```

#### 4.3 Quality Validation Integration

**ps-critic Pattern:**

```yaml
# Quality thresholds
validation:
  quality_threshold: 0.90
  criteria:
    - "Core validation (files 00-07)"
    - "MM-* criteria (if mindmap present)"
    - "AM-* criteria (if ASCII mindmap present)"
```

### 5. Tool Invocation Examples

**Critical for Agent Clarity:**

```markdown
### Tool Invocation Examples

1. **Finding existing research:**
   ```
   Glob(pattern="docs/research/**/*.md")
   → Returns list of prior research documents
   ```

2. **Creating research output (MANDATORY per P-002):**
   ```
   Write(
       file_path="projects/${JERRY_PROJECT}/research/{id}-{topic}.md",
       content="# Research: {Topic}\n\n## L0: Executive Summary\n..."
   )
   → Persist findings - transient output VIOLATES P-002
   ```
```

**Source:** Jerry agent files (ps-researcher.md, orch-tracker.md)

---

## L2: Architectural Implications (Architect)

### 1. Strategic Trade-offs

#### 1.1 Single Skill vs. Multi-Skill Architecture

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Single Monolithic Skill** | Simple to maintain, single source of truth | Limited reusability, bloated SKILL.md | Simple, focused tasks |
| **Modular Multi-Skill** | Composable, reusable agents | Coordination overhead, state management complexity | Complex workflows, multiple use cases |
| **Federated Template** | 73% code reuse, consistent patterns | Template maintenance burden | Multiple skills with similar structure |

**Jerry Decision:** Federated template architecture for agent definitions (PS_AGENT_TEMPLATE.md + domain extensions).

#### 1.2 Agent Nesting Depth

**Design Decision: P-003 (Hard Constraint)**

| Depth | Pattern | Support |
|-------|---------|---------|
| 0 | Direct execution (no agents) | Supported |
| 1 | Orchestrator → Workers | **Supported (recommended)** |
| 2+ | Worker → Sub-workers | **FORBIDDEN** |

**Rationale:**
- **Context preservation:** Each nesting level loses context
- **Debugging complexity:** Deep stacks are hard to trace
- **State management:** Each level adds handoff overhead
- **Industry alignment:** Matches CrewAI, LangGraph patterns

**Source:** [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)

#### 1.3 File Persistence (P-002) Design

**Trade-off Matrix:**

| Approach | Persistence | Recoverability | Context Efficiency |
|----------|-------------|----------------|-------------------|
| Transient only | None | Low (lost on session end) | High (no I/O) |
| File after completion | Full | High (survives compaction) | Medium (one write) |
| Streaming writes | Full | Very High (crash recovery) | Lower (multiple writes) |

**Jerry Decision:** File after completion (mandatory per P-002).

**Rationale:**
- Context rot research shows LLM performance degrades with context size
- File persistence offloads state from context window
- Enables cross-session continuity

**Source:** [Chroma Context Rot Research](https://research.trychroma.com/context-rot)

### 2. Skill Architecture Patterns

#### 2.1 Hybrid Architecture (Python + LLM)

**Transcript Skill Pattern:**

```
VTT Input → Python Parser (deterministic) → Chunked JSON
    ↓
LLM Agents (extraction, formatting) → Structured Output
    ↓
ps-critic (validation) → Quality Score
```

**Benefits:**
- **1,250x cost reduction** for parsing (Python vs. LLM)
- **100% accuracy** for deterministic operations
- **Sub-second parsing** for large files

**Source:** Jerry transcript skill DISC-009 (Agent-only architecture caused 99.8% data loss)

#### 2.2 Cross-Pollinated Pipeline Pattern

**Orchestration Skill Pattern:**

```
Pipeline A (PS)              Pipeline B (NSE)
    │                              │
    ▼                              ▼
┌─────────┐                  ┌─────────┐
│ Phase 1 │                  │ Phase 1 │
└────┬────┘                  └────┬────┘
     │                            │
     └──────────┬─────────────────┘
                ▼
        ╔═══════════════╗
        ║   BARRIER 1   ║  ← Cross-pollination
        ╚═══════════════╝
```

**Benefits:**
- Parallel execution of independent agents
- Sync barriers for cross-pipeline insights
- Checkpoint recovery for long workflows

#### 2.3 Context Injection Pattern

**Domain-Specific Customization:**

```yaml
domains:
  - name: "software-engineering"
    entities: [commitments, blockers, risks]

  - name: "security-engineering"
    entities: [vulnerabilities, threats, compliance_gaps]
    special_requirements: ["stride_support"]
```

**Design Implications:**
- Skills can serve multiple domains with same core logic
- Context files customize extraction rules
- Template variables inject domain-specific prompts

### 3. Open Standard Considerations

**Anthropic's Position:**

> "Like MCP, we believe skills should be portable across tools and platforms—the same skill should work whether you're using Claude or other AI platforms."

**Source:** [Anthropic Agent Skills Announcement](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

**Implications for OSS Release:**

| Consideration | Impact | Mitigation |
|---------------|--------|------------|
| Platform portability | Skills must use standard formats | Stick to YAML frontmatter + Markdown |
| Tool dependencies | Some tools are Claude-specific | Abstract tool calls, document alternatives |
| State management | Different platforms have different state | Use file-based state (universal) |
| Agent invocation | Task tool is Claude-specific | Document invocation patterns abstractly |

### 4. Performance and Scaling

#### 4.1 Context Window Management

**Best Practices:**
- Keep SKILL.md under 10,000 tokens for fast loading
- Use progressive disclosure (reference files for details)
- Chunk large inputs (transcript skill: 500 segments per chunk)

**Jerry Pattern:**
```yaml
# SKILL.md: Core instructions only (~3,000 tokens)
# agents/*.md: Detailed agent specs (loaded on demand)
# docs/*.md: Reference documentation (loaded on demand)
```

#### 4.2 Agent Model Selection

| Model | Use Case | Jerry Pattern |
|-------|----------|---------------|
| opus | Complex reasoning, research | ps-researcher, ps-architect |
| sonnet | Balanced capability | ps-analyst, ts-extractor |
| haiku | Fast, simple tasks | Orchestration, routing |

**Dynamic Selection:**
```yaml
model: auto  # Let Claude select based on task complexity
```

### 5. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Context overflow | Medium | High (skill fails to load) | Progressive disclosure, chunking |
| Agent recursion | Low | High (infinite loops) | P-003 hard constraint |
| State loss | Medium | Medium (restart required) | File persistence (P-002) |
| Version mismatch | Low | Low (degraded behavior) | Schema versioning |
| Platform lock-in | Medium | Medium (portability issues) | Use open standards |

---

## References

### Primary Sources (Official Documentation)

1. [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) - Official Anthropic documentation on skill structure and best practices

2. [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) - Anthropic engineering blog on Claude Code patterns

3. [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Anthropic's agent skills announcement and open standard

4. [GitHub - anthropics/skills](https://github.com/anthropics/skills) - Anthropic's official skills repository

### Secondary Sources (Industry Guidance)

5. [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) (Context7: `/affaan-m/everything-claude-code`) - Benchmark Score: 68.5 - Battle-tested configurations from Anthropic hackathon winner

6. [Claude Code Handbook](https://github.com/nikiforovall/claude-code-rules) (Context7: `/nikiforovall/claude-code-rules`) - Benchmark Score: 65.2 - Collection of Claude Code recommendations

7. [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - Technical analysis of skill architecture

8. [Claude Skills and CLAUDE.md: a practical 2026 guide for teams](https://www.gend.co/blog/claude-skills-claude-md-guide) - Team implementation guidance

### Framework References

9. [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - Multi-agent coordination patterns

10. [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - State machine patterns for agents

11. [CrewAI Flows](https://docs.crewai.com/concepts/flows) - Agent orchestration patterns

### Jerry Framework Sources (Analyzed)

12. `skills/problem-solving/SKILL.md` - v2.1.0 - Multi-agent problem-solving framework

13. `skills/orchestration/SKILL.md` - v2.1.0 - Cross-pollinated pipeline orchestration

14. `skills/transcript/SKILL.md` - v2.5.0 - Hybrid Python+LLM architecture

15. `skills/problem-solving/agents/ps-researcher.md` - v2.2.0 - Agent definition pattern

16. `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` - v1.0.0 - Federated template architecture

---

## PS Integration

### State Output

```yaml
researcher_output:
  ps_id: "PROJ-001-oss-release"
  entry_id: "EN-105"
  artifact_path: "projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher-skills/skills-best-practices.md"
  summary: "Comprehensive research on Claude Code skills best practices covering SKILL.md structure, agent patterns, integration methods, and documentation standards"
  sources_count: 16
  confidence: "high"
  next_agent_hint: "ps-analyst for synthesis with other research streams"
```

### Key Findings for Cross-Pollination

1. **SKILL.md Structure:** YAML frontmatter (name, description, version) + Markdown instructions
2. **Agent Pattern:** Identity → Persona → Capabilities → Guardrails → Constitution → Output
3. **Hard Constraint:** P-003 (No recursive subagents) - ONE level max
4. **Persistence:** P-002 requires file output - transient responses forbidden
5. **Documentation:** L0/L1/L2 triple-lens structure for multiple audiences
6. **Integration:** Slash commands, keyword activation, Task tool invocation
7. **Open Standard:** Skills designed for cross-platform portability

---

*Research completed: 2026-01-31*
*Agent: ps-researcher v2.2.0*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
