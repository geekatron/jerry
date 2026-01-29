# FEAT-002:DISC-007: VTT Generation Validation Gap

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-28
> **Completed:** 2026-01-28
> **Parent:** FEAT-002-implementation
> **Owner:** Claude
> **Source:** EN-017 TASK-142 execution

---

## Summary

The test infrastructure validates **parser behavior** (how ts-parser handles various VTT inputs) but lacks **VTT file compliance validation** (ensuring generated VTT files meet W3C WebVTT specification before they enter the pipeline).

**Key Findings:**
- Parser-tests.yaml validates parser OUTPUT quality, not VTT INPUT compliance
- No standalone tool validates VTT files against W3C spec before processing
- Golden dataset generation could produce invalid VTT files that waste tokens and cause downstream issues

**Validation:** DOCUMENTED - Gap confirmed through code inspection and test infrastructure review

---

## Context

### Background

During EN-017 TASK-142 (Create meeting-005-roadmap-review.vtt), the user ran the W3C WebVTT validator and reported validation errors. Investigation revealed that while the current file appears valid, the underlying infrastructure lacks proactive validation.

### Research Question

Does the transcript skill have adequate infrastructure to validate VTT file compliance with W3C specification before files enter the parsing pipeline?

### Investigation Approach

1. Searched for validation tools in `skills/transcript/test_data/`
2. Reviewed `parser-tests.yaml` test specifications
3. Reviewed `ts-parser.md` agent definition
4. Reviewed `test_data/README.md` for validation coverage

---

## Finding

### Two Distinct Validation Concerns

| Concern | Description | Current State |
|---------|-------------|---------------|
| **VTT File Compliance** | Does the raw VTT file meet W3C WebVTT spec? | **GAP** - No automated validation |
| **Parser Behavior** | Does ts-parser handle various VTT inputs correctly? | COVERED by parser-tests.yaml |

### Gap Analysis

**What parser-tests.yaml covers:**
- Voice tag extraction (with/without closing tags)
- Timestamp normalization (VTT format to milliseconds)
- Speaker extraction from `<v>` tags
- Multi-line payload handling
- Edge cases (unicode, entities, malformed cues)
- Encoding fallback (Windows-1252, ISO-8859-1)

**What is NOT covered:**
- Validation that WEBVTT header is present
- Validation that timestamps are monotonically increasing
- Validation that seconds values are < 60
- Validation that cue structure follows spec (blank line between cues)
- Pre-processing validation before files enter pipeline

### W3C WebVTT Compliance Rules (Relevant Subset)

Per W3C WebVTT Specification (https://www.w3.org/TR/webvtt1/):

1. **Header**: File MUST start with "WEBVTT"
2. **Timestamps**: Format `[HH:]MM:SS.mmm --> [HH:]MM:SS.mmm`
3. **Timestamp Ordering**: Start timestamp MUST be >= previous cue's start timestamp
4. **Seconds**: MUST be 00-59 (not >= 60)
5. **Cue Structure**: Cues separated by blank lines
6. **Voice Tags**: `<v Name>` opens, `</v>` closes (closing optional)

### Validation

The gap was confirmed by:
1. Grepping for "valid" in test_data/ - found only parser behavior tests
2. Reviewing ts-parser.md - focuses on parsing, not input validation
3. Reviewing test_data/README.md - no mention of pre-processing validation
4. Creating ad-hoc Python validation script that passed all golden files

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Code | parser-tests.yaml tests parser output, not input compliance | skills/transcript/test_data/validation/parser-tests.yaml | 2026-01-28 |
| E-002 | Spec | W3C WebVTT specification defines validation rules | https://www.w3.org/TR/webvtt1/ | 2026-01-28 |
| E-003 | Tool | W3C WebVTT online validator | https://w3c.github.io/webvtt.js/parser.html | 2026-01-28 |

### Reference Material

- **Source:** W3C WebVTT Specification
- **URL:** https://www.w3.org/TR/webvtt1/
- **Date Accessed:** 2026-01-28
- **Relevance:** Defines what constitutes a valid VTT file

---

## Implications

### Impact on Project

Without VTT compliance validation:
- Large transcript generation (EN-017) could produce invalid files
- Token waste when regenerating invalid content
- Potential downstream parser errors or silent data corruption
- No safety net for human-created or AI-generated VTT files

### Design Decisions Affected

- **Decision:** EN-017 large transcript generation strategy
  - **Impact:** Should validate VTT files during creation, not after
  - **Rationale:** Catch errors early, avoid token waste

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Invalid VTT files enter pipeline | HIGH | Add pre-processing validation step |
| Token waste on regeneration | MEDIUM | Validate incrementally during generation |
| Silent data corruption | LOW | Parser defensively handles malformed input |

### Opportunities Created

- Create reusable VTT validation utility for EN-017 and EN-015
- Add validation step to TASK-144 (Dataset Validation)
- Enhance parser-tests.yaml with input compliance tests

---

## Relationships

### Creates

- VTT validation utility (skills/transcript/scripts/validate_vtt.py) - RECOMMENDED
- TASK-144 should include VTT compliance validation step

### Informs

- [EN-017](./EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) - Large transcript generation
- [TASK-142](./EN-017-large-transcript-dataset/TASK-142-meeting-005-creation.md) - meeting-005 creation
- [TASK-143](./EN-017-large-transcript-dataset/TASK-143-meeting-006-creation.md) - meeting-006 creation
- [TASK-144](./EN-017-large-transcript-dataset/TASK-144-dataset-validation.md) - Dataset validation

### Related Discoveries

- [FEAT-002--DISC-006-token-estimation-formula.md](./FEAT-002--DISC-006-token-estimation-formula.md) - Token estimation inaccuracy

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002-implementation.md](./FEAT-002-implementation.md) | Parent feature |
| Test Spec | [parser-tests.yaml](../../../skills/transcript/test_data/validation/parser-tests.yaml) | Parser behavior tests |
| W3C Spec | https://www.w3.org/TR/webvtt1/ | WebVTT specification |

---

## Recommendations

### Immediate Actions

1. Create `skills/transcript/scripts/validate_vtt.py` utility that checks:
   - WEBVTT header presence
   - Timestamp format compliance
   - Monotonic timestamp ordering
   - Seconds < 60 validation
   - Cue structure validation

2. Update TASK-144 (Dataset Validation) to include VTT compliance validation step

### Long-term Considerations

- Consider adding VTT validation to ts-parser as pre-processing step
- Add VTT compliance tests to parser-tests.yaml (input validation suite)
- Document VTT generation rules for golden dataset creation

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Created discovery documenting VTT validation gap |

---

## Metadata

```yaml
id: "FEAT-002:DISC-007"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "VTT Generation Validation Gap"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-28"
updated_at: "2026-01-28"
completed_at: "2026-01-28"
tags: [validation, vtt, w3c, quality, testing]
source: "EN-017 TASK-142 execution"
finding_type: GAP
confidence_level: HIGH
validated: true
```
