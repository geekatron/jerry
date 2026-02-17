# TASK-005: Fix ci.yml test-uv Windows shell syntax

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Created:** 2026-02-16T23:00:00Z
> **Parent:** BUG-001
> **Owner:** Claude
> **Activity:** DEVELOPMENT
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical details |
| [Evidence](#evidence) | Verification |
| [History](#history) | Changes |

---

## Description

Update `.github/workflows/ci.yml` test-uv job to use `shell: bash` on steps with multi-line commands that use bash-style `\` line continuations. Windows runners default to PowerShell, which cannot parse `\` continuations, causing `ParserError`.

---

## Acceptance Criteria

- [ ] `test-uv` job steps with multi-line `\` commands have `shell: bash`
- [ ] CI YAML syntax is valid (`act` or manual review)

---

## Implementation Notes

**File:** `.github/workflows/ci.yml`

The `test-uv` job's "Run tests with coverage" step uses:
```yaml
- name: Run tests with coverage
  run: |
    uv run pytest \
      -m "not llm" \
      ...
```

Add `shell: bash` to this step:
```yaml
- name: Run tests with coverage
  shell: bash
  run: |
    uv run pytest \
      -m "not llm" \
      ...
```

Review all other steps in the job for similar issues.

---

## Related Items

- Parent: [BUG-001](./BUG-001-pr13-ci-pipeline-failures.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| — | — | — |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation |

---
