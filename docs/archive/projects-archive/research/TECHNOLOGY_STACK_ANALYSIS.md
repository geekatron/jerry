# Technology Stack Analysis for Jerry Framework

**Document ID**: RESEARCH-001
**Date**: 2026-01-07
**Author**: Claude (Distinguished Systems Engineering Persona)
**Status**: DRAFT - Pending Review

---

## Executive Summary

This document presents an evidence-based analysis of technology stack options for the Jerry framework, a behavior and workflow guardrails system designed to operate within Claude Code Web Research Preview. The primary constraint is the sandboxed, ephemeral cloud environment with pre-installed runtimes.

**Recommendation**: **Python with zero/minimal dependencies** is the optimal choice, with strategic use of stdlib and pre-installed packages only.

---

## 1. Problem Statement

### 1.1 Core Requirements

1. **Runtime Environment**: Must execute within Claude Code Web Research Preview (Anthropic-managed sandbox)
2. **Context Rot Mitigation**: Framework must help survive long-running sessions where context degrades
3. **Work Tracker**: First skill implementation - local Azure DevOps/JIRA equivalent
4. **Hexagonal Architecture**: Domain-Driven Design with Ports & Adapters pattern
5. **Knowledge Accrual**: System must accumulate wisdom, experience, and knowledge over time

### 1.2 The Context Rot Problem

Per Chroma Research and Anthropic's engineering blog:

> "Context Rot is the phenomenon where an LLM's performance degrades as the context window fills up, even when total token count is well within the technical limit."
> — [Chroma Research](https://research.trychroma.com/context-rot)

The effective context window where models perform optimally is often **<256k tokens**, far below advertised limits. This is an architectural reality of transformer attention mechanisms creating n² pairwise relationships.

**Mitigation strategies** (per [Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)):
- Context Offloading (filesystem as infinite memory)
- Context Reduction (compression/summarization)
- Context Retrieval (dynamic loading)
- Context Isolation (separation of concerns)

---

## 2. Environment Constraints Analysis

### 2.1 Claude Code Web Research Preview Specifications

| Aspect | Specification | Source |
|--------|---------------|--------|
| **Execution** | Isolated Gvisor sandbox on Anthropic infrastructure | [Anthropic News](https://www.anthropic.com/news/claude-code-on-the-web) |
| **Base Image** | Ubuntu-based container | [Claude Code Docs](https://code.claude.com/docs/en/claude-code-on-the-web) |
| **Filesystem** | Read/write to working directory only | [Sandboxing Docs](https://code.claude.com/docs/en/sandboxing) |
| **Network** | Configurable: locked down, allowlist, or open | [Claude Code Docs](https://code.claude.com/docs/en/claude-code-on-the-web) |
| **Git** | GitHub only (via secure proxy) | [VentureBeat](https://venturebeat.com/ai/claude-code-comes-to-web-and-mobile-letting-devs-launch-parallel-jobs-on/) |
| **Persistence** | Ephemeral - no state between sessions | [DevToolHub](https://devtoolhub.com/claude-code-on-the-web/) |

### 2.2 Pre-installed Runtimes and Tools

Per [Claude Code Docs](https://code.claude.com/docs/en/claude-code-on-the-web), the cloud image includes:

| Language/Tool | Details |
|--------------|---------|
| **Python** | pip, poetry, NumPy, etc. |
| **Node.js** | npm, yarn, pnpm |
| **Go** | Standard toolchain |
| **Rust** | Cargo |
| **Java** | JDK |
| **C++** | GCC/Clang |
| **Testing** | Frameworks pre-installed |
| **Linters** | Pre-installed |

### 2.3 Dependency Installation

Per documentation, dependencies can be installed via SessionStart hooks:

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "scripts/install_pkgs.sh"
    }]
  }
}
```

**However**, this introduces:
- Session startup latency
- Network dependency (may fail)
- Rate limit consumption
- Potential security exposure via trusted network access

---

## 3. Technology Stack Evaluation

### 3.1 Evaluation Criteria

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Zero-dependency capability** | 35% | Reduces failure modes, startup time |
| **Hexagonal architecture support** | 25% | Core requirement per user spec |
| **Pre-installed ecosystem** | 20% | Leverage existing environment |
| **Context efficiency** | 15% | Code verbosity affects token usage |
| **Developer experience** | 5% | Secondary to reliability |

### 3.2 Python Analysis

#### Strengths

1. **"Batteries Included" Philosophy**
   > "Python is a 'batteries-included' kind of language, and comes with an HTTP server module."
   > — [Drew's Blogsite](https://drewsh.com/minimal-python-server)

2. **Stdlib Capabilities for Our Use Case**:
   - `dataclasses` - Value Objects, Entities (Python 3.7+)
   - `abc` - Abstract Base Classes for Ports
   - `typing` - Type hints, Protocol classes
   - `json` - Serialization
   - `sqlite3` - Persistence (zero external deps)
   - `pathlib` - Filesystem operations
   - `datetime` - Temporal handling
   - `uuid` - Identity generation
   - `collections` - Data structures
   - `contextlib` - Resource management
   - `unittest` - Testing framework

3. **Hexagonal Architecture Support**
   > "In Python, hexagonal architecture can be implemented using Abstract Base Classes (ABCs) for ports and concrete implementations for adapters."
   > — [Software Patterns Lexicon](https://softwarepatternslexicon.com/python/architectural-patterns/hexagonal-architecture-ports-and-adapters/)

4. **Pre-installed in Environment**: Python with pip, poetry, NumPy already available

5. **DDD/CQRS Resources**: Strong community with examples (e.g., [Hexagonal Architecture with Python + FastAPI](https://github.com/marcosvs98/hexagonal-architecture-with-python))

#### Weaknesses

1. **Type System**: Runtime-only checking without external tools (mypy)
2. **Verbosity**: More boilerplate than TypeScript for some patterns
3. **Import System**: Can be confusing for complex package structures

#### Zero-Dependency Feasibility Assessment

| Component | Stdlib Solution | External Alternative |
|-----------|-----------------|---------------------|
| Domain Entities | `dataclasses` | Pydantic |
| Ports (Interfaces) | `abc.ABC`, `typing.Protocol` | N/A |
| Persistence | `sqlite3`, `json` | SQLAlchemy |
| HTTP Server | `http.server` | FastAPI, Flask |
| CLI | `argparse` | Click, Typer |
| Testing | `unittest` | pytest |
| Validation | Manual + `typing` | Pydantic |
| Serialization | `json` | marshmallow |

**Verdict**: **100% stdlib implementation is feasible** for Work Tracker use case.

### 3.3 TypeScript/Node.js Analysis

#### Strengths

1. **Type System**: Compile-time type checking built-in
2. **Strong Hexagonal Examples**: [domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon) - 14k+ stars
3. **Interface Definition**: Native interface/type constructs
4. **Async-First**: Native Promise/async-await patterns

#### Weaknesses

1. **Dependency Culture**
   > "The npm ecosystem traditionally relies heavily on external packages even for basic functionality."

2. **Node.js Stdlib Limitations**:
   - No built-in SQLite (requires `better-sqlite3`)
   - Limited CLI parsing (basic `process.argv`)
   - No built-in testing framework
   - No built-in validation

3. **Zero-Dependency Feasibility**:

| Component | Stdlib Solution | Reality |
|-----------|-----------------|---------|
| Domain Entities | Class + interfaces | Feasible |
| Ports | Interfaces | Feasible |
| Persistence | **None** | Requires `better-sqlite3` or fs-based |
| HTTP Server | `http` module | Feasible but primitive |
| CLI | `process.argv` | Very limited |
| Testing | **None** | Requires Jest/Vitest |
| Validation | **None** | Requires Zod/Joi |

**Verdict**: **Zero-dependency TypeScript is NOT feasible** for Work Tracker without significant compromise.

### 3.4 Comparative Scoring

| Criterion | Weight | Python | TypeScript | Notes |
|-----------|--------|--------|------------|-------|
| Zero-dependency capability | 35% | 9/10 | 4/10 | Python stdlib far superior |
| Hexagonal architecture support | 25% | 8/10 | 9/10 | Both excellent, TS slightly more ergonomic |
| Pre-installed ecosystem | 20% | 9/10 | 8/10 | Both available, Python more complete |
| Context efficiency | 15% | 7/10 | 8/10 | TS slightly more concise |
| Developer experience | 5% | 8/10 | 8/10 | Comparable |
| **Weighted Total** | 100% | **8.25** | **6.55** | |

---

## 4. Hexagonal Architecture Foundation

### 4.1 Original Pattern Definition

Per Alistair Cockburn (pattern creator, 2005):

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."
> — [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)

### 4.2 Core Principles

1. **Application Core Independence**: Business logic has no dependencies on frameworks or external resources
2. **Ports as Contracts**: Abstract interfaces defining interaction points
3. **Adapters as Implementations**: Concrete implementations connecting to external world
4. **Dependency Inversion**: Outer layers depend on inner layers, never reverse

### 4.3 Python Implementation Pattern

```python
# Port (Abstract Interface)
from abc import ABC, abstractmethod
from typing import Protocol

class IWorkItemRepository(Protocol):
    """Secondary Port - Driven by application"""
    def save(self, item: WorkItem) -> None: ...
    def get(self, id: WorkItemId) -> WorkItem | None: ...

# Domain Entity
from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class WorkItem:
    """Aggregate Root"""
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    status: str = "pending"

    def complete(self) -> None:
        if self.status == "completed":
            raise DomainError("Already completed")
        self.status = "completed"

# Adapter (Infrastructure)
class SQLiteWorkItemRepository:
    """Secondary Adapter - Implements Port"""
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def save(self, item: WorkItem) -> None:
        # Implementation
        pass
```

---

## 5. Risk Analysis

### 5.1 Python Zero-Dependency Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Stdlib inadequacy discovered late | Low | High | Proof-of-concept first |
| Performance bottlenecks | Low | Medium | Profile early |
| Type safety gaps | Medium | Medium | Use mypy if available, defensive coding |
| Testing limitations | Low | Medium | unittest is sufficient |

### 5.2 External Dependency Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Package installation failure | Medium | Critical | Zero-dep eliminates |
| Version conflicts | Medium | High | Zero-dep eliminates |
| Network unavailable | Medium | Critical | Zero-dep eliminates |
| Security vulnerabilities | Medium | High | Zero-dep reduces surface |
| Startup latency | High | Medium | Zero-dep eliminates |

---

## 6. Recommendation

### 6.1 Primary Recommendation

**Adopt Python with zero/minimal external dependencies.**

Rationale:
1. **Reliability**: No network dependency for package installation
2. **Simplicity**: Reduced complexity and failure modes
3. **Alignment**: Python's stdlib philosophy matches our constraints
4. **Feasibility**: All required components achievable with stdlib
5. **Environment**: Pre-installed and fully supported

### 6.2 Allowed Dependencies (if absolutely necessary)

If stdlib proves insufficient, prefer pre-installed packages:
- `numpy` - Pre-installed, for any numerical operations
- `poetry` - Pre-installed, for dependency management IF needed

### 6.3 Recommended Stdlib Stack

| Layer | Stdlib Components |
|-------|-------------------|
| **Domain** | `dataclasses`, `abc`, `typing`, `uuid`, `datetime`, `enum` |
| **Application** | `typing.Protocol`, `collections`, `functools` |
| **Infrastructure** | `sqlite3`, `json`, `pathlib`, `os` |
| **Interface** | `argparse`, `http.server` (if needed) |
| **Testing** | `unittest`, `unittest.mock` |

---

## 7. Self-Critique

### 7.1 Potential Weaknesses in This Analysis

1. **Bias toward simplicity**: My preference for zero-dependency may undervalue the productivity gains from well-chosen libraries
2. **Limited TypeScript stdlib knowledge**: Node.js ecosystem may have more stdlib than I credit
3. **Theoretical vs practical**: Should validate with proof-of-concept before committing
4. **Mypy availability**: Assumed mypy might not be available; should verify

### 7.2 Recommended Validation Steps

1. Create minimal proof-of-concept with Python stdlib only
2. Verify sqlite3 persistence works in sandbox environment
3. Test SessionStart hook reliability for fallback dependency installation
4. Benchmark token usage of Python vs TypeScript implementations

---

## 8. References

### Primary Sources

1. Cockburn, A. (2005). "Hexagonal Architecture." https://alistair.cockburn.us/hexagonal-architecture/
2. Anthropic. (2025). "Claude Code on the web." https://www.anthropic.com/news/claude-code-on-the-web
3. Anthropic. (2025). "Effective context engineering for AI agents." https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
4. Claude Code Docs. "Sandboxing." https://code.claude.com/docs/en/sandboxing
5. Claude Code Docs. "Claude Code on the web." https://code.claude.com/docs/en/claude-code-on-the-web

### Secondary Sources

6. Chroma Research. "Context Rot: How Increasing Input Tokens Impacts LLM Performance." https://research.trychroma.com/context-rot
7. Inkeep. "Fighting Context Rot." https://inkeep.com/blog/fighting-context-rot
8. GitHub. "domain-driven-hexagon." https://github.com/Sairyss/domain-driven-hexagon
9. GitHub. "hexagonal-architecture-with-python." https://github.com/marcosvs98/hexagonal-architecture-with-python
10. Medium. "Zero-Dependency Python: Building Tools That Avoid External Libraries." https://medium.com/@CodeWithHannan/zero-dependency-python-building-tools-that-avoid-external-libraries-f2a8f5092b57
11. Software Patterns Lexicon. "Hexagonal Architecture: Ports and Adapters in Python." https://softwarepatternslexicon.com/python/architectural-patterns/hexagonal-architecture-ports-and-adapters/

---

## Appendix A: Migration Path

If we need to migrate from zero-dep to library-based later:

| Current (Stdlib) | Future (Library) | Migration Complexity |
|-----------------|------------------|---------------------|
| `dataclasses` | Pydantic | Low - similar API |
| `sqlite3` | SQLAlchemy | Medium - abstracted by port |
| `argparse` | Click/Typer | Low - adapter only |
| `unittest` | pytest | Low - compatible |
| `json` | orjson | Low - drop-in |

The hexagonal architecture explicitly enables this migration by isolating technology choices in adapters.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-07 | Claude | Initial draft |
