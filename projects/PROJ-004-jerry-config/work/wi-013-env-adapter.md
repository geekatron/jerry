# WI-013: Environment Variable Adapter

| Field | Value |
|-------|-------|
| **ID** | WI-013 |
| **Title** | Environment Variable Adapter |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-04 |
| **Assignee** | WT-Infra |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement an environment variable adapter that reads configuration from environment variables with automatic type conversion and key mapping (e.g., `JERRY_LOGGING__LEVEL` → `logging.level`).

---

## Acceptance Criteria

- [ ] AC-013.1: Maps env vars with `JERRY_` prefix to config keys
- [ ] AC-013.2: Uses `__` for nested keys (e.g., `JERRY_LOGGING__LEVEL`)
- [ ] AC-013.3: Auto-converts string values to bool/int/float/list
- [ ] AC-013.4: Implements `IConfigurationProvider` port interface
- [ ] AC-013.5: Unit tests for all type conversions
- [ ] AC-013.6: Unit tests for key mapping edge cases

---

## Sub-tasks

- [ ] ST-013.1: Create `src/infrastructure/adapters/configuration/env_config_adapter.py`
- [ ] ST-013.2: Implement env var scanning with prefix filter
- [ ] ST-013.3: Implement key mapping (env → config key)
- [ ] ST-013.4: Implement type coercion logic
- [ ] ST-013.5: Write comprehensive unit tests

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-013.1 | - | - |
| AC-013.2 | - | - |
| AC-013.3 | - | - |
| AC-013.4 | - | - |
| AC-013.5 | - | - |
| AC-013.6 | - | - |

---

## Implementation Notes

```python
# src/infrastructure/adapters/configuration/env_config_adapter.py
import os
import json
from typing import Any


class EnvConfigAdapter:
    """Adapter for reading configuration from environment variables."""

    def __init__(self, prefix: str = "JERRY_") -> None:
        self._prefix = prefix
        self._cache: dict[str, Any] = {}
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Scan environment for prefixed variables."""
        for key, value in os.environ.items():
            if key.startswith(self._prefix):
                config_key = self._env_to_config_key(key)
                self._cache[config_key] = self._parse_value(value)

    def _env_to_config_key(self, env_key: str) -> str:
        """Convert env var name to config key."""
        # JERRY_LOGGING__LEVEL → logging.level
        key = env_key[len(self._prefix):]
        return key.lower().replace("__", ".")

    def _parse_value(self, value: str) -> Any:
        """Parse string value to appropriate type."""
        # Boolean
        if value.lower() in ("true", "yes", "on", "1"):
            return True
        if value.lower() in ("false", "no", "off", "0"):
            return False

        # Integer
        try:
            return int(value)
        except ValueError:
            pass

        # Float
        try:
            return float(value)
        except ValueError:
            pass

        # JSON (list or dict)
        if value.startswith("[") or value.startswith("{"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        # Comma-separated list
        if "," in value and not value.startswith('"'):
            return [v.strip() for v in value.split(",")]

        return value

    def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def has(self, key: str) -> bool:
        return key in self._cache
```

---

## Type Conversion Rules

| Target Type | Recognized Values |
|-------------|-------------------|
| `bool` | `true/false`, `1/0`, `yes/no`, `on/off` (case-insensitive) |
| `int` | Numeric string: `42` |
| `float` | Numeric string: `3.14` |
| `list` | JSON array: `["a","b"]` or comma-separated: `a,b,c` |
| `dict` | JSON object: `{"key": "value"}` |

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-008 | Domain model design provides port interface |
| Blocks | WI-014 | Layered config needs env adapter |

---

## Related Artifacts

- **Research**: [PROJ-004-e-004](../research/PROJ-004-e-004-config-precedence.md)
- **12-Factor App**: [Config](https://12factor.net/config)
