# TASK-001: Restore missing transcript test data from jerry-core migration

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

Copy 34 missing transcript test data files from the jerry-core source repository to jerry. These files were omitted during the jerry-core -> jerry repository migration, causing BUG-004 (transcript pipeline test finds no datasets).

**Source:** `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/`

**Destination:** `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data/transcripts/`

The data is 606 KB total (34 files), well within git limits. The files include:
- **Golden datasets** (11 files, 593 KB): meeting-001 through meeting-006 in VTT/SRT/TXT/JSON
- **Edge cases** (20 files, ~8 KB): W3C WebVTT edge case tests including binary encoding files
- **Real samples** (3 files, ~5 KB): Real transcript files for parsing verification

**Critical:** 4 of the edge case files are **binary** (Windows-1252 and ISO-8859-1 encoded). They must be copied with `cp` (binary mode), NOT recreated with a text editor.

### Previous Approach (SUPERSEDED)

This task was originally scoped as "Skip transcript pipeline combined test when golden datasets missing" — a workaround that would hide the problem. The ps-investigator research revealed the data exists in jerry-core and should be restored. See [research-transcript-data-migration-gap.md](./research-transcript-data-migration-gap.md).

### Acceptance Criteria

- [x] `skills/transcript/test_data/transcripts/` directory exists in jerry
- [x] `transcripts/golden/` contains 11 files (6 VTT + 3 expected JSON + 1 SRT + 1 TXT)
- [x] `transcripts/edge_cases/` contains 20 files (VTT, SRT, TXT, including 4 binary encoding files)
- [x] `transcripts/real/` contains 3 files (VTT, SRT, TXT)
- [x] Total file count: 33 (1 fewer than jerry-core due to index.json exclusion)
- [x] Binary encoding files are byte-identical to source (verified with `diff`)
- [x] `test_all_datasets_complete_under_30_seconds` passes (finds and processes 6 datasets)
- [x] All transcript integration tests pass: `uv run pytest tests/integration/transcript/ -v`
- [ ] Fix works across Python 3.11-3.14 on both pip and uv CI jobs (pending CI verification)

### Implementation

```bash
SOURCE="/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data"
DEST="/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data"

# Copy entire transcripts/ directory structure
cp -R "${SOURCE}/transcripts/" "${DEST}/transcripts/"

# Verify file count
find "${DEST}/transcripts" -type f | wc -l
# Expected: 34

# Verify binary files are identical
diff "${SOURCE}/transcripts/edge_cases/windows1252_sample.vtt" \
     "${DEST}/transcripts/edge_cases/windows1252_sample.vtt"
# Expected: No output (identical)
```

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `skills/transcript/test_data/transcripts/golden/` | Test data | Copy 11 files from jerry-core |
| `skills/transcript/test_data/transcripts/edge_cases/` | Test data | Copy 20 files from jerry-core |
| `skills/transcript/test_data/transcripts/real/` | Test data | Copy 3 files from jerry-core |

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
- [ ] Binary encoding files verified with `diff` against source
- [ ] CI Test pip and Test uv jobs pass

---

## Related Items

- Parent: [BUG-004: Transcript pipeline test finds no datasets](./BUG-004-transcript-pipeline-no-datasets.md)
- Enabler: [EN-002: Fix Test Infrastructure](./EN-002-fix-test-infrastructure.md)
- Feature: [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)
- Research: [Transcript Data Migration Gap](./research-transcript-data-migration-gap.md) — ps-investigator 5W2H analysis

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-11 | pending | Created as "Skip pipeline test when golden datasets missing" (workaround approach). |
| 2026-02-11 | pending | SUPERSEDED: ps-investigator research revealed data migration gap. Task reframed from "skip guard" to "restore missing data from jerry-core". Priority raised to HIGH. |
| 2026-02-11 | done | 33 files restored from jerry-core. All transcript integration tests pass (56 passed). Committed in `4789625`. |
