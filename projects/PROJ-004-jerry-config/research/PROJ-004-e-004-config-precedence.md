# Research Artifact: Configuration Precedence Model

> **PS ID:** PROJ-004
> **Entry ID:** e-004
> **Date:** 2026-01-12
> **Researcher:** ps-researcher (v2.0.0)
> **Sources:**
> - [The Twelve-Factor App - Config](https://12factor.net/config)
> - [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
> - [Dynaconf Documentation](https://www.dynaconf.com/)
> - [Django Settings Documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
> - [Django Configurations - Best Practices](https://djangostars.com/blog/configuring-django-settings-best-practices/)
> - [Pydantic BaseSettings vs. Dynaconf Comparison](https://leapcell.io/blog/pydantic-basesettings-vs-dynaconf-a-modern-guide-to-application-configuration)
> - pydantic/pydantic-settings (Context7)
> - dynaconf/dynaconf (Context7)

---

## L0: Executive Summary (ELI5)

Configuration precedence should follow the 12-factor app principle: environment variables override file-based configuration, which overrides defaults. Jerry currently uses `JERRY_PROJECT` and `CLAUDE_PROJECT_DIR` environment variables but lacks a unified configuration system with layered precedence. The recommended approach is to implement a simple precedence chain: **Environment Variables > Project Config > Root Config > Defaults**.

---

## L1: Technical Findings

### 1. Standard Precedence Order

The industry-standard precedence order (highest to lowest priority) is:

| Priority | Source | Example |
|----------|--------|---------|
| 1 (Highest) | CLI Arguments | `--project=PROJ-001` |
| 2 | Environment Variables | `JERRY_PROJECT=PROJ-001` |
| 3 | Project-level Config File | `projects/PROJ-001/.jerry/config.json` |
| 4 | Root Config File | `.jerry/config.json` |
| 5 (Lowest) | Code Defaults | `DEFAULT_LOG_LEVEL = "INFO"` |

This aligns with both pydantic-settings and dynaconf patterns:

**Pydantic-settings Default Order:**
```python
# Default order (first has highest priority)
return (
    init_settings,      # __init__ kwargs
    env_settings,       # Environment variables
    dotenv_settings,    # .env file
    file_secret_settings,  # Secrets directory
)
```

**Dynaconf Order:**
```
CLI args > Environment vars > Config Maps/Vault > Config files > Defaults
```

### 2. Current Jerry Environment Variable Usage

Analysis of the Jerry codebase reveals the following environment variable usage:

| Variable | Location | Purpose | Current Usage |
|----------|----------|---------|---------------|
| `JERRY_PROJECT` | `bootstrap.py`, `session_start.py`, handlers | Active project ID | Direct `os.environ.get()` |
| `CLAUDE_PROJECT_DIR` | `bootstrap.py`, `session_start.py` | Root directory for projects | Direct `os.environ.get()` |
| `ECW_DEBUG` | `.claude/statusline.py` | Debug mode toggle | Direct `os.environ.get()` |

**Current Implementation Pattern:**
```python
# From src/bootstrap.py
project_id = os.environ.get("JERRY_PROJECT")
project_root = os.environ.get("CLAUDE_PROJECT_DIR")
```

**Current Port Abstraction (IEnvironmentProvider):**
```python
# From src/session_management/application/ports/environment.py
class IEnvironmentProvider(Protocol):
    def get_env(self, name: str) -> str | None: ...
    def get_env_or_default(self, name: str, default: str) -> str: ...

# Adapter: src/session_management/infrastructure/adapters/os_environment_adapter.py
class OsEnvironmentAdapter:
    def get_env(self, name: str) -> str | None:
        value = os.environ.get(name)
        if value is None or value.strip() == "":
            return None
        return value.strip()
```

### 3. Framework Patterns Analysis

#### Django Pattern
Django uses module-level settings with environment-based switching:

```python
# settings/base.py - Base configuration
DEBUG = False
DATABASE_URL = "sqlite:///db.sqlite3"

# settings/dev.py - Development overrides
from .base import *
DEBUG = True

# Selection via environment
DJANGO_SETTINGS_MODULE = "project.settings.dev"
```

#### Flask Pattern
Flask uses a simple dictionary-based config with environment loading:

```python
app.config.from_object('config.default')
app.config.from_envvar('APP_SETTINGS', silent=True)
app.config.from_prefixed_env()  # APP_* env vars
```

#### Pydantic-Settings Pattern
Pydantic provides type-safe configuration with customizable precedence:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='JERRY_',
        env_file='.env',
        env_file_encoding='utf-8',
    )

    project: str | None = None
    log_level: str = "INFO"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        # Custom order: env > init > dotenv > secrets
        return env_settings, init_settings, dotenv_settings, file_secret_settings
```

#### Dynaconf Pattern
Dynaconf provides layered configuration with multiple file format support:

```toml
# settings.toml
[default]
log_level = "INFO"

[development]
log_level = "DEBUG"

[production]
log_level = "WARNING"
```

```python
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="JERRY",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    env_switcher="JERRY_ENV",
)
```

### 4. Nested Configuration Overrides

For nested configuration values, there are two common patterns:

#### Double-Underscore Separator (Industry Standard)
```bash
# Override config.logging.level
export JERRY_LOGGING__LEVEL=DEBUG

# Override config.database.host
export JERRY_DATABASE__HOST=localhost
```

This is supported by both pydantic-settings and dynaconf:

```python
# Pydantic-settings
model_config = SettingsConfigDict(
    env_nested_delimiter='__',  # Use double underscore
)

# Dynaconf
export DYNACONF_DATABASE__HOST=localhost
export DYNACONF_DATABASE__PORT=5432
```

#### JSON-Encoded Values (Alternative)
```bash
export JERRY_DATABASE='{"host": "localhost", "port": 5432}'
```

### 5. Type Conversion Patterns

Environment variables are always strings. Common conversion patterns:

| Target Type | Env Value | Conversion |
|-------------|-----------|------------|
| `bool` | `"true"`, `"1"`, `"yes"` | Case-insensitive truthy check |
| `int` | `"42"` | `int(value)` |
| `float` | `"3.14"` | `float(value)` |
| `list` | `"a,b,c"` or `'["a","b","c"]'` | Split on delimiter or JSON parse |
| `dict` | `'{"key": "value"}'` | JSON parse |
| `None` | `""` or unset | Return `None` |

**Pydantic-settings handles this automatically:**
```python
class Settings(BaseSettings):
    debug: bool = False  # Parses "true", "1", "yes" etc.
    port: int = 8080     # Parses string to int
    tags: list[str] = [] # Parses JSON array or comma-separated
```

### 6. Configuration Documentation Patterns

Best practices for documenting configuration:

#### Table-Based Documentation
```markdown
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| JERRY_PROJECT | string | None | Active project ID |
| JERRY_LOG_LEVEL | string | "INFO" | Logging level (DEBUG, INFO, WARN, ERROR) |
```

#### Code-as-Documentation (Pydantic)
```python
class Settings(BaseSettings):
    """Jerry Framework Configuration.

    All settings can be overridden via environment variables
    with the JERRY_ prefix.
    """

    project: str | None = Field(
        default=None,
        description="Active project ID (e.g., PROJ-001-plugin-cleanup)",
        examples=["PROJ-001-plugin-cleanup", "PROJ-002-api-redesign"],
    )

    log_level: Literal["DEBUG", "INFO", "WARN", "ERROR"] = Field(
        default="INFO",
        description="Logging verbosity level",
    )
```

#### Auto-Generated Documentation
Both pydantic-settings and dynaconf support automatic documentation generation:

```python
# Pydantic - Generate JSON Schema
Settings.model_json_schema()

# Dynaconf - List all settings
dynaconf list --all
```

---

## L2: Strategic Recommendation for Jerry

### Recommended Architecture

Given Jerry's hexagonal architecture and zero-dependency domain requirement, I recommend a **layered configuration system** with the following structure:

```
                    ┌─────────────────────────────────┐
                    │        ConfigurationPort        │ ← Domain Port
                    │   (src/domain/ports/config.py)  │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │      LayeredConfigAdapter       │ ← Infrastructure
                    │ (src/infrastructure/adapters/)  │
                    └────────────────┬────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
   ┌─────────┐              ┌────────────────┐           ┌────────────────┐
   │ EnvVars │              │  Config Files  │           │   Defaults     │
   │ (os.env)│              │  (.jerry/*)    │           │  (code/class)  │
   └─────────┘              └────────────────┘           └────────────────┘
   Priority: 1              Priority: 2-3                Priority: 4
```

### Proposed Configuration File Location

```
jerry/
├── .jerry/
│   └── config.json              # Root-level config (optional)
└── projects/
    └── PROJ-001-plugin-cleanup/
        └── .jerry/
            └── config.json      # Project-level config (optional)
```

### Proposed Config Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "version": { "type": "string", "const": "1.0" },
    "logging": {
      "type": "object",
      "properties": {
        "level": { "enum": ["DEBUG", "INFO", "WARN", "ERROR"] },
        "format": { "type": "string" }
      }
    },
    "work_tracking": {
      "type": "object",
      "properties": {
        "auto_snapshot_interval": { "type": "integer", "default": 10 },
        "quality_gate_enabled": { "type": "boolean", "default": true }
      }
    }
  }
}
```

### Recommended Implementation Approach

Given Jerry's constraints:
1. **Zero external dependencies in domain** - Use stdlib only
2. **Hexagonal architecture** - Ports and adapters pattern
3. **Python 3.11+** - Modern typing features available

**Option A: Pure Stdlib Implementation (Recommended for Jerry)**

```python
# src/domain/ports/configuration.py
from typing import Protocol, Any

class IConfigurationProvider(Protocol):
    """Port for accessing configuration values."""

    def get(self, key: str) -> Any | None:
        """Get a configuration value by key."""
        ...

    def get_string(self, key: str, default: str = "") -> str:
        """Get a string configuration value."""
        ...

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value."""
        ...

    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value."""
        ...

# src/infrastructure/adapters/layered_config_adapter.py
class LayeredConfigAdapter:
    """Adapter implementing layered configuration precedence."""

    def __init__(
        self,
        env_prefix: str = "JERRY_",
        root_config_path: Path | None = None,
        project_config_path: Path | None = None,
        defaults: dict[str, Any] | None = None,
    ) -> None:
        self._env_prefix = env_prefix
        self._root_config = self._load_json(root_config_path) if root_config_path else {}
        self._project_config = self._load_json(project_config_path) if project_config_path else {}
        self._defaults = defaults or {}

    def get(self, key: str) -> Any | None:
        # 1. Check environment variable (highest priority)
        env_key = self._to_env_key(key)
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return self._parse_value(env_value)

        # 2. Check project config
        if key in self._project_config:
            return self._project_config[key]

        # 3. Check root config
        if key in self._root_config:
            return self._root_config[key]

        # 4. Return default
        return self._defaults.get(key)

    def _to_env_key(self, key: str) -> str:
        """Convert config key to environment variable name."""
        # config.logging.level -> JERRY_LOGGING__LEVEL
        return self._env_prefix + key.upper().replace(".", "__")
```

**Option B: Pydantic-Settings (If external deps allowed in infrastructure)**

```python
# src/infrastructure/adapters/pydantic_config_adapter.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class JerrySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JERRY_",
        env_nested_delimiter="__",
        env_file=".jerry/.env",
        json_file=".jerry/config.json",
    )

    project: str | None = None
    log_level: str = "INFO"
    auto_snapshot_interval: int = 10
    quality_gate_enabled: bool = True
```

### Migration Path from Current Implementation

1. **Phase 1: Port Abstraction** (Low risk)
   - Extend `IEnvironmentProvider` to `IConfigurationProvider`
   - Add config file loading to `OsEnvironmentAdapter`

2. **Phase 2: Layered Loading** (Medium risk)
   - Implement precedence chain in adapter
   - Add project-level config support

3. **Phase 3: Schema Validation** (Low risk)
   - Add JSON schema for config files
   - Validate on load

### Environment Variable Naming Convention

| Config Path | Environment Variable |
|-------------|---------------------|
| `project` | `JERRY_PROJECT` |
| `logging.level` | `JERRY_LOGGING__LEVEL` |
| `work_tracking.snapshot_interval` | `JERRY_WORK_TRACKING__SNAPSHOT_INTERVAL` |

### Type Conversion Rules

```python
def _parse_value(self, value: str) -> Any:
    """Parse environment variable string to appropriate type."""
    # Boolean
    if value.lower() in ("true", "1", "yes", "on"):
        return True
    if value.lower() in ("false", "0", "no", "off"):
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

    # JSON (for complex types)
    if value.startswith(("{", "[")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

    # String (default)
    return value
```

---

## Cross-References

| Reference | Purpose |
|-----------|---------|
| PROJ-004-e-001 | Configuration system requirements |
| PROJ-004-e-002 | Config file format selection |
| PROJ-004-e-003 | Environment variable analysis |
| ADR-CLI-002 | CLI namespace implementation (related precedence patterns) |
| `.claude/rules/architecture-standards.md` | Hexagonal architecture constraints |
| `src/session_management/application/ports/environment.py` | Current IEnvironmentProvider port |

---

## Implementation Checklist

Based on industry research, the following patterns should be implemented:

- [ ] Define `IConfigurationProvider` port in domain layer
- [ ] Implement `LayeredConfigAdapter` in infrastructure layer
- [ ] Support environment variable override with `JERRY_` prefix
- [ ] Support `__` (double-underscore) for nested config paths
- [ ] Implement type conversion for bool, int, float, JSON
- [ ] Create `.jerry/config.json` schema
- [ ] Add project-level config support (`projects/*/jerry/config.json`)
- [ ] Document all configuration options in a table format
- [ ] Add validation on config load
- [ ] Migrate existing `JERRY_PROJECT` and `CLAUDE_PROJECT_DIR` usage

---

## Sources

- [The Twelve-Factor App - Config](https://12factor.net/config)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Dynaconf Documentation](https://www.dynaconf.com/)
- [Django Settings Documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Django Configurations - Best Practices](https://djangostars.com/blog/configuring-django-settings-best-practices/)
- [Pydantic BaseSettings vs. Dynaconf Comparison](https://leapcell.io/blog/pydantic-basesettings-vs-dynaconf-a-modern-guide-to-application-configuration)
- [Python Structured Config with Dynaconf/Pydantic](https://medium.com/@2nick2patel2/python-structured-config-with-dynaconf-pydantic-twelve-factor-services-without-surprises-518349d92d4f)

---

*Document generated for PROJ-004 Configuration System Design*
*Research conducted via Context7, Web Search, and Codebase Analysis*
