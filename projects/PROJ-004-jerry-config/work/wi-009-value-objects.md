# WI-009: Configuration Value Objects

| Field | Value |
|-------|-------|
| **ID** | WI-009 |
| **Title** | Configuration Value Objects |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-03 |
| **Assignee** | WT-Domain |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement immutable value objects for the configuration domain: ConfigKey, ConfigPath, ConfigValue. These value objects encapsulate validation logic and type conversion.

---

## Acceptance Criteria

- [ ] AC-009.1: `ConfigKey` value object with dot-notation support
- [ ] AC-009.2: `ConfigKey.to_env_key()` converts to env var format (JERRY_*)
- [ ] AC-009.3: `ConfigPath` value object wraps Path with validation
- [ ] AC-009.4: `ConfigValue` supports type coercion (str → bool/int/list)
- [ ] AC-009.5: All value objects are immutable (`@dataclass(frozen=True, slots=True)`)
- [ ] AC-009.6: Unit tests with 90%+ coverage

---

## Sub-tasks

- [ ] ST-009.1: Create `src/domain/value_objects/config_key.py`
- [ ] ST-009.2: Create `src/domain/value_objects/config_path.py`
- [ ] ST-009.3: Create `src/domain/value_objects/config_value.py`
- [ ] ST-009.4: Write unit tests for each value object
- [ ] ST-009.5: Document value object contracts

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-009.1 | - | - |
| AC-009.2 | - | - |
| AC-009.3 | - | - |
| AC-009.4 | - | - |
| AC-009.5 | - | - |
| AC-009.6 | - | - |

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
