# Skill Development Best Practices — Jerry Framework

> Synthesized from [Anthropic's Complete Guide to Building Skills for Claude](anthropic-skill-development-guide.pdf) and Jerry's established skill conventions (adversary, problem-solving, orchestration, worktracker, nasa-se, architecture, transcript, bootstrap).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Anthropic Universal Requirements](#anthropic-universal-requirements) | Official platform requirements from Anthropic |
| [Jerry Framework Conventions](#jerry-framework-conventions) | Jerry-specific patterns observed across 8 production skills |
| [Structural Checklist](#structural-checklist) | Combined pre-ship checklist |
| [Gap Analysis Template](#gap-analysis-template) | How to evaluate a skill against best practices |
| [References](#references) |  Source documents |

---

## Anthropic Universal Requirements

> Source: *The Complete Guide to Building Skills for Claude* (Anthropic, January 2026)

### File Structure

```
your-skill-name/
├── SKILL.md              # Required — main skill file
├── scripts/              # Optional — executable code
├── references/           # Optional — documentation loaded as needed
└── assets/               # Optional — templates, fonts, icons
```

**Critical rules:**
- File MUST be exactly `SKILL.md` (case-sensitive)
- Folder MUST use kebab-case (`saucer-boy` not `saucer_boy` or `SaucerBoy`)
- NO `README.md` inside the skill folder (all docs go in SKILL.md or references/)
- SKILL.md SHOULD be under 5,000 words

### Progressive Disclosure (3 Levels)

| Level | What | Token Impact |
|-------|------|-------------|
| **Level 1: YAML frontmatter** | Always loaded in Claude's system prompt. Just enough for Claude to know WHEN to use the skill. | Minimal — always present |
| **Level 2: SKILL.md body** | Loaded when Claude determines skill is relevant. Full instructions and guidance. | Moderate — on demand |
| **Level 3: Linked files** | References, scripts, assets that Claude loads only as needed. | Heavy — selective loading |

**Design implication:** Keep Level 1 lean. Push detailed content to Level 2 and reference files to Level 3.

### YAML Frontmatter

**Required fields:**

| Field | Rules |
|-------|-------|
| `name` | kebab-case, no spaces/capitals, SHOULD match folder name |
| `description` | MUST include WHAT it does + WHEN to use it + trigger phrases. Under 1024 chars. No XML tags (`< >`). |

**Optional fields:**

| Field | Purpose |
|-------|---------|
| `license` | Open source license (MIT, Apache-2.0) |
| `allowed-tools` | Restrict tool access (e.g., `"Bash(python:*) WebFetch"`) |
| `compatibility` | Environment requirements (1-500 chars) |
| `metadata` | Custom key-value pairs (author, version, mcp-server) |

**Jerry addition:**

| Field | Purpose |
|-------|---------|
| `version` | Semantic version (Jerry convention, maps to Anthropic's `metadata.version`) |
| `activation-keywords` | Explicit keyword list for skill routing (Jerry convention) |

### Description Field — The Most Critical Piece

The description is how Claude decides whether to load the skill. Structure:

```
[What it does] + [When to use it] + [Key capabilities]
```

**Good:**
```yaml
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".
```

**Bad:**
```yaml
description: Helps with projects.  # Too vague, no triggers
```

### Recommended SKILL.md Body Structure

```markdown
# Your Skill Name

## Instructions
### Step 1: [First Major Step]
Clear explanation of what happens.
Expected output: [describe what success looks like]

### Step 2: [Second Major Step]
...

## Examples
### Example 1: [Common scenario]
User says: "..."
Actions:
1. ...
2. ...
Result: ...

## Troubleshooting
### Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

### Instruction Writing Best Practices

| Practice | Good | Bad |
|----------|------|-----|
| Be specific | `Run scripts/validate.py --input {filename}` | `Validate the data` |
| Include error handling | `If validation fails, common issues include: ...` | (no error guidance) |
| Reference resources clearly | `Consult references/api-patterns.md for rate limiting guidance` | `Check the docs` |
| Use progressive disclosure | Keep SKILL.md focused; move details to `references/` | Inline everything |
| Put critical instructions first | `## Important` or `## Critical` headers at top | Bury key info |

### Workflow Patterns (from Anthropic)

| Pattern | When to Use | Key Techniques |
|---------|-------------|----------------|
| **Sequential Orchestration** | Multi-step processes in specific order | Explicit ordering, dependencies, validation per stage, rollback |
| **Multi-MCP Coordination** | Workflows spanning multiple services | Phase separation, data passing, cross-phase validation |
| **Iterative Refinement** | Output quality improves with iteration | Quality criteria, validation scripts, refinement loops, stop conditions |
| **Context-Aware Selection** | Same outcome, different tools by context | Decision trees, fallbacks, transparency about choices |
| **Domain-Specific Intelligence** | Specialized knowledge beyond tool access | Embedded expertise, compliance-before-action, audit trails |

### Testing Categories

| Category | Goal | How |
|----------|------|-----|
| **Triggering** | Skill loads at right times | Test obvious tasks, paraphrased requests, unrelated topics |
| **Functional** | Correct outputs produced | Valid outputs, API success, error handling, edge cases |
| **Performance** | Skill improves vs. baseline | Compare with/without: message count, tool calls, tokens, errors |

---

## Jerry Framework Conventions

> Observed across: `/adversary`, `/problem-solving`, `/orchestration`, `/worktracker`, `/nasa-se`, `/architecture`, `/transcript`, `/bootstrap`

### YAML Frontmatter — Jerry Pattern

Every Jerry skill uses these frontmatter fields:

```yaml
---
name: skill-name
description: >-
  [What it does]. [When to use it — trigger phrases].
version: "X.Y.Z"
allowed-tools: Read, Write, Edit, Glob, Grep
activation-keywords:
  - "keyword one"
  - "keyword two"
---
```

**Jerry-specific fields not in Anthropic's spec:**
- `version` — Semantic versioning at frontmatter level (not nested under metadata)
- `allowed-tools` — Comma-separated tool list (not quoted glob patterns)
- `activation-keywords` — YAML array of trigger phrases for Jerry's skill routing

### SKILL.md Body — Jerry Pattern

All Jerry skills follow this structural pattern:

```markdown
# Skill Name

> **Version:** X.Y.Z
> **Framework:** Jerry [Domain] ([Abbreviation])
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** [path to SSOT if applicable]

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent](#invoking-an-agent), [Available Agents](#available-agents) |
| **L2 (Architect)** | Workflow designers | [P-003 Compliance](#p-003-compliance), [Integration Points](#integration-points) |

---

## Purpose

[What the skill does + Key Capabilities list]

---

## When to Use This Skill

Activate when:
- [trigger condition 1]
- [trigger condition 2]

**Do NOT use when:**
- [anti-pattern 1]
- [anti-pattern 2]

---

## Available Agents

| Agent | Role | Model | Output Location |
|-------|------|-------|-----------------|
| `agent-name` | Role description | sonnet/haiku | `docs/output-dir/` |

---

## P-003 Compliance

[Agent hierarchy diagram showing MAIN CONTEXT as orchestrator, agents as workers]

---

## Invoking an Agent

### Option 1: Natural Language Request
[Examples]

### Option 2: Explicit Agent Request
[Examples]

### Option 3: Task Tool Invocation
[Code example with Task() call]

---

## [Domain-Specific Sections]

[Skill-specific content organized by topic]

---

## Integration Points

[How this skill connects to other skills/systems]

---

## Constitutional Compliance

| Principle | Requirement |
|-----------|-------------|
| P-001 | ... |
| P-002 | ... |

---

## Quick Reference

### Common Workflows
| Need | Agent | Command Example |
|------|-------|-----------------|

### Agent Selection Hints
| Keywords | Likely Agent |
|----------|--------------|

---

## References

| Source | Content |
|--------|---------|
| `full/path/to/file.md` | Description |

---

*Skill Version: X.Y.Z*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `path/to/ssot.md`*
*Created: YYYY-MM-DD*
```

### Section-by-Section Requirements

| Section | Required? | Notes |
|---------|-----------|-------|
| Version blockquote header | YES | Version, Framework, Constitutional Compliance |
| Triple-Lens audience table | YES | With preamble: "This SKILL.md serves multiple audiences:" |
| Purpose + Key Capabilities | YES | Bullet list of capabilities |
| When to Use / Do NOT use | YES | Trigger conditions AND anti-patterns |
| Available Agents | YES (if multi-agent) | Agent, Role, Model, Output Location columns |
| P-003 Compliance | YES (if multi-agent) | ASCII hierarchy diagram |
| Invoking an Agent (3 options) | YES (if multi-agent) | Natural language, explicit, Task tool code |
| Domain-specific content | YES | Skill-specific guidance organized by topic |
| Integration Points | RECOMMENDED | Cross-skill connections |
| Constitutional Compliance | RECOMMENDED | P-NNN principle mapping |
| Quick Reference | RECOMMENDED | Common workflows + agent selection hints |
| References | YES | **Full repo-relative paths** (e.g., `skills/saucer-boy/references/voice-guide.md`) |
| Footer | YES | Version, compliance, SSOT, date |

### File Reference Rules

**CRITICAL:** All file references in SKILL.md MUST use **full repo-relative paths**, not relative paths.

| Bad | Good |
|-----|------|
| `references/voice-guide.md` | `skills/saucer-boy/references/voice-guide.md` |
| `agents/sb-reviewer.md` | `skills/saucer-boy/agents/sb-reviewer.md` |
| `../quality-enforcement.md` | `.context/rules/quality-enforcement.md` |

**Rationale:** When Claude loads a SKILL.md, it needs unambiguous paths to navigate to referenced files. Relative paths are ambiguous depending on Claude's current working directory.

### Agent Definition Files

Each agent gets a separate `.md` file in `agents/`:

```
skills/your-skill/
├── SKILL.md
├── agents/
│   ├── agent-one.md
│   ├── agent-two.md
│   └── agent-three.md
└── references/
    ├── ref-one.md
    └── ref-two.md
```

Agent files define:
- Agent identity (name, version, role)
- Context requirements (what must be provided)
- Output format and persistence location (P-002)
- Tool usage patterns
- Reference files to load (and when)

### Registration Requirements

When a new skill is added to Jerry, it MUST be registered in:

| File | What to Add |
|------|-------------|
| `CLAUDE.md` | Entry in Quick Reference Skills table |
| `AGENTS.md` | All agents in Agent Summary + skill section |
| `.context/rules/mandatory-skill-usage.md` | Trigger keywords in Trigger Map (AE-002 auto-C3) |

---

## Structural Checklist

### Pre-Ship Checklist

**Anthropic requirements:**
- [ ] Folder named in kebab-case
- [ ] `SKILL.md` file exists (exact spelling, case-sensitive)
- [ ] YAML frontmatter has `---` delimiters
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `description` includes WHAT + WHEN + trigger phrases
- [ ] No XML tags (`< >`) anywhere in frontmatter
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked
- [ ] SKILL.md under 5,000 words
- [ ] No README.md in skill folder

**Jerry framework requirements:**
- [ ] Version blockquote header (Version, Framework, Constitutional Compliance)
- [ ] Triple-Lens audience table with preamble
- [ ] Purpose section with Key Capabilities
- [ ] When to Use / Do NOT use sections
- [ ] Available Agents table (if multi-agent)
- [ ] P-003 Compliance diagram (if multi-agent)
- [ ] Invoking an Agent with 3 options (if multi-agent)
- [ ] All file references use full repo-relative paths
- [ ] References table with full paths
- [ ] Footer with version, compliance, SSOT, date
- [ ] Registered in CLAUDE.md, AGENTS.md
- [ ] `activation-keywords` in frontmatter
- [ ] `version` in frontmatter

**Testing:**
- [ ] Triggers on obvious tasks
- [ ] Triggers on paraphrased requests
- [ ] Does NOT trigger on unrelated topics
- [ ] Functional outputs correct
- [ ] Agent invocation works (all 3 options)

---

## Gap Analysis Template

Use this to evaluate an existing skill against best practices:

```markdown
## Gap Analysis: /skill-name

### Anthropic Requirements
| Requirement | Status | Notes |
|-------------|--------|-------|
| kebab-case folder | ✅/❌ | |
| SKILL.md exists | ✅/❌ | |
| Frontmatter valid | ✅/❌ | |
| Description has WHAT+WHEN | ✅/❌ | |
| Under 5,000 words | ✅/❌ | |
| No README.md | ✅/❌ | |
| Examples included | ✅/❌ | |
| Error handling | ✅/❌ | |

### Jerry Conventions
| Convention | Status | Notes |
|------------|--------|-------|
| Version blockquote | ✅/❌ | |
| Triple-Lens table | ✅/❌ | |
| Purpose + capabilities | ✅/❌ | |
| When/Don't use | ✅/❌ | |
| Agents table | ✅/❌ | |
| P-003 diagram | ✅/❌ | |
| 3 invocation options | ✅/❌ | |
| Full repo-relative paths | ✅/❌ | |
| References table | ✅/❌ | |
| Footer | ✅/❌ | |
| CLAUDE.md registered | ✅/❌ | |
| AGENTS.md registered | ✅/❌ | |
```

---

## References

| Source | Content |
|--------|---------|
| `docs/knowledge/anthropic-skill-development-guide.pdf` | Anthropic's official 33-page skill development guide (January 2026) |
| `skills/adversary/SKILL.md` | Reference skill: adversarial quality reviews (428 lines) |
| `skills/problem-solving/SKILL.md` | Reference skill: structured problem-solving (442 lines) |
| `skills/orchestration/SKILL.md` | Reference skill: multi-agent workflow orchestration |
| `skills/worktracker/SKILL.md` | Reference skill: work item tracking |
| `skills/nasa-se/SKILL.md` | Reference skill: NASA systems engineering |
| `.context/rules/mandatory-skill-usage.md` | Skill invocation rules and trigger map |
| `.context/rules/quality-enforcement.md` | Quality gate SSOT |

---

*Synthesized: 2026-02-19*
*Sources: Anthropic Skill Guide (Jan 2026), Jerry Framework Skills v0.2.3*
