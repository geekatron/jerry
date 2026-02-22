# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Composition Root - Application Bootstrap.

This module is the sole owner of dependency wiring.
It creates infrastructure adapters and wires them to handlers.

The key principle: NO adapter should instantiate its own dependencies.
All dependencies are created HERE and injected.

This follows the Composition Root pattern from Clean Architecture:
- Infrastructure adapters are instantiated here
- Handlers receive adapters via constructor injection
- Dispatcher is configured with handlers
- CLI adapter receives the dispatcher

Example:
    >>> from src.bootstrap import create_query_dispatcher
    >>> dispatcher = create_query_dispatcher()
    >>> # dispatcher is fully configured with all handlers

TD-018 Changes:
- Added FileSystemEventStore factory
- Added EventSourcedWorkItemRepository factory
- Added CommandDispatcher factory
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from src.application.dispatchers.command_dispatcher import CommandDispatcher
from src.application.dispatchers.query_dispatcher import QueryDispatcher
from src.application.handlers.queries import (
    RetrieveProjectContextQueryHandler,
    ScanProjectsQueryHandler,
    ValidateProjectQueryHandler,
)
from src.application.queries import (
    RetrieveProjectContextQuery,
    ScanProjectsQuery,
    ValidateProjectQuery,
)

# EN-001: Local context support for session hook
from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
    FilesystemLocalContextAdapter,
)
from src.infrastructure.adapters.serialization.toon_serializer import ToonSerializer
from src.session_management.application.commands import (
    AbandonSessionCommand,
    CreateSessionCommand,
    EndSessionCommand,
)
from src.session_management.application.handlers.commands import (
    AbandonSessionCommandHandler,
    CreateSessionCommandHandler,
    EndSessionCommandHandler,
)
from src.session_management.application.handlers.queries import GetSessionStatusQueryHandler
from src.session_management.application.queries import GetSessionStatusQuery
from src.session_management.infrastructure import (
    FilesystemProjectAdapter,
    InMemorySessionRepository,
    OsEnvironmentAdapter,
)
from src.session_management.infrastructure.adapters.event_sourced_session_repository import (
    EventSourcedSessionRepository,
)

# EN-025: Transcript parsing components (TDD-FEAT-004 Section 11.4)
from src.transcript.application.commands import ParseTranscriptCommand
from src.transcript.application.handlers import ParseTranscriptCommandHandler
from src.transcript.application.services.chunker import TranscriptChunker
from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
from src.work_tracking.application.commands import (
    BlockWorkItemCommand,
    CancelWorkItemCommand,
    CompleteWorkItemCommand,
    CreateWorkItemCommand,
    StartWorkItemCommand,
)
from src.work_tracking.application.handlers.commands import (
    BlockWorkItemCommandHandler,
    CancelWorkItemCommandHandler,
    CompleteWorkItemCommandHandler,
    CreateWorkItemCommandHandler,
    StartWorkItemCommandHandler,
)
from src.work_tracking.application.handlers.queries import (
    GetWorkItemQueryHandler,
    ListWorkItemsQueryHandler,
)
from src.work_tracking.application.queries import (
    GetWorkItemQuery,
    ListWorkItemsQuery,
)
from src.work_tracking.domain.services.id_generator import WorkItemIdGenerator
from src.work_tracking.infrastructure.adapters import InMemoryWorkItemRepository
from src.work_tracking.infrastructure.adapters.event_sourced_work_item_repository import (
    EventSourcedWorkItemRepository,
)
from src.work_tracking.infrastructure.persistence.filesystem_event_store import (
    FileSystemEventStore,
)
from src.work_tracking.infrastructure.persistence.in_memory_event_store import (
    InMemoryEventStore,
)

# Module-level session repository singleton for session state persistence
# EN-001: Uses EventSourcedSessionRepository for cross-process persistence
_session_repository: EventSourcedSessionRepository | InMemorySessionRepository | None = None

# Module-level event store and work item repository singletons
# TD-018: Event-sourced implementation with FileSystemEventStore
_event_store: FileSystemEventStore | InMemoryEventStore | None = None
_work_item_repository: EventSourcedWorkItemRepository | InMemoryWorkItemRepository | None = None

# Module-level ID generator singleton
# Phase 4.5: WorkItemIdGenerator for creating new work items
_id_generator: WorkItemIdGenerator | None = None

# Module-level serializer singleton
# DISC-012: TOON Format for LLM context serialization
_serializer: ToonSerializer | None = None


def get_session_repository() -> EventSourcedSessionRepository | InMemorySessionRepository:
    """Get the shared session repository instance.

    Returns:
        EventSourcedSessionRepository if a project is active (cross-process persistence),
        InMemorySessionRepository otherwise (in-process only).

    Note:
        EN-001: Uses event-sourced repository with FileSystemEventStore
        for cross-process session persistence.
    """
    global _session_repository
    if _session_repository is None:
        event_store = get_event_store()
        if isinstance(event_store, FileSystemEventStore):
            _session_repository = EventSourcedSessionRepository(event_store=event_store)
        else:
            _session_repository = InMemorySessionRepository()
    return _session_repository


def get_project_data_path() -> Path | None:
    """Get the data path for the current project.

    Returns:
        Path to project data directory, or None if no project is active.

    Resolution order:
        1. JERRY_PROJECT environment variable + projects directory
        2. None (no active project)
    """
    project_id = os.environ.get("JERRY_PROJECT")
    if not project_id:
        return None

    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        base = Path(project_root)
    else:
        base = Path.cwd()

    return base / "projects" / project_id


def create_event_store(
    project_path: Path | None = None,
    use_in_memory: bool = False,
) -> FileSystemEventStore | InMemoryEventStore:
    """Create an event store for work item persistence.

    Args:
        project_path: Path to project directory. If None, uses current project.
        use_in_memory: If True, use in-memory store (for testing).

    Returns:
        Event store instance (FileSystem or InMemory).

    Note:
        If no project path and no active project, uses in-memory store.
    """
    if use_in_memory:
        return InMemoryEventStore()

    if project_path is None:
        project_path = get_project_data_path()

    if project_path is None:
        # No active project - use in-memory (won't persist)
        return InMemoryEventStore()

    return FileSystemEventStore(project_path)


def get_event_store() -> FileSystemEventStore | InMemoryEventStore:
    """Get the shared event store instance.

    Returns:
        Event store singleton instance.

    Note:
        Uses FileSystemEventStore if a project is active,
        otherwise uses InMemoryEventStore.
    """
    global _event_store
    if _event_store is None:
        _event_store = create_event_store()
    return _event_store


def create_work_item_repository(
    event_store: FileSystemEventStore | InMemoryEventStore | None = None,
) -> EventSourcedWorkItemRepository:
    """Create an event-sourced work item repository.

    Args:
        event_store: Event store to use. If None, uses shared store.

    Returns:
        EventSourcedWorkItemRepository instance.

    Note:
        TD-018: Replaced InMemoryWorkItemRepository with EventSourced.
    """
    if event_store is None:
        event_store = get_event_store()

    return EventSourcedWorkItemRepository(event_store)


def get_work_item_repository() -> EventSourcedWorkItemRepository | InMemoryWorkItemRepository:
    """Get the shared work item repository instance.

    Returns:
        Work item repository singleton instance.

    Note:
        TD-018: Now uses EventSourcedWorkItemRepository backed by
        FileSystemEventStore when a project is active.
    """
    global _work_item_repository
    if _work_item_repository is None:
        _work_item_repository = create_work_item_repository()
    return _work_item_repository


def get_id_generator() -> WorkItemIdGenerator:
    """Get the shared work item ID generator instance.

    Returns:
        WorkItemIdGenerator singleton instance.

    Note:
        Phase 4.5: Used by CreateWorkItemCommandHandler for generating
        unique work item IDs with Snowflake internal IDs.
    """
    global _id_generator
    if _id_generator is None:
        _id_generator = WorkItemIdGenerator()
    return _id_generator


def create_serializer(
    indent: int = 2,
    delimiter: str = ",",
) -> ToonSerializer:
    """Create a TOON serializer for LLM context formatting.

    Args:
        indent: Spaces per indentation level (default: 2)
        delimiter: Column separator for tabular arrays (default: ,)

    Returns:
        ToonSerializer instance.

    Note:
        DISC-012: TOON format provides 30-60% token reduction vs JSON.
    """
    return ToonSerializer(indent=indent, delimiter=delimiter)


def get_serializer() -> ToonSerializer:
    """Get the shared serializer instance.

    Returns:
        ToonSerializer singleton instance.

    Note:
        DISC-012: Used by interface adapters for LLM-optimized output.
    """
    global _serializer
    if _serializer is None:
        _serializer = create_serializer()
    return _serializer


# =============================================================================
# Transcript Parsing Factories (TDD-FEAT-004 Section 11.4)
# =============================================================================


def create_vtt_parser() -> VTTParser:
    """Create a VTT parser instance.

    Returns:
        VTTParser instance with encoding detection.

    References:
        - EN-020: Python Parser Implementation
        - TDD-FEAT-004: Hybrid Infrastructure Design
    """
    return VTTParser()


def create_transcript_chunker(
    chunk_size: int = 500,
    target_tokens: int | None = 18000,
) -> TranscriptChunker:
    """Create a transcript chunker instance.

    Args:
        chunk_size: Number of segments per chunk (default: 500, deprecated)
        target_tokens: Target tokens per chunk (default: 18000, recommended)

    Returns:
        TranscriptChunker instance.

    References:
        - EN-021: Chunking Strategy
        - EN-026: Token-Based Chunking (BUG-001 fix)
        - ADR-004: File Splitting Strategy

    Note:
        EN-026: target_tokens=18000 is the recommended default to ensure
        chunks fit within Claude Code Read limit (25K tokens).
    """
    return TranscriptChunker(chunk_size=chunk_size, target_tokens=target_tokens)


def get_projects_directory() -> str:
    """Determine the projects directory path.

    Returns:
        Absolute path to the projects directory

    Resolution order:
        1. CLAUDE_PROJECT_DIR environment variable (set by Claude Code)
        2. Current working directory
    """
    project_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_root:
        return str(Path(project_root) / "projects")

    return str(Path.cwd() / "projects")


def create_query_dispatcher() -> QueryDispatcher:
    """Create a fully configured QueryDispatcher.

    This is the factory function that wires all query handlers
    with their infrastructure dependencies.

    Returns:
        QueryDispatcher with all handlers registered
    """
    # Create infrastructure adapters (secondary adapters)
    project_repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()
    session_repository = get_session_repository()

    # EN-001: Create local context reader for .jerry/local/context.toml
    # The adapter reads from CLAUDE_PROJECT_DIR (or cwd) for local context
    projects_dir = get_projects_directory()
    base_path = Path(projects_dir).parent  # Parent of projects/ is the workspace root
    local_context_reader = FilesystemLocalContextAdapter(base_path=base_path)

    # Create project-related handlers
    retrieve_project_context_handler = RetrieveProjectContextQueryHandler(
        repository=project_repository,
        environment=environment,
        local_context_reader=local_context_reader,  # EN-001: Wire local context support
    )
    scan_projects_handler = ScanProjectsQueryHandler(
        repository=project_repository,
    )
    validate_project_handler = ValidateProjectQueryHandler(
        repository=project_repository,
    )

    # Create session-related handlers
    get_session_status_handler = GetSessionStatusQueryHandler(
        repository=session_repository,
    )

    # Create work-item-related handlers
    work_item_repository = get_work_item_repository()
    list_work_items_handler = ListWorkItemsQueryHandler(
        repository=work_item_repository,
    )
    get_work_item_handler = GetWorkItemQueryHandler(
        repository=work_item_repository,
    )

    # Create and configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(RetrieveProjectContextQuery, retrieve_project_context_handler.handle)
    dispatcher.register(ScanProjectsQuery, scan_projects_handler.handle)
    dispatcher.register(ValidateProjectQuery, validate_project_handler.handle)
    dispatcher.register(GetSessionStatusQuery, get_session_status_handler.handle)
    dispatcher.register(ListWorkItemsQuery, list_work_items_handler.handle)
    dispatcher.register(GetWorkItemQuery, get_work_item_handler.handle)

    return dispatcher


def create_session_command_handlers() -> dict[str, Any]:
    """Create session command handlers.

    Returns a dictionary of command handlers for session management.

    Returns:
        Dictionary mapping command types to handler instances

    Note:
        Legacy dict-based approach. Consider using create_command_dispatcher()
        for a more type-safe approach.
    """
    session_repository = get_session_repository()

    return {
        "create": CreateSessionCommandHandler(repository=session_repository),
        "end": EndSessionCommandHandler(repository=session_repository),
        "abandon": AbandonSessionCommandHandler(repository=session_repository),
    }


def create_command_dispatcher() -> CommandDispatcher:
    """Create a fully configured CommandDispatcher.

    This is the factory function that wires all command handlers
    with their infrastructure dependencies.

    Returns:
        CommandDispatcher with all handlers registered.

    Note:
        TD-018: Wires session commands.
        Phase 4.5: Added work item commands.
    """
    session_repository = get_session_repository()
    work_item_repository = get_work_item_repository()
    id_generator = get_id_generator()

    # Create session command handlers
    create_session_handler = CreateSessionCommandHandler(repository=session_repository)
    end_session_handler = EndSessionCommandHandler(repository=session_repository)
    abandon_session_handler = AbandonSessionCommandHandler(repository=session_repository)

    # Create work item command handlers (Phase 4.5)
    create_work_item_handler = CreateWorkItemCommandHandler(
        repository=work_item_repository,
        id_generator=id_generator,
    )
    start_work_item_handler = StartWorkItemCommandHandler(
        repository=work_item_repository,
    )
    complete_work_item_handler = CompleteWorkItemCommandHandler(
        repository=work_item_repository,
    )
    block_work_item_handler = BlockWorkItemCommandHandler(
        repository=work_item_repository,
    )
    cancel_work_item_handler = CancelWorkItemCommandHandler(
        repository=work_item_repository,
    )

    # Create and configure dispatcher
    dispatcher = CommandDispatcher()

    # Register session commands
    dispatcher.register(CreateSessionCommand, create_session_handler.handle)
    dispatcher.register(EndSessionCommand, end_session_handler.handle)
    dispatcher.register(AbandonSessionCommand, abandon_session_handler.handle)

    # Register work item commands (Phase 4.5)
    dispatcher.register(CreateWorkItemCommand, create_work_item_handler.handle)
    dispatcher.register(StartWorkItemCommand, start_work_item_handler.handle)
    dispatcher.register(CompleteWorkItemCommand, complete_work_item_handler.handle)
    dispatcher.register(BlockWorkItemCommand, block_work_item_handler.handle)
    dispatcher.register(CancelWorkItemCommand, cancel_work_item_handler.handle)

    # Register transcript commands (EN-025: TDD-FEAT-004 Section 11.4)
    vtt_parser = create_vtt_parser()
    chunker = create_transcript_chunker()
    parse_transcript_handler = ParseTranscriptCommandHandler(
        vtt_parser=vtt_parser,
        chunker=chunker,
    )
    dispatcher.register(ParseTranscriptCommand, parse_transcript_handler.handle)

    return dispatcher


def create_hooks_handlers() -> dict[str, Any]:
    """Create hooks command handlers for the CLI.

    Wires all dependencies for the 4 hook event handlers:
    - prompt-submit: Context fill estimation + L2 quality reinforcement
    - session-start: Project context + resumption + quality reinforcement
    - pre-compact: Checkpoint creation + context fill estimation
    - pre-tool-use: AST enforcement + staleness detection

    Returns:
        Dictionary mapping hook command names to handler instances.

    References:
        - EN-006: jerry hooks CLI Command Namespace
        - PROJ-004: Context Resilience
    """
    from pathlib import Path

    from src.context_monitoring.application.services.checkpoint_service import (
        CheckpointService,
    )
    from src.context_monitoring.application.services.context_fill_estimator import (
        ContextFillEstimator,
    )
    from src.context_monitoring.application.services.resumption_context_generator import (
        ResumptionContextGenerator,
    )
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
    from src.infrastructure.internal.enforcement.pre_tool_enforcement_engine import (
        PreToolEnforcementEngine,
    )
    from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
        PromptReinforcementEngine,
    )
    from src.infrastructure.internal.enforcement.session_quality_context_generator import (
        SessionQualityContextGenerator,
    )
    from src.interface.cli.hooks.hooks_pre_compact_handler import (
        HooksPreCompactHandler,
    )
    from src.interface.cli.hooks.hooks_pre_tool_use_handler import (
        HooksPreToolUseHandler,
    )
    from src.interface.cli.hooks.hooks_prompt_submit_handler import (
        HooksPromptSubmitHandler,
    )
    from src.interface.cli.hooks.hooks_session_start_handler import (
        HooksSessionStartHandler,
    )

    project_root = Path.cwd()

    # Shared infrastructure
    file_adapter = AtomicFileAdapter()
    reinforcement_engine = PromptReinforcementEngine()

    # Context monitoring services
    transcript_reader = JsonlTranscriptReader()
    config_adapter = LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=project_root / ".jerry" / "config.toml",
        defaults={
            # NOTE: context_window_tokens is intentionally NOT in defaults.
            # The adapter must distinguish "user explicitly configured" from
            # "default" to support auto-detection priority chain (TASK-006).
            "context_monitor.nominal_threshold": 0.55,
            "context_monitor.warning_threshold": 0.70,
            "context_monitor.critical_threshold": 0.80,
            "context_monitor.emergency_threshold": 0.88,
            "context_monitor.compaction_detection_threshold": 10000,
            "context_monitor.enabled": True,
        },
    )
    threshold_config = ConfigThresholdAdapter(config=config_adapter)
    context_fill_estimator = ContextFillEstimator(
        reader=transcript_reader,
        threshold_config=threshold_config,
    )

    # Checkpoint services
    checkpoint_dir = project_root / ".jerry" / "checkpoints"
    checkpoint_repository = FilesystemCheckpointRepository(
        checkpoint_dir=checkpoint_dir,
        file_adapter=file_adapter,
    )
    checkpoint_service = CheckpointService(repository=checkpoint_repository)

    # Session handlers (for pre-compact abandon)
    session_repository = get_session_repository()
    abandon_handler = AbandonSessionCommandHandler(repository=session_repository)

    # Query dispatcher (for session-start project context)
    query_dispatcher = create_query_dispatcher()

    # Resumption context generator
    resumption_generator = ResumptionContextGenerator()

    # Staleness detector
    staleness_detector = StalenessDetector(project_root=project_root)

    # Pre-tool enforcement engine
    pre_tool_engine = PreToolEnforcementEngine(project_root=project_root)

    return {
        "prompt-submit": HooksPromptSubmitHandler(
            context_fill_estimator=context_fill_estimator,
            checkpoint_service=checkpoint_service,
            reinforcement_engine=reinforcement_engine,
        ),
        "session-start": HooksSessionStartHandler(
            query_dispatcher=query_dispatcher,
            projects_dir=get_projects_directory(),
            checkpoint_repository=checkpoint_repository,
            resumption_generator=resumption_generator,
            quality_context_generator=SessionQualityContextGenerator(),
        ),
        "pre-compact": HooksPreCompactHandler(
            checkpoint_service=checkpoint_service,
            context_fill_estimator=context_fill_estimator,
            abandon_handler=abandon_handler,
        ),
        "pre-tool-use": HooksPreToolUseHandler(
            enforcement_engine=pre_tool_engine,
            staleness_detector=staleness_detector,
        ),
    }


def create_context_estimate_handler() -> Any:
    """Create the context estimate CLI handler with all dependencies.

    Wires ContextEstimateComputer, FilesystemContextStateStore,
    ContextEstimateService, and ContextEstimateHandler.

    Returns:
        ContextEstimateHandler ready to process stdin JSON.

    References:
        - EN-012: jerry context estimate CLI Command
        - EN-013: Bootstrap Wiring + Config Integration
    """
    from src.context_monitoring.application.services.context_estimate_service import (
        ContextEstimateService,
    )
    from src.context_monitoring.domain.services.context_estimate_computer import (
        ContextEstimateComputer,
    )
    from src.context_monitoring.infrastructure.adapters.filesystem_context_state_store import (
        FilesystemContextStateStore,
    )
    from src.interface.cli.context.context_estimate_handler import (
        ContextEstimateHandler,
    )

    project_root = Path.cwd()
    state_dir = project_root / ".jerry" / "local"

    computer = ContextEstimateComputer()
    state_store = FilesystemContextStateStore(state_dir=state_dir)
    service = ContextEstimateService(computer, state_store)

    return ContextEstimateHandler(service)


def reset_singletons() -> None:
    """Reset all module-level singletons (for testing).

    This clears all cached instances so fresh instances are created
    on next access. Useful for integration tests.
    """
    global _session_repository, _event_store, _work_item_repository, _id_generator
    global _serializer
    _session_repository = None
    _event_store = None
    _work_item_repository = None
    _id_generator = None
    _serializer = None
