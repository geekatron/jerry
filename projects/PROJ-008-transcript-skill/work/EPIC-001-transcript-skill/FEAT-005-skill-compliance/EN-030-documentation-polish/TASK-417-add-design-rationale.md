# TASK-417: Add design rationale to PLAYBOOK.md

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-417"
work_type: TASK
title: "Add design rationale to PLAYBOOK.md"
status: BACKLOG
priority: LOW
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-030"
effort: 2
activity: DOCUMENTATION
```

---

## Description

Add design rationale section to PLAYBOOK.md documenting why key architectural decisions were made. Addresses GAP-D-005: Design rationale missing.

**File to modify:**
- skills/transcript/docs/PLAYBOOK.md

**Location:** L2 section, after Constraints & Boundaries

---

## Acceptance Criteria

- [ ] "Design Rationale" section header added
- [ ] Rationale for hybrid Python+LLM architecture
- [ ] Rationale for chunked architecture
- [ ] Rationale for Sequential Chain pattern
- [ ] References to relevant ADRs and DISCs

---

## Implementation Notes

**Content to add:**

```markdown
### Design Rationale

#### Why Hybrid Python+LLM Architecture?

**Decision:** Use Python for VTT parsing, LLM for extraction/formatting

**Rationale:**
- Python parsing is 1,250x cheaper and 100% accurate for structured VTT
- LLM excels at semantic extraction (action items, decisions, questions)
- Hybrid approach optimizes both cost and accuracy

**Reference:** DISC-009, TDD-FEAT-004

---

#### Why Chunked Architecture?

**Decision:** Split transcripts into 500-segment chunks

**Rationale:**
- Large transcripts (3000+ segments) overflow context window
- Agent-only architecture caused 99.8% data loss (see DISC-009)
- Chunking enables processing of any transcript size
- Each chunk is < 150KB (fits comfortably in context)

**Reference:** DISC-009

---

#### Why Sequential Chain Pattern?

**Decision:** Use Pattern 2 (Sequential Chain) for pipeline

**Rationale:**
- Each step strictly depends on previous step's output
- No parallelism opportunities between main stages
- Simple, predictable execution flow
- Easy to debug and trace errors

**Reference:** orchestration SKILL.md Pattern Catalog

---

#### Why Mindmaps On by Default?

**Decision:** Generate mindmaps unless --no-mindmap flag (ADR-006)

**Rationale:**
- Provides immediate visual navigation
- Low cost (adds ~2K tokens per format)
- Opt-out rather than opt-in reduces friction
- Users who don't want mindmaps can easily disable

**Reference:** ADR-006
```

---

## Related Items

- Parent: [EN-030: Documentation Polish](./EN-030-documentation-polish.md)
- Gap: GAP-D-005 (Design rationale missing)
- References: DISC-009, ADR-006, TDD-FEAT-004

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| PLAYBOOK.md | Documentation | skills/transcript/docs/PLAYBOOK.md |

### Verification

- [ ] Design Rationale section present
- [ ] 4+ rationale entries documented
- [ ] References to source documents included
- [ ] Decision + Rationale format consistent

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-030 |
