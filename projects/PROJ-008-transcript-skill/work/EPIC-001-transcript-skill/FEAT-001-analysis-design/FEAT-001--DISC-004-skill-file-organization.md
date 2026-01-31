# DISC-004: Skill and Agent File Organization Standards

<!--
TEMPLATE: Discovery
SOURCE: ONTOLOGY-v1.md Section 3.4.8
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "DISC-004"
work_type: DISCOVERY
title: "Skill and Agent File Organization Standards for Claude Code"

# === LIFECYCLE ===
status: DOCUMENTED
severity: HIGH
impact: ARCHITECTURAL

# === TIMESTAMPS ===
discovered_at: "2026-01-26T14:00:00Z"
discovered_by: "Claude"

# === HIERARCHY ===
parent_id: "FEAT-001"

# === TAGS ===
tags:
  - "file-organization"
  - "claude-code"
  - "industry-standards"
  - "skill-structure"
```

---

## Discovery Summary

Research into Claude Code industry standards for skill and agent file organization confirms that **agents are flat markdown files** (e.g., `ts-parser.md`), not subdirectories with an `AGENT.md` file inside. This discovery directly informs how we should organize the Transcript Skill implementation.

---

## L0: Simple Explanation (ELI5)

Think of organizing files in a filing cabinet:
- **Wrong way**: Creating a folder named "Tax Documents" and putting a single piece of paper called "THE DOCUMENT" inside
- **Right way**: Just putting a piece of paper named "Tax-2026.pdf" directly in the drawer

For Claude Code agents:
- **Wrong**: `agents/ts-parser/AGENT.md` (folder → file)
- **Right**: `agents/ts-parser.md` (just a file)

---

## L1: Technical Analysis

### Research Sources

| Source | Type | Credibility | URL |
|--------|------|-------------|-----|
| Claude Code Official Docs | Primary | HIGH | [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) |
| Anthropic Engineering Blog | Primary | HIGH | [anthropic.com/engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| Context7 Claude Code Library | Secondary | HIGH | `/anthropics/claude-code` |
| Claude Blog - Skills Explained | Primary | HIGH | [claude.com/blog/skills-explained](https://claude.com/blog/skills-explained) |
| Industry Guide - AGENTS.md | Secondary | MEDIUM | [pnote.eu/notes/agents-md](https://pnote.eu/notes/agents-md/) |

### Finding 1: Agent File Structure

**Official Claude Code Documentation States:**

> Custom agents are stored as Markdown files with YAML frontmatter at `.claude/agents/your-agent-name.md`

**Evidence from Context7 Query (`/anthropics/claude-code`):**

```
agents/
├── analyzer.md
├── reviewer.md
└── generator.md
```

**NOT:**

```
agents/
├── analyzer/
│   └── AGENT.md
├── reviewer/
│   └── AGENT.md
└── generator/
    └── AGENT.md
```

### Finding 2: Skill Directory Structure

**Official Plugin Documentation States:**

> To add skills to a plugin, add a `skills/` directory at your plugin root with Skill folders containing SKILL.md files.

**Correct Structure:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Only this goes here!
├── skills/
│   └── my-skill/
│       ├── SKILL.md         # Required: Entry point
│       ├── agents/          # Optional: Sub-agents
│       │   ├── parser.md
│       │   └── formatter.md
│       └── docs/            # Optional: Supporting docs
└── hooks/                   # At plugin root, NOT inside .claude-plugin
```

### Finding 3: Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Agent file | lowercase-kebab-case.md | `ts-parser.md` |
| Skill directory | lowercase-kebab-case | `transcript-skill/` |
| SKILL.md | UPPERCASE | `SKILL.md` |
| Supporting docs | lowercase-kebab-case | `usage-guide.md` |

### Finding 4: YAML Frontmatter Requirements

**For Agents (minimal):**

```yaml
---
name: ts-parser
description: Parses VTT/SRT transcript files into structured JSON
---
```

**For Skills (full):**

```yaml
---
name: transcript
description: Processes meeting transcripts into structured knowledge artifacts
---
```

Only `name` and `description` are **required**. Additional fields are optional.

### Finding 5: Progressive Disclosure Pattern

From Anthropic Engineering:

> "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable. Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed."

This means:
- SKILL.md should be the entry point (<500 lines)
- Complex instructions split to sub-files
- Agents as separate files that can be loaded on-demand

---

## L2: Architectural Implications

### Impact on Transcript Skill

**Current (Wrong) Structure:**

```
EN-005-design-documentation/
├── agents/
│   ├── ts-parser/
│   │   └── AGENT.md         ✗ Wrong pattern
│   ├── ts-extractor/
│   │   └── AGENT.md         ✗ Wrong pattern
│   └── ts-formatter/
│       └── AGENT.md         ✗ Wrong pattern
└── SKILL.md
```

**Target (Correct) Structure:**

```
skills/
└── transcript/
    ├── SKILL.md              # Entry point orchestrator
    ├── agents/
    │   ├── ts-parser.md      ✓ Flat file
    │   ├── ts-extractor.md   ✓ Flat file
    │   └── ts-formatter.md   ✓ Flat file
    ├── docs/
    │   ├── PLAYBOOK.md       # Execution guide
    │   └── RUNBOOK.md        # Troubleshooting guide
    └── templates/            # Optional: Output templates
```

### Migration Path

| Current File | Target Location |
|--------------|-----------------|
| `agents/ts-parser/AGENT.md` | `skills/transcript/agents/ts-parser.md` |
| `agents/ts-extractor/AGENT.md` | `skills/transcript/agents/ts-extractor.md` |
| `agents/ts-formatter/AGENT.md` | `skills/transcript/agents/ts-formatter.md` |
| `SKILL.md` | `skills/transcript/SKILL.md` |
| `docs/PLAYBOOK-en005.md` | `skills/transcript/docs/PLAYBOOK.md` |
| `docs/RUNBOOK-en005.md` | `skills/transcript/docs/RUNBOOK.md` |

### Conformance with Jerry Architecture

This aligns with Jerry's existing patterns:

```
skills/
├── problem-solving/
│   ├── SKILL.md
│   └── agents/
│       ├── ps-researcher.md    ← Same pattern!
│       ├── ps-analyst.md
│       ├── ps-architect.md
│       └── ...
├── orchestration/
│   └── SKILL.md
└── transcript/                  ← New skill follows same pattern
    ├── SKILL.md
    └── agents/
        ├── ts-parser.md
        ├── ts-extractor.md
        └── ts-formatter.md
```

---

## Decision Options

| Option | Description | Conformance | Recommendation |
|--------|-------------|-------------|----------------|
| **A** | Flat files: `agents/ts-parser.md` | ✓ Industry Standard | **RECOMMENDED** |
| B | Subdirectories: `agents/ts-parser/AGENT.md` | ✗ Non-standard | Not recommended |

---

## Evidence Summary

### Primary Evidence (Authoritative Sources)

1. **Claude Code Official Docs**: States agents are `.md` files at `agents/your-agent-name.md`
2. **Anthropic Engineering Blog**: Shows skills with flat agent files
3. **Context7 Query Results**: Official examples show `analyzer.md`, `reviewer.md` pattern

### Secondary Evidence (Industry Practice)

4. **Jerry Framework Existing Skills**: `ps-researcher.md`, `ps-analyst.md` pattern already used
5. **Community Guides**: Multiple sources confirm flat file pattern
6. **AGENTS.md Convention**: Industry-wide standard emerging for AI coding assistants

---

## Conclusion

**Option A (flat files)** is definitively the correct pattern based on:

1. Official Claude Code documentation
2. Anthropic Engineering best practices
3. Jerry Framework existing conventions
4. Industry-wide emerging standards

The Transcript Skill agents should be:
- `ts-parser.md` (not `ts-parser/AGENT.md`)
- `ts-extractor.md` (not `ts-extractor/AGENT.md`)
- `ts-formatter.md` (not `ts-formatter/AGENT.md`)

---

## Action Items

1. ✓ Research complete with evidence
2. → Present to user for confirmation
3. → Update DEC-002 with confirmed decision
4. → Create migration TASK in FEAT-002 to relocate files with correct naming

---

## Sources

### Primary Sources (Anthropic/Official)

- [Claude Code Official Documentation - Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Engineering - Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Blog - Skills explained](https://claude.com/blog/skills-explained)
- [Claude Code Docs - Create plugins](https://code.claude.com/docs/en/plugins)

### Secondary Sources (Industry)

- [AGENTS.md Convention](https://pnote.eu/notes/agents-md/)
- [Understanding Claude Code's Full Stack](https://alexop.dev/posts/understanding-claude-code-full-stack/)
- [Mastering Agentic Coding in Claude](https://medium.com/@lmpo/mastering-agentic-coding-in-claude-a-guide-to-skills-sub-agents-slash-commands-and-mcp-servers-5c58e03d4a35)
- [Claude Agent Skills Landing Guide](https://claudecn.com/en/blog/claude-agent-skills-landing-guide/)

### Context7 Research

- Library: `/anthropics/claude-code` - Official Claude Code documentation
- Library: `/affaan-m/everything-claude-code` - Best practices collection

---

*Discovery ID: DISC-004*
*Severity: HIGH*
*Status: DOCUMENTED*
*Research Method: Context7 + WebSearch + Jerry Framework Analysis*
