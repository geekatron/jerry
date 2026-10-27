# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Make the release archives from a tagged commit, and check everything on the way.

The ``release`` job of ``.github/workflows/release.yml`` runs this file with
``python3 -I -``: it reads the file from the git object of the commit that triggered the
run, not from the work tree, and hands it to Python on standard input, so nothing in the
work tree can change what runs. That job is the only one that can write to the repository,
to the attestation store and to the release, so this file runs no dependency code. It
needs Python 3.11 or newer and the standard library, nothing else, and it is one file
because isolated mode (``-I``) leaves the folder of the script off ``sys.path`` (a script
read from standard input has no folder at all).

A run goes in this order. Any failure ends it with one line ``REJECTED: <reason>`` and
exit status 1; so does a mistake on the command line (only the help text exits with 0).
The four directories (``--sbom-dir``, ``--output-dir``, ``--repo``, ``--work-dir``, and
the variables ``GITHUB_WORKSPACE`` and ``RUNNER_TEMP`` that stand in for the last two)
must be absolute paths: ``tar`` and ``zip`` run inside the pack directory, so a relative
path would mean one place to the script and another to them.

1. The event is a tag push (a release) or a manual run (a check only).
2. The checkout is the top of a work tree at the commit that triggered the run. The tag,
   when there is one, is ``v<version>``, annotated, made by the version bump bot, and
   points at that commit, and that commit is on the first-parent line of
   ``origin/main``. The version of the tag is the ``[project] version`` of
   ``pyproject.toml`` at that commit.
3. The software bill of materials (SBOM) that the ``build`` job made is exactly one
   regular file, within a size bound, valid JavaScript Object Notation (JSON) with
   the shape of a CycloneDX file.
4. The tree of the commit under the packed paths is read with ``git ls-tree``. Only plain
   files and symbolic links are accepted, and the symbolic links are exactly the two known
   ones, which point nowhere in the archives. Every name is valid UTF-8 (the 8-bit Unicode
   Transformation Format) and in normal form: no empty part, no ``.`` or ``..``, and no
   part that a file system could read as ``.git`` (in any letter case, with trailing
   spaces or dots, with invisible characters, as ``GIT~1``, or with a ``:`` stream
   suffix). No two paths, and no two directories on them, differ only in letter case or in
   the form of a character: a system that ignores those would unpack them to one file.
5. The output directory and the pack directory are created (neither may exist). The pack
   is written from the git objects of the commit, never from the work tree and never
   through a link, and is compared with the commit entry by entry. ``tar`` and ``zip``
   make the archives from the pack, and each archive is read back with the standard
   library and compared with what the tree implies.
6. ``checksums.sha256`` is written from the two archives, the SBOM is copied in, and the
   output directory is checked to hold exactly these four files.

The five guards of the design, and where they are:

1. Before anything is written, the tracked links under the packed paths are exactly the
   two known ones, by name and target, and both dangle in the pack (``check_links``,
   ``check_links_dangle``).
2. No signing-request variable reaches a child process: the script removes them from
   its own environment, and every child gets an environment that is built from a short
   list (``scrub_environment``, ``git_environment``, ``packer_environment``). Nothing is
   copied with ``cp``, and nothing reads through a link.
3. Only plain files and links are accepted, under names that unpack to the same files
   everywhere (``parse_tree``, ``check_tree_shape``).
4. The output directory and the pack directory must not exist, and the archives must not
   exist before the tools run (``make_new_directory``, ``pack_archives``).
5. Any failure stops the run with one ``REJECTED:`` line. The pack is compared with the
   commit, and each archive with the tree, entry by entry (``compare_trees``,
   ``check_archive``).

Everything the script prints passes through ``say`` or ``clean``, so that no line is a
command for the runner (a line that starts with two colons, or that holds ``##[``) and
no control character reaches the log.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import hashlib
import io
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import unicodedata
import zipfile
import zlib
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import IO, NoReturn, cast

# A tree entry as ``git ls-tree`` gives it: mode, object id, path. A member of a tree as
# the checks compare it: kind ("dir", "file" or "link"), mode, and what identifies the
# content (the git blob id of a file, the target of a link, nothing for a directory).
Entry = tuple[bytes, bytes, bytes]
Member = tuple[str, int, bytes]
Tree = dict[bytes, Member]

MIN_PYTHON = (3, 11)

# The identity of the bot that makes release tags (see version-bump.yml).
BOT = "github-actions[bot] <github-actions[bot]@users.noreply.github.com>"

# What the archives hold: these top-level paths of the tagged commit, and nothing else.
PACKED_DIRS = (".claude", ".claude-plugin", "skills", "src", "docs", "scripts", "hooks")
PACKED_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    "GOVERNANCE.md",
    "README.md",
    "pyproject.toml",
    "pytest.ini",
    ".gitignore",
)

# The only symbolic links that the tagged commit may hold under the packed paths. Both
# point into ``.context``, which is not packed, so both dangle in the pack and in the zip.
KNOWN_LINKS = {
    b".claude/patterns": b"../.context/patterns",
    b".claude/rules": b"../.context/rules",
}

SIGNING_VARIABLES = ("ACTIONS_ID_TOKEN_REQUEST_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_URL")
SBOM_NAME = "sbom.cyclonedx.json"
CHECKSUMS_NAME = "checksums.sha256"

# Bounds, in bytes unless said otherwise. The archives are about 5 and 6 megabytes today,
# the SBOM about 130 kilobytes, and the files of an archive add up to about 20 megabytes,
# so each bound leaves room to grow and still stops something that is wildly out of shape.
MAX_ARCHIVE_BYTES = 157_286_400
MAX_SBOM_BYTES = 8_388_608
MAX_CHECKSUMS_BYTES = 4_096
MAX_PACK_BYTES = 268_435_456
MAX_LINK_BYTES = 4_096
MAX_ENTRIES = 50_000
MAX_VERSION_CHARS = 40
TOOL_TIMEOUT_SECONDS = 300.0
LIST_LIMIT = 10
CHUNK_BYTES = 1 << 20

# One version has one spelling: numbers have no leading zero and at most six digits.
_NUMBER = r"(?:0|[1-9][0-9]{0,5})"
VERSION_SHAPE = re.compile(
    rf"{_NUMBER}\.{_NUMBER}\.{_NUMBER}(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+){{0,3}})?"
)
_COMMIT_ID = re.compile(r"[0-9a-f]{40}")
_OBJECT_ID = re.compile(rb"[0-9a-f]{40}")
_TAG_TIME = re.compile(rb"[0-9]{1,12} [+-][0-9]{4}")
_SPEC_VERSION = re.compile(r"1\.[0-9]+")
_PLAIN_ENTRIES = {(b"100644", b"blob"), (b"100755", b"blob"), (b"120000", b"blob")}
_PLAIN_TEXT = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ._/-+=,@~()"
)

# The code points that Unicode lists as Default_Ignorable_Code_Point (DerivedCoreProperties.txt
# of Unicode 15.1.0, with neighbouring ranges joined). A display or a file system may leave
# them out, so a name that holds one can read as another name. The class is built from the
# numbers, so that no invisible character stands in this file.
_IGNORABLE_RANGES = (
    (0x00AD, 0x00AD),
    (0x034F, 0x034F),
    (0x061C, 0x061C),
    (0x115F, 0x1160),
    (0x17B4, 0x17B5),
    (0x180B, 0x180F),
    (0x200B, 0x200F),
    (0x202A, 0x202E),
    (0x2060, 0x206F),
    (0x3164, 0x3164),
    (0xFE00, 0xFE0F),
    (0xFEFF, 0xFEFF),
    (0xFFA0, 0xFFA0),
    (0xFFF0, 0xFFF8),
    (0x1BCA0, 0x1BCA3),
    (0x1D173, 0x1D17A),
    (0xE0000, 0xE0FFF),
)
_IGNORABLE = re.compile(
    "[" + "".join(f"{chr(low)}-{chr(high)}" for low, high in _IGNORABLE_RANGES) + "]"
)


class Rejected(Exception):
    """A check of the release failed. The message is one line of text that is safe to print."""


# ---------------------------------------------------------------------------
# Output that the runner cannot misread
# ---------------------------------------------------------------------------


def clean(value: str | bytes, limit: int = 100) -> str:
    """Return ``value`` as text that is safe to put in a message.

    Every character outside a short plain set (letters, digits, space and ``._/-+=,@~()``)
    becomes ``?``, bytes that are not UTF-8 (the 8-bit Unicode Transformation Format)
    included, and a long value is cut at ``limit`` characters and ends with ``...``.

    Args:
        value: A name, a path or a piece of tool output, from a source that is not trusted.
        limit: The number of characters to keep.

    Returns:
        A single line of plain text in ASCII (the American Standard Code for Information
        Interchange).
    """
    text = value.decode("utf-8", "replace") if isinstance(value, bytes) else value
    shown = "".join(char if char in _PLAIN_TEXT else "?" for char in text[:limit])
    return f"{shown}..." if len(text) > limit else shown


def say(message: str) -> None:
    """Print ``message`` so that the runner cannot read any line of it as a command.

    The runner acts on a line that starts with two colons (after white space) and on the
    older ``##[`` form anywhere in a line. A character that is not printable ASCII
    becomes ``?``, ``##[`` becomes ``##?``, and a leading ``::`` becomes ``?:``.

    Args:
        message: The text to print; a message of several lines prints as several lines.
    """
    for line in message.splitlines() or [""]:
        text = "".join(char if " " <= char <= "~" else "?" for char in line)
        text = text.replace("##[", "##?")
        if text.lstrip().startswith("::"):
            text = text.replace("::", "?:", 1)
        print(text, flush=True)


# ---------------------------------------------------------------------------
# The environment and the child processes (guard 2)
# ---------------------------------------------------------------------------


def require_python(version_info: Sequence[object]) -> None:
    """Refuse a Python that is older than the oldest one the script supports.

    Args:
        version_info: ``sys.version_info`` or a tuple that starts the same way.

    Raises:
        Rejected: The version is older than ``MIN_PYTHON``.
    """
    major, minor, micro = (int(str(part)) for part in version_info[:3])
    if (major, minor) < MIN_PYTHON:
        raise Rejected(
            f"python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required; "
            f"this is {major}.{minor}.{micro}"
        )


def scrub_environment(environ: MutableMapping[str, str]) -> list[str]:
    """Remove the two signing-request variables from ``environ`` and say which were there.

    Args:
        environ: The environment of this process (``os.environ`` removes them for real).

    Returns:
        The names that were removed.
    """
    removed = [name for name in SIGNING_VARIABLES if name in environ]
    for name in removed:
        del environ[name]
    return removed


def git_environment(environ: Mapping[str, str]) -> dict[str, str]:
    """Build the environment of a git process: a few names from ``environ`` and fixed values.

    The locale is fixed so that git prints the same text everywhere, and the objects of the
    commit are read as they are: no replacement refs, no fetch, no prompt.

    Args:
        environ: The environment of this process.

    Returns:
        A new mapping that holds no signing-request variable and no secret.
    """
    env = {
        "LANG": "C",
        "LC_ALL": "C",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
    }
    env.update({name: environ[name] for name in ("PATH", "HOME") if name in environ})
    return env


def packer_environment(environ: Mapping[str, str]) -> dict[str, str]:
    """Build the environment of ``tar`` and ``zip``: the names they need and the locale.

    The locale of the run is passed on, as it was in the job that made the archives
    before, so a name that is not ASCII is stored the way it was. Nothing else comes
    through: no signing-request variable, no token, and none of the variables that change
    how ``tar``, ``zip`` or ``gzip`` behave.

    Args:
        environ: The environment of this process.

    Returns:
        A new mapping.
    """
    keep = ("PATH", "HOME", "TMPDIR", "TZ", "LANG", "LANGUAGE")
    return {
        name: value for name, value in environ.items() if name in keep or name.startswith("LC_")
    }


def run_tool(
    argv: Sequence[str],
    *,
    env: Mapping[str, str],
    what: str,
    cwd: Path | None = None,
    stdin: bytes | None = None,
    timeout: float = 0.0,
) -> bytes:
    """Run a program without a shell and return what it wrote to standard output.

    Args:
        argv: The program and its arguments.
        env: The whole environment of the program. It never inherits one.
        what: The name to use in a message.
        cwd: The folder to run in, if not the current one.
        stdin: Bytes to send to the program, if any.
        timeout: Seconds to wait; zero means ``TOOL_TIMEOUT_SECONDS``.

    Returns:
        The standard output of the program.

    Raises:
        Rejected: The program is not there, did not finish, or ended with a status other
            than zero. The message holds the start of its error output, cleaned.
    """
    limit = timeout if timeout > 0 else TOOL_TIMEOUT_SECONDS
    try:
        done = subprocess.run(
            list(argv),
            env=dict(env),
            cwd=cwd,
            input=stdin,
            stdin=subprocess.DEVNULL if stdin is None else None,
            capture_output=True,
            timeout=limit,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise Rejected(f"{what} did not finish within {limit:g} seconds") from error
    except OSError as error:
        reason = clean(error.strerror or str(error))
        raise Rejected(f"{what} is not installed or cannot be started: {reason}") from error
    if done.returncode != 0:
        detail = clean(done.stderr, 300)
        suffix = f": {detail}" if detail else ""
        raise Rejected(f"{what} failed with exit status {done.returncode}{suffix}")
    return done.stdout


def run_git(repo: Path, env: Mapping[str, str], *args: str) -> bytes:
    """Run ``git -C repo`` with the given arguments and return its standard output."""
    return run_tool(["git", "-C", str(repo), *args], env=env, what="git")


@contextlib.contextmanager
def object_reader(repo: Path, env: Mapping[str, str]) -> Iterator[Callable[[bytes, int], bytes]]:
    """Start ``git cat-file --batch`` and give out a function that reads one blob at a time.

    The function takes an object id (forty lowercase hex digits) and a size limit, sends
    the id to git, waits for the whole answer, and returns the content of the blob. One
    request is in flight at a time, so the two pipes cannot block each other. When the
    block ends, however it ends, git is stopped.

    Args:
        repo: The top of the work tree.
        env: The environment of git.

    Yields:
        ``read(object_id, limit)``, which raises ``Rejected`` for a name that is not an
        object id, an object that is missing or is not a blob, and a blob above the limit.

    Raises:
        Rejected: git cannot be started.
    """
    try:
        process = subprocess.Popen(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=dict(env),
        )
    except OSError as error:
        reason = clean(error.strerror or str(error))
        raise Rejected(f"git is not installed or cannot be started: {reason}") from error
    requests = cast("IO[bytes]", process.stdin)
    answers = cast("IO[bytes]", process.stdout)

    def read(oid: bytes, limit: int) -> bytes:
        if not _OBJECT_ID.fullmatch(oid):
            raise Rejected(f"{clean(oid)} is not an object id")
        requests.write(oid + b"\n")
        requests.flush()
        answer = answers.readline().split()
        if not (
            len(answer) == 3 and answer[0] == oid and answer[1] == b"blob" and answer[2].isdigit()
        ):
            raise Rejected(f"git has no blob {clean(oid)}: it answered {clean(b' '.join(answer))}")
        size = int(answer[2])
        if size > limit:
            raise Rejected(f"the blob {clean(oid)} is larger than {limit} bytes")
        data = answers.read(size)
        if len(data) != size or answers.read(1) != b"\n":
            raise Rejected("git ended its answer early")
        return data

    try:
        yield read
    finally:
        for stream in (requests, answers):
            with contextlib.suppress(OSError):
                stream.close()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


# ---------------------------------------------------------------------------
# The run, the checkout, the tag and the version
# ---------------------------------------------------------------------------


def check_event(environ: Mapping[str, str]) -> bool:
    """Say whether this run is a check only, and refuse a run that is neither kind.

    Args:
        environ: The environment of the run.

    Returns:
        True for a manual run (the attestation and the release are skipped), False for a
        tag push.

    Raises:
        Rejected: The event is neither a push nor a manual run.
    """
    event = environ.get("GITHUB_EVENT_NAME", "")
    if event == "push":
        return False
    if event == "workflow_dispatch":
        return True
    raise Rejected(f'this job runs for a tag push or a manual check, not for "{clean(event)}"')


def check_repository(repo: Path, env: Mapping[str, str]) -> None:
    """Check that ``repo`` is the top of a git work tree.

    Args:
        repo: The checkout directory.
        env: The environment of git.

    Raises:
        Rejected: It is not a work tree, or it is a folder inside one.
    """
    shown = clean(str(repo))
    try:
        prefix = run_git(repo, env, "rev-parse", "--show-prefix").strip()
    except Rejected as error:
        raise Rejected(f"the checkout {shown} is not the top of a work tree ({error})") from error
    if prefix:
        raise Rejected(
            f"the checkout {shown} is not the top of a work tree (it is inside one, at "
            f"{clean(prefix)})"
        )


def check_head(repo: Path, environ: Mapping[str, str], env: Mapping[str, str]) -> str:
    """Check that the checkout is the commit that triggered the run, and return its id.

    The pinned checkout action stops if a tag moved after the run started; this check
    does not rely on that.

    Args:
        repo: The top of the work tree.
        environ: The environment of the run.
        env: The environment of git.

    Returns:
        The commit id, forty lowercase hex digits.

    Raises:
        Rejected: ``GITHUB_SHA`` is not a commit id, or the checkout is another commit.
    """
    triggered = environ.get("GITHUB_SHA", "")
    if not _COMMIT_ID.fullmatch(triggered):
        raise Rejected(f"GITHUB_SHA is not forty lowercase hex digits: {clean(triggered)}")
    head = run_git(repo, env, "rev-parse", "--verify", "HEAD^{commit}").decode("ascii").strip()
    if head != triggered:
        raise Rejected("the checked-out commit is not the commit that triggered this run")
    return head


def resolve_ref(repo: Path, env: Mapping[str, str], ref: str) -> str | None:
    """Return the object id that the ref ``ref`` holds, or None if there is no such ref."""
    listing = run_git(repo, env, "for-each-ref", "--format=%(objectname) %(refname)", ref)
    for line in listing.decode("ascii", "replace").splitlines():
        oid, _, name = line.partition(" ")
        if name == ref:
            return oid
    return None


def check_tag(
    repo: Path, environ: Mapping[str, str], commit: str, env: Mapping[str, str]
) -> str | None:
    """Check the tag of the run and return its name, or None when the run is on a branch.

    What is checked is that the tag looks like what ``version-bump.yml`` makes: the name is
    ``v`` and a version, the object is annotated and has exactly the header lines of a
    release tag, the tagger is the version bump bot, and the message is exactly
    ``Release <tag>``. The tagger line is a text field that anyone who can push a tag can
    write, so this is a check of shape and not authentication. The commit must be on the
    first-parent line of ``origin/main``.

    Args:
        repo: The top of the work tree.
        environ: The environment of the run.
        commit: The commit that triggered the run.
        env: The environment of git.

    Returns:
        The tag name, or None if the ref of the run is not a tag.

    Raises:
        Rejected: Any check fails.
    """
    if environ.get("GITHUB_REF_TYPE") != "tag":
        return None
    ref = environ.get("GITHUB_REF", "")
    if not ref.startswith("refs/tags/"):
        raise Rejected(f"the ref of this run is not a tag ref: {clean(ref)}")
    tag = ref[len("refs/tags/") :]
    version = tag[1:]
    if not (
        tag.startswith("v")
        and len(version) <= MAX_VERSION_CHARS
        and VERSION_SHAPE.fullmatch(version)
    ):
        raise Rejected(
            f"the tag {clean(tag)} is not v<version> with a version of the form X.Y.Z or X.Y.Z-label"
        )
    oid = resolve_ref(repo, env, ref)
    if oid is None:
        raise Rejected(f"the tag is not in this checkout: {tag}")
    if run_git(repo, env, "cat-file", "-t", oid).strip() != b"tag":
        raise Rejected(f"the tag {tag} is not an annotated tag")
    raw = run_git(repo, env, "cat-file", "tag", oid)
    if b"\0" in raw:
        raise Rejected("the tag holds a NUL (zero) byte")
    # The header is exactly: the commit, its type, the tag name, the tagger, an empty line.
    # Tools disagree about which of two tagger lines counts, so an extra line is refused.
    parts = raw.split(b"\n", 5)
    if len(parts) < 6:
        raise Rejected("the header of the tag is incomplete")
    if parts[0] != b"object " + commit.encode("ascii"):
        raise Rejected(
            "the tag does not point at the commit that triggered this run (it was moved)"
        )
    if parts[1] != b"type commit":
        raise Rejected("the tag does not point at a commit")
    if parts[2] != b"tag " + tag.encode("ascii"):
        raise Rejected("the tag object names another tag")
    prefix = b"tagger " + BOT.encode("ascii") + b" "
    if not (parts[3].startswith(prefix) and _TAG_TIME.fullmatch(parts[3][len(prefix) :])):
        raise Rejected(
            f"the tagger of the tag is not the version bump bot ({clean(parts[3], 160)})"
        )
    if parts[4] != b"":
        raise Rejected("the tag has a header that a release tag never has")
    if parts[5] != b"Release " + tag.encode("ascii") + b"\n":
        raise Rejected('the message of the tag is not exactly "Release <tag>"')
    if resolve_ref(repo, env, "refs/remotes/origin/main") is None:
        raise Rejected("origin/main is not in this checkout")
    first_parent = run_git(repo, env, "rev-list", "--first-parent", "refs/remotes/origin/main")
    if commit.encode("ascii") not in set(first_parent.split()):
        raise Rejected("the tagged commit is not on the first-parent line of origin/main")
    return tag


def check_version(repo: Path, commit: str, tag: str | None, env: Mapping[str, str]) -> str:
    """Read the ``[project] version`` of ``pyproject.toml`` at ``commit`` and check it.

    Args:
        repo: The top of the work tree.
        commit: The commit that triggered the run.
        tag: The tag name, or None when the run is on a branch.
        env: The environment of git.

    Returns:
        The version.

    Raises:
        Rejected: The file is missing or is not valid TOML (Tom's Obvious Minimal
            Language), the version is not of the form X.Y.Z or X.Y.Z-label, or the tag
            names another version.
    """
    # Python 3.11 and newer. It is imported here, not at the top, so that an older Python
    # gets as far as ``require_python`` and its one-line refusal.
    import tomllib

    try:
        data = run_git(repo, env, "cat-file", "blob", f"{commit}:pyproject.toml")
    except Rejected as error:
        raise Rejected(f"pyproject.toml is not in the commit ({error})") from error
    if b"\0" in data:
        raise Rejected("pyproject.toml holds a NUL (zero) byte")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Rejected("pyproject.toml is not valid UTF-8") from error
    try:
        document = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise Rejected(f"pyproject.toml is not valid TOML ({clean(str(error))})") from error
    project = document.get("project")
    version = project.get("version") if isinstance(project, dict) else None
    if not isinstance(version, str):
        raise Rejected("pyproject.toml has no [project] version that is a string")
    if len(version) > MAX_VERSION_CHARS or not VERSION_SHAPE.fullmatch(version):
        raise Rejected(
            f"the [project] version of pyproject.toml ({clean(version)}) is not of the form "
            "X.Y.Z or X.Y.Z-label"
        )
    if tag is not None and tag[1:] != version:
        raise Rejected(
            f"the version of the tag ({tag[1:]}) is not the version in pyproject.toml of "
            f"the tagged commit ({version})"
        )
    return version


# ---------------------------------------------------------------------------
# The SBOM
# ---------------------------------------------------------------------------


def checked_size(path: Path, name: str, low: int, high: int) -> int:
    """Check that ``path`` is a regular file (not a link) of ``low`` to ``high`` bytes."""
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode):
        raise Rejected(f"{name} is not a regular file")
    if not low <= info.st_size <= high:
        raise Rejected(
            f"{name} is {info.st_size} bytes, outside the allowed range of {low} to {high} bytes"
        )
    return info.st_size


def read_file(path: Path, limit: int) -> bytes:
    """Read up to ``limit`` + 1 bytes of the file at ``path``, and never through a link."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as handle:
        return handle.read(limit + 1)


def _reject_constant(name: str) -> None:
    """Refuse ``NaN`` and ``Infinity``, which JSON does not have."""
    raise ValueError(f"the constant {name} is not JSON")


def _reject_repeats(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build an object from its pairs, and refuse a key that occurs twice."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"the key {key} occurs twice")
        result[key] = value
    return result


def check_sbom_document(data: bytes) -> None:
    """Check that ``data`` is plain valid JSON with the shape of a CycloneDX file.

    It checks the shape only: ``bomFormat`` is ``CycloneDX``, ``specVersion`` is ``1.N`` and
    ``components`` is a list. What the SBOM says about the dependencies is not checked.

    Args:
        data: The bytes of the file.

    Raises:
        Rejected: The bytes hold a NUL (zero) byte, are not UTF-8, are not valid JSON (a repeated key,
            ``NaN`` and a nesting too deep for the parser are refused too), or have the
            wrong shape.
    """
    if b"\0" in data:
        raise Rejected("the SBOM holds a NUL (zero) byte")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Rejected("the SBOM is not valid UTF-8") from error
    try:
        document = json.loads(
            text, parse_constant=_reject_constant, object_pairs_hook=_reject_repeats
        )
    except (ValueError, RecursionError) as error:
        raise Rejected(f"the SBOM is not valid JSON ({clean(str(error), 120)})") from error
    if not isinstance(document, dict):
        raise Rejected("the SBOM is not a JSON object")
    if document.get("bomFormat") != "CycloneDX":
        raise Rejected('the SBOM has no bomFormat "CycloneDX"')
    spec = document.get("specVersion")
    if not (isinstance(spec, str) and _SPEC_VERSION.fullmatch(spec)):
        raise Rejected("the SBOM has no specVersion of the form 1.N")
    if not isinstance(document.get("components"), list):
        raise Rejected("the SBOM has no components list")


def read_sbom(sbom_dir: Path) -> bytes:
    """Read the SBOM that the ``build`` job made, after checking what can be checked.

    Args:
        sbom_dir: The directory that the download step made.

    Returns:
        The bytes of the SBOM.

    Raises:
        Rejected: The directory is a link, missing, or holds anything but the one file; the
            file is not a regular file within the size bound; or it is not a CycloneDX file.
    """
    shown = clean(str(sbom_dir))
    try:
        info = os.lstat(sbom_dir)
    except FileNotFoundError as error:
        raise Rejected(f"the SBOM directory {shown} does not exist") from error
    if not stat.S_ISDIR(info.st_mode):
        raise Rejected(f"the SBOM directory {shown} is not a directory")
    names = sorted(os.listdir(sbom_dir))
    if names != [SBOM_NAME]:
        raise Rejected(
            f"the SBOM directory must hold exactly the one file {SBOM_NAME}; "
            f"it holds {clean(', '.join(names))}"
        )
    path = sbom_dir / SBOM_NAME
    checked_size(path, SBOM_NAME, 1, MAX_SBOM_BYTES)
    data = read_file(path, MAX_SBOM_BYTES)
    check_sbom_document(data)
    return data


# ---------------------------------------------------------------------------
# The tagged tree (guards 1 and 3)
# ---------------------------------------------------------------------------


def parse_tree(raw: bytes) -> list[Entry]:
    """Read the output of ``git ls-tree -r -z`` and refuse an entry that is not plain.

    Args:
        raw: The bytes that git printed, for each entry: the mode, a space, the type, a space,
            the object id, a tab, the path and a zero byte.

    Returns:
        ``(mode, object id, path)`` for each entry.

    Raises:
        Rejected: The listing cannot be read, or an entry is not a plain file (mode 100644
            or 100755) or a symbolic link (mode 120000), for example a submodule.
    """
    if not raw:
        return []
    if not raw.endswith(b"\0"):
        raise Rejected("the tree listing of git is cut short")
    entries: list[Entry] = []
    for record in raw[:-1].split(b"\0"):
        meta, tab, path = record.partition(b"\t")
        fields = meta.split(b" ")
        if not tab or len(fields) != 3 or not _OBJECT_ID.fullmatch(fields[2]):
            raise Rejected(f"git printed a tree entry that cannot be read: {clean(record)}")
        mode, kind, oid = fields
        if (mode, kind) not in _PLAIN_ENTRIES:
            raise Rejected(
                f"{clean(path)} is not a plain file or a symbolic link "
                f"(mode {clean(mode)}, type {clean(kind)})"
            )
        entries.append((mode, oid, path))
    return entries


def read_tree(repo: Path, commit: str, env: Mapping[str, str]) -> list[Entry]:
    """List every entry of ``commit`` under the packed paths, from the objects of git.

    Args:
        repo: The top of the work tree.
        commit: The commit id.
        env: The environment of git.

    Returns:
        The entries, as ``parse_tree`` returns them.
    """
    raw = run_git(
        repo,
        env,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        commit,
        "--",
        *PACKED_FILES,
        *PACKED_DIRS,
    )
    return parse_tree(raw)


def folded(name: str) -> str:
    """Return ``name`` the way a system that ignores letter case and character form reads it.

    Two names with the same result are one name on such a system (Windows, and the default
    file system of macOS): the letters are folded to one case, and each character is put in
    its decomposed form. The fold is a little wider than any one system's (it joins ``ss``
    and the German sharp s, for one), which only makes the check stricter.

    Args:
        name: A name or a path, as text.

    Returns:
        The folded text.
    """
    return unicodedata.normalize("NFD", unicodedata.normalize("NFD", name).casefold())


def reads_as_git(part: str) -> bool:
    """Say whether a file system could read one name of a path as the ``.git`` directory.

    Windows drops trailing spaces and dots, reads a ``:`` as the start of a stream name, and
    keeps the short name ``GIT~1`` for ``.git``; macOS and many displays leave out the
    default-ignorable code points; letter case does not matter on either.

    Args:
        part: One name of a path, as text.

    Returns:
        True when the name, read that way, is ``.git`` or ``GIT~1``.
    """
    visible = _IGNORABLE.sub("", part).split(":", 1)[0].rstrip(" .")
    return folded(visible) in (".git", "git~1")


def check_no_twins(paths: Iterable[bytes]) -> None:
    """Refuse two paths, or two directories on them, that differ only in case or form.

    Args:
        paths: The paths of the tree, each valid UTF-8.

    Raises:
        Rejected: Two different spellings are the same name once folded.
    """
    seen: dict[str, str] = {}
    for path in sorted(paths):
        parts = path.decode("utf-8").split("/")
        for count in range(1, len(parts) + 1):
            prefix = "/".join(parts[:count])
            first = seen.setdefault(folded(prefix), prefix)
            if first != prefix:
                raise Rejected(
                    f"the paths {clean(first)} and {clean(prefix)} differ only in letter case "
                    "or in the form of a character"
                )


def check_tree_shape(entries: Sequence[Entry]) -> None:
    """Check the paths of the tree before anything is written.

    Every path is valid UTF-8 and in normal form (no empty part, no ``.`` or ``..``, no part
    that a file system could read as ``.git``), holds no control character and no backslash,
    and occurs once. No two paths, and no two directories on them, differ only in letter
    case or in the form of a character. No path is both a file and a directory, every path
    lies under a packed path, and each packed path has something in the commit.

    Args:
        entries: The entries of the tree.

    Raises:
        Rejected: Any of these does not hold, or there are more entries than the bound.
    """
    if len(entries) > MAX_ENTRIES:
        raise Rejected(f"the commit has more than {MAX_ENTRIES} entries under the packed paths")
    paths: set[bytes] = set()
    for _mode, _oid, path in entries:
        shown = clean(path)
        if any(byte < 0x20 or byte == 0x7F for byte in path):
            raise Rejected(f"the path {shown} holds a control character")
        if b"\\" in path:
            raise Rejected(f"the path {shown} holds a backslash")
        try:
            text = path.decode("utf-8")
        except UnicodeDecodeError as error:
            raise Rejected(f"the path {shown} is not valid UTF-8") from error
        if any(part in ("", ".", "..") or reads_as_git(part) for part in text.split("/")):
            raise Rejected(f"the path {shown} is not in normal form")
        if path in paths:
            raise Rejected(f"the path {shown} occurs twice")
        paths.add(path)
    check_no_twins(paths)
    directories: set[bytes] = set()
    for path in paths:
        parts = path.split(b"/")
        directories.update(b"/".join(parts[:count]) for count in range(1, len(parts)))
    packed = {name.encode("utf-8") for name in (*PACKED_FILES, *PACKED_DIRS)}
    for path in sorted(paths):
        if path in directories:
            raise Rejected(f"the path {clean(path)} is both a file and a directory")
        if path.split(b"/", 1)[0] not in packed:
            raise Rejected(f"the path {clean(path)} is outside the packed paths")
    for name in PACKED_FILES:
        if name.encode("utf-8") not in paths:
            raise Rejected(f"the commit has nothing at the packed path {name}")
    for name in PACKED_DIRS:
        if name.encode("utf-8") not in directories:
            raise Rejected(f"the commit has nothing at the packed path {name}")


def read_link_targets(
    entries: Sequence[Entry], read_object: Callable[[bytes, int], bytes]
) -> dict[bytes, bytes]:
    """Read the text of every symbolic link of the tree from its blob.

    Args:
        entries: The entries of the tree.
        read_object: The function that ``object_reader`` gives out.

    Returns:
        The target of each link, by path.
    """
    return {
        path: read_object(oid, MAX_LINK_BYTES) for mode, oid, path in entries if mode == b"120000"
    }


def check_links(entries: Sequence[Entry], targets: Mapping[bytes, bytes]) -> None:
    """Check (guard 1) that the links of the tree are exactly the two known ones.

    Each must be there with its known target, and both must dangle in the pack: nothing
    of the tree may lie at the place that a link points to.

    Args:
        entries: The entries of the tree.
        targets: The target of each link, by path.

    Raises:
        Rejected: A third link, a known link that is missing or points somewhere else, or a
            known link that would resolve inside the pack.
    """
    links = {path for mode, _oid, path in entries if mode == b"120000"}
    for path in sorted(links):
        if path not in KNOWN_LINKS:
            raise Rejected(
                f"{clean(path)} is a symbolic link that is not one of the two known links"
            )
    for path, known in KNOWN_LINKS.items():
        if path not in links:
            raise Rejected(f"a known symbolic link is missing from the commit: {clean(path)}")
        if targets.get(path) != known:
            raise Rejected(
                f"the symbolic link {clean(path)} points somewhere else: "
                f"{clean(targets.get(path, b''))}"
            )
    paths = {path for _mode, _oid, path in entries}
    for path, known in KNOWN_LINKS.items():
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), known))
        if any(other == resolved or other.startswith(resolved + b"/") for other in paths):
            raise Rejected(f"the symbolic link {clean(path)} would resolve inside the pack")


# ---------------------------------------------------------------------------
# The pack (guard 4), and the comparison of the pack with the commit (guard 5)
# ---------------------------------------------------------------------------


def make_new_directory(path: Path, what: str, mode: int = 0o755) -> None:
    """Create a directory that must not exist, and give it exactly ``mode``.

    ``mkdir`` fails if anything is there, a link that points nowhere included, and the mode
    is set afterwards so that the umask of the run does not matter.

    Args:
        path: The directory to create; its parent must exist.
        what: The name to use in a message.
        mode: The permission bits.

    Raises:
        Rejected: Something exists at ``path``, or the directory cannot be created.
    """
    try:
        os.mkdir(path, mode)
    except FileExistsError as error:
        raise Rejected(f"the {what} exists before packing: {clean(str(path))}") from error
    except OSError as error:
        reason = clean(error.strerror or str(error))
        raise Rejected(f"could not create the {what} {clean(str(path))}: {reason}") from error
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fchmod(descriptor, mode)
    finally:
        os.close(descriptor)


def write_new_file(path: Path, data: bytes, mode: int) -> None:
    """Write ``data`` to a file that must not exist, with exactly ``mode``, never through a link.

    Raises:
        Rejected: Something exists at ``path``.
    """
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError as error:
        raise Rejected(f"{clean(str(path))} exists before packing") from error
    with os.fdopen(descriptor, "wb") as handle:
        os.fchmod(handle.fileno(), mode)
        handle.write(data)


def write_pack(
    top_dir: Path,
    entries: Sequence[Entry],
    read_object: Callable[[bytes, int], bytes],
) -> None:
    """Write the tagged tree to ``top_dir`` from the git objects, without ``cp``.

    Every directory and file is created so that creation fails if something is there, each
    file gets its bytes from the blob that git holds and the mode that git records
    (0644 or 0755), each link is made from the text of its blob, and nothing is ever read
    through a link. A directory is made only for an entry that needs it.

    Args:
        top_dir: The top directory of the pack, ``jerry-plugin-<version>``; it must not
            exist and its parent must.
        entries: The entries of the tree.
        read_object: The function that ``object_reader`` gives out.

    Raises:
        Rejected: A path is taken, the content is above ``MAX_PACK_BYTES``, or an object
            cannot be read.
    """
    make_new_directory(top_dir, "pack directory")
    root = os.fsencode(top_dir)
    made = {b""}
    total = 0
    for mode, oid, path in entries:
        parts = path.split(b"/")[:-1]
        for count in range(1, len(parts) + 1):
            prefix = b"/".join(parts[:count])
            if prefix not in made:
                make_new_directory(Path(os.fsdecode(os.path.join(root, prefix))), "directory")
                made.add(prefix)
        target = os.path.join(root, path)
        if mode == b"120000":
            os.symlink(read_object(oid, MAX_LINK_BYTES), target)
            continue
        data = read_object(oid, MAX_PACK_BYTES - total)
        total += len(data)
        if total > MAX_PACK_BYTES:
            raise Rejected(f"the pack would hold more than {MAX_PACK_BYTES} bytes")
        write_new_file(Path(os.fsdecode(target)), data, 0o755 if mode == b"100755" else 0o644)


def expected_tree(entries: Sequence[Entry], targets: Mapping[bytes, bytes]) -> Tree:
    """Describe the pack that the tree implies: the top directory, the parents, the entries.

    Args:
        entries: The entries of the tree.
        targets: The target of each link, by path.

    Returns:
        A member for the top directory (the empty path), for every directory that holds an
        entry, and for every file (its mode, 0644 or 0755, and its blob id) and link.
    """
    tree: Tree = {b"": ("dir", 0o755, b"")}
    for mode, oid, path in entries:
        parts = path.split(b"/")
        for count in range(1, len(parts)):
            tree[b"/".join(parts[:count])] = ("dir", 0o755, b"")
        if mode == b"120000":
            tree[path] = ("link", 0, targets[path])
        else:
            tree[path] = ("file", 0o755 if mode == b"100755" else 0o644, oid)
    return tree


def blob_id_of_stream(handle: IO[bytes], size: int, what: str) -> bytes:
    """Return the git blob id of the ``size`` bytes that ``handle`` yields.

    Raises:
        Rejected: The stream holds more or fewer bytes than ``size``.
    """
    digest = hashlib.sha1(b"blob %d\0" % size, usedforsecurity=False)  # the format of git
    seen = 0
    while chunk := handle.read(CHUNK_BYTES):
        seen += len(chunk)
        if seen > size:
            break
        digest.update(chunk)
    if seen != size:
        raise Rejected(f"{what}: its data is {seen} bytes but its size is {size}")
    return digest.hexdigest().encode("ascii")


def file_blob_id(path: bytes) -> bytes:
    """Return the git blob id of the file at ``path``, which is opened without following a link."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as handle:
        return blob_id_of_stream(handle, os.fstat(handle.fileno()).st_size, clean(path))


def walk_pack(top_dir: Path) -> Tree:
    """Describe what is on disk under ``top_dir``, walking it with ``lstat``.

    Nothing is followed: a link is read with ``readlink`` and not opened, and a directory
    behind a link is not entered.

    Args:
        top_dir: The top directory of the pack.

    Returns:
        The members, in the form that ``expected_tree`` uses.

    Raises:
        Rejected: ``top_dir`` is not a directory, or something under it is not a file, a
            directory or a symbolic link.
    """
    root = os.fsencode(top_dir)
    info = os.lstat(root)
    if not stat.S_ISDIR(info.st_mode):
        raise Rejected(f"the pack directory {clean(root)} is not a directory")
    tree: Tree = {b"": ("dir", stat.S_IMODE(info.st_mode), b"")}
    pending = [b""]
    while pending:
        directory = pending.pop()
        with os.scandir(os.path.join(root, directory) if directory else root) as children:
            for child in children:
                relative = directory + b"/" + child.name if directory else child.name
                found = child.stat(follow_symlinks=False)
                mode = stat.S_IMODE(found.st_mode)
                if stat.S_ISDIR(found.st_mode):
                    tree[relative] = ("dir", mode, b"")
                    pending.append(relative)
                elif stat.S_ISLNK(found.st_mode):
                    tree[relative] = ("link", 0, os.readlink(child.path))
                elif stat.S_ISREG(found.st_mode):
                    tree[relative] = ("file", mode, file_blob_id(child.path))
                else:
                    raise Rejected(
                        f"{clean(relative)} is not a file, a directory or a symbolic link"
                    )
    return tree


def _describe(member: Member) -> str:
    """Describe a member in one short piece of text."""
    kind, mode, identity = member
    return f"{kind} {mode:o} {clean(identity, 14)}"


def compare_trees(
    label: str, expected: Mapping[bytes, Member], actual: Mapping[bytes, Member]
) -> None:
    """Compare two trees entry by entry, and print what differs.

    Args:
        label: What ``actual`` is, for the message ("the pack", "the tar").
        expected: The tree that the commit implies.
        actual: The tree that was found.

    Raises:
        Rejected: They differ. The message counts the missing, extra and different
            entries and names the first; the first ten of each kind are printed.
    """
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    different = sorted(
        path for path in set(expected) & set(actual) if expected[path] != actual[path]
    )
    if not (missing or extra or different):
        return
    for title, paths in (("missing", missing), ("extra", extra), ("different", different)):
        for path in paths[:LIST_LIMIT]:
            detail = ""
            if title == "different":
                detail = f": expected {_describe(expected[path])}, found {_describe(actual[path])}"
            say(f"  {title}: {clean(path)}{detail}")
        if len(paths) > LIST_LIMIT:
            say(f"  ... and {len(paths) - LIST_LIMIT} more {title}")
    first = sorted([*missing, *extra, *different])[0]
    raise Rejected(
        f"{label} is not the tagged tree: {len(missing)} missing, {len(extra)} extra, "
        f"{len(different)} different (the first is {clean(first)})"
    )


def check_links_dangle(top_dir: Path) -> None:
    """Check that neither known link resolves to anything inside the pack.

    Raises:
        Rejected: Something is at the place that a known link points to.
    """
    root = os.fsencode(top_dir)
    for name in sorted(KNOWN_LINKS):
        if os.path.exists(os.path.join(root, name)):
            raise Rejected(f"the link {clean(name)} resolves in the pack; it must point nowhere")


# ---------------------------------------------------------------------------
# The archives, and what they hold (guard 5)
# ---------------------------------------------------------------------------


def archive_names(version: str) -> tuple[str, str, str]:
    """Return the top directory, the tar.gz name and the zip name for ``version``."""
    top = f"jerry-plugin-{version}"
    return top, f"{top}.tar.gz", f"{top}.zip"


def pack_archives(
    pack_root: Path, top: str, tar_path: Path, zip_path: Path, env: Mapping[str, str]
) -> None:
    """Run ``tar`` and then ``zip`` on the pack, from the folder that holds ``top``.

    Args:
        pack_root: The folder that holds the top directory.
        top: The top directory, ``jerry-plugin-<version>``.
        tar_path: Where ``tar`` writes the archive; nothing may exist there.
        zip_path: Where ``zip`` writes the archive; nothing may exist there.
        env: The environment of both tools.

    Raises:
        Rejected: An archive exists before packing, or a tool fails.
    """
    for path in (tar_path, zip_path):
        if os.path.lexists(path):
            raise Rejected(f"the archive {clean(str(path))} exists before packing")
    run_tool(["tar", "-czf", str(tar_path), top], env=env, what="tar", cwd=pack_root)
    run_tool(["zip", "-rq", str(zip_path), top], env=env, what="zip", cwd=pack_root)


def _reduced_mode(mode: int) -> int:
    """Reduce a mode to the one bit that matters for a release: the owner execute bit."""
    return 0o755 if mode & 0o100 else 0o644


def _member_path(name: bytes, top: bytes, *, directory: bool, label: str) -> bytes:
    """Return the path of an archive member relative to ``top``, or refuse the name."""
    raw = name[:-1] if directory and name.endswith(b"/") else name
    if raw == top:
        return b""
    if not raw.startswith(top + b"/"):
        raise Rejected(f"{label} member {clean(name)} is not under the top directory")
    relative = raw[len(top) + 1 :]
    if any(part in (b"", b".", b"..") for part in relative.split(b"/")):
        raise Rejected(f"{label} member {clean(name)} is not in normal form")
    return relative


def tar_members_view(items: Iterable[tuple[tarfile.TarInfo, IO[bytes] | None]], top: str) -> Tree:
    """Describe the members of a tar the way ``expected_tree`` describes a pack.

    Args:
        items: Each member and a stream of its data (None for a member without data).
        top: The top directory, ``jerry-plugin-<version>``.

    Returns:
        The members by path relative to ``top``.

    Raises:
        Rejected: A name is outside ``top`` or not in normal form, a name occurs twice, a
            member is not a file, a directory or a symbolic link, or a file holds more or
            fewer bytes than its size says.
    """
    top_bytes = top.encode("utf-8")
    view: Tree = {}
    for info, handle in items:
        name = info.name.encode("utf-8", "surrogateescape")
        if info.isdir():
            kind = "dir"
        elif info.issym():
            kind = "link"
        elif info.isreg():
            kind = "file"
        else:
            raise Rejected(
                f"tar member {clean(name)} is not a file, a directory or a symbolic link"
            )
        path = _member_path(name, top_bytes, directory=kind == "dir", label="tar")
        if path in view:
            raise Rejected(f"tar member {clean(name)} occurs twice")
        if kind == "dir":
            view[path] = ("dir", _reduced_mode(info.mode), b"")
        elif kind == "link":
            view[path] = ("link", 0, info.linkname.encode("utf-8", "surrogateescape"))
        else:
            blob = blob_id_of_stream(handle or io.BytesIO(b""), info.size, clean(name))
            view[path] = ("file", _reduced_mode(info.mode), blob)
    return view


def zip_members_view(
    items: Iterable[tuple[zipfile.ZipInfo, Callable[[], IO[bytes]]]], top: str
) -> Tree:
    """Describe the members of a zip the way ``expected_tree`` describes a pack.

    The raw bytes of a name are recovered from the name as the header gave it, with the
    encoding that the header's flag says (UTF-8, or the older code page 437), whatever an
    extra field says. A zip that holds a symbolic link is refused: the links dangle in the
    pack and ``zip`` leaves out what it cannot find.

    Args:
        items: Each member and a function that opens its data.
        top: The top directory, ``jerry-plugin-<version>``.

    Returns:
        The members by path relative to ``top``.

    Raises:
        Rejected: As ``tar_members_view``, and a member is a symbolic link.
    """
    top_bytes = top.encode("utf-8")
    view: Tree = {}
    for info, opener in items:
        name = info.orig_filename.encode("utf-8" if info.flag_bits & 0x800 else "cp437")
        unix_mode = (info.external_attr >> 16) & 0xFFFF if info.create_system == 3 else 0
        if stat.S_ISLNK(unix_mode):
            raise Rejected(f"zip member {clean(name)} is a symbolic link; the zip holds none")
        directory = info.is_dir()
        path = _member_path(name, top_bytes, directory=directory, label="zip")
        if path in view:
            raise Rejected(f"zip member {clean(name)} occurs twice")
        if directory:
            view[path] = ("dir", _reduced_mode(unix_mode), b"")
        else:
            with opener() as handle:
                blob = blob_id_of_stream(handle, info.file_size, clean(name))
            view[path] = ("file", _reduced_mode(unix_mode), blob)
    return view


def read_tar(path: Path, top: str) -> Tree:
    """Read a tar.gz with the standard library and describe its members.

    Raises:
        Rejected: The file is not a readable tar.gz, or ``tar_members_view`` refuses a member.
    """
    try:
        with tarfile.open(path, "r:gz") as archive:
            members = ((m, archive.extractfile(m) if m.isreg() else None) for m in archive)
            return tar_members_view(members, top)
    except (tarfile.TarError, OSError, EOFError, zlib.error) as error:
        raise Rejected(f"the tar cannot be read: {clean(str(error))}") from error


def read_zip(path: Path, top: str) -> Tree:
    """Read a zip with the standard library and describe its members.

    Raises:
        Rejected: The file is not a readable zip, or ``zip_members_view`` refuses a member.
    """
    try:
        with zipfile.ZipFile(path) as archive:
            members = [(info, functools.partial(archive.open, info)) for info in archive.infolist()]
            return zip_members_view(members, top)
    except (zipfile.BadZipFile, OSError, EOFError, zlib.error) as error:
        raise Rejected(f"the zip cannot be read: {clean(str(error))}") from error


def archive_view(expected: Mapping[bytes, Member], *, links: bool) -> Tree:
    """Return the members that an archive of the pack must hold.

    A tar holds files, directories and links. A zip holds no link: both known links dangle
    in the pack, and ``zip`` leaves out what it cannot find.

    Args:
        expected: The tree that the commit implies.
        links: True for a tar, False for a zip.
    """
    return {path: member for path, member in expected.items() if links or member[0] != "link"}


def check_archive(
    label: str, expected: Mapping[bytes, Member], actual: Mapping[bytes, Member]
) -> None:
    """Check an archive against what the tree implies: first the count, then every member.

    Raises:
        Rejected: The count differs, or any member does.
    """
    if len(actual) != len(expected):
        raise Rejected(
            f"{label} lists {len(actual)} members, but the tagged tree implies {len(expected)}"
        )
    compare_trees(label, expected, actual)


# ---------------------------------------------------------------------------
# Checksums and the output directory
# ---------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    """Return the SHA-256 (Secure Hash Algorithm, 256 bits) digest of a file as lowercase hex."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while chunk := handle.read(CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums(output_dir: Path, names: Sequence[str]) -> str:
    """Write ``checksums.sha256`` for the files ``names`` in the form that ``sha256sum`` uses.

    Args:
        output_dir: The directory that holds the files.
        names: The file names, in the order of the lines.

    Returns:
        The text that was written: one ``<digest>  <name>`` line per file.

    Raises:
        Rejected: ``checksums.sha256`` exists already.
    """
    text = "".join(f"{sha256_file(output_dir / name)}  {name}\n" for name in names)
    write_new_file(output_dir / CHECKSUMS_NAME, text.encode("ascii"), 0o644)
    return text


def check_output_directory(output_dir: Path, tar_name: str, zip_name: str) -> None:
    """Check what the later steps will attest and publish: exactly the four files, read from disk.

    The four are regular files (no link) within their size bounds, ``checksums.sha256`` is
    the two lines of the two archives, and the SBOM is still a CycloneDX file.

    Args:
        output_dir: The output directory.
        tar_name: The name of the tar.gz.
        zip_name: The name of the zip.

    Raises:
        Rejected: Any of these does not hold.
    """
    info = os.lstat(output_dir)
    if not stat.S_ISDIR(info.st_mode):
        raise Rejected(f"the output directory {clean(str(output_dir))} is not a directory")
    wanted = sorted([tar_name, zip_name, CHECKSUMS_NAME, SBOM_NAME])
    found = sorted(os.listdir(output_dir))
    if found != wanted:
        raise Rejected(
            f"the output directory must hold exactly {', '.join(wanted)}; "
            f"it holds {clean(', '.join(found))}"
        )
    bounds = {
        tar_name: MAX_ARCHIVE_BYTES,
        zip_name: MAX_ARCHIVE_BYTES,
        CHECKSUMS_NAME: MAX_CHECKSUMS_BYTES,
        SBOM_NAME: MAX_SBOM_BYTES,
    }
    for name, high in bounds.items():
        checked_size(output_dir / name, name, 1, high)
    expected = "".join(
        f"{sha256_file(output_dir / name)}  {name}\n" for name in (tar_name, zip_name)
    )
    if read_file(output_dir / CHECKSUMS_NAME, MAX_CHECKSUMS_BYTES) != expected.encode("ascii"):
        raise Rejected(
            f"{CHECKSUMS_NAME} is not the two lines that sha256sum writes for the two archives"
        )
    check_sbom_document(read_file(output_dir / SBOM_NAME, MAX_SBOM_BYTES))


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


class _CommandLine(argparse.ArgumentParser):
    """An argument parser that reports a mistake as ``Rejected`` instead of exiting with 2."""

    def error(self, message: str) -> NoReturn:
        """Raise ``Rejected`` with the parser's message; print no usage text and do not exit."""
        raise Rejected(f"command line: {clean(message, 300)}")


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line; ``argv`` None means ``sys.argv``.

    Args:
        argv: The command line without the program name.

    Returns:
        The options. The help option prints the help text and exits with status 0, as usual.

    Raises:
        Rejected: The command line is wrong: a missing option or value, or one that is unknown.
    """
    parser = _CommandLine(
        prog="assemble_release.py",
        description=(
            "Check the tagged commit, make the release archives from its git objects, "
            "and check the archives. The four directories must be absolute paths."
        ),
        allow_abbrev=False,
    )
    parser.add_argument(
        "--sbom-dir",
        required=True,
        help="the directory that holds the downloaded SBOM (an absolute path)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="the directory to create for the four release files; it must not exist "
        "(an absolute path)",
    )
    parser.add_argument("--repo", help="the checkout, an absolute path (default: GITHUB_WORKSPACE)")
    parser.add_argument(
        "--work-dir", help="the directory for the pack, an absolute path (default: RUNNER_TEMP)"
    )
    return parser.parse_args(None if argv is None else list(argv))


def require_absolute(value: str, name: str) -> Path:
    """Return ``value`` as a path, or refuse it if it is not an absolute path.

    ``tar`` and ``zip`` run inside the pack directory, so a relative path would mean one place
    to the script and another to them.

    Args:
        value: The path as it was given.
        name: The option or the variable that it came from, for the message.

    Returns:
        The path.

    Raises:
        Rejected: The path is not absolute.
    """
    path = Path(value)
    if not path.is_absolute():
        raise Rejected(f"{name} must be an absolute path: {clean(value)}")
    return path


def directory_from(
    option: str | None, environ: Mapping[str, str], variable: str, flag: str, what: str
) -> Path:
    """Return the directory from its option, or from its variable of the run (absolute)."""
    value = option or environ.get(variable)
    if not value:
        raise Rejected(f"no {what} directory: pass {flag} or set {variable}")
    return require_absolute(value, flag if option else variable)


def append_text(environ: Mapping[str, str], variable: str, text: str, what: str) -> None:
    """Append ``text`` to the file that ``variable`` names, if it is set (the runner's files)."""
    path = environ.get(variable)
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(text)
    except OSError as error:
        reason = clean(error.strerror or str(error))
        raise Rejected(f"could not write the {what}: {reason}") from error


def write_from_objects(
    repo: Path,
    env: Mapping[str, str],
    entries: Sequence[Entry],
    output_dir: Path,
    work_root: Path,
    top: str,
) -> tuple[Path, Path, dict[bytes, bytes]]:
    """Check the links, then create the directories and write the pack from the git objects.

    Everything before the directories are made only reads. From there on the script writes,
    into directories that it creates and that did not exist.

    Args:
        repo: The top of the work tree.
        env: The environment of git.
        entries: The entries of the tree, already checked for their shape.
        output_dir: The output directory to create.
        work_root: The directory that holds the work directory of this run.
        top: The top directory of the pack, ``jerry-plugin-<version>``.

    Returns:
        The folder that holds the top directory, the top directory, and the link targets.
    """
    with object_reader(repo, env) as read_object:
        targets = read_link_targets(entries, read_object)
        check_links(entries, targets)
        make_new_directory(output_dir, "output directory")
        pack_root = Path(tempfile.mkdtemp(prefix="release-pack-", dir=work_root)) / "pack"
        make_new_directory(pack_root, "pack directory")
        top_dir = pack_root / top
        write_pack(top_dir, entries, read_object)
        return pack_root, top_dir, targets


def assemble(
    args: argparse.Namespace, environ: MutableMapping[str, str], removed: Sequence[str]
) -> None:
    """Do the whole run described at the top of this file; raise ``Rejected`` on any failure."""
    repo = directory_from(args.repo, environ, "GITHUB_WORKSPACE", "--repo", "checkout")
    work_root = directory_from(args.work_dir, environ, "RUNNER_TEMP", "--work-dir", "work")
    sbom_dir = require_absolute(args.sbom_dir, "--sbom-dir")
    output_dir = require_absolute(args.output_dir, "--output-dir")
    check_only = check_event(environ)
    if check_only:
        say("Check only: the attestation and the release are skipped.")
    if removed:
        say(
            "Removed from the environment of this script and of the tools it starts: "
            + ", ".join(removed)
        )
    env = git_environment(environ)
    check_repository(repo, env)
    commit = check_head(repo, environ, env)
    tag = check_tag(repo, environ, commit, env)
    if tag is None:
        if not check_only:
            raise Rejected(
                "a release is made from a tag push; this run is on "
                + clean(environ.get("GITHUB_REF", ""))
            )
        say(
            "No tag on this ref: the tag checks are skipped; the version of pyproject.toml "
            "stands in for it."
        )
    version = check_version(repo, commit, tag, env)
    top, tar_name, zip_name = archive_names(version)
    say(f"Version {version}, commit {commit}")

    sbom = read_sbom(sbom_dir)
    entries = read_tree(repo, commit, env)
    check_tree_shape(entries)
    pack_root, top_dir, targets = write_from_objects(repo, env, entries, output_dir, work_root, top)
    check_links_dangle(top_dir)
    expected = expected_tree(entries, targets)
    compare_trees("the pack", expected, walk_pack(top_dir))
    tar_path = output_dir / tar_name
    zip_path = output_dir / zip_name
    pack_archives(pack_root, top, tar_path, zip_path, packer_environment(environ))
    check_archive("the tar", archive_view(expected, links=True), read_tar(tar_path, top))
    check_archive("the zip", archive_view(expected, links=False), read_zip(zip_path, top))
    checksums = write_checksums(output_dir, [tar_name, zip_name])
    write_new_file(output_dir / SBOM_NAME, sbom, 0o644)
    check_output_directory(output_dir, tar_name, zip_name)

    digests = [line.split("  ")[0] for line in checksums.splitlines()]
    summary = [
        "## Release check (no attestation, no release)" if check_only else "## Release assembled",
        f"- **Version:** {version}",
        f"- **Commit:** {commit}",
        f"- **Tag:** {tag or 'none (manual check on a branch)'}",
        "- **Archives:** made here from the git objects of the tagged commit, read back and "
        "compared with it, entry by entry",
        f"- **sha256 {tar_name}:** {digests[0]}",
        f"- **sha256 {zip_name}:** {digests[1]}",
    ]
    append_text(environ, "GITHUB_OUTPUT", f"version={version}\ncommit={commit}\n", "step outputs")
    append_text(environ, "GITHUB_STEP_SUMMARY", "\n".join(summary) + "\n", "step summary")
    say(f"Checked: tag {tag or 'none'}, commit {commit}, version {version}")
    say(f"Files: {tar_name}, {zip_name}, {CHECKSUMS_NAME}, {SBOM_NAME}")
    if check_only:
        prerelease = " --prerelease" if "-" in version else ""
        say(
            "Check only: the release would be created with: "
            f'gh release create v{version} --verify-tag --title "Jerry Framework v{version}" '
            f"--notes-file <notes>{prerelease} <the four files>"
        )


def main(argv: Sequence[str] | None = None, environ: MutableMapping[str, str] | None = None) -> int:
    """Run the script. Return 0 on success; on any failure print one ``REJECTED:`` line, return 1.

    Args:
        argv: The command line without the program name; None means ``sys.argv``.
        environ: The environment of the run; None means ``os.environ``, which is changed:
            the signing-request variables are removed from it first.

    Returns:
        The exit status.
    """
    environment = os.environ if environ is None else environ
    removed = scrub_environment(environment)
    try:
        require_python(sys.version_info)
        assemble(parse_args(argv), environment, removed)
    except Rejected as error:
        say(f"REJECTED: {error}")
        return 1
    except Exception as error:  # a line of text for the log, not a traceback
        say(f"REJECTED: unexpected {type(error).__name__}: {clean(str(error), 200)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
