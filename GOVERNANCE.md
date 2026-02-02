# GOVERNANCE.md - Protocols for Planning & Handoffs

> This document defines the governance protocols that ensure quality,
> consistency, and accountability in Jerry framework development.

---

## Core Principles

1. **Evidence-Based Decisions** - All decisions must cite sources
2. **Explicit Planning** - Complex tasks require PLAN files
3. **Quality Gates** - Handoffs enforce review checkpoints
4. **Knowledge Capture** - Learnings persist in docs/
5. **Traceability** - All work links to Work Tracker items

---

## Planning Protocol

### When to Create a PLAN File

Create a PLAN file (`docs/plans/PLAN_{slug}.md`) when:
- Task involves 3+ files or components
- Multiple valid approaches exist
- Architectural decisions required
- Estimated effort > 1 hour
- User explicitly requests planning

### PLAN File Structure

```markdown
# PLAN: {Title}

**ID**: PLAN-{YYYYMMDD}-{slug}
**Status**: DRAFT | IN_REVIEW | APPROVED | IN_PROGRESS | COMPLETED | ABANDONED
**Author**: {agent/user}
**Created**: {date}
**Work Items**: WORK-{id}, WORK-{id}

## Problem Statement
{What problem are we solving? Why now?}

## Proposed Solution
{High-level approach}

## Alternatives Considered
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A | ... | ... | Rejected: {reason} |
| B | ... | ... | **Selected** |

## Implementation Steps
1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## References
- {Citation 1}
- {Citation 2}
```

### PLAN Lifecycle

```
DRAFT → IN_REVIEW → APPROVED → IN_PROGRESS → COMPLETED
                  ↘ ABANDONED (if rejected)
```

---

## Handoff Protocol

### Types of Handoffs

1. **Code → Review**: After implementation, before merge
2. **Review → QA**: After review approval
3. **QA → Security**: For sensitive changes
4. **Security → Merge**: Final approval

### Handoff Checklist

Before handing off, ensure:
- [ ] Work Tracker item updated with current status
- [ ] All changes committed with semantic messages
- [ ] Tests passing (if applicable)
- [ ] Documentation updated (if API changed)
- [ ] PLAN file updated (if exists)

### Handoff Message Format

```
## Handoff: {from} → {to}

**Work Item**: WORK-{id}
**Summary**: {one-line description}

### Completed
- {what was done}

### Remaining
- {what's left for next agent}

### Context
- {important information for receiving agent}

### Files Changed
- `path/to/file.py`: {what changed}
```

---

## Quality Gates

### Gate 1: Pre-Implementation

**Trigger**: Before writing code
**Checks**:
- [ ] PLAN exists (if required)
- [ ] Work Item created in tracker
- [ ] Acceptance criteria defined

### Gate 2: Pre-Review

**Trigger**: After implementation, before review
**Checks**:
- [ ] All tests passing
- [ ] No linting errors
- [ ] Type checking passes (mypy)
- [ ] Self-review completed

### Gate 3: Pre-Merge

**Trigger**: After review approval
**Checks**:
- [ ] Review comments addressed
- [ ] QA sign-off (if required)
- [ ] Security sign-off (if sensitive)
- [ ] Documentation complete

---

## Knowledge Capture Protocol

### What to Capture

| Type | Location | When |
|------|----------|------|
| Decisions | `docs/design/` | Architectural choices |
| Research | `docs/research/` | Investigation results |
| Learnings | `docs/experience/` | Post-implementation insights |
| Patterns | `docs/wisdom/` | Reusable solutions |
| Analysis | `docs/analysis/` | Problem breakdowns |
| Explorations | `docs/explorations/` | Spike results |

### Capture Format

```markdown
# {Title}

**Document ID**: {TYPE}-{NNN}
**Date**: {YYYY-MM-DD}
**Author**: {agent/user}
**Status**: DRAFT | FINAL

## Context
{Why this document exists}

## Content
{Main content}

## References
{Citations}

## Document History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
```

---

## Escalation Protocol

### When to Escalate to User

1. **Ambiguity**: Requirements unclear after research
2. **Risk**: Decision has significant irreversible impact
3. **Authority**: Action exceeds agent's mandate
4. **Conflict**: Competing constraints can't be resolved
5. **Failure**: Repeated attempts unsuccessful

### Escalation Format

```
## Escalation Required

**Reason**: {Ambiguity | Risk | Authority | Conflict | Failure}

### Situation
{What happened}

### Options
1. {Option A}: {pros/cons}
2. {Option B}: {pros/cons}

### Recommendation
{What I suggest and why}

### Decision Needed
{Specific question for user}
```

---

## Compliance Checklist

For each piece of work, verify:

- [ ] Work Item exists in tracker
- [ ] PLAN file created (if required)
- [ ] Evidence-based decisions documented
- [ ] Handoffs followed protocol
- [ ] Quality gates passed
- [ ] Knowledge captured
- [ ] All references cited
