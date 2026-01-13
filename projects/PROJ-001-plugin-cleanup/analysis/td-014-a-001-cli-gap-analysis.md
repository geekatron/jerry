# TD-014-A-001: CLI Gap Analysis

> **Analysis Task:** TD-014.A1
> **Date:** 2026-01-12
> **Input:** TD-014.R1, TD-014.R2, TD-014.R3
> **Status:** COMPLETE

---

## Executive Summary

This analysis synthesizes findings from three research documents to determine:
1. What CLI commands can be implemented NOW (v0.0.1)
2. What is BLOCKED due to missing application layer
3. What is the minimum viable CLI for v0.0.1 release

**Key Finding:** Jerry v0.0.1 can ship with a **minimal CLI** that exposes the 4 existing queries. Full work tracking CLI requires application layer commands that don't yet exist.

---

## Gap Analysis Matrix

### Layer 1: Domain → Application

| Domain Capability | Application Use Case | Gap |
|------------------|---------------------|-----|
| `WorkItem.create()` | Command (TBD) | **MISSING** |
| `WorkItem.start_work()` | Command (TBD) | **MISSING** |
| `WorkItem.complete()` | Command (TBD) | **MISSING** |
| `WorkItem.block()` | Command (TBD) | **MISSING** |
| `WorkItem.cancel()` | Command (TBD) | **MISSING** |
| `Session.create()` | Command (TBD) | **MISSING** |
| `Session.link_project()` | Command (TBD) | **MISSING** |
| `Session.complete()` | Command (TBD) | **MISSING** |
| `ProjectInfo` read | `GetProjectContextQuery` | **READY** |
| `ProjectInfo` list | `ScanProjectsQuery` | **READY** |
| `ProjectInfo` validate | `ValidateProjectQuery` | **READY** |
| Next project number | `GetNextProjectNumberQuery` | **READY** |

### Layer 2: Application → CLI

| Use Case | CLI Command | Implementation Status |
|----------|-------------|----------------------|
| `GetProjectContextQuery` | `jerry init` | Ready to implement |
| `ScanProjectsQuery` | `jerry projects list` | Ready to implement |
| `ValidateProjectQuery` | `jerry projects validate <id>` | Ready to implement |
| `GetNextProjectNumberQuery` | (internal use) | Ready to implement |
| WorkItem Commands | `jerry items *` | **BLOCKED** (no commands) |
| Session Commands | `jerry session *` | **BLOCKED** (no commands) |

---

## v0.0.1 Minimum Viable CLI

Based on the gap analysis, v0.0.1 should ship with:

### Must Have (MVP)

| Command | Use Case | Purpose |
|---------|----------|---------|
| `jerry --help` | - | Display available commands |
| `jerry --version` | - | Display version info |
| `jerry init` | `GetProjectContextQuery` | Initialize/display project context |
| `jerry projects list` | `ScanProjectsQuery` | List available projects |
| `jerry projects validate <id>` | `ValidateProjectQuery` | Validate project structure |

### Nice to Have (v0.0.2)

| Command | Dependency | Blocker |
|---------|------------|---------|
| `jerry session start` | Session Commands | Application layer |
| `jerry session end` | Session Commands | Application layer |
| `jerry items create` | WorkItem Commands | Application layer |
| `jerry items list` | WorkItem Queries | Application layer |
| `jerry link-artifact` | TD-010 | CLI infrastructure |

---

## Implementation Strategy

### Phase 1: CLI Infrastructure (TD-014.I1)

Create `src/interface/cli/main.py` with:

1. **Entry point**: `def main()` function that pyproject.toml references
2. **Argument parser**: Using stdlib `argparse` (zero-dependency core)
3. **Command routing**: Dispatch to command handlers
4. **Factory composition**: Wire dependencies like `session_start.py` does

### Phase 2: Command Groups (TD-014.I2)

Organize commands hierarchically:

```
jerry
├── init              # GetProjectContextQuery
├── projects
│   ├── list          # ScanProjectsQuery
│   └── validate      # ValidateProjectQuery
└── (future: session, items)
```

### Phase 3: Tests (TD-014.T1)

| Test Type | Location | Count (Est.) |
|-----------|----------|--------------|
| Unit | `tests/interface/cli/unit/` | ~15 |
| Integration | `tests/interface/cli/integration/` | ~10 |
| Architecture | `tests/interface/cli/architecture/` | ~5 |

---

## Hexagonal Architecture Compliance

### First Principles Checklist

| Principle | CLI Compliance |
|-----------|----------------|
| Adapters are stupid | CLI only translates CLI protocol → use cases |
| Ports define capabilities | CLI imports from application ports |
| Use Cases are behavioral | CLI calls Query/Command use cases |
| Domain owns invariants | CLI does NOT validate business rules |
| Dependencies point inward | CLI → Application → Domain (never reverse) |

### Factory Composition Pattern

```python
# src/interface/cli/main.py (conceptual)
def main():
    # Parse CLI arguments
    args = parse_args()

    # Create dependencies (composition root)
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Execute use case
    if args.command == "init":
        query = GetProjectContextQuery(repository, environment, base_path)
        result = query.execute()
        output(result)  # Translate to CLI format
```

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing entry point breaks `pip install` | HIGH | Implement immediately (TD-014.I1) |
| No work tracking CLI | MEDIUM | Document as v0.0.2 feature |
| Users expect `jerry` command to work | HIGH | Minimal MVP must work |

---

## Recommendations

1. **Implement minimal CLI for v0.0.1** with 5 commands (help, version, init, projects list, projects validate)
2. **Fix pyproject.toml entry point** as first priority (DISC-006 resolution)
3. **Follow factory composition pattern** from `session_start.py`
4. **Defer work tracking CLI** to v0.0.2 when application layer commands exist
5. **Create ADR-CLI-001** documenting design decisions

---

## Next Steps

1. **TD-014.D1**: Create ADR-CLI-001 with design decisions
2. **TD-014.I1**: Implement `src/interface/cli/main.py`
3. **TD-014.I2**: Implement command groups (projects subcommand)
4. **TD-014.T1**: Write tests (unit, integration, architecture)
5. **TD-014.V1**: Verify `pip install -e .` and `jerry --help`

---

## Document Lineage

| Artifact | Relationship |
|----------|--------------|
| TD-014 | Parent tech debt item |
| TD-014.R1 | Input: Use case inventory |
| TD-014.R2 | Input: Domain capabilities |
| TD-014.R3 | Input: Knowledge base patterns |
| TD-014.D1 | Next: ADR-CLI-001 design |
