# TD-017-E-003: One-Class-Per-File (Flat Structure) Patterns

> **Type**: Research Evidence
> **Date**: 2026-01-11
> **Researcher**: Claude (Opus 4.5)
> **Task**: TD-017 - Comprehensive Design Canon
> **Entry ID**: td-017-e-003

---

## Executive Summary

This research investigates industry best practices for one-class-per-file organization in Python projects. The findings reveal a nuanced landscape: while Python's community tradition favors "one idea per file" over strict one-class-per-file (as in Java/C#), emerging AI-assisted development patterns and Clean Architecture implementations provide compelling reasons for Jerry's adoption of flat file structure.

**Key Findings**:
1. Traditional Python favors module-based organization ("one idea per file")
2. Java/C# mandate one-class-per-file for versioning and tooling benefits
3. AI coding assistants (Claude Code, Cursor) benefit from predictable file-to-class mapping
4. Hexagonal/Clean Architecture implementations often adopt flat structure for clarity
5. Jerry's current approach is well-justified for LLM-navigable codebases

**Recommendation**: Jerry should preserve its one-class-per-file pattern with documented exceptions, as it optimizes for AI agent navigation while maintaining Clean Architecture principles.

---

## 1. Industry Pattern Definition

### 1.1 What is "Flat Structure"?

**Flat Structure** (also called "one-class-per-file") is a code organization pattern where each source file contains exactly one public class, interface, or protocol. The file name matches the class name (using the language's naming convention).

```
# Flat Structure Example (Python)
src/application/ports/primary/
├── iquerydispatcher.py        # Contains only IQueryDispatcher
└── icommanddispatcher.py      # Contains only ICommandDispatcher
```

### 1.2 Contrast: Traditional Python Modules

Python's traditional approach groups related functionality into modules ("one idea per file"):

```python
# Traditional Python: decimal.py contains multiple classes
# - Decimal
# - Context
# - DecimalException (and subclasses)
# All revolve around the "decimal" topic
```

**Citations**:
- [Python Standard Library - decimal.py](https://github.com/python/cpython/blob/main/Lib/decimal.py) - Multiple classes grouped by concept
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/) - No mandate on class-per-file, focuses on naming conventions

### 1.3 Java/C# Mandate

In Java, one-class-per-file is enforced by the compiler for public classes. C# follows a similar convention by strong tradition.

**Rationale**:
1. **Compiler enforcement** (Java): "You don't get a choice, because the compiler assumes a class can be found in the correspondingly named file"
2. **Version control optimization**: Each class change is isolated to one file, reducing merge conflicts
3. **IDE navigation**: Go-to-definition works predictably

**Citations**:
- [Java Language Specification](https://docs.oracle.com/javase/specs/) - Public class naming rules
- [C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)

---

## 2. Benefits vs. Traditional Python

### 2.1 Arguments FOR One-Class-Per-File

| Benefit | Description | Jerry Relevance |
|---------|-------------|-----------------|
| **LLM Navigation** | AI agents can predict file locations from class names | HIGH - Jerry is an LLM-first framework |
| **Merge Conflict Reduction** | Parallel edits to different classes don't conflict | MEDIUM - Multi-agent workflows |
| **IDE Go-To-Definition** | Predictable file-to-class mapping | HIGH - Developer experience |
| **Smaller Files** | Each file is focused and readable | MEDIUM - Cognitive load |
| **CQRS Alignment** | Each command/query/handler in its own file | HIGH - Jerry uses CQRS |
| **Test Isolation** | Test file maps 1:1 to source file | HIGH - Testing standards |

### 2.2 Arguments AGAINST (Python Community Perspective)

| Concern | Description | Jerry Mitigation |
|---------|-------------|------------------|
| **Many Small Files** | Difficult to track in large projects | `__init__.py` exports provide module-level API |
| **Against Python Idiom** | "Totally pointless and counterproductive in Python" | Context-specific: AI navigation justifies it |
| **Import Overhead** | More import statements needed | Centralized `__init__.py` exports |
| **Namespace Fragmentation** | Related classes separated | Package structure groups by concept |

**Key Python Community Quote**:
> "Perhaps a better rule of thumb is 'one idea per file.'" - Python Mailing List Discussion

**Citations**:
- [The Hitchhiker's Guide to Python - Structuring Your Project](https://docs.python-guide.org/writing/structure/)
- [Quora Discussion: One Class Per File in Python](https://www.quora.com/Why-in-Python-is-the-convention-to-using-one-class-per-file-not-common-I-thought-it-was-a-universal-good-practice)

### 2.3 The AI Agent Perspective (Emerging Best Practice)

Recent developments in AI-assisted coding have introduced new considerations:

**Claude Code Behavior**:
> "Claude Code maps out the entire structure, dependencies, and relationships between files... it can make intelligent, multi-file edits that actually work because it understands the full context."

**AGENTS.md Pattern**:
> "Using an AGENTS.md file to define project structure (e.g., 'see App.tsx for routes', 'components live in app/components') provides faster results because the agent starts where humans would start."

**Context Management**:
> "LLMs work best with focused, relevant information. Poor context can mean insufficient context (causing AI agents to hallucinate with nonexistent APIs and packages) or context overflow."

**Jerry's Advantage**: One-class-per-file creates a predictable, LLM-friendly codebase where file paths encode semantic meaning.

**Citations**:
- [Anthropic - Claude Code](https://www.claude.com/product/claude-code)
- [Builder.io - AGENTS.md Best Practices](https://www.builder.io/blog/agents-md)
- [DigitalOcean - Context Management for AI Code Generation](https://docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/)

---

## 3. Implementation Guidelines

### 3.1 File Naming Convention

| Type | File Name Pattern | Class Name |
|------|-------------------|------------|
| Aggregate | `work_item.py` | `WorkItem` |
| Value Object | `project_id.py` | `ProjectId` |
| Command | `create_task_command.py` | `CreateTaskCommand` |
| Query | `retrieve_project_query.py` | `RetrieveProjectQuery` |
| Handler | `create_task_command_handler.py` | `CreateTaskCommandHandler` |
| Port (Interface) | `iquerydispatcher.py` | `IQueryDispatcher` |
| Adapter | `filesystem_project_adapter.py` | `FilesystemProjectAdapter` |

**Rule**: File name is snake_case version of class name.

### 3.2 Directory Structure

```
src/application/handlers/
├── __init__.py              # Exports public API
├── commands/
│   ├── __init__.py
│   ├── create_task_command_handler.py
│   └── complete_task_command_handler.py
└── queries/
    ├── __init__.py
    ├── retrieve_project_query_handler.py
    └── scan_projects_query_handler.py
```

### 3.3 `__init__.py` Export Pattern

Each `__init__.py` explicitly exports the public API, maintaining Python's module abstraction:

```python
# src/application/handlers/__init__.py
from src.application.handlers.commands.create_task_command_handler import (
    CreateTaskCommandHandler,
)
from src.application.handlers.queries.retrieve_project_query_handler import (
    RetrieveProjectQueryHandler,
)

__all__ = [
    "CreateTaskCommandHandler",
    "RetrieveProjectQueryHandler",
]
```

**Benefit**: External consumers can import from the package level:
```python
from src.application.handlers import CreateTaskCommandHandler
```

### 3.4 Wemake Python Styleguide Alignment

The Wemake Python Styleguide provides validation for module complexity:

```python
# WPS202: Found too many module members: {0}
# Default --max-module-members: 7
```

This aligns with one-class-per-file: if a module has too many classes/functions, it should be split.

**Citations**:
- [Wemake Python Styleguide](https://wemake-python-styleguide.readthedocs.io/)

---

## 4. Exceptions Policy

### 4.1 When Grouping is Acceptable

| Exception | Rationale | Example |
|-----------|-----------|---------|
| **Related Small Value Objects** | Cohesive concept, often used together | `Priority` enum + `PriorityLevel` type alias |
| **Domain Events for Same Aggregate** | Logically coupled, share context | `TaskCreated`, `TaskCompleted` in `task_events.py` |
| **Exception Hierarchy** | All exceptions for a domain | `DomainError`, `WorkItemNotFoundError` in `exceptions.py` |
| **Type Aliases** | Supporting types for main class | Type definitions alongside primary class |
| **Test Fixtures** | Shared test setup | `conftest.py` with multiple fixtures |

### 4.2 Decision Criteria

Apply these questions to determine if grouping is appropriate:

1. **Are the classes always used together?** If yes, group is acceptable.
2. **Would separating cause import chains?** If yes, group is acceptable.
3. **Is the total file under 200 lines?** If no, split required.
4. **Do the classes represent a single concept?** If yes, group is acceptable.
5. **Would an LLM naturally look for them together?** If yes, group is acceptable.

### 4.3 Anti-Patterns (Always Avoid)

| Anti-Pattern | Why Problematic |
|--------------|-----------------|
| Multiple aggregates in one file | Each aggregate is a consistency boundary |
| Port + Adapter in same file | Violates dependency inversion |
| Command + Handler in same file | Different lifecycle and testing needs |
| Multiple unrelated protocols | No cohesive concept |

---

## 5. Jerry-Specific Recommendations

### 5.1 Preserve Current Pattern

Jerry's one-class-per-file approach is well-justified and should be preserved:

**Rationale**:
1. **LLM Optimization**: Jerry is designed for Claude Code and AI agent workflows. Predictable file-to-class mapping improves agent navigation accuracy.
2. **CQRS Alignment**: Each command, query, and handler in its own file matches Clean Architecture patterns used in production C#/Java systems.
3. **Multi-Agent Workflows**: Reduced merge conflicts when multiple agents edit the codebase.
4. **Testing Clarity**: Test file maps directly to source file.

### 5.2 Formalize as Pattern

Add to Pattern Catalog (`.claude/patterns/PATTERN-CATALOG.md`):

```markdown
## PAT-ARCH-004: One-Class-Per-File (Flat Structure)

**Intent**: Each Python file contains exactly one public class/protocol.

**Rationale**:
- Predictable file-to-class mapping for LLM navigation
- Reduced merge conflicts in multi-agent workflows
- IDE go-to-definition works cleanly
- Aligns with Java/C# conventions for CQRS implementations

**Structure**:
- File name: snake_case version of class name
- Package `__init__.py`: Explicit exports of public API
- Directory structure: Group by layer, then by type

**Exceptions**:
- Related small value objects (same concept)
- Domain events for same aggregate
- Exception hierarchies

**Enforcement**:
- Architecture tests validate one public class per file
- Wemake WPS202 (max-module-members: 7) as soft limit
```

### 5.3 Update Rules Files

The existing `.claude/rules/file-organization.md` already documents this pattern. Ensure cross-reference to Pattern Catalog:

```markdown
## One Class Per File Rule

**MANDATORY**: Each Python file contains exactly ONE public class/protocol.

See: **PAT-ARCH-004** in Pattern Catalog for full specification.
```

### 5.4 Architecture Test

Add to `tests/architecture/test_layer_boundaries.py`:

```python
def test_one_class_per_file():
    """Each Python file should contain at most one public class."""
    for file in Path("src").rglob("*.py"):
        if file.name == "__init__.py":
            continue
        public_classes = count_public_classes(file)
        assert public_classes <= 1, f"{file} has {public_classes} public classes"
```

---

## 6. Industry Comparison

### 6.1 Framework Survey

| Framework | Pattern | Notes |
|-----------|---------|-------|
| **Django** | One idea per file | `models.py`, `views.py` can have many classes |
| **FastAPI** | Module-based | Routers, models, schemas grouped by domain |
| **Flask** | Flexible | Blueprints encourage separation |
| **Hexagonal Python** | Flat structure | AWS recommends separate files for ports/adapters |
| **Clean Architecture (Python)** | Often flat | GitHub examples show one-class-per-file |

### 6.2 Hexagonal Architecture Alignment

AWS Prescriptive Guidance recommends:

```
app/
├── adapters/          # Each adapter in separate file
├── entrypoints/       # Entry points separated
├── domain/
│   ├── command_handlers/  # One handler per file
│   └── ...
```

**Citation**:
- [AWS - Structure Python Project in Hexagonal Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/structure-a-python-project-in-hexagonal-architecture-using-aws-lambda.html)

---

## 7. Conclusion

Jerry's one-class-per-file pattern is a deliberate architectural choice optimized for:

1. **AI Agent Navigation**: Predictable file locations from class names
2. **Clean Architecture**: CQRS elements (commands, queries, handlers) in separate files
3. **Multi-Agent Development**: Reduced merge conflicts
4. **Testing Clarity**: 1:1 mapping between source and test files

While this deviates from traditional Python idioms ("one idea per file"), the emergence of AI-assisted development and the specific needs of Hexagonal Architecture justify this approach.

**Recommendation**: Preserve the pattern, formalize as PAT-ARCH-004, and add architecture tests for enforcement.

---

## References

### Primary Sources

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [The Hitchhiker's Guide to Python - Project Structure](https://docs.python-guide.org/writing/structure/)
- [Python Packaging User Guide - Src Layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Wemake Python Styleguide](https://wemake-python-styleguide.readthedocs.io/)

### Hexagonal/Clean Architecture

- [AWS - Hexagonal Architecture with Python](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/structure-a-python-project-in-hexagonal-architecture-using-aws-lambda.html)
- [Clean Architecture Python Example (GitHub)](https://github.com/Enforcer/clean-architecture)
- [Hexagonal Architecture in Python (Szymon Miks)](https://blog.szymonmiks.pl/p/hexagonal-architecture-in-python/)
- [Python Design Patterns for Clean Architecture (Rost Glukhov)](https://www.glukhov.org/post/2025/11/python-design-patterns-for-clean-architecture/)

### AI-Assisted Development

- [Claude Code - Anthropic](https://www.claude.com/product/claude-code)
- [Claude Code vs Cursor Comparison (Qodo)](https://www.qodo.ai/blog/claude-code-vs-cursor/)
- [AGENTS.md Best Practices (Builder.io)](https://www.builder.io/blog/agents-md)
- [Context Management for AI Code Generation (DigitalOcean)](https://docs.digitalocean.com/products/gradient-ai-platform/concepts/context-management/)
- [How I Code With LLMs (Honeycomb)](https://www.honeycomb.io/blog/how-i-code-with-llms-these-days/)

### Community Discussions

- [Why One Class Per File Not Common in Python (Quora)](https://www.quora.com/Why-in-Python-is-the-convention-to-using-one-class-per-file-not-common-I-thought-it-was-a-universal-good-practice)
- [Benefits of One Class Per File (Quora)](https://www.quora.com/What-are-the-benefits-of-having-only-one-class-per-file-instead-of-multiple-classes-in-one-file-What-can-happen-if-we-dont-follow-this-rule)
- [Python Mailing List - One Class Per File](https://python-list.python.narkive.com/iphg8nWr/one-class-per-file)

### FastAPI/Django Organization

- [FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI Best Practices (GitHub)](https://github.com/zhanymkanov/fastapi-best-practices)
- [Django Folder and File Structure Best Practices 2025](https://studygyaan.com/django/best-practice-to-structure-django-project-directories-and-files)

---

## Appendix: Jerry's Current Implementation

### File Organization Example

From `.claude/rules/file-organization.md`:

```
src/application/handlers/
├── __init__.py
├── commands/
│   ├── __init__.py
│   ├── create_task_command_handler.py
│   └── complete_task_command_handler.py
└── queries/
    ├── __init__.py
    ├── retrieve_project_context_query_handler.py
    └── validate_project_query_handler.py
```

### Current Exception Example

From Jerry codebase:

```python
# src/domain/events/task_events.py
# Contains: TaskCreated, TaskCompleted
# Rationale: Both events belong to same aggregate (Task)
```

This exception is documented and follows the "same aggregate" rule.
