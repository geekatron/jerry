# ADR-CLI-002: Phase 4 CLI Namespace Implementation

> **Status:** ACCEPTED
> **Date:** 2026-01-12
> **Decision Makers:** Claude, User
> **Supersedes:** ADR-CLI-001 D6 (refinement)
> **Related:** PHASE4-R-001 (5W1H research), TD-015

---

## Context

ADR-CLI-001 D6 established the principle of CLI namespaces per bounded context. This ADR details the specific implementation for Phase 4, which refactors the current flat CLI structure into a namespaced hierarchy.

### Current State

```bash
jerry init                      # Project context
jerry projects list             # List projects
jerry projects validate <id>    # Validate project
```

### Target State (v0.1.0)

```bash
jerry session start/end/status/abandon
jerry items create/list/show/start/complete/block/cancel
jerry projects list/validate/context
```

---

## Decision

### D1: Namespace Structure

**Three namespaces aligned with bounded contexts:**

| Namespace | Bounded Context | Primary Aggregate |
|-----------|-----------------|-------------------|
| `session` | session_management | Session |
| `items` | work_tracking | WorkItem |
| `projects` | session_management | ProjectInfo |

**Note:** "items" was chosen over "worktracker" for conciseness and user ergonomics.

### D2: Command Mapping

#### Session Namespace

| Command | Aggregate Method | Application Handler |
|---------|------------------|---------------------|
| `session start` | `Session.create()` | `CreateSessionCommandHandler` |
| `session end` | `Session.complete()` | `EndSessionCommandHandler` |
| `session status` | Query | `GetSessionStatusQueryHandler` |
| `session abandon` | `Session.abandon()` | `AbandonSessionCommandHandler` |

#### Items Namespace

| Command | Aggregate Method | Application Handler |
|---------|------------------|---------------------|
| `items create` | `WorkItem.create()` | `CreateWorkItemCommandHandler` |
| `items list` | Query | `ListWorkItemsQueryHandler` |
| `items show` | Query | `GetWorkItemQueryHandler` |
| `items start` | `WorkItem.start_work()` | `StartWorkItemCommandHandler` |
| `items complete` | `WorkItem.complete()` | `CompleteWorkItemCommandHandler` |
| `items block` | `WorkItem.block()` | `BlockWorkItemCommandHandler` |
| `items cancel` | `WorkItem.cancel()` | `CancelWorkItemCommandHandler` |

#### Projects Namespace

| Command | Current | Change |
|---------|---------|--------|
| `projects list` | EXISTS | MOVE |
| `projects validate` | EXISTS | MOVE |
| `projects context` | `jerry init` | RENAME |

### D3: Breaking Change Strategy

**Option B Selected: Breaking change to v0.1.0**

| Old Command | New Command | Migration |
|-------------|-------------|-----------|
| `jerry init` | `jerry projects context` | REMOVED |
| `jerry projects list` | `jerry projects list` | SAME |
| `jerry projects validate <id>` | `jerry projects validate <id>` | SAME |

**Rationale:**
- Pre-v1.0, no external users
- Minimal existing commands (3 total)
- Clean slate for proper architecture
- Skills/docs updated simultaneously

### D4: Implementation Architecture

```
src/interface/cli/
├── main.py                    # Entry point (thin routing)
├── parser.py                  # argparse namespace setup
├── adapter.py                 # CLIAdapter with namespace methods
└── commands/                  # Command group modules
    ├── session.py             # Session namespace
    ├── items.py               # Items namespace
    └── projects.py            # Projects namespace
```

### D5: Dependency Injection

**Adapter receives dispatchers from composition root:**

```python
# src/bootstrap.py
def create_cli_adapter() -> CLIAdapter:
    query_dispatcher = create_query_dispatcher()
    command_dispatcher = create_command_dispatcher()
    return CLIAdapter(query_dispatcher, command_dispatcher)

# src/interface/cli/adapter.py
class CLIAdapter:
    def __init__(
        self,
        query_dispatcher: IQueryDispatcher,
        command_dispatcher: ICommandDispatcher,
    ) -> None:
        self._query_dispatcher = query_dispatcher
        self._command_dispatcher = command_dispatcher
```

### D6: Output Formats

**Three formats supported:**

| Format | Flag | Default | Use Case |
|--------|------|---------|----------|
| Text | (default) | YES | Human terminal |
| JSON | `--json` | NO | AI/automation |
| TOON | `--toon` | NO | Future (token-efficient) |

### D7: Application Layer Requirements

**New handlers required (must be created):**

| Handler | Type | Priority |
|---------|------|----------|
| `CreateSessionCommandHandler` | Command | HIGH |
| `EndSessionCommandHandler` | Command | HIGH |
| `AbandonSessionCommandHandler` | Command | MEDIUM |
| `GetSessionStatusQueryHandler` | Query | HIGH |
| `CreateWorkItemCommandHandler` | Command | HIGH |
| `ListWorkItemsQueryHandler` | Query | HIGH |
| `GetWorkItemQueryHandler` | Query | HIGH |
| `StartWorkItemCommandHandler` | Command | MEDIUM |
| `CompleteWorkItemCommandHandler` | Command | MEDIUM |
| `BlockWorkItemCommandHandler` | Command | MEDIUM |
| `CancelWorkItemCommandHandler` | Command | LOW |

---

## Implementation Order

### Phase 4.1: Parser Infrastructure (RED)

1. Create `src/interface/cli/parser.py`
2. Write tests for parser structure
3. Implement namespace subparsers

### Phase 4.2: Projects Namespace (GREEN)

1. Migrate existing commands to projects namespace
2. Rename `init` to `projects context`
3. Update tests

### Phase 4.3: Session Namespace (Priority 1)

1. Create application layer handlers (Commands + Queries)
2. Implement CLI commands
3. Write tests

### Phase 4.4: Items Namespace - Queries

1. Create `ListWorkItemsQueryHandler`
2. Create `GetWorkItemQueryHandler`
3. Implement `items list` and `items show`

### Phase 4.5: Items Namespace - Commands

1. Create command handlers incrementally
2. Implement CLI commands
3. Write tests

### Phase 4.6: Integration & Documentation

1. E2E tests for full workflows
2. Update CLAUDE.md
3. Update skills documentation

---

## Consequences

### Positive

1. **Clean Architecture**: CLI properly aligned with bounded contexts
2. **Extensible**: New commands fit naturally in namespaces
3. **Discoverable**: `jerry session --help` shows session commands
4. **Testable**: Each namespace isolated for testing

### Negative

1. **Breaking Change**: Existing scripts need update
2. **More Code**: More files than current flat structure
3. **Application Layer Work**: Many handlers to create

### Neutral

1. **Learning Curve**: Users must learn new structure
2. **Documentation**: Must update all references

---

## Validation Criteria

| Test | Command | Expected |
|------|---------|----------|
| Session help | `jerry session --help` | Shows session commands |
| Items help | `jerry items --help` | Shows items commands |
| Projects context | `jerry projects context` | Shows project context |
| JSON output | `jerry --json projects list` | Valid JSON |
| Version | `jerry --version` | Shows 0.1.0 |

---

## References

- PHASE4-R-001: `research/phase4-cli-e-001-5w1h-namespaces.md`
- ADR-CLI-001: Original CLI architecture
- Context7 Research: Click, Typer, argparse patterns

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | Claude | 2026-01-12 | ACCEPTED |
| Reviewer | User | 2026-01-12 | APPROVED |
