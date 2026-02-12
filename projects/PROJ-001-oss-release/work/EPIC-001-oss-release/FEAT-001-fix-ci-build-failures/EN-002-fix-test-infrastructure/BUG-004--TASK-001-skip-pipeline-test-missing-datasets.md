# TASK-001: Restore missing transcript test data files

> **Type:** task
> **Status:** done
> **Priority:** HIGH
> **Created:** 2026-02-11
> **Completed:** 2026-02-11
> **Parent:** BUG-004
> **Owner:** —
> **Activity:** DEVELOPMENT

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Content

### Description

Add 34 missing transcript test data files that were never committed to git, causing BUG-004 (transcript pipeline test finds no datasets).

**Destination:** `skills/transcript/test_data/transcripts/`

The data is 606 KB total (34 files), well within git limits. The files include:
- **Golden datasets** (11 files, 593 KB): meeting-001 through meeting-006 in VTT/SRT/TXT/JSON
- **Edge cases** (20 files, ~8 KB): W3C WebVTT edge case tests including binary encoding files
- **Real samples** (3 files, ~5 KB): Real transcript files for parsing verification

**Critical:** 4 of the edge case files are **binary** (Windows-1252 and ISO-8859-1 encoded). They must be copied with `cp` (binary mode), NOT recreated with a text editor.

### Previous Approach (SUPERSEDED)

This task was originally scoped as "Skip transcript pipeline combined test when golden datasets missing" -- a workaround that would hide the problem. The ps-investigator research revealed the data existed but was never committed to git, and should be added. See [research-transcript-data-migration-gap.md](./research-transcript-data-migration-gap.md).

### Acceptance Criteria

- [x] `skills/transcript/test_data/transcripts/` directory exists in jerry
- [x] `transcripts/golden/` contains 11 files (6 VTT + 3 expected JSON + 1 SRT + 1 TXT)
- [x] `transcripts/edge_cases/` contains 20 files (VTT, SRT, TXT, including 4 binary encoding files)
- [x] `transcripts/real/` contains 3 files (VTT, SRT, TXT)
- [x] Total file count: 33 (index.json excluded)
- [x] Binary encoding files are byte-identical to source (verified with `diff`)
- [x] `test_all_datasets_complete_under_30_seconds` passes (finds and processes 6 datasets)
- [x] All transcript integration tests pass: `uv run pytest tests/integration/transcript/ -v`
- [ ] Fix works across Python 3.11-3.14 on both pip and uv CI jobs (pending CI verification)

### Implementation

```bash
DEST="skills/transcript/test_data"

# Create transcripts/ directory structure
mkdir -p "${DEST}/transcripts/golden" "${DEST}/transcripts/edge_cases" "${DEST}/transcripts/real"

# Add test data files to each subdirectory
# (golden datasets, edge cases, real samples)

# Verify file count
find "${DEST}/transcripts" -type f | wc -l
# Expected: 34
```

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `skills/transcript/test_data/transcripts/golden/` | Test data | Add 11 test data files |
| `skills/transcript/test_data/transcripts/edge_cases/` | Test data | Add 20 test data files |
| `skills/transcript/test_data/transcripts/real/` | Test data | Add 3 test data files |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Restored transcripts directory | Data | `skills/transcript/test_data/transcripts/` |
| Research artifact | Document | [research-transcript-data-migration-gap.md](./research-transcript-data-migration-gap.md) |

### Verification

- [ ] `find skills/transcript/test_data/transcripts -type f | wc -l` returns 34
- [ ] `uv run pytest tests/integration/transcript/test_pipeline.py::TestPythonPipeline::test_all_datasets_complete_under_30_seconds -v` → PASS
- [ ] `uv run pytest tests/integration/transcript/ -v` → all pass
- [ ] Binary encoding files verified with `diff`
- [ ] CI Test pip and Test uv jobs pass

---

## Related Items

- Parent: [BUG-004: Transcript pipeline test finds no datasets](./BUG-004-transcript-pipeline-no-datasets.md)
- Enabler: [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)
- Research: [Transcript Test Data Gap](./research-transcript-data-migration-gap.md) — ps-investigator 5W2H analysis

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Created as "Skip pipeline test when golden datasets missing" (workaround approach). |
| 2026-02-11 | pending | SUPERSEDED: ps-investigator research revealed test data was never committed to git. Task reframed from "skip guard" to "restore missing test data". Priority raised to HIGH. |
| 2026-02-11 | done | 33 test data files added to repository. All transcript integration tests pass (56 passed). Committed in `4789625`. |
