# Task: TASK-141 - Create meeting-004-sprint-planning.vtt

> **Task ID:** TASK-141
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-017-large-transcript-dataset](./EN-017-large-transcript-dataset.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Create a ~45-minute sprint planning transcript with approximately 25K tokens. This transcript tests behavior NEAR the soft limit (31.5K) without triggering a split.

---

## Acceptance Criteria

- [ ] **AC-1:** Duration approximately 45 minutes
- [ ] **AC-2:** Token count between 22K-28K tokens
- [ ] **AC-3:** Valid W3C WebVTT format
- [ ] **AC-4:** Contains 6 speakers (Scrum Master, 4 Engineers, PO)
- [ ] **AC-5:** Contains 3-4 distinct topics
- [ ] **AC-6:** Contains 8-12 action items
- [ ] **AC-7:** Contains 2-3 decisions
- [ ] **AC-8:** Contains 5-8 questions
- [ ] **AC-9:** File saved to `skills/transcript/test_data/input/meeting-004-sprint-planning.vtt`

---

## Technical Specifications

### Token Target
- **Target:** ~25,000 tokens
- **Range:** 22,000 - 28,000 tokens
- **Words needed:** ~8,000 words (using formula: words × 1.3 × 1.1)

### Speaker Roster

| Speaker | Role | Contribution % |
|---------|------|----------------|
| Sam | Scrum Master (Facilitator) | 20% |
| Emily | Senior Engineer | 20% |
| Jake | Backend Engineer | 15% |
| Maria | Frontend Engineer | 15% |
| Chris | QA Engineer | 15% |
| Lisa | Product Owner | 15% |

### Agenda Structure

1. **Sprint Review (10 min)** - Review completed work
2. **Backlog Grooming (15 min)** - Prioritize upcoming work
3. **Capacity Planning (10 min)** - Estimate team capacity
4. **Sprint Commitment (10 min)** - Commit to sprint goals

### Expected Entities

| Entity Type | Expected Count |
|-------------|----------------|
| Speakers | 6 |
| Topics | 3-4 |
| Action Items | 8-12 |
| Decisions | 2-3 |
| Questions | 5-8 |

---

## Unit of Work

### Step 1: Create VTT Header
```
WEBVTT

NOTE Duration: ~45 minutes
NOTE Token Target: ~25,000
NOTE Topic: Sprint Planning
```

### Step 2: Write Sprint Review Section (~2,500 words)
- Demo completed features
- Discuss blockers resolved
- Review metrics

### Step 3: Write Backlog Grooming Section (~2,500 words)
- Review prioritized backlog
- Discuss technical complexity
- Estimate story points

### Step 4: Write Capacity Planning Section (~1,500 words)
- Review team availability
- Account for PTO/meetings
- Calculate capacity

### Step 5: Write Sprint Commitment Section (~1,500 words)
- Commit to sprint goals
- Assign action items
- Set next meeting

### Step 6: Validate Format
- Run through ts-parser
- Verify token count
- Check entity extraction

---

## Dependencies

### Depends On
- TASK-140 (Dataset Design)

### Blocks
- TASK-144 (Dataset Validation)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1-2 | TokenCounter output showing ~25K tokens |
| AC-3 | ts-parser validation passes |
| AC-4-8 | ts-extractor entity counts |
| AC-9 | File exists at specified path |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
