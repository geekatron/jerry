# TD-017-E-001: Knowledge Inventory Report

> **Type**: Research Evidence
> **Date**: 2026-01-11
> **Researcher**: Claude (Opus 4.5)
> **Task**: TD-017.R-000 - Inventory existing repository knowledge

---

## Executive Summary

Comprehensive inventory of Jerry repository knowledge to identify gaps in design documentation
before launching research agents for TD-017 (Comprehensive Design Canon).

**Key Finding**: Existing pattern catalog (31 patterns) has strong coverage but lacks:
- Bounded context organization details
- One-class-per-file (flat structure) documentation
- TD-015 dispatcher pattern codification
- Industry citations at pattern level
- Jerry-specific opinion preservation

---

## Inventory Statistics

| Category | Count | Location |
|----------|-------|----------|
| Research Documents | 60+ | `projects/*/research/` |
| Synthesis Documents | 8 | `projects/*/synthesis/` |
| Analysis Documents | 20+ | `projects/*/analysis/` |
| ADRs | 30+ | `projects/*/decisions/` |
| Knowledge Documents | 40+ | `docs/knowledge/` |
| Rules Files | 4 | `.claude/rules/` |
| Pattern Catalog | 1 (31 patterns) | `.claude/patterns/PATTERN-CATALOG.md` |

---

## Existing Design Canon

**Authoritative Source**: `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`

### Pattern Categories Covered

| Category | Patterns | Status |
|----------|----------|--------|
| Identity (PAT-ID-*) | 4 | Complete |
| Entity (PAT-ENT-*) | 5 | Complete |
| Aggregate (PAT-AGG-*) | 4 | Complete |
| Event (PAT-EVT-*) | 4 | Complete |
| CQRS (PAT-CQRS-*) | 3 | Complete |
| Repository (PAT-REPO-*) | 3 | Complete |
| Graph (PAT-GRAPH-*) | 3 | Complete |
| Architecture (PAT-ARCH-*) | 3 | **Incomplete** |
| Testing (PAT-TEST-*) | 3 | Complete |

---

## Gap Analysis

### GAP-001: Bounded Context Organization Not Fully Documented

**Current State**:
- PAT-ARCH-003 lists contexts: `session_management/`, `work_tracking/`, `shared_kernel/`
- Missing `problem_solving/` (future, per user)

**Missing Documentation**:
- Directory structure per bounded context
- How to create/add new bounded context
- Inter-BC communication patterns
- Context mapping (shared kernel, anti-corruption layer)
- Current implementation vs. design canon discrepancy

**Evidence**: Design canon (lines 1821-1900) mentions Work Management, Knowledge Capture, Identity & Access, Reporting - but actual implementation uses session_management, work_tracking.

**Impact**: Agents don't know how to structure new bounded contexts.

---

### GAP-002: Flat Structure / One-Class-Per-File Not Documented

**Current State**:
- `.claude/rules/architecture-standards.md` mentions "One Class Per File Rule"
- `.claude/rules/file-organization.md` has directory structure
- NOT in pattern catalog as a formal pattern

**Missing Documentation**:
- Explicit pattern with rationale
- Examples of correct vs. incorrect file organization
- Exceptions policy (e.g., related small value objects)
- Industry justification and citations

**Evidence**: Search found 126 files mention "one class" or "flat structure" in various contexts but no unified pattern.

**Impact**: Inconsistent file organization across codebase.

---

### GAP-003: TD-015 Dispatcher Pattern Not Codified

**Current State**:
- TD-015 implemented QueryDispatcher, CommandDispatcher
- CLIAdapter with dependency injection
- Composition root at `src/bootstrap.py`

**Missing Documentation**:
- PAT-CQRS-004: Dispatcher Pattern (not yet added)
- PAT-ARCH-004: Composition Root Pattern (not yet added)
- PAT-ARCH-005: CLIAdapter Pattern (not yet added)

**Evidence**: TD-015 completed (commit e791dc6) but patterns not added to catalog.

**Impact**: Future developers won't know about dispatcher pattern.

---

### GAP-004: No Industry Citations at Pattern Level

**Current State**:
- Pattern catalog has References section at bottom
- Individual patterns don't cite sources

**Missing Documentation**:
- Per-pattern "Prior Art" or "Industry Reference"
- Authoritative source citations (Cockburn, Evans, Fowler, Vernon)
- Link between Jerry patterns and industry patterns

**Example Needed**:
```markdown
### PAT-ARCH-001: Hexagonal Architecture
**Status**: MANDATORY | **Category**: Architecture
**Industry Prior Art**:
- [Alistair Cockburn (2005)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Netflix Engineering](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)
```

**Impact**: Patterns lack authority and evidence-based justification.

---

### GAP-005: Jerry-Specific Opinions Not Explicitly Preserved

**Current State**:
- Many decisions captured in ADRs
- But not linked to patterns

**Missing Documentation**:
- "Jerry Opinion" sections in patterns
- Explicit override of generic patterns where we differ
- Rationale for Jerry-specific choices

**Examples of Jerry Opinions**:
1. CloudEvents for external only, DomainEvent for internal
2. TOON format for LLM-friendly serialization
3. Specific bounded context choices (session_management vs. generic "identity")
4. File-per-class over traditional Python module organization

**Impact**: Generic research could override our intentional decisions.

---

## Recommended Research Streams (Fan-Out)

Based on gaps, launch 5 parallel research agents:

| ID | Research Topic | Agent | Priority |
|----|----------------|-------|----------|
| R-001 | Bounded Context Organization | ps-researcher | HIGH |
| R-002 | One-Class-Per-File Patterns | ps-researcher | HIGH |
| R-003 | Clean Architecture / Hexagonal | ps-researcher | MEDIUM |
| R-004 | CQRS/ES Naming Conventions | ps-researcher | MEDIUM |
| R-005 | Claude Code Rules Best Practices | ps-researcher | HIGH |

---

## Sources Consulted

### Repository Sources
- `.claude/patterns/PATTERN-CATALOG.md` (31 patterns)
- `.claude/rules/*.md` (4 rules files)
- `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md`
- `docs/design/PYTHON-ARCHITECTURE-STANDARDS.md`
- `docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`

### External Sources (To Be Researched)
- Alistair Cockburn - Hexagonal Architecture
- Eric Evans - Domain-Driven Design (Bounded Contexts)
- Martin Fowler - CQRS, Event Sourcing
- Vaughn Vernon - Implementing Domain-Driven Design
- Robert C. Martin - Clean Architecture

---

## Conclusion

The Jerry repository has substantial design documentation but needs enhancement in 5 specific areas.
TD-017 should proceed with fan-out research to fill these gaps while preserving existing Jerry opinions.
