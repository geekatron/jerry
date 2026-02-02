# Transcript Skill Critic Extension

> **Version:** 1.0.0
> **Purpose:** Mindmap validation criteria for ps-critic when evaluating transcript skill outputs
> **Source:** ADR-006 Section 5.5 (ps-critic Integration)
> **Created:** 2026-01-30
> **Task:** EN-024:TASK-245

---

## Overview

This document extends ps-critic's evaluation criteria for transcript skill outputs that include mindmap artifacts. When mindmaps are present in the packet (default behavior unless `--no-mindmap` is used), ps-critic applies these additional validation criteria.

### L0 (ELI5): The Quality Inspector's Extra Checklist

When the Quality Inspector (ps-critic) reviews a transcript packet that includes mind maps, they get an extra checklist:
- **For Mermaid diagrams:** Check the diagram code is correct and links work
- **For ASCII art:** Make sure it fits on screen (80 characters) and has a legend

This checklist is only used when mindmaps exist in the packet.

### L1 (Software Engineer): Conditional Validation

```yaml
# Validation is conditional on mindmap presence
IF file_exists("08-mindmap/mindmap.mmd"):
    APPLY Mermaid criteria MM-001 through MM-007
ENDIF

IF file_exists("08-mindmap/mindmap.ascii.txt"):
    APPLY ASCII criteria AM-001 through AM-005
ENDIF
```

### L2 (Architect): Quality Score Composition

When mindmaps are present, the quality score composition changes:

| Condition | Core Packet Weight | Mindmap Weight |
|-----------|-------------------|----------------|
| Mindmaps present (default) | 85% | 15% |
| Mindmaps absent (`--no-mindmap`) | 100% | N/A |

This prevents quality score regression when users opt-out of mindmap generation.

---

## Mermaid Mindmap Criteria (MM-*)

These criteria apply when `08-mindmap/mindmap.mmd` exists.

### MM-001: Valid Mermaid Mindmap Syntax

| Attribute | Value |
|-----------|-------|
| **ID** | MM-001 |
| **Severity** | ERROR |
| **Weight** | 0.20 |
| **Description** | The mindmap file must contain valid Mermaid mindmap syntax |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | File starts with `mindmap` keyword, valid indentation, parseable |
| 0.5 | Minor syntax issues that don't prevent rendering |
| 0.0 | Invalid syntax, fails to parse, wrong diagram type |

**Evidence to Check:**
```
- File begins with "mindmap" keyword on first line
- Indentation is consistent (2 spaces per level)
- All nodes have valid content (no empty parentheses)
- No syntax errors when processed by mermaid-cli (conceptual check)
```

---

### MM-002: Root Node Present and Labeled

| Attribute | Value |
|-----------|-------|
| **ID** | MM-002 |
| **Severity** | ERROR |
| **Weight** | 0.15 |
| **Description** | Mindmap must have exactly one root node with meeting title |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | Single root node with `root((Title))` format, title matches meeting |
| 0.7 | Root node present but title doesn't match meeting exactly |
| 0.0 | No root node, multiple roots, or malformed root syntax |

**Evidence to Check:**
```
- Pattern: root((Meeting Title))
- Exactly one occurrence of "root(("
- Title relates to meeting content
```

---

### MM-003: Deep Links Use Correct Anchor Format

| Attribute | Value |
|-----------|-------|
| **ID** | MM-003 |
| **Severity** | ERROR |
| **Weight** | 0.20 |
| **Description** | Entity nodes must have deep links using ADR-003 anchor format |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | All entity nodes have links matching `(#xxx-NNN)` format |
| 0.7 | 80%+ of entities have correct link format |
| 0.5 | 50-79% of entities have correct link format |
| 0.0 | Less than 50% have links or links use wrong format |

**Valid Anchor Patterns (ADR-003):**
```
- Action items: (#act-001), (#act-002), etc.
- Decisions: (#dec-001), (#dec-002), etc.
- Questions: (#que-001), (#que-002), etc.
- Topics: (#top-001), (#top-002), etc.
- Speakers: (#spk-alice), (#spk-bob), etc.
```

---

### MM-004: Topic Hierarchy Matches Extraction Report

| Attribute | Value |
|-----------|-------|
| **ID** | MM-004 |
| **Severity** | WARNING |
| **Weight** | 0.15 |
| **Description** | Topics in mindmap should match extraction report topics |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | All topics from extraction report appear in mindmap |
| 0.8 | 90%+ topic coverage |
| 0.6 | 70-89% topic coverage |
| 0.3 | 50-69% topic coverage |
| 0.0 | Less than 50% coverage or major discrepancies |

**Verification Method:**
```
Compare extraction-report.json topics[] with mindmap topic nodes
Allow for truncation in mindmap (long titles may be shortened)
```

---

### MM-005: Entity Symbols Present

| Attribute | Value |
|-----------|-------|
| **ID** | MM-005 |
| **Severity** | WARNING |
| **Weight** | 0.10 |
| **Description** | Entity nodes should have appropriate visual symbols |

**Expected Symbols:**
| Entity Type | Symbol | Example |
|-------------|--------|---------|
| Action Item | → | `→ Send report to team` |
| Decision | ! | `! Approved Q4 budget` |
| Question | ? | `? When is the deadline?` |
| Topic | * | `* Budget Review` |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | All entity types have appropriate symbols |
| 0.7 | Most entities (80%+) have symbols |
| 0.3 | Some symbols present but inconsistent |
| 0.0 | No symbols or wrong symbols used |

---

### MM-006: Maximum Topic Overflow Handling

| Attribute | Value |
|-----------|-------|
| **ID** | MM-006 |
| **Severity** | WARNING |
| **Weight** | 0.10 |
| **Description** | Large topic counts (50+) should degrade gracefully |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | Topics ≤ 30 displayed, or overflow indicator present ("... and N more") |
| 0.7 | Topics 31-50 without overflow, but still readable |
| 0.3 | Topics > 50 without truncation, diagram hard to read |
| 0.0 | Diagram unreadable due to overcrowding |

---

### MM-007: File Size Under Token Limit

| Attribute | Value |
|-----------|-------|
| **ID** | MM-007 |
| **Severity** | ERROR |
| **Weight** | 0.10 |
| **Description** | Mindmap file must be under 35K token limit (ADR-004) |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | File size < 31.5K tokens (soft limit) |
| 0.7 | File size 31.5K - 35K tokens |
| 0.0 | File size > 35K tokens (hard limit violation) |

---

## ASCII Mindmap Criteria (AM-*)

These criteria apply when `08-mindmap/mindmap.ascii.txt` exists.

### AM-001: 80-Character Line Width Constraint

| Attribute | Value |
|-----------|-------|
| **ID** | AM-001 |
| **Severity** | ERROR |
| **Weight** | 0.25 |
| **Description** | No line in the ASCII mindmap may exceed 80 characters |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | All lines ≤ 80 characters |
| 0.7 | 95%+ lines within limit |
| 0.3 | 80-94% lines within limit |
| 0.0 | More than 20% lines exceed limit |

**Verification:**
```bash
# Conceptual check - agent should verify longest line
awk '{ print length }' mindmap.ascii.txt | sort -rn | head -1
# Result should be ≤ 80
```

---

### AM-002: Legend Present at Bottom

| Attribute | Value |
|-----------|-------|
| **ID** | AM-002 |
| **Severity** | ERROR |
| **Weight** | 0.20 |
| **Description** | ASCII mindmap must include a legend explaining symbols |

**Required Legend Content:**
```
Legend:
  [→] Action Item
  [?] Question
  [!] Decision
  [*] Topic
```

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | Legend present with all 4 entity symbols explained |
| 0.7 | Legend present but missing 1 symbol |
| 0.3 | Legend present but missing 2+ symbols |
| 0.0 | No legend present |

---

### AM-003: Valid UTF-8 Box-Drawing Characters

| Attribute | Value |
|-----------|-------|
| **ID** | AM-003 |
| **Severity** | ERROR |
| **Weight** | 0.20 |
| **Description** | File uses proper Unicode box-drawing characters |

**Required Characters:**
| Character | Unicode | Purpose |
|-----------|---------|---------|
| ┌ | U+250C | Top-left corner |
| ┐ | U+2510 | Top-right corner |
| └ | U+2514 | Bottom-left corner |
| ┘ | U+2518 | Bottom-right corner |
| ─ | U+2500 | Horizontal line |
| │ | U+2502 | Vertical line |
| ├ | U+251C | Left T-junction |
| ┬ | U+252C | Top T-junction |
| ▼ | U+25BC | Down arrow (child indicator) |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | File uses proper box-drawing characters, valid UTF-8 |
| 0.5 | Uses ASCII fallback (+-|) but consistent |
| 0.0 | Invalid encoding or broken characters |

---

### AM-004: Tree Structure Visually Balanced

| Attribute | Value |
|-----------|-------|
| **ID** | AM-004 |
| **Severity** | WARNING |
| **Weight** | 0.15 |
| **Description** | Visual tree should be reasonably balanced and readable |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | Balanced tree, clear hierarchy, easy to follow |
| 0.7 | Slightly unbalanced but still readable |
| 0.3 | Significantly unbalanced, hard to follow |
| 0.0 | Unreadable structure, broken layout |

---

### AM-005: Entity Symbols Match Mermaid Version

| Attribute | Value |
|-----------|-------|
| **ID** | AM-005 |
| **Severity** | WARNING |
| **Weight** | 0.20 |
| **Description** | Entity symbols in ASCII should match Mermaid symbols |

**Symbol Consistency:**
| Entity | Mermaid | ASCII |
|--------|---------|-------|
| Action | → | [→] |
| Question | ? | [?] |
| Decision | ! | [!] |
| Topic | * | [*] |

**Evaluation Rubric:**

| Score | Criteria |
|-------|----------|
| 1.0 | All symbols consistent between formats |
| 0.7 | 80%+ symbol consistency |
| 0.3 | Some symbols match, others different |
| 0.0 | No consistency or wrong mapping |

---

## Quality Score Calculation

### When Mindmaps Present (Default)

```
Final Score = (Core Score × 0.85) + (Mindmap Score × 0.15)

Where:
  Core Score = Existing ps-critic evaluation of packet files
  Mindmap Score = Weighted average of MM-* and AM-* criteria

Mindmap Score Breakdown:
  IF only Mermaid present:
    Mindmap Score = MM-001 through MM-007 weighted average
  IF only ASCII present:
    Mindmap Score = AM-001 through AM-005 weighted average
  IF both present (default):
    Mindmap Score = (Mermaid Score × 0.6) + (ASCII Score × 0.4)
```

### When Mindmaps Absent (--no-mindmap)

```
Final Score = Core Score × 1.00
# No penalty for intentional opt-out
```

---

## Integration with ps-critic

### Invocation Protocol

When ps-critic is invoked for transcript skill validation:

```yaml
# Additional context to include in ps-critic invocation
transcript_validation_context:
  mindmap_enabled: true  # Unless --no-mindmap was used
  mindmap_directory: "08-mindmap/"
  files_to_validate:
    - "08-mindmap/mindmap.mmd"      # If exists
    - "08-mindmap/mindmap.ascii.txt" # If exists
  criteria_extension: "skills/transcript/validation/ts-critic-extension.md"
  score_composition:
    core_weight: 0.85
    mindmap_weight: 0.15
```

### Output Format Extension

ps-critic output should include mindmap validation section:

```markdown
## Mindmap Validation (MM-*/AM-*)

| Criterion | Score | Status | Notes |
|-----------|-------|--------|-------|
| MM-001 Valid Syntax | 1.0 | PASS | Mermaid syntax correct |
| MM-002 Root Node | 1.0 | PASS | Root present with title |
| MM-003 Deep Links | 0.9 | PASS | 18/20 links valid |
| ... | ... | ... | ... |
| AM-001 Line Width | 1.0 | PASS | Max width: 78 chars |
| ... | ... | ... | ... |

**Mindmap Subscore:** 0.93
**Overall Score:** (0.89 × 0.85) + (0.93 × 0.15) = 0.90
```

---

## Graceful Degradation

When mindmap generation fails but pipeline continues:

```yaml
mindmap_validation:
  status: "skipped"
  reason: "Mindmap generation failed - see ts_mindmap_output.error_message"
  score_impact: "Core score used at 100% weight"
  recommendation: "To regenerate: /transcript --regenerate-mindmap <packet-path>"
```

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| [ADR-006](../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) | Authoritative source (Section 5.5) |
| [ps-critic.md](../../problem-solving/agents/ps-critic.md) | Base agent definition |
| [ts-mindmap-mermaid.md](../agents/ts-mindmap-mermaid.md) | Mermaid generator agent |
| [ts-mindmap-ascii.md](../agents/ts-mindmap-ascii.md) | ASCII generator agent |
| [mindmap-tests.yaml](../test_data/validation/mindmap-tests.yaml) | Test specifications |
| [DISC-001](../../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-024-mindmap-pipeline-integration/EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md) | 08-mindmap/ numbering |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-30 | Initial creation per ADR-006 Section 5.5 and TASK-245 |

---

*Document Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0 (P-001, P-002, P-022)*
*Quality Threshold: ps-critic ≥ 0.90*
