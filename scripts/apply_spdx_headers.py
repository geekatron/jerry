#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Apply SPDX Apache-2.0 license headers to all .py files in specified directories.

One-time migration script for EN-932 (FEAT-015 License Migration).
"""

import sys
from pathlib import Path

HEADER_LINES = [
    "# SPDX-License-Identifier: Apache-2.0",
    "# Copyright (c) 2026 Adam Nowak",
]

SCOPE_DIRS = ["src", "scripts", "hooks", "tests"]

SPDX_MARKER = "SPDX-License-Identifier"


def has_shebang(content: str) -> bool:
    return content.startswith("#!")


def already_has_header(content: str) -> bool:
    return SPDX_MARKER in content


def apply_header(filepath: Path) -> dict:
    """Apply SPDX header to a single file. Returns a result dict."""
    content = filepath.read_text(encoding="utf-8")

    if already_has_header(content):
        return {"path": str(filepath), "action": "skipped", "reason": "already has SPDX header"}

    header_block = "\n".join(HEADER_LINES)

    if not content.strip():
        # Empty file (or whitespace only)
        new_content = header_block + "\n"
        filepath.write_text(new_content, encoding="utf-8")
        return {"path": str(filepath), "action": "added", "note": "empty file"}

    if has_shebang(content):
        # Split at first newline to preserve shebang
        first_newline = content.index("\n")
        shebang_line = content[: first_newline + 1]
        rest = content[first_newline + 1 :]
        new_content = shebang_line + "\n" + header_block + "\n\n" + rest
        filepath.write_text(new_content, encoding="utf-8")
        return {"path": str(filepath), "action": "added", "note": "after shebang"}

    # Normal file — header at top
    new_content = header_block + "\n\n" + content
    filepath.write_text(new_content, encoding="utf-8")
    return {"path": str(filepath), "action": "added", "note": "top of file"}


def main() -> None:
    results = {"added": [], "skipped": [], "errors": []}

    for scope_dir in SCOPE_DIRS:
        scope_path = Path(scope_dir)
        if not scope_path.exists():
            print(f"WARNING: {scope_dir}/ does not exist, skipping")
            continue

        for filepath in sorted(scope_path.rglob("*.py")):
            try:
                result = apply_header(filepath)
                if result["action"] == "added":
                    results["added"].append(result)
                else:
                    results["skipped"].append(result)
            except Exception as e:
                results["errors"].append({"path": str(filepath), "error": str(e)})

    # Summary
    print(f"Files modified: {len(results['added'])}")
    print(f"Files skipped:  {len(results['skipped'])}")
    print(f"Errors:         {len(results['errors'])}")

    if results["errors"]:
        print("\nERRORS:")
        for err in results["errors"]:
            print(f"  {err['path']}: {err['error']}")
        sys.exit(1)

    # Detailed output
    shebang_count = sum(1 for r in results["added"] if r.get("note") == "after shebang")
    empty_count = sum(1 for r in results["added"] if r.get("note") == "empty file")
    normal_count = sum(1 for r in results["added"] if r.get("note") == "top of file")
    print(
        f"\nBreakdown: {normal_count} normal, {shebang_count} after shebang, {empty_count} empty files"
    )

    if results["skipped"]:
        print("\nSkipped files (already had header):")
        for s in results["skipped"]:
            print(f"  {s['path']}")


if __name__ == "__main__":
    main()
