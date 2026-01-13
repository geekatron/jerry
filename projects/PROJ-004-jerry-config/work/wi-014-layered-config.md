# WI-014: Layered Config Adapter

| Field | Value |
|-------|-------|
| **ID** | WI-014 |
| **Title** | Layered Config Adapter |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | CRITICAL |
| **Phase** | PHASE-04 |
| **Assignee** | WT-Infra |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Implement the layered configuration adapter that combines all config sources with proper precedence: Environment Variables > Project Config > Root Config > Defaults. This is the main `IConfigurationProvider` implementation.

---

## Acceptance Criteria

- [x] AC-014.1: Implements `IConfigurationProvider` port interface
- [x] AC-014.2: Respects precedence order: env > project > root > defaults
- [x] AC-014.3: Loads TOML config files using `tomllib` (stdlib)
- [x] AC-014.4: Uses `AtomicFileAdapter` for file reads
- [x] AC-014.5: Gracefully handles missing config files
- [x] AC-014.6: Integration tests verifying precedence

---

## Sub-tasks

- [x] ST-014.1: Create `src/infrastructure/adapters/configuration/layered_config_adapter.py`
- [x] ST-014.2: Implement TOML loading via `tomllib`
- [x] ST-014.3: Wire together EnvConfigAdapter + file configs + defaults
- [x] ST-014.4: Implement `get`, `get_string`, `get_bool`, `get_int`, `get_list`
- [x] ST-014.5: Write integration tests for precedence validation (27/27 passed)

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-014.1 | Implements `IConfigurationProvider` protocol with all required methods | `layered_config_adapter.py:36-65` |
| AC-014.2 | `get()` checks env → project → root → defaults in order | `layered_config_adapter.py:178-196` |
| AC-014.3 | `_load_toml()` uses `tomllib.loads()` (Python 3.11+ stdlib) | `layered_config_adapter.py:130-149` |
| AC-014.4 | Constructor accepts `file_adapter` param for dependency injection | `layered_config_adapter.py:96-100` |
| AC-014.5 | `_load_toml()` returns empty dict on missing file or parse error; Tests: `test_missing_file_returns_empty`, `test_invalid_toml_returns_empty`, `test_empty_file_returns_empty` | `layered_config_adapter.py:139-149`, `test_layered_config_adapter.py:142-176` |
| AC-014.6 | **27/27 integration tests passed**: TestLayeredConfigAdapterInit (3), TestLayeredConfigAdapterPrecedence (6), TestLayeredConfigAdapterToml (4), TestLayeredConfigAdapterTypedGetters (5), TestLayeredConfigAdapterHas (2), TestLayeredConfigAdapterGetSource (5), TestLayeredConfigAdapterReload (2), TestLayeredConfigAdapterAllKeys (1) | `test_layered_config_adapter.py` |

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
| 2026-01-12T14:00:00Z | Status changed to IN_PROGRESS - starting implementation in WT-Infra worktree | Claude |
| 2026-01-12T14:45:00Z | Implemented LayeredConfigAdapter with TOML loading via tomllib (stdlib) | Claude |
| 2026-01-12T14:50:00Z | Integrated with EnvConfigAdapter and AtomicFileAdapter via dependency injection | Claude |
| 2026-01-12T14:55:00Z | Functional tests passed (3/3): defaults work, env overrides, source detection works | Claude |
| 2026-01-12T15:00:00Z | Added `get_source()`, `reload()`, `all_keys()` utility methods | Claude |
| 2026-01-12T15:10:00Z | Created integration tests in `tests/unit/infrastructure/adapters/configuration/test_layered_config_adapter.py` | Claude |
| 2026-01-12T15:15:00Z | **TESTS PASSED**: 27/27 integration tests passed covering init, precedence, TOML loading, typed getters, has, get_source, reload, all_keys | Claude |
| 2026-01-12T15:20:00Z | **COMPLETED**: All acceptance criteria verified with evidence, all sub-tasks done, 27/27 integration tests | Claude |

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
