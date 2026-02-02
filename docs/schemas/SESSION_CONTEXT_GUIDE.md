# Session Context Schema Guide

> **Schema Version:** 1.0.0
> **Status:** ACTIVE
> **Work Item:** WI-SAO-001
> **Created:** 2026-01-10

---

## Overview

The Session Context Schema defines the canonical format for agent-to-agent handoffs in the Jerry Framework. It enables reliable agent chaining across the `ps-*` (Problem-Solving) and `nse-*` (NASA SE) agent families.

**Schema Location:** `docs/schemas/session_context.json`

---

## Quick Start

### Producing Context (Source Agent)

When an agent completes its work and needs to hand off to another agent:

```json
{
  "schema_version": "1.0.0",
  "session_id": "{{ SESSION_ID }}",
  "source_agent": {
    "id": "ps-researcher",
    "family": "ps",
    "cognitive_mode": "divergent"
  },
  "target_agent": {
    "id": "nse-requirements",
    "family": "nse",
    "cognitive_mode": "convergent"
  },
  "timestamp": "{{ ISO_8601_NOW }}",
  "payload": {
    "key_findings": [...],
    "open_questions": [...],
    "blockers": [],
    "confidence": {
      "overall": 0.85,
      "reasoning": "..."
    }
  }
}
```

### Consuming Context (Target Agent)

When receiving context, validate and extract:

```python
# Pseudo-code for context consumption
context = receive_handoff()

# Validate schema version
if context["schema_version"] != "1.0.0":
    raise SchemaVersionMismatchError()

# Validate session
if context["session_id"] != current_session_id:
    log.warning("Session mismatch - may be stale state")

# Process payload
for finding in context["payload"]["key_findings"]:
    process_finding(finding)

# Handle blockers
if context["payload"]["blockers"]:
    escalate_blockers(context["payload"]["blockers"])
```

---

## Schema Structure

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Semver version (e.g., "1.0.0") |
| `session_id` | string | Current session identifier |
| `source_agent` | object | Agent producing the context |
| `target_agent` | object | Intended recipient agent |
| `timestamp` | string | ISO-8601 timestamp |
| `payload` | object | The handoff content |

### Agent Reference

```json
{
  "id": "nse-requirements",       // Required: agent identifier
  "family": "nse",                // Required: ps, nse, or orch
  "cognitive_mode": "convergent", // Optional: convergent/divergent/mixed
  "model": "sonnet"               // Optional: opus/sonnet/haiku/auto
}
```

### Payload Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key_findings` | array | Yes | Primary insights from source agent |
| `open_questions` | array | No | Unresolved questions |
| `blockers` | array | No | Issues blocking completion |
| `confidence` | object | Yes | Confidence score (0.0-1.0) |
| `artifacts` | array | No | File paths to outputs |
| `context` | object | No | Domain-specific data |
| `recommendations` | array | No | Suggested actions |

---

## Validation Rules

### P-003 Compliance (Nesting Depth)

The `trace.depth` field MUST be <= 1:

```json
{
  "trace": {
    "depth": 0  // OK: orchestrator to worker
    // depth: 1 = worker to worker (allowed)
    // depth: 2 = VIOLATION - workers spawning workers
  }
}
```

### Session Validation

Always validate session ID to detect stale state:

```python
if handoff_session_id != current_session_id:
    # Options:
    # 1. Reject and request fresh context
    # 2. Accept with warning (log for debugging)
    # 3. Start fresh with no input context
    log.warning(f"Session mismatch: {handoff_session_id} vs {current_session_id}")
```

### Cross-Skill Handoffs

When `source_agent.family != target_agent.family`:

1. Log the cross-skill handoff for traceability
2. Validate domain-specific context is present
3. Apply any family-specific transformations

```json
{
  "source_agent": { "family": "ps" },
  "target_agent": { "family": "nse" }
  // This is a cross-skill handoff: ps -> nse
}
```

---

## ID Patterns

### Finding ID

Pattern: `F-NNN` (e.g., F-001, F-042)

### Question ID

Pattern: `Q-NNN` (e.g., Q-001, Q-015)

### Blocker ID

Pattern: `BLK-NNN` (e.g., BLK-001, BLK-003)

### Agent ID

Pattern: `{family}-{role}` (e.g., ps-researcher, nse-requirements, orch-planner)

---

## Confidence Scoring

### Overall Score

| Range | Meaning |
|-------|---------|
| 0.9-1.0 | Very High - Strong evidence, well-validated |
| 0.7-0.9 | High - Good evidence, minor gaps |
| 0.5-0.7 | Medium - Some evidence, notable gaps |
| 0.3-0.5 | Low - Limited evidence, significant gaps |
| 0.0-0.3 | Very Low - Speculative, needs verification |

### Breakdown Categories

```json
{
  "confidence": {
    "overall": 0.75,
    "breakdown": {
      "source_quality": 0.90,   // How reliable are the sources?
      "completeness": 0.60,     // How complete is the analysis?
      "accuracy": 0.80,         // How accurate are the findings?
      "relevance": 0.85         // How relevant to the task?
    }
  }
}
```

---

## Artifact References

### Artifact Types

| Type | Description | Producer Agents |
|------|-------------|-----------------|
| `requirement` | Requirements specification | nse-requirements |
| `risk` | Risk register/assessment | nse-risk |
| `architecture` | Trade study, design docs | nse-architecture |
| `verification` | VCRM, test plans | nse-verification |
| `review` | Review packages | nse-reviewer |
| `integration` | ICDs, interface specs | nse-integration |
| `configuration` | CI lists, baselines | nse-configuration |
| `report` | Status reports | nse-reporter |
| `analysis` | Gap analysis, research | ps-analyst |
| `synthesis` | Consolidated findings | ps-synthesizer |

### Path Rules

1. All paths MUST be repository-relative (no absolute paths)
2. Paths MUST NOT start with `/`
3. Paths SHOULD use forward slashes (cross-platform)

```json
{
  "path": "projects/PROJ-002/requirements/REQ-001.md",  // GOOD
  "path": "/Users/me/projects/PROJ-002/requirements/REQ-001.md"  // BAD
}
```

---

## Error Handling

### Schema Validation Errors

When validation fails:

1. Log the validation error with context
2. Return structured error to caller
3. Do NOT proceed with malformed context

```python
class SessionContextValidationError(Exception):
    def __init__(self, field: str, error: str, context: dict):
        self.field = field
        self.error = error
        self.context = context
```

### Common Errors

| Error | Field | Resolution |
|-------|-------|------------|
| Missing required field | Any required | Add the missing field |
| Invalid pattern | `*.id` | Fix the ID format |
| Schema version mismatch | `schema_version` | Update producer or consumer |
| Session mismatch | `session_id` | Decide: accept with warning or reject |
| Invalid confidence | `confidence.overall` | Ensure 0.0 <= value <= 1.0 |

---

## Evolution Strategy

### Adding Fields

1. New fields MUST be optional
2. Consumers MUST ignore unknown fields
3. Update `schema_version` minor version

### Breaking Changes

1. Increment `schema_version` major version
2. Document migration path
3. Support old version for deprecation period

### Version Compatibility

| Consumer | Producer | Compatible? |
|----------|----------|-------------|
| 1.0.x | 1.0.x | Yes |
| 1.1.x | 1.0.x | Yes (backward) |
| 1.0.x | 1.1.x | Yes (ignore new fields) |
| 2.0.x | 1.x.x | No (breaking change) |

---

## Integration with ORCHESTRATION.yaml

The session context flows through the orchestration workflow:

```yaml
# ORCHESTRATION.yaml
pipelines:
  nse:
    phases:
      - id: 1
        agents:
          - id: nse-requirements
            session_context:
              input: "contexts/ps-to-nse.json"   # Input context
              output: "contexts/nse-req-out.json" # Output context
```

---

## References

- **JSON Schema Draft-07:** https://json-schema.org/draft-07/schema
- **ISO-8601 Timestamps:** https://en.wikipedia.org/wiki/ISO_8601
- **Jerry Constitution:** `docs/governance/JERRY_CONSTITUTION.md`
- **Orchestration State Schema:** `skills/orchestration/docs/STATE_SCHEMA.md`

---

*Created: 2026-01-10*
*Work Item: WI-SAO-001*
