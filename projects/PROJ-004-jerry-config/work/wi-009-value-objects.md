# WI-009: Configuration Value Objects

| Field | Value |
|-------|-------|
| **ID** | WI-009 |
| **Title** | Configuration Value Objects |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | HIGH |
| **Phase** | PHASE-03 |
| **Assignee** | WT-Domain |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Implement immutable value objects for the configuration domain: ConfigKey, ConfigPath, ConfigValue. These value objects encapsulate validation logic and type conversion.

---

## Acceptance Criteria

- [x] AC-009.1: `ConfigKey` value object with dot-notation support
- [x] AC-009.2: `ConfigKey.to_env_key()` converts to env var format (JERRY_*)
- [x] AC-009.3: `ConfigPath` value object wraps Path with validation
- [x] AC-009.4: `ConfigValue` supports type coercion (str → bool/int/list)
- [x] AC-009.5: All value objects are immutable (`@dataclass(frozen=True, slots=True)`)
- [x] AC-009.6: Unit tests with 90%+ coverage (221 tests)

---

## Sub-tasks

- [x] ST-009.1: Create `src/configuration/domain/value_objects/config_key.py`
- [x] ST-009.2: Create `src/configuration/domain/value_objects/config_path.py`
- [x] ST-009.3: Create `src/configuration/domain/value_objects/config_value.py`
- [x] ST-009.4: Write unit tests for each value object (221 tests)
- [x] ST-009.5: ConfigSource enum added with 5-level precedence

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-009.1 | ConfigKey with `parts`, `depth`, `child()`, `parent()`, `matches()` | `src/configuration/domain/value_objects/config_key.py` |
| AC-009.2 | `to_env_key()` and `from_env_key()` implemented | `config_key.py:lines 113-150` |
| AC-009.3 | ConfigPath with validation, file type detection, navigation | `src/configuration/domain/value_objects/config_path.py` |
| AC-009.4 | `as_string()`, `as_bool()`, `as_int()`, `as_float()`, `as_list()`, `as_dict()` | `src/configuration/domain/value_objects/config_value.py` |
| AC-009.5 | All use `@dataclass(frozen=True, slots=True)` | All value object files |
| AC-009.6 | 221 unit tests passing | `pytest tests/unit/configuration/domain/value_objects/ -v` |

---

## Implementation Notes

```python
# Example: ConfigKey value object
@dataclass(frozen=True, slots=True)
class ConfigKey:
    """Immutable configuration key with dot-notation support."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValidationError(field="key", message="cannot be empty")

    def to_env_key(self, prefix: str = "JERRY_") -> str:
        """Convert to environment variable name."""
        return prefix + self.value.upper().replace(".", "__")

    @classmethod
    def from_env_key(cls, env_key: str, prefix: str = "JERRY_") -> "ConfigKey":
        """Create from environment variable name."""
        if not env_key.startswith(prefix):
            raise ValidationError(field="env_key", message=f"must start with {prefix}")
        key = env_key[len(prefix):].lower().replace("__", ".")
        return cls(key)
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |
| 2026-01-12T18:00:00Z | Implementation complete: ConfigKey, ConfigPath, ConfigValue, ConfigSource | Claude |
| 2026-01-12T18:30:00Z | Unit tests written: 221 tests covering all value objects | Claude |
| 2026-01-12T19:00:00Z | Tests passing, work item COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-008 | Domain model design must be complete |
| Blocks | WI-015 | CLI integration needs value objects |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md, Phase 1: Domain Layer](../PLAN.md)
- **Pattern**: [Immutable Value Object](../../../../.claude/patterns/value-object/immutable-value-object.md)
