# Problem-Solving Agents Directory

This directory contains agent instruction files and supporting templates for the problem-solving skill.

## File Types

| Pattern | Purpose |
|---------|---------|
| `ps-*.md` | Agent instruction files (loaded by Task tool) |
| `PS_AGENT_TEMPLATE.md` | Template for creating new PS agents |
| `PS_EXTENSION.md` | Shared agent extensions (cognitive modes, output formats) |

Agent instruction files define the agent's identity, capabilities, guardrails, and output format. They are loaded as prompts when the main context invokes an agent via the Task tool.

Template and extension files are reference documents — they are not invoked directly.
