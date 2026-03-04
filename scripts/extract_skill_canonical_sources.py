#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Migration script: Extract canonical source files from existing SKILL.md.

For each skill with a skill.jerry.yaml:
  1. Parse SKILL.md frontmatter and body
  2. Add 'description' to skill.jerry.yaml (if not already present)
  3. Create skill.claude-code.yaml with allowed-tools and other vendor fields
  4. Create skill.jerry.prompt.md with body content (governance sections stripped)

Governance sections (## Skill Version, ## Activation Keywords, etc.) are
stripped from the prompt body since the compose pipeline re-generates them.

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILLS_DIR = _REPO_ROOT / "skills"

# Footer pattern (mirrors compose handler)
_FOOTER_RE = re.compile(r"^\*{0,2}Skill Version:.*$", re.MULTILINE)

# Italic footer lines — governance metadata that the compose pipeline preserves
# but should NOT be in the canonical prompt source.
# Patterns: *Skill Version: ...*, *Constitutional Compliance: ...*, *SSOT: ...*,
#           *Created: ...*, *Source: ...*, *Agent: ...*
_ITALIC_FOOTER_RE = re.compile(
    r"^\*(?:Skill Version|Constitutional Compliance|SSOT|Created|Source|Agent|Standards Version"
    r"|Canonical Source):.*\*$"
)

# Blockquote header lines — governance metadata like:
#   > **Version:** 1.0.0
#   > **Framework:** Jerry Adversarial Quality (ADV)
#   > **Constitutional Compliance:** Jerry Constitution v1.0
_BLOCKQUOTE_GOVERNANCE_KEYS = {
    "Version",
    "Framework",
    "Constitutional Compliance",
    "SSOT Reference",
    "SSOT",
    "Canonical Source",
}
_BLOCKQUOTE_GOV_RE = re.compile(
    r"^>\s*\*\*(" + "|".join(re.escape(k) for k in _BLOCKQUOTE_GOVERNANCE_KEYS) + r"):\*\*"
)

# Governance sections to strip from prompt body
_GOVERNANCE_HEADINGS = {
    "Skill Version",
    "Activation Keywords",
    "Agent Registry",
    "Context Injection",
}

_GOVERNANCE_XML_TAGS = {
    "skill_version",
    "activation_keywords",
    "agent_registry",
    "context_injection",
}

# Fields that belong in skill.jerry.yaml (NOT in skill.claude-code.yaml)
_JERRY_FIELDS = {
    "name",
    "version",
    "activation-keywords",
    "agents",
    "context_injection",
    "license",
    "compatibility",
    "metadata",
    "description",
}

# Fields that belong in skill.claude-code.yaml (vendor-specific runtime)
_VENDOR_FIELDS = {
    "allowed-tools",
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "model",
    "context",
    "agent",
    "hooks",
}


def parse_skill_md(content: str) -> tuple[dict, str]:
    """Parse SKILL.md into frontmatter dict and body string."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_text = content[4:end]
    body = content[end + 4 :].lstrip("\n")

    try:
        fm_data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm_data = {}

    return fm_data, body


def strip_governance_sections(body: str) -> str:
    """Strip governance sections from body for canonical prompt source.

    Removes:
    - ## Heading format governance sections (Skill Version, Activation Keywords, etc.)
    - <xml_tag> format governance sections
    - Blockquote header lines (> **Version:** ..., > **Framework:** ..., etc.)
    - Italic footer lines (*Skill Version: ...*, *Constitutional Compliance: ...*, etc.)
    - Horizontal rules (---) that are left orphaned after stripping
    """
    lines = body.split("\n")
    result_lines: list[str] = []
    in_governance_heading = False
    in_governance_xml = False
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if not in_governance_heading and not in_governance_xml:
                result_lines.append(line)
            continue

        if in_code_block:
            if not in_governance_heading and not in_governance_xml:
                result_lines.append(line)
            continue

        # Strip blockquote governance header lines (> **Version:** ...)
        if _BLOCKQUOTE_GOV_RE.match(stripped):
            continue

        # Strip italic footer lines (*Skill Version: ...*)
        if _ITALIC_FOOTER_RE.match(stripped):
            continue

        # Check for ## heading
        heading_match = re.match(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", line)
        if heading_match:
            heading_text = heading_match.group(1).strip()
            if heading_text in _GOVERNANCE_HEADINGS:
                in_governance_heading = True
                continue
            else:
                in_governance_heading = False
                result_lines.append(line)
                continue

        # Check for XML governance opening tags
        is_xml_open = False
        for tag in _GOVERNANCE_XML_TAGS:
            if stripped == f"<{tag}>" or re.match(rf"<{tag}\s", stripped):
                is_xml_open = True
                break
        if is_xml_open:
            in_governance_xml = True
            continue

        # Check for XML governance closing tags
        is_xml_close = False
        for tag in _GOVERNANCE_XML_TAGS:
            if stripped == f"</{tag}>":
                is_xml_close = True
                break
        if is_xml_close:
            in_governance_xml = False
            continue

        # Footer pattern terminates governance heading section
        if in_governance_heading and _FOOTER_RE.match(stripped):
            in_governance_heading = False

        if in_governance_heading:
            continue

        if in_governance_xml:
            continue

        result_lines.append(line)

    # Clean up trailing blank lines from stripped sections
    result = "\n".join(result_lines)
    # Collapse 3+ newlines to 2
    result = re.sub(r"\n{3,}", "\n\n", result)
    # Strip trailing --- that may be orphaned after footer removal
    result = re.sub(r"\n---\s*$", "", result)
    return result.rstrip("\n") + "\n"


def migrate_skill(
    skill_name: str, dry_run: bool = False, force_prompt: bool = False
) -> dict[str, str]:
    """Migrate a single skill to canonical source files.

    Args:
        skill_name: Skill directory name.
        dry_run: If True, report what would change without writing.
        force_prompt: If True, re-strip existing skill.jerry.prompt.md files.

    Returns:
        Dict with migration actions taken.
    """
    skill_dir = _SKILLS_DIR / skill_name
    comp_dir = skill_dir / "composition"
    yaml_path = comp_dir / "skill.jerry.yaml"
    skill_md_path = skill_dir / "SKILL.md"

    actions: dict[str, str] = {}

    if not yaml_path.exists():
        actions["error"] = f"No skill.jerry.yaml found at {yaml_path}"
        return actions

    if not skill_md_path.exists():
        actions["error"] = f"No SKILL.md found at {skill_md_path}"
        return actions

    # Parse existing files
    yaml_content = yaml_path.read_text(encoding="utf-8")
    yaml_data = yaml.safe_load(yaml_content)
    if not isinstance(yaml_data, dict):
        actions["error"] = "skill.jerry.yaml is not a YAML mapping"
        return actions

    skill_md_content = skill_md_path.read_text(encoding="utf-8")
    frontmatter, body = parse_skill_md(skill_md_content)

    # 1. Add description to skill.jerry.yaml
    description = frontmatter.get("description", "")
    if description and "description" not in yaml_data:
        # Insert description after version field
        # We manipulate the raw YAML string to preserve existing formatting
        insertion_done = False
        yaml_lines = yaml_content.split("\n")
        new_lines: list[str] = []
        for _i, line in enumerate(yaml_lines):
            new_lines.append(line)
            if line.startswith("version:") and not insertion_done:
                # Add description after version
                # Escape the description for YAML (use literal block for multiline)
                if "\n" in description:
                    new_lines.append("description: |-")
                    for desc_line in description.split("\n"):
                        new_lines.append(f"  {desc_line}")
                else:
                    # Use quoted style for single-line to handle special chars
                    escaped = description.replace('"', '\\"')
                    new_lines.append(f'description: "{escaped}"')
                insertion_done = True
                actions["yaml_description"] = f"Added description ({len(description)} chars)"

        if insertion_done and not dry_run:
            yaml_path.write_text("\n".join(new_lines), encoding="utf-8")
    elif description and "description" in yaml_data:
        actions["yaml_description"] = "Already present"
    else:
        actions["yaml_description"] = "No description in SKILL.md frontmatter"

    # 2. Create skill.claude-code.yaml with vendor fields
    vendor_path = comp_dir / "skill.claude-code.yaml"
    vendor_fields: dict[str, object] = {}
    for key, value in frontmatter.items():
        if key in _VENDOR_FIELDS and value:
            vendor_fields[key] = value

    if vendor_fields:
        if not vendor_path.exists():
            vendor_yaml = yaml.dump(
                vendor_fields,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=float("inf"),
            )
            # Add header comment
            header = f"# Claude Code vendor overrides for: {skill_name}\n"
            if not dry_run:
                vendor_path.write_text(header + vendor_yaml, encoding="utf-8")
            actions["claude_code_yaml"] = f"Created with {list(vendor_fields.keys())}"
        else:
            actions["claude_code_yaml"] = "Already exists"
    else:
        actions["claude_code_yaml"] = "No vendor fields to extract"

    # 3. Create or re-strip skill.jerry.prompt.md with body content (governance stripped)
    prompt_md_path = comp_dir / "skill.jerry.prompt.md"
    if not prompt_md_path.exists():
        prompt_body = strip_governance_sections(body)
        if not dry_run:
            prompt_md_path.write_text(prompt_body, encoding="utf-8")
        actions["prompt_md"] = f"Created ({len(prompt_body)} chars)"
    elif force_prompt:
        # Re-strip existing file to remove governance patterns missed earlier
        existing = prompt_md_path.read_text(encoding="utf-8")
        cleaned = strip_governance_sections(existing)
        if cleaned != existing:
            if not dry_run:
                prompt_md_path.write_text(cleaned, encoding="utf-8")
            actions["prompt_md"] = f"Re-stripped ({len(existing)} -> {len(cleaned)} chars)"
        else:
            actions["prompt_md"] = "Already clean"
    else:
        actions["prompt_md"] = "Already exists"

    return actions


def main() -> int:
    """Run migration on all skills with skill.jerry.yaml."""
    dry_run = "--dry-run" in sys.argv
    force_prompt = "--force-prompt" in sys.argv

    if dry_run:
        print("DRY RUN — no files will be written\n")
    if force_prompt:
        print("FORCE PROMPT — re-stripping existing skill.jerry.prompt.md files\n")

    migrated = 0
    errors = 0

    for skill_dir in sorted(_SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        yaml_path = skill_dir / "composition" / "skill.jerry.yaml"
        if not yaml_path.exists():
            continue

        skill_name = skill_dir.name
        print(f"--- {skill_name} ---")

        actions = migrate_skill(skill_name, dry_run=dry_run, force_prompt=force_prompt)

        if "error" in actions:
            print(f"  ERROR: {actions['error']}")
            errors += 1
        else:
            for key, value in actions.items():
                print(f"  {key}: {value}")
            migrated += 1

        print()

    print(f"\nSummary: {migrated} skills migrated, {errors} errors")
    if dry_run:
        print("(dry run — no files written)")

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
