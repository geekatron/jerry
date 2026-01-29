# Task: TASK-142 - Create meeting-005-roadmap-review.vtt

> **Task ID:** TASK-142
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-017-large-transcript-dataset](./EN-017-large-transcript-dataset.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Create a ~90-minute product roadmap review transcript with approximately 45K tokens. This transcript tests single-split behavior (exceeds 31.5K soft limit but stays under 70K).

---

## Acceptance Criteria

- [ ] **AC-1:** Duration approximately 90 minutes
- [ ] **AC-2:** Token count between 42K-48K tokens
- [ ] **AC-3:** Valid W3C WebVTT format
- [ ] **AC-4:** Contains 7 speakers (VP Product, 3 PMs, 2 Eng Leads, Designer)
- [ ] **AC-5:** Contains 4-5 distinct topics
- [ ] **AC-6:** Contains 10-15 action items
- [ ] **AC-7:** Contains 4-6 decisions
- [ ] **AC-8:** Contains 8-12 questions
- [ ] **AC-9:** File saved to `skills/transcript/test_data/input/meeting-005-roadmap-review.vtt`
- [ ] **AC-10:** Expected to trigger 1 file split

---

## Technical Specifications

### Token Target
- **Target:** ~45,000 tokens
- **Range:** 42,000 - 48,000 tokens
- **Words needed:** ~15,000 words
- **Expected splits:** 1 (at semantic ## boundary)

### Speaker Roster

| Speaker | Role | Contribution % |
|---------|------|----------------|
| Rachel | VP Product (Facilitator) | 25% |
| Tom | Product Manager - Platform | 15% |
| Sarah | Product Manager - Mobile | 15% |
| Mike | Product Manager - Enterprise | 15% |
| Dan | Engineering Lead - Backend | 10% |
| Alex | Engineering Lead - Frontend | 10% |
| Kim | UX Designer | 10% |

### Agenda Structure

1. **Q4 Retrospective (20 min)** - Review last quarter achievements
2. **Market Analysis (15 min)** - Competitive landscape update
3. **Q1 Priorities (25 min)** - Key initiatives discussion
4. **Resource Allocation (15 min)** - Team capacity planning
5. **Timeline & Milestones (15 min)** - Key dates and dependencies

### Expected Entities

| Entity Type | Expected Count |
|-------------|----------------|
| Speakers | 7 |
| Topics | 4-5 |
| Action Items | 10-15 |
| Decisions | 4-6 |
| Questions | 8-12 |

---

## Unit of Work

### Step 1: Create VTT Header
```
WEBVTT

NOTE Duration: ~90 minutes
NOTE Token Target: ~45,000
NOTE Topic: Product Roadmap Review
NOTE Expected Splits: 1
```

### Step 2: Write Q4 Retrospective Section (~3,000 words)
- Review shipped features
- Discuss customer feedback
- Analyze metrics

### Step 3: Write Market Analysis Section (~2,500 words)
- Competitive updates
- Market trends
- Customer research insights

### Step 4: Write Q1 Priorities Section (~4,500 words)
- Initiative proposals
- Technical feasibility discussions
- Priority debates

### Step 5: Write Resource Allocation Section (~2,500 words)
- Team capacity review
- Cross-team dependencies
- Hiring needs

### Step 6: Write Timeline Section (~2,500 words)
- Milestone planning
- Risk identification
- Commitment discussions

### Step 7: Validate Format & Split Behavior
- Run through ts-parser
- Verify token count exceeds soft limit
- Verify single split expected

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
| AC-1-2 | TokenCounter output showing ~45K tokens |
| AC-3 | ts-parser validation passes |
| AC-4-8 | ts-extractor entity counts |
| AC-9 | File exists at specified path |
| AC-10 | TokenCounter indicates 1 split required |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
