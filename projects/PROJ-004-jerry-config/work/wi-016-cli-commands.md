# WI-016: CLI Config Commands

| Field | Value |
|-------|-------|
| **ID** | WI-016 |
| **Title** | CLI Config Commands |
| **Type** | Task |
| **Status** | COMPLETED |
| **Priority** | MEDIUM |
| **Phase** | PHASE-05 |
| **Assignee** | WT-CLI |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Implement CLI commands for viewing and managing configuration: `jerry config show`, `jerry config get <key>`, `jerry config set <key> <value>`, and `jerry config path`.

---

## Acceptance Criteria

- [x] AC-016.1: `jerry config show` displays merged configuration
- [x] AC-016.2: `jerry config show --json` outputs JSON format
- [x] AC-016.3: `jerry config get <key>` retrieves specific value
- [x] AC-016.4: `jerry config set <key> <value> --scope` writes to appropriate file
- [x] AC-016.5: `jerry config path` shows config file locations
- [x] AC-016.6: E2E tests for all commands

---

## Sub-tasks

- [x] ST-016.1: Add config namespace to parser.py
- [x] ST-016.2: Implement `show` command with table/JSON output
- [x] ST-016.3: Implement `get` command
- [x] ST-016.4: Implement `set` command with scope selection
- [x] ST-016.5: Implement `path` command
- [x] ST-016.6: Write E2E tests (10 tests)

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-016.1 | `cmd_config_show()` displays merged config via LayeredConfigAdapter | `src/interface/cli/adapter.py:1032-1091` |
| AC-016.2 | `--json` flag outputs valid JSON with `json.dumps()` | `src/interface/cli/adapter.py:1054-1063` |
| AC-016.3 | `cmd_config_get()` retrieves value via `config.get(key)` | `src/interface/cli/adapter.py:1093-1134` |
| AC-016.4 | `cmd_config_set()` writes to project/root/local based on scope | `src/interface/cli/adapter.py:1136-1277` |
| AC-016.5 | `cmd_config_path()` shows all config file paths | `src/interface/cli/adapter.py:1279-1322` |
| AC-016.6 | 10/10 E2E tests pass | `tests/e2e/test_config_commands.py` |

### Test Results

| Test Suite | Count | Status |
|------------|-------|--------|
| CLI unit tests | 15 | PASSED |
| Config E2E tests | 10 | PASSED |

---

## Implementation Notes

```bash
# Show current configuration (merged from all sources)
jerry config show

# Output example:
# ┌────────────────────────────────┬──────────┬─────────┐
# │ Key                            │ Value    │ Source  │
# ├────────────────────────────────┼──────────┼─────────┤
# │ logging.level                  │ INFO     │ root    │
# │ work_tracking.auto_snapshot    │ 5        │ project │
# │ project.id                     │ PROJ-004 │ env     │
# └────────────────────────────────┴──────────┴─────────┘

# JSON output
jerry config show --json
# {"logging.level": {"value": "INFO", "source": "root"}, ...}

# Get specific value
jerry config get logging.level
# INFO

# Set value (writes to project config)
jerry config set logging.level DEBUG --scope project

# Set value (writes to root config)
jerry config set logging.level DEBUG --scope root

# Show config file paths
jerry config path
# Root:    .jerry/config.toml
# Project: projects/PROJ-004-jerry-config/.jerry/config.toml
# Local:   .jerry/local/context.toml
```

---

## CLI Command Structure

```python
# src/interface/cli/commands/config_commands.py
import click

from src.infrastructure.adapters.configuration.layered_config_adapter import LayeredConfigAdapter


@click.group()
def config():
    """Manage Jerry configuration."""
    pass


@config.command()
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def show(json_output: bool):
    """Show current configuration."""
    adapter = create_config_adapter()
    # ... display merged config


@config.command()
@click.argument("key")
def get(key: str):
    """Get a configuration value."""
    adapter = create_config_adapter()
    value = adapter.get(key)
    if value is None:
        click.echo(f"Key '{key}' not found", err=True)
        raise SystemExit(1)
    click.echo(value)


@config.command()
@click.argument("key")
@click.argument("value")
@click.option("--scope", type=click.Choice(["project", "root"]), default="project")
def set(key: str, value: str, scope: str):
    """Set a configuration value."""
    # Write to appropriate config file
    ...


@config.command()
def path():
    """Show configuration file paths."""
    # Display paths
    ...
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |
| 2026-01-12T21:00:00Z | Started WI-016 implementation | Claude |
| 2026-01-12T21:05:00Z | Added config namespace to parser.py | Claude |
| 2026-01-12T21:10:00Z | Added `_handle_config()` to main.py | Claude |
| 2026-01-12T21:20:00Z | Implemented `cmd_config_show()` with table/JSON output | Claude |
| 2026-01-12T21:25:00Z | Implemented `cmd_config_get()` with source info | Claude |
| 2026-01-12T21:35:00Z | Implemented `cmd_config_set()` with scope selection | Claude |
| 2026-01-12T21:40:00Z | Implemented `cmd_config_path()` | Claude |
| 2026-01-12T21:45:00Z | Created 10 E2E tests | Claude |
| 2026-01-12T21:50:00Z | All tests pass (10/10 E2E, 15/15 unit) | Claude |
| 2026-01-12T21:55:00Z | Updated evidence table and marked COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-015 | Session hook must be integrated first |
| Blocks | WI-018 | E2E tests need CLI commands |

---

## Related Artifacts

- **Plan Reference**: [PLAN.md, Phase 3](../PLAN.md)
- **CLI Standards**: `.claude/rules/architecture-standards.md`
