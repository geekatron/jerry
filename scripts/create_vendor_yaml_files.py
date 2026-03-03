#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Generate .claude-code.yaml vendor files for all agents.

Reads frontmatter from composed agent .md files in skills/*/agents/
and generates .claude-code.yaml files in skills/*/composition/.

Usage:
    uv run python scripts/create_vendor_yaml_files.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"


def parse_frontmatter(md_path: Path) -> dict[str, object]:
    """Extract YAML frontmatter from a markdown file as a dict."""
    text = md_path.read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm: dict[str, object] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        # Key: value
        kv_match = re.match(r"^(\w+):\s*(.*)", line)
        if not kv_match:
            i += 1
            continue

        key = kv_match.group(1)
        value = kv_match.group(2).strip()

        # Check if this is a multi-line value (mapping or list)
        if value == "":
            # Could be a mapping or list — look ahead
            sub: dict[str, object] = {}
            i += 1
            while i < len(lines):
                sub_line = lines[i]
                if sub_line.startswith("  "):
                    # Sub-item
                    sub_match = re.match(r"^\s+(\w[\w-]*):\s*(.*)", sub_line)
                    if sub_match:
                        sub[sub_match.group(1)] = sub_match.group(2).strip()
                    i += 1
                else:
                    break
            fm[key] = sub if sub else ""
            continue
        elif value == ">-" or value == ">":
            # Folded scalar — collect continuation lines
            parts = []
            i += 1
            while i < len(lines):
                if lines[i].startswith("  "):
                    parts.append(lines[i].strip())
                    i += 1
                else:
                    break
            fm[key] = " ".join(parts)
            continue
        elif value.startswith("[") and value.endswith("]"):
            # Inline list
            inner = value[1:-1]
            items = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
            fm[key] = items
        elif value.startswith('"') and value.endswith('"'):
            fm[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            fm[key] = value[1:-1]
        elif value in ("true", "True"):
            fm[key] = True
        elif value in ("false", "False"):
            fm[key] = False
        elif value.isdigit():
            fm[key] = int(value)
        else:
            fm[key] = value

        i += 1

    return fm


def format_tools(tools: object) -> str:
    """Format tools list for YAML output."""
    if isinstance(tools, list):
        return "[" + ", ".join(tools) + "]"
    if isinstance(tools, str):
        return tools
    return "[]"


def format_mcp_servers(mcp: object) -> str | None:
    """Format mcpServers block. Returns None if empty."""
    if isinstance(mcp, dict) and mcp:
        lines = ["mcpServers:"]
        for k, v in mcp.items():
            val = "true" if v is True or v == "true" else str(v)
            lines.append(f"  {k}: {val}")
        return "\n".join(lines)
    return None


def generate_vendor_yaml(fm: dict[str, object], agent_name: str) -> str:
    """Generate .claude-code.yaml content from frontmatter."""
    lines = [
        f"# Claude Code vendor configuration for {agent_name}",
        "# Layer 4 of 4: per-agent vendor-specific overrides.",
        "# Reference: https://docs.anthropic.com/en/docs/claude-code/agent-tool",
        "",
    ]

    # name
    name = fm.get("name", agent_name)
    lines.append(f"name: {name}")

    # description — use folded scalar if multiline
    desc = fm.get("description", "")
    if isinstance(desc, str) and desc:
        if len(desc) > 80:
            lines.append("description: >-")
            # Wrap at ~78 chars
            words = desc.split()
            current_line = "  "
            for word in words:
                if len(current_line) + len(word) + 1 > 80:
                    lines.append(current_line)
                    current_line = "  " + word
                else:
                    if current_line == "  ":
                        current_line += word
                    else:
                        current_line += " " + word
            if current_line.strip():
                lines.append(current_line)
        else:
            lines.append(f'description: "{desc}"')
    else:
        lines.append("# description:")

    # model
    model = fm.get("model")
    if model:
        lines.append(f"model: {model}")
    else:
        lines.append("# model:")

    # tools
    tools = fm.get("tools")
    if tools:
        lines.append(f"tools: {format_tools(tools)}")
    else:
        lines.append("# tools:")

    # disallowedTools
    disallowed = fm.get("disallowedTools")
    if disallowed:
        lines.append(f"disallowedTools: {format_tools(disallowed)}")
    else:
        lines.append("# disallowedTools:")

    # mcpServers
    mcp = fm.get("mcpServers")
    mcp_block = format_mcp_servers(mcp)
    if mcp_block:
        lines.append(mcp_block)
    else:
        lines.append("# mcpServers:")

    # permissionMode
    pm = fm.get("permissionMode")
    if pm:
        lines.append(f"permissionMode: {pm}")
    else:
        lines.append("permissionMode: default")

    # background
    bg = fm.get("background")
    if bg is True:
        lines.append("background: true")
    else:
        lines.append("background: false")

    # Commented-out fields that are rarely used
    lines.append("# maxTurns:")
    lines.append("# skills:")
    lines.append("# hooks:")
    lines.append("# memory:")
    lines.append("# isolation:")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    """Generate .claude-code.yaml for all agents."""
    created = 0
    errors = []

    for agents_dir in sorted(SKILLS_DIR.glob("*/agents")):
        skill_name = agents_dir.parent.name
        comp_dir = agents_dir.parent / "composition"

        if not comp_dir.exists():
            errors.append(f"No composition dir for skill {skill_name}")
            continue

        for md_file in sorted(agents_dir.glob("*.md")):
            agent_name = md_file.stem
            fm = parse_frontmatter(md_file)

            if not fm:
                errors.append(f"No frontmatter in {md_file}")
                continue

            yaml_content = generate_vendor_yaml(fm, agent_name)
            out_path = comp_dir / f"{agent_name}.claude-code.yaml"
            out_path.write_text(yaml_content)
            created += 1
            print(f"  Created: {out_path.relative_to(ROOT)}")

    print(f"\nCreated {created} .claude-code.yaml files")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
