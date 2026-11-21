# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Guard: the workflow-level concurrency of ci.yml gives each push a group of its own.

GitHub does not always create runs in commit order.  On 20 November 2026 the run for an older merge
was created 71 seconds after that merge and joined the group that every push to main shared; the
run for main's head was cancelled, so the head had no finished run and uploaded no coverage report.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.security

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "ci.yml"
# A pull request has a number, so its runs share a group and a newer run cancels an older one.
# A push has none, so its group is its own run id, which no other run has.
GROUP = "${{ github.workflow }}-${{ github.event.pull_request.number || github.run_id }}"


def test_workflow_concurrency_when_read_then_each_push_has_a_group_of_its_own() -> None:
    """Only the runs of one pull request share a group; each push has a group of its own."""
    found = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8")).get("concurrency")

    assert found == {"group": GROUP, "cancel-in-progress": True}, (
        f"ci.yml concurrency is {found!r}, not the expected group {GROUP!r}. A push must have "
        "a group of its own: a group that all pushes share lets a run that GitHub creates late "
        "cancel the run for main's head. If you change the group on purpose, change GROUP too."
    )
