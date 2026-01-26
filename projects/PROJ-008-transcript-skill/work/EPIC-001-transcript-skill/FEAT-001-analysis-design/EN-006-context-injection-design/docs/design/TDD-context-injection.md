# Technical Design Document: Context Injection Mechanism

<!--
DOCUMENT: TDD-context-injection.md
VERSION: 1.1.0
STATUS: DRAFT
TASK: TASK-034 (Phase 2, Iteration 2)
AUTHOR: ps-architect
QUALITY TARGET: >= 0.90
-->

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Document ID** | TDD-CI-001 |
| **Version** | 1.1.0 |
| **Status** | DRAFT |
| **Quality Score** | Pending ps-critic review |
| **Created** | 2026-01-26 |
| **Author** | ps-architect |
| **Reviewer** | ps-critic (pending) |
| **Validator** | nse-architecture (pending) |

### Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-01-26 | ps-architect | Initial TDD creation (Iteration 1) |
| 1.1.0 | 2026-01-26 | ps-architect | Iteration 2: Added Trade Study Summary (AC-012), Interface Verification Matrix (AC-013), EN-003 Backward Traceability (AC-009), Resolved TBD comments (AC-017), Added AGENT.md example (AC-004), Completed API Contracts (AC-007) |

### Approval Status

| Role | Name | Status | Date |
|------|------|--------|------|
| Architect | ps-architect | COMPLETED | 2026-01-26 |
| NASA SE Validator | nse-architecture | PENDING | - |
| Quality Reviewer | ps-critic | PENDING | - |
| Human Approver | User | PENDING (GATE-4) | - |

---

## L0: Executive Summary (ELI5)

### What is Context Injection?

Imagine teaching a new employee about your company. Instead of explaining everything from scratch every time, you give them an **employee handbook** with company-specific terminology, processes, and rules. **Context injection** does the same thing for AI agents - it gives them domain-specific knowledge so they can work smarter on specialized tasks.

### How Does It Work?

```
THREE-STEP PROCESS (Like Making Coffee)
=======================================

STEP 1: LOAD THE BEANS (Static Context)
┌─────────────────────────────────────────┐
│ Read domain knowledge from files:       │
│ • Legal terms dictionary               │
│ • Sales playbook rules                 │
│ • Engineering patterns                 │
└─────────────────────────────────────────┘
                    │
                    ▼
STEP 2: ADD THE WATER (Dynamic Context)
┌─────────────────────────────────────────┐
│ Get runtime information:               │
│ • Document being analyzed              │
│ • User preferences                     │
│ • Previous analysis results            │
└─────────────────────────────────────────┘
                    │
                    ▼
STEP 3: BREW (Template Resolution)
┌─────────────────────────────────────────┐
│ Combine and serve to the agent:        │
│ "Analyze this {{$domain}} transcript   │
│  using these {{$extraction_rules}}"    │
└─────────────────────────────────────────┘
```

### Key Numbers

| Metric | Target | What It Means |
|--------|--------|---------------|
| Loading Time | < 500ms | Context loads faster than a blink |
| Max Size | 50MB | Prevents memory overload |
| Domains Supported | 3+ | Legal, sales, engineering out-of-box |
| Fallback Success | 100% | Always works, even if parts fail |

### Why Does This Matter?

**Without Context Injection:**
- Generic AI answers that miss domain nuances
- Manual prompt engineering every time (4+ hours)
- Inconsistent results across sessions

**With Context Injection:**
- Domain-expert-level extraction accuracy (+50%)
- Configure once, use everywhere (<2 hours)
- Deterministic, testable results

---

## L1: Technical Design (Software Engineer)

### 1. Overview

#### 1.1 Purpose

This TDD describes the technical design for the Context Injection Mechanism, which enables the Transcript Skill to load, validate, and apply domain-specific context to AI agents. The design implements the Hybrid Approach (A5) selected in the EN-006 trade study, combining:

1. **Static Context** - YAML files with domain schemas
2. **Dynamic Context** - Runtime information from MCP tools
3. **Template Resolution** - Variable substitution in prompts

#### 1.2 Scope

**In Scope:**
- `IContextProvider` port interface definition
- `FilesystemContextAdapter` for static YAML loading
- `TemplateResolver` for `{{$variable}}` substitution
- JSON Schema validation for context payloads
- Graceful degradation when dynamic sources fail
- Circuit breaker for external calls

**Out of Scope:**
- Full MCP server implementation (future Phase 3)
- Cross-agent context sharing (future enhancement)
- Context compression/optimization (future enhancement)

#### 1.3 Audience

| Audience | Relevant Sections |
|----------|------------------|
| Developers implementing context injection | Sections 2-4 |
| QA engineers writing tests | Sections 4.3, 6.3 |
| DevOps configuring deployments | Section 5.2 |
| Architects reviewing design | Sections 2.2, 3.1 |

#### 1.4 Requirements Traceability

This TDD implements the following requirements from EN-006 Requirements Supplement:

| Requirement | Section | Implementation |
|-------------|---------|----------------|
| REQ-CI-I-001 | 2.2 | IContextProvider port definition |
| REQ-CI-I-002 | 2.2.1 | Port operations specification |
| REQ-CI-F-001 | 3.1 | Static context loading from YAML |
| REQ-CI-F-002 | 3.1.2 | SKILL.md context section |
| REQ-CI-F-005 | 3.2 | Loading lifecycle state machine |
| REQ-CI-F-006 | 3.3 | JSON Schema validation |
| REQ-CI-F-008 | 3.4 | Template variable resolution |
| REQ-CI-F-009 | 3.5 | Context merging |
| REQ-CI-F-010 | 3.6 | Error propagation |
| REQ-CI-F-011 | 3.7 | Graceful degradation |
| REQ-CI-P-001 | 5.1 | 500ms loading time |
| REQ-CI-P-002 | 5.1 | 50MB size limit |
| REQ-CI-P-003 | 3.7.2 | Circuit breaker pattern |

#### 1.5 Trade Study Summary

This TDD implements the **Hybrid Approach (A5)** selected from the EN-006 Trade Space Analysis. The trade study evaluated 5 candidate approaches using 8 weighted criteria.

**Reference:** `docs/research/en006-trade-space.md`

##### 1.5.1 Candidate Approaches

| ID | Approach | Description | Weighted Score |
|----|----------|-------------|----------------|
| A1 | Static Context Files | Pre-loaded markdown/YAML files | 8.05 |
| A2 | Dynamic Tool-Based | Runtime retrieval via tools | 6.75 |
| A3 | Task Dependency Injection | Explicit task `context=[]` | 6.55 |
| A4 | Template Variables | `{{$variable}}` substitution | 7.85 |
| **A5** | **Hybrid (Selected)** | **Combination of A1 + A2 + A4** | **8.25** |

##### 1.5.2 Evaluation Criteria and Weights

| Criterion | Weight | A5 Score | Rationale |
|-----------|--------|----------|-----------|
| C1: Ease of Configuration | 15% | 8 | Clear separation of static/dynamic |
| C2: Performance (Latency) | 15% | 8 | Static handles most context |
| C3: Flexibility | 10% | 9 | Dynamic layer fetches fresh data |
| C4: Testability | 15% | 8 | Mock dynamic, test static directly |
| C5: Model-Agnostic | 15% | 9 | Best alignment with MA-001 |
| C6: Schema Validation | 10% | 8 | JSON Schema on YAML files |
| C7: Memory/Persistence | 10% | 8 | File-based persistence |
| C8: MCP Compatibility | 10% | 8 | Clear migration path |

##### 1.5.3 Decision Rationale

```
TRADE STUDY SCORING VISUALIZATION
=================================

A5: Hybrid      ████████████████████████████████████████████ 8.25  ★ SELECTED
A1: Static      ████████████████████████████████████████     8.05
A4: Templates   ███████████████████████████████████████      7.85
A2: Dynamic     █████████████████████████████████            6.75
A3: Task Dep    ████████████████████████████████             6.55

                ├────────┼────────┼────────┼────────┼────────┤
                0        2        4        6        8       10
```

**Selection Justification:**
1. **Highest weighted score** (8.25/10) across all criteria
2. **Best alignment** with EN-003 requirements (MA-001, MA-002, SK-004)
3. **No score below 8** - balanced across all criteria
4. **Clear MCP migration path** for future Phase 3 evolution
5. **Combines best aspects**: Static files for stability, dynamic tools for freshness, templates for customization

#### 1.6 EN-003 Backward Traceability

This TDD addresses the following base requirements from EN-003 (REQUIREMENTS-SPECIFICATION.md):

##### 1.6.1 Stakeholder Needs Addressed

| EN-003 ID | Need Statement | TDD Implementation |
|-----------|----------------|-------------------|
| STK-009 | System must integrate seamlessly with Jerry framework | IContextProvider port, SKILL.md integration (Sections 2.2, 3.1.2) |
| STK-010 | System must support pipeline automation (CI/CD) | JSON Schema validation, deterministic loading (Section 3.3) |

##### 1.6.2 Interface Requirements Addressed

| EN-003 ID | Requirement | TDD Implementation |
|-----------|-------------|-------------------|
| IR-004 | System SHALL provide SKILL.md interface compatible with Jerry | SKILL.md context_injection section (Section 3.1.2) |
| IR-005 | System architecture SHALL conform to hexagonal patterns | IContextProvider port, FilesystemContextAdapter (Section 2.2) |

##### 1.6.3 Non-Functional Requirements Addressed

| EN-003 ID | Requirement | TDD Implementation |
|-----------|-------------|-------------------|
| MA-001 | Context format SHALL be model-agnostic | YAML schemas, no provider-specific features (Section 3.1.1) |
| MA-002 | Avoid provider-specific features | Generic template syntax `{{$variable}}` (Section 3.4) |
| NFR-001 | Processing performance target | 500ms context loading budget (Section 5.1) |

##### 1.6.4 Traceability Matrix

```
EN-003 REQUIREMENT → TDD SECTION MAPPING
========================================

    EN-003 ID       │   TDD Section(s)           │   Implementation
────────────────────┼────────────────────────────┼────────────────────────
    STK-009         │   2.2, 3.1.2, 4.2          │   Jerry framework integration
    STK-010         │   3.3, 4.1.1, 5.2          │   CI/CD compatibility
    IR-004          │   3.1.2, 4.1.2             │   SKILL.md interface
    IR-005          │   2.2, 2.2.1, 3.1.3        │   Hexagonal architecture
    MA-001          │   3.1.1, 3.3               │   Model-agnostic format
    MA-002          │   3.4                      │   No provider lock-in
    NFR-001         │   5.1                      │   Performance budget
────────────────────┴────────────────────────────┴────────────────────────
```

---

### 2. Architecture

#### 2.1 System Context Diagram

```
SYSTEM CONTEXT: Context Injection Mechanism
============================================

                     ┌─────────────────────────────────────────────┐
                     │              JERRY FRAMEWORK                 │
                     │  ┌─────────────────────────────────────┐    │
                     │  │           Transcript Skill           │    │
                     │  │                                     │    │
                     │  │  ┌──────────────────────────────┐  │    │
                     │  │  │  CONTEXT INJECTION MECHANISM  │  │    │
                     │  │  │  (This TDD)                   │  │    │
                     │  │  └──────────────────────────────┘  │    │
                     │  │              │  ▲                   │    │
                     │  └──────────────│──│───────────────────┘    │
                     │                 │  │                         │
                     └─────────────────│──│─────────────────────────┘
                                       │  │
           ┌───────────────────────────┼──┼───────────────────────────┐
           │                           │  │                           │
           ▼                           │  │                           ▼
    ┌─────────────┐           ┌────────▼──┴──────┐           ┌─────────────┐
    │  SKILL.md   │           │  EXTERNAL SYSTEM │           │   MCP       │
    │  AGENT.md   │           │  ─────────────── │           │  SERVERS    │
    │  contexts/  │           │  • CLI Input     │           │  ────────   │
    │  *.yaml     │           │  • User Prefs    │           │  memory-    │
    │             │           │  • Document      │           │  keeper     │
    └─────────────┘           └──────────────────┘           └─────────────┘
    Static Context                 Triggering                Dynamic Context
    (Filesystem)                   Inputs                    (Future Phase)
```

#### 2.2 Component Architecture

```
HEXAGONAL ARCHITECTURE: Context Injection
=========================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           INTERFACE LAYER                                    │
│                      (Primary Adapters - Driving)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │   CLI Adapter    │  │  SKILL.md Loader │  │  Agent Invoker   │          │
│  │   (--domain)     │  │  (SessionStart)  │  │  (Task dispatch) │          │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                     │                     │
│           └─────────────────────┼─────────────────────┘                     │
│                                 │                                            │
└─────────────────────────────────┼────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                                   │
│                       (Use Cases - Commands/Queries)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    LoadContextCommand                               │    │
│  │  ────────────────────────────────────────────────────────────────  │    │
│  │  + domain: str                                                      │    │
│  │  + document_id: Optional[str]                                       │    │
│  │  + template_vars: Dict[str, Any]                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    LoadContextCommandHandler                        │    │
│  │  ────────────────────────────────────────────────────────────────  │    │
│  │  - context_provider: IContextProvider                              │    │
│  │  - lifecycle: ContextLoadingLifecycle                              │    │
│  │  ────────────────────────────────────────────────────────────────  │    │
│  │  + handle(command) -> ContextResult                                 │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 ▼                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                      IContextProvider [PORT]                        │    │
│  │  ────────────────────────────────────────────────────────────────  │    │
│  │  + load_static_context(domain: str) -> ContextResult               │    │
│  │  + load_dynamic_context(doc_id: str) -> ContextResult              │    │
│  │  + resolve_template(template: str, ctx: Context) -> str            │    │
│  │  + validate_context(context: Context) -> ValidationResult          │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────┼───────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE LAYER                                  │
│                     (Secondary Adapters - Driven)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │ Filesystem         │  │ MCP Context        │  │ Memory Keeper      │    │
│  │ ContextAdapter     │  │ Adapter (Stub)     │  │ Adapter (Future)   │    │
│  │                    │  │                    │  │                    │    │
│  │ • YAML parsing     │  │ • MCP protocol     │  │ • Cross-session    │    │
│  │ • JSON Schema      │  │ • Circuit breaker  │  │ • Persistence      │    │
│  │ • SKILL.md extract │  │ • Fallback logic   │  │                    │    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│           │                       │                       │                 │
│           ▼                       ▼                       ▼                 │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐         │
│  │ contexts/   │          │ MCP Server  │          │ memory-     │         │
│  │ *.yaml      │          │ (External)  │          │ keeper      │         │
│  └─────────────┘          └─────────────┘          └─────────────┘         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.2.1 IContextProvider Port Interface

```python
from typing import Protocol, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ContextLoadStatus(Enum):
    """Status of context loading operation."""
    SUCCESS = "success"
    PARTIAL = "partial"       # Some sources succeeded, others failed
    FALLBACK = "fallback"     # Using fallback context
    FAILED = "failed"


@dataclass(frozen=True)
class ValidationError:
    """Single validation error."""
    field: str
    message: str
    path: Optional[str] = None


@dataclass(frozen=True)
class ValidationResult:
    """Result of context validation."""
    is_valid: bool
    errors: tuple[ValidationError, ...]
    schema_version: str


@dataclass(frozen=True)
class Context:
    """Immutable context container."""
    domain: str
    entities: Dict[str, Any]
    extraction_rules: tuple[Dict[str, Any], ...]
    prompt_guidance: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class ContextResult:
    """Result of context loading with status."""
    status: ContextLoadStatus
    context: Optional[Context]
    errors: tuple[str, ...]
    load_time_ms: float


class IContextProvider(Protocol):
    """Port interface for context injection.

    This is a ONE-WAY DOOR decision - API changes require major version bump.
    Implements: REQ-CI-I-001, REQ-CI-I-002

    All methods return Result types - NEVER raise exceptions (REQ-CI-F-010).
    """

    def load_static_context(self, domain: str) -> ContextResult:
        """Load domain schema from filesystem.

        Args:
            domain: Domain identifier (e.g., "legal", "sales")

        Returns:
            ContextResult with loaded context or error details

        Implements: REQ-CI-F-001
        """
        ...

    def load_dynamic_context(self, document_id: str) -> ContextResult:
        """Load runtime context from MCP/tools.

        Args:
            document_id: Identifier for the document being analyzed

        Returns:
            ContextResult with dynamic context or fallback

        Implements: REQ-CI-F-011 (fallback to static on failure)
        """
        ...

    def resolve_template(
        self,
        template: str,
        context: Context
    ) -> str:
        """Resolve {{$variable}} placeholders in template.

        Args:
            template: Template string with {{$variable}} syntax
            context: Context object with variable values

        Returns:
            Resolved template string

        Implements: REQ-CI-F-008
        """
        ...

    def validate_context(self, context: Context) -> ValidationResult:
        """Validate context against JSON Schema.

        Args:
            context: Context object to validate

        Returns:
            ValidationResult with validation status

        Implements: REQ-CI-F-006
        """
        ...

    def merge_contexts(
        self,
        static: Context,
        dynamic: Optional[Context]
    ) -> Context:
        """Merge static and dynamic contexts.

        Dynamic context values override static for same keys.

        Args:
            static: Base static context
            dynamic: Optional dynamic context overlay

        Returns:
            Merged context object

        Implements: REQ-CI-F-009
        """
        ...
```

#### 2.3 Data Flow Diagram

```
CONTEXT INJECTION DATA FLOW
===========================

User Request                     Context Loading                    Agent Execution
────────────                     ───────────────                    ───────────────

    │
    ▼
┌─────────────────┐
│ "Analyze this   │
│  legal contract │
│  transcript"    │
└────────┬────────┘
         │
         │ 1. Extract domain="legal"
         ▼
┌─────────────────┐
│ LoadContext     │
│ Command         │
│ ────────────    │
│ domain: "legal" │
│ doc_id: "doc1"  │
└────────┬────────┘
         │
         │ 2. Execute loading lifecycle
         ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                    CONTEXT LOADING LIFECYCLE                               │
│                                                                            │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐               │
│  │  STATIC     │      │  DYNAMIC    │      │  TEMPLATE   │               │
│  │  LOADING    │─────►│  LOADING    │─────►│  RESOLUTION │               │
│  │             │      │             │      │             │               │
│  │ legal.yaml  │      │ MCP/Tools   │      │ {{$domain}} │               │
│  │ SKILL.md    │      │ (optional)  │      │ {{$rules}}  │               │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘               │
│         │                    │                    │                       │
│         │ Context:           │ Context:           │ Resolved:            │
│         │ - entities         │ - doc_metadata     │ - final_prompt       │
│         │ - rules            │ - user_prefs       │                       │
│         │ - guidance         │ - cache            │                       │
│         └────────────────────┴────────────────────┘                       │
│                              │                                            │
│                              ▼ 3. Merge all contexts                      │
│                    ┌─────────────────┐                                    │
│                    │ MERGED CONTEXT  │                                    │
│                    │ ───────────────│                                    │
│                    │ domain: "legal" │                                    │
│                    │ entities: {...} │                                    │
│                    │ rules: [...]    │                                    │
│                    │ prompt: "..."   │                                    │
│                    └────────┬────────┘                                    │
│                             │                                             │
└─────────────────────────────┼─────────────────────────────────────────────┘
                              │
                              │ 4. Pass to agent
                              ▼
                    ┌─────────────────┐
                    │ AGENT EXECUTION │
                    │ ───────────────│
                    │ • ts-parser     │
                    │ • ts-extractor  │
                    │ • ts-formatter  │
                    └─────────────────┘
```

---

### 3. Design Details

#### 3.1 Static Context Loading

##### 3.1.1 Domain Schema Structure

**Location:** `skills/transcript/contexts/{domain}.yaml`

```yaml
# contexts/legal.yaml - Legal Domain Schema
# Implements: REQ-CI-F-001

schema_version: "1.0.0"
domain: "legal"
display_name: "Legal Document Analysis"

# Entity definitions for extraction
entity_definitions:
  party:
    description: "Legal entity (person or organization) mentioned in document"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "enum"
        values: ["buyer", "seller", "guarantor", "witness", "attorney"]
        required: true
      - name: "jurisdiction"
        type: "string"
        required: false
    extraction_patterns:
      - pattern: '{{name}} \((?:the\s+)?"{{role}}"\)'
        confidence: 0.95
      - pattern: "{{role}}:\s*{{name}}"
        confidence: 0.85

  obligation:
    description: "Contractual obligation or commitment"
    attributes:
      - name: "obligor"
        type: "reference"
        ref: "party"
      - name: "obligee"
        type: "reference"
        ref: "party"
      - name: "terms"
        type: "string"
      - name: "deadline"
        type: "date"
        format: "ISO8601"
    extraction_patterns:
      - pattern: "{{obligor}} shall {{terms}}"
        confidence: 0.90

  date:
    description: "Significant date mentioned in document"
    attributes:
      - name: "value"
        type: "date"
        format: "ISO8601"
      - name: "context"
        type: "string"
        description: "What this date represents (signing, effective, deadline)"
    extraction_patterns:
      - pattern: '\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b'
        confidence: 0.80
      - pattern: '\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        confidence: 0.90

# Extraction rules with priority ordering
extraction_rules:
  - id: "identify-parties"
    description: "Identify all parties by name and role"
    entity_type: "party"
    priority: 1
    confidence_threshold: 0.85

  - id: "extract-obligations"
    description: "Extract contractual obligations and terms"
    entity_type: "obligation"
    priority: 2
    confidence_threshold: 0.80
    dependencies:
      - "identify-parties"  # Must identify parties first

  - id: "extract-dates"
    description: "Extract all significant dates in ISO 8601 format"
    entity_type: "date"
    priority: 3
    confidence_threshold: 0.85

# Prompt guidance for LLM
prompt_guidance: |
  When analyzing legal documents:

  1. **Party Identification**: Identify all parties before analyzing obligations.
     Look for named individuals and organizations with their legal roles.

  2. **Obligation Analysis**: Extract each obligation with clear obligor→obligee
     relationships. Note any conditions or contingencies.

  3. **Date Extraction**: Convert all dates to ISO 8601 format. Note the context
     of each date (signing date, effective date, deadline, etc.).

  4. **Confidence Scoring**: Flag any extractions below 0.85 confidence for
     human review.

  5. **Jurisdictional Notes**: Note any jurisdiction-specific terms or clauses
     that may require specialized interpretation.

# Metadata
metadata:
  author: "ps-architect"
  created: "2026-01-26"
  reviewed_by: "legal-sme"
  industry_standard: "IRAC Method"
```

##### 3.1.2 SKILL.md Context Section

**Location:** `skills/transcript/SKILL.md` frontmatter

```yaml
# SKILL.md frontmatter - Context injection configuration
# Implements: REQ-CI-F-002

context_injection:
  enabled: true
  default_domain: "general"

  # Available domains
  available_domains:
    - id: "general"
      schema: "contexts/general.yaml"
      description: "General-purpose transcript analysis"
    - id: "legal"
      schema: "contexts/legal.yaml"
      description: "Legal document and deposition analysis"
    - id: "sales"
      schema: "contexts/sales.yaml"
      description: "Sales call and meeting analysis"
    - id: "engineering"
      schema: "contexts/engineering.yaml"
      description: "Technical meeting and standup analysis"

  # Context loading configuration
  loading:
    static_first: true              # Always load static before dynamic
    max_load_time_ms: 500           # REQ-CI-P-001
    max_context_size_mb: 50         # REQ-CI-P-002
    fallback_to_static: true        # REQ-CI-F-011

  # Template configuration
  template:
    syntax: "{{$variable}}"         # Semantic Kernel compatible
    resolution_timeout_ms: 50       # REQ-CI-P-004

  # Validation
  validation:
    schema_path: "schemas/context-schema.json"
    validate_on_load: true          # REQ-CI-F-006
    strict_mode: false              # Allow additional properties
```

##### 3.1.3 AGENT.md Persona Context

**Location:** `skills/transcript/agents/{agent-name}/AGENT.md` frontmatter

**Implements:** REQ-CI-F-003

AGENT.md files provide persona-specific context that is injected when agents are invoked. This enables specialized behavior per agent within the skill.

```yaml
# agents/ts-extractor/AGENT.md frontmatter
# Persona context for the extraction agent

agent_context:
  persona: "ts-extractor"
  role: "Entity Extraction Specialist"

  # Persona-specific capabilities
  capabilities:
    - "Speaker identification from voice tags and patterns"
    - "Action item extraction with confidence scoring"
    - "Decision and question classification"
    - "Named entity recognition (PERSON, ORG, DATE)"

  # Extraction behavior configuration
  extraction_config:
    # Confidence thresholds per entity type
    confidence_thresholds:
      speaker: 0.95        # High confidence for structural extraction
      action_item: 0.80    # Moderate for semantic extraction
      decision: 0.75       # Lower for implicit decisions
      question: 0.70       # Lowest for classification

    # Entity prioritization order
    extraction_order:
      - speakers          # Must identify speakers first
      - action_items      # Then commitments
      - decisions         # Then decisions
      - questions         # Finally questions

    # Fallback behavior
    fallback_strategy: "rule_based"  # Use rules if ML confidence low

  # Domain context override
  # When present, overrides SKILL.md context for this agent
  domain_overrides:
    legal:
      confidence_boost: 0.05  # Legal domain gets confidence boost
      additional_entities:
        - "obligation"
        - "party"
        - "jurisdiction"

  # Prompt injection point
  prompt_prefix: |
    You are a specialized entity extraction agent.
    Focus on precision over recall for action items.
    Always provide source citations for extractions.
```

**Context Loading Flow:**

```
AGENT.MD CONTEXT LOADING
========================

               SKILL.md                      AGENT.md
           (Skill-level context)         (Agent-level context)
                   │                            │
                   │ 1. Load at skill           │ 2. Load at agent
                   │    activation               │    invocation
                   ▼                            ▼
           ┌──────────────┐             ┌──────────────┐
           │ context_     │             │ agent_       │
           │ injection:   │             │ context:     │
           │   enabled    │             │   persona    │
           │   domains    │             │   config     │
           │   loading    │             │   overrides  │
           └──────┬───────┘             └──────┬───────┘
                  │                            │
                  └────────────┬───────────────┘
                               │
                               ▼ 3. Merge (agent overrides skill)
                      ┌──────────────────┐
                      │  MERGED CONTEXT  │
                      │  ───────────────│
                      │  • skill base    │
                      │  • agent config  │
                      │  • domain rules  │
                      └──────────────────┘
```

##### 3.1.4 FilesystemContextAdapter Implementation

```python
"""Filesystem adapter for static context loading.

Implements: REQ-CI-F-001, REQ-CI-F-002, REQ-CI-F-006
"""

from pathlib import Path
from typing import Optional
import yaml
import json
import time
from dataclasses import dataclass

from ..ports.context_provider import (
    IContextProvider,
    Context,
    ContextResult,
    ContextLoadStatus,
    ValidationResult,
    ValidationError,
)


@dataclass
class FilesystemContextAdapter:
    """Adapter for loading context from filesystem.

    Loads YAML domain schemas and validates against JSON Schema.
    """

    contexts_dir: Path
    schema_path: Path
    max_load_time_ms: float = 500.0
    max_size_bytes: int = 50 * 1024 * 1024  # 50MB

    def __post_init__(self) -> None:
        self._schema = self._load_json_schema()
        self._cache: dict[str, Context] = {}

    def load_static_context(self, domain: str) -> ContextResult:
        """Load domain schema from YAML file.

        Implements: REQ-CI-F-001
        """
        start_time = time.monotonic()

        # Check cache first
        if domain in self._cache:
            load_time = (time.monotonic() - start_time) * 1000
            return ContextResult(
                status=ContextLoadStatus.SUCCESS,
                context=self._cache[domain],
                errors=(),
                load_time_ms=load_time,
            )

        # Locate schema file
        schema_path = self.contexts_dir / f"{domain}.yaml"

        if not schema_path.exists():
            load_time = (time.monotonic() - start_time) * 1000
            return ContextResult(
                status=ContextLoadStatus.FAILED,
                context=None,
                errors=(f"Domain schema not found: {schema_path}",),
                load_time_ms=load_time,
            )

        # Check file size (REQ-CI-P-002)
        file_size = schema_path.stat().st_size
        if file_size > self.max_size_bytes:
            load_time = (time.monotonic() - start_time) * 1000
            return ContextResult(
                status=ContextLoadStatus.FAILED,
                context=None,
                errors=(f"Context file exceeds {self.max_size_bytes} bytes limit: {file_size}",),
                load_time_ms=load_time,
            )

        # Load and parse YAML
        try:
            with schema_path.open() as f:
                raw_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            load_time = (time.monotonic() - start_time) * 1000
            return ContextResult(
                status=ContextLoadStatus.FAILED,
                context=None,
                errors=(f"YAML parse error: {e}",),
                load_time_ms=load_time,
            )

        # Validate against JSON Schema (REQ-CI-F-006)
        validation_result = self._validate_raw_context(raw_data)
        if not validation_result.is_valid:
            load_time = (time.monotonic() - start_time) * 1000
            error_msgs = tuple(
                f"{e.field}: {e.message}" for e in validation_result.errors
            )
            return ContextResult(
                status=ContextLoadStatus.FAILED,
                context=None,
                errors=error_msgs,
                load_time_ms=load_time,
            )

        # Build context object
        context = Context(
            domain=domain,
            entities=raw_data.get("entity_definitions", {}),
            extraction_rules=tuple(raw_data.get("extraction_rules", [])),
            prompt_guidance=raw_data.get("prompt_guidance", ""),
            metadata=raw_data.get("metadata", {}),
        )

        # Cache for future requests
        self._cache[domain] = context

        load_time = (time.monotonic() - start_time) * 1000

        # Check load time constraint (REQ-CI-P-001)
        if load_time > self.max_load_time_ms:
            # IMPLEMENTATION NOTE: Log warning via logging module
            # Return success but include load_time in result for monitoring
            # Performance degradation tracked via metrics, not failure
            pass

        return ContextResult(
            status=ContextLoadStatus.SUCCESS,
            context=context,
            errors=(),
            load_time_ms=load_time,
        )

    def _load_json_schema(self) -> dict:
        """Load JSON Schema for validation."""
        if not self.schema_path.exists():
            return {}
        with self.schema_path.open() as f:
            return json.load(f)

    def _validate_raw_context(self, data: dict) -> ValidationResult:
        """Validate raw YAML data against JSON Schema.

        Implements: REQ-CI-F-006
        """
        # DEFERRED: Full jsonschema library validation in implementation phase
        # Current: Manual field validation for core requirements
        errors = []

        # Required fields check
        required_fields = ["schema_version", "domain", "entity_definitions"]
        for field in required_fields:
            if field not in data:
                errors.append(ValidationError(
                    field=field,
                    message=f"Required field '{field}' is missing",
                ))

        # Version check
        schema_version = data.get("schema_version", "")
        if not schema_version.startswith("1."):
            errors.append(ValidationError(
                field="schema_version",
                message=f"Unsupported schema version: {schema_version}",
            ))

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            schema_version=schema_version or "unknown",
        )
```

#### 3.2 Loading Lifecycle State Machine

**Implements:** REQ-CI-F-005

```
CONTEXT LOADING STATE MACHINE
=============================

           ┌─────────────────────────────────────────────────────────────┐
           │                         STATES                               │
           └─────────────────────────────────────────────────────────────┘

    ┌──────────┐     start      ┌──────────┐    success    ┌──────────┐
    │          │────────────────►          │──────────────►│          │
    │   IDLE   │                │  LOADING │               │  STATIC  │
    │          │◄───────────────│  STATIC  │◄──────────────│  LOADED  │
    └──────────┘    reset       └──────────┘    retry      └────┬─────┘
                                     │                          │
                                     │ failure                  │ continue
                                     ▼                          ▼
                               ┌──────────┐             ┌──────────────┐
                               │  FAILED  │             │   LOADING    │
                               │          │             │   DYNAMIC    │
                               └──────────┘             └──────┬───────┘
                                                               │
                                    ┌──────────────────────────┤
                                    │                          │
                                    │ failure                  │ success
                                    ▼                          ▼
                             ┌──────────────┐          ┌──────────────┐
                             │  FALLBACK    │          │   DYNAMIC    │
                             │  (static     │          │   LOADED     │
                             │   only)      │          │              │
                             └──────┬───────┘          └──────┬───────┘
                                    │                          │
                                    │                          │
                                    └────────────┬─────────────┘
                                                 │
                                                 ▼ resolve
                                          ┌──────────────┐
                                          │  RESOLVING   │
                                          │  TEMPLATES   │
                                          └──────┬───────┘
                                                 │
                                                 │ complete
                                                 ▼
                                          ┌──────────────┐
                                          │   COMPLETE   │
                                          │   (merged    │
                                          │    context)  │
                                          └──────────────┘

           ┌─────────────────────────────────────────────────────────────┐
           │                     TRANSITIONS                              │
           └─────────────────────────────────────────────────────────────┘

    | From State      | Event         | To State        | Action                  |
    |-----------------|---------------|-----------------|-------------------------|
    | IDLE            | start         | LOADING_STATIC  | Begin static load       |
    | LOADING_STATIC  | success       | STATIC_LOADED   | Cache static context    |
    | LOADING_STATIC  | failure       | FAILED          | Log error, no retry     |
    | STATIC_LOADED   | continue      | LOADING_DYNAMIC | Begin dynamic load      |
    | LOADING_DYNAMIC | success       | DYNAMIC_LOADED  | Merge contexts          |
    | LOADING_DYNAMIC | failure       | FALLBACK        | Use static only         |
    | DYNAMIC_LOADED  | resolve       | RESOLVING       | Template substitution   |
    | FALLBACK        | resolve       | RESOLVING       | Template with static    |
    | RESOLVING       | complete      | COMPLETE        | Return merged context   |
    | COMPLETE        | reset         | IDLE            | Clear state             |
    | FAILED          | reset         | IDLE            | Clear error state       |
```

```python
"""Context loading lifecycle state machine.

Implements: REQ-CI-F-005
"""

from enum import Enum, auto
from typing import Optional, Callable
from dataclasses import dataclass, field


class LoadingState(Enum):
    """States in the context loading lifecycle."""
    IDLE = auto()
    LOADING_STATIC = auto()
    STATIC_LOADED = auto()
    LOADING_DYNAMIC = auto()
    DYNAMIC_LOADED = auto()
    FALLBACK = auto()
    RESOLVING = auto()
    COMPLETE = auto()
    FAILED = auto()


class LoadingEvent(Enum):
    """Events that trigger state transitions."""
    START = auto()
    SUCCESS = auto()
    FAILURE = auto()
    CONTINUE = auto()
    RESOLVE = auto()
    COMPLETE = auto()
    RESET = auto()


@dataclass
class ContextLoadingLifecycle:
    """State machine for context loading.

    Ensures correct ordering: static → dynamic → template (REQ-CI-F-005).
    """

    state: LoadingState = LoadingState.IDLE
    static_context: Optional[Context] = None
    dynamic_context: Optional[Context] = None
    merged_context: Optional[Context] = None
    error_message: Optional[str] = None

    # Transition table
    _transitions: dict = field(default_factory=lambda: {
        (LoadingState.IDLE, LoadingEvent.START): LoadingState.LOADING_STATIC,
        (LoadingState.LOADING_STATIC, LoadingEvent.SUCCESS): LoadingState.STATIC_LOADED,
        (LoadingState.LOADING_STATIC, LoadingEvent.FAILURE): LoadingState.FAILED,
        (LoadingState.STATIC_LOADED, LoadingEvent.CONTINUE): LoadingState.LOADING_DYNAMIC,
        (LoadingState.LOADING_DYNAMIC, LoadingEvent.SUCCESS): LoadingState.DYNAMIC_LOADED,
        (LoadingState.LOADING_DYNAMIC, LoadingEvent.FAILURE): LoadingState.FALLBACK,
        (LoadingState.DYNAMIC_LOADED, LoadingEvent.RESOLVE): LoadingState.RESOLVING,
        (LoadingState.FALLBACK, LoadingEvent.RESOLVE): LoadingState.RESOLVING,
        (LoadingState.RESOLVING, LoadingEvent.COMPLETE): LoadingState.COMPLETE,
        (LoadingState.COMPLETE, LoadingEvent.RESET): LoadingState.IDLE,
        (LoadingState.FAILED, LoadingEvent.RESET): LoadingState.IDLE,
    })

    def transition(self, event: LoadingEvent) -> bool:
        """Attempt a state transition.

        Returns True if transition was valid, False otherwise.
        """
        key = (self.state, event)
        if key not in self._transitions:
            return False

        self.state = self._transitions[key]
        return True

    def can_transition(self, event: LoadingEvent) -> bool:
        """Check if transition is valid without executing it."""
        return (self.state, event) in self._transitions

    @property
    def is_complete(self) -> bool:
        """Check if loading is complete."""
        return self.state == LoadingState.COMPLETE

    @property
    def is_failed(self) -> bool:
        """Check if loading failed."""
        return self.state == LoadingState.FAILED

    @property
    def using_fallback(self) -> bool:
        """Check if using fallback (static only)."""
        return self.state in (LoadingState.FALLBACK, LoadingState.COMPLETE) and \
               self.dynamic_context is None
```

#### 3.3 JSON Schema Validation

**Implements:** REQ-CI-F-006

**Location:** `skills/transcript/schemas/context-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "context-schema.json",
  "title": "Domain Context Schema",
  "description": "JSON Schema for validating domain context YAML files",
  "type": "object",
  "required": ["schema_version", "domain", "entity_definitions"],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^1\\.[0-9]+\\.[0-9]+$",
      "description": "Semantic version of schema format"
    },
    "domain": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50,
      "pattern": "^[a-z][a-z0-9-]*$",
      "description": "Domain identifier"
    },
    "display_name": {
      "type": "string",
      "maxLength": 100,
      "description": "Human-readable domain name"
    },
    "entity_definitions": {
      "type": "object",
      "additionalProperties": {
        "$ref": "#/$defs/entity_definition"
      },
      "minProperties": 1,
      "description": "Entity types for extraction"
    },
    "extraction_rules": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/extraction_rule"
      },
      "description": "Ordered extraction rules"
    },
    "prompt_guidance": {
      "type": "string",
      "maxLength": 5000,
      "description": "Guidance text for LLM"
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata"
    }
  },
  "$defs": {
    "entity_definition": {
      "type": "object",
      "required": ["description", "attributes"],
      "properties": {
        "description": {
          "type": "string",
          "maxLength": 500
        },
        "attributes": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/attribute"
          },
          "minItems": 1
        },
        "extraction_patterns": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/extraction_pattern"
          }
        }
      }
    },
    "attribute": {
      "type": "object",
      "required": ["name", "type"],
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_]*$"
        },
        "type": {
          "type": "string",
          "enum": ["string", "number", "boolean", "date", "enum", "reference", "array"]
        },
        "required": {
          "type": "boolean",
          "default": false
        },
        "values": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Enum values (when type=enum)"
        },
        "ref": {
          "type": "string",
          "description": "Entity reference (when type=reference)"
        },
        "format": {
          "type": "string",
          "description": "Format specifier (e.g., ISO8601 for dates)"
        }
      }
    },
    "extraction_pattern": {
      "type": "object",
      "required": ["pattern"],
      "properties": {
        "pattern": {
          "type": "string",
          "description": "Extraction pattern with {{variable}} placeholders"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.8
        }
      }
    },
    "extraction_rule": {
      "type": "object",
      "required": ["id", "description", "entity_type"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9-]*$"
        },
        "description": {
          "type": "string",
          "maxLength": 500
        },
        "entity_type": {
          "type": "string"
        },
        "priority": {
          "type": "integer",
          "minimum": 1
        },
        "confidence_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

#### 3.4 Template Variable Resolution

**Implements:** REQ-CI-F-008

```python
"""Template resolver for {{$variable}} syntax.

Implements: REQ-CI-F-008
Compatible with Semantic Kernel variable syntax.
"""

import re
from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class TemplateResolver:
    """Resolves {{$variable}} placeholders in templates.

    Supports:
    - Simple variables: {{$domain}}
    - Nested access: {{$context.entities.party}}
    - Default values: {{$missing|default}}
    """

    # Pattern matches {{$variable}} and {{$var.nested.path}}
    VARIABLE_PATTERN = re.compile(
        r'\{\{\$([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)(?:\|([^}]*))?\}\}'
    )

    resolution_timeout_ms: float = 50.0

    def resolve(self, template: str, context: Dict[str, Any]) -> str:
        """Resolve all variables in template.

        Args:
            template: Template string with {{$variable}} placeholders
            context: Dictionary with variable values

        Returns:
            Resolved template string
        """
        def replace_match(match: re.Match) -> str:
            var_path = match.group(1)
            default_value = match.group(2) if match.group(2) else ""

            # Navigate nested path
            value = self._resolve_path(var_path, context)

            if value is None:
                return default_value

            # Convert to string if needed
            if isinstance(value, (list, dict)):
                return self._format_complex(value)
            return str(value)

        return self.VARIABLE_PATTERN.sub(replace_match, template)

    def _resolve_path(self, path: str, context: Dict[str, Any]) -> Any:
        """Resolve a dotted path in context."""
        parts = path.split('.')
        current = context

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _format_complex(self, value: Any) -> str:
        """Format complex values for template insertion."""
        if isinstance(value, list):
            return '\n'.join(f"- {item}" for item in value)
        if isinstance(value, dict):
            return '\n'.join(f"{k}: {v}" for k, v in value.items())
        return str(value)

    def get_variables(self, template: str) -> set[str]:
        """Extract all variable names from template."""
        matches = self.VARIABLE_PATTERN.findall(template)
        return {match[0] for match in matches}

    def validate_template(self, template: str, context: Dict[str, Any]) -> list[str]:
        """Check for unresolved variables."""
        variables = self.get_variables(template)
        missing = []

        for var in variables:
            if self._resolve_path(var, context) is None:
                missing.append(var)

        return missing
```

#### 3.5 Context Merging

**Implements:** REQ-CI-F-009

```python
"""Context merging strategy.

Implements: REQ-CI-F-009
"""

from typing import Optional, Dict, Any
from ..domain.context import Context


class ContextMerger:
    """Merge static and dynamic contexts.

    Dynamic values override static for same keys.
    Lists are concatenated, not replaced.
    """

    def merge(
        self,
        static: Context,
        dynamic: Optional[Context]
    ) -> Context:
        """Merge static and dynamic contexts.

        Priority: dynamic > static (dynamic overrides)

        Args:
            static: Base static context (always present)
            dynamic: Optional dynamic context overlay

        Returns:
            New merged Context object
        """
        if dynamic is None:
            return static

        # Merge entities (dynamic overrides)
        merged_entities = {**static.entities}
        for key, value in dynamic.entities.items():
            if key in merged_entities and isinstance(merged_entities[key], dict):
                merged_entities[key] = {**merged_entities[key], **value}
            else:
                merged_entities[key] = value

        # Merge extraction rules (concatenate, deduplicate by id)
        static_rules = {r.get('id'): r for r in static.extraction_rules}
        for rule in dynamic.extraction_rules:
            rule_id = rule.get('id')
            if rule_id:
                static_rules[rule_id] = rule
            else:
                static_rules[f"dynamic_{len(static_rules)}"] = rule
        merged_rules = tuple(static_rules.values())

        # Merge prompt guidance (concatenate with separator)
        merged_guidance = static.prompt_guidance
        if dynamic.prompt_guidance:
            merged_guidance = f"{static.prompt_guidance}\n\n---\n\n{dynamic.prompt_guidance}"

        # Merge metadata
        merged_metadata = {**static.metadata, **dynamic.metadata}
        merged_metadata['merge_source'] = 'static+dynamic'

        return Context(
            domain=static.domain,  # Keep static domain
            entities=merged_entities,
            extraction_rules=merged_rules,
            prompt_guidance=merged_guidance,
            metadata=merged_metadata,
        )
```

#### 3.6 Error Propagation

**Implements:** REQ-CI-F-010

```python
"""Error propagation strategy using Result types.

Implements: REQ-CI-F-010
Adapters NEVER return empty context on failure - always explicit errors.
"""

from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar('T')


@dataclass(frozen=True)
class Ok(Generic[T]):
    """Success result."""
    value: T


@dataclass(frozen=True)
class Err:
    """Error result with message."""
    message: str
    error_type: str = "unknown"
    details: dict = None

    def __post_init__(self):
        if self.details is None:
            object.__setattr__(self, 'details', {})


# Result type alias
Result = Union[Ok[T], Err]


def is_ok(result: Result) -> bool:
    """Check if result is successful."""
    return isinstance(result, Ok)


def is_err(result: Result) -> bool:
    """Check if result is an error."""
    return isinstance(result, Err)


def unwrap(result: Result[T]) -> T:
    """Get value from Ok result, raise if Err."""
    if isinstance(result, Ok):
        return result.value
    raise ValueError(f"Cannot unwrap Err: {result.message}")


def unwrap_or(result: Result[T], default: T) -> T:
    """Get value from Ok result, return default if Err."""
    if isinstance(result, Ok):
        return result.value
    return default
```

#### 3.7 Graceful Degradation and Circuit Breaker

**Implements:** REQ-CI-F-011, REQ-CI-P-003

```python
"""Graceful degradation and circuit breaker implementation.

Implements: REQ-CI-F-011 (fallback to static)
Implements: REQ-CI-P-003 (circuit breaker pattern)
"""

import time
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Callable, TypeVar

T = TypeVar('T')


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = auto()    # Normal operation, requests pass through
    OPEN = auto()      # Tripped, requests fail fast
    HALF_OPEN = auto() # Testing if service recovered


@dataclass
class CircuitBreaker:
    """Circuit breaker for external calls.

    Implements: REQ-CI-P-003
    Threshold: 5 consecutive failures = OPEN
    """

    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[float] = None

    def call(
        self,
        operation: Callable[[], T],
        fallback: Callable[[], T]
    ) -> T:
        """Execute operation with circuit breaker protection.

        Args:
            operation: Primary operation to execute
            fallback: Fallback operation if circuit is open

        Returns:
            Result from operation or fallback
        """
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
            else:
                return fallback()

        try:
            result = operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            return fallback()

    def _should_attempt_recovery(self) -> bool:
        """Check if enough time has passed for recovery attempt."""
        if self.last_failure_time is None:
            return True
        elapsed = time.monotonic() - self.last_failure_time
        return elapsed >= self.recovery_timeout_seconds

    def _on_success(self) -> None:
        """Handle successful operation."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.monotonic()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    @property
    def is_open(self) -> bool:
        """Check if circuit is open (failing fast)."""
        return self.state == CircuitState.OPEN


@dataclass
class GracefulDegradation:
    """Graceful degradation strategy.

    Implements: REQ-CI-F-011
    Falls back to static context when dynamic sources fail.
    """

    circuit_breaker: CircuitBreaker = field(default_factory=CircuitBreaker)

    def load_with_fallback(
        self,
        dynamic_loader: Callable[[], ContextResult],
        static_context: Context
    ) -> ContextResult:
        """Load dynamic context with fallback to static.

        Args:
            dynamic_loader: Function to load dynamic context
            static_context: Pre-loaded static context as fallback

        Returns:
            ContextResult from dynamic or fallback
        """
        def operation() -> ContextResult:
            result = dynamic_loader()
            if result.status == ContextLoadStatus.FAILED:
                raise RuntimeError(result.errors[0] if result.errors else "Unknown error")
            return result

        def fallback() -> ContextResult:
            return ContextResult(
                status=ContextLoadStatus.FALLBACK,
                context=static_context,
                errors=("Using static fallback due to dynamic context failure",),
                load_time_ms=0.0,
            )

        return self.circuit_breaker.call(operation, fallback)
```

---

### 4. Interfaces

#### 4.1 External Interfaces

##### 4.1.1 CLI Interface

```
COMMAND LINE INTERFACE
======================

# Domain selection (REQ-CI-F-004)
transcript analyze <file> --domain <domain>

Examples:
  transcript analyze meeting.vtt --domain legal
  transcript analyze standup.srt --domain engineering
  transcript analyze call.vtt --domain sales

# Available options
--domain <name>     Domain context to use (default: "general")
--no-context        Disable context injection
--context-debug     Print loaded context (debug mode)
--validate-only     Validate context without processing
```

##### 4.1.2 SKILL.md Integration

```yaml
# skills/transcript/SKILL.md - Context injection interface

# Skill invocation triggers context loading
# Context is automatically available in agents via $CONTEXT variable

skill_invocation: |
  When this skill is invoked:
  1. Load context_injection.default_domain
  2. If --domain specified, override with specified domain
  3. Validate context against schema
  4. Make context available as $CONTEXT in all agents
```

#### 4.2 Internal Interfaces

##### 4.2.1 Port-Adapter Mapping

| Port | Adapter | Implementation |
|------|---------|----------------|
| `IContextProvider` | `FilesystemContextAdapter` | YAML file loading |
| `IContextProvider` | `MCPContextAdapter` (stub) | MCP protocol (future) |
| `ISchemaValidator` | `JsonSchemaValidator` | JSON Schema validation |
| `ITemplateResolver` | `TemplateResolver` | `{{$variable}}` syntax |

##### 4.2.2 Dependency Injection

```python
# bootstrap.py - Context injection composition root

from skills.transcript.context.ports import IContextProvider
from skills.transcript.context.adapters import FilesystemContextAdapter
from skills.transcript.context.adapters import MCPContextAdapter
from skills.transcript.context.lifecycle import ContextLoadingLifecycle


def create_context_provider(config: SkillConfig) -> IContextProvider:
    """Create context provider with configured adapters.

    Composition Root pattern - all dependencies wired here.
    """
    # Primary adapter: Filesystem
    filesystem_adapter = FilesystemContextAdapter(
        contexts_dir=config.contexts_dir,
        schema_path=config.schema_path,
        max_load_time_ms=config.max_load_time_ms,
        max_size_bytes=config.max_size_bytes,
    )

    # Optional: MCP adapter with circuit breaker
    mcp_adapter = None
    if config.mcp_enabled:
        mcp_adapter = MCPContextAdapter(
            server_url=config.mcp_server_url,
            circuit_breaker=CircuitBreaker(
                failure_threshold=5,
                recovery_timeout_seconds=30.0,
            ),
        )

    # Compose with graceful degradation
    return CompositeContextProvider(
        static_adapter=filesystem_adapter,
        dynamic_adapter=mcp_adapter,
        degradation=GracefulDegradation(),
        lifecycle=ContextLoadingLifecycle(),
    )
```

#### 4.3 API Contracts

##### 4.3.1 Context Loading Contract

```python
# Contract: Context loading must complete within budget
@contract
def load_static_context_contract():
    """Contract for static context loading."""

    # Preconditions
    requires(domain is not None)
    requires(len(domain) > 0)

    # Postconditions
    ensures(result.status in ContextLoadStatus)
    ensures(result.load_time_ms >= 0)
    ensures(result.load_time_ms <= 500)  # REQ-CI-P-001

    # If success, context must be present
    ensures(implies(
        result.status == ContextLoadStatus.SUCCESS,
        result.context is not None
    ))

    # If failure, errors must be present
    ensures(implies(
        result.status == ContextLoadStatus.FAILED,
        len(result.errors) > 0
    ))
```

##### 4.3.2 Validation Contract

```python
# Contract: Validation must be deterministic
@contract
def validate_context_contract():
    """Contract for context validation."""

    # Preconditions
    requires(context is not None)

    # Postconditions - deterministic
    ensures(
        validate(context) == validate(context)  # Idempotent
    )

    # Schema version always present
    ensures(result.schema_version is not None)
```

##### 4.3.3 Template Resolution Contract

```python
# Contract: Template resolution must be deterministic and bounded
@contract
def resolve_template_contract():
    """Contract for template variable resolution.

    Implements: REQ-CI-F-008, REQ-CI-P-004
    """

    # Preconditions
    requires(template is not None)
    requires(context is not None)
    requires(isinstance(template, str))

    # Postconditions - deterministic
    ensures(
        resolve_template(template, context) == resolve_template(template, context)
    )

    # Performance constraint
    ensures(execution_time_ms <= 50)  # REQ-CI-P-004

    # Output is always a string
    ensures(isinstance(result, str))

    # No unresolved variables with defaults
    ensures(not contains_unresolved_with_default(result))

    # Idempotent: resolving an already-resolved template is no-op
    ensures(
        resolve_template(result, context) == result
    )
```

##### 4.3.4 Context Merging Contract

```python
# Contract: Context merging must be deterministic with clear precedence
@contract
def merge_contexts_contract():
    """Contract for context merging.

    Implements: REQ-CI-F-009
    Precedence: dynamic > static (dynamic overrides)
    """

    # Preconditions
    requires(static is not None)  # Static always required
    requires(static.domain is not None)
    # dynamic may be None (fallback case)

    # Postconditions - domain preserved
    ensures(result.domain == static.domain)

    # Postconditions - deterministic
    ensures(
        merge_contexts(static, dynamic) == merge_contexts(static, dynamic)
    )

    # If dynamic is None, result equals static
    ensures(implies(
        dynamic is None,
        result == static
    ))

    # If dynamic has key, it overrides static
    ensures(implies(
        dynamic is not None and key in dynamic.entities,
        result.entities[key] == dynamic.entities[key]
    ))

    # Extraction rules are concatenated (deduplicated by id)
    ensures(
        len(result.extraction_rules) >= len(static.extraction_rules)
    )

    # Metadata includes merge source
    ensures(implies(
        dynamic is not None,
        result.metadata.get('merge_source') == 'static+dynamic'
    ))
```

##### 4.3.5 Dynamic Context Loading Contract

```python
# Contract: Dynamic context loading with graceful degradation
@contract
def load_dynamic_context_contract():
    """Contract for dynamic context loading.

    Implements: REQ-CI-F-011 (fallback), REQ-CI-P-003 (circuit breaker)
    """

    # Preconditions
    requires(document_id is not None)
    requires(len(document_id) > 0)

    # Postconditions - always returns valid result
    ensures(result is not None)
    ensures(result.status in ContextLoadStatus)
    ensures(result.load_time_ms >= 0)

    # If success, context must be present
    ensures(implies(
        result.status == ContextLoadStatus.SUCCESS,
        result.context is not None
    ))

    # If failure, must return FALLBACK status (not FAILED)
    # per REQ-CI-F-011 graceful degradation
    ensures(implies(
        external_source_unavailable,
        result.status == ContextLoadStatus.FALLBACK
    ))

    # Circuit breaker: after 5 failures, fail fast
    ensures(implies(
        circuit_breaker.failure_count >= 5,
        execution_time_ms < 10  # Fast failure
    ))

    # Errors must be explicit (REQ-CI-F-010)
    ensures(implies(
        result.status != ContextLoadStatus.SUCCESS,
        len(result.errors) > 0
    ))
```

---

### 5. Non-Functional Requirements

#### 5.1 Performance Requirements

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| REQ-CI-P-001 | Static context < 500ms | Caching, YAML pre-parsing |
| REQ-CI-P-002 | Max context 50MB | File size check before load |
| REQ-CI-P-003 | Circuit breaker (5 failures) | CircuitBreaker class |
| REQ-CI-P-004 | Template resolution < 50ms | Regex pre-compilation |

```
PERFORMANCE BUDGET ALLOCATION
=============================

Total Budget: 500ms (REQ-CI-P-001)

┌─────────────────────────────────────────────────────────────────────────────┐
│                        500ms PERFORMANCE BUDGET                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  YAML Parse    Schema Validation    Template Resolution    Overhead         │
│  ───────────   ─────────────────    ──────────────────    ─────────        │
│  │██████████│  │████████████████│  │████████│             │████│           │
│  │   200ms  │  │      150ms     │  │  50ms  │             │100ms           │
│  │   40%    │  │       30%      │  │  10%   │             │ 20%│           │
│  └──────────┘  └────────────────┘  └────────┘             └────┘           │
│                                                                              │
│  Mitigation Strategies:                                                      │
│  ├── YAML Parse: Cache parsed results (hit rate > 90%)                      │
│  ├── Schema: Pre-compile JSON Schema validators                              │
│  ├── Template: Pre-compile regex patterns                                   │
│  └── Overhead: Minimize object allocations                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.2 Deployment Configuration

```yaml
# config/context-injection.yaml - Deployment configuration

context_injection:
  # Performance tuning
  performance:
    max_load_time_ms: 500
    max_context_size_mb: 50
    template_timeout_ms: 50
    cache_ttl_seconds: 300

  # Circuit breaker settings
  circuit_breaker:
    failure_threshold: 5
    recovery_timeout_seconds: 30
    half_open_requests: 3

  # Logging
  logging:
    level: INFO
    include_timing: true
    include_context_hash: true

  # Feature flags
  features:
    dynamic_context_enabled: false  # Phase 1: static only
    mcp_adapter_enabled: false
    template_caching: true
```

#### 5.3 Security Considerations

| Concern | Mitigation |
|---------|------------|
| Schema injection | JSON Schema validation before use |
| Path traversal | Whitelist `contexts/` directory |
| Template injection | Sanitize variable values |
| Size-based DoS | Enforce 50MB limit |
| Information disclosure | No sensitive data in logs |

---

### 6. Implementation Considerations

#### 6.1 Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| `pyyaml` | >= 6.0 | YAML parsing |
| `jsonschema` | >= 4.0 | Schema validation |
| `pathlib` | stdlib | Path handling |
| `dataclasses` | stdlib | Immutable types |

**Note:** All dependencies are either stdlib or pre-installed in Jerry environment.

#### 6.2 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schema evolution breaks backward compatibility | Medium | High | Semantic versioning, migration guide |
| Performance degradation with large contexts | Low | Medium | Size limits, lazy loading |
| Template syntax conflicts with content | Low | Low | Escape sequence support |
| MCP server unavailability | Medium | Medium | Circuit breaker, static fallback |

#### 6.3 Testing Strategy

```
TEST PYRAMID FOR CONTEXT INJECTION
==================================

                    ┌─────────────┐
                    │    E2E      │ 5%
                    │  Full flow  │
                   ┌┴─────────────┴┐
                   │  Integration  │ 15%
                   │   Adapters    │
                  ┌┴───────────────┴┐
                  │      Unit       │ 60%
                  │  Domain Logic   │
                 ┌┴─────────────────┴┐
                 │    Contract       │ 20%
                 │ Interface Tests   │
                 └───────────────────┘

SPECIFIC TESTS:

Unit Tests:
├── test_context_loading_success
├── test_context_loading_file_not_found
├── test_context_validation_valid_schema
├── test_context_validation_invalid_schema
├── test_template_resolution_simple_variable
├── test_template_resolution_nested_path
├── test_context_merge_override_behavior
├── test_lifecycle_state_transitions
├── test_circuit_breaker_opens_after_threshold
└── test_circuit_breaker_half_open_recovery

Integration Tests:
├── test_filesystem_adapter_loads_yaml
├── test_skill_md_context_extraction
├── test_full_loading_lifecycle
├── test_fallback_to_static_on_dynamic_failure
└── test_cli_domain_flag_integration

Contract Tests:
├── test_load_time_under_500ms
├── test_context_size_under_50mb
├── test_template_resolution_under_50ms
└── test_adapter_error_propagation

E2E Tests:
├── test_legal_domain_transcript_analysis
└── test_graceful_degradation_user_experience
```

#### 6.4 Interface Verification Matrix

**Implements:** AC-013 (Interface verification coverage)

This matrix maps each `IContextProvider` operation to specific verification activities, ensuring complete test coverage across all interface methods.

##### 6.4.1 IContextProvider Operations Verification

| Operation | Unit Test | Integration Test | Contract Test | V-Method | REQ Coverage |
|-----------|-----------|------------------|---------------|----------|--------------|
| `load_static_context()` | `test_load_yaml_success` | `test_filesystem_adapter_loads` | `test_load_time_under_500ms` | T | REQ-CI-F-001 |
| | `test_load_file_not_found` | `test_skill_md_extraction` | `test_context_size_under_50mb` | T | REQ-CI-P-001 |
| | `test_load_invalid_yaml` | | | T | REQ-CI-P-002 |
| `load_dynamic_context()` | `test_load_dynamic_success` | `test_mcp_adapter_connection` | `test_fallback_on_failure` | T | REQ-CI-F-011 |
| | `test_load_dynamic_failure` | `test_circuit_breaker_integration` | `test_circuit_breaker_threshold` | T | REQ-CI-P-003 |
| | `test_load_with_circuit_open` | | | T | REQ-CI-F-010 |
| `resolve_template()` | `test_resolve_simple_var` | `test_template_with_context` | `test_resolution_under_50ms` | T | REQ-CI-F-008 |
| | `test_resolve_nested_path` | | `test_template_idempotent` | T | REQ-CI-P-004 |
| | `test_resolve_with_default` | | | T | |
| | `test_resolve_missing_var` | | | T | |
| `validate_context()` | `test_validate_valid_schema` | `test_schema_file_loading` | `test_validation_deterministic` | T | REQ-CI-F-006 |
| | `test_validate_missing_fields` | | | T | |
| | `test_validate_version_check` | | | T | |
| `merge_contexts()` | `test_merge_static_only` | `test_full_merge_lifecycle` | `test_merge_deterministic` | T | REQ-CI-F-009 |
| | `test_merge_with_override` | | `test_merge_precedence` | T | |
| | `test_merge_rule_dedup` | | | T | |

##### 6.4.2 Verification Coverage Summary

```
INTERFACE VERIFICATION COVERAGE
===============================

                    Unit       Integration    Contract     Total
                    Tests      Tests          Tests        Coverage
                    ─────      ─────────      ────────     ────────
load_static_context   3           2              2            7
load_dynamic_context  3           2              2            7
resolve_template      4           1              2            7
validate_context      3           1              1            5
merge_contexts        3           1              2            6
                    ─────      ─────────      ────────     ────────
TOTAL:               16           7              9           32 tests

Coverage per V-Method:
├── Test (T):       32 tests  ████████████████████████████████  100%
├── Demo (D):        0 tests                                      0%
├── Inspect (I):     0 tests                                      0%
└── Analysis (A):    0 tests                                      0%

Note: All IContextProvider operations verified via Test (T) method
      per REQ-CI-I-002 requirements.
```

##### 6.4.3 Test-to-Requirement Traceability

| Test Category | Requirements Verified | Test Count |
|---------------|----------------------|------------|
| Static Loading | REQ-CI-F-001, REQ-CI-P-001, REQ-CI-P-002 | 7 |
| Dynamic Loading | REQ-CI-F-010, REQ-CI-F-011, REQ-CI-P-003 | 7 |
| Template Resolution | REQ-CI-F-008, REQ-CI-P-004 | 7 |
| Validation | REQ-CI-F-006 | 5 |
| Merging | REQ-CI-F-009 | 6 |
| **TOTAL** | **11 requirements** | **32 tests** |

---

## L2: Architecture Implications (Principal Architect)

### 1. Strategic Trade-offs

#### 1.1 Trade-off Analysis

| Trade-off | Option A | Option B | Decision | Rationale |
|-----------|----------|----------|----------|-----------|
| Validation timing | Load-time (fail fast) | Use-time (lazy) | **Load-time** | Ishikawa P1-1 - catch errors early |
| Error handling | Exceptions | Result type | **Result type** | REQ-CI-F-010 - explicit errors |
| Context storage | In-memory only | File-based persistence | **File-based** | Jerry P-002 compliance |
| Schema format | JSON Schema + YAML | Pydantic models | **JSON Schema** | MA-001 - model agnostic |
| Template syntax | Jinja2 | Semantic Kernel `{{$var}}` | **Semantic Kernel** | Industry compatibility |

#### 1.2 One-Way Door Decisions

| Decision | Type | Reversibility | Mitigation |
|----------|------|---------------|------------|
| `IContextProvider` interface | One-way door | Low | Extensive design review, version interface |
| YAML schema format | Two-way door | High | Migration tooling planned |
| `{{$variable}}` template syntax | One-way door | Medium | Well-documented, industry standard |
| Circuit breaker thresholds | Two-way door | High | Configurable values |

### 2. Future Evolution Path

```
CONTEXT INJECTION EVOLUTION ROADMAP
===================================

PHASE 1 (Current)           PHASE 2 (Q2 2026)         PHASE 3 (Q4 2026)
─────────────────           ─────────────────         ─────────────────
Hybrid without MCP          MCP-aware hybrid          Full MCP integration

┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ • YAML schemas      │    │ • MCP Resources     │    │ • Native MCP        │
│ • Filesystem loading│───►│   (context files)   │───►│   server            │
│ • Template resolver │    │ • MCP Prompts       │    │ • Discoverable      │
│ • Static fallback   │    │   (templates)       │    │   context           │
│                     │    │ • MCP Tools         │    │ • Cross-agent       │
│                     │    │   (dynamic fetch)   │    │   sharing           │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘

BACKWARD COMPATIBILITY:
├── Phase 1 → Phase 2: YAML schemas remain valid, adapters wrap to MCP
├── Phase 2 → Phase 3: MCP resources become native, filesystem adapter deprecated
└── All phases: IContextProvider port interface remains stable
```

### 3. NASA SE Compliance

| NASA SE Process | Application | TDD Section |
|-----------------|-------------|-------------|
| Process 3: Logical Decomposition | Hexagonal architecture, component separation | 2.2 |
| Process 4: Design Solution | Detailed adapter implementation | 3.x |
| Process 5: Risk Management | Ishikawa root cause coverage | 3.7 |
| Process 11: Traceability | Requirements to design mapping | 1.4 |

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Context** | Domain-specific knowledge provided to agents |
| **Static Context** | Pre-defined context loaded from YAML files |
| **Dynamic Context** | Runtime context from MCP tools or external sources |
| **Template Resolution** | Substituting `{{$variable}}` placeholders with values |
| **Circuit Breaker** | Pattern to prevent cascading failures from external services |
| **Graceful Degradation** | Continuing operation with reduced functionality when components fail |
| **Port** | Interface defining operations (hexagonal architecture) |
| **Adapter** | Implementation of a port interface |

### Appendix B: References

1. **Phase 1 Analysis:**
   - EN-006 5W2H Analysis: `docs/analysis/en006-5w2h-analysis.md`
   - EN-006 Ishikawa & Pareto: `docs/analysis/en006-ishikawa-pareto-analysis.md`
   - EN-006 Requirements Supplement: `docs/requirements/en006-requirements-supplement.md`

2. **Research Sources:**
   - EN-006 Research Synthesis: `docs/research/en006-research-synthesis.md`
   - EN-006 Trade Space Analysis: `docs/research/en006-trade-space.md`

3. **External References:**
   - [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
   - [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25)
   - [NASA Systems Engineering Handbook](https://www.nasa.gov/connect/ebooks/nasa-systems-engineering-handbook-rev-2/)
   - [Microsoft Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/)

### Appendix C: Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-26 | ps-architect | Initial TDD (Iteration 1) |
| 1.1.0 | 2026-01-26 | ps-architect | Iteration 2 revisions based on ps-critic feedback |

**v1.1.0 Changes (Iteration 2):**
- Added Trade Study Summary (Section 1.5) - AC-012
- Added EN-003 Backward Traceability (Section 1.6) - AC-009
- Added AGENT.md Persona Context Example (Section 3.1.3) - AC-004
- Added API Contracts for `resolve_template()`, `merge_contexts()`, `load_dynamic_context()` (Section 4.3.3-4.3.5) - AC-007
- Added Interface Verification Matrix (Section 6.4) - AC-013
- Resolved TBD comments with explicit deferrals - AC-017

---

*Document ID: TDD-CI-001*
*Task: TASK-034 (Phase 2, Iteration 2)*
*Quality Target: >= 0.90*
*Status: Pending ps-critic review*
