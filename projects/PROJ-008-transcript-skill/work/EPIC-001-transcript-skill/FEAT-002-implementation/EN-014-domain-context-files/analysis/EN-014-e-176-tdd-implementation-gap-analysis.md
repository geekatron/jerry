# EN-014-e-176: Comprehensive TDD Implementation Gap Analysis

<!--
PS-ID: EN-014
Entry-ID: e-176
Agent: ps-analyst (v2.0.0)
Topic: Comprehensive TDD Implementation Gap Analysis
Created: 2026-01-29
Template: docs/knowledge/exemplars/templates/analysis.md
Frameworks: 5W2H, Ishikawa, Pareto
-->

> **Analysis ID:** EN-014-e-176
> **PS ID:** EN-014
> **Entry ID:** e-176
> **Agent:** ps-analyst (v2.0.0)
> **Status:** COMPLETE
> **Created:** 2026-01-29T15:00:00Z
> **Input Documents:** DISC-008, DEC-001, TDD-EN014-domain-schema-v2.md

---

## 1. Executive Summary (L0 - ELI5)

### The Instruction Manual Problem

Imagine you received an instruction manual for building a complex LEGO set. The manual has beautiful pictures of the finished model (the JSON Schema specification) and detailed descriptions of each piece (entity relationships, metadata, context rules, validation). But when you sit down to actually build it, you realize:

1. **No tools are included** - You need a screwdriver and wrench, but the manual doesn't tell you which ones or where to get them
2. **No step-by-step guide** - The manual shows the end result but not the sequence of steps to get there
3. **No quality checklist** - You don't know if you've built it correctly until someone else looks at it
4. **No connection to your existing toolbox** - You already have a toolkit (Jerry CLI), but the manual ignores it

**The Fix:** This analysis identifies exactly what's missing and provides a roadmap to complete the manual so anyone (including an AI assistant) can build the LEGO set without getting stuck.

### Key Finding

The TDD passed automated quality reviews (0.90+) but **fails the implementability test**. Sections 5.2.1 and 5.2.2 provide Python code as "afterthought patches" without explaining:
- How to run the code
- When validation is triggered
- Who/what calls the validators
- How to test the validators
- How to integrate with CI/CD

---

## 2. Technical Analysis (L1 - Engineer)

### 2.1 Gap Inventory

| Gap ID | Category | Severity | DISC-008 Ref | User Decision |
|--------|----------|----------|--------------|---------------|
| GAP-IMPL-001 | Technology | HIGH | Yes | D-001: Python code (not LLM spec) |
| GAP-IMPL-002 | Location | HIGH | Yes | D-002: `jerry transcript validate-domain` |
| GAP-IMPL-003 | Execution | CRITICAL | Yes | Unresolved - requires TDD revision |
| GAP-IMPL-004 | Algorithm | MEDIUM | Yes | SV-006 in TDD 5.2.2 (incomplete) |
| GAP-IMPL-005 | Runtime | CRITICAL | Yes | Unresolved - requires TDD revision |
| GAP-IMPL-006 | Testing | CRITICAL | Yes | Unresolved - requires TDD revision |
| GAP-IMPL-007 | CI/CD | HIGH | Yes | Unresolved - requires TDD revision |
| GAP-IMPL-008 | CLI | HIGH | Yes | D-002: Use Jerry CLI, not custom script |
| GAP-IMPL-009 | Implementability | CRITICAL | Yes | Validation: Self-assessment fails |

### 2.2 TDD Section Analysis

#### Section 5.2.1 (Semantic Validator Implementation)

**Current State:**
```python
# skills/transcript/validators/domain_validator.py
from typing import Any
from dataclasses import dataclass
import jsonschema

@dataclass
class ValidationError:
    path: str
    rule: str
    message: str
    severity: str  # "error" | "warning"
```

**Critical Missing Elements:**
1. No module path specification (`skills/transcript/validators/` doesn't exist in Jerry architecture)
2. No entry point definition (how is this called?)
3. No CLI integration pattern
4. No dependency injection pattern (required by Jerry hexagonal architecture)
5. No port/adapter separation

#### Section 5.2.2 (SV-006 Circular Relationship Detection)

**Current State:**
```python
def _sv006_circular_relationships(domain_data: dict) -> list[ValidationError]:
    """Detect circular relationships using DFS."""
    ...
```

**Critical Missing Elements:**
1. Function exists in isolation - no caller specified
2. No integration with validation pipeline
3. No test specification
4. No error handling for malformed input

### 2.3 Jerry CLI Architecture Analysis

**Existing CLI Structure:**
```
src/interface/cli/
├── main.py           # Entry point: creates CLIAdapter, routes by namespace
├── parser.py         # Argument parser with namespace/command structure
└── adapter.py        # CLIAdapter: receives dispatcher via constructor injection
```

**Existing Namespaces:**
- `session`: start, end, status, abandon
- `items`: list, show, create, start, complete, block, cancel
- `projects`: context, list, validate
- `config`: show, get, set, path

**Missing:** `transcript` namespace for domain validation

**Integration Pattern (from existing code):**

1. **Parser Registration** (`parser.py`):
```python
def _add_transcript_namespace(subparsers):
    """Add transcript namespace commands."""
    transcript_parser = subparsers.add_parser(
        "transcript",
        help="Transcript skill commands",
        description="Manage transcript skill operations.",
    )
    transcript_subparsers = transcript_parser.add_subparsers(...)

    # validate-domain subcommand
    validate_parser = transcript_subparsers.add_parser(
        "validate-domain",
        help="Validate domain context YAML",
    )
    validate_parser.add_argument("path", help="Path to domain YAML file")
```

2. **Main Routing** (`main.py`):
```python
elif args.namespace == "transcript":
    return _handle_transcript(adapter, args, json_output)
```

3. **CLIAdapter Method** (`adapter.py`):
```python
def cmd_transcript_validate_domain(
    self,
    path: str,
    json_output: bool = False,
) -> int:
    """Validate a domain context YAML file."""
    ...
```

4. **Bootstrap Wiring** (`bootstrap.py`):
```python
def create_domain_validator() -> DomainValidator:
    """Create domain validator with schema loaded."""
    ...
```

### 2.4 Test Infrastructure Analysis

**Existing Test Structure:**
```
tests/
├── conftest.py                     # Minimal config (editable install)
├── unit/                           # Unit tests by layer
│   ├── application/                # Handler tests
│   ├── configuration/              # Config domain tests
│   └── infrastructure/             # Adapter tests
├── integration/                    # Cross-boundary tests
│   ├── cli/                        # CLI integration
│   └── test_bootstrap.py           # Wiring tests
├── e2e/                            # Full workflow tests
├── contract/                       # External interface contracts
├── architecture/                   # Layer boundary tests
└── shared_kernel/                  # Shared library tests
```

**Pytest Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
markers = [
    "happy-path: marks tests as happy path scenarios",
    "negative: marks tests as negative/error scenarios",
    "edge-case: marks tests as edge case scenarios",
    "boundary: marks tests as boundary value scenarios",
]
```

**Required for Domain Validators:**
1. `tests/unit/transcript/validators/test_domain_validator.py`
2. `tests/unit/transcript/validators/test_sv001_relationship_targets.py`
3. `tests/unit/transcript/validators/test_sv006_circular_relationships.py`
4. `tests/integration/transcript/test_cli_validate_domain.py`
5. `tests/contract/transcript/test_validation_output_contract.py`

---

## 3. Architectural Implications (L2 - Architect)

### 3.1 One-Way Door Analysis

| Decision | Reversibility | Risk | Impact |
|----------|---------------|------|--------|
| CLI namespace: `jerry transcript` | Reversible | LOW | Can rename later via version bump |
| Validator location: `src/transcript/` | Reversible | LOW | Standard refactoring |
| Python 3.11+ requirement | Committed | LOW | Already project-wide |
| jsonschema library | Reversible | LOW | Can swap validators later |
| hexagonal architecture | Committed | HIGH | Must follow port/adapter pattern |

### 3.2 Performance Implications

| Concern | Current TDD | Required Specification |
|---------|-------------|----------------------|
| Validation time | "≤8ms (P95)" | Benchmark methodology missing |
| Memory overhead | "+15% max" | tracemalloc integration unspecified |
| CI impact | Not addressed | GitHub Actions workflow required |
| Large file handling | Not addressed | Streaming validation if >1MB |

### 3.3 Integration Points

```
DOMAIN VALIDATION INTEGRATION MATRIX
=====================================

Integration Point      When Called              How Called           Who Calls
──────────────────────────────────────────────────────────────────────────────
Skill Invocation       /transcript invoke       Pre-extraction       ts-parser agent
CLI Command            jerry transcript         User request         Developer/CI
CI Pipeline            PR/Push                  GitHub Actions       Automated
Quality Gate (EN-015)  Extraction complete      Post-processing      ts-formatter agent
Test Suite             pytest run               Automated            Developer/CI
```

### 3.4 Blast Radius from Adding `transcript` Namespace

```
AFFECTED COMPONENTS
===================

src/interface/cli/
├── main.py ─────────────────────────► MODIFY (add _handle_transcript)
├── parser.py ───────────────────────► MODIFY (add _add_transcript_namespace)
└── adapter.py ──────────────────────► MODIFY (add cmd_transcript_validate_domain)

src/
└── transcript/ ─────────────────────► CREATE (new bounded context)
    ├── __init__.py
    ├── domain/
    │   ├── validators/
    │   │   ├── __init__.py
    │   │   ├── schema_validator.py
    │   │   └── semantic_validators.py
    │   └── ports/
    │       └── ivalidator.py
    ├── application/
    │   ├── queries/
    │   │   └── validate_domain_query.py
    │   └── handlers/
    │       └── validate_domain_handler.py
    └── infrastructure/
        └── adapters/
            └── filesystem_schema_adapter.py

src/bootstrap.py ────────────────────► MODIFY (add create_domain_validator)

tests/
├── unit/transcript/ ────────────────► CREATE (validator unit tests)
├── integration/transcript/ ─────────► CREATE (CLI integration tests)
└── contract/transcript/ ────────────► CREATE (output contract tests)

.github/workflows/ ──────────────────► CREATE (validate-domain.yml)
```

---

## 4. 5W2H Gap Analysis Matrix

### GAP-IMPL-001: Technology Selection

| Dimension | Analysis |
|-----------|----------|
| **What** | TDD provides Python code but no runtime specification |
| **Why** | User cannot execute validators without knowing interpreter, venv, dependencies |
| **Who** | Affects: Implementer (Claude), CI/CD pipeline, manual testing |
| **When** | Manifests at first implementation attempt |
| **Where** | TDD Section 5.2.1 |
| **How** | Remediate: Add runtime environment section specifying Python 3.11+, pyproject.toml dependencies, execution command |
| **How Much** | Effort: LOW (1 section addition), Impact: HIGH (unblocks implementation) |

### GAP-IMPL-002: Validator Location

| Dimension | Analysis |
|-----------|----------|
| **What** | TDD says "skills/transcript/validators/" but Jerry uses hexagonal architecture in src/ |
| **Why** | Skills folder is for agent definitions, not code; breaks Jerry architecture |
| **Who** | Affects: Architecture consistency, code organization, imports |
| **When** | Manifests at file creation |
| **Where** | TDD Section 5.2.1 |
| **How** | Remediate: Specify `src/transcript/domain/validators/` following hexagonal pattern |
| **How Much** | Effort: LOW (path change), Impact: MEDIUM (architecture compliance) |

### GAP-IMPL-003: Execution Context

| Dimension | Analysis |
|-----------|----------|
| **What** | TDD provides validators but no execution lifecycle |
| **Why** | Validators need to be called from CLI, agents, and CI - all need different entry points |
| **Who** | Affects: All integration points (CLI, agents, CI, tests) |
| **When** | Manifests when trying to wire validators |
| **Where** | TDD Section 5.2 (entire section) |
| **How** | Remediate: Add Section 6 "Integration Specification" with sequence diagrams for each integration point |
| **How Much** | Effort: MEDIUM (new section), Impact: CRITICAL (core gap) |

### GAP-IMPL-004: SV-006 Algorithm

| Dimension | Analysis |
|-----------|----------|
| **What** | SV-006 function exists but has no caller, no tests, no integration |
| **Why** | Dangling method - can't be used without understanding invocation context |
| **Who** | Affects: Implementer, test author |
| **When** | Manifests at integration testing |
| **Where** | TDD Section 5.2.2 |
| **How** | Remediate: Show SV-006 in context of full validation pipeline with caller chain |
| **How Much** | Effort: LOW (context addition), Impact: MEDIUM (clarifies flow) |

### GAP-IMPL-005: Runtime Environment

| Dimension | Analysis |
|-----------|----------|
| **What** | No Python version, venv, dependency management specification |
| **Why** | User cannot set up environment for development or CI |
| **Who** | Affects: All implementers, CI/CD |
| **When** | Manifests at environment setup |
| **Where** | TDD (missing section) |
| **How** | Remediate: Add Section 7 "Runtime Environment" specifying Python 3.11+, pyproject.toml entry, venv activation |
| **How Much** | Effort: LOW (new section), Impact: HIGH (unblocks setup) |

### GAP-IMPL-006: Testing Strategy

| Dimension | Analysis |
|-----------|----------|
| **What** | No testing approach, no test file locations, no coverage requirements |
| **Why** | Cannot implement RED/GREEN/REFACTOR without test scaffolding |
| **Who** | Affects: Implementer, QA |
| **When** | Manifests at test authoring |
| **Where** | TDD (missing section) |
| **How** | Remediate: Add Section 8 "Testing Strategy" with RED/GREEN/REFACTOR flow, test locations, coverage targets |
| **How Much** | Effort: MEDIUM (detailed section), Impact: CRITICAL (enables TDD) |

### GAP-IMPL-007: CI/CD Pipeline

| Dimension | Analysis |
|-----------|----------|
| **What** | No GitHub Actions workflow, no quality gates, no trigger conditions |
| **Why** | Validation only useful if enforced in CI |
| **Who** | Affects: DevOps, code review process |
| **When** | Manifests at PR submission |
| **Where** | TDD (missing section) |
| **How** | Remediate: Add Section 9 "CI/CD Specification" with workflow YAML template |
| **How Much** | Effort: MEDIUM (new section with YAML), Impact: HIGH (automation) |

### GAP-IMPL-008: Jerry CLI Integration

| Dimension | Analysis |
|-----------|----------|
| **What** | TDD ignores existing Jerry CLI architecture |
| **Why** | Jerry already has CLI patterns; custom scripts would fragment tooling |
| **Who** | Affects: User experience, maintainability |
| **When** | Manifests at CLI implementation |
| **Where** | TDD (missing consideration) |
| **How** | Remediate: Add Section 10 "Jerry CLI Integration" with parser, adapter, and bootstrap wiring |
| **How Much** | Effort: MEDIUM (detailed patterns), Impact: HIGH (consistency) |

### GAP-IMPL-009: Implementability Self-Assessment

| Dimension | Analysis |
|-----------|----------|
| **What** | TDD passes automated reviews but would block implementer |
| **Why** | Automated reviews check structure, not execution feasibility |
| **Who** | Affects: Anyone attempting implementation |
| **When** | Manifests immediately upon implementation start |
| **Where** | TDD as a whole |
| **How** | Remediate: Add implementability checklist: "Can I run this? Can I test this? Can I integrate this?" |
| **How Much** | Effort: LOW (checklist), Impact: CRITICAL (quality gate) |

---

## 5. Ishikawa Root Cause Diagram

```
                              ┌──────────────────────────────────────────────┐
                              │   TDD FAILS IMPLEMENTABILITY TEST            │
                              │   (Passes 0.90+ automated reviews)           │
                              └──────────────────────────────────────────────┘
                                                    │
        ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
        │                   │                       │                       │                   │
        ▼                   ▼                       ▼                       ▼                   ▼
┌───────────────┐   ┌───────────────┐       ┌───────────────┐       ┌───────────────┐   ┌───────────────┐
│    METHOD     │   │    MACHINE    │       │   MATERIAL    │       │  MEASUREMENT  │   │  ENVIRONMENT  │
└───────────────┘   └───────────────┘       └───────────────┘       └───────────────┘   └───────────────┘
        │                   │                       │                       │                   │
        ▼                   ▼                       ▼                       ▼                   ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         ROOT CAUSES                                                    │
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│  METHOD (Process Issues)                  MACHINE (Tool Issues)                                       │
│  ├─► Schema design separate from          ├─► Jerry CLI architecture not                              │
│  │   implementation planning                  consulted during TDD creation                           │
│  ├─► TDD created by schema expert,        ├─► Test infrastructure patterns                            │
│  │   not implementation engineer              not referenced in TDD                                   │
│  ├─► Adversarial reviews focus on         ├─► Bootstrap/composition root                              │
│  │   schema correctness, not runnability      pattern ignored                                         │
│  └─► CRITICAL: Design-Implementation      └─► pyproject.toml structure                                │
│      boundary not enforced                    not incorporated                                        │
│                                                                                                        │
│  MATERIAL (Input Issues)                  MEASUREMENT (Validation Issues)                             │
│  ├─► DISC-006 gap analysis focused        ├─► ps-critic reviews structure,                            │
│  │   on schema gaps, not implementation       not executability                                       │
│  ├─► ADR-EN014-001 did not address        ├─► nse-qa reviews compliance,                              │
│  │   integration architecture                 not implementability                                    │
│  ├─► Requirements (EN-003) are            ├─► No "self-implementation test"                           │
│  │   high-level, not detailed                 in review criteria                                      │
│  └─► No prior art analysis of Jerry       └─► CRITICAL: Quality gates don't                           │
│      CLI implementation patterns              test "would Claude be blocked?"                         │
│                                                                                                        │
│  MAN/PEOPLE (Communication Issues)        ENVIRONMENT (Context Issues)                                │
│  ├─► User expectations for               ├─► Time pressure led to                                      │
│  │   "implementation-ready" unclear           schema-first approach                                   │
│  ├─► Agent handoff did not include        ├─► Multiple sessions without                               │
│  │   implementation context                   context preservation                                    │
│  └─► Design vs Implementation             └─► Existing codebase patterns                              │
│      boundary communication gap               not visible during TDD creation                         │
│                                                                                                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Ishikawa Analysis Summary

#### Method Category (Highest Impact)

**Root Cause M-001:** TDD creation focused on "what" (schema structure) not "how" (implementation mechanics)
- **Evidence:** Sections 1-4 have detailed schema specs; Sections 5.2.1/5.2.2 are code snippets without context
- **Countermeasure:** Add implementation architecture sections (6-10) before declaring TDD complete

**Root Cause M-002:** Design-Implementation boundary not enforced
- **Evidence:** TDD declared ready after schema reviews passed, without implementation review
- **Countermeasure:** Add implementability gate: "Can an AI implement this without asking questions?"

#### Measurement Category (Second Highest Impact)

**Root Cause ME-001:** Quality reviews don't test executability
- **Evidence:** ps-critic and nse-qa scored 0.90+ but TDD is unimplementable
- **Countermeasure:** Add implementability criterion to ps-critic rubric

**Root Cause ME-002:** No self-implementation test
- **Evidence:** User had to ask "would you be blocked?" - this should be automatic
- **Countermeasure:** Add ps-validator agent that simulates implementation attempt

#### Machine Category (Third Highest Impact)

**Root Cause MA-001:** Jerry CLI architecture not consulted
- **Evidence:** TDD ignores existing `parser.py`, `adapter.py`, `bootstrap.py` patterns
- **Countermeasure:** Require CLI integration specification for any TDD adding user-facing commands

---

## 6. Prioritized Remediation Requirements

### Priority Matrix (Pareto 80/20)

```
IMPACT vs EFFORT QUADRANT
=========================

                    HIGH IMPACT
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │  ★ GAP-006 (Tests) │  ★ GAP-003 (Exec)  │
    │  ★ GAP-008 (CLI)   │  ★ GAP-007 (CI/CD) │
    │                    │                    │
    │      MEDIUM        │       HIGH         │
    │      EFFORT        │       EFFORT       │
    │                    │                    │
LOW ├────────────────────┼────────────────────┤ HIGH
EFFORT                   │                    EFFORT
    │                    │                    │
    │  ★ GAP-001 (Tech)  │  ★ GAP-009 (Self)  │
    │  ★ GAP-002 (Loc)   │                    │
    │  ★ GAP-004 (SV006) │                    │
    │  ★ GAP-005 (Runtime)                    │
    │                    │                    │
    │       LOW          │       LOW          │
    │      EFFORT        │       EFFORT       │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    LOW IMPACT
```

### Remediation Order (Critical Path)

| Order | Gap ID | Action | Blocks |
|-------|--------|--------|--------|
| 1 | GAP-IMPL-005 | Add Section 7: Runtime Environment | All other gaps |
| 2 | GAP-IMPL-002 | Fix validator location to `src/transcript/` | GAP-003, GAP-008 |
| 3 | GAP-IMPL-008 | Add Section 10: Jerry CLI Integration | GAP-003, GAP-007 |
| 4 | GAP-IMPL-003 | Add Section 6: Integration Specification | GAP-006, GAP-007 |
| 5 | GAP-IMPL-006 | Add Section 8: Testing Strategy | GAP-007, GAP-009 |
| 6 | GAP-IMPL-007 | Add Section 9: CI/CD Specification | GAP-009 |
| 7 | GAP-IMPL-001 | Verify tech selection (jsonschema) | None |
| 8 | GAP-IMPL-004 | Update SV-006 with caller context | None |
| 9 | GAP-IMPL-009 | Add implementability checklist | None |

---

## 7. Jerry CLI Integration Specification

### 7.1 Parser Registration

**File:** `src/interface/cli/parser.py`

**Pattern to Follow:**
```python
def _add_transcript_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add transcript namespace commands.

    Commands:
        - validate-domain: Validate a domain context YAML file

    References:
        - DEC-001: CLI Namespace for Domain Validation
        - TDD-EN014: Domain Schema V2 Design
    """
    transcript_parser = subparsers.add_parser(
        "transcript",
        help="Transcript skill commands",
        description="Manage transcript skill operations.",
    )

    transcript_subparsers = transcript_parser.add_subparsers(
        title="commands",
        dest="command",
        metavar="<command>",
    )

    # validate-domain command
    validate_parser = transcript_subparsers.add_parser(
        "validate-domain",
        help="Validate domain context YAML",
        description="Validate a domain context YAML file against the schema and semantic rules.",
    )
    validate_parser.add_argument(
        "path",
        help="Path to domain YAML file",
    )
    validate_parser.add_argument(
        "--schema-version",
        default="1.1.0",
        help="Schema version to validate against (default: 1.1.0)",
    )
```

**Add to `create_parser()`:**
```python
# Add transcript namespace after config
_add_transcript_namespace(subparsers)
```

### 7.2 Main Routing

**File:** `src/interface/cli/main.py`

**Add handler:**
```python
def _handle_transcript(adapter: CLIAdapter, args: Any, json_output: bool) -> int:
    """Route transcript namespace commands.

    Args:
        adapter: CLI adapter instance
        args: Parsed arguments
        json_output: Whether to output JSON

    Returns:
        Exit code
    """
    if args.command is None:
        print("Error: No transcript command specified. Use 'jerry transcript --help'")
        return 1

    if args.command == "validate-domain":
        return adapter.cmd_transcript_validate_domain(
            path=args.path,
            schema_version=getattr(args, "schema_version", "1.1.0"),
            json_output=json_output,
        )

    print(f"Error: Unknown transcript command '{args.command}'")
    return 1
```

**Update main() routing:**
```python
elif args.namespace == "transcript":
    return _handle_transcript(adapter, args, json_output)
```

### 7.3 CLIAdapter Method

**File:** `src/interface/cli/adapter.py`

**Add method:**
```python
def cmd_transcript_validate_domain(
    self,
    path: str,
    schema_version: str = "1.1.0",
    json_output: bool = False,
) -> int:
    """Validate a domain context YAML file.

    Args:
        path: Path to domain YAML file
        schema_version: Schema version to validate against
        json_output: Whether to output as JSON

    Returns:
        Exit code (0 for valid, 1 for invalid)

    References:
        - DEC-001: CLI Namespace for Domain Validation
        - TDD-EN014: Domain Schema V2 Design
    """
    try:
        query = ValidateDomainQuery(
            path=path,
            schema_version=schema_version,
        )
        result = self._dispatcher.dispatch(query)

        if json_output:
            output = {
                "valid": result.valid,
                "path": path,
                "schema_version": schema_version,
                "errors": [
                    {
                        "path": e.path,
                        "rule": e.rule,
                        "message": e.message,
                        "severity": e.severity,
                    }
                    for e in result.errors
                ],
                "warnings": [
                    {
                        "path": w.path,
                        "rule": w.rule,
                        "message": w.message,
                        "severity": w.severity,
                    }
                    for w in result.warnings
                ],
            }
            print(json.dumps(output, indent=2))
        else:
            if result.valid:
                print(f"Valid: {path}")
                if result.warnings:
                    print(f"Warnings: {len(result.warnings)}")
                    for w in result.warnings:
                        print(f"  [{w.rule}] {w.message}")
            else:
                print(f"Invalid: {path}")
                print(f"Errors: {len(result.errors)}")
                for e in result.errors:
                    print(f"  [{e.rule}] {e.message}")

        return 0 if result.valid else 1

    except FileNotFoundError:
        if json_output:
            print(json.dumps({"error": f"File not found: {path}"}))
        else:
            print(f"Error: File not found: {path}")
        return 1

    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}")
        return 1
```

### 7.4 Bootstrap Wiring

**File:** `src/bootstrap.py`

**Add factory functions:**
```python
from src.transcript.application.queries import ValidateDomainQuery
from src.transcript.application.handlers.queries import ValidateDomainQueryHandler
from src.transcript.domain.validators import DomainValidator
from src.transcript.infrastructure.adapters import FilesystemSchemaAdapter


def create_domain_validator(
    schema_version: str = "1.1.0",
) -> DomainValidator:
    """Create a domain validator with schema loaded.

    Args:
        schema_version: Schema version to use

    Returns:
        DomainValidator instance with schema loaded.
    """
    schema_adapter = FilesystemSchemaAdapter()
    schema = schema_adapter.load_schema(schema_version)
    return DomainValidator(schema=schema)


def create_query_dispatcher() -> QueryDispatcher:
    """Create a fully configured QueryDispatcher."""
    # ... existing code ...

    # Add domain validation handler
    domain_validator = create_domain_validator()
    validate_domain_handler = ValidateDomainQueryHandler(
        validator=domain_validator,
    )
    dispatcher.register(ValidateDomainQuery, validate_domain_handler.handle)

    return dispatcher
```

---

## 8. Test Strategy Specification

### 8.1 Test Pyramid for Domain Validation

```
                    ┌─────────────────┐
                    │   E2E (5%)      │
                    │ CLI subprocess  │
                   ┌┴─────────────────┴┐
                   │   Integration     │
                   │      (15%)        │
                  ┌┴───────────────────┴┐
                  │   Unit Tests (70%)  │
                  │  - SV-001..SV-006   │
                  │  - ValidationResult │
                 ┌┴─────────────────────┴┐
                 │  Contract Tests (10%) │
                 │  - JSON output format │
                 └───────────────────────┘
```

### 8.2 RED/GREEN/REFACTOR Flow

**Phase 1: RED (Write Failing Tests)**

```python
# tests/unit/transcript/validators/test_sv001_relationship_targets.py

def test_sv001_when_target_exists_then_no_error():
    """SV-001: Valid relationship targets pass."""
    # RED: Write test before implementation
    domain_data = {
        "entity_definitions": {
            "blocker": {
                "relationships": [
                    {"type": "blocks", "target": "commitment"}
                ]
            },
            "commitment": {"description": "..."}
        }
    }

    errors = sv001_relationship_targets(domain_data)

    assert len(errors) == 0


def test_sv001_when_target_missing_then_error():
    """SV-001: Missing relationship target fails."""
    domain_data = {
        "entity_definitions": {
            "blocker": {
                "relationships": [
                    {"type": "blocks", "target": "nonexistent"}
                ]
            }
        }
    }

    errors = sv001_relationship_targets(domain_data)

    assert len(errors) == 1
    assert errors[0].rule == "SV-001"
    assert "nonexistent" in errors[0].message
```

**Phase 2: GREEN (Minimal Implementation)**

```python
# src/transcript/domain/validators/semantic_validators.py

def sv001_relationship_targets(domain_data: dict) -> list[ValidationError]:
    """SV-001: Validate relationship targets exist."""
    errors = []
    entity_names = set(domain_data.get("entity_definitions", {}).keys())

    for entity_name, entity_def in domain_data.get("entity_definitions", {}).items():
        for rel in entity_def.get("relationships", []):
            target = rel.get("target")
            if target and target not in entity_names:
                errors.append(ValidationError(
                    path=f"entity_definitions.{entity_name}.relationships",
                    rule="SV-001",
                    message=f"Target '{target}' not in entity_definitions",
                    severity="error",
                ))

    return errors
```

**Phase 3: REFACTOR**
- Extract common patterns
- Add type hints
- Improve error messages
- Add logging

### 8.3 Test File Locations

| Test Type | File Path | Coverage |
|-----------|-----------|----------|
| Unit: SV-001 | `tests/unit/transcript/validators/test_sv001.py` | Relationship targets |
| Unit: SV-002 | `tests/unit/transcript/validators/test_sv002.py` | Context rule entities |
| Unit: SV-003 | `tests/unit/transcript/validators/test_sv003.py` | Validation entities |
| Unit: SV-004 | `tests/unit/transcript/validators/test_sv004.py` | Extraction rule entities |
| Unit: SV-005 | `tests/unit/transcript/validators/test_sv005.py` | Duplicate entity names |
| Unit: SV-006 | `tests/unit/transcript/validators/test_sv006.py` | Circular relationships |
| Unit: Full | `tests/unit/transcript/validators/test_domain_validator.py` | Pipeline integration |
| Integration | `tests/integration/transcript/test_cli_validate_domain.py` | CLI adapter |
| Contract | `tests/contract/transcript/test_validation_output.py` | JSON format |
| E2E | `tests/e2e/transcript/test_validate_domain_workflow.py` | Full workflow |

### 8.4 Coverage Requirements

| Layer | Target | Rationale |
|-------|--------|-----------|
| Semantic validators (SV-*) | 100% | Critical path, pure functions |
| Domain validator pipeline | 95% | Core logic |
| CLI adapter | 90% | User-facing |
| Bootstrap wiring | 80% | Configuration code |

---

## 9. CI/CD Pipeline Specification

### 9.1 GitHub Actions Workflow

**File:** `.github/workflows/validate-domain.yml`

```yaml
name: Domain Validation

on:
  push:
    paths:
      - 'skills/transcript/domains/**/*.yaml'
      - 'skills/transcript/domains/**/*.yml'
      - 'src/transcript/**'
      - 'tests/unit/transcript/**'
  pull_request:
    paths:
      - 'skills/transcript/domains/**/*.yaml'
      - 'skills/transcript/domains/**/*.yml'
      - 'src/transcript/**'
      - 'tests/unit/transcript/**'

jobs:
  validate-domains:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev,test]"

      - name: Run domain validation
        run: |
          for file in skills/transcript/domains/*.yaml; do
            echo "Validating: $file"
            jerry transcript validate-domain "$file"
          done

      - name: Run validator tests
        run: |
          pytest tests/unit/transcript/validators/ -v --cov=src/transcript

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: transcript-validators
```

### 9.2 Quality Gates

| Gate | Threshold | Enforcement |
|------|-----------|-------------|
| All domain YAMLs valid | 100% | Block merge |
| Validator test coverage | ≥90% | Block merge |
| SV-* tests pass | 100% | Block merge |
| No new validation errors | 0 | Block merge |

---

## 10. Recommendations for TDD Revision

### 10.1 Required New Sections

| Section | Title | Content |
|---------|-------|---------|
| 6 | Integration Specification | Sequence diagrams for skill, CLI, CI integration |
| 7 | Runtime Environment | Python 3.11+, dependencies, venv, execution |
| 8 | Testing Strategy | RED/GREEN/REFACTOR, test locations, coverage |
| 9 | CI/CD Specification | GitHub Actions workflow, quality gates |
| 10 | Jerry CLI Integration | Parser, adapter, bootstrap patterns |

### 10.2 Section 5.2 Revisions

| Current | Revision |
|---------|----------|
| 5.2.1 shows code in `skills/transcript/validators/` | Move to `src/transcript/domain/validators/` |
| 5.2.2 SV-006 is dangling | Show full call chain from CLI to SV-006 |
| No error handling | Add error handling specification |
| No logging | Add logging specification |

### 10.3 Implementability Checklist (New Section 11)

The revised TDD should include this self-assessment checklist:

```markdown
## 11. Implementability Checklist

Before declaring TDD complete, verify:

- [ ] **Runtime:** Can I set up the environment? (Python version, venv, deps)
- [ ] **Location:** Do file paths follow Jerry hexagonal architecture?
- [ ] **Execution:** Can I trace from user action to code execution?
- [ ] **Testing:** Can I write RED tests before implementation?
- [ ] **Integration:** Are all integration points specified? (CLI, agents, CI)
- [ ] **CI/CD:** Is the GitHub Actions workflow specified?
- [ ] **Self-Test:** If I gave this to another Claude instance, could they implement without blocking questions?
```

---

## 11. Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | ps-analyst (v2.0.0) | Initial comprehensive gap analysis |

---

## 12. References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | DISC-008 | Internal | Gap discovery source |
| 2 | DEC-001 | Internal | User decisions on validators and CLI |
| 3 | TDD-EN014-domain-schema-v2.md | Internal | Document under analysis |
| 4 | src/interface/cli/main.py | Internal | Jerry CLI architecture |
| 5 | src/interface/cli/parser.py | Internal | Parser namespace pattern |
| 6 | src/interface/cli/adapter.py | Internal | CLIAdapter pattern |
| 7 | src/bootstrap.py | Internal | Composition root pattern |
| 8 | pyproject.toml | Internal | Python project configuration |
| 9 | tests/conftest.py | Internal | Pytest configuration |

---

## 13. Metadata

```yaml
id: "EN-014-e-176"
ps_id: "EN-014"
entry_id: "e-176"
type: analysis
agent: ps-analyst
agent_version: "2.0.0"
topic: "Comprehensive TDD Implementation Gap Analysis"
status: COMPLETE
created_at: "2026-01-29T15:00:00Z"
frameworks_applied:
  - "5W2H"
  - "Ishikawa (6M)"
  - "Pareto (80/20)"
gaps_analyzed: 9
root_causes_identified: 8
recommendations: 15
integration_points_specified: 5
test_files_specified: 10
constitutional_compliance:
  - "P-001 (Truth and Accuracy)"
  - "P-002 (File Persistence)"
  - "P-004 (Provenance)"
```

---

*Document ID: EN-014-e-176*
*Analysis Session: en014-task176-gap-analysis*
*Constitutional Compliance: P-001, P-002, P-004*

**Generated by:** ps-analyst agent (v2.0.0)
**Framework Application:** 5W2H + Ishikawa + Pareto
**Prior Art:** Jerry CLI architecture, pytest patterns, GitHub Actions
