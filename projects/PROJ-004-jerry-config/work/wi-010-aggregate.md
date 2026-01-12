# WI-010: Configuration Aggregate

| Field | Value |
|-------|-------|
| **ID** | WI-010 |
| **Title** | Configuration Aggregate |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-03 |
| **Assignee** | WT-Domain |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement the Configuration aggregate root that manages configuration state and emits domain events. The aggregate encapsulates configuration loading, value access, and change tracking.

---

## Acceptance Criteria

- [ ] AC-010.1: `Configuration` aggregate root with version tracking
- [ ] AC-010.2: Support for nested key access (`config.get("logging.level")`)
- [ ] AC-010.3: Type-safe accessors (`get_string`, `get_bool`, `get_int`, `get_list`)
- [ ] AC-010.4: Emits `ConfigurationLoaded` event on creation
- [ ] AC-010.5: Emits `ConfigurationValueChanged` on mutations
- [ ] AC-010.6: Unit tests with 90%+ coverage

---

## Sub-tasks

- [ ] ST-010.1: Create `src/domain/aggregates/configuration.py`
- [ ] ST-010.2: Implement nested key resolution
- [ ] ST-010.3: Implement type coercion methods
- [ ] ST-010.4: Wire domain event emission
- [ ] ST-010.5: Write comprehensive unit tests

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-010.1 | - | - |
| AC-010.2 | - | - |
| AC-010.3 | - | - |
| AC-010.4 | - | - |
| AC-010.5 | - | - |
| AC-010.6 | - | - |

---

## Implementation Notes

```python
# Example: Configuration aggregate
class Configuration(AggregateRoot):
    """Aggregate root for configuration management."""

    def __init__(self, data: dict[str, Any], source: str = "unknown") -> None:
        super().__init__()
        self._data = data
        self._source = source
        self._apply_event(ConfigurationLoaded.create(
            source=source,
            keys_loaded=self._count_keys(data),
        ))

    def get(self, key: str) -> Any | None:
        """Get value by dot-notation key."""
        parts = key.split(".")
        current = self._data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current

    def get_string(self, key: str, default: str = "") -> str:
        value = self.get(key)
        return str(value) if value is not None else default
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-008 | Domain model design must be complete |
| Depends On | WI-009 | Value objects must exist |
| Blocks | WI-015 | CLI integration needs aggregate |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md, Phase 1: Domain Layer](../PLAN.md)
- **Pattern**: [Aggregate Root](../../../../.claude/patterns/entity/aggregate-root.md)
