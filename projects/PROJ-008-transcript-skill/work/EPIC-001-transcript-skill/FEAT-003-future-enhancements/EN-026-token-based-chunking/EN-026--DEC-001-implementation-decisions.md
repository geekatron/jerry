# EN-026:DEC-001: Token-Based Chunking Implementation Decisions

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-30
PURPOSE: Document implementation decisions for EN-026 token-based chunking
-->

> **Type:** decision
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Created:** 2026-01-30T09:00:00Z
> **Parent:** EN-026
> **Owner:** Claude
> **Related:** BUG-001, EN-021

---

## Frontmatter

```yaml
id: "EN-026:DEC-001"
work_type: DECISION
title: "Token-Based Chunking Implementation Decisions"
status: DOCUMENTED
priority: HIGH
created_by: "Claude"
participants:
  - "Adam Nowak"
  - "Claude"
created_at: "2026-01-30T09:00:00Z"
updated_at: "2026-01-30T09:00:00Z"
decided_at: "2026-01-30T09:00:00Z"
parent_id: "EN-026"
tags: ["architecture", "tdd", "tiktoken", "chunking", "implementation"]
superseded_by: null
supersedes: null
decision_count: 7
```

---

## Summary

This document captures 7 implementation decisions made during the EN-026 planning phase. These decisions establish the architectural approach, test strategy, and backward compatibility model for implementing token-based chunking.

**Decisions Captured:** 7

**Key Outcomes:**
- TokenCounter as separate injectable service (Hexagonal Architecture)
- tiktoken `p50k_base` encoding with 18,000 token target
- Backward compatible API with `target_tokens` taking precedence
- Comprehensive TDD with separate test files per service

---

## Decision Context

### Background

BUG-001 identified that the current segment-based chunking (500 segments/chunk) produces ~49K tokens per chunk, exceeding Claude Code's Read tool limit of 25K tokens. EN-026 was created to implement token-based chunking as a proper fix.

Before implementation could begin, several architectural and implementation decisions needed to be made regarding:
- Token counting approach and library selection
- Service architecture and dependency injection
- Test organization and TDD methodology
- Backward compatibility with existing API

### Constraints

- Must use tiktoken (approved dependency) not Anthropic API
- Must maintain backward compatibility with existing `chunk_size` parameter
- Must follow Hexagonal Architecture patterns
- Must follow Red/Green/Refactor TDD methodology
- Target 18,000 tokens per chunk (25% safety margin below 25K limit)

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Adam Nowak | Product Owner | API stability, quality |
| Claude | Implementer | Architecture clarity, testability |
| Future Maintainers | Developers | Code maintainability |

---

## Decisions

### D-001: Task File Creation

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Should individual TASK-260.md through TASK-267.md files be created in the EN-026 folder following the TASK template, or is the task list in the enabler sufficient?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Create individual TASK files | Full traceability, detailed AC per task | More files to maintain |
| **B** | Task list in EN-026 only | Simpler, less overhead | Less granular tracking |

#### Decision

**We decided:** Create individual TASK-260.md through TASK-267.md files in the EN-026 folder following the TASK template.

#### Rationale

Individual task files provide:
- Detailed acceptance criteria per task
- Evidence tracking for each deliverable
- Consistent with worktracker conventions
- Better audit trail for mission-critical software

---

### D-002: TDD Scope

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Which tasks require strict TDD (Red/Green/Refactor) vs. which are infrastructure/configuration?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | TDD for all tasks | Maximum rigor | Overhead for config tasks |
| **B** | TDD for code, skip for infra | Pragmatic | Clear scope |

#### Decision

**We decided:** TDD applies to TASK-261, TASK-262, TASK-264, TASK-265, TASK-266. Infrastructure tasks (TASK-260: add dependency, TASK-263: schema update, TASK-267: documentation) don't require TDD.

#### Rationale

- TASK-260 (Add tiktoken) is dependency management, not code
- TASK-263 (Schema update) is covered by contract tests (TASK-266)
- TASK-267 (Documentation) is prose, not code
- Code tasks (261, 262) and test tasks (264, 265, 266) follow TDD

---

### D-003: Test File Organization

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Where should tests for the new TokenCounter service and updated TranscriptChunker be located?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | All tests in existing `test_chunker.py` | Simple | Mixed concerns |
| **B** | Separate file per service | SRP, clear ownership | More files |
| **C** | Separate file for TokenCounter, add to existing for Chunker | Balanced | Best of both |

#### Decision

**We decided:** Option C - Create `test_token_counter.py` for TokenCounter tests; add token-based tests to existing `test_chunker.py` for TranscriptChunker.

#### Rationale

- TokenCounter is a new independent service → deserves its own test file
- TranscriptChunker already has tests → add token-based tests alongside existing ones
- Keeps test files aligned 1:1 with production code (standard practice)
- Makes it clear which tests cover which service

#### Implications

- **Positive:** Clear test ownership, easier to find tests
- **Negative:** Slightly more files to maintain
- **Follow-up required:** Create `tests/unit/transcript/application/services/test_token_counter.py`

---

### D-004: TokenCounter Architecture

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Should token counting be a separate service class or integrated into TranscriptChunker?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Separate TokenCounter service | SRP, testable, injectable | More components |
| **B** | Method within TranscriptChunker | Simpler | Harder to test, tightly coupled |

#### Decision

**We decided:** Option A - Create TokenCounter as a separate service class following Hexagonal Architecture.

#### Rationale

- Follows Single Responsibility Principle
- Better testability (can mock TokenCounter in Chunker tests)
- Follows our established Hexagonal Architecture patterns
- Enables future replacement (e.g., Anthropic API) without changing Chunker

---

### D-005: Dependency Injection

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Should TranscriptChunker receive TokenCounter via constructor injection?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Constructor injection | Testable, explicit deps | Requires passing dependency |
| **B** | Internal instantiation | Simpler API | Hard to test, hidden deps |

#### Decision

**We decided:** Yes, TranscriptChunker will receive TokenCounter via constructor injection.

#### Rationale

- Allows mocking TokenCounter in unit tests
- Follows our Hexagonal Architecture dependency inversion principle
- Makes dependencies explicit and testable
- Consistent with existing patterns in codebase

---

### D-006: Backward Compatibility Strategy

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

Current `TranscriptChunker.__init__(chunk_size: int = 500)` uses segment count. How should we handle the new `target_tokens` parameter?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Replace `chunk_size` with `target_tokens` | Clean break | Breaks existing code |
| **B** | Add `target_tokens`, deprecate `chunk_size` | Transition path | Dual params |
| **C** | Keep both, use `target_tokens` if provided | Full compat | Complexity |

#### Decision

**We decided:** Option C - Keep both parameters; use `target_tokens` if provided, otherwise fall back to `chunk_size` (segment-based).

#### Rationale

- Maintains backward compatibility with existing usage
- Allows gradual migration
- Doesn't break any existing tests or integrations
- Users can explicitly choose segment-based (legacy) or token-based (new)

---

### D-007: Parameter Precedence

**Date:** 2026-01-30
**Participants:** Adam Nowak, Claude

#### Question/Context

When BOTH `chunk_size` and `target_tokens` are provided, which takes precedence?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | `target_tokens` wins | Newer param, recommended | Silent override |
| **B** | Raise error | Explicit | Poor UX |
| **C** | Use more restrictive | Predictable | Complex logic |

#### Decision

**We decided:** Option A - `target_tokens` takes precedence when both are provided. A deprecation warning will be logged when `chunk_size` is used alone.

#### Rationale

- Newer parameter should be the preferred path
- Users explicitly providing `target_tokens` are opting into new behavior
- Deprecation warning guides users toward `target_tokens`
- Avoids breaking existing code that might pass both

#### Implications

- **Positive:** Clear migration path, no breaking changes
- **Negative:** Silent override when both provided
- **Follow-up required:** Add deprecation warning when `chunk_size` used alone

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Create individual TASK files for each task | 2026-01-30 | ACCEPTED |
| D-002 | TDD for code tasks (261,262,264,265,266), not infra | 2026-01-30 | ACCEPTED |
| D-003 | Separate test_token_counter.py, add to test_chunker.py | 2026-01-30 | ACCEPTED |
| D-004 | TokenCounter as separate injectable service | 2026-01-30 | ACCEPTED |
| D-005 | Constructor injection for TokenCounter | 2026-01-30 | ACCEPTED |
| D-006 | Keep both chunk_size and target_tokens (Option C) | 2026-01-30 | ACCEPTED |
| D-007 | target_tokens takes precedence, deprecation warning | 2026-01-30 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-026](./EN-026-token-based-chunking.md) | Parent enabler |
| Bug | [BUG-001](../../FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/BUG-001-chunk-token-overflow.md) | Bug being fixed |
| Original | [EN-021](../../FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/EN-021-chunking-strategy.md) | Original chunking implementation |
| Research | [Token Counting Guide 2025](https://www.propelcode.ai/blog/token-counting-tiktoken-anthropic-gemini-guide-2025) | tiktoken encoding research |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-30 | Claude | Created decision document with 7 decisions from Q&A cycle |

---

## Metadata

```yaml
id: "EN-026:DEC-001"
parent_id: "EN-026"
work_type: DECISION
title: "Token-Based Chunking Implementation Decisions"
status: DOCUMENTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-30T09:00:00Z"
updated_at: "2026-01-30T09:00:00Z"
decided_at: "2026-01-30T09:00:00Z"
participants: ["Adam Nowak", "Claude"]
tags: ["architecture", "tdd", "tiktoken", "chunking", "implementation"]
decision_count: 7
superseded_by: null
supersedes: null
```
