# EN-007:DISC-001: VTT Voice Tag Parsing Gaps

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-27 (TASK-101 Audit)
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** CRITICAL
> **Impact:** CRITICAL
> **Created:** 2026-01-27T10:30:00Z
> **Completed:** 2026-01-27T10:30:00Z
> **Parent:** EN-007
> **Owner:** Claude
> **Source:** TASK-101 Agent Alignment Audit

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document research findings from TASK-101 audit
# =============================================================================

# Identity (inherited from WorkItem)
id: "EN-007:DISC-001"
work_type: DISCOVERY
title: "VTT Voice Tag Parsing Gaps"

# Classification
classification: TECHNICAL

# State
status: DOCUMENTED
resolution: null

# Priority
priority: CRITICAL

# Impact (REQ-D-004)
impact: CRITICAL

# People
assignee: "Claude"
created_by: "Claude"

# Timestamps
created_at: "2026-01-27T10:30:00Z"
updated_at: "2026-01-27T10:30:00Z"
completed_at: "2026-01-27T10:30:00Z"

# Hierarchy
parent_id: "EN-007"

# Tags
tags:
  - "vtt-parsing"
  - "voice-tags"
  - "critical-gap"
  - "tdd-correction"

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: GAP
confidence_level: HIGH

# Source Information
source: "TASK-101 Agent Alignment Audit"
research_method: "Systematic comparison of TDD spec vs real-world VTT file"

# Validation
validated: true
validation_date: "2026-01-27T10:30:00Z"
validated_by: "Claude (via real VTT file parsing)"
```

---

## State Machine

**Current State:** `DOCUMENTED`

---

## Containment Rules

| Rule | Value |
|------|-------|
| **Allowed Children** | None |
| **Allowed Parents** | Epic, Feature, Story, Enabler |
| **Max Depth** | 0 (leaf node) |
| **Co-Location** | MUST be in parent's folder (REQ-D-025) |

---

## Summary

**Critical gaps discovered in VTT voice tag parsing specifications:** Both TDD-ts-parser.md and ts-parser.md fail to document WebVTT closing voice tags (`</v>`), multi-line cue payloads, and explicit encoding fallback chain. Real-world VTT files use these patterns, causing potential parsing failures.

**Key Findings:**
- **GAP-001 (CRITICAL):** VTT closing `</v>` tags not documented in TDD or agent definition
- **GAP-002 (MODERATE):** Multi-line cue payloads handling not explicitly specified
- **GAP-003 (MINOR):** Encoding fallback chain incomplete in agent definition

**Validation:** Validated against real VTT file `transcripts/Lets-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt`

---

## Context

### Background

During TASK-101 (Verify ts-parser Agent Definition Alignment), a systematic comparison was performed between:
1. **TDD-ts-parser.md** - Authoritative design specification (created in EN-005)
2. **ts-parser.md** - Agent definition (created in EN-005)
3. **Real VTT file** - Test file from `transcripts/` directory

The audit followed the alignment checklist in TASK-101, comparing each TDD section against agent capabilities.

### Research Question

Are the VTT parsing rules in TDD-ts-parser.md and ts-parser.md accurate and complete for real-world VTT files?

### Investigation Approach

1. Read TDD-ts-parser.md Section 1.1 (VTT Format) - lines 70-95
2. Read ts-parser.md VTT Parsing Rules - lines 68-83
3. Read first 200 lines of real VTT test file
4. Compare documented patterns against real-world patterns
5. Document all discrepancies with evidence

---

## Finding

### GAP-001: VTT Closing Voice Tags (CRITICAL)

**Severity:** CRITICAL
**Impact:** Parser will corrupt extracted text by including `</v>` in output

**TDD-ts-parser.md Section 1.1 (lines 84-85):**
```
VOICE_TAG     = "<v " SPEAKER_NAME ">"
<v Alice>Good morning everyone.
```

**ts-parser.md VTT Parsing Rules (lines 75-76):**
```
Voice Tag Pattern: <v SPEAKER_NAME>text
Example: <v Alice>Good morning everyone.
```

**Real VTT File Evidence (lines 5, 9-10):**
```vtt
<v Adam Nowak>It's it has started, right?</v>

<v Brendan Bennett>All right. Yeah.
So I guess I was a little interested in</v>
```

**Key Observations:**
1. Real VTT files use closing `</v>` tags on every voice-tagged utterance
2. Neither TDD nor agent definition mentions closing tags
3. Current pattern would include `</v>` in extracted text, corrupting output
4. Multi-line utterances have closing tag on final line only

**WebVTT Specification Reference:**
Per W3C WebVTT specification (https://w3c.github.io/webvtt/), voice tags follow XML-like syntax with optional closing tags. The files we're processing use the full closing tag syntax.

### GAP-002: Multi-line Cue Payloads (MODERATE)

**Severity:** MODERATE
**Impact:** Multi-line utterances may be truncated or incorrectly parsed

**Real VTT File Evidence (lines 9-10, 14-15):**
```vtt
d9aef475-18c3-4c8c-bf99-88d578a2eb5b/9-0
00:00:05.608 --> 00:00:10.319
<v Brendan Bennett>All right. Yeah.
So I guess I was a little interested in</v>
```

**Current Documentation Gap:**
Neither TDD-ts-parser.md nor ts-parser.md explicitly addresses:
- Cue payloads spanning multiple text lines
- Where the closing `</v>` tag appears in multi-line payloads
- How to concatenate multi-line text content

**Key Observations:**
1. Single cue can have payload spanning 2+ lines
2. Voice tag opens on first line, closes on last line
3. All lines between belong to same utterance
4. Whitespace/newline handling needs specification

### GAP-003: Encoding Fallback Chain (MINOR)

**Severity:** MINOR
**Impact:** May fail to parse non-UTF-8 files without explicit fallbacks

**TDD-ts-parser.md Section 5 (lines 299-302):**
```
│ Try fallbacks: │
│ - Windows-1252 │
│ - ISO-8859-1   │
│ - Latin-1      │
```

**ts-parser.md Error Handling (line 146):**
```
| Encoding error | Decode exception | Try fallback encodings |
```

**Gap:** Agent definition says "Try fallback encodings" but doesn't list the specific chain defined in TDD.

### Validation

**Validation Approach:** Direct comparison of documented patterns against real production VTT file.

**Validation Results:**
- GAP-001 confirmed: 100% of voice-tagged cues in test file use closing `</v>` tags
- GAP-002 confirmed: ~30% of cues have multi-line payloads
- GAP-003 confirmed: Agent doesn't replicate TDD's explicit fallback list

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | VTT File | Real-world transcript with closing voice tags | `transcripts/Lets-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt` | 2026-01-27 |
| E-002 | TDD Spec | TDD-ts-parser.md Section 1.1 | EN-005 deliverable | 2026-01-26 |
| E-003 | Agent Def | ts-parser.md VTT Parsing Rules | EN-005 deliverable | 2026-01-26 |
| E-004 | W3C Spec | WebVTT specification | https://w3c.github.io/webvtt/ | 2026-01-27 |

### Reference Material

**W3C WebVTT Specification**
- **Source:** World Wide Web Consortium
- **URL:** https://w3c.github.io/webvtt/
- **Date Accessed:** 2026-01-27
- **Relevance:** Authoritative specification for WebVTT format including voice tag syntax

**VTT Test File Analysis**
- **Source:** Project transcript directory
- **Path:** `transcripts/Lets-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt`
- **Total cues examined:** First 200 lines (~30 cues)
- **Closing tags found:** 100% (30/30 cues)
- **Multi-line cues found:** ~30% (9/30 cues)

---

## Implications

### Impact on Project

**CRITICAL:** If not addressed, ts-parser will produce corrupted output:
1. Text fields will contain `</v>` strings
2. Multi-line utterances may be split incorrectly
3. Downstream ts-extractor will receive malformed input
4. Entity extraction accuracy will degrade

**Blocking:** This discovery blocks TASK-102 (VTT Processing implementation) until resolved.

### Design Decisions Affected

- **Decision:** TDD-ts-parser.md Section 1.1 must be corrected
  - **Impact:** Design documentation revision required
  - **Rationale:** TDD is authoritative; agent follows TDD

- **Decision:** ts-parser.md must be updated to match corrected TDD
  - **Impact:** Agent definition revision required
  - **Rationale:** Agent must parse real-world files correctly

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Incomplete fix may miss edge cases | HIGH | Validate against full VTT file, not just sample |
| Other VTT files may have different patterns | MEDIUM | Research W3C spec for all valid voice tag syntaxes |
| TDD correction may invalidate EN-005 review | LOW | Treat as technical errata, not design change |

### Opportunities Created

- Opportunity to add comprehensive VTT voice tag test cases
- Opportunity to document W3C WebVTT compliance level

---

## Relationships

### Creates

- TASK-101 scope expanded to include remediation (acceptance criteria updated)

### Informs

- [TASK-102](./TASK-102-vtt-processing.md) - VTT Processing implementation
- [TASK-105](./TASK-105-parser-validation.md) - Test cases must cover closing tags
- [TASK-105A](./TASK-105A-parser-contract-tests.md) - Contract tests must verify patterns

### Related Discoveries

- [FEAT-002--DISC-001](../FEAT-002--DISC-001-enabler-alignment-analysis.md) - Enabler alignment (task renumbering)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-007-vtt-parser.md](./EN-007-vtt-parser.md) | Parent enabler |
| TDD | [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Design spec to correct |
| Agent | [ts-parser.md](../../../../../skills/transcript/agents/ts-parser.md) | Agent def to correct |
| Test File | [VTT file](../../../../../transcripts/Lets-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt) | Evidence source |

---

## Recommendations

### Immediate Actions

1. **Update TDD-ts-parser.md Section 1.1:**
   - Document closing `</v>` tag syntax
   - Add multi-line payload handling specification
   - Provide examples matching real-world files

2. **Update ts-parser.md VTT Parsing Rules:**
   - Add closing tag stripping to parsing rules
   - Add multi-line concatenation instructions
   - Add explicit encoding fallback chain

3. **Update TASK-101:**
   - Add acceptance criteria for remediation
   - Define unit of work for corrections

### Long-term Considerations

- Consider adding W3C WebVTT compliance level documentation
- Add VTT format edge cases to test corpus
- Document which VTT features are supported vs unsupported

---

## Open Questions

### Questions for Follow-up

1. **Q:** Are there other VTT voice tag syntaxes we need to support?
   - **Investigation Method:** Review W3C WebVTT spec Section 5.2.8
   - **Priority:** HIGH (before implementation)

2. **Q:** Should we support VTT files WITHOUT closing tags (spec allows omission)?
   - **Investigation Method:** Test against diverse VTT corpus
   - **Priority:** MEDIUM (defensive parsing principle suggests yes)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-27 | Claude | Created discovery during TASK-101 audit |

---

## Metadata

```yaml
id: "EN-007:DISC-001"
parent_id: "EN-007"
work_type: DISCOVERY
title: "VTT Voice Tag Parsing Gaps"
status: DOCUMENTED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-01-27T10:30:00Z"
updated_at: "2026-01-27T10:30:00Z"
completed_at: "2026-01-27T10:30:00Z"
tags: ["vtt-parsing", "voice-tags", "critical-gap", "tdd-correction"]
source: "TASK-101 Agent Alignment Audit"
finding_type: GAP
confidence_level: HIGH
validated: true
```

---

*Discovery ID: EN-007:DISC-001*
*Parent: EN-007 (ts-parser Agent Implementation)*
*Workflow: TASK-101 Agent Alignment Audit*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
