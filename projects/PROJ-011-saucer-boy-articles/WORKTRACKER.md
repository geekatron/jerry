# PROJ-011: Saucer Boy Articles - Work Tracker

> Global Manifest for PROJ-011. High-quality articles in the Saucer Boy (McConkey) voice covering LLM engineering topics. C4 adversarial quality gates before publication.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and status |
| [Articles](#articles) | Article registry and status |
| [Marketing](#marketing) | Marketing deliverables work items |
| [Decisions](#decisions) | Key decisions |
| [History](#history) | Change log |

---

## Summary

| Field | Value |
|-------|-------|
| Project | PROJ-011-saucer-boy-articles |
| Status | IN-PROGRESS |
| Created | 2026-02-23 |
| Voice | Saucer Boy (Shane McConkey persona) |
| Quality Bar | >= 0.95 content + >= 0.95 LLM-tell + >= 0.95 voice authenticity |

---

## Articles

| ID | Title | Status | Score | Draft |
|----|-------|--------|-------|-------|
| ART-001 | Why Structured Prompting Works | IN-PROGRESS | 0.938 (iter-3, pre-humanization) | [draft-4-human-rewrite](./work/articles/ART-001-structured-prompting/drafts/draft-4-human-rewrite.md) |

---

## Marketing

### STORY-001: Marketing Deliverables for ART-001

| Field | Value |
|-------|-------|
| Status | completed |
| Score | 0.970 (Medium article, S-014 iter-6) |
| Location | [STORY-001](./work/articles/ART-001-structured-prompting/STORY-001-marketing-deliverables/STORY-001-marketing-deliverables.md) |

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| TASK-001 | Create Medium article | completed | 111 lines, inline citation hyperlinks |
| TASK-002 | Create Slack promotion message | completed | Short + longer versions, P6 caveats applied |
| TASK-003 | Execute C4 adversarial tournament | completed | All 10 strategies, 6 scoring iterations, 0.970 PASS |
| TASK-004 | Apply targeted revisions (P1-P6) | completed | 5 Medium edits + 1 Slack edit |
| TASK-005 | Fix blog citation defect | completed | Liu et al. (2023) changed to (2024) |

---

## Decisions

| ID | Title | Status | Impact |
|----|-------|--------|--------|
| DEC-001 | C4 adversarial review for all articles | decided | high |
| DEC-002 | Three independent quality gates (content, LLM-tell, voice) | decided | high |

---

## History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-23 | Claude | PROJ-011 created. Article pipeline for Saucer Boy voice content. |
| 2026-02-23 | Claude | ART-001 migrated from previous session. Draft-4 (human rewrite) is current. C4 adversarial review iteration 1-3 complete (10 strategies). Score: 0.938. |
| 2026-02-24 | Claude | STORY-001 marketing deliverables completed. Medium article 0.970 PASS (C4 tournament, 6 iterations). Slack message accepted as promotional artifact. Blog Liu et al. year defect fixed. |
| 2026-02-24 | Claude | Worktracker entities created: STORY-001 + TASK-001 through TASK-005 under ART-001. |
