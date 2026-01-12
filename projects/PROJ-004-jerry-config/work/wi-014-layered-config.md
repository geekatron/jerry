# WI-014: Layered Config Adapter

| Field | Value |
|-------|-------|
| **ID** | WI-014 |
| **Title** | Layered Config Adapter |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | CRITICAL |
| **Phase** | PHASE-04 |
| **Assignee** | WT-Infra |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement the layered configuration adapter that combines all config sources with proper precedence: Environment Variables > Project Config > Root Config > Defaults. This is the main `IConfigurationProvider` implementation.

---

## Acceptance Criteria

- [ ] AC-014.1: Implements `IConfigurationProvider` port interface
- [ ] AC-014.2: Respects precedence order: env > project > root > defaults
- [ ] AC-014.3: Loads TOML config files using `tomllib` (stdlib)
- [ ] AC-014.4: Uses `AtomicFileAdapter` for file reads
- [ ] AC-014.5: Gracefully handles missing config files
- [ ] AC-014.6: Integration tests verifying precedence

---

## Sub-tasks

- [ ] ST-014.1: Create `src/infrastructure/adapters/configuration/layered_config_adapter.py`
- [ ] ST-014.2: Implement TOML loading via `tomllib`
- [ ] ST-014.3: Wire together EnvConfigAdapter + file configs + defaults
- [ ] ST-014.4: Implement `get`, `get_string`, `get_bool`, `get_int`, `get_list`
- [ ] ST-014.5: Write integration tests for precedence validation

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-014.1 | - | - |
| AC-014.2 | - | - |
| AC-014.3 | - | - |
| AC-014.4 | - | - |
| AC-014.5 | - | - |
| AC-014.6 | - | - |

---

## Implementation Notes

```python
# src/infrastructure/adapters/configuration/layered_config_adapter.py
import tomllib
from pathlib import Path
from typing import Any

from src.domain.ports.configuration import IConfigurationProvider
from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter
from src.infrastructure.adapters.configuration.env_config_adapter import EnvConfigAdapter


class LayeredConfigAdapter(IConfigurationProvider):
    """Adapter implementing layered configuration precedence."""

    def __init__(
        self,
        env_prefix: str = "JERRY_",
        root_config_path: Path | None = None,
        project_config_path: Path | None = None,
        defaults: dict[str, Any] | None = None,
    ) -> None:
        self._file_adapter = AtomicFileAdapter()
        self._env_adapter = EnvConfigAdapter(prefix=env_prefix)
        self._root_config = self._load_toml(root_config_path)
        self._project_config = self._load_toml(project_config_path)
        self._defaults = defaults or {}

    def _load_toml(self, path: Path | None) -> dict[str, Any]:
        """Load TOML config file, return empty dict if missing."""
        if path is None or not path.exists():
            return {}
        content = self._file_adapter.read_with_lock(path)
        if not content:
            return {}
        return tomllib.loads(content)

    def get(self, key: str) -> Any | None:
        # Priority 1: Environment variable
        if self._env_adapter.has(key):
            return self._env_adapter.get(key)

        # Priority 2: Project config
        value = self._get_nested(self._project_config, key)
        if value is not None:
            return value

        # Priority 3: Root config
        value = self._get_nested(self._root_config, key)
        if value is not None:
            return value

        # Priority 4: Defaults
        return self._defaults.get(key)

    def _get_nested(self, data: dict[str, Any], key: str) -> Any | None:
        """Get value from nested dict using dot notation."""
        parts = key.split(".")
        current = data
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current

    def get_string(self, key: str, default: str = "") -> str:
        value = self.get(key)
        return str(value) if value is not None else default

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "on", "1")
        return bool(value)

    def get_int(self, key: str, default: int = 0) -> int:
        value = self.get(key)
        if value is None:
            return default
        return int(value)

    def get_list(self, key: str, default: list | None = None) -> list:
        value = self.get(key)
        if value is None:
            return default or []
        if isinstance(value, list):
            return value
        return [value]

    def has(self, key: str) -> bool:
        return self.get(key) is not None
```

---

## Precedence Order

| Priority | Source | Example Path |
|----------|--------|--------------|
| 1 (Highest) | Environment Variables | `JERRY_LOGGING__LEVEL=DEBUG` |
| 2 | Project Config | `projects/PROJ-*/. jerry/config.toml` |
| 3 | Root Config | `.jerry/config.toml` |
| 4 (Lowest) | Code Defaults | `defaults={"logging.level": "INFO"}` |

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
| Depends On | WI-012 | Needs AtomicFileAdapter |
| Depends On | WI-013 | Needs EnvConfigAdapter |
| Blocks | WI-015 | CLI integration uses layered config |

---

## Related Artifacts

- **Research**: [PROJ-004-e-004](../research/PROJ-004-e-004-config-precedence.md)
- **Plan Reference**: [PLAN.md, Phase 2](../PLAN.md)
