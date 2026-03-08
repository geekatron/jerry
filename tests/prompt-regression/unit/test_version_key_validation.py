# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for BaselineStore._validate_version_key() — CG-027.

Verifies that the VERSION_KEY_PATTERN regex and the surrounding validation
logic in _validate_version_key() correctly accepts well-formed keys and
rejects keys containing injection-enabling characters (newlines, null bytes)
or a structurally invalid git hash.

No filesystem I/O is performed. All tests call the static method directly.

References:
    - CG-027: VERSION_KEY_PATTERN regex for version key format validation
    - FR-004: Version key format "{git_commit_hash}:{file_path}"
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest

from jerry.testing.baselines.store import VERSION_KEY_PATTERN, BaselineStore


class TestVersionKeyValidation:
    """Unit tests for BaselineStore._validate_version_key() (CG-027).

    Each test targets a distinct input class: valid short SHA, valid full SHA,
    newline injection, null-byte injection, empty string, and missing colon.
    BDD-style names are used per H-20.
    """

    @pytest.mark.unit
    def test_valid_short_sha_with_path_should_be_accepted(self) -> None:
        """A 7-character hex SHA with a colon-separated path is a valid key.

        This is the minimum-length git short hash (7 hex chars). The validator
        must accept it without raising.
        """
        valid_key = "abc1234:path/to/file.py"

        # Should not raise
        BaselineStore._validate_version_key(valid_key)

    @pytest.mark.unit
    def test_valid_40char_sha_with_path_should_be_accepted(self) -> None:
        """A full 40-character hex SHA with a colon-separated path is a valid key.

        Full SHAs are used in FULL-mode baseline version keys to ensure
        uniqueness across long development histories.
        """
        full_sha = "a" * 40
        valid_key = f"{full_sha}:skills/ps-researcher.md"

        # Should not raise
        BaselineStore._validate_version_key(valid_key)

    @pytest.mark.unit
    def test_version_key_with_newline_should_raise_value_error(self) -> None:
        """A version key containing a newline character is rejected (log injection).

        Newlines in version keys can corrupt log records and break GHA output
        format (key=value\\n protocol). CG-027 enforces rejection.
        """
        key_with_newline = "abc1234:path/to/file.py\nINJECTED=evil"

        with pytest.raises(ValueError, match="CG-027"):
            BaselineStore._validate_version_key(key_with_newline)

    @pytest.mark.unit
    def test_version_key_with_null_byte_should_raise_value_error(self) -> None:
        """A version key containing a null byte is rejected (file path corruption).

        Null bytes in file paths cause silent truncation in C-based filesystem
        calls and can enable path confusion attacks. CG-027 enforces rejection.
        """
        key_with_null = "abc1234:path/to/file\x00.py"

        with pytest.raises(ValueError, match="CG-027"):
            BaselineStore._validate_version_key(key_with_null)

    @pytest.mark.unit
    def test_empty_string_should_raise_value_error(self) -> None:
        """An empty version key is rejected because it contains no colon separator.

        The colon structural check runs before the regex check; either path
        produces a ValueError.
        """
        with pytest.raises(ValueError):
            BaselineStore._validate_version_key("")

    @pytest.mark.unit
    def test_version_key_without_colon_should_raise_value_error(self) -> None:
        """A version key without the colon separator is rejected immediately.

        The structural colon-split check fires before the regex check,
        providing a clear error message about the missing separator.
        """
        with pytest.raises(ValueError):
            BaselineStore._validate_version_key("abc1234nocoilonhere")

    @pytest.mark.unit
    def test_version_key_with_uppercase_hex_should_raise_value_error(self) -> None:
        """A git hash containing uppercase hex characters is rejected (CG-027).

        Git hashes are always lowercase hexadecimal. Uppercase letters in the
        hash portion indicate a non-standard or fabricated key.
        """
        key_with_uppercase = "ABC1234:path/to/file.py"

        with pytest.raises(ValueError, match="CG-027"):
            BaselineStore._validate_version_key(key_with_uppercase)

    @pytest.mark.unit
    def test_version_key_with_carriage_return_should_raise_value_error(self) -> None:
        """A version key containing \\r is rejected (CG-027 newline injection).

        Carriage returns cause the same log injection risk as \\n and are
        explicitly covered by the [^\\n\\r\\0] character class.
        """
        key_with_cr = "abc1234:path/to/file.py\rINJECTED"

        with pytest.raises(ValueError, match="CG-027"):
            BaselineStore._validate_version_key(key_with_cr)

    @pytest.mark.unit
    def test_version_key_pattern_accepts_path_with_slashes_and_dots(self) -> None:
        """The VERSION_KEY_PATTERN regex accepts paths with slashes and dots.

        Agent definition paths such as 'skills/ps-researcher/agents/ps-researcher.md'
        are the primary use case. The regex must not reject forward slashes or dots.
        """
        key = "abc1234:skills/ps-researcher/agents/ps-researcher.md"

        assert VERSION_KEY_PATTERN.match(key) is not None

    @pytest.mark.unit
    def test_version_key_hash_too_short_should_raise_value_error(self) -> None:
        """A git hash shorter than 7 characters is rejected by CG-027.

        The minimum short hash length for git disambiguation is 7 characters.
        Shorter hashes are not valid git identifiers and are rejected.
        """
        short_hash_key = "abc12:path/to/file.py"

        with pytest.raises(ValueError, match="CG-027"):
            BaselineStore._validate_version_key(short_hash_key)
