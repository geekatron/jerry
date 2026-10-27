# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for making the archives and for judging what they hold.

No test here builds, lists or unpacks an archive. The code that calls ``tar``
and ``zip`` is tested with fake programs that record how they were called. The
code that judges the members of an archive works on plain member records, so it
is tested with ``TarInfo`` and ``ZipInfo`` objects made in memory. The two thin
readers that open a real archive are tested by the archive tests, which are
skipped unless real tools may run (see ``test_archive_tools.py``).

Guard 2 is pinned here for the packing tools: they get no signing-request
variable. Guard 5, second half: each archive is judged against what the tagged
tree implies. A tar holds files, links and directories; a zip holds files and
directories, but not the two links, because they dangle in the pack and ``zip``
leaves out what it cannot find.
"""

from __future__ import annotations

import hashlib
import io
import os
import sys
import tarfile
import zipfile
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import assert_inert_output  # noqa: E402

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

TOP = "jerry-plugin-1.2.3"


def blob_oid(data: bytes) -> bytes:
    """Return the git object id of a blob with this content."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest().encode()  # noqa: S324


# --- names ------------------------------------------------------------------------------------


def test_archive_names_follow_the_version() -> None:
    """archive_names builds the top folder and both archive file names from the version."""
    assert ar.archive_names("1.2.3") == (
        "jerry-plugin-1.2.3",
        "jerry-plugin-1.2.3.tar.gz",
        "jerry-plugin-1.2.3.zip",
    )


# --- run_tool ---------------------------------------------------------------------------------


def test_run_tool_returns_the_standard_output_of_the_program() -> None:
    """run_tool returns what the program wrote to standard output."""
    out = ar.run_tool(["sh", "-c", "printf hello"], env={"PATH": os.environ["PATH"]}, what="sh")
    assert out == b"hello"


def test_run_tool_passes_standard_input_and_the_working_folder(tmp_path: Path) -> None:
    """run_tool feeds the given input to the program and runs it in the given folder."""
    out = ar.run_tool(
        ["sh", "-c", "cat; pwd"],
        env={"PATH": os.environ["PATH"]},
        what="sh",
        stdin=b"input\n",
        cwd=tmp_path,
    )
    assert out.startswith(b"input\n")
    assert out.strip().endswith(os.fsencode(tmp_path.resolve()))


def test_run_tool_runs_the_program_without_a_shell() -> None:
    """run_tool passes arguments as they are, with no shell to expand ;, $ or *."""
    out = ar.run_tool(
        ["printf", "%s", "a b;c $HOME *"], env={"PATH": os.environ["PATH"]}, what="printf"
    )
    assert out == b"a b;c $HOME *"


def test_run_tool_rejects_a_failing_program_with_its_exit_status_and_a_cleaned_message() -> None:
    """A failing program is refused with its exit status and a cleaned error message."""
    with pytest.raises(ar.Rejected) as info:
        ar.run_tool(
            ["sh", "-c", "echo '::error::pwned' >&2; echo '##[add-mask]x' >&2; exit 3"],
            env={"PATH": os.environ["PATH"]},
            what="tool",
        )
    message = str(info.value)
    assert "tool failed with exit status 3" in message
    assert_inert_output(message)
    assert "\n" not in message


def test_run_tool_rejects_a_program_that_is_not_installed(tmp_path: Path) -> None:
    """run_tool refuses, with a reason, a program that is not installed."""
    with pytest.raises(ar.Rejected) as info:
        ar.run_tool(["no-such-tool-xyz"], env={"PATH": str(tmp_path)}, what="no-such-tool-xyz")
    assert "is not installed" in str(info.value)


def test_run_tool_rejects_a_program_that_runs_too_long() -> None:
    """run_tool stops and refuses a program that runs past its time limit."""
    with pytest.raises(ar.Rejected) as info:
        ar.run_tool(["sleep", "5"], env={"PATH": os.environ["PATH"]}, what="sleep", timeout=0.2)
    assert "did not finish" in str(info.value)


def test_run_tool_cuts_a_very_long_message() -> None:
    """run_tool shortens a very long error message before reporting it."""
    with pytest.raises(ar.Rejected) as info:
        ar.run_tool(
            ["sh", "-c", "i=0; while [ $i -lt 3000 ]; do printf x; i=$((i+1)); done >&2; exit 1"],
            env={"PATH": os.environ["PATH"]},
            what="tool",
        )
    assert len(str(info.value)) < 600


# --- pack_archives: guard 2 and the way the tools are called --------------------------------


PARENT_WITH_TOKENS = {
    "PATH": "",
    "HOME": "/nonexistent-home",
    "LANG": "C.UTF-8",
    "ACTIONS_ID_TOKEN_REQUEST_TOKEN": "secret-request-token",
    "ACTIONS_ID_TOKEN_REQUEST_URL": "https://token.example.invalid/request",
    "GITHUB_TOKEN": "secret-github-token",
    "ACTIONS_RUNTIME_TOKEN": "secret-runtime-token",
}


def packer_env() -> dict[str, str]:
    """Return the environment that the script gives to ``tar`` and ``zip``."""
    parent = dict(PARENT_WITH_TOKENS)
    parent["PATH"] = os.environ["PATH"]
    return ar.packer_environment(parent)


def test_pack_archives_calls_tar_and_then_zip_with_quiet_arguments_from_the_pack_directory(
    tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """pack_archives runs tar, then zip, with quiet options, from the pack folder."""
    fake = fake_tools()
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    ar.pack_archives(pack, TOP, out / f"{TOP}.tar.gz", out / f"{TOP}.zip", packer_env())
    calls = fake.calls()
    assert [call["tool"] for call in calls] == ["tar", "zip"]
    assert calls[0]["args"] == ["-czf", str(out / f"{TOP}.tar.gz"), TOP]
    assert calls[1]["args"] == ["-rq", str(out / f"{TOP}.zip"), TOP]
    assert os.path.realpath(str(calls[0]["cwd"])) == os.path.realpath(pack)
    assert os.path.realpath(str(calls[1]["cwd"])) == os.path.realpath(pack)
    assert (out / f"{TOP}.tar.gz").exists()
    assert (out / f"{TOP}.zip").exists()


def test_pack_archives_gives_neither_tool_a_signing_request_variable_nor_any_other_secret(
    tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """Neither tar nor zip receives a signing-request variable or any other secret."""
    fake = fake_tools()
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", packer_env())
    for call in fake.calls():
        names = set(call["env"])  # type: ignore[arg-type]
        assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" not in names
        assert "ACTIONS_ID_TOKEN_REQUEST_URL" not in names
        assert "ACTIONS_RUNTIME_TOKEN" not in names
        assert "GITHUB_TOKEN" not in names
        assert call["env"]["LANG"] == "C.UTF-8"  # type: ignore[index]


def test_pack_archives_stops_when_tar_fails_and_does_not_run_zip(
    tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """When tar fails, pack_archives stops before running zip."""
    fake = fake_tools(tar_code=2, tar_stderr="tar: ::error::cannot do it\n")
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", packer_env())
    assert "tar failed with exit status 2" in str(info.value)
    assert_inert_output(str(info.value))
    assert [call["tool"] for call in fake.calls()] == ["tar"]


def test_pack_archives_stops_when_zip_fails(
    tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """When zip fails, pack_archives stops with a refusal."""
    fake_tools(zip_code=18, zip_stderr="zip error: could not open for reading\n")
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", packer_env())
    assert "zip failed with exit status 18" in str(info.value)


@pytest.mark.parametrize("existing", ["a.tar.gz", "a.zip"])
def test_pack_archives_refuses_an_archive_that_exists_before_packing(
    existing: str, tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """pack_archives refuses to start when an archive file already exists."""
    fake = fake_tools()
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    (out / existing).write_bytes(b"left over from somewhere")
    with pytest.raises(ar.Rejected) as info:
        ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", packer_env())
    assert "exists before packing" in str(info.value)
    assert fake.calls() == []


def test_pack_archives_refuses_a_link_where_an_archive_should_go(
    tmp_path: Path, fake_tools: Callable[..., SimpleNamespace]
) -> None:
    """pack_archives refuses a symbolic link at an archive's path."""
    fake = fake_tools()
    pack = tmp_path / "pack"
    pack.mkdir()
    out = tmp_path / "dist"
    out.mkdir()
    os.symlink(tmp_path / "nowhere", out / "a.zip")
    with pytest.raises(ar.Rejected):
        ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", packer_env())
    assert fake.calls() == []


# --- tar_members_view -----------------------------------------------------------------------------


def tar_item(
    name: str,
    kind: str = "file",
    data: bytes = b"",
    mode: int = 0o644,
    linkname: str = "",
) -> tuple[tarfile.TarInfo, io.BytesIO | None]:
    """Make a tar member record in memory."""
    info = tarfile.TarInfo(name)
    info.mode = mode
    info.linkname = linkname
    kinds = {
        "file": tarfile.REGTYPE,
        "dir": tarfile.DIRTYPE,
        "symlink": tarfile.SYMTYPE,
        "hardlink": tarfile.LNKTYPE,
        "device": tarfile.CHRTYPE,
        "fifo": tarfile.FIFOTYPE,
    }
    info.type = kinds[kind]
    if kind == "file":
        info.size = len(data)
        return info, io.BytesIO(data)
    return info, None


def test_tar_members_view_reads_directories_files_and_links_relative_to_the_top() -> None:
    """The tar view lists folders, files and links by their path below the top folder."""
    items = [
        tar_item(TOP, "dir", mode=0o755),
        tar_item(f"{TOP}/docs", "dir", mode=0o755),
        tar_item(f"{TOP}/docs/a.md", data=b"hello\n"),
        tar_item(f"{TOP}/bin.sh", data=b"#!/bin/sh\n", mode=0o755),
        tar_item(f"{TOP}/.claude/rules", "symlink", linkname="../.context/rules"),
    ]
    view = ar.tar_members_view(items, TOP)
    assert view[b""] == ("dir", 0o755, b"")
    assert view[b"docs"] == ("dir", 0o755, b"")
    assert view[b"docs/a.md"] == ("file", 0o644, blob_oid(b"hello\n"))
    assert view[b"bin.sh"] == ("file", 0o755, blob_oid(b"#!/bin/sh\n"))
    assert view[b".claude/rules"] == ("link", 0, b"../.context/rules")
    assert len(view) == 5


@pytest.mark.parametrize(
    ("mode", "expected"),
    [(0o644, 0o644), (0o755, 0o755), (0o775, 0o755), (0o700, 0o755), (0o666, 0o644)],
)
def test_tar_members_view_reduces_a_mode_to_the_owner_execute_bit(mode: int, expected: int) -> None:
    """The tar view reduces each file mode to 755 or 644, by the owner's execute bit."""
    view = ar.tar_members_view([tar_item(TOP, "dir"), tar_item(f"{TOP}/f", mode=mode)], TOP)
    assert view[b"f"][1] == expected


def test_tar_members_view_accepts_a_directory_name_with_a_trailing_slash() -> None:
    """The tar view accepts a folder name that ends with a slash."""
    view = ar.tar_members_view([tar_item(f"{TOP}/", "dir"), tar_item(f"{TOP}/d/", "dir")], TOP)
    assert set(view) == {b"", b"d"}


@pytest.mark.parametrize(
    "name",
    [
        "other-dir/file",
        f"{TOP}x/file",
        f"/{TOP}/file",
        f"./{TOP}/file",
        f"{TOP}/../escape",
        f"{TOP}/./file",
        f"{TOP}//file",
        f"{TOP}/a/../../escape",
    ],
)
def test_tar_members_view_refuses_a_name_outside_the_top_or_not_in_normal_form(name: str) -> None:
    """The tar view refuses a name outside the top folder or not in normal form."""
    with pytest.raises(ar.Rejected):
        ar.tar_members_view([tar_item(name)], TOP)


def test_tar_members_view_refuses_a_name_that_occurs_twice() -> None:
    """The tar view refuses an archive in which a name occurs twice."""
    items = [tar_item(f"{TOP}/a", data=b"1"), tar_item(f"{TOP}/a", data=b"2")]
    with pytest.raises(ar.Rejected) as info:
        ar.tar_members_view(items, TOP)
    assert "occurs twice" in str(info.value)


@pytest.mark.parametrize("kind", ["hardlink", "device", "fifo"])
def test_tar_members_view_refuses_a_member_that_is_not_a_file_a_directory_or_a_symbolic_link(
    kind: str,
) -> None:
    """The tar view refuses a member that is not a file, folder or symbolic link."""
    with pytest.raises(ar.Rejected) as info:
        ar.tar_members_view([tar_item(f"{TOP}/x", kind)], TOP)
    assert "not a file, a directory or a symbolic link" in str(info.value)


def test_tar_members_view_refuses_a_file_whose_data_is_not_as_long_as_its_size() -> None:
    """The tar view refuses a file whose data is shorter than its stated size."""
    info = tarfile.TarInfo(f"{TOP}/short")
    info.size = 10
    with pytest.raises(ar.Rejected) as raised:
        ar.tar_members_view([(info, io.BytesIO(b"abc"))], TOP)
    assert "size" in str(raised.value)


def test_tar_members_view_refuses_a_file_whose_data_is_longer_than_its_size() -> None:
    """The tar view refuses a file whose data is longer than its stated size."""
    info = tarfile.TarInfo(f"{TOP}/long")
    info.size = 2
    with pytest.raises(ar.Rejected) as raised:
        ar.tar_members_view([(info, io.BytesIO(b"abcdef"))], TOP)
    assert "size" in str(raised.value)


def test_tar_members_view_is_inert_for_a_hostile_name() -> None:
    """The tar view refuses a hostile member name and reports it in cleaned form."""
    with pytest.raises(ar.Rejected) as info:
        ar.tar_members_view([tar_item("::error::pwned\n##[add-mask]x/file")], TOP)
    assert_inert_output(str(info.value))


# --- zip_members_view --------------------------------------------------------------------------------


def zip_item(
    name: str,
    data: bytes = b"",
    *,
    kind: str = "file",
    mode: int = 0o644,
    utf8: bool = True,
) -> tuple[zipfile.ZipInfo, Callable[[], io.BytesIO]]:
    """Make a zip member record in memory, as ``zip`` on Unix would write it."""
    info = zipfile.ZipInfo(name)
    info.create_system = 3
    info.file_size = len(data)
    if utf8:
        info.flag_bits |= 0x800
    if kind == "dir":
        info.external_attr = ((0o40000 | mode) << 16) | 0x10
    elif kind == "symlink":
        info.external_attr = (0o120777) << 16
    else:
        info.external_attr = (0o100000 | mode) << 16
    return info, lambda: io.BytesIO(data)


def test_zip_members_view_reads_directories_and_files_relative_to_the_top() -> None:
    """The zip view lists folders and files by their path below the top folder."""
    items = [
        zip_item(f"{TOP}/", kind="dir", mode=0o755),
        zip_item(f"{TOP}/docs/", kind="dir", mode=0o755),
        zip_item(f"{TOP}/docs/a.md", b"hello\n"),
        zip_item(f"{TOP}/bin.sh", b"#!/bin/sh\n", mode=0o755),
    ]
    view = ar.zip_members_view(items, TOP)
    assert view[b""] == ("dir", 0o755, b"")
    assert view[b"docs"] == ("dir", 0o755, b"")
    assert view[b"docs/a.md"] == ("file", 0o644, blob_oid(b"hello\n"))
    assert view[b"bin.sh"] == ("file", 0o755, blob_oid(b"#!/bin/sh\n"))
    assert len(view) == 4


def test_zip_members_view_refuses_a_member_that_is_a_symbolic_link() -> None:
    """The zip view refuses a member stored as a symbolic link."""
    with pytest.raises(ar.Rejected) as info:
        ar.zip_members_view(
            [zip_item(f"{TOP}/", kind="dir"), zip_item(f"{TOP}/l", kind="symlink")], TOP
        )
    assert "symbolic link" in str(info.value)


@pytest.mark.parametrize(
    "name", ["other/file", f"/{TOP}/file", f"{TOP}/../x", f"{TOP}//x", f"{TOP}/./x"]
)
def test_zip_members_view_refuses_a_name_outside_the_top_or_not_in_normal_form(name: str) -> None:
    """The zip view refuses a name outside the top folder or not in normal form."""
    with pytest.raises(ar.Rejected):
        ar.zip_members_view([zip_item(name)], TOP)


def test_zip_members_view_refuses_a_name_that_occurs_twice() -> None:
    """The zip view refuses an archive in which a name occurs twice."""
    with pytest.raises(ar.Rejected) as info:
        ar.zip_members_view([zip_item(f"{TOP}/a", b"1"), zip_item(f"{TOP}/a", b"2")], TOP)
    assert "occurs twice" in str(info.value)


def test_zip_members_view_treats_a_directory_and_a_file_of_the_same_name_as_a_repeat() -> None:
    """In a zip, a folder and a file with the same name count as a repeated name."""
    with pytest.raises(ar.Rejected):
        ar.zip_members_view([zip_item(f"{TOP}/a/", kind="dir"), zip_item(f"{TOP}/a", b"1")], TOP)


def test_zip_members_view_refuses_a_file_whose_data_is_not_as_long_as_its_size() -> None:
    """The zip view refuses a file whose data is shorter than its stated size."""
    info, _ = zip_item(f"{TOP}/short", b"0123456789")
    with pytest.raises(ar.Rejected) as raised:
        ar.zip_members_view([(info, lambda: io.BytesIO(b"abc"))], TOP)
    assert "size" in str(raised.value)


def test_zip_members_view_recovers_the_bytes_of_a_name_whatever_the_encoding_flag() -> None:
    """The zip view recovers a name's original bytes, with or without the UTF-8 flag."""
    raw = "docs/– dash.md".encode()  # an en dash, as in one real file name
    flagged = zip_item(f"{TOP}/docs/– dash.md", b"x", utf8=True)
    unflagged = zip_item(f"{TOP}/".encode().decode() + raw.decode("cp437"), b"x", utf8=False)
    for item in (flagged, unflagged):
        view = ar.zip_members_view([zip_item(f"{TOP}/", kind="dir"), item], TOP)
        assert raw in view


def test_zip_members_view_reads_the_owner_execute_bit_from_the_unix_attributes() -> None:
    """The zip view reads the owner's execute bit from the Unix attributes."""
    items = [
        zip_item(f"{TOP}/", kind="dir"),
        zip_item(f"{TOP}/x", b"1", mode=0o755),
        zip_item(f"{TOP}/y", b"1", mode=0o664),
    ]
    view = ar.zip_members_view(items, TOP)
    assert view[b"x"][1] == 0o755
    assert view[b"y"][1] == 0o644


def test_zip_members_view_treats_a_member_without_unix_attributes_as_not_executable() -> None:
    """A zip member with no Unix attributes is read as not executable (644)."""
    info = zipfile.ZipInfo(f"{TOP}/f")
    info.create_system = 0
    info.file_size = 1
    view = ar.zip_members_view(
        [zip_item(f"{TOP}/", kind="dir"), (info, lambda: io.BytesIO(b"1"))], TOP
    )
    assert view[b"f"][1] == 0o644


# --- archive_view and check_archive ----------------------------------------------------------------------


def expected_pack() -> dict[bytes, tuple[str, int, bytes]]:
    """Return a small expected tree with a directory, two files and one link."""
    return {
        b"": ("dir", 0o755, b""),
        b".claude": ("dir", 0o755, b""),
        b".claude/rules": ("link", 0, b"../.context/rules"),
        b"docs": ("dir", 0o755, b""),
        b"docs/a.md": ("file", 0o644, blob_oid(b"a")),
        b"run.sh": ("file", 0o755, blob_oid(b"run")),
    }


def test_archive_view_of_a_tar_keeps_directories_files_and_links() -> None:
    """The expected view of a tar holds the folders, the files and the two links."""
    view = ar.archive_view(expected_pack(), links=True)
    assert view == expected_pack()


def test_archive_view_of_a_zip_leaves_out_the_links_that_dangle() -> None:
    """The expected view of a zip leaves out the two links, which point outside the pack."""
    view = ar.archive_view(expected_pack(), links=False)
    assert b".claude/rules" not in view
    assert len(view) == len(expected_pack()) - 1
    assert view[b".claude"] == ("dir", 0o755, b"")


def test_check_archive_accepts_members_that_are_the_tagged_tree() -> None:
    """check_archive accepts an archive whose members are the tagged tree."""
    ar.check_archive("the tar", expected_pack(), dict(expected_pack()))


def test_check_archive_says_the_member_count_when_it_is_not_the_one_the_tree_implies() -> None:
    """A member count other than the tree implies is refused, and the reason gives the count."""
    actual = dict(expected_pack())
    del actual[b".claude/rules"]
    with pytest.raises(ar.Rejected) as info:
        ar.check_archive("the tar", expected_pack(), actual)
    assert "lists 5 members" in str(info.value)
    assert "implies 6" in str(info.value)


def test_check_archive_refuses_a_zip_that_holds_a_link() -> None:
    """check_archive refuses a zip archive that contains a symbolic link."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_archive("the zip", ar.archive_view(expected_pack(), links=False), expected_pack())
    assert "lists 6 members" in str(info.value)


def test_check_archive_refuses_a_member_with_other_content_even_when_the_count_is_right() -> None:
    """check_archive refuses a member with changed content even when the count matches."""
    actual = dict(expected_pack())
    actual[b"docs/a.md"] = ("file", 0o644, blob_oid(b"other"))
    with pytest.raises(ar.Rejected) as info:
        ar.check_archive("the tar", expected_pack(), actual)
    assert "not the tagged tree" in str(info.value)
    assert "docs/a.md" in str(info.value)


def test_check_archive_refuses_a_member_with_the_wrong_execute_bit() -> None:
    """check_archive refuses a member whose execute bit differs from the tree."""
    actual = dict(expected_pack())
    actual[b"run.sh"] = ("file", 0o644, blob_oid(b"run"))
    with pytest.raises(ar.Rejected):
        ar.check_archive("the tar", expected_pack(), actual)


def test_check_archive_refuses_a_swapped_name_when_the_count_is_right() -> None:
    """check_archive refuses swapped names even when the count matches."""
    actual = dict(expected_pack())
    actual[b"docs/b.md"] = actual.pop(b"docs/a.md")
    with pytest.raises(ar.Rejected):
        ar.check_archive("the tar", expected_pack(), actual)
