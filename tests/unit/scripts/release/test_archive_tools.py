# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Archive tests: the real ``tar`` and ``zip``, real archives, real listings.

These build, list and read archives, so they are on by default on Linux only and
are skipped elsewhere. Set ``JERRY_RELEASE_ARCHIVE_TESTS=1`` to force them on
(a container, or a machine where archive work is allowed) and
``JERRY_RELEASE_ARCHIVE_TESTS=0`` to force them off. A skip says why, and shows
with ``pytest -rs``. When the switch is ``1``, a missing tool fails the test
instead of skipping it.

They are marked neither ``subprocess`` nor ``llm``: the pull request checks run
them on Linux, so a change of the runner image that changes ``tar`` or ``zip``
shows up there before it reaches a release.

What they pin that the other tests cannot:

- the archives that the real tools make from the pack hold the members that the
  tagged tree implies (the tar holds the two links, the zip holds neither);
- the two readers read what the real tools wrote;
- the real ``zip`` exits with status 0 although the two links dangle;
- long names and a name that is not ASCII survive in both archives;
- a whole run on the repository's own tree.
"""

from __future__ import annotations

import os
import stat
import subprocess
import sys
import tarfile
import zipfile
from collections.abc import Callable
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import (  # noqa: E402
    REPO_ROOT,
    STANDARD_EXECUTABLES,
    STANDARD_FILES,
    STANDARD_LINKS,
    VERSION,
)

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

TOP = f"jerry-plugin-{VERSION}"
KNOWN = {
    b".claude/patterns": b"../.context/patterns",
    b".claude/rules": b"../.context/rules",
}
RealRun = Callable[..., tuple[Path, Path, str, str]]


def packed_files() -> dict[str, str]:
    """Return the standard files that lie under the packed paths."""
    top = set(ar.PACKED_FILES) | set(ar.PACKED_DIRS)
    return {name: text for name, text in STANDARD_FILES.items() if name.split("/")[0] in top}


def directories_of(paths: list[str]) -> set[str]:
    """Return every directory that holds one of the paths."""
    found: set[str] = set()
    for path in paths:
        parts = path.split("/")
        for count in range(1, len(parts)):
            found.add("/".join(parts[:count]))
    return found


def run_release(
    repo: Path,
    environ: dict[str, str],
    sbom_dir: Path,
    out: Path,
    capsys: pytest.CaptureFixture[str],
) -> str:
    """Run the script once with the real tools and return what it printed."""
    capsys.readouterr()
    code = ar.main(
        [
            "--repo",
            str(repo),
            "--sbom-dir",
            str(sbom_dir),
            "--output-dir",
            str(out),
            "--work-dir",
            environ["RUNNER_TEMP"],
        ],
        environ,
    )
    printed = capsys.readouterr().out
    assert code == 0, printed
    return printed


@pytest.fixture
def real_run(
    archive_tools: dict[str, str],
    make_repo: Callable[..., tuple[Path, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
    run_environment: Callable[..., dict[str, str]],
    sbom_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> RealRun:
    """Return a function that makes a repository and runs a real release over it."""

    def run(
        files: dict[str, str] | None = None,
        *,
        name: str = "out",
        extra: dict[str, str] | None = None,
    ) -> tuple[Path, Path, str, str]:
        repo, commit = make_repo(files)
        make_tag(repo, f"v{VERSION}")
        set_origin_main(repo, commit)
        environ = run_environment(repo, commit, extra=extra)
        out = tmp_path / name
        printed = run_release(repo, environ, sbom_dir, out, capsys)
        return repo, out, commit, printed

    return run


def test_the_real_tools_make_archives_that_hold_the_members_the_tagged_tree_implies(
    real_run: RealRun,
) -> None:
    """The real tar and zip tools produce archives whose members match the tagged tree."""
    repo, out, commit, printed = real_run()
    names = sorted(packed_files())
    directories = directories_of(names)
    with tarfile.open(out / f"{TOP}.tar.gz", "r:gz") as tar:
        members = {member.name.rstrip("/"): member for member in tar.getmembers()}
        assert len(members) == 1 + len(directories) + len(names) + 2
        for name in names:
            member = members[f"{TOP}/{name}"]
            assert member.isreg()
            assert bool(member.mode & 0o100) == (name in STANDARD_EXECUTABLES)
            extracted = tar.extractfile(member)
            assert extracted is not None
            assert extracted.read() == (repo / name).read_bytes()
        for link, target in STANDARD_LINKS.items():
            assert members[f"{TOP}/{link}"].issym()
            assert members[f"{TOP}/{link}"].linkname == target
    with zipfile.ZipFile(out / f"{TOP}.zip") as archive:
        listed = {info.filename.rstrip("/") for info in archive.infolist()}
        assert len(listed) == 1 + len(directories) + len(names)
        assert not any(link in item for link in STANDARD_LINKS for item in listed)
        assert archive.testzip() is None
    assert f"Checked: tag v{VERSION}, commit {commit}, version {VERSION}" in printed


def test_the_readers_return_what_the_script_expects_of_each_real_archive(
    real_run: RealRun,
) -> None:
    """Reading back each real archive gives exactly the view the script expects."""
    repo, out, commit, _ = real_run()
    entries = ar.read_tree(repo, commit, ar.git_environment({"PATH": os.environ["PATH"]}))
    expected = ar.expected_tree(entries, KNOWN)
    assert ar.read_tar(out / f"{TOP}.tar.gz", TOP) == ar.archive_view(expected, links=True)
    assert ar.read_zip(out / f"{TOP}.zip", TOP) == ar.archive_view(expected, links=False)


def test_the_real_zip_exits_with_status_zero_although_the_two_links_dangle(
    archive_tools: dict[str, str], tmp_path: Path
) -> None:
    """The real zip succeeds although the two links point outside the packed files."""
    pack = tmp_path / "pack"
    top = pack / TOP
    (top / ".claude").mkdir(parents=True)
    (top / "README.md").write_text("readme\n", encoding="utf-8")
    os.symlink("../.context/rules", top / ".claude" / "rules")
    os.symlink("../.context/patterns", top / ".claude" / "patterns")
    out = tmp_path / "dist"
    out.mkdir()
    env = ar.packer_environment(dict(os.environ))
    ar.pack_archives(pack, TOP, out / "a.tar.gz", out / "a.zip", env)
    with zipfile.ZipFile(out / "a.zip") as archive:
        names = {info.filename for info in archive.infolist()}
    assert f"{TOP}/README.md" in names
    assert not any("rules" in name or "patterns" in name for name in names)
    with tarfile.open(out / "a.tar.gz", "r:gz") as tar:
        assert sum(1 for member in tar.getmembers() if member.issym()) == 2


def test_a_second_release_of_the_same_commit_lists_the_same_members(
    archive_tools: dict[str, str],
    make_repo: Callable[..., tuple[Path, str]],
    make_tag: Callable[..., str],
    set_origin_main: Callable[[Path, str], None],
    run_environment: Callable[..., dict[str, str]],
    sbom_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Two releases of one commit list identical archive members."""
    repo, commit = make_repo()
    make_tag(repo, f"v{VERSION}")
    set_origin_main(repo, commit)
    first = tmp_path / "first"
    second = tmp_path / "second"
    for out in (first, second):
        run_release(repo, run_environment(repo, commit), sbom_dir, out, capsys)
    assert ar.read_tar(first / f"{TOP}.tar.gz", TOP) == ar.read_tar(second / f"{TOP}.tar.gz", TOP)
    assert ar.read_zip(first / f"{TOP}.zip", TOP) == ar.read_zip(second / f"{TOP}.zip", TOP)


def test_long_names_and_a_name_that_is_not_ascii_survive_in_both_archives(
    real_run: RealRun,
) -> None:
    """Long names and a non-ASCII name come through both archives unchanged."""
    long_dir = "/".join(["d" * 40] * 3)
    en_dash = "docs/knowledge/Hexagonal Architecture – Comprehensive Guide.docx"
    files = {f"docs/{long_dir}/a-file-with-a-long-name.md": "long\n", en_dash: "dash\n"}
    # The hosted Ubuntu runner has a UTF-8 locale, and C.UTF-8 is the UTF-8 locale that every
    # Ubuntu has without extra packages. ``tar`` and ``zip`` get the locale of the run, so the
    # test has to give the run one: with none they would use the C locale, which is not the
    # case that matters here.
    _, out, _, _ = real_run(files, extra={"LANG": "C.UTF-8"})
    raw_name = f"{TOP}/{en_dash}".encode()
    with tarfile.open(out / f"{TOP}.tar.gz", "r:gz") as tar:
        assert raw_name in {os.fsencode(member.name) for member in tar.getmembers()}
        assert any(len(member.name) > 100 for member in tar.getmembers())
    with zipfile.ZipFile(out / f"{TOP}.zip") as archive:
        raw_names = {
            info.orig_filename.encode("utf-8" if info.flag_bits & 0x800 else "cp437")
            for info in archive.infolist()
        }
        assert raw_name in raw_names


def test_a_whole_run_on_the_repository_own_tree_makes_archives_that_match_its_head(
    archive_tools: dict[str, str],
    run_environment: Callable[..., dict[str, str]],
    git_in: Callable[..., str],
    sbom_dir: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A full check-only run on this repository's own tree makes archives that match its head."""
    if not (REPO_ROOT / ".git").exists():
        pytest.skip("this check needs a git work tree")
    commit = git_in(REPO_ROOT, "rev-parse", "HEAD")
    environ = run_environment(REPO_ROOT, commit, event="workflow_dispatch", tag=None)
    out = tmp_path / "dist"
    printed = run_release(REPO_ROOT, environ, sbom_dir, out, capsys)
    assert "Check only: the attestation and the release are skipped." in printed
    # Count what git holds under the packed paths, without the code under test.
    listing = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            commit,
            "--",
            *ar.PACKED_DIRS,
            *ar.PACKED_FILES,
        ],
        capture_output=True,
        env={"PATH": os.environ["PATH"], "HOME": environ["HOME"]},
        check=True,
    ).stdout
    records = [record for record in listing.split(b"\0") if record]
    paths = [record.split(b"\t", 1)[1].decode("utf-8", "surrogateescape") for record in records]
    links = sum(1 for record in records if record.startswith(b"120000"))
    directories = len(directories_of(paths))
    version = ar.check_version(REPO_ROOT, commit, None, ar.git_environment(environ))
    top = f"jerry-plugin-{version}"
    with tarfile.open(out / f"{top}.tar.gz", "r:gz") as tar:
        assert sum(1 for _ in tar) == 1 + directories + len(paths)
    with zipfile.ZipFile(out / f"{top}.zip") as archive:
        assert len(archive.infolist()) == 1 + directories + len(paths) - links


def test_the_readers_refuse_an_archive_that_holds_a_hard_link_or_a_name_outside_the_top(
    archive_tools: dict[str, str], tmp_path: Path
) -> None:
    """The archive readers refuse a hard link and any member outside the top folder."""
    tar_path = tmp_path / "bad.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        directory = tarfile.TarInfo(TOP)
        directory.type = tarfile.DIRTYPE
        directory.mode = 0o755
        tar.addfile(directory)
        link = tarfile.TarInfo(f"{TOP}/hard")
        link.type = tarfile.LNKTYPE
        link.linkname = f"{TOP}/other"
        tar.addfile(link)
    with pytest.raises(ar.Rejected):
        ar.read_tar(tar_path, TOP)
    zip_path = tmp_path / "bad.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("elsewhere/file.txt", "x")
    with pytest.raises(ar.Rejected):
        ar.read_zip(zip_path, TOP)


def test_the_zip_reader_refuses_a_member_that_is_a_symbolic_link(
    archive_tools: dict[str, str], tmp_path: Path
) -> None:
    """The zip reader refuses a member stored as a symbolic link."""
    zip_path = tmp_path / "link.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(f"{TOP}/", "")
        info = zipfile.ZipInfo(f"{TOP}/link")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, "target")
    with pytest.raises(ar.Rejected) as raised:
        ar.read_zip(zip_path, TOP)
    assert "symbolic link" in str(raised.value)


def test_the_readers_refuse_a_file_that_is_not_an_archive(
    archive_tools: dict[str, str], tmp_path: Path
) -> None:
    """The archive readers refuse a file that is not a tar or zip archive."""
    (tmp_path / "x.tar.gz").write_bytes(b"not a tar")
    (tmp_path / "x.zip").write_bytes(b"not a zip")
    with pytest.raises(ar.Rejected):
        ar.read_tar(tmp_path / "x.tar.gz", TOP)
    with pytest.raises(ar.Rejected):
        ar.read_zip(tmp_path / "x.zip", TOP)
