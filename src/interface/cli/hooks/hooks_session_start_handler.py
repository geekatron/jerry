# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HooksSessionStartHandler - CLI handler for the SessionStart hook.

Reads Claude Code ``SessionStart`` JSON from stdin, invokes the project
context query, quality reinforcement engine, resumption context
generator, and WORKTRACKER.md injection, then returns a JSON response
with ``additionalContext`` combining all four.

Design Principles:
    - **Fail-open everywhere**: Each step is wrapped in try/except.
      Step failures log to stderr, but processing continues.
    - **Exit 0 always**: The handler always exits 0 even on partial failure.
    - **Valid JSON always**: The response is always valid JSON.

References:
    - EN-006: jerry hooks CLI Command Namespace
    - EN-001: Local context support for session hook
    - EN-004: ResumptionContextGenerator
    - EN-008 TASK-002: WORKTRACKER.md auto-injection in resumption
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape

from src.application.ports.primary.iquerydispatcher import IQueryDispatcher
from src.application.queries import RetrieveProjectContextQuery
from src.context_monitoring.application.ports.checkpoint_repository import (
    ICheckpointRepository,
)
from src.context_monitoring.application.services.resumption_context_generator import (
    ResumptionContextGenerator,
)
from src.infrastructure.internal.enforcement.session_quality_context_generator import (
    SessionQualityContextGenerator,
)

# TASK-002: Max chars for WORKTRACKER.md injection (prevents context bloat)
_WORKTRACKER_MAX_CHARS = 4000

logger = logging.getLogger(__name__)


class HooksSessionStartHandler:
    """CLI handler for the Claude Code SessionStart hook.

    Combines project context, quality reinforcement, and checkpoint
    resumption context into a single ``additionalContext`` payload.

    Each processing step is fail-open: failures log to stderr and
    processing continues with an empty contribution from the failed step.

    Attributes:
        _query_dispatcher: Query dispatcher for project context retrieval.
        _projects_dir: Path to the projects directory for context queries.
        _checkpoint_repository: Repository for loading the latest checkpoint.
        _resumption_generator: Generator for resumption context XML.
        _quality_context_generator: Generator for L1 session quality context XML.

    Example:
        >>> handler = HooksSessionStartHandler(
        ...     query_dispatcher=dispatcher,
        ...     projects_dir="projects",
        ...     checkpoint_repository=repo,
        ...     resumption_generator=generator,
        ...     quality_context_generator=generator,
        ... )
        >>> exit_code = handler.handle(stdin_json)
    """

    def __init__(
        self,
        query_dispatcher: IQueryDispatcher,
        projects_dir: str,
        checkpoint_repository: ICheckpointRepository,
        resumption_generator: ResumptionContextGenerator,
        quality_context_generator: SessionQualityContextGenerator,
    ) -> None:
        """Initialize the handler with required services.

        Args:
            query_dispatcher: Query dispatcher for project context retrieval.
            projects_dir: Path to the projects directory for context queries.
            checkpoint_repository: Repository for loading the latest checkpoint.
            resumption_generator: Generator for resumption context XML.
            quality_context_generator: Generator for L1 session quality context XML.
        """
        self._query_dispatcher = query_dispatcher
        self._projects_dir = projects_dir
        self._checkpoint_repository = checkpoint_repository
        self._resumption_generator = resumption_generator
        self._quality_context_generator = quality_context_generator

    def handle(self, stdin_json: str) -> int:
        """Handle a SessionStart hook event.

        Reads the hook input JSON, fetches project context, quality
        reinforcement, and resumption checkpoint data (all fail-open),
        and prints the combined JSON response to stdout.

        Args:
            stdin_json: The JSON payload from the Claude Code hook.

        Returns:
            Exit code (always 0).
        """
        context_parts: list[str] = []

        # Step 1: Parse hook input (fail-open)
        hook_data: dict[str, Any] = {}
        try:
            hook_data = json.loads(stdin_json)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[hooks/session-start] Failed to parse hook input: {exc}", file=sys.stderr)

        _ = hook_data  # Available for future use (e.g., session_id)

        # Step 2: Project context query (fail-open)
        try:
            query = RetrieveProjectContextQuery(base_path=self._projects_dir)
            context = self._query_dispatcher.dispatch(query)

            jerry_project = context.get("jerry_project") or ""
            project_id = context.get("project_id") or ""

            if jerry_project or project_id:
                project_xml = (
                    "<project-context>\n"
                    f"  <jerry-project>{jerry_project}</jerry-project>\n"
                    f"  <project-id>{project_id}</project-id>\n"
                    "</project-context>"
                )
                context_parts.append(project_xml)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/session-start] Project context query failed: {exc}",
                file=sys.stderr,
            )

        # Step 3: Quality context XML preamble (fail-open)
        try:
            quality_context = self._quality_context_generator.generate()
            if quality_context.preamble:
                context_parts.append(quality_context.preamble)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/session-start] Quality context generation failed: {exc}",
                file=sys.stderr,
            )

        # Step 4: Resumption context from latest checkpoint (fail-open)
        # DEF-005: acknowledge() MUST be called AFTER checkpoint data is
        # formatted for the response, ensuring delivery before marking consumed.
        try:
            checkpoint = self._checkpoint_repository.get_latest_unacknowledged()
            if checkpoint is not None:
                resumption_xml = self._resumption_generator.generate(checkpoint)
                if resumption_xml:
                    context_parts.append(resumption_xml)
                # DEF-005: Acknowledge after successful formatting
                try:
                    self._checkpoint_repository.acknowledge(checkpoint.checkpoint_id)
                except Exception as ack_exc:  # noqa: BLE001
                    print(
                        f"[hooks/session-start] Checkpoint acknowledge failed: {ack_exc}",
                        file=sys.stderr,
                    )
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/session-start] Resumption context generation failed: {exc}",
                file=sys.stderr,
            )

        # Step 5: WORKTRACKER.md injection (TASK-002, fail-open)
        try:
            worktracker_xml = self._read_worktracker()
            if worktracker_xml:
                context_parts.append(worktracker_xml)
        except Exception as exc:  # noqa: BLE001
            print(
                f"[hooks/session-start] WORKTRACKER.md injection failed: {exc}",
                file=sys.stderr,
            )

        # Assemble and emit response
        additional_context = "\n\n".join(context_parts)
        response: dict[str, Any] = {"additionalContext": additional_context}
        print(json.dumps(response))

        return 0

    def _read_worktracker(self) -> str | None:
        """Read WORKTRACKER.md for the active project and format as XML.

        TASK-002: Injects WORKTRACKER.md content into session start context
        so the LLM has work item state for resumption. Truncates to
        _WORKTRACKER_MAX_CHARS to prevent context bloat.

        Returns:
            XML string with worktracker content, or None if unavailable.
        """
        project_id = os.environ.get("JERRY_PROJECT")
        if not project_id:
            return None

        project_root = os.environ.get("CLAUDE_PROJECT_DIR")
        if project_root:
            base = Path(project_root)
        else:
            base = Path.cwd()

        worktracker_path = base / "projects" / project_id / "WORKTRACKER.md"
        if not worktracker_path.exists():
            return None

        content = worktracker_path.read_text(encoding="utf-8")
        if not content.strip():
            return None

        # Truncate to prevent context bloat
        if len(content) > _WORKTRACKER_MAX_CHARS:
            content = content[:_WORKTRACKER_MAX_CHARS] + "\n... (truncated)"

        # Escape XML-special characters to prevent malformed XML
        escaped_content = xml_escape(content)

        return f"<worktracker>\n{escaped_content}\n</worktracker>"
