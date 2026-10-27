# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for reading the tagged tree and for guards 1 and 3.

Guard 1: before anything is written, the tracked links under the copied paths
must be exactly the two known ones, by name and target, and both must dangle in
the pack. Guard 3: a tree entry that is not a plain file or a symbolic link is
refused.
"""

from __future__ import annotations

import hashlib
import os
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import STANDARD_FILES, assert_inert_output  # noqa: E402

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

KNOWN = {
    b".claude/patterns": b"../.context/patterns",
    b".claude/rules": b"../.context/rules",
}


def oid_of(path: bytes) -> bytes:
    """Make a stable fake object id for a path."""
    return hashlib.sha1(path).hexdigest().encode()


def entry(path: str | bytes, mode: bytes = b"100644") -> tuple[bytes, bytes, bytes]:
    """Make a tree entry as ``parse_tree`` returns it."""
    raw = path.encode() if isinstance(path, str) else path
    return (mode, oid_of(raw), raw)


def standard_entries() -> list[tuple[bytes, bytes, bytes]]:
    """Return the packed entries of the standard repository, with its two links."""
    top_level = set(ar.PACKED_FILES) | set(ar.PACKED_DIRS)
    entries = [entry(name) for name in STANDARD_FILES if name.split("/")[0] in top_level]
    entries.append(entry(".claude/patterns", b"120000"))
    entries.append(entry(".claude/rules", b"120000"))
    return sorted(entries, key=lambda item: item[2])


def raw_line(mode: bytes, kind: bytes, oid: bytes, path: bytes) -> bytes:
    """Format one entry as ``git ls-tree -r -z`` prints it."""
    return mode + b" " + kind + b" " + oid + b"\t" + path + b"\0"


# --- parse_tree: reading what git prints, and guard 3 ----------------------------


def test_parse_tree_reads_mode_object_id_and_path() -> None:
    """parse_tree splits each listing entry into its mode, object id and path."""
    oid = b"a" * 40
    raw = raw_line(b"100644", b"blob", oid, b"CLAUDE.md") + raw_line(
        b"120000", b"blob", oid, b".claude/rules"
    )
    assert ar.parse_tree(raw) == [
        (b"100644", oid, b"CLAUDE.md"),
        (b"120000", oid, b".claude/rules"),
    ]


def test_parse_tree_returns_nothing_for_an_empty_listing() -> None:
    """parse_tree returns an empty list for an empty listing."""
    assert ar.parse_tree(b"") == []


def test_parse_tree_keeps_a_tab_and_a_newline_inside_a_path() -> None:
    """parse_tree keeps a tab and a newline that are part of a path."""
    oid = b"b" * 40
    raw = raw_line(b"100644", b"blob", oid, b"docs/a\tb\nc.md")
    assert ar.parse_tree(raw) == [(b"100644", oid, b"docs/a\tb\nc.md")]


@pytest.mark.parametrize("mode", [b"100644", b"100755", b"120000"])
def test_parse_tree_accepts_exactly_the_three_modes_of_plain_files_and_links(mode: bytes) -> None:
    """parse_tree accepts the modes of a plain file, an executable file and a link."""
    assert ar.parse_tree(raw_line(mode, b"blob", b"c" * 40, b"x"))[0][0] == mode


@pytest.mark.parametrize(
    ("mode", "kind"),
    [
        (b"160000", b"commit"),  # a submodule
        (b"040000", b"tree"),
        (b"100664", b"blob"),
        (b"100600", b"blob"),
        (b"100644", b"commit"),
        (b"120000", b"tree"),
        (b"000000", b"blob"),
    ],
)
def test_parse_tree_refuses_an_entry_that_is_not_a_plain_file_or_a_symbolic_link(
    mode: bytes, kind: bytes
) -> None:
    """parse_tree refuses an entry that is neither a plain file nor a link, such as a submodule."""
    with pytest.raises(ar.Rejected) as info:
        ar.parse_tree(raw_line(mode, kind, b"d" * 40, b"hooks/vendored"))
    assert "not a plain file or a symbolic link" in str(info.value)
    assert "hooks/vendored" in str(info.value)


@pytest.mark.parametrize(
    "raw",
    [
        b"100644 blob " + b"a" * 40 + b"\tCLAUDE.md",  # no NUL at the end
        b"100644 blob " + b"a" * 40 + b" CLAUDE.md\0",  # no tab
        b"100644 blob\tCLAUDE.md\0",  # a field is missing
        b"100644 blob " + b"a" * 39 + b"\tCLAUDE.md\0",  # object id too short
        b"100644 blob " + b"A" * 40 + b"\tCLAUDE.md\0",  # not lowercase hex
        b"100644 blob " + b"a" * 40 + b" extra\tCLAUDE.md\0",  # four fields
    ],
)
def test_parse_tree_refuses_a_listing_that_cannot_be_read(raw: bytes) -> None:
    """parse_tree refuses a listing that does not have the expected format."""
    with pytest.raises(ar.Rejected):
        ar.parse_tree(raw)


def test_parse_tree_message_is_inert_for_a_hostile_path() -> None:
    """parse_tree refuses a hostile path and reports it in cleaned form."""
    raw = raw_line(b"160000", b"commit", b"e" * 40, b"hooks/\n::error::pwned\n##[add-mask]x")
    with pytest.raises(ar.Rejected) as info:
        ar.parse_tree(raw)
    assert_inert_output(str(info.value))


# --- read_tree: real git ----------------------------------------------------------


def test_read_tree_lists_only_the_packed_paths_and_marks_modes(
    standard_repo: tuple[Path, str],
) -> None:
    """read_tree lists only entries under the packed paths, each with its mode."""
    repo, commit = standard_repo
    entries = ar.read_tree(repo, commit, ar.git_environment({"PATH": os.environ["PATH"]}))
    paths = {path for _, _, path in entries}
    assert b".context/rules/rule.md" not in paths
    assert b"CHANGELOG.md" not in paths
    assert b"uv.lock" not in paths
    assert b"README.md" in paths
    modes = {path: mode for mode, _, path in entries}
    assert modes[b"scripts/tool.py"] == b"100755"
    assert modes[b".claude/rules"] == b"120000"
    assert modes[b".claude/patterns"] == b"120000"
    assert modes[b"docs/guide.md"] == b"100644"
    expected = [
        name
        for name in STANDARD_FILES
        if name.split("/")[0] in set(ar.PACKED_FILES) | set(ar.PACKED_DIRS)
    ]
    assert len(entries) == len(expected) + 2


def test_read_tree_refuses_a_submodule_entry_under_a_packed_path(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """read_tree refuses a submodule (a commit entry) inside a packed folder."""
    repo, commit = make_repo(gitlinks={"hooks/vendored": "a" * 40})
    with pytest.raises(ar.Rejected) as info:
        ar.read_tree(repo, commit, ar.git_environment({"PATH": os.environ["PATH"]}))
    assert "not a plain file or a symbolic link" in str(info.value)
    assert "hooks/vendored" in str(info.value)


def test_read_tree_ignores_a_submodule_entry_outside_the_packed_paths(
    make_repo: Callable[..., tuple[Path, str]],
) -> None:
    """A submodule outside the packed folders does not stop read_tree."""
    repo, commit = make_repo(gitlinks={"tests/vendored": "a" * 40})
    entries = ar.read_tree(repo, commit, ar.git_environment({"PATH": os.environ["PATH"]}))
    assert all(not path.startswith(b"tests/") for _, _, path in entries)


def test_read_tree_rejects_a_commit_that_does_not_exist(
    standard_repo: tuple[Path, str],
) -> None:
    """read_tree refuses a commit that the repository does not have."""
    repo, _ = standard_repo
    with pytest.raises(ar.Rejected):
        ar.read_tree(repo, "f" * 40, ar.git_environment({"PATH": os.environ["PATH"]}))


# --- check_tree_shape ---------------------------------------------------------------


def test_check_tree_shape_accepts_the_standard_entries() -> None:
    """check_tree_shape accepts a tree with the usual entries."""
    ar.check_tree_shape(standard_entries())


def test_check_tree_shape_refuses_more_entries_than_the_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """check_tree_shape refuses a tree with more entries than the limit."""
    monkeypatch.setattr(ar, "MAX_ENTRIES", 3)
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(standard_entries())
    assert "more than" in str(info.value)


@pytest.mark.parametrize(
    "path",
    [
        b"docs/a\nb.md",
        b"docs/a\x01b.md",
        b"docs/a\x7fb.md",
        b"docs/a\rb.md",
        b"docs/\n::error::boom.md",
    ],
)
def test_check_tree_shape_refuses_a_control_character_in_a_path(path: bytes) -> None:
    """check_tree_shape refuses a path that contains a control character."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(path)])
    assert "control character" in str(info.value)
    assert_inert_output(str(info.value))


def test_check_tree_shape_refuses_a_backslash_in_a_path() -> None:
    """check_tree_shape refuses a path that contains a backslash."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(b"docs\\evil.md")])
    assert "backslash" in str(info.value)


@pytest.mark.parametrize(
    "path",
    [
        b"docs/../x.md",
        b"docs/./x.md",
        b"docs//x.md",
        b"docs/.git/config",
        b"docs/.GIT/config",
        b"docs/x/",
    ],
)
def test_check_tree_shape_refuses_a_path_that_is_not_in_normal_form(path: bytes) -> None:
    """check_tree_shape refuses a path that is not in normal form, such as one with a .. part."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(path)])
    assert "normal form" in str(info.value)


# A part that another system reads as the .git directory: Windows drops trailing dots and
# spaces and has the short name GIT~1; NTFS reads a stream suffix after a colon; macOS drops
# characters that are default-ignorable in Unicode (zero-width and others). Written as the
# code points, so that no editor can hide them.
GIT_LOOK_ALIKES = [
    b"docs/.git ",
    b"docs/.git  ",
    b"docs/.git.",
    b"docs/.git..",
    b"docs/.git. .",
    b"docs/.Git ",
    "docs/.gi\u200ct".encode(),  # zero-width non-joiner
    "docs/.\u200bgit".encode(),  # zero-width space
    "docs/.git\u200d".encode(),  # zero-width joiner
    "docs/.g\u00adit".encode(),  # soft hyphen
    "docs/.git\ufeff".encode(),  # byte order mark
    "docs/.gi\u2060t".encode(),  # word joiner
    "docs/.gi\u202et".encode(),  # right-to-left override
    "docs/.gi\ufe0ft".encode(),  # variation selector
    "docs/.gi\U000e0100t".encode(),  # variation selector supplement
    b"docs/GIT~1",
    b"docs/git~1",
    b"docs/Git~1",
    b"docs/GIT~1 ",
    b"docs/.git::$INDEX_ALLOCATION",
    b"docs/.git:stream",
    b".git ",
    b"GIT~1/config",
    b"docs/sub/.git /config",
]


@pytest.mark.parametrize("path", GIT_LOOK_ALIKES)
def test_check_tree_shape_refuses_a_part_that_another_system_reads_as_dot_git(path: bytes) -> None:
    """check_tree_shape refuses a path part that another system could read as .git."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(path)])
    assert "normal form" in str(info.value)
    assert_inert_output(str(info.value))


@pytest.mark.parametrize(
    "name",
    [
        b"docs/.gitignore",
        b"docs/.gitattributes",
        b"docs/.github/x.md",
        b"docs/git",
        b"docs/gitlab.md",
        b"docs/digit.md",
        b"docs/legit~1",
        b"docs/GIT~12",
        b"docs/my.git.md",
        b"docs/a.git",
        b"docs/.gitkeep",
        b"docs/git~",
        "docs/café.md".encode(),
        "docs/Hexagonal Architecture – Guide.docx".encode(),
        "docs/日本語.md".encode(),
    ],
)
def test_check_tree_shape_accepts_names_that_only_look_a_little_like_dot_git(name: bytes) -> None:
    """check_tree_shape accepts names such as .gitignore that only resemble .git."""
    ar.check_tree_shape([*standard_entries(), entry(name)])


def test_check_tree_shape_refuses_two_paths_that_differ_only_in_letter_case() -> None:
    """check_tree_shape refuses two file paths that differ only in letter case."""
    entries = [*standard_entries(), entry("docs/readme.md"), entry("docs/README.md")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "differ only in" in str(info.value)
    assert "docs/readme.md" in str(info.value)
    assert "docs/README.md" in str(info.value)


def test_check_tree_shape_refuses_two_directories_that_differ_only_in_letter_case() -> None:
    """check_tree_shape refuses two folders whose names differ only in letter case."""
    entries = [*standard_entries(), entry("docs/Extra/a.md"), entry("docs/extra/b.md")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "differ only in" in str(info.value)


def test_check_tree_shape_refuses_a_file_and_a_directory_that_differ_only_in_letter_case() -> None:
    """check_tree_shape refuses a file and a folder whose names differ only in letter case."""
    entries = [*standard_entries(), entry("docs/Notes"), entry("docs/notes/a.md")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "differ only in" in str(info.value)


def test_check_tree_shape_refuses_two_names_that_differ_only_in_the_form_of_a_character() -> None:
    """check_tree_shape refuses two names that differ only in Unicode normalization form."""
    composed = "docs/caf\u00e9.md".encode()
    decomposed = "docs/cafe\u0301.md".encode()
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(composed), entry(decomposed)])
    assert "differ only in" in str(info.value)


def test_check_tree_shape_refuses_two_names_that_differ_in_case_and_in_character_form() -> None:
    """check_tree_shape refuses two names that differ only in case and normalization together."""
    entries = [
        *standard_entries(),
        entry("docs/Café.md".encode()),
        entry("docs/cafe\u0301.MD".encode()),
    ]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "differ only in" in str(info.value)


def test_check_tree_shape_accepts_names_that_differ_in_more_than_case() -> None:
    """check_tree_shape accepts names that differ by more than letter case."""
    entries = [
        *standard_entries(),
        entry("docs/readme.md"),
        entry("docs/readme2.md"),
        entry("docs/Extra/a.md"),
        entry("docs/Extras/b.md"),
        entry("docs/café.md".encode()),
        entry("docs/cafe.md"),
    ]
    ar.check_tree_shape(entries)


@pytest.mark.parametrize(
    "path", [b"docs/\xff.md", b"docs/a\xc3.md", b"docs/\xed\xa0\x80.md", b"\xfe/x"]
)
def test_check_tree_shape_refuses_a_name_that_is_not_valid_utf_8(path: bytes) -> None:
    """check_tree_shape refuses a path that is not valid UTF-8."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry(path)])
    assert "UTF-8" in str(info.value)
    assert_inert_output(str(info.value))


def test_check_tree_shape_refuses_a_path_that_is_both_a_file_and_a_directory() -> None:
    """check_tree_shape refuses a path that is both a file and the parent of other entries."""
    entries = [*standard_entries(), entry("docs/a"), entry("docs/a/b")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "both a file and a directory" in str(info.value)


def test_check_tree_shape_refuses_a_path_that_occurs_twice() -> None:
    """check_tree_shape refuses a tree in which a path occurs twice."""
    entries = [*standard_entries(), entry("docs/guide.md")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "occurs twice" in str(info.value)


def test_check_tree_shape_refuses_an_entry_outside_the_packed_paths() -> None:
    """check_tree_shape refuses any entry that lies outside the packed folders and files."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry("tests/x.py")])
    assert "outside the packed paths" in str(info.value)


def test_check_tree_shape_refuses_a_packed_file_name_that_is_a_directory() -> None:
    """check_tree_shape refuses a packed file name that is a folder in the commit."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape([*standard_entries(), entry("pytest.ini/inner")])
    assert "pytest.ini" in str(info.value)


def test_check_tree_shape_refuses_a_packed_directory_name_that_is_a_file() -> None:
    """check_tree_shape refuses a packed folder name that is a file in the commit."""
    entries = [item for item in standard_entries() if not item[2].startswith(b"hooks/")]
    entries.append(entry("hooks"))
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert "hooks" in str(info.value)


@pytest.mark.parametrize(
    "name", ["hooks", ".claude-plugin", "README.md", ".gitignore", "pytest.ini"]
)
def test_check_tree_shape_refuses_a_commit_that_has_nothing_at_a_packed_path(name: str) -> None:
    """check_tree_shape refuses a commit that lacks one of the packed paths."""
    entries = [
        item
        for item in standard_entries()
        if item[2] != name.encode() and not item[2].startswith(name.encode() + b"/")
    ]
    with pytest.raises(ar.Rejected) as info:
        ar.check_tree_shape(entries)
    assert f"nothing at the packed path {name}" in str(info.value)


# --- guard 1: the links ----------------------------------------------------------------


def test_read_link_targets_returns_the_text_of_each_link() -> None:
    """read_link_targets returns each link's target text."""
    blobs = {oid_of(path): target for path, target in KNOWN.items()}
    entries = standard_entries()
    targets = ar.read_link_targets(entries, lambda oid, limit: blobs[oid])
    assert targets == KNOWN


def test_check_links_accepts_exactly_the_two_known_links() -> None:
    """check_links accepts a tree whose only links are the two known ones."""
    ar.check_links(standard_entries(), KNOWN)


def test_check_links_refuses_a_third_link_anywhere() -> None:
    """check_links refuses any link besides the two known ones."""
    entries = [*standard_entries(), entry("docs/extra", b"120000")]
    targets = {**KNOWN, b"docs/extra": b"/etc/passwd"}
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(entries, targets)
    assert "not one of the two known" in str(info.value)
    assert "docs/extra" in str(info.value)


def test_check_links_refuses_a_top_level_file_that_is_a_link_to_a_file_of_the_runner() -> None:
    """check_links refuses a top-level packed file that is a link to a file on the runner."""
    entries = [item for item in standard_entries() if item[2] != b"README.md"]
    entries.append(entry("README.md", b"120000"))
    targets = {**KNOWN, b"README.md": b"/proc/self/environ"}
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(entries, targets)
    assert "README.md" in str(info.value)


@pytest.mark.parametrize("missing", sorted(KNOWN))
def test_check_links_refuses_a_commit_where_a_known_link_is_gone(missing: bytes) -> None:
    """check_links refuses a commit in which one of the two known links is missing."""
    entries = [item for item in standard_entries() if item[2] != missing]
    targets = {path: target for path, target in KNOWN.items() if path != missing}
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(entries, targets)
    assert "known symbolic link is missing" in str(info.value)


@pytest.mark.parametrize(
    "target",
    [
        b"../.context/other",
        b"/etc/passwd",
        b"../.context/rules\n",
        b"..//.context/rules",
        b"",
        b"../.context/rules/",
    ],
)
def test_check_links_refuses_a_known_link_that_points_somewhere_else(target: bytes) -> None:
    """check_links refuses a known link whose target has changed."""
    targets = {**KNOWN, b".claude/rules": target}
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(standard_entries(), targets)
    assert "points somewhere else" in str(info.value)


def test_check_links_refuses_a_known_link_that_would_resolve_inside_the_pack() -> None:
    """check_links refuses a known link whose target would resolve inside the packed files."""
    entries = [*standard_entries(), entry(".context/rules/rule.md")]
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(entries, KNOWN)
    assert "would resolve inside the pack" in str(info.value)


def test_check_links_message_is_inert_for_a_hostile_link_name() -> None:
    """check_links refuses a hostile link name and reports it in cleaned form."""
    hostile = b"docs/\n::error::pwned"
    entries = [*standard_entries(), entry(hostile, b"120000")]
    targets = {**KNOWN, hostile: b"x"}
    with pytest.raises(ar.Rejected) as info:
        ar.check_links(entries, targets)
    assert_inert_output(str(info.value))


# --- object_reader: git cat-file --batch, one object at a time ----------------------------------


def blob_id(repo: Path, git_in: Callable[..., str], path: str) -> bytes:
    """Return the object id that git holds for a path of the committed tree."""
    return git_in(repo, "rev-parse", f"HEAD:{path}").encode()


def test_object_reader_returns_the_content_of_a_blob(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """The object reader returns a blob's exact content."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with ar.object_reader(repo, env) as read:
        assert read(blob_id(repo, git_in, "README.md"), 1000) == (repo / "README.md").read_bytes()
        assert read(blob_id(repo, git_in, "docs/guide.md"), 1000) == b"guide\n"


def test_object_reader_reads_a_link_as_the_text_of_its_target(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """The object reader returns a link's blob as the text of its target."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with ar.object_reader(repo, env) as read:
        assert read(blob_id(repo, git_in, ".claude/rules"), 100) == b"../.context/rules"


def test_object_reader_keeps_answering_after_many_reads(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """The object reader still answers correctly after 300 reads in a row."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    oid = blob_id(repo, git_in, "CLAUDE.md")
    with ar.object_reader(repo, env) as read:
        assert all(read(oid, 100) == b"claude\n" for _ in range(300))


def test_object_reader_refuses_an_object_that_is_not_there(
    standard_repo: tuple[Path, str],
) -> None:
    """The object reader refuses an object id that the repository does not have."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with ar.object_reader(repo, env) as read, pytest.raises(ar.Rejected):
        read(b"1" * 40, 100)


def test_object_reader_refuses_an_object_above_the_limit(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """The object reader refuses an object larger than the size limit."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with ar.object_reader(repo, env) as read, pytest.raises(ar.Rejected) as info:
        read(blob_id(repo, git_in, "README.md"), 3)
    assert "larger than" in str(info.value)


def test_object_reader_refuses_an_object_that_is_a_tree(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """The object reader refuses an object that is a tree, not a blob."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    tree = git_in(repo, "rev-parse", "HEAD:docs").encode()
    with ar.object_reader(repo, env) as read, pytest.raises(ar.Rejected):
        read(tree, 1000)


@pytest.mark.parametrize(
    "name", [b"HEAD", b"1" * 39, b"A" * 40, b"1" * 40 + b"\nHEAD:README.md", b""]
)
def test_object_reader_refuses_a_name_that_is_not_an_object_id(
    standard_repo: tuple[Path, str], name: bytes
) -> None:
    """The object reader refuses a name that is not a 40-digit object id."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with ar.object_reader(repo, env) as read, pytest.raises(ar.Rejected) as info:
        read(name, 100)
    assert "is not an object id" in str(info.value)


def test_object_reader_lets_an_error_of_the_block_through_and_stops_git(
    standard_repo: tuple[Path, str], git_in: Callable[..., str]
) -> None:
    """An error inside the reader's block passes through, and the reader still stops git."""
    repo, _ = standard_repo
    env = ar.git_environment({"PATH": os.environ["PATH"]})
    with pytest.raises(RuntimeError), ar.object_reader(repo, env) as read:
        read(blob_id(repo, git_in, "README.md"), 1000)
        raise RuntimeError("the block failed")


def test_object_reader_refuses_to_start_when_git_is_not_installed(
    standard_repo: tuple[Path, str], tmp_path: Path
) -> None:
    """The object reader refuses to start when git is not installed."""
    repo, _ = standard_repo
    empty = tmp_path / "empty-path"
    empty.mkdir()
    with pytest.raises(ar.Rejected) as info, ar.object_reader(repo, {"PATH": str(empty)}):
        pass
    assert "git" in str(info.value)
