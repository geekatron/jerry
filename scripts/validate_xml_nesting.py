#!/usr/bin/env -S uv run python

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Validate XML nesting in composed agent .md and SKILL.md files.

Checks:
  XN-001: Agent files with body_format=xml have <agent> wrapper
  XN-002: Every opening <tag> has exactly one matching </tag>
  XN-003: No duplicate opening tags (outside code blocks)
  XN-004: No orphaned closing tags
  XN-005: SKILL.md governance XML tags present when canonical source declares them
  XN-006: SKILL.md XML tags are well-formed (opening + closing match)

Exit 0 if all files pass, exit 1 otherwise.

References:
    - PROJ-012: Skill Composition Pipeline
    - Phase 4: XML Structural Validation
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Root of the repository
_REPO_ROOT = Path(__file__).resolve().parent.parent
_SKILLS_DIR = _REPO_ROOT / "skills"

# Tags used in agent .md bodies
_AGENT_WRAPPER_TAG = "agent"

# Known semantic section tags in agent definitions
_KNOWN_AGENT_TAGS = {
    "agent",
    "identity",
    "persona",
    "purpose",
    "input",
    "capabilities",
    "guardrails",
    "methodology",
    "output",
    "constitution",
    "execution_process",
    # Governance tags injected by compose pipeline
    "agent_version",
    "tool_tier",
    "enforcement",
    "portability",
    "prior_art",
    "session_context",
}

# Governance tag mappings for SKILL.md (field_key -> xml_tag)
_SKILL_GOVERNANCE_TAGS = {
    "version": "skill_version",
    "activation-keywords": "activation_keywords",
    "agents": "agent_registry",
    "context_injection": "context_injection",
}

# HTML void elements — self-closing, never have matching </tag>
_HTML_VOID_ELEMENTS = {
    "br",
    "hr",
    "img",
    "input",
    "meta",
    "link",
    "area",
    "base",
    "col",
    "embed",
    "source",
    "track",
    "wbr",
}

# Regex to match XML-like tags, excluding code blocks and self-closing tags
# Negative lookbehind (?<!/) prevents matching self-closing <tag /> as opening
_OPEN_TAG_RE = re.compile(r"<([a-z_]+)(?:\s[^>]*)?(?<!/)>")
_CLOSE_TAG_RE = re.compile(r"</([a-z_]+)>")

# Code block detection
_CODE_FENCE_RE = re.compile(r"^```")


def _strip_code_blocks(content: str) -> str:
    """Remove fenced code blocks from content to avoid false positives.

    Args:
        content: Full file content.

    Returns:
        Content with fenced code blocks replaced by empty lines.
    """
    lines = content.split("\n")
    result: list[str] = []
    in_code_block = False

    for line in lines:
        if _CODE_FENCE_RE.match(line.strip()):
            in_code_block = not in_code_block
            result.append("")
            continue
        if in_code_block:
            result.append("")
        else:
            result.append(line)

    return "\n".join(result)


def _strip_inline_code(content: str) -> str:
    """Remove inline code spans to avoid false positives.

    Args:
        content: Content (already stripped of code blocks).

    Returns:
        Content with inline code spans removed.
    """
    return re.sub(r"`[^`]+`", "", content)


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from .md file.

    Args:
        content: Full .md file content.

    Returns:
        Tuple of (frontmatter_dict, body_string).
    """
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


def _get_body_format(skill_name: str, agent_name: str) -> str:
    """Read body_format from canonical .jerry.yaml source.

    Args:
        skill_name: Skill directory name.
        agent_name: Agent name (without .md extension).

    Returns:
        Body format string ("xml", "markdown", etc.) or empty string.
    """
    yaml_path = _SKILLS_DIR / skill_name / "composition" / f"{agent_name}.jerry.yaml"
    if not yaml_path.exists():
        return ""

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            portability = data.get("portability", {})
            if isinstance(portability, dict):
                return str(portability.get("body_format", ""))
    except (yaml.YAMLError, OSError):
        pass

    return ""


def _get_skill_governance_fields(skill_name: str) -> dict:
    """Read governance fields from skill.jerry.yaml canonical source.

    Args:
        skill_name: Skill directory name.

    Returns:
        Dict with canonical governance fields.
    """
    yaml_path = _SKILLS_DIR / skill_name / "composition" / "skill.jerry.yaml"
    if not yaml_path.exists():
        return {}

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (yaml.YAMLError, OSError):
        pass

    return {}


class ValidationResult:
    """Collects validation findings for a single file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def validate_agent_xml(file_path: Path, skill_name: str, agent_name: str) -> ValidationResult:
    """Validate XML nesting in a composed agent .md file.

    Args:
        file_path: Path to the composed agent .md file.
        skill_name: Skill directory name.
        agent_name: Agent name.

    Returns:
        ValidationResult with errors and warnings.
    """
    rel_path = str(file_path.relative_to(_REPO_ROOT))
    result = ValidationResult(rel_path)

    body_format = _get_body_format(skill_name, agent_name)
    if body_format != "xml":
        # Skip XML validation for non-xml agents
        return result

    content = file_path.read_text(encoding="utf-8")
    _, body = _parse_frontmatter(content)

    # Strip code blocks and inline code to avoid false positives
    clean_body = _strip_inline_code(_strip_code_blocks(body))

    # XN-001: Agent wrapper tag
    open_agents = [t for t in _OPEN_TAG_RE.findall(clean_body) if t not in _HTML_VOID_ELEMENTS]
    close_agents = [t for t in _CLOSE_TAG_RE.findall(clean_body) if t not in _HTML_VOID_ELEMENTS]

    if _AGENT_WRAPPER_TAG not in open_agents:
        result.errors.append(f"[XN-001] Missing <{_AGENT_WRAPPER_TAG}> wrapper tag")
    if _AGENT_WRAPPER_TAG not in close_agents:
        result.errors.append(f"[XN-001] Missing </{_AGENT_WRAPPER_TAG}> closing tag")

    # XN-002: Every opening tag has matching closing tag
    open_counts: dict[str, int] = {}
    close_counts: dict[str, int] = {}

    for tag in open_agents:
        open_counts[tag] = open_counts.get(tag, 0) + 1
    for tag in close_agents:
        close_counts[tag] = close_counts.get(tag, 0) + 1

    all_tags = set(open_counts.keys()) | set(close_counts.keys())
    for tag in sorted(all_tags):
        opens = open_counts.get(tag, 0)
        closes = close_counts.get(tag, 0)

        if opens > 0 and closes == 0:
            result.errors.append(f"[XN-004] Orphaned opening tag <{tag}> with no matching </{tag}>")
        elif closes > 0 and opens == 0:
            result.errors.append(f"[XN-004] Orphaned closing tag </{tag}> with no matching <{tag}>")
        elif opens != closes:
            result.errors.append(
                f"[XN-002] Tag mismatch: <{tag}> opens {opens} time(s) "
                f"but </{tag}> closes {closes} time(s)"
            )

    # XN-003: No duplicate opening tags for known structural tags
    for tag in sorted(_KNOWN_AGENT_TAGS):
        count = open_counts.get(tag, 0)
        if count > 1:
            result.errors.append(f"[XN-003] Duplicate opening tag <{tag}> found {count} times")

    return result


def validate_skill_xml(file_path: Path, skill_name: str) -> ValidationResult:
    """Validate XML governance tags in a composed SKILL.md file.

    Args:
        file_path: Path to the composed SKILL.md file.
        skill_name: Skill directory name.

    Returns:
        ValidationResult with errors and warnings.
    """
    rel_path = str(file_path.relative_to(_REPO_ROOT))
    result = ValidationResult(rel_path)

    content = file_path.read_text(encoding="utf-8")
    _, body = _parse_frontmatter(content)

    # Strip code blocks and inline code
    clean_body = _strip_inline_code(_strip_code_blocks(body))

    # XN-005: Check governance XML tags when canonical source declares them
    governance = _get_skill_governance_fields(skill_name)
    for field_key, xml_tag in _SKILL_GOVERNANCE_TAGS.items():
        value = governance.get(field_key)
        if value:
            # Check for <xml_tag> OR ## Heading (dual detection like SCV-003)
            heading_map = {
                "version": "Skill Version",
                "activation-keywords": "Activation Keywords",
                "agents": "Agent Registry",
                "context_injection": "Context Injection",
            }
            heading_text = heading_map.get(field_key, "")

            has_xml = re.search(rf"<{xml_tag}[\s/>]", clean_body)
            has_heading = (
                re.search(
                    rf"^##\s+{re.escape(heading_text)}\s*$",
                    clean_body,
                    re.MULTILINE | re.IGNORECASE,
                )
                if heading_text
                else None
            )

            if not has_xml and not has_heading:
                result.errors.append(
                    f"[XN-005] Governance field '{field_key}' declared in "
                    f"canonical source but neither '<{xml_tag}>' tag nor "
                    f"'## {heading_text}' heading found in SKILL.md body"
                )

    # XN-006: Any XML tags present must be well-formed (matching open/close)
    open_tags = [t for t in _OPEN_TAG_RE.findall(clean_body) if t not in _HTML_VOID_ELEMENTS]
    close_tags = [t for t in _CLOSE_TAG_RE.findall(clean_body) if t not in _HTML_VOID_ELEMENTS]

    open_counts: dict[str, int] = {}
    close_counts: dict[str, int] = {}

    for tag in open_tags:
        open_counts[tag] = open_counts.get(tag, 0) + 1
    for tag in close_tags:
        close_counts[tag] = close_counts.get(tag, 0) + 1

    all_tags = set(open_counts.keys()) | set(close_counts.keys())
    for tag in sorted(all_tags):
        opens = open_counts.get(tag, 0)
        closes = close_counts.get(tag, 0)

        if opens != closes:
            result.errors.append(
                f"[XN-006] XML tag mismatch in SKILL.md: <{tag}> opens "
                f"{opens} time(s) but </{tag}> closes {closes} time(s)"
            )

    return result


def main() -> None:
    """Run XML nesting validation on all composed files."""
    print("=" * 70)
    print("XML Nesting Validation Report")
    print("=" * 70)

    if not _SKILLS_DIR.is_dir():
        print(f"  FATAL: Skills directory not found: {_SKILLS_DIR}")
        sys.exit(1)

    results: list[ValidationResult] = []
    agent_count = 0
    skill_count = 0

    # Discover all skill directories
    skill_dirs = sorted(
        d for d in _SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")
    )

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name

        # Validate agent .md files
        agents_dir = skill_dir / "agents"
        if agents_dir.is_dir():
            for agent_file in sorted(agents_dir.glob("*.md")):
                agent_name = agent_file.stem
                r = validate_agent_xml(agent_file, skill_name, agent_name)
                results.append(r)
                agent_count += 1

        # Validate SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            r = validate_skill_xml(skill_md, skill_name)
            results.append(r)
            skill_count += 1

    # Report
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    print(f"\nScanned: {agent_count} agent files, {skill_count} SKILL.md files")
    print(f"Total files: {len(results)}")

    if failed:
        print(f"\n--- FAILURES ({len(failed)}) ---")
        for r in failed:
            print(f"\n  {r.file_path}:")
            for err in r.errors:
                print(f"    ERROR: {err}")
            for warn in r.warnings:
                print(f"    WARN:  {warn}")

    print(f"\n{'=' * 70}")
    print(f"Results: {len(passed)}/{len(results)} passed, {len(failed)} failed")
    verdict = "VALIDATED" if not failed else "FAILED"
    print(f"Verdict: {verdict}")
    print("=" * 70)

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
