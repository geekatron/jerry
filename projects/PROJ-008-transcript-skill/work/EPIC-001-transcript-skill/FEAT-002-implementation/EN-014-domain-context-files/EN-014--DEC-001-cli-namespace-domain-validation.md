# EN-014:DEC-001: CLI Namespace for Domain Validation

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-29 (User Review - Post TASK-168)
PURPOSE: Document CLI namespace decision for domain validation command
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-29T14:30:00Z
> **Parent:** EN-014
> **Owner:** User + Claude
> **Related:** DISC-008, TASK-169

---

## Frontmatter

```yaml
id: "EN-014:DEC-001"
work_type: DECISION
title: "CLI Namespace for Domain Validation"

status: ACCEPTED

priority: HIGH

created_by: "Claude"
participants:
  - "User"
  - "Claude"

created_at: "2026-01-29T14:30:00Z"
updated_at: "2026-01-29T14:30:00Z"
decided_at: "2026-01-29T14:30:00Z"

parent_id: "EN-014"

tags:
  - "cli"
  - "namespace"
  - "domain-validation"
  - "yagni"
  - "transcript-skill"

superseded_by: null
supersedes: null

decision_count: 2
```

---

## State Machine

**Current State:** `ACCEPTED`

```
              +----------+
              |  PENDING |
              +----+-----+
                   |
                   v
            +------------+
            | DOCUMENTED |
            +------+-----+
                   |
                   v
             +----------+
             | ACCEPTED |  <-- Current
             +----------+
             (Terminal)
```

---

## Summary

This decision document captures two related decisions made during the TDD gap analysis discussion:

1. **Validator Nature:** All semantic validators (SV-001 through SV-006) should be runnable Python code, not LLM specifications
2. **CLI Namespace:** Domain validation should use `jerry transcript validate-domain <path>`, scoped to the transcript skill

**Decisions Captured:** 2

**Key Outcomes:**
- Validators will be deterministic Python code
- CLI command will be transcript-skill-scoped (YAGNI)
- Can extract to cross-cutting namespace later if other skills need validation

---

## Decision Context

### Background

During review of TDD-EN014-domain-schema-v2.md (post TASK-168), discussion arose about:
1. How validators should be implemented (code vs LLM instructions)
2. Where domain validation CLI commands should live in the Jerry CLI hierarchy

The Jerry CLI already has established namespaces:
- `jerry session start|end|status|abandon`
- `jerry items list|show|create|start|complete`
- `jerry projects context|list|validate`

### Constraints

- Jerry CLI architecture already established with namespace pattern
- Session start hook already uses Jerry CLI (`scripts/session_start_hook.py`)
- Domain context files currently only used by transcript skill
- YAGNI principle: don't build for hypothetical future needs

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Project Owner | Pragmatic architecture, avoid over-engineering |
| Claude | Implementer | Clear, unambiguous implementation guidance |
| Future Developers | Maintenance | Consistent CLI patterns |

---

## Decisions

### D-001: Validator Implementation Nature

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked: "The TDD specifies semantic validators (SV-001 through SV-006). What is their intended nature?"

| Option | Description |
|--------|-------------|
| **A. Runnable Code** | Python validators that execute against YAML files |
| **B. LLM Specifications** | Rules that Claude/agents follow during extraction |
| **C. Hybrid** | Some as code, some as LLM instructions |

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Runnable Python code | Deterministic, testable, CI-compatible | Requires runtime setup |
| **B** | LLM specifications | No runtime needed | Non-deterministic, can't run in CI |
| **C** | Hybrid | Flexibility | Inconsistent enforcement, testing complexity |

#### Decision

**We decided:** Option A - All semantic validators should be runnable Python code.

#### Rationale

1. **Domain YAML files are static artifacts** - deterministic validation is appropriate
2. **All integration points require code** - skill invocation, CLI, CI pipeline all need deterministic behavior
3. **Testing is possible** - can write unit tests with expected pass/fail assertions
4. **Consistency** - same validation logic everywhere, same results
5. **CI/CD compatibility** - can run validation in GitHub Actions without LLM API calls

The LLM's role is different: ts-extractor CONSUMES validated domain files and APPLIES extraction rules. The agent follows the YAML specification, but the YAML itself must be pre-validated by code.

#### Implications

- **Positive:** Deterministic validation, testable, CI-compatible
- **Negative:** Requires Python runtime specification in TDD
- **Follow-up required:** TDD must specify runtime environment, dependencies, execution method

---

### D-002: CLI Namespace for Domain Validation

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked: "Should domain validation be a new CLI namespace, extend existing namespace, or be transcript-specific?"

| Option | Command | Description |
|--------|---------|-------------|
| **A** | `jerry domain validate <path>` | New CLI namespace |
| **B** | `jerry projects validate-domain <path>` | Extend projects namespace |
| **C** | `jerry transcript validate-domain <path>` | Transcript-specific namespace |

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | New `jerry domain` namespace | Clean separation, cross-cutting | YAGNI if only transcript needs it |
| **B** | Extend `jerry projects` | Leverages existing namespace | Conflates project and domain validation |
| **C** | `jerry transcript` namespace | Scoped to skill, follows pattern | Narrow if other skills need it later |

#### Decision

**We decided:** Option C - `jerry transcript validate-domain <path>`

#### Rationale

**User Quote:**
> "Option A sounds appealing but I don't yet see the use of these as a cross-cutting concern. They live in the transcript skill currently. At the moment it makes sense to go with Option C unless there is better justification. Option A sounds a bit YAGNI. When we get to that point we can then always make a new CLI Namespace for that."

1. **YAGNI Principle** - Domain context files are currently only used by transcript skill
2. **Scoped appropriately** - Validation is transcript-skill-specific at this time
3. **Extractable later** - If other skills need domain validation, can create `jerry domain` namespace then
4. **Follows pattern** - Consistent with skill-scoped commands

#### Implications

- **Positive:** Avoids over-engineering, scoped appropriately, follows YAGNI
- **Negative:** May need refactoring if other skills adopt domain validation
- **Follow-up required:** TDD must specify `jerry transcript validate-domain` as the CLI interface

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | All validators are runnable Python code | 2026-01-29 | ACCEPTED |
| D-002 | CLI namespace: `jerry transcript validate-domain <path>` | 2026-01-29 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-014-domain-context-files.md](./EN-014-domain-context-files.md) | Parent enabler |
| Discovery | [EN-014--DISC-008](./EN-014--DISC-008-comprehensive-tdd-implementation-gap.md) | Gap discovery that prompted decisions |
| TDD | [TDD-EN014-domain-schema-v2.md](./docs/design/TDD-EN014-domain-schema-v2.md) | Document to be revised |
| Jerry CLI | src/interface/cli/ | Existing CLI architecture |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Claude | Created decision document from user discussion |

---

## Metadata

```yaml
id: "EN-014:DEC-001"
parent_id: "EN-014"
work_type: DECISION
title: "CLI Namespace for Domain Validation"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-29T14:30:00Z"
updated_at: "2026-01-29T14:30:00Z"
decided_at: "2026-01-29T14:30:00Z"
participants: ["User", "Claude"]
tags: ["cli", "namespace", "domain-validation", "yagni", "transcript-skill"]
decision_count: 2
superseded_by: null
supersedes: null
```
