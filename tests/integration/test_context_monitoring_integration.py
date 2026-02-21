# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for context_monitoring bounded context.

Tests verify real component wiring without mocks:
    - ConfigThresholdAdapter + real LayeredConfigAdapter
    - ContextFillEstimator + real JsonlTranscriptReader with JSONL files
    - Checkpoint create → persist → retrieve roundtrip (all FillEstimate fields)
    - ResumptionContextGenerator with real checkpoints
    - StalenessDetector with real YAML files
    - Fail-open recovery (fail → succeed on next call)

Test Distribution:
    - Happy Path (60%): 18 tests
    - Negative (30%): 8 tests
    - Edge (10%): 4 tests

Acceptance Criteria Coverage:
    - AC-FEAT001-001: Context fill estimation from transcript (token counting)
    - AC-FEAT001-002: Tier classification against configurable thresholds
    - AC-FEAT001-003: XML context-monitor tag generation
    - AC-FEAT001-004: Checkpoint create/persist/retrieve lifecycle
    - AC-FEAT001-005: Fail-open on error (monitoring_ok=False, NOMINAL)
    - AC-FEAT001-006: Resumption context generation from checkpoint
    - AC-FEAT002-001: Staleness detection for ORCHESTRATION.yaml

StalenessDetector Contract Test Justification:
    StalenessDetector is a concrete infrastructure adapter without a port
    protocol interface. It was intentionally designed as a direct dependency
    (not injected via port) because staleness detection is infrastructure-
    specific behavior with no alternative implementations planned. Contract
    tests are reserved for port/adapter pairs (IThresholdConfiguration,
    ITranscriptReader, ICheckpointRepository). Integration tests here
    provide equivalent behavioral verification for StalenessDetector.

References:
    - FEAT-001: Context Detection (EN-003, EN-004)
    - FEAT-002: Pre-Tool-Use Hooks (EN-005)
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from src.context_monitoring.application.services.checkpoint_service import (
    CheckpointService,
)
from src.context_monitoring.application.services.context_fill_estimator import (
    ContextFillEstimator,
)
from src.context_monitoring.application.services.resumption_context_generator import (
    ResumptionContextGenerator,
)
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
from src.context_monitoring.infrastructure.adapters.staleness_detector import (
    StalenessDetector,
)
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)

pytestmark = [
    pytest.mark.integration,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def layered_config(tmp_path: Path) -> LayeredConfigAdapter:
    """Create a real LayeredConfigAdapter with default settings."""
    return LayeredConfigAdapter(
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


@pytest.fixture()
def threshold_config(layered_config: LayeredConfigAdapter) -> ConfigThresholdAdapter:
    """Create a real ConfigThresholdAdapter from real LayeredConfigAdapter."""
    return ConfigThresholdAdapter(config=layered_config)


@pytest.fixture()
def transcript_reader() -> JsonlTranscriptReader:
    """Create a real JsonlTranscriptReader."""
    return JsonlTranscriptReader()


@pytest.fixture()
def estimator(
    transcript_reader: JsonlTranscriptReader,
    threshold_config: ConfigThresholdAdapter,
) -> ContextFillEstimator:
    """Create a real ContextFillEstimator with real dependencies."""
    return ContextFillEstimator(
        reader=transcript_reader,
        threshold_config=threshold_config,
    )


@pytest.fixture()
def checkpoint_repo(tmp_path: Path) -> FilesystemCheckpointRepository:
    """Create a real FilesystemCheckpointRepository with isolated lock directory.

    Lock directory is scoped to tmp_path to prevent lock file leakage
    into the project working directory and avoid inter-test interference
    when running under pytest-xdist parallel execution.
    """
    return FilesystemCheckpointRepository(
        checkpoint_dir=tmp_path / "checkpoints",
        file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
    )


@pytest.fixture()
def checkpoint_service(
    checkpoint_repo: FilesystemCheckpointRepository,
) -> CheckpointService:
    """Create a real CheckpointService."""
    return CheckpointService(repository=checkpoint_repo)


@pytest.fixture()
def resumption_generator() -> ResumptionContextGenerator:
    """Create a real ResumptionContextGenerator."""
    return ResumptionContextGenerator()


# =============================================================================
# Happy Path (60%)
# =============================================================================


class TestConfigThresholdAdapterIntegration:
    """Integration: ConfigThresholdAdapter reads from real LayeredConfigAdapter.

    Acceptance Criteria: AC-FEAT001-002 (configurable thresholds)
    References: FEAT-001 (EN-004), PROJ-004
    """

    def test_reads_default_thresholds(self, threshold_config: ConfigThresholdAdapter) -> None:
        """Adapter returns default thresholds from LayeredConfigAdapter defaults."""
        assert threshold_config.get_threshold("nominal") == 0.55
        assert threshold_config.get_threshold("warning") == 0.70
        assert threshold_config.get_threshold("critical") == 0.80
        assert threshold_config.get_threshold("emergency") == 0.88

    def test_enabled_defaults_to_true(self, threshold_config: ConfigThresholdAdapter) -> None:
        """Adapter reads enabled=True from LayeredConfigAdapter defaults."""
        assert threshold_config.is_enabled() is True

    def test_context_window_defaults_to_200k(
        self, threshold_config: ConfigThresholdAdapter
    ) -> None:
        """Adapter returns 200K default context window."""
        assert threshold_config.get_context_window_tokens() == 200_000
        assert threshold_config.get_context_window_source() == "default"

    def test_env_var_override_threshold(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Environment variable overrides LayeredConfigAdapter default threshold."""
        monkeypatch.setenv("JERRY_CONTEXT_MONITOR__WARNING_THRESHOLD", "0.65")
        layered = LayeredConfigAdapter(
            env_prefix="JERRY_",
            root_config_path=tmp_path / "config.toml",
            defaults={
                "context_monitor.warning_threshold": 0.70,
            },
        )
        adapter = ConfigThresholdAdapter(config=layered)
        assert adapter.get_threshold("warning") == 0.65


class TestEstimatorWithRealReaderIntegration:
    """Integration: ContextFillEstimator reads real JSONL transcript files.

    Acceptance Criteria: AC-FEAT001-001 (token counting), AC-FEAT001-002 (tier classification)
    References: FEAT-001 (EN-003, EN-004), PROJ-004
    """

    def test_reads_real_transcript_and_classifies(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Estimator reads a real JSONL file and returns correct classification."""
        transcript = create_transcript(tmp_path / "transcript.jsonl", 100_000)
        result = estimator.estimate(str(transcript))
        assert result.fill_percentage == pytest.approx(0.5)
        assert result.tier == ThresholdTier.NOMINAL
        assert result.token_count == 100_000
        assert result.monitoring_ok is True

    def test_warning_tier_from_real_transcript(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Estimator correctly classifies WARNING from real transcript."""
        transcript = create_transcript(tmp_path / "transcript.jsonl", 150_000)
        result = estimator.estimate(str(transcript))
        assert result.tier == ThresholdTier.WARNING
        assert result.fill_percentage == pytest.approx(0.75)

    def test_emergency_tier_from_real_transcript(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Estimator correctly classifies EMERGENCY from real transcript."""
        transcript = create_transcript(tmp_path / "transcript.jsonl", 180_000)
        result = estimator.estimate(str(transcript))
        assert result.tier == ThresholdTier.EMERGENCY

    def test_xml_tag_from_real_estimate(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Estimator generates valid XML tag from real transcript reading."""
        transcript = create_transcript(tmp_path / "transcript.jsonl", 150_000)
        result = estimator.estimate(str(transcript))
        tag = estimator.generate_context_monitor_tag(result)
        assert "<context-monitor>" in tag
        assert "<tier>WARNING</tier>" in tag
        assert "<monitoring-ok>true</monitoring-ok>" in tag


class TestCheckpointRoundtripIntegration:
    """Integration: Checkpoint create → persist → retrieve lifecycle.

    Verifies all FillEstimate fields survive serialization roundtrip.
    Acceptance Criteria: AC-FEAT001-004 (checkpoint lifecycle), AC-FEAT001-005 (fail-open)
    References: FEAT-001 (EN-003), PROJ-004
    """

    def test_create_and_retrieve_checkpoint(
        self,
        checkpoint_service: CheckpointService,
        checkpoint_repo: FilesystemCheckpointRepository,
    ) -> None:
        """Checkpoint persists to filesystem and is retrievable."""
        fill = FillEstimate(
            fill_percentage=0.72,
            tier=ThresholdTier.WARNING,
            token_count=144_000,
        )
        checkpoint = checkpoint_service.create_checkpoint(fill, "pre-compact")
        assert checkpoint.checkpoint_id == "cx-001"

        retrieved = checkpoint_repo.get_latest_unacknowledged()
        assert retrieved is not None
        assert retrieved.checkpoint_id == "cx-001"
        assert retrieved.context_state.fill_percentage == pytest.approx(0.72)

    def test_checkpoint_roundtrip_preserves_all_fields(
        self,
        checkpoint_service: CheckpointService,
        checkpoint_repo: FilesystemCheckpointRepository,
    ) -> None:
        """All FillEstimate fields survive checkpoint save→load roundtrip.

        Verifies monitoring_ok, context_window, and context_window_source
        are preserved through filesystem serialization/deserialization.
        """
        fill = FillEstimate(
            fill_percentage=0.85,
            tier=ThresholdTier.CRITICAL,
            token_count=170_000,
            monitoring_ok=True,
            context_window=500_000,
            context_window_source="env",
        )
        checkpoint_service.create_checkpoint(fill, "pre-compact")

        retrieved = checkpoint_repo.get_latest_unacknowledged()
        assert retrieved is not None
        state = retrieved.context_state
        assert state.fill_percentage == pytest.approx(0.85)
        assert state.tier == ThresholdTier.CRITICAL
        assert state.token_count == 170_000
        assert state.monitoring_ok is True
        assert state.context_window == 500_000
        assert state.context_window_source == "env"

    def test_fail_open_estimate_roundtrip_preserves_monitoring_ok(
        self,
        checkpoint_service: CheckpointService,
        checkpoint_repo: FilesystemCheckpointRepository,
    ) -> None:
        """Fail-open estimate with monitoring_ok=False survives roundtrip.

        Distinguishes fail-open NOMINAL from genuine NOMINAL after checkpoint.
        """
        fail_open_fill = FillEstimate(
            fill_percentage=0.0,
            tier=ThresholdTier.NOMINAL,
            token_count=None,
            monitoring_ok=False,
        )
        checkpoint_service.create_checkpoint(fail_open_fill, "error-recovery")

        retrieved = checkpoint_repo.get_latest_unacknowledged()
        assert retrieved is not None
        assert retrieved.context_state.monitoring_ok is False
        assert retrieved.context_state.fill_percentage == 0.0

    def test_acknowledge_checkpoint(
        self,
        checkpoint_service: CheckpointService,
        checkpoint_repo: FilesystemCheckpointRepository,
    ) -> None:
        """Acknowledged checkpoint is excluded from get_latest_unacknowledged."""
        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        checkpoint = checkpoint_service.create_checkpoint(fill, "test")

        checkpoint_repo.acknowledge(checkpoint.checkpoint_id)
        assert checkpoint_repo.get_latest_unacknowledged() is None

    def test_sequential_checkpoint_ids(
        self,
        checkpoint_service: CheckpointService,
    ) -> None:
        """Checkpoints get sequential IDs: cx-001, cx-002, cx-003."""
        fill = FillEstimate(fill_percentage=0.5, tier=ThresholdTier.NOMINAL)
        c1 = checkpoint_service.create_checkpoint(fill, "test")
        c2 = checkpoint_service.create_checkpoint(fill, "test")
        c3 = checkpoint_service.create_checkpoint(fill, "test")
        assert c1.checkpoint_id == "cx-001"
        assert c2.checkpoint_id == "cx-002"
        assert c3.checkpoint_id == "cx-003"

    def test_resumption_context_from_real_checkpoint(
        self,
        checkpoint_service: CheckpointService,
        resumption_generator: ResumptionContextGenerator,
    ) -> None:
        """ResumptionContextGenerator produces empty string without orchestration_path.

        Production CheckpointService is wired without orchestration_path
        (src/bootstrap.py), so resumption_state is always None.
        """
        fill = FillEstimate(
            fill_percentage=0.82,
            tier=ThresholdTier.CRITICAL,
            token_count=164_000,
        )
        checkpoint = checkpoint_service.create_checkpoint(fill, "pre-compact")
        assert checkpoint.resumption_state is None
        xml = resumption_generator.generate(checkpoint)
        assert xml == ""


class TestStalenessDetectorIntegration:
    """Integration: StalenessDetector reads real ORCHESTRATION.yaml files.

    Clock Handling: All staleness tests use an explicit ``reference_time``
    parameter (deterministic datetime) rather than ``datetime.now()``. This
    ensures tests are reproducible and not affected by wall-clock drift.
    The StalenessDetector.check_staleness() method accepts ``reference_time``
    as a required parameter specifically to support deterministic testing.

    Acceptance Criteria: AC-FEAT002-001 (staleness detection)
    References: FEAT-002 (EN-005), PROJ-004
    """

    def test_stale_orchestration_detected(self, tmp_path: Path) -> None:
        """Detects stale ORCHESTRATION.yaml with old updated_at timestamp."""
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_path.write_text(
            "resumption:\n  recovery_state:\n    updated_at: '2026-02-18T10:00:00+00:00'\n"
        )

        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is True
        assert result.warning_message is not None
        assert "stale" in result.warning_message.lower()

    def test_fresh_orchestration_passes_through(self, tmp_path: Path) -> None:
        """Fresh ORCHESTRATION.yaml passes through without warning."""
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_path.write_text(
            "resumption:\n  recovery_state:\n    updated_at: '2026-02-20T10:00:00+00:00'\n"
        )

        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is False

    def test_non_orchestration_path_passes_through(self, tmp_path: Path) -> None:
        """Non-ORCHESTRATION.yaml paths pass through immediately."""
        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="src/main.py",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is False

    def test_missing_orchestration_fails_open(self, tmp_path: Path) -> None:
        """Missing ORCHESTRATION.yaml fails open (no stale warning)."""
        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is False

    def test_malformed_yaml_fails_open(self, tmp_path: Path) -> None:
        """Malformed YAML content fails open (no stale warning)."""
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_path.write_text("not: [valid: yaml: content")

        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is False

    def test_missing_updated_at_field_fails_open(self, tmp_path: Path) -> None:
        """ORCHESTRATION.yaml without updated_at field fails open."""
        orch_path = tmp_path / "ORCHESTRATION.yaml"
        orch_path.write_text("resumption:\n  recovery_state:\n    status: ACTIVE\n")

        detector = StalenessDetector(project_root=tmp_path)
        result = detector.check_staleness(
            tool_target_path="ORCHESTRATION.yaml",
            reference_time=datetime(2026, 2, 19, 8, 0, 0, tzinfo=UTC),
        )
        assert result.is_stale is False


# =============================================================================
# Negative (30%)
# =============================================================================


class TestNegativeIntegration:
    """Negative integration: Error cases across real components.

    References: FEAT-001, PROJ-004
    """

    def test_missing_transcript_fails_open(
        self,
        estimator: ContextFillEstimator,
    ) -> None:
        """Missing transcript file returns NOMINAL with monitoring_ok=False."""
        result = estimator.estimate("/nonexistent/transcript.jsonl")
        assert result.tier == ThresholdTier.NOMINAL
        assert result.fill_percentage == 0.0
        assert result.monitoring_ok is False

    def test_empty_transcript_fails_open(
        self,
        estimator: ContextFillEstimator,
        tmp_path: Path,
    ) -> None:
        """Empty transcript file returns NOMINAL fail-open."""
        empty = tmp_path / "empty.jsonl"
        empty.write_text("")
        result = estimator.estimate(str(empty))
        assert result.tier == ThresholdTier.NOMINAL
        assert result.monitoring_ok is False

    def test_malformed_jsonl_fails_open(
        self,
        estimator: ContextFillEstimator,
        tmp_path: Path,
    ) -> None:
        """Malformed JSONL file returns NOMINAL fail-open."""
        bad = tmp_path / "bad.jsonl"
        bad.write_text("not json at all\n")
        result = estimator.estimate(str(bad))
        assert result.tier == ThresholdTier.NOMINAL
        assert result.monitoring_ok is False

    def test_disabled_monitoring_returns_fail_open(self, create_transcript, tmp_path: Path) -> None:
        """Disabled monitoring returns NOMINAL with monitoring_ok=False."""
        layered = LayeredConfigAdapter(
            env_prefix="JERRY_",
            root_config_path=tmp_path / "config.toml",
            defaults={"context_monitor.enabled": False},
        )
        config = ConfigThresholdAdapter(config=layered)
        reader = JsonlTranscriptReader()
        est = ContextFillEstimator(reader=reader, threshold_config=config)
        transcript = create_transcript(tmp_path / "t.jsonl", 190_000)
        result = est.estimate(str(transcript))
        assert result.tier == ThresholdTier.NOMINAL
        assert result.monitoring_ok is False

    def test_no_checkpoints_returns_none(
        self,
        checkpoint_repo: FilesystemCheckpointRepository,
    ) -> None:
        """Empty checkpoint directory returns None for latest unacknowledged."""
        assert checkpoint_repo.get_latest_unacknowledged() is None

    def test_invalid_tier_raises_value_error(
        self, threshold_config: ConfigThresholdAdapter
    ) -> None:
        """Invalid tier name raises ValueError through real adapter chain."""
        with pytest.raises(ValueError, match="Unrecognized threshold tier"):
            threshold_config.get_threshold("invalid_tier")

    def test_fail_open_recovery_after_error(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Estimator recovers correctly after a fail-open error.

        Verifies the fail-open sentinel is not shared/mutated: a failed call
        followed by a valid call produces correct results on the second call.
        """
        # First call: fail-open
        result1 = estimator.estimate("/nonexistent/transcript.jsonl")
        assert result1.monitoring_ok is False
        assert result1.tier == ThresholdTier.NOMINAL

        # Second call: valid transcript should produce correct result
        transcript = create_transcript(tmp_path / "valid.jsonl", 150_000)
        result2 = estimator.estimate(str(transcript))
        assert result2.monitoring_ok is True
        assert result2.tier == ThresholdTier.WARNING
        assert result2.fill_percentage == pytest.approx(0.75)

    def test_corrupt_checkpoint_file_skipped(self, tmp_path: Path) -> None:
        """Corrupt checkpoint file is silently skipped (fail-open).

        A valid JSON file with wrong schema is caught and skipped,
        not crashing the entire checkpoint loading.
        """
        checkpoint_dir = tmp_path / "checkpoints"
        checkpoint_dir.mkdir()

        # Write a corrupt checkpoint file (valid JSON, wrong schema)
        corrupt = checkpoint_dir / "cx-001.json"
        corrupt.write_text(json.dumps({"not_a": "checkpoint"}))

        # Write a valid checkpoint file
        valid = checkpoint_dir / "cx-002.json"
        valid.write_text(
            json.dumps(
                {
                    "checkpoint_id": "cx-002",
                    "context_state": {
                        "fill_percentage": 0.72,
                        "tier": "warning",
                        "token_count": 144_000,
                        "monitoring_ok": True,
                        "context_window": 200_000,
                        "context_window_source": "default",
                    },
                    "resumption_state": None,
                    "created_at": "2026-02-20T12:00:00+00:00",
                }
            )
        )

        repo = FilesystemCheckpointRepository(
            checkpoint_dir=checkpoint_dir,
            file_adapter=AtomicFileAdapter(lock_dir=tmp_path / "locks"),
        )
        latest = repo.get_latest_unacknowledged()
        assert latest is not None
        assert latest.checkpoint_id == "cx-002"


# =============================================================================
# Edge Cases (10%)
# =============================================================================


class TestEdgeCaseIntegration:
    """Edge case integration: boundary conditions across real components.

    References: FEAT-001, PROJ-004
    """

    def test_exact_boundary_token_count(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Token count exactly at boundary classifies correctly."""
        # 0.55 * 200_000 = 110_000 -> exactly at nominal/low boundary
        transcript = create_transcript(tmp_path / "t.jsonl", 110_000)
        result = estimator.estimate(str(transcript))
        assert result.tier == ThresholdTier.LOW

    def test_multi_entry_transcript_uses_last(
        self,
        estimator: ContextFillEstimator,
        tmp_path: Path,
    ) -> None:
        """Multi-entry JSONL uses the last assistant entry, not first."""
        transcript = tmp_path / "multi.jsonl"
        entries = []
        # First entry: low token count
        entries.append(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "usage": {"input_tokens": 10_000},
                    },
                }
            )
        )
        # Second entry: high token count (this should be used)
        entries.append(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "role": "assistant",
                        "usage": {"input_tokens": 180_000},
                    },
                }
            )
        )
        transcript.write_text("\n".join(entries) + "\n")
        result = estimator.estimate(str(transcript))
        assert result.tier == ThresholdTier.EMERGENCY
        assert result.token_count == 180_000

    def test_cache_fields_contribute_to_token_sum(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Non-zero cache fields are included in the token sum."""
        transcript = create_transcript(
            tmp_path / "cache.jsonl",
            100_000,
            cache_creation=30_000,
            cache_read=20_000,
        )
        result = estimator.estimate(str(transcript))
        assert result.token_count == 150_000
        assert result.tier == ThresholdTier.WARNING

    def test_all_tier_boundary_exact_values(
        self,
        estimator: ContextFillEstimator,
        create_transcript,
        tmp_path: Path,
    ) -> None:
        """Exact boundary token values classify into the higher tier (>= semantics)."""
        # Boundaries: nominal=0.55, warning=0.70, critical=0.80, emergency=0.88
        # context_window=200_000
        boundaries = [
            (110_000, ThresholdTier.LOW),  # 0.55 exactly -> LOW
            (140_000, ThresholdTier.WARNING),  # 0.70 exactly -> WARNING
            (160_000, ThresholdTier.CRITICAL),  # 0.80 exactly -> CRITICAL
            (176_000, ThresholdTier.EMERGENCY),  # 0.88 exactly -> EMERGENCY
        ]
        for i, (tokens, expected_tier) in enumerate(boundaries):
            transcript = create_transcript(tmp_path / f"boundary_{i}.jsonl", tokens)
            result = estimator.estimate(str(transcript))
            assert result.tier == expected_tier, (
                f"At {tokens} tokens (fill={tokens / 200_000:.4f}), "
                f"expected {expected_tier}, got {result.tier}"
            )
