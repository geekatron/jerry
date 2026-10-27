# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the checksums and for the check of the output directory.

The output directory ends with exactly four regular files: the tar.gz, the zip,
``checksums.sha256`` in the two-line form that ``sha256sum`` writes, and the
software bill of materials (SBOM). The final check reads them back from disk, so
it judges what the later steps will attest and publish.
"""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import SBOM_TEXT  # noqa: E402

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

TAR = "jerry-plugin-0.31.9.tar.gz"
ZIP = "jerry-plugin-0.31.9.zip"
SBOM = "sbom.cyclonedx.json"
CHECKSUMS = "checksums.sha256"


def sha256_hex(data: bytes) -> str:
    """Return the SHA-256 digest of ``data`` as lowercase hex."""
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Make an output directory that holds the four files, as a run leaves it."""
    out = tmp_path / "dist"
    out.mkdir()
    (out / TAR).write_bytes(b"tar bytes")
    (out / ZIP).write_bytes(b"zip bytes")
    (out / SBOM).write_text(SBOM_TEXT, encoding="utf-8")
    ar.write_checksums(out, [TAR, ZIP])
    return out


# --- sha256_file ------------------------------------------------------------------------------


def test_sha256_file_gives_the_known_digest_of_abc(tmp_path: Path) -> None:
    """sha256_file returns the published SHA-256 digest of the text abc."""
    (tmp_path / "abc").write_bytes(b"abc")
    assert (
        ar.sha256_file(tmp_path / "abc")
        == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_file_reads_a_file_larger_than_one_chunk(tmp_path: Path) -> None:
    """sha256_file gives the right digest for a file larger than its read chunk."""
    data = os.urandom(3 * 1024 * 1024 + 17)
    (tmp_path / "big").write_bytes(data)
    assert ar.sha256_file(tmp_path / "big") == sha256_hex(data)


# --- write_checksums ------------------------------------------------------------------------------


def test_write_checksums_writes_two_lines_in_the_form_that_sha256sum_writes(tmp_path: Path) -> None:
    """write_checksums writes one line per archive, in the format that sha256sum uses."""
    (tmp_path / TAR).write_bytes(b"tar bytes")
    (tmp_path / ZIP).write_bytes(b"zip bytes")
    text = ar.write_checksums(tmp_path, [TAR, ZIP])
    expected = f"{sha256_hex(b'tar bytes')}  {TAR}\n{sha256_hex(b'zip bytes')}  {ZIP}\n"
    assert text == expected
    assert (tmp_path / CHECKSUMS).read_bytes() == expected.encode()


def test_write_checksums_gives_the_same_length_as_the_real_file_at_these_names(
    tmp_path: Path,
) -> None:
    """The checksums file for these names is 183 bytes, the size of the released file."""
    (tmp_path / TAR).write_bytes(b"a")
    (tmp_path / ZIP).write_bytes(b"b")
    ar.write_checksums(tmp_path, [TAR, ZIP])
    assert (tmp_path / CHECKSUMS).stat().st_size == 183


def test_write_checksums_makes_a_file_that_everyone_may_read(tmp_path: Path) -> None:
    """write_checksums leaves the file readable by everyone (mode 644)."""
    (tmp_path / TAR).write_bytes(b"a")
    (tmp_path / ZIP).write_bytes(b"b")
    ar.write_checksums(tmp_path, [TAR, ZIP])
    assert stat.S_IMODE((tmp_path / CHECKSUMS).stat().st_mode) == 0o644


def test_write_checksums_refuses_to_replace_a_file_that_exists(tmp_path: Path) -> None:
    """write_checksums refuses to overwrite an existing file."""
    (tmp_path / TAR).write_bytes(b"a")
    (tmp_path / ZIP).write_bytes(b"b")
    (tmp_path / CHECKSUMS).write_text("old", encoding="utf-8")
    with pytest.raises(ar.Rejected):
        ar.write_checksums(tmp_path, [TAR, ZIP])


# --- check_output_directory --------------------------------------------------------------------------


def test_check_output_directory_accepts_the_four_files(output_dir: Path) -> None:
    """check_output_directory accepts a folder holding exactly the four release files."""
    ar.check_output_directory(output_dir, TAR, ZIP)


@pytest.mark.parametrize("name", [TAR, ZIP, SBOM, CHECKSUMS])
def test_check_output_directory_refuses_a_missing_file(output_dir: Path, name: str) -> None:
    """check_output_directory refuses a folder that lacks one of the four files."""
    (output_dir / name).unlink()
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "exactly" in str(info.value)


@pytest.mark.parametrize(
    "extra", ["stray.txt", ".hidden", "jerry-plugin-0.31.9.zip.bak", "other.tar.gz"]
)
def test_check_output_directory_refuses_an_extra_file(output_dir: Path, extra: str) -> None:
    """check_output_directory refuses a folder with a fifth file."""
    (output_dir / extra).write_text("x", encoding="utf-8")
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "exactly" in str(info.value)


def test_check_output_directory_refuses_a_subdirectory(output_dir: Path) -> None:
    """check_output_directory refuses a subfolder in the output folder."""
    (output_dir / "sub").mkdir()
    with pytest.raises(ar.Rejected):
        ar.check_output_directory(output_dir, TAR, ZIP)


@pytest.mark.parametrize("name", [TAR, ZIP, SBOM, CHECKSUMS])
def test_check_output_directory_refuses_a_link_in_place_of_a_file(
    output_dir: Path, tmp_path: Path, name: str
) -> None:
    """check_output_directory refuses a symbolic link standing in for one of the files."""
    real = tmp_path / "real-file"
    real.write_bytes((output_dir / name).read_bytes())
    (output_dir / name).unlink()
    os.symlink(real, output_dir / name)
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "not a regular file" in str(info.value)


def test_check_output_directory_refuses_a_directory_that_is_a_link(
    output_dir: Path, tmp_path: Path
) -> None:
    """check_output_directory refuses an output folder that is a symbolic link."""
    link = tmp_path / "dist-link"
    os.symlink(output_dir, link)
    with pytest.raises(ar.Rejected):
        ar.check_output_directory(link, TAR, ZIP)


@pytest.mark.parametrize("name", [TAR, ZIP])
def test_check_output_directory_refuses_an_empty_archive(output_dir: Path, name: str) -> None:
    """check_output_directory refuses an archive of zero bytes."""
    (output_dir / name).write_bytes(b"")
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "outside the allowed" in str(info.value)


def test_check_output_directory_refuses_an_archive_above_the_size_bound(
    output_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """check_output_directory refuses an archive larger than the size limit."""
    monkeypatch.setattr(ar, "MAX_ARCHIVE_BYTES", 5)
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "outside the allowed" in str(info.value)


def test_check_output_directory_refuses_a_checksum_file_above_the_size_bound(
    output_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """check_output_directory refuses a checksums file larger than its size limit."""
    monkeypatch.setattr(ar, "MAX_CHECKSUMS_BYTES", 50)
    with pytest.raises(ar.Rejected):
        ar.check_output_directory(output_dir, TAR, ZIP)


def test_check_output_directory_refuses_an_sbom_above_the_size_bound(
    output_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """check_output_directory refuses an SBOM larger than its size limit."""
    monkeypatch.setattr(ar, "MAX_SBOM_BYTES", 10)
    with pytest.raises(ar.Rejected):
        ar.check_output_directory(output_dir, TAR, ZIP)


def test_check_output_directory_judges_the_sbom_on_disk_as_it_judged_the_download(
    output_dir: Path,
) -> None:
    """check_output_directory judges the SBOM on disk by the same checks as the download."""
    (output_dir / SBOM).write_text("not json", encoding="utf-8")
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "not valid JSON" in str(info.value)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "not checksums\n",
        f"{'0' * 64}  {TAR}\n{'0' * 64}  {ZIP}\n",
        f"{sha256_hex(b'tar bytes')}  {TAR}\n",
        f"{sha256_hex(b'zip bytes')}  {ZIP}\n{sha256_hex(b'tar bytes')}  {TAR}\n",
        f"{sha256_hex(b'tar bytes')} {TAR}\n{sha256_hex(b'zip bytes')} {ZIP}\n",
        f"{sha256_hex(b'tar bytes')}  {TAR}\n{sha256_hex(b'zip bytes')}  {ZIP}",
        f"{sha256_hex(b'tar bytes')}  {TAR}\n{sha256_hex(b'zip bytes')}  {ZIP}\n\n",
        f"{sha256_hex(b'tar bytes').upper()}  {TAR}\n{sha256_hex(b'zip bytes').upper()}  {ZIP}\n",
    ],
)
def test_check_output_directory_refuses_checksums_that_are_not_those_of_the_two_archives(
    output_dir: Path, text: str
) -> None:
    """check_output_directory refuses checksums that do not match the two archives."""
    (output_dir / CHECKSUMS).write_text(text, encoding="utf-8")
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "checksums.sha256" in str(info.value)


def test_check_output_directory_notices_an_archive_that_changed_after_the_checksums(
    output_dir: Path,
) -> None:
    """check_output_directory catches an archive changed after its checksum was written."""
    (output_dir / ZIP).write_bytes(b"zip bytes, changed")
    with pytest.raises(ar.Rejected) as info:
        ar.check_output_directory(output_dir, TAR, ZIP)
    assert "checksums.sha256" in str(info.value)
