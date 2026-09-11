#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Fail when a plugin in marketplace.json exceeds the organization-distribution file cap.

Claude Code organization sync (claude.ai Organization settings > Plugins, on Team and
Enterprise plans) refuses a plugin of more than 5000 files:

    Plugin contains too many files (6499, maximum 5000)

The plugin is skipped, so members keep whatever version synced last, or receive nothing.
Nothing in the repository signals the problem beforehand, which is what this check is for.

    python3 scripts/check_plugin_size.py [repo_root]
"""

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

MAX_FILES = 5000


def tracked_files(root: Path, prefix: Path) -> list[str]:
    """Paths tracked by git under prefix, relative to prefix."""
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", str(prefix)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    rel = prefix.relative_to(root).as_posix()
    paths = [p for p in out.split("\0") if p]
    if rel == ".":
        return paths
    return [p[len(rel) + 1 :] for p in paths]


def local_plugin_roots(root: Path) -> list[tuple[str, Path]]:
    """(name, path) for every marketplace entry with a relative source."""
    manifest = root / ".claude-plugin" / "marketplace.json"
    if not manifest.is_file():
        print(f"no .claude-plugin/marketplace.json in {root} - nothing to check")
        return []
    entries = json.loads(manifest.read_text(encoding="utf-8")).get("plugins", [])
    roots = []
    for entry in entries:
        source = entry.get("source")
        if isinstance(source, str):
            roots.append((entry.get("name", "?"), (root / source).resolve()))
    return roots


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    over = []
    for name, plugin_root in local_plugin_roots(root):
        files = tracked_files(root, plugin_root)
        count = len(files)
        status = "OK  " if count <= MAX_FILES else "OVER"
        print(f"  {status}  {name}: {count} files (maximum {MAX_FILES})")
        if count <= MAX_FILES:
            continue
        over.append((name, count))
        top = Counter(p.split("/")[0] for p in files if "/" in p)
        print(f"        largest directories in {name}:")
        for directory, n in top.most_common(5):
            share = 100 * n // count
            print(f"          {n:6}  {share:3}%  {directory}/")

    if over:
        print()
        for name, count in over:
            print(
                f"{name} exceeds the organization-distribution cap by "
                f"{count - MAX_FILES} files and will be skipped at sync."
            )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
