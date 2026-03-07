#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Transform agent .md files: official Claude Code frontmatter + governance YAML.

Usage: uv run python scripts/transform_agents.py [--dry-run]
"""

import re
import sys
from pathlib import Path

import yaml

AGENTS_ROOT = Path("skills")

EXCLUDE_FILES = {
    "README.md",
    "PS_AGENT_TEMPLATE.md",
    "PS_EXTENSION.md",
    "NSE_AGENT_TEMPLATE.md",
    "NSE_EXTENSION.md",
}

NATIVE_TOOLS = {
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
    "WebSearch",
    "WebFetch",
    "NotebookEdit",
}

MCP_C7 = ("mcp__context7__",)
MCP_MK = ("mcp__memory-keeper__", "mcp__memory_keeper__")


def _fix_mixed_yaml(text):
    """Fix invalid YAML where array items and mapping keys are mixed.

    Transcript agents have input_validation blocks like:
        input_validation:
          - pattern: "..."
            enforcement: hard
            rationale: "..."
          key: value  # <-- invalid: mixing array and mapping

    This removes the array items so the block parses as a pure mapping.
    """
    lines = text.splitlines()
    out = []
    skip = False
    for line in lines:
        stripped = line.lstrip()
        if skip:
            # Skip continuation lines of the array item (deeper indent)
            if stripped.startswith("enforcement:") or stripped.startswith("rationale:"):
                continue
            skip = False
        if stripped.startswith("- pattern:"):
            skip = True
            continue
        out.append(line)
    return "\n".join(out)


def parse_fm(content):
    if not content.startswith("---"):
        return None, content
    m = re.search(r"\n---\s*\n", content[3:])
    if not m:
        m = re.search(r"\n---\s*$", content[3:])
        if not m:
            return None, content
    end = m.start() + 3
    body = content[end + 1 + m.end() - m.start() :]
    raw = content[3 : end + 1]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        # Retry with mixed-array fix for transcript agents
        try:
            data = yaml.safe_load(_fix_mixed_yaml(raw))
        except yaml.YAMLError:
            return None, content
    return (data if isinstance(data, dict) else None), body


def build_official(data):
    o = {}
    o["name"] = data.get("name", "unknown")
    desc = data.get("description", "")
    o["description"] = " ".join(str(desc).split()) if desc else ""
    model = str(data.get("model", "sonnet")).split("#")[0].strip().strip('"').strip("'")
    o["model"] = model

    at = data.get("capabilities", {}).get("allowed_tools", [])
    native = [t for t in at if t in NATIVE_TOOLS and t != "Task"]
    if native:
        o["tools"] = ", ".join(native)

    servers = {}
    if any(any(str(t).startswith(p) for p in MCP_C7) for t in at):
        servers["context7"] = True
    if any(any(str(t).startswith(p) for p in MCP_MK) for t in at):
        servers["memory-keeper"] = True
    if servers:
        o["mcpServers"] = servers

    return o


def fix_cm(mode):
    return {
        "strategic": "convergent",
        "mixed": "integrative",
        "critical": "convergent",
        "communicative": "divergent",
    }.get(mode, mode)


def tier(at):
    s = {str(t) for t in at}
    if "Task" in s:
        return "T5"
    ext = any(t in ("WebSearch", "WebFetch") for t in s) or any(
        any(str(t).startswith(p) for p in MCP_C7) for t in s
    )
    mem = any(any(str(t).startswith(p) for p in MCP_MK) for t in s)
    if mem and ext:
        return "T5"
    if mem:
        return "T4"
    if ext:
        return "T3"
    if any(t in ("Write", "Edit", "Bash") for t in s):
        return "T2"
    return "T1"


def build_gov(data):
    g = {}
    if "version" in data:
        g["version"] = data["version"]
    at = data.get("capabilities", {}).get("allowed_tools", [])
    g["tool_tier"] = tier(at)

    if "identity" in data and isinstance(data["identity"], dict):
        ident = dict(data["identity"])
        if "cognitive_mode" in ident:
            ident["cognitive_mode"] = fix_cm(ident["cognitive_mode"])
        g["identity"] = ident

    for k in (
        "persona",
        "guardrails",
        "output",
        "constitution",
        "validation",
        "prior_art",
        "enforcement",
        "session_context",
        "portability",
    ):
        if k in data:
            g[k] = data[k]

    if "capabilities" in data and isinstance(data["capabilities"], dict):
        caps = {
            k: data["capabilities"][k]
            for k in ("forbidden_actions", "output_formats", "required_features")
            if k in data["capabilities"]
        }
        if caps:
            g["capabilities"] = caps

    skip = {
        "name",
        "description",
        "model",
        "version",
        "identity",
        "persona",
        "capabilities",
        "guardrails",
        "output",
        "constitution",
        "validation",
        "prior_art",
        "enforcement",
        "session_context",
        "portability",
        "tools",
        "disallowedTools",
        "permissionMode",
        "maxTurns",
        "skills",
        "mcpServers",
        "hooks",
        "memory",
        "background",
        "isolation",
    }
    for k in data:
        if k not in skip:
            g[k] = data[k]

    return g


def transform(path, dry_run=False):
    content = path.read_text(encoding="utf-8")
    data, body = parse_fm(content)
    if data is None or "name" not in data:
        return False, f"SKIP: {path}"

    official = build_official(data)
    governance = build_gov(data)

    if dry_run:
        return (
            True,
            f"DRY: {data['name']} tier={governance.get('tool_tier')} tools=[{official.get('tools', '')}]",
        )

    oy = yaml.dump(
        official, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
    ).rstrip("\n")
    path.write_text(f"---\n{oy}\n---\n{body}", encoding="utf-8")

    gp = path.with_suffix(".governance.yaml")
    gh = f"# Governance metadata for {data['name']}\n# Validated by: docs/schemas/agent-governance-v1.schema.json\n# Runtime config: {path.name}\n\n"
    gy = yaml.dump(
        governance, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
    )
    gp.write_text(gh + gy, encoding="utf-8")

    return True, f"OK: {data['name']}"


def main():
    dry = "--dry-run" in sys.argv
    results = []
    for d in sorted(AGENTS_ROOT.glob("*/agents/")):
        for f in sorted(d.glob("*.md")):
            if f.name in EXCLUDE_FILES:
                continue
            results.append(transform(f, dry))

    ok = sum(1 for r, _ in results if r)
    fail = sum(1 for r, _ in results if not r)
    print(f"\n{'DRY RUN ' if dry else ''}Complete: {ok} ok, {fail} fail, {len(results)} total")
    for r, m in results:
        print(f"  {'  ' if r else '!!'} {m}")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
