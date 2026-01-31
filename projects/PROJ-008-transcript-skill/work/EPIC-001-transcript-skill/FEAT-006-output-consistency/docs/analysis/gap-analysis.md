# Gap Analysis: Transcript Skill Output Consistency

> **PS ID:** FEAT-006-phase-0
> **Entry ID:** e-001
> **Topic:** Gap Analysis - Transcript Skill Output Consistency
> **Author:** ps-analyst v2.0.0
> **Date:** 2026-01-31
> **Status:** Complete

---

## Executive Summary

This gap analysis compares two transcript skill outputs generated from the same source meeting:

| Attribute | Input A (Sonnet/Default) | Input B (Opus) |
|-----------|--------------------------|----------------|
| **Path** | `2026-01-30-certificate-architecture/` | `2026-01-30-certificate-architecture-opus-v2/` |
| **Model** | Sonnet (Default) | Opus |
| **Status** | CORRECT (Reference) | INCORRECT (Divergent) |
| **Quality Score** | 0.92 | 0.996 |

**Critical Finding:** The Opus model produces structurally different output that violates the ADR-002 8-file packet schema despite reporting a higher quality score. This indicates the model is evaluating its own non-compliant output favorably.

### Impact Assessment

| Severity | Count | Description |
|----------|-------|-------------|
| **Critical** | 2 | Missing required file (02-transcript.md), incorrect file numbering |
| **Major** | 3 | Added non-standard file (06-timeline.md), different ID schemes, different index format |
| **Minor** | 5+ | Navigation links, citation formats, content organization |

---

## Document Audience (Triple-Lens)

### L0 (ELI5) - What's Wrong?

Imagine you have a recipe book where every recipe follows the same format: ingredients first, then steps, then tips. The "Sonnet Chef" follows this format perfectly. But the "Opus Chef" decided to reorganize recipes their own way - skipping the ingredients section and adding a "history" section that wasn't supposed to be there.

**The problem:** When someone reads an Opus recipe expecting the standard format, they can't find the ingredients (02-transcript.md) because it doesn't exist. The instructions are also numbered differently (action-items is 02 not 04), so automation breaks.

**Root cause:** The Opus model wasn't given strict enough instructions about following the exact format, so it "improved" things in ways that break compatibility.

### L1 (Engineer) - Technical Details

The transcript skill defines an 8-file packet structure in ADR-002:

```
Expected (ADR-002):           Actual (Opus):
00-index.md                   00-index.md        (format differs)
01-summary.md                 01-summary.md      (format differs)
02-transcript.md  <-- MISSING 02-action-items.md (wrong file!)
03-speakers.md                03-decisions.md    (wrong position)
04-action-items.md            04-questions.md    (wrong position)
05-decisions.md               05-speakers.md     (wrong position)
06-questions.md               06-timeline.md     <-- EXTRA FILE!
07-topics.md                  07-topics.md       (same position)
```

**Key technical gaps:**
1. **Missing `02-transcript.md`** - The full formatted transcript is a required file
2. **Added `06-timeline.md`** - Not part of the ADR-002 schema
3. **File numbering mismatch** - Breaks any automation expecting specific file positions
4. **ID scheme change** - Opus uses `ACT-001`, Sonnet uses `AI-001`
5. **Citation format change** - Opus uses `[seg-xxx](canonical-transcript.json#seg-xxx)`, Sonnet uses inline quotes

### L2 (Architect) - Design Implications

**One-Way Door Decision Impact:**

The transcript skill's 8-file packet structure (ADR-002) is a contract with downstream consumers. Changes to this structure constitute a **breaking change** requiring version increment.

**Root Cause Analysis (Ishikawa):**

```
                     ┌─────────────────────────────────────────────┐
                     │   Output Inconsistency Between Models       │
                     └─────────────────────────────────────────────┘
                                          ▲
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
    ┌─────┴─────┐                   ┌─────┴─────┐                   ┌─────┴─────┐
    │   Model   │                   │  Process  │                   │  Schema   │
    │  Behavior │                   │   Gaps    │                   │  Gaps     │
    └───────────┘                   └───────────┘                   └───────────┘
         │                               │                               │
         ├── No model-specific tests     ├── ts-formatter lacks          ├── ADR-002 not
         ├── Model creativity varies     │   explicit file list          │   machine-readable
         ├── Opus more "opinionated"     ├── No file existence           ├── No schema validation
         └── No guardrails on output     │   post-check                  │   hook
                                         └── No file order enforcement   └── No "must include"
                                                                             list in SKILL.md
```

**Design Tradeoffs:**

| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| Hardcode file list in ts-formatter | Guaranteed compliance | Less flexible | **YES** |
| Schema validation post-hook | Catches errors | Doesn't prevent | YES |
| Model-specific prompts | Optimized per model | Maintenance burden | Maybe |
| Remove model flexibility | Consistent output | Loses capability | No |

---

## Methodology

### 5W2H Framework

| Question | Answer |
|----------|--------|
| **What** | Inconsistent file structure between model outputs |
| **Why** | ts-formatter agent lacks explicit file enumeration requirement |
| **Who** | Affects all transcript skill users expecting ADR-002 compliance |
| **When** | Discovered 2026-01-30, documented 2026-01-31 |
| **Where** | ts-formatter agent output phase |
| **How** | Opus model "improved" structure based on its interpretation |
| **How Much** | 2 critical files affected, 100% of file positions shifted |

### Pareto Analysis (80/20)

The **20% of issues causing 80% of impact**:

1. **Missing `02-transcript.md`** (40% of impact)
   - Breaks automation expecting this file
   - Loses full transcript accessibility

2. **Added `06-timeline.md`** (30% of impact)
   - Confuses consumers expecting 8 files
   - Shifts all subsequent file numbers

3. **File numbering mismatch** (10% of impact)
   - Breaks hardcoded file references
   - Requires dynamic discovery instead

**Remaining 20% of issues:**
- Citation format differences
- ID scheme differences (ACT vs AI)
- Index format differences
- Navigation link differences

---

## Detailed Findings

### 1. File Structure Comparison

#### 1.1 Directory Listing

**Input A (Sonnet/Default) - CORRECT:**
```
00-index.md           (1,506 bytes)
01-summary.md         (2,698 bytes)
02-transcript.md      (32,795 bytes)  <-- REQUIRED FILE
03-speakers.md        (4,595 bytes)
04-action-items.md    (4,829 bytes)
05-decisions.md       (6,775 bytes)
06-questions.md       (5,801 bytes)
07-topics.md          (8,435 bytes)
08-mindmap/           (directory)
```

**Input B (Opus) - INCORRECT:**
```
00-index.md           (3,039 bytes)   <-- Different format
01-summary.md         (3,807 bytes)   <-- Different format
02-action-items.md    (5,318 bytes)   <-- WRONG FILE (should be transcript)
03-decisions.md       (8,128 bytes)   <-- Wrong position
04-questions.md       (7,259 bytes)   <-- Wrong position
05-speakers.md        (7,382 bytes)   <-- Wrong position
06-timeline.md        (7,813 bytes)   <-- EXTRA FILE (not in spec)
07-topics.md          (13,691 bytes)  <-- Same position
08-mindmap/           (directory)
```

#### 1.2 File Presence Matrix

| File | ADR-002 Required | Sonnet | Opus | Gap |
|------|------------------|--------|------|-----|
| 00-index.md | YES | PRESENT | PRESENT | Format differs |
| 01-summary.md | YES | PRESENT | PRESENT | Format differs |
| 02-transcript.md | YES | PRESENT | **MISSING** | **CRITICAL** |
| 03-speakers.md | YES | PRESENT | Renamed to 05 | Position shift |
| 04-action-items.md | YES | PRESENT | Renamed to 02 | Position shift |
| 05-decisions.md | YES | PRESENT | Renamed to 03 | Position shift |
| 06-questions.md | YES | PRESENT | Renamed to 04 | Position shift |
| 07-topics.md | YES | PRESENT | PRESENT | Same position |
| 06-timeline.md | NO | N/A | **ADDED** | **Non-compliant** |

### 2. Content Format Analysis

#### 2.1 Index File (00-index.md)

**Sonnet Format:**
```markdown
# Certificate Architecture Meeting - Index

> **Meeting Date:** 2026-01-30
> **Duration:** 32:02 (1,922,219 ms)
> **Participants:** 7

## Navigation
| # | Document | Description |
|---|----------|-------------|
| 01 | [Summary](01-summary.md) | Executive summary, key outcomes... |
| 02 | [Transcript](02-transcript.md) | Full formatted transcript... |
...
```

**Opus Format:**
```markdown
# Certificate Architecture Discussion - Index

> **Navigation Hub** | Generated: 2026-01-31

## Meeting Overview
| Property | Value |
|----------|-------|
| **Packet ID** | `transcript-certificate-architecture-20260130` |
...

## Document Navigation
| Document | Description |
|----------|-------------|
| [01-summary.md](01-summary.md) | Executive summary... |
| [02-action-items.md](02-action-items.md) | 5 action items... |  <-- WRONG!
...
```

**Gaps Identified:**
- Different title format ("Meeting" vs "Discussion")
- Different metadata structure (blockquote vs table)
- Missing transcript reference in navigation
- Added elements (Packet ID, Schema Compliance Checklist)

#### 2.2 Action Items Citations

**Sonnet Format (CORRECT):**
```markdown
### AI-001: Chase Registration Team for Resourcing {#ai-001}

**Citation:**
> *[15:58] Adam Nowak:* "Great. Thank you very much..."
```

**Opus Format (INCORRECT):**
```markdown
### ACT-001: Registration Team Resourcing

#### Citation

> "Great. Thank you very much..."

- **Segment**: [seg-241](canonical-transcript.json#seg-241)
- **Timestamp**: [15:59]
- **Chunk**: chunk-002
```

**Gaps Identified:**
- ID scheme: `AI-001` (Sonnet) vs `ACT-001` (Opus)
- Citation format: Inline speaker + timestamp vs separated metadata
- Link format: Inline quote vs separate segment reference
- Anchor format: `{#ai-001}` (Sonnet) vs none (Opus)

#### 2.3 Navigation Links

**Sonnet Format:**
```markdown
## Navigation

- [Back to Index](00-index.md)
- [Previous: Speakers](03-speakers.md)
- [Next: Decisions](05-decisions.md)
```

**Opus Format:**
```markdown
[Back to Index](00-index.md)
```

**Gap:** Opus lacks Previous/Next navigation links, breaking linear document traversal.

### 3. Link Validation

#### 3.1 Sonnet Links (All Valid)

| Link | Target | Status |
|------|--------|--------|
| `[Transcript](02-transcript.md)` | 02-transcript.md | EXISTS |
| `[Speakers](03-speakers.md)` | 03-speakers.md | EXISTS |
| `[Action Items](04-action-items.md)` | 04-action-items.md | EXISTS |

#### 3.2 Opus Links (Several Invalid)

| Link | Target | Status | Issue |
|------|--------|--------|-------|
| `[02-action-items.md](02-action-items.md)` | 02-action-items.md | EXISTS | Wrong file at this position |
| `[seg-241](canonical-transcript.json#seg-241)` | canonical-transcript.json | EXISTS | Links to forbidden large file |
| `(Previous: ...)` | N/A | MISSING | No prev/next navigation |

**Critical Issue:** Opus citation links reference `canonical-transcript.json`, which is a 930KB file that should NOT be read by LLM agents. The SKILL.md explicitly forbids reading this file.

### 4. Extraction Report Comparison

| Metric | Sonnet | Opus | Match |
|--------|--------|------|-------|
| Speakers | 7 | 7 | YES |
| Action Items | 5 | 5 | YES |
| Decisions | 6 | 6 | YES |
| Questions | 6 | 8 | **NO** |
| Topics | 6 | 6 | YES |
| Total Segments | 501 | 501 | YES |

**Gap:** Opus extracted 8 questions vs Sonnet's 6. This suggests different extraction criteria or additional rhetorical question capture.

---

## Gap Matrix

| Category | Gap ID | Severity | Sonnet (Correct) | Opus (Incorrect) | Impact |
|----------|--------|----------|------------------|------------------|--------|
| **File Structure** | GAP-001 | CRITICAL | 02-transcript.md exists | MISSING | Breaks transcript access |
| **File Structure** | GAP-002 | CRITICAL | 8 files only | 9 files (timeline added) | Schema violation |
| **File Numbering** | GAP-003 | MAJOR | 02=transcript | 02=action-items | Automation breakage |
| **File Numbering** | GAP-004 | MAJOR | 03=speakers | 03=decisions | Position mismatch |
| **ID Scheme** | GAP-005 | MAJOR | AI-001 format | ACT-001 format | Cross-reference breaks |
| **Citation Format** | GAP-006 | MINOR | Inline quotes | Separated metadata | Style inconsistency |
| **Navigation** | GAP-007 | MINOR | Prev/Index/Next | Index only | User experience |
| **Link Target** | GAP-008 | MAJOR | Inline anchors | canonical-json links | Links to forbidden file |
| **Index Format** | GAP-009 | MINOR | Simple blockquote | Complex tables | Style drift |
| **Extraction** | GAP-010 | MINOR | 6 questions | 8 questions | Count mismatch |

---

## Root Cause Hypothesis

### Primary Cause: Missing Explicit File Enumeration in ts-formatter

The ts-formatter agent definition specifies a packet structure but does not explicitly enumerate the **exact file list** that must be created. The agent is told to create "8 files" but the list is presented as examples rather than requirements.

**Evidence from ts-formatter.md:**
```markdown
Create the following files in the packet directory:
├── 00-index.md          # Navigation hub (~2K tokens)
├── 01-summary.md        # Executive summary (~5K tokens)
├── 02-transcript.md     # Full transcript (may split)
...
```

This is presented as guidance, not a hard requirement. Different models may interpret this differently.

### Secondary Cause: Model Creativity Variance

Opus is a more capable model that tends to "improve" on instructions when it perceives opportunities. This is beneficial for many tasks but harmful for strict schema compliance.

**Observed Opus behaviors:**
1. Added `06-timeline.md` because it seemed useful
2. Changed ID scheme to `ACT-001` (more explicit than `AI-001`)
3. Enhanced index with schema compliance checklist
4. Added segment reference metadata to citations

These are all "improvements" from Opus's perspective but violations from the schema's perspective.

### Tertiary Cause: Insufficient Post-Validation

The ps-critic agent evaluates quality but does not validate schema compliance. The Opus output received a 0.996 quality score despite violating the 8-file schema.

**Evidence:**
- ps-critic evaluates content quality (citations, confidence, etc.)
- ps-critic does NOT validate file existence or naming
- No automated schema validation hook exists

---

## Recommendations

### Immediate (P0 - Blocking)

1. **R-001: Add explicit file list to ts-formatter**
   - Create a MUST-CREATE file list with exact names
   - Add validation step that verifies all files exist
   - Fail the pipeline if any required file is missing

2. **R-002: Add schema validation to ps-critic**
   - New criterion: `FILE-001 - Required Files Present`
   - Check for exactly 8 core files + optional mindmap directory
   - Hard fail if missing required files

3. **R-003: Standardize ID schemes in SKILL.md**
   - Define exact ID format: `AI-nnn` for action items, `DEC-nnn` for decisions
   - Add to ts-formatter agent definition
   - Include in ps-critic validation

### Short-Term (P1 - This Sprint)

4. **R-004: Create machine-readable ADR-002 schema**
   - JSON Schema for packet structure
   - Automated validation tool
   - Integration with CI/CD

5. **R-005: Add model-specific test cases**
   - Run transcript skill with each supported model
   - Compare outputs against reference
   - Flag deviations as test failures

6. **R-006: Fix citation link targets**
   - Links should reference packet files (02-transcript.md#seg-xxx)
   - NOT canonical-transcript.json (forbidden file)

### Long-Term (P2 - Future Enhancements)

7. **R-007: Model-specific prompt tuning**
   - Investigate if Opus needs stronger constraint language
   - Consider model-specific agent variants

8. **R-008: Add regression test suite**
   - Golden output comparison tests
   - Structural compliance tests
   - Cross-model consistency tests

---

## References

| Reference | Path |
|-----------|------|
| ADR-002 | `skills/transcript/docs/ADR-002-packet-structure.md` |
| ts-formatter Agent | `skills/transcript/agents/ts-formatter.md` |
| SKILL.md | `skills/transcript/SKILL.md` |
| Input A (Sonnet) | `Downloads/chats/2026-01-30-certificate-architecture/` |
| Input B (Opus) | `Downloads/chats/2026-01-30-certificate-architecture-opus-v2/` |

---

## Appendix A: Full File Comparison

### A.1 Input A Files (Sonnet/Default)

```
-rw-r--r--  1,506 bytes  00-index.md
-rw-r--r--  2,698 bytes  01-summary.md
-rw-r--r-- 32,795 bytes  02-transcript.md
-rw-r--r--  4,595 bytes  03-speakers.md
-rw-r--r--  4,829 bytes  04-action-items.md
-rw-r--r--  6,775 bytes  05-decisions.md
-rw-r--r--  5,801 bytes  06-questions.md
-rw-r--r--  8,435 bytes  07-topics.md
drwxr-xr-x       128     08-mindmap/
-rw-r--r--135,677 bytes  canonical-transcript.json
drwxr-xr-x       160     chunks/
-rw-r--r-- 13,535 bytes  extraction-report.json
-rw-r--r--  1,988 bytes  index.json
-rw-r--r-- 12,753 bytes  quality-review.md
```

### A.2 Input B Files (Opus)

```
-rw-r--r--  3,039 bytes  00-index.md
-rw-r--r--  3,807 bytes  01-summary.md
-rw-r--r--  5,318 bytes  02-action-items.md    <-- WRONG
-rw-r--r--  8,128 bytes  03-decisions.md       <-- WRONG
-rw-r--r--  7,259 bytes  04-questions.md       <-- WRONG
-rw-r--r--  7,382 bytes  05-speakers.md        <-- WRONG
-rw-r--r--  7,813 bytes  06-timeline.md        <-- EXTRA
-rw-r--r-- 13,691 bytes  07-topics.md
drwxr-xr-x       128     08-mindmap/
-rw-r--r--135,677 bytes  canonical-transcript.json
drwxr-xr-x       160     chunks/
-rw-r--r-- 18,221 bytes  extraction-report.json
-rw-r--r--  1,988 bytes  index.json
-rw-r--r--  8,394 bytes  quality-review.md
```

---

## Appendix B: Quality Review Comparison

| Metric | Sonnet Review | Opus Review | Note |
|--------|---------------|-------------|------|
| Quality Score | 0.92 | 0.996 | Opus scores higher despite violations |
| Status | PASS | PASS | Both pass threshold |
| Criteria Evaluated | N/A | 12 | Different review structure |
| File Compliance | Checked | NOT CHECKED | Gap in Opus review |

**Key Observation:** The Opus quality review does NOT validate file structure compliance, allowing the schema violation to pass undetected.

---

*Generated by ps-analyst v2.0.0*
*Analysis Date: 2026-01-31*
*Frameworks Applied: 5W2H, Ishikawa, Pareto Analysis*
