# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for Layer4Pipeline._validate_output_path() — CG-025.

Verifies that _validate_output_path():
  - Accepts paths that resolve within the current working directory.
  - Rejects paths that traverse outside the CWD via '../' sequences.

All tests use tmp_path and monkeypatch to control the CWD so that the
production implementation's Path.cwd() call returns a stable, isolated
directory regardless of where pytest is invoked.

No LLM calls are performed. No filesystem side effects beyond tmp_path.

References:
    - CG-025: _validate_output_path() path traversal prevention
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jerry.testing.layer4_stats import Layer4Pipeline


class TestValidateOutputPath:
    """Unit tests for Layer4Pipeline._validate_output_path() (CG-025).

    The method is a staticmethod; tests call it directly without constructing
    a full Layer4Pipeline instance.
    """

    @pytest.mark.unit
    def test_valid_path_within_cwd_should_be_accepted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A path that resolves within the CWD is returned as its resolved absolute form.

        This is the primary happy path: a relative path such as
        'regression-report.json' within the working directory is accepted and
        its resolved absolute form is returned.
        """
        monkeypatch.chdir(tmp_path)
        output_file = tmp_path / "regression-report.json"

        result = Layer4Pipeline._validate_output_path(output_file)

        assert result == output_file.resolve()
        assert result.is_absolute()

    @pytest.mark.unit
    def test_nested_path_within_cwd_should_be_accepted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A path nested several levels within the CWD is accepted.

        Subdirectory output paths (e.g., 'reports/2026/agent/report.json')
        are a common production pattern and must not be rejected.
        """
        monkeypatch.chdir(tmp_path)
        nested = tmp_path / "reports" / "2026" / "agent" / "report.json"

        result = Layer4Pipeline._validate_output_path(nested)

        assert result == nested.resolve()

    @pytest.mark.unit
    def test_path_traversal_outside_cwd_should_raise_value_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A path that traverses outside the CWD raises ValueError (CG-025).

        The '../' sequence in a path can escape the project root and write
        to arbitrary filesystem locations. CG-025 enforces rejection by
        checking that the resolved path is_relative_to the CWD.
        """
        # Set up: work inside a subdirectory so '../' escapes to tmp_path's parent.
        work_dir = tmp_path / "workdir"
        work_dir.mkdir()
        monkeypatch.chdir(work_dir)

        # This path resolves to tmp_path (one level above work_dir).
        escaping_path = work_dir / ".." / "secret.json"

        with pytest.raises(ValueError, match="CG-025"):
            Layer4Pipeline._validate_output_path(escaping_path)

    @pytest.mark.unit
    def test_absolute_path_outside_cwd_should_raise_value_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An absolute path pointing outside the CWD raises ValueError (CG-025).

        Even without '../' traversal, an absolute path to '/tmp/evil.json'
        from within a project subdirectory must be rejected to prevent
        accidental writes to operating-system temporary directories.
        """
        work_dir = tmp_path / "project"
        work_dir.mkdir()
        monkeypatch.chdir(work_dir)

        # Create a sibling directory outside the CWD
        outside = tmp_path / "outside.json"

        with pytest.raises(ValueError, match="CG-025"):
            Layer4Pipeline._validate_output_path(outside)
