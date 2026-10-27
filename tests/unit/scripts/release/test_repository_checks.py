# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the checks on the run, the tag and the version.

These use real ``git`` in temporary repositories: annotated tags with a chosen
tagger and message, hand-written tag objects for the malformed cases, and
commits that are, or are not, on the first-parent line of ``origin/main``.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    BOT_EMAIL,
    BOT_NAME,
    TAG_DATE,
    VERSION,
    assert_inert_output,
)

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

TAGGER = f"{BOT_NAME} <{BOT_EMAIL}> {TAG_DATE}"


def git_environment() -> dict[str, str]:
    """Return the environment that the script gives to git."""
    return ar.git_environment({"PATH": os.environ.get("PATH", "")})


def raw_tag_bytes(
    commit: str,
    tag: str,
    *,
    tagger: str = TAGGER,
    extra: str = "",
    message: str | None = None,
) -> bytes:
    """Build the bytes of a tag object, with room for mistakes."""
    text = message if message is not None else f"Release {tag}\n"
    return f"object {commit}\ntype commit\ntag {tag}\ntagger {tagger}\n{extra}\n{text}".encode()


# --- check_event -----------------------------------------------------------


@pytest.mark.parametrize(("event", "expected"), [("push", False), ("workflow_dispatch", True)])
def test_check_event_returns_whether_the_run_is_check_only(event: str, expected: bool) -> None:
    """check_event reports a manual run as check-only and a tag push as a real release."""
    assert ar.check_event({"GITHUB_EVENT_NAME": event}) is expected


@pytest.mark.parametrize("event", ["", "pull_request", "schedule", "::error::x"])
def test_check_event_rejects_any_other_event(event: str) -> None:
    """check_event refuses any event other than a tag push or a manual run."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_event({"GITHUB_EVENT_NAME": event})
    assert "tag push or a manual check" in str(info.value)
    assert_inert_output(str(info.value))


def test_check_event_rejects_a_run_without_an_event_name() -> None:
    """check_event refuses a run whose event name is missing."""
    with pytest.raises(ar.Rejected):
        ar.check_event({})


# --- check_repository --------------------------------------------------------


def test_check_repository_accepts_the_top_of_a_work_tree(standard_repo: tuple[Path, str]) -> None:
    """check_repository accepts the top folder of a git work tree."""
    repo, _ = standard_repo
    ar.check_repository(repo, git_environment())


def test_check_repository_rejects_a_folder_inside_a_work_tree(
    standard_repo: tuple[Path, str],
) -> None:
    """check_repository refuses a tracked subfolder; the reason asks for the top of a work tree."""
    repo, _ = standard_repo
    with pytest.raises(ar.Rejected) as info:
        ar.check_repository(repo / "docs", git_environment())
    assert "top of a work tree" in str(info.value)


def test_check_repository_rejects_a_folder_that_is_not_a_repository(tmp_path: Path) -> None:
    """check_repository refuses a folder that is not in a git repository."""
    folder = tmp_path / "plain"
    folder.mkdir()
    with pytest.raises(ar.Rejected):
        ar.check_repository(folder, git_environment())


def test_check_repository_rejects_a_folder_inside_a_work_tree_that_is_not_a_repository_itself(
    standard_repo: tuple[Path, str],
) -> None:
    """check_repository refuses an untracked plain folder inside a work tree, too."""
    repo, _ = standard_repo
    plain = repo / "not-tracked-folder"
    plain.mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.check_repository(plain, git_environment())
    assert "top of a work tree" in str(info.value)


def test_check_repository_says_when_git_is_not_installed(tmp_path: Path) -> None:
    """check_repository says so when git is not installed."""
    empty = tmp_path / "empty-path"
    empty.mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.check_repository(tmp_path, {"PATH": str(empty)})
    assert "git is not installed" in str(info.value)


# --- check_head ---------------------------------------------------------------


def test_check_head_returns_the_commit_when_the_checkout_is_the_triggering_commit(
    standard_repo: tuple[Path, str], run_environment: Callable[..., dict[str, str]]
) -> None:
    """check_head returns the commit when HEAD is the commit that started the run."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit)
    assert ar.check_head(repo, environ, ar.git_environment(environ)) == commit


def test_check_head_rejects_a_checkout_that_is_another_commit(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    git_in: Callable[..., str],
) -> None:
    """check_head refuses a checkout whose HEAD is not the triggering commit."""
    repo, commit = standard_repo
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "second")
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_head(repo, environ, ar.git_environment(environ))
    assert "not the commit that triggered this run" in str(info.value)


@pytest.mark.parametrize("bad", ["", "ABC", "a" * 39, "a" * 41, "g" * 40, "A" * 40, "::error::x"])
def test_check_head_rejects_a_triggering_commit_that_is_not_forty_lowercase_hex_digits(
    bad: str, standard_repo: tuple[Path, str], run_environment: Callable[..., dict[str, str]]
) -> None:
    """check_head refuses a GITHUB_SHA that is not 40 lowercase hex digits."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, extra={"GITHUB_SHA": bad})
    with pytest.raises(ar.Rejected) as info:
        ar.check_head(repo, environ, ar.git_environment(environ))
    assert "GITHUB_SHA" in str(info.value)
    assert_inert_output(str(info.value))


# --- check_tag: the accepted case and the cases that are skipped --------------


def test_check_tag_accepts_an_annotated_tag_by_the_bot_on_the_first_parent_line(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag accepts the bot's annotated tag on a commit on main's first-parent line."""
    repo, commit = standard_repo
    make_tag(repo, f"v{VERSION}")
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    assert ar.check_tag(repo, environ, commit, ar.git_environment(environ)) == f"v{VERSION}"


def test_check_tag_skips_every_tag_check_for_a_branch_ref(
    standard_repo: tuple[Path, str], run_environment: Callable[..., dict[str, str]]
) -> None:
    """For a branch ref, check_tag runs no tag check and returns None."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, event="workflow_dispatch", tag=None)
    assert ar.check_tag(repo, environ, commit, ar.git_environment(environ)) is None


# --- check_tag: the tag name ---------------------------------------------------


@pytest.mark.parametrize(
    "ref",
    [
        "refs/tags/1.2.3",
        "refs/tags/V1.2.3",
        "refs/tags/v1.2",
        "refs/tags/v01.2.3",
        "refs/tags/v1.2.3-",
        "refs/tags/v1.2.3-a..b",
        "refs/tags/v1.2.3+build",
        "refs/tags/v1.2.3-rc.1.2.3.4",
        "refs/tags/v1.2.3 ",
        "refs/tags/v1234567.2.3",
        "refs/tags/v1.2.3-" + "a" * 40,
        "refs/tags/v1.2.3\n::error::x",
    ],
)
def test_check_tag_rejects_a_name_that_is_not_a_version_tag(
    ref: str, standard_repo: tuple[Path, str], run_environment: Callable[..., dict[str, str]]
) -> None:
    """check_tag refuses a tag name that is not a version tag."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, extra={"GITHUB_REF": ref})
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert_inert_output(str(info.value))


def test_check_tag_rejects_a_ref_that_is_not_a_tag_ref_although_the_type_says_tag(
    standard_repo: tuple[Path, str], run_environment: Callable[..., dict[str, str]]
) -> None:
    """check_tag refuses a ref outside refs/tags/ even when the ref type says tag."""
    repo, commit = standard_repo
    environ = run_environment(repo, commit, extra={"GITHUB_REF": "refs/heads/v1.2.3"})
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "not a tag ref" in str(info.value)


@pytest.mark.parametrize(
    "name",
    ["v0.0.0", "v1.2.3", "v10.200.3000", "v1.2.3-rc", "v1.2.3-rc.1", "v1.2.3-beta.1.2.3"],
)
def test_check_tag_accepts_the_version_forms_that_the_old_checks_accepted(
    name: str,
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag accepts every version form that the old workflow checks accepted."""
    repo, commit = standard_repo
    make_tag(repo, name)
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit, tag=name)
    assert ar.check_tag(repo, environ, commit, ar.git_environment(environ)) == name


# --- check_tag: the tag object ---------------------------------------------------


def test_check_tag_rejects_a_tag_that_is_not_in_the_checkout(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag that the checkout does not have."""
    repo, commit = standard_repo
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "tag is not in this checkout" in str(info.value)


def test_check_tag_rejects_a_lightweight_tag(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    git_in: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a lightweight tag."""
    repo, commit = standard_repo
    git_in(repo, "tag", f"v{VERSION}", commit)
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "not an annotated tag" in str(info.value)


def test_check_tag_rejects_a_tag_that_was_moved_to_another_commit(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    git_in: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag that points at another commit than the run's."""
    repo, commit = standard_repo
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "second")
    second = git_in(repo, "rev-parse", "HEAD")
    make_tag(repo, f"v{VERSION}", commit=second)
    set_origin_main(repo, second)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "does not point at the commit that triggered this run" in str(info.value)


def test_check_tag_rejects_a_tag_made_by_a_person(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag whose tagger is not the bot's name and email."""
    repo, commit = standard_repo
    make_tag(repo, f"v{VERSION}", tagger_name="A Person", tagger_email="person@example.invalid")
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "tagger of the tag is not the version bump bot" in str(info.value)


@pytest.mark.parametrize(
    "message", ["hello", "Release v9.9.9", f"Release v{VERSION}\n\nmore text", ""]
)
def test_check_tag_rejects_a_tag_whose_message_is_not_exactly_release_and_the_tag(
    message: str,
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag whose message is not exactly Release followed by the tag."""
    repo, commit = standard_repo
    body = f"{message}\n" if message else ""
    make_raw_tag(repo, f"v{VERSION}", raw_tag_bytes(commit, f"v{VERSION}", message=body))
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "message of the tag" in str(info.value)


def test_check_tag_rejects_a_tag_with_a_second_tagger_line(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag object with a second tagger line."""
    repo, commit = standard_repo
    other = f"A Person <person@example.invalid> {TAG_DATE}"
    make_raw_tag(
        repo, f"v{VERSION}", raw_tag_bytes(commit, f"v{VERSION}", extra=f"tagger {other}\n")
    )
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "header that a release tag never has" in str(info.value)


def test_check_tag_rejects_a_tag_object_that_names_another_tag(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag object whose tag line names another tag."""
    repo, commit = standard_repo
    make_raw_tag(repo, f"v{VERSION}", raw_tag_bytes(commit, "v9.9.9", message="Release v9.9.9\n"))
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "names another tag" in str(info.value)


def test_check_tag_rejects_a_tag_object_whose_type_line_is_not_commit(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag object that does not point at a commit."""
    repo, commit = standard_repo
    content = (
        f"object {commit}\ntype tree\ntag v{VERSION}\ntagger {TAGGER}\n\nRelease v{VERSION}\n"
    ).encode()
    make_raw_tag(repo, f"v{VERSION}", content)
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "does not point at a commit" in str(info.value)


def test_check_tag_rejects_a_tag_that_holds_a_nul_byte(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag object that contains a NUL byte."""
    repo, commit = standard_repo
    content = raw_tag_bytes(commit, f"v{VERSION}")[:-1] + b"\x00\n"
    make_raw_tag(repo, f"v{VERSION}", content)
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "NUL" in str(info.value)


def test_check_tag_rejects_a_tag_header_that_is_incomplete(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tag object whose header lacks a required line."""
    repo, commit = standard_repo
    make_raw_tag(repo, f"v{VERSION}", f"object {commit}\ntype commit\n".encode())
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "header of the tag is incomplete" in str(info.value)


@pytest.mark.parametrize(
    "tagger",
    [
        f"{BOT_NAME} <{BOT_EMAIL}> 0123456789012 +0000",
        f"{BOT_NAME} <{BOT_EMAIL}> 17 0000",
        f"{BOT_NAME} <{BOT_EMAIL}> x +0000",
        f"{BOT_NAME} <{BOT_EMAIL}>",
        f"someone-else <{BOT_EMAIL}> {TAG_DATE}",
    ],
)
def test_check_tag_rejects_a_tagger_line_of_the_wrong_shape(
    tagger: str,
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_raw_tag: Callable[[Path, str, bytes], str],
    set_origin_main: Callable[[Path, str], None],
) -> None:
    """check_tag refuses a tagger line that does not have the expected shape."""
    repo, commit = standard_repo
    make_raw_tag(repo, f"v{VERSION}", raw_tag_bytes(commit, f"v{VERSION}", tagger=tagger))
    set_origin_main(repo, commit)
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "tagger" in str(info.value)


# --- check_tag: the tagged commit must be on the first-parent line of origin/main --


def test_check_tag_rejects_a_checkout_without_origin_main(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
) -> None:
    """check_tag refuses a checkout that has no origin/main to compare with."""
    repo, commit = standard_repo
    make_tag(repo, f"v{VERSION}")
    environ = run_environment(repo, commit)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, commit, ar.git_environment(environ))
    assert "origin/main is not in this checkout" in str(info.value)


def test_check_tag_rejects_a_commit_that_origin_main_does_not_contain(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
    git_in: Callable[..., str],
) -> None:
    """check_tag refuses a tagged commit that is not in origin/main."""
    repo, commit = standard_repo
    git_in(repo, "switch", "-q", "-c", "elsewhere")
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "not on main")
    other = git_in(repo, "rev-parse", "HEAD")
    make_tag(repo, f"v{VERSION}", commit=other)
    set_origin_main(repo, commit)
    environ = run_environment(repo, other)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, other, ar.git_environment(environ))
    assert "first-parent line of origin/main" in str(info.value)


def test_check_tag_rejects_a_commit_that_main_reached_only_through_a_merged_side_branch(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
    git_in: Callable[..., str],
) -> None:
    """check_tag refuses a commit that main reaches only through a merged side branch."""
    repo, _ = standard_repo
    git_in(repo, "switch", "-q", "-c", "side")
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "side work")
    side = git_in(repo, "rev-parse", "HEAD")
    git_in(repo, "switch", "-q", "main")
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "main work")
    git_in(repo, "merge", "-q", "--no-ff", "-m", "merge side", "side")
    merged = git_in(repo, "rev-parse", "HEAD")
    make_tag(repo, f"v{VERSION}", commit=side)
    set_origin_main(repo, merged)
    # The commit is reachable from main (git exits 0), but it is not on the first-parent line.
    git_in(repo, "merge-base", "--is-ancestor", side, merged)
    environ = run_environment(repo, side)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tag(repo, environ, side, ar.git_environment(environ))
    assert "first-parent line of origin/main" in str(info.value)


def test_check_tag_accepts_a_commit_that_is_older_than_the_tip_of_origin_main(
    standard_repo: tuple[Path, str],
    run_environment: Callable[..., dict[str, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
    git_in: Callable[..., str],
) -> None:
    """check_tag accepts a commit on main's first-parent line that is older than its tip."""
    repo, commit = standard_repo
    make_tag(repo, f"v{VERSION}")
    git_in(repo, "commit", "--allow-empty", "-q", "-m", "later work")
    set_origin_main(repo, git_in(repo, "rev-parse", "HEAD"))
    environ = run_environment(repo, commit)
    assert ar.check_tag(repo, environ, commit, ar.git_environment(environ)) == f"v{VERSION}"


# --- check_version ------------------------------------------------------------------


def test_check_version_reads_the_project_version_of_the_tagged_commit(
    standard_repo: tuple[Path, str],
) -> None:
    """check_version reads the project version from the tagged commit's pyproject.toml."""
    repo, commit = standard_repo
    assert ar.check_version(repo, commit, None, git_environment()) == VERSION
    assert ar.check_version(repo, commit, f"v{VERSION}", git_environment()) == VERSION


def test_check_version_rejects_a_tag_whose_version_differs_from_pyproject(
    standard_repo: tuple[Path, str],
) -> None:
    """check_version refuses a tag whose version differs from pyproject.toml."""
    repo, commit = standard_repo
    with pytest.raises(ar.Rejected) as info:
        ar.check_version(repo, commit, "v1.2.4", git_environment())
    assert "version of the tag (1.2.4)" in str(info.value)
    assert f"({VERSION})" in str(info.value)


@pytest.mark.parametrize(
    ("pyproject", "reason"),
    [
        ("[project]\nname = 'x'\n", "no [project] version"),
        ("[tool.other]\nversion = '1.2.3'\n", "no [project] version"),
        ("[project]\nversion = 1\n", "no [project] version"),
        ("[project]\ndynamic = ['version']\n", "no [project] version"),
        ("[project\nversion = '1.2.3'\n", "not valid TOML"),
        ("[project]\nversion = '1.2.3'\nversion = '1.2.4'\n", "not valid TOML"),
        ("[project]\nversion = '1.2'\n", "not of the form"),
        ("[project]\nversion = '01.2.3'\n", "not of the form"),
        ("[project]\nversion = '1.2.3+local'\n", "not of the form"),
        ("[project]\nversion = '1.2.3-" + "a" * 40 + "'\n", "not of the form"),
        (b"[project]\nversion = '1.2.3'\n\x00", "NUL"),
        (b"[project]\nversion = '1.2.3'\n\xff\xfe", "UTF-8"),
    ],
)
def test_check_version_rejects_a_pyproject_without_one_valid_project_version(
    pyproject: str | bytes,
    reason: str,
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """check_version refuses a pyproject.toml without exactly one valid project version."""
    repo, commit = make_repo({"pyproject.toml": pyproject})
    with pytest.raises(ar.Rejected) as info:
        ar.check_version(repo, commit, None, git_environment())
    assert reason in str(info.value)


def test_check_version_rejects_a_commit_without_pyproject(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """check_version refuses a commit that has no pyproject.toml."""
    repo, commit = make_repo({"README.md": "x\n"}, standard=False)
    with pytest.raises(ar.Rejected) as info:
        ar.check_version(repo, commit, None, git_environment())
    assert "pyproject.toml is not in the commit" in str(info.value)


@pytest.mark.parametrize("version", ["1.2.3-rc.1", "0.31.9", "10.0.0-beta.1.2.3"])
def test_check_version_accepts_a_label_after_the_numbers(
    version: str, make_repo: Callable[..., tuple[Path, str]]
) -> None:
    """check_version accepts a version with a pre-release label after the numbers."""
    repo, commit = make_repo({"pyproject.toml": f"[project]\nversion = '{version}'\n"})
    assert ar.check_version(repo, commit, f"v{version}", git_environment()) == version
