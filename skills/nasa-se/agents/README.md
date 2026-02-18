# NASA-SE Agents Directory

This directory contains agent instruction files and supporting templates for the NASA Systems Engineering skill.

## File Types

| Pattern | Purpose |
|---------|---------|
| `nse-*.md` | Agent instruction files (loaded by Task tool) |
| `NSE_AGENT_TEMPLATE.md` | Template for creating new NSE agents |
| `NSE_EXTENSION.md` | Shared agent extensions (NPR 7123.1D processes, output formats) |

Agent instruction files define the agent's identity, capabilities, guardrails, and output format. They are loaded as prompts when the main context invokes an agent via the Task tool.

Template and extension files are reference documents — they are not invoked directly.
