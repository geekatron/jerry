# EN-006:DEC-002: Implementation Approach - Claude Code Skills

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-26 (EN-006 TASK-035 Specification Creation)
PURPOSE: Document implementation approach decision for context injection mechanism
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** CRITICAL
> **Created:** 2026-01-26
> **Parent:** EN-006
> **Owner:** Claude + User
> **Related:** TASK-035, TDD-context-injection.md, FEAT-002

---

## Frontmatter

```yaml
# =============================================================================
# DECISION WORK ITEM
# Source: worktracker.md (Decision File), ADR/MADR best practices
# Purpose: Document implementation approach for EN-006 Context Injection Mechanism
# =============================================================================

# Identity (inherited from WorkItem)
id: "EN-006:DEC-002"                       # Required, immutable - Format: PARENT:DEC-NNN
work_type: DECISION                         # Required, immutable - Discriminator
title: "Implementation Approach - Claude Code Skills"  # Required - Max 500 chars

# State (see State Machine below)
status: ACCEPTED                            # Required - PENDING | DOCUMENTED | SUPERSEDED | ACCEPTED

# Priority
priority: CRITICAL                          # Optional - CRITICAL | HIGH | MEDIUM | LOW

# People
created_by: "Claude"                        # Required, auto-populated
participants:                               # Required - Array of decision participants
  - "Claude"
  - "User"

# Timestamps (auto-managed)
created_at: "2026-01-26T22:00:00Z"          # Required, auto, immutable (ISO 8601)
updated_at: "2026-01-26T22:00:00Z"          # Required, auto (ISO 8601)
decided_at: "2026-01-26T22:00:00Z"          # Optional - When decisions were accepted (ISO 8601)

# Hierarchy
parent_id: "EN-006"                         # Required - Parent work item

# Tags
tags:
  - "implementation"
  - "claude-code-skills"
  - "architecture"
  - "one-way-door"
  - "feat-002"

# =============================================================================
# DECISION-SPECIFIC PROPERTIES
# =============================================================================

# Supersession (for ADR pattern)
superseded_by: null                         # Optional - ADR/DEC ID that replaces this decision
supersedes: null                            # Optional - ADR/DEC ID this decision replaces

# Decision Count
decision_count: 1                           # Auto-calculated from D-NNN entries

# Decision Classification
decision_type: "ONE_WAY_DOOR"               # ONE_WAY_DOOR | TWO_WAY_DOOR
reversibility: "LOW"                        # HIGH | MEDIUM | LOW
impact: "HIGH"                              # HIGH | MEDIUM | LOW
```

---

## Summary

This decision document captures the approved implementation approach for the Context Injection Mechanism. The implementation will use **Claude Code Skills** (SKILL.md, AGENT.md, contexts/*.yaml, hooks) rather than Python CLI modules.

**Key Outcome:** The TDD's Python code (IContextProvider pattern) represents **conceptual design patterns** that map to Claude Code skill constructs, NOT actual Python implementation code.

---

## Decision Context

### Background

During TASK-035 (Specification Creation) preparation, a clarification was needed regarding the implementation approach. The TDD (docs/design/TDD-context-injection.md) contains Python interfaces and code patterns that could be interpreted as:

1. **Actual implementation code** - Build Python modules with CLI integration
2. **Conceptual patterns** - Design patterns that map to Claude Code skill constructs

The user clarified that FEAT-002 (Implementation) will focus exclusively on Claude Code Skills, not Python CLI development.

### Constraints

- Claude Code Skills provide SKILL.md for natural language instructions
- Claude Code Skills provide AGENT.md for agent persona definitions
- Claude Code Skills provide contexts/*.yaml for domain knowledge
- Claude Code Skills provide hooks for lifecycle events
- Jerry CLI (Python) is NOT the focus for FEAT-002
- The TDD's Python code serves as conceptual documentation

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Product Owner | Implementation uses Claude Code Skills capabilities fully |
| Claude | Implementation Agent | Clear mapping from conceptual patterns to skill constructs |
| Future Implementers | FEAT-002 Team | Understand that TDD Python is conceptual, not literal |

---

## Decisions

### D-001: Claude Code Skills as Primary Implementation Technology

**Date:** 2026-01-26
**Participants:** Claude, User

#### Question/Context

Claude asked: "Should the specification describe:

**Option A:** How IContextProvider pattern maps to Claude Code skill constructs (SKILL.md, AGENT.md, contexts/*.yaml, hooks)

**Option B:** Python implementation details for the Jerry CLI framework"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Claude Code Skills | Leverages native Claude Code capabilities; No custom code needed; Plugin distribution ready | Requires understanding of skill construct mapping |
| **B** | Python CLI | Full programmatic control; Familiar paradigm | Duplicates Claude Code capabilities; More maintenance |

#### Decision

**We decided:** Option A - Claude Code Skills as Primary Implementation Technology

User clarification: *"Option A is correct. Remember to capture this decision and update respective artifacts in the repo so we operate accordingly in downstream phases."*

#### Rationale

1. **Native Capabilities**: Claude Code Skills provide built-in support for context injection through SKILL.md instructions, AGENT.md personas, and contexts/*.yaml files
2. **Zero Custom Code**: Skill-based implementation requires no Python modules beyond hook scripts
3. **Plugin Distribution**: Aligns with .claude-plugin/ distribution model
4. **Evidence-Based**: Research synthesis (en006-research-synthesis.md) showed skill-based patterns in Anthropic's own recommendations

#### Implications

- **TDD Interpretation**: The Python code in TDD-context-injection.md (IContextProvider, ContextPayload, etc.) should be understood as conceptual patterns, not literal implementation
- **TASK-035 Scope**: Specification will focus on skill construct mapping, NOT Python APIs
- **FEAT-002 Scope**: Implementation will create/modify SKILL.md, AGENT.md, contexts/*.yaml files
- **Artifact Updates**: All downstream artifacts must reflect this approach

---

## Pattern Mapping

### IContextProvider → Skill Constructs

| TDD Concept | Claude Code Skill Construct | Implementation |
|-------------|----------------------------|----------------|
| `IContextProvider` interface | SKILL.md instructions | Natural language directives |
| `load_static_context()` | `contexts/{domain}.yaml` | YAML files loaded at skill init |
| `resolve_template()` | Template variables `{{$variable}}` | SKILL.md prompt sections |
| `ContextPayload` | Skill invocation arguments | `"skill": "...", "args": "..."` |
| `CircuitBreaker` | Hook with timeout/retry | `hooks/context-loader.py` |
| Agent integration | AGENT.md files | Agent persona definitions |

### Example Mapping

**TDD Conceptual Python:**
```python
class IContextProvider(Protocol):
    def load_static_context(self) -> ContextPayload: ...
    def resolve_template(self, template: str, variables: dict) -> str: ...
```

**Claude Code Skill Implementation:**
```yaml
# contexts/transcript.yaml
domain: transcript
entities:
  - name: Speaker
    attributes: [name, role, timestamp]
  - name: Segment
    attributes: [speaker, content, timestamp]
```

```markdown
<!-- SKILL.md -->
## Context Loading

When processing transcripts, load domain context from `contexts/transcript.yaml`.

Use template variables for customization:
- `{{$domain}}` - Current domain (e.g., "legal", "sales")
- `{{$extraction_rules}}` - Domain-specific extraction patterns
```

---

## Impact on Downstream Phases

### TASK-035 (Specification)

The specification must:
- [ ] Focus on Claude Code skill construct mapping
- [ ] NOT define Python APIs or modules
- [ ] Provide SKILL.md template patterns
- [ ] Provide AGENT.md integration patterns
- [ ] Define contexts/*.yaml schema
- [ ] Specify hook interfaces (minimal Python for lifecycle events)

### FEAT-002 (Implementation)

Implementation deliverables:
- [ ] Updated SKILL.md for transcript skill
- [ ] AGENT.md files (ts-parser, ts-extractor, ts-formatter)
- [ ] contexts/*.yaml files for domain knowledge
- [ ] Hook scripts (if needed) for lifecycle events
- [ ] NO Python CLI modules

### Documentation Updates

All documentation must clarify:
- TDD Python code = conceptual patterns
- Actual implementation = Claude Code Skills
- Jerry CLI remains as-is (no new modules)

---

## Decision Summary

| ID | Decision | Date | Status | Type |
|----|----------|------|--------|------|
| D-001 | Claude Code Skills as Primary Implementation Technology | 2026-01-26 | ACCEPTED | ONE_WAY_DOOR |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-006](./EN-006-context-injection-design.md) | Parent enabler |
| TDD | [TDD-context-injection.md](./docs/design/TDD-context-injection.md) | Contains conceptual Python patterns |
| Prior Decision | [DEC-001](./EN-006--DEC-001-phase1-execution-strategy.md) | Phase 1 execution strategy |
| Research | [en006-research-synthesis.md](./docs/research/en006-research-synthesis.md) | Industry patterns research |
| Claude Code Docs | https://code.claude.com/docs/en/skills | Skills documentation |
| Claude Code Docs | https://code.claude.com/docs/en/plugins | Plugin documentation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude | Created decision document capturing Option A selection |
| 2026-01-26 | User | Approved decision, status → ACCEPTED |

---

## Metadata

```yaml
id: "EN-006:DEC-002"
parent_id: "EN-006"
work_type: DECISION
title: "Implementation Approach - Claude Code Skills"
status: ACCEPTED
priority: CRITICAL
created_by: "Claude"
created_at: "2026-01-26T22:00:00Z"
updated_at: "2026-01-26T22:00:00Z"
decided_at: "2026-01-26T22:00:00Z"
participants: ["Claude", "User"]
tags: ["implementation", "claude-code-skills", "architecture", "one-way-door", "feat-002"]
decision_count: 1
decision_type: "ONE_WAY_DOOR"
superseded_by: null
supersedes: null
```
