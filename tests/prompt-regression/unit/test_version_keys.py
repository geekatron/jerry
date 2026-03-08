# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for tests/prompt-regression/version_keys.py — FR-004 Version Keys.

Tests the VersionKey, VersionKeyRegistry, EvaluationMode, and BaselineMetadata
security constructs that enforce FR-004 (version key composite format) and
prevent path traversal attacks (OWASP A03:2021 Injection).

All tests are deterministic. No git subprocess calls are made
(tests use pre-validated hash strings).

Security focus areas tested:
    - Full 40-char hash requirement (abbreviated hash rejection)
    - Path traversal prevention
    - Composite key format integrity
    - Minimum run count validation per evaluation mode

References:
    - CG-027: VERSION_KEY_PATTERN regex for version key format validation
    - FR-004: Version key composite format {commit_hash}:{file_path}
    - FR-004 AC-1..AC-3: Format, retrieval, and integrity constraints
    - OWASP A03:2021 Injection
    - ASVS V5.1 Input Validation
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest

# Import from the module under test (in tests/prompt-regression/).
# sys.path is configured by tests/prompt-regression/conftest.py.
from version_keys import (
    BaselineMismatchError,
    BaselineVersionRecord,
    EvaluationMode,
    VersionKey,
    VersionKeyError,
    VersionKeyRegistry,
    validate_baseline_version_key,
)

pytestmark = [pytest.mark.unit]

# ---------------------------------------------------------------------------
# Constants for testing
# ---------------------------------------------------------------------------

# A valid full 40-character SHA-1 hash
_VALID_HASH: str = "a" * 40

# A valid agent definition file path
_VALID_PATH: str = "skills/problem-solving/agents/ps-researcher.md"

# A valid composite key
_VALID_KEY_STR: str = f"{_VALID_HASH}:{_VALID_PATH}"


# ---------------------------------------------------------------------------
# EvaluationMode (local version in version_keys.py)
# ---------------------------------------------------------------------------


class TestEvaluationModeVersionKeys:
    """Verify EvaluationMode enum in version_keys.py matches the canonical definition (CG-027)."""

    def test_smoke_value_should_equal_smoke_string(self) -> None:
        """EvaluationMode.SMOKE should have value 'Smoke'."""
        assert EvaluationMode.SMOKE.value == "Smoke"

    def test_standard_value_should_equal_standard_string(self) -> None:
        """EvaluationMode.STANDARD should have value 'Standard'."""
        assert EvaluationMode.STANDARD.value == "Standard"

    def test_full_value_should_equal_full_string(self) -> None:
        """EvaluationMode.FULL should have value 'Full'."""
        assert EvaluationMode.FULL.value == "Full"

    def test_local_enum_members_should_match_canonical_types(self) -> None:
        """Local EvaluationMode enum members and values must exactly match jerry.testing.types.

        This cross-check prevents future drift between the standalone version_keys.py
        definition (used inside Docker where jerry package may not be installed) and
        the canonical jerry.testing.types.EvaluationMode.
        """
        from jerry.testing.types import EvaluationMode as CanonicalEvaluationMode

        # Verify member names are identical
        local_names = {m.name for m in EvaluationMode}
        canonical_names = {m.name for m in CanonicalEvaluationMode}
        assert local_names == canonical_names, (
            f"EvaluationMode member names differ between version_keys.py and "
            f"jerry.testing.types: local={local_names}, canonical={canonical_names}"
        )

        # Verify member values are identical
        for member in EvaluationMode:
            canonical_member = CanonicalEvaluationMode[member.name]
            assert member.value == canonical_member.value, (
                f"EvaluationMode.{member.name} value mismatch: "
                f"version_keys.py={member.value!r}, "
                f"jerry.testing.types={canonical_member.value!r}"
            )


# ---------------------------------------------------------------------------
# VersionKey construction
# ---------------------------------------------------------------------------


class TestVersionKeyValidConstruction:
    """VersionKey accepts well-formed inputs (FR-004, CG-027)."""

    def test_version_key_should_construct_with_valid_hash_and_path(self) -> None:
        """Full 40-char hash + valid path constructs without error."""
        key = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        assert key.commit_hash == _VALID_HASH
        assert key.file_path == _VALID_PATH

    def test_version_key_should_produce_correct_composite_format(self) -> None:
        """composite_key property (str()) should return '{hash}:{path}'."""
        key = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        assert str(key) == f"{_VALID_HASH}:{_VALID_PATH}"

    def test_version_key_should_round_trip_through_from_string(self) -> None:
        """from_string(str(key)) should produce an equivalent VersionKey."""
        original = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        reconstructed = VersionKey.from_string(str(original))
        assert reconstructed.commit_hash == original.commit_hash
        assert reconstructed.file_path == original.file_path

    def test_version_key_should_be_frozen(self) -> None:
        """VersionKey should be immutable (frozen dataclass)."""
        key = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        import dataclasses

        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            key.commit_hash = "b" * 40  # type: ignore[misc]

    def test_version_key_should_accept_uppercase_hex_characters(self) -> None:
        """Both upper and lowercase hex characters should be accepted."""
        upper_hash = "A" * 40
        key = VersionKey(commit_hash=upper_hash, file_path=_VALID_PATH)
        assert key.commit_hash == upper_hash

    def test_version_key_should_accept_different_agent_paths(self) -> None:
        """Paths for different agents in the allowlist should all be accepted."""
        valid_paths = [
            "skills/problem-solving/agents/ps-researcher.md",
            "skills/problem-solving/agents/ps-analyst.md",
            "skills/adversary/agents/adv-scorer.md",
        ]
        for path in valid_paths:
            key = VersionKey(commit_hash=_VALID_HASH, file_path=path)
            assert key.file_path == path


# ---------------------------------------------------------------------------
# Hash validation
# ---------------------------------------------------------------------------


class TestVersionKeyShortHashRejected:
    """VersionKey rejects abbreviated commit hashes to prevent key collisions (FR-004, CG-027)."""

    def test_version_key_should_reject_short_hash(self) -> None:
        """A 7-character hash (abbreviated) should raise VersionKeyError."""
        with pytest.raises(VersionKeyError) as exc_info:
            VersionKey(commit_hash="abc1234", file_path=_VALID_PATH)
        assert "40" in str(exc_info.value) or "abbreviated" in str(exc_info.value)

    def test_version_key_should_reject_39_char_hash(self) -> None:
        """39 characters (one too few) should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash="a" * 39, file_path=_VALID_PATH)

    def test_version_key_should_reject_41_char_hash(self) -> None:
        """41 characters (one too many) should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash="a" * 41, file_path=_VALID_PATH)

    def test_version_key_should_reject_empty_hash(self) -> None:
        """Empty commit hash should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash="", file_path=_VALID_PATH)

    def test_version_key_should_reject_non_hex_characters(self) -> None:
        """Non-hex characters in hash should raise VersionKeyError."""
        invalid_hash = "g" * 40  # 'g' is not a valid hex character
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash=invalid_hash, file_path=_VALID_PATH)


# ---------------------------------------------------------------------------
# Path traversal prevention (OWASP A03:2021)
# ---------------------------------------------------------------------------


class TestVersionKeyPathTraversalRejected:
    """VersionKey rejects path traversal attempts to prevent injection attacks (OWASP A03:2021)."""

    def test_version_key_should_reject_dotdot_path_traversal(self) -> None:
        """'../etc/passwd' path should raise VersionKeyError."""
        with pytest.raises(VersionKeyError) as exc_info:
            VersionKey(commit_hash=_VALID_HASH, file_path="../etc/passwd")
        assert "traversal" in str(exc_info.value).lower() or ".." in str(exc_info.value)

    def test_version_key_should_reject_absolute_path(self) -> None:
        """Absolute path (starting with '/') should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash=_VALID_HASH, file_path="/etc/passwd")

    def test_version_key_should_reject_path_outside_skills(self) -> None:
        """Path not matching 'skills/*/agents/*.md' should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash=_VALID_HASH, file_path="jerry/testing/stats.py")

    def test_version_key_should_reject_empty_path(self) -> None:
        """Empty file path should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(commit_hash=_VALID_HASH, file_path="")

    def test_version_key_should_reject_dotdot_in_middle_of_path(self) -> None:
        """Path with '..' in the middle should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey(
                commit_hash=_VALID_HASH,
                file_path="skills/../../../etc/passwd",
            )


# ---------------------------------------------------------------------------
# from_string() parsing
# ---------------------------------------------------------------------------


class TestVersionKeyFromString:
    """VersionKey.from_string() parses and validates the composite key format (FR-004, CG-027)."""

    def test_from_string_should_parse_valid_composite_key(self) -> None:
        """Valid composite key string should parse correctly."""
        key = VersionKey.from_string(_VALID_KEY_STR)
        assert key.commit_hash == _VALID_HASH
        assert key.file_path == _VALID_PATH

    def test_from_string_should_raise_for_missing_colon_separator(self) -> None:
        """String without ':' separator should raise VersionKeyError."""
        with pytest.raises(VersionKeyError):
            VersionKey.from_string("nocolonhere")

    def test_from_string_should_trim_surrounding_whitespace(self) -> None:
        """Surrounding whitespace should be stripped from hash and path."""
        key_str = f"  {_VALID_HASH}  :  {_VALID_PATH}  "
        key = VersionKey.from_string(key_str)
        assert key.commit_hash == _VALID_HASH
        assert key.file_path == _VALID_PATH


# ---------------------------------------------------------------------------
# BaselineVersionRecord.validate_minimum_runs()
# ---------------------------------------------------------------------------


class TestBaselineMetadataMinimumRuns:
    """BaselineVersionRecord.validate_minimum_runs() enforces mode-specific minimums (FR-004)."""

    def _make_record(
        self,
        mode: EvaluationMode,
        run_count: int,
    ) -> BaselineVersionRecord:
        key = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        return BaselineVersionRecord(
            version_key=key,
            evaluation_mode=mode,
            run_count=run_count,
            captured_at_iso="2026-03-01T12:00:00Z",
            model_id="claude-sonnet-4",
        )

    def test_smoke_mode_should_accept_minimum_one_run(self) -> None:
        """SMOKE mode requires run_count >= 1."""
        record = self._make_record(EvaluationMode.SMOKE, 1)
        record.validate_minimum_runs()  # Should not raise

    def test_smoke_mode_should_raise_for_zero_runs(self) -> None:
        """SMOKE mode with run_count=0 should raise VersionKeyError."""
        record = self._make_record(EvaluationMode.SMOKE, 0)
        with pytest.raises(VersionKeyError):
            record.validate_minimum_runs()

    def test_standard_mode_should_accept_minimum_ten_runs(self) -> None:
        """STANDARD mode requires run_count >= 10."""
        record = self._make_record(EvaluationMode.STANDARD, 10)
        record.validate_minimum_runs()  # Should not raise

    def test_standard_mode_should_raise_for_insufficient_runs(self) -> None:
        """STANDARD mode with run_count < 10 should raise VersionKeyError."""
        record = self._make_record(EvaluationMode.STANDARD, 9)
        with pytest.raises(VersionKeyError) as exc_info:
            record.validate_minimum_runs()
        assert "10" in str(exc_info.value)

    def test_full_mode_should_accept_minimum_thirty_runs(self) -> None:
        """FULL mode requires run_count >= 30."""
        record = self._make_record(EvaluationMode.FULL, 30)
        record.validate_minimum_runs()  # Should not raise

    def test_full_mode_should_raise_for_insufficient_runs(self) -> None:
        """FULL mode with run_count < 30 should raise VersionKeyError."""
        record = self._make_record(EvaluationMode.FULL, 29)
        with pytest.raises(VersionKeyError) as exc_info:
            record.validate_minimum_runs()
        assert "30" in str(exc_info.value)

    def test_full_mode_should_pass_at_exact_minimum(self) -> None:
        """FULL mode with exactly 30 runs should pass."""
        record = self._make_record(EvaluationMode.FULL, 30)
        record.validate_minimum_runs()  # Should not raise


# ---------------------------------------------------------------------------
# validate_baseline_version_key()
# ---------------------------------------------------------------------------


class TestValidateBaselineVersionKey:
    """validate_baseline_version_key() detects commit hash and path mismatches (FR-004)."""

    def test_matching_keys_should_not_raise(self) -> None:
        """Identical baseline and current keys should not raise."""
        key_a = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        key_b = VersionKey(commit_hash=_VALID_HASH, file_path=_VALID_PATH)
        validate_baseline_version_key(key_a, key_b)  # Should not raise

    def test_hash_mismatch_should_raise_baseline_mismatch_error(self) -> None:
        """Different commit hashes should raise BaselineMismatchError."""
        baseline_key = VersionKey(commit_hash="a" * 40, file_path=_VALID_PATH)
        current_key = VersionKey(commit_hash="b" * 40, file_path=_VALID_PATH)
        with pytest.raises(BaselineMismatchError) as exc_info:
            validate_baseline_version_key(baseline_key, current_key)
        assert "hash" in str(exc_info.value).lower() or "commit" in str(exc_info.value).lower()

    def test_path_mismatch_should_raise_baseline_mismatch_error(self) -> None:
        """Different file paths should raise BaselineMismatchError."""
        baseline_key = VersionKey(
            commit_hash=_VALID_HASH,
            file_path="skills/problem-solving/agents/ps-researcher.md",
        )
        current_key = VersionKey(
            commit_hash=_VALID_HASH,
            file_path="skills/problem-solving/agents/ps-analyst.md",
        )
        with pytest.raises(BaselineMismatchError):
            validate_baseline_version_key(baseline_key, current_key)


# ---------------------------------------------------------------------------
# VersionKeyRegistry
# ---------------------------------------------------------------------------


class TestVersionKeyRegistry:
    """Tests for VersionKeyRegistry covered agents and error cases (FR-004, CG-027)."""

    def test_registry_covered_agents_should_be_nonempty(self) -> None:
        """COVERED_AGENTS frozenset should be non-empty."""
        assert len(VersionKeyRegistry.COVERED_AGENTS) > 0

    def test_registry_should_include_ps_researcher_in_covered_agents(self) -> None:
        """ps-researcher should be in COVERED_AGENTS."""
        assert "ps-researcher" in VersionKeyRegistry.COVERED_AGENTS

    def test_registry_all_covered_agents_should_have_file_path_entries(self) -> None:
        """All COVERED_AGENTS should have entries in AGENT_FILE_PATHS."""
        for agent_id in VersionKeyRegistry.COVERED_AGENTS:
            assert agent_id in VersionKeyRegistry.AGENT_FILE_PATHS

    def test_registry_should_raise_for_unknown_agent(self) -> None:
        """get_version_key() with unknown agent_id should raise VersionKeyError."""
        registry = VersionKeyRegistry()
        with pytest.raises(VersionKeyError) as exc_info:
            registry.get_version_key("nonexistent-agent-xyz")
        assert "not in" in str(exc_info.value).lower() or "PROJ-036" in str(exc_info.value)

    def test_registry_invalidate_should_clear_all_cached_keys(self) -> None:
        """invalidate() with no argument should clear all cached keys."""
        registry = VersionKeyRegistry()
        # Manually populate cache
        registry._registry["ps-researcher"] = VersionKey(  # type: ignore[attr-defined]
            commit_hash=_VALID_HASH,
            file_path=_VALID_PATH,
        )
        registry.invalidate()
        assert len(registry._registry) == 0  # type: ignore[attr-defined]

    def test_registry_invalidate_should_remove_only_specified_agent(self) -> None:
        """invalidate(agent_id) should remove only that agent's key from cache."""
        registry = VersionKeyRegistry()
        registry._registry["ps-researcher"] = VersionKey(  # type: ignore[attr-defined]
            commit_hash=_VALID_HASH,
            file_path="skills/problem-solving/agents/ps-researcher.md",
        )
        registry._registry["ps-analyst"] = VersionKey(  # type: ignore[attr-defined]
            commit_hash=_VALID_HASH,
            file_path="skills/problem-solving/agents/ps-analyst.md",
        )
        registry.invalidate("ps-researcher")
        assert "ps-researcher" not in registry._registry  # type: ignore[attr-defined]
        assert "ps-analyst" in registry._registry  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# build_version_key() — mock-based non-git path tests
# ---------------------------------------------------------------------------


class TestBuildVersionKeyMocked:
    """Tests for build_version_key() using pre-validated hash strings (FR-004, OWASP A03:2021).

    These tests inject mock git subprocess responses to cover the non-git path
    (where git may be unavailable or the environment is CI-isolated).
    No real git subprocess calls are made.

    References:
        - FR-004: Version key composite format {commit_hash}:{file_path}
        - OWASP A03:2021 Injection — validated args only, no shell=True
    """

    def test_build_version_key_should_use_file_last_commit_hash(self, monkeypatch) -> None:
        """build_version_key() with use_file_last_commit=True injects pre-validated hash.

        Monkeypatches get_file_last_commit_hash to return a known hash,
        verifying the returned VersionKey has the correct composite format.
        """
        import version_keys

        pre_validated_hash = "c" * 40

        monkeypatch.setattr(
            version_keys,
            "get_file_last_commit_hash",
            lambda file_path, repo_root=None: pre_validated_hash,
        )

        key = version_keys.build_version_key(
            file_path=_VALID_PATH,
            use_file_last_commit=True,
        )

        assert isinstance(key, VersionKey)
        assert key.commit_hash == pre_validated_hash
        assert key.file_path == _VALID_PATH
        assert str(key) == f"{pre_validated_hash}:{_VALID_PATH}"

    def test_build_version_key_should_use_head_commit_when_specified(self, monkeypatch) -> None:
        """build_version_key() with use_file_last_commit=False injects HEAD hash.

        Monkeypatches get_current_commit_hash to return a known hash,
        verifying the returned VersionKey uses HEAD rather than file-last-commit.
        """
        import version_keys

        head_hash = "d" * 40

        monkeypatch.setattr(
            version_keys,
            "get_current_commit_hash",
            lambda file_path, repo_root=None: head_hash,
        )

        key = version_keys.build_version_key(
            file_path=_VALID_PATH,
            use_file_last_commit=False,
        )

        assert isinstance(key, VersionKey)
        assert key.commit_hash == head_hash
        assert key.file_path == _VALID_PATH
