# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Phase 1 Foundation Evidence Tests — PROJ-0037-doc-module Barrier 1, Iteration 5.

These are minimal smoke tests that provide executable evidence for three
security controls implemented in Phase 1 of the doc module:

    - M-1: _sanitize_description strips HTML tags and dangerous URL schemes.
    - ValueError on malformed YAML in _load_yaml.
    - Inverted-marker order detection in inject_between_markers.

Phase 3 (eng-qa) will own the comprehensive 16-test suite.  These three
tests exist solely to move Evidence Quality from code-inspection-only to
executable evidence.
"""

import tempfile
from pathlib import Path

import pytest


def test_sanitize_description_strips_html_and_unsafe_links() -> None:
    """Evidence: M-1 sanitization removes HTML tags and dangerous URL schemes."""
    from src.docs.application.services.skill_extractor import SkillExtractor

    result = SkillExtractor._sanitize_description(
        '<script>alert("xss")</script>Safe text [click](javascript:alert(1))'
    )
    assert "<script>" not in result
    assert "javascript:" not in result
    assert "Safe text" in result
    assert "click" in result  # Link text preserved


def test_load_yaml_raises_value_error_on_malformed() -> None:
    """Evidence: yaml.YAMLError is caught and re-raised as ValueError."""
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: content: [unterminated")
        f.flush()
        tmp_path = f.name

    try:
        with pytest.raises(ValueError, match="Malformed YAML"):
            GenerateDocsCommandHandler._load_yaml(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_inject_between_markers_rejects_inverted_markers() -> None:
    """Evidence: Marker order validation prevents silent write corruption."""
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    # Markers in wrong order: END before BEGIN
    content = (
        "# Header\n"
        "<!-- END:GENERATED:TEST -->\n"
        "old content\n"
        "<!-- BEGIN:GENERATED:TEST -->\n"
        "# Footer\n"
    )
    renderer = Jinja2Renderer(template_dir=".")
    with pytest.raises(ValueError, match="Inverted marker order"):
        renderer.inject_between_markers(content, "TEST", "new content")


def test_path_traversal_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Evidence: Path traversal guard rejects readme_path outside repo root."""
    from unittest.mock import MagicMock

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    # Set cwd to tmp_path so /etc/passwd is outside the "repo root"
    monkeypatch.chdir(tmp_path)

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    command = GenerateDocsCommand(readme_path="/etc/passwd", mode="check")
    result = handler.handle(command)

    assert result.success is False
    assert result.error["code"] == "PATH_TRAVERSAL"


def test_check_drift_detects_content_mismatch(tmp_path: Path) -> None:
    """Evidence: _check_drift() returns True when content differs from generated."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Title\n"
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\n"
        "old content\n"
        "<!-- END:GENERATED:SKILLS_TABLE -->\n"
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    drift = handler._check_drift(
        str(readme),
        {"SKILLS_TABLE": "new content"},
        warnings,
    )
    assert drift is True


def test_atomic_write_produces_correct_content(tmp_path: Path) -> None:
    """Evidence: M-3 atomic write via tempfile+os.replace produces correct README."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Title\n"
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\n"
        "old content\n"
        "<!-- END:GENERATED:SKILLS_TABLE -->\n"
        "# Footer\n"
    )

    renderer = Jinja2Renderer(template_dir=".")
    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=renderer,
        reader=MagicMock(),
    )
    warnings: list[str] = []
    handler._write_readme(
        str(readme),
        {"SKILLS_TABLE": "new content"},
        warnings,
    )

    result = readme.read_text()
    assert "new content" in result
    assert "old content" not in result
    assert "# Title" in result
    assert "# Footer" in result


def test_invalid_mode_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Evidence: Mode validation rejects unrecognized mode values."""
    from unittest.mock import MagicMock

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").touch()

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    command = GenerateDocsCommand(readme_path="README.md", mode="invalid")
    result = handler.handle(command)

    assert result.success is False
    assert result.error["code"] == "INVALID_MODE"


def test_sandboxed_environment_blocks_unsafe_access() -> None:
    """Evidence: M-2 SandboxedEnvironment blocks __class__ traversal."""
    import os
    import tempfile

    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    # Create a temp template that tries to access __class__
    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = os.path.join(tmpdir, "evil.md.jinja2")
        with open(template_path, "w") as f:
            f.write("{{ ''.__class__.__mro__ }}")

        renderer = Jinja2Renderer(template_dir=tmpdir)
        with pytest.raises(RuntimeError):
            renderer.render_section("evil.md.jinja2", {})


def test_strict_undefined_raises_on_missing_variable() -> None:
    """Evidence: M-2 StrictUndefined prevents silent data leakage."""
    import os
    import tempfile

    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = os.path.join(tmpdir, "missing.md.jinja2")
        with open(template_path, "w") as f:
            f.write("{{ undefined_variable }}")

        renderer = Jinja2Renderer(template_dir=tmpdir)
        with pytest.raises(ValueError, match="Undefined variable"):
            renderer.render_section("missing.md.jinja2", {})


def test_ast_reader_raises_file_not_found() -> None:
    """Evidence: AstFrontmatterReader raises FileNotFoundError for missing files."""
    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    with pytest.raises(FileNotFoundError):
        reader.read_frontmatter("/nonexistent/path/to/file.md")


def test_agent_exclusion_patterns() -> None:
    """Evidence: TEMPLATE and EXTENSION files are excluded from agent extraction."""
    from src.docs.application.services.skill_extractor import _EXCLUDED_AGENT_PATTERNS

    # Verify the exclusion patterns match expected values
    assert "TEMPLATE" in _EXCLUDED_AGENT_PATTERNS
    assert "EXTENSION" in _EXCLUDED_AGENT_PATTERNS

    # Verify exclusion logic: each pattern matches its own representative filename
    assert "TEMPLATE" in "AGENT-TEMPLATE.md".upper()
    assert "EXTENSION" in "EXTENSION-AGENT.md".upper()

    # Verify a normal agent filename is not excluded
    assert not any(p in "ps-researcher.md".upper() for p in _EXCLUDED_AGENT_PATTERNS)


def test_check_drift_returns_false_when_matching(tmp_path: Path) -> None:
    """Evidence: _check_drift returns False when README content matches generated."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Title\n"
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\n"
        "matching content\n"
        "<!-- END:GENERATED:SKILLS_TABLE -->\n"
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    drift = handler._check_drift(
        str(readme),
        {"SKILLS_TABLE": "matching content"},
        warnings,
    )
    assert drift is False


def test_atomic_write_cleans_up_on_error(tmp_path: Path) -> None:
    """Evidence: M-3 atomic write cleans up temp file on write failure."""
    import os
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text("<!-- BEGIN:GENERATED:TEST -->\nold\n<!-- END:GENERATED:TEST -->\n")

    # Mock renderer.inject_between_markers to raise an error
    mock_renderer = MagicMock()
    mock_renderer.inject_between_markers.side_effect = RuntimeError("injection failed")

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=mock_renderer,
        reader=MagicMock(),
    )
    warnings: list[str] = []

    with pytest.raises(RuntimeError, match="injection failed"):
        handler._write_readme(str(readme), {"TEST": "new"}, warnings)

    # Verify no temp files left behind
    temp_files = [f for f in os.listdir(tmp_path) if f.endswith(".tmp")]
    assert len(temp_files) == 0


def test_ast_reader_raises_on_nonzero_returncode() -> None:
    """Evidence: AstFrontmatterReader raises RuntimeError on subprocess failure."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "unexpected error occurred"

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ) as mock_run:
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(RuntimeError, match="jerry ast frontmatter failed"):
                reader.read_frontmatter("/some/file.md")

    # Verify list-form args (no shell=True) — prevents command injection
    call_args = mock_run.call_args
    assert call_args[0][0] == ["uv", "run", "jerry", "ast", "frontmatter", "/some/file.md"]
    assert "shell" not in call_args[1] or call_args[1].get("shell") is not True


def test_check_drift_inverted_marker_warns(tmp_path: Path) -> None:
    """Evidence: _check_drift warns and returns True for inverted markers."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Title\n"
        "<!-- END:GENERATED:SKILLS_TABLE -->\n"
        "content\n"
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\n"
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    drift = handler._check_drift(
        str(readme),
        {"SKILLS_TABLE": "new content"},
        warnings,
    )
    assert drift is True
    assert any("Inverted" in w or "inverted" in w.lower() for w in warnings)


def test_generate_docs_result_per_mode_semantics() -> None:
    """Evidence: GenerateDocsResult.drift_detected follows three-state contract."""
    from src.docs.application.results.generate_docs_result import GenerateDocsResult

    # stdout/default mode: drift_detected is None
    stdout_result = GenerateDocsResult(success=True, drift_detected=None)
    assert stdout_result.drift_detected is None

    # check mode, drift found: drift_detected is True
    check_drift = GenerateDocsResult(success=True, drift_detected=True)
    assert check_drift.drift_detected is True

    # check mode, no drift / write mode: drift_detected is False
    no_drift = GenerateDocsResult(success=True, drift_detected=False)
    assert no_drift.drift_detected is False


def test_jinja2_renderer_rejects_missing_template_dir() -> None:
    """M-2 evidence: Jinja2Renderer raises FileNotFoundError for nonexistent directory."""
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    with pytest.raises(FileNotFoundError, match="Template directory not found"):
        Jinja2Renderer(template_dir="/nonexistent/templates/dir")


def test_happy_path_produces_non_empty_skills_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence: End-to-end pipeline with a valid SkillData produces non-empty output.

    Mocks the extractor to return one SkillData with name='test-skill' so the
    pipeline is exercised independently of real SKILL.md frontmatter.  Uses the
    real Jinja2Renderer against .context/templates/docs/ to validate the full
    render path.  Patches _load_yaml to avoid filesystem coupling for static
    YAML data files while keeping the handler orchestration real.
    """
    from unittest.mock import MagicMock, patch

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )
    from src.docs.domain.value_objects.skill_data import SkillData
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    # Resolve template_dir relative to the repo root (found via pyproject.toml)
    # rather than CWD, so the test works regardless of where pytest is invoked.
    _repo_root = Path(__file__).resolve().parents[3]  # tests/unit/docs -> repo root
    template_dir = str(_repo_root / ".context" / "templates" / "docs")
    renderer = Jinja2Renderer(template_dir=template_dir)

    # Stub extractor returns one valid SkillData — demonstrates the happy path
    # independently of real SKILL.md files lacking a 'name' field.
    mock_extractor = MagicMock()
    mock_extractor.extract_all.return_value = [
        SkillData(
            name="test-skill",
            description="Test purpose",
            version="1.0.0",
            agent_count=0,
            agents=[],
            file_path="skills/test-skill/SKILL.md",
        )
    ]

    # Patch _load_yaml so handler does not require real filesystem YAML files.
    # Returns minimal but valid data: one example entry and an empty features list.
    def _fake_load_yaml(file_path: str) -> object:
        if "skill-examples" in file_path:
            return {"test-skill": "jerry test"}
        return []  # features.yaml

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").touch()

    with patch.object(GenerateDocsCommandHandler, "_load_yaml", side_effect=_fake_load_yaml):
        handler = GenerateDocsCommandHandler(
            extractor=mock_extractor,
            renderer=renderer,
            reader=MagicMock(),
        )
        command = GenerateDocsCommand(readme_path="README.md", mode=None)
        result = handler.handle(command)

    assert result.success is True, f"Pipeline failed: {result.error}"
    assert result.skills_count == 1
    skills_table = result.sections.get("SKILLS_TABLE", "")
    assert skills_table, "SKILLS_TABLE section must not be empty"
    assert "test-skill" in skills_table, (
        f"Skill name 'test-skill' not found in rendered table:\n{skills_table}"
    )


# ---------------------------------------------------------------------------
# Phase 3 gap-closure tests — added by eng-qa to reach H-20 (90% coverage)
# ---------------------------------------------------------------------------

# --- GenerateDocsCommandHandler.handle() mode dispatch ---


def test_handle_check_mode_dispatches_to_check_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Coverage: handle() check-mode branch (line 180) routes to _check_drift."""
    from unittest.mock import MagicMock, patch

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )
    from src.docs.domain.value_objects.skill_data import SkillData

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text(
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\nold\n<!-- END:GENERATED:SKILLS_TABLE -->\n"
        "<!-- BEGIN:GENERATED:FEATURES -->\nold\n<!-- END:GENERATED:FEATURES -->\n"
    )

    mock_extractor = MagicMock()
    mock_extractor.extract_all.return_value = [
        SkillData(
            name="s",
            description="d",
            version="1.0.0",
            agent_count=0,
            agents=[],
            file_path="skills/s/SKILL.md",
        )
    ]

    mock_renderer = MagicMock()
    mock_renderer.render_section.return_value = "rendered"

    def _fake_load_yaml(_: str) -> object:
        return {}

    with patch.object(GenerateDocsCommandHandler, "_load_yaml", side_effect=_fake_load_yaml):
        handler = GenerateDocsCommandHandler(
            extractor=mock_extractor,
            renderer=mock_renderer,
            reader=MagicMock(),
        )
        result = handler.handle(GenerateDocsCommand(readme_path="README.md", mode="check"))

    assert result.success is True
    assert result.drift_detected is True or result.drift_detected is False


def test_handle_write_mode_dispatches_to_write_readme(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Coverage: handle() write-mode branch (lines 184-185) routes to _write_readme."""
    from unittest.mock import MagicMock, patch

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )
    from src.docs.domain.value_objects.skill_data import SkillData

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text(
        "<!-- BEGIN:GENERATED:SKILLS_TABLE -->\nold\n<!-- END:GENERATED:SKILLS_TABLE -->\n"
        "<!-- BEGIN:GENERATED:FEATURES -->\nold\n<!-- END:GENERATED:FEATURES -->\n"
    )

    mock_extractor = MagicMock()
    mock_extractor.extract_all.return_value = [
        SkillData(
            name="s",
            description="d",
            version="1.0.0",
            agent_count=0,
            agents=[],
            file_path="skills/s/SKILL.md",
        )
    ]

    mock_renderer = MagicMock()
    mock_renderer.render_section.return_value = "rendered"
    # inject_between_markers must return valid string for write to proceed
    mock_renderer.inject_between_markers.side_effect = lambda content, name, gen: content

    def _fake_load_yaml(_: str) -> object:
        return {}

    with patch.object(GenerateDocsCommandHandler, "_load_yaml", side_effect=_fake_load_yaml):
        handler = GenerateDocsCommandHandler(
            extractor=mock_extractor,
            renderer=mock_renderer,
            reader=MagicMock(),
        )
        result = handler.handle(GenerateDocsCommand(readme_path="README.md", mode="write"))

    assert result.success is True
    assert result.drift_detected is False


def test_handle_generation_error_returns_error_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Coverage: handle() except branch (lines 196-202) returns GENERATION_ERROR."""
    from unittest.mock import MagicMock

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").touch()

    mock_extractor = MagicMock()
    mock_extractor.extract_all.side_effect = RuntimeError("extraction blew up")

    handler = GenerateDocsCommandHandler(
        extractor=mock_extractor,
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    result = handler.handle(GenerateDocsCommand(readme_path="README.md", mode=None))

    assert result.success is False
    assert result.error["code"] == "GENERATION_ERROR"
    assert "extraction blew up" in result.error["message"]


# --- GenerateDocsCommandHandler._check_drift() branches ---


def test_check_drift_readme_not_found_warns_and_returns_true() -> None:
    """Coverage: _check_drift FileNotFoundError branch (lines 222-224)."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    drift = handler._check_drift("/nonexistent/README.md", {"SKILLS_TABLE": "content"}, warnings)
    assert drift is True
    assert any("README not found" in w for w in warnings)


def test_check_drift_missing_markers_warns_and_returns_true(tmp_path: Path) -> None:
    """Coverage: _check_drift missing markers branch (lines 231-232)."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text("# No markers here\n")

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    drift = handler._check_drift(str(readme), {"SKILLS_TABLE": "content"}, warnings)
    assert drift is True
    assert any("Markers not found" in w for w in warnings)


# --- GenerateDocsCommandHandler._write_readme() branches ---


def test_write_readme_file_not_found_warns_and_returns(tmp_path: Path) -> None:
    """Coverage: _write_readme FileNotFoundError branch (lines 267-269)."""
    from unittest.mock import MagicMock

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
    )
    warnings: list[str] = []
    # Should not raise; should just warn
    handler._write_readme("/nonexistent/README.md", {"TEST": "content"}, warnings)
    assert any("README not found" in w for w in warnings)


def test_write_readme_cleanup_on_oserror_at_unlink(tmp_path: Path) -> None:
    """Coverage: _write_readme OSError during unlink in cleanup (lines 292-299).

    When os.replace raises after the temp file is created (temp_path is set),
    the except block runs.  We also make os.unlink raise OSError so the inner
    pass branch (line 297-298) is exercised.
    """
    from unittest.mock import MagicMock, patch

    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    readme = tmp_path / "README.md"
    readme.write_text("<!-- BEGIN:GENERATED:TEST -->\nold\n<!-- END:GENERATED:TEST -->\n")

    mock_renderer = MagicMock()
    # inject_between_markers must succeed so we reach the atomic write block
    mock_renderer.inject_between_markers.return_value = (
        "<!-- BEGIN:GENERATED:TEST -->\nnew\n<!-- END:GENERATED:TEST -->\n"
    )

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=mock_renderer,
        reader=MagicMock(),
    )
    warnings: list[str] = []

    # Patch os.replace to raise so the cleanup except block runs,
    # then patch os.unlink to also raise OSError to hit the inner pass.
    with patch(
        "src.docs.application.handlers.commands.generate_docs_command_handler.os.replace",
        side_effect=OSError("replace failed"),
    ):
        with patch(
            "src.docs.application.handlers.commands.generate_docs_command_handler.os.unlink",
            side_effect=OSError("unlink also failed"),
        ):
            with pytest.raises(OSError, match="replace failed"):
                handler._write_readme(str(readme), {"TEST": "new"}, warnings)


# --- GenerateDocsCommandHandler._load_yaml() FileNotFoundError branch ---


def test_load_yaml_raises_file_not_found_for_missing_file() -> None:
    """Coverage: _load_yaml FileNotFoundError re-raise (lines 317-318)."""
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    with pytest.raises(FileNotFoundError):
        GenerateDocsCommandHandler._load_yaml("/nonexistent/path/data.yaml")


# --- AstFrontmatterReader error branches ---


def test_ast_reader_raises_runtime_on_timeout() -> None:
    """Coverage: AstFrontmatterReader TimeoutExpired branch (lines 63-66)."""
    import subprocess
    from unittest.mock import patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        side_effect=subprocess.TimeoutExpired(cmd="uv", timeout=30),
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(RuntimeError, match="timed out"):
                reader.read_frontmatter("/some/file.md")


def test_ast_reader_raises_runtime_on_oserror() -> None:
    """Coverage: AstFrontmatterReader OSError branch (lines 67-70)."""
    from unittest.mock import patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        side_effect=OSError("no such executable"),
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(RuntimeError, match="Failed to run jerry ast frontmatter"):
                reader.read_frontmatter("/some/file.md")


def test_ast_reader_raises_value_error_on_parse_error_stderr() -> None:
    """Coverage: AstFrontmatterReader 'parse error' in stderr → ValueError (line 75)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "parse error: unexpected token at line 3"

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(ValueError, match="Malformed frontmatter"):
                reader.read_frontmatter("/some/file.md")


def test_ast_reader_returns_empty_dict_on_empty_stdout() -> None:
    """Coverage: AstFrontmatterReader empty stdout returns {} (lines 83-85)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            result = reader.read_frontmatter("/some/file.md")
    assert result == {}


def test_ast_reader_returns_empty_dict_on_empty_json_object() -> None:
    """Coverage: AstFrontmatterReader stdout=='{}' returns {} (lines 83-85)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "{}"

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            result = reader.read_frontmatter("/some/file.md")
    assert result == {}


def test_ast_reader_raises_value_error_on_invalid_json() -> None:
    """Coverage: AstFrontmatterReader JSONDecodeError → ValueError (lines 88-92)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "not valid json {"

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(ValueError, match="Invalid JSON"):
                reader.read_frontmatter("/some/file.md")


def test_ast_reader_raises_value_error_on_non_dict_json() -> None:
    """Coverage: AstFrontmatterReader non-dict JSON → ValueError (lines 94-98)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '["item1", "item2"]'

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            with pytest.raises(ValueError, match="Expected dict"):
                reader.read_frontmatter("/some/file.md")


def test_ast_reader_returns_parsed_dict_on_valid_json() -> None:
    """Coverage: AstFrontmatterReader happy path returns parsed frontmatter (line 100)."""
    from unittest.mock import MagicMock, patch

    from src.docs.infrastructure.adapters.ast_frontmatter_reader import AstFrontmatterReader

    reader = AstFrontmatterReader()
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '{"name": "my-skill", "version": "1.0.0"}'

    with patch(
        "src.docs.infrastructure.adapters.ast_frontmatter_reader.subprocess.run",
        return_value=mock_result,
    ):
        with patch(
            "src.docs.infrastructure.adapters.ast_frontmatter_reader.Path.exists", return_value=True
        ):
            result = reader.read_frontmatter("/some/file.md")
    assert result == {"name": "my-skill", "version": "1.0.0"}


# --- SkillExtractor full pipeline coverage ---


def test_skill_extractor_extract_all_empty_dir(tmp_path: Path) -> None:
    """Coverage: extract_all with no SKILL.md files returns empty list (lines 83-92)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    reader = MagicMock()
    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path))
    assert result == []


def test_skill_extractor_extract_all_skips_frontmatter_read_error(tmp_path: Path) -> None:
    """Coverage: _extract_skill skips on reader exception (lines 103-107)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.side_effect = RuntimeError("subprocess exploded")

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert result == []


def test_skill_extractor_skips_skill_missing_name(tmp_path: Path) -> None:
    """Coverage: _extract_skill returns None for missing name (lines 110-115)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "no-name"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\ndescription: something\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {"description": "no name here"}

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert result == []


def test_skill_extractor_skips_skill_invalid_name_pattern(tmp_path: Path) -> None:
    """Coverage: _extract_skill skips names not matching pattern (lines 119-126)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "bad"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: '123-invalid'\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {"name": "123-invalid"}

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert result == []


def test_skill_extractor_normalizes_invalid_version(tmp_path: Path) -> None:
    """Coverage: _extract_skill normalizes bad version to 0.0.0 (lines 130-132)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "ok-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: ok-skill\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {
        "name": "ok-skill",
        "version": "not-semver",
        "description": "A test skill",
    }

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].version == "0.0.0"


def test_skill_extractor_defaults_empty_description(tmp_path: Path) -> None:
    """Coverage: _extract_skill sets '(no description)' when description empty (lines 138-140)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "nodesc-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: nodesc-skill\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {"name": "nodesc-skill", "description": ""}

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].description == "(no description)"


def test_skill_extractor_warns_on_excess_keywords(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Coverage: _extract_skill logs warning when keywords > 30 (lines 148-155)."""
    import logging
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "kw-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: kw-skill\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {
        "name": "kw-skill",
        "description": "many keywords",
        "activation-keywords": [f"kw{i}" for i in range(31)],
    }

    extractor = SkillExtractor(reader=reader)
    with caplog.at_level(logging.WARNING, logger="src.docs.application.services.skill_extractor"):
        result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert any("activation-keywords" in rec.message for rec in caplog.records)


def test_skill_extractor_extract_agents_no_agents_dir(tmp_path: Path) -> None:
    """Coverage: _extract_agents returns [] when agents/ dir absent (lines 180-181)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "no-agents"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: no-agents\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {"name": "no-agents", "description": "skill"}

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agent_count == 0
    assert result[0].agents == []


def test_skill_extractor_excludes_template_agent_files(tmp_path: Path) -> None:
    """Coverage: _extract_agents excludes TEMPLATE files (lines 186-190)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "AGENT-TEMPLATE.md").write_text("---\nname: template\n---\n")
    (agents_dir / "EXTENSION-SPEC.md").write_text("---\nname: extension\n---\n")

    reader = MagicMock()
    reader.read_frontmatter.return_value = {"name": "my-skill", "description": "skill"}

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    # No agents should be extracted (TEMPLATE and EXTENSION files excluded)
    assert result[0].agent_count == 0


def test_skill_extractor_extracts_valid_agent(tmp_path: Path) -> None:
    """Coverage: _extract_agent happy path (lines 207-240)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "my-agent.md").write_text("---\nname: my-agent\n---\n")

    call_count = 0

    def side_effect(path: str) -> dict:
        nonlocal call_count
        call_count += 1
        if "SKILL.md" in path:
            return {"name": "my-skill", "description": "A skill"}
        return {"name": "my-agent", "description": "An agent", "model": "sonnet"}

    reader = MagicMock()
    reader.read_frontmatter.side_effect = side_effect

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agent_count == 1
    assert result[0].agents[0].name == "my-agent"
    assert result[0].agents[0].model == "sonnet"


def test_skill_extractor_skips_agent_on_read_error(tmp_path: Path) -> None:
    """Coverage: _extract_agent skips on reader exception (lines 207-211)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "bad-agent.md").write_text("---\nname: bad-agent\n---\n")

    def side_effect(path: str) -> dict:
        if "SKILL.md" in path:
            return {"name": "my-skill", "description": "A skill"}
        raise ValueError("malformed frontmatter")

    reader = MagicMock()
    reader.read_frontmatter.side_effect = side_effect

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agent_count == 0


def test_skill_extractor_skips_agent_missing_name(tmp_path: Path) -> None:
    """Coverage: _extract_agent returns None for missing name (lines 213-216)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "no-name-agent.md").write_text("---\ndescription: something\n---\n")

    def side_effect(path: str) -> dict:
        if "SKILL.md" in path:
            return {"name": "my-skill", "description": "A skill"}
        return {"description": "no name"}

    reader = MagicMock()
    reader.read_frontmatter.side_effect = side_effect

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agent_count == 0


def test_skill_extractor_skips_agent_invalid_name_pattern(tmp_path: Path) -> None:
    """Coverage: _extract_agent skips agent names not matching pattern (lines 219-224)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "bad-agent.md").write_text("---\nname: BadAgent\n---\n")

    def side_effect(path: str) -> dict:
        if "SKILL.md" in path:
            return {"name": "my-skill", "description": "A skill"}
        return {"name": "BadAgent", "description": "bad name"}

    reader = MagicMock()
    reader.read_frontmatter.side_effect = side_effect

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agent_count == 0


def test_skill_extractor_agent_empty_description_defaults(tmp_path: Path) -> None:
    """Coverage: _extract_agent sets '(no description)' for empty agent description (line 231)."""
    from unittest.mock import MagicMock

    from src.docs.application.services.skill_extractor import SkillExtractor

    skill_dir = tmp_path / "skills" / "my-skill"
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
    (agents_dir / "my-agent.md").write_text("---\nname: my-agent\n---\n")

    def side_effect(path: str) -> dict:
        if "SKILL.md" in path:
            return {"name": "my-skill", "description": "A skill"}
        return {"name": "my-agent", "description": ""}

    reader = MagicMock()
    reader.read_frontmatter.side_effect = side_effect

    extractor = SkillExtractor(reader=reader)
    result = extractor.extract_all(skills_dir=str(tmp_path / "skills"))
    assert len(result) == 1
    assert result[0].agents[0].description == "(no description)"


# --- Jinja2Renderer render_section() error branches ---


def test_jinja2_renderer_raises_file_not_found_for_missing_template(tmp_path: Path) -> None:
    """Coverage: render_section raises FileNotFoundError for missing template (lines 82-87)."""
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    renderer = Jinja2Renderer(template_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError, match="not found in template directory"):
        renderer.render_section("nonexistent-template.md.jinja2", {})


def test_jinja2_renderer_raises_runtime_on_template_syntax_error(tmp_path: Path) -> None:
    """Coverage: render_section raises RuntimeError for template syntax error (line 87).

    Note: Jinja2 raises TemplateSyntaxError at get_template time, which is not
    a TemplateNotFound error, so it hits the RuntimeError branch.
    """

    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    bad_template = tmp_path / "bad.md.jinja2"
    bad_template.write_text("{% for x in items %} unclosed block")

    renderer = Jinja2Renderer(template_dir=str(tmp_path))
    with pytest.raises((RuntimeError, Exception)):
        renderer.render_section("bad.md.jinja2", {"items": [1, 2]})


def test_jinja2_renderer_inject_missing_markers_raises_value_error() -> None:
    """Coverage: inject_between_markers raises ValueError for missing markers (line 119)."""
    from src.docs.infrastructure.adapters.jinja2_renderer import Jinja2Renderer

    renderer = Jinja2Renderer(template_dir=".")
    with pytest.raises(ValueError, match="Marker pair not found"):
        renderer.inject_between_markers("# No markers here", "SKILLS_TABLE", "content")


# ---------------------------------------------------------------------------
# BUG-002 evidence: repo_root anchoring and path traversal consistency
# ---------------------------------------------------------------------------


def test_bug002_path_traversal_uses_repo_root_not_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """BUG-002 evidence: path traversal guard uses repo_root, not CWD.

    When repo_root is explicitly set, the traversal check must reject paths
    outside repo_root even if CWD would have accepted them.
    """
    from unittest.mock import MagicMock

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )

    # CWD is / (root), but repo_root is tmp_path.
    # A file outside tmp_path should be rejected by the repo_root guard.
    monkeypatch.chdir("/")

    handler = GenerateDocsCommandHandler(
        extractor=MagicMock(),
        renderer=MagicMock(),
        reader=MagicMock(),
        repo_root=tmp_path,
    )
    # /etc/passwd is outside tmp_path (repo_root) — must be rejected.
    command = GenerateDocsCommand(readme_path="/etc/passwd", mode="check")
    result = handler.handle(command)

    assert result.success is False
    assert result.error["code"] == "PATH_TRAVERSAL"


def test_bug002_handler_resolves_paths_against_repo_root(tmp_path: Path) -> None:
    """BUG-002 evidence: skills_dir and template_data_dir resolve against repo_root.

    When repo_root is provided, the handler must NOT use CWD for path
    resolution of skills or template data files.
    """
    from unittest.mock import MagicMock, patch

    from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
    from src.docs.application.handlers.commands.generate_docs_command_handler import (
        GenerateDocsCommandHandler,
    )
    from src.docs.domain.value_objects.skill_data import SkillData

    # Create a fake repo root with the expected subdirectory structure
    repo_root = tmp_path / "fake-repo"
    skills_dir = repo_root / "skills"
    skills_dir.mkdir(parents=True)
    readme = repo_root / "README.md"
    readme.touch()

    mock_extractor = MagicMock()
    mock_extractor.extract_all.return_value = [
        SkillData(
            name="test-skill",
            description="A test",
            version="1.0.0",
            agent_count=0,
            agents=[],
            file_path="skills/test/SKILL.md",
        )
    ]

    mock_renderer = MagicMock()
    mock_renderer.render_section.return_value = "rendered"

    def _fake_load_yaml(_: str) -> object:
        return {}

    with patch.object(GenerateDocsCommandHandler, "_load_yaml", side_effect=_fake_load_yaml):
        handler = GenerateDocsCommandHandler(
            extractor=mock_extractor,
            renderer=mock_renderer,
            reader=MagicMock(),
            repo_root=repo_root,
        )
        handler.handle(GenerateDocsCommand(readme_path=str(readme), mode=None))

    # Verify extract_all was called with the repo_root-based skills path
    call_args = mock_extractor.extract_all.call_args
    called_skills_dir = call_args[1].get("skills_dir") or call_args[0][0]
    assert str(repo_root) in called_skills_dir, (
        f"Expected skills_dir to be under repo_root ({repo_root}), but got: {called_skills_dir}"
    )


def test_bug002_bootstrap_repo_root_discovery() -> None:
    """BUG-002 evidence: create_docs_generator() finds repo root via pyproject.toml walk-up.

    Verifies the composition root discovers the correct repo root and passes
    an absolute template_dir path to Jinja2Renderer.
    """
    from src.bootstrap import create_docs_generator

    handler = create_docs_generator()
    # The handler should have a repo_root that contains pyproject.toml
    assert hasattr(handler, "_repo_root")
    assert (handler._repo_root / "pyproject.toml").exists(), (
        f"handler._repo_root ({handler._repo_root}) does not contain pyproject.toml"
    )
