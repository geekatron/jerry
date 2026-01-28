# TASK-108: Implement/Verify TieredExtractor (PAT-001)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-108"
work_type: TASK
title: "Implement/Verify TieredExtractor (PAT-001)"
description: |
  Implement and verify the TieredExtractor component using the Rule → ML → LLM
  extraction pipeline per TDD-ts-extractor.md Section 2.

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
  - "tiered-extraction"
  - "PAT-001"

effort: 3
acceptance_criteria: |
  - Tier 1 (Rule) extracts explicit patterns with confidence ≥0.85
  - Tier 2 (ML) extracts pattern-matching entities with confidence 0.70-0.85
  - Tier 3 (LLM) extracts contextual entities with confidence 0.50-0.70
  - Cascading fallback when higher tier fails
  - All 4 entity types supported (action items, decisions, questions, topics)

due_date: null

activity: DEVELOPMENT
original_estimate: 6
remaining_work: 6
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

Implement and verify the TieredExtractor component that applies a three-tier extraction pipeline to extract entities from transcript segments. The implementation must follow PAT-001 from TDD-ts-extractor.md.

### PAT-001: Tiered Extraction Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           TIERED EXTRACTION PIPELINE                            │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  INPUT: Transcript Segments                                                     │
│         │                                                                       │
│         ▼                                                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐     │
│  │ TIER 1: RULE-BASED EXTRACTION                                         │     │
│  │ ─────────────────────────────────────────────────────────────────     │     │
│  │ • Explicit patterns: "ACTION:", "DECISION:", "TODO:", "Q:"           │     │
│  │ • Keyword triggers: "will", "must", "decided", "let's", "?"          │     │
│  │ • Confidence: 0.85 - 1.0                                              │     │
│  │ • Coverage: ~40% of entities                                          │     │
│  └───────────────────────────────────────────────────────────────────────┘     │
│         │ Unmatched segments                                                    │
│         ▼                                                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐     │
│  │ TIER 2: ML PATTERN MATCHING                                           │     │
│  │ ─────────────────────────────────────────────────────────────────     │     │
│  │ • Phrase patterns: "can you", "I'll", "we should"                    │     │
│  │ • Sentence structure: Imperative, Interrogative                       │     │
│  │ • Confidence: 0.70 - 0.85                                             │     │
│  │ • Coverage: ~30% of entities                                          │     │
│  └───────────────────────────────────────────────────────────────────────┘     │
│         │ Unmatched segments                                                    │
│         ▼                                                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐     │
│  │ TIER 3: LLM CONTEXTUAL EXTRACTION                                     │     │
│  │ ─────────────────────────────────────────────────────────────────     │     │
│  │ • Semantic understanding of implicit actions/decisions               │     │
│  │ • Context-dependent extraction                                        │     │
│  │ • Confidence: 0.50 - 0.70                                             │     │
│  │ • Coverage: ~30% of entities                                          │     │
│  └───────────────────────────────────────────────────────────────────────┘     │
│         │                                                                       │
│         ▼                                                                       │
│  OUTPUT: Extracted Entities with Confidence Scores                              │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

### Extraction Rules by Entity Type

#### Action Items (FR-006)

| Tier | Pattern | Example | Confidence |
|------|---------|---------|------------|
| 1 | `ACTION:`, `TODO:`, `@assignee` | "ACTION: Bob review docs" | 0.95 |
| 1 | Modal + assignee + verb | "Bob, can you send the report" | 0.90 |
| 2 | Future tense commitment | "I'll have it ready by Friday" | 0.80 |
| 2 | Request pattern | "Would you mind checking..." | 0.75 |
| 3 | Implicit commitment | (contextual analysis) | 0.60 |

#### Decisions (FR-007)

| Tier | Pattern | Example | Confidence |
|------|---------|---------|------------|
| 1 | `DECISION:`, `AGREED:` | "DECISION: Use React" | 0.95 |
| 1 | Decision verbs | "We've decided to...", "Let's go with..." | 0.90 |
| 2 | Agreement patterns | "Everyone agrees", "That works for all" | 0.80 |
| 3 | Implicit consensus | (contextual analysis) | 0.55 |

#### Questions (FR-008)

| Tier | Pattern | Example | Confidence |
|------|---------|---------|------------|
| 1 | Question mark | "How does this work?" | 0.95 |
| 1 | `Q:` prefix | "Q: What's the timeline?" | 0.95 |
| 2 | Interrogative structure | "I wonder if...", "Can someone explain" | 0.80 |
| 3 | Rhetorical vs real | (contextual analysis) | 0.60 |

### Acceptance Criteria

- [x] Tier 1 rule patterns implemented for all entity types (ts-extractor.md Processing Instructions)
- [x] Tier 2 ML patterns implemented (NER, Intent Classification)
- [x] Tier 3 LLM extraction prompts defined
- [x] Confidence scores assigned per tier (0.85-1.0, 0.70-0.85, 0.50-0.70)
- [x] Cascading fallback: Tier 1 → Tier 2 → Tier 3 documented
- [x] Entity types: Action Items (FR-006), Decisions (FR-007), Questions (FR-008)
- [x] Token budget documented in TDD (~12K per invocation)
- [⏳] >85% precision - Deferred to EN-015 validation testing
- [⏳] >80% recall - Deferred to EN-015 validation testing

### Test Cases (from EN-015)

Reference test scenarios in extractor-tests.yaml:
- Explicit patterns (Tier 1)
- Phrase patterns (Tier 2)
- Contextual extraction (Tier 3)
- Mixed tiers in same transcript
- Edge cases: sarcasm, rhetorical questions

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- Blocked By: [TASK-106: Agent alignment](./TASK-106-extractor-agent-alignment.md)
- References: [TDD-ts-extractor.md Section 2](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- Validated By: [TASK-135: Extractor tests](../EN-015-transcript-validation/TASK-135-extractor-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md TieredExtractor section | Agent | skills/transcript/agents/ts-extractor.md |
| Extraction rule patterns | Documentation | (embedded in agent) |
| Tiered extraction test results | Test Evidence | (link to test output) |

### Verification

- [x] All three tiers implemented in ts-extractor.md
- [x] All four entity types supported (Actions, Decisions, Questions + Topics in separate section)
- [x] Confidence scores in expected ranges (Tier1: 0.85-1.0, Tier2: 0.70-0.85, Tier3: 0.50-0.70)
- [⏳] Precision ≥85% - Deferred to EN-015 (TASK-135)
- [⏳] Recall ≥80% - Deferred to EN-015 (TASK-135)
- [x] Reviewed by: Claude (2026-01-28)

### Implementation Details

**Implementation Approach:** Prompt-Based Agent (per ADR-005)

The TieredExtractor is implemented via detailed instructions in ts-extractor.md:
- **Section:** "Tiered Extraction Pipeline (PAT-001)"
- **Patterns:** ACTION ITEM PATTERNS, QUESTION PATTERNS, DECISION PATTERNS
- **ML Section:** NER EXTRACTION, INTENT CLASSIFICATION
- **LLM Section:** Prompt template for contextual extraction

**Verification:** Agent definition v1.1.0 has complete PAT-001 implementation.

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |
| 2026-01-28 | DONE | Implementation verified in ts-extractor.md. All 3 tiers with correct confidence ranges. Precision/recall testing deferred to EN-015. |

