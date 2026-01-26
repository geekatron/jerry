# TASK-005: Research tl;dv

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.7
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-01-25T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** EN-001
> **Owner:** ps-researcher
> **Effort Points:** 2

---

## Summary

Conduct comprehensive research on tl;dv - a meeting recorder and AI assistant that provides summaries and timestamps. Document features, entity extraction capabilities, integrations, and architecture patterns.

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Research document created at `research/TLDV-analysis.md` | [ ] |
| AC-2 | L0/L1/L2 summaries completed | [ ] |
| AC-3 | Core features documented with evidence | [ ] |
| AC-4 | Entity extraction capabilities documented | [ ] |
| AC-5 | Integrations catalogued | [ ] |
| AC-6 | Transcript format support documented | [ ] |
| AC-7 | All claims have citations (URLs with access dates) | [ ] |

---

## Research Questions

### 5W2H Framework

| Question | Focus Area |
|----------|------------|
| **What** | What features does tl;dv offer? What entities does it extract? |
| **Why** | Why do users choose tl;dv? What problems does it solve? |
| **Who** | Who are the target users? What personas does it serve? |
| **When** | When in the meeting workflow is it used? |
| **Where** | Where does it integrate (Slack, CRM, Calendar)? |
| **How** | How does it create summaries? How does timestamping work? |
| **How much** | What is the pricing? What accuracy claims are made? |

### Specific Research Areas

1. **Core Capabilities**
   - Meeting recording
   - AI transcription
   - Automatic summaries
   - Timestamp marking
   - Clip creation

2. **Entity Types**
   - Speakers
   - Key topics
   - Action items
   - Timestamps/Markers
   - Meeting notes

3. **Technical Architecture**
   - Recording technology
   - Transcript processing
   - Export formats
   - API availability

4. **Integrations**
   - Zoom, Google Meet, Microsoft Teams
   - Slack
   - Notion
   - HubSpot, Salesforce

---

## Output Artifact

Create file: `research/TLDV-analysis.md`

Use the standard research template from EN-001.

---

## Execution Notes

### Agent Configuration

```yaml
agent: ps-researcher
task: TASK-005-research-tldv
inputs:
  - url: https://tldv.io/
  - research_template: EN-001 research template
outputs:
  - research/TLDV-analysis.md
tools:
  - WebFetch
  - WebSearch
```

---

## Related Items

### Hierarchy

- **Parent Enabler:** [EN-001: Market Analysis Research](./EN-001-market-analysis.md)

### Sibling Tasks

- TASK-001: Research Pocket
- TASK-002: Research Otter.ai
- TASK-003: Research Fireflies.ai
- TASK-004: Research Grain

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | None | Can execute in parallel |
| Blocks | TASK-006 | Synthesis needs this research |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-25 | Claude | pending | Task created |
