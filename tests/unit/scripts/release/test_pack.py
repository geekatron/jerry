# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for writing the pack from git objects and for comparing it with the commit.

The pack is the tagged tree, written without ``cp``: each file comes from the
object that git holds, each link is made from the text of its blob, and nothing
ever reads through a link. Guard 4 (the pack and output directories must not
exist before packing) and the first half of guard 5 (the packed tree is compared
with the commit, entry by entry, walking it with ``lstat``) are pinned here.
"""

from __future__ import annotations

import contextlib
import hashlib
import os
import signal
import stat
import sys
from collections.abc import Callable, Iterator, Mapping
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    STANDARD_EXECUTABLES,
    STANDARD_FILES,
    assert_inert_output,
)

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

LINKS = {".claude/patterns": "../.context/patterns", ".claude/rules": "../.context/rules"}
TOP = "jerry-plugin-1.2.3"

Entry = tuple[bytes, bytes, bytes]


def blob_oid(data: bytes) -> bytes:
    """Return the git object id of a blob with this content."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest().encode()  # noqa: S324


def build_tree(
    files: Mapping[str, str | bytes],
    links: Mapping[str, str] | None = None,
    executables: tuple[str, ...] = (),
) -> tuple[list[Entry], dict[bytes, bytes]]:
    """Make tree entries and the blobs behind them, as git would hold them."""
    entries: list[Entry] = []
    blobs: dict[bytes, bytes] = {}
    for name, content in files.items():
        data = content.encode() if isinstance(content, str) else content
        oid = blob_oid(data)
        blobs[oid] = data
        entries.append((b"100755" if name in executables else b"100644", oid, name.encode()))
    for name, target in (links or {}).items():
        data = target.encode()
        oid = blob_oid(data)
        blobs[oid] = data
        entries.append((b"120000", oid, name.encode()))
    entries.sort(key=lambda item: item[2])
    return entries, blobs


def packed_files() -> dict[str, str]:
    """Return the standard files that lie under the packed paths."""
    top = set(ar.PACKED_FILES) | set(ar.PACKED_DIRS)
    return {name: text for name, text in STANDARD_FILES.items() if name.split("/")[0] in top}


def standard_tree() -> tuple[list[Entry], dict[bytes, bytes]]:
    """Build the packed part of the standard repository."""
    return build_tree(packed_files(), LINKS, STANDARD_EXECUTABLES)


def reader(blobs: Mapping[bytes, bytes]) -> Callable[[bytes, int], bytes]:
    """Return a stand-in for the git object reader."""
    return lambda oid, limit: blobs[oid]


def known_targets() -> dict[bytes, bytes]:
    """Return the two known links as the checks see them."""
    return {name.encode(): target.encode() for name, target in LINKS.items()}


@contextlib.contextmanager
def deadline(seconds: int) -> Iterator[None]:
    """Fail the test if the code inside blocks, for example on a FIFO behind a link."""

    def blocked(signum: int, frame: object) -> None:
        raise AssertionError("the code blocked: it read through a link")

    previous = signal.signal(signal.SIGALRM, blocked)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


@pytest.fixture
def written(tmp_path: Path) -> tuple[Path, list[Entry]]:
    """Write the standard pack and return its top directory and entries."""
    entries, blobs = standard_tree()
    top = tmp_path / "pack" / TOP
    (tmp_path / "pack").mkdir()
    ar.write_pack(top, entries, reader(blobs))
    return top, entries


# --- make_new_directory (guard 4) ---------------------------------------------------


def test_make_new_directory_creates_a_directory_that_did_not_exist(tmp_path: Path) -> None:
    """make_new_directory creates a folder at a free path."""
    ar.make_new_directory(tmp_path / "fresh", "output directory")
    assert (tmp_path / "fresh").is_dir()


def test_make_new_directory_refuses_a_directory_that_exists(tmp_path: Path) -> None:
    """make_new_directory refuses a path where a folder already exists."""
    (tmp_path / "dist").mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.make_new_directory(tmp_path / "dist", "output directory")
    assert "output directory" in str(info.value)
    assert "exists before packing" in str(info.value)


def test_make_new_directory_refuses_a_file_of_that_name(tmp_path: Path) -> None:
    """make_new_directory refuses a path where a file already exists."""
    (tmp_path / "dist").write_text("x", encoding="utf-8")
    with pytest.raises(ar.Rejected):
        ar.make_new_directory(tmp_path / "dist", "output directory")


def test_make_new_directory_refuses_a_link_of_that_name_even_when_it_points_nowhere(
    tmp_path: Path,
) -> None:
    """make_new_directory refuses a path that holds a link, even a dangling one."""
    os.symlink(tmp_path / "nowhere", tmp_path / "dist")
    with pytest.raises(ar.Rejected):
        ar.make_new_directory(tmp_path / "dist", "output directory")
    assert not (tmp_path / "nowhere").exists()


def test_make_new_directory_refuses_when_the_parent_is_missing(tmp_path: Path) -> None:
    """make_new_directory refuses a path whose parent folder does not exist."""
    with pytest.raises(ar.Rejected):
        ar.make_new_directory(tmp_path / "no" / "such" / "dist", "output directory")


# --- expected_tree ---------------------------------------------------------------------


def test_expected_tree_lists_the_top_directory_parents_files_and_links() -> None:
    """The expected tree holds the top folder, every parent folder, the files and the links."""
    entries, _ = standard_tree()
    expected = ar.expected_tree(entries, known_targets())
    assert expected[b""] == ("dir", 0o755, b"")
    assert expected[b"skills"] == ("dir", 0o755, b"")
    assert expected[b"skills/alpha"] == ("dir", 0o755, b"")
    assert expected[b"skills/alpha/agents/a.md"][0] == "file"
    assert expected[b"scripts/tool.py"][1] == 0o755
    assert expected[b"README.md"][1] == 0o644
    assert expected[b".claude/rules"] == ("link", 0, b"../.context/rules")


def test_expected_tree_has_no_directory_that_holds_no_entry() -> None:
    """The expected tree adds no folder that holds no packed entry, such as .context."""
    entries, _ = standard_tree()
    expected = ar.expected_tree(entries, known_targets())
    directories = {path for path, member in expected.items() if member[0] == "dir"}
    assert b".context" not in directories
    assert directories == {
        b"",
        b".claude",
        b".claude-plugin",
        b"skills",
        b"skills/alpha",
        b"skills/alpha/agents",
        b"src",
        b"src/pkg",
        b"docs",
        b"scripts",
        b"hooks",
    }


# --- write_pack and walk_pack -----------------------------------------------------------


def test_the_pack_that_write_pack_makes_is_the_expected_tree(
    written: tuple[Path, list[Entry]],
) -> None:
    """The folder that write_pack builds matches the expected tree exactly."""
    top, entries = written
    ar.compare_trees("pack", ar.expected_tree(entries, known_targets()), ar.walk_pack(top))


def test_write_pack_sets_the_modes_whatever_the_umask_is(tmp_path: Path) -> None:
    """write_pack sets file modes to 644 or 755, whatever the umask."""
    entries, blobs = standard_tree()
    (tmp_path / "pack").mkdir()
    top = tmp_path / "pack" / TOP
    os.umask(0o077)
    ar.write_pack(top, entries, reader(blobs))
    assert stat.S_IMODE((top / "README.md").lstat().st_mode) == 0o644
    assert stat.S_IMODE((top / "scripts" / "tool.py").lstat().st_mode) == 0o755
    assert stat.S_IMODE((top / "skills").lstat().st_mode) == 0o755
    assert stat.S_IMODE(top.lstat().st_mode) == 0o755


def test_write_pack_makes_each_link_from_the_text_of_its_blob(
    written: tuple[Path, list[Entry]],
) -> None:
    """write_pack makes each link point at the text stored in its blob."""
    top, _ = written
    assert os.readlink(top / ".claude" / "rules") == "../.context/rules"
    assert os.readlink(top / ".claude" / "patterns") == "../.context/patterns"
    assert not os.path.exists(top / ".claude" / "rules")  # both dangle in the pack


def test_write_pack_writes_the_bytes_of_the_blob_without_any_conversion(tmp_path: Path) -> None:
    """write_pack writes each blob's bytes as they are, with no line-ending conversion."""
    # A checkout may change line endings or expand attributes; the pack holds the blob as it is.
    files: dict[str, str | bytes] = {
        "README.md": b"line one\r\nline two\r\n",
        "docs/binary.bin": bytes(range(256)) * 3,
        "docs/no-newline.txt": b"no newline at the end",
        "docs/empty.txt": b"",
        "docs/ident.txt": b"$Id$ and $Format:%H$ stay as they are\n",
        "docs/big.bin": os.urandom(2 * 1024 * 1024 + 5),
    }
    entries, blobs = build_tree(files)
    (tmp_path / "pack").mkdir()
    top = tmp_path / "pack" / TOP
    ar.write_pack(top, entries, reader(blobs))
    for name, content in files.items():
        assert (top / name).read_bytes() == content


def test_write_pack_holds_no_directory_that_git_does_not_hold(tmp_path: Path) -> None:
    """write_pack creates no folder that the commit does not hold."""
    entries, blobs = build_tree({"docs/a.md": "a\n"})
    (tmp_path / "pack").mkdir()
    top = tmp_path / "pack" / TOP
    ar.write_pack(top, entries, reader(blobs))
    assert sorted(path.name for path in top.iterdir()) == ["docs"]
    assert sorted(path.name for path in (top / "docs").iterdir()) == ["a.md"]


def test_write_pack_never_reads_through_a_link(tmp_path: Path) -> None:
    """write_pack writes a link as a link and never reads the file it points to."""
    secret = tmp_path / "runner-file.txt"
    secret.write_text("SECRET-OF-THE-RUNNER", encoding="utf-8")
    files = {"README.md": "readme\n", "docs/guide.md": "guide\n"}
    entries, blobs = build_tree(files, {"CLAUDE.md": str(secret)})
    (tmp_path / "pack").mkdir()
    top = tmp_path / "pack" / TOP
    ar.write_pack(top, entries, reader(blobs))
    assert (top / "CLAUDE.md").is_symlink()
    assert os.readlink(top / "CLAUDE.md") == str(secret)
    for path in top.rglob("*"):
        if path.is_file() and not path.is_symlink():
            assert b"SECRET-OF-THE-RUNNER" not in path.read_bytes()


def test_write_pack_does_not_write_through_a_link_that_a_later_entry_needs_as_a_directory(
    tmp_path: Path,
) -> None:
    """write_pack refuses to write through a link that a later entry would use as a folder."""
    outside = tmp_path / "outside"
    outside.mkdir()
    entries, blobs = build_tree({"docs/x": "payload\n"}, {"docs": str(outside)})
    (tmp_path / "pack").mkdir()
    top = tmp_path / "pack" / TOP
    with pytest.raises(ar.Rejected):
        ar.write_pack(top, entries, reader(blobs))
    assert list(outside.iterdir()) == []


def test_write_pack_refuses_a_top_directory_that_exists(tmp_path: Path) -> None:
    """write_pack refuses to start when the top folder already exists."""
    entries, blobs = standard_tree()
    (tmp_path / "pack" / TOP).mkdir(parents=True)
    with pytest.raises(ar.Rejected) as info:
        ar.write_pack(tmp_path / "pack" / TOP, entries, reader(blobs))
    assert "exists before packing" in str(info.value)


def test_write_pack_refuses_more_content_than_the_bound(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """write_pack refuses content larger in total than the size limit."""
    entries, blobs = standard_tree()
    monkeypatch.setattr(ar, "MAX_PACK_BYTES", 20)
    (tmp_path / "pack").mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.write_pack(tmp_path / "pack" / TOP, entries, reader(blobs))
    assert "more than" in str(info.value)


def test_write_pack_turns_a_failure_to_write_into_a_rejection(tmp_path: Path) -> None:
    """write_pack reports a failure to write as a refusal, not a crash."""
    entries, blobs = standard_tree()
    (tmp_path / "pack").mkdir()
    (tmp_path / "pack").chmod(0o500)
    try:
        if os.access(tmp_path / "pack", os.W_OK):
            pytest.skip("this account can write into a read-only directory")
        with pytest.raises(ar.Rejected):
            ar.write_pack(tmp_path / "pack" / TOP, entries, reader(blobs))
    finally:
        (tmp_path / "pack").chmod(0o700)


def test_write_pack_passes_on_a_rejection_from_the_object_reader(tmp_path: Path) -> None:
    """write_pack passes on a refusal from the object reader unchanged."""
    entries, _ = standard_tree()

    def refuse(oid: bytes, limit: int) -> bytes:
        raise ar.Rejected("git has no such object")

    (tmp_path / "pack").mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.write_pack(tmp_path / "pack" / TOP, entries, refuse)
    assert "no such object" in str(info.value)


# --- compare_trees: every kind of difference between pack and commit ------------------------


def compare(top: Path, entries: list[Entry]) -> None:
    """Compare the pack at ``top`` with the expected tree."""
    ar.compare_trees("pack", ar.expected_tree(entries, known_targets()), ar.walk_pack(top))


def test_compare_refuses_a_file_whose_content_changed(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a packed file whose content changed."""
    top, entries = written
    (top / "README.md").write_bytes(b"tampered\n")
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert "README.md" in str(info.value)
    assert "different" in str(info.value)


def test_compare_refuses_a_content_that_differs_by_one_byte_at_the_end(
    written: tuple[Path, list[Entry]],
) -> None:
    """The comparison catches content that differs only in its last byte."""
    top, entries = written
    (top / "docs" / "guide.md").write_bytes(b"guide\n\n")
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_file_that_lost_its_execute_bit(
    written: tuple[Path, list[Entry]],
) -> None:
    """The comparison refuses a file that lost its execute bit."""
    top, entries = written
    (top / "scripts" / "tool.py").chmod(0o644)
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert "tool.py" in str(info.value)


def test_compare_refuses_a_file_that_gained_the_execute_bit(
    written: tuple[Path, list[Entry]],
) -> None:
    """The comparison refuses a file that gained an execute bit."""
    top, entries = written
    (top / "README.md").chmod(0o755)
    with pytest.raises(ar.Rejected):
        compare(top, entries)


@pytest.mark.parametrize("mode", [0o664, 0o666, 0o600, 0o745])
def test_compare_refuses_a_mode_other_than_the_two_that_git_records(
    mode: int, written: tuple[Path, list[Entry]]
) -> None:
    """The comparison refuses a file mode other than 644 or 755."""
    top, entries = written
    (top / "README.md").chmod(mode)
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_directory_with_another_mode(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a folder whose mode is not 755."""
    top, entries = written
    (top / "skills").chmod(0o775)
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_missing_file(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a pack that lacks a file."""
    top, entries = written
    (top / "hooks" / "hook.py").unlink()
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert "missing" in str(info.value)


def test_compare_refuses_an_extra_file(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a pack with an extra file."""
    top, entries = written
    (top / "docs" / "stray.md").write_text("stray\n", encoding="utf-8")
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert "extra" in str(info.value)


def test_compare_refuses_an_empty_directory_that_git_does_not_hold(
    written: tuple[Path, list[Entry]],
) -> None:
    """The comparison refuses an empty folder that the commit does not hold."""
    top, entries = written
    (top / "docs" / "emptydir").mkdir()
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_file_that_was_replaced_by_a_link_to_another_file(
    written: tuple[Path, list[Entry]], tmp_path: Path
) -> None:
    """The comparison refuses a file replaced by a link to another file."""
    top, entries = written
    other = tmp_path / "other.md"
    other.write_text("readme\n", encoding="utf-8")  # same content as the genuine file
    (top / "README.md").unlink()
    os.symlink(other, top / "README.md")
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_directory_that_was_replaced_by_a_link(
    written: tuple[Path, list[Entry]], tmp_path: Path
) -> None:
    """The comparison refuses a folder replaced by a link."""
    top, entries = written
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (top / "hooks" / "hook.py").unlink()
    (top / "hooks").rmdir()
    os.symlink(elsewhere, top / "hooks")
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_compare_refuses_a_link_that_was_retargeted(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a link that now points elsewhere."""
    top, entries = written
    (top / ".claude" / "rules").unlink()
    os.symlink("../.context/other", top / ".claude" / "rules")
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert ".claude/rules" in str(info.value)


def test_compare_refuses_a_link_that_became_a_file(written: tuple[Path, list[Entry]]) -> None:
    """The comparison refuses a link that was replaced by a file."""
    top, entries = written
    (top / ".claude" / "rules").unlink()
    (top / ".claude" / "rules").write_text("../.context/rules", encoding="utf-8")
    with pytest.raises(ar.Rejected):
        compare(top, entries)


def test_walk_pack_refuses_something_that_is_not_a_file_a_directory_or_a_link(
    written: tuple[Path, list[Entry]],
) -> None:
    """walk_pack refuses an entry that is not a file, folder or link, such as a pipe."""
    top, _ = written
    os.mkfifo(top / "docs" / "pipe")
    with pytest.raises(ar.Rejected) as info:
        ar.walk_pack(top)
    assert "not a file, a directory or a symbolic link" in str(info.value)


def test_walk_pack_does_not_open_what_a_link_points_at(
    written: tuple[Path, list[Entry]], tmp_path: Path
) -> None:
    """walk_pack records a link's target without opening it, even a pipe."""
    top, _ = written
    fifo = tmp_path / "blocks-on-open"
    os.mkfifo(fifo)  # opening this for reading would block for ever
    os.symlink(fifo, top / "docs" / "pointer")
    with deadline(10):
        tree = ar.walk_pack(top)
    assert tree[b"docs/pointer"] == ("link", 0, str(fifo).encode())


def test_walk_pack_does_not_descend_into_a_directory_behind_a_link(
    written: tuple[Path, list[Entry]], tmp_path: Path
) -> None:
    """walk_pack records a link to a folder as a link and does not walk into it."""
    top, _ = written
    outside = tmp_path / "outside"
    (outside / "deep").mkdir(parents=True)
    (outside / "deep" / "file.txt").write_text("x", encoding="utf-8")
    os.symlink(outside, top / "docs" / "pointer")
    tree = ar.walk_pack(top)
    assert tree[b"docs/pointer"][0] == "link"
    assert not any(path.startswith(b"docs/pointer/") for path in tree)


def test_walk_pack_refuses_a_top_directory_that_is_a_link(tmp_path: Path) -> None:
    """walk_pack refuses a top folder that is a link."""
    real = tmp_path / "real"
    real.mkdir()
    os.symlink(real, tmp_path / "top")
    with pytest.raises(ar.Rejected):
        ar.walk_pack(tmp_path / "top")


def test_compare_trees_says_how_many_differ_and_names_the_first(
    written: tuple[Path, list[Entry]], capsys: pytest.CaptureFixture[str]
) -> None:
    """A mismatch is refused with the number of differences and the first one named."""
    top, entries = written
    (top / "README.md").write_bytes(b"x")
    (top / "docs" / "stray.md").write_text("stray\n", encoding="utf-8")
    (top / "hooks" / "hook.py").unlink()
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    message = str(info.value)
    assert "1 missing, 1 extra, 1 different" in message
    assert "not the tagged tree" in message
    printed = capsys.readouterr().out
    assert "hooks/hook.py" in printed
    assert "docs/stray.md" in printed
    assert "README.md" in printed


def test_compare_trees_prints_the_first_ten_of_a_kind_and_counts_the_rest(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """compare_trees lists up to ten differences of each kind and counts the rest."""
    expected = {b"": ("dir", 0o755, b"")}
    expected.update({f"f{number:02d}".encode(): ("file", 0o644, b"a" * 40) for number in range(14)})
    actual = {b"": ("dir", 0o755, b"")}
    with pytest.raises(ar.Rejected) as info:
        ar.compare_trees("pack", expected, actual)
    assert "14 missing, 0 extra, 0 different" in str(info.value)
    printed = capsys.readouterr().out.splitlines()
    assert sum(1 for line in printed if line.startswith("  missing: ")) == 10
    assert "  ... and 4 more missing" in printed


def test_compare_trees_is_inert_for_a_hostile_file_name(
    written: tuple[Path, list[Entry]], capsys: pytest.CaptureFixture[str]
) -> None:
    """compare_trees reports a hostile file name in cleaned form."""
    top, entries = written
    hostile = os.fsencode(top) + b"/docs/\n::error::pwned\n##[add-mask]x"
    with open(hostile, "wb") as handle:
        handle.write(b"x")
    with pytest.raises(ar.Rejected) as info:
        compare(top, entries)
    assert_inert_output(str(info.value))
    assert_inert_output(capsys.readouterr().out)


def test_compare_trees_accepts_two_equal_trees() -> None:
    """compare_trees raises nothing when the two trees are equal."""
    tree = {b"": ("dir", 0o755, b""), b"a": ("file", 0o644, b"x" * 40)}
    ar.compare_trees("pack", tree, dict(tree))


# --- check_links_dangle: both known links must dangle in the pack --------------------------


def test_check_links_dangle_accepts_the_standard_pack(written: tuple[Path, list[Entry]]) -> None:
    """check_links_dangle accepts the standard pack, whose two links point outside it."""
    top, _ = written
    ar.check_links_dangle(top)


@pytest.mark.parametrize("kind", ["directory", "file", "link"])
def test_check_links_dangle_refuses_a_pack_where_a_link_would_resolve(
    kind: str, written: tuple[Path, list[Entry]], tmp_path: Path
) -> None:
    """check_links_dangle refuses a pack in which a link would resolve to a packed file."""
    top, _ = written
    (top / ".context").mkdir()
    target = top / ".context" / "rules"
    if kind == "directory":
        target.mkdir()
    elif kind == "file":
        target.write_text("x", encoding="utf-8")
    else:
        os.symlink(tmp_path, target)
    with pytest.raises(ar.Rejected) as info:
        ar.check_links_dangle(top)
    assert "resolves in the pack" in str(info.value)
