# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Guard: the Codecov upload names only ``coverage.xml``; ``.github/codecov.yml`` pins its settings.

Codecov's uploader searches the whole checkout for coverage reports.  It found an old report that
was committed as project evidence and sent it with the real one.  Codecov refused such uploads as
expired: the last upload of ``main`` that it processed was on 25 February 2026, and nothing on the
pull requests said so.  This test reads ``.github/workflows/ci.yml`` and ``.github/codecov.yml``
(Codecov reads its settings from the repository root, ``dev/`` or ``.github/``) as they are in the
repository and fails if the upload step may search the tree again, if the settings that report
failures are missing, or if the layout of the pull request comment is not the one that was written
out: its ``files`` item puts each changed file, with its coverage and how many lines it leaves
uncovered, in the comment, and the other parts add the Coverage Diff counts and the legend.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.security

ROOT = Path(__file__).resolve().parents[2]
ACTION = "codecov/codecov-action@"
NO_FILE = "Codecov would use its defaults: no notice of a failed upload, and a layout of its own"
# The settings of codecov.yml that are checked: the path, the value it must have, and why.
SETTINGS = {
    "codecov.notify.notify_error": (True, "without it a refused upload goes unseen"),
    "coverage.status.project.default.informational": (
        True,
        "the project status must pass whatever the coverage",
    ),
    "coverage.status.patch.default.informational": (
        True,
        "the patch status must pass whatever the coverage",
    ),
    "comment.hide_project_coverage": (False, "the comment must show the project coverage number"),
    "comment.require_changes": (False, "the comment must be posted when coverage does not change"),
    # The layout is pinned as written, so that no part goes unseen: a part that is removed takes a
    # table, the Coverage Diff block or the legend out of the comment. The file item stays a plain
    # ``files``: Codecov adds the table of files with uncovered lines only for the exact names
    # ``files`` and ``tree``, so ``files:25`` would lose it (from Codecov's code; not tried).
    "comment.layout": (
        "header, diff, flags, files, footer",
        "the comment must keep every part of its layout, the file tables among them",
    ),
}


def _shown(value: object) -> str:
    """How a value is named in a message: ``missing`` when the key is absent, else its repr."""
    return "missing" if value is None else repr(value)


def _read(path: str, why: str) -> Any:
    """The parsed YAML of ``path`` under the repository root; fails if the file is missing."""
    file = ROOT / path
    assert file.is_file(), f"{path} does not exist: {why}"
    return yaml.safe_load(file.read_text(encoding="utf-8"))


def test_workflow_when_read_then_the_one_upload_step_sends_only_coverage_xml() -> None:
    """ci.yml has exactly one Codecov upload step; it names coverage.xml and does not search."""
    workflow = _read(".github/workflows/ci.yml", "there is no upload step to check")
    steps = [
        step
        for job in workflow.get("jobs", {}).values()
        for step in job.get("steps") or []
        if str(step.get("uses", "")).startswith(ACTION)
    ]
    assert len(steps) == 1, (
        f"ci.yml must have exactly one step that uses {ACTION}, but has {len(steps)}: with none "
        "no coverage reaches Codecov (and this must fail, not pass), with two one is unchecked"
    )
    inputs = steps[0].get("with") or {}
    files, search = inputs.get("files"), inputs.get("disable_search")
    assert files == "coverage.xml", (
        f"the upload step must send only coverage.xml, but files is {_shown(files)}: any other "
        "report in the upload can make Codecov refuse all of it"
    )
    # PyYAML also reads yes and on as true; the action honours only true or 1: write true.
    assert search in (True, "true"), (
        f"the upload step must set disable_search: true, but it is {_shown(search)}: the uploader "
        "would search the whole tree and send an old committed report along, which Codecov "
        "refused as expired"
    )


@pytest.mark.parametrize(
    ("setting", "expected", "why"), [(k, *v) for k, v in SETTINGS.items()], ids=list(SETTINGS)
)
def test_settings_file_when_read_then_the_setting_has_the_wanted_value(
    setting: str, expected: bool | str, why: str
) -> None:
    """.github/codecov.yml exists, and ``setting`` in it is ``expected``."""
    value = _read(".github/codecov.yml", NO_FILE)
    for key in setting.split("."):
        value = value.get(key) if isinstance(value, dict) else None
    message = (
        f".github/codecov.yml: {setting} is {_shown(value)}, but it must be {expected!r}: {why}"
    )
    # The type is compared too: a number or a text (1, 0, "false") must not stand in for a boolean.
    assert type(value) is type(expected) and value == expected, message
