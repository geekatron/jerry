# TASK-003: Session Hook Enhancement Architecture Design

<!--
DOCUMENT-ID: FEAT-005:EN-405:TASK-003
TEMPLATE: Architecture Design
VERSION: 1.0.0
AGENT: ps-architect-405 (Claude Opus 4.6)
DATE: 2026-02-14
PARENT: EN-405 (Session Context Enforcement Injection)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
REQUIREMENTS-COVERED: IR-405-001 through IR-405-007, EH-405-001 through EH-405-004, PR-405-001
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-405 (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-14
> **Primary Reference:** EN-403 TASK-004 (SessionStart Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Enhancement Strategy](#enhancement-strategy) | Why additive content injection, not hook rewrite |
| [Architecture Overview](#architecture-overview) | High-level module layout and data flow |
| [SessionQualityContextGenerator Design](#sessionqualitycontextgenerator-design) | The generator class interface and internal structure |
| [Integration Into session_start_hook.py](#integration-into-session_start_hookpy) | Two modification points in the existing hook |
| [Output Format](#output-format) | XML tags within additionalContext |
| [Error Handling Design](#error-handling-design) | Fail-open behavior for import and generation failures |
| [L1-L2 Coordination Architecture](#l1-l2-coordination-architecture) | How SessionStart sets foundation, UserPromptSubmit reinforces |
| [Stdlib-Only Constraint](#stdlib-only-constraint) | No external dependencies permitted |
| [File Layout](#file-layout) | Where new and modified files live |
| [Testing Architecture](#testing-architecture) | Unit and integration test strategy |
| [Traceability](#traceability) | Requirements coverage |
| [References](#references) | Source documents |

---

## Enhancement Strategy

### Additive Content Injection (Not Replacement)

The session_start_hook.py will NOT be rewritten. Instead, a **quality context generation module** produces additional content that is appended to the hook's existing `additionalContext` output.

**Why additive:**

| Reason | Detail |
|--------|--------|
| Risk minimization | Existing hook is battle-tested; handles project validation, error formatting, pre-commit checks |
| Separation of concerns | Project context (existing) and quality context (new) are independent concerns |
| Incremental deployment | Module can be deployed without modifying the hook's core logic |
| Safe rollback | Removing the module restores original behavior |
| Independent testing | Generator can be unit tested without hook infrastructure |

### What Changes vs. What Does Not

| Aspect | Changed? | Detail |
|--------|----------|--------|
| Project context resolution | NO | Valid/invalid/no-project logic untouched |
| Pre-commit hook warning | NO | Warning logic untouched |
| Error handling for uv/CLI failures | NO | Exception handling untouched |
| `systemMessage` content | NO | User-visible output untouched |
| Hook JSON output structure | NO | Same `systemMessage` + `hookSpecificOutput.additionalContext` |
| `additionalContext` content | YES | Quality context appended after existing content |
| Imports section | YES | Try/except import of SessionQualityContextGenerator added |
| `main()` function | YES | 8 lines added between format_hook_output() and output_json() |

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│            SESSION START FLOW (ENHANCED)                      │
│                                                              │
│  scripts/session_start_hook.py (THIN ADAPTER)                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. Find uv, sync deps                (existing)    │    │
│  │ 2. Run jerry --json projects context  (existing)    │    │
│  │ 3. Parse CLI JSON                     (existing)    │    │
│  │ 4. format_hook_output()               (existing)    │    │
│  │ 5. Check pre-commit hooks             (existing)    │    │
│  │ 6. Generate quality context           (NEW)         │    │
│  │ 7. Append quality context             (NEW)         │    │
│  │ 8. output_json()                      (existing)    │    │
│  └──────────────────┬──────────────────────────────────┘    │
│                     │                                        │
│                     ▼                                        │
│  src/infrastructure/internal/enforcement/                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ session_quality_context.py (ENFORCEMENT LOGIC)      │    │
│  │                                                     │    │
│  │   class SessionQualityContextGenerator:             │    │
│  │     VERSION: str = "1.0"                            │    │
│  │     def generate() -> str                           │    │
│  │       -> _quality_gate_section()                    │    │
│  │       -> _constitutional_section()                  │    │
│  │       -> _strategies_section()                      │    │
│  │       -> _criticality_section()                     │    │
│  │                                                     │    │
│  │   Output: XML-tagged quality context string         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Hexagonal Architecture Compliance:                          │
│  - Generator is in infrastructure/internal/enforcement/      │
│  - Hook script is a thin adapter (interface layer analog)    │
│  - No domain/application layer dependencies                  │
└──────────────────────────────────────────────────────────────┘
```

### Layer Assignment

| Component | Hexagonal Layer | Justification |
|-----------|----------------|---------------|
| `session_start_hook.py` | Interface (thin adapter) | Reads stdin, invokes logic, formats output, handles errors |
| `SessionQualityContextGenerator` | Infrastructure (internal) | Produces enforcement context; no domain entities; no I/O |

**Why Infrastructure, not Domain or Application:**
- The generator produces enforcement text, not business logic
- It has no domain entities, value objects, or aggregate roots
- It does not implement a use case (command/query handler)
- It is a technical utility for the enforcement infrastructure
- This matches EN-403 TASK-004's placement decision (REQ-403-080)

---

## SessionQualityContextGenerator Design

### Class Interface

```python
class SessionQualityContextGenerator:
    """Generates quality framework context for session start.

    The generated content includes:
    - Quality gate threshold and scoring requirements
    - Constitutional principles summary
    - Available adversarial strategies
    - Decision criticality framework

    The generator is stateless and produces identical output
    on every invocation (content is static by design).
    """

    VERSION: str = "1.0"

    def generate(self) -> str:
        """Generate the quality framework context block.

        Returns:
            XML-tagged quality context string (~370 tokens).
        """
```

### Internal Methods

| Method | Responsibility | Output Section |
|--------|---------------|----------------|
| `_quality_gate_section()` | Threshold, scoring, bias, cycle, SYN #1 | `<quality-gate>` |
| `_constitutional_section()` | P-003, P-020, P-022, UV-only | `<constitutional-principles>` |
| `_strategies_section()` | All 10 strategies with descriptions | `<adversarial-strategies>` |
| `_criticality_section()` | C1-C4 framework + AUTO-ESCALATE | `<decision-criticality>` |

### Design Properties

| Property | Value | Rationale |
|----------|-------|-----------|
| Stateless | Yes | No instance state; identical output every invocation |
| Pure | Yes | No I/O, no file reads, no network, no randomness |
| Deterministic | Yes | Same output every time |
| Stdlib-only | Yes | No external imports (REQ-403-075) |
| Testable | Yes | Typed parameters, typed return (REQ-403-081) |

### Future Enhancement Path

The `generate()` method signature is deliberately simple. If future requirements add dynamic content (e.g., project-specific criticality defaults), the interface can be extended:

```python
# Current (static)
def generate(self) -> str: ...

# Future (dynamic, backward-compatible)
def generate(self, *, project_context: str | None = None) -> str: ...
```

---

## Integration Into session_start_hook.py

### Change 1: Import Block (Near Top of File)

```python
# Add after existing imports (line ~23, after 'from pathlib import Path')
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except ImportError:
    QUALITY_CONTEXT_AVAILABLE = False
```

**Why `sys.path.insert`:** The session_start_hook.py runs from `scripts/` which is not on the Python path. The parent directory (project root) must be added for the `src.` import to resolve.

**Why `QUALITY_CONTEXT_AVAILABLE` flag:** Decouples deployment. If the module has not been deployed, the hook runs unchanged.

### Change 2: Quality Context Generation (In `main()`, After Line 301)

```python
        # Generate quality framework context (NEW - EN-405)
        quality_context = ""
        if QUALITY_CONTEXT_AVAILABLE:
            try:
                generator = SessionQualityContextGenerator()
                quality_context = generator.generate()
            except Exception as e:
                log_error(log_file, f"WARNING: Quality context generation failed: {e}")
                quality_context = ""  # Fail-open: session proceeds without quality context

        # Append quality context to additional context (NEW - EN-405)
        if quality_context:
            additional_context = additional_context + "\n\n" + quality_context

        # Transform to hook format (existing - line 302)
        output_json(system_message, additional_context)
```

### Integration Flow (Step by Step)

```
main() execution:
  1. Find uv, sync deps               (existing, lines 235-262)
  2. Run jerry --json projects context (existing, lines 264-282)
  3. Parse CLI JSON                    (existing, lines 285-290)
  4. Check pre-commit hooks            (existing, lines 294-298)
  5. format_hook_output()              (existing, line 301)
     -> Returns (system_message, additional_context)
  6. IF QUALITY_CONTEXT_AVAILABLE:     (NEW)
     a. Instantiate SessionQualityContextGenerator
     b. Call generator.generate()
     c. Catch any Exception -> log + empty string
  7. IF quality_context non-empty:     (NEW)
     -> Append to additional_context with "\n\n" separator
  8. output_json()                     (existing, line 302)
```

### Line Count Impact

| Change | Lines Added | Lines Modified | Lines Removed |
|--------|------------|----------------|---------------|
| Import block | 7 | 0 | 0 |
| main() quality context block | 10 | 0 | 0 |
| **Total** | **17** | **0** | **0** |

---

## Output Format

### Enhanced additionalContext

```
Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: PROJ-001-oss-release
ProjectPath: /path/to/project
ValidationMessage: Project is properly configured
</project-context>

<quality-framework version="1.0">
  <quality-gate>
    Target: >= 0.92 for all deliverables.
    Scoring: Use S-014 (LLM-as-Judge) with dimension-level rubrics.
    Known bias: S-014 has leniency bias. Score critically -- 0.92 means genuinely excellent.
    Cycle: Creator -> Critic -> Revision (minimum 3 iterations). Do not bypass.
    Pairing: Steelman (S-003) before Devil's Advocate (S-002) -- canonical review protocol.
  </quality-gate>

  <constitutional-principles>
    HARD constraints (cannot be overridden):
    - P-003: No recursive subagents. Max ONE level: orchestrator -> worker.
    - P-020: User authority. User decides. Never override. Ask before destructive ops.
    - P-022: No deception. Never deceive about actions, capabilities, or confidence.
    Python: UV only. Never use python/pip directly. Use 'uv run'.
  </constitutional-principles>

  <adversarial-strategies>
    Available strategies for quality enforcement:
    - S-014 (LLM-as-Judge): Rubric-based scoring. Use for all deliverables.
    - S-007 (Constitutional AI): Principle-by-principle review. Check .claude/rules/.
    - S-010 (Self-Refine): Self-review before presenting outputs. Apply always.
    - S-003 (Steelman): Charitable reconstruction before critique.
    - S-002 (Devil's Advocate): Strongest counterargument to prevailing conclusion.
    - S-013 (Inversion): Ask 'how could this fail?' before proposing.
    - S-004 (Pre-Mortem): 'Imagine it failed -- why?' for planning tasks.
    - S-012 (FMEA): Systematic failure mode enumeration for architecture.
    - S-011 (CoVe): Factual verification for claims and documentation.
    - S-001 (Red Team): Adversary simulation for security-sensitive work.
  </adversarial-strategies>

  <decision-criticality>
    Assess every task's criticality:
    - C1 (Routine): Reversible, < 3 files, no external deps -> Self-Check only
    - C2 (Standard): Reversible within 1 day, 3-10 files -> Standard Critic
    - C3 (Significant): > 1 day to reverse, > 10 files, API changes -> Deep Review
    - C4 (Critical): Irreversible, architecture/governance changes -> Tournament Review
    AUTO-ESCALATE: Any change to docs/governance/, .context/rules/, or .claude/rules/ is C3 or higher.
  </decision-criticality>
</quality-framework>
```

### Hook JSON Output Structure (Unchanged)

```json
{
    "systemMessage": "Jerry Framework: Project PROJ-001-oss-release active",
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "... project context ... \n\n<quality-framework version=\"1.0\">...</quality-framework>"
    }
}
```

The JSON structure and `systemMessage` are unchanged. Quality context is invisible to the user terminal output.

---

## Error Handling Design

### Fail-Open at Two Levels

**Level 1: Import Failure**

```python
try:
    from src.infrastructure.internal.enforcement.session_quality_context import (
        SessionQualityContextGenerator,
    )
    QUALITY_CONTEXT_AVAILABLE = True
except ImportError:
    QUALITY_CONTEXT_AVAILABLE = False
```

**Behavior:** Module not found -> `QUALITY_CONTEXT_AVAILABLE = False` -> quality context generation skipped entirely -> hook outputs existing content only.

**Level 2: Generation Failure**

```python
try:
    generator = SessionQualityContextGenerator()
    quality_context = generator.generate()
except Exception as e:
    log_error(log_file, f"WARNING: Quality context generation failed: {e}")
    quality_context = ""
```

**Behavior:** Any exception during generation -> error logged -> `quality_context = ""` -> quality context not appended -> hook outputs existing content only.

### Failure Cascade Analysis

| Failure | Impact on SessionStart | Impact on L2 (UserPromptSubmit) |
|---------|----------------------|-------------------------------|
| Import failure | No quality context; project context works | L2 operates independently; provides basic reinforcement |
| Generation exception | No quality context; project context works | L2 operates independently; provides basic reinforcement |
| Malformed XML output | Claude may partially parse; project context works | L2 operates independently |
| Empty string output | No quality context appended; project context works | L2 operates independently |

**Key design property:** L2 enforcement does NOT depend on L1 having successfully loaded quality context. The two hooks operate independently, providing defense-in-depth.

---

## L1-L2 Coordination Architecture

### Session Lifecycle

```
Session Start
    │
    ├── [L1] SessionStart fires ONCE
    │   ├── Project context (existing)
    │   └── Quality framework context (NEW, ~370 tokens)
    │       ├── Full strategy catalog
    │       ├── C1-C4 detailed criteria
    │       ├── Scoring methodology
    │       └── Constitutional principles
    │
    ├── [L1] .claude/rules/ loaded by Claude Code
    │   └── Full rule files (~11,000-12,000 tokens)
    │
    └── [Session continues...]
        │
        ├── User Prompt 1
        │   └── [L2] UserPromptSubmit fires (~600 tokens)
        │       ├── Constitutional reminders (ultra-compact)
        │       ├── Quality threshold reminder
        │       └── Self-review reminder
        │
        ├── User Prompt 2
        │   └── [L2] UserPromptSubmit fires (~600 tokens)
        │       └── Same reinforcement content
        │
        └── ... (continues for every prompt)
```

### The Coordination Principle

**SessionStart (L1)** provides the **comprehensive** quality context when the context window is clean and attention is maximal. It can afford to be detailed (~370 tokens) because it fires once.

**UserPromptSubmit (L2)** provides **ultra-compact** reinforcement (~600 tokens) on every prompt to sustain critical rules as the context degrades from context rot after ~20K tokens.

**The two are complementary, not dependent.** Each operates independently. The overlap (quality threshold, constitutional principles, self-review) is intentional redundancy for defense-in-depth.

---

## Stdlib-Only Constraint

Per REQ-403-075, all enforcement logic uses Python stdlib only:

| Module Used | Purpose | stdlib? |
|-------------|---------|---------|
| `__future__.annotations` | Forward reference support | Yes |
| (none else) | Generator is pure string concatenation | N/A |

The SessionQualityContextGenerator has **zero imports** beyond the future annotations. It uses only Python string operations (`f""`, `+`, `.join()`). This is the simplest possible implementation that satisfies the requirement.

---

## File Layout

### New Files

| File | Layer | Purpose | Lines (est.) |
|------|-------|---------|-------------|
| `src/infrastructure/internal/enforcement/__init__.py` | Infrastructure | Package init | 1 |
| `src/infrastructure/internal/enforcement/session_quality_context.py` | Infrastructure | Quality context generator | ~80 |

### Modified Files

| File | Change | Lines Added |
|------|--------|-------------|
| `scripts/session_start_hook.py` | Import block + main() quality context block | ~17 |

### Directory Structure

```
src/
└── infrastructure/
    └── internal/
        └── enforcement/          (NEW directory)
            ├── __init__.py       (NEW)
            └── session_quality_context.py  (NEW)

scripts/
└── session_start_hook.py         (MODIFIED: +17 lines)
```

---

## Testing Architecture

### Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_generate_returns_xml_tagged_content` | `test_session_quality_context.py` | FR-405-010 |
| `test_quality_gate_includes_092_threshold` | `test_session_quality_context.py` | FR-405-001 |
| `test_quality_gate_includes_leniency_bias` | `test_session_quality_context.py` | FR-405-006 |
| `test_quality_gate_includes_creator_critic_revision` | `test_session_quality_context.py` | FR-405-005 |
| `test_quality_gate_includes_syn1_pairing` | `test_session_quality_context.py` | SR-405-005 |
| `test_constitutional_includes_p003_p020_p022` | `test_session_quality_context.py` | FR-405-002 |
| `test_constitutional_includes_uv_only` | `test_session_quality_context.py` | FR-405-002 |
| `test_strategies_lists_all_10_selected` | `test_session_quality_context.py` | FR-405-003, FR-405-020 |
| `test_strategies_ordered_by_role_prominence` | `test_session_quality_context.py` | SR-405-002 |
| `test_criticality_includes_c1_through_c4` | `test_session_quality_context.py` | FR-405-004 |
| `test_criticality_includes_auto_escalation` | `test_session_quality_context.py` | FR-405-007, FR-405-022 |
| `test_output_contains_4_xml_sections` | `test_session_quality_context.py` | FR-405-011 |
| `test_generator_is_stateless` | `test_session_quality_context.py` | Stateless property |
| `test_generator_uses_no_external_imports` | `test_session_quality_context.py` | REQ-403-075 |
| `test_token_estimate_within_budget` | `test_session_quality_context.py` | PR-405-002 |

### Integration Tests

| Test | Validates |
|------|-----------|
| Hook includes quality context in output when module available | IR-405-002 |
| Hook preserves existing project context output | IR-405-001, IR-405-007 |
| Hook fails-open when generator module unavailable | EH-405-004 |
| Hook fails-open when generator raises exception | EH-405-001, EH-405-002 |
| Hook systemMessage is unchanged | IR-405-003 |
| Hook JSON structure is valid and parseable | Output format contract |

### Test File Location

```
tests/
└── unit/
    └── enforcement/
        └── test_session_quality_context.py
```

---

## Traceability

### Requirements Covered

| Requirement | Coverage |
|-------------|----------|
| IR-405-001 | Additive design; existing format_hook_output() unchanged |
| IR-405-002 | Quality context appended to additionalContext |
| IR-405-003 | systemMessage not modified |
| IR-405-004 | Generator in infrastructure/internal/enforcement/ |
| IR-405-005 | try/except import with QUALITY_CONTEXT_AVAILABLE flag |
| IR-405-006 | Generation after format_hook_output(), before output_json() |
| IR-405-007 | Existing behaviors listed as unchanged |
| EH-405-001 | try/except with empty string fallback |
| EH-405-002 | log_error() on generation failure |
| EH-405-003 | L2 independence documented |
| EH-405-004 | ImportError -> QUALITY_CONTEXT_AVAILABLE = False |
| PR-405-001 | Generator is pure string concatenation; overhead << 1ms |

---

## References

| # | Document | Content Used |
|---|----------|--------------|
| 1 | EN-403 TASK-004 (SessionStart Design) | Primary reference: architecture, integration flow, error handling, file layout |
| 2 | EN-403 TASK-001 (Hook Requirements) | REQ-403-050 through REQ-403-096 |
| 3 | Current session_start_hook.py | Existing implementation to enhance |
| 4 | TASK-001 (this enabler's requirements) | IR-405-xxx, EH-405-xxx, PR-405-xxx |
| 5 | TASK-002 (this enabler's preamble design) | XML content specification |

---

*Agent: ps-architect-405 (Claude Opus 4.6)*
*Date: 2026-02-14*
*Parent: EN-405 Session Context Enforcement Injection*
*Quality Target: >= 0.92*
*Lines Changed: +17 in session_start_hook.py, +80 new module*
