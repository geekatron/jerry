# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Shared fixtures for the tests of ``scripts/release/assemble_release.py``.

Three things in here matter for how the tests behave.

1. Real ``git`` runs in temporary repositories, with an environment that starts
   empty (no ``GIT_*`` variable from the caller, no global configuration), so
   the tests give the same result inside and outside a git hook.
2. No test in this directory runs the real ``tar``, ``zip`` or ``unzip`` unless
   the archive tests are switched on. The tests that exercise the code around
   those tools use small fake programs that record how they were called. A
   tripwire program that fails loudly stands in for each real tool otherwise.
3. The archive tests (real tools, real archives) are on by default on Linux and
   off elsewhere. ``JERRY_RELEASE_ARCHIVE_TESTS=1`` forces them on and
   ``JERRY_RELEASE_ARCHIVE_TESTS=0`` forces them off, without a code change.
   The skip message names the reason and shows with ``pytest -rs``.
"""

from __future__ import annotations

import os
import shutil
import stat
import sys
import types
from collections.abc import Callable, Iterator, Mapping
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    ARCHIVE_TOOL_NAMES,
    BOT_EMAIL,
    BOT_NAME,
    FAKE_TOOL,
    GUARDED_MODULES,
    HERE,
    REPO_ROOT,
    SBOM_TEXT,
    STANDARD_EXECUTABLES,
    STANDARD_FILES,
    STANDARD_LINKS,
    TAG_DATE,
    VERSION,
    archive_tests_state,
    build_repo,
    guard_work_tree,
    parse_calls,
    run_git,
    session_folders_inside,
)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip the whole directory on Windows: the script runs on Linux and needs POSIX files."""
    if sys.platform != "win32":
        return
    skip = pytest.mark.skip(reason="release script tests need POSIX files and links")
    for item in items:
        if HERE in Path(str(item.fspath)).resolve().parents:
            item.add_marker(skip)


# ---------------------------------------------------------------------------
# The work tree stays as it is found
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True, scope="module")
def work_tree_is_left_as_found(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Iterator[None]:
    """Fail a module whose tests changed ``git status`` of the work tree.

    A test that writes a file with a name that has no folder writes it to the folder the tests
    run from, which is the work tree (a stray file once appeared in the repository root this
    way). The fixture reads ``git status --porcelain`` before the first test of a module and
    after the last, and fails the module, naming the lines that differ, when the two readings
    differ. It compares and does not expect an empty status: the work tree of a developer is
    seldom clean, and an untracked folder that is always there is one line in both readings.
    The temporary folders of the session itself are left out.

    Once for each module and not for each test, because one reading takes about a tenth of a
    second here (measured: 109 ms in a work tree of 6,451 tracked files with one large untracked
    folder), so a reading before and after each of some 800 tests would add more than two
    minutes to a suite that takes about one. The error is reported at the end of the module
    that did it, with the lines that changed.
    """
    GUARDED_MODULES.append(request.module.__name__)
    ignored = session_folders_inside(REPO_ROOT, tmp_path_factory.getbasetemp())
    yield from guard_work_tree(REPO_ROOT, ignored)


# ---------------------------------------------------------------------------
# The environment: no real archive tool, a private home directory
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def tripwire_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Make a directory of programs that fail when a unit test runs a real archive tool."""
    path = tmp_path_factory.mktemp("tripwire")
    for name in ARCHIVE_TOOL_NAMES:
        program = path / name
        program.write_text(
            "#!/bin/sh\n"
            'echo "a unit test ran the real archive tool $0; use the fake tools" >&2\n'
            "exit 97\n",
            encoding="utf-8",
        )
        program.chmod(0o755)
    return path


@pytest.fixture(autouse=True)
def isolated_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    tripwire_dir: Path,
) -> Iterator[Path]:
    """Give each test its own home directory and keep real archive tools out of reach."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    enabled, _, _ = archive_tests_state()
    if not enabled:
        monkeypatch.setenv("PATH", f"{tripwire_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    old_umask = os.umask(0o022)
    os.umask(old_umask)
    yield home
    os.umask(old_umask)


@pytest.fixture
def archive_tools() -> dict[str, str]:
    """Skip unless the real archive tools may run here, then return their paths.

    The skip reason names what decided. When the switch was set to ``1`` a missing
    tool fails the test instead of skipping it, so a forced run cannot pass silently.
    """
    enabled, forced, reason = archive_tests_state()
    if not enabled:
        pytest.skip(reason)
    found = {name: shutil.which(name) for name in ("tar", "zip")}
    missing = [name for name, path in found.items() if path is None]
    if missing:
        message = f"archive tests need {', '.join(missing)} on PATH"
        if forced:
            pytest.fail(message)
        pytest.skip(message)
    return {name: path for name, path in found.items() if path is not None}


# ---------------------------------------------------------------------------
# Real git in temporary repositories
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def standard_repo_template(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    """Build the standard repository once for the whole session."""
    base = tmp_path_factory.mktemp("standard-repo")
    home = base / "home"
    home.mkdir()
    repo = base / "repo"
    commit = build_repo(
        repo,
        home,
        STANDARD_FILES,
        links=STANDARD_LINKS,
        executables=STANDARD_EXECUTABLES,
    )
    return repo, commit


@pytest.fixture
def standard_repo(
    standard_repo_template: tuple[Path, str],
    tmp_path: Path,
) -> tuple[Path, str]:
    """Copy the standard repository for one test and return its path and commit id."""
    template, commit = standard_repo_template
    copy = tmp_path / "work-repo"
    shutil.copytree(template, copy, symlinks=True)
    return copy, commit


@pytest.fixture
def make_repo(tmp_path: Path, isolated_environment: Path) -> Callable[..., tuple[Path, str]]:
    """Return a function that builds a repository with the given content."""
    counter = {"n": 0}

    def make(
        files: Mapping[str, str | bytes] | None = None,
        *,
        links: Mapping[str, str] | None = None,
        executables: tuple[str, ...] = STANDARD_EXECUTABLES,
        gitlinks: Mapping[str, str] | None = None,
        standard: bool = True,
    ) -> tuple[Path, str]:
        counter["n"] += 1
        content: dict[str, str | bytes] = dict(STANDARD_FILES) if standard else {}
        content.update(files or {})
        all_links = dict(STANDARD_LINKS) if standard else {}
        all_links.update(links or {})
        repo = tmp_path / f"repo-{counter['n']}"
        commit = build_repo(
            repo,
            isolated_environment,
            content,
            links=all_links,
            executables=executables,
            gitlinks=gitlinks,
        )
        return repo, commit

    return make


@pytest.fixture
def git_in(isolated_environment: Path) -> Callable[..., str]:
    """Return a function that runs git in a repository with the test environment."""

    def run(
        repo: Path,
        *args: str,
        extra_env: Mapping[str, str] | None = None,
        stdin: bytes | None = None,
    ) -> str:
        return run_git(repo, *args, home=isolated_environment, extra_env=extra_env, stdin=stdin)

    return run


@pytest.fixture
def make_tag(git_in: Callable[..., str]) -> Callable[..., str]:
    """Return a function that makes an annotated tag with a chosen tagger and message."""

    def make(
        repo: Path,
        name: str,
        *,
        commit: str | None = None,
        tagger_name: str = BOT_NAME,
        tagger_email: str = BOT_EMAIL,
        date: str = TAG_DATE,
        message: str | None = None,
    ) -> str:
        env = {
            "GIT_COMMITTER_NAME": tagger_name,
            "GIT_COMMITTER_EMAIL": tagger_email,
            "GIT_COMMITTER_DATE": date,
        }
        text = f"Release {name}" if message is None else message
        args = ["tag", "-a", name, "-m", text]
        if commit:
            args.append(commit)
        git_in(repo, *args, extra_env=env)
        return git_in(repo, "rev-parse", f"refs/tags/{name}")

    return make


@pytest.fixture
def make_raw_tag(git_in: Callable[..., str]) -> Callable[[Path, str, bytes], str]:
    """Return a function that stores a hand-written tag object and points a tag at it."""

    def make(repo: Path, name: str, content: bytes) -> str:
        oid = git_in(
            repo, "hash-object", "-t", "tag", "-w", "--literally", "--stdin", stdin=content
        )
        # ``git update-ref`` refuses an object that git cannot parse as a tag (one with no
        # ``tag`` line, for example), and that is one of the cases to test. So the ref is
        # written as the file that git itself would write.
        ref_file = repo / ".git" / "refs" / "tags" / name
        ref_file.parent.mkdir(parents=True, exist_ok=True)
        ref_file.write_text(f"{oid}\n", encoding="ascii")
        return oid

    return make


@pytest.fixture
def set_origin_main(git_in: Callable[..., str]) -> Callable[[Path, str], None]:
    """Return a function that points ``refs/remotes/origin/main`` at a commit."""

    def point(repo: Path, commit: str) -> None:
        git_in(repo, "update-ref", "refs/remotes/origin/main", commit)

    return point


# ---------------------------------------------------------------------------
# Fake tar and zip
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_tools(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., types.SimpleNamespace]:
    """Return a function that puts fake ``tar`` and ``zip`` first on ``PATH``."""

    def install(
        *,
        tar_code: int = 0,
        zip_code: int = 0,
        tar_stderr: str = "",
        zip_stderr: str = "",
    ) -> types.SimpleNamespace:
        bin_dir = tmp_path / "fake-bin"
        bin_dir.mkdir(exist_ok=True)
        record = tmp_path / "fake-calls.txt"
        for tool, code, text in (("tar", tar_code, tar_stderr), ("zip", zip_code, zip_stderr)):
            stderr_file = tmp_path / f"{tool}-stderr.txt"
            stderr_file.write_text(text, encoding="utf-8")
            program = bin_dir / tool
            program.write_text(
                FAKE_TOOL.format(record=record, stderr=stderr_file, code=code),
                encoding="utf-8",
            )
            program.chmod(stat.S_IRWXU)
        monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
        return types.SimpleNamespace(
            bin_dir=bin_dir,
            record=record,
            calls=lambda: parse_calls(record),
        )

    return install


# ---------------------------------------------------------------------------
# The software bill of materials (SBOM) input and the environment of a run
# ---------------------------------------------------------------------------


@pytest.fixture
def sbom_dir(tmp_path: Path) -> Path:
    """Make a directory with one valid SBOM, as the download step would."""
    path = tmp_path / "sbom-in"
    path.mkdir()
    (path / "sbom.cyclonedx.json").write_text(SBOM_TEXT, encoding="utf-8")
    return path


@pytest.fixture
def run_environment(tmp_path: Path, isolated_environment: Path) -> Callable[..., dict[str, str]]:
    """Return a function that builds the environment variables of a workflow run."""

    def build(
        repo: Path,
        commit: str,
        *,
        event: str = "push",
        tag: str | None = f"v{VERSION}",
        extra: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        runner_temp = tmp_path / "runner-temp"
        runner_temp.mkdir(exist_ok=True)
        env = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": str(isolated_environment),
            "GITHUB_EVENT_NAME": event,
            "GITHUB_SHA": commit,
            "GITHUB_WORKSPACE": str(repo),
            "RUNNER_TEMP": str(runner_temp),
            "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "secret-request-token",
            "ACTIONS_ID_TOKEN_REQUEST_URL": "https://token.example.invalid/request",
            "GITHUB_TOKEN": "secret-github-token",
        }
        if tag is None:
            env["GITHUB_REF"] = "refs/heads/work"
            env["GITHUB_REF_TYPE"] = "branch"
        else:
            env["GITHUB_REF"] = f"refs/tags/{tag}"
            env["GITHUB_REF_TYPE"] = "tag"
        env.update(extra or {})
        return env

    return build
