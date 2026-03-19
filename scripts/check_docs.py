# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Pre-commit hook: verify README documentation sections are current.

Exit codes:
    0 -- README.md is up to date; no action required.
    1 -- Drift detected; README.md differs from generated output.
         Run: uv run jerry docs generate --write
    2+ -- Documentation generation error (parse error, template error, etc.).

Usage (pre-commit hook registration):
    Add to .pre-commit-config.yaml:

        - repo: local
          hooks:
            - id: check-docs
              name: Check README documentation sections
              language: system
              entry: uv run python scripts/check_docs.py
              pass_filenames: false

    Or invoke directly:
        uv run python scripts/check_docs.py
"""

import subprocess
import sys


def main() -> None:
    """Run the documentation drift check and report results."""
    result = subprocess.run(
        ["uv", "run", "jerry", "docs", "generate", "--check"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 1:
        print("README.md documentation sections are out of date.")
        print("Run: uv run jerry docs generate --write")
        if result.stdout:
            print(result.stdout)
        sys.exit(1)
    elif result.returncode > 1:
        print(f"Documentation generation error: {result.stderr}")
        sys.exit(result.returncode)

    # returncode == 0: README is current, nothing to do.


if __name__ == "__main__":
    main()
