#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Create canonical composition files (.jerry.yaml + .jerry.prompt.md) for new agents.

Reads existing composed .md and .governance.yaml files, then generates canonical
.jerry.yaml and .jerry.prompt.md files in the composition directory.
"""

import os

import yaml

# Portable tool mapping (Claude Code name -> portable name)
TOOL_MAP = {
    "Read": "file_read",
    "Write": "file_write",
    "Edit": "file_edit",
    "Glob": "file_search_glob",
    "Grep": "file_search_content",
    "Bash": "shell_execute",
    "WebSearch": "web_search",
    "WebFetch": "web_fetch",
}

# Model tier mapping (Claude Code model -> portable tier)
MODEL_MAP = {
    "opus": "reasoning_high",
    "sonnet": "reasoning_standard",
    "haiku": "fast",
}

# Agents to process: (skill, agent_name)
AGENTS = [
    ("diataxis", "diataxis-auditor"),
    ("diataxis", "diataxis-classifier"),
    ("diataxis", "diataxis-explanation"),
    ("diataxis", "diataxis-howto"),
    ("diataxis", "diataxis-reference"),
    ("diataxis", "diataxis-tutorial"),
    ("prompt-engineering", "pe-builder"),
    ("prompt-engineering", "pe-constraint-gen"),
    ("prompt-engineering", "pe-scorer"),
]


def parse_frontmatter(md_content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from markdown content."""
    # Split on --- delimiters
    parts = md_content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Could not find YAML frontmatter delimiters")
    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()
    return frontmatter, body


def parse_tools(tools_field) -> list[str]:
    """Parse tools field from frontmatter (may be string or list)."""
    if isinstance(tools_field, str):
        return [t.strip() for t in tools_field.split(",")]
    if isinstance(tools_field, list):
        return tools_field
    return []


def build_jerry_yaml(name: str, skill: str, frontmatter: dict, gov_data: dict) -> str:
    """Build canonical .jerry.yaml content."""
    # Build the YAML structure manually for controlled ordering
    lines = [
        "# Canonical Agent Definition",
        "# Schema: docs/schemas/agent-canonical-v1.schema.json",
        "",
    ]

    # Top-level fields
    lines.append(f"name: {name}")
    version = gov_data.get("version", "0.1.0")
    if isinstance(version, str):
        lines.append(
            f'version: "{version}"' if not version.startswith('"') else f"version: {version}"
        )
    else:
        lines.append(f'version: "{version}"')

    # Description - use YAML block scalar for multi-line
    desc = frontmatter.get("description", "")
    if isinstance(desc, str) and len(desc) > 80:
        lines.append("description: >")
        # Wrap at ~80 chars
        words = desc.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > 90:
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
        lines.append(f"description: {desc}")

    lines.append(f"skill: {skill}")

    # Identity section
    identity = gov_data.get("identity", {})
    lines.append("identity:")
    lines.append(f"  role: {identity.get('role', 'Agent')}")
    expertise = identity.get("expertise", [])
    lines.append("  expertise:")
    for exp in expertise:
        lines.append(f"  - {exp}")
    lines.append(f"  cognitive_mode: {identity.get('cognitive_mode', 'systematic')}")
    if "model_justification" in identity:
        lines.append(f'  model_justification: "{identity["model_justification"]}"')

    # Persona section
    persona = gov_data.get("persona", {})
    lines.append("persona:")
    lines.append(f"  tone: {persona.get('tone', 'professional')}")
    lines.append(f"  communication_style: {persona.get('communication_style', 'structured')}")
    lines.append(f"  audience_level: {persona.get('audience_level', 'adaptive')}")

    # Model section (portable tier)
    model_name = frontmatter.get("model", "sonnet")
    model_tier = MODEL_MAP.get(model_name, "reasoning_standard")
    lines.append("model:")
    lines.append(f"  tier: {model_tier}")

    # Tools section (portable names)
    tools_raw = parse_tools(frontmatter.get("tools", ""))
    native_tools = []
    for t in tools_raw:
        if t in TOOL_MAP:
            native_tools.append(TOOL_MAP[t])
    lines.append("tools:")
    lines.append("  native:")
    for t in native_tools:
        lines.append(f"  - {t}")
    lines.append("  forbidden:")
    lines.append("  - agent_delegate")

    # Tool tier
    lines.append(f"tool_tier: {gov_data.get('tool_tier', 'T1')}")

    # Guardrails section
    guardrails = gov_data.get("guardrails", {})
    lines.append("guardrails:")
    input_val = guardrails.get("input_validation", [])
    lines.append("  input_validation:")
    for iv in input_val:
        if isinstance(iv, dict):
            for k, v in iv.items():
                lines.append(f"  - {k}: {v}")
        else:
            lines.append(f"  - {iv}")
    output_filter = guardrails.get("output_filtering", [])
    lines.append("  output_filtering:")
    for of in output_filter:
        lines.append(f"  - {of}")
    fb = guardrails.get("fallback_behavior", "warn_and_retry")
    lines.append(f"  fallback_behavior: {fb}")

    # Capabilities section
    capabilities = gov_data.get("capabilities", {})
    forbidden_actions = capabilities.get("forbidden_actions", [])
    if forbidden_actions:
        lines.append("capabilities:")
        lines.append("  forbidden_actions:")
        for fa in forbidden_actions:
            lines.append(f'  - "{fa}"')
        fa_format = capabilities.get("forbidden_action_format")
        if fa_format:
            lines.append(f"  forbidden_action_format: {fa_format}")

    # Output section
    output = gov_data.get("output", {})
    lines.append("output:")
    lines.append(f"  required: {str(output.get('required', True)).lower()}")
    if "location" in output:
        lines.append(f'  location: "{output["location"]}"')
    if "template" in output:
        lines.append(f'  template: "{output["template"]}"')
    levels = output.get("levels", ["L1"])
    lines.append("  levels:")
    for level in levels:
        lines.append(f"  - {level}")

    # Constitution section
    constitution = gov_data.get("constitution", {})
    lines.append("constitution:")
    lines.append(
        f"  reference: {constitution.get('reference', 'docs/governance/JERRY_CONSTITUTION.md')}"
    )
    principles = constitution.get("principles_applied", [])
    lines.append("  principles_applied:")
    for p in principles:
        lines.append(f"  - '{p}'")
    const_fa = constitution.get("forbidden_actions")
    if const_fa:
        lines.append("  forbidden_actions:")
        for fa in const_fa:
            lines.append(f"  - {fa}")

    # Validation section
    validation = gov_data.get("validation", {})
    lines.append("validation:")
    if "file_must_exist" in validation:
        lines.append(f"  file_must_exist: {str(validation['file_must_exist']).lower()}")
    checks = validation.get("post_completion_checks", [])
    if checks:
        lines.append("  post_completion_checks:")
        for c in checks:
            lines.append(f"  - {c}")

    # Enforcement section
    enforcement = gov_data.get("enforcement", {})
    if enforcement:
        lines.append("enforcement:")
        lines.append(f"  tier: {enforcement.get('tier', 'medium')}")
        if "escalation_path" in enforcement:
            lines.append(f"  escalation_path: {enforcement['escalation_path']}")

    # Session context section
    session_ctx = gov_data.get("session_context", {})
    if session_ctx:
        lines.append("session_context:")
        on_receive = session_ctx.get("on_receive", {})
        if on_receive:
            lines.append("  on_receive:")
            if isinstance(on_receive, dict):
                for k, v in on_receive.items():
                    lines.append(f'    {k}: "{v}"')
            elif isinstance(on_receive, list):
                for item in on_receive:
                    lines.append(f"  - {item}")
        on_send = session_ctx.get("on_send", {})
        if on_send:
            lines.append("  on_send:")
            if isinstance(on_send, dict):
                for k, v in on_send.items():
                    lines.append(f'    {k}: "{v}"')
            elif isinstance(on_send, list):
                for item in on_send:
                    lines.append(f"  - {item}")

    lines.append("")  # trailing newline
    return "\n".join(lines)


def build_prompt_md(name: str, body: str) -> str:
    """Build canonical .jerry.prompt.md content."""
    # Remove stray closing tags at the end (known issue)
    body = body.rstrip()
    if body.endswith("</output>"):
        body = body[: -len("</output>")].rstrip()
    return f"# {name} System Prompt\n\n{body}\n"


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    for skill, name in AGENTS:
        md_path = f"skills/{skill}/agents/{name}.md"
        gov_path = f"skills/{skill}/agents/{name}.governance.yaml"
        comp_dir = f"skills/{skill}/composition"

        print(f"Processing {name}...")

        # Read source files
        with open(md_path) as f:
            md_content = f.read()
        with open(gov_path) as f:
            gov_content = f.read()

        # Parse
        frontmatter, body = parse_frontmatter(md_content)
        gov_data = yaml.safe_load(gov_content)

        # Generate .jerry.yaml
        jerry_yaml = build_jerry_yaml(name, skill, frontmatter, gov_data)
        yaml_path = f"{comp_dir}/{name}.jerry.yaml"
        with open(yaml_path, "w") as f:
            f.write(jerry_yaml)
        print(f"  Created {yaml_path}")

        # Generate .jerry.prompt.md
        prompt_md = build_prompt_md(name, body)
        prompt_path = f"{comp_dir}/{name}.jerry.prompt.md"
        with open(prompt_path, "w") as f:
            f.write(prompt_md)
        print(f"  Created {prompt_path}")

    print(f"\nDone! Created {len(AGENTS) * 2} files.")


if __name__ == "__main__":
    main()
