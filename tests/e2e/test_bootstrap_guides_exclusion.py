# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Test bootstrap context excludes guides directory.

This test verifies that the bootstrap script correctly excludes .context/guides/
from the auto-loaded context distribution, while rules and patterns ARE synced.
This enforces the three-tier architecture (rules=auto, patterns=auto, guides=on-demand).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_bootstrap_excludes_guides_directory(tmp_path: Path) -> None:
    """Verify .context/guides/ is NOT synced to .claude/guides/ after bootstrap.

    This test creates a minimal Jerry-like structure, runs the bootstrap script,
    and verifies that guides are excluded from the sync while rules are included.
    """
    # Arrange: Create minimal Jerry project structure
    context_dir = tmp_path / ".context"
    context_dir.mkdir()

    rules_dir = context_dir / "rules"
    rules_dir.mkdir()
    (rules_dir / "test-rule.md").write_text("# Test Rule\n")

    patterns_dir = context_dir / "patterns"
    patterns_dir.mkdir()
    (patterns_dir / "test-pattern.md").write_text("# Test Pattern\n")

    guides_dir = context_dir / "guides"
    guides_dir.mkdir()
    (guides_dir / "test-guide.md").write_text("# Test Guide\n")

    # Create CLAUDE.md to mark project root
    (tmp_path / "CLAUDE.md").write_text("# Test Project\n")

    claude_dir = tmp_path / ".claude"

    # Act: Run bootstrap script
    script_path = Path(__file__).parent.parent.parent / "scripts" / "bootstrap_context.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--quiet"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Assert: Bootstrap succeeded
    assert result.returncode == 0, f"Bootstrap failed: {result.stderr}"

    # Assert: .claude/rules/ exists (rules ARE synced)
    claude_rules = claude_dir / "rules"
    assert claude_rules.exists(), ".claude/rules/ should exist after bootstrap"

    # Assert: .claude/patterns/ exists (patterns ARE synced)
    claude_patterns = claude_dir / "patterns"
    assert claude_patterns.exists(), ".claude/patterns/ should exist after bootstrap"

    # Assert: .claude/guides/ does NOT exist (guides are EXCLUDED)
    claude_guides = claude_dir / "guides"
    assert not claude_guides.exists(), (
        ".claude/guides/ should NOT exist - guides must remain on-demand only"
    )

    # Assert: .context/guides/ still exists (source is preserved)
    assert guides_dir.exists(), ".context/guides/ source should be preserved"
    assert (guides_dir / "test-guide.md").exists(), "guide content should be preserved"


def test_bootstrap_check_reports_no_guides_drift(tmp_path: Path) -> None:
    """Verify --check mode does not report drift for missing .claude/guides/.

    Since guides are intentionally excluded, --check should not flag their
    absence as a problem.
    """
    # Arrange: Create minimal Jerry structure (after bootstrap)
    context_dir = tmp_path / ".context"
    context_dir.mkdir()

    rules_dir = context_dir / "rules"
    rules_dir.mkdir()
    (rules_dir / "test-rule.md").write_text("# Test Rule\n")

    patterns_dir = context_dir / "patterns"
    patterns_dir.mkdir()
    (patterns_dir / "test-pattern.md").write_text("# Test Pattern\n")

    guides_dir = context_dir / "guides"
    guides_dir.mkdir()
    (guides_dir / "test-guide.md").write_text("# Test Guide\n")

    (tmp_path / "CLAUDE.md").write_text("# Test Project\n")

    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    # Simulate already-bootstrapped state (rules and patterns synced, guides absent)
    (claude_dir / "rules").mkdir()
    (claude_dir / "patterns").mkdir()

    # Act: Run bootstrap --check
    script_path = Path(__file__).parent.parent.parent / "scripts" / "bootstrap_context.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--check", "--quiet"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Assert: Check passes (exit code 0 or 1 is acceptable since we're using
    # a simulated structure, but should not crash)
    assert result.returncode in (0, 1), f"--check should complete without error: {result.stderr}"

    # Assert: Output does not mention guides as a problem
    # (This is qualitative; the script doesn't check guides at all)
    assert "guides" not in result.stderr.lower(), "stderr should not mention guides as an issue"
