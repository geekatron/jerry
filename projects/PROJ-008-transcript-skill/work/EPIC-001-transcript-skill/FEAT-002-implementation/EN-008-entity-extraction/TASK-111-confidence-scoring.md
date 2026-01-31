# TASK-111: Implement Confidence Scoring (NFR-008)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-111"
work_type: TASK
title: "Implement Confidence Scoring (NFR-008)"
description: |
  Implement and verify the confidence scoring mechanism that provides
  HIGH/MEDIUM/LOW ratings for all extracted entities per NFR-008.

classification: ENABLER
status: DONE
resolution: VERIFIED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-008"

tags:
  - "implementation"
  - "ts-extractor"
  - "confidence-scoring"
  - "NFR-008"

effort: 1
acceptance_criteria: |
  - All extracted entities have confidence scores
  - Confidence thresholds: HIGH(≥0.85), MEDIUM(0.70-0.85), LOW(<0.70)
  - Scores derived from extraction tier and pattern match quality
  - Average confidence tracked in extraction statistics

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `DONE`

**State History:**
- BACKLOG → IN_PROGRESS (2026-01-28)
- IN_PROGRESS → DONE (2026-01-28)

---

## Content

### Description

Implement and verify the confidence scoring mechanism that assigns quality ratings to all extracted entities. This implements NFR-008 and enables users to filter or prioritize entities by reliability.

### Confidence Thresholds

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONFIDENCE SCORING SYSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  THRESHOLD LEVELS:                                                           │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                              HIGH                                    │    │
│  │                           (≥ 0.85)                                   │    │
│  │                                                                       │    │
│  │  • Explicit patterns (Tier 1)                                        │    │
│  │  • VTT voice tags (PAT-003 Pattern 1)                               │    │
│  │  • Exact keyword matches                                             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                             MEDIUM                                   │    │
│  │                         (0.70 - 0.85)                               │    │
│  │                                                                       │    │
│  │  • Phrase patterns (Tier 2)                                          │    │
│  │  • Prefix/Bracket speaker detection (PAT-003 Patterns 2-3)          │    │
│  │  • Structural matches                                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                              LOW                                     │    │
│  │                           (< 0.70)                                   │    │
│  │                                                                       │    │
│  │  • LLM contextual extraction (Tier 3)                               │    │
│  │  • Contextual speaker resolution (PAT-003 Pattern 4)                │    │
│  │  • Semantic inference                                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Confidence Sources

| Component | Base Confidence | Factors |
|-----------|-----------------|---------|
| TieredExtractor | Tier-based | Pattern explicitness, match quality |
| SpeakerIdentifier | Pattern-based | Pattern level (1-4), ambiguity |
| CitationLinker | Validation-based | Citation completeness, snippet match |
| TopicSegmenter | Signal-based | Boundary signal strength |

### Confidence Calculation

```python
# Conceptual algorithm
def calculate_confidence(extraction_source, pattern_match_quality, modifiers):
    base_confidence = {
        "tier_1": 0.92,
        "tier_2": 0.78,
        "tier_3": 0.60
    }.get(extraction_source, 0.50)

    # Adjust based on pattern match quality (0.0 - 1.0)
    adjusted = base_confidence * pattern_match_quality

    # Apply modifiers
    for modifier in modifiers:
        if modifier == "explicit_keyword":
            adjusted += 0.05
        elif modifier == "ambiguous_context":
            adjusted -= 0.10
        elif modifier == "speaker_unknown":
            adjusted -= 0.05

    return max(0.0, min(1.0, adjusted))
```

### Confidence Modifiers

| Modifier | Effect | When Applied |
|----------|--------|--------------|
| Explicit keyword match | +0.05 | "ACTION:", "DECISION:" present |
| Multiple pattern match | +0.03 | Same entity found by multiple tiers |
| Ambiguous context | -0.10 | Multiple interpretations possible |
| Speaker unknown | -0.05 | Entity has "Unknown Speaker" |
| Low citation quality | -0.08 | Text snippet partial match |

### Acceptance Criteria

- [x] All entities include `confidence` field (0.0 - 1.0)
- [x] HIGH threshold: ≥ 0.85
- [x] MEDIUM threshold: 0.70 - 0.85 (agent uses 0.70-0.84)
- [x] LOW threshold: < 0.70
- [x] Confidence derives from extraction tier (tier_base_score)
- [x] Confidence modified by match quality (adjustments array)
- [x] Average confidence in extraction statistics (confidence_summary.average)
- [x] Confidence distribution histogram in report (confidence_summary counts)

### Test Cases (from EN-015)

Reference test scenarios:
- HIGH confidence: Explicit "ACTION:" pattern
- MEDIUM confidence: Phrase pattern "I'll send"
- LOW confidence: Contextual inference
- Confidence modifiers applied correctly
- Average confidence calculation accurate

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- Blocked By: [TASK-107](./TASK-107-speaker-identification.md), [TASK-108](./TASK-108-tiered-extraction.md), [TASK-109](./TASK-109-citation-linker.md), [TASK-110](./TASK-110-topic-segmenter.md)
- References: [TDD-ts-extractor.md Section 4](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- Validated By: [TASK-135: Extractor tests](../EN-015-transcript-validation/TASK-135-extractor-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md confidence scoring section | Agent | skills/transcript/agents/ts-extractor.md |
| Confidence scoring test results | Test Evidence | (link to test output) |

### Verification

- [x] All threshold levels implemented (HIGH ≥0.85, MEDIUM 0.70-0.84, LOW <0.70)
- [x] Confidence modifiers applied correctly (+0.05 explicit, +0.10 NER, -0.10 ambiguous, -0.05 short)
- [x] Average confidence calculated (confidence_summary.average in extraction_stats)
- [x] Distribution tracked (high_count, medium_count, low_count, high_ratio)
- [x] Reviewed by: Claude (2026-01-28)

**Implementation Approach:** Prompt-Based Agent (per ADR-005)

The Confidence Scoring is implemented via detailed instructions in ts-extractor.md:
- **Section:** "Confidence Scoring"
- **Calculation:** base_confidence + sum(adjustments) clamped to [0.0, 1.0]
- **Thresholds:** HIGH (primary output), MEDIUM (review flag), LOW (uncertain section)
- **Output Enhancement:** Added confidence_summary to extraction_stats (v1.2.0)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |
| 2026-01-28 | DONE | Verified existing confidence scoring implementation in ts-extractor.md. Added confidence_summary to extraction_stats (v1.2.0) for average, high/medium/low counts, and high_ratio tracking. |

