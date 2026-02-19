# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""MkDocs research section validation tests.

Validates that the built MkDocs site has:
1. No unresolved octicon/emoji syntax (rendered as literal text)
2. No links referencing internal "bug" prefixed filenames
3. All same-page anchor links resolve to existing IDs
4. mkdocs build --strict passes with zero warnings
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]

ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = ROOT / "site"
RESEARCH_DIR = SITE_DIR / "research"


@pytest.fixture(scope="module", autouse=True)
def build_site() -> None:
    """Build MkDocs site before running tests.

    Cleans site/ directory first to prevent stale artifact interference.
    """
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, f"mkdocs build --strict failed:\n{result.stderr}"


def _get_research_html_files() -> list[Path]:
    """Return all HTML files under site/research/."""
    if not RESEARCH_DIR.exists():
        pytest.skip("site/research/ not found — build may have failed")
    return list(RESEARCH_DIR.rglob("*.html"))


class TestIconRendering:
    """Verify octicon/material icon syntax does not appear as literal text."""

    # Pattern matches :octicons-*: or :material-*: literal text in HTML
    UNRESOLVED_ICON = re.compile(r":(?:octicons|material|fontawesome)-[a-z0-9-]+:")
    # Strip <code> and <pre> blocks before scanning — icon syntax inside
    # code examples is intentionally literal and should not trigger failures.
    CODE_BLOCK = re.compile(r"<(?:code|pre)[^>]*>.*?</(?:code|pre)>", re.DOTALL)

    def test_no_unresolved_icons_in_research_pages(self) -> None:
        """All :octicons-*: and :material-*: syntax must resolve to HTML elements."""
        failures: list[str] = []
        for html_file in _get_research_html_files():
            content = html_file.read_text(encoding="utf-8")
            # Remove code blocks to avoid false positives from documented examples
            content_no_code = self.CODE_BLOCK.sub("", content)
            matches = self.UNRESOLVED_ICON.findall(content_no_code)
            if matches:
                rel = html_file.relative_to(SITE_DIR)
                failures.append(f"{rel}: {', '.join(set(matches))}")
        assert not failures, (
            "Unresolved icon syntax found (pymdownx.emoji may be misconfigured):\n"
            + "\n".join(failures)
        )


class TestLinkQuality:
    """Verify links don't expose internal naming artifacts."""

    def test_no_bug_prefixed_filenames_in_links(self) -> None:
        """Public-facing links must not reference files with 'bug' prefix."""
        bug_link = re.compile(r'href="[^"]*bug\d+-[^"]*"', re.IGNORECASE)
        failures: list[str] = []
        for html_file in _get_research_html_files():
            content = html_file.read_text(encoding="utf-8")
            matches = bug_link.findall(content)
            if matches:
                rel = html_file.relative_to(SITE_DIR)
                failures.append(f"{rel}: {', '.join(matches)}")
        assert not failures, "Links with 'bug' prefix found in public pages:\n" + "\n".join(
            failures
        )


class TestAnchorIntegrity:
    """Verify same-page anchor links resolve to existing element IDs."""

    def test_same_page_anchors_resolve(self) -> None:
        """All href='#fragment' links must have a matching id in the same page."""
        anchor_link = re.compile(r'href="#([^"]+)"')
        element_id = re.compile(r'id="([^"]+)"')
        failures: list[str] = []
        for html_file in _get_research_html_files():
            content = html_file.read_text(encoding="utf-8")
            ids = set(element_id.findall(content))
            anchors = set(anchor_link.findall(content))
            broken = anchors - ids
            # Filter out common framework anchors (e.g., __tabbed_1, __codelineno)
            broken = {a for a in broken if not a.startswith("__")}
            if broken:
                rel = html_file.relative_to(SITE_DIR)
                failures.append(f"{rel}: {', '.join(sorted(broken))}")
        assert not failures, "Broken same-page anchor links:\n" + "\n".join(failures)
