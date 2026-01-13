# WI-003: JSON5 Python Support Investigation

| Field | Value |
|-------|-------|
| **ID** | WI-003 |
| **Title** | Research JSON5 support in Python ecosystem |
| **Type** | Research |
| **Status** | COMPLETED |
| **Priority** | HIGH |
| **Phase** | PHASE-01 |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Investigate JSON5 library support in Python 3.11+ for configuration files with comments. Determine best format for Jerry configuration.

---

## Acceptance Criteria

- [x] AC-003.1: Identify available json5 Python libraries
- [x] AC-003.2: Evaluate stdlib compatibility (no external deps for domain)
- [x] AC-003.3: Assess read/write capability
- [x] AC-003.4: Document recommendation with trade-offs

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-003.1 | `json5` (pure Python, zero deps) and `pyjson5` (Cython, fast) identified | PROJ-004-e-001, Section 1 |
| AC-003.2 | `tomllib` is stdlib in Python 3.11+ (read-only TOML); no JSON5 stdlib | PROJ-004-e-001, Section 2.1-2.2 |
| AC-003.3 | json5: read/write, pyjson5: read/write, tomllib: read-only (need tomli-w for write) | PROJ-004-e-001, Section 3 |
| AC-003.4 | **Recommendation: TOML with tomllib** - zero deps, Python ecosystem aligned | PROJ-004-e-001, L2 Section |

---

## Sub-tasks

- [x] ST-003.1: Search PyPI for json5 packages
- [x] ST-003.2: Review pyjson5, json5 library docs
- [x] ST-003.3: Check if tomllib (stdlib) is a viable alternative
- [x] ST-003.4: Create research artifact with findings

---

## Key Finding

**TOML recommended over JSON5** for Jerry configuration:
- `tomllib` is stdlib (zero dependencies)
- Python ecosystem standard (pyproject.toml)
- Native comment support
- json5 is 200-6000x slower than stdlib json

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T10:10:00Z | Work item created, ps-researcher agent spawned | Claude |
| 2026-01-12T10:15:00Z | Research completed, artifact created | ps-researcher |
| 2026-01-12T10:16:00Z | All acceptance criteria verified, WI-003 COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-002 | Tracking must be set up |
| Blocks | WI-007 | Plan needs format decision |

---

## Related Artifacts

- **Research Artifact**: [PROJ-004-e-001-json5-python-support.md](../research/PROJ-004-e-001-json5-python-support.md)

---

## Sources

- [json5 PyPI](https://pypi.org/project/json5/)
- [pyjson5 PyPI](https://pypi.org/project/pyjson5/)
- [Python tomllib Documentation](https://docs.python.org/3/library/tomllib.html)
- [PEP 680 - tomllib](https://peps.python.org/pep-0680/)
