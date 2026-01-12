# PHASE-BUGS: Bug Tracking

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-BUGS |
| **Title** | Bug Tracking |
| **Status** | ONGOING |
| **Purpose** | Track bugs discovered during implementation |

---

## Active Bugs

| Bug ID | Title | Severity | Status | Work Item | Found | Resolved |
|--------|-------|----------|--------|-----------|-------|----------|
| - | No bugs reported yet | - | - | - | - | - |

---

## Bug Template

When adding a bug, use this template:

```markdown
### BUG-{NNN}: {Title}

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Status** | OPEN / IN_PROGRESS / FIXED / WONTFIX |
| **Found In** | WI-{NNN} |
| **Reported** | {date} |
| **Resolved** | {date} |

**Description**:
{Describe the bug}

**Steps to Reproduce**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected Behavior**:
{What should happen}

**Actual Behavior**:
{What actually happens}

**Root Cause**:
{Analysis of why this happened}

**Fix**:
{Description of the fix applied}

**Evidence**:
- Commit: {hash}
- Test: {test file/function}
```

---

## Severity Definitions

| Severity | Definition | Response |
|----------|------------|----------|
| CRITICAL | System unusable, data corruption | Fix immediately |
| HIGH | Major functionality broken | Fix within current phase |
| MEDIUM | Minor functionality impacted | Fix before phase completion |
| LOW | Cosmetic or minor inconvenience | Fix when convenient |

---

## Bug Statistics

| Metric | Value |
|--------|-------|
| Total Bugs | 0 |
| Open | 0 |
| Fixed | 0 |
| Won't Fix | 0 |

---

## Navigation

- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
- **Tech Debt**: [PHASE-TECHDEBT.md](PHASE-TECHDEBT.md)
- **Discoveries**: [PHASE-DISCOVERY.md](PHASE-DISCOVERY.md)
