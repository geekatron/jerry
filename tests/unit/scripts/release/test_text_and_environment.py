# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the text cleaning and the environment handling of the release script.

Guard 2 of the script (no signing-request variable reaches a child process) is
pinned here at the level of the helper functions; ``test_main.py`` pins it for
every child process of a whole run.

Every printed line has to be inert: no line may start with ``::`` (after white
space) or contain ``##[``, because the runner reads those as commands, and no
control character may reach the log.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    CHILD_GIT_NAMES,
    CHILD_PACKER_NAMES,
    HOSTILE_NAMES,
    packer_name_is_allowed,
)

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

# Characters that matter to the runner or to a terminal, mixed with plain ones.
POOL = [
    ":",
    ":",
    "#",
    "[",
    "]",
    " ",
    " ",
    "\n",
    "\r",
    "\t",
    "\x1b",
    "\x00",
    "\x7f",
    "\x85",
    " ",
    "\u202e",
    "é",
    "–",
    "a",
    "b",
    "-",
    ".",
    "/",
]

HOSTILE_TEXTS = [
    "::error::boom",
    "   ::set-env name=X::y",
    "plain ##[add-mask]secret",
    "carriage\rreturn ::error::x",
    "escape \x1b[31mred\x1b[0m",
    "nul\x00byte",
    "new\nline\n::stop-commands::abc",
    "tab\tseparated",
    "delete\x7fchar",
    "unicode – dash and \u202e override",
    "",
]


# --- clean -----------------------------------------------------------------


def test_clean_keeps_a_plain_character_set_when_the_text_is_ordinary() -> None:
    """clean leaves a plain path made of ordinary characters unchanged."""
    assert ar.clean("jerry-plugin-1.2.3/skills/a_b.md") == "jerry-plugin-1.2.3/skills/a_b.md"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("::error::x", "??error??x"),
        ("a##[b]", "a???b?"),
        ("line\nbreak", "line?break"),
        ("cr\rx", "cr?x"),
        ("esc\x1bx", "esc?x"),
        ("nul\x00x", "nul?x"),
        ("dash – here", "dash ? here"),
    ],
)
def test_clean_replaces_every_character_outside_the_plain_set_with_a_question_mark(
    raw: str, expected: str
) -> None:
    """clean turns each character outside the plain set into a question mark."""
    assert ar.clean(raw) == expected


def test_clean_decodes_bytes_and_replaces_bytes_that_are_not_text() -> None:
    """clean decodes bytes; a non-plain character and each invalid byte become a question mark."""
    assert ar.clean(b"docs/\xe2\x80\x93.md") == "docs/?.md"
    assert ar.clean(b"bad \xff\xfe bytes") == "bad ?? bytes"


def test_clean_cuts_a_long_value_and_marks_the_cut() -> None:
    """clean shortens an over-long value and ends it with three dots."""
    cleaned = ar.clean("a" * 500, limit=40)
    assert cleaned == "a" * 40 + "..."


def test_clean_returns_an_empty_string_for_an_empty_value() -> None:
    """clean returns an empty string for empty input."""
    assert ar.clean("") == ""
    assert ar.clean(b"") == ""


# --- say -------------------------------------------------------------------


@pytest.mark.parametrize("text", HOSTILE_TEXTS)
def test_say_never_prints_a_line_the_runner_could_read_as_a_command(
    text: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """say never prints a line that starts as a workflow command (::)."""
    ar.say(text)
    out = capsys.readouterr().out
    for line in out.splitlines():
        assert not line.lstrip().startswith("::"), line
        assert "##[" not in line, line
        assert all(ord(c) >= 0x20 and ord(c) != 0x7F for c in line), repr(line)


def test_say_and_clean_are_inert_for_two_thousand_random_strings(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """For 2,000 random strings, say and clean produce no newline and no command line."""
    rng = random.Random(20261103)
    for _ in range(2000):
        text = "".join(rng.choice(POOL) for _ in range(rng.randint(0, 40)))
        ar.say(text)
        ar.say(f"REJECTED: {ar.clean(text)}")
        printed = capsys.readouterr().out
        for line in printed.splitlines():
            assert not line.lstrip().startswith("::"), repr(text)
            assert "##[" not in line, repr(text)
            assert all(" " <= char <= "~" for char in line), repr(text)
        assert "\n" not in ar.clean(text)
        assert all(" " <= char <= "~" for char in ar.clean(text))


def test_say_prints_an_ordinary_message_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    """say prints an ordinary message as it is."""
    ar.say('Checked: tag v1.2.3, commit abc, version 1.2.3 (all "fine")')
    assert (
        capsys.readouterr().out == 'Checked: tag v1.2.3, commit abc, version 1.2.3 (all "fine")\n'
    )


def test_say_breaks_a_multi_line_message_into_separate_safe_lines(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """say prints a multi-line message as separate lines, each made safe."""
    ar.say("first\n::error::second")
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 2
    assert lines[0] == "first"
    assert not lines[1].startswith("::")


# --- scrub_environment ------------------------------------------------------


def test_scrub_environment_removes_both_signing_request_variables() -> None:
    """scrub_environment removes both ACTIONS_ID_TOKEN_REQUEST variables and names them."""
    environ = {
        "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "t",
        "ACTIONS_ID_TOKEN_REQUEST_URL": "u",
        "PATH": "/usr/bin",
    }
    removed = ar.scrub_environment(environ)
    assert sorted(removed) == ["ACTIONS_ID_TOKEN_REQUEST_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_URL"]
    assert environ == {"PATH": "/usr/bin"}


def test_scrub_environment_does_nothing_when_the_variables_are_absent() -> None:
    """scrub_environment removes nothing when neither signing variable is set."""
    environ = {"PATH": "/usr/bin"}
    assert ar.scrub_environment(environ) == []
    assert environ == {"PATH": "/usr/bin"}


# --- child environments -------------------------------------------------------

PARENT = {
    "PATH": "/usr/bin:/bin",
    "HOME": "/home/runner",
    "TMPDIR": "/tmp/x",
    "TZ": "UTC",
    "LANG": "C.UTF-8",
    "LANGUAGE": "en",
    "LC_CTYPE": "C.UTF-8",
    "LC_ALL": "en_US.UTF-8",
    "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "secret",
    "ACTIONS_ID_TOKEN_REQUEST_URL": "https://example.invalid",
    "ACTIONS_RUNTIME_TOKEN": "secret2",
    "GITHUB_TOKEN": "secret3",
    "GIT_DIR": "/elsewhere/.git",
    "GIT_INDEX_FILE": "/elsewhere/index",
    "GIT_WORK_TREE": "/elsewhere",
    "GZIP": "-9",
    "PYTHONPATH": "/planted",
}


@pytest.mark.parametrize("make", ["git_environment", "packer_environment"])
def test_child_environments_carry_no_signing_request_variable_and_no_other_secret(
    make: str,
) -> None:
    """No child environment carries a signing-request variable or any other secret."""
    env = getattr(ar, make)(PARENT)
    for name in (
        "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
        "ACTIONS_ID_TOKEN_REQUEST_URL",
        "ACTIONS_RUNTIME_TOKEN",
        "GITHUB_TOKEN",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_WORK_TREE",
        "GZIP",
        "PYTHONPATH",
    ):
        assert name not in env


def test_git_environment_fixes_the_locale_and_keeps_only_what_git_needs() -> None:
    """git_environment fixes the locale and git's own settings, takes PATH and HOME from the parent, and keeps nothing else."""
    env = ar.git_environment(PARENT)
    assert env["PATH"] == "/usr/bin:/bin"
    assert env["HOME"] == "/home/runner"
    assert env["LC_ALL"] == "C"
    assert env["LANG"] == "C"
    assert "LC_CTYPE" not in env
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    # The objects of the commit are read as they are: no replacement refs, no fetch.
    assert env["GIT_NO_REPLACE_OBJECTS"] == "1"
    assert env["GIT_NO_LAZY_FETCH"] == "1"


def test_packer_environment_keeps_the_locale_of_the_run_as_the_old_build_job_did() -> None:
    """packer_environment passes the run's locale on, as the old build job did."""
    env = ar.packer_environment(PARENT)
    assert env["LANG"] == "C.UTF-8"
    assert env["LC_CTYPE"] == "C.UTF-8"
    assert env["LC_ALL"] == "en_US.UTF-8"
    assert env["TZ"] == "UTC"
    assert env["PATH"] == "/usr/bin:/bin"


def test_packer_environment_does_not_invent_a_locale_when_the_run_has_none() -> None:
    """packer_environment adds no locale variable that the run does not have."""
    env = ar.packer_environment({"PATH": "/usr/bin"})
    assert "LC_ALL" not in env
    assert "LANG" not in env


# --- the allowlist itself: only these names reach a child (guard 2) ---------------------------


def hostile_parent() -> dict[str, str]:
    """Build a parent environment that holds every hostile name and many other names."""
    parent: dict[str, str] = dict.fromkeys(HOSTILE_NAMES, "x")
    parent.update({f"OTHER_NAME_{number}": "x" for number in range(200)})
    parent.update(
        {
            "PATH": "/usr/bin:/bin",
            "HOME": "/home/runner",
            "TMPDIR": "/tmp/run",
            "TZ": "UTC",
            "LANG": "en_US.UTF-8",
            "LANGUAGE": "en",
            "LC_ALL": "en_US.UTF-8",
            "LC_CTYPE": "en_US.UTF-8",
            "LC_MESSAGES": "en_US.UTF-8",
            "lc_all": "x",
            "path": "x",
            "xLC_ALL": "x",
            "LC": "x",
            "": "x",
        }
    )
    return parent


@pytest.mark.parametrize("name", HOSTILE_NAMES)
@pytest.mark.parametrize("make", ["git_environment", "packer_environment"])
def test_no_hostile_name_reaches_a_child_even_when_it_is_the_only_extra_name(
    make: str, name: str
) -> None:
    """A hostile variable never reaches a child, even when it is the only extra one."""
    env = getattr(ar, make)({"PATH": "/usr/bin", "HOME": "/home/runner", name: "x"})
    assert name not in env


def test_the_hostile_names_are_all_outside_what_any_child_may_have() -> None:
    """None of the hostile variable names is on a child's allowed list."""
    # A guard on the test itself: no hostile name may also be an allowed name.
    assert not set(HOSTILE_NAMES) & CHILD_GIT_NAMES
    assert not set(HOSTILE_NAMES) & CHILD_PACKER_NAMES
    assert not any(name.startswith("LC_") for name in HOSTILE_NAMES)


def test_git_environment_holds_only_the_allowed_names_whatever_the_parent_holds() -> None:
    """git_environment holds only allowed names, whatever the parent environment holds."""
    env = ar.git_environment(hostile_parent())
    assert set(env) <= CHILD_GIT_NAMES, sorted(set(env) - CHILD_GIT_NAMES)
    # and it is not empty: the fixed names are always there, PATH and HOME come from the parent
    assert set(env) == CHILD_GIT_NAMES


def test_git_environment_takes_only_path_and_home_from_the_parent() -> None:
    """git_environment copies only PATH and HOME from the parent; its other values are fixed."""
    env = ar.git_environment({"LANGUAGE": "en", "TZ": "UTC", "TMPDIR": "/t", "LC_CTYPE": "x"})
    assert set(env) == CHILD_GIT_NAMES - {"PATH", "HOME"}


def test_packer_environment_holds_only_the_allowed_names_and_every_one_the_run_has() -> None:
    """packer_environment holds only allowed names, and every allowed name the run has."""
    parent = hostile_parent()
    env = ar.packer_environment(parent)
    expected = {name for name in parent if packer_name_is_allowed(name)}
    assert set(env) <= expected, sorted(set(env) - expected)
    assert set(env) == expected, sorted(expected - set(env))
    assert all(env[name] == parent[name] for name in env)


def test_the_expected_names_of_a_packer_are_the_fixed_ones_and_the_locale_variables() -> None:
    """A packer's names are the fixed ones plus the run's locale variables."""
    env = ar.packer_environment(hostile_parent())
    assert set(env) == CHILD_PACKER_NAMES | {"LC_ALL", "LC_CTYPE", "LC_MESSAGES"}
