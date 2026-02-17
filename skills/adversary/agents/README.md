# Adversary Agents Directory

This directory contains Claude agent specifications for the `/adversary` skill.

## File Types

| Type | Files | Purpose |
|------|-------|---------|
| **Agent Specifications** | `adv-*.md` | Claude agent behavior definitions for strategy selection, execution, and scoring |
| **Template Files** | `.context/templates/adversarial/s-*.md` | Static strategy execution methodologies (separate directory) |

## Agent Responsibilities

- **Agent files** (`adv-*.md`) define agent behavior, context requirements, and output formats
- **Template files** (in `.context/templates/adversarial/`) define strategy execution methodology
- Agent files orchestrate workflow; templates define what to execute

## Available Agents

| Agent | Role |
|-------|------|
| `adv-selector.md` | Strategy selection by criticality level |
| `adv-executor.md` | Strategy template execution against deliverables |
| `adv-scorer.md` | S-014 LLM-as-Judge quality scoring |
