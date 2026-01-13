# TD-014-E-013: Knowledge Base Patterns for CLI and Hexagonal Architecture

> **Research Task:** TD-014.R3
> **Date:** 2026-01-11
> **Researcher:** ps-researcher (Agent abca05c)
> **Status:** COMPLETE

---

## Executive Summary (L0)

The Jerry framework knowledge base contains comprehensive guidance on hexagonal architecture, CLI adapter patterns, and port-adapter design. Five primary sources were identified that provide both theoretical foundations and practical implementation guidance. All first principles (adapters are stupid, ports define capabilities, use cases are behavioral units, dependencies point inward) are validated with explicit citations from the knowledge base.

**Key Finding:** A complete teaching edition document exists (`work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`) that serves as the authoritative reference for CLI implementation as a primary adapter.

---

## Technical Findings (L1)

### Source 1: Hexagonal Architecture Teaching Edition

**Location:** `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`

**Relevance:** CRITICAL - Core reference document

**Key Sections:**
- **Section 2 (Lines 185-249):** Hexagonal Architecture overview with zone map
- **Section 7 (Lines 472-522):** CLI Adapter as Primary Adapter
- **Section 6 (Lines 378-471):** Repository Pattern and Secondary Adapter chain
- **Appendix A (Lines 702-777):** Python project layout

**Evidence for First Principles:**

| Principle | Evidence | Citation |
|-----------|----------|----------|
| Adapters are stupid | "CLI is a remote control. It only presses buttons. It doesn't contain the rules." | Section 7, lines 474-479 |
| Ports define capabilities | "Not all adapters expose all capabilities. A Public API might expose only end-user use cases." | Section 1.2, lines 91-92 |
| Use Cases are behavioral | "Commands (write): AddWorkItem. Queries (read): ListWorkItems. Each use case does one thing." | Section 4, lines 310-318 |
| Dependencies point inward | "Rule: The domain owns abstractions. Infrastructure owns implementations." | Section 2, line 251 |

---

### Source 2: CLI-Blackboard Integration Architecture

**Location:** `docs/knowledge/dragonsbelurkin/aspirations/blackboard/phase-38.17-e-156-cli-blackboard-integration-architecture.md`

**Relevance:** HIGH - Direct application of patterns

**Key Sections:**
- **Section 4.1 (Lines 88-137):** Process boundary diagram
- **Section 4.2.2 (Lines 163-177):** Factory composition root pattern
- **Section 4.3 (Lines 230-284):** Hexagonal boundary diagram
- **Section 4.3.2 (Lines 288-294):** Boundary compliance matrix
- **Section 4.6.1 (Lines 390-440):** Factory extension pattern

**Key Insights:**
- CLI runs as subprocess, cannot access MCP context
- Factory composition root centralizes dependency wiring
- Compliance matrix validates hexagonal boundaries

---

### Source 3: CLI Session Start Implementation

**Location:** `src/interface/cli/session_start.py`

**Relevance:** MEDIUM - Working example

**Key Patterns:**
- **Lines 162-172:** Factory composition root usage
- **Lines 156-201:** Structured output formatting
- **Lines 36-49:** Dependency discovery logic

**Pattern Applied:**
```
CLI receives input → Create service via factory → Call use case → Translate result
```

---

### Source 4: Jerry Framework Architecture Overview

**Location:** `CLAUDE.md`

**Relevance:** MEDIUM - Framework-level principles

**Key Principles (Lines 45-56):**
1. Hexagonal Architecture (Ports & Adapters)
2. Zero-Dependency Core (Python stdlib only in domain)
3. CQRS Pattern (Commands/Queries separation)

---

### Source 5: Canonical Structure and Documentation

**Location:** `docs/knowledge/exemplars/patterns/canonical-structure.md`

**Relevance:** LOW-MEDIUM - Naming conventions

**Documentation Patterns:**
- **ADR prefix:** Architecture Decision Records
- **LES prefix:** Lessons Learned
- **PAT prefix:** Proven patterns

---

## Strategic Implications (L2)

### 1. CLI Implementation Pattern is Well-Established

The combination of teaching edition and working implementation provides clear guidance:

**Implementation Strategy:**
1. CLI receives user input (translate from CLI protocol)
2. Create/retrieve service instance via factory
3. Call use case (Command/Query) on service
4. Translate service result back to CLI output format

### 2. Multiple Surface Pattern

The knowledge base documents that a single domain can be exposed through multiple ports:
- Public API (end-user operations)
- Admin API (administrative operations)
- User CLI (command-line interface)

**Implication:** TD-014 CLI should define explicit facades as primary ports.

### 3. Port Placement is Critical

**Rule:** The domain owns abstractions. Infrastructure owns implementations.

This means:
- Ports must be defined in `application/` layer
- Adapters must live in `infrastructure/` or `interface/`
- Domain must have NO imports from ports, adapters, or infrastructure

### 4. Factory Composition Root

Both teaching edition and working example show the factory pattern as the composition root:

**Benefits:**
- Centralized dependency creation
- Adapter wiring
- Configuration management
- Logging/tracing setup

**Implication:** TD-014 should create `interface/cli/factory.py`.

### 5. Process Boundaries

CLI runs as a subprocess and cannot access MCP context:
- CLI CAN create its own service instances (via factory)
- CLI CAN write to SQLite or files
- CLI CANNOT directly invoke Task tool or access memory keeper

**Implication:** TD-014 should support file-based output formats.

---

## Recommendations

### 1. Use Teaching Edition as Primary Reference
- Provides 3-level explanations (ELI5, Junior, Architect)
- All major concepts explained with ASCII diagrams
- References to Cockburn, Evans, Fowler, Vernon

### 2. Follow Factory Pattern for Composition
- Create `src/interface/cli/factory.py`
- Wire primary ports and adapters there
- Keep CLI adapter thin

### 3. Define Primary Ports Explicitly
- Separate facades if needed (`IPublicCLIFacade`, `IAdminCLIFacade`)
- Place in `src/application/ports/primary/`
- Document capability boundaries

### 4. Validate Hexagonal Boundaries
- Use compliance matrix from e-156 as framework
- Ensure CLI only calls application layer
- Ensure ports are imported inbound only

### 5. Document Architecture Decisions
- Create ADR for CLI design choices: `ADR-CLI-001-primary-adapter.md`
- Reference teaching edition in rationale
- Document lessons as `LES-NNN-slug.md`

---

## First Principles Validation

| Principle | Validated | Source Citation |
|-----------|-----------|-----------------|
| Adapters are stupid | ✅ | Teaching edition Section 7 |
| Ports define capabilities | ✅ | Teaching edition Section 1.1 |
| Use Cases are behavioral | ✅ | Teaching edition Section 4 |
| Dependencies point inward | ✅ | CLAUDE.md lines 45-48 |

---

## Cited Files (Absolute Paths)

1. `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`
2. `docs/knowledge/dragonsbelurkin/aspirations/blackboard/phase-38.17-e-156-cli-blackboard-integration-architecture.md`
3. `src/interface/cli/session_start.py`
4. `CLAUDE.md`
5. `docs/knowledge/exemplars/patterns/canonical-structure.md`

---

## Document Lineage

| Artifact | Relationship |
|----------|--------------|
| TD-014 | Parent tech debt item |
| TD-014.R1 | Sibling research (use cases) |
| TD-014.R2 | Sibling research (domain capabilities) |
