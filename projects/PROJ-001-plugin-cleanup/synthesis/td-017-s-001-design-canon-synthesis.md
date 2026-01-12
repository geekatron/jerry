# TD-017-S-001: Design Canon Synthesis

> **Type**: Synthesis Document
> **Date**: 2026-01-11
> **Author**: Claude (Opus 4.5) - Orchestrator
> **Task**: TD-017 - Comprehensive Design Canon
> **Entry ID**: td-017-s-001
> **Status**: COMPLETE

---

## Executive Summary

This synthesis consolidates findings from 5 parallel research streams (td-017-e-002 through td-017-e-006) into actionable updates for Jerry's design documentation. The research phase followed a fan-out pattern with parallel agents investigating distinct topics; this synthesis follows the fan-in pattern to unify findings.

### Key Synthesis Findings

| Gap | Research Source | Jerry Alignment | Action Required |
|-----|-----------------|-----------------|-----------------|
| GAP-001 | td-017-e-002 (BC Patterns) | ALIGNED | Document BC structure formally |
| GAP-002 | td-017-e-003 (Flat Structure) | ALIGNED | Add PAT-ARCH-004 pattern |
| GAP-003 | td-017-e-004 (Hexagonal) | ALIGNED | Document TD-015 patterns |
| GAP-004 | td-017-e-005 (CQRS Naming) | ALIGNED | Minor verb standardization |
| GAP-005 | td-017-e-006 (Claude Code) | GAPS FOUND | Reduce CLAUDE.md verbosity |

### Synthesis Verdict

**Jerry's architecture is sound.** Research confirms that our patterns align with industry best practices from Cockburn, Martin, Evans, and modern implementations. The gaps identified are documentation gaps, not architectural gaps.

---

## 1. Bounded Context Organization (td-017-e-002)

### Research Findings

| Finding | Industry Pattern | Jerry Implementation | Status |
|---------|------------------|---------------------|--------|
| BC Directory Structure | Layered per BC (domain/application/infrastructure) | Matches exactly | ALIGNED |
| BC Independence | Each BC is "mini application" | Our BC design follows this | ALIGNED |
| Shared Kernel | Small, jointly-maintained, data structures only | `src/shared_kernel/` is correctly scoped | ALIGNED |
| Context Mapping | 9 patterns (Partnership, ACL, etc.) | Partially implemented | ENHANCEMENT |

### Jerry Opinion Preservation

> **Jerry Decision**: We use `session_management`, `work_tracking` as BC names rather than generic "Identity & Access", "Work Management" because they better describe our implementation scope.

### Actions

1. **Add PAT-ARCH-003 Enhancement**: Expand bounded context documentation with:
   - BC creation checklist
   - Context map diagram
   - Inter-BC communication patterns

2. **Create BC Template Script**: `scripts/create_bounded_context.py` (optional future enhancement)

---

## 2. One-Class-Per-File Pattern (td-017-e-003)

### Research Findings

| Finding | Industry Pattern | Jerry Implementation | Status |
|---------|------------------|---------------------|--------|
| Python idiom | "One idea per file" | We use one-class-per-file | INTENTIONAL DEVIATION |
| Java/C# mandate | One public class per file | We follow this for LLM benefits | ALIGNED |
| LLM Navigation | Predictable file-to-class mapping | Exactly why we chose this | ALIGNED |
| Exceptions | Related small value objects, domain events | We allow these exceptions | ALIGNED |

### Jerry Opinion Preservation

> **Jerry Decision**: We intentionally deviate from Python's "one idea per file" tradition because one-class-per-file optimizes for LLM agent navigation. This is a deliberate architectural choice, not ignorance of Python conventions.

### Actions

1. **Add PAT-ARCH-004**: New pattern for one-class-per-file with:
   - Rationale (LLM optimization, CQRS alignment, merge conflict reduction)
   - File naming conventions
   - Exceptions policy
   - Architecture test for enforcement

---

## 3. Hexagonal Architecture Patterns (td-017-e-004)

### Research Findings

| Finding | Industry Pattern | Jerry Implementation | Status |
|---------|------------------|---------------------|--------|
| Layer Dependencies | Inner layers define ports, outer layers implement | Bootstrap + CLIAdapter pattern | ALIGNED |
| Port Classification | Primary (driving) vs Secondary (driven) | `ports/primary/` and `ports/secondary/` | ALIGNED |
| Composition Root | Single location for all wiring | `src/bootstrap.py` | ALIGNED |
| Adapter Naming | `{Tech}{Entity}Adapter` | FilesystemProjectAdapter, etc. | ALIGNED |

### Jerry Opinion Preservation

> **Jerry Decision**: We use constructor injection with factory functions (no DI container) for simplicity. This is a deliberate choice for a framework of our size.

### Actions

1. **Document TD-015 Patterns**: Add to pattern catalog:
   - PAT-CQRS-004: Dispatcher Pattern
   - PAT-ARCH-005: Composition Root Pattern
   - PAT-ARCH-006: CLIAdapter Pattern

2. **Ensure Architecture Standards Has**: Dependency matrix, port classification, composition root rules

---

## 4. CQRS Naming Conventions (td-017-e-005)

### Research Findings

| Element | Industry Pattern | Jerry Pattern | Status |
|---------|------------------|---------------|--------|
| Commands | `{Verb}{Noun}Command` | `CreateTaskCommand` | ALIGNED |
| Queries | `{Verb}{Noun}Query` | `RetrieveProjectContextQuery` | ALIGNED |
| Events | `{Noun}{PastVerb}` (no "Was") | `TaskCreated` | ALIGNED |
| Handlers | `{Name}Handler` | `CreateTaskCommandHandler` | ALIGNED |
| File naming | snake_case version of class | `create_task_command.py` | ALIGNED |

### Query Verb Guidelines

| Scenario | Recommended Verb | Example |
|----------|------------------|---------|
| Single entity by ID | `Get` or `Retrieve` | `RetrieveProjectContextQuery` |
| Collection (paginated) | `List` | `ListTasksQuery` |
| Discovery/scan | `Scan` | `ScanProjectsQuery` |
| Validation | `Validate` | `ValidateProjectQuery` |

### Actions

1. **Update Architecture Standards**: Add query verb decision matrix
2. **Document Event Naming**: Confirm `{Noun}{PastVerb}` without "Was" prefix

---

## 5. Claude Code Rules Best Practices (td-017-e-006)

### Research Findings

| Finding | Industry Best Practice | Jerry Current State | Gap Level |
|---------|----------------------|---------------------|-----------|
| CLAUDE.md length | 100-200 lines max | ~400+ lines | MEDIUM |
| Rules total | <200 lines total | ~800+ lines (4 files) | LARGE |
| Progressive disclosure | Pointer files, not full content | We do this well | ALIGNED |
| Path scoping | Scope rules to file patterns | Not used | ENHANCEMENT |

### Recommendations from Research

| ID | Recommendation | Priority | Effort |
|----|----------------|----------|--------|
| R1 | Restructure CLAUDE.md as index with `@path` imports | HIGH | LOW |
| R2 | Add path scoping to testing-standards.md | MEDIUM | LOW |
| R3 | Consider skill format for Pattern Catalog | LOW | HIGH |
| R4 | Move session-specific content to project CLAUDE.md | MEDIUM | LOW |

### Jerry Opinion Preservation

> **Jerry Decision**: We intentionally have detailed rules because reproducibility is critical for AI agents. However, we can use `@path` imports to load them on-demand rather than front-loading everything.

### Actions

1. **Review CLAUDE.md**: Consider restructuring to use `@path` imports
2. **Add Path Scoping**: For testing-standards.md (`tests/**/*.py`)
3. **Defer Skill Format**: Pattern Catalog works well as-is

---

## 6. New Patterns to Add to Catalog

Based on synthesis, add the following patterns to `.claude/patterns/PATTERN-CATALOG.md`:

### PAT-ARCH-004: One-Class-Per-File (Flat Structure)

```markdown
### PAT-ARCH-004: One-Class-Per-File (Flat Structure)
**Status**: MANDATORY | **Category**: Architecture

**Intent**: Each Python file contains exactly one public class/protocol.

**Rationale**:
- Predictable file-to-class mapping for LLM navigation
- Reduced merge conflicts in multi-agent workflows
- IDE go-to-definition works cleanly
- Aligns with CQRS implementations

**File Naming**: snake_case version of class name

**Exceptions**:
- Related small value objects (same concept)
- Domain events for same aggregate
- Exception hierarchies

**Industry Prior Art**:
- Java Language Specification (public class naming)
- AWS Hexagonal Architecture Guide

**Jerry Opinion**: We intentionally deviate from Python's "one idea per file" tradition for LLM optimization.
```

### PAT-CQRS-004: Dispatcher Pattern

```markdown
### PAT-CQRS-004: Dispatcher Pattern
**Status**: MANDATORY | **Category**: CQRS

**Intent**: Route commands/queries to registered handlers without direct coupling.

**Structure**:
- `IQueryDispatcher` / `ICommandDispatcher` ports
- `QueryDispatcher` / `CommandDispatcher` implementations
- Handler registration at composition root

**Implementation**:
```python
class QueryDispatcher:
    def register(self, query_type: type, handler: Callable) -> None: ...
    def dispatch(self, query: Query) -> Any: ...
```

**Industry Prior Art**:
- MediatR (.NET) - [jbogard/mediatr](https://github.com/jbogard/mediatr)
- Cosmic Python - [Chapter 12: CQRS](https://www.cosmicpython.com/book/chapter_12_cqrs.html)
```

### PAT-ARCH-005: Composition Root Pattern

```markdown
### PAT-ARCH-005: Composition Root Pattern
**Status**: MANDATORY | **Category**: Architecture

**Intent**: Single location (`bootstrap.py`) where all dependencies are wired.

**Rules**:
1. Only `bootstrap.py` may instantiate infrastructure adapters
2. Adapters receive dependencies via constructor injection
3. No adapter self-instantiates its dependencies
4. Factory functions return fully-wired components

**Implementation**: `src/bootstrap.py`

**Industry Prior Art**:
- Robert C. Martin - Clean Architecture (2017)
- Szymon Miks - [Hexagonal Architecture in Python](https://blog.szymonmiks.pl/p/hexagonal-architecture-in-python/)
```

---

## 7. Updates to .claude/rules/

### architecture-standards.md Updates

1. Add Bounded Context section with:
   - Context map diagram
   - BC creation checklist
   - Inter-BC communication patterns

2. Add Composition Root section with:
   - Factory function examples
   - Dependency injection rules

3. Add Dispatcher section with:
   - Registration pattern
   - Handler invocation

### file-organization.md Updates

1. Expand One-Class-Per-File section with:
   - Decision criteria for grouping
   - Anti-patterns to avoid
   - Exception examples

### testing-standards.md Updates

1. Add path scoping frontmatter:
```yaml
---
paths:
  - "tests/**/*.py"
---
```

---

## 8. Implementation Checklist

### Immediate Actions (TD-017.I-001)

- [ ] Add PAT-ARCH-004 to Pattern Catalog
- [ ] Add PAT-CQRS-004 to Pattern Catalog
- [ ] Add PAT-ARCH-005 to Pattern Catalog
- [ ] Update architecture-standards.md with BC section
- [ ] Update architecture-standards.md with Composition Root section
- [ ] Verify all patterns have industry citations

### Future Enhancements (Backlog)

- [ ] Consider CLAUDE.md restructuring with `@path` imports
- [ ] Add path scoping to testing-standards.md
- [ ] Create BC template script (optional)
- [ ] Formalize IntegrationEvent pattern

---

## 9. Research Sources Consolidated

### Primary Sources (Authoritative)

| Source | Author | Topic | URL |
|--------|--------|-------|-----|
| Hexagonal Architecture | Alistair Cockburn | Original pattern | [cockburn.us](https://alistair.cockburn.us/hexagonal-architecture/) |
| Clean Architecture | Robert C. Martin | Layer rules | [blog.cleancoder.com](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) |
| CQRS | Martin Fowler | Pattern definition | [martinfowler.com](https://www.martinfowler.com/bliki/CQRS.html) |
| Bounded Context | Eric Evans | DDD concept | [martinfowler.com](https://martinfowler.com/bliki/BoundedContext.html) |

### Implementation References

| Source | Topic | URL |
|--------|-------|-----|
| Domain-Driven Hexagon | Python DDD | [GitHub](https://github.com/sairyss/domain-driven-hexagon) |
| MediatR | Dispatcher pattern | [GitHub](https://github.com/jbogard/mediatr) |
| Cosmic Python | CQRS in Python | [Book](https://www.cosmicpython.com/) |
| AWS Hexagonal | Lambda architecture | [AWS Docs](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/structure-a-python-project-in-hexagonal-architecture-using-aws-lambda.html) |

### Claude Code Configuration

| Source | Topic | URL |
|--------|-------|-----|
| Claude Code Memory | Configuration | [code.claude.com](https://code.claude.com/docs/en/memory) |
| Claude Code Best Practices | CLAUDE.md | [anthropic.com](https://www.anthropic.com/engineering/claude-code-best-practices) |
| Skill Best Practices | Skill authoring | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

---

## 10. Conclusion

The TD-017 research phase confirms that Jerry's architecture is well-aligned with industry best practices. The gaps identified are primarily documentation gaps that can be addressed by:

1. Adding 3 new patterns to the catalog (PAT-ARCH-004, PAT-CQRS-004, PAT-ARCH-005)
2. Expanding existing rules files with BC organization and composition root details
3. Adding industry citations to all patterns

The implementation phase (TD-017.I-001, TD-017.I-002) should proceed with updating the pattern catalog and rules files.

---

*Synthesis completed by Claude (Opus 4.5) as part of TD-017 fan-in phase*
*Date: 2026-01-11*
*Status: COMPLETE - Ready for implementation*
