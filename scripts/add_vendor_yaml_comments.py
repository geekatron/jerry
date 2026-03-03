#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Add inline documentation comments to all .claude-code.yaml vendor files.

Rewrites each file preserving its values but adding explanatory comments
for every property, including valid options and Jerry-specific guidance.
"""

from __future__ import annotations

from pathlib import Path

import yaml

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"


def _render(agent_name: str, data: dict) -> str:
    """Render a fully commented .claude-code.yaml file."""
    lines: list[str] = []

    # Header
    lines.append(f"# Claude Code vendor overrides for: {agent_name}")
    lines.append("#")
    lines.append("# Layer 4 of 4 in the compose pipeline merge hierarchy:")
    lines.append("#   1. jerry-agent-defaults.yaml     (governance defaults)")
    lines.append("#   2. jerry-claude-code-defaults.yaml (vendor defaults)")
    lines.append("#   3. {agent}.jerry.yaml             (canonical agent config)")
    lines.append("#   4. THIS FILE                      (per-agent vendor overrides)")
    lines.append("#")
    lines.append("# Only set values here that DIFFER from the defaults in layers 1-3.")
    lines.append("# Commented-out fields show available options; uncomment to override.")
    lines.append("#")
    lines.append("# Spec: https://docs.anthropic.com/en/docs/claude-code/agent-tool")
    lines.append("")

    # --- name ---
    lines.append("# Agent identifier. Must match the .jerry.yaml `name` field.")
    name = data.get("name", agent_name)
    lines.append(f"name: {name}")
    lines.append("")

    # --- description ---
    lines.append("# When Claude should delegate to this agent.")
    lines.append("# Used for routing — be specific about WHAT, WHEN, and trigger keywords.")
    desc = data.get("description", "")
    if desc:
        lines.append("description: >-")
        # Wrap description at ~78 chars with 2-space indent
        words = desc.split()
        current_line = ""
        for word in words:
            if current_line and len(current_line) + len(word) + 1 > 76:
                lines.append("  " + current_line)
                current_line = word
            elif current_line:
                current_line += " " + word
            else:
                current_line = word
        if current_line:
            lines.append("  " + current_line)
    else:
        lines.append(f"description: '{agent_name} agent'")
    lines.append("")

    # --- model ---
    lines.append("# LLM model for this agent.")
    lines.append("#   opus   — complex reasoning, research, architecture, synthesis")
    lines.append("#   sonnet — balanced analysis, standard production tasks (default)")
    lines.append("#   haiku  — fast repetitive tasks, formatting, validation")
    model = data.get("model", "sonnet")
    lines.append(f"model: {model}")
    lines.append("")

    # --- tools ---
    lines.append("# Allowed tools. Comma-separated string or YAML array.")
    lines.append("# IMPORTANT: If omitted, agent INHERITS ALL tools (unsafe for workers).")
    lines.append("# Available tools: Read, Write, Edit, Glob, Grep, Bash,")
    lines.append("#   WebSearch, WebFetch, Task (T5 orchestrators only)")
    lines.append("# Jerry tool tiers: T1=Read-only, T2=Read-Write, T3=External,")
    lines.append("#   T4=Persistent (MCP), T5=Full (Task). Use lowest tier needed.")
    tools = data.get("tools", "")
    if tools:
        lines.append(f"tools: {tools}")
    else:
        lines.append("# tools:")
    lines.append("")

    # --- disallowedTools ---
    lines.append("# Tools to explicitly deny. Comma-separated string or YAML array.")
    lines.append("# Use when inheriting a broad set but need to block specific tools.")
    disallowed = data.get("disallowedTools")
    if disallowed:
        lines.append(f"disallowedTools: {disallowed}")
    else:
        lines.append("# disallowedTools:")
    lines.append("")

    # --- mcpServers ---
    lines.append("# MCP servers available to this agent. Object format: {name: true}")
    lines.append("# Available servers: context7 (library docs), memory-keeper (persistence)")
    lines.append("# Only enable servers the agent actually needs per mcp-tool-standards.md.")
    mcp = data.get("mcpServers")
    if mcp and isinstance(mcp, dict):
        lines.append("mcpServers:")
        for server_name, enabled in mcp.items():
            lines.append(f"  {server_name}: {str(enabled).lower()}")
    else:
        lines.append("# mcpServers:")
        lines.append("#   context7: true")
        lines.append("#   memory-keeper: true")
    lines.append("")

    # --- permissionMode ---
    lines.append("# How the agent handles tool permissions.")
    lines.append("#   default          — prompt user for each tool call (safest)")
    lines.append("#   acceptEdits      — auto-approve file edits, prompt for others")
    lines.append("#   dontAsk          — auto-approve most tools")
    lines.append("#   bypassPermissions — skip all permission checks (use with caution)")
    lines.append("#   plan             — planning mode only, no tool execution")
    perm = data.get("permissionMode", "default")
    lines.append(f"permissionMode: {perm}")
    lines.append("")

    # --- background ---
    lines.append("# Run as a background task (true) or foreground (false).")
    lines.append("# Background agents return immediately; check output later.")
    bg = data.get("background", False)
    lines.append(f"background: {str(bg).lower()}")
    lines.append("")

    # --- maxTurns ---
    lines.append("# Maximum agentic turns (API round-trips) before stopping.")
    lines.append("# Omit to use the system default. Set to limit runaway agents.")
    max_turns = data.get("maxTurns")
    if max_turns:
        lines.append(f"maxTurns: {max_turns}")
    else:
        lines.append("# maxTurns:")
    lines.append("")

    # --- skills ---
    lines.append("# Skills to preload into this agent's context.")
    lines.append("# Array of skill names. Only use for agents that need skill knowledge.")
    skills = data.get("skills")
    if skills:
        lines.append("skills:")
        for s in skills:
            lines.append(f"  - {s}")
    else:
        lines.append("# skills:")
    lines.append("")

    # --- hooks ---
    lines.append("# Lifecycle hooks — shell commands triggered by agent events.")
    lines.append("# Format: {event: [{command: '...', timeout: N}]}")
    lines.append("# Events: PreToolUse, PostToolUse, Notification, Stop")
    hooks = data.get("hooks")
    if hooks:
        lines.append("hooks:")
        lines.append(f"  {yaml.dump(hooks, default_flow_style=False).strip()}")
    else:
        lines.append("# hooks:")
    lines.append("")

    # --- memory ---
    lines.append("# Memory scope for this agent's CLAUDE.md loading.")
    lines.append("#   user    — load user-level CLAUDE.md")
    lines.append("#   project — load project-level CLAUDE.md")
    lines.append("#   local   — load local directory CLAUDE.md")
    memory = data.get("memory")
    if memory:
        lines.append(f"memory: {memory}")
    else:
        lines.append("# memory:")
    lines.append("")

    # --- isolation ---
    lines.append("# Isolation mode for the agent's execution environment.")
    lines.append("#   worktree — run in a temporary git worktree (isolated file changes)")
    isolation = data.get("isolation")
    if isolation:
        lines.append(f"isolation: {isolation}")
    else:
        lines.append("# isolation:")

    return "\n".join(lines) + "\n"


def main() -> None:
    """Rewrite all .claude-code.yaml files with documentation comments."""
    count = 0
    for yaml_file in sorted(SKILLS_DIR.rglob("*.claude-code.yaml")):
        content = yaml_file.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
        agent_name = data.get("name", yaml_file.stem.replace(".claude-code", ""))

        commented = _render(agent_name, data)
        yaml_file.write_text(commented, encoding="utf-8")
        count += 1
        print(f"  {yaml_file.relative_to(SKILLS_DIR.parent)}")

    print(f"\nDone. Updated {count} files.")


if __name__ == "__main__":
    main()
