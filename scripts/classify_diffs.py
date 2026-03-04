#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Classify differences between composed agents on this branch vs main.

Categories:
  FM   - Frontmatter additions (permissionMode, background)
  GOV  - Governance section injection (agent_version, tool_tier, etc.)
  XML  - Body format transform (heading→XML, <agent> wrapper)
  DESC - Description YAML reformatting
  OTHER- Anything not in the above categories
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile


def get_main_content(fpath: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "show", f"main:{fpath}"],
            stderr=subprocess.DEVNULL,
        ).decode()
    except subprocess.CalledProcessError:
        return None


def get_diff_lines(main: str, branch: str) -> tuple[list[str], list[str]]:
    """Return (added_lines, removed_lines) from a unified diff."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f1:
        f1.write(main)
        f1_path = f1.name
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f2:
        f2.write(branch)
        f2_path = f2.name

    try:
        result = subprocess.run(
            ["diff", "-u", f1_path, f2_path],
            capture_output=True,
            text=True,
        )
        added = []
        removed = []
        for line in result.stdout.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added.append(line[1:])
            elif line.startswith("-") and not line.startswith("---"):
                removed.append(line[1:])
        return added, removed
    finally:
        os.unlink(f1_path)
        os.unlink(f2_path)


GOV_TAGS = {
    "agent_version",
    "tool_tier",
    "enforcement",
    "portability",
    "prior_art",
    "session_context",
}

FM_LINES = {"permissionMode: default", "background: false", "background: true"}

XML_STRUCTURAL = {"<agent>", "</agent>", ""}

KNOWN_XML_TAGS = {
    "identity",
    "persona",
    "capabilities",
    "methodology",
    "guardrails",
    "output",
    "output_structure",
    "output_format",
    "constitutional_compliance",
    "invocation_protocol",
    "p_003_runtime_self_check",
    "state_management",
    "mermaid_syntax_guidelines",
    "diagram_examples",
    "input",
    "purpose",
    "execution_process",
    "verification_methodology",
}


def classify(added: list[str], removed: list[str]) -> set[str]:
    cats: set[str] = set()
    unexplained_added: list[str] = []
    unexplained_removed: list[str] = []

    for line in added:
        s = line.strip()
        if s in FM_LINES:
            cats.add("FM")
        elif s in XML_STRUCTURAL:
            cats.add("XML")
        elif any(
            s.startswith(f"<{tag}>")
            or s.startswith(f"</{tag}>")
            or s == f"<{tag}>"
            or s == f"</{tag}>"
            for tag in GOV_TAGS
        ):
            cats.add("GOV")
        elif any(
            s.startswith(f"<{tag}>")
            or s.startswith(f"</{tag}>")
            or s == f"<{tag}>"
            or s == f"</{tag}>"
            for tag in KNOWN_XML_TAGS
        ):
            cats.add("XML")
        elif s.startswith("description:"):
            cats.add("DESC")
        elif re.match(
            r"^(tier:|escalation_path:|enabled:|minimum_context_window:|reasoning_strategy:|body_format:|schema:|schema_version:|input_validation:|output_validation:|on_receive:|on_send:|- )",
            s,
        ):
            cats.add("GOV")  # governance section content
        elif s in ("", "---"):
            pass  # whitespace/delimiter
        else:
            unexplained_added.append(s)

    for line in removed:
        s = line.strip()
        if s.startswith("## "):
            # Heading that was likely converted to XML tag
            heading_slug = (
                s[3:]
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "_")
            )
            if heading_slug in KNOWN_XML_TAGS or any(
                heading_slug.startswith(t) for t in KNOWN_XML_TAGS
            ):
                cats.add("XML")
            else:
                unexplained_removed.append(s)
        elif s.startswith("### "):
            heading_slug = (
                s[4:]
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "_")
            )
            if heading_slug in KNOWN_XML_TAGS or any(
                heading_slug.startswith(t) for t in KNOWN_XML_TAGS
            ):
                cats.add("XML")
            else:
                unexplained_removed.append(s)
        elif s.startswith("</constitutional_compliance>"):
            cats.add("XML")
        elif s.startswith("description:") or s.startswith("  "):
            cats.add("DESC")
        elif s in ("", "---"):
            pass
        else:
            unexplained_removed.append(s)

    if unexplained_added or unexplained_removed:
        cats.add("OTHER")

    return cats, unexplained_added, unexplained_removed


def main():
    summary = {"FM": 0, "GOV": 0, "XML": 0, "DESC": 0, "OTHER": 0, "IDENTICAL": 0}
    other_details = []

    for dirpath, _, filenames in sorted(os.walk("skills")):
        if "/agents" not in dirpath:
            continue
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            fpath = os.path.join(dirpath, fn)
            main_content = get_main_content(fpath)
            if main_content is None:
                continue

            with open(fpath) as f:
                branch_content = f.read()

            if main_content == branch_content:
                summary["IDENTICAL"] += 1
                continue

            added, removed = get_diff_lines(main_content, branch_content)
            cats, unexplained_added, unexplained_removed = classify(added, removed)

            for c in cats:
                summary[c] = summary.get(c, 0) + 1

            cat_str = " ".join(sorted(cats))
            if "OTHER" in cats:
                other_details.append((fpath, unexplained_added[:5], unexplained_removed[:5]))
            print(f"  {fpath}: {cat_str}")

    print("\n=== Summary ===")
    print(f"  Identical to main: {summary['IDENTICAL']}")
    print(f"  Frontmatter additions only: {summary['FM']} agents")
    print(f"  Governance injection: {summary['GOV']} agents")
    print(f"  XML body transform: {summary['XML']} agents")
    print(f"  Description reformat: {summary['DESC']} agents")
    print(f"  OTHER (unexpected): {summary['OTHER']} agents")

    if other_details:
        print("\n=== OTHER diff details (first 5 lines each) ===")
        for fpath, ua, ur in other_details:
            print(f"\n  {fpath}:")
            if ua:
                print(f"    Added: {ua}")
            if ur:
                print(f"    Removed: {ur}")


if __name__ == "__main__":
    main()
