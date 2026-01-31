# Task: TASK-140 - Dataset Design & Planning

> **Task ID:** TASK-140
> **Status:** DONE
> **Priority:** high
> **Enabler:** [EN-017-large-transcript-dataset](./EN-017-large-transcript-dataset.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Design the large transcript dataset with detailed specifications for token targets, topic domains, speaker rosters, and expected entity distributions for each of the 3 transcripts.

---

## Acceptance Criteria

- [x] **AC-1:** Token targets documented with estimation formula
- [x] **AC-2:** Topic domains defined with context rationale
- [x] **AC-3:** Speaker roster defined for each transcript
- [x] **AC-4:** Expected entity counts estimated per transcript
- [x] **AC-5:** Timeline/agenda structure planned for each transcript
- [x] **AC-6:** Design documented in EN-017 enabler file

---

## Unit of Work

### Step 1: Define Token Targets
- meeting-004: 22K-28K tokens (near soft limit, no split)
- meeting-005: 42K-48K tokens (triggers 1 split)
- meeting-006: 85K-95K tokens (triggers 2-3 splits)

### Step 2: Design Topic Domains
- meeting-004: Engineering Sprint Planning (technical context)
- meeting-005: Product Roadmap Review (business context)
- meeting-006: Quarterly All-Hands (mixed context)

### Step 3: Create Speaker Rosters
Define realistic speaker sets for each meeting type.

### Step 4: Plan Agenda Structure
Create realistic meeting agendas that naturally generate the required content length.

### Step 5: Estimate Entity Distribution
Project expected counts for: speakers, topics, action items, decisions, questions.

---

## Dependencies

### Depends On
- None (first task in EN-017)

### Blocks
- TASK-141, TASK-142, TASK-143 (transcript creation)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | Token targets in enabler file |
| AC-2 | Topic rationale documented |
| AC-3 | Speaker rosters in enabler file |
| AC-4 | Entity distribution table |
| AC-5 | Agenda outlines documented |
| AC-6 | EN-017 updated with design |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
| 2026-01-28 | Claude | DONE: Added detailed meeting agendas to EN-017 enabler. Token targets (25K/45K/90K), speaker rosters with IDs, entity distribution targets, agenda timelines with topic breakdowns, and VTT generation guidelines. |
