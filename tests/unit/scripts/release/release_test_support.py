# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Plain helpers shared by the tests of ``scripts/release/assemble_release.py``.

The tests run with ``--import-mode=importlib`` and this directory is not a
package, so the helpers live in a module that each test file imports after it
puts this directory on ``sys.path``. The fixtures are in ``conftest.py``.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]

ARCHIVE_SWITCH = "JERRY_RELEASE_ARCHIVE_TESTS"
ARCHIVE_TOOL_NAMES = ("tar", "zip", "unzip", "gzip", "bsdtar")

BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "github-actions[bot]@users.noreply.github.com"
TAG_DATE = "1786646916 +0000"
VERSION = "1.2.3"


def archive_tests_state() -> tuple[bool, bool, str]:
    """Say whether the archive tests may run here.

    Returns:
        A tuple of ``enabled``, ``forced`` (the switch was set explicitly) and a
        reason that names what decided.
    """
    flag = os.environ.get(ARCHIVE_SWITCH, "").strip()
    if flag == "1":
        return True, True, f"archive tests are switched on by {ARCHIVE_SWITCH}=1"
    if flag == "0":
        return False, True, f"archive tests are switched off by {ARCHIVE_SWITCH}=0"
    if sys.platform == "linux":
        return True, False, "archive tests run by default on Linux"
    return (
        False,
        False,
        f"archive tests run only on Linux unless {ARCHIVE_SWITCH}=1 "
        f"(this platform is {sys.platform})",
    )


def git_env(home: Path, extra: Mapping[str, str] | None = None) -> dict[str, str]:
    """Build an environment for the test's own git calls, starting from nothing."""
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_AUTHOR_NAME": "Test Author",
        "GIT_AUTHOR_EMAIL": "author@example.invalid",
        "GIT_AUTHOR_DATE": "1700000000 +0000",
        "GIT_COMMITTER_NAME": "Test Committer",
        "GIT_COMMITTER_EMAIL": "committer@example.invalid",
        "GIT_COMMITTER_DATE": "1700000000 +0000",
    }
    env.update(extra or {})
    return env


def run_git(
    repo: Path,
    *args: str,
    home: Path,
    extra_env: Mapping[str, str] | None = None,
    stdin: bytes | None = None,
) -> str:
    """Run git in ``repo`` and return its standard output as stripped text."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        input=stdin,
        capture_output=True,
        env=git_env(home, extra_env),
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}"
        )
    return result.stdout.decode("utf-8", "surrogateescape").strip()


STANDARD_FILES: dict[str, str] = {
    "CLAUDE.md": "claude\n",
    "AGENTS.md": "agents\n",
    "GOVERNANCE.md": "governance\n",
    "README.md": "readme\n",
    "pyproject.toml": f'[project]\nname = "jerry"\nversion = "{VERSION}"\n',
    "pytest.ini": "[pytest]\n",
    ".gitignore": "dist/\n",
    ".claude/settings.json": "{}\n",
    ".claude-plugin/plugin.json": "{}\n",
    "skills/alpha/SKILL.md": "alpha skill\n",
    "skills/alpha/agents/a.md": "agent\n",
    "src/pkg/module.py": "x = 1\n",
    "docs/guide.md": "guide\n",
    "scripts/tool.py": "print('tool')\n",
    "hooks/hook.py": "print('hook')\n",
    # Tracked, but not packed:
    ".context/rules/rule.md": "rule\n",
    ".context/patterns/pattern.md": "pattern\n",
    "CHANGELOG.md": "changes\n",
    "uv.lock": "lock\n",
}
STANDARD_LINKS: dict[str, str] = {
    ".claude/patterns": "../.context/patterns",
    ".claude/rules": "../.context/rules",
}
STANDARD_EXECUTABLES = ("scripts/tool.py",)


def build_repo(
    path: Path,
    home: Path,
    files: Mapping[str, str | bytes],
    *,
    links: Mapping[str, str] | None = None,
    executables: tuple[str, ...] = (),
    gitlinks: Mapping[str, str] | None = None,
) -> str:
    """Create a repository at ``path`` with one commit and return the commit id."""
    path.mkdir(parents=True)
    run_git(path, "init", "-q", "-b", "main", home=home)
    for name, content in files.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, str):
            target.write_text(content, encoding="utf-8", newline="")
        else:
            target.write_bytes(content)
        if name in executables:
            target.chmod(0o755)
    for name, link_target in (links or {}).items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(link_target, target)
    run_git(path, "add", "-A", "-f", home=home)
    for name, commit_id in (gitlinks or {}).items():
        run_git(
            path,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{commit_id},{name}",
            home=home,
        )
    run_git(path, "commit", "-q", "-m", "Test commit", home=home)
    return run_git(path, "rev-parse", "HEAD", home=home)


FAKE_TOOL = """#!/bin/sh
# A stand-in for tar or zip: record the call, then write a placeholder output file.
name=$(basename "$0")
{{
  echo "tool=$name"
  echo "cwd=$(pwd)"
  for a in "$@"; do echo "arg=$a"; done
  env | sort | sed 's/^/env=/'
  echo "end"
}} >> '{record}'
if [ -s '{stderr}' ]; then cat '{stderr}' >&2; fi
if [ {code} -eq 0 ]; then printf 'placeholder archive bytes' > "$2"; fi
exit {code}
"""


def parse_calls(record: Path) -> list[dict[str, object]]:
    """Read the record that the fake tools wrote."""
    calls: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    if not record.exists():
        return calls
    for line in record.read_text(encoding="utf-8").splitlines():
        if line.startswith("tool="):
            current = {"tool": line[5:], "cwd": "", "args": [], "env": {}}
        elif current is None:
            continue
        elif line.startswith("cwd="):
            current["cwd"] = line[4:]
        elif line.startswith("arg="):
            current["args"].append(line[4:])  # type: ignore[union-attr]
        elif line.startswith("env="):
            key, _, value = line[4:].partition("=")
            current["env"][key] = value  # type: ignore[index]
        elif line == "end":
            calls.append(current)
            current = None
    return calls


SBOM_TEXT = (
    "{\n"
    '  "$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json",\n'
    '  "bomFormat": "CycloneDX",\n'
    '  "specVersion": "1.6",\n'
    '  "version": 1,\n'
    '  "components": [\n'
    '    {"type": "library", "name": "example", "version": "1.0"}\n'
    "  ]\n"
    "}\n"
)


# The names a child process may receive (guard 2). They are written out here, apart from
# the script, on purpose: a test that only looks for a list of bad names cannot notice a
# new bad name, but a test that checks "only these names" can.
CHILD_GIT_NAMES = frozenset(
    {
        "PATH",
        "HOME",
        "LANG",
        "LC_ALL",
        "GIT_TERMINAL_PROMPT",
        "GIT_NO_REPLACE_OBJECTS",
        "GIT_NO_LAZY_FETCH",
    }
)
CHILD_PACKER_NAMES = frozenset({"PATH", "HOME", "TMPDIR", "TZ", "LANG", "LANGUAGE"})

# Names that make git, tar, zip, gzip, a shell, a program loader or an interpreter do
# something else, or that carry a token or a path of the run. None may reach any child.
HOSTILE_NAMES = (
    # git
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_KEY_0",
    "GIT_CONFIG_VALUE_0",
    "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_EXEC_PATH",
    "GIT_SSH",
    "GIT_SSH_COMMAND",
    "GIT_ASKPASS",
    "SSH_ASKPASS",
    "GIT_EXTERNAL_DIFF",
    "GIT_PAGER",
    "GIT_EDITOR",
    "GIT_SEQUENCE_EDITOR",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_OBJECT_DIRECTORY",
    "GIT_NAMESPACE",
    "GIT_CEILING_DIRECTORIES",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_PROXY_COMMAND",
    "GIT_TRACE",
    "GIT_TRACE2",
    "GIT_DIR",
    "GIT_INDEX_FILE",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_REPLACE_REF_BASE",
    "GIT_PROTOCOL",
    "GIT_SHALLOW_FILE",
    # tar, zip, gzip and the other compressors
    "TAR_OPTIONS",
    "ZIPOPT",
    "ZIP",
    "GZIP",
    "GZIP_OPT",
    "BZIP2",
    "XZ_OPT",
    "TAPE",
    # program loader, shell, interpreters
    "LD_PRELOAD",
    "LD_LIBRARY_PATH",
    "LD_AUDIT",
    "DYLD_INSERT_LIBRARIES",
    "DYLD_LIBRARY_PATH",
    "BASH_ENV",
    "ENV",
    "SHELLOPTS",
    "BASHOPTS",
    "PS4",
    "IFS",
    "CDPATH",
    "GLOBIGNORE",
    "PROMPT_COMMAND",
    "PYTHONPATH",
    "PYTHONHOME",
    "PYTHONSTARTUP",
    "PYTHONINSPECT",
    "PYTHONWARNINGS",
    "PYTHONUSERBASE",
    "PERL5LIB",
    "PERL5OPT",
    "RUBYOPT",
    "NODE_OPTIONS",
    # tokens and paths of the run
    "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
    "ACTIONS_ID_TOKEN_REQUEST_URL",
    "ACTIONS_RUNTIME_TOKEN",
    "ACTIONS_RUNTIME_URL",
    "ACTIONS_CACHE_URL",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "GITHUB_ENV",
    "GITHUB_PATH",
    "GITHUB_OUTPUT",
    "GITHUB_STEP_SUMMARY",
    "GITHUB_WORKSPACE",
    "GITHUB_SHA",
    "RUNNER_TEMP",
    "SSH_AUTH_SOCK",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    # the rest of an ordinary environment
    "TMP",
    "TEMP",
    "USER",
    "LOGNAME",
    "SHELL",
    "PAGER",
    "EDITOR",
    "VISUAL",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_CACHE_HOME",
    "OLDPWD",
    "PWD",
)


def packer_name_is_allowed(name: str) -> bool:
    """Say whether ``tar`` and ``zip`` may receive a variable of this name."""
    return name in CHILD_PACKER_NAMES or name.startswith("LC_")


def assert_inert_output(text: str) -> None:
    """Assert that no line of ``text`` could be read by the runner as a command."""
    for line in text.splitlines():
        assert not line.lstrip().startswith("::"), line
        assert "##[" not in line, line
        assert all(ord(char) >= 0x20 and ord(char) != 0x7F for char in line), repr(line)


# ---------------------------------------------------------------------------
# The work-tree guard: no test of this folder may change `git status` of the work tree
# ---------------------------------------------------------------------------

# The modules for which the guard fixture of conftest.py has been set up in this session.
GUARDED_MODULES: list[str] = []


def work_tree_status(root: Path) -> frozenset[str] | None:
    """Return the lines of ``git status --porcelain`` for the work tree at ``root``.

    The lines are the state of the work tree as git sees it: tracked files that are modified,
    deleted or staged, and untracked files, where an untracked folder is one line however much
    it holds. Ignored files are not listed. git runs without any ``GIT_*`` variable of the
    caller (a git hook sets some that name another index), without a file-system monitor and
    with ``--no-optional-locks``, so the answer is the same inside and outside a hook and the
    call never writes to the index.

    Args:
        root: The top of the work tree.

    Returns:
        The lines, or None when git cannot tell (it is not installed, ``root`` is not a work
        tree, or it failed); the guard then has nothing to compare.
    """
    env = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "--no-optional-locks",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "status.showUntrackedFiles=normal",
                "status",
                "--porcelain",
            ],
            env=env,
            capture_output=True,
            check=False,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    text = result.stdout.decode("utf-8", "replace")
    return frozenset(line for line in text.splitlines() if line)


def session_folders_inside(root: Path, basetemp: Path) -> tuple[str, ...]:
    """Return the base folder of the test session as a path prefix of ``root``, if it lies inside.

    ``--basetemp`` can put the temporary folders of a session inside the work tree, and the
    first test that asks for one creates the folder. That is the session's own doing and not a
    change by a test, so the guard leaves it out.

    Args:
        root: The top of the work tree.
        basetemp: The base folder of the temporary folders of the session.

    Returns:
        A one-item tuple with the folder relative to ``root``, with a trailing slash, or an
        empty tuple when the folder is outside ``root`` or is ``root`` itself.
    """
    try:
        relative = basetemp.resolve().relative_to(root.resolve())
    except ValueError:
        return ()
    if relative == Path():
        return ()
    return (f"{relative.as_posix()}/",)


def work_tree_changes(
    before: frozenset[str], after: frozenset[str], ignored: Sequence[str] = ()
) -> list[str]:
    """Return what differs between two readings of the status, one line each.

    A line that is new is marked ``+ `` and a line that went away ``- ``. A status line is two
    letters, a space and a path (``?? stray.txt``, `` M README.md``). The status says that a
    file differs from the commit, not how, so a file that was already modified and is modified
    again is not seen.

    Args:
        before: The status before.
        after: The status after.
        ignored: Folders, relative to the work tree and with a trailing slash, whose lines are
            left out in both directions.

    Returns:
        The new lines sorted, then the lines that went away sorted.
    """

    def path_of(line: str) -> str:
        return line[3:].rsplit(" -> ", 1)[-1].strip('"')  # a rename reads "old -> new"

    def left_out(line: str) -> bool:
        return any(path_of(line).startswith(prefix) for prefix in ignored)

    new = sorted(line for line in after - before if not left_out(line))
    gone = sorted(line for line in before - after if not left_out(line))
    return [f"+ {line}" for line in new] + [f"- {line}" for line in gone]


def guard_work_tree(root: Path, ignored: Sequence[str] = ()) -> Iterator[None]:
    """Read the status of the work tree, let the tests run, and fail if the status changed.

    This is the body of the fixture in ``conftest.py``, kept here so that a test can run it
    against a throwaway work tree. Use it as ``yield from guard_work_tree(root)``. When git
    cannot answer, before or after, it checks nothing.

    Args:
        root: The top of the work tree.
        ignored: Folders to leave out, as for ``work_tree_changes``.

    Yields:
        Once, while the tests run.
    """
    before = work_tree_status(root)
    yield
    after = work_tree_status(root)
    if before is None or after is None:
        return
    changes = work_tree_changes(before, after, ignored)
    if changes:
        listed = "\n".join(f"  {line}" for line in changes)
        pytest.fail(
            "a test of this module changed the work tree (git status --porcelain):\n"
            f"{listed}\n"
            "A test that needs a file writes it under tmp_path: a name without a folder is "
            "written to the folder the tests run from, and that is the work tree.",
            pytrace=False,
        )
