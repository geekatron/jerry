# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for hook wrapper scripts (EN-007).

BDD scenarios:
    - Each wrapper script exists in hooks/ directory
    - Each wrapper is thin (<= 15 lines)
    - No wrapper imports from src/
    - Each wrapper calls the correct jerry CLI command
    - Wrappers always exit 0 (fail-open design)
    - Wrappers handle subprocess timeouts gracefully

References:
    - EN-007: Hook Wrapper Scripts
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import pytest

# Project root for locating hook scripts
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

# Hook wrapper scripts and their expected CLI commands
WRAPPER_SPECS = {
    "session-start": {
        "path": PROJECT_ROOT / "hooks" / "session-start.py",
        "cli_command": "session-start",
        "timeout": 9,
    },
    "pre-compact": {
        "path": PROJECT_ROOT / "hooks" / "pre-compact.py",
        "cli_command": "pre-compact",
        "timeout": 9,
    },
    "pre-tool-use": {
        "path": PROJECT_ROOT / "hooks" / "pre-tool-use.py",
        "cli_command": "pre-tool-use",
        "timeout": 4,
    },
    "user-prompt-submit": {
        "path": PROJECT_ROOT / "hooks" / "user-prompt-submit.py",
        "cli_command": "prompt-submit",
        "timeout": 4,
    },
}


# =============================================================================
# Tests: Wrapper Script Existence and Structure
# =============================================================================


class TestWrapperScriptsExist:
    """BDD: Each hook wrapper script exists in the hooks/ directory."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_wrapper_script_exists(self, name: str, spec: dict) -> None:
        """GIVEN the hooks/ directory WHEN checking for {name} THEN it exists."""
        assert spec["path"].exists(), f"hooks/{name}.py does not exist"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_wrapper_script_is_thin(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN counting lines THEN <= 30 lines."""
        content = spec["path"].read_text()
        line_count = len(content.strip().splitlines())
        assert line_count <= 30, f"hooks/{name}.py has {line_count} lines (max 30)"


class TestWrapperScriptsNoSrcImports:
    """BDD: No wrapper script imports from src/ (thin delegation only)."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_no_src_imports(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN scanning for imports THEN no src/ imports."""
        content = spec["path"].read_text()
        assert "from src" not in content, f"hooks/{name}.py contains 'from src'"
        assert "import src" not in content, f"hooks/{name}.py contains 'import src'"


class TestWrapperScriptsCorrectCliCommand:
    """BDD: Each wrapper calls the correct jerry hooks CLI command."""

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_calls_correct_command(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN contains jerry hooks {command}."""
        content = spec["path"].read_text()
        expected_cmd = f'"hooks", "{spec["cli_command"]}"'
        assert expected_cmd in content, (
            f"hooks/{name}.py does not contain expected command: {expected_cmd}"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_has_correct_timeout(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN has correct timeout."""
        content = spec["path"].read_text()
        expected_timeout = f"timeout={spec['timeout']}"
        assert expected_timeout in content, f"hooks/{name}.py does not contain {expected_timeout}"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_always_exits_zero(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN has sys.exit(0)."""
        content = spec["path"].read_text()
        assert "sys.exit(0)" in content, (
            f"hooks/{name}.py does not contain sys.exit(0) (fail-open required)"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_has_shebang(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading first line THEN has python shebang."""
        content = spec["path"].read_text()
        first_line = content.splitlines()[0]
        assert first_line.startswith("#!/usr/bin/env"), f"hooks/{name}.py missing shebang line"

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_pipes_stdin(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN pipes stdin to subprocess."""
        content = spec["path"].read_text()
        assert "sys.stdin.buffer.read()" in content, (
            f"hooks/{name}.py does not pipe stdin to subprocess"
        )

    @pytest.mark.parametrize("name,spec", WRAPPER_SPECS.items())
    def test_pipes_stdout(self, name: str, spec: dict) -> None:
        """GIVEN hooks/{name}.py WHEN reading content THEN pipes stdout back."""
        content = spec["path"].read_text()
        assert "sys.stdout.buffer.write" in content, f"hooks/{name}.py does not pipe stdout back"


# =============================================================================
# Helpers: start hook commands from a plugin folder whose path has a space (#435)
# =============================================================================
#
# These helpers model how a command hook is started. They do not run Claude Code, uv or Jerry.
#
# What the model follows, from Claude Code's documentation:
#   - Hooks reference, "Exec form and shell form" (https://code.claude.com/docs/en/hooks):
#     a command hook without `args` is passed to `sh -c` on macOS and Linux; one with `args` is
#     spawned directly with no shell, and the placeholder is substituted into `command` and into
#     each `args` element; both forms export CLAUDE_PLUGIN_ROOT in the hook's environment.
#   - Plugins reference, "Where each variable resolves"
#     (https://code.claude.com/docs/en/plugins/manifest-reference): for hook commands the
#     placeholder resolves "Anywhere in `command` and `args`".
# The documentation describes both a replaced placeholder and an exported variable, so a
# shell-form command is started both ways: with the placeholder replaced in the text before
# `sh -c` ("placeholder-replaced"), and with the text as written and the variable left for the
# shell to expand ("variable-expanded"). A hook with `args` is started with no shell
# ("exec-form"). On Windows, Claude Code uses Git Bash or PowerShell; this model does not cover it.
#
# uv is replaced by the small /bin/sh script in _UV_STAND_IN; its folder is the only entry on PATH.
# It checks what uv would check here (the folder after --directory exists, the script file exists),
# fails with the error text that #435 reports for uv when one is missing, records its arguments
# and, for a script, runs the script with this test's own Python. It never starts Jerry and never
# installs anything.

# The placeholder that the hooks.json commands use for the plugin folder.
_PLACEHOLDER = "${CLAUDE_PLUGIN_ROOT}"

# Seconds that one start of a hook command may take; a start takes a fraction of a second.
_START_TIMEOUT_SECONDS = 30

# The uv stand-in. It handles `uv run [options] --directory DIR TARGET [arguments]` where TARGET is
# a .py file (run with the Python in STAND_IN_PYTHON) or `jerry` (the wrapper's own call, which only
# exits 0). Options other than --directory are skipped, so the value of an option that takes one
# is taken as the target. A target that is neither a .py file, nor `jerry`, nor an existing path
# makes the stand-in print `stand-in uv: unsupported option or target` and exit 3, so such a
# failure is not mistaken for uv's missing-file error.
# Each call is appended to STAND_IN_LOG as its arguments, each followed by a NUL byte, and then a
# byte with the value 1.
_UV_STAND_IN = r"""#!/bin/sh
{ printf '%s\0' "$@"; printf '\001'; } >> "$STAND_IN_LOG"
fail() {
    echo "error: No such file or directory (os error 2)" >&2
    exit 2
}
if [ "$1" != run ]; then
    echo "stand-in uv: only 'uv run' is supported" >&2
    exit 3
fi
shift
directory=
while [ "$#" -gt 0 ]; do
    case "$1" in
        --directory)
            [ "$#" -ge 2 ] || fail
            directory=$2
            shift 2
            ;;
        -*) shift ;;
        *) break ;;
    esac
done
[ -z "$directory" ] || [ -d "$directory" ] || fail
case "$1" in
    jerry) exit 0 ;;
    *.py)
        [ -f "$1" ] || fail
        exec "$STAND_IN_PYTHON" "$@"
        ;;
    *)
        if [ ! -e "$1" ]; then
            echo "stand-in uv: unsupported option or target" >&2
            exit 3
        fi
        echo "stand-in uv: cannot run '$1'" >&2
        exit 3
        ;;
esac
"""


@pytest.fixture(scope="module")
def uv_stand_in_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Return a folder with the uv stand-in in it, written once for the module.

    On the macOS machine where this test was written, the first run of a newly written script took
    0.2 to 0.5 seconds and later runs 0.04 seconds, so the tests share one script.
    """
    bin_dir = tmp_path_factory.mktemp("uv-stand-in")
    stand_in = bin_dir / "uv"
    stand_in.write_text(_UV_STAND_IN, encoding="utf-8")
    stand_in.chmod(0o755)
    return bin_dir


class _HookStart(NamedTuple):
    """How one start of a hook command ended: exit code, stderr text and the uv calls it made."""

    returncode: int
    stderr: str
    calls: list[list[str]]


def _command_hooks() -> list[tuple[str, dict]]:
    """Return every command hook in hooks/hooks.json as an ``(event, hook)`` pair."""
    hooks_json = json.loads((PROJECT_ROOT / "hooks" / "hooks.json").read_text())
    return [
        (event, hook)
        for event, entries in hooks_json["hooks"].items()
        for entry in entries
        for hook in entry.get("hooks", [])
        if hook.get("type") == "command"
    ]


def _start_cases() -> list[object]:
    """Return one test case per command hook in hooks.json and per way its command is started.

    A hook with ``args`` is started with no shell. Any other hook is started both with the
    placeholder replaced in its text and with the text as written (see the notes above).
    """
    cases: list[object] = []
    for event, hook in _command_hooks():
        forms = ["exec-form"] if "args" in hook else ["placeholder-replaced", "variable-expanded"]
        cases.extend(pytest.param(event, hook, form, id=f"{event}-{form}") for form in forms)
    return cases


def _uv_calls(log: Path) -> list[list[str]]:
    """Return the calls that the uv stand-in recorded in ``log``: one list of arguments per call."""
    if not log.exists():
        return []
    chunks = [chunk for chunk in log.read_bytes().split(b"\x01") if chunk]
    return [[arg.decode("utf-8") for arg in chunk.split(b"\0")[:-1]] for chunk in chunks]


def _start_hook(hook: dict, form: str, plugin_root: Path, uv_dir: Path, log: Path) -> _HookStart:
    """Start one hook command from ``plugin_root`` with the uv stand-in as the only tool on PATH.

    ``plugin_root`` gets a copy of the real wrapper scripts in hooks/. ``uv_dir`` holds the
    stand-in and ``log`` receives its calls. ``form`` is one of the forms that ``_start_cases``
    names. The environment holds CLAUDE_PLUGIN_ROOT in each form, as the documentation says.
    """
    hooks_dir = plugin_root / "hooks"
    hooks_dir.mkdir(parents=True)
    for script in (PROJECT_ROOT / "hooks").glob("*.py"):
        shutil.copy2(script, hooks_dir / script.name)
    root = str(plugin_root)
    env = {
        "PATH": str(uv_dir),
        "CLAUDE_PLUGIN_ROOT": root,
        "STAND_IN_LOG": str(log),
        "STAND_IN_PYTHON": sys.executable,
    }
    command = hook["command"]
    if form == "exec-form":
        argv = [part.replace(_PLACEHOLDER, root) for part in [command, *hook["args"]]]
    elif form == "placeholder-replaced":
        argv = ["/bin/sh", "-c", command.replace(_PLACEHOLDER, root)]
    else:
        argv = ["/bin/sh", "-c", command]
    done = subprocess.run(
        argv,
        input=b"{}",
        capture_output=True,
        env=env,
        cwd=log.parent,
        timeout=_START_TIMEOUT_SECONDS,
        check=False,
    )
    return _HookStart(done.returncode, done.stderr.decode("utf-8", "replace"), _uv_calls(log))


def _short(value: object, tmp_path: Path) -> str:
    """Return the text of ``value`` with the pytest temporary folder shortened to ``<tmp>``."""
    return str(value).replace(str(tmp_path), "<tmp>")


# =============================================================================
# Tests: hooks.json Structure
# =============================================================================


class TestHooksJsonStructure:
    """BDD: hooks.json has correct structure with all hook events."""

    @pytest.fixture()
    def hooks_json(self) -> dict:
        """Load and parse hooks.json."""
        hooks_path = PROJECT_ROOT / "hooks" / "hooks.json"
        assert hooks_path.exists(), "hooks/hooks.json does not exist"
        content = hooks_path.read_text()
        return json.loads(content)

    def test_hooks_json_is_valid(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN parsed THEN is valid JSON with hooks key."""
        assert "hooks" in hooks_json
        assert "description" in hooks_json

    def test_session_start_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking SessionStart THEN points to hooks/session-start.py."""
        assert "SessionStart" in hooks_json["hooks"]
        session_start = hooks_json["hooks"]["SessionStart"]
        commands = [h["command"] for entry in session_start for h in entry.get("hooks", [])]
        assert any("hooks/session-start.py" in cmd for cmd in commands), (
            f"SessionStart does not point to hooks/session-start.py. Commands: {commands}"
        )

    def test_user_prompt_submit_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking UserPromptSubmit THEN points to hooks/user-prompt-submit.py."""
        assert "UserPromptSubmit" in hooks_json["hooks"]
        prompt_submit = hooks_json["hooks"]["UserPromptSubmit"]
        commands = [h["command"] for entry in prompt_submit for h in entry.get("hooks", [])]
        assert any("hooks/user-prompt-submit.py" in cmd for cmd in commands), (
            f"UserPromptSubmit does not point to hooks/user-prompt-submit.py. Commands: {commands}"
        )

    def test_pre_compact_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking PreCompact THEN points to hooks/pre-compact.py."""
        assert "PreCompact" in hooks_json["hooks"]
        pre_compact = hooks_json["hooks"]["PreCompact"]
        commands = [h["command"] for entry in pre_compact for h in entry.get("hooks", [])]
        assert any("hooks/pre-compact.py" in cmd for cmd in commands), (
            f"PreCompact does not point to hooks/pre-compact.py. Commands: {commands}"
        )

    def test_pre_tool_use_registered(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking PreToolUse THEN has hooks/pre-tool-use.py."""
        assert "PreToolUse" in hooks_json["hooks"]
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        commands = [h["command"] for entry in pre_tool_use for h in entry.get("hooks", [])]
        assert any("hooks/pre-tool-use.py" in cmd for cmd in commands), (
            f"PreToolUse does not include hooks/pre-tool-use.py. Commands: {commands}"
        )

    def test_pre_tool_use_consolidated_single_cli_path(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN PreToolUse THEN single CLI path after #150 consolidation."""
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        commands = [h["command"] for entry in pre_tool_use for h in entry.get("hooks", [])]
        assert len(commands) == 1, f"PreToolUse should have 1 hook after #150. Found: {commands}"
        assert "hooks/pre-tool-use.py" in commands[0]

    def test_subagent_stop_consolidated_single_cli_path(self, hooks_json: dict) -> None:
        """GIVEN hooks.json WHEN checking SubagentStop THEN uses single CLI path (STORY-024)."""
        assert "SubagentStop" in hooks_json["hooks"]
        subagent = hooks_json["hooks"]["SubagentStop"]
        commands = [h["command"] for entry in subagent for h in entry.get("hooks", [])]
        assert len(commands) == 1, (
            f"SubagentStop should have 1 hook after STORY-024. Found: {commands}"
        )
        assert "hooks/subagent-stop.py" in commands[0]

    def test_session_start_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json SessionStart WHEN checking timeout THEN is 10000ms."""
        session_start = hooks_json["hooks"]["SessionStart"]
        for entry in session_start:
            for hook in entry.get("hooks", []):
                if "session-start.py" in hook.get("command", ""):
                    assert hook["timeout"] == 10000

    def test_user_prompt_submit_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json UserPromptSubmit WHEN checking timeout THEN is 5000ms."""
        prompt_submit = hooks_json["hooks"]["UserPromptSubmit"]
        for entry in prompt_submit:
            for hook in entry.get("hooks", []):
                if "user-prompt-submit.py" in hook.get("command", ""):
                    assert hook["timeout"] == 5000

    def test_pre_compact_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json PreCompact WHEN checking timeout THEN is 10000ms."""
        pre_compact = hooks_json["hooks"]["PreCompact"]
        for entry in pre_compact:
            for hook in entry.get("hooks", []):
                if "pre-compact.py" in hook.get("command", ""):
                    assert hook["timeout"] == 10000

    def test_pre_tool_use_context_monitor_timeout(self, hooks_json: dict) -> None:
        """GIVEN hooks.json PreToolUse context monitor hook WHEN checking timeout THEN is 5000ms."""
        pre_tool_use = hooks_json["hooks"]["PreToolUse"]
        for entry in pre_tool_use:
            for hook in entry.get("hooks", []):
                if "hooks/pre-tool-use.py" in hook.get("command", ""):
                    assert hook["timeout"] == 5000

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="starts commands with /bin/sh and a /bin/sh stand-in for uv; Windows has neither",
    )
    @pytest.mark.parametrize(("event", "hook", "form"), _start_cases())
    def test_hook_start_when_plugin_path_has_space_then_uv_gets_whole_paths(
        self, tmp_path: Path, uv_stand_in_dir: Path, event: str, hook: dict, form: str
    ) -> None:
        """GIVEN a command hook in hooks.json and a plugin folder whose path has a space
        WHEN the command is started from that folder (#435)
        THEN the hook exits 0 with nothing on stderr, and uv gets the same arguments as from a
        folder without a space, with the folder path swapped (so no path splits at the space).

        #435 reports that a plugin folder under "Application Support" splits an unquoted
        ${CLAUDE_PLUGIN_ROOT}. The start is modelled, not run in Claude Code: see the notes above
        _UV_STAND_IN. The start from a folder without a space gives the arguments to expect, and
        shows that the set-up works.
        """
        plain_root = tmp_path / "plugins" / "jerry"
        spaced_root = tmp_path / "Application Support" / "jerry"

        control = _start_hook(hook, form, plain_root, uv_stand_in_dir, tmp_path / "control.log")
        started = _start_hook(hook, form, spaced_root, uv_stand_in_dir, tmp_path / "spaced.log")

        wanted = [
            [arg.replace(str(plain_root), str(spaced_root)) for arg in call]
            for call in control.calls
        ]
        assert control.returncode == 0 and not control.stderr and control.calls, (
            f"{event} ({form}): the command does not start even from a folder whose path has no "
            f"space, so the command or this set-up is broken. exit code {control.returncode}, "
            f"stderr {control.stderr!r}, uv received {_short(control.calls, tmp_path)}"
        )
        report = (
            f"{event} ({form}) from a folder whose path has a space: "
            f"exit code {started.returncode}, stderr {started.stderr!r}; "
            f"uv received {_short(started.calls, tmp_path)}; "
            f"uv should receive {_short(wanted, tmp_path)}"
        )
        assert started.returncode == 0, report
        assert not started.stderr, report
        assert started.calls == wanted, report


# =============================================================================
# Tests: Retired Scripts
# =============================================================================


class TestRetiredScripts:
    """BDD: Old hook scripts are retired (not deleted)."""

    def test_session_start_hook_retired(self) -> None:
        """GIVEN scripts/session_start_hook.py WHEN checking THEN is marked retired."""
        retired_path = PROJECT_ROOT / "scripts" / "session_start_hook.py.retired"
        original_path = PROJECT_ROOT / "scripts" / "session_start_hook.py"
        # Either renamed to .retired OR original has retired comment at top
        if retired_path.exists():
            assert True
        elif original_path.exists():
            content = original_path.read_text()
            assert "RETIRED" in content.upper(), (
                "scripts/session_start_hook.py exists but is not marked as retired"
            )
        else:
            pytest.fail(
                "Neither scripts/session_start_hook.py nor "
                "scripts/session_start_hook.py.retired exists"
            )
