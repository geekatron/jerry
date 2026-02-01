# TASK-003: Token Budget Optimization Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Description](#description) | Context rot science and token targets |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Token Budget Optimization Research"
status: DONE
priority: HIGH
assignee: "ps-researcher-claude-md"
parent_id: "EN-003"
effort: 1
activity: RESEARCH
```

---

## Description

Research token budget optimization techniques and context rot science to establish targets for CLAUDE.md reduction.

### Context Rot Science (Chroma Research)

- LLM performance degrades as context window fills
- **75% utilization is the sweet spot** for quality
- At 90%+ utilization, performance significantly degrades
- Selective context > maximum context

### Token Targets

| Metric | Current | Target | Reduction |
|--------|---------|--------|-----------|
| CLAUDE.md tokens | ~10,000 | ~3,500 | 65% |
| Session start total | ~15,000 | ~5,000 | 67% |

### Acceptance Criteria

- [x] Context rot research analyzed
- [x] Token targets established
- [x] Optimization techniques identified

### Related Items

- Parent: [EN-003](./EN-003-claude-md-optimization.md)
- Source: [Chroma Context Rot Research](https://research.trychroma.com/context-rot)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | DONE | Research complete |
