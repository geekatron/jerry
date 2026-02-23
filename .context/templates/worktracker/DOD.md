# Definition of Done (Team-Level)

> These items apply to ALL work items equally. They do NOT belong in individual Acceptance Criteria.
> If it applies to every work item, it is DoD -- not AC. See `worktracker-content-standards.md`.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Code Quality](#code-quality) | Review, testing, and coverage standards |
| [Documentation](#documentation) | Documentation update requirements |
| [Verification](#verification) | QA and acceptance verification |
| [Usage Guidance](#usage-guidance) | When and how to reference this file |

---

## Code Quality

- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code coverage meets threshold

## Documentation

- [ ] Documentation updated
- [ ] API documentation current
- [ ] User-facing help updated (if applicable)

## Verification

- [ ] Acceptance criteria verified
- [ ] QA testing complete
- [ ] No critical bugs remaining

---

## Usage Guidance

### What This File Is

This file defines the **team-level Definition of Done** -- the process-quality standards that every work item must satisfy before closure. These are universal requirements, not specific to any individual story, bug, or task.

### What This File Is NOT

This file is NOT a source of Acceptance Criteria. Do not copy these items into individual work item AC sections.

### The Universal Test

> **If it applies to every work item equally, it is DoD -- not AC.**

| Example | AC or DoD? |
|---------|-----------|
| "User can reset password via email" | AC (specific to one story) |
| "All unit tests pass" | DoD (applies to everything) |
| "API returns 404 for missing asset" | AC (specific to one endpoint) |
| "Code reviewed by a peer" | DoD (applies to everything) |

### Cross-References

- **Content Quality Standards:** `skills/worktracker/rules/worktracker-content-standards.md`
- **Behavior Rules (WTI-008a):** `skills/worktracker/rules/worktracker-behavior-rules.md`
