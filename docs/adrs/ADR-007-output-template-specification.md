# ADR-007: Output Template Specification

> **PS:** FEAT-006-phase-3
> **Exploration:** e-004
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Agent:** ps-architect v2.0.0
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

The Transcript Skill produces inconsistent output when used with different LLM models. A critical discovery (2026-01-30) revealed that Claude Opus produces structurally different output compared to Claude Sonnet, despite both models claiming ADR-002 compliance.

### Problem Statement

**Observed Behavior:**
- **Sonnet (Default):** Produces correct 8-file packet per ADR-002
- **Opus:** Produces 9-file packet with missing `02-transcript.md` and added `06-timeline.md`

| File Position | ADR-002 Spec | Sonnet Output | Opus Output |
|---------------|--------------|---------------|-------------|
| 02 | transcript.md | transcript.md | action-items.md |
| 03 | speakers.md | speakers.md | decisions.md |
| 04 | action-items.md | action-items.md | questions.md |
| 05 | decisions.md | decisions.md | speakers.md |
| 06 | questions.md | questions.md | timeline.md |

**Root Cause:** The current specifications are fragmented across 4+ documents (ADR-002, ADR-003, ts-formatter.md, PLAYBOOK.md) and use "guidance" language rather than explicit requirements. Different models interpret this guidance differently.

### Background

Gap Analysis (FEAT-006-e-001) identified:
- **2 Critical Gaps:** Missing required file, non-standard file added
- **3 Major Gaps:** File numbering mismatch, ID scheme change, link target violations
- **5+ Minor Gaps:** Citation format, navigation links, index format variations

Industry Research (FEAT-006-e-003) established:
- **Pydantic validation** is the industry standard for LLM output validation
- **JSON Schema** enables model-agnostic enforcement
- **T=0.0 temperature** achieves 100% consistency on smaller models
- **Retry mechanisms** (Instructor library pattern) handle validation failures

Historical Research (FEAT-006-e-002) found:
- Templates exist but are embedded in prose, not standalone files
- Anchor formats vary between documents
- No single source of truth exists

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Must produce exactly 8 core files (numbered 00-07) | ADR-002, Gap Analysis GAP-001 |
| C-002 | Each file must stay under 35K tokens | ADR-002, NFR-001 |
| C-003 | Anchors must use `{type}-{NNN}` format | ADR-003, Historical Research |
| C-004 | Output must work with any Claude model | Model-agnostic requirement |
| C-005 | Validation must be deterministic | Industry best practice |
| C-006 | Specification must be machine-readable | Automation requirement |
| C-007 | Must support file splitting for large content | ADR-004 |
| C-008 | Must maintain bidirectional linking | ADR-003 |

### Forces

1. **Explicit vs. Implicit:** Explicit specifications are verbose but unambiguous. Implicit guidance is concise but model-dependent.

2. **Flexibility vs. Consistency:** Allowing model creativity enables "improvements" but causes incompatibility. Strict rules ensure consistency but may feel restrictive.

3. **Human vs. Machine Readable:** Prose documentation is human-friendly but not machine-enforceable. JSON Schema is machine-enforceable but less readable.

4. **Single vs. Distributed:** A single document is easy to find but may become large. Distributed specifications enable modularity but risk fragmentation.

---

## Options Considered

### Option 1: Update Existing Documents with Stricter Language

Modify ADR-002, ts-formatter.md, and SKILL.md to use MUST/MUST NOT language per RFC 2119.

**Pros:**
- Minimal changes to existing structure
- No new files to maintain
- Backwards compatible

**Cons:**
- Doesn't address the distributed specification problem
- Still relies on LLM interpretation of prose
- No machine-readable validation
- Doesn't prevent model creativity

**Fit with Constraints:**
- C-001: PARTIAL - Stricter language helps but doesn't enforce
- C-004: FAIL - Models still interpret prose differently
- C-006: FAIL - Not machine-readable

### Option 2: Create JSON Schema with Validation Layer

Create a JSON Schema that defines the exact packet structure, with a Python validation layer using Pydantic.

**Pros:**
- Machine-enforceable constraints
- Model-agnostic by design
- Enables automated retry on failure
- Industry best practice (per research)

**Cons:**
- Requires Python implementation
- Adds complexity to the pipeline
- Schema must be kept in sync with documentation

**Fit with Constraints:**
- C-001: PASS - Schema enforces exact file list
- C-004: PASS - Validation is model-agnostic
- C-006: PASS - JSON Schema is machine-readable
- C-005: PASS - Deterministic validation

### Option 3: Golden Template Specification with Validation Checklist (Recommended)

Create a single, authoritative specification document (ADR-007) that:
1. Defines the exact 8-file packet structure with explicit MUST-CREATE and MUST-NOT-CREATE rules
2. Provides complete content templates for each file type
3. Specifies citation and anchor formats precisely
4. Includes a validation checklist for ps-critic
5. Is supplemented by a JSON Schema for machine validation

**Pros:**
- Single source of truth for output format
- Human-readable AND machine-enforceable
- Explicit enumeration leaves no room for interpretation
- Validation criteria integrated with specification
- Extensible to support future file types

**Cons:**
- Longer than existing specifications
- Requires updating ts-formatter and ps-critic agents
- Initial implementation effort

**Fit with Constraints:**
- C-001: PASS - Explicit file list with numbers
- C-002: PASS - Token budgets specified per file
- C-003: PASS - Anchor format defined with regex
- C-004: PASS - Model-agnostic explicit rules
- C-005: PASS - Deterministic validation criteria
- C-006: PASS - Includes JSON Schema
- C-007: PASS - Split file naming convention
- C-008: PASS - Backlinks format specified

---

## Decision

**We will use Option 3: Golden Template Specification with Validation Checklist.**

### Rationale

1. **Eliminates Ambiguity (C-001, C-003):** Explicit enumeration of required files and formats leaves no room for model interpretation. The Opus "improvement" of adding timeline.md would be caught immediately.

2. **Model-Agnostic Design (C-004):** By defining the specification in terms of exact outputs rather than guidance, any model can produce compliant output. The specification is the contract, not the agent definition.

3. **Machine-Enforceable (C-005, C-006):** The included JSON Schema enables automated validation. ps-critic can verify compliance before accepting output.

4. **Single Source of Truth:** All format requirements consolidated in one document, reducing fragmentation and drift.

5. **Industry Alignment:** Follows Pydantic/JSON Schema validation patterns per industry research (e-003).

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 8 constraints satisfied |
| Risk Level | LOW | Proven patterns, explicit rules |
| Implementation Effort | MEDIUM | Template creation + agent updates |
| Reversibility | HIGH | Can relax rules if too strict |

---

## Specification

### 1. File Structure (8-File Packet)

#### 1.1 MUST-CREATE Files

The following files MUST be created for every transcript packet. Failure to create any of these files is a validation failure.

| Number | File Name | Description | Token Budget | Splittable |
|--------|-----------|-------------|--------------|------------|
| 00 | `00-index.md` | Navigation hub and metadata | 2,000 | NO |
| 01 | `01-summary.md` | Executive summary | 5,000 | NO |
| 02 | `02-transcript.md` | Full formatted transcript | 35,000 | YES |
| 03 | `03-speakers.md` | Speaker directory | 8,000 | YES |
| 04 | `04-action-items.md` | Action items extracted | 10,000 | YES |
| 05 | `05-decisions.md` | Decisions made | 10,000 | YES |
| 06 | `06-questions.md` | Questions (open + answered) | 10,000 | YES |
| 07 | `07-topics.md` | Topic hierarchy | 15,000 | YES |

**Total: 8 files numbered 00-07.**

#### 1.2 REQUIRED Supporting Files

| File Name | Description | Required |
|-----------|-------------|----------|
| `_anchors.json` | Anchor registry for deep linking | YES |

#### 1.3 OPTIONAL Directories

| Directory | Description | Condition |
|-----------|-------------|-----------|
| `08-mindmap/` | Mermaid mindmap files | Only if `--mindmap` flag |

#### 1.4 MUST-NOT-CREATE Files

The following files MUST NOT be created. Their presence is a validation failure.

| Forbidden File | Reason |
|----------------|--------|
| `*-timeline.md` | Not part of ADR-002 schema |
| `*-sentiment.md` | Not part of ADR-002 schema |
| `*-analysis.md` | Not part of ADR-002 schema |
| `08-*.md` | 08 is reserved for mindmap directory |
| Any unnumbered `*.md` in root | All files must be numbered 00-07 |

**Exception:** `_anchors.json` is the only non-numbered file allowed in root.

#### 1.5 File Numbering Rules

```
PATTERN: {NN}-{name}.md
WHERE:
  - NN = Two-digit number (00-07)
  - name = lowercase-hyphenated-name
  - Extension = .md (Markdown only)

VALID:
  00-index.md
  01-summary.md
  02-transcript.md
  02-transcript-01.md  (split file)
  02-transcript-02.md  (split file)

INVALID:
  0-index.md           (single digit)
  index.md             (no number)
  00-Index.md          (uppercase)
  00_index.md          (underscore)
  08-timeline.md       (08 reserved)
```

#### 1.6 Split File Naming

When a file exceeds the token budget:

```
PATTERN: {NN}-{name}-{SS}.md
WHERE:
  - NN = Original file number (02-07)
  - name = Original file name
  - SS = Split sequence (01, 02, 03, ...)

EXAMPLES:
  02-transcript-01.md
  02-transcript-02.md
  02-transcript-03.md

RULES:
  - Original file (02-transcript.md) becomes index to splits
  - Splits numbered sequentially starting from 01
  - Each split must have prev/next navigation
```

---

### 2. Content Templates

#### 2.1 00-index.md Template

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_8601_TIMESTAMP}"
packet_id: "{PACKET_ID}"
---

# {MEETING_TITLE} - Index

> **Meeting Date:** {YYYY-MM-DD}
> **Duration:** {HH:MM:SS} ({DURATION_MS} ms)
> **Participants:** {SPEAKER_COUNT}

## Quick Stats

| Metric | Count |
|--------|-------|
| Action Items | {ACTION_COUNT} |
| Decisions | {DECISION_COUNT} |
| Open Questions | {QUESTION_COUNT} |
| Topics | {TOPIC_COUNT} |

## Navigation

| # | Document | Description |
|---|----------|-------------|
| 01 | [Summary](01-summary.md) | Executive summary, key outcomes |
| 02 | [Transcript](02-transcript.md) | Full formatted transcript with timestamps |
| 03 | [Speakers](03-speakers.md) | Speaker profiles and participation |
| 04 | [Action Items](04-action-items.md) | Tasks with assignees and due dates |
| 05 | [Decisions](05-decisions.md) | Decisions made with rationale |
| 06 | [Questions](06-questions.md) | Open and answered questions |
| 07 | [Topics](07-topics.md) | Discussion topics and summaries |

## Anchor Registry

- [View anchor registry](_anchors.json)
- Total anchors: {ANCHOR_COUNT}
- Backlinks: {BACKLINK_COUNT}

---

*Generated by ts-formatter v{VERSION}*
```

#### 2.2 Entity File Template (04-07)

Apply this template to action-items, decisions, questions, and topics files:

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_8601_TIMESTAMP}"
entity_type: "{action-item|decision|question|topic}"
---

# {ENTITY_PLURAL_TITLE}

> **Extracted from:** [{PACKET_ID}](00-index.md)
> **Total:** {COUNT}
> **High Confidence (>0.85):** {HIGH_CONF_COUNT}

## {ENTITY_PLURAL_TITLE}

### {ENTITY_ID}: {ENTITY_TITLE} {#{ANCHOR_ID}}

**Details:**
- **{FIELD_1}:** {VALUE_1}
- **{FIELD_2}:** {VALUE_2}
- **Confidence:** {CONFIDENCE}
- **Source:** [{TIMESTAMP}](02-transcript.md#{SEGMENT_ANCHOR})

**Citation:**
> "{QUOTED_TEXT}"
>
> -- [{SPEAKER}](03-speakers.md#{SPEAKER_ANCHOR}), [{TIMESTAMP}](02-transcript.md#{SEGMENT_ANCHOR})

---

## Navigation

- [Back to Index](00-index.md)
- [Previous: {PREV_FILE}]({PREV_FILE}.md)
- [Next: {NEXT_FILE}]({NEXT_FILE}.md)

---

<backlinks>
<!-- Auto-generated backlinks section -->
</backlinks>

---

*Generated by ts-formatter v{VERSION}*
```

#### 2.3 Split File Template

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_8601_TIMESTAMP}"
split_info:
  part: {N}
  total: {TOTAL}
  parent_file: "{PARENT_FILE}.md"
---

# {TITLE} (Part {N} of {TOTAL})

> **Continued from:** [{PREV_FILE}]({PREV_FILE}.md)
> **Next part:** [{NEXT_FILE}]({NEXT_FILE}.md)
> **Anchor Registry:** [_anchors.json](_anchors.json)

---

{CONTENT}

---

## Navigation

- Previous: [{PREV_FILE}]({PREV_FILE}.md)
- Next: [{NEXT_FILE}]({NEXT_FILE}.md)
- Index: [00-index.md](00-index.md)

---

*Generated by ts-formatter v{VERSION}*
```

---

### 3. Citation Format Specification

#### 3.1 Anchor ID Formats

| Entity Type | Prefix | Pattern | Regex | Examples |
|-------------|--------|---------|-------|----------|
| Segment | seg | seg-{NNN} | `^seg-\d{3}$` | seg-001, seg-042, seg-501 |
| Speaker | spk | spk-{slug} | `^spk-[a-z0-9-]+$` | spk-alice, spk-bob-smith |
| Action Item | act | act-{NNN} | `^act-\d{3}$` | act-001, act-002 |
| Decision | dec | dec-{NNN} | `^dec-\d{3}$` | dec-001, dec-002 |
| Question | que | que-{NNN} | `^que-\d{3}$` | que-001, que-002 |
| Topic | top | top-{NNN} | `^top-\d{3}$` | top-001, top-002 |

**RULES:**
- NNN = 3-digit, zero-padded (001-999)
- Slugs = lowercase, hyphen-separated
- Anchors MUST be unique within the packet

**INVALID FORMATS (Must Reject):**
- `AI-001` (wrong prefix for action items)
- `ACT-001` (uppercase not allowed)
- `action-1` (not zero-padded)
- `seg-42` (only 2 digits)

#### 3.2 Citation Link Format

**Standard Citation:**
```markdown
> "{QUOTED_TEXT}"
>
> -- [{SPEAKER}](03-speakers.md#{SPEAKER_ANCHOR}), [{TIMESTAMP}](02-transcript.md#{SEGMENT_ANCHOR})
```

**Example:**
```markdown
> "We need to finalize the API documentation by Friday."
>
> -- [Alice Smith](03-speakers.md#spk-alice-smith), [[15:23]](02-transcript.md#seg-042)
```

**RULES:**
- Quote text in blockquote with `>`
- Attribution line starts with `> -- `
- Speaker links to 03-speakers.md
- Timestamp links to 02-transcript.md
- Timestamp format: `[HH:MM]` or `[HH:MM:SS]`

**FORBIDDEN:**
- Links to `canonical-transcript.json` (file too large for LLM context)
- Inline text without speaker attribution
- Missing segment anchor reference

#### 3.3 Backlinks Section Format

```markdown
<backlinks>
Referenced in:
- [04-action-items.md#act-001](04-action-items.md#act-001) - "Assigned to Alice"
- [05-decisions.md#dec-003](05-decisions.md#dec-003) - "Alice proposed..."
</backlinks>
```

**RULES:**
- Use `<backlinks>` tag (not `## Backlinks` heading)
- Each backlink includes: file, anchor, context snippet
- Context snippet max 50 characters
- One backlink per line with `-` bullet

#### 3.4 Navigation Link Format

**Header Navigation (for entity files):**
```markdown
## Navigation

- [Back to Index](00-index.md)
- [Previous: {PREV_FILE_NAME}]({PREV_FILE}.md)
- [Next: {NEXT_FILE_NAME}]({NEXT_FILE}.md)
```

**File Sequence:**
| Current | Previous | Next |
|---------|----------|------|
| 01-summary.md | 00-index.md | 02-transcript.md |
| 02-transcript.md | 01-summary.md | 03-speakers.md |
| 03-speakers.md | 02-transcript.md | 04-action-items.md |
| 04-action-items.md | 03-speakers.md | 05-decisions.md |
| 05-decisions.md | 04-action-items.md | 06-questions.md |
| 06-questions.md | 05-decisions.md | 07-topics.md |
| 07-topics.md | 06-questions.md | 00-index.md |

---

### 4. Validation Rules

#### 4.1 File Existence Validation

```yaml
validation_rules:
  file_existence:
    - rule_id: FILE-001
      description: "All 8 core files must exist"
      check: |
        REQUIRED_FILES = [
          "00-index.md",
          "01-summary.md",
          "02-transcript.md",  # or 02-transcript-01.md if split
          "03-speakers.md",
          "04-action-items.md",
          "05-decisions.md",
          "06-questions.md",
          "07-topics.md"
        ]
        for file in REQUIRED_FILES:
          if not exists(file) and not exists_split(file):
            FAIL("Missing required file: {file}")
      severity: CRITICAL
      fail_action: REJECT

    - rule_id: FILE-002
      description: "Anchor registry must exist"
      check: exists("_anchors.json")
      severity: CRITICAL
      fail_action: REJECT

    - rule_id: FILE-003
      description: "No forbidden files present"
      check: |
        FORBIDDEN_PATTERNS = [
          "*-timeline.md",
          "*-sentiment.md",
          "*-analysis.md",
          "08-*.md"
        ]
        for pattern in FORBIDDEN_PATTERNS:
          if matches_any(pattern):
            FAIL("Forbidden file detected: {file}")
      severity: CRITICAL
      fail_action: REJECT
```

#### 4.2 Content Validation

```yaml
validation_rules:
  content_validation:
    - rule_id: CONTENT-001
      description: "YAML frontmatter required"
      check: |
        for file in packet_files:
          if not has_yaml_frontmatter(file):
            FAIL("Missing YAML frontmatter: {file}")
          if not frontmatter.schema_version:
            FAIL("Missing schema_version: {file}")
      severity: MAJOR
      fail_action: WARN

    - rule_id: CONTENT-002
      description: "Navigation section required"
      check: |
        for file in ["01-07"]:
          if not has_section("## Navigation", file):
            FAIL("Missing Navigation section: {file}")
      severity: MINOR
      fail_action: WARN

    - rule_id: CONTENT-003
      description: "Token limit respected"
      check: |
        for file in packet_files:
          if token_count(file) > 35000:
            FAIL("Token limit exceeded: {file} ({tokens} > 35000)")
      severity: CRITICAL
      fail_action: REJECT
```

#### 4.3 Anchor Validation

```yaml
validation_rules:
  anchor_validation:
    - rule_id: ANCHOR-001
      description: "Anchor format compliance"
      check: |
        VALID_PATTERNS = {
          "segment": r"^seg-\d{3}$",
          "speaker": r"^spk-[a-z0-9-]+$",
          "action": r"^act-\d{3}$",
          "decision": r"^dec-\d{3}$",
          "question": r"^que-\d{3}$",
          "topic": r"^top-\d{3}$"
        }
        for anchor in anchors:
          if not matches_pattern(anchor, VALID_PATTERNS):
            FAIL("Invalid anchor format: {anchor}")
      severity: MAJOR
      fail_action: REJECT

    - rule_id: ANCHOR-002
      description: "Anchor uniqueness"
      check: |
        if len(anchors) != len(set(anchors)):
          FAIL("Duplicate anchors detected")
      severity: CRITICAL
      fail_action: REJECT

    - rule_id: ANCHOR-003
      description: "Link resolution"
      check: |
        for link in internal_links:
          if not resolves(link):
            FAIL("Broken link: {link}")
      severity: MAJOR
      fail_action: WARN
```

#### 4.4 ps-critic Validation Checklist

Add these criteria to ps-critic agent:

```yaml
ps_critic_criteria:
  schema_compliance:
    - id: SCHEMA-001
      name: "8-File Packet Structure"
      description: "Exactly 8 core files numbered 00-07 exist"
      weight: 0.20
      pass_threshold: 1.0  # All or nothing
      check_type: FILE_EXISTS

    - id: SCHEMA-002
      name: "No Forbidden Files"
      description: "No timeline, sentiment, analysis, or 08-* files"
      weight: 0.10
      pass_threshold: 1.0
      check_type: FILE_NOT_EXISTS

    - id: SCHEMA-003
      name: "Anchor Format Compliance"
      description: "All anchors match {type}-{NNN} pattern"
      weight: 0.15
      pass_threshold: 0.95
      check_type: REGEX_MATCH

    - id: SCHEMA-004
      name: "Navigation Links Present"
      description: "All entity files have prev/next navigation"
      weight: 0.10
      pass_threshold: 0.90
      check_type: SECTION_EXISTS

    - id: SCHEMA-005
      name: "Citation Format Compliance"
      description: "Citations include speaker link and timestamp"
      weight: 0.15
      pass_threshold: 0.85
      check_type: CONTENT_PATTERN

    - id: SCHEMA-006
      name: "No Canonical JSON Links"
      description: "No links to canonical-transcript.json"
      weight: 0.10
      pass_threshold: 1.0
      check_type: CONTENT_NOT_CONTAINS

    - id: SCHEMA-007
      name: "Token Limits Respected"
      description: "All files under 35K tokens"
      weight: 0.10
      pass_threshold: 1.0
      check_type: TOKEN_COUNT

    - id: SCHEMA-008
      name: "YAML Frontmatter Present"
      description: "All files have schema_version in frontmatter"
      weight: 0.10
      pass_threshold: 0.95
      check_type: FRONTMATTER_EXISTS
```

---

### 5. Model-Agnostic Requirements

#### 5.1 Temperature Setting

**REQUIREMENT:** Use `temperature=0.0` for deterministic output.

**Rationale:** IBM research (arXiv:2511.07585) shows T=0.0 achieves 100% output consistency on structured tasks for smaller models.

#### 5.2 Retry Strategy

When validation fails:

```
RETRY ALGORITHM:
1. Run ts-formatter
2. Validate output using rules above
3. IF validation FAILS:
   a. Capture validation errors
   b. Add to context: "Validation failed: {errors}"
   c. Re-run ts-formatter with corrected instructions
   d. Repeat up to MAX_RETRIES (3) times
4. IF still fails after MAX_RETRIES:
   a. Log error with full context
   b. Return partial output with warnings
   c. Require human review
```

#### 5.3 Explicit Instructions for ts-formatter

Add to ts-formatter agent definition:

```markdown
## CRITICAL OUTPUT RULES (MUST FOLLOW)

**MUST CREATE (exactly these 8 files):**
1. `00-index.md`
2. `01-summary.md`
3. `02-transcript.md`
4. `03-speakers.md`
5. `04-action-items.md`
6. `05-decisions.md`
7. `06-questions.md`
8. `07-topics.md`

**MUST NOT CREATE:**
- timeline.md (ANY file with "timeline" in name)
- sentiment.md (ANY file with "sentiment" in name)
- analysis.md (ANY file with "analysis" in name)
- Any file starting with 08, 09, 10, etc.

**ANCHOR FORMAT (MUST USE):**
- seg-NNN (e.g., seg-001, NOT segment-001)
- act-NNN (e.g., act-001, NOT AI-001 or ACT-001)
- dec-NNN (e.g., dec-001, NOT decision-001)
- que-NNN (e.g., que-001, NOT question-001)
- top-NNN (e.g., top-001, NOT topic-001)
- spk-{slug} (e.g., spk-alice-smith)

**LINK TARGETS (MUST NOT LINK TO):**
- canonical-transcript.json (file too large)
```

---

### 6. JSON Schema

#### 6.1 Packet Structure Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://jerry.dev/schemas/transcript-packet-v1.0.json",
  "title": "Transcript Packet Structure",
  "description": "JSON Schema for validating transcript skill output packets",
  "type": "object",
  "required": [
    "packet_id",
    "files",
    "anchors"
  ],
  "properties": {
    "packet_id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$"
    },
    "files": {
      "type": "object",
      "required": [
        "00-index.md",
        "01-summary.md",
        "02-transcript.md",
        "03-speakers.md",
        "04-action-items.md",
        "05-decisions.md",
        "06-questions.md",
        "07-topics.md"
      ],
      "additionalProperties": false,
      "patternProperties": {
        "^0[0-7]-[a-z-]+\\.md$": {
          "type": "object",
          "required": ["exists", "token_count"],
          "properties": {
            "exists": { "type": "boolean", "const": true },
            "token_count": { "type": "integer", "maximum": 35000 },
            "has_frontmatter": { "type": "boolean" },
            "has_navigation": { "type": "boolean" }
          }
        },
        "^0[2-7]-[a-z-]+-\\d{2}\\.md$": {
          "type": "object",
          "description": "Split file pattern",
          "properties": {
            "exists": { "type": "boolean", "const": true },
            "token_count": { "type": "integer", "maximum": 35000 },
            "split_part": { "type": "integer", "minimum": 1 },
            "split_total": { "type": "integer", "minimum": 2 }
          }
        }
      }
    },
    "anchors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "file"],
        "properties": {
          "id": {
            "type": "string",
            "oneOf": [
              { "pattern": "^seg-\\d{3}$" },
              { "pattern": "^spk-[a-z0-9-]+$" },
              { "pattern": "^act-\\d{3}$" },
              { "pattern": "^dec-\\d{3}$" },
              { "pattern": "^que-\\d{3}$" },
              { "pattern": "^top-\\d{3}$" }
            ]
          },
          "type": {
            "type": "string",
            "enum": ["segment", "speaker", "action", "decision", "question", "topic"]
          },
          "file": {
            "type": "string",
            "pattern": "^0[0-7]-[a-z-]+(-\\d{2})?\\.md$"
          }
        }
      }
    },
    "forbidden_files": {
      "type": "array",
      "maxItems": 0,
      "description": "Must be empty - no forbidden files allowed"
    }
  }
}
```

---

## Consequences

### Positive Consequences

1. **Model Agnosticism:** Any Claude model (Sonnet, Opus, Haiku) will produce identical file structures, eliminating the observed inconsistency.

2. **Automated Validation:** ps-critic can programmatically verify compliance using the validation rules, catching errors before they reach users.

3. **Clear Contracts:** ts-formatter has unambiguous requirements, reducing cognitive load and interpretation errors.

4. **Deterministic Output:** T=0.0 temperature + explicit rules = reproducible results across sessions.

5. **Debugging Clarity:** When validation fails, specific rule IDs indicate exactly what went wrong.

### Negative Consequences

1. **Reduced Flexibility:** Models cannot "improve" the output format. Genuine enhancements require ADR amendment.

2. **Documentation Overhead:** This specification is significantly longer than existing prose documentation.

3. **Migration Required:** Existing ts-formatter and ps-critic agents must be updated.

### Neutral Consequences

1. **Template Verbosity:** Explicit templates are longer but clearer.

2. **Validation Latency:** Post-generation validation adds processing time (estimated <100ms).

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Over-restrictive rules block valid use cases | LOW | MEDIUM | Include exception mechanism via ADR amendment |
| JSON Schema drift from prose spec | MEDIUM | LOW | Generate schema from authoritative prose |
| Validation false positives | LOW | LOW | Extensive testing with golden outputs |
| Retry loop exhaustion | LOW | MEDIUM | Human review fallback after 3 retries |

---

## Implementation

### Action Items

| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Update ts-formatter.md with explicit MUST-CREATE/MUST-NOT-CREATE lists | ps-architect | 2026-02-01 | PENDING |
| 2 | Add schema compliance criteria to ps-critic.md | ps-architect | 2026-02-01 | PENDING |
| 3 | Create JSON Schema file at `skills/transcript/schemas/packet-structure.schema.json` | ps-architect | 2026-02-01 | PENDING |
| 4 | Update SKILL.md with model-agnostic requirements section | ps-architect | 2026-02-02 | PENDING |
| 5 | Create validation test suite with golden outputs | ps-validator | 2026-02-03 | PENDING |
| 6 | Run multi-model regression tests (Sonnet, Opus, Haiku) | ps-validator | 2026-02-03 | PENDING |
| 7 | Update PLAYBOOK.md with validation workflow | ps-architect | 2026-02-02 | PENDING |
| 8 | Document migration path from current output to ADR-007 spec | ps-architect | 2026-02-01 | PENDING |

### Validation Criteria

1. **Cross-Model Consistency:** Sonnet and Opus produce identical file structures
2. **Anchor Compliance:** 100% of anchors match specified patterns
3. **Zero Forbidden Files:** No timeline.md, sentiment.md, or 08-*.md in any output
4. **Navigation Complete:** All entity files (01-07) have prev/next/index navigation
5. **Citation Compliance:** >90% of citations link to transcript with speaker attribution
6. **Token Limits:** 100% of files under 35K tokens
7. **Regression Pass:** All existing test cases pass with new specification

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-002 | CONSTRAINS | Defines 8-file packet structure (refined here) |
| ADR-003 | CONSTRAINS | Defines anchor naming (standardized here) |
| ADR-004 | CONSTRAINS | Defines file splitting (validated here) |
| ADR-005 | RELATED_TO | Agent implementation affected |
| ADR-006 | RELATED_TO | Mindmap pipeline unaffected by core 8 files |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | FEAT-006-e-001-gap-analysis.md | Analysis | Identified the Sonnet/Opus inconsistency |
| 2 | FEAT-006-e-002-historical-research.md | Research | Found fragmented template specifications |
| 3 | FEAT-006-e-003-industry-research.md | Research | Pydantic/JSON Schema best practices |
| 4 | ADR-002-artifact-structure.md | ADR | Original 8-file packet definition |
| 5 | ADR-003-bidirectional-linking.md | ADR | Original anchor naming conventions |
| 6 | ts-formatter.md | Agent | Current formatter agent definition |
| 7 | Pydantic LLM Guide | Industry | https://pydantic.dev/articles/llm-intro |
| 8 | IBM Output Drift Research | Research | https://arxiv.org/abs/2511.07585 |
| 9 | Guardrails AI | Industry | https://github.com/guardrails-ai/guardrails |
| 10 | RFC 2119 | Standard | MUST/SHOULD/MAY terminology |

---

## Appendix A: Anchor ID Examples

### Valid Anchors

| Anchor | Type | File |
|--------|------|------|
| `seg-001` | Segment | 02-transcript.md |
| `seg-042` | Segment | 02-transcript.md |
| `seg-501` | Segment | 02-transcript-02.md |
| `spk-alice-smith` | Speaker | 03-speakers.md |
| `spk-bob` | Speaker | 03-speakers.md |
| `act-001` | Action Item | 04-action-items.md |
| `dec-003` | Decision | 05-decisions.md |
| `que-002` | Question | 06-questions.md |
| `top-005` | Topic | 07-topics.md |

### Invalid Anchors (MUST REJECT)

| Invalid Anchor | Reason | Correct Form |
|----------------|--------|--------------|
| `AI-001` | Wrong prefix | `act-001` |
| `ACT-001` | Uppercase | `act-001` |
| `action-1` | Not zero-padded | `act-001` |
| `segment-042` | Wrong prefix | `seg-042` |
| `speaker-alice` | Wrong prefix | `spk-alice` |
| `dec-1` | Only 1 digit | `dec-001` |
| `que-1234` | Too many digits | `que-999` max |

---

## Appendix B: Complete File Structure Example

```
2026-01-30-certificate-architecture/
├── 00-index.md                 # REQUIRED
├── 01-summary.md               # REQUIRED
├── 02-transcript.md            # REQUIRED (or split)
├── 02-transcript-01.md         # OPTIONAL (split part 1)
├── 02-transcript-02.md         # OPTIONAL (split part 2)
├── 03-speakers.md              # REQUIRED
├── 04-action-items.md          # REQUIRED
├── 05-decisions.md             # REQUIRED
├── 06-questions.md             # REQUIRED
├── 07-topics.md                # REQUIRED
├── 08-mindmap/                 # OPTIONAL (only if --mindmap)
│   ├── mindmap.mmd
│   └── mindmap.svg
├── _anchors.json               # REQUIRED
├── canonical-transcript.json   # Parser output (DO NOT LINK)
├── chunks/                     # Parser output
│   ├── chunk-001.json
│   └── chunk-002.json
├── extraction-report.json      # Extractor output
├── index.json                  # Parser output
└── quality-review.md           # Critic output

Files NOT ALLOWED:
- 06-timeline.md               (FORBIDDEN)
- 09-sentiment.md              (FORBIDDEN)
- 10-analysis.md               (FORBIDDEN)
- timeline.md                  (FORBIDDEN - any timeline file)
```

---

## Appendix C: Migration Path

### Existing Output Migration

For existing packets that don't comply with ADR-007:

1. **Validation Run:** Execute validation rules against existing output
2. **Gap Report:** Generate list of non-compliant files/anchors
3. **Remediation Options:**
   a. Regenerate packet with updated ts-formatter
   b. Manual correction for minor issues
   c. Accept non-compliance with documentation

### Deprecation Timeline

| Date | Action |
|------|--------|
| 2026-02-01 | ADR-007 published as PROPOSED |
| 2026-02-03 | Validation tests complete |
| 2026-02-05 | ts-formatter updated |
| 2026-02-07 | ADR-007 status → ACCEPTED |
| 2026-03-01 | All new packets must comply |
| 2026-04-01 | Non-compliant packets deprecated |

---

**Generated by:** ps-architect v2.0.0
**Template Version:** 1.0 (Michael Nygard ADR Format)
**Quality Review:** PENDING
**Constitutional Compliance:** P-002 (file persistence), P-004 (provenance documented), P-011 (evidence-based)
