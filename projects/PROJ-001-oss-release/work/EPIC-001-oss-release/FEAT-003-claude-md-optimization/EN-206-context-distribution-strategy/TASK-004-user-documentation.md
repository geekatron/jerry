# EN-206:TASK-004: Create User Documentation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-02 (Claude)
PURPOSE: Create user-facing documentation for the bootstrap process
-->

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-02T06:30:00Z
> **Due:** 2026-02-15T00:00:00Z
> **Completed:** -
> **Parent:** EN-206
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task objective - create user documentation |
| [Documentation Scope](#documentation-scope) | What to document |
| [Target Audience](#target-audience) | Who the docs are for |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Create user-facing documentation explaining:

1. **Why** - Why Jerry uses `.context/` and `.claude/` split
2. **How** - How to use `/bootstrap` to set up guardrails
3. **Troubleshooting** - Common issues and fixes
4. **Platform Notes** - Windows-specific considerations

---

## Documentation Scope

### Documents to Create/Update

| Document | Location | Purpose |
|----------|----------|---------|
| Bootstrap Guide | `docs/BOOTSTRAP.md` | Primary user guide |
| Installation Update | `docs/INSTALLATION.md` | Add bootstrap section |
| EN-205 Integration | TASK within EN-205 | Reference to bootstrap |

### Bootstrap Guide Outline

```markdown
# Jerry Bootstrap Guide

## Overview
Why Jerry separates .context/ (canonical) from .claude/ (active)

## Quick Start
jerry /bootstrap

## What Gets Bootstrapped
- Rules (mandatory-skill-usage, etc.)
- Patterns (PATTERN-CATALOG)

## Platform Notes
### macOS/Linux
Symlinks (fast, efficient)

### Windows
[Strategy from SPIKE-001]

## Troubleshooting
### "Rules not loading"
### "Permission denied"
### "Already bootstrapped"

## Advanced
### --check
### --force
### Manual setup
```

---

## Target Audience

### L0 (ELI5) - New Users

"Just run `/bootstrap` and Jerry will help you get set up."

### L1 (Engineer) - Developers

- Understand `.context/` vs `.claude/` split
- Know how to troubleshoot sync issues
- Can manually set up if needed

### L2 (Architect) - Contributors

- Understand why this architecture was chosen
- Can extend/modify the bootstrap process
- Know the trade-offs

---

## Acceptance Criteria

### Definition of Done

- [ ] `docs/BOOTSTRAP.md` created
- [ ] `docs/INSTALLATION.md` updated with bootstrap reference
- [ ] L0/L1/L2 perspectives included
- [ ] Platform-specific notes for Windows
- [ ] Troubleshooting section complete
- [ ] References to /bootstrap skill

### Documentation Quality

| Criterion | Verified |
|-----------|----------|
| Clear for new users | [ ] |
| Technically accurate | [ ] |
| Platform notes complete | [ ] |
| Troubleshooting helpful | [ ] |

---

## Related Items

### Hierarchy

- **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy.md)

### Dependencies

- **Depends On:** TASK-002 (sync mechanism), TASK-003 (/bootstrap skill)
- **Integrates With:** EN-205 (Documentation Update)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-02T06:30:00Z | Claude | pending | Task created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Task |
| **SAFe** | Task |
| **JIRA** | Task |
