# TASK-418: Add cross-skill integration examples

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-418"
work_type: TASK
title: "Add cross-skill integration examples"
status: BACKLOG
priority: LOW
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-030"
effort: 1
activity: DOCUMENTATION
```

---

## Description

Add cross-skill integration examples to PLAYBOOK.md showing how transcript skill composes with problem-solving and orchestration skills. Addresses GAP-D-006: Cross-skill integration undocumented.

**File to modify:**
- skills/transcript/docs/PLAYBOOK.md

**Location:** L2 section, after Design Rationale

---

## Acceptance Criteria

- [ ] "Cross-Skill Integration" section header added
- [ ] Integration with problem-solving skill documented
- [ ] Integration with orchestration skill documented
- [ ] State handoff between skills explained
- [ ] session_context schema referenced

---

## Implementation Notes

**Content to add:**

```markdown
### Cross-Skill Integration

#### With problem-solving Skill

The transcript skill integrates with problem-solving via **ps-critic** for quality review:

```
/transcript meeting.vtt
       │
       ▼
  ts-parser → ts-extractor → ts-formatter → ts-mindmap-*
                                                   │
                                                   ▼
                                            ps-critic (quality >= 0.90)
```

**State Handoff:**
- `ts_formatter_output` → `ps_critic_input`
- `session_context` schema v1.0.0 ensures compatibility

**Example:**
```yaml
# After ts-formatter completes
ps_critic_input:
  packet_path: "output/transcript-001/"
  quality_threshold: 0.90
  include_mindmap_validation: true
```

---

#### With orchestration Skill

For complex multi-transcript workflows, use orchestration to coordinate:

```
ORCHESTRATION_PLAN.md:
- Phase 1: Parse transcripts (transcript skill × N)
- Phase 2: Synthesize findings (problem-solving skill)
- Phase 3: Generate executive summary (problem-solving skill)
```

**Use Case:** Processing multiple meeting transcripts and generating a consolidated report.

**Sync Barrier Example:**
```yaml
# Wait for all transcripts before synthesis
sync_barrier:
  name: "all-transcripts-parsed"
  wait_for:
    - transcript-001: ts_formatter_output
    - transcript-002: ts_formatter_output
    - transcript-003: ts_formatter_output
```

---

#### With nasa-se Skill

For requirements-critical meetings, extract requirements using nasa-se skill:

```
1. /transcript requirements-review.vtt
2. /nasa-se requirements from output/packet/05-decisions.md
```

**Traceability:** Action items become requirement candidates with transcript citations.
```

---

## Related Items

- Parent: [EN-030: Documentation Polish](./EN-030-documentation-polish.md)
- Gap: GAP-D-006 (Cross-skill integration undocumented)
- Reference: problem-solving SKILL.md, orchestration SKILL.md

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| PLAYBOOK.md | Documentation | skills/transcript/docs/PLAYBOOK.md |

### Verification

- [ ] Cross-Skill Integration section present
- [ ] problem-solving integration documented
- [ ] orchestration integration documented
- [ ] session_context handoff explained

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-030 |
