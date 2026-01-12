# PHASE-TECHDEBT: Technical Debt

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-TECHDEBT |
| **Title** | Technical Debt |
| **Status** | ONGOING |
| **Purpose** | Track technical debt incurred during implementation |

---

## Active Technical Debt

| Debt ID | Title | Severity | Phase | Added | Resolved |
|---------|-------|----------|-------|-------|----------|
| TD-001 | TOML write needs tomli-w | LOW | PHASE-02 | 2026-01-12 | - |
| TD-002 | Windows locking needs filelock | MEDIUM | PHASE-02 | 2026-01-12 | - |

---

## Technical Debt Details

### TD-001: TOML Write Needs tomli-w

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Phase** | PHASE-02 (Architecture & Design) |
| **Added** | 2026-01-12 |
| **Owner** | - |
| **Resolution Target** | Future iteration |

**Description**:
Python's stdlib `tomllib` only supports reading TOML files. To write TOML files (for `jerry config set`), we need the `tomli-w` package.

**Current Workaround**:
For MVP, config writes can output to stdout and user can manually update files. Or use simple key=value format.

**Proper Solution**:
Add `tomli-w` to dependencies in infrastructure layer.

**Risk if Unresolved**:
Users cannot modify config via CLI, must edit files manually.

---

### TD-002: Windows Locking Needs filelock

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Phase** | PHASE-02 (Architecture & Design) |
| **Added** | 2026-01-12 |
| **Owner** | - |
| **Resolution Target** | Phase 2 of implementation |

**Description**:
The `fcntl` module is Unix-only. Windows requires `msvcrt` for file locking, or the cross-platform `filelock` library.

**Current Workaround**:
Only support Unix platforms (macOS, Linux) in initial implementation.

**Proper Solution**:
Add `filelock` package to infrastructure layer for cross-platform support.

**Risk if Unresolved**:
Windows users cannot safely use Jerry with multiple processes.

---

## Technical Debt Template

When adding technical debt, use this template:

```markdown
### TD-{NNN}: {Title}

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Phase** | {Phase where debt was incurred} |
| **Added** | {date} |
| **Owner** | {who will resolve} |
| **Resolution Target** | {when it should be resolved} |

**Description**:
{Describe the technical debt}

**Current Workaround**:
{What we're doing instead}

**Proper Solution**:
{What the correct solution should be}

**Risk if Unresolved**:
{Consequences of not addressing this debt}
```

---

## Severity Definitions

| Severity | Definition | Resolution Timeline |
|----------|------------|---------------------|
| CRITICAL | Blocks functionality | Must resolve before release |
| HIGH | Significant limitation | Resolve within 1 iteration |
| MEDIUM | Known limitation | Resolve within 3 iterations |
| LOW | Nice to have | Resolve when convenient |

---

## Technical Debt Statistics

| Metric | Value |
|--------|-------|
| Total Debt Items | 2 |
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 1 |
| Resolved | 0 |

---

## Navigation

- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
- **Bugs**: [PHASE-BUGS.md](PHASE-BUGS.md)
- **Discoveries**: [PHASE-DISCOVERY.md](PHASE-DISCOVERY.md)
