# TASK-421: Update SKILL.md model documentation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-421"
work_type: TASK
title: "Update SKILL.md model documentation"
status: BACKLOG
priority: MEDIUM
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-031"
effort: 4
activity: DOCUMENTATION
```

---

## Description

Update SKILL.md to document the new model selection parameters, including usage examples, default values, and cost implications.

**File to modify:**
- skills/transcript/SKILL.md

**Depends on:** TASK-420 (Add CLI model parameters)

---

## Acceptance Criteria

- [ ] "Model Selection" section added to SKILL.md
- [ ] All `--model-*` parameters documented
- [ ] Default values documented with rationale
- [ ] Cost implications table included
- [ ] Usage examples provided
- [ ] Model profiles referenced (from TASK-423)

---

## Implementation Notes

### Section to Add

```markdown
## Model Selection

The transcript skill supports configurable models for each agent to optimize cost and quality.

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--model-parser` | haiku | Model for ts-parser (orchestration, routing) |
| `--model-extractor` | sonnet | Model for ts-extractor (entity extraction) |
| `--model-formatter` | sonnet | Model for ts-formatter (packet generation) |
| `--model-mindmap` | sonnet | Model for ts-mindmap-* (visualization) |
| `--model-critic` | sonnet | Model for ps-critic (quality review) |

### Cost Optimization

| Configuration | Estimated Cost (10K tokens) | Quality Trade-off |
|---------------|----------------------------|-------------------|
| Default (mixed) | ~$0.12 | Balanced |
| All haiku | ~$0.015 | 88% savings, lower extraction quality |
| All sonnet | ~$0.15 | Baseline quality |
| All opus | ~$0.75 | Highest quality, 6x cost |

### Usage Examples

```bash
# Economy mode - use haiku where possible
uv run jerry transcript parse meeting.vtt \
    --model-formatter haiku \
    --model-mindmap haiku

# Quality mode - use opus for critical extraction
uv run jerry transcript parse meeting.vtt \
    --model-extractor opus \
    --model-critic opus

# Balanced mode (default)
uv run jerry transcript parse meeting.vtt
```

### Recommendations

- **Extraction:** Use sonnet or opus for accurate entity extraction
- **Formatting:** Can use haiku if extraction quality is good
- **Critic:** Use sonnet for reliable quality assessment
- **Parser:** Haiku is sufficient (minimal semantic work)
```

---

## Related Items

- Parent: [EN-031: Model Selection Capability](./EN-031-model-selection-capability.md)
- Depends on: TASK-420 (Add CLI model parameters)
- Related: TASK-423 (Implement profiles)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Model Selection section present
- [ ] All parameters documented
- [ ] Cost table included
- [ ] Examples are accurate

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-031 |
