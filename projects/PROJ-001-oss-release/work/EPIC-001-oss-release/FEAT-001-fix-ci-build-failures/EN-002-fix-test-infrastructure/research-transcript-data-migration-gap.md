# Research: Transcript Test Data Migration Gap

> **Type:** research
> **Status:** completed
> **Created:** 2026-02-11
> **Author:** ps-investigator (Claude)
> **Related Bug:** [BUG-004: Transcript pipeline test finds no datasets](./BUG-004-transcript-pipeline-no-datasets.md)
> **Related Task:** [TASK-001: Skip pipeline test](./BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md)
> **Source:** jerry-core → jerry migration investigation
> **Framework Reference:** Jerry Constitution P-002 (Persist Everything), P-004 (Provenance)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings and recommended action |
| [5W2H Analysis](#5w2h-analysis) | Structured investigation using 5 Whys + How framework |
| [Root Cause Analysis](#root-cause-analysis) | Migration gap diagnosis |
| [Impact Assessment](#impact-assessment) | Which tests are affected |
| [File Inventory](#file-inventory) | Detailed missing file catalog |
| [Size Analysis](#size-analysis) | Git-friendliness of test data |
| [.gitignore Analysis](#gitignore-analysis) | Exclusion pattern investigation |
| [Recommended Fix](#recommended-fix) | Copy strategy from source |
| [Updated BUG-004 Recommendation](#updated-bug-004-recommendation) | Corrected fix approach |
| [References](#references) | Evidence and citations |

---

## Executive Summary

### Key Finding

**34 transcript test data files** were NOT migrated from `jerry-core` to `jerry` during the repository split. This is the **root cause of BUG-004** (transcript pipeline test finds no datasets).

### Migration Gap

**Source Location (jerry-core):**
```
/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/
skills/transcript/test_data/transcripts/
```

**Missing in jerry:**
```
/Users/adam.nowak/workspace/GitHub/geekatron/jerry/
skills/transcript/test_data/transcripts/  ← DOES NOT EXIST
```

### What Was Migrated ✓

| Directory | Files | Status |
|-----------|-------|--------|
| `test_data/contexts/` | 10 files | ✓ Migrated |
| `test_data/expected/` | 21 files | ✓ Migrated |
| `test_data/schemas/` | 5 files | ✓ Migrated |
| `test_data/expected_output/` | 9 files | ✓ Migrated |
| `test_data/validation/` | Many files | ✓ Migrated |
| `test_data/README.md` | 1 file | ✓ Migrated |

### What Was NOT Migrated ✗

| Directory | Files | Status |
|-----------|-------|--------|
| `test_data/transcripts/golden/` | 11 files (593 KB) | ✗ Missing |
| `test_data/transcripts/edge_cases/` | 20 files (8 KB) | ✗ Missing |
| `test_data/transcripts/real/` | 3 files (5 KB) | ✗ Missing |
| **TOTAL** | **34 files (606 KB)** | **✗ Missing** |

### Recommendation

**Copy the missing 34 files from jerry-core to jerry.** The data is small (606 KB total), git-friendly, and essential for test suite integrity.

**Do NOT use the skip guard approach from TASK-001.** That was a workaround based on incomplete information. The correct fix is to restore the missing data.

---

## 5W2H Analysis

### What (Problem)

**What happened?**
During the jerry-core → jerry migration, the entire `skills/transcript/test_data/transcripts/` directory (34 files, 606 KB) was not copied to the new repository.

**What is the impact?**
- BUG-004: Pipeline integration test `test_all_datasets_complete_under_30_seconds` expects 6 VTT files, finds 0
- Edge case tests (18 test IDs from vtt-006 through vtt-014) cannot run
- Encoding fallback tests (4 test IDs enc-001 through enc-004) cannot run
- Real transcript parsing verification (vtt-001 through vtt-005) cannot run

### Why (Root Cause)

**Why were the transcripts not migrated?**

**5 Whys Analysis:**

1. **Why did BUG-004 occur?**
   - Because the test expects 6 VTT files in `skills/transcript/test_data/transcripts/golden/` but finds 0.

2. **Why does the directory have 0 files?**
   - Because the `transcripts/` directory does not exist in jerry's `test_data/` folder.

3. **Why does the directory not exist?**
   - Because it was not copied during the jerry-core → jerry repository migration.

4. **Why was it not copied during migration?**
   - Likely because:
     - The migration script/process selectively copied files
     - The `transcripts/` directory was inadvertently excluded
     - No migration checklist verified completeness of test_data/ subdirectories

5. **Why was there no verification?**
   - The migration did not include a test data inventory checklist comparing source vs. destination.
   - The CI pipeline did not run integration tests immediately after migration (would have caught this).

**Conclusion:** Process gap in migration — no systematic verification of test data completeness.

### Who (Stakeholders)

**Who is affected?**
- **Developers:** Cannot run full transcript skill test suite locally
- **CI/CD:** 3 integration tests fail on every run
- **QA/Testing:** Cannot verify transcript parsing edge cases, encoding fallback, or performance

**Who created the test data?**
- Original creator: jerry-core PROJ-008-transcript-skill team
- Test data version: 1.3.0 (updated 2026-01-28 per README.md)

### When (Timeline)

**When was test data created?**
- Initial creation: 2026-01-27 (version 1.0.0)
- Large golden dataset added: 2026-01-28 (version 1.3.0, EN-017)

**When did migration occur?**
- Repository split: Unknown exact date (between 2026-01-28 and 2026-02-10)
- BUG-004 discovered: 2026-02-10 (PR #6 CI failures)

**When was the gap discovered?**
- 2026-02-11 (this investigation)

### Where (Locations)

**Source (jerry-core):**
```
/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/
skills/transcript/test_data/transcripts/
├── golden/          (11 files, 593 KB)
├── edge_cases/      (20 files, 8 KB)
└── real/            (3 files, 5 KB)
```

**Destination (jerry):**
```
/Users/adam.nowak/workspace/GitHub/geekatron/jerry/
skills/transcript/test_data/
├── contexts/        ✓ EXISTS
├── expected/        ✓ EXISTS
├── schemas/         ✓ EXISTS
├── expected_output/ ✓ EXISTS
├── validation/      ✓ EXISTS
├── README.md        ✓ EXISTS
└── transcripts/     ✗ MISSING (should have 3 subdirectories, 34 files)
```

### How (Mechanism)

**How did migration occur?**
- Unknown exact migration mechanism (git filter-branch, git subtree, manual copy, etc.)
- Partial test_data/ migration: 6 items migrated, 1 item (transcripts/) omitted

**How was the gap detected?**
- CI pipeline failure: `test_all_datasets_complete_under_30_seconds` assertion error
- Investigation: Directory listing comparison between jerry-core and jerry

**How should it be fixed?**
- Copy the 34 missing files from jerry-core source to jerry destination
- Verify .gitignore does not exclude these files
- Commit to git (files are small and text-based)

### How Much (Quantification)

**Data Volume:**
- **Total:** 606 KB (34 files)
- **Golden datasets:** 593 KB (11 files, largest is 338 KB)
- **Edge cases:** 8 KB (20 files, all < 3 KB)
- **Real samples:** 5 KB (3 files)

**Git Impact:**
- All files are < 500 KB (well below GitHub's 100 MB limit)
- Total addition: 606 KB (negligible for git)
- Format: Text-based VTT/SRT/TXT (compresses well)

**Test Coverage Impact:**
- **Core VTT tests:** 5 tests (vtt-001 through vtt-005) — BLOCKED
- **Edge case tests:** 9 tests (vtt-006 through vtt-014) — BLOCKED
- **Encoding tests:** 4 tests (enc-001 through enc-004) — BLOCKED
- **Integration tests:** 1 combined performance test — BLOCKED
- **Total blocked:** 19 test cases across 4 categories

---

## Root Cause Analysis

### Migration Process Gap

**Evidence:**
1. **Selective migration:** Some test_data/ subdirectories were migrated (contexts/, expected/, schemas/, expected_output/, validation/), but transcripts/ was omitted.
2. **No migration manifest:** No checklist or manifest comparing source vs. destination test data.
3. **CI not run post-migration:** Integration tests were not executed immediately after migration to verify completeness.

**Root Cause:**
Incomplete migration process lacking systematic verification of test data dependencies.

### Why Transcripts Were Critical

Per the test_data/README.md (identical in both jerry-core and jerry):

```
test_data/
├── transcripts/           ← Test input files
│   ├── real/              ← Real VTT files from users
│   ├── golden/            ← Synthetic golden dataset (EN-017)
│   └── edge_cases/        ← Edge case VTT files (W3C research)
├── expected/              ← Expected parser outputs
└── validation/            ← Test specifications
```

The `transcripts/` directory contains the **input files** for all transcript skill tests. The `expected/` directory contains the **golden outputs** for comparison. Without inputs, tests cannot run.

### Why Other Test Data Was Migrated

Possible explanations:
1. **Alphabetical ordering:** `contexts/`, `expected/`, `expected_output/`, `schemas/`, `validation/` come before `transcripts/` alphabetically — may have been copied first and process stopped before transcripts/.
2. **Directory depth:** `transcripts/` has 3 subdirectories (golden/, edge_cases/, real/), others are flatter — may have been excluded by a shallow copy script.
3. **Timing:** README.md shows "Updated: 2026-01-28 (Added large transcript golden dataset - EN-017)" — if migration occurred before 2026-01-28, the transcripts/ directory may not have existed yet. However, BUG-004 was discovered 2026-02-10, suggesting migration occurred after the data was created.

---

## Impact Assessment

### Tests Affected

Based on test_data/README.md test case summary:

#### 1. Core VTT Tests (BLOCKED)

| Test ID | Name | Input File | Requirement | Status |
|---------|------|------------|-------------|--------|
| vtt-001 | Voice tags with closing tags | k8-network-policies-sample.vtt | FR-001.3 | ✗ Missing input |
| vtt-002 | Multi-line cue payloads | k8-network-policies-sample.vtt | FR-001.4 | ✗ Missing input |
| vtt-003 | Timestamp normalization | k8-network-policies-sample.vtt | NFR-006 | ✗ Missing input |
| vtt-004 | Speaker extraction | k8-network-policies-sample.vtt | FR-001.3 | ✗ Missing input |
| vtt-005 | Canonical JSON schema | k8-network-policies-sample.vtt | TDD Section 3 | ✗ Missing input |

**File:** `transcripts/real/k8-network-policies-sample.vtt` (2.9 KB) — MISSING

#### 2. Edge Case Tests (BLOCKED)

| Test ID | Name | Input File | Research ID | Status |
|---------|------|------------|-------------|--------|
| vtt-006 | Voice tags without closing | voice_tag_no_close.vtt | VT-004 | ✗ Missing input |
| vtt-007 | Voice tags with classes | voice_tag_with_class.vtt | VT-006, VT-007 | ✗ Missing input |
| vtt-008 | Multiple speakers per cue | multi_speaker_cue.vtt | VT-009 | ✗ Missing input |
| vtt-009 | Nested formatting tags | nested_formatting.vtt | VT-008, TT-008 | ✗ Missing input |
| vtt-010 | Unicode speakers/content | unicode_speakers.vtt | CE-003, CE-004 | ✗ Missing input |
| vtt-011 | HTML entity decoding | entity_escapes.vtt | CE-005–CE-007 | ✗ Missing input |
| vtt-012 | Timestamp edge cases | timestamp_edge_cases.vtt | TS-001–TS-005 | ✗ Missing input |
| vtt-013 | Empty/malformed (PAT-002) | empty_and_malformed.vtt | Error handling | ✗ Missing input |
| vtt-014 | Combined edge cases | combined_edge_cases.vtt | Comprehensive | ✗ Missing input |

**All files in:** `transcripts/edge_cases/` — MISSING

#### 3. Encoding Fallback Tests (BLOCKED)

| Test ID | Name | Input File | Requirement | Status |
|---------|------|------------|-------------|--------|
| enc-001 | Windows-1252 VTT fallback | windows1252_sample.vtt | NFR-007.1, NFR-007.2 | ✗ Missing input |
| enc-002 | ISO-8859-1 VTT fallback | iso88591_sample.vtt | NFR-007.1, NFR-007.4 | ✗ Missing input |
| enc-003 | Windows-1252 SRT fallback | windows1252_sample.srt | NFR-007.2 | ✗ Missing input |
| enc-004 | ISO-8859-1 SRT fallback | iso88591_sample.srt | NFR-007.4 | ✗ Missing input |

**All encoding test files in:** `transcripts/edge_cases/` — MISSING

**⚠️ CRITICAL:** These are **BINARY files** with specific byte sequences (Windows-1252, ISO-8859-1 encoded). They must be copied as-is using binary mode. Do NOT edit with text editors.

#### 4. Integration Pipeline Test (BLOCKED)

**Test:** `test_all_datasets_complete_under_30_seconds` in `tests/integration/transcript/test_pipeline.py`

**Expected datasets (6 VTT files in `transcripts/golden/`):**
1. `meeting-001.vtt` (4.8 KB, 8 min)
2. `meeting-002.vtt` (12 KB, unknown duration)
3. `meeting-003.vtt` (7.2 KB, unknown duration)
4. `meeting-004-sprint-planning.vtt` (89 KB, 126 min, ~23K tokens)
5. `meeting-005-roadmap-review.vtt` (142 KB, 160 min, ~37K tokens)
6. `meeting-006-all-hands.vtt` (338 KB, 304 min, ~94K tokens)

**Status:** All 6 files MISSING → test finds 0 datasets → AssertionError

---

## File Inventory

### Golden Dataset (11 files, 593 KB)

| File | Size | Format | Description |
|------|------|--------|-------------|
| `meeting-001.vtt` | 4.8 KB | VTT | Team standup (8 min, ~1.6K tokens) |
| `meeting-001.srt` | Unknown | SRT | SRT version of meeting-001 |
| `meeting-001.txt` | Unknown | TXT | Plain text version |
| `meeting-001.expected.json` | Unknown | JSON | Expected parser output |
| `meeting-002.vtt` | 12 KB | VTT | Unknown topic |
| `meeting-002.expected.json` | Unknown | JSON | Expected parser output |
| `meeting-003.vtt` | 7.2 KB | VTT | Unknown topic |
| `meeting-003.expected.json` | Unknown | JSON | Expected parser output |
| `meeting-004-sprint-planning.vtt` | 89 KB | VTT | Engineering sprint (126 min, 536 cues) |
| `meeting-005-roadmap-review.vtt` | 142 KB | VTT | Product roadmap (160 min, 899 cues) |
| `meeting-006-all-hands.vtt` | 338 KB | VTT | Quarterly all-hands (304 min, 3071 cues) |

**Purpose:** Large transcript golden dataset for testing file splitting behavior (EN-017).

**Token counts:** Uses formula `actual_tokens = (word_count × 1.3) + (cue_count × 12)` to test soft/hard split thresholds (31,500/35,000 tokens).

### Edge Cases (20 files, ~8 KB)

| File | Size | Test IDs | Description |
|------|------|----------|-------------|
| `combined_edge_cases.vtt` | 2.6 KB | All | All edge cases in one file |
| `empty_and_malformed.vtt` | 339 B | PAT-002 | Defensive parsing tests |
| `entity_escapes.vtt` | 397 B | CE-005–CE-007 | HTML entities: &amp;, &lt;, &gt; |
| `iso88591_sample.vtt` | 134 B | ENC-002 | ⚠️ BINARY: ISO-8859-1 encoding |
| `iso88591_sample.srt` | Unknown | ENC-004 | ⚠️ BINARY: ISO-8859-1 SRT |
| `multi_speaker_cue.vtt` | 279 B | VT-009 | Multiple speakers per cue |
| `multiline_payload.vtt` | 415 B | ML-001–ML-005 | Multi-line cue payloads |
| `nested_formatting.vtt` | 481 B | VT-008, TT-008 | Nested &lt;b&gt;, &lt;i&gt;, &lt;u&gt; tags |
| `timestamp_edge_cases.vtt` | 486 B | TS-001–TS-005 | Timestamp formats |
| `unicode_speakers.vtt` | 517 B | CE-003, CE-004 | Chinese, Arabic, Greek, Japanese, Emoji |
| `voice_tag_basic.vtt` | 288 B | VT-001, VT-002 | Basic voice tags |
| `voice_tag_no_close.vtt` | Unknown | VT-004 | Voice tags without &lt;/v&gt; |
| `voice_tag_with_class.vtt` | Unknown | VT-006, VT-007 | Voice tags with CSS classes |
| `windows1252_sample.vtt` | Unknown | ENC-001 | ⚠️ BINARY: Windows-1252 encoding |
| `windows1252_sample.srt` | Unknown | ENC-003 | ⚠️ BINARY: Windows-1252 SRT |
| `srt_mixed_speakers.srt` | Unknown | SRT tests | SRT with mixed speakers |
| `srt_period_timestamps.srt` | Unknown | SRT tests | SRT with period separators |
| `txt_allcaps_speakers.txt` | Unknown | TXT tests | Plain text with ALLCAPS speakers |
| `txt_bracket_speakers.txt` | Unknown | TXT tests | Plain text with [Speaker] format |
| `txt_no_speakers.txt` | Unknown | TXT tests | Plain text without speaker tags |

**Purpose:** W3C WebVTT specification edge case testing (from research in EN-007).

**⚠️ CRITICAL ENCODING FILES:**
- `iso88591_sample.vtt`, `iso88591_sample.srt` — BINARY (ISO-8859-1 bytes)
- `windows1252_sample.vtt`, `windows1252_sample.srt` — BINARY (Windows-1252 bytes)

These files contain **intentionally invalid UTF-8 byte sequences** to test encoding fallback (NFR-007). They MUST be copied in binary mode.

### Real Samples (3 files, ~5 KB)

| File | Size | Format | Description |
|------|------|--------|-------------|
| `k8-network-policies-sample.vtt` | 2.9 KB | VTT | Real user VTT (first 20 cues, 2 speakers) |
| `sample-meeting-zoom.srt` | 924 B | SRT | Real Zoom meeting SRT |
| `sample-interview.txt` | 873 B | TXT | Real interview plain text |

**Purpose:** Core VTT parsing verification (vtt-001 through vtt-005).

---

## Size Analysis

### Git-Friendliness Assessment

| Category | Total Size | Largest File | Format | Git-Friendly? |
|----------|------------|--------------|--------|---------------|
| Golden datasets | 593 KB | 338 KB | Text (VTT/SRT/TXT/JSON) | ✓ YES |
| Edge cases | ~8 KB | 2.6 KB | Text + Binary | ✓ YES |
| Real samples | ~5 KB | 2.9 KB | Text | ✓ YES |
| **TOTAL** | **~606 KB** | **338 KB** | Mixed | **✓ YES** |

**Conclusion:** All files are well below GitHub's recommended limits:
- Recommended max: 50 MB per file
- Hard limit: 100 MB per file
- Large file warning: > 50 MB
- Our largest file: 338 KB (0.34% of recommended max)

### Compression Potential

VTT/SRT/TXT files are text-based and compress well with git's internal compression:
- **Expected compression ratio:** 60-80% (typical for text)
- **Estimated git storage:** ~240-360 KB (compressed)

**Verdict:** These files are **SAFE and RECOMMENDED** for git storage.

---

## .gitignore Analysis

### Jerry Root .gitignore

Reviewing `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/.gitignore`:

```gitignore
# Jerry local data (locks, sessions)
.jerry/local/
projects/*/.jerry/
logs/hook-errors.log
```

**Key patterns:**
- `.jerry/local/` — Excludes local session data
- `projects/*/.jerry/` — Excludes project-level jerry data
- `logs/hook-errors.log` — Excludes hook error logs

**Patterns that DO NOT match transcript test data:**
- No pattern for `skills/`
- No pattern for `test_data/`
- No pattern for `*.vtt`, `*.srt`, `*.txt` files
- No pattern for `transcripts/`

**Conclusion:** `.gitignore` does NOT exclude the missing transcript files. They were never added to git, not ignored.

### Verification

```bash
# Test if transcripts/ would be ignored
git check-ignore -v skills/transcript/test_data/transcripts/golden/meeting-001.vtt
# Expected: No match (file not ignored)
```

**Result:** The files are NOT gitignored. They simply were never added during migration.

---

## Recommended Fix

### Strategy: Copy Missing Files from Source

**Approach:** Copy the 34 missing files from jerry-core to jerry, preserving directory structure.

### Copy Commands

```bash
# Define paths
SOURCE="/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data"
DEST="/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data"

# Create destination directory
mkdir -p "${DEST}/transcripts"

# Copy entire transcripts/ directory structure
cp -R "${SOURCE}/transcripts/" "${DEST}/transcripts/"

# Verify copy
ls -lR "${DEST}/transcripts/"
```

**Expected result:**
```
transcripts/
├── golden/          (11 files)
├── edge_cases/      (20 files)
└── real/            (3 files)
```

### Verification Steps

1. **Count files:**
   ```bash
   find "${DEST}/transcripts" -type f | wc -l
   # Expected: 34
   ```

2. **Check sizes match:**
   ```bash
   du -sh "${SOURCE}/transcripts/"
   du -sh "${DEST}/transcripts/"
   # Expected: Both ~606 KB (756K per du output)
   ```

3. **Verify binary files (encoding tests):**
   ```bash
   # These MUST be binary identical
   diff "${SOURCE}/transcripts/edge_cases/windows1252_sample.vtt" \
        "${DEST}/transcripts/edge_cases/windows1252_sample.vtt"
   # Expected: No output (files identical)
   ```

4. **Run affected test:**
   ```bash
   uv run pytest tests/integration/transcript/test_pipeline.py::TestPythonPipeline::test_all_datasets_complete_under_30_seconds -v
   # Expected: PASS (finds and processes 6 datasets)
   ```

### Git Commit

```bash
cd /Users/adam.nowak/workspace/GitHub/geekatron/jerry

# Stage files
git add skills/transcript/test_data/transcripts/

# Commit
git commit -m "fix(transcript): restore missing test data from jerry-core migration

Restore 34 transcript test input files that were omitted during jerry-core → jerry migration:

- Golden datasets (11 files, 593 KB): meeting-001 through meeting-006 VTT/SRT/TXT/JSON
- Edge cases (20 files, 8 KB): W3C WebVTT edge case tests, encoding fallback tests
- Real samples (3 files, 5 KB): k8-network-policies-sample.vtt and others

Root cause: Incomplete migration process lacking test data verification.

Fixes: BUG-004 (Transcript pipeline test finds no datasets)
Unblocks: 19 test cases across 4 categories (Core VTT, Edge Cases, Encoding, Integration)

Source: jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/
Research: projects/PROJ-001-oss-release/.../research-transcript-data-migration-gap.md
"
```

---

## Updated BUG-004 Recommendation

### Original TASK-001 Approach (OBSOLETE)

**TASK-001** proposed: "Skip transcript pipeline combined test when golden datasets missing"

**Rationale at the time:** Assumed test data was intentionally excluded or too large for git.

**Approach:** Add `pytest.mark.skipif` guard:
```python
@pytest.mark.skipif(
    not GOLDEN_DATASETS_DIR.exists() or not list(GOLDEN_DATASETS_DIR.glob("*.vtt")),
    reason="Golden datasets not available (not in git)"
)
def test_all_datasets_complete_under_30_seconds(...):
```

### New Recommendation (CORRECT FIX)

**Approach:** Restore the missing test data instead of skipping tests.

**Rationale:**
1. **Data is git-friendly:** 606 KB total, largest file 338 KB (well within limits)
2. **Data exists in source:** All 34 files present in jerry-core with version 1.3.0
3. **Tests are valid:** They were designed and validated in jerry-core (PROJ-008)
4. **Migration gap:** This is a migration defect, not a design decision

**Action Items:**
1. **Abandon TASK-001** — Skip guard is a workaround, not a fix
2. **Execute copy strategy** — Restore 34 missing files from jerry-core
3. **Update BUG-004 status** → Resolved (once files are committed)
4. **Add migration checklist** — Prevent future test data gaps

### TASK-001 Disposition

**Status:** OBSOLETE / SUPERSEDED

**Reason:** Original analysis was based on incomplete information (assumed data was intentionally excluded). Investigation revealed the data exists, is git-friendly, and should be migrated.

**Recommended Action:** Close TASK-001 as "Won't Fix - Root cause addressed by restoring missing data"

**Alternative:** If TASK-001 is kept, reframe it as: "TASK-001: Restore missing transcript test data from jerry-core migration"

---

## References

### Source Files (jerry-core)

| File | Path | Purpose |
|------|------|---------|
| Test Data README | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/README.md` | Test data structure and inventory (v1.3.0) |
| Golden datasets | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/golden/` | 11 VTT/SRT/TXT/JSON files (593 KB) |
| Edge cases | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/edge_cases/` | 20 VTT/SRT files (8 KB, includes binary) |
| Real samples | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/real/` | 3 VTT/SRT/TXT files (5 KB) |

### Destination Files (jerry)

| File | Path | Status |
|------|------|--------|
| Test Data README | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data/README.md` | ✓ Migrated (identical to source) |
| Transcripts directory | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data/transcripts/` | ✗ MISSING (does not exist) |

### Bug Reports

| File | Path | Description |
|------|------|-------------|
| BUG-004 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004-transcript-pipeline-no-datasets.md` | Main bug report (status: pending) |
| TASK-001 | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-001-fix-ci-build-failures/EN-002-fix-test-infrastructure/BUG-004--TASK-001-skip-pipeline-test-missing-datasets.md` | Skip guard workaround (now obsolete) |

### Test Files

| File | Path | Description |
|------|------|-------------|
| Pipeline integration test | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/tests/integration/transcript/test_pipeline.py` | Contains `test_all_datasets_complete_under_30_seconds` (expects 6 VTT files) |

### Migration Evidence

| Evidence | Finding |
|----------|---------|
| Source directory exists | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry-core-gitwt/PROJ-008-transcript-skill/skills/transcript/test_data/transcripts/` contains 34 files |
| Destination directory missing | `/Users/adam.nowak/workspace/GitHub/geekatron/jerry/skills/transcript/test_data/transcripts/` does not exist |
| Partial migration | 6/7 test_data/ subdirectories migrated, transcripts/ omitted |
| .gitignore clean | No patterns in `.gitignore` match transcript files |

### Jerry Framework References

| Principle | Relevance |
|-----------|-----------|
| P-002: Persist Everything | Test data MUST be persisted to enable reproducible testing |
| P-004: Provenance | Test data source (jerry-core PROJ-008, EN-017) documented in README.md |
| P-022: No Deception | Must not skip tests without explaining why data is missing |

### Jerry Design Patterns

| Pattern | Application |
|---------|-------------|
| Test Data as Artifacts | Golden datasets, edge cases, and real samples are first-class artifacts |
| Self-Contained Skills | Transcript skill test data should live in `skills/transcript/test_data/` (correctly designed) |
| Evidence-Based Decisions | This investigation provides evidence for copy strategy over skip strategy |

---

## Conclusion

The transcript test data migration gap is a **process defect**, not a design decision. The correct fix is to **restore the missing 34 files** (606 KB total) from jerry-core to jerry. This will:

1. **Resolve BUG-004** (test finds 0 of 6 expected datasets)
2. **Unblock 19 test cases** across Core VTT, Edge Cases, Encoding, and Integration categories
3. **Restore test suite integrity** to match jerry-core PROJ-008 validation framework
4. **Prevent technical debt** from accumulating (skip guards are workarounds, not solutions)

**Recommended Action:** Execute the copy strategy outlined in [Recommended Fix](#recommended-fix) section.

---

*Research completed: 2026-02-11*
*Investigator: ps-investigator (Claude)*
*Framework: Jerry Constitution P-002, P-004*
*Evidence: jerry-core source files, jerry destination inspection, .gitignore analysis, BUG-004 symptoms*
