# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Contract tests for context_monitoring port/adapter compliance.

Verifies that concrete adapters satisfy their port protocol contracts
both structurally (isinstance) and behaviorally (correct return values,
invariants, error conditions):
    - ConfigThresholdAdapter satisfies IThresholdConfiguration
    - JsonlTranscriptReader satisfies ITranscriptReader
    - FilesystemCheckpointRepository satisfies ICheckpointRepository

Acceptance Criteria Coverage:
    - AC-FEAT001-002: Threshold configuration port contract
    - AC-FEAT001-001: Transcript reader port contract (token counting formula)
    - AC-FEAT001-004: Checkpoint repository port contract (save/load/acknowledge)

Port Coverage Note:
    StalenessDetector has no contract test because it is a concrete
    infrastructure adapter without a corresponding port protocol interface.
    It was designed as a direct dependency (not DI-injected) because
    staleness detection is infrastructure-specific with no alternative
    implementations. See integration test docstring for behavioral coverage.

References:
    - FEAT-001: Context Detection (EN-003, EN-004)
    - PROJ-004: Context Resilience
    - H-07/H-08: Hexagonal layer boundaries
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.context_monitoring.application.ports.checkpoint_repository import (
    ICheckpointRepository,
)
from src.context_monitoring.application.ports.threshold_configuration import (
    IThresholdConfiguration,
)
from src.context_monitoring.application.ports.transcript_reader import ITranscriptReader
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier
from src.context_monitoring.infrastructure.adapters.config_threshold_adapter import (
    ConfigThresholdAdapter,
)
from src.context_monitoring.infrastructure.adapters.filesystem_checkpoint_repository import (
    FilesystemCheckpointRepository,
)
from src.context_monitoring.infrastructure.adapters.jsonl_transcript_reader import (
    JsonlTranscriptReader,
)
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)

pytestmark = [
    pytest.mark.contract,
]


# =============================================================================
# IThresholdConfiguration Contract
# =============================================================================


class TestThresholdConfigurationContract:
    """Contract: ConfigThresholdAdapter satisfies IThresholdConfiguration protocol.

    References: FEAT-001 (EN-004), PROJ-004
    """

    @pytest.fixture()
    def adapter(self, tmp_path: Path) -> ConfigThresholdAdapter:
        """Create a ConfigThresholdAdapter for contract testing."""
        layered = LayeredConfigAdapter(
            env_prefix="JERRY_",
            root_config_path=tmp_path / "config.toml",
            defaults={
                "context_monitor.nominal_threshold": 0.55,
                "context_monitor.warning_threshold": 0.70,
                "context_monitor.critical_threshold": 0.80,
                "context_monitor.emergency_threshold": 0.88,
                "context_monitor.compaction_detection_threshold": 10000,
                "context_monitor.enabled": True,
            },
        )
        return ConfigThresholdAdapter(config=layered)

    def test_is_instance_of_protocol(self, adapter: ConfigThresholdAdapter) -> None:
        """ConfigThresholdAdapter satisfies IThresholdConfiguration protocol."""
        assert isinstance(adapter, IThresholdConfiguration)

    def test_get_threshold_returns_float(self, adapter: ConfigThresholdAdapter) -> None:
        """get_threshold returns a float value."""
        result = adapter.get_threshold("warning")
        assert isinstance(result, float)

    def test_get_threshold_accepts_all_tiers(self, adapter: ConfigThresholdAdapter) -> None:
        """get_threshold accepts all valid tier names and returns values in [0, 1]."""
        for tier in ("nominal", "warning", "critical", "emergency"):
            result = adapter.get_threshold(tier)
            assert 0.0 <= result <= 1.0, f"Threshold for {tier} must be in [0.0, 1.0], got {result}"

    def test_is_enabled_returns_bool(self, adapter: ConfigThresholdAdapter) -> None:
        """is_enabled returns a boolean."""
        assert isinstance(adapter.is_enabled(), bool)

    def test_get_compaction_detection_threshold_returns_int(
        self, adapter: ConfigThresholdAdapter
    ) -> None:
        """get_compaction_detection_threshold returns a positive integer."""
        result = adapter.get_compaction_detection_threshold()
        assert isinstance(result, int)
        assert result > 0

    def test_get_all_thresholds_returns_dict(self, adapter: ConfigThresholdAdapter) -> None:
        """get_all_thresholds returns dict with all 4 tier keys."""
        result = adapter.get_all_thresholds()
        assert isinstance(result, dict)
        assert set(result.keys()) == {"nominal", "warning", "critical", "emergency"}

    def test_get_context_window_tokens_returns_positive_int(
        self, adapter: ConfigThresholdAdapter
    ) -> None:
        """get_context_window_tokens returns a positive integer."""
        result = adapter.get_context_window_tokens()
        assert isinstance(result, int)
        assert result > 0

    def test_get_context_window_source_returns_string(
        self, adapter: ConfigThresholdAdapter
    ) -> None:
        """get_context_window_source returns a non-empty string."""
        result = adapter.get_context_window_source()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_thresholds_are_monotonically_increasing(self, adapter: ConfigThresholdAdapter) -> None:
        """Threshold values must be monotonically increasing: nominal < warning < critical < emergency."""
        thresholds = adapter.get_all_thresholds()
        assert thresholds["nominal"] < thresholds["warning"], (
            f"nominal ({thresholds['nominal']}) must be < warning ({thresholds['warning']})"
        )
        assert thresholds["warning"] < thresholds["critical"], (
            f"warning ({thresholds['warning']}) must be < critical ({thresholds['critical']})"
        )
        assert thresholds["critical"] < thresholds["emergency"], (
            f"critical ({thresholds['critical']}) must be < emergency ({thresholds['emergency']})"
        )

    def test_get_threshold_returns_values_in_valid_range(
        self, adapter: ConfigThresholdAdapter
    ) -> None:
        """All thresholds fall within the valid operational range [0.3, 0.99].

        This is a behavioral invariant for any conforming implementation:
        thresholds outside this range indicate misconfiguration that would
        break tier classification logic.
        """
        thresholds = adapter.get_all_thresholds()
        for tier, value in thresholds.items():
            assert 0.3 <= value <= 0.99, (
                f"Threshold {tier} ({value}) outside valid range [0.3, 0.99]"
            )


# =============================================================================
# ITranscriptReader Contract
# =============================================================================


class TestTranscriptReaderContract:
    """Contract: JsonlTranscriptReader satisfies ITranscriptReader protocol.

    References: FEAT-001 (EN-003), PROJ-004
    """

    @pytest.fixture()
    def reader(self) -> JsonlTranscriptReader:
        """Create a JsonlTranscriptReader for contract testing."""
        return JsonlTranscriptReader()

    def test_is_instance_of_protocol(self, reader: JsonlTranscriptReader) -> None:
        """JsonlTranscriptReader satisfies ITranscriptReader protocol."""
        assert isinstance(reader, ITranscriptReader)

    def test_read_latest_tokens_returns_int(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """read_latest_tokens returns an integer for valid transcript."""
        transcript = tmp_path / "t.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {"input_tokens": 50000},
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")
        result = reader.read_latest_tokens(str(transcript))
        assert isinstance(result, int)
        assert result == 50000

    def test_read_latest_tokens_raises_on_missing_file(self, reader: JsonlTranscriptReader) -> None:
        """read_latest_tokens raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            reader.read_latest_tokens("/nonexistent/file.jsonl")

    def test_read_latest_tokens_raises_on_empty_file(
        self, reader: JsonlTranscriptReader, tmp_path: Path
    ) -> None:
        """read_latest_tokens raises ValueError for empty files."""
        empty = tmp_path / "empty.jsonl"
        empty.write_text("")
        with pytest.raises(ValueError):
            reader.read_latest_tokens(str(empty))

    def test_cumulative_token_formula(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """Token count includes input_tokens + cache_creation + cache_read.

        Verifies the documented cumulative formula from the ITranscriptReader
        protocol specification.
        """
        transcript = tmp_path / "cache.jsonl"
        entry = {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "usage": {
                    "input_tokens": 100_000,
                    "cache_creation_input_tokens": 25_000,
                    "cache_read_input_tokens": 15_000,
                },
            },
        }
        transcript.write_text(json.dumps(entry) + "\n")
        result = reader.read_latest_tokens(str(transcript))
        assert result == 140_000, f"Expected 100000+25000+15000=140000, got {result}"

    def test_uses_last_assistant_entry(self, reader: JsonlTranscriptReader, tmp_path: Path) -> None:
        """Multiple entries: returns token count from the last assistant entry."""
        transcript = tmp_path / "multi.jsonl"
        entries = [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "usage": {"input_tokens": 10_000}},
                }
            ),
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"role": "assistant", "usage": {"input_tokens": 90_000}},
                }
            ),
        ]
        transcript.write_text("\n".join(entries) + "\n")
        result = reader.read_latest_tokens(str(transcript))
        assert result == 90_000


# =============================================================================
# ICheckpointRepository Contract
# =============================================================================


class TestCheckpointRepositoryContract:
    """Contract: FilesystemCheckpointRepository satisfies ICheckpointRepository.

    References: FEAT-001 (EN-003), PROJ-004
    """

    @pytest.fixture()
    def repo(self, tmp_path: Path) -> FilesystemCheckpointRepository:
        """Create a FilesystemCheckpointRepository for contract testing.

        Lock directory is scoped to tmp_path for test isolation.
        """
        return FilesystemCheckpointRepository(
            checkpoint_dir=tmp_path / "checkpoints",
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )

    def _make_checkpoint(
        self,
        checkpoint_id: str,
        monitoring_ok: bool = True,
        context_window: int = 200_000,
        context_window_source: str = "default",
    ) -> CheckpointData:
        """Create a test CheckpointData with all FillEstimate fields."""
        return CheckpointData(
            checkpoint_id=checkpoint_id,
            context_state=FillEstimate(
                fill_percentage=0.72,
                tier=ThresholdTier.WARNING,
                token_count=144_000,
                monitoring_ok=monitoring_ok,
                context_window=context_window,
                context_window_source=context_window_source,
            ),
            created_at="2026-02-20T12:00:00+00:00",
        )

    def test_is_instance_of_protocol(self, repo: FilesystemCheckpointRepository) -> None:
        """FilesystemCheckpointRepository satisfies ICheckpointRepository protocol."""
        assert isinstance(repo, ICheckpointRepository)

    def test_save_does_not_raise(self, repo: FilesystemCheckpointRepository) -> None:
        """save() accepts a CheckpointData without raising."""
        checkpoint = self._make_checkpoint("cx-001")
        repo.save(checkpoint)

    def test_get_latest_unacknowledged_returns_optional(
        self, repo: FilesystemCheckpointRepository
    ) -> None:
        """get_latest_unacknowledged returns None when empty."""
        result = repo.get_latest_unacknowledged()
        assert result is None

    def test_get_latest_unacknowledged_returns_checkpoint_data(
        self, repo: FilesystemCheckpointRepository
    ) -> None:
        """get_latest_unacknowledged returns CheckpointData after save."""
        checkpoint = self._make_checkpoint("cx-001")
        repo.save(checkpoint)
        result = repo.get_latest_unacknowledged()
        assert isinstance(result, CheckpointData)

    def test_save_load_roundtrip_preserves_all_fields(
        self, repo: FilesystemCheckpointRepository
    ) -> None:
        """save→load roundtrip preserves all FillEstimate fields including new ones."""
        original = self._make_checkpoint(
            "cx-001",
            monitoring_ok=False,
            context_window=500_000,
            context_window_source="env",
        )
        repo.save(original)
        loaded = repo.get_latest_unacknowledged()

        assert loaded is not None
        assert loaded.checkpoint_id == "cx-001"
        assert loaded.context_state.fill_percentage == pytest.approx(0.72)
        assert loaded.context_state.tier == ThresholdTier.WARNING
        assert loaded.context_state.token_count == 144_000
        assert loaded.context_state.monitoring_ok is False
        assert loaded.context_state.context_window == 500_000
        assert loaded.context_state.context_window_source == "env"

    def test_acknowledge_marks_checkpoint(self, repo: FilesystemCheckpointRepository) -> None:
        """acknowledge() causes checkpoint to not appear in get_latest_unacknowledged."""
        checkpoint = self._make_checkpoint("cx-001")
        repo.save(checkpoint)
        repo.acknowledge("cx-001")
        assert repo.get_latest_unacknowledged() is None

    def test_list_all_returns_list(self, repo: FilesystemCheckpointRepository) -> None:
        """list_all() returns a list of CheckpointData."""
        result = repo.list_all()
        assert isinstance(result, list)

    def test_list_all_includes_acknowledged(self, repo: FilesystemCheckpointRepository) -> None:
        """list_all() includes both acknowledged and unacknowledged checkpoints."""
        repo.save(self._make_checkpoint("cx-001"))
        repo.save(self._make_checkpoint("cx-002"))
        repo.acknowledge("cx-001")

        all_checkpoints = repo.list_all()
        assert len(all_checkpoints) == 2
        ids = [c.checkpoint_id for c in all_checkpoints]
        assert "cx-001" in ids
        assert "cx-002" in ids

    def test_next_checkpoint_id_returns_string(self, repo: FilesystemCheckpointRepository) -> None:
        """next_checkpoint_id() returns a string starting with 'cx-'."""
        result = repo.next_checkpoint_id()
        assert isinstance(result, str)
        assert result.startswith("cx-")

    def test_next_checkpoint_id_sequential(self, repo: FilesystemCheckpointRepository) -> None:
        """Sequential checkpoint IDs increment correctly."""
        id1 = repo.next_checkpoint_id()
        repo.save(self._make_checkpoint(id1))
        id2 = repo.next_checkpoint_id()
        repo.save(self._make_checkpoint(id2))
        id3 = repo.next_checkpoint_id()

        assert id1 == "cx-001"
        assert id2 == "cx-002"
        assert id3 == "cx-003"
