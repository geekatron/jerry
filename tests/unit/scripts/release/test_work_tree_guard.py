# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests of the work-tree guard.

The guard is an automatic fixture in ``conftest.py``. It takes ``git status --porcelain`` of the
work tree before the tests of a module and again after them, and fails the module when the two
differ: a test that writes a stray file into the folder it runs from (a relative name does that),
or that edits or deletes a tracked file, is found at once instead of by the next ``git status``.

The tests here cover the parts: reading the status, comparing two readings, and the folders of
the test session itself. One test runs the guard end to end, in a throwaway work tree and a
throwaway pytest session, with test modules that behave well and badly. The last tests check
that the real fixture is automatic.
"""

from __future__ import annotations

import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    GUARDED_MODULES,
    HERE,
    REPO_ROOT,
    guard_work_tree,
    session_folders_inside,
    work_tree_changes,
    work_tree_status,
)

pytestmark = pytest.mark.unit

TRACKED = {"tracked.txt": "tracked\n", "other.txt": "other\n", ".gitignore": "dist/\n"}

# --- reading the status ----------------------------------------------------------------------


def test_a_work_tree_with_nothing_changed_has_an_empty_status(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """An unchanged work tree gives an empty status."""
    repo, _ = make_repo(TRACKED, standard=False)
    assert work_tree_status(repo) == frozenset()


def test_a_stray_file_is_one_untracked_line(make_repo: Callable[..., tuple[Path, str]]) -> None:
    """A new stray file shows as one untracked (??) line."""
    repo, _ = make_repo(TRACKED, standard=False)
    (repo / "stray.txt").write_text("stray\n", encoding="utf-8")
    assert work_tree_status(repo) == frozenset({"?? stray.txt"})


def test_an_edited_and_a_deleted_tracked_file_are_lines_of_the_status(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """Editing one tracked file and deleting another gives one status line each."""
    repo, _ = make_repo(TRACKED, standard=False)
    (repo / "tracked.txt").write_text("edited\n", encoding="utf-8")
    (repo / "other.txt").unlink()
    assert work_tree_status(repo) == frozenset({" M tracked.txt", " D other.txt"})


def test_a_staged_change_is_a_line_of_the_status(
    make_repo: Callable[..., tuple[Path, str]], git_in: Callable[..., str]
) -> None:
    """A staged change shows as a status line."""
    repo, _ = make_repo(TRACKED, standard=False)
    (repo / "tracked.txt").write_text("edited\n", encoding="utf-8")
    git_in(repo, "add", "tracked.txt")
    assert work_tree_status(repo) == frozenset({"M  tracked.txt"})


def test_an_untracked_folder_is_one_line_however_much_it_holds(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """An untracked folder shows as a single line, whatever it holds."""
    repo, _ = make_repo(TRACKED, standard=False)
    folder = repo / "project" / "notes"
    folder.mkdir(parents=True)
    (folder / "one.txt").write_text("1\n", encoding="utf-8")
    before = work_tree_status(repo)
    assert before == frozenset({"?? project/"})
    (folder / "two.txt").write_text("2\n", encoding="utf-8")
    (repo / "project" / "three.txt").write_text("3\n", encoding="utf-8")
    after = work_tree_status(repo)
    assert after == before
    assert before is not None
    assert after is not None
    assert work_tree_changes(before, after) == []


def test_an_ignored_file_is_not_a_line_of_the_status(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """A file matched by .gitignore does not appear in the status."""
    repo, _ = make_repo(TRACKED, standard=False)
    (repo / "dist").mkdir()
    (repo / "dist" / "built.txt").write_text("built\n", encoding="utf-8")
    assert work_tree_status(repo) == frozenset()


def test_the_status_is_none_when_git_is_not_there(
    make_repo: Callable[..., tuple[Path, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without git on the path, the status reading is None."""
    repo, _ = make_repo(TRACKED, standard=False)
    monkeypatch.setenv("PATH", "")
    assert work_tree_status(repo) is None


def test_the_status_is_none_when_git_fails(
    make_repo: Callable[..., tuple[Path, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """When git exits with an error, the status reading is None."""
    repo, _ = make_repo(TRACKED, standard=False)

    def fail(arguments: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(arguments, 128, b"", b"fatal: not a git repository")

    monkeypatch.setattr(subprocess, "run", fail)
    assert work_tree_status(repo) is None


def test_git_gets_no_variable_of_the_caller_that_names_another_repository(
    make_repo: Callable[..., tuple[Path, str]],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Caller variables such as GIT_DIR cannot point the reading at another repository."""
    # In a git hook, GIT_INDEX_FILE (and sometimes GIT_DIR) point at the repository of the hook.
    repo, _ = make_repo(TRACKED, standard=False)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "somewhere-else"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "some-index"))
    monkeypatch.setenv("GIT_WORK_TREE", str(tmp_path))
    assert work_tree_status(repo) == frozenset()


def test_the_real_work_tree_can_be_read() -> None:
    """The status of this repository's own work tree can be read."""
    if not (REPO_ROOT / ".git").exists():
        pytest.skip("these tests run from an export of the repository, not from a work tree")
    assert work_tree_status(REPO_ROOT) is not None


# --- comparing two readings -------------------------------------------------------------------


def test_two_equal_readings_have_no_changes() -> None:
    """Two equal readings report no change."""
    reading = frozenset({"?? project/", " M README.md"})
    assert work_tree_changes(reading, reading) == []


def test_a_new_line_is_a_change_marked_with_a_plus() -> None:
    """A status line that appears is reported with a plus sign."""
    before = frozenset({"?? project/"})
    after = frozenset({"?? project/", "?? stray.txt"})
    assert work_tree_changes(before, after) == ["+ ?? stray.txt"]


def test_a_line_that_went_away_is_a_change_marked_with_a_minus() -> None:
    """A status line that disappears is reported with a minus sign."""
    before = frozenset({"?? project/", " M README.md"})
    after = frozenset({"?? project/"})
    assert work_tree_changes(before, after) == ["-  M README.md"]


def test_a_file_that_was_already_changed_and_changed_again_is_not_seen() -> None:
    """A file that was already changed and is changed again adds no line, so it goes unseen."""
    # The status says only that the file differs from the commit, not how. This is the limit of
    # a guard that reads the status; the test records it so that nobody relies on more.
    before = frozenset({" M README.md"})
    assert work_tree_changes(before, before) == []


def test_changes_are_listed_in_a_fixed_order() -> None:
    """Changes are listed in a fixed, sorted order."""
    after = frozenset({"?? b.txt", "?? a.txt", " M c.txt"})
    assert work_tree_changes(frozenset(), after) == ["+  M c.txt", "+ ?? a.txt", "+ ?? b.txt"]


def test_lines_under_a_folder_of_the_session_are_left_out_in_both_directions() -> None:
    """Lines under the test session's own folders are ignored, whether added or removed."""
    before = frozenset({"?? run-1/"})
    after = frozenset({"?? run-2/", "?? stray.txt"})
    assert work_tree_changes(before, after, ("run-1/", "run-2/")) == ["+ ?? stray.txt"]


def test_a_folder_of_the_session_is_matched_as_a_folder_not_as_a_prefix_of_a_name() -> None:
    """A session folder run-1/ does not hide a file named run-10.txt."""
    after = frozenset({"?? run-10.txt"})
    assert work_tree_changes(frozenset(), after, ("run-1/",)) == ["+ ?? run-10.txt"]


def test_a_renamed_file_is_matched_by_the_name_it_has_now() -> None:
    """A rename into a session folder is ignored by its new name."""
    after = frozenset({"R  old.txt -> run-1/new.txt"})
    assert work_tree_changes(frozenset(), after, ("run-1/",)) == []


def test_a_quoted_path_is_matched_without_its_quotes() -> None:
    """A path that git quotes is matched against the session folders without its quotes."""
    after = frozenset({'?? "run-1/a b.txt"'})
    assert work_tree_changes(frozenset(), after, ("run-1/",)) == []


# --- the folders of the session itself ----------------------------------------------------------


def test_the_base_folder_of_a_session_inside_the_work_tree_is_a_folder_to_leave_out(
    tmp_path: Path,
) -> None:
    """A session's base folder inside the work tree is added to the folders to ignore."""
    root = tmp_path / "work"
    (root / ".pytest-run").mkdir(parents=True)
    assert session_folders_inside(root, root / ".pytest-run") == (".pytest-run/",)


def test_a_base_folder_outside_the_work_tree_leaves_nothing_out(tmp_path: Path) -> None:
    """A session's base folder outside the work tree adds nothing to ignore."""
    root = tmp_path / "work"
    root.mkdir()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert session_folders_inside(root, elsewhere) == ()


def test_the_work_tree_itself_is_never_a_folder_to_leave_out(tmp_path: Path) -> None:
    """The work tree's own root is never treated as a folder to ignore."""
    assert session_folders_inside(tmp_path, tmp_path) == ()


# --- the guard, end to end -----------------------------------------------------------------------

SAMPLE_CONFTEST = """\
import os
from pathlib import Path

import pytest
from release_test_support import guard_work_tree


@pytest.fixture(autouse=True, scope="module")
def work_tree_is_left_as_found():
    yield from guard_work_tree(Path(os.environ["GUARDED_WORK_TREE"]))
"""

SAMPLE_HEAD = """\
import os
from pathlib import Path

ROOT = Path(os.environ["GUARDED_WORK_TREE"])


"""

# One module for each behaviour. The test in each module passes by itself; what the guard is
# asked is whether the module left the work tree as it found it.
SAMPLES = {
    "test_leaves_the_tree_alone": (
        'def test_it(tmp_path):\n    (tmp_path / "a.txt").write_text("a")\n'
    ),
    "test_writes_a_stray_file": ('def test_it():\n    (ROOT / "stray.txt").write_text("stray")\n'),
    "test_edits_a_tracked_file": (
        'def test_it():\n    (ROOT / "tracked.txt").write_text("edited")\n'
    ),
    "test_deletes_a_tracked_file": "def test_it():\n    (ROOT / 'other.txt').unlink()\n",
    "test_writes_into_the_folder_that_is_always_there": (
        'def test_it():\n    (ROOT / "always-there" / "new.txt").write_text("new")\n'
    ),
    "test_writes_a_file_and_removes_it": (
        'def test_it():\n    path = ROOT / "passing.txt"\n    path.write_text("p")\n    path.unlink()\n'
    ),
}
LEFT_ALONE = {
    "test_leaves_the_tree_alone",
    "test_writes_into_the_folder_that_is_always_there",
    "test_writes_a_file_and_removes_it",
}


def test_the_guard_fails_a_module_that_changed_the_work_tree_and_only_that_one(
    make_repo: Callable[..., tuple[Path, str]],
    tmp_path: Path,
    isolated_environment: Path,
) -> None:
    """The guard fails the one test module that changed the work tree, and no other."""
    repo, _ = make_repo(TRACKED, standard=False)
    (repo / "always-there").mkdir()
    (repo / "always-there" / "old.txt").write_text("old\n", encoding="utf-8")
    suite = tmp_path / "suite"
    suite.mkdir()
    (suite / "conftest.py").write_text(SAMPLE_CONFTEST, encoding="utf-8")
    for name, body in SAMPLES.items():
        (suite / f"{name}.py").write_text(SAMPLE_HEAD + body, encoding="utf-8")
    report = tmp_path / "report.xml"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(suite),
            "-p",
            "no:cacheprovider",
            "-q",
            f"--junitxml={report}",
        ],
        cwd=suite,
        env={
            "PATH": os.environ.get("PATH", ""),
            "HOME": str(isolated_environment),
            "PYTHONPATH": str(HERE),
            "PYTHONDONTWRITEBYTECODE": "1",
            "GUARDED_WORK_TREE": str(repo),
        },
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    assert result.returncode == 1, result.stdout + result.stderr
    broken = {
        case.get("classname")
        for case in ET.parse(report).iter("testcase")
        if case.find("error") is not None or case.find("failure") is not None
    }
    assert broken == set(SAMPLES) - LEFT_ALONE, result.stdout
    assert "+ ?? stray.txt" in result.stdout
    assert "+  M tracked.txt" in result.stdout
    assert "+  D other.txt" in result.stdout
    assert "always-there" not in result.stdout
    assert "passing.txt" not in result.stdout


def test_the_guard_stays_quiet_when_git_cannot_answer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When git cannot answer, the guard does not fail the module."""
    monkeypatch.setenv("PATH", "")
    steps = guard_work_tree(tmp_path)
    next(steps)  # before: git is not there, so there is nothing to compare
    (tmp_path / "stray.txt").write_text("stray\n", encoding="utf-8")
    with pytest.raises(StopIteration):
        next(steps)


def test_the_guard_names_what_changed_and_what_to_do_about_it(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """The guard's failure message lists what changed and what to do about it."""
    repo, _ = make_repo(TRACKED, standard=False)
    steps = guard_work_tree(repo)
    next(steps)
    (repo / "stray.txt").write_text("stray\n", encoding="utf-8")
    with pytest.raises(pytest.fail.Exception) as info:
        next(steps)
    message = str(info.value)
    assert "+ ?? stray.txt" in message
    assert "tmp_path" in message


# --- the real fixture ------------------------------------------------------------------------------


def test_the_real_guard_is_automatic_for_the_modules_of_this_folder(
    request: pytest.FixtureRequest,
) -> None:
    """The guard runs automatically for every test module in this folder."""
    # The fixture of conftest.py is autouse and runs once for each module; it records the name
    # of every module that it has been set up for. This module is one.
    assert request.module.__name__ in GUARDED_MODULES
