# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
JSON Schema definition for the ORCHESTRATION.yaml v2.0 resumption section.

Defines the 7 sub-sections of the enhanced resumption schema:
  1. recovery_state   -- current phase, agent status, pipeline positions
  2. files_to_read    -- ordered list of files the resuming session must read
  3. quality_trajectory -- QG scores, iteration counts, pass/fail status
  4. defect_summary   -- accumulated defect counts and recurring patterns
  5. decision_log     -- cross-phase decisions made during execution
  6. agent_summaries  -- one-line summaries of completed agents
  7. compaction_events -- compaction event records

References:
    - ST-001: Enhanced Resumption Schema + Update Protocol
    - SPIKE-001 Phase 4: Resumption Completeness Assessment
"""

from __future__ import annotations

# ISO 8601 datetime pattern (allows Z or +HH:MM offset)
ISO_8601_PATTERN = (
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(Z|[+-]\d{2}:\d{2})$"
)

RESUMPTION_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ORCHESTRATION.yaml v2.0 Resumption Schema",
    "description": (
        "Enhanced resumption section for context-resilient session handoff. "
        "7 sub-sections replace the original 5-field structure while preserving "
        "backward compatibility (original fields exist within recovery_state)."
    ),
    "type": "object",
    "required": [
        "recovery_state",
        "files_to_read",
        "quality_trajectory",
        "defect_summary",
        "decision_log",
        "agent_summaries",
        "compaction_events",
    ],
    "properties": {
        # --- 1. Recovery State (replaces/subsumes original 5 fields) ---
        "recovery_state": {
            "type": "object",
            "description": (
                "Current execution state. Subsumes the original 5 fields: "
                "last_checkpoint, current_state (now structured), next_step, "
                "cross_session_portable, ephemeral_references."
            ),
            "required": [
                "last_checkpoint",
                "current_phase",
                "current_phase_name",
                "workflow_status",
                "current_activity",
                "next_step",
                "context_fill_at_update",
                "updated_at",
            ],
            "properties": {
                "last_checkpoint": {
                    "description": "Most recent checkpoint ID (e.g., 'CP-002') or null",
                    "type": ["string", "null"],
                },
                "current_phase": {
                    "description": "Numeric phase index (machine-readable)",
                    "type": "integer",
                    "minimum": 0,
                },
                "current_phase_name": {
                    "description": "Human-readable phase name",
                    "type": "string",
                },
                "workflow_status": {
                    "description": "Workflow lifecycle state",
                    "type": "string",
                    "enum": [
                        "ACTIVE",
                        "PAUSED",
                        "COMPLETE",
                        "FAILED",
                        "CANCELLED",
                    ],
                },
                "current_activity": {
                    "description": (
                        "What was happening at update time. Values: "
                        "phase-N-agent-execution, qg-N-iteration-M, "
                        "compaction-recovery, idle"
                    ),
                    "type": "string",
                },
                "next_step": {
                    "description": "Clear, actionable next step for the resuming session",
                    "type": "string",
                },
                "context_fill_at_update": {
                    "description": (
                        "Context fill percentage (0.0-1.0) when this section "
                        "was last updated. Null if unknown."
                    ),
                    "type": ["number", "null"],
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "updated_at": {
                    "description": "ISO 8601 timestamp of last resumption update",
                    "type": "string",
                    "pattern": ISO_8601_PATTERN,
                },
                # Backward-compatible optional fields
                "cross_session_portable": {
                    "description": "Whether state is portable across sessions (backward compat)",
                    "type": "boolean",
                    "default": True,
                },
                "ephemeral_references": {
                    "description": "Whether state contains ephemeral references (backward compat)",
                    "type": "boolean",
                    "default": False,
                },
            },
            "additionalProperties": False,
        },
        # --- 2. Files to Read (enhanced with priority and purpose) ---
        "files_to_read": {
            "type": "array",
            "description": (
                "Ordered list of files the resuming session must read. "
                "Backward compatible: simple string paths are accepted alongside "
                "structured entries with priority/purpose/sections."
            ),
            "items": {
                "oneOf": [
                    # Structured entry (v2.0)
                    {
                        "type": "object",
                        "required": ["path", "priority", "purpose"],
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the file",
                            },
                            "priority": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "Load order (1 = first)",
                            },
                            "purpose": {
                                "type": "string",
                                "description": "Why this file matters for resumption",
                            },
                            "sections": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific sections to read within the file",
                            },
                        },
                        "additionalProperties": False,
                    },
                    # Simple string path (v1.0 backward compat)
                    {
                        "type": "string",
                        "description": "Simple file path (v1.0 backward compatibility)",
                    },
                ],
            },
            "minItems": 1,
        },
        # --- 3. Quality Trajectory ---
        "quality_trajectory": {
            "type": "object",
            "description": "Structured quality gate scores and iteration tracking",
            "required": [
                "gates_completed",
                "gates_remaining",
                "current_gate",
                "current_gate_iteration",
                "score_history",
                "lowest_dimension",
                "total_iterations_used",
            ],
            "properties": {
                "gates_completed": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of completed gate IDs",
                },
                "gates_remaining": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of remaining gate IDs",
                },
                "current_gate": {
                    "type": ["string", "null"],
                    "description": "Gate ID if in-progress, null if between gates",
                },
                "current_gate_iteration": {
                    "type": ["integer", "null"],
                    "description": "Iteration number within current gate, null if between gates",
                },
                "score_history": {
                    "type": "object",
                    "description": "Per-gate array of scores per iteration",
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                    },
                },
                "lowest_dimension": {
                    "type": ["string", "null"],
                    "description": "Recurring weakest S-014 dimension across gates",
                },
                "total_iterations_used": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Sum of all gate iterations so far",
                },
            },
            "additionalProperties": False,
        },
        # --- 4. Defect Summary ---
        "defect_summary": {
            "type": "object",
            "description": "Accumulated defect context across all quality gates",
            "required": [
                "total_defects_found",
                "total_defects_resolved",
                "unresolved_defects",
                "recurring_patterns",
                "last_gate_primary_defect",
            ],
            "properties": {
                "total_defects_found": {
                    "type": "integer",
                    "minimum": 0,
                },
                "total_defects_resolved": {
                    "type": "integer",
                    "minimum": 0,
                },
                "unresolved_defects": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of unresolved defect IDs or descriptions",
                },
                "recurring_patterns": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["pattern", "gates_affected"],
                        "properties": {
                            "pattern": {"type": "string"},
                            "gates_affected": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "resolution": {
                                "type": ["string", "null"],
                            },
                        },
                        "additionalProperties": False,
                    },
                },
                "last_gate_primary_defect": {
                    "type": ["string", "null"],
                    "description": "Primary defect from most recent gate iteration",
                },
            },
            "additionalProperties": False,
        },
        # --- 5. Decision Log ---
        "decision_log": {
            "type": "array",
            "description": "Cross-phase decisions made during execution",
            "items": {
                "type": "object",
                "required": ["id", "decision", "rationale"],
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Decision identifier (e.g., 'RD-001')",
                    },
                    "gate": {
                        "type": ["string", "null"],
                        "description": "Gate ID where decision was made",
                    },
                    "iteration": {
                        "type": ["integer", "null"],
                        "description": "Gate iteration number",
                    },
                    "decision": {
                        "type": "string",
                        "description": "What was decided",
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Why this decision was made",
                    },
                    "affects_phases": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Phase numbers affected by this decision",
                    },
                    "applied": {
                        "type": "boolean",
                        "description": "Whether the decision has been applied",
                    },
                },
                "additionalProperties": False,
            },
        },
        # --- 6. Agent Summaries ---
        "agent_summaries": {
            "type": "object",
            "description": (
                "One-line summaries of completed agents. Keys are agent IDs, "
                "values are summary strings. Agents not yet executed are omitted."
            ),
            "additionalProperties": {
                "type": "string",
            },
        },
        # --- 7. Compaction Events ---
        "compaction_events": {
            "type": "object",
            "description": "Compaction event records for context resilience",
            "required": ["count", "events"],
            "properties": {
                "count": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of compaction events in this session",
                },
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "id",
                            "timestamp",
                            "trigger",
                            "estimated_fill_before",
                        ],
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Compaction event ID (e.g., 'CX-001')",
                            },
                            "timestamp": {
                                "type": "string",
                                "pattern": ISO_8601_PATTERN,
                            },
                            "trigger": {
                                "type": "string",
                                "enum": ["auto", "manual"],
                            },
                            "estimated_fill_before": {
                                "type": "number",
                                "minimum": 0.0,
                                "maximum": 1.0,
                            },
                            "active_phase": {
                                "type": ["integer", "null"],
                            },
                            "active_gate": {
                                "type": ["string", "null"],
                            },
                            "active_gate_iteration": {
                                "type": ["integer", "null"],
                            },
                            "checkpoint_file": {
                                "type": ["string", "null"],
                            },
                            "acknowledged": {
                                "type": "boolean",
                                "default": False,
                            },
                        },
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        },
    },
    "additionalProperties": False,
}

# The 5 original fields that must be preserved for backward compatibility.
# These fields must exist within the v2.0 schema (mapped into recovery_state
# and files_to_read).
ORIGINAL_V1_FIELDS = [
    "last_checkpoint",      # -> recovery_state.last_checkpoint
    "current_state",        # -> recovery_state.{current_phase, workflow_status, current_activity}
    "next_step",            # -> recovery_state.next_step
    "files_to_read",        # -> files_to_read (top-level, now structured)
    "cross_session_portable",  # -> recovery_state.cross_session_portable
]
