# Rules Content Inventory

> Comprehensive catalog of all content in `.claude/rules/` for gap analysis.
> Part of TASK-002: Extract and catalog ALL content from .claude/rules/

**Parent:** EN-202-claude-md-rewrite
**Created:** 2026-02-01
**Purpose:** Identify content that could overlap with or replace CLAUDE.md content

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [File Summary](#file-summary) | Overview of all files with line counts |
| [architecture-standards.md](#architecture-standardsmd) | Full content breakdown |
| [coding-standards.md](#coding-standardsmd) | Full content breakdown |
| [error-handling-standards.md](#error-handling-standardsmd) | Full content breakdown |
| [file-organization.md](#file-organizationmd) | Full content breakdown |
| [markdown-navigation-standards.md](#markdown-navigation-standardsmd) | Full content breakdown |
| [python-environment.md](#python-environmentmd) | Full content breakdown |
| [testing-standards.md](#testing-standardsmd) | Full content breakdown |
| [tool-configuration.md](#tool-configurationmd) | Full content breakdown |
| [Overlap Analysis](#overlap-analysis) | Content that overlaps with CLAUDE.md |
| [Recommendations](#recommendations) | Gap closure recommendations |

---

## File Summary

| File | Line Count | Primary Focus | CLAUDE.md Overlap Risk |
|------|------------|---------------|------------------------|
| `architecture-standards.md` | 566 | Hexagonal Architecture, CQRS, Event Sourcing | **HIGH** - Architecture section exists in CLAUDE.md |
| `coding-standards.md` | 493 | Python coding rules, naming conventions | **HIGH** - Code Standards section exists in CLAUDE.md |
| `error-handling-standards.md` | 576 | Exception hierarchy, error patterns | **MEDIUM** - Referenced but not duplicated |
| `file-organization.md` | 344 | Directory structure, naming conventions | **HIGH** - Architecture section has similar content |
| `markdown-navigation-standards.md` | 329 | Navigation table requirements | **LOW** - New standard, not in CLAUDE.md |
| `python-environment.md` | 124 | UV usage, dependency management | **LOW** - Operational, not conceptual |
| `testing-standards.md` | 408 | Test pyramid, BDD, coverage | **MEDIUM** - Some overlap with Code Standards |
| `tool-configuration.md` | 528 | pytest, mypy, ruff configuration | **LOW** - Tool-specific, not conceptual |

**Total Lines:** 3,368 lines across 8 files

---

## architecture-standards.md

**Path:** `.claude/rules/architecture-standards.md`
**Line Count:** 566

### Main Sections

1. **Hexagonal Architecture** (Lines 16-72)
   - Layer Structure diagram (src/ tree)
   - Dependency Rules table
   - Shared Kernel explanation

2. **Ports and Adapters** (Lines 75-115)
   - Port Naming Convention table
   - Adapter Naming Convention table
   - Composition Root pattern with code example

3. **CQRS Pattern** (Lines 118-187)
   - Command Structure with code examples
   - Query Structure with code examples
   - File Naming Rules table
   - Dispatcher Pattern

4. **Event Sourcing** (Lines 190-255)
   - Domain Events with code examples
   - Event Store Port
   - Aggregate Root Pattern with code
   - Snapshot Optimization

5. **Value Objects** (Lines 258-296)
   - Immutable Value Objects with code
   - Value Object Rules table
   - Value Object Types table

6. **Domain Services** (Lines 299-362)
   - Service Classification table
   - Domain Service Pattern with code
   - Application Service (Handler) with code

7. **Repository Pattern** (Lines 365-415)
   - Repository Hierarchy diagram
   - Generic Repository Port with code
   - Event-Sourced Repository with code

8. **Bounded Contexts** (Lines 418-479)
   - Context Structure diagram
   - Context Map ASCII art
   - Context Communication rules

9. **Validation Enforcement** (Lines 482-507)
   - Test examples for architecture enforcement

10. **Primary and Secondary Adapters** (Lines 510-566)
    - Primary Adapters table
    - Secondary Adapters table
    - References section

### Key Content for CLAUDE.md Overlap

- **Layer Structure diagram** - Similar to CLAUDE.md Architecture section
- **Dependency Rules** - Partially duplicated
- **Key Design Principles** - Partially duplicated (Hexagonal, Zero-Dependency Core, CQRS)

---

## coding-standards.md

**Path:** `.claude/rules/coding-standards.md`
**Line Count:** 493

### Main Sections

1. **Language: Python 3.11+** (Lines 21-134)
   - Type Hints rules with code examples
   - Docstrings (Google-style) with code examples
   - Naming Conventions table
   - Line Length (100 characters)
   - Imports grouping rules
   - TYPE_CHECKING Pattern with code
   - Protocol Pattern with code

2. **Architecture Rules** (Lines 138-167)
   - Domain Layer rules
   - Application Layer rules
   - Infrastructure Layer rules
   - Interface Layer rules

3. **Value Object Coding** (Lines 170-227)
   - Immutable Dataclass Pattern with code
   - Enum Value Object Pattern with code

4. **CQRS Naming Conventions** (Lines 230-263)
   - File Naming table
   - Class Naming table
   - Query Verbs table

5. **Domain Event Coding** (Lines 266-305)
   - Event Structure with code
   - Event Naming Rules

6. **Testing Standards** (Lines 308-343)
   - Test File Naming
   - Test Function Naming
   - Test Structure (AAA pattern)

7. **Git Standards** (Lines 346-383)
   - Commit Messages (conventional commits)
   - Branch Naming

8. **Error Handling** (Lines 386-449)
   - Exception Hierarchy
   - Exception Pattern with code
   - Error Messages guidelines

9. **Documentation Standards** (Lines 452-482)
   - File Headers
   - Knowledge Capture locations

10. **Enforcement** (Lines 485-493)
    - Pre-commit hooks, CI, Code review, QA Agent

### Key Content for CLAUDE.md Overlap

- **Architecture Rules** - DIRECTLY overlaps with CLAUDE.md "Architecture" section
- **Code Standards** reference exists in CLAUDE.md but points to this file

---

## error-handling-standards.md

**Path:** `.claude/rules/error-handling-standards.md`
**Line Count:** 576

### Main Sections

1. **Exception Hierarchy** (Lines 10-36)
   - Base Classes tree diagram (DomainError, ApplicationError, InfrastructureError)

2. **Domain Exceptions** (Lines 40-242)
   - Location: `src/shared_kernel/exceptions.py`
   - Base Domain Error with code
   - ValidationError with code
   - NotFoundError with code
   - AggregateNotFoundError with code
   - InvalidStateError with code
   - InvalidStateTransitionError with code
   - InvariantViolationError with code
   - ConcurrencyError with code
   - QualityGateError with code

3. **Application Exceptions** (Lines 246-282)
   - Location: `src/application/exceptions.py`
   - ApplicationError, HandlerNotFoundError, UnauthorizedError, ConfigurationError

4. **Infrastructure Exceptions** (Lines 285-332)
   - Location: `src/infrastructure/exceptions.py`
   - InfrastructureError, PersistenceError, EventStoreError, StreamNotFoundError, ExternalServiceError

5. **Exception Selection Guidelines** (Lines 336-353)
   - Situation-to-Exception mapping table

6. **Error Message Guidelines** (Lines 356-400)
   - Include Context examples
   - Suggest Action examples
   - Be Specific examples

7. **Error Handling in Handlers** (Lines 404-442)
   - Full code example

8. **Error Handling in CLI Adapter** (Lines 446-480)
   - Full code example with exit codes

9. **Testing Exceptions** (Lines 484-521)
   - Test examples for exceptions

10. **Anti-Patterns** (Lines 525-566)
    - Using Generic Exceptions
    - Catching Too Broadly
    - Losing Exception Context

11. **References** (Lines 570-576)

### Key Content for CLAUDE.md Overlap

- **LOW OVERLAP** - CLAUDE.md does not duplicate this content, only references it

---

## file-organization.md

**Path:** `.claude/rules/file-organization.md`
**Line Count:** 344

### Main Sections

1. **Project Root Structure** (Lines 10-66)
   - Full directory tree diagram of jerry/

2. **Source Code Structure** (Lines 70-194)
   - Domain Layer (`src/domain/`) tree
   - Application Layer (`src/application/`) tree
   - Infrastructure Layer (`src/infrastructure/`) tree
   - Interface Layer (`src/interface/`) tree

3. **Test Structure** (Lines 198-233)
   - tests/ directory tree
   - Test File Naming table

4. **Project Workspace Structure** (Lines 236-264)
   - projects/PROJ-{NNN}-{slug}/ tree

5. **Naming Conventions** (Lines 268-311)
   - File Names table
   - Class Names table
   - Module `__init__.py` Exports with code

6. **One Class Per File Rule** (Lines 314-336)
   - MANDATORY rule explanation
   - Correct vs Incorrect examples

7. **References** (Lines 339-344)

### Key Content for CLAUDE.md Overlap

- **HIGH OVERLAP** - CLAUDE.md "Architecture" section has similar directory structure
- Project Root Structure nearly identical to CLAUDE.md architecture diagram

---

## markdown-navigation-standards.md

**Path:** `.claude/rules/markdown-navigation-standards.md`
**Line Count:** 329

### Main Sections

1. **Intention** (Lines 27-54)
   - Why Navigation Tables with Anchor Links Matter
   - Anthropic Official Guidance (quoted)
   - Industry Evidence (quoted)

2. **Strategy** (Lines 56-166)
   - Placement rules (after frontmatter, before content)
   - Anchor Link Syntax rules table
   - Table Formats:
     - Format 1: Section Index with Anchors
     - Format 2: Triple-Lens Audience with Anchors
     - Format 3: Hybrid

3. **Requirements** (Lines 168-203)
   - Mandatory Elements table (NAV-001 through NAV-006)
   - File Types Covered table
   - Exceptions list

4. **Examples** (Lines 205-263)
   - Example 1: Rule File
   - Example 2: Enabler File
   - Example 3: Skill File
   - Example 4: Worktracker Template

5. **Validation** (Lines 265-292)
   - Compliance Checklist
   - Anchor Link Verification
   - Automated Validation (Future)

6. **References** (Lines 294-329)
   - Primary Sources table
   - Secondary Sources table
   - Jerry Internal Sources table

### Key Content for CLAUDE.md Overlap

- **NO OVERLAP** - This is a NEW standard created during PROJ-001
- Should be REFERENCED from CLAUDE.md, not duplicated

---

## python-environment.md

**Path:** `.claude/rules/python-environment.md`
**Line Count:** 124

### Main Sections

1. **UV Usage (MANDATORY)** (Lines 8-59)
   - Running the Jerry CLI examples
   - Running Other Python Commands examples
   - Adding Dependencies examples
   - Running Tests examples

2. **Why UV?** (Lines 63-69)
   - Reproducible environments
   - Isolation
   - Speed
   - No conflicts

3. **Common Commands Reference** (Lines 72-82)
   - Task-to-Command table

4. **Large File Handling (Transcript Skill)** (Lines 85-110)
   - Files Agents Should Read table
   - Files Agents Should NEVER Read table

5. **Enforcement** (Lines 113-118)
   - HARD rule declaration

### Key Content for CLAUDE.md Overlap

- **LOW OVERLAP** - This is operational guidance, not conceptual architecture
- Could be referenced from CLAUDE.md but content is distinct

---

## testing-standards.md

**Path:** `.claude/rules/testing-standards.md`
**Line Count:** 408

### Main Sections

1. **Test Pyramid** (Lines 10-36)
   - ASCII art pyramid diagram
   - Test Distribution per Feature table

2. **BDD Red/Green/Refactor Cycle** (Lines 39-86)
   - The Cycle ASCII diagram
   - RED Phase Requirements with code
   - GREEN Phase Requirements
   - REFACTOR Phase Requirements

3. **Test Scenarios** (Lines 89-145)
   - Happy Path (60%) with code
   - Negative Cases (30%) with code
   - Edge Cases (10%) with code

4. **Test File Organization** (Lines 148-173)
   - Location table
   - Naming Convention with examples

5. **Test Structure (AAA Pattern)** (Lines 176-193)
   - Code example

6. **Coverage Requirements** (Lines 196-221)
   - Minimum Thresholds table
   - Exclusions list
   - CI Enforcement example

7. **Architecture Tests** (Lines 224-255)
   - Purpose
   - Location
   - Examples with code

8. **Contract Tests** (Lines 258-293)
   - Purpose
   - Examples with code

9. **Test Fixtures** (Lines 296-334)
   - Shared Fixtures in conftest.py with code
   - Factory Functions with code

10. **Mocking Guidelines** (Lines 337-365)
    - When to Mock list
    - When NOT to Mock list
    - Example with code

11. **Test Data** (Lines 368-397)
    - Principles list
    - Bad Example
    - Good Example

12. **References** (Lines 400-408)

### Key Content for CLAUDE.md Overlap

- **MEDIUM OVERLAP** - CLAUDE.md "Code Standards" section mentions testing
- Test function naming convention duplicated in coding-standards.md

---

## tool-configuration.md

**Path:** `.claude/rules/tool-configuration.md`
**Line Count:** 528

### Main Sections

1. **Python Environment** (Lines 13-32)
   - Required Version (Python 3.11+)
   - Virtual Environment commands

2. **pyproject.toml** (Lines 36-68)
   - Project Metadata
   - Build System

3. **pytest Configuration** (Lines 72-156)
   - pytest.ini Settings
   - pyproject.toml Alternative
   - Coverage Configuration
   - Running Tests commands

4. **mypy Configuration** (Lines 160-201)
   - pyproject.toml Settings
   - Running mypy commands

5. **Ruff Configuration** (Lines 205-268)
   - pyproject.toml Settings
   - Running Ruff commands

6. **Pre-commit Configuration** (Lines 272-313)
   - .pre-commit-config.yaml
   - Installing Pre-commit

7. **Editor Configuration** (Lines 317-363)
   - .editorconfig
   - VS Code Settings

8. **Makefile** (Lines 367-410)
   - Common Commands

9. **CI/CD Configuration** (Lines 414-461)
   - GitHub Actions workflow

10. **Environment Variables** (Lines 465-505)
    - Development
    - Testing
    - Loading Environment with code

11. **Jerry-Specific Decisions** (Lines 509-518)
    - Ruff over Black+isort+flake8
    - Strict mypy
    - pytest markers
    - Coverage threshold

12. **References** (Lines 521-528)

### Key Content for CLAUDE.md Overlap

- **LOW OVERLAP** - Tool configuration details not in CLAUDE.md
- CLAUDE.md mentions pyproject.toml and pytest.ini but doesn't detail them

---

## Overlap Analysis

### HIGH OVERLAP Areas (Must Deduplicate)

| CLAUDE.md Section | Rules File | Overlap Type |
|-------------------|------------|--------------|
| Architecture (jerry/ tree) | `file-organization.md` (Project Root Structure) | **DUPLICATE** - Same directory tree |
| Architecture (Layer Structure) | `architecture-standards.md` (Hexagonal Architecture) | **DUPLICATE** - Same content |
| Architecture (Key Design Principles) | `architecture-standards.md` | **PARTIAL** - Similar concepts |
| Architecture Rules | `coding-standards.md` (Architecture Rules) | **DUPLICATE** - Same rules |
| Code Standards reference | `coding-standards.md` | **POINTER** - CLAUDE.md points here |

### MEDIUM OVERLAP Areas (Consider Consolidation)

| CLAUDE.md Section | Rules File | Overlap Type |
|-------------------|------------|--------------|
| Testing mention | `coding-standards.md`, `testing-standards.md` | **FRAGMENTED** - Split across files |
| Error Handling | `error-handling-standards.md` | **POINTER** - Should just reference |
| CLI Commands | `python-environment.md` | **OPERATIONAL** - Different audience |

### LOW/NO OVERLAP Areas (New Content)

| Rules File | Status |
|------------|--------|
| `markdown-navigation-standards.md` | **NEW** - Should be referenced |
| `tool-configuration.md` | **DISTINCT** - Tool-specific details |

---

## Recommendations

### 1. Deduplicate Architecture Content

**Current State:**
- CLAUDE.md has ~50 lines of architecture content
- `file-organization.md` has ~66 lines of Project Root Structure
- `architecture-standards.md` has ~566 lines of detailed standards

**Recommendation:**
- CLAUDE.md should have MINIMAL architecture overview (10-20 lines)
- Replace duplicate content with reference: "See `.claude/rules/architecture-standards.md`"
- Keep only high-level conceptual description in CLAUDE.md

### 2. Consolidate Code Standards References

**Current State:**
- CLAUDE.md mentions "Code Standards" briefly
- `coding-standards.md` has comprehensive 493-line document

**Recommendation:**
- CLAUDE.md should ONLY reference: "See `.claude/rules/coding-standards.md`"
- Remove any duplicated rules from CLAUDE.md

### 3. Add New References

**CLAUDE.md should add references to:**
- `.claude/rules/markdown-navigation-standards.md` (NEW)
- `.claude/rules/python-environment.md` (UV requirement)

### 4. Content Preservation Checklist

Content that MUST remain in CLAUDE.md (unique, not in rules/):
- [ ] Project Overview and Context Rot explanation
- [ ] Worktracker system documentation
- [ ] TODO behavior requirements
- [ ] Skills Available table
- [ ] Mandatory Skill Usage (problem-solving, nasa-se, orchestration)
- [ ] Agent Governance (Jerry Constitution)
- [ ] Project Enforcement (JERRY_PROJECT workflow)
- [ ] Project-Based Workflow guidance

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total files analyzed | 8 |
| Total lines in rules/ | 3,368 |
| Files with HIGH overlap | 3 (`architecture-standards.md`, `coding-standards.md`, `file-organization.md`) |
| Files with MEDIUM overlap | 2 (`error-handling-standards.md`, `testing-standards.md`) |
| Files with LOW/NO overlap | 3 (`markdown-navigation-standards.md`, `python-environment.md`, `tool-configuration.md`) |
| Estimated duplicate lines | ~150-200 lines |

---

*Inventory completed: 2026-02-01*
*TASK-002 of Gap Analysis*
