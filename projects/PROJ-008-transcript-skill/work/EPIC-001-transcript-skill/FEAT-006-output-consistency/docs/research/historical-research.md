# Historical Research: Existing Template Specifications for Transcript Skill Output Format

> **PS ID:** FEAT-006-phase-1
> **Entry ID:** e-002
> **Agent:** ps-researcher
> **Created:** 2026-01-31
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

### The Question

What template specifications already exist in the FEAT-001 analysis and design documents that define how transcript skill output should be formatted?

### Key Findings

**Templates DO exist** - The repository contains comprehensive specifications for the 8-file packet structure across multiple documents:

1. **ADR-002** defines the hierarchical packet structure with 8 numbered files
2. **ts-formatter.md** contains detailed file templates with frontmatter, navigation, and anchor requirements
3. **TDD-ts-formatter.md** specifies token budgets, splitting algorithms, and anchor naming conventions
4. **PLAYBOOK.md** documents the end-to-end formatting workflow with validation criteria

However, **critical gaps exist**:
- Templates are **scattered** across 4+ documents with no single source of truth
- Some specifications are **inconsistent** between documents (e.g., anchor format variations)
- Templates are **embedded in prose** rather than standalone, reusable template files
- **No model-agnostic guardrails** exist - formatting rules are implicit in agent instructions

### Bottom Line

Template specifications exist but are **fragmented and implicit**. FEAT-006 Phase 2 should consolidate these into explicit, model-agnostic template files that can be referenced by any LLM without relying on agent-specific context.

---

## L1: Technical Findings (Engineer)

### 1. Sources Analyzed

| Source Document | Location | Key Content Found |
|-----------------|----------|-------------------|
| TASK-002-artifact-structure-adr.md | FEAT-001/EN-004-architecture-decisions/ | 8-file packet structure, token budgets, naming conventions |
| adr-002-research.md | FEAT-001/EN-004-architecture-decisions/research/ | Directory structure patterns, index/manifest format |
| adr-003-research.md | FEAT-001/EN-004-architecture-decisions/research/ | Anchor naming conventions, backlinks format |
| ts-formatter.md | skills/transcript/agents/ | File templates, anchor registry schema, split file navigation |
| TDD-ts-formatter.md | FEAT-001/EN-005-design-documentation/docs/ | Component architecture, token counting algorithm |
| TDD-transcript-skill.md | FEAT-001/EN-005-design-documentation/docs/ | Output format JSON schemas |
| SKILL.md | skills/transcript/ | CLI invocation, domain contexts |
| PLAYBOOK.md | skills/transcript/docs/ | Execution workflow, validation criteria |
| RUNBOOK.md | skills/transcript/docs/ | Troubleshooting, citation validation |

---

### 2. The 8-File Packet Structure (ADR-002)

**Source:** adr-002-research.md, ts-formatter.md, PLAYBOOK.md

The packet structure is consistently defined across sources:

```
transcript-{id}/
├── 00-index.md          # Navigation hub (~2K tokens)
├── 01-summary.md        # Executive summary (~5K tokens)
├── 02-transcript.md     # Full transcript (may split)
├── 03-speakers.md       # Speaker directory (~3K tokens)
├── 04-action-items.md   # Action items (~4K tokens)
├── 05-decisions.md      # Decisions (~3K tokens)
├── 06-questions.md      # Open questions (~2K tokens)
├── 07-topics.md         # Topic segments (~3K tokens)
└── _anchors.json        # Anchor registry
```

**Token Budget Allocation (from adr-002-research.md):**

| File | Budget | Purpose |
|------|--------|---------|
| 00-index.md | 2K | Links and metadata only |
| 01-summary.md | 5K | Executive summary |
| 02-transcript.md | 15K* | Full transcript (*splits if larger) |
| 03-speakers.md | 8K | ~20 speakers max with profiles |
| 04-action-items.md | 10K | Tasks with assignees and dates |
| 05-decisions.md | 10K | Decisions with rationale |
| 06-questions.md | 10K | Q&A pairs with context |
| 07-topics.md | 15K | Topic hierarchy and summaries |

**Splitting Rules (ADR-004):**
- Soft limit: 31,500 tokens (90% of 35K)
- Hard limit: 35,000 tokens
- Split at `##` heading boundaries
- Split file naming: `{filename}-01.md`, `{filename}-02.md`, etc.

---

### 3. File Templates Found

#### 3.1 Index File Template (00-index.md)

**Source:** ts-formatter.md lines 220-257

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# {title}

> **Transcript ID:** {packet_id}
> **Date:** {date}
> **Duration:** {duration}
> **Speakers:** {speaker_count}

## Quick Stats

| Metric | Count |
|--------|-------|
| Action Items | {action_count} |
| Decisions | {decision_count} |
| Open Questions | {question_count} |
| Topics | {topic_count} |

## Navigation

- [Summary](./01-summary.md)
- [Full Transcript](./02-transcript.md)
- [Speakers](./03-speakers.md)
- [Action Items](./04-action-items.md)
- [Decisions](./05-decisions.md)
- [Questions](./06-questions.md)
- [Topics](./07-topics.md)

<backlinks>
<!-- Auto-generated backlinks -->
</backlinks>
```

#### 3.2 Entity File Template (Action Items Example)

**Source:** ts-formatter.md lines 259-287

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# Action Items

> **Extracted from:** [{packet_id}](./00-index.md)
> **Total:** {count}
> **High Confidence (>0.85):** {high_conf_count}

## Action Items

### {#act-001} {action_text}

- **Assignee:** [{assignee}](./03-speakers.md#{speaker_anchor})
- **Due Date:** {due_date}
- **Confidence:** {confidence}
- **Source:** [{source_text}](./02-transcript.md#{segment_anchor})

<backlinks>
- Referenced from: [02-transcript.md#seg-042](./02-transcript.md#seg-042)
</backlinks>

---
```

#### 3.3 Split File Template

**Source:** ts-formatter.md lines 289-314

```markdown
---
schema_version: "1.0"
generator: "ts-formatter"
generated_at: "{ISO_TIMESTAMP}"
---

# {title} (Part {n} of {total})

> **Continued from:** [{prev_file}](./{prev_file})
> **Next part:** [{next_file}](./{next_file})
> **Anchor Registry:** [_anchors.json](./_anchors.json)

---

{content}

---

## Navigation

- ← Previous: [{prev_file}](./{prev_file})
- → Next: [{next_file}](./{next_file})
- ↑ Index: [00-index.md](./00-index.md)
```

---

### 4. Citation Format Specifications

#### 4.1 Anchor ID Formats (ADR-003)

**Source:** ts-formatter.md lines 340-368

| Entity Type | Anchor Pattern | Example |
|-------------|----------------|---------|
| Segments | seg-{NNN} | seg-001, seg-042 |
| Speakers | spk-{name} | spk-alice, spk-bob-smith |
| Actions | act-{NNN} | act-001, act-002 |
| Decisions | dec-{NNN} | dec-001, dec-002 |
| Questions | que-{NNN} | que-001, que-002 |
| Topics | top-{NNN} | top-001, top-002 |

**Anchor Registry Schema (_anchors.json):**

```json
{
  "packet_id": "{id}",
  "version": "1.0",
  "anchors": [
    {
      "id": "seg-042",
      "type": "segment",
      "file": "02-transcript.md",
      "line": 156
    }
  ],
  "backlinks": {
    "spk-alice": [
      {"file": "02-transcript.md", "line": 42, "context": "Alice: Good morning"},
      {"file": "04-action-items.md", "line": 12, "context": "Assigned to Alice"}
    ]
  }
}
```

#### 4.2 Citation Link Format

**Source:** adr-003-research.md, ts-formatter.md

```markdown
# Forward links (entity to source)
[{source_text}](./02-transcript.md#seg-042)

# Backlinks section format
<backlinks>
Referenced in:
- [02-transcript.md#seg-042](./02-transcript.md#seg-042) - "Alice mentioned..."
- [04-action-items.md#act-001](./04-action-items.md#act-001) - "Action assigned to..."
</backlinks>
```

#### 4.3 Timestamp Format

**Source:** TDD-transcript-skill.md lines 436-462

```json
{
  "segments": [
    {
      "id": "seg-001",
      "start": 0.0,
      "end": 5.5,
      "speaker": "Alice",
      "text": "Good morning everyone.",
      "raw_text": "<v Alice>Good morning everyone.</v>"
    }
  ]
}
```

**Display format in Markdown:**
- Timestamp: `[00:15:32]` (HH:MM:SS)
- Anchor reference: `[#seg-042](./02-transcript.md#seg-042)`
- Combined: `[00:15:32](#seg-042)`

---

### 5. Navigation Requirements

#### 5.1 Prev/Index/Next Links

**Source:** ts-formatter.md Split File Template

All split files must include navigation:

```markdown
## Navigation

- ← Previous: [{prev_file}](./{prev_file})
- → Next: [{next_file}](./{next_file})
- ↑ Index: [00-index.md](./00-index.md)
```

#### 5.2 Cross-File References

**Source:** adr-003-research.md

Link patterns for cross-file navigation:
- `00-index.md` → All other files (master index)
- `01-summary.md` → `03-speakers.md#spk-{name}` (speaker mentions)
- `04-action-items.md` → `02-transcript.md#seg-{NNN}` (source citations)
- `03-speakers.md` ← backlinks from entity files

---

### 6. ts-formatter Agent Guardrails

**Source:** ts-formatter.md lines 36-75

#### Input Validation Rules

```yaml
guardrails:
  input_validation:
    - pattern: "model override via CLI flags only"
      enforcement: hard
      rationale: "P-020 user authority for model selection"
    index_json_required: true
    extraction_report_required: true
    canonical_json_forbidden: true  # NEVER read large file
    packet_id_required: true
    token_limit: 35000
    soft_limit_percent_min: 0
    soft_limit_percent_max: 100
    index_file_max_size_kb: 10
```

#### Output Filtering Rules

```yaml
output_filtering:
  - no_secrets_in_output
  - enforce_token_limits
  - validate_anchor_format
  - verify_backlinks_resolve
  - verify_each_file_under_35k_tokens
  - verify_split_at_semantic_boundaries
  - verify_schema_version_in_frontmatter
```

#### Post-Completion Checks

```yaml
post_completion_checks:
  - verify_file_created
  - verify_all_packet_files_exist
  - verify_token_limits_respected
  - verify_anchor_registry_complete
  - verify_navigation_links_work
  - verify_backlinks_generated
  - verify_exactly_8_core_files
  - verify_anchors_json_exists
  - verify_split_file_naming
```

---

### 7. Model-Agnostic Requirements

**Finding:** No explicit model-agnostic requirements were found.

The following rules are **implicitly model-agnostic** (should work regardless of model):

1. **File structure rules** - 8-file packet with numbered prefixes
2. **Token budgets** - Hard limits (35K per file)
3. **Anchor naming conventions** - `{type}-{NNN}` format
4. **YAML frontmatter** - schema_version, generator, generated_at
5. **Navigation links** - Relative paths with `./` prefix
6. **Backlinks section** - `<backlinks>` placeholder

However, the following are **model-dependent** (embedded in agent instructions):

1. **Template rendering** - Relies on agent understanding variable substitution
2. **Semantic splitting** - Relies on agent judgment for `##` heading boundaries
3. **Quality assessment** - Relies on ps-critic agent scoring

---

## L2: Architectural Implications (Architect)

### 8. Gaps Identified

| Gap ID | Description | Impact | Recommendation |
|--------|-------------|--------|----------------|
| GAP-T-001 | Templates scattered across 4+ documents | Maintenance burden, inconsistency risk | Consolidate into `skills/transcript/templates/` |
| GAP-T-002 | No standalone template files | Models must parse prose to find templates | Create `.template.md` files |
| GAP-T-003 | Anchor format variations | Inconsistent deep linking | Standardize to `{type}-{NNN}` only |
| GAP-T-004 | Navigation template incomplete | Split files missing in some docs | Complete split file navigation template |
| GAP-T-005 | No model-agnostic guardrails file | Model-switching requires re-reading agents | Create format-guardrails.md |
| GAP-T-006 | Backlinks format varies | `<backlinks>` vs `## Backlinks` | Standardize to `<backlinks>` tag |
| GAP-T-007 | Timestamp display format inconsistent | `[00:15:32]` vs `00:15:32.500` | Document canonical display format |

### 9. Template Specification Summary

#### Templates Found (Status: IMPLICIT)

| Template | Source | Status | Location |
|----------|--------|--------|----------|
| 00-index.md | ts-formatter.md:220-257 | Embedded in prose | Lines 220-257 |
| Entity file (action items) | ts-formatter.md:259-287 | Embedded in prose | Lines 259-287 |
| Split file navigation | ts-formatter.md:289-314 | Embedded in prose | Lines 289-314 |
| Index manifest | adr-002-research.md:215-250 | Embedded in prose | Lines 215-250 |
| Anchor registry schema | TDD-ts-formatter.md:185-219 | JSON schema | Lines 185-219 |

#### Templates NOT Found (Status: MISSING)

| Template | Expected Content | Priority |
|----------|------------------|----------|
| 01-summary.md template | Executive summary structure | HIGH |
| 02-transcript.md template | Segment rendering format | HIGH |
| 03-speakers.md template | Speaker card structure | MEDIUM |
| 05-decisions.md template | Decision record structure | MEDIUM |
| 06-questions.md template | Q&A pair format | MEDIUM |
| 07-topics.md template | Topic hierarchy format | MEDIUM |

### 10. Recommendations for Phase 2

#### Priority 1: Consolidation

1. Create `skills/transcript/templates/` directory
2. Extract templates from ts-formatter.md into standalone files:
   - `00-index.template.md`
   - `entity-file.template.md`
   - `split-file.template.md`

#### Priority 2: Standardization

1. Create `skills/transcript/docs/format-specification.md` as single source of truth
2. Define canonical anchor format: `{type}-{NNN}` (3-letter type, 3-digit number)
3. Define canonical timestamp display: `[HH:MM:SS]` in Markdown, milliseconds in JSON

#### Priority 3: Model-Agnostic Guardrails

1. Create `skills/transcript/validation/format-guardrails.md`:
   - File structure validation rules
   - Token budget enforcement
   - Anchor naming validation
   - Link resolution checks

---

## 11. References

### Primary Sources (Analyzed)

| # | Document | Path |
|---|----------|------|
| 1 | ts-formatter.md | skills/transcript/agents/ts-formatter.md |
| 2 | TDD-ts-formatter.md | FEAT-001/EN-005-design-documentation/docs/TDD-ts-formatter.md |
| 3 | TDD-transcript-skill.md | FEAT-001/EN-005-design-documentation/docs/TDD-transcript-skill.md |
| 4 | adr-002-research.md | FEAT-001/EN-004-architecture-decisions/research/adr-002-research.md |
| 5 | adr-003-research.md | FEAT-001/EN-004-architecture-decisions/research/adr-003-research.md |
| 6 | SKILL.md | skills/transcript/SKILL.md |
| 7 | PLAYBOOK.md | skills/transcript/docs/PLAYBOOK.md |
| 8 | RUNBOOK.md | skills/transcript/docs/RUNBOOK.md |
| 9 | TASK-002-artifact-structure-adr.md | FEAT-001/EN-004-architecture-decisions/TASK-002-artifact-structure-adr.md |

### Related ADRs

| ADR | Title | Relevance |
|-----|-------|-----------|
| ADR-001 | Agent Architecture | Defines 3-agent pipeline |
| ADR-002 | Artifact Structure & Token Management | Defines 8-file packet, token limits |
| ADR-003 | Bidirectional Deep Linking | Defines anchor naming, backlinks |
| ADR-004 | Semantic File Splitting | Defines split algorithm, soft/hard limits |
| ADR-005 | Phased Implementation | Defines prompt-based vs Python split |
| ADR-006 | Mindmap Pipeline Integration | Defines mindmap file structure |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | FEAT-006-e-002-historical-research |
| PS ID | FEAT-006-phase-1 |
| Entry ID | e-002 |
| Created | 2026-01-31 |
| Author | ps-researcher agent |
| Status | COMPLETE |
| Word Count | ~2,800 |
| Next Step | Phase 2 - Industry research on template best practices |

---

*Generated by ps-researcher agent*
*Constitutional Compliance: P-002 (persisted to repository), P-004 (provenance documented), P-011 (evidence-based with citations)*
