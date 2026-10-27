# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the checks on the software bill of materials (SBOM).

The SBOM is the one file that crosses from the ``build`` job. It is attested as
it is, so the script checks only what it can: that the download holds exactly
one regular file, within a size bound, with no NUL (zero) byte, and that the
file is valid JSON (JavaScript Object Notation) with the shape of a CycloneDX
bill of materials. What the SBOM says about the dependencies is not checked.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from release_test_support import SBOM_TEXT  # noqa: E402

from scripts.release import assemble_release as ar  # noqa: E402

pytestmark = pytest.mark.unit

MINIMAL = b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": []}'


# --- read_sbom: the download directory ----------------------------------------------


def test_read_sbom_returns_the_bytes_of_the_one_file(sbom_dir: Path) -> None:
    """With exactly one SBOM file in the folder, read_sbom returns its bytes unchanged."""
    assert ar.read_sbom(sbom_dir) == SBOM_TEXT.encode()


def test_read_sbom_rejects_a_directory_that_does_not_exist(tmp_path: Path) -> None:
    """read_sbom refuses a folder that does not exist."""
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(tmp_path / "missing")
    assert "SBOM directory" in str(info.value)


def test_read_sbom_rejects_a_directory_that_is_a_link(sbom_dir: Path, tmp_path: Path) -> None:
    """read_sbom refuses a folder that is a symbolic link."""
    link = tmp_path / "link-to-sbom"
    os.symlink(sbom_dir, link)
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(link)
    assert "not a directory" in str(info.value)


def test_read_sbom_rejects_an_empty_directory(tmp_path: Path) -> None:
    """read_sbom refuses an empty folder."""
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(empty)
    assert "exactly the one file" in str(info.value)


@pytest.mark.parametrize("extra", ["other.json", ".hidden", "sbom.cyclonedx.json.bak"])
def test_read_sbom_rejects_a_second_file_of_any_name(sbom_dir: Path, extra: str) -> None:
    """read_sbom refuses a folder that holds a second file, whatever its name."""
    (sbom_dir / extra).write_text("{}", encoding="utf-8")
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(sbom_dir)
    assert "exactly the one file" in str(info.value)


def test_read_sbom_rejects_a_subdirectory_next_to_the_file(sbom_dir: Path) -> None:
    """read_sbom refuses a subfolder beside the SBOM file."""
    (sbom_dir / "sub").mkdir()
    with pytest.raises(ar.Rejected):
        ar.read_sbom(sbom_dir)


def test_read_sbom_rejects_a_file_with_another_name(tmp_path: Path) -> None:
    """read_sbom refuses a lone file that does not carry the expected name."""
    folder = tmp_path / "wrong-name"
    folder.mkdir()
    (folder / "bom.json").write_bytes(MINIMAL)
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(folder)
    assert "exactly the one file" in str(info.value)


def test_read_sbom_rejects_a_link_in_place_of_the_file(tmp_path: Path) -> None:
    """read_sbom refuses a symbolic link standing where the file should be."""
    folder = tmp_path / "with-link"
    folder.mkdir()
    real = tmp_path / "elsewhere.json"
    real.write_bytes(MINIMAL)
    os.symlink(real, folder / "sbom.cyclonedx.json")
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(folder)
    assert "not a regular file" in str(info.value)


def test_read_sbom_rejects_an_empty_file(tmp_path: Path) -> None:
    """read_sbom refuses an SBOM file with no content."""
    folder = tmp_path / "zero"
    folder.mkdir()
    (folder / "sbom.cyclonedx.json").write_bytes(b"")
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(folder)
    assert "bytes" in str(info.value)


def test_read_sbom_rejects_a_file_above_the_size_bound(
    sbom_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """read_sbom refuses a file larger than the size limit."""
    monkeypatch.setattr(ar, "MAX_SBOM_BYTES", len(SBOM_TEXT) - 1)
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(sbom_dir)
    assert "outside the allowed" in str(info.value)


def test_read_sbom_accepts_a_file_exactly_at_the_size_bound(
    sbom_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """read_sbom accepts a file whose size equals the limit."""
    monkeypatch.setattr(ar, "MAX_SBOM_BYTES", len(SBOM_TEXT))
    assert ar.read_sbom(sbom_dir) == SBOM_TEXT.encode()


def test_read_sbom_rejects_a_file_that_is_not_a_bill_of_materials(tmp_path: Path) -> None:
    """read_sbom refuses a file whose content is not a bill of materials."""
    folder = tmp_path / "text"
    folder.mkdir()
    (folder / "sbom.cyclonedx.json").write_bytes(b"not json at all")
    with pytest.raises(ar.Rejected) as info:
        ar.read_sbom(folder)
    assert "not valid JSON" in str(info.value)


# --- check_sbom_document -----------------------------------------------------------


def test_check_sbom_document_accepts_the_shape_of_a_cyclonedx_file() -> None:
    """check_sbom_document accepts a document with the CycloneDX shape."""
    ar.check_sbom_document(MINIMAL)
    ar.check_sbom_document(SBOM_TEXT.encode())


@pytest.mark.parametrize("spec", ["1.0", "1.6", "1.10", "1.99"])
def test_check_sbom_document_accepts_any_one_dot_number_spec_version(spec: str) -> None:
    """check_sbom_document accepts any spec version of the form 1.N."""
    ar.check_sbom_document(
        f'{{"bomFormat": "CycloneDX", "specVersion": "{spec}", "components": []}}'.encode()
    )


@pytest.mark.parametrize(
    ("data", "reason"),
    [
        (b"[]", "not a JSON object"),
        (b'"text"', "not a JSON object"),
        (b"null", "not a JSON object"),
        (b'{"specVersion": "1.6", "components": []}', "bomFormat"),
        (b'{"bomFormat": "SPDX", "specVersion": "1.6", "components": []}', "bomFormat"),
        (b'{"bomFormat": ["CycloneDX"], "specVersion": "1.6", "components": []}', "bomFormat"),
        (b'{"bomFormat": "CycloneDX", "components": []}', "specVersion"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "2.0", "components": []}', "specVersion"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "1", "components": []}', "specVersion"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "1.x", "components": []}', "specVersion"),
        (b'{"bomFormat": "CycloneDX", "specVersion": 1.6, "components": []}', "specVersion"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "1.6"}', "components"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": {}}', "components"),
        (b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": "x"}', "components"),
    ],
)
def test_check_sbom_document_rejects_a_shape_that_is_not_cyclonedx(
    data: bytes, reason: str
) -> None:
    """check_sbom_document refuses a JSON document that is not CycloneDX."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_sbom_document(data)
    assert reason in str(info.value)


@pytest.mark.parametrize(
    ("data", "reason"),
    [
        (b"", "not valid JSON"),
        (b"{", "not valid JSON"),
        (MINIMAL + b" trailing", "not valid JSON"),
        (b"\xef\xbb\xbf" + MINIMAL, "not valid JSON"),
        (
            b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": [], "x": NaN}',
            "not valid JSON",
        ),
        (
            b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": [Infinity]}',
            "not valid JSON",
        ),
        (
            b'{"bomFormat": "CycloneDX", "bomFormat": "CycloneDX", "specVersion": "1.6", "components": []}',
            "not valid JSON",
        ),
        (
            b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": [{"a": 1, "a": 2}]}',
            "not valid JSON",
        ),
        (b"\xff\xfe{}", "UTF-8"),
        (b'{"bomFormat": "CycloneDX"}\x00', "NUL"),
        (b'{"bomFormat": "Cyclone\x00DX"}', "NUL"),
    ],
)
def test_check_sbom_document_rejects_text_that_is_not_plain_valid_json(
    data: bytes, reason: str
) -> None:
    """check_sbom_document refuses text that is not plain, valid JSON."""
    with pytest.raises(ar.Rejected) as info:
        ar.check_sbom_document(data)
    assert reason in str(info.value)


def test_check_sbom_document_rejects_nesting_so_deep_that_the_parser_gives_up() -> None:
    """check_sbom_document turns JSON nested too deeply to parse into a refusal, not a crash."""
    depth = 200_000
    data = (
        b'{"bomFormat": "CycloneDX", "specVersion": "1.6", "components": '
        + b"[" * depth
        + b"]" * depth
        + b"}"
    )
    with pytest.raises(ar.Rejected) as info:
        ar.check_sbom_document(data)
    assert "not valid JSON" in str(info.value)
