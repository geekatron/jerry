# PHASE-05: Integration & CLI

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-05 |
| **Title** | Integration & CLI |
| **Status** | PENDING |
| **Parallelizable** | No (needs PHASE-03 + PHASE-04) |
| **Work Items** | WI-015, WI-016 |
| **Assignee** | WT-CLI |
| **Started** | - |
| **Completed** | - |

---

## Objective

Integrate the configuration system into the existing Jerry CLI: update the `session_start.py` hook to use the new config system, and add `jerry config` commands for configuration management.

---

## Work Items

| ID | Title | Status | File |
|----|-------|--------|------|
| WI-015 | Update session_start.py Hook | PENDING | [wi-015-session-hook.md](wi-015-session-hook.md) |
| WI-016 | CLI Config Commands | PENDING | [wi-016-cli-commands.md](wi-016-cli-commands.md) |

---

## Blockers

| Blocker | Status | Resolution |
|---------|--------|------------|
| WI-009-011 (Domain Layer) | PENDING | Must complete PHASE-03 |
| WI-012-014 (Infrastructure) | PENDING | Must complete PHASE-04 |

---

## Parallelization Strategy

### Worktree Assignment

| Branch | Work Items | Files Modified |
|--------|------------|----------------|
| `PROJ-004-config-cli` | WI-015, WI-016 | `src/interface/**`, `scripts/**` |

### Merge Order

```
1. WT-Main completes WI-008 (interfaces)
2. WT-Domain and WT-Infra work in parallel
3. Merge WT-Domain (PHASE-03) to main
4. Merge WT-Infra (PHASE-04) to main
5. WT-CLI branches from main ← THIS PHASE
6. Merge WT-CLI (PHASE-05) to main
```

---

## Deliverables

### Session Hook Update (WI-015)

```
scripts/
└── session_start.py  # Updated to use LayeredConfigAdapter
```

**Changes**:
- Use `LayeredConfigAdapter` for configuration
- Read `JERRY_PROJECT` from env or local context
- Update local context when project is selected
- Maintain backward compatibility with existing workflow

### CLI Commands (WI-016)

```
src/interface/cli/commands/
└── config_commands.py  # New config command group

Commands:
- jerry config show [--json]
- jerry config get <key>
- jerry config set <key> <value> --scope [project|root]
- jerry config path
```

---

## Backward Compatibility

The following existing behaviors must be preserved:

| Behavior | Current | New |
|----------|---------|-----|
| Project selection | `JERRY_PROJECT` env var | Works unchanged |
| Project discovery | Scans `projects/` | Works unchanged |
| Hook output format | `<project-context>`, `<project-required>` | Works unchanged |

---

## New Capabilities

| Capability | Description |
|------------|-------------|
| Config file loading | Loads `.jerry/config.toml` at root and project level |
| Precedence order | Env > Project > Root > Defaults |
| Local context | Remembers active project in `.jerry/local/context.toml` |
| Config CLI | View and modify configuration via `jerry config` |

---

## Phase Summary

This phase brings together the domain and infrastructure layers into the user-facing CLI. The session hook becomes config-aware, and new `jerry config` commands provide visibility and control over configuration.

---

## Navigation

- **Previous Phase**: [PHASE-03: Domain](PHASE-03-domain.md) and [PHASE-04: Infrastructure](PHASE-04-infrastructure.md)
- **Next Phase**: [PHASE-06: Testing & Validation](PHASE-06-testing.md)
- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
