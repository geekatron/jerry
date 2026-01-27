# TASK-101: Verify ts-parser Agent Definition Alignment

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
REVISED: 2026-01-27 per DISC-001 audit findings
-->

---

## Frontmatter

```yaml
id: "TASK-101"
work_type: TASK
title: "Verify ts-parser Agent Definition Alignment"
description: |
  Review and verify that the existing ts-parser agent definition
  (skills/transcript/agents/ts-parser.md) aligns with TDD-ts-parser.md.
  REVISED: Includes remediation of DISC-001 gaps (VTT voice tag parsing).

classification: ENABLER
status: DONE
resolution: completed
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-27T12:30:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "alignment"
  - "disc-001"

effort: 3  # Increased from 2 due to remediation scope
acceptance_criteria: |
  See Acceptance Criteria section below (revised per DISC-001)

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 0
time_spent: 4
```

---

## State Machine

**Current State:** `IN_PROGRESS`

**State History:**
- 2026-01-26: BACKLOG (created)
- 2026-01-27: IN_PROGRESS (audit started, DISC-001 discovered)

---

## Content

### Description

Review the existing ts-parser agent definition (created in EN-005) and verify alignment with the authoritative TDD-ts-parser.md document. This is the foundation task that all other EN-007 tasks depend on.

**REVISED 2026-01-27:** During audit execution, critical gaps were discovered (see [DISC-001](./EN-007--DISC-001-vtt-voice-tag-gaps.md)). This task now includes remediation work to fix both TDD-ts-parser.md and ts-parser.md.

---

## Unit of Work

### Phase 1: Audit (COMPLETE)

Systematic comparison of ts-parser.md against TDD-ts-parser.md:

| TDD Section | Status | Finding |
|-------------|--------|---------|
| 1.1 VTT Processing | ⚠️ GAP | Closing `</v>` tags not documented |
| 1.2 SRT Processing | ✅ ALIGNED | - |
| 1.3 Plain Text Processing | ✅ ALIGNED | - |
| 2 Format Detection | ✅ ALIGNED | - |
| 3 Canonical Schema | ✅ ALIGNED | - |
| 4 Timestamp Normalization | ✅ ALIGNED | - |
| 5 Encoding Detection | ⚠️ MINOR | Fallback chain incomplete |
| 6 Error Handling | ✅ ALIGNED | - |

**Overall Alignment:** 85% - REVISIONS REQUIRED

### Phase 2: Remediation (IN PROGRESS)

Fix identified gaps in both design specification and agent definition:

#### 2.1 Update TDD-ts-parser.md

**File:** `projects/.../EN-005-design-documentation/docs/TDD-ts-parser.md`

**Changes Required:**

1. **Section 1.1 VTT Format (lines 70-95):**
   - Add closing `</v>` tag to VOICE_TAG grammar
   - Update example to show closing tag
   - Add multi-line payload handling specification

2. **Section 5 Encoding Detection (lines 269-304):**
   - No changes needed (already explicit)

**Expected Deliverable:** Corrected TDD-ts-parser.md with errata documented

#### 2.2 Update ts-parser.md

**File:** `skills/transcript/agents/ts-parser.md`

**Changes Required:**

1. **VTT Parsing Rules (lines 68-83):**
   - Update Voice Tag Pattern to include closing tag
   - Add closing tag stripping instructions
   - Add multi-line cue payload handling

2. **Error Handling (line 146):**
   - Add explicit encoding fallback chain

**Expected Deliverable:** Corrected ts-parser.md matching revised TDD

### Phase 3: Validation (PENDING)

Verify corrections against real VTT file:
- Test file: `transcripts/Lets-chat-internal-sample-and-dual-bindings-for-Defense-in-Depth.vtt`
- Validate voice tag patterns match
- Validate multi-line handling specified

---

## Acceptance Criteria

### Phase 1: Audit (COMPLETE)

- [x] **AC-001:** Read current ts-parser.md agent definition
- [x] **AC-002:** Compare against TDD-ts-parser.md requirements
- [x] **AC-003:** Verify FormatDetector capability documented
- [x] **AC-004:** Verify VTTProcessor capability documented
- [x] **AC-005:** Verify SRTProcessor capability documented
- [x] **AC-006:** Verify PlainParser capability documented
- [x] **AC-007:** Verify Normalizer capability documented
- [x] **AC-008:** Verify output schema matches TDD Section 3
- [x] **AC-009:** Document any discrepancies (see DISC-001)

### Phase 2: Remediation (COMPLETE)

- [x] **AC-010:** TDD Section 1.1 updated with closing `</v>` tag documentation
- [x] **AC-011:** TDD Section 1.1 updated with multi-line payload handling
- [x] **AC-012:** ts-parser.md VTT Parsing Rules updated with closing tag stripping
- [x] **AC-013:** ts-parser.md VTT Parsing Rules updated with multi-line handling
- [x] **AC-014:** ts-parser.md encoding fallback chain made explicit
- [x] **AC-015:** Both files maintain internal consistency

### Phase 3: Validation (COMPLETE)

- [x] **AC-016:** Voice tag pattern validated against real VTT file
  - Evidence: Line 5: `<v Adam Nowak>It's it has started, right?</v>`
  - Closing `</v>` present on 100% of cues examined (80 lines)
- [x] **AC-017:** Multi-line payload handling validated against real VTT file
  - Evidence: Lines 9-10: `<v Brendan Bennett>All right. Yeah.\nSo I guess I was a little interested in</v>`
  - ~30% of cues have multi-line payloads
- [x] **AC-018:** Document errata in TDD document history (v1.1 - 2026-01-27)
- [x] **AC-019:** Document revision in agent document history (v1.1.0 - 2026-01-27)

---

## Implementation Notes

### Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| TDD-ts-parser.md | Section 1.1 VTT grammar + multi-line handling | CRITICAL |
| ts-parser.md | VTT Parsing Rules + encoding fallback | CRITICAL |

### Evidence Required

| Evidence | Type | Status |
|----------|------|--------|
| DISC-001 | Discovery document | COMPLETE |
| TDD diff | Before/after comparison | COMPLETE (v1.0 → v1.1) |
| Agent diff | Before/after comparison | COMPLETE (v1.0.0 → v1.1.0) |
| Validation | Real VTT file parsing test | COMPLETE (80 lines validated) |

### Key Patterns to Add

**VTT Voice Tag with Closing Tag:**
```
Voice Tag Pattern: <v SPEAKER_NAME>text</v>
- Opening tag: <v Speaker>
- Text content: Everything between tags
- Closing tag: </v> (MUST strip from extracted text)
- May span multiple lines

Example:
<v Brendan Bennett>All right. Yeah.
So I guess I was a little interested in</v>

Extract as:
- speaker: "Brendan Bennett"
- text: "All right. Yeah. So I guess I was a little interested in"
```

**Multi-line Cue Payload Handling:**
```
Multi-line Payloads:
- Cue payloads may span multiple lines
- Concatenate all payload lines until next cue or EOF
- Voice tag opens on first line, closes on last line
- Join lines with single space (normalize whitespace)
- Strip closing </v> tag from final line
```

**Encoding Fallback Chain:**
```
Encoding Fallback Chain (NFR-007):
1. UTF-8 (primary - check BOM first)
2. UTF-8 without BOM (try decode)
3. Windows-1252 (common Windows encoding)
4. ISO-8859-1 (Western European)
5. Latin-1 (fallback)
```

---

## Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Discovery: [DISC-001: VTT Voice Tag Parsing Gaps](./EN-007--DISC-001-vtt-voice-tag-gaps.md)
- References: [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Blocks: TASK-102, TASK-103, TASK-104

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| DISC-001 | Discovery | [EN-007--DISC-001-vtt-voice-tag-gaps.md](./EN-007--DISC-001-vtt-voice-tag-gaps.md) | COMPLETE |
| TDD-ts-parser.md (corrected) | Design Spec | TDD-ts-parser.md | COMPLETE (v1.1) |
| ts-parser.md (corrected) | Agent Definition | skills/transcript/agents/ts-parser.md | COMPLETE (v1.1.0) |
| Alignment Report | Documentation | This file (Alignment Notes section) | COMPLETE |

### Verification

- [x] TDD Section 1 requirements audited
- [x] TDD Section 2 requirements audited
- [x] TDD Section 3 schema audited
- [x] TDD Section 4-6 requirements audited
- [x] Gaps documented in DISC-001
- [x] Remediation complete (TDD v1.1, Agent v1.1.0)
- [x] Validation against real VTT file (80 lines validated)

### Alignment Notes (Findings)

| TDD Section | Finding | Action | Status |
|-------------|---------|--------|--------|
| 1.1 VTT | **CRITICAL GAP:** Closing `</v>` tags not documented | Update TDD + Agent | ✅ FIXED |
| 1.1 VTT | **MODERATE GAP:** Multi-line payloads not addressed | Update TDD + Agent | ✅ FIXED |
| 1.2 SRT | ALIGNED - comma/period both supported | None | ✅ OK |
| 1.3 Plain | ALIGNED - all 3 patterns present | None | ✅ OK |
| 2 Detection | ALIGNED - flowchart matches | None | ✅ OK |
| 3 Schema | ALIGNED - JSON schema correct | None | ✅ OK |
| 4 Timestamps | ALIGNED - 10ms precision correct | None | ✅ OK |
| 5 Encoding | **MINOR GAP:** Agent doesn't list fallbacks explicitly | Update Agent | ✅ FIXED |
| 6 Errors | ALIGNED - PAT-002 implemented | None | ✅ OK |

**Aggregate Quality Score:** 100% (8/8 sections fully aligned after remediation)

**Verdict:** ✅ ALIGNMENT COMPLETE - Ready for TASK-102

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |
| 2026-01-27 | IN_PROGRESS | Audit started; DISC-001 discovered |
| 2026-01-27 | REVISED | Added remediation scope per DISC-001 findings |
| 2026-01-27 | DONE | Phase 1-3 complete: Audit, Remediation, Validation all passed; TDD v1.1, Agent v1.1.0 |

---

*Task ID: TASK-101*
*Parent: EN-007 (ts-parser Agent Implementation)*
*Discovery: DISC-001 (VTT Voice Tag Parsing Gaps)*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
