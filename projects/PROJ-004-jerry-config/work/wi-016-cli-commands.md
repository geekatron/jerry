# WI-016: CLI Config Commands

| Field | Value |
|-------|-------|
| **ID** | WI-016 |
| **Title** | CLI Config Commands |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | MEDIUM |
| **Phase** | PHASE-05 |
| **Assignee** | WT-CLI |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement CLI commands for viewing and managing configuration: `jerry config show`, `jerry config get <key>`, `jerry config set <key> <value>`, and `jerry config path`.

---

## Acceptance Criteria

- [ ] AC-016.1: `jerry config show` displays merged configuration
- [ ] AC-016.2: `jerry config show --json` outputs JSON format
- [ ] AC-016.3: `jerry config get <key>` retrieves specific value
- [ ] AC-016.4: `jerry config set <key> <value> --scope` writes to appropriate file
- [ ] AC-016.5: `jerry config path` shows config file locations
- [ ] AC-016.6: E2E tests for all commands

---

## Sub-tasks

- [ ] ST-016.1: Create `src/interface/cli/commands/config_commands.py`
- [ ] ST-016.2: Implement `show` command with table/JSON output
- [ ] ST-016.3: Implement `get` command
- [ ] ST-016.4: Implement `set` command with scope selection
- [ ] ST-016.5: Implement `path` command
- [ ] ST-016.6: Write E2E tests

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-016.1 | - | - |
| AC-016.2 | - | - |
| AC-016.3 | - | - |
| AC-016.4 | - | - |
| AC-016.5 | - | - |
| AC-016.6 | - | - |

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
